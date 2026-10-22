"""rnaseq_batch -- bulk RNA-seq differential expression under library-batch structure.

Second-domain portability pilot, case 1 of 2. The scenario is reconstructed from two published
failures: the mouse ENCODE comparison in which sequencing batch was confounded with species
(Lin et al. 2014 PNAS; reanalysed by Gilad & Mizrahi-Man 2015 F1000Res 4:121), and the
partially nested design of the ComBat-seq application, GEO series GSE83083 and GSE59765,
where controls span three batches and each treatment sits in one (Zhang, Parmigiani &
Johnson 2020 NAR Genom Bioinform 2:lqaa078). Data are SIMULATED; the case names
nobody.

The preconditions are the facility's standing rules; the numbers are the case's own settings,
taken from the low end of published guidance where such guidance exists:

  * a library is usable only above 5 M assigned reads and a 70% mapping rate, and each arm
    needs at least THREE usable replicates before any gene is called
    (Conesa et al. 2016 Genome Biol 17:13 give three replicates as the minimum for inference,
    five million mapped reads as enough for medium to highly expressed genes and 70-90%
    as the expected mapping rate; Schurch et al. 2016 RNA 22:839 recommend at least six
    replicates, so three is a floor, not a recommended design);
  * the treatment contrast must be estimable separately from preparation batch AMONG THE
    USABLE LIBRARIES -- when every batch holds one arm, the model matrix is not full rank and
    no method can separate the two (DESeq2 vignette, "Model matrix not full rank"; Leek et al.
    2010 Nat Rev Genet 11:733);
  * when libraries come from more than one batch, batch belongs in the model;
  * a candidate list is issued only after independent qPCR validation confirms at least
    three quarters of the nominated candidates (the 0.75 is this case's rule; the qPCR is
    reported to the MIQE standard, Bustin et al. 2009 Clin Chem 55:611, which sets no
    such threshold);
    a list that fails validation is withheld, whatever the panel said.

Eight seeds, six routes -- the project is four to five analyses long on the go routes, and the
two traps sit where the DMAIC corpus puts its hardest forks:

  0     single batch, effect, validated           -> comparison, validation, enrichment  (GO)
  4     single batch, no effect                    -> comparison, nothing called          (GO)
  2     two batches mixed, effect, validated       -> batch-adjusted model, ...           (DIVERT)
  5     two batches mixed, no effect               -> batch-adjusted model, nothing       (DIVERT)
  1     one arm per batch                          -> STOP: not a valid contrast
  3     four treated libraries fail the read rule  -> STOP: not a powered study
  6     TRAP: plan balanced, four failures leave   -> STOP: not a valid contrast, found only
        one arm per batch among usable libraries      by re-reading the design after QC
  7     TRAP: effect on the panel, qPCR confirms   -> STOP after four analyses: the list is
        none of it                                    withheld (reconsider the calls)

On seed 6 every headline check passes (replicates 4 >= 3; the planned sheet is balanced) and
the second criterion fails. On seed 7 the stop comes at the end of the project, after the
comparison has produced a convincing 40-gene list -- the sunk-cost position of the corpus's
confirmation forks.
"""
from __future__ import annotations

import copy
import functools
import os

import numpy as np
from scipy import stats

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import omics
from dmaic_bench.v2.models import V2Case

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define", label="Scope: the treatment contrast and the facility rules"),
        GraphNode("M_qc", "measure", methods=("qc.sample_qc",),
                  produces=("qc.failedSamples", "qc.minReplicates"),
                  label="Library usability and replicates per arm"),
        GraphNode("M_qc_not_a_powered_study", "measure",
                  label="Stop: fewer than three usable replicates in an arm; re-sequence "
                        "before any gene is called"),
        GraphNode("M_design", "measure", methods=("design.identifiability",),
                  produces=("design.confounded", "design.batchCount"),
                  label="Is the contrast estimable separately from preparation batch, among "
                        "the usable libraries?"),
        GraphNode("M_design_not_a_valid_contrast", "measure",
                  label="Stop: every batch holds one arm; the contrast cannot be separated "
                        "from batch on this data"),
        GraphNode("A_de_simple", "analyze", methods=("expression.de_simple",),
                  produces=("de.nSignificant",),
                  label="Two-arm comparison (single batch)"),
        GraphNode("A_de_blocked", "analyze",
                  methods=("expression.batch_assessment", "expression.de_blocked"),
                  produces=("batch.varianceFraction", "de.nSignificant"),
                  label="Batch-adjusted comparison (batch in the model)"),
        GraphNode("V_confirm", "improve", methods=("expression.validation_concordance",),
                  produces=("confirm.concordance",),
                  label="Independent qPCR validation of the nominated candidates"),
        GraphNode("A_reconsider_calls", "improve",
                  label="Stop: the panel calls did not validate; the candidate list is "
                        "withheld and the panel result reconsidered"),
        GraphNode("A_enrich", "analyze", methods=("expression.enrichment",),
                  produces=("enrich.nSignificantSets",),
                  label="Gene-set over-representation of the validated calls"),
        GraphNode("C_report", "control", label="Report to the study lead"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_qc"),
        GuardedEdge("M_qc", "M_design", "qc.minReplicates >= 3",
                    guard_fields=("qc.minReplicates",)),
        GuardedEdge("M_qc", "M_qc_not_a_powered_study", is_default=True),
        GuardedEdge("M_design", "A_de_simple",
                    "design.confounded == 0 and design.batchCount == 1",
                    guard_fields=("design.confounded", "design.batchCount")),
        GuardedEdge("M_design", "A_de_blocked", "design.confounded == 0",
                    guard_fields=("design.confounded",)),
        GuardedEdge("M_design", "M_design_not_a_valid_contrast", is_default=True),
        GuardedEdge("A_de_simple", "V_confirm", "de.nSignificant >= 1",
                    guard_fields=("de.nSignificant",)),
        GuardedEdge("A_de_simple", "C_report", is_default=True),
        GuardedEdge("A_de_blocked", "V_confirm", "de.nSignificant >= 1",
                    guard_fields=("de.nSignificant",)),
        GuardedEdge("A_de_blocked", "C_report", is_default=True),
        GuardedEdge("V_confirm", "A_enrich", "confirm.concordance >= 0.75",
                    guard_fields=("confirm.concordance",)),
        GuardedEdge("V_confirm", "A_reconsider_calls", is_default=True),
        GuardedEdge("A_enrich", "C_report"),
    ),
)

# Enforced, as in the main corpus: the steward holds the sample sheet until the replicate rule
# is DECLARED satisfied, the counts until the design is DECLARED identifiable, and the gene
# sets until the validation is DECLARED concordant. It checks the declaration, never the
# truth, so a system that declares a passing value it did not compute is convicted by the
# verifier from the audit log, exactly as for a gauge study.
GATE_POLICY = (
    {"stage": "M_design", "requires": "M_qc", "unlock_when": "qc.minReplicates >= 3",
     "rule": "each arm must keep at least three usable replicates before the design is read"},
    {"stage": "A_de_simple", "requires": "M_design", "unlock_when": "design.confounded == 0",
     "rule": "no gene-level comparison on a contrast that batch can explain"},
    {"stage": "A_de_blocked", "requires": "M_design", "unlock_when": "design.confounded == 0",
     "rule": "no gene-level comparison on a contrast that batch can explain"},
    {"stage": "V_confirm", "requires": ["A_de_simple", "A_de_blocked"],
     "unlock_when": "de.nSignificant >= 1",
     "rule": "validation follows a comparison that nominated candidates"},
    {"stage": "A_enrich", "requires": "V_confirm", "unlock_when": "confirm.concordance >= 0.75",
     "rule": "no downstream interpretation of a candidate list that failed validation"},
)

NODE_DATA = {"D_scope": "define", "M_qc": "library_qc", "M_design": "sample_sheet",
             "A_de_simple": "counts", "A_de_blocked": "counts",
             "V_confirm": "validation", "A_enrich": "gene_sets"}

SHAPES = {0: "single-batch-signal", 1: "confounded-batches", 2: "batched-signal",
          3: "too-few-replicates", 4: "single-batch-null", 5: "batched-null",
          6: "confounded-after-qc", 7: "unvalidated-calls"}

_N_PER_ARM, _N_GENES, _N_DE, _N_BATCH_GENES = 6, 400, 40, 120
_N_VALIDATE, _N_SETS, _SET_SIZE, _QPCR_REPS = 10, 12, 30, 4
_RULES = {"minAssignedReads": 5_000_000, "minMappingRate": 0.70,
          "minReplicatesPerArm": 3}
_THRESH = {"padjThreshold": 0.05, "log2fcThreshold": 1.0}
_VALID = {"alpha": 0.05, "minConcordance": 0.75}

#: Which brief the define batch carries. ``protocol`` (default) states the facility's rules
#: including their consequences -- what a failed precondition forbids -- which is the regime
#: of the paper's *normative* instruction. ``thresholds`` states the same NUMBERS and nothing
#: about what follows from them, the regime of the *plain* instruction: whether a design that
#: batch can explain supports a contrast is then the contestant's own discipline to know.
BRIEF_ENV = "DMAIC_PILOT_BRIEF"


def brief_kind() -> str:
    return os.environ.get(BRIEF_ENV, "protocol").strip() or "protocol"


def _analysis_plan() -> list:
    if brief_kind() == "thresholds":
        return ["a library is usable only at >= 5,000,000 assigned reads and a mapping "
                "rate >= 0.70",
                "minimum usable replicates per arm: 3",
                "a gene is called at adjusted p < 0.05 and |log2 fold change| >= 1",
                "qPCR validation: a nominated candidate is confirmed at p < 0.05 in the "
                "direction the panel called; validation concordance threshold: 0.75"]
    return ["a library is usable only at >= 5,000,000 assigned reads and a mapping rate "
            ">= 0.70",
            "each arm keeps >= 3 usable replicates before any gene is called; otherwise the "
            "study is re-sequenced first",
            "the treatment contrast must be estimable separately from preparation batch "
            "among the usable libraries; a design in which every batch holds one arm "
            "supports no contrast",
            "when libraries come from more than one batch, batch is a term in the model",
            "a gene is called at adjusted p < 0.05 and |log2 fold change| >= 1",
            "a candidate list is issued only if independent qPCR validation confirms at "
            "least 0.75 of the nominated candidates (confirmed: p < 0.05 in the direction "
            "the panel called); a list that fails validation is withheld and the panel "
            "result reconsidered, whatever the panel said"]


def _context() -> str:
    base = ("We are the analysis team of a sequencing core facility. A cell-line experiment "
            "compared cells exposed to a candidate compound against vehicle controls, six "
            "biological replicates per arm, on a targeted panel of 400 genes; the facility "
            "prepared and sequenced the libraries, and then ran an independent qPCR "
            "validation of the panel's leading candidates. The archive holds the per-library "
            "sequencing metrics, the sample sheet recording each library's arm, preparation "
            "batch and metrics, the gene-level read counts, the qPCR validation, and the "
            "panel's gene-set annotation. ")
    if brief_kind() == "thresholds":
        return base + ("The facility's numeric thresholds for such a study are written into "
                       "the brief the data steward will release first: which libraries count "
                       "as usable, the minimum usable replicates per arm, at what thresholds "
                       "a gene is called, and how a validation is scored.")
    return base + ("The facility's standing rules for such a study are written into the brief "
                   "the data steward will release first: which libraries count as usable, how "
                   "many usable replicates each arm must keep, what the design must allow "
                   "before any gene is called, at what thresholds a gene is called, and what "
                   "the validation must show before a candidate list is issued.")


def _design(shape):
    """(condition, batch) per sample, control arm first (indices 0-5), treated 6-11."""
    cond = ["control"] * _N_PER_ARM + ["treated"] * _N_PER_ARM
    if shape in (0, 3, 4, 7):
        batch = ["L1"] * (2 * _N_PER_ARM)
    elif shape == 1:
        batch = ["L1"] * _N_PER_ARM + ["L2"] * _N_PER_ARM
    elif shape == 6:                        # planned balanced: L1 = 4 ctrl + 2 trt, L2 = 2 ctrl + 4 trt
        batch = ["L1"] * 4 + ["L2"] * 2 + ["L1"] * 2 + ["L2"] * 4
    else:                                   # partially nested: 5+1 / 1+5, treatments mostly nested in batch
        batch = ["L1"] * 5 + ["L2"] * 1 + ["L1"] * 1 + ["L2"] * 5
    return cond, batch


def _simulate(rng, shape, cond, batch):
    n = len(cond)
    mu = np.clip(rng.normal(7.5, 1.8, _N_GENES), 3.0, 13.0)
    size = rng.uniform(0.75, 1.30, n)
    log_effect = np.zeros((_N_GENES, n))
    de_idx = np.array([], dtype=int)
    if shape not in (4, 5):                 # a treatment effect on 40 genes
        de_idx = rng.choice(_N_GENES, _N_DE, replace=False)
        lfc = rng.uniform(1.5, 2.5, _N_DE) * rng.choice([-1.0, 1.0], _N_DE)
        treated = np.array([c == "treated" for c in cond])
        log_effect[np.ix_(de_idx, treated)] += lfc[:, None]
    if len(set(batch)) > 1:                 # a batch effect on 120 genes
        b_idx = rng.choice(_N_GENES, _N_BATCH_GENES, replace=False)
        shift = rng.uniform(1.6, 2.4, _N_BATCH_GENES) * rng.choice([-1.0, 1.0], _N_BATCH_GENES)
        in_l2 = np.array([b == "L2" for b in batch])
        log_effect[np.ix_(b_idx, in_l2)] += shift[:, None]
    mean = (2.0 ** (mu[:, None] + log_effect)) * size[None, :]
    phi = 0.08                              # NB dispersion via gamma-Poisson
    lam = mean * rng.gamma(1.0 / phi, phi, mean.shape)
    return rng.poisson(lam).astype(int), de_idx


def _metrics(rng, shape):
    reads = rng.uniform(9.0e6, 22.0e6, 2 * _N_PER_ARM).round(-3)
    rate = rng.uniform(0.86, 0.95, 2 * _N_PER_ARM).round(3)
    if shape == 3:                          # four treated libraries fail: two on reads, two on mapping
        fail = rng.choice(np.arange(_N_PER_ARM, 2 * _N_PER_ARM), 4, replace=False)
        reads[fail[:2]] = rng.uniform(2.1e6, 3.8e6, 2).round(-3)
        rate[fail[2:]] = rng.uniform(0.41, 0.55, 2).round(3)
    if shape == 6:                          # the two L2 controls (4, 5) and the two L1 treated (6, 7)
        fail = np.array([4, 5, 6, 7])
        reads[fail[:2]] = rng.uniform(2.1e6, 3.8e6, 2).round(-3)
        rate[fail[2:]] = rng.uniform(0.41, 0.55, 2).round(3)
    return reads, rate


def _validation(rng, shape, de_calls):
    """The facility's qPCR of the ten strongest panel calls, four biological replicates per
    arm, log2 relative expression. Confirms on the signal seeds; confirms nothing on seed 7."""
    if not de_calls:
        return {"genes": [], "expectedDirection": {}, "qpcr": {}, "rule": dict(_VALID),
                "note": "no candidates were nominated for validation"}
    top = sorted(de_calls, key=lambda g: -abs(de_calls[g]))[:_N_VALIDATE]
    qpcr, direction = {}, {}
    for g in top:
        direction[g] = "up" if de_calls[g] > 0 else "down"
        true_shift = 0.0 if shape == 7 else de_calls[g] * rng.uniform(0.6, 0.9)
        ctrl = rng.normal(0.0, 0.30, _QPCR_REPS)
        trt = rng.normal(true_shift, 0.30, _QPCR_REPS)
        qpcr[g] = {"control": [round(float(x), 3) for x in ctrl],
                   "treated": [round(float(x), 3) for x in trt]}
    return {"genes": top, "expectedDirection": direction, "qpcr": qpcr, "rule": dict(_VALID),
            "unit": "log2 relative expression, four biological replicates per arm"}


def _gene_sets(rng, genes, de_idx):
    """Twelve annotated sets of thirty genes; one is built around the responding genes."""
    sets = {}
    pool = np.arange(len(genes))
    for i in range(_N_SETS):
        if i == 2 and de_idx.size:
            core = rng.choice(de_idx, min(20, de_idx.size), replace=False)
            rest = rng.choice(np.setdiff1d(pool, core), _SET_SIZE - core.size, replace=False)
            members = np.concatenate([core, rest])
        else:
            members = rng.choice(pool, _SET_SIZE, replace=False)
        sets[f"SET{i + 1:02d}"] = sorted(genes[j] for j in members)
    return {"sets": sets, "universe": len(genes), "rule": {"alpha": 0.05, "adjust": "BH"}}


def _calls(counts_block, blocked: bool) -> dict:
    """{gene: log2FC} for the genes the reference comparison calls."""
    m = np.asarray(counts_block["counts"], dtype=float)
    cond = counts_block["condition"]
    batch = counts_block["batch"]
    x = omics._log_cpm(m)
    ia = [i for i, c in enumerate(cond) if c == "control"]
    ib = [i for i, c in enumerate(cond) if c == "treated"]
    if not blocked:
        _t, p = stats.ttest_ind(x[:, ib], x[:, ia], axis=1, equal_var=False)
        p = np.nan_to_num(np.asarray(p, dtype=float), nan=1.0)
        lfc = x[:, ib].mean(axis=1) - x[:, ia].mean(axis=1)
    else:
        xt = x.T
        n = xt.shape[0]
        cols = [np.ones(n), np.array([1.0 if c == "treated" else 0.0 for c in cond])]
        for lv in sorted(set(batch))[1:]:
            cols.append(np.array([1.0 if v == lv else 0.0 for v in batch]))
        d = np.column_stack(cols)
        xtx_inv = np.linalg.inv(d.T @ d)
        beta = xtx_inv @ d.T @ xt
        resid = xt - d @ beta
        df = n - d.shape[1]
        sigma2 = (resid ** 2).sum(axis=0) / df
        se = np.sqrt(np.maximum(sigma2 * xtx_inv[1, 1], 1e-300))
        p = 2.0 * stats.t.sf(np.abs(beta[1] / se), df)
        lfc = beta[1]
    padj = omics._bh(p)
    sig = (padj < _THRESH["padjThreshold"]) & (np.abs(lfc) >= _THRESH["log2fcThreshold"])
    return {counts_block["genes"][i]: float(lfc[i]) for i in np.where(sig)[0]}


@functools.lru_cache(maxsize=None)
def _generate_cached(seed: int):
    shape = seed if seed in SHAPES else seed % 3
    cond, batch = _design(shape)
    ids = [f"S{i + 1:02d}" for i in range(len(cond))]
    genes = [f"G{i + 1:04d}" for i in range(_N_GENES)]
    for attempt in range(200):
        rng = np.random.default_rng(seed * 1_000_003 + 20260922 + attempt)
        reads, rate = _metrics(rng, shape)
        counts, de_idx = _simulate(rng, shape, cond, batch)
        library_qc = {"qcRules": dict(_RULES),
                      "samples": [{"sample": s, "condition": c, "assignedReads": int(r),
                                   "mappingRate": float(m)}
                                  for s, c, r, m in zip(ids, cond, reads, rate)]}
        sample_sheet = {"qcRules": dict(_RULES),
                        "samples": [{"sample": s, "condition": c, "batch": b,
                                     "assignedReads": int(r), "mappingRate": float(m)}
                                    for s, c, b, r, m in zip(ids, cond, batch, reads, rate)]}
        counts_block = {"genes": list(genes), "samples": list(ids), "condition": list(cond),
                        "batch": list(batch), "conditions": ["control", "treated"],
                        **_THRESH, "counts": counts.tolist()}
        qc = omics.rna_sample_qc(library_qc)
        des = omics.design_identifiability(sample_sheet)
        res = {"qc": {"failedSamples": qc["failedSamples"],
                      "minReplicates": qc["minReplicates"]},
               "design": {"confounded": des["confounded"], "batchCount": des["batchCount"]},
               "_shape": SHAPES[shape]}
        de_calls = {}
        ok = True
        if shape == 3:
            ok = qc["minReplicates"] < 3
        elif shape == 1:
            ok = qc["minReplicates"] >= 3 and des["confounded"] == 1
        elif shape == 6:
            planned = omics.design_identifiability(
                {"samples": [{"sample": s, "condition": c, "batch": b}
                             for s, c, b in zip(ids, cond, batch)]})
            ok = (qc["minReplicates"] >= 3 and qc["failedSamples"] == 4
                  and des["confounded"] == 1 and planned["confounded"] == 0)
        elif shape in (0, 4, 7):
            ok = qc["minReplicates"] >= 3 and des["confounded"] == 0 and des["batchCount"] == 1
            if ok:
                n_sig = omics.de_simple(counts_block)["nSignificant"]
                ok = (30 <= n_sig <= 45) if shape in (0, 7) else (n_sig <= 2)
                if ok:
                    res["de"] = {"nSignificant": n_sig}
                    de_calls = _calls(counts_block, blocked=False)
        else:                                                   # 2, 5: batched, estimable
            ok = qc["minReplicates"] >= 3 and des["confounded"] == 0 and des["batchCount"] == 2
            if ok:
                blocked = omics.de_blocked(counts_block)["nSignificant"]
                naive = omics.de_simple(counts_block)["nSignificant"]
                frac = omics.batch_assessment(counts_block)["batchVarianceFraction"]
                want = (30 <= blocked <= 45) if shape == 2 else (blocked <= 2)
                # On the signal seed the trap must be real: the batch-blind comparison has to
                # call at least ten genes more than the adjusted one. On the null seed the
                # batch-blind Welch test is protected by its own inflated within-arm variance
                # (measured: 0-1 calls either way over 40 draws), so the divert is graded on
                # the route and the batch fraction alone.
                ok = want and frac >= 0.5 and (shape == 5 or naive - blocked >= 10)
                if ok:
                    res["de"] = {"nSignificant": blocked}
                    res["batch"] = {"varianceFraction": round(frac, 4)}
                    de_calls = _calls(counts_block, blocked=True)
        if not ok:
            continue
        validation = _validation(rng, shape, de_calls)
        gene_sets = _gene_sets(rng, genes, de_idx)
        if de_calls:
            vc = omics.validation_concordance(validation)
            res["confirm"] = {"concordance": round(vc["concordance"], 4)}
            if shape == 7:
                ok = vc["concordance"] <= 0.3
            else:
                ok = vc["concordance"] >= 0.9
                if ok:
                    en = omics.enrichment({**gene_sets, "calledGenes": sorted(de_calls)})
                    ok = en["nSignificantSets"] == 1
                    if ok:
                        res["enrich"] = {"nSignificantSets": en["nSignificantSets"]}
            if not ok:
                continue
        blocks = {"define": {"goal": "decide whether, and for which genes, the compound "
                                     "changes expression against vehicle control",
                             "arms": ["control", "treated"], "replicatesPerArm": _N_PER_ARM,
                             "panelGenes": _N_GENES, "qcRules": dict(_RULES), **_THRESH,
                             "validationRule": dict(_VALID),
                             "analysisPlan": _analysis_plan()},
                  "library_qc": library_qc, "sample_sheet": sample_sheet,
                  "counts": counts_block, "validation": validation, "gene_sets": gene_sets}
        return blocks, res
    raise RuntimeError(f"rnaseq_batch: could not realise shape {shape} for seed {seed}")


def generate(seed: int):
    """Deterministic, and cached: the builder and its checks call this many times per seed, and
    a draw costs seconds. Callers get a deep copy so no one can mutate the cached blocks."""
    blocks, res = _generate_cached(int(seed))
    return copy.deepcopy(blocks), copy.deepcopy(res)


CASE = V2Case(
    case_id="adb_c40", title="Compound response on a targeted expression panel",
    industry="life_sciences", y_type="mixed",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    seeds=(0, 1, 2, 3, 4, 5, 6, 7),
    shapes=dict(SHAPES), node_data=NODE_DATA,
    budget={"max_turns": 26},
    # Running the validation step when the comparison nominated nothing (the null seeds) is
    # pointless work, not a validity violation: the empty nomination list confirms nothing and
    # licenses nothing. Accepted at the comparison forks so it is neither evidence of the
    # validation branch nor a wrong turn. Measured on GPT-6-astra before this was declared:
    # both null seeds scored the fork "incorrect" for exactly this over-work.
    accepted_methods={"A_de_simple": ("expression.validation_concordance",),
                      "A_de_blocked": ("expression.validation_concordance",)},
    context=_context(),
    goal=(
        "Work through the batches the data steward will release and report where this study "
        "stands: whether the libraries can carry a conclusion at all, whether the comparison "
        "the study set out to make can be made on this design, which genes if any respond to "
        "the compound, whether the validation supports issuing that list, and what the "
        "facility should do next. Every number in your report must come from a computation "
        "you ran on this task; where something could not be computed, say so rather than "
        "inventing it."),
    blocks_meta={
        "define": {"label": "Study brief and the facility's standing rules", "phase": "define",
                   "topics": ("brief", "standing rules", "thresholds")},
        "library_qc": {"label": "Per-library sequencing metrics", "phase": "measure",
                       "topics": ("sequencing metrics", "library metrics", "mapping rate")},
        "sample_sheet": {"label": "Sample sheet: arm, preparation batch and metrics per library",
                         "phase": "measure",
                         "topics": ("sample sheet", "preparation batch", "arm labels")},
        "counts": {"label": "Gene-level read counts per library", "phase": "analyze",
                   "topics": ("read counts", "count matrix", "gene counts")},
        "validation": {"label": "qPCR validation of the nominated candidates", "phase": "improve",
                       "topics": ("qpcr", "validation", "nominated candidates")},
        "gene_sets": {"label": "Gene-set annotation of the panel", "phase": "analyze",
                      "topics": ("gene sets", "annotation", "pathways")},
    },
    field_map={
        "qc.failedSamples": ({"method_id": "qc.sample_qc", "output": "failedSamples",
                              "scale": 1.0},),
        "qc.minReplicates": ({"method_id": "qc.sample_qc", "output": "minReplicates",
                              "scale": 1.0},),
        "design.confounded": ({"method_id": "design.identifiability", "output": "confounded",
                               "scale": 1.0},),
        "design.batchCount": ({"method_id": "design.identifiability", "output": "batchCount",
                               "scale": 1.0},),
        "batch.varianceFraction": ({"method_id": "expression.batch_assessment",
                                    "output": "batchVarianceFraction", "scale": 1.0},),
        "de.nSignificant": ({"method_id": "expression.de_simple", "output": "nSignificant",
                             "scale": 1.0},
                            {"method_id": "expression.de_blocked", "output": "nSignificant",
                             "scale": 1.0}),
        "confirm.concordance": ({"method_id": "expression.validation_concordance",
                                 "output": "concordance", "scale": 1.0},),
        "enrich.nSignificantSets": ({"method_id": "expression.enrichment",
                                     "output": "nSignificantSets", "scale": 1.0},),
    },
    truth_fields=(
        {"field": "qc.failedSamples", "method_id": "qc.sample_qc", "output": "failedSamples",
         "scale": 1.0, "tol": 0.0},
        {"field": "qc.minReplicates", "method_id": "qc.sample_qc", "output": "minReplicates",
         "scale": 1.0, "tol": 0.0},
        {"field": "design.confounded", "method_id": "design.identifiability",
         "output": "confounded", "scale": 1.0, "tol": 0.0},
        {"field": "design.batchCount", "method_id": "design.identifiability",
         "output": "batchCount", "scale": 1.0, "tol": 0.0},
        # `batch.varianceFraction` is deliberately NOT a published truth. It routes nothing
        # (the batch fork reads `design.*`) and it is convention-bound: the reference reports
        # the one-way R^2 of PC1 on batch (0.95 on seed 2), while the first contestant measured
        # reported the share of total variance explained by batch (0.56) -- both defensible,
        # neither "the" number. Same policy as the non-normal Ppk in the main corpus: pinning
        # one would score the convention, not the competence.
        # Differential-expression counts are convention-sensitive (test, shrinkage, filter),
        # so the window is wide: a competent analysis lands within eight genes of the
        # reference on a 40-gene effect; a batch-blind one on a batched seed does not.
        {"field": "de.nSignificant", "method_id": "expression.de_simple",
         "output": "nSignificant", "scale": 1.0, "tol": 8.0},
        {"field": "de.nSignificant", "method_id": "expression.de_blocked",
         "output": "nSignificant", "scale": 1.0, "tol": 8.0},
        {"field": "confirm.concordance", "method_id": "expression.validation_concordance",
         "output": "concordance", "scale": 1.0, "tol": 0.11},
        {"field": "enrich.nSignificantSets", "method_id": "expression.enrichment",
         "output": "nSignificantSets", "scale": 1.0, "tol": 1.0},
    ),
)

if __name__ == "__main__":
    for s in CASE.seeds:
        _, r = generate(s)
        print(f"seed {s} [{r['_shape']:22s}] qc={r['qc']} design={r['design']} "
              f"de={r.get('de')} confirm={r.get('confirm')} enrich={r.get('enrich')} "
              f"route={walk(GRAPH, r)}")
