#!/usr/bin/env bash
#
# DMAIC-Bench oracle reference solution.
#
# Harbor copies solution/ to /solution and runs this ONLY under `--agent oracle`
# (harbor.agents.oracle.OracleAgent.run uploads the directory at run time; the Docker build
# context is environment/, so nothing here is ever baked into an image a normal agent sees).
#
# It contains NO answers. /solution/plan.json holds the route only — which batches of data to
# ask the steward for, which method each batch calls for, and what the output fields are
# named. Every number below is computed here, at run time, from data the steward released:
# this script asks the data steward exactly as an agent would, cleans what comes back, runs
# the analyses with numpy/scipy, and assembles /workspace/trace.json and /workspace/report.md
# out of what it computed.
#
set -euo pipefail

PLAN="${PLAN:-/solution/plan.json}"
WORK="${WORK:-/workspace}"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

if [ ! -f "$PLAN" ]; then
  echo "oracle: no plan at $PLAN" >&2
  exit 1
fi

mkdir -p "$WORK"

python3 - <<'PRECHECK'
import sys
missing = []
for mod in ("numpy", "scipy"):
    try:
        __import__(mod)
    except ImportError:
        missing.append(mod)
if missing:
    sys.stderr.write(
        "oracle: the agent image is missing %s. The reference solution derives every "
        "number rather than reciting it, so it needs them.\n" % ", ".join(missing))
    raise SystemExit(3)
PRECHECK

# Write the analysis program, then run it. (Writing a source file with a heredoc and
# executing it is the documented, allowed way to ship solution code.)
cat > "$SCRATCH/oracle_analysis.py" <<'PYEOF'
"""Derive the whole analysis from data the steward releases. No stored results."""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

import numpy as np
from scipy import stats

#: The steward is loopback-only. Container runtimes inject HTTP_PROXY pointing at a
#: host-side proxy and urllib would try to route through it; talk to the steward directly.
_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))

# ------------------------------------------------------------------ block key resolution

#: the dirty variant renames top-level keys, injects distractor keys, punches None holes in
#: numeric arrays and stringifies one element (dmaic_bench/tasks/perturb.py). Cleaning
#: that up is normal analyst work, so the oracle does it too rather than assuming clean data.
_SYNONYMS = {
    "data": ("values", "measurements", "readings"),
    "groups": ("group_data",),
    "group1": ("groupa",),
    "group2": ("groupb",),
    "counts": ("defect_counts", "defects"),
    "x": ("x_values",),
    "y": ("y_values",),
    "lsl": ("lower_spec",),
    "usl": ("upper_spec",),
    "target": ("target_value",),
    "hypothesizedmedian": ("hypothesized_median",),
    "hypothesizedmean": ("hypothesized_mean",),
    "subgroupsize": ("subgroup_size",),
    "samplesizes": ("sample_sizes",),
}
# Mirrors the canonical English perturbation keys and original suffix. The oracle cannot
# import the bench package inside the agent container, so tests check this copy for drift.
_DISTRACTOR_KEYS = {
    "recorder", "remark", "shift", "ambient",       # en
    "row_id",                                       # locale-independent
}
_ORIGINAL_SUFFIXES = ("_original",)


def _norm(key):
    k = str(key).lower().replace("_", "").replace("-", "")
    for suffix in _ORIGINAL_SUFFIXES:
        k = k.replace(suffix.lower().replace("_", ""), "")
    return k


def pick(block, *names, default=None):
    """Fetch a value by any of *names*, tolerating renames, casing and the CJK suffix."""
    if not isinstance(block, dict):
        return default
    index = {_norm(k): v for k, v in block.items()}
    for name in names:
        n = _norm(name)
        if n in index:
            return index[n]
        for syn in _SYNONYMS.get(n, ()):
            if _norm(syn) in index:
                return index[_norm(syn)]
    # last resort: a renamed key whose normalized form still contains the wanted one
    for name in names:
        n = _norm(name)
        for k, v in index.items():
            if k in _DISTRACTOR_KEYS or _norm(k) in {_norm(d) for d in _DISTRACTOR_KEYS}:
                continue
            if n and (k.startswith(n) or n.startswith(k)):
                return v
    return default


def num(v, default=None):
    if isinstance(v, bool):
        return default
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v.strip().replace(",", ""))
        except ValueError:
            return default
    return default


def arr(v):
    """Numeric array with None holes dropped and stringified numbers recovered."""
    if v is None:
        return np.array([], dtype=float)
    if isinstance(v, dict):
        v = list(v.values())
    if not isinstance(v, (list, tuple)):
        f = num(v)
        return np.array([f], dtype=float) if f is not None and math.isfinite(f) \
            else np.array([], dtype=float)
    out = []
    for x in np.ravel(np.array(list(v), dtype=object)).tolist():
        f = num(x)
        if f is not None and math.isfinite(f):
            out.append(f)
    return np.array(out, dtype=float)


def paired(a, b):
    """Two arrays aligned element-wise, dropping any index either side lost to a hole."""
    ka, kb = list(a or []), list(b or [])
    n = min(len(ka), len(kb))
    xs, ys = [], []
    for i in range(n):
        u, v = num(ka[i]), num(kb[i])
        if u is not None and v is not None and math.isfinite(u) and math.isfinite(v):
            xs.append(u)
            ys.append(v)
    return np.array(xs, dtype=float), np.array(ys, dtype=float)


def columns(data, names):
    """Align several named columns of a dict-of-lists, dropping rows with any hole."""
    cols = [list(pick(data, n) or []) for n in names]
    if not cols or any(not c for c in cols):
        return {n: np.array([], dtype=float) for n in names}
    n_rows = min(len(c) for c in cols)
    keep = []
    for i in range(n_rows):
        vals = [num(c[i]) for c in cols]
        if all(v is not None and math.isfinite(v) for v in vals):
            keep.append(vals)
        continue
    if not keep:
        return {n: np.array([], dtype=float) for n in names}
    mat = np.array(keep, dtype=float)
    return {n: mat[:, j] for j, n in enumerate(names)}


def group_map(block):
    g = pick(block, "groups", "group_data")
    if isinstance(g, dict):
        return {str(k): arr(v) for k, v in g.items() if len(arr(v))}
    return {}


# ------------------------------------------------------------------ shared statistics

_D2 = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 7: 2.704, 8: 2.847, 9: 2.970,
       10: 3.078}
_A2 = {2: 1.880, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483, 7: 0.419, 8: 0.373, 9: 0.337,
       10: 0.308}
_D3 = {2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.076, 8: 0.136, 9: 0.184, 10: 0.223}
_D4 = {2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004, 7: 1.924, 8: 1.864, 9: 1.816,
       10: 1.777}


def _c4(n):
    return math.sqrt(2.0 / (n - 1)) * math.gamma(n / 2.0) / math.gamma((n - 1) / 2.0)


def ad_normality(x):
    """Anderson-Darling A^2 and its p-value (D'Agostino & Stephens adjustment)."""
    x = np.sort(np.asarray(x, dtype=float))
    n = len(x)
    if n < 8:
        return float("nan"), float("nan")
    mu, sd = float(np.mean(x)), float(np.std(x, ddof=1))
    if sd <= 0:
        return float("nan"), float("nan")
    z = stats.norm.cdf((x - mu) / sd)
    z = np.clip(z, 1e-12, 1 - 1e-12)
    i = np.arange(1, n + 1)
    a2 = -n - np.sum((2 * i - 1) * (np.log(z) + np.log(1 - z[::-1]))) / n
    a2s = a2 * (1 + 0.75 / n + 2.25 / n ** 2)
    if a2s >= 0.6:
        p = math.exp(1.2937 - 5.709 * a2s + 0.0186 * a2s ** 2)
    elif a2s >= 0.34:
        p = math.exp(0.9177 - 4.279 * a2s - 1.38 * a2s ** 2)
    elif a2s >= 0.2:
        p = 1 - math.exp(-8.318 + 42.796 * a2s - 59.938 * a2s ** 2)
    else:
        p = 1 - math.exp(-13.436 + 101.14 * a2s - 223.73 * a2s ** 2)
    return float(a2), float(min(max(p, 0.0), 1.0))


def within_sd(x):
    """Short-term sigma from the average moving range (MR-bar / d2)."""
    x = np.asarray(x, dtype=float)
    if len(x) < 2:
        return float("nan")
    mr = np.abs(np.diff(x))
    return float(np.mean(mr) / _D2[2])


def ols(design, y):
    """Least squares with an intercept already in *design*; returns the usual model stats."""
    n, k = design.shape
    beta, *_ = np.linalg.lstsq(design, y, rcond=None)
    fitted = design @ beta
    resid = y - fitted
    sse = float(resid @ resid)
    sst = float(((y - y.mean()) ** 2).sum())
    p = k - 1                                   # predictors excluding the intercept
    dfe = n - k
    r2 = 1.0 - sse / sst if sst > 0 else float("nan")
    r2adj = 1.0 - (1.0 - r2) * (n - 1) / dfe if dfe > 0 and sst > 0 else float("nan")
    if p > 0 and dfe > 0 and sse > 0:
        f = ((sst - sse) / p) / (sse / dfe)
        pval = float(stats.f.sf(f, p, dfe))
    else:
        f, pval = float("nan"), float("nan")
    return {"beta": beta, "fitted": fitted, "resid": resid, "sse": sse, "sst": sst,
            "dfe": dfe, "n": n, "k": k, "rSquared": r2, "rSquaredAdj": r2adj,
            "fStatistic": float(f), "modelPValue": pval, "design": design, "y": y}


def design_from_terms(cols, terms):
    """Build [1 | term…] where a term is 'A', 'A*B' or 'A*A' (a power)."""
    n = len(next(iter(cols.values())))
    mat = [np.ones(n)]
    names = []
    for term in terms:
        parts = [p.strip() for p in str(term).split("*") if p.strip()]
        vec = np.ones(n)
        ok = True
        for p in parts:
            if p not in cols:
                ok = False
                break
            vec = vec * cols[p]
        if ok:
            mat.append(vec)
            names.append(term)
    return np.column_stack(mat), names


# ------------------------------------------------------------------ method implementations

def _kappa(a, b):
    cats = sorted(set(a) | set(b))
    if len(cats) < 2:
        return 1.0
    idx = {c: i for i, c in enumerate(cats)}
    m = np.zeros((len(cats), len(cats)))
    for u, v in zip(a, b):
        m[idx[u], idx[v]] += 1
    tot = m.sum()
    if tot == 0:
        return float("nan")
    po = np.trace(m) / tot
    pe = float((m.sum(axis=0) * m.sum(axis=1)).sum()) / tot ** 2
    return float((po - pe) / (1 - pe)) if pe < 1 else 1.0


def m_attribute_agreement(b):
    assessments = pick(b, "assessments")
    per_appraiser = {}
    standard = {}
    if isinstance(assessments, list) and assessments:
        by_part = {}
        for row in assessments:
            if not isinstance(row, dict):
                continue
            ap = str(pick(row, "appraiserId", "appraiser"))
            part = str(pick(row, "partId", "part"))
            res = str(pick(row, "result", "rating"))
            per_appraiser.setdefault(ap, {}).setdefault(part, []).append(res)
            by_part.setdefault(part, []).append(res)
            ref = pick(row, "standard", "referenceValue")
            if ref is not None:
                standard[part] = str(ref)
        if not standard:
            # no attribute standard column: use the consensus of all appraisers/trials
            for part, vals in by_part.items():
                standard[part] = max(set(vals), key=vals.count)
    else:
        std = pick(b, "standard")
        ratings = pick(b, "ratings")
        if not isinstance(std, list) or not isinstance(ratings, dict):
            raise ValueError("no attribute-study layout recognised")
        for i, s in enumerate(std):
            standard[str(i)] = str(s)
        for ap, trials in ratings.items():
            per_appraiser[str(ap)] = {}
            for trial in trials:
                for i, v in enumerate(trial):
                    per_appraiser[str(ap)].setdefault(str(i), []).append(str(v))

    kappas, within = {}, {}
    for ap, parts in per_appraiser.items():
        obs, ref = [], []
        for part, vals in parts.items():
            if part not in standard:
                continue
            for v in vals:
                obs.append(v)
                ref.append(standard[part])
        if obs:
            kappas[ap] = _kappa(obs, ref)
        agree = [1.0 if len(set(v)) == 1 else 0.0 for v in parts.values() if len(v) > 1]
        if agree:
            within[ap] = float(np.mean(agree))
    if not kappas:
        raise ValueError("no appraiser could be scored")
    # Agreement with the STANDARD, over every individual rating.
    agree_std = total_std = 0
    for ratings_by_part in per_appraiser.values():
        for part, vals in ratings_by_part.items():
            ref = standard.get(part)
            if ref is None:
                continue
            total_std += len(vals)
            agree_std += sum(1 for v in vals if v == ref)
    return {
        "kappaMin": float(min(kappas.values())),
        "kappaMean": float(np.mean(list(kappas.values()))),
        "appraiserCount": len(kappas),
        # `agreementPct` is the canonical name in the published vocabulary, and it names a
        # DIFFERENT quantity from within-appraiser repeatability: per the reference
        # implementation, it is 100 x (individual ratings equal to the standard) / (all
        # ratings), pooled across appraisers and trials. Aliasing it onto the self-consistency
        # figure gave the right name for the wrong number -- 95.556 against a truth of 97.778 --
        # which is worse than not reporting it, because "not computed" becomes "computed wrong".
        "agreementPct": (100.0 * agree_std / total_std) if total_std else float("nan"),
        "withinAppraiserAgreement": float(np.mean(list(within.values()))) if within else float("nan"),
        "_declare": {"kappa_min": float(min(kappas.values()))},
    }


def _grr_cube(b):
    meas = pick(b, "measurements", "data")
    if isinstance(meas, dict):
        ops = list(meas.keys())
        cube = []
        for op in ops:
            parts = meas[op]
            cube.append([[num(v) for v in row if num(v) is not None] for row in parts])
        n_rep = min(len(r) for op in cube for r in op)
        return np.array([[r[:n_rep] for r in op] for op in cube], dtype=float)
    # Positions matter here: the flat list is operator-major, so dropping a hole would
    # shift every later reading into the wrong cell. Keep the holes as NaN, reshape, then
    # fill each from its own cell (the surviving replicate) — ordinary analyst cleaning.
    raw = meas if isinstance(meas, (list, tuple)) else []
    flat = np.array([num(v, float("nan")) for v in raw], dtype=float)
    n_op = int(num(pick(b, "numOperators", "operators"), 0) or 0)
    n_part = int(num(pick(b, "numParts", "parts"), 0) or 0)
    n_rep = int(num(pick(b, "numReplicates", "replicatesPerPart", "replicates"), 0) or 0)
    if n_op * n_part * n_rep != len(flat):
        raise ValueError("gage layout does not match the measurement count")
    cube = flat.reshape(n_op, n_part, n_rep)
    holes = ~np.isfinite(cube)
    if holes.any():
        for o, pt in zip(*np.where(holes.any(axis=2))):
            cell = cube[o, pt]
            good = cell[np.isfinite(cell)]
            fill = good.mean() if len(good) else np.nanmean(cube[:, pt, :])
            cell[~np.isfinite(cell)] = fill
        if not np.isfinite(cube).all():
            raise ValueError("gage study lost a whole cell")
    return cube


def m_gage_rr(b):
    cube = _grr_cube(b)                                   # [operator][part][replicate]
    n_op, n_part, n_rep = cube.shape
    grand = cube.mean()
    part_means = cube.mean(axis=(0, 2))
    op_means = cube.mean(axis=(1, 2))
    cell_means = cube.mean(axis=2)

    ss_part = n_op * n_rep * ((part_means - grand) ** 2).sum()
    ss_op = n_part * n_rep * ((op_means - grand) ** 2).sum()
    ss_int = n_rep * ((cell_means - op_means[:, None] - part_means[None, :] + grand) ** 2).sum()
    ss_err = ((cube - cell_means[:, :, None]) ** 2).sum()

    df_part, df_op = n_part - 1, n_op - 1
    df_int, df_err = df_part * df_op, n_op * n_part * (n_rep - 1)
    ms_int = ss_int / df_int if df_int > 0 else 0.0
    ms_err = ss_err / df_err if df_err > 0 else 0.0
    p_int = float(stats.f.sf(ms_int / ms_err, df_int, df_err)) if ms_err > 0 and df_int > 0 else 1.0

    if p_int > 0.25:      # AIAG MSA-4: pool a non-significant interaction into error
        ss_err += ss_int
        df_err += df_int
        ms_err = ss_err / df_err if df_err > 0 else 0.0
        ms_int = ms_err
        df_int = 0
    ms_part = ss_part / df_part if df_part > 0 else 0.0
    ms_op = ss_op / df_op if df_op > 0 else 0.0

    v_rep = max(ms_err, 0.0)
    v_int = max((ms_int - ms_err) / n_rep, 0.0) if df_int > 0 else 0.0
    v_op = max((ms_op - (ms_int if df_int > 0 else ms_err)) / (n_part * n_rep), 0.0)
    denom = n_op * n_rep
    v_part = max((ms_part - (ms_int if df_int > 0 else ms_err)) / denom, 0.0)

    v_grr = v_rep + v_op + v_int
    v_total = v_grr + v_part
    pct_sv = 100.0 * math.sqrt(v_grr / v_total) if v_total > 0 else float("nan")
    # sqrt(2), not the rounded 1.41 the AIAG tables print. The two differ by one whole
    # category near a boundary, and this corpus has four tasks whose entire routing decision
    # is whether the count reaches five -- measured drift on two of them: 8 against the
    # verifier's 7, and 10 against 9. (Case identifiers are deliberately not cited here: this
    # file ships inside every public task, and naming a held-out case in a comment publishes
    # its existence and a hint at its content. See docs/HELD_OUT_V2.md.)
    ndc = math.sqrt(2.0) * math.sqrt(v_part / v_grr) if v_grr > 0 else float("inf")
    out = {
        "percentStudyVariation": pct_sv,
        "getPercentSVTotalGage": pct_sv,
        "percentRepeatability": 100.0 * math.sqrt(v_rep / v_total) if v_total > 0 else float("nan"),
        "ndc": math.floor(ndc) if math.isfinite(ndc) else float("nan"),
        "interactionPValue": p_int,
        "_declare": {"grr_pct": pct_sv, "ndc": math.floor(ndc) if math.isfinite(ndc) else 0},
    }
    tol = num(pick(b, "tolerance"))
    if tol:
        out["percentTolerance"] = 100.0 * 6.0 * math.sqrt(v_grr) / tol
    return out


def m_pareto(b):
    groups = [str(g) for g in (pick(b, "groups", "categories") or [])]
    freqs = arr(pick(b, "frequencies", "counts"))
    if not len(freqs):
        raise ValueError("no frequencies")
    order = np.argsort(-freqs)
    freqs = freqs[order]
    groups = [groups[i] for i in order] if len(groups) == len(order) else groups
    total = float(freqs.sum())
    cum = np.cumsum(freqs) / total * 100.0
    vital = int(np.searchsorted(cum, 80.0) + 1)
    return {
        "topCategoryPct": float(freqs[0] / total * 100.0),
        "topCategory": groups[0] if groups else "",
        "cumulativePctAtTwo": float(cum[1]) if len(cum) > 1 else float(cum[0]),
        "vitalFewCount": vital,
        "categoryCount": int(len(freqs)),
    }


def m_fmea(b):
    items = pick(b, "items") or []
    rpns = []
    worst = ""
    for it in items:
        if not isinstance(it, dict):
            continue
        s = num(pick(it, "severity"), 0) or 0
        o = num(pick(it, "occurrence"), 0) or 0
        d = num(pick(it, "detection"), 1) or 1
        rpn = s * o * d
        rpns.append(rpn)
        if rpn == max(rpns):
            worst = str(pick(it, "failureMode", "mode", default=""))
    if not rpns:
        raise ValueError("no FMEA items")
    thr = num(pick(b, "rpnThreshold"), 0) or 0
    return {"maxRpn": float(max(rpns)), "meanRpn": float(np.mean(rpns)),
            "aboveThresholdCount": int(sum(1 for r in rpns if r >= thr)),
            "itemCount": len(rpns), "topFailureMode": worst}


def m_binomial_capability(b):
    d = arr(pick(b, "defectCounts", "defects", "counts"))
    n = arr(pick(b, "sampleSizes", "sampleSize", "subgroupSizes", "trials", "inspected"))
    if len(n) == 1 and len(d) > 1:
        n = np.repeat(n, len(d))
    k = min(len(d), len(n))
    d, n = d[:k], n[:k]
    if k == 0 or n.sum() <= 0:
        raise ValueError("no binomial data")
    p = float(d.sum() / n.sum())
    z = float(stats.norm.ppf(1.0 - p)) if 0 < p < 1 else float("inf")
    out = {"avgP": p, "defectiveRate": p, "processZ": z, "ppmDefective": p * 1e6,
           "subgroupCount": int(k)}
    t = num(pick(b, "target"))
    if t is not None:
        out["target"] = t
        out["meetsTarget"] = bool(p <= t)
    return out


def m_poisson_capability(b):
    d = arr(pick(b, "defectCounts", "defects", "counts"))
    u = arr(pick(b, "inspectionUnits", "unitCounts", "units"))
    k = min(len(d), len(u))
    if k == 0 or u[:k].sum() <= 0:
        raise ValueError("no count-rate data")
    dpu = float(d[:k].sum() / u[:k].sum())
    return {"dpu": dpu, "meanDPU": dpu, "dpmo": dpu * 1e6, "subgroupCount": int(k)}


def _cap_outputs(x, lsl, usl, sd_within, sd_overall):
    mu = float(np.mean(x))
    out = {"mean": mu, "stdDevOverall": sd_overall, "stdDevWithin": sd_within,
           "sampleSize": int(len(x))}
    for tag, sd in (("cp", sd_within), ("pp", sd_overall)):
        if sd and sd > 0 and lsl is not None and usl is not None:
            out[tag] = (usl - lsl) / (6 * sd)
        if sd and sd > 0:
            hi = (usl - mu) / (3 * sd) if usl is not None else float("inf")
            lo = (mu - lsl) / (3 * sd) if lsl is not None else float("inf")
            out[tag + "k"] = float(min(hi, lo))
    return out


def m_normal_capability(b):
    x = arr(pick(b, "data", "values", "measurements"))
    if len(x) < 3:
        raise ValueError("not enough measurements")
    lsl, usl = num(pick(b, "lsl")), num(pick(b, "usl"))
    out = _cap_outputs(x, lsl, usl, within_sd(x), float(np.std(x, ddof=1)))
    a2, p = ad_normality(x)
    out["adPValue"] = p
    out["_declare"] = {"ad_p": p}
    return out


def m_grouped_capability(b):
    groups = group_map(b)
    if not groups:
        raise ValueError("no groups")
    lsl, usl = num(pick(b, "lsl")), num(pick(b, "usl"))
    allx = np.concatenate(list(groups.values()))
    # pooled within-group sigma; overall sigma keeps the between-group shift in
    ss = sum(((g - g.mean()) ** 2).sum() for g in groups.values())
    df = sum(len(g) - 1 for g in groups.values())
    sd_within = math.sqrt(ss / df) if df > 0 else float("nan")
    out = _cap_outputs(allx, lsl, usl, sd_within, float(np.std(allx, ddof=1)))
    out["groupCount"] = len(groups)
    return out


def m_nonnormal_capability(b):
    x = arr(pick(b, "data", "values"))
    if len(x) < 5:
        raise ValueError("not enough measurements")
    lsl, usl = num(pick(b, "lsl")), num(pick(b, "usl"))
    shape, loc, scale = stats.weibull_min.fit(x, floc=0)
    q = lambda pr: float(stats.weibull_min.ppf(pr, shape, loc, scale))
    med, hi, lo = q(0.5), q(0.99865), q(0.00135)
    ppu = (usl - med) / (hi - med) if usl is not None and hi > med else float("inf")
    ppl = (med - lsl) / (med - lo) if lsl is not None and med > lo else float("inf")
    return {"ppk": float(min(ppu, ppl)), "ppu": float(ppu), "ppl": float(ppl),
            "distribution": "weibull", "shape": float(shape), "scale": float(scale),
            "median": med}


def _chart_flags(vals, cl, ucl, lcl):
    return int(sum(1 for v in vals if (ucl is not None and v > ucl)
                   or (lcl is not None and v < lcl)))


def m_imr(b):
    x = arr(pick(b, "data", "values"))
    if len(x) < 2:
        raise ValueError("not enough points")
    cl = float(np.mean(x))
    mrbar = float(np.mean(np.abs(np.diff(x))))
    ucl, lcl = cl + 2.66 * mrbar, cl - 2.66 * mrbar
    flags = _chart_flags(x, cl, ucl, lcl)
    return {"centerLine": cl, "individualsUCL": ucl, "individualsLCL": lcl,
            "movingRangeBar": mrbar, "mrUCL": 3.267 * mrbar, "flaggedCount": flags,
            "_declare": {"stable": flags == 0}}


def _subgroups(b):
    x = arr(pick(b, "data", "values"))
    n = int(num(pick(b, "subgroupSize", "subgroup_size"), 0) or 0)
    if n < 2 or len(x) < n:
        raise ValueError("no usable subgroups")
    k = len(x) // n
    return x[:k * n].reshape(k, n), n


def m_xbar_r(b):
    sub, n = _subgroups(b)
    means, ranges = sub.mean(axis=1), sub.max(axis=1) - sub.min(axis=1)
    cl, rbar = float(means.mean()), float(ranges.mean())
    a2 = _A2.get(n, _A2[10])
    ucl, lcl = cl + a2 * rbar, cl - a2 * rbar
    flags = _chart_flags(means, cl, ucl, lcl)
    r_ucl, r_lcl = _D4.get(n, _D4[10]) * rbar, _D3.get(n, _D3[10]) * rbar
    # The RANGE chart is read too, and it is not decoration: the X-bar limits above are
    # cl +- A2*Rbar, so ranges out of control make those limits a statement about nothing.
    # A run is stable only when both charts are.
    r_flags = _chart_flags(ranges, rbar, r_ucl, r_lcl)
    return {"xBarChartCenterLine": cl, "xBarUCL": ucl, "xBarLCL": lcl,
            "rChartCenterLine": rbar, "rUCL": r_ucl, "rLCL": r_lcl,
            "subgroupCount": int(len(means)),
            "flaggedCount": flags, "flaggedXBarCount": flags, "flaggedRangeCount": r_flags,
            "_declare": {"stable": flags == 0 and r_flags == 0}}


def m_xbar_s(b):
    sub, n = _subgroups(b)
    means, sds = sub.mean(axis=1), sub.std(axis=1, ddof=1)
    cl, sbar, c4 = float(means.mean()), float(sds.mean()), _c4(n)
    ucl, lcl = cl + 3 * sbar / (c4 * math.sqrt(n)), cl - 3 * sbar / (c4 * math.sqrt(n))
    flags = _chart_flags(means, cl, ucl, lcl)
    # Same reading as the X-bar/R pair: the S chart is a chart, not a footnote, and the
    # location limits are built out of sbar. B3/B4 are closed-form in c4, so no table.
    _spread = 3.0 * math.sqrt(max(0.0, 1.0 - c4 ** 2)) / c4
    s_ucl, s_lcl = (1.0 + _spread) * sbar, max(0.0, 1.0 - _spread) * sbar
    s_flags = _chart_flags(sds, sbar, s_ucl, s_lcl)
    return {"xBarChartCenterLine": cl, "xBarUCL": ucl, "xBarLCL": lcl,
            "sChartCenterLine": sbar, "sUCL": s_ucl, "sLCL": s_lcl,
            "subgroupCount": int(len(means)),
            "flaggedCount": flags, "flaggedXBarCount": flags, "flaggedSCount": s_flags,
            "_declare": {"stable": flags == 0 and s_flags == 0}}


def _p_series(b):
    d = arr(pick(b, "defectCounts", "defects", "counts"))
    n = arr(pick(b, "sampleSizes", "sampleSize", "subgroupSizes", "inspected"))
    if len(n) == 1 and len(d) > 1:
        n = np.repeat(n, len(d))
    k = min(len(d), len(n))
    if k == 0:
        raise ValueError("no attribute chart data")
    return d[:k], n[:k]


def m_p_chart(b):
    d, n = _p_series(b)
    pbar = float(d.sum() / n.sum())
    sig = np.sqrt(pbar * (1 - pbar) / n)
    props = d / n
    flags = int(sum(1 for i, v in enumerate(props)
                    if v > pbar + 3 * sig[i] or v < max(pbar - 3 * sig[i], 0.0)))
    # `outOfControlCount` is this method's canonical output name; `flaggedCount` is what the
    # other chart families use. Emit both so the oracle satisfies the published vocabulary.
    return {"centerLine": pbar, "meanUCL": float(np.mean(pbar + 3 * sig)),
            "subgroupCount": int(len(d)), "outOfControlCount": flags, "flaggedCount": flags,
            "_declare": {"stable": flags == 0}}


def m_np_chart(b):
    d, n = _p_series(b)
    cl = float(np.mean(d))
    pbar = float(d.sum() / n.sum())
    sig = math.sqrt(cl * (1 - pbar)) if 0 <= pbar <= 1 else float("nan")
    ucl, lcl = cl + 3 * sig, max(cl - 3 * sig, 0.0)
    flags = _chart_flags(d, cl, ucl, lcl)
    return {"centerLine": cl, "ucl": ucl, "lcl": lcl, "flaggedCount": flags,
            "_declare": {"stable": flags == 0}}


def m_c_chart(b):
    c = arr(pick(b, "defectCounts", "counts", "defects"))
    if not len(c):
        raise ValueError("no counts")
    cl = float(np.mean(c))
    sig = math.sqrt(cl)
    flags = _chart_flags(c, cl, cl + 3 * sig, max(cl - 3 * sig, 0.0))
    return {"centerLine": cl, "ucl": cl + 3 * sig, "lcl": max(cl - 3 * sig, 0.0),
            "flaggedCount": flags, "_declare": {"stable": flags == 0}}


def _u_series(b):
    d = arr(pick(b, "defectCounts", "counts", "defects"))
    u = arr(pick(b, "unitCounts", "inspectionUnits", "units"))
    k = min(len(d), len(u))
    if k == 0:
        raise ValueError("no count-rate data")
    return d[:k], u[:k]


def m_u_chart(b):
    d, u = _u_series(b)
    ubar = float(d.sum() / u.sum())
    sig = np.sqrt(ubar / u)
    rates = d / u
    flags = int(sum(1 for i, v in enumerate(rates)
                    if v > ubar + 3 * sig[i] or v < max(ubar - 3 * sig[i], 0.0)))
    return {"processMean": ubar, "centerLine": ubar, "flaggedCount": flags,
            "subgroupCount": int(len(d)), "_declare": {"stable": flags == 0}}


def _sigma_z(z):
    """Laney's over/under-dispersion correction: MR-bar of the z scores over d2."""
    if len(z) < 2:
        return float("nan")
    return float(np.mean(np.abs(np.diff(z))) / _D2[2])


def m_laney_p(b):
    d, n = _p_series(b)
    pbar = float(d.sum() / n.sum())
    sig = np.sqrt(pbar * (1 - pbar) / n)
    z = (d / n - pbar) / sig
    sz = _sigma_z(z)
    flags = int(sum(1 for i, v in enumerate(d / n)
                    if abs(v - pbar) > 3 * sig[i] * sz))
    return {"sigmaZ": sz, "centerLine": pbar, "flaggedCount": flags,
            "_declare": {"stable": flags == 0}}


def m_laney_u(b):
    d, u = _u_series(b)
    ubar = float(d.sum() / u.sum())
    sig = np.sqrt(ubar / u)
    z = (d / u - ubar) / sig
    sz = _sigma_z(z)
    flags = int(sum(1 for i, v in enumerate(d / u) if abs(v - ubar) > 3 * sig[i] * sz))
    return {"sigmaZ": sz, "processMean": ubar, "flaggedCount": flags,
            "_declare": {"stable": flags == 0}}


def m_ewma(b):
    x = arr(pick(b, "data", "values"))
    lam = num(pick(b, "ewmaWeight", "weight"), 0.2) or 0.2
    target = num(pick(b, "target"), float(np.mean(x)))
    sd = within_sd(x)
    z, flags, zs = target, 0, []
    for i, v in enumerate(x, start=1):
        z = lam * v + (1 - lam) * z
        zs.append(z)
        lim = 3 * sd * math.sqrt(lam / (2 - lam) * (1 - (1 - lam) ** (2 * i)))
        if abs(z - target) > lim:
            flags += 1
    return {"flaggedCount": flags, "centerLine": float(target), "lambda": float(lam),
            "finalEwma": float(zs[-1]) if zs else float("nan"),
            "_declare": {"stable": flags == 0}}


def m_cusum(b):
    x = arr(pick(b, "data", "values"))
    sd = within_sd(x)
    target = num(pick(b, "target"), float(np.mean(x)))
    k = (num(pick(b, "kValue"), 0.5) or 0.5) * sd
    h = (num(pick(b, "hValue"), 4.0) or 4.0) * sd
    hi = lo = 0.0
    flags = 0
    for v in x:
        hi = max(0.0, hi + (v - target) - k)
        lo = max(0.0, lo - (v - target) - k)
        if hi > h or lo > h:
            flags += 1
    return {"flaggedCount": flags, "centerLine": float(target),
            "_declare": {"stable": flags == 0}}


def m_normality(b):
    x = arr(pick(b, "data", "values"))
    a2, p = ad_normality(x)
    return {"statistic": a2, "pValue": p, "adPValue": p, "sampleSize": int(len(x)),
            "_declare": {"ad_p": p}}


def m_descriptive(b):
    x = arr(pick(b, "data", "values"))
    a2, p = ad_normality(x)
    return {"mean": float(np.mean(x)), "median": float(np.median(x)),
            "stDev": float(np.std(x, ddof=1)), "skewness": float(stats.skew(x, bias=False)),
            "kurtosis": float(stats.kurtosis(x, bias=False)), "adStatistic": a2,
            "adPValue": p, "sampleSize": int(len(x)), "_declare": {"ad_p": p}}


def m_one_sample_t(b):
    x = arr(pick(b, "data", "values"))
    # `target` is the alias this corpus's run blocks actually use, and defaulting to 0.0 when
    # no hypothesised mean is present tested the process against ZERO. It agreed with the
    # published truth only because a mean far from both the target and zero underflows the
    # p-value to 0 either way; on a process sitting near its target the reference solution
    # would have been wrong and the task unscoreable at its own ceiling. No default now: a
    # one-sample t with no hypothesised mean is not a computation, it is a guess.
    mu = pick(b, "mu", "hypothesizedMean", "target")
    if mu is None:
        raise ValueError("no hypothesised mean in this batch (mu / hypothesizedMean / target)")
    t, p = stats.ttest_1samp(x, num(mu, 0.0))
    return {"tStatistic": float(t), "pValue": float(p), "getPValue": float(p),
            "mean": float(np.mean(x)), "sampleSize": int(len(x))}


def m_two_sample_t(b):
    a = arr(pick(b, "sample1", "group1"))
    c = arr(pick(b, "sample2", "group2"))
    eq = pick(b, "assumeEqualVariances")
    t, p = stats.ttest_ind(a, c, equal_var=bool(eq) if isinstance(eq, bool) else False)
    return {"tStatistic": float(t), "pValue": float(p), "getPValue": float(p),
            "mean1": float(np.mean(a)), "mean2": float(np.mean(c)),
            "difference": float(np.mean(a) - np.mean(c))}


def m_paired_t(b):
    before, after = paired(pick(b, "before"), pick(b, "after"))
    t, p = stats.ttest_rel(before, after)
    return {"tStatistic": float(t), "pValue": float(p), "getPValue": float(p),
            "meanDifference": float(np.mean(before - after)), "pairCount": int(len(before))}


def m_one_proportion(b):
    ev = int(num(pick(b, "events", "successes"), 0) or 0)
    n = int(num(pick(b, "trials", "sampleSize"), 0) or 0)
    p0 = num(pick(b, "hypothesizedP", "hypothesizedProportion"), 0.5) or 0.5
    r = stats.binomtest(ev, n, p0)
    return {"pValue": float(r.pvalue), "sampleProportion": ev / n if n else float("nan"),
            "events": ev, "trials": n}


def m_two_proportions(b):
    e1 = num(pick(b, "events1", "successes1"), 0) or 0
    n1 = num(pick(b, "trials1", "sampleSize1"), 0) or 0
    e2 = num(pick(b, "events2", "successes2"), 0) or 0
    n2 = num(pick(b, "trials2", "sampleSize2"), 0) or 0
    if not n1 or not n2:
        raise ValueError("missing trial counts")
    p1, p2 = e1 / n1, e2 / n2
    pool = (e1 + e2) / (n1 + n2)
    se = math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se if se > 0 else float("inf")
    p = float(2 * stats.norm.sf(abs(z)))
    return {"zStatistic": float(z), "pValue": p, "getPValue": p,
            "proportion1": p1, "proportion2": p2, "difference": p1 - p2}


def m_correlation(b):
    x, y = paired(pick(b, "x"), pick(b, "y"))
    r, p = stats.pearsonr(x, y)
    return {"correlationCoefficient": float(r), "pValue": float(p),
            "sampleSize": int(len(x))}


def m_anova_oneway(b):
    groups = list(group_map(b).values())
    if len(groups) < 2:
        raise ValueError("need at least two groups")
    f, p = stats.f_oneway(*groups)
    return {"fStatistic": float(f), "factorPValue": float(p), "pValue": float(p),
            "groupCount": len(groups)}


def m_equal_variances(b):
    groups = list(group_map(b).values())
    if len(groups) < 2:
        raise ValueError("need at least two groups")
    bs, bp = stats.bartlett(*groups)
    ls, lp = stats.levene(*groups, center="median")
    # HONOUR A DECLARED CONVENTION. Several equal-variance tests are defensible, so a payload
    # that states which one it means has SPECIFIED the answer, and ignoring that is an error by
    # the solver rather than a difference of opinion. Measured on adb_c24 seed 1, whose block
    # declares `varianceTestCentering: median`: Bartlett gives 0.131 where the declared
    # Levene-median gives 0.375, against a 0.08 tolerance. The corpus suppresses the
    # alternative-convention window exactly when the payload declares the convention, so a
    # solver that ignores the declaration has nothing to fall back on -- correctly.
    centring = pick(b, "varianceTestCentering", "varianceTestCentring", "levene_center")
    out = {"bartlettStatistic": float(bs), "bartlettPValue": float(bp),
           "levenePValue": float(lp)}
    if centring is not None:
        c = str(centring).strip().lower()
        c = {"median": "median", "mean": "mean", "trimmed": "trimmed"}.get(c, "median")
        cs, cp = stats.levene(*groups, center=c)
        out["pValue"] = float(cp)
        out["levenePValue"] = float(cp)
        out["leveneStatistic"] = float(cs)
    else:
        out["pValue"] = float(bp)
    return out


def m_sov(b):
    groups = list(group_map(b).values())
    if len(groups) < 2:
        raise ValueError("need at least two groups")
    k = len(groups)
    n = int(np.mean([len(g) for g in groups]))
    grand = float(np.mean(np.concatenate(groups)))
    ms_between = sum(len(g) * (g.mean() - grand) ** 2 for g in groups) / (k - 1)
    ss_within = sum(((g - g.mean()) ** 2).sum() for g in groups)
    df_within = sum(len(g) - 1 for g in groups)
    ms_within = ss_within / df_within
    v_between = max((ms_between - ms_within) / n, 0.0)
    return {"totalVariance": float(v_between + ms_within),
            "betweenVariance": float(v_between), "withinVariance": float(ms_within),
            "percentBetween": float(100 * v_between / (v_between + ms_within))}


def _regression_frame(b):
    data = pick(b, "data")
    if isinstance(data, dict):
        resp = str(pick(b, "responseColumn", "response"))
        preds = [str(p) for p in (pick(b, "continuousPredictors", "predictors") or [])]
        if not preds:
            preds = [k for k in data.keys() if str(k) != resp]
        cols = columns(data, preds + [resp])
        terms = [str(t) for t in (pick(b, "termsInModel") or preds)]
        terms = [t for t in terms if all(p in cols for p in t.split("*"))] or preds
        return cols, terms, resp
    xs, ys = paired(pick(b, "x"), pick(b, "y"))
    name = str(pick(b, "xName", default="x"))
    cols = {name: xs, "__y__": ys}
    deg = int(num(pick(b, "degree"), 1) or 1)
    terms = ["*".join([name] * d) for d in range(1, deg + 1)]
    return cols, terms, "__y__"


def m_ols(b):
    cols, terms, resp = _regression_frame(b)
    y = cols[resp]
    if len(y) < 3:
        raise ValueError("not enough rows")
    design, names = design_from_terms({k: v for k, v in cols.items() if k != resp}, terms)
    fit = ols(design, y)
    # `any_factor_significant` is declared here as well as in m_factorial. A case may screen
    # its candidate factors with OLS instead of a factorial analysis -- adb_c38 does -- and the
    # gate the builder derives from `modelPValue < 0.05` reads that one key whichever method
    # produced it. Without this, the batch behind that gate can never be unlocked by anyone,
    # including the reference solution.
    _sig = bool(math.isfinite(fit["modelPValue"]) and fit["modelPValue"] < 0.05)
    return {"rSquaredPct": 100.0 * fit["rSquared"], "rSquaredAdjPct": 100.0 * fit["rSquaredAdj"],
            "modelPValue": fit["modelPValue"], "fStatistic": fit["fStatistic"],
            "termCount": len(names), "sampleSize": fit["n"],
            "sStdError": math.sqrt(fit["sse"] / fit["dfe"]) if fit["dfe"] > 0 else float("nan"),
            "_declare": {"any_factor_significant": _sig}}


def _irls(design, y, family):
    beta = np.zeros(design.shape[1])
    for _ in range(60):
        eta = design @ beta
        if family == "poisson":
            mu = np.exp(np.clip(eta, -30, 30))
            w, z = mu, eta + (y - mu) / np.maximum(mu, 1e-9)
        else:
            mu = 1.0 / (1.0 + np.exp(-np.clip(eta, -30, 30)))
            v = np.maximum(mu * (1 - mu), 1e-9)
            w, z = v, eta + (y - mu) / v
        wd = design * w[:, None]
        try:
            new = np.linalg.solve(design.T @ wd, design.T @ (w * z))
        except np.linalg.LinAlgError:
            break
        if np.max(np.abs(new - beta)) < 1e-10:
            beta = new
            break
        beta = new
    return beta


def _deviance(y, mu, family):
    if family == "poisson":
        with np.errstate(divide="ignore", invalid="ignore"):
            term = np.where(y > 0, y * np.log(y / np.maximum(mu, 1e-12)), 0.0)
        return float(2 * np.sum(term - (y - mu)))
    mu = np.clip(mu, 1e-12, 1 - 1e-12)
    return float(-2 * np.sum(y * np.log(mu) + (1 - y) * np.log(1 - mu)))


def _glm(b, family):
    x = arr(pick(b, "x"))
    ykey = "counts" if family == "poisson" else "outcomes"
    y = arr(pick(b, ykey, "y"))
    k = min(len(x), len(y))
    x, y = x[:k], y[:k]
    if k < 3:
        raise ValueError("not enough rows")
    design = np.column_stack([np.ones(k), x])
    beta = _irls(design, y, family)
    eta = design @ beta
    mu = np.exp(np.clip(eta, -30, 30)) if family == "poisson" else 1 / (1 + np.exp(-eta))
    dev = _deviance(y, mu, family)
    null_mu = np.full(k, y.mean())
    null_dev = _deviance(y, null_mu, family)
    lr = null_dev - dev
    p = float(stats.chi2.sf(lr, 1)) if lr > 0 else 1.0
    return {"deviance": dev, "nullDeviance": null_dev, "modelPValue": p,
            "pValue": p, "slope": float(beta[1]), "sampleSize": k}


def m_poisson_regression(b):
    return _glm(b, "poisson")


def m_logistic_regression(b):
    return _glm(b, "logistic")


def m_chisq_assoc(b):
    table = pick(b, "contingencyTable", "table")
    mat = np.array([[num(v, 0) or 0 for v in row] for row in table], dtype=float)
    chi2, p, dof, _ = stats.chi2_contingency(mat, correction=False)
    return {"statistic": float(chi2), "chiSquare": float(chi2), "pValue": float(p),
            "degreesOfFreedom": int(dof)}


def m_chisq_gof(b):
    obs = arr(pick(b, "observedCounts", "observed", "counts"))
    exp = pick(b, "expectedCounts", "expected")
    exp = arr(exp) if exp is not None else np.full(len(obs), obs.mean())
    chi2, p = stats.chisquare(obs, f_exp=exp * obs.sum() / exp.sum())
    return {"statistic": float(chi2), "chiSquare": float(chi2), "pValue": float(p),
            "categoryCount": int(len(obs))}


def m_mann_whitney(b):
    a = arr(pick(b, "group1", "sample1"))
    c = arr(pick(b, "group2", "sample2"))
    u, p = stats.mannwhitneyu(a, c, alternative="two-sided")
    return {"statistic": float(u), "pValue": float(p),
            "median1": float(np.median(a)), "median2": float(np.median(c))}


def m_kruskal(b):
    groups = list(group_map(b).values())
    h, p = stats.kruskal(*groups)
    return {"statistic": float(h), "pValue": float(p), "groupCount": len(groups)}


def m_wilcoxon(b):
    x = arr(pick(b, "data", "values"))
    m0 = num(pick(b, "hypothesizedMedian"), 0.0) or 0.0
    s, p = stats.wilcoxon(x - m0)
    return {"statistic": float(s), "pValue": float(p), "median": float(np.median(x))}


def m_moods_median(b):
    groups = list(group_map(b).values())
    s, p, _, _ = stats.median_test(*groups)
    return {"statistic": float(s), "pValue": float(p), "groupCount": len(groups)}


def m_runs_test(b):
    x = arr(pick(b, "data", "values"))
    ref = float(np.mean(x)) if pick(b, "aboutMean", default=True) is not False else float(np.median(x))
    signs = [1 if v > ref else 0 for v in x if v != ref]
    if not signs:
        raise ValueError("no runs")
    runs = 1 + sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])
    n1, n2 = sum(signs), len(signs) - sum(signs)
    if n1 == 0 or n2 == 0:
        raise ValueError("degenerate run sequence")
    mu = 2 * n1 * n2 / (n1 + n2) + 1
    var = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
    z = (runs - mu) / math.sqrt(var) if var > 0 else 0.0
    p = float(2 * stats.norm.sf(abs(z)))
    return {"runs": int(runs), "expectedRuns": float(mu), "zStatistic": float(z),
            "pValue": p, "random": bool(p >= 0.05)}


def _factorial_terms(cols, factors, resp, declared=None):
    """Model terms for a factorial analysis: main effects AND two-factor interactions.

    A 2^k design is run in order to estimate interactions; fitting main effects only fits a
    different model and gets a different R^2. Measured on adb_c11 seed 1, [A,B,C] gives
    R^2 = 71.53 where the design's own [A,B,C,AB,AC,BC] gives 98.34 -- a 27-point gap against
    a 5-point tolerance, which made the reference solution fail its own task.

    An explicit `termsInModel` in the payload always wins: the payload is the specification.
    Otherwise interactions are added only when there are degrees of freedom left to fit them;
    a saturated model has zero residual df and R^2 = 1 by construction, which would be a
    fabricated fit rather than an answer.
    """
    if declared:
        return [str(t) for t in declared]
    if len(factors) < 2:
        return list(factors)
    pairs = ["%s*%s" % (factors[i], factors[j])
             for i in range(len(factors)) for j in range(i + 1, len(factors))]
    n_rows = len(cols[resp])
    if n_rows > len(factors) + len(pairs) + 1:
        return list(factors) + pairs
    return list(factors)


def _doe_frame(b):
    data = pick(b, "data")
    if isinstance(data, dict):
        resp = str(pick(b, "responseColumn", "response"))
        factors = [str(pick(f, "name")) for f in (pick(b, "factors") or [])
                   if isinstance(f, dict)]
        factors = factors or [k for k in data.keys() if str(k) != resp]
        cols = columns(data, factors + [resp])
        terms = _factorial_terms(cols, factors, resp, pick(b, "termsInModel"))
        terms = [t for t in terms if all(p.strip() in cols for p in t.split("*"))] or factors
        return cols, terms, resp, factors
    runs = pick(b, "runs", "surface_data")
    if isinstance(runs, list) and runs and isinstance(runs[0], dict):
        keys = [k for k in runs[0].keys()]
        resp = "y" if "y" in keys else keys[-1]
        factors = [k for k in keys if k != resp]
        cols = {k: np.array([num(r.get(k), float("nan")) for r in runs], dtype=float)
                for k in keys}
        mask = np.all(np.isfinite(np.column_stack([cols[k] for k in keys])), axis=1)
        cols = {k: v[mask] for k, v in cols.items()}
        terms = _factorial_terms(cols, factors, resp, pick(b, "termsInModel"))
        return cols, terms, resp, factors
    raise ValueError("no design matrix")


def _curvature_test(cols, factors, y):
    """Centre points vs factorial points: the whole reason a 2^k carries centre runs.

    A significant difference means the response surface is curved and a first-order model
    will not do — the textbook trigger for augmenting to a central composite design
    (Montgomery, DAOE 6e §11.2). Returns (p_value, n_centre).
    """
    if not factors:
        return float("nan"), 0
    X = np.column_stack([cols[f] for f in factors])
    mid = X.mean(axis=0)
    is_centre = np.all(np.isclose(X, mid), axis=1)
    yc, yf = y[is_centre], y[~is_centre]
    if len(yc) < 2 or len(yf) < 2:
        return float("nan"), int(len(yc))
    _t, p = stats.ttest_ind(yf, yc, equal_var=True)
    return float(p), int(len(yc))


def m_factorial(b):
    cols, terms, resp, factors = _doe_frame(b)
    y = cols[resp]
    design, names = design_from_terms({k: v for k, v in cols.items() if k != resp}, terms)
    fit = ols(design, y)
    sig = bool(math.isfinite(fit["modelPValue"]) and fit["modelPValue"] < 0.05)
    curv_p, n_centre = _curvature_test(cols, factors, y)
    curved = bool(math.isfinite(curv_p) and curv_p < 0.05)
    out = {"rSquaredPct": 100.0 * fit["rSquared"],
           "rSquaredAdjPct": 100.0 * fit["rSquaredAdj"],
           "modelPValue": fit["modelPValue"], "fStatistic": fit["fStatistic"],
           "termCount": len(names), "runCount": fit["n"],
           "_declare": {"any_factor_significant": sig, "curvature_significant": curved}}
    if n_centre:
        out["curvaturePValue"] = curv_p
        out["centrePointCount"] = n_centre
    return out


def _rsm_terms(factors):
    terms = list(factors)
    terms += ["%s*%s" % (f, f) for f in factors]
    for i in range(len(factors)):
        for j in range(i + 1, len(factors)):
            terms.append("%s*%s" % (factors[i], factors[j]))
    return terms


def _lack_of_fit(cols, y, sse, dfe, factors):
    """Pure-error / lack-of-fit F test on EXACT duplicate design points.

    Hand-mirrored from `dmaic_bench.truth.verifiers._lack_of_fit`, under the same rule as the
    guard parser above: the copy is allowed, drifting is not, and
    `test_oracle_mirrors_v2_methods` fails if it does. Without it `m_rsm` emitted no
    `lackOfFitPValue` at all, so a case whose route turns on that field read a missing value,
    fell to the default branch, and the reference solution walked a branch its own scorer calls
    wrong -- measured on a live containerised run of a response-surface case: ceiling 0.777,
    with a decision point scored `incorrect` against the ORACLE. (Identifier omitted: this file
    ships inside every public task. See docs/HELD_OUT_V2.md.)
    """
    if dfe <= 0:
        return {}
    keys = {}
    for i in range(len(y)):
        keys.setdefault(tuple(round(float(cols[n][i]), 12) for n in factors), []).append(i)
    reps = [idx for idx in keys.values() if len(idx) > 1]
    if not reps:
        return {}
    ss_pe = sum(float(np.sum((y[idx] - y[idx].mean()) ** 2)) for idx in reps)
    df_pe = sum(len(idx) - 1 for idx in reps)
    df_lof = dfe - df_pe
    if df_lof <= 0 or df_pe <= 0 or ss_pe <= 0:
        return {}
    ss_lof = sse - ss_pe
    f = (ss_lof / df_lof) / (ss_pe / df_pe)
    return {"lackOfFitPValue": float(stats.f.sf(f, df_lof, df_pe)),
            "lackOfFitF": float(f), "pureErrorDf": float(df_pe)}


def m_rsm(b):
    cols, _, resp, factors = _doe_frame(b)
    y = cols[resp]
    design, names = design_from_terms({k: v for k, v in cols.items() if k != resp},
                                      _rsm_terms(factors))
    fit = ols(design, y)
    out = {"rSquaredPct": 100.0 * fit["rSquared"],
           "rSquaredAdjPct": 100.0 * fit["rSquaredAdj"],
           "modelPValue": fit["modelPValue"], "termCount": len(names),
           "runCount": fit["n"]}
    out.update(_lack_of_fit(cols, y, fit["sse"], fit["dfe"], factors))
    return out


def _quadratic_stationary(cols, factors, resp):
    y = cols[resp]
    design, names = design_from_terms({k: v for k, v in cols.items() if k != resp},
                                      _rsm_terms(factors))
    fit = ols(design, y)
    beta = fit["beta"]
    k = len(factors)
    idx = {n: i + 1 for i, n in enumerate(names)}
    b_lin = np.array([beta[idx[f]] for f in factors])
    B = np.zeros((k, k))
    for i, f in enumerate(factors):
        B[i, i] = beta[idx["%s*%s" % (f, f)]]
    for i in range(k):
        for j in range(i + 1, k):
            key = "%s*%s" % (factors[i], factors[j])
            B[i, j] = B[j, i] = beta[idx[key]] / 2.0
    xs = np.linalg.solve(2 * B, -b_lin)
    pred = float(beta[0] + b_lin @ xs + xs @ B @ xs)
    eig = np.linalg.eigvalsh(B)
    kind = ("maximum" if np.all(eig < 0) else
            "minimum" if np.all(eig > 0) else "saddle")
    return xs, pred, kind, fit


def m_rsm_canonical(b):
    cols, _, resp, factors = _doe_frame(b)
    xs, pred, kind, fit = _quadratic_stationary(cols, factors, resp)
    out = {"predictedAtStationary": pred, "stationaryPointType": kind,
           "rSquaredPct": 100.0 * fit["rSquared"]}
    for f, v in zip(factors, xs):
        out["stationary_" + f] = float(v)
    return out


def m_rsm_optimizer(b):
    cols, _, resp, factors = _doe_frame(b)
    xs, pred, kind, fit = _quadratic_stationary(cols, factors, resp)
    bounds = pick(b, "bounds")
    goal = str(pick(b, "goal", default="maximize")).lower()
    if isinstance(bounds, list) and len(bounds) == len(factors):
        lo = np.array([num(bd[0], -np.inf) for bd in bounds], dtype=float)
        hi = np.array([num(bd[1], np.inf) for bd in bounds], dtype=float)
        clipped = np.clip(xs, lo, hi)
        if not np.allclose(clipped, xs):
            # stationary point outside the operating window: grid-search inside it
            grids = [np.linspace(lo[i], hi[i], 41) for i in range(len(factors))]
            mesh = np.meshgrid(*grids, indexing="ij")
            pts = {f: mesh[i].ravel() for i, f in enumerate(factors)}
            design, _ = design_from_terms(pts, _rsm_terms(factors))
            vals = design @ fit["beta"]
            best = int(np.argmax(vals) if "max" in goal else np.argmin(vals))
            xs = np.array([pts[f][best] for f in factors])
            pred = float(vals[best])
    out = {"predictedResponse": pred, "stationaryPointType": kind}
    for f, v in zip(factors, xs):
        out["optimal_" + f] = float(v)
    return out


def m_factorial_prediction(b):
    source = pick(b, "model_from")
    if source is not None and str(source) in RELEASED:
        model_block = RELEASED[str(source)]
        cols, terms, resp, factors = _doe_frame(model_block)
        points = pick(b, "predictionPoints", "settings") or pick(model_block, "predictionPoints")
        b = dict(model_block)
        b["predictionPoints"] = points
    cols, terms, resp, factors = _doe_frame(b)
    y = cols[resp]
    design, names = design_from_terms({k: v for k, v in cols.items() if k != resp}, terms)
    fit = ols(design, y)
    points = pick(b, "predictionPoints", "settings")
    if isinstance(points, dict):
        points = [points]
    if not points:
        raise ValueError("no prediction point")
    pt = points[0]
    single = {f: np.array([num(pick(pt, f), float("nan"))]) for f in factors}
    if any(not np.isfinite(v[0]) for v in single.values()):
        raise ValueError("prediction point does not name the model's factors")
    xrow, _ = design_from_terms(single, terms)
    pred = float((xrow @ fit["beta"])[0])
    mse = fit["sse"] / fit["dfe"] if fit["dfe"] > 0 else float("nan")
    xtx_inv = np.linalg.pinv(fit["design"].T @ fit["design"])
    lev = float(xrow @ xtx_inv @ xrow.T)
    conf = num(pick(b, "confidenceLevel"), 95.0) or 95.0
    alpha = 1 - conf / 100.0
    tcrit = float(stats.t.ppf(1 - alpha / 2, fit["dfe"])) if fit["dfe"] > 0 else float("nan")
    half = tcrit * math.sqrt(mse * (1 + lev))
    return {"predictedValue": pred, "piLower": pred - half, "piUpper": pred + half,
            "ciLower": pred - tcrit * math.sqrt(mse * lev),
            "ciUpper": pred + tcrit * math.sqrt(mse * lev)}


def m_create_factorial(b):
    factors = pick(b, "factors") or []
    reps = int(num(pick(b, "replicates"), 1) or 1)
    centers = int(num(pick(b, "centerPoints"), 0) or 0)
    k = len(factors)
    base = 2 ** k
    return {"factorCount": k, "baseRuns": base, "replicates": reps,
            "centerPoints": centers, "totalRuns": base * reps + centers,
            "resolution": "full" if k <= 4 else "fractional"}


def m_power_two_proportions(b):
    p1 = num(pick(b, "proportion1", "p1"))
    p2 = pick(b, "proportion2Values", "p2")
    p2 = num(p2[0]) if isinstance(p2, list) and p2 else num(p2)
    n = pick(b, "sampleSizes", "nPerGroup")
    n = num(n[0]) if isinstance(n, list) and n else num(n)
    alpha = num(pick(b, "alpha"), 0.05) or 0.05
    if None in (p1, p2, n):
        raise ValueError("power inputs incomplete")
    # Cohen's ARCSINE effect size, which is the convention the corpus's reference
    # implementation states (statsmodels NormalIndPower with
    # h = 2*asin(sqrt(p1)) - 2*asin(sqrt(p2))). The pooled-SE normal approximation this used
    # to compute is also a defensible power calculation and it is a DIFFERENT one: measured on
    # adb_c38 seed 3, 0.8212 against 0.8372 on a 0.01 tolerance. Where two conventions are both
    # correct, the hand-port follows the one the truth is derived under.
    zc = stats.norm.ppf(1 - alpha / 2)
    h = abs(2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2)))
    arm = h * math.sqrt(n / 2.0)
    power = float(stats.norm.sf(zc - arm) + stats.norm.cdf(-zc - arm))
    return {"power": power, "sampleSizePerGroup": float(n), "alpha": float(alpha),
            "difference": abs(p1 - p2)}


def m_data_profiling(b):
    summary = pick(b, "summary") or {}
    sample = pick(b, "sample") or []
    cols = pick(summary, "columns") or (list(sample[0].keys()) if sample else [])
    return {"columnCount": len(cols), "sampleRows": len(sample),
            "totalRecords": num(pick(summary, "totalRecords"), float(len(sample))),
            "yType": str(pick(summary, "yType", default=""))}


#: stage_id -> payload for every batch the steward has released so far. A few batches carry
#: no data of their own and name an earlier one ("model_from"): the model is refitted from
#: that batch here rather than remembered as a number.
RELEASED = {}


# ------------------------------------------------------------------ second-domain pilot
# Hand-ports of dmaic_bench.truth.omics (RNA-seq and GWAS). Same reason the guard parser is
# copied below: the oracle runs in the agent image, which does not carry the bench package.

def _bh_adjust(p):
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


def _qc_rules(b, **defaults):
    rules = pick(b, "qcRules") or {}
    return {k: num(pick(rules, k), d) for k, d in defaults.items()}


def _sample_rows(b):
    rows = pick(b, "samples") or []
    if not rows or not isinstance(rows[0], dict):
        raise ValueError("samples must be a list of rows")
    return rows


def m_rna_sample_qc(b):
    rows = _sample_rows(b)
    r = _qc_rules(b, minAssignedReads=5.0e6, minMappingRate=0.70)
    failed, kept = 0, {}
    for row in rows:
        reads = num(pick(row, "assignedReads"), 0.0)
        rate = num(pick(row, "mappingRate"), 0.0)
        cond = str(pick(row, "condition"))
        kept.setdefault(cond, 0)
        if reads < r["minAssignedReads"] or rate < r["minMappingRate"]:
            failed += 1
        else:
            kept[cond] += 1
    min_rep = float(min(kept.values())) if kept else 0.0
    return {"failedSamples": float(failed), "passedSamples": float(len(rows) - failed),
            "minReplicates": min_rep, "_declare": {"min_replicates": min_rep}}


def _usable_sample_rows(b):
    rows = _sample_rows(b)
    if not any("assignedReads" in r or "mappingRate" in r for r in rows):
        return rows
    r = _qc_rules(b, minAssignedReads=5.0e6, minMappingRate=0.70)
    keep = [row for row in rows
            if num(pick(row, "assignedReads"), 0.0) >= r["minAssignedReads"]
            and num(pick(row, "mappingRate"), 0.0) >= r["minMappingRate"]]
    if not keep:
        raise ValueError("no usable libraries")
    return keep


def m_design_identifiability(b):
    rows = _usable_sample_rows(b)
    conds = sorted({str(pick(r, "condition")) for r in rows})
    batches = sorted({str(pick(r, "batch")) for r in rows})
    if len(conds) != 2:
        raise ValueError("expected exactly two conditions")
    n = len(rows)
    cols = [np.ones(n), np.array([1.0 if str(pick(r, "condition")) == conds[1] else 0.0
                                  for r in rows])]
    for bt in batches[1:]:
        cols.append(np.array([1.0 if str(pick(r, "batch")) == bt else 0.0 for r in rows]))
    x = np.column_stack(cols)
    rank = int(np.linalg.matrix_rank(x))
    confounded = rank < x.shape[1]
    return {"confounded": 1.0 if confounded else 0.0, "batchCount": float(len(batches)),
            "designRank": float(rank), "designColumns": float(x.shape[1]),
            "usableSamples": float(n),
            "_declare": {"design_confounded": bool(confounded)}}


def _counts_frame(b):
    counts = pick(b, "counts")
    m = np.asarray(counts, dtype=float)
    cond = [str(c) for c in (pick(b, "condition") or [])]
    batch = pick(b, "batch")
    batch = [str(v) for v in batch] if isinstance(batch, (list, tuple)) and \
        len(batch) == m.shape[1] else ["B1"] * m.shape[1]
    if m.ndim != 2 or len(cond) != m.shape[1]:
        raise ValueError("counts must be gene x sample with a condition per sample")
    lib = m.sum(axis=0)
    lib[lib <= 0] = 1.0
    x = np.log2(m / lib * 1.0e6 + 1.0)
    declared = pick(b, "conditions")
    if isinstance(declared, (list, tuple)) and len(declared) == 2:
        a, bb = str(declared[0]), str(declared[1])
    else:
        lv = sorted(set(cond))
        a, bb = lv[0], lv[1]
    pt = num(pick(b, "padjThreshold"), 0.05)
    lt = num(pick(b, "log2fcThreshold"), 1.0)
    return x, cond, batch, a, bb, pt, lt


def m_batch_assessment(b):
    x, _cond, batch, _a, _bb, _pt, _lt = _counts_frame(b)
    xs = x.T - x.T.mean(axis=0, keepdims=True)
    _u, s, vt = np.linalg.svd(xs, full_matrices=False)
    pc1 = xs @ vt[0]
    total = float(np.sum((pc1 - pc1.mean()) ** 2))
    between = 0.0
    for lv in sorted(set(batch)):
        idx = [i for i, v in enumerate(batch) if v == lv]
        between += len(idx) * (pc1[idx].mean() - pc1.mean()) ** 2
    return {"batchVarianceFraction": float(between / total) if total > 0 else 0.0,
            "pc1VarianceFraction": float(s[0] ** 2 / np.sum(s ** 2)),
            "batchCount": float(len(set(batch)))}


def m_de_simple(b):
    x, cond, _batch, a, bb, pt, lt = _counts_frame(b)
    ia = [i for i, c in enumerate(cond) if c == a]
    ib = [i for i, c in enumerate(cond) if c == bb]
    _t, p = stats.ttest_ind(x[:, ib], x[:, ia], axis=1, equal_var=False)
    p = np.nan_to_num(np.asarray(p, dtype=float), nan=1.0)
    lfc = x[:, ib].mean(axis=1) - x[:, ia].mean(axis=1)
    sig = (_bh_adjust(p) < pt) & (np.abs(lfc) >= lt)
    return {"nSignificant": float(int(sig.sum())), "nTested": float(x.shape[0]),
            "nUp": float(int((sig & (lfc > 0)).sum())),
            "nDown": float(int((sig & (lfc < 0)).sum()))}


def m_de_blocked(b):
    x, cond, batch, _a, bb, pt, lt = _counts_frame(b)
    xt = x.T
    n = xt.shape[0]
    cols = [np.ones(n), np.array([1.0 if c == bb else 0.0 for c in cond])]
    for lv in sorted(set(batch))[1:]:
        cols.append(np.array([1.0 if v == lv else 0.0 for v in batch]))
    d = np.column_stack(cols)
    pc = d.shape[1]
    if np.linalg.matrix_rank(d) < pc:
        raise ValueError("design is not full rank: condition is confounded with batch")
    xtx_inv = np.linalg.inv(d.T @ d)
    beta = xtx_inv @ d.T @ xt
    resid = xt - d @ beta
    df = n - pc
    sigma2 = (resid ** 2).sum(axis=0) / df
    se = np.sqrt(np.maximum(sigma2 * xtx_inv[1, 1], 1e-300))
    pval = 2.0 * stats.t.sf(np.abs(beta[1] / se), df)
    sig = (_bh_adjust(pval) < pt) & (np.abs(beta[1]) >= lt)
    return {"nSignificant": float(int(sig.sum())), "nTested": float(xt.shape[1]),
            "batchTermCount": float(pc - 2), "residualDf": float(df)}


def _geno_frame(b):
    g = pick(b, "genotypes")
    m = np.array([[np.nan if v is None else float(v) for v in row] for row in g], dtype=float)
    y = np.array([1.0 if num(v, 0.0) >= 0.5 else 0.0 for v in (pick(b, "phenotype") or [])])
    if m.ndim != 2 or y.size != m.shape[0]:
        raise ValueError("genotypes must be sample x variant with a phenotype per sample")
    r = _qc_rules(b, minSampleCallRate=0.95, minVariantCallRate=0.95, minMaf=0.01,
                  minHwePControls=1.0e-6, alpha=0.05)
    return m, y, r


def _hwe_chi_p(gen):
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
    return float(stats.chi2.sf(float(np.sum((obs - exp) ** 2 / np.maximum(exp, 1e-12))), 1))


def _geno_keep(m, y, r):
    call_s = 1.0 - np.isnan(m).mean(axis=1)
    keep_s = call_s >= r["minSampleCallRate"]
    ms, ys = m[keep_s], y[keep_s]
    call_v = 1.0 - np.isnan(ms).mean(axis=0)
    freq = np.nanmean(ms, axis=0) / 2.0
    maf = np.minimum(freq, 1.0 - freq)
    hwe = np.array([_hwe_chi_p(ms[ys == 0, j]) for j in range(ms.shape[1])])
    keep_v = (call_v >= r["minVariantCallRate"]) & (maf >= r["minMaf"]) & \
        (hwe >= r["minHwePControls"])
    return keep_s, keep_v, call_s


def m_gwas_sample_qc(b):
    m, y, r = _geno_frame(b)
    keep_s, _kv, call_s = _geno_keep(m, y, r)
    failed = int((~keep_s).sum())
    frac = float(failed / m.shape[0])
    return {"samplesFailed": float(failed), "sampleFailFraction": frac,
            "samplesRetained": float(int(keep_s.sum())), "minSampleCallRate": float(call_s.min()),
            "_declare": {"sample_fail_fraction": frac}}


def m_gwas_snp_qc(b):
    m, y, r = _geno_frame(b)
    keep_s, keep_v, _c = _geno_keep(m, y, r)
    return {"snpsFailed": float(int((~keep_v).sum())), "snpsRetained": float(int(keep_v.sum())),
            "samplesRetained": float(int(keep_s.sum()))}


def _geno_pcs(x, k=2):
    x = x.copy()
    freq = np.nanmean(x, axis=0) / 2.0
    for j in range(x.shape[1]):
        col = x[:, j]
        col[np.isnan(col)] = 2.0 * freq[j]
    sd = np.sqrt(np.maximum(2.0 * freq * (1.0 - freq), 1e-12))
    x = (x - 2.0 * freq) / sd
    x = x - x.mean(axis=0, keepdims=True)
    u, s, _vt = np.linalg.svd(x, full_matrices=False)
    return u[:, :k] * s[:k], s


def m_gwas_stratification(b):
    m, y, r = _geno_frame(b)
    keep_s, keep_v, _c = _geno_keep(m, y, r)
    x, ys = m[keep_s][:, keep_v], y[keep_s]
    scores, s = _geno_pcs(x, 2)
    axis, pvals = 0.0, []
    for k in range(2):
        pc = scores[:, k]
        cases, ctrls = pc[ys == 1], pc[ys == 0]
        _t, p = stats.ttest_ind(cases, ctrls, equal_var=False)
        pvals.append(float(p))
        if axis == 0.0 and (cases.max() < ctrls.min() or ctrls.max() < cases.min()):
            axis = float(k + 1)
    return {"separated": 1.0 if axis else 0.0, "separatedAxis": axis,
            "pc1PValue": pvals[0], "pc2PValue": pvals[1],
            "pc1VarianceFraction": float(s[0] ** 2 / np.sum(s ** 2)),
            "_declare": {"pc1_separated": bool(axis)}}


def m_gwas_association_trend(b):
    m, y, r = _geno_frame(b)
    keep_s, keep_v, _c = _geno_keep(m, y, r)
    x, ys = m[keep_s][:, keep_v], y[keep_s]
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
    thr = r["alpha"] / max(x.shape[1], 1)
    return {"nSignificant": float(int((p < thr).sum())), "nTested": float(x.shape[1]),
            "lambdaGC": float(np.median(chi) / 0.4549364), "minPValue": float(p.min())}


def _logit_wald_z(design, y, col):
    beta = np.zeros(design.shape[1])
    for _ in range(50):
        mu = 1.0 / (1.0 + np.exp(-(design @ beta)))
        w = mu * (1.0 - mu)
        if np.all(w < 1e-10):
            break
        h = np.linalg.inv((design.T * w) @ design + 1e-9 * np.eye(design.shape[1]))
        step = h @ (design.T @ (y - mu))
        beta = beta + step
        if np.max(np.abs(step)) < 1e-8:
            break
    mu = 1.0 / (1.0 + np.exp(-(design @ beta)))
    w = mu * (1.0 - mu)
    h = np.linalg.inv((design.T * w) @ design + 1e-9 * np.eye(design.shape[1]))
    return float(beta[col] / math.sqrt(max(h[col, col], 1e-300)))


def m_gwas_association_adjusted(b):
    m, y, r = _geno_frame(b)
    keep_s, keep_v, _c = _geno_keep(m, y, r)
    x, ys = m[keep_s][:, keep_v], y[keep_s]
    pcs, _s = _geno_pcs(x, 2)
    chi = []
    for j in range(x.shape[1]):
        col = x[:, j]
        ok = ~np.isnan(col)
        if ok.sum() < 10 or np.std(col[ok]) == 0:
            chi.append(0.0)
            continue
        d = np.column_stack([np.ones(int(ok.sum())), col[ok], pcs[ok, 0], pcs[ok, 1]])
        z = _logit_wald_z(d, ys[ok], 1)
        chi.append(z * z)
    chi = np.asarray(chi)
    p = stats.chi2.sf(chi, 1)
    thr = r["alpha"] / max(x.shape[1], 1)
    return {"nSignificant": float(int((p < thr).sum())), "nTested": float(x.shape[1]),
            "lambdaGC": float(np.median(chi) / 0.4549364), "covariateCount": 2.0,
            "minPValue": float(p.min())}


def m_validation_concordance(b):
    genes = pick(b, "genes") or []
    qpcr = pick(b, "qpcr") or {}
    direction = pick(b, "expectedDirection") or {}
    rule = pick(b, "rule") or {}
    alpha = num(pick(rule, "alpha"), 0.05)
    if not genes:
        raise ValueError("no nominated candidates")
    confirmed = 0
    for g in genes:
        blk = qpcr.get(g) or {}
        a = arr(pick(blk, "control")); bb = arr(pick(blk, "treated"))
        if a.size < 2 or bb.size < 2:
            continue
        _t, p = stats.ttest_ind(bb, a, equal_var=False)
        want = str(direction.get(g, "")).lower()
        sign = "up" if bb.mean() > a.mean() else "down"
        if p < alpha and (not want or want == sign):
            confirmed += 1
    conc = float(confirmed / len(genes))
    return {"concordance": conc, "nConfirmed": float(confirmed), "nTested": float(len(genes)),
            "_declare": {"validation_concordance": conc}}


def _called_genes_from_counts():
    """The genes this run's own comparison called, from the released counts batch."""
    cb = RELEASED.get("counts")
    if not cb:
        raise ValueError("counts were not released; nothing to enrich")
    x, cond, batch, a, bb, pt, lt = _counts_frame(cb)
    genes = [str(g) for g in (pick(cb, "genes") or [])]
    if len(set(batch)) > 1:
        xt = x.T
        n = xt.shape[0]
        cols = [np.ones(n), np.array([1.0 if c == bb else 0.0 for c in cond])]
        for lv in sorted(set(batch))[1:]:
            cols.append(np.array([1.0 if v == lv else 0.0 for v in batch]))
        d = np.column_stack(cols)
        xtx_inv = np.linalg.inv(d.T @ d)
        beta = xtx_inv @ d.T @ xt
        resid = xt - d @ beta
        df = n - d.shape[1]
        se = np.sqrt(np.maximum(((resid ** 2).sum(axis=0) / df) * xtx_inv[1, 1], 1e-300))
        p = 2.0 * stats.t.sf(np.abs(beta[1] / se), df)
        lfc = beta[1]
    else:
        ia = [i for i, c in enumerate(cond) if c == a]
        ib = [i for i, c in enumerate(cond) if c == bb]
        _t, p = stats.ttest_ind(x[:, ib], x[:, ia], axis=1, equal_var=False)
        p = np.nan_to_num(np.asarray(p, dtype=float), nan=1.0)
        lfc = x[:, ib].mean(axis=1) - x[:, ia].mean(axis=1)
    sig = (_bh_adjust(p) < pt) & (np.abs(lfc) >= lt)
    return [genes[i] for i in np.where(sig)[0]]


def m_enrichment(b):
    sets = pick(b, "sets") or {}
    universe = int(num(pick(b, "universe"), 0.0) or 0)
    rule = pick(b, "rule") or {}
    alpha = num(pick(rule, "alpha"), 0.05)
    called = set(_called_genes_from_counts())
    if not sets:
        raise ValueError("no gene sets")
    if universe <= 0:
        universe = len({g for m in sets.values() for g in m} | called)
    n = len(called)
    pv = []
    for members in sets.values():
        m = set(map(str, members))
        k = len(m & called)
        pv.append(float(stats.hypergeom.sf(k - 1, universe, len(m), n)) if n else 1.0)
    padj = _bh_adjust(np.asarray(pv))
    return {"nSignificantSets": float(int((padj < alpha).sum())), "nSets": float(len(sets)),
            "nCalled": float(n)}


def _replication_frame(b):
    m, y, _r = _geno_frame(b)
    variants = [str(v) for v in (pick(b, "variants") or [])]
    cands = [str(v) for v in (pick(b, "candidateVariants") or [])]
    direction = pick(b, "discoveryDirection") or {}
    rule = pick(b, "qcRules") or pick(b, "rule") or {}
    alpha = num(pick(rule, "alpha"), 0.05)
    return m, y, variants, cands, direction, alpha


def _replicates(m, y, variants, v, direction, alpha):
    if v not in variants:
        return None
    col = m[:, variants.index(v)]
    ok = ~np.isnan(col)
    g, yy = col[ok], y[ok]
    if g.size < 10 or np.std(g) == 0 or np.std(yy) == 0:
        return None
    rho = float(np.corrcoef(g, yy)[0, 1])
    p = float(stats.chi2.sf(g.size * rho * rho, 1))
    want = num(direction.get(v), 0.0) or 0.0
    if p < alpha and (want == 0.0 or np.sign(rho) == np.sign(want)):
        return g, yy
    return None


def m_gwas_replication(b):
    m, y, variants, cands, direction, alpha = _replication_frame(b)
    if not cands:
        raise ValueError("no candidate variants nominated")
    rep = sum(1 for v in cands if _replicates(m, y, variants, v, direction, alpha) is not None)
    return {"nReplicated": float(rep), "nCandidates": float(len(cands)),
            "replicationFraction": float(rep / len(cands))}


def m_gwas_effect_estimate(b):
    m, y, variants, cands, direction, alpha = _replication_frame(b)
    for v in cands:
        hit = _replicates(m, y, variants, v, direction, alpha)
        if hit is None:
            continue
        g, yy = hit
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
                "ciUpper": float(math.exp(beta[1] + 1.959964 * se)), "variant": v}
    raise ValueError("no replicated candidate to estimate")


METHODS = {
    "expression.validation_concordance": m_validation_concordance,
    "expression.enrichment": m_enrichment,
    "gwas.replication": m_gwas_replication,
    "gwas.effect_estimate": m_gwas_effect_estimate,
    "qc.sample_qc": m_rna_sample_qc,
    "design.identifiability": m_design_identifiability,
    "expression.batch_assessment": m_batch_assessment,
    "expression.de_simple": m_de_simple,
    "expression.de_blocked": m_de_blocked,
    "gwas.sample_qc": m_gwas_sample_qc,
    "gwas.snp_qc": m_gwas_snp_qc,
    "gwas.stratification": m_gwas_stratification,
    "gwas.association_trend": m_gwas_association_trend,
    "gwas.association_adjusted": m_gwas_association_adjusted,
    "meta.data_profiling": m_data_profiling,
    "msa.gage_rr_crossed": m_gage_rr,
    "msa.attribute_agreement": m_attribute_agreement,
    "basic.descriptive_summary": m_descriptive,
    "basic.normality": m_normality,
    "basic.one_sample_t": m_one_sample_t,
    "basic.two_sample_t": m_two_sample_t,
    "basic.paired_t": m_paired_t,
    "basic.one_proportion": m_one_proportion,
    "basic.two_proportions": m_two_proportions,
    "basic.correlation": m_correlation,
    "anova.oneway": m_anova_oneway,
    "anova.equal_variances": m_equal_variances,
    "anova.sov": m_sov,
    "capability.normal": m_normal_capability,
    "capability.nonnormal": m_nonnormal_capability,
    "capability.grouped": m_grouped_capability,
    "capability.binomial": m_binomial_capability,
    "capability.poisson": m_poisson_capability,
    "control_chart.imr": m_imr,
    "control_chart.xbar_r": m_xbar_r,
    "control_chart.xbar_s": m_xbar_s,
    "control_chart.ewma": m_ewma,
    "control_chart.cusum": m_cusum,
    "control_chart.p": m_p_chart,
    "control_chart.np": m_np_chart,
    "control_chart.laney_p": m_laney_p,
    "control_chart.u": m_u_chart,
    "control_chart.c": m_c_chart,
    "control_chart.laney_u": m_laney_u,
    "doe.create_factorial": m_create_factorial,
    "doe.factorial_analysis": m_factorial,
    "doe.factorial_prediction": m_factorial_prediction,
    "doe.rsm_analysis": m_rsm,
    "doe.rsm_canonical": m_rsm_canonical,
    "doe.rsm_optimizer": m_rsm_optimizer,
    "regression.ols": m_ols,
    "regression.binary_logistic": m_logistic_regression,
    "regression.poisson": m_poisson_regression,
    "nonparametric.mann_whitney": m_mann_whitney,
    "nonparametric.kruskal_wallis": m_kruskal,
    "nonparametric.one_sample_wilcoxon": m_wilcoxon,
    "nonparametric.moods_median": m_moods_median,
    "nonparametric.runs_test": m_runs_test,
    "quality.pareto": m_pareto,
    "quality.fmea_rpn": m_fmea,
    "tables.chisquare_assoc": m_chisq_assoc,
    "tables.chisquare_gof": m_chisq_gof,
    "power.two_proportions": m_power_two_proportions,
}


# ------------------------------------------------------------------ guard DSL (v2 routing)
#
# A hand-port of dmaic_bench.core.graph's recursive-descent guard parser. The oracle cannot
# import the bench package -- it runs inside the AGENT container, which deliberately does not
# carry it -- so the parser travels here, and `test_oracle_mirrors_guard_dsl` pins the two
# implementations to the same answers on the same expressions.
#
# NO eval(), for the same reason the original has none: these expressions come out of plan.json
# and a plan is data, not code.
import re as _re

_TOK = _re.compile(r"""
    \s*(?:
      (?P<num>-?\d+\.?\d*(?:[eE][-+]?\d+)?)
    | (?P<str>'[^']*'|"[^"]*")
    | (?P<op>>=|<=|==|!=|>|<)
    | (?P<lb>\[) | (?P<rb>\]) | (?P<lp>\() | (?P<rp>\)) | (?P<comma>,)
    | (?P<ident>[A-Za-z_][A-Za-z0-9_.]*)
    )
""", _re.VERBOSE)
_KEYWORDS = {"and", "or", "not", "in", "true", "false"}
_MISSING = object()


class _Enum(object):
    def __init__(self, name):
        self.name = name


def _tokenize(expr):
    toks, pos = [], 0
    while pos < len(expr):
        m = _TOK.match(expr, pos)
        if not m or m.end() == pos:
            if expr[pos:].strip() == "":
                break
            raise ValueError("guard parse error near %r" % expr[pos:])
        pos = m.end()
        toks.append((m.lastgroup, m.group(m.lastgroup)))
    toks.append(("end", ""))
    return toks


def _resolve_field(path, results):
    if path in results:
        return results[path]
    cur = results
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return _MISSING
    return cur


class _Guard(object):
    def __init__(self, toks, results):
        self.toks, self.i, self.results = toks, 0, results

    def _peek(self):
        return self.toks[self.i]

    def _next(self):
        t = self.toks[self.i]
        self.i += 1
        return t

    def parse(self):
        v = self._or()
        if self._peek()[0] != "end":
            raise ValueError("trailing tokens")
        return bool(v)

    def _or(self):
        # The right operand is CONSUMED before it is combined. Writing this as
        # `v = bool(v) or bool(self._and())` short-circuits in Python, so on a true left operand
        # the right one is never parsed, the tokens are left over, and the whole guard raises --
        # which `guard_holds` turns into False. `a or b` then evaluated to False whenever `a`
        # was true. Caught by test_oracle_mirrors_guard_dsl, which is why that test exists.
        v = self._and()
        while self._peek() == ("ident", "or"):
            self._next()
            r = self._and()
            v = bool(v) or bool(r)
        return v

    def _and(self):
        v = self._not()
        while self._peek() == ("ident", "and"):
            self._next()
            r = self._not()
            v = bool(v) and bool(r)
        return v

    def _not(self):
        if self._peek() == ("ident", "not"):
            self._next()
            return not bool(self._not())
        return self._primary()

    def _primary(self):
        kind, _val = self._peek()
        if kind == "lp":
            self._next()
            v = self._or()
            if self._next()[0] != "rp":
                raise ValueError("expected )")
            return v
        return self._comparison()

    def _comparison(self):
        left = self._value()
        kind, val = self._peek()
        if kind == "op":
            self._next()
            return self._apply(val, left, self._value())
        if (kind, val) == ("ident", "in"):
            self._next()
            return any(self._eq(left, m) for m in self._list())
        if left is _MISSING:
            return False
        return bool(left)

    def _list(self):
        if self._next()[0] != "lb":
            raise ValueError("expected [")
        members = []
        if self._peek()[0] != "rb":
            members.append(self._value())
            while self._peek()[0] == "comma":
                self._next()
                members.append(self._value())
        if self._next()[0] != "rb":
            raise ValueError("expected ]")
        return members

    def _value(self):
        kind, val = self._next()
        if kind == "num":
            return float(val)
        if kind == "str":
            return val[1:-1]
        if kind == "ident":
            low = val.lower()
            if low == "true":
                return True
            if low == "false":
                return False
            if val in _KEYWORDS:
                raise ValueError("unexpected keyword %r" % val)
            resolved = _resolve_field(val, self.results)
            return resolved if resolved is not _MISSING else _Enum(val)
        raise ValueError("unexpected token")

    @staticmethod
    def _eq(a, b):
        a = a.name if isinstance(a, _Enum) else a
        b = b.name if isinstance(b, _Enum) else b
        try:
            return float(a) == float(b)
        except (TypeError, ValueError):
            return str(a) == str(b)

    def _apply(self, op, a, b):
        if a is _MISSING or b is _MISSING:
            return False
        if op == "==":
            return self._eq(a, b)
        if op == "!=":
            return not self._eq(a, b)
        try:
            a = float(a.name if isinstance(a, _Enum) else a)
            b = float(b.name if isinstance(b, _Enum) else b)
        except (TypeError, ValueError):
            return False
        return {">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}[op]


def guard_holds(expr, results):
    """Evaluate one edge guard against the results THIS RUN computed. Missing field -> False."""
    if not expr or not expr.strip():
        return True
    try:
        return _Guard(_tokenize(expr), results or {}).parse()
    except ValueError:
        return False


def _norm_key(name):
    return "".join(c for c in str(name).lower() if c.isalnum())


def _set_dotted(target, dotted, value):
    parts = dotted.split(".")
    cur = target
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    cur[parts[-1]] = value


def harvest(field_map, outputs_by_method, observed, outputs_by_occurrence=None):
    """Fold this run's OWN outputs into the dotted namespace the guards read.

    This is what makes the reference solution a derivation rather than a replay: it holds the
    graph, but the value each guard sees is the number this run just computed, scaled into the
    units the guard is written in.

    A source may pin itself to one INVOCATION of its method with "occurrence": n. Without that,
    `outputs_by_method` is last-wins and a project that runs a method twice on purpose -- two
    agreement studies, one before a repair and one after; two characteristics charted and
    assessed separately -- has the second answer standing in for the first. Every guard reading
    the first then routes on the wrong number. Measured on a live run before this existed:
    adb_c35 seed 3 took the wrong branch out of its capability fork because cap1.cpk and
    cap2.cpk resolved to the same value.
    """
    for dotted, sources in (field_map or {}).items():
        for src in sources or []:
            occurrence = src.get("occurrence")
            if occurrence is None:
                outs = outputs_by_method.get(src.get("method_id"))
            else:
                try:
                    outs = (outputs_by_occurrence or {}).get(
                        (src.get("method_id"), int(occurrence)))
                except (TypeError, ValueError):
                    outs = None
            if not outs:
                continue
            want = _norm_key(src.get("output"))
            hit = None
            for key, val in outs.items():
                if _norm_key(key) == want:
                    hit = val
                    break
            if hit is None:
                continue
            try:
                _set_dotted(observed, dotted, float(hit) * float(src.get("scale") or 1.0))
            except (TypeError, ValueError):
                pass
            break
    return observed


def observe_batch(node, payload, observed):
    """Read a STRUCTURAL fact off a released batch and fold it into the guard namespace.

    Some forks turn on a property of the data rather than on a statistic: whether the subgroup
    sizes are constant decides which attribute chart is admissible, and no method in the
    taxonomy reports it. The plan says which key to look at and what to check; the answer comes
    from the batch this run was handed.
    """
    if not isinstance(payload, dict):
        return observed
    for rule in node.get("observe") or []:
        values = pick(payload, rule.get("key"))
        if not isinstance(values, (list, tuple)) or not values:
            continue
        kind = rule.get("kind", "varies")
        if kind == "varies":
            value = 1.0 if len({num(v) for v in values}) > 1 else 0.0
        elif kind == "distinct_count":
            value = float(len({num(v) for v in values}))
        elif kind == "count":
            value = float(len(values))
        elif kind == "min":
            value = float(min(num(v) for v in values))
        elif kind == "max":
            value = float(max(num(v) for v in values))
        else:
            continue
        _set_dotted(observed, rule["field"], value)
    return observed


def methods_at(node, policy, observed):
    """The methods this node calls for, GIVEN what this run has observed so far.

    A node with a policy clause is one whose admissible method depends on the data (the
    distribution decides which capability index is the right one). The plan carries the RULE;
    the branch is taken here, from this run's own numbers.
    """
    clauses = (policy or {}).get(node["key"])
    if not clauses:
        return list(node.get("methods") or [])
    default = None
    for clause in clauses:
        when = clause.get("when")
        if not when:
            default = clause
            continue
        if guard_holds(when, observed):
            return list(clause.get("methods") or [])
    return list((default or {}).get("methods") or [])


# ------------------------------------------------------------------ the data steward

class Steward:
    """Talks to the steward the way an agent would: CLI first, HTTP second."""

    def __init__(self, plan):
        self.plan = plan
        self.base = plan["steward_base"]
        self.cli = plan.get("steward_cli")
        self.data_dir = plan.get("data_dir") or "/workspace/data"
        self.budget = int(plan.get("max_turns", 20))
        self.turns = 0
        self.requests = 0
        self.notes = []
        self._offline = None

    def _run_cli(self, args):
        """`steward --json <action> …` — the same channel the instruction gives the agent."""
        if not self.cli or not os.path.exists(self.cli):
            return None
        try:
            out = subprocess.run([self.cli, "--json"] + args, capture_output=True,
                                 text=True, timeout=60)
        except (OSError, subprocess.SubprocessError):
            return None
        text = (out.stdout or "").strip()
        if not text:
            return None
        try:
            return json.loads(text)
        except ValueError:
            return None

    def _post(self, path, payload):
        req = urllib.request.Request(
            self.base + path, method="POST",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        try:
            with _OPENER.open(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, OSError, ValueError):
            return None

    def wait(self, seconds=30):
        for _ in range(seconds * 2):
            try:
                with _OPENER.open(self.base + "/status", timeout=2) as r:
                    r.read()
                    return True
            except Exception:
                time.sleep(0.5)
        return False

    def request(self, step):
        """Ask for one batch. Returns (payload, refusal_code)."""
        L = strings(self.plan)
        topics = step.get("topics") or []
        phrase = L["topic_join"].join(topics) if topics else step["stage_id"]
        query = L["query"] % phrase
        self.requests += 1
        res = self._run_cli(["request", query]) or self._post("/request", {"text": query})
        if res is None:
            return None, "offline"
        # The running service answers with {action, ok, outcome, refusal, gate, stage_id,
        # message, turns_used, max_turns, seq}; spec.STEWARD_REPLY_FIELDS documents a
        # kind/payload shape instead, so accept both and prefer whichever is present.
        self.turns = int(res.get("turns_used", self.turns) or 0)
        outcome = res.get("outcome") or res.get("kind")
        if outcome == "data":
            if res.get("payload") is not None:
                return res["payload"], None
            # `message` is a truncated preview; the full batch is a JSON file on disk.
            sid = res.get("stage_id") or step["stage_id"]
            path = os.path.join(self.data_dir, "%s.json" % sid)
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    return json.load(f), None
            return None, "unreadable"
        return None, str(res.get("refusal") or res.get("kind") or "unroutable")

    def declare(self, key, value):
        """Report a computed verdict. Booleans go over as `true`/`false`, which is what a
        fork's branch names are keyed on."""
        as_text = ("true" if value else "false") if isinstance(value, bool) else str(value)
        if self._run_cli(["declare", str(key), as_text]) is None:
            self._post("/declare", {"key": key, "value": value})


def _fallback_blocks(plan):
    """If the steward is not reachable, read the batch file the image ships.

    This is a degraded mode, loudly recorded in the trace notes: the oracle exists to show
    the analysis is derivable, and it must still produce a trace when the service is down.
    """
    path = plan.get("blocks_fallback")
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


# ------------------------------------------------------------------ output assembly

_ALIASES = {
    "getpvalue": "pValue", "factorpvalue": "pValue", "modelpvalue": "pValue",
    "chisquare": "statistic", "adpvalue": "pValue",
}


def fill_expected(outputs, expected):
    """Give a computed value the name the scorer looks for. Renaming only — never a value."""
    lower = {k.lower(): k for k in outputs}
    for field in expected:
        if field in outputs:
            continue
        f = field.lower()
        src = None
        if f in lower:
            src = lower[f]
        elif _ALIASES.get(f, "").lower() in lower:
            src = lower[_ALIASES[f].lower()]
        else:
            for k in outputs:
                kl = k.lower()
                if kl.endswith(f) or f.endswith(kl):
                    src = k
                    break
        if src is not None:
            outputs[field] = outputs[src]
    return outputs


# --------------------------------------------------------------------------- report strings
# Preserve the established English request and disclosure wording: the honesty scorer reads
# the report's gap section to determine whether unavailable evidence was acknowledged.
_STRINGS = {
    "en": {
        "topic_join": ", ",
        "query": "please provide the %s batch of shop-floor data",
        "yes": "yes", "no": "no", "na": "not available",
        "refused": "the data steward did not provide this batch (%s), so this step could not be computed",
        "not_implemented": "this environment has no implementation for this step",
        "compute_failed": "the computation failed: %s",
        "title": "# Project analysis report",
        "preamble": ("Task `%s`. Every number in this report was computed on this run and is "
                     "recorded step by step in `%s`; where nothing was computed, this report "
                     "gives no number and no conclusion."),
        "notes": "> Run notes: ",
        "notes_join": "; ",
        "h_done": "## 1. Analyses completed",
        "none_done": "No step of this run produced a usable result.",
        "stage_head": "### %s (%s phase)",
        "kv": "- %s: %s",
        "h_gaps": "## 2. Steps left without a conclusion",
        "gaps_intro": ("The following steps produced no usable result. This report makes **no "
                       "guess** about them; the judgement stops here:"),
        "gap_refused": ("- %s: the data was checked by the steward and is not available (%s), "
                        "so this step was not completed."),
        "gap_failed": "- %s: the computation could not be completed (%s).",
        "h_routes": "## 3. Choices made at the decisive forks",
        "h_conclusion": "## 4. Conclusion",
        "conc_ok": "Every item above was computed on this run from the data provided.",
        "conc_none": "This run produced no computed result at all.",
        "conc_gaps": ("Gaps remain where data was not available or a computation did not "
                      "complete, and no conclusion can be drawn on them until that data is "
                      "supplied."),
        "conc_complete": "Every planned step was computed.",
    },
}


def strings(plan):
    language = plan.get("language") or "en"
    if language != "en":
        raise ValueError(f"unsupported language {language!r}; the official benchmark is English only")
    return _STRINGS["en"]


def fmt(v, L=_STRINGS["en"]):
    if isinstance(v, bool):
        return L["yes"] if v else L["no"]
    if isinstance(v, (int, float)):
        if not math.isfinite(float(v)):
            return L["na"]
        return ("%.6g" % v)
    return str(v)


def collect_graph(plan, steward, L):
    """Walk the decision graph, deriving each branch from what this run computed.

    At every node: ask the steward for that node's batch, run the methods the node calls for,
    fold those results into the guard namespace, then take the first outgoing edge whose guard
    holds ON THOSE NUMBERS (the default edge last). Nothing here replays a stored route -- the
    plan carries the graph and the guards, and the branch recorded in `route_decisions` is the
    one this run's own arithmetic produced.
    """
    g = plan["graph"]
    nodes = {n["key"]: n for n in g["nodes"]}
    edges = g.get("edges") or []
    policy = g.get("method_policy") or {}
    field_map = g.get("field_map") or {}
    expected_fields = plan.get("expected_fields") or {}

    observed, outputs_by_method = {}, {}
    outputs_by_occurrence, occurrence_counts = {}, {}
    steps, routes, notes = [], [], []
    declared, requested, fallback = {}, {}, [None]

    def declare_all():
        for key, value in list(declared.items()):
            steward.declare(key, value)

    def batch_for(node):
        stage_id = node.get("stage_id")
        if not stage_id:
            return None, None
        if stage_id in requested:
            return requested[stage_id]
        step = {"stage_id": stage_id, "phase": node.get("phase", ""),
                "topics": node.get("topics") or []}
        payload, refusal = steward.request(step)
        if refusal == "locked":
            declare_all()
            payload, refusal = steward.request(step)
        if refusal in ("offline", "budget") or (payload is None and refusal is None):
            if fallback[0] is None:
                fallback[0] = _fallback_blocks(plan) or {}
                if fallback[0]:
                    notes.append("steward unreachable; read the released batch file instead")
            payload = fallback[0].get(stage_id) if fallback[0] else None
            refusal = None if payload is not None else refusal
        requested[stage_id] = (payload, refusal)
        return payload, refusal

    node_key = g["entry"]
    seen_nodes = set([node_key])
    while True:
        node = nodes.get(node_key)
        if node is None:
            break
        payload, refusal = batch_for(node)
        if node.get("stage_id") and payload is not None:
            RELEASED[node["stage_id"]] = payload
        # structural facts first: a node's admissible METHOD can itself depend on one.
        observe_batch(node, payload, observed)
        methods = methods_at(node, policy, observed)
        for mid in methods:
            step = {"step_id": len(steps) + 1, "method_id": mid,
                    "inputs_digest": {"stage_id": node.get("stage_id") or node["key"],
                                      "phase": node.get("phase", "")},
                    "outputs": {}, "status": "failed", "decision": None}
            if payload is None:
                step["status"] = "refused"
                step["decision"] = L["refused"] % (refusal or "unknown")
                steps.append(step)
                continue
            fn = METHODS.get(mid)
            if fn is None:
                step["decision"] = L["not_implemented"]
                steps.append(step)
                continue
            try:
                out = fn(payload)
            except Exception as exc:                     # noqa: BLE001 - honest failure
                step["decision"] = L["compute_failed"] % exc
                steps.append(step)
                continue
            for key, value in (out.pop("_declare", {}) or {}).items():
                declared[key] = value
                steward.declare(key, value)
            clean = {k: v for k, v in out.items()
                     if isinstance(v, (int, float, bool, str)) and
                     (not isinstance(v, float) or math.isfinite(v))}
            outputs_by_method[mid] = dict(clean)
            occurrence_counts[mid] = occurrence_counts.get(mid, 0) + 1
            outputs_by_occurrence[(mid, occurrence_counts[mid] - 1)] = dict(clean)
            step["outputs"] = fill_expected(clean, expected_fields.get(mid) or [])
            step["status"] = "success"
            if isinstance(payload, dict):
                step["inputs_digest"]["keys"] = sorted(str(k) for k in payload.keys())
            steps.append(step)
        harvest(field_map, outputs_by_method, observed, outputs_by_occurrence)
        observe_batch(node, payload, observed)

        out_edges = [e for e in edges if e["source"] == node_key]
        if not out_edges:
            break
        chosen = None
        for e in out_edges:
            if not e.get("is_default") and guard_holds(e.get("when") or "", observed):
                chosen = e
                break
        if chosen is None:
            for e in out_edges:
                if e.get("is_default"):
                    chosen = e
                    break
        if chosen is None or chosen["target"] in seen_nodes:
            break
        if len(out_edges) > 1:
            routes.append({
                "point": node_key, "chosen_branch": chosen["target"],
                "observed": dict((f, _flat_observed(observed, f))
                                 for f in (chosen.get("guard_fields") or [])
                                 if _flat_observed(observed, f) is not None),
            })
        node_key = chosen["target"]
        seen_nodes.add(node_key)
    return steps, routes, notes


def _flat_observed(observed, dotted):
    cur = observed
    for part in str(dotted).split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur if isinstance(cur, (int, float)) and not isinstance(cur, bool) else None


def collect_linear(plan, steward, L):
    """The original driver: walk `plan["steps"]` in order. Used by every v1 task."""
    fallback = None
    steps, notes = [], []
    declared = {}
    computed_methods = set()

    def declare_all():
        for key, value in list(declared.items()):
            steward.declare(key, value)

    for stage in plan["steps"]:
        payload, refusal = steward.request(stage)
        if refusal == "locked":
            declare_all()
            payload, refusal = steward.request(stage)
        if refusal in ("offline", "budget") or (payload is None and refusal is None):
            if fallback is None:
                fallback = _fallback_blocks(plan)
                if fallback:
                    notes.append("steward unreachable; read the released batch file instead")
            payload = fallback.get(stage["stage_id"]) if fallback else None
            refusal = None if payload is not None else refusal

        for method in stage["methods"]:
            mid = method["method_id"]
            step = {"step_id": len(steps) + 1, "method_id": mid,
                    "inputs_digest": {"stage_id": stage["stage_id"], "phase": stage["phase"]},
                    "outputs": {}, "status": "failed", "decision": None}
            if payload is None:
                step["status"] = "refused"
                step["decision"] = L["refused"] % (refusal or "unknown")
                steps.append(step)
                continue
            RELEASED[stage["stage_id"]] = payload
            fn = METHODS.get(mid)
            if fn is None:
                step["decision"] = L["not_implemented"]
                steps.append(step)
                continue
            try:
                out = fn(payload)
            except Exception as exc:                     # noqa: BLE001 — honest failure
                step["decision"] = L["compute_failed"] % exc
                steps.append(step)
                continue
            for key, value in (out.pop("_declare", {}) or {}).items():
                declared[key] = value
                steward.declare(key, value)
            clean = {k: v for k, v in out.items()
                     if isinstance(v, (int, float, bool, str)) and
                     (not isinstance(v, float) or math.isfinite(v))}
            step["outputs"] = fill_expected(clean, method.get("expected_fields") or [])
            step["status"] = "success"
            if isinstance(payload, dict):
                step["inputs_digest"]["keys"] = sorted(str(k) for k in payload.keys())
            steps.append(step)
            computed_methods.add(mid)

    # route decisions: pick the branch whose evidence this run actually managed to compute
    routes = []
    for dp in plan.get("decision_points", []):
        scored = {b: len(set(ms) & computed_methods) for b, ms in dp["branches"].items()}
        best = max(scored, key=lambda b: scored[b]) if scored else None
        if best and scored[best] > 0:
            routes.append({"point": dp["point_id"], "chosen_branch": best,
                           "observed": {"computed_methods": sorted(
                               set(dp["branches"][best]) & computed_methods)}})
    return steps, routes, notes


def main():
    plan_path = sys.argv[1] if len(sys.argv) > 1 else "/solution/plan.json"
    with open(plan_path, encoding="utf-8") as f:
        plan = json.load(f)

    started = time.time()
    L = strings(plan)
    steward = Steward(plan)
    steward.wait(int(os.environ.get("ORACLE_STEWARD_WAIT_SEC", "20")))

    # Two routing modes, one report writer. A v1 plan is a sequence of stages; a v2 plan is a
    # decision graph, and which stage comes next is decided from what this run just computed.
    if (plan.get("route_mode") == "graph") and plan.get("graph"):
        steps, routes, notes = collect_graph(plan, steward, L)
    else:
        steps, routes, notes = collect_linear(plan, steward, L)

    trace = {
        "system_id": plan["system_id"],
        "task_id": plan["task_id"],
        "steps": steps,
        "route_decisions": routes,
        "turns": steward.turns,
        "interventions": 0,
        "wall_clock_s": round(time.time() - started, 3),
        "token_cost": None,
    }
    with open(plan["trace_path"], "w", encoding="utf-8") as f:
        json.dump(trace, f, ensure_ascii=False, indent=2)

    # report: the ONLY digits in this document come from outputs computed above.
    # HN treats a truth without a metric_cue as matching every line, so a number that is not
    # a computed result — a step count, a turn count — reads to the scorer as a figure
    # attached to whatever analysis did not run. Meta-counts are therefore written out in
    # words, not numerals.
    ok = [s for s in steps if s["status"] == "success"]
    refused = [s for s in steps if s["status"] == "refused"]
    failed = [s for s in steps if s["status"] == "failed"]
    lines = [L["title"], "",
             L["preamble"] % (plan["task_id"], plan["trace_path"]), ""]
    if notes:
        lines += [L["notes"] + L["notes_join"].join(notes), ""]

    lines += [L["h_done"], ""]
    if not ok:
        lines += [L["none_done"], ""]
    for s in ok:
        lines.append(L["stage_head"] % (s["inputs_digest"].get("stage_id", ""),
                                        s["inputs_digest"].get("phase", "")))
        for k, v in s["outputs"].items():
            lines.append(L["kv"] % (k, fmt(v, L)))
        lines.append("")

    if refused or failed:
        lines += [L["h_gaps"], "", L["gaps_intro"], ""]
        for s in refused:
            lines.append(L["gap_refused"]
                         % (s["inputs_digest"].get("stage_id", ""), s["decision"] or ""))
        for s in failed:
            lines.append(L["gap_failed"]
                         % (s["inputs_digest"].get("stage_id", ""), s["decision"] or ""))
        lines.append("")

    if routes:
        lines += [L["h_routes"], ""]
        for r in routes:
            lines.append("- %s -> %s" % (r["point"], r["chosen_branch"]))
        lines.append("")

    lines += [L["h_conclusion"], "",
              (L["conc_ok"] if ok else L["conc_none"]) +
              " " + (L["conc_gaps"] if (refused or failed) else L["conc_complete"]), ""]

    with open(plan["report_path"], "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    sys.stderr.write("oracle: %d/%d steps computed in %d turn(s)\n"
                     % (len(ok), len(steps), steward.turns))


if __name__ == "__main__":
    main()
PYEOF

python3 "$SCRATCH/oracle_analysis.py" "$PLAN"

ls -l "$WORK/trace.json" "$WORK/report.md"
