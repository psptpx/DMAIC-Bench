"""Independent reference implementations for truth verification (V7 gate).

Each verifier takes the SAME stage payload dict a case generator emits and recomputes the
canonical outputs with scipy/statsmodels. The onboarding validator cross-checks generator-claimed
truths against these — a case whose numbers its own generator can't reproduce independently is
rejected. The private contestant's own solver is deliberately NOT a source here (contestants
can't be referees).

Payload shape conventions follow the legacy eval provider (dmaic_data_provider.py) so bridge
cases verify too where field names line up. Every shape below is ACCEPTED IN ADDITION to the
others for the same method — a reader never drops a shape it used to read:
  two groups:    {"group1": [...], "group2": [...]} or {"groups": {name: [...]}}
                 or {"sample1": [...], "sample2": [...]}
                 or long format (below) that resolves to exactly two levels
  k groups:      {"groups": {name: [...]}} or group1/group2/... or sample1/sample2/...
                 or long format (below)
  long format:   a response column plus a parallel factor column, e.g.
                 {"response": [...], "factor": ["line 1", "line 1", "line 2", ...]} — grouped by factor
                 value, levels in FIRST-APPEARANCE order (never sorted, so a numeric-looking
                 label cannot silently reorder the groups). Accepted response/factor key
                 pairs are listed in _LONG_FORMAT_PAIRS.
  one sample:    {"data": [...]} (+ "hypothesizedMedian"/"testMedian"/"median0" for the
                 signed-rank null, "mu"/"hypothesizedMean" for the t-test null)
  correlation:   {"x": [...], "y": [...]}
  gof:           {"observed": [...]} / {"counts": [...]} / {"observedCounts": [...]}
                 (+ optional "expected")
  assoc:         {"table": [[...], ...]} or {"contingencyTable": [[...], ...]}
  proportions:   {"events1": e1, "trials1": t1, "events2": e2, "trials2": t2}
  prop power:    {"p1", "p2", "nPerGroup"} or the Minitab-style
                 {"proportion1": p1, "proportion2Values": [p2], "sampleSizes": [n],
                  "computationType": "POWER", "alpha": a} — the *Values/*Sizes lists must hold
                 exactly one entry each (a multi-point power curve has no single truth value,
                 so it is refused rather than guessed at), and a computationType that asks for
                 anything but POWER is refused.
  regression:    {"x": [...], "y": [...]} (+ optional "degree") or the column-table form
                 {"data": {colName: [...]}, "responseColumn": name,
                  "continuousPredictors": [name, ...], "termsInModel": [term, ...]} where a
                 term is a "*"-joined product of column names ("A", "A*A", "A*B") — so
                 polynomial and interaction models are built from the declared terms rather
                 than assumed. Absent termsInModel, the predictors enter linearly.
  poisson reg:   {"y"/"counts": [...], "x": [...]} or the column-table form
                 {"responseData": [...], "continuousData": {colName: [...]},
                  "continuousPredictors": [name, ...]}
  attribute MSA: {"standard": [label per item], "ratings": {appraiser: [[trial labels], ...]}}
                 or the legacy row table {"assessments": [{"appraiserId", "partId", "trial",
                 "result", "standard"}, ...]} — pivoted to the former, items in
                 first-appearance order of partId and trials in ascending trial number.
  any test:      optional {"alternativeHypothesis": "LESS_THAN"|"GREATER_THAN"|"NOT_EQUAL"}
                 — honoured by _alternative(); absent means two-sided.
  poisson cap:   {"defectCounts": [...], "inspectionUnits": [...]} or scalars
"""
from __future__ import annotations

import inspect
import itertools
import json
import math
from functools import lru_cache

import numpy as np
from scipy import integrate, optimize, stats


class NotVerifiable(Exception):
    """Payload shape not recognized by this verifier — skip, don't fail."""


# ---- scipy.stats.anderson compatibility ---------------------------------------------
#
# SciPy 1.17 began emitting a FutureWarning from `stats.anderson` when `method` is not
# given: in 1.19 the result object drops `critical_values` / `significance_level` /
# `fit_result` and always carries a `pvalue`. Every call site in this package reads ONLY
# `.statistic`, so nothing we derive is at risk — but an unguarded call would start
# warning on 1.17+ and is one release away from an API it no longer matches.
#
# `method` cannot simply be passed unconditionally: it does NOT exist before 1.17, and the
# pinned environment (spec.ANALYSIS_PINS) runs scipy 1.14.1, where passing it is a
# TypeError. So the support is detected once, here, and the argument is supplied only
# where it is accepted.
#
# The accepted literal is "interpolate". SciPy's own docstring says "interpolated"; the
# implementation rejects that with `ValueError: `method` must be either 'interpolate' or an
# instance of `MonteCarloMethod``. Verified against 1.18.1 — do not "correct" this spelling.
#
# `.statistic` is bit-identical with and without the argument (checked across n = 8 … 500),
# which is why this is a latent-API fix and not a truth change.
try:
    _ANDERSON_METHOD_KW = (
        "method" in inspect.signature(stats.anderson).parameters
    )
except (TypeError, ValueError):  # pragma: no cover - signature unavailable
    _ANDERSON_METHOD_KW = False


def anderson_statistic(x, dist: str = "norm") -> float:
    """The Anderson-Darling A² statistic, forward-compatible with SciPy 1.19.

    THE single entry point for `stats.anderson` in this package: it is the only thing that
    knows whether this SciPy wants `method`. Call it instead of `stats.anderson` so a
    future SciPy bump is a one-line change here rather than a hunt through the cases.
    """
    if _ANDERSON_METHOD_KW:
        return float(stats.anderson(x, dist=dist, method="interpolate").statistic)
    return float(stats.anderson(x, dist=dist).statistic)


def _arr(payload, *keys):
    payload = _unwrap_text_payload(payload)
    for k in keys:
        v = payload.get(k)
        if isinstance(v, (list, tuple)) and len(v) >= 2:
            return np.asarray(v, dtype=float)
    raise NotVerifiable(f"none of {keys} found")


#: (response key, factor key) pairs recognised as LONG (stacked) format: one row per
#: observation, the group identified by a parallel label column. The corpus writes
#: ("response", "factor") — carrying the human labels separately as responseName/factorName,
#: which are NOT data and are ignored here. The other pairs are the same layout under the
#: other names the legacy provider uses for a measurement column.
_LONG_FORMAT_PAIRS = (
    ("response", "factor"),
    ("response", "group"),
    ("response", "groupLabels"),
    ("values", "factor"),
    ("values", "group"),
    ("data", "factor"),
    ("data", "group"),
    ("y", "factor"),
    ("y", "group"),
)


def _numbered(payload, prefix):
    """[payload[prefix1], payload[prefix2], ...] while the keys run consecutively from 1."""
    out, i = [], 1
    while isinstance(payload.get(f"{prefix}{i}"), (list, tuple, np.ndarray)):
        out.append(np.asarray(payload[f"{prefix}{i}"], float))
        i += 1
    return out


def _unwrap_text_payload(payload):
    """A payload whose data arrived as a JSON STRING under "text"/"json"/"payload".

    This is transport, not statistics: some stages ship their table as an embedded JSON
    document with a human label beside it. Unwrapping it changes no convention and infers
    nothing — it only stops a readable table from being invisible to every reader in this
    module. A string that is not a JSON object is left alone.
    """
    if not isinstance(payload, dict):
        return payload
    for key in ("text", "json", "payload", "body"):
        raw = payload.get(key)
        if not isinstance(raw, str) or not raw.strip().startswith("{"):
            continue
        try:
            inner = json.loads(raw)
        except (ValueError, TypeError):
            continue
        if isinstance(inner, dict) and inner:
            merged = {k: v for k, v in payload.items() if k != key}
            merged.update(inner)   # inner columns win; the wrapper only carries labels
            return merged
    return payload


#: Cardinality rule for inferring which of two parallel columns is the FACTOR, used only
#: when neither column name appears in ``_LONG_FORMAT_PAIRS``. Deliberately narrow.
_INFERRED_FACTOR_MAX_LEVELS = 12


def _inferred_long_format(payload):
    """Long-format groups from a two-column table whose column NAMES are not recognised.

    Stated rule, and it is intentionally narrow enough to refuse rather than guess: the
    payload must contain EXACTLY TWO parallel list columns of equal length >= 4; exactly one
    of them must look like a factor — at most ``_INFERRED_FACTOR_MAX_LEVELS`` distinct values
    AND at most one third as many distinct values as there are rows; and the other column
    must have strictly more distinct values than it. Anything else raises. Two columns that
    both look continuous, or both look categorical, or a 2-of-3-columns table, are not
    resolvable without knowing what the study was, and this refuses them.

    Levels come out in FIRST-APPEARANCE order, exactly as in ``_long_format_groups``.
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    cols = {k: v for k, v in payload.items()
            if isinstance(v, (list, tuple)) and len(v) >= 4
            and all(not isinstance(e, (list, tuple, dict)) for e in v)}
    if len(cols) != 2:
        raise NotVerifiable(f"inferred long format needs exactly 2 columns, saw {len(cols)}")
    (na, va), (nb, vb) = cols.items()
    if len(va) != len(vb):
        raise NotVerifiable(f"columns {na}/{nb} have different lengths")
    n = len(va)

    def looks_like_factor(v):
        k = len({str(e) for e in v})
        return 2 <= k <= min(_INFERRED_FACTOR_MAX_LEVELS, n // 3)

    fa, fb = looks_like_factor(va), looks_like_factor(vb)
    if fa == fb:
        raise NotVerifiable(
            f"cannot tell response from factor in columns {na!r}/{nb!r} — refusing to guess")
    fkey, ykey = (na, nb) if fa else (nb, na)
    try:
        y = [float(e) for e in payload[ykey]]
    except (TypeError, ValueError):
        raise NotVerifiable(f"response column {ykey!r} is not numeric")
    if len({str(e) for e in payload[fkey]}) >= len(set(y)):
        raise NotVerifiable(f"column {fkey!r} is not less varied than {ykey!r}")
    levels, buckets = [], {}
    for label, value in zip(payload[fkey], y):
        key = str(label)
        if key not in buckets:
            buckets[key] = []
            levels.append(key)
        buckets[key].append(value)
    return [np.asarray(buckets[lv], float) for lv in levels]


def _long_format_groups(payload):
    """Split a response column by a parallel factor column (long/stacked format).

    Levels come out in FIRST-APPEARANCE order, never sorted: sorting would silently reorder
    the groups whenever the labels are numeric-looking strings, and every k-group statistic
    that is not symmetric in its arguments would then be computed on a different partition
    than the one the truth was derived from.

    A length mismatch RAISES rather than zipping to the shorter column — a truncated
    response column is a corrupt payload, not a smaller study, and silently analysing the
    prefix would produce a plausible wrong number.
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    for ykey, fkey in _LONG_FORMAT_PAIRS:
        y, f = payload.get(ykey), payload.get(fkey)
        if not (isinstance(y, (list, tuple, np.ndarray))
                and isinstance(f, (list, tuple, np.ndarray))):
            continue
        if len(y) != len(f):
            raise NotVerifiable(
                f"long format {ykey}/{fkey} length mismatch: {len(y)} vs {len(f)}")
        levels, buckets = [], {}
        for label, value in zip(f, y):
            key = str(label)
            if key not in buckets:
                buckets[key] = []
                levels.append(key)
            buckets[key].append(float(value))
        if len(levels) < 2:
            raise NotVerifiable(f"long format {ykey}/{fkey} has a single factor level")
        return [np.asarray(buckets[lv], float) for lv in levels]
    try:
        return _inferred_long_format(payload)
    except NotVerifiable as exc:
        raise NotVerifiable(
            f"no long-format response/factor pair among the declared key pairs, and "
            f"column-shape inference refused as well: {exc}")


def _two_groups(payload):
    payload = _unwrap_text_payload(payload)
    if "group1" in payload and "group2" in payload:
        return (np.asarray(payload["group1"], float), np.asarray(payload["group2"], float))
    if "sample1" in payload and "sample2" in payload:
        return (np.asarray(payload["sample1"], float), np.asarray(payload["sample2"], float))
    groups = payload.get("groups")
    if isinstance(groups, dict) and len(groups) >= 2:
        vals = [np.asarray(v, float) for v in groups.values()]
        return vals[0], vals[1]
    try:
        long = _long_format_groups(payload)
    except NotVerifiable:
        raise NotVerifiable("no two-group structure")
    if len(long) != 2:
        # Taking the first two of k would answer a different question than the truth asks.
        raise NotVerifiable(f"long format has {len(long)} levels, not 2")
    return long[0], long[1]


def _all_groups(payload):
    payload = _unwrap_text_payload(payload)
    groups = payload.get("groups")
    if isinstance(groups, dict) and len(groups) >= 2:
        return [np.asarray(v, float) for v in groups.values()]
    for prefix in ("group", "sample"):
        out = _numbered(payload, prefix)
        if len(out) >= 2:
            return out
    try:
        return _long_format_groups(payload)
    except NotVerifiable:
        raise NotVerifiable("no k-group structure")


# ---- verifiers (payload -> {canonical_field: value}) --------------------------------

def descriptive_summary(payload):
    x = _arr(payload, "data", "values", "measurements")
    ad_stat = anderson_statistic(x, dist="norm")
    # AD p-value via D'Agostino approximation used by Minitab-family tools
    a2 = ad_stat * (1 + 0.75 / len(x) + 2.25 / len(x) ** 2)
    if a2 >= 0.6:
        p = math.exp(1.2937 - 5.709 * a2 + 0.0186 * a2 * a2)
    elif a2 >= 0.34:
        p = math.exp(0.9177 - 4.279 * a2 - 1.38 * a2 * a2)
    elif a2 >= 0.2:
        p = 1 - math.exp(-8.318 + 42.796 * a2 - 59.938 * a2 * a2)
    else:
        p = 1 - math.exp(-13.436 + 101.14 * a2 - 223.73 * a2 * a2)
    return {
        "mean": float(np.mean(x)),
        "median": float(np.median(x)),
        "stdDev": float(np.std(x, ddof=1)),
        "skewness": float(stats.skew(x, bias=False)),
        "adPValue": float(p),
    }


def normality(payload):
    """Anderson-Darling normality test.

    Emits BOTH the p-value and the raw A² statistic. The statistic was previously absent,
    which made every ``basic.normality.statistic`` truth in the corpus unverifiable through
    the V7 gate — the reference implementation existed and simply did not return the field
    the truth named. ``statistic`` is the UNADJUSTED A² (scipy's ``stats.anderson``), the
    same quantity the D'Agostino small-sample adjustment inside ``descriptive_summary`` then
    corrects before mapping to a p-value; the two are not interchangeable and are reported
    under separate names.
    """
    x = _arr(payload, "data", "values", "measurements")
    d = descriptive_summary(payload)
    return {
        "pValue": d["adPValue"],
        "statistic": anderson_statistic(x, dist="norm"),
        "adStatistic": anderson_statistic(x, dist="norm"),
    }


def mann_whitney(payload):
    a, b = _two_groups(payload)
    r = stats.mannwhitneyu(a, b, alternative=_alternative(payload))
    return {"pValue": float(r.pvalue), "statistic": float(r.statistic)}


def kruskal_wallis(payload):
    r = stats.kruskal(*_all_groups(payload))
    return {"pValue": float(r.pvalue), "statistic": float(r.statistic)}


def one_sample_wilcoxon(payload):
    x = _arr(payload, "data", "values")
    # "testMedian" is the corpus spelling of the same null; "median0" the legacy one.
    med = next((payload[k] for k in ("hypothesizedMedian", "testMedian", "median0")
                if payload.get(k) is not None), None)
    if med is None:
        raise NotVerifiable("no hypothesized median (hypothesizedMedian/testMedian/median0)")
    r = stats.wilcoxon(x - float(med), alternative=_alternative(payload))
    return {"pValue": float(r.pvalue)}


def moods_median(payload):
    r = stats.median_test(*_all_groups(payload))
    return {"pValue": float(r.pvalue)}


# ---- declared alternative hypothesis --------------------------------------------------
#
# A payload may declare which alternative the analyst intended
# (``{"alternativeHypothesis": "LESS_THAN"}``); every verifier here used to ignore that and
# compute two-sided unconditionally. That is not a rounding difference -- it is a factor of
# two, and it is silent: the V7 gate reports the truth as unreproducible while the truth is
# the correct one. Measured on adb_c03 / A_CreepageOneSampleT (H1: mu < 3 mm, n = 30,
# t = -1.8795): declared one-sided p = 0.0351, computed two-sided p = 0.0703, truth 0.035.
#
# Unrecognised spellings raise instead of defaulting to two-sided. A default here would
# reintroduce exactly the failure this exists to prevent, in the one case where we know the
# payload was trying to tell us something and we did not understand it.
_ALTERNATIVES = {
    "NOT_EQUAL": "two-sided", "TWO_SIDED": "two-sided", "TWO-SIDED": "two-sided",
    "TWOSIDED": "two-sided", "NE": "two-sided",
    "LESS_THAN": "less", "LESS": "less", "LT": "less",
    "GREATER_THAN": "greater", "GREATER": "greater", "GT": "greater",
}


def _alternative(payload) -> str:
    """The declared alternative as a SciPy keyword; 'two-sided' when nothing is declared."""
    if not isinstance(payload, dict):
        return "two-sided"
    for key in ("alternativeHypothesis", "alternative", "tail", "side", "sides"):
        raw = payload.get(key)
        if raw is None:
            continue
        norm = _ALTERNATIVES.get(str(raw).strip().upper().replace(" ", "_"))
        if norm is None:
            raise NotVerifiable(f"unrecognised {key}={raw!r} — refusing to assume two-sided")
        return norm
    return "two-sided"


def correlation(payload):
    x, y = _arr(payload, "x"), _arr(payload, "y")
    r = stats.pearsonr(x, y, alternative=_alternative(payload))
    return {"correlationCoefficient": float(r.statistic), "pValue": float(r.pvalue)}


def one_sample_t(payload):
    x = _arr(payload, "data", "values")
    mu = payload.get("mu", payload.get("hypothesizedMean"))
    if mu is None:
        raise NotVerifiable("no hypothesized mean")
    r = stats.ttest_1samp(x, float(mu), alternative=_alternative(payload))
    return {"pValue": float(r.pvalue), "tStatistic": float(r.statistic)}


def two_sample_t(payload):
    a, b = _two_groups(payload)
    r = stats.ttest_ind(a, b, equal_var=False, alternative=_alternative(payload))
    return {"pValue": float(r.pvalue), "tStatistic": float(r.statistic)}


def paired_t(payload):
    a = _arr(payload, "before", "group1")
    b = _arr(payload, "after", "group2")
    r = stats.ttest_rel(a, b, alternative=_alternative(payload))
    return {"pValue": float(r.pvalue), "tStatistic": float(r.statistic)}


def anova_oneway(payload):
    r = stats.f_oneway(*_all_groups(payload))
    return {"factorPValue": float(r.pvalue), "fStatistic": float(r.statistic)}


def two_proportions(payload):
    try:
        e1, t1 = float(payload["events1"]), float(payload["trials1"])
        e2, t2 = float(payload["events2"]), float(payload["trials2"])
    except KeyError as e:
        raise NotVerifiable(str(e))
    p1, p2 = e1 / t1, e2 / t2
    p = (e1 + e2) / (t1 + t2)
    se = math.sqrt(p * (1 - p) * (1 / t1 + 1 / t2))
    z = (p1 - p2) / se
    return {"pValue": float(2 * stats.norm.sf(abs(z))), "zStatistic": float(z)}


def chisquare_gof(payload):
    obs = _arr(payload, "observed", "counts", "observedCounts")
    exp = payload.get("expected")
    r = stats.chisquare(obs, f_exp=np.asarray(exp, float) if exp else None)
    return {"chiSquare": float(r.statistic), "pValue": float(r.pvalue)}


def chisquare_assoc(payload):
    table = payload.get("table") or payload.get("contingencyTable")
    if not table:
        raise NotVerifiable("no table/contingencyTable")
    r = stats.chi2_contingency(np.asarray(table, float), correction=False)
    return {"statistic": float(r.statistic), "pValue": float(r.pvalue)}


def _sigma_within(payload, x):
    """(σ̂_within, method-name) for a normal-capability payload.

    Cp/Cpk are defined on the WITHIN-SUBGROUP (short-term) sigma; Pp/Ppk on the OVERALL
    sigma. Returning only the overall quantities is why ``capability.normal.cpk`` had never
    been reproduced by anything: ``cpk`` simply was not a key this module emitted, and the
    V7 gate read that absence as "nothing to check".

    THE HOUSE RULE, taken verbatim from docs/archive/control-phase-design-2026-09-04.md §4.1 (which
    cites AIAG SPC-2 2e Ch. IV for the within/overall distinction and ISO 22514-2:2017 §4 for
    the C/P index naming). It is adopted here rather than reinvented, because the Control
    phase is about to bind subgrouped ``cpk`` truths and a benchmark that carries two
    within-sigma conventions is worse than one that carries a stated convention:

    * UNGROUPED individuals              -> MR̄ / d2(2)   (span-2 moving ranges, given order)
    * SUBGROUPED with 2 <= n <= 8        -> R̄  / d2(n)
    * SUBGROUPED with n >= 9             -> s̄  / c4(n)

    The pooled-standard-deviation estimate (Minitab's other offering,
    s_p = sqrt(Σ(n_i-1)s_i²/Σ(n_i-1)) unbiased by c4) is a defensible alternative rather than
    a wrong answer, so it is reported alongside as ``sigmaWithinPooled`` instead of being
    silently discarded — a mismatch against a tool configured that way is then diagnosable as
    a convention difference rather than an arithmetic one.
    """
    try:
        g = _subgroups(payload, values=payload.get("data") if isinstance(payload, dict) else None)
    except NotVerifiable:
        g = None
    if g is not None and g.shape[1] >= 2:
        n_i = g.shape[1]
        dof = g.shape[0] * (n_i - 1)
        s_p = math.sqrt(float(np.sum((n_i - 1) * g.var(axis=1, ddof=1))) / dof) / c4(dof + 1)
        if n_i <= 8:
            return float(np.mean(np.ptp(g, axis=1)) / d2(n_i)), "rBar", s_p
        return float(np.mean(g.std(axis=1, ddof=1)) / c4(n_i)), "sBar", s_p
    return sigma_within_individuals(x), "movingRange", None


def capability_normal(payload):
    """Normal process capability: Cp/Cpk (within sigma) AND Pp/Ppk (overall sigma).

    Payload: {"data": [...], "lsl": .., "usl": ..} — either limit may be absent, in which
    case only the one-sided indices are defined. Conventions for σ̂_within are stated in
    ``_sigma_within``; σ̂_overall is the ordinary sample SD (ddof=1).
        Cp  = (USL-LSL)/(6σ_w)    Cpk = min((USL-μ)/3σ_w, (μ-LSL)/3σ_w)
        Pp  = (USL-LSL)/(6σ_o)    Ppk = min((USL-μ)/3σ_o, (μ-LSL)/3σ_o)
    """
    x = _arr(payload, "data", "measurements", "values")
    lsl, usl = payload.get("lsl"), payload.get("usl")
    if lsl is None and usl is None:
        raise NotVerifiable("no spec limits")
    mu, sd = float(np.mean(x)), float(np.std(x, ddof=1))
    if sd <= 0:
        raise NotVerifiable("zero overall variance")
    sw, sw_method, sw_pooled = _sigma_within(payload, x)
    if sw <= 0:
        raise NotVerifiable("zero within-subgroup variance")
    out = {"mean": mu, "sigmaOverall": sd, "sigmaWithin": float(sw),
           "sigmaWithinMethod": sw_method}
    if sw_pooled is not None:
        out["sigmaWithinPooled"] = float(sw_pooled)
    if lsl is not None and usl is not None:
        out["pp"] = (float(usl) - float(lsl)) / (6 * sd)
        out["cp"] = (float(usl) - float(lsl)) / (6 * sw)
    over = [z for z in (
        (float(usl) - mu) / (3 * sd) if usl is not None else None,
        (mu - float(lsl)) / (3 * sd) if lsl is not None else None) if z is not None]
    within = [z for z in (
        (float(usl) - mu) / (3 * sw) if usl is not None else None,
        (mu - float(lsl)) / (3 * sw) if lsl is not None else None) if z is not None]
    out["ppk"] = min(over)
    out["cpk"] = min(within)
    if usl is not None:
        out["ppu"], out["cpu"] = (float(usl) - mu) / (3 * sd), (float(usl) - mu) / (3 * sw)
    if lsl is not None:
        out["ppl"], out["cpl"] = (mu - float(lsl)) / (3 * sd), (mu - float(lsl)) / (3 * sw)
    return out


def capability_grouped(payload):
    """Grouped capability comparison. Payload: {"groups": {name: [...]}, "lsl", "usl"}.

    Convention: each group is evaluated with ITS OWN mean and ITS OWN sample SD (ddof=1)
    against the SHARED spec limits, and the reported ``ppk`` is the WORST (minimum) group —
    the number that decides whether the process as a whole is capable. ``ppkBest`` and
    ``ppkPooled`` (all groups pooled into one sample) are reported alongside so a differing
    convention is visible rather than mistaken for a wrong answer.

    ``cpk`` is deliberately NOT emitted here. Cpk needs a within-subgroup sigma, and the
    groups of this payload are process strata (workstation, supplier, shift), not rational
    time-ordered subgroups: the values carry no order guarantee, so a moving-range estimate
    would be an invented number dressed as a reference value. The V7 gate now reports that
    absence as a named warning instead of skipping it silently.
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    groups = payload.get("groups")
    if not isinstance(groups, dict) or len(groups) < 2:
        raise NotVerifiable("need a groups dict with >=2 groups")
    lsl, usl = payload.get("lsl"), payload.get("usl")
    if lsl is None and usl is None:
        raise NotVerifiable("no spec limits")

    def ppk_of(a):
        mu, sd = float(np.mean(a)), float(np.std(a, ddof=1))
        if sd <= 0:
            raise NotVerifiable("zero variance in a group")
        z = [v for v in (
            (float(usl) - mu) / (3 * sd) if usl is not None else None,
            (mu - float(lsl)) / (3 * sd) if lsl is not None else None) if v is not None]
        return min(z)

    per = {}
    for name, vals in groups.items():
        a = np.asarray(vals, float)
        if a.ndim != 1 or len(a) < 2:
            raise NotVerifiable(f"group {name!r} is not a series of >=2 values")
        per[name] = ppk_of(a)
    pooled = np.concatenate([np.asarray(v, float) for v in groups.values()])
    return {
        "ppk": float(min(per.values())),
        "ppkWorstGroup": float(min(per.values())),
        "ppkBest": float(max(per.values())),
        "ppkPooled": float(ppk_of(pooled)),
        "groupCount": float(len(per)),
    }


#: Candidate distributions for non-normal capability, each fitted by MLE with the location
#: pinned at 0 (a physical measurement of a positive quantity has no free threshold to
#: absorb). Selection is by SMALLEST ANDERSON-DARLING A² over exactly this set — see
#: ``capability_nonnormal`` and ``_ad_gof``.
_NONNORMAL_CANDIDATES = (
    ("lognormal", stats.lognorm),
    ("weibull", stats.weibull_min),
    ("gamma", stats.gamma),
    ("exponential", stats.expon),
)


def _ad_gof(x, dist, par) -> float:
    """Anderson-Darling A² of a sample against a FITTED continuous distribution.

        A² = -n - (1/n)·Σ (2i-1)·[ln F(x_(i)) + ln(1 - F(x_(n+1-i)))]

    the standard empirical form (Stephens 1974, JASA 69, 730-737). Reported unadjusted:
    the small-sample adjustment is a monotone rescaling per distribution family and does not
    reorder candidates fitted to the same n, which is all this is used for.
    """
    x = np.sort(np.asarray(x, float))
    n = len(x)
    F = np.clip(dist.cdf(x, *par), 1e-14, 1.0 - 1e-14)
    i = np.arange(1, n + 1)
    return float(-n - np.sum((2 * i - 1) * (np.log(F) + np.log(1.0 - F[::-1]))) / n)


def capability_nonnormal(payload):
    """Non-normal capability by the PERCENTILE method (ISO 22514-2; Minitab's default).

    Payload: {"data": [...], "usl" and/or "lsl", "autoSelectDistribution": bool,
              optional "distribution": name}.

    Convention — the two halves that must both be stated:
      1. DISTRIBUTION. If the payload names one, it is used. Otherwise — which is what
         ``autoSelectDistribution`` asks for — the candidate with the SMALLEST
         ANDERSON-DARLING A² among ``_NONNORMAL_CANDIDATES`` is chosen, each fitted by MLE
         with ``floc=0``. AD is the ranking Minitab's Individual Distribution Identification
         uses and the one this corpus's truths were derived under; ranking by raw
         log-likelihood instead is a defensible-sounding choice that is NOT the same, and
         choosing it here was a measured defect: on adb_c06 seed 3 the likelihood rule picks
         gamma over lognormal by 0.09 nats and lands on Ppk = 1.369 against a lognormal truth
         of 0.993 — a 38% error produced entirely by the selection rule. Both the choice and
         its margin are reported (``selectedDistribution``, ``selectedDistributionAD``,
         ``runnerUpAD``), because a near-tie between two distributions that disagree by 38%
         on Ppk is something a reader of this number must be told.
      2. INDICES. There is no 6σ here; the spread is the 0.135%-99.865% percentile span,
         which coincides with ±3σ for a normal:
             Ppu = (USL - x_0.5)/(x_0.99865 - x_0.5)
             Ppl = (x_0.5 - LSL)/(x_0.5 - x_0.00135)
             Ppk = min(available), Pp = (USL-LSL)/(x_0.99865 - x_0.00135)
         The MEDIAN, not the mean, is the centre — that is what makes it the percentile
         method rather than a normal calculation with a fitted sigma.
    """
    x = _arr(payload, "data", "measurements", "values")
    if np.any(x <= 0):
        raise NotVerifiable("percentile fits here pin location at 0; data must be positive")
    lsl, usl = payload.get("lsl"), payload.get("usl")
    if lsl is None and usl is None:
        raise NotVerifiable("no spec limits")
    named = payload.get("distribution")
    cands = _NONNORMAL_CANDIDATES
    if named:
        key = str(named).strip().lower()
        cands = tuple((n, d) for n, d in _NONNORMAL_CANDIDATES if n == key)
        if not cands:
            raise NotVerifiable(f"unsupported distribution {named!r}")
    ranked = []
    for name, dist in cands:
        try:
            par = dist.fit(x, floc=0)
            a2 = _ad_gof(x, dist, par)
            ll = float(np.sum(dist.logpdf(x, *par)))
        except Exception:  # a candidate that will not fit is simply not the best one
            continue
        if not (math.isfinite(a2) and math.isfinite(ll)):
            continue
        ranked.append((a2, ll, name, dist, par))
    if not ranked:
        raise NotVerifiable("no candidate distribution could be fitted")
    ranked.sort(key=lambda r: r[0])
    a2, ll, name, dist, par = ranked[0]
    x00135, x50, x99865 = (float(dist.ppf(q, *par)) for q in (0.00135, 0.5, 0.99865))
    if not all(map(math.isfinite, (x00135, x50, x99865))) or x99865 <= x50 or x50 <= x00135:
        raise NotVerifiable("degenerate fitted percentiles")
    out = {"selectedDistribution": name, "selectedDistributionAD": a2,
           "selectedDistributionLogLik": ll, "median": x50,
           "p00135": x00135, "p99865": x99865}
    if len(ranked) > 1:
        out["runnerUpDistribution"] = ranked[1][2]
        out["runnerUpAD"] = ranked[1][0]
    zs = []
    if usl is not None:
        out["ppu"] = (float(usl) - x50) / (x99865 - x50)
        zs.append(out["ppu"])
    if lsl is not None:
        out["ppl"] = (x50 - float(lsl)) / (x50 - x00135)
        zs.append(out["ppl"])
    if lsl is not None and usl is not None:
        out["pp"] = (float(usl) - float(lsl)) / (x99865 - x00135)
    out["ppk"] = float(min(zs))
    return out


# ======================================================================================
# SPC / control-chart reference layer
# ======================================================================================
#
# CONVENTIONS ADOPTED HERE (stated once, in full, because an unstated convention is how a
# truth ships that its own verifier cannot reproduce):
#
# * Unbiasing constants d2(n), d3(n) are computed by NUMERICAL INTEGRATION of the
#   distribution of the range of n i.i.d. standard normals — not read from a printed table.
#   d2(n) = ∫ [1 - Φ(x)^n - (1-Φ(x))^n] dx   (a single 1-D quadrature)
#   d3(n) = sqrt(E[W²] - d2(n)²) with E[W²] = ∫ 2t·P(W>t) dt and
#           P(W ≤ t) = n ∫ φ(x)[Φ(x+t) - Φ(x)]^(n-1) dx     (nested quadrature)
#   Checked against the AIAG SPC-2 / Montgomery ISQC 6e Appendix VI table to every printed
#   digit: d2(2)=1.128, d2(5)=2.326, d3(5)=0.864, D4(5)=2.114, D3(8)=0.136, D4(8)=1.864,
#   A2(5)=0.577. A table would have been a second place for a typo to hide; the integral is
#   the definition.
# * c4(n) = sqrt(2/(n-1))·Γ(n/2)/Γ((n-1)/2) — closed form, exact (no integration needed).
# * Derived chart factors, all closed-form from the above:
#       A2 = 3/(d2·√n)      A3 = 3/(c4·√n)      E2 = 3/d2 (individuals, n=2 moving range)
#       D3 = max(0, 1 - 3·d3/d2)                D4 = 1 + 3·d3/d2
#       B3 = max(0, 1 - 3·√(1-c4²)/c4)          B4 = 1 + 3·√(1-c4²)/c4
# * σ̂_within for INDIVIDUALS data is MR̄/d2(2) — the mean of the |x_i - x_(i-1)| moving
#   ranges of span 2, in the payload's given order (Montgomery ISQC 6e §6.4). Every chart
#   here that needs a short-term sigma from an ungrouped series uses exactly this, so I-MR,
#   EWMA, CUSUM and within-subgroup capability all agree with one another by construction.
# * RUN RULES. ``flaggedCount`` / ``outOfControlCount`` count points OUTSIDE THE CONTROL
#   LIMITS ONLY — Nelson Test 1, equivalently Western Electric Rule 1. That is the rule the
#   corpus's own derivations state ("count of points outside", "count of points with C+>h or
#   C-<-h"), and silently adding Tests 2-8 would make this reference disagree with correct
#   truths. The full Nelson 1984 (JQT 16(4) 237-239) set — the eight tests Minitab applies by
#   default — is computed separately and reported as ``nelsonFlaggedCount`` plus per-test
#   ``nelsonTest<k>Count`` on the constant-limit charts, so the stricter convention is
#   available and named rather than assumed. Western Electric's four-rule subset is Nelson
#   tests 1, 5, 6 and 2-at-9 (WE uses 8-in-a-row for its run rule); where the two differ this
#   module follows NELSON, because that is what the reference tool of this corpus applies.
#   Charts with point-varying limits (p/u with unequal n, Laney, EWMA) get Test 1 only: the
#   zone tests are defined on a constant sigma and are not well-defined there.
#
# None of this layer imports the contestant's solver. It is scipy + numpy + closed form.

_QUAD_LIMIT = 200
_QUAD_TAIL = 12.0  # ±12 sigma: Φ is 1 - 2e-33 there, far beyond quadrature resolution


@lru_cache(maxsize=None)
def d2(n: int) -> float:
    """E[range of n i.i.d. N(0,1)] — by quadrature, not by table lookup."""
    n = int(n)
    if n < 2:
        raise NotVerifiable(f"d2 undefined for subgroup size {n}")
    def integrand(x):
        F = stats.norm.cdf(x)
        return 1.0 - F ** n - (1.0 - F) ** n
    val, _ = integrate.quad(integrand, -_QUAD_TAIL, _QUAD_TAIL, limit=_QUAD_LIMIT)
    return float(val)


@lru_cache(maxsize=None)
def d3(n: int) -> float:
    """SD[range of n i.i.d. N(0,1)] — by nested quadrature (see the module note above)."""
    n = int(n)
    if n < 2:
        raise NotVerifiable(f"d3 undefined for subgroup size {n}")

    def survival(t):
        if t <= 0:
            return 1.0
        def inner(x):
            return stats.norm.pdf(x) * (stats.norm.cdf(x + t) - stats.norm.cdf(x)) ** (n - 1)
        cdf, _ = integrate.quad(inner, -_QUAD_TAIL, _QUAD_TAIL, limit=_QUAD_LIMIT)
        return 1.0 - n * cdf

    e_w2, _ = integrate.quad(lambda t: 2.0 * t * survival(t), 0.0, 2 * _QUAD_TAIL,
                             limit=_QUAD_LIMIT)
    return float(math.sqrt(max(e_w2 - d2(n) ** 2, 0.0)))


def c4(n: int) -> float:
    """Unbiasing constant for the sample SD of n normals: E[s] = c4(n)·σ. Closed form."""
    n = int(n)
    if n < 2:
        raise NotVerifiable(f"c4 undefined for subgroup size {n}")
    return float(math.sqrt(2.0 / (n - 1)) * math.gamma(n / 2.0) / math.gamma((n - 1) / 2.0))


def A2(n): return 3.0 / (d2(n) * math.sqrt(n))
def A3(n): return 3.0 / (c4(n) * math.sqrt(n))
def D3(n): return max(0.0, 1.0 - 3.0 * d3(n) / d2(n))
def D4(n): return 1.0 + 3.0 * d3(n) / d2(n)
def B3(n): return max(0.0, 1.0 - 3.0 * math.sqrt(1.0 - c4(n) ** 2) / c4(n))
def B4(n): return 1.0 + 3.0 * math.sqrt(1.0 - c4(n) ** 2) / c4(n)
def E2(n=2): return 3.0 / d2(n)


def _series(payload, *keys):
    """A 1-D float series from the first present key, keeping the payload's ORDER.

    Order is data here, not presentation: every moving-range estimate and every run rule is
    order-dependent, so nothing in this layer ever sorts.
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    for k in keys:
        v = payload.get(k)
        if isinstance(v, (list, tuple, np.ndarray)) and len(v) >= 2:
            arr = np.asarray(v, dtype=float)
            if arr.ndim != 1:
                continue
            return arr
    raise NotVerifiable(f"none of {keys} found as a 1-D series")


def _moving_range(x):
    """|x_i - x_(i-1)| for a series in production order (span-2 moving ranges)."""
    if len(x) < 2:
        raise NotVerifiable("need >=2 observations for a moving range")
    return np.abs(np.diff(np.asarray(x, dtype=float)))


def sigma_within_individuals(x) -> float:
    """σ̂ = MR̄ / d2(2) — the short-term sigma of an ungrouped series (Montgomery §6.4)."""
    return float(np.mean(_moving_range(x)) / d2(2))


def _subgroups(payload, values=None):
    """(k x n) subgroup matrix from {"data": flat, "subgroupSize": n} or a list of lists.

    A flat series whose length is not a multiple of ``subgroupSize`` is REFUSED rather than
    truncated: analysing a prefix would answer a different question than the truth asks.
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    raw = values
    if raw is None:
        for k in ("data", "measurements", "values", "subgroups", "observations"):
            if isinstance(payload.get(k), (list, tuple)):
                raw = payload[k]
                break
    if raw is None:
        raise NotVerifiable("no data/measurements/values/subgroups series")
    if raw and isinstance(raw[0], (list, tuple)):
        rows = [np.asarray(r, float) for r in raw]
        widths = {len(r) for r in rows}
        if len(widths) != 1:
            raise NotVerifiable(f"ragged subgroups (sizes {sorted(widths)})")
        g = np.vstack(rows)
    else:
        n = payload.get("subgroupSize", payload.get("subgroup_size"))
        if n is None:
            raise NotVerifiable("flat series without subgroupSize")
        n = int(n)
        arr = np.asarray(raw, float)
        if n < 2 or len(arr) % n:
            raise NotVerifiable(f"{len(arr)} observations do not split into subgroups of {n}")
        g = arr.reshape(-1, n)
    if g.shape[0] < 2 or g.shape[1] < 2:
        raise NotVerifiable(f"need >=2 subgroups of size >=2, got {g.shape}")
    return g


def _beyond(values, lcl, ucl) -> int:
    """Nelson Test 1 count. ``lcl``/``ucl`` may be arrays (point-varying limits)."""
    v = np.asarray(values, float)
    lo = np.full_like(v, -np.inf) if lcl is None else np.asarray(lcl, float)
    hi = np.full_like(v, np.inf) if ucl is None else np.asarray(ucl, float)
    return int(np.sum((v > hi) | (v < lo)))


def nelson_flags(values, center: float, sigma: float) -> dict:
    """Nelson 1984 tests 1-8 on a constant-limit chart -> per-test flagged-point counts.

    Returns ``{"nelsonTest1Count": .., ..., "nelsonFlaggedCount": n}`` where the last is the
    number of DISTINCT points flagged by at least one test. Reported alongside — never
    instead of — the Test-1-only ``flaggedCount``, so the two conventions stay separable.
    """
    v = np.asarray(values, float)
    n = len(v)
    if sigma <= 0 or n == 0:
        return {f"nelsonTest{i}Count": 0 for i in range(1, 9)} | {"nelsonFlaggedCount": 0}
    z = (v - center) / sigma
    hits = {i: set() for i in range(1, 9)}

    for i in range(n):                                    # 1: beyond 3 sigma
        if abs(z[i]) > 3:
            hits[1].add(i)
    side = np.sign(z)
    run = 0                                               # 2: 9 in a row, same side
    for i in range(n):
        run = run + 1 if i and side[i] == side[i - 1] and side[i] != 0 else (1 if side[i] else 0)
        if run >= 9:
            hits[2].update(range(i - 8, i + 1))
    inc = dec = 1                                         # 3: 6 in a row monotone
    for i in range(1, n):
        inc = inc + 1 if v[i] > v[i - 1] else 1
        dec = dec + 1 if v[i] < v[i - 1] else 1
        if inc >= 6:
            hits[3].update(range(i - 5, i + 1))
        if dec >= 6:
            hits[3].update(range(i - 5, i + 1))
    alt = 1                                               # 4: 14 in a row alternating
    for i in range(1, n):
        up_prev = v[i - 1] - v[i - 2] if i >= 2 else None
        up = v[i] - v[i - 1]
        alt = alt + 1 if (up_prev is not None and up * up_prev < 0) else 1
        if alt >= 13:
            hits[4].update(range(i - 13, i + 1))
    for i in range(2, n):                                 # 5: 2 of 3 beyond 2 sigma, same side
        w = z[i - 2:i + 1]
        for sgn in (1, -1):
            if np.sum(sgn * w > 2) >= 2 and sgn * z[i] > 2:
                hits[5].update(j for j in range(i - 2, i + 1) if sgn * z[j] > 2)
    for i in range(4, n):                                 # 6: 4 of 5 beyond 1 sigma, same side
        w = z[i - 4:i + 1]
        for sgn in (1, -1):
            if np.sum(sgn * w > 1) >= 4 and sgn * z[i] > 1:
                hits[6].update(j for j in range(i - 4, i + 1) if sgn * z[j] > 1)
    run = 0                                               # 7: 15 in a row within 1 sigma
    for i in range(n):
        run = run + 1 if abs(z[i]) < 1 else 0
        if run >= 15:
            hits[7].update(range(i - 14, i + 1))
    run = 0                                               # 8: 8 in a row beyond 1 sigma
    for i in range(n):
        run = run + 1 if abs(z[i]) > 1 else 0
        if run >= 8:
            hits[8].update(range(i - 7, i + 1))

    out = {f"nelsonTest{i}Count": len(hits[i]) for i in range(1, 9)}
    out["nelsonFlaggedCount"] = len(set().union(*hits.values()))
    return out


# ---- variables control charts ---------------------------------------------------------

def control_chart_imr(payload):
    """I-MR chart. Payload: {"data": [...] in production order} (+ optional "unit"/"order").

    CL_I = x̄; σ̂ = MR̄/d2(2); I limits = x̄ ± 3σ̂ (equivalently x̄ ± E2·MR̄, E2 = 3/d2(2) =
    2.65869 — the corpus generator rounds this to 2.66, a 0.05% difference on the limit).
    MR chart: CL = MR̄, UCL = D4(2)·MR̄, LCL = D3(2)·MR̄ = 0.
    """
    x = _series(payload, "data", "measurements", "values", "individuals")
    mr = _moving_range(x)
    mrbar = float(np.mean(mr))
    if mrbar <= 0:
        raise NotVerifiable("every moving range is zero — control limits are degenerate")
    sigma = mrbar / d2(2)
    cl = float(np.mean(x))
    ucl, lcl = cl + 3 * sigma, cl - 3 * sigma
    mr_ucl, mr_lcl = D4(2) * mrbar, D3(2) * mrbar
    out = {
        "centerLine": cl,
        "individualsUCL": float(ucl),
        "individualsLCL": float(lcl),
        "sigmaWithin": float(sigma),
        "movingRangeCenterLine": mrbar,
        "movingRangeUCL": float(mr_ucl),
        "movingRangeLCL": float(mr_lcl),
        "flaggedCount": float(_beyond(x, lcl, ucl)),
        "movingRangeFlaggedCount": float(_beyond(mr, mr_lcl, mr_ucl)),
    }
    out.update({k: float(v) for k, v in nelson_flags(x, cl, sigma).items()})
    return out


def _xbar_common(g):
    xbars = g.mean(axis=1)
    return float(g.mean()), xbars


def control_chart_xbar_r(payload):
    """X̄-R chart. Payload: {"data": flat series, "subgroupSize": n} or list-of-lists.

    CL_X̄ = grand mean of ALL observations (identical to the mean of the subgroup means for
    equal subgroup sizes, which is the only shape this reader accepts).
    X̄ limits = x̄̄ ± A2(n)·R̄; R chart CL = R̄, UCL = D4(n)·R̄, LCL = D3(n)·R̄.
    σ̂_within = R̄/d2(n).
    """
    g = _subgroups(payload)
    n = g.shape[1]
    grand, xbars = _xbar_common(g)
    rbar = float(np.mean(np.ptp(g, axis=1)))
    if rbar <= 0:
        raise NotVerifiable("every subgroup range is zero — control limits are degenerate")
    sigma = rbar / d2(n)
    ucl, lcl = grand + A2(n) * rbar, grand - A2(n) * rbar
    r_ucl, r_lcl = D4(n) * rbar, D3(n) * rbar
    ranges = np.ptp(g, axis=1)
    out = {
        "xBarChartCenterLine": grand,
        "centerLine": grand,
        "xBarUCL": float(ucl), "xBarLCL": float(lcl),
        "rChartCenterLine": rbar, "rUCL": float(r_ucl), "rLCL": float(r_lcl),
        "sigmaWithin": float(sigma),
        "subgroupCount": float(g.shape[0]), "subgroupSize": float(n),
        "flaggedXBarCount": float(_beyond(xbars, lcl, ucl)),
        "flaggedRangeCount": float(_beyond(ranges, r_lcl, r_ucl)),
        "flaggedCount": float(_beyond(xbars, lcl, ucl)),
    }
    out.update({k: float(v) for k, v in
                nelson_flags(xbars, grand, sigma / math.sqrt(n)).items()})
    return out


def control_chart_xbar_s(payload):
    """X̄-S chart. Payload: {"data": flat series, "subgroupSize": n} or list-of-lists.

    CL_X̄ = grand mean; X̄ limits = x̄̄ ± A3(n)·s̄ with s̄ the mean of the per-subgroup sample
    SDs (ddof=1); S chart CL = s̄, UCL = B4(n)·s̄, LCL = B3(n)·s̄; σ̂_within = s̄/c4(n).
    """
    g = _subgroups(payload)
    n = g.shape[1]
    grand, xbars = _xbar_common(g)
    sds = g.std(axis=1, ddof=1)
    sbar = float(np.mean(sds))
    if sbar <= 0:
        raise NotVerifiable("every subgroup SD is zero — control limits are degenerate")
    sigma = sbar / c4(n)
    ucl, lcl = grand + A3(n) * sbar, grand - A3(n) * sbar
    s_ucl, s_lcl = B4(n) * sbar, B3(n) * sbar
    out = {
        "xBarChartCenterLine": grand,
        "centerLine": grand,
        "xBarUCL": float(ucl), "xBarLCL": float(lcl),
        "sChartCenterLine": sbar, "sUCL": float(s_ucl), "sLCL": float(s_lcl),
        "sigmaWithin": float(sigma),
        "subgroupCount": float(g.shape[0]), "subgroupSize": float(n),
        "flaggedXBarCount": float(_beyond(xbars, lcl, ucl)),
        "flaggedSCount": float(_beyond(sds, s_lcl, s_ucl)),
        "flaggedCount": float(_beyond(xbars, lcl, ucl)),
    }
    out.update({k: float(v) for k, v in
                nelson_flags(xbars, grand, sigma / math.sqrt(n)).items()})
    return out


def control_chart_ewma(payload):
    """EWMA chart. Payload: {"data": [...], "target": μ0, "ewmaWeight": λ} (+ "L").

    z_i = λ·x_i + (1-λ)·z_(i-1), z_0 = the DECLARED target (not x̄ — the payload states the
    aim, and using the sample mean instead would silently re-centre the chart).
    Exact time-varying limits: μ0 ± L·σ̂·sqrt(λ/(2-λ)·(1 - (1-λ)^(2i))), L = 3 by default,
    σ̂ = MR̄/d2(2). ``flaggedCount`` = points with |z_i - μ0| beyond that limit.
    """
    x = _series(payload, "data", "measurements", "values")
    lam = payload.get("ewmaWeight", payload.get("lambda", payload.get("weight")))
    if lam is None:
        raise NotVerifiable("no ewmaWeight/lambda")
    lam = float(lam)
    if not 0 < lam <= 1:
        raise NotVerifiable(f"ewmaWeight={lam} outside (0, 1]")
    target = payload.get("target", payload.get("mu0"))
    mu0 = float(target) if target is not None else float(np.mean(x))
    L = float(payload.get("L", payload.get("kSigma", 3.0)))
    sigma = sigma_within_individuals(x)
    z, zs, lims = mu0, [], []
    for i, v in enumerate(x, start=1):
        z = lam * float(v) + (1 - lam) * z
        zs.append(z)
        lims.append(L * sigma * math.sqrt(lam / (2 - lam) * (1 - (1 - lam) ** (2 * i))))
    zs, lims = np.asarray(zs), np.asarray(lims)
    return {
        "centerLine": mu0,
        "sigmaWithin": float(sigma),
        "lambda": lam,
        "finalEwma": float(zs[-1]),
        "steadyStateUCL": float(mu0 + L * sigma * math.sqrt(lam / (2 - lam))),
        "steadyStateLCL": float(mu0 - L * sigma * math.sqrt(lam / (2 - lam))),
        "flaggedCount": float(np.sum(np.abs(zs - mu0) > lims)),
        "outOfControlCount": float(np.sum(np.abs(zs - mu0) > lims)),
    }


def control_chart_cusum(payload):
    """Tabular CUSUM. Payload: {"data": [...], "target": μ0, "kValue": k, "hValue": h}.

    k and h are in SIGMA UNITS (the corpus writes k=0.5, h=4 — Montgomery ISQC 6e §9.1.2's
    standard design), σ̂ = MR̄/d2(2):
        C+_i = max(0, x_i - (μ0 + kσ̂) + C+_(i-1)),  C-_i = max(0, (μ0 - kσ̂) - x_i + C-_(i-1))
    ``flaggedCount`` = points with C+ > hσ̂ or C- > hσ̂ (the corpus writes the lower arm with
    the opposite sign, C- < -hσ̂; identical set of points).
    """
    x = _series(payload, "data", "measurements", "values")
    target = payload.get("target", payload.get("mu0"))
    mu0 = float(target) if target is not None else float(np.mean(x))
    k = float(payload.get("kValue", payload.get("k", 0.5)))
    h = float(payload.get("hValue", payload.get("h", 4.0)))
    sigma = sigma_within_individuals(x)
    cp = cm = 0.0
    flagged, cps, cms = 0, [], []
    for v in x:
        cp = max(0.0, float(v) - (mu0 + k * sigma) + cp)
        cm = max(0.0, (mu0 - k * sigma) - float(v) + cm)
        cps.append(cp)
        cms.append(cm)
        if cp > h * sigma or cm > h * sigma:
            flagged += 1
    return {
        "centerLine": mu0,
        "sigmaWithin": float(sigma),
        "decisionInterval": float(h * sigma),
        "referenceValue": float(k * sigma),
        "maxCusumPlus": float(max(cps)), "maxCusumMinus": float(max(cms)),
        "flaggedCount": float(flagged),
        "outOfControlCount": float(flagged),
    }


# ---- attribute control charts ----------------------------------------------------------

def _counts_and_sizes(payload, size_keys):
    counts = payload.get("defectCounts", payload.get("counts", payload.get("defectives")))
    if not isinstance(counts, (list, tuple)) or len(counts) < 2:
        raise NotVerifiable("no defectCounts/counts series")
    c = np.asarray(counts, float)
    sizes = None
    for k in size_keys:
        v = payload.get(k)
        if isinstance(v, (list, tuple)):
            sizes = np.asarray(v, float)
            break
        if isinstance(v, (int, float)):
            sizes = np.full(len(c), float(v))
            break
    if sizes is None:
        raise NotVerifiable(f"none of {size_keys} found")
    if len(sizes) != len(c):
        raise NotVerifiable(f"counts/sizes length mismatch: {len(c)} vs {len(sizes)}")
    if np.any(sizes <= 0):
        raise NotVerifiable("non-positive subgroup size")
    return c, sizes


def control_chart_p(payload):
    """p chart (fraction nonconforming). Payload: {"defectCounts": [...], "sampleSizes": [...]}.

    CL = p̄ = Σd / Σn (the POOLED proportion, AIAG SPC-2 Ch. II — not the mean of the
    per-subgroup p̂_i, which differs whenever the n_i are unequal, as they are here).
    Point-varying limits p̄ ± 3·sqrt(p̄(1-p̄)/n_i), LCL floored at 0.
    """
    c, n = _counts_and_sizes(payload, ("sampleSizes", "sampleSize", "subgroupSizes",
                                       "subgroupSize", "n"))
    if np.any(c > n):
        raise NotVerifiable(
            "a defectives count exceeds its sample size — the payload is labelling DEFECTS "
            "as DEFECTIVES; a p chart is not the right chart for it")
    pbar = float(c.sum() / n.sum())
    se = np.sqrt(pbar * (1 - pbar) / n)
    # AIAG SPC-2 Ch. II: a negative limit is reported as zero, and a proportion cannot exceed 1
    ucl, lcl = np.minimum(pbar + 3 * se, 1.0), np.maximum(pbar - 3 * se, 0.0)
    phat = c / n
    ooc = _beyond(phat, lcl, ucl)
    return {
        "centerLine": pbar, "pBar": pbar, "processMean": pbar,
        "meanUCL": float(np.mean(ucl)), "meanLCL": float(np.mean(lcl)),
        "outOfControlCount": float(ooc), "flaggedCount": float(ooc),
    }


def control_chart_np(payload):
    """np chart (count nonconforming, CONSTANT n). Payload: {"defectCounts", "sampleSize"}.

    CL = n·p̄ with p̄ = Σd/(k·n); limits CL ± 3·sqrt(n·p̄(1-p̄)), LCL floored at 0.
    Unequal subgroup sizes are refused — an np chart is only defined for constant n.
    """
    c, n = _counts_and_sizes(payload, ("sampleSize", "sampleSizes", "subgroupSize", "n"))
    if np.any(c > n):
        raise NotVerifiable("a defectives count exceeds its sample size")
    if len(np.unique(n)) != 1:
        raise NotVerifiable("np chart requires a constant subgroup size")
    nn = float(n[0])
    pbar = float(c.sum() / (len(c) * nn))
    cl = nn * pbar
    sd = math.sqrt(nn * pbar * (1 - pbar))
    ucl, lcl = cl + 3 * sd, max(cl - 3 * sd, 0.0)
    out = {
        "centerLine": cl, "pBar": pbar,
        "ucl": float(ucl), "lcl": float(lcl),
        "outOfControlCount": float(_beyond(c, lcl, ucl)),
        "flaggedCount": float(_beyond(c, lcl, ucl)),
    }
    out.update({k: float(v) for k, v in nelson_flags(c, cl, sd).items()})
    return out


def control_chart_c(payload):
    """c chart (defect count per CONSTANT inspection unit). Payload: {"defectCounts": [...]}.

    CL = c̄ = mean count; limits c̄ ± 3·sqrt(c̄), LCL floored at 0 (AIAG SPC-2 Ch. II).
    """
    counts = payload.get("defectCounts", payload.get("counts"))
    if not isinstance(counts, (list, tuple)) or len(counts) < 2:
        raise NotVerifiable("no defectCounts series")
    c = np.asarray(counts, float)
    cbar = float(c.mean())
    sd = math.sqrt(cbar)
    ucl, lcl = cbar + 3 * sd, max(cbar - 3 * sd, 0.0)
    out = {
        "centerLine": cbar, "cBar": cbar, "processMean": cbar,
        "ucl": float(ucl), "lcl": float(lcl),
        "outOfControlCount": float(_beyond(c, lcl, ucl)),
        "flaggedCount": float(_beyond(c, lcl, ucl)),
    }
    out.update({k: float(v) for k, v in nelson_flags(c, cbar, sd).items()})
    return out


def control_chart_u(payload):
    """u chart (defects per unit). Payload: {"defectCounts": [...], "unitCounts": [...]}.

    CL = ū = Σc / Σn (pooled DPU); point-varying limits ū ± 3·sqrt(ū/n_i), LCL floored at 0.
    """
    c, n = _counts_and_sizes(payload, ("unitCounts", "inspectionUnits", "sampleSizes",
                                       "unitCount", "sampleSize", "n"))
    ubar = float(c.sum() / n.sum())
    se = np.sqrt(ubar / n)
    ucl, lcl = ubar + 3 * se, np.maximum(ubar - 3 * se, 0.0)
    u = c / n
    ooc = _beyond(u, lcl, ucl)
    return {
        "centerLine": ubar, "processMean": ubar, "uBar": ubar,
        "meanUCL": float(np.mean(ucl)), "meanLCL": float(np.mean(lcl)),
        "outOfControlCount": float(ooc), "flaggedCount": float(ooc),
    }


def _laney_sigma_z(z) -> float:
    """σ_Z = MR̄(z)/d2(2) over the standardized series — Laney (2002) QE 14(4) 531-537.

    σ_Z > 1 means overdispersion (the classic chart's limits are too tight); σ_Z < 1 means
    underdispersion. Minitab's P′/U′ charts multiply the classic limits by exactly this.
    """
    return float(np.mean(_moving_range(np.asarray(z, float))) / d2(2))


def control_chart_laney_p(payload):
    """Laney P′ chart. Payload: {"defectCounts": [...], "sampleSizes": [...]}.

    z_i = (p̂_i - p̄)/sqrt(p̄(1-p̄)/n_i); σ_Z = MR̄(z)/d2(2);
    limits p̄ ± 3·σ_Z·sqrt(p̄(1-p̄)/n_i). σ_Z is the whole point of the chart, so it is the
    field the corpus binds.
    """
    c, n = _counts_and_sizes(payload, ("sampleSizes", "sampleSize", "subgroupSizes", "n"))
    if np.any(c > n):
        raise NotVerifiable("a defectives count exceeds its sample size")
    pbar = float(c.sum() / n.sum())
    if not 0 < pbar < 1:
        raise NotVerifiable(f"degenerate p̄={pbar}")
    se = np.sqrt(pbar * (1 - pbar) / n)
    z = (c / n - pbar) / se
    sz = _laney_sigma_z(z)
    ucl = np.minimum(pbar + 3 * sz * se, 1.0)
    lcl = np.maximum(pbar - 3 * sz * se, 0.0)
    ooc = _beyond(c / n, lcl, ucl)
    return {
        "sigmaZ": sz, "centerLine": pbar, "pBar": pbar,
        "meanUCL": float(np.mean(ucl)), "meanLCL": float(np.mean(lcl)),
        "outOfControlCount": float(ooc), "flaggedCount": float(ooc),
    }


def control_chart_laney_u(payload):
    """Laney U′ chart. Payload: {"defectCounts": [...], "unitCounts": [...]}.

    z_i = (u_i - ū)/sqrt(ū/n_i); σ_Z = MR̄(z)/d2(2); limits ū ± 3·σ_Z·sqrt(ū/n_i).
    """
    c, n = _counts_and_sizes(payload, ("unitCounts", "inspectionUnits", "sampleSizes", "n"))
    ubar = float(c.sum() / n.sum())
    if ubar <= 0:
        raise NotVerifiable(f"degenerate ū={ubar}")
    se = np.sqrt(ubar / n)
    z = (c / n - ubar) / se
    sz = _laney_sigma_z(z)
    ucl, lcl = ubar + 3 * sz * se, np.maximum(ubar - 3 * sz * se, 0.0)
    ooc = _beyond(c / n, lcl, ucl)
    return {
        "sigmaZ": sz, "centerLine": ubar, "processMean": ubar, "uBar": ubar,
        "meanUCL": float(np.mean(ucl)), "meanLCL": float(np.mean(lcl)),
        "outOfControlCount": float(ooc), "flaggedCount": float(ooc),
    }


def capability_poisson(payload):
    counts = payload.get("defectCounts")
    units = payload.get("inspectionUnits")
    if counts is None or units is None:
        raise NotVerifiable("no counts/units")
    return {"dpu": float(np.sum(counts) / np.sum(units))}


def capability_binomial(payload):
    defects = payload.get("defectCounts", payload.get("defects"))
    sizes = payload.get("subgroupSizes", payload.get("sampleSizes"))
    if defects is None:
        raise NotVerifiable("no defect counts")
    total_n = float(np.sum(sizes)) if sizes else float(payload.get("totalTrials", 0))
    if not total_n:
        raise NotVerifiable("no trials")
    p = float(np.sum(defects)) / total_n
    return {"avgP": p, "processZ": float(stats.norm.ppf(1 - p))}


def _ols_design(payload):
    """(design matrix WITHOUT intercept, response) for either accepted regression shape.

    Shape A — {"x": [...], "y": [...], "degree": d}: the classic polynomial form, columns
    x, x², … x^d.
    Shape B — the corpus column table {"data": {col: [...]}, "responseColumn": name,
    "continuousPredictors": [...], "termsInModel": [...]}: one column per DECLARED term,
    each term a "*"-joined product of data columns, so "A*A" is the quadratic term and "A*B"
    the interaction. The declared terms are used verbatim rather than inferred — a payload
    that says cubic gets a cubic model, and a payload that declares an interaction does not
    get silently fitted as main effects only, either of which would change R² and the model
    F-test and so mis-report a correct truth as unreproducible.
    """
    x, y = payload.get("x"), payload.get("y")
    if x is not None and y is not None:
        x, y = np.asarray(x, float), np.asarray(y, float)
        degree = int(payload.get("degree", 1))
        return np.vander(x, degree + 1, increasing=True)[:, 1:], y

    data = payload.get("data")
    resp = payload.get("responseColumn")
    if not isinstance(data, dict) or resp not in data:
        raise NotVerifiable("no simple x/y regression structure and no data/responseColumn table")
    y = np.asarray(data[resp], float)
    terms = payload.get("termsInModel") or payload.get("continuousPredictors")
    if not terms:
        raise NotVerifiable("no termsInModel/continuousPredictors")
    cols = []
    for term in terms:
        col = np.ones(len(y), dtype=float)
        for factor in str(term).split("*"):
            name = factor.strip()
            if name not in data:
                raise NotVerifiable(f"term {term!r} references unknown column {name!r}")
            col = col * np.asarray(data[name], float)
        cols.append(col)
    return np.column_stack(cols), y


def ols(payload):
    """OLS on either the x/y(+degree) form or the corpus data/responseColumn column table.

    Reports R², adjusted R² and the overall model F-test p-value; k is the number of MODEL
    TERMS (excluding the intercept), which is what the F-test's numerator df must be.
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    Xt, y = _ols_design(payload)
    n, k = len(y), Xt.shape[1]
    if n <= k + 1:
        raise NotVerifiable(f"n={n} leaves no residual df for k={k} terms")
    X = np.column_stack([np.ones(n), Xt])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    ss_res, ss_tot = float(resid @ resid), float(np.sum((y - y.mean()) ** 2))
    if ss_tot == 0:
        raise NotVerifiable("response has zero variance")
    r2 = 1 - ss_res / ss_tot
    f = (r2 / k) / ((1 - r2) / (n - k - 1))
    return {
        "rSquaredPct": 100 * r2,
        "rSquaredAdjPct": 100 * (1 - (1 - r2) * (n - 1) / (n - k - 1)),
        "modelPValue": float(stats.f.sf(f, k, n - k - 1)),
    }


def runs_test(payload):
    x = _arr(payload, "data", "sequence", "values")
    med = float(np.mean(x)) if payload.get("aboutMean", True) else float(np.median(x))
    signs = x > med
    signs = signs[x != med] if np.any(x == med) else signs
    n1, n2 = int(np.sum(signs)), int(np.sum(~signs))
    runs = 1 + int(np.sum(signs[1:] != signs[:-1]))
    mu = 2 * n1 * n2 / (n1 + n2) + 1
    var = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
    z = (runs - mu) / math.sqrt(var)
    return {"pValue": float(2 * stats.norm.sf(abs(z)))}


def pareto(payload):
    counts = payload.get("counts") or payload.get("group_counts")
    if isinstance(counts, dict):
        vals = sorted(counts.values(), reverse=True)
    elif isinstance(counts, (list, tuple)):
        vals = sorted((float(c) for c in counts), reverse=True)
    else:
        raise NotVerifiable("no counts")
    total = sum(vals)
    return {"topCategoryPct": 100.0 * vals[0] / total}


def _flat_gage_layout(payload, flat):
    """A flat GRR reading list + declared dimensions -> the operator->parts dict.

    Payload: {"measurements": [...], "numParts": p, "numOperators": o, "numReplicates": r}.
    The dimensions must be DECLARED — they are never factored out of the length, because
    60 readings are 10x3x2 and also 5x4x3, and picking one would be a guess.

    LAYOUT CONVENTION: OPERATOR-MAJOR, then part, then replicate — index = ((operator * p) +
    part) * r + replicate. This is the AIAG MSA-4 gage study data-sheet order (each appraiser
    completes the full part set before the next begins) and it is the layout this corpus
    writes.

    It was not assumed: of the four candidate axis orders, operator-major reproduces
    adb_c05/M_GRR_4's stored %StudyVariation of 6.76 as 6.765, while part-major gives 94.6,
    operator-major-with-trials-outside gives 73.4 and part-then-replicate gives 84.3. One
    ordering agrees to four significant figures and the others are 11x-14x off, which
    identifies the layout rather than merely fitting it.
    """
    p_ = payload.get("numParts")
    o_ = payload.get("numOperators")
    r_ = payload.get("numReplicates")
    if None in (p_, o_, r_):
        raise NotVerifiable("flat measurements need numParts/numOperators/numReplicates")
    p_, o_, r_ = int(p_), int(o_), int(r_)
    if p_ < 2 or o_ < 2 or r_ < 2:
        raise NotVerifiable(f"need >=2 parts/operators/replicates, got {p_}/{o_}/{r_}")
    if len(flat) != p_ * o_ * r_:
        raise NotVerifiable(
            f"{len(flat)} readings do not fill {o_} operators x {p_} parts x {r_} replicates")
    arr = np.asarray(flat, float).reshape(o_, p_, r_)
    return {f"operator{i + 1}": arr[i].tolist() for i in range(o_)}


def gage_rr_crossed(payload):
    """Crossed Gage R&R via two-way ANOVA variance decomposition (Minitab conventions).

    Payload shape (native cases): {"measurements": {operator: [[rep, ...] per part, ...]}} —
    a dict mapping operator name -> list with one entry per part, each entry the list of that
    operator's replicate readings on that part. All operators measure the same parts in the
    same order. Flat lists / row tables (legacy payloads) are NOT verifiable here.

    Conventions (documented so the derivation is auditable):
      * full model WITH the operator*part interaction ALWAYS retained (no alpha-to-remove
        pruning, unlike Minitab's default drop-if-p>0.05 heuristic);
      * negative variance components floored at 0 (AIAG MSA-4 practice);
      * %StudyVariation = 100*sqrt(GRR/Total) — the 6*sigma study-variation multiplier
        cancels in the ratio of standard deviations;
      * ndc = floor(sqrt(2) * SD_part / SD_GRR).
    """
    meas = payload.get("measurements") if isinstance(payload, dict) else None
    if isinstance(meas, (list, tuple)) and meas and not isinstance(meas[0], (list, tuple)):
        meas = _flat_gage_layout(payload, meas)
    if not isinstance(meas, dict) or len(meas) < 2:
        raise NotVerifiable("measurements must be an operator->parts dict")
    rows = list(meas.values())
    if not all(isinstance(v, (list, tuple)) and v and isinstance(v[0], (list, tuple))
               for v in rows):
        raise NotVerifiable("each operator needs a list of per-part replicate lists")
    x = np.asarray(rows, dtype=float)                     # shape (o, p, r)
    if x.ndim != 3 or x.shape[1] < 2 or x.shape[2] < 2:
        raise NotVerifiable("need >=2 parts and >=2 replicates")
    o, p, r = x.shape
    grand = x.mean()
    op_means = x.mean(axis=(1, 2))
    part_means = x.mean(axis=(0, 2))
    cell_means = x.mean(axis=2)
    ss_op = p * r * float(np.sum((op_means - grand) ** 2))
    ss_part = o * r * float(np.sum((part_means - grand) ** 2))
    ss_int = r * float(np.sum(
        (cell_means - op_means[:, None] - part_means[None, :] + grand) ** 2))
    ss_err = float(np.sum((x - cell_means[:, :, None]) ** 2))
    ms_op = ss_op / (o - 1)
    ms_part = ss_part / (p - 1)
    ms_int = ss_int / ((o - 1) * (p - 1))
    ms_err = ss_err / (o * p * (r - 1))
    var_repeat = ms_err
    var_int = max((ms_int - ms_err) / r, 0.0)
    var_op = max((ms_op - ms_int) / (p * r), 0.0)
    var_part = max((ms_part - ms_int) / (o * r), 0.0)
    grr = var_repeat + var_op + var_int
    total = grr + var_part
    pct_sv = 100.0 * math.sqrt(grr / total)
    ndc = math.floor(math.sqrt(2.0) * math.sqrt(var_part / grr)) if grr > 0 else float("inf")
    return {"percentStudyVariation": float(pct_sv), "ndc": float(ndc)}


def _pivot_assessments(payload):
    """Pivot the legacy row table into (standard, ratings) — the shape this module analyses.

    Rows are {"appraiserId", "partId", "trial", "result", "standard"}; the same part appears
    once per (appraiser, trial). Item order is the FIRST APPEARANCE of each partId, not sorted
    — "P10" sorts before "P2" as a string, and a reordering silently misaligns every rating
    against the standard while still producing a plausible kappa.

    The pivot REFUSES rather than repairs whenever the table is not a complete crossed study:
    a part whose rows disagree about the standard, or an appraiser missing a reading, would
    otherwise be papered over into a wrong agreement rate.
    """
    rows = payload.get("assessments")
    if not isinstance(rows, (list, tuple)) or not rows:
        raise NotVerifiable("need standard list + ratings dict, or an assessments row table")
    order, standard, table = [], {}, {}
    for row in rows:
        if not isinstance(row, dict):
            raise NotVerifiable("assessments rows must be dicts")
        try:
            appraiser, part, trial = row["appraiserId"], row["partId"], row["trial"]
            result, ref = row["result"], row["standard"]
        except KeyError as exc:
            raise NotVerifiable(f"assessment row missing {exc}")
        if part not in standard:
            standard[part] = ref
            order.append(part)
        elif standard[part] != ref:
            raise NotVerifiable(
                f"part {part!r} carries conflicting standards {standard[part]!r} / {ref!r}")
        cell = table.setdefault(appraiser, {}).setdefault(trial, {})
        if part in cell:
            raise NotVerifiable(f"duplicate reading for {appraiser!r}/{part!r}/trial {trial!r}")
        cell[part] = result
    ratings = {}
    for appraiser, trials in table.items():
        per_trial = []
        for trial in sorted(trials, key=lambda t: (isinstance(t, str), t)):
            cell = trials[trial]
            missing = [p for p in order if p not in cell]
            if missing:
                raise NotVerifiable(
                    f"{appraiser!r} trial {trial!r} is missing parts {missing[:5]}")
            per_trial.append([cell[p] for p in order])
        ratings[appraiser] = per_trial
    return [standard[p] for p in order], ratings


def attribute_agreement(payload):
    """Attribute agreement analysis versus a known standard.

    Payload shape (native cases): {"standard": [label per item],
                                   "ratings": {appraiser: [[trial-1 labels], [trial-2 labels], ...]}}
    Every trial list is item-aligned with "standard". The legacy row table
    {"assessments": [{"appraiserId", "partId", "trial", "result", "standard"}, ...]} is also
    accepted and pivoted into that shape by _pivot_assessments().

    Conventions: per appraiser, pool all trials and compute Cohen's kappa against the standard
    (standard repeated once per trial); kappaMin = minimum kappa over appraisers;
    agreementPct = 100 * (individual ratings equal to standard) / (all ratings).
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    std = payload.get("standard")
    ratings = payload.get("ratings")
    if not isinstance(std, (list, tuple)) or not isinstance(ratings, dict) or not ratings:
        std, ratings = _pivot_assessments(payload)
    m = len(std)
    kappas, match, total = [], 0, 0
    for trials in ratings.values():
        if not isinstance(trials, (list, tuple)) or not all(
                isinstance(t, (list, tuple)) and len(t) == m for t in trials):
            raise NotVerifiable("each appraiser needs item-aligned trial lists")
        pooled = [lab for t in trials for lab in t]
        truth = list(std) * len(trials)
        n = len(pooled)
        match += sum(1 for a, s in zip(pooled, truth) if a == s)
        total += n
        po = sum(1 for a, s in zip(pooled, truth) if a == s) / n
        cats = sorted({*pooled, *truth}, key=str)
        pe = sum((pooled.count(c) / n) * (truth.count(c) / n) for c in cats)
        kappas.append(1.0 if pe >= 1.0 else (po - pe) / (1.0 - pe))
    return {"kappaMin": float(min(kappas)), "agreementPct": float(100.0 * match / total)}


def one_proportion(payload):
    """One-proportion test, normal approximation: z = (p̂ - p0)/sqrt(p0(1-p0)/n),
    two-sided p-value, NO continuity correction. Payload: {"events", "trials", "hypothesizedP"}."""
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    try:
        e, n, p0 = float(payload["events"]), float(payload["trials"]), float(payload["hypothesizedP"])
    except (KeyError, TypeError, ValueError) as exc:
        raise NotVerifiable(str(exc))
    if not (n > 0 and 0 < p0 < 1):
        raise NotVerifiable("bad trials/hypothesizedP")
    z = (e / n - p0) / math.sqrt(p0 * (1 - p0) / n)
    alt = _alternative(payload)
    p = (2 * stats.norm.sf(abs(z)) if alt == "two-sided"
         else stats.norm.cdf(z) if alt == "less"
         else stats.norm.sf(z))
    return {"pValue": float(p), "zStatistic": float(z)}


def _power_two_proportions_minitab(payload):
    """(p1, p2, nPerGroup) from the Minitab-style power payload.

    {"proportion1": p1, "proportion2Values": [p2, ...], "sampleSizes": [n, ...],
     "computationType": "POWER", "alpha": a}. Minitab sweeps the *Values / *Sizes lists to
    draw a power CURVE; a truth entry is a single scalar, so more than one entry in either
    list means the payload does not identify which point the truth refers to — refused, not
    guessed. A computationType asking for anything but POWER (e.g. SAMPLE_SIZE) is a
    different quantity entirely and is likewise refused.
    """
    comp = payload.get("computationType")
    if comp is not None and str(comp).strip().upper() not in ("POWER", "COMPUTE_POWER"):
        raise NotVerifiable(f"computationType={comp!r} does not ask for power")
    try:
        p1 = float(payload["proportion1"])
    except (KeyError, TypeError, ValueError) as exc:
        raise NotVerifiable(f"no p1/proportion1: {exc}")
    p2s = payload.get("proportion2Values")
    if p2s is None and payload.get("proportion2") is not None:
        p2s = [payload["proportion2"]]
    ns = payload.get("sampleSizes")
    if ns is None and payload.get("nPerGroup") is not None:
        ns = [payload["nPerGroup"]]
    for label, seq in (("proportion2Values", p2s), ("sampleSizes", ns)):
        if not isinstance(seq, (list, tuple)) or not seq:
            raise NotVerifiable(f"no {label}")
        if len(seq) != 1:
            raise NotVerifiable(
                f"{label} has {len(seq)} entries — a power curve has no single truth value")
    return p1, float(p2s[0]), float(ns[0])


def power_two_proportions(payload):
    """Power of the two-sided two-proportions test with equal group sizes.

    Payload: {"p1", "p2", "nPerGroup", "alpha"(default 0.05)}.
    Convention: statsmodels NormalIndPower with Cohen's effect size
    h = 2*asin(sqrt(p1)) - 2*asin(sqrt(p2)) (arcsine-transform normal approximation)."""
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    if "p1" in payload:
        try:
            p1, p2 = float(payload["p1"]), float(payload["p2"])
            n = float(payload["nPerGroup"])
        except (KeyError, TypeError, ValueError) as exc:
            raise NotVerifiable(str(exc))
    else:
        p1, p2, n = _power_two_proportions_minitab(payload)
    alpha = float(payload.get("alpha", 0.05))
    from statsmodels.stats.power import NormalIndPower
    h = abs(2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2)))
    pw = NormalIndPower().power(effect_size=h, nobs1=n, alpha=alpha, ratio=1.0,
                                alternative="two-sided")
    return {"power": float(pw)}


def equal_variances(payload):
    """Homogeneity of variances across k groups: Levene's test with MEDIAN centering
    (Brown-Forsythe). Bartlett's test answers the same question for near-normal data and lands
    within the wide soft tolerance cases attach to this p-value; the reference convention here
    is Levene/median. Payload: {"groups": {name: [...]}} or group1/group2/..."""
    r = stats.levene(*_all_groups(payload), center="median")
    return {"pValue": float(r.pvalue), "statistic": float(r.statistic)}


def poisson_regression(payload):
    """Poisson GLM (log link) deviance, from either the y/x form or the corpus column table.

    Column-table form: {"responseData": [...], "continuousData": {col: [...]},
    "continuousPredictors": [col, ...]} — predictors enter in the DECLARED order, since the
    deviance is order-invariant but the design must still contain exactly the declared columns.
    """
    import statsmodels.api as sm
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    y = payload.get("counts", payload.get("y"))
    x = payload.get("x")
    if y is None or x is None:
        y = payload.get("responseData")
        cont = payload.get("continuousData")
        names = payload.get("continuousPredictors")
        if y is None or not isinstance(cont, dict) or not names:
            raise NotVerifiable("no y/x and no responseData/continuousData table")
        missing = [n for n in names if n not in cont]
        if missing:
            raise NotVerifiable(f"continuousPredictors not in continuousData: {missing}")
        x = np.column_stack([np.asarray(cont[n], float) for n in names])
    X = sm.add_constant(np.asarray(x, float))
    fit = sm.GLM(np.asarray(y, float), X, family=sm.families.Poisson()).fit()
    return {"deviance": float(fit.deviance)}



# ======================================================================================
# DOE reference layer
# ======================================================================================
#
# CONVENTIONS. Every model below is ORDINARY LEAST SQUARES on the design as the payload
# DECLARES it — coded units where the payload is coded, engineering units where it is not.
# Nothing is re-coded, re-centred or re-scaled on the way in: a silent recoding changes the
# intercept, every interaction coefficient and every prediction interval, and would report a
# correct truth as unreproducible.
#
#   * ``termsInModel`` (when present) is honoured verbatim; "A*B" is a product column and
#     "A*A" a quadratic one. Absent, main effects only for a factorial column table.
#   * RSM run tables ({"runs": [{x1:.., x2:.., y:..}]}) get the FULL QUADRATIC model in the
#     declared coded factors: intercept, linear terms, pure quadratics, all two-factor
#     interactions (Montgomery DAOE 6e §11.3 — the second-order model a CCD is built to fit).
#     A factorial run table with a "coding" key and no centre/axial points gets the full
#     2^k model to the two-factor-interaction order, which is what a resolution-V design
#     supports and what the corpus generator fitted.
#   * PREDICTION vs CONFIDENCE intervals differ by one term and are BOTH reported, because
#     the two are routinely confused and the difference is exactly what a verifier exists to
#     catch:
#         CI half-width = t(1-α/2, n-p)·s·sqrt(x0'(X'X)⁻¹x0)
#         PI half-width = t(1-α/2, n-p)·s·sqrt(1 + x0'(X'X)⁻¹x0)
#     α from the payload's ``confidenceLevel``, default 0.95.
#   * The RSM optimizer maximises (or minimises) the fitted surface over the DECLARED bounds
#     by multi-start L-BFGS-B on a grid of starts, and — for a quadratic surface — also
#     solves the stationary point ∇ŷ = 0 in closed form and keeps it when it is feasible and
#     better. A single local search from one start is not a reference implementation.
#     Desirability follows Derringer & Suich (1980): for "maximize", d = 0 below the lower
#     bound of the observed response range, 1 at or above the upper, linear between; the
#     composite is the geometric mean over responses (one response here, so d itself).


def _doe_columns(payload):
    """(column dict, response name) for the column-table DOE shape."""
    data = payload.get("data")
    resp = payload.get("responseColumn", payload.get("response"))
    if not isinstance(data, dict) or resp not in data:
        raise NotVerifiable("no data/responseColumn column table")
    return data, resp


def _doe_terms(payload, data, resp):
    terms = payload.get("termsInModel")
    if not terms:
        factors = payload.get("factors")
        if isinstance(factors, (list, tuple)) and factors:
            terms = [f["name"] if isinstance(f, dict) else str(f) for f in factors]
        else:
            terms = [c for c in data if c != resp]
    return [str(t) for t in terms]


def _term_column(term, source, length):
    col = np.ones(length, dtype=float)
    for factor in term.split("*"):
        name = factor.strip()
        if name not in source:
            raise NotVerifiable(f"term {term!r} references unknown column {name!r}")
        col = col * np.asarray(source[name], float)
    return col


def _term_value(term, point):
    val = 1.0
    for factor in term.split("*"):
        name = factor.strip()
        if name not in point:
            raise NotVerifiable(f"prediction point does not set {name!r}")
        val *= float(point[name])
    return val


def _run_table_columns(runs, response_key="y"):
    """{name: column} from a list of run dicts, response under ``response_key``."""
    if not isinstance(runs, (list, tuple)) or len(runs) < 3:
        raise NotVerifiable("no runs table")
    names = [k for k in runs[0] if k != response_key]
    if not names or any(response_key not in r for r in runs):
        raise NotVerifiable(f"runs table has no {response_key!r} response column")
    cols = {n: np.asarray([float(r[n]) for r in runs], float) for n in names}
    y = np.asarray([float(r[response_key]) for r in runs], float)
    return cols, y, names


def _quadratic_terms(names):
    """[linear..., pure quadratics..., two-factor interactions...] — declared order kept."""
    terms = list(names)
    terms += [f"{n}*{n}" for n in names]
    terms += [f"{a}*{b}" for i, a in enumerate(names) for b in names[i + 1:]]
    return terms


def _two_factor_terms(names):
    return list(names) + [f"{a}*{b}" for i, a in enumerate(names) for b in names[i + 1:]]


def _fit_ols(cols, y, terms):
    X = np.column_stack([np.ones(len(y))] + [_term_column(t, cols, len(y)) for t in terms])
    n, p = X.shape
    if n <= p:
        raise NotVerifiable(f"n={n} runs cannot fit {p} coefficients")
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    ss_res = float(resid @ resid)
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    if ss_tot <= 0:
        raise NotVerifiable("response has zero variance")
    return X, beta, ss_res, ss_tot


def _model_stats(X, beta, ss_res, ss_tot, y):
    n, p = X.shape
    k = p - 1
    r2 = 1 - ss_res / ss_tot
    dfe = n - p
    out = {"rSquaredPct": 100 * r2, "residualDf": float(dfe)}
    if dfe > 0:
        out["rSquaredAdjPct"] = 100 * (1 - (1 - r2) * (n - 1) / dfe)
        out["sigma"] = math.sqrt(ss_res / dfe)
        if r2 < 1:
            f = (r2 / k) / ((1 - r2) / dfe)
            out["modelPValue"] = float(stats.f.sf(f, k, dfe))
            out["fStatistic"] = float(f)
    return out


def _lack_of_fit(cols, y, ss_res, dfe, names):
    """Pure-error / lack-of-fit F test, using EXACT duplicate design points as replicates."""
    if dfe <= 0:
        return {}
    keys = {}
    for i in range(len(y)):
        keys.setdefault(tuple(round(float(cols[n][i]), 12) for n in names), []).append(i)
    reps = [idx for idx in keys.values() if len(idx) > 1]
    if not reps:
        return {}
    ss_pe = sum(float(np.sum((y[idx] - y[idx].mean()) ** 2)) for idx in reps)
    df_pe = sum(len(idx) - 1 for idx in reps)
    df_lof = dfe - df_pe
    if df_lof <= 0 or df_pe <= 0 or ss_pe <= 0:
        return {}
    ss_lof = ss_res - ss_pe
    f = (ss_lof / df_lof) / (ss_pe / df_pe)
    return {"lackOfFitPValue": float(stats.f.sf(f, df_lof, df_pe)),
            "lackOfFitF": float(f), "pureErrorDf": float(df_pe)}


def _rsm_fit(payload):
    """(cols, y, names, terms, X, beta, ss_res, ss_tot) for an RSM run/surface table."""
    runs = (payload.get("runs") or payload.get("surface_data")
            or payload.get("surfaceData") or payload.get("design_points"))
    if not isinstance(runs, (list, tuple)):
        raise NotVerifiable("no runs/surface_data table")
    cols, y, names = _run_table_columns(runs)
    terms = _quadratic_terms(names)
    X, beta, ss_res, ss_tot = _fit_ols(cols, y, terms)
    return cols, y, names, terms, X, beta, ss_res, ss_tot


def doe_rsm_analysis(payload):
    """Second-order response-surface model. Payload: {"runs": [{code: level, ..., "y": ..}]}.

    Full quadratic in the declared coded factors (see the section note). Reports R², adjusted
    R², the model F-test and — where the design carries replicated points, as a CCD's centre
    runs do — the lack-of-fit test against pure error.
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    cols, y, names, terms, X, beta, ss_res, ss_tot = _rsm_fit(payload)
    out = _model_stats(X, beta, ss_res, ss_tot, y)
    out.update(_lack_of_fit(cols, y, ss_res, X.shape[0] - X.shape[1], names))
    out["termCount"] = float(len(terms))
    return out


def doe_rsm_canonical(payload):
    """Canonical analysis of the fitted quadratic surface: stationary point and its response.

    ∇ŷ = 0 solved in closed form (b + 2Bx = 0 for ŷ = b0 + b'x + x'Bx); the eigenvalues of B
    classify the surface (all negative = maximum, all positive = minimum, mixed = saddle).
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    cols, y, names, terms, X, beta, ss_res, ss_tot = _rsm_fit(payload)
    xs, Bm, grad = _quadratic_stationary(beta, names)
    if xs is None:
        raise NotVerifiable("quadratic form is singular — no unique stationary point")
    eig = np.linalg.eigvalsh(Bm)
    return {
        "predictedAtStationary": float(_quadratic_predict(beta, names, terms, xs)),
        "minEigenvalue": float(np.min(eig)), "maxEigenvalue": float(np.max(eig)),
        **{f"stationary_{n}": float(v) for n, v in zip(names, xs)},
    }


def _quadratic_stationary(beta, names):
    """(x*, B, b) for ŷ = b0 + b'x + x'Bx read off the coefficient vector."""
    k = len(names)
    b = np.asarray(beta[1:1 + k], float)
    Bm = np.zeros((k, k))
    for i in range(k):
        Bm[i, i] = beta[1 + k + i]
    idx = 1 + 2 * k
    for i in range(k):
        for j in range(i + 1, k):
            Bm[i, j] = Bm[j, i] = beta[idx] / 2.0
            idx += 1
    try:
        xs = np.linalg.solve(2 * Bm, -b)
    except np.linalg.LinAlgError:
        return None, Bm, b
    return xs, Bm, b


def _quadratic_predict(beta, names, terms, point):
    pt = {n: float(v) for n, v in zip(names, np.asarray(point, float).ravel())}
    x0 = np.array([1.0] + [_term_value(t, pt) for t in terms])
    return float(x0 @ beta)


def doe_rsm_optimizer(payload):
    """Constrained optimum of the fitted surface + Derringer-Suich desirability.

    Payload: {"surface_data": [{code: level, ..., "y": ..}], "goal": "maximize"|"minimize",
              "bounds": [[lo, hi], ...] in the same order as the factor columns}.

    Multi-start L-BFGS-B over a grid of starts inside ``bounds``, PLUS the closed-form
    stationary point when it is feasible — a single local search is not a reference.
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    cols, y, names, terms, X, beta, ss_res, ss_tot = _rsm_fit(payload)
    goal = str(payload.get("goal", "maximize")).strip().lower()
    if goal not in ("maximize", "minimize", "max", "min"):
        raise NotVerifiable(f"unsupported goal {payload.get('goal')!r}")
    maximize = goal.startswith("max")
    bounds = payload.get("bounds")
    if not isinstance(bounds, (list, tuple)) or len(bounds) != len(names):
        raise NotVerifiable(f"bounds must give one [lo, hi] per factor ({len(names)})")
    bounds = [(float(lo), float(hi)) for lo, hi in bounds]

    sign = -1.0 if maximize else 1.0
    obj = lambda v: sign * _quadratic_predict(beta, names, terms, v)
    grids = [np.linspace(lo, hi, 5) for lo, hi in bounds]
    best = None
    for start in itertools.product(*grids):
        r = optimize.minimize(obj, np.asarray(start, float), bounds=bounds, method="L-BFGS-B")
        if best is None or r.fun < best[0]:
            best = (float(r.fun), np.asarray(r.x, float))
    xs, _, _ = _quadratic_stationary(beta, names)
    if xs is not None and all(lo <= v <= hi for v, (lo, hi) in zip(xs, bounds)):
        f_st = obj(xs)
        if f_st < best[0]:
            best = (float(f_st), xs)
    value = sign * best[0]
    lo_y, hi_y = float(np.min(y)), float(np.max(y))
    if hi_y > lo_y:
        d = (value - lo_y) / (hi_y - lo_y) if maximize else (hi_y - value) / (hi_y - lo_y)
        d = float(min(max(d, 0.0), 1.0))
    else:
        d = 1.0
    return {
        "predictedResponse": float(value),
        "compositeDesirability": d,
        "individualDesirability": d,
        **{f"optimal_{n}": float(v) for n, v in zip(names, best[1])},
    }


def doe_factorial_analysis(payload):
    """Factorial model fit. Accepts the column table ({"data", "responseColumn",
    "termsInModel"}) and the coded run table ({"runs": [{A:.., B:.., "y":..}], "coding": ..}).

    For a run table the model runs to the two-factor-interaction order (all main effects plus
    every AB pair), which is what the corpus generator fitted and what a 2^k design supports
    without aliasing main effects.
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    if isinstance(payload.get("runs"), (list, tuple)):
        cols, y, names = _run_table_columns(payload["runs"])
        terms = _two_factor_terms(names)
    else:
        data, resp = _doe_columns(payload)
        terms = _doe_terms(payload, data, resp)
        y = np.asarray(data[resp], float)
        cols = {k: np.asarray(v, float) for k, v in data.items()}
    X, beta, ss_res, ss_tot = _fit_ols(cols, y, terms)
    out = _model_stats(X, beta, ss_res, ss_tot, y)
    out["termCount"] = float(len(terms))
    return out


def doe_factorial_prediction(payload, blocks=None):
    """Point prediction + confidence AND prediction intervals from a fitted factorial model.

    Two payload shapes, both in the corpus:
      A) self-contained — {"data": {col: [...]}, "responseColumn", "termsInModel",
         "predictionPoints": [{col: level}], "confidenceLevel"}.
      B) a REFERENCE to the stage that holds the design — {"model_from": "<stage_id>",
         "settings": {factor: level}}. The model is refitted from THAT stage's run table
         (two-factor-interaction order, as ``doe_factorial_analysis`` does), then evaluated at
         ``settings``. This shape is why the verifier takes the sibling blocks: a prediction
         truth whose design lives in another stage is not verifiable from its own payload
         alone, and skipping it is precisely the silent gap this module exists to close.
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    ref = payload.get("model_from") or payload.get("modelFrom")
    if ref is not None:
        if not isinstance(blocks, dict) or ref not in blocks:
            raise NotVerifiable(f"model_from={ref!r} but that stage's block was not supplied")
        source = blocks[ref]
        if not isinstance(source.get("runs"), (list, tuple)):
            raise NotVerifiable(f"stage {ref!r} carries no runs table to refit")
        cols, y, names = _run_table_columns(source["runs"])
        terms = _two_factor_terms(names)
        point = payload.get("settings") or payload.get("predictionPoint")
        if not isinstance(point, dict):
            raise NotVerifiable("no settings/predictionPoint")
        points = [point]
        conf = float(payload.get("confidenceLevel", source.get("confidenceLevel", 0.95)))
    else:
        data, resp = _doe_columns(payload)
        terms = _doe_terms(payload, data, resp)
        y = np.asarray(data[resp], float)
        cols = {k: np.asarray(v, float) for k, v in data.items()}
        points = payload.get("predictionPoints") or (
            [payload["predictionPoint"]] if isinstance(payload.get("predictionPoint"), dict)
            else None)
        if not points:
            raise NotVerifiable("no predictionPoints")
        conf = float(payload.get("confidenceLevel", 0.95))
    if len(points) != 1:
        raise NotVerifiable(
            f"{len(points)} prediction points — a scalar truth does not say which one")
    if not 0 < conf < 1:
        conf = conf / 100.0 if 1 < conf < 100 else conf
    if not 0 < conf < 1:
        raise NotVerifiable(f"bad confidenceLevel {payload.get('confidenceLevel')!r}")

    X, beta, ss_res, _ = _fit_ols(cols, y, terms)
    n, p = X.shape
    dfe = n - p
    if dfe <= 0:
        raise NotVerifiable("saturated model leaves no residual df for an interval")
    s2 = ss_res / dfe
    x0 = np.array([1.0] + [_term_value(t, points[0]) for t in terms])
    lev = float(x0 @ np.linalg.pinv(X.T @ X) @ x0)
    yhat = float(x0 @ beta)
    tcrit = float(stats.t.ppf(1 - (1 - conf) / 2, dfe))
    half_ci = tcrit * math.sqrt(max(s2 * lev, 0.0))
    half_pi = tcrit * math.sqrt(max(s2 * (1 + lev), 0.0))
    return {
        "predictedValue": yhat, "fittedValue": yhat,
        "piLower": yhat - half_pi, "piUpper": yhat + half_pi,
        "ciLower": yhat - half_ci, "ciUpper": yhat + half_ci,
        "seFit": math.sqrt(max(s2 * lev, 0.0)), "residualDf": float(dfe),
    }


doe_factorial_prediction.wants_blocks = True


def fmea_rpn(payload):
    """FMEA risk priority numbers. Payload: {"items": [{"severity","occurrence","detection"}]}.

    RPN = S x O x D per item, on whatever 1-10 scale the payload declares (the scale text is
    not data). ``maxRpn`` is the largest, which is the number that decides where the team
    starts. ``aboveThresholdCount`` uses the payload's own ``rpnThreshold`` when it declares
    one; no default threshold is invented, because 100 and 125 are both common house rules and
    picking one silently would manufacture a disagreement.
    """
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    items = payload.get("items")
    if not isinstance(items, (list, tuple)) or not items:
        raise NotVerifiable("no items list")
    rpns = []
    for it in items:
        if not isinstance(it, dict):
            raise NotVerifiable("FMEA items must be dicts")
        try:
            rpns.append(float(it["severity"]) * float(it["occurrence"]) * float(it["detection"]))
        except (KeyError, TypeError, ValueError) as exc:
            raise NotVerifiable(f"FMEA item missing severity/occurrence/detection: {exc}")
    out = {"maxRpn": float(max(rpns)), "meanRpn": float(np.mean(rpns)),
           "totalRpn": float(np.sum(rpns)), "itemCount": float(len(rpns))}
    thr = payload.get("rpnThreshold")
    if thr is not None:
        out["aboveThresholdCount"] = float(sum(1 for r in rpns if r >= float(thr)))
    return out


def binary_logistic(payload):
    """Binary logistic regression. Payload: {"x": [...], "outcomes": [0/1, ...]}.

    Logit link, intercept + the declared predictor(s). ``modelPValue`` is the LIKELIHOOD-RATIO
    test of the whole model against the intercept-only null (statsmodels ``llr_pvalue``) — not
    a Wald test on a single coefficient, which is a different statistic that happens to be
    close on well-behaved data and is what a careless reference would compute instead.
    """
    import statsmodels.api as sm
    if not isinstance(payload, dict):
        raise NotVerifiable("payload not a dict")
    y = payload.get("outcomes", payload.get("y", payload.get("responseData")))
    if not isinstance(y, (list, tuple)) or len(y) < 4:
        raise NotVerifiable("no outcomes/y binary response")
    yv = np.asarray(y, float)
    if not set(np.unique(yv)).issubset({0.0, 1.0}) or len(np.unique(yv)) < 2:
        raise NotVerifiable("response is not a non-degenerate 0/1 series")
    x = payload.get("x")
    if isinstance(x, (list, tuple)) and x and not isinstance(x[0], (list, tuple)):
        X = np.asarray(x, float).reshape(-1, 1)
    elif isinstance(x, (list, tuple)) and x:
        X = np.asarray(x, float)
    else:
        cont = payload.get("continuousData")
        names = payload.get("continuousPredictors")
        if not isinstance(cont, dict) or not names:
            raise NotVerifiable("no x and no continuousData/continuousPredictors table")
        missing = [n for n in names if n not in cont]
        if missing:
            raise NotVerifiable(f"continuousPredictors not in continuousData: {missing}")
        X = np.column_stack([np.asarray(cont[n], float) for n in names])
    if len(X) != len(yv):
        raise NotVerifiable(f"predictor/response length mismatch: {len(X)} vs {len(yv)}")
    fit = sm.Logit(yv, sm.add_constant(X)).fit(disp=0)
    return {"modelPValue": float(fit.llr_pvalue), "logLikelihood": float(fit.llf),
            "llrStatistic": float(fit.llr), "pseudoRSquared": float(fit.prsquared)}


def anova_sov(payload):
    """Sources-of-variation decomposition for stratified/nested sampling.

    Payload: {"groups": {stratum: [...]}} (or any k-group shape this module reads).

    Conventions:
      * ``totalVariance`` is the TOTAL sample variance of every observation pooled,
        Sigma(x - grand mean)^2 / (N-1) — the plain variance of the whole data set, not the sum
        of the estimated components (the two differ, and only one of them is what a total
        variance means).
      * The random-effects one-way components are reported alongside on the standard
        expected-mean-square identities for BALANCED groups:
            withinVariance  = MSE
            betweenVariance = max((MSB - MSE)/n, 0)     (negative estimates floored at 0,
                                                         AIAG MSA-4 practice)
        with n the common group size; for UNBALANCED groups n is replaced by
        n0 = (N - Sigma n_i^2 / N)/(k-1), the standard unbalanced correction. Components are
        omitted rather than approximated when fewer than two groups carry replicates.
    """
    groups = _all_groups(payload)
    allx = np.concatenate(groups)
    N, k = len(allx), len(groups)
    if N < 2:
        raise NotVerifiable("need >=2 observations")
    out = {"totalVariance": float(np.var(allx, ddof=1)),
           "grandMean": float(np.mean(allx)), "groupCount": float(k)}
    sizes = np.array([len(g) for g in groups], float)
    if k >= 2 and np.all(sizes >= 2):
        grand = allx.mean()
        ss_b = float(np.sum(sizes * np.array([g.mean() - grand for g in groups]) ** 2))
        ss_w = float(np.sum([np.sum((g - g.mean()) ** 2) for g in groups]))
        ms_b, ms_w = ss_b / (k - 1), ss_w / (N - k)
        n0 = sizes[0] if len(np.unique(sizes)) == 1 else \
            (N - float(np.sum(sizes ** 2)) / N) / (k - 1)
        out["withinVariance"] = float(ms_w)
        out["betweenVariance"] = float(max((ms_b - ms_w) / n0, 0.0))
        out["componentSumVariance"] = out["withinVariance"] + out["betweenVariance"]
    return out

REFERENCE_IMPLS = {
    "msa.gage_rr_crossed": gage_rr_crossed,
    "msa.attribute_agreement": attribute_agreement,
    "basic.descriptive_summary": descriptive_summary,
    "basic.normality": normality,
    "basic.one_sample_t": one_sample_t,
    "basic.two_sample_t": two_sample_t,
    "basic.paired_t": paired_t,
    "basic.correlation": correlation,
    "basic.one_proportion": one_proportion,
    "basic.two_proportions": two_proportions,
    "power.two_proportions": power_two_proportions,
    "anova.oneway": anova_oneway,
    "anova.equal_variances": equal_variances,
    "nonparametric.mann_whitney": mann_whitney,
    "nonparametric.kruskal_wallis": kruskal_wallis,
    "nonparametric.one_sample_wilcoxon": one_sample_wilcoxon,
    "nonparametric.moods_median": moods_median,
    "nonparametric.runs_test": runs_test,
    "tables.chisquare_gof": chisquare_gof,
    "tables.chisquare_assoc": chisquare_assoc,
    "capability.normal": capability_normal,
    "capability.grouped": capability_grouped,
    "capability.nonnormal": capability_nonnormal,
    "capability.poisson": capability_poisson,
    "capability.binomial": capability_binomial,
    "control_chart.imr": control_chart_imr,
    "control_chart.xbar_r": control_chart_xbar_r,
    "control_chart.xbar_s": control_chart_xbar_s,
    "control_chart.ewma": control_chart_ewma,
    "control_chart.cusum": control_chart_cusum,
    "control_chart.p": control_chart_p,
    "control_chart.np": control_chart_np,
    "control_chart.c": control_chart_c,
    "control_chart.u": control_chart_u,
    "control_chart.laney_p": control_chart_laney_p,
    "control_chart.laney_u": control_chart_laney_u,
    "doe.factorial_analysis": doe_factorial_analysis,
    "doe.factorial_prediction": doe_factorial_prediction,
    "doe.rsm_analysis": doe_rsm_analysis,
    "doe.rsm_canonical": doe_rsm_canonical,
    "doe.rsm_optimizer": doe_rsm_optimizer,
    "regression.ols": ols,
    "regression.poisson": poisson_regression,
    "quality.pareto": pareto,
    "quality.fmea_rpn": fmea_rpn,
    "regression.binary_logistic": binary_logistic,
    "anova.sov": anova_sov,
}


def wants_blocks(fn) -> bool:
    """True when a reference impl needs the case's OTHER stage payloads as a 2nd argument.

    A DOE prediction whose design lives in a sibling stage cannot be recomputed from its own
    block. Rather than teach the validator a hard-coded list of such methods, each verifier
    declares the need itself.
    """
    return bool(getattr(fn, "wants_blocks", False))


# ======================================================================================
# Alternative-convention reference layer
# ======================================================================================
#
# Everything above computes THE convention a truth was frozen under. This section computes
# the OTHER defensible one, so that ``TruthEntry.accepts`` can be populated with a number
# somebody derived rather than a number somebody typed.
#
# Why it has to exist at all: the numeric-fidelity axis could not fail. 45 of the corpus's
# 118 registry truths were ``soft``, and a soft miss enters neither the numerator nor the
# denominator of nf.py's ratio -- on those entries WRONG and SILENT are the same verdict.
# Most of them were soft because nobody had discharged the doubt; the ones that genuinely ARE
# convention-variant can only be hardened once the second convention is admitted at its own
# precision, which is what ``accepts`` does and what these functions supply the numbers for.
#
# Each variant is a NAMED default of a real toolchain, not a plausible-looking recomputation:
#
#   yates_continuity      R's ``prop.test()`` applies Yates' continuity correction;
#                         statsmodels' ``proportions_ztest`` does not. Both are correct.
#   exact_binomial        Minitab's 1 Proportion offers the exact binomial test; the normal
#                         approximation is the other offering.
#   pooled_equal_variance Student's pooled-variance two-sample t, against Welch's default.
#   welch_anova           Welch's heteroscedastic one-way F (R's ``oneway.test`` default),
#                         against the classic pooled-error F.
#   bartlett /            Minitab's Test for Equal Variances reports Bartlett for normal data
#   levene_mean           and Levene/Brown-Forsythe otherwise; SciPy's ``levene`` centres on
#                         the mean by default where this corpus centres on the median.
#   shapiro_wilk          R's ``shapiro.test`` is the default normality test where Minitab's
#                         is Anderson-Darling. Same question, different statistic and p-value.
#
# THE GATING RULES, applied by ``convention_windows`` and deliberately conservative, because a
# second window can only ever make a truth EASIER to satisfy:
#
#   1. A payload that DECLARES the convention suppresses its variant. That is the corpus's
#      standing policy (see TruthEntry.accepts and cases/legacy_bridge._CONVENTION_BY_SHAPE):
#      where the task states which default to take, taking the other one is a failure to read
#      the specification, not a convention difference.
#   2. A variant already inside the primary window is dropped. It admits nothing new, and an
#      accepts entry that changes no verdict is noise in the audit trail.
#   3. A variant's own tolerance is min(primary tol, gap/4, (gap - primary tol)/2) -- never
#      wider than the primary, and provably NON-TOUCHING: the last term is what guarantees
#      that a value between the two windows fails, which gap/4 alone does not when the primary
#      tolerance is itself a large fraction of the gap. Widening the primary instead is the
#      wrong tool: stretching adb_c03's two-proportion window to admit Yates needs +/-0.0113,
#      which then admits almost anything.

def two_proportions_yates(payload):
    """R's ``prop.test()`` default: pooled z with Yates' continuity correction."""
    try:
        e1, t1 = float(payload["events1"]), float(payload["trials1"])
        e2, t2 = float(payload["events2"]), float(payload["trials2"])
    except (KeyError, TypeError) as exc:
        raise NotVerifiable(str(exc))
    p1, p2 = e1 / t1, e2 / t2
    p = (e1 + e2) / (t1 + t2)
    se = math.sqrt(p * (1 - p) * (1 / t1 + 1 / t2))
    d = max(0.0, abs(p1 - p2) - 0.5 * (1 / t1 + 1 / t2))
    z = math.copysign(d, p1 - p2) / se
    return {"pValue": float(2 * stats.norm.sf(abs(z))), "zStatistic": float(z)}


def one_proportion_yates(payload):
    """One-proportion normal approximation WITH the continuity correction (R prop.test)."""
    try:
        e, n = float(payload["events"]), float(payload["trials"])
        p0 = float(payload["hypothesizedP"])
    except (KeyError, TypeError) as exc:
        raise NotVerifiable(str(exc))
    if not (n > 0 and 0 < p0 < 1):
        raise NotVerifiable("bad trials/hypothesizedP")
    d = max(0.0, abs(e / n - p0) - 0.5 / n)
    z = math.copysign(d, e / n - p0) / math.sqrt(p0 * (1 - p0) / n)
    return {"pValue": float(2 * stats.norm.sf(abs(z))), "zStatistic": float(z)}


def one_proportion_exact(payload):
    """Minitab's exact binomial test for one proportion (its default at small n)."""
    try:
        e, n = int(payload["events"]), int(payload["trials"])
        p0 = float(payload["hypothesizedP"])
    except (KeyError, TypeError, ValueError) as exc:
        raise NotVerifiable(str(exc))
    if not (n > 0 and 0 < p0 < 1):
        raise NotVerifiable("bad trials/hypothesizedP")
    return {"pValue": float(stats.binomtest(e, n, p0,
                                            alternative=_alternative(payload)).pvalue)}


def two_sample_t_pooled(payload):
    """Student's pooled-variance two-sample t, against ``two_sample_t``'s Welch default."""
    a, b = _two_groups(payload)
    r = stats.ttest_ind(a, b, equal_var=True, alternative=_alternative(payload))
    return {"pValue": float(r.pvalue), "tStatistic": float(r.statistic)}


def anova_oneway_welch(payload):
    """Welch's heteroscedastic one-way F -- R's ``oneway.test()`` default.

    Written out rather than delegated to SciPy: ``f_oneway(equal_var=False)`` only exists in
    recent SciPy, and a reference implementation that silently disappears under an older pin
    is worse than one that is six lines long. Welch (1951, Biometrika 38, 330-336).
    """
    ks = [np.asarray(x, float) for x in _all_groups(payload)]
    k = len(ks)
    if k < 2 or any(len(x) < 2 or x.var(ddof=1) <= 0 for x in ks):
        raise NotVerifiable("Welch's F needs >=2 groups with positive within-group variance")
    w = [len(x) / x.var(ddof=1) for x in ks]
    sw = sum(w)
    mbar = sum(wi * x.mean() for wi, x in zip(w, ks)) / sw
    lam = sum((1 - wi / sw) ** 2 / (len(x) - 1) for wi, x in zip(w, ks))
    num = sum(wi * (x.mean() - mbar) ** 2 for wi, x in zip(w, ks)) / (k - 1)
    f = num / (1 + 2 * (k - 2) / (k * k - 1) * lam)
    df2 = 1.0 / (3.0 / (k * k - 1) * lam)
    return {"fStatistic": float(f), "factorPValue": float(stats.f.sf(f, k - 1, df2))}


def equal_variances_bartlett(payload):
    """Bartlett's test -- Minitab's recommended equal-variance test for normal data."""
    r = stats.bartlett(*_all_groups(payload))
    return {"pValue": float(r.pvalue), "statistic": float(r.statistic)}


def equal_variances_levene_mean(payload):
    """Levene's original mean-centred test, against this corpus's median centring."""
    r = stats.levene(*_all_groups(payload), center="mean")
    return {"pValue": float(r.pvalue), "statistic": float(r.statistic)}


def normality_shapiro(payload):
    """Shapiro-Wilk -- R's ``shapiro.test``, against Anderson-Darling.

    Only ``pValue`` is emitted. W and A-squared are DIFFERENT QUANTITIES on different scales,
    so offering W as a variant window for a truth bound to ``statistic`` would admit an
    unrelated number under a name it does not belong to; the p-value is the quantity the two
    tests genuinely both answer.
    """
    x = _arr(payload, "data", "values", "measurements")
    if len(x) < 3:
        raise NotVerifiable("Shapiro-Wilk needs n >= 3")
    return {"pValue": float(stats.shapiro(x).pvalue)}


def chisquare_assoc_yates(payload):
    """R's ``chisq.test()`` default on a 2x2 table: Yates' continuity correction.

    Refused on any other shape, because R applies the correction to 2x2 tables ONLY and a
    "corrected" 3x2 is not a convention anyone's toolchain produces.
    """
    table = payload.get("table") or payload.get("contingencyTable")
    if not table:
        raise NotVerifiable("no table/contingencyTable")
    arr = np.asarray(table, float)
    if arr.shape != (2, 2):
        raise NotVerifiable("Yates' correction is a 2x2-only default")
    r = stats.chi2_contingency(arr, correction=True)
    return {"statistic": float(r.statistic), "pValue": float(r.pvalue)}


#: method_id -> ((convention name, reference impl, declaration keys that suppress it), ...)
#:
#: A declaration key present in the payload means the task STATES which convention to use, so
#: the variant is not admitted -- see gating rule 1 above.
CONVENTION_VARIANTS = {
    "basic.two_proportions": (
        ("yates_continuity", two_proportions_yates, ("continuityCorrection",)),
    ),
    "basic.one_proportion": (
        ("yates_continuity", one_proportion_yates, ("continuityCorrection",)),
        ("exact_binomial", one_proportion_exact, ("testMethod", "exactTest")),
    ),
    "basic.two_sample_t": (
        ("pooled_equal_variance", two_sample_t_pooled, ("assumeEqualVariances",)),
    ),
    "anova.oneway": (
        ("welch_anova", anova_oneway_welch, ("assumeEqualVariances",)),
    ),
    "anova.equal_variances": (
        ("bartlett", equal_variances_bartlett, ("varianceTestCentering", "varianceTest")),
        ("levene_mean", equal_variances_levene_mean, ("varianceTestCentering", "varianceTest")),
    ),
    "basic.normality": (
        ("shapiro_wilk", normality_shapiro, ("normalityTest",)),
    ),
    "tables.chisquare_assoc": (
        ("yates_continuity", chisquare_assoc_yates, ("continuityCorrection",)),
    ),
}

#: Variant windows are never wider than the primary window, and are additionally narrowed so
#: that the space between the two conventions stays a failure -- see gating rule 3.
_VARIANT_GAP_DIVISOR = 4.0


def convention_windows(method_id: str, field: str, payload, expected: float, tol: float,
                       blocks=None) -> tuple:
    """``TruthEntry.accepts`` for one truth: every alternative convention worth admitting.

    Returns ``((name, expected, tol), ...)`` COMPUTED from the payload -- a generator calls
    this instead of hand-writing a second number, so a variant's audit trail is the same
    reference layer that verifies the primary.

    Returns ``()`` -- and that is the common answer -- when the payload declares the
    convention, when no alternative is defined for the method, when the alternative lands
    inside the primary window anyway, or when the reference refuses the payload.
    """
    out, seen = [], []
    for name, fn, decl_keys in CONVENTION_VARIANTS.get(method_id, ()):
        if isinstance(payload, dict) and any(k in payload for k in decl_keys):
            continue
        try:
            ref = fn(payload, blocks) if wants_blocks(fn) else fn(payload)
        except NotVerifiable:
            continue
        except Exception:                      # a variant is a bonus, never a build failure
            continue
        val = ref.get(field)
        if val is None:
            continue
        val = float(val)
        if not math.isfinite(val):
            continue
        gap = abs(val - float(expected))
        if gap <= float(tol):                  # rule 2: admits nothing new
            continue
        if any(abs(val - v) <= 1e-12 for v in seen):
            continue
        seen.append(val)
        width = min(float(tol), gap / _VARIANT_GAP_DIVISOR, 0.5 * (gap - float(tol)))
        if width <= 0:
            continue
        out.append((name, round(val, 12), round(width, 12)))
    return tuple(out)


# --------------------------------------------------------------------------- second-domain pilot
# RNA-seq and GWAS reference implementations live in their own module so this file stays the
# quality-engineering layer; they register here so the verifier resolves them by method_id.
from dmaic_bench.truth.omics import OMICS_IMPLS as _OMICS_IMPLS  # noqa: E402

REFERENCE_IMPLS.update(_OMICS_IMPLS)
