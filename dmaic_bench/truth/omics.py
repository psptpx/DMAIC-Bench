"""Reference implementations for the second-domain portability pilot (RNA-seq and GWAS).

Same contract as :mod:`dmaic_bench.truth.verifiers`: each function takes ONE released batch
payload (a dict) and returns a flat dict of canonical outputs. numpy + scipy only, no solver,
no R, no Bioconductor -- every number here is something a contestant can reproduce inside the
pinned agent image, which is the whole point of a truth layer.

Two workflows, chosen because each has textbook preconditions with published thresholds:

* **bulk RNA-seq differential expression.** Before any gene is called responsive, (i) each
  condition needs enough usable replicates (Schurch et al. 2016 RNA 22:839; Conesa et al.
  2016 Genome Biol 17:13), and (ii) the comparison of interest must be estimable separately
  from library batch -- a design in which every batch holds one condition is not full rank
  (DESeq2 vignette, "Model matrix not full rank"; Leek et al. 2010 Nat Rev Genet 11:733;
  Gilad & Mizrahi-Man 2015 F1000Res 4:121). Where batch structure exists but is estimable,
  the batch term belongs in the model.
* **case-control genotype association.** Before any variant is called associated, samples
  and variants are filtered on call rate, minor-allele frequency and Hardy-Weinberg
  (Anderson et al. 2010 Nat Protoc 5:1564; Marees et al. 2018 Int J Methods Psychiatr Res
  27:e1608), and the cohort is checked for population structure: a cohort whose cases and
  controls are drawn from different ancestries cannot support a case-control comparison at
  all, and one with partial structure needs the leading principal components as covariates
  (Price et al. 2006 Nat Genet 38:904).
"""
from __future__ import annotations

import math

import numpy as np
from scipy import stats



def _nv(msg):
    """verifiers.NotVerifiable, resolved at call time: verifiers imports this module at its
    end to register these implementations, so a top-level import here would be circular."""
    from dmaic_bench.truth import verifiers as _v
    return _v.NotVerifiable(msg)


# --------------------------------------------------------------------------- helpers

def _num(v, default=None):
    if isinstance(v, bool):
        return default
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError:
            return default
    return default


def _bh(p):
    """Benjamini-Hochberg adjusted p-values (monotone, capped at 1)."""
    p = np.asarray(p, dtype=float)
    n = p.size
    if n == 0:
        return p
    order = np.argsort(p)
    ranked = p[order] * n / (np.arange(n) + 1.0)
    ranked = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.minimum(ranked, 1.0)
    return out


def _samples_table(payload):
    rows = payload.get("samples") if isinstance(payload, dict) else None
    if not isinstance(rows, (list, tuple)) or not rows or not isinstance(rows[0], dict):
        raise _nv("samples must be a list of row dicts")
    return list(rows)


def _rules(payload, **defaults):
    rules = payload.get("qcRules") if isinstance(payload, dict) else None
    rules = rules if isinstance(rules, dict) else {}
    out = {}
    for k, d in defaults.items():
        out[k] = _num(rules.get(k), d)
    return out


# =========================================================================== RNA-seq

def rna_sample_qc(payload):
    """Library QC over the sample sheet: which libraries are usable, and how many replicates
    each condition keeps. A library fails on too few assigned reads or too low a mapping rate."""
    rows = _samples_table(payload)
    r = _rules(payload, minAssignedReads=5.0e6, minMappingRate=0.70)
    failed, kept = 0, {}
    for row in rows:
        reads = _num(row.get("assignedReads"), 0.0)
        rate = _num(row.get("mappingRate"), 0.0)
        cond = str(row.get("condition"))
        kept.setdefault(cond, 0)
        if reads < r["minAssignedReads"] or rate < r["minMappingRate"]:
            failed += 1
        else:
            kept[cond] += 1
    return {"failedSamples": float(failed),
            "passedSamples": float(len(rows) - failed),
            "minReplicates": float(min(kept.values())) if kept else 0.0}


def design_identifiability(payload):
    """Is the condition contrast estimable separately from library batch?

    Builds the model matrix [intercept, condition, batch dummies] over the sample sheet and
    reports whether it is full rank. For a two-level condition that is exactly the question
    "does any batch hold both conditions?": when every batch holds one condition only, the
    condition column is a linear combination of the batch columns and no model can separate
    them. `batchCount` is the number of distinct batches; a single batch has no batch term to
    fit and none to adjust for.
    """
    rows = _usable_rows(payload)
    conds = sorted({str(r.get("condition")) for r in rows})
    batches = sorted({str(r.get("batch")) for r in rows})
    if len(conds) != 2:
        raise _nv("design check expects exactly two conditions among usable libraries")
    n = len(rows)
    cols = [np.ones(n), np.array([1.0 if str(r.get("condition")) == conds[1] else 0.0
                                  for r in rows])]
    for b in batches[1:]:
        cols.append(np.array([1.0 if str(r.get("batch")) == b else 0.0 for r in rows]))
    x = np.column_stack(cols)
    rank = int(np.linalg.matrix_rank(x))
    confounded = 1.0 if rank < x.shape[1] else 0.0
    return {"confounded": confounded, "batchCount": float(len(batches)),
            "designRank": float(rank), "designColumns": float(x.shape[1]),
            "usableSamples": float(n)}


def _usable_rows(payload):
    """The sample sheet restricted to libraries that pass the QC rules -- when the sheet
    carries the metrics and the rules. A design is a property of the libraries that will be
    analysed, not of the ones that were planned: a balanced plan whose failed libraries all
    sit in one arm of one batch is confounded once they are dropped (seed 6)."""
    rows = _samples_table(payload)
    if not any("assignedReads" in r or "mappingRate" in r for r in rows):
        return rows
    r = _rules(payload, minAssignedReads=5.0e6, minMappingRate=0.70)
    keep = [row for row in rows
            if _num(row.get("assignedReads"), 0.0) >= r["minAssignedReads"]
            and _num(row.get("mappingRate"), 0.0) >= r["minMappingRate"]]
    if not keep:
        raise _nv("no usable libraries")
    return keep


def _count_matrix(payload):
    counts = payload.get("counts") if isinstance(payload, dict) else None
    if not isinstance(counts, (list, tuple)) or not counts:
        raise _nv("counts must be a gene x sample matrix")
    m = np.asarray(counts, dtype=float)
    if m.ndim != 2 or m.shape[1] < 4:
        raise _nv("counts must be 2-D with >= 4 samples")
    cond = payload.get("condition")
    batch = payload.get("batch")
    if not isinstance(cond, (list, tuple)) or len(cond) != m.shape[1]:
        raise _nv("condition must label every sample column")
    cond = [str(c) for c in cond]
    batch = [str(b) for b in batch] if isinstance(batch, (list, tuple)) and \
        len(batch) == m.shape[1] else ["B1"] * m.shape[1]
    return m, cond, batch


def _log_cpm(m):
    lib = m.sum(axis=0)
    lib[lib <= 0] = 1.0
    return np.log2(m / lib * 1.0e6 + 1.0)


def _thresholds(payload):
    return (_num(payload.get("padjThreshold"), 0.05) if isinstance(payload, dict) else 0.05,
            _num(payload.get("log2fcThreshold"), 1.0) if isinstance(payload, dict) else 1.0)


def _levels(payload, cond):
    declared = payload.get("conditions") if isinstance(payload, dict) else None
    if isinstance(declared, (list, tuple)) and len(declared) == 2:
        return str(declared[0]), str(declared[1])
    lv = sorted(set(cond))
    if len(lv) != 2:
        raise _nv("expected exactly two conditions")
    return lv[0], lv[1]


def batch_assessment(payload):
    """How much of the leading axis of expression variation is explained by library batch.

    PCA on centred log2-CPM (samples as observations), then the one-way R^2 of PC1 scores on
    batch. A fraction near 1 says the first thing the data varies by is the batch.
    """
    m, _cond, batch = _count_matrix(payload)
    x = _log_cpm(m).T                                # samples x genes
    x = x - x.mean(axis=0, keepdims=True)
    _u, s, vt = np.linalg.svd(x, full_matrices=False)
    pc1 = x @ vt[0]
    total = float(np.sum((pc1 - pc1.mean()) ** 2))
    between = 0.0
    for b in sorted(set(batch)):
        idx = [i for i, v in enumerate(batch) if v == b]
        between += len(idx) * (pc1[idx].mean() - pc1.mean()) ** 2
    frac = float(between / total) if total > 0 else 0.0
    return {"batchVarianceFraction": frac,
            "pc1VarianceFraction": float(s[0] ** 2 / np.sum(s ** 2)),
            "batchCount": float(len(set(batch)))}


def de_simple(payload):
    """Two-group differential expression on log2-CPM: Welch t per gene, BH adjustment, a gene
    is called when padj < threshold and |log2FC| >= threshold. log2FC is level[1] - level[0]."""
    m, cond, _batch = _count_matrix(payload)
    a, b = _levels(payload, cond)
    x = _log_cpm(m)
    ia = [i for i, c in enumerate(cond) if c == a]
    ib = [i for i, c in enumerate(cond) if c == b]
    if len(ia) < 2 or len(ib) < 2:
        raise _nv("each condition needs >= 2 samples")
    t, p = stats.ttest_ind(x[:, ib], x[:, ia], axis=1, equal_var=False)
    p = np.nan_to_num(np.asarray(p, dtype=float), nan=1.0)
    lfc = x[:, ib].mean(axis=1) - x[:, ia].mean(axis=1)
    padj = _bh(p)
    pt, lt = _thresholds(payload)
    sig = (padj < pt) & (np.abs(lfc) >= lt)
    return {"nSignificant": float(int(sig.sum())), "nTested": float(x.shape[0]),
            "nUp": float(int((sig & (lfc > 0)).sum())),
            "nDown": float(int((sig & (lfc < 0)).sum()))}


def de_blocked(payload):
    """Differential expression with batch in the model: per gene, OLS of log2-CPM on
    intercept + condition + batch dummies; t-test on the condition coefficient; BH; same call
    rule as :func:`de_simple`. Raises when the design is not full rank -- the batch term
    cannot be fitted on a confounded design, and that is the answer, not a number."""
    m, cond, batch = _count_matrix(payload)
    a, b = _levels(payload, cond)
    x = _log_cpm(m).T                                # samples x genes
    n = x.shape[0]
    cols = [np.ones(n), np.array([1.0 if c == b else 0.0 for c in cond])]
    for lv in sorted(set(batch))[1:]:
        cols.append(np.array([1.0 if v == lv else 0.0 for v in batch]))
    d = np.column_stack(cols)
    p_cols = d.shape[1]
    if np.linalg.matrix_rank(d) < p_cols:
        raise _nv("design is not full rank: condition is confounded with batch")
    if n - p_cols < 1:
        raise _nv("no residual degrees of freedom")
    xtx_inv = np.linalg.inv(d.T @ d)
    beta = xtx_inv @ d.T @ x                          # p x genes
    resid = x - d @ beta
    df = n - p_cols
    sigma2 = (resid ** 2).sum(axis=0) / df
    se = np.sqrt(np.maximum(sigma2 * xtx_inv[1, 1], 1e-300))
    tval = beta[1] / se
    pval = 2.0 * stats.t.sf(np.abs(tval), df)
    padj = _bh(pval)
    pt, lt = _thresholds(payload)
    sig = (padj < pt) & (np.abs(beta[1]) >= lt)
    return {"nSignificant": float(int(sig.sum())), "nTested": float(x.shape[1]),
            "batchTermCount": float(p_cols - 2), "residualDf": float(df)}


# =========================================================================== GWAS

def _genotype_matrix(payload):
    g = payload.get("genotypes") if isinstance(payload, dict) else None
    if not isinstance(g, (list, tuple)) or not g:
        raise _nv("genotypes must be a sample x variant matrix")
    m = np.array([[np.nan if v is None else float(v) for v in row] for row in g], dtype=float)
    if m.ndim != 2 or m.shape[0] < 10 or m.shape[1] < 5:
        raise _nv("genotype matrix too small")
    pheno = payload.get("phenotype")
    if not isinstance(pheno, (list, tuple)) or len(pheno) != m.shape[0]:
        raise _nv("phenotype must label every sample row")
    y = np.array([1.0 if _num(v, 0.0) >= 0.5 else 0.0 for v in pheno])
    return m, y


def _gwas_rules(payload):
    return _rules(payload, minSampleCallRate=0.95, minVariantCallRate=0.95,
                  minMaf=0.01, minHwePControls=1.0e-6, alpha=0.05)


def _sample_keep(m, r):
    call = 1.0 - np.isnan(m).mean(axis=1)
    return call >= r["minSampleCallRate"], call


def gwas_sample_qc(payload):
    """Per-sample call rate against the published threshold."""
    m, _y = _genotype_matrix(payload)
    r = _gwas_rules(payload)
    keep, call = _sample_keep(m, r)
    failed = int((~keep).sum())
    return {"samplesFailed": float(failed), "sampleFailFraction": float(failed / m.shape[0]),
            "samplesRetained": float(int(keep.sum())),
            "minSampleCallRate": float(call.min())}


def _hwe_p(gen):
    """Chi-square HWE test (1 df) on the genotype counts of one variant."""
    gen = gen[~np.isnan(gen)]
    n = gen.size
    if n < 5:
        return 1.0
    n_aa = float((gen == 0).sum()); n_ab = float((gen == 1).sum()); n_bb = float((gen == 2).sum())
    p = (2 * n_bb + n_ab) / (2.0 * n)
    if p <= 0 or p >= 1:
        return 1.0
    exp = np.array([n * (1 - p) ** 2, n * 2 * p * (1 - p), n * p ** 2])
    obs = np.array([n_aa, n_ab, n_bb])
    chi2 = float(np.sum((obs - exp) ** 2 / np.maximum(exp, 1e-12)))
    return float(stats.chi2.sf(chi2, 1))


def _variant_keep(m, y, r):
    """Boolean mask of variants passing call rate, MAF and HWE-in-controls on QC-passed samples."""
    keep_s, _ = _sample_keep(m, r)
    ms = m[keep_s]
    ys = y[keep_s]
    call = 1.0 - np.isnan(ms).mean(axis=0)
    freq = np.nanmean(ms, axis=0) / 2.0
    maf = np.minimum(freq, 1.0 - freq)
    hwe = np.array([_hwe_p(ms[ys == 0, j]) for j in range(ms.shape[1])])
    keep_v = (call >= r["minVariantCallRate"]) & (maf >= r["minMaf"]) & \
        (hwe >= r["minHwePControls"])
    return keep_s, keep_v


def gwas_snp_qc(payload):
    m, y = _genotype_matrix(payload)
    r = _gwas_rules(payload)
    keep_s, keep_v = _variant_keep(m, y, r)
    return {"snpsFailed": float(int((~keep_v).sum())),
            "snpsRetained": float(int(keep_v.sum())),
            "samplesRetained": float(int(keep_s.sum()))}


def _pcs(m, k=2):
    """Leading PC scores of the standardised, mean-imputed genotype matrix (samples x k)."""
    x = m.copy()
    freq = np.nanmean(x, axis=0) / 2.0
    for j in range(x.shape[1]):
        col = x[:, j]
        col[np.isnan(col)] = 2.0 * freq[j]
    sd = np.sqrt(np.maximum(2.0 * freq * (1.0 - freq), 1e-12))
    x = (x - 2.0 * freq) / sd
    x = x - x.mean(axis=0, keepdims=True)
    u, s, _vt = np.linalg.svd(x, full_matrices=False)
    scores = u[:, :k] * s[:k]
    return scores, s


def gwas_stratification(payload):
    """Population structure on the QC-passed cohort: PC1 of the standardised genotype matrix,
    whether cases and controls occupy disjoint ranges of it, and the Welch p-value for a shift
    in PC1 between cases and controls. Sign and scale of the PC are irrelevant to both."""
    m, y = _genotype_matrix(payload)
    r = _gwas_rules(payload)
    keep_s, keep_v = _variant_keep(m, y, r)
    x = m[keep_s][:, keep_v]
    ys = y[keep_s]
    scores, s = _pcs(x, 2)
    if (ys == 1).sum() < 2 or (ys == 0).sum() < 2:
        raise _nv("need cases and controls")
    # Disjoint ranges on EITHER leading axis: a balanced site or ancestry split can own PC1
    # while the status-aligned ancestry difference sits on PC2 (seed 6). The headline axis
    # then says "no separation" and the cohort is still two ancestries.
    axis = 0.0
    pvals = []
    for k in range(2):
        pc = scores[:, k]
        cases, ctrls = pc[ys == 1], pc[ys == 0]
        _t, p = stats.ttest_ind(cases, ctrls, equal_var=False)
        pvals.append(float(p))
        if axis == 0.0 and (cases.max() < ctrls.min() or ctrls.max() < cases.min()):
            axis = float(k + 1)
    return {"separated": 1.0 if axis else 0.0, "separatedAxis": axis,
            "pc1PValue": pvals[0], "pc2PValue": pvals[1],
            "pc1VarianceFraction": float(s[0] ** 2 / np.sum(s ** 2))}


def _bonferroni(r, m_tests):
    return r["alpha"] / max(m_tests, 1)


def gwas_association_trend(payload):
    """Cochran-Armitage trend test per QC-passed variant (chi-square = N * r^2 between genotype
    dosage and status), Bonferroni over the tested variants, genomic-control lambda."""
    m, y = _genotype_matrix(payload)
    r = _gwas_rules(payload)
    keep_s, keep_v = _variant_keep(m, y, r)
    x = m[keep_s][:, keep_v]
    ys = y[keep_s]
    chi = []
    for j in range(x.shape[1]):
        col = x[:, j]
        ok = ~np.isnan(col)
        g, yy = col[ok], ys[ok]
        if g.size < 10 or np.std(g) == 0 or np.std(yy) == 0:
            chi.append(0.0)
            continue
        rho = float(np.corrcoef(g, yy)[0, 1])
        chi.append(g.size * rho * rho)
    chi = np.asarray(chi)
    p = stats.chi2.sf(chi, 1)
    thr = _bonferroni(r, x.shape[1])
    lam = float(np.median(chi) / 0.4549364) if chi.size else 1.0
    return {"nSignificant": float(int((p < thr).sum())), "nTested": float(x.shape[1]),
            "lambdaGC": lam, "minPValue": float(p.min()) if p.size else 1.0}


def _logit_wald(design, y, col):
    """Wald z for column *col* of a logistic regression fitted by IRLS."""
    beta = np.zeros(design.shape[1])
    for _ in range(50):
        eta = design @ beta
        mu = 1.0 / (1.0 + np.exp(-eta))
        w = mu * (1.0 - mu)
        if np.all(w < 1e-10):
            break
        xtw = design.T * w
        try:
            h = np.linalg.inv(xtw @ design + 1e-9 * np.eye(design.shape[1]))
        except np.linalg.LinAlgError:
            return 0.0
        step = h @ (design.T @ (y - mu))
        beta = beta + step
        if np.max(np.abs(step)) < 1e-8:
            break
    eta = design @ beta
    mu = 1.0 / (1.0 + np.exp(-eta))
    w = mu * (1.0 - mu)
    h = np.linalg.inv((design.T * w) @ design + 1e-9 * np.eye(design.shape[1]))
    se = math.sqrt(max(h[col, col], 1e-300))
    return float(beta[col] / se)


def gwas_association_adjusted(payload):
    """Logistic regression of status on genotype dosage with PC1 and PC2 as covariates, per
    QC-passed variant; Wald test on the genotype term; Bonferroni; lambda from the Wald
    chi-squares."""
    m, y = _genotype_matrix(payload)
    r = _gwas_rules(payload)
    keep_s, keep_v = _variant_keep(m, y, r)
    x = m[keep_s][:, keep_v]
    ys = y[keep_s]
    pcs, _s = _pcs(x, 2)
    chi = []
    for j in range(x.shape[1]):
        col = x[:, j]
        ok = ~np.isnan(col)
        if ok.sum() < 10 or np.std(col[ok]) == 0:
            chi.append(0.0)
            continue
        d = np.column_stack([np.ones(int(ok.sum())), col[ok], pcs[ok, 0], pcs[ok, 1]])
        z = _logit_wald(d, ys[ok], 1)
        chi.append(z * z)
    chi = np.asarray(chi)
    p = stats.chi2.sf(chi, 1)
    thr = _bonferroni(r, x.shape[1])
    lam = float(np.median(chi) / 0.4549364) if chi.size else 1.0
    return {"nSignificant": float(int((p < thr).sum())), "nTested": float(x.shape[1]),
            "lambdaGC": lam, "covariateCount": 2.0,
            "minPValue": float(p.min()) if p.size else 1.0}


# --------------------------------------------------------------------------- late-stage steps

def validation_concordance(payload):
    """Independent qPCR validation of the nominated candidates: per gene, Welch t on log2
    expression between arms; a candidate is confirmed at p < alpha with the direction the
    panel called. `concordance` is confirmed / nominated."""
    genes = payload.get("genes") if isinstance(payload, dict) else None
    qpcr = payload.get("qpcr") if isinstance(payload, dict) else None
    direction = payload.get("expectedDirection") if isinstance(payload, dict) else None
    if not isinstance(genes, (list, tuple)) or not genes or not isinstance(qpcr, dict):
        raise _nv("validation needs nominated genes with qPCR values")
    r = _rules(payload, alpha=0.05, minConcordance=0.75)
    confirmed = 0
    for g in genes:
        block = qpcr.get(g) or {}
        a = np.asarray(block.get("control") or [], dtype=float)
        b = np.asarray(block.get("treated") or [], dtype=float)
        if a.size < 2 or b.size < 2:
            continue
        _t, p = stats.ttest_ind(b, a, equal_var=False)
        want = str((direction or {}).get(g, "")).lower()
        sign = "up" if b.mean() > a.mean() else "down"
        if p < r["alpha"] and (not want or want == sign):
            confirmed += 1
    return {"concordance": float(confirmed / len(genes)), "nConfirmed": float(confirmed),
            "nTested": float(len(genes))}


def enrichment(payload):
    """Over-representation of the called genes in annotated sets: hypergeometric upper tail
    per set, BH across sets, significant at padj < alpha. `calledGenes` is the list the
    caller supplies (the generator passes the reference calls; the oracle its own)."""
    sets = payload.get("sets") if isinstance(payload, dict) else None
    called = payload.get("calledGenes") if isinstance(payload, dict) else None
    universe = int(_num(payload.get("universe"), 0.0) or 0) if isinstance(payload, dict) else 0
    if not isinstance(sets, dict) or not sets or not isinstance(called, (list, tuple)):
        raise _nv("enrichment needs gene sets and the called genes")
    r = _rules(payload, alpha=0.05)
    called_set = set(map(str, called))
    if universe <= 0:
        universe = len({g for members in sets.values() for g in members} | called_set)
    n = len(called_set)
    pv = []
    for members in sets.values():
        m = set(map(str, members))
        k = len(m & called_set)
        pv.append(float(stats.hypergeom.sf(k - 1, universe, len(m), n)) if n else 1.0)
    padj = _bh(np.asarray(pv))
    return {"nSignificantSets": float(int((padj < r["alpha"]).sum())),
            "nSets": float(len(sets)), "nCalled": float(n)}


def gwas_replication(payload):
    """Replication of the nominated discovery variants in an independent cohort: trend test
    per candidate, replicated at p < alpha with the discovery direction."""
    m, y = _genotype_matrix(payload)
    r = _rules(payload, alpha=0.05)
    variants = [str(v) for v in (payload.get("variants") or [])]
    cands = [str(v) for v in (payload.get("candidateVariants") or [])]
    direction = payload.get("discoveryDirection") or {}
    if not cands:
        raise _nv("no candidate variants nominated")
    rep = 0
    for v in cands:
        if v not in variants:
            continue
        col = m[:, variants.index(v)]
        ok = ~np.isnan(col)
        g, yy = col[ok], y[ok]
        if g.size < 10 or np.std(g) == 0 or np.std(yy) == 0:
            continue
        rho = float(np.corrcoef(g, yy)[0, 1])
        p = float(stats.chi2.sf(g.size * rho * rho, 1))
        want = _num(direction.get(v), 0.0) or 0.0
        if p < r["alpha"] and (want == 0.0 or np.sign(rho) == np.sign(want)):
            rep += 1
    return {"nReplicated": float(rep), "nCandidates": float(len(cands)),
            "replicationFraction": float(rep / len(cands))}


def gwas_effect_estimate(payload):
    """Per-allele odds ratio with a 95% Wald interval for the first replicated candidate, by
    logistic regression on the replication cohort."""
    m, y = _genotype_matrix(payload)
    variants = [str(v) for v in (payload.get("variants") or [])]
    cands = [str(v) for v in (payload.get("candidateVariants") or [])]
    r = _rules(payload, alpha=0.05)
    direction = payload.get("discoveryDirection") or {}
    for v in cands:
        if v not in variants:
            continue
        col = m[:, variants.index(v)]
        ok = ~np.isnan(col)
        g, yy = col[ok], y[ok]
        if g.size < 10 or np.std(g) == 0:
            continue
        rho = float(np.corrcoef(g, yy)[0, 1])
        p = float(stats.chi2.sf(g.size * rho * rho, 1))
        want = _num(direction.get(v), 0.0) or 0.0
        if not (p < r["alpha"] and (want == 0.0 or np.sign(rho) == np.sign(want))):
            continue
        d = np.column_stack([np.ones(g.size), g])
        beta = np.zeros(2)
        for _ in range(50):
            mu = 1.0 / (1.0 + np.exp(-(d @ beta)))
            w = mu * (1.0 - mu)
            h = np.linalg.inv((d.T * w) @ d + 1e-9 * np.eye(2))
            step = h @ (d.T @ (yy - mu))
            beta = beta + step
            if np.max(np.abs(step)) < 1e-8:
                break
        mu = 1.0 / (1.0 + np.exp(-(d @ beta)))
        w = mu * (1.0 - mu)
        se = math.sqrt(max(np.linalg.inv((d.T * w) @ d + 1e-9 * np.eye(2))[1, 1], 1e-300))
        return {"oddsRatio": float(math.exp(beta[1])),
                "ciLower": float(math.exp(beta[1] - 1.959964 * se)),
                "ciUpper": float(math.exp(beta[1] + 1.959964 * se)),
                "variant": v}
    raise _nv("no replicated candidate to estimate")


OMICS_IMPLS = {
    "expression.validation_concordance": validation_concordance,
    "expression.enrichment": enrichment,
    "gwas.replication": gwas_replication,
    "gwas.effect_estimate": gwas_effect_estimate,
    "qc.sample_qc": rna_sample_qc,
    "design.identifiability": design_identifiability,
    "expression.batch_assessment": batch_assessment,
    "expression.de_simple": de_simple,
    "expression.de_blocked": de_blocked,
    "gwas.sample_qc": gwas_sample_qc,
    "gwas.snp_qc": gwas_snp_qc,
    "gwas.stratification": gwas_stratification,
    "gwas.association_trend": gwas_association_trend,
    "gwas.association_adjusted": gwas_association_adjusted,
}
