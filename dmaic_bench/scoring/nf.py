"""NF — Numeric Fidelity.

Did the numbers the system computed match the frozen truths? This layer only judges what WAS
computed: a truth whose method never succeeded is "not_computed" and stays out of the NF
denominator — the omission is Method-Selection's (ms.py) job to punish, so a system is never
double-charged for the same miss.

Matching is the suffix rule ported from the originating evaluation harness's `check_values`
(a separate, unpublished codebase): systems flatten their outputs with arbitrary
nesting/prefixes, so a truth field ``pValue`` accepts any flattened key equal to it or
ending in ``.pValue``. Any one within-tol match passes — different key paths carrying the
same quantity must not fail each other.
"""
from __future__ import annotations


def flatten(obj, prefix: str = "") -> dict:
    """Flatten nested dict/list into {"a.b.0.c": scalar}; keeps numeric leaves only."""
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            out.update(flatten(v, f"{prefix}.{i}" if prefix else str(i)))
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        out[prefix] = float(obj)
    return out


def merged_outputs(trace, method_id: str):
    """All success-step outputs for this method, flattened and merged in step order (last wins).

    Returns None when the method has no successful step — callers must treat that as
    "not computed", never as "empty outputs".

    NOTE the last-wins merge, and see :func:`step_outputs` for why it is not enough on its own.
    """
    merged, seen = {}, False
    for step in trace.steps:
        if step.method_id == method_id and step.status == "success":
            seen = True
            merged.update(flatten(step.outputs))
    return merged if seen else None


def step_outputs(trace, method_id: str):
    """One flattened dict per successful step of this method, in execution order.

    A case may legitimately run the same method on several stages — two regressions on different
    responses, a capability study in Measure and again in Control to confirm the improvement.
    Merging those with last-wins DISCARDS every earlier result, so when two truths exist for one
    method at different stages, at most one can ever be scored correctly no matter how good the
    contestant is. Measured live: `adb_c19` holds `regression.ols.rSquaredAdjPct` at 93.84 for
    the frame regression and 98.21 for the light-angle regression, and only whichever the agent
    reported last was visible.

    That mattered little while the corpus was Measure/Analyze-heavy. It becomes structural the
    moment Control confirms capability against a target set in Define, which is the whole point
    of a cross-phase dependency — so the fix belongs here rather than in an authoring rule
    forbidding method reuse.
    """
    return [flatten(step.outputs) for step in trace.steps
            if step.method_id == method_id and step.status == "success"]


def _norm(name: str) -> str:
    """Conservative field-name normalization: case/underscore/hyphen-insensitive.

    Contestants legitimately write pythonic snake_case (p_value) where the canonical name is
    camelCase (pValue); requiring exact spelling would score naming, not statistics. The match
    stays segment-level (last dotted segment), so group1_p never matches pValue and
    U_statistic never matches statistic.
    """
    return "".join(c for c in name.lower() if c.isalnum())


# Conservative canonical-field synonym table (normalized forms). Only unambiguous statistical
# synonyms belong here — a wrong-scale twin (rSquaredPct vs r_squared fraction) must NOT match,
# because a name hit with an out-of-tol value turns "absent" into "failed".
FIELD_SYNONYMS = {
    "pValue": {"pval", "p", "sig", "twosidedp"},
    "factorPValue": {"pvalue", "pval", "p"},
    "modelPValue": {"pvalue", "pval", "p", "modelp"},
    "correlationCoefficient": {"pearsonr", "r", "corr", "correlation"},
    "fStatistic": {"f", "fvalue", "fstat"},
    "tStatistic": {"t", "tvalue", "tstat"},
    "zStatistic": {"z", "zvalue", "zstat"},
    "chiSquare": {"chi2", "chisq", "chisquared", "statistic"},
    "dpu": {"defectsperunit"},
    "kappaMin": {"kappa", "minkappa", "fleisskappa"},
    "processZ": {"zbench", "processsigma"},
    "centerLine": {"cl", "center"},
    "stdDev": {"std", "sd", "sigma", "stddeviation"},
    # NOT topcumulativepct: the vital-few cumulative share is a different quantity — a name hit
    # with wrong semantics must fail, that's the point of the rename.
    "topCategoryPct": {"top1pct", "topsharepct", "topcategoryshare"},
}


def _field_matches(key: str, field: str) -> bool:
    """Does a trace output key name this canonical field?

    A dot in a reported key is ambiguous and both readings are legitimate:

      * a NAMESPACE separator, from `flatten` walking a nested result object --
        ``getCapability.processZ`` means the field ``processZ``; and
      * a WORD separator, which is base R's own convention -- ``t.test()`` returns
        ``$p.value``, and ``jsonlite::toJSON`` writes that key verbatim.

    Reading only the last segment (the original behaviour) silently rejects the second:
    ``p.value`` normalised to ``value`` matched nothing, so an agent that computed correctly
    in R was scored ``failed`` -- not ``not_computed`` -- on 27 of the corpus's 55 hard truths.
    That made the benchmark score toolchain choice rather than statistics, which is exactly
    what `_norm`'s docstring says it must not do.

    So every dotted SUFFIX of the key is tried, longest match wins nothing special -- any hit
    is a hit. ``test.p.value`` yields ``value``, ``p.value``, ``test.p.value``, of which the
    second normalises onto ``pValue``.

    The documented negatives still hold, because they contain no dot and so still normalise
    whole: ``group1_p`` -> ``group1p`` never reaches ``pValue``, and ``U_statistic`` ->
    ``ustatistic`` never reaches ``statistic``. A synonym is only ever consulted for the last
    segment, keeping the loose one-letter aliases (``p``, ``t``, ``z``) from being reachable
    through a longer path.
    """
    if key == field or key.endswith("." + field):
        return True
    target = _norm(field)
    parts = key.split(".")
    for i in range(len(parts)):
        if _norm("".join(parts[i:])) == target:
            return True
    return _norm(parts[-1]) in FIELD_SYNONYMS.get(field, ())


def _count_by_method(truths) -> dict:
    counts: dict = {}
    for t in truths:
        counts[t.method_id] = counts.get(t.method_id, 0) + 1
    return counts


def _claim_step(trace, truth, claimed: dict):
    """Pick the step that satisfies this truth, without letting two truths reuse one step.

    Prefers an unclaimed step whose value is within tolerance; falls back to the merged view so
    a genuine miss still reports "out of tol" against something the contestant actually wrote,
    rather than degrading to "not computed" and hiding the error.
    """
    steps = step_outputs(trace, truth.method_id)
    if not steps:
        return None
    # Claim per (method, FIELD). One step legitimately satisfies several truths of the same
    # method for DIFFERENT fields -- a capability study reports avgP and processZ together --
    # so a method-wide claim set lets the first field's truths consume every step and starves
    # the second field. Measured: adb_c24 runs capability.binomial in Define and again in
    # Control, and its two avgP truths claimed both steps before processZ was reached.
    used = claimed.setdefault((truth.method_id, _norm(truth.field)), set())
    for i, flat in enumerate(steps):
        if i in used:
            continue
        if any(_field_matches(k, truth.field) and abs(v - truth.expected) <= truth.tol
               for k, v in flat.items()):
            used.add(i)
            return flat
    for i, flat in enumerate(steps):
        if i not in used and any(_field_matches(k, truth.field) for k in flat):
            used.add(i)
            return flat
    return merged_outputs(trace, truth.method_id)


def check_values(task, trace) -> list:
    """One verdict dict per TruthEntry of the task.

    status: not_computed | passed | failed | soft_warn
    (soft entries can never be "failed" — convention-variant quantities warn only)
    """
    details = []
    # When one method carries SEVERAL truths in a case -- two regressions, a capability study
    # repeated to confirm an improvement -- the merged view shows only the last run, so every
    # earlier truth is unscoreable however well the contestant did. Where that happens, each
    # truth is matched against an individual step and a step is CLAIMED once, so two truths
    # cannot both be satisfied by the same reported number. Single-truth methods keep the
    # merged view unchanged: it tolerates a contestant splitting one analysis across steps.
    _per_method = _count_by_method(task.truths)
    _claimed: dict = {}

    for t in task.truths:
        d = dict(method_id=t.method_id, field=t.field, expected=t.expected, tol=t.tol, soft=t.soft)
        if _per_method.get(t.method_id, 0) > 1:
            flat = _claim_step(trace, t, _claimed)
        else:
            flat = merged_outputs(trace, t.method_id)
        if flat is None:
            d["status"] = "not_computed"
        else:
            numeric = {k: v for k, v in flat.items() if _field_matches(k, t.field)}
            hits = {k: v for k, v in numeric.items() if abs(v - t.expected) <= t.tol}
            # An alternative CONVENTION is correct statistics computed a different defensible
            # way -- R's prop.test applies Yates by default where statsmodels does not. Admitting
            # it at its own precision keeps the primary tolerance tight; widening the primary
            # instead would admit nearly anything (see TruthEntry.accepts). The convention that
            # was used is recorded, so "which default did this model take" is measurable rather
            # than a silent penalty.
            variant = None
            if not hits:
                for name, exp_alt, tol_alt in (getattr(t, "accepts", ()) or ()):
                    alt = {k: v for k, v in numeric.items() if abs(v - exp_alt) <= tol_alt}
                    if alt:
                        hits, variant = alt, name
                        break
            if hits:
                d["status"] = "passed"
                d["matched"] = hits
                if variant:
                    d["convention"] = variant
            elif numeric:
                d["status"] = "soft_warn" if t.soft else "failed"
                d["reason"] = f"out of tol: {numeric}"
            else:
                d["status"] = "soft_warn" if t.soft else "failed"
                d["reason"] = "no suffix-matching numeric key in " + str(sorted(flat.keys())[:20])
        details.append(d)
    return details


def summarize(details: list) -> dict:
    counts = {s: sum(1 for d in details if d["status"] == s)
              for s in ("passed", "failed", "soft_warn", "not_computed")}
    denom = counts["passed"] + counts["failed"]
    return {
        "checked": len(details),
        **counts,
        "ratio": counts["passed"] / denom if denom else 1.0,
    }
