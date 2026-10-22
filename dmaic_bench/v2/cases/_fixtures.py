"""Raw-data fixtures shared by the v2 project cases.

WHY THIS FILE EXISTS. Every v2 case claimed "generate-then-derive": the routing fields the
graph guards read are supposed to be COMPUTED from the data the steward hands out. Three of
the five cases broke that claim in the same place -- the measurement-system batch was a
one-line summary (``{"gageRR_pctTol": 0.15, "ndc": 6}``) and the guard value was the literal
0.15 typed beside it. Two consequences, both fatal to a Harbor build:

  * the node's declared method (``msa.gage_rr_crossed``) is not computable from that payload,
    so the reference solution cannot run the step the task requires -- the oracle ceiling
    drops below 1.000 for a reason that is a task defect, not difficulty; and
  * the agent reads the answer to the gate in the batch it is handed.

These helpers emit the RAW study data instead, and the case derives the guard value from it
with :mod:`dmaic_bench.truth.verifiers` -- the same code the corpus's numeric truths come
from. The draw is rejection-sampled onto a target window so the branch a case intends stays
the branch the data produces.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import stats

from dmaic_bench.truth import verifiers


def _pooled_stats(payload) -> tuple:
    """``(%StudyVariation, ndc)`` under the AIAG alpha-to-remove convention. Percent and count.

    Two defensible conventions exist for a crossed Gage R&R and they give different numbers:

    * ``verifiers.gage_rr_crossed`` retains the operator x part interaction unconditionally,
      which is this corpus's declared convention; and
    * AIAG MSA-4 (and the reference solution, and Minitab's default) POOLS a non-significant
      interaction into error at alpha = 0.25.

    They agree when the interaction is significant and diverge when it is not -- measured across
    every seed of the v2 corpus that ships a gauge study, by up to 1.80 percentage points (0.85
    before the gauge-rejection seeds were added, which is why ``pooled_window`` exists: at a
    rejection the divergence is largest and both conventions still have to land on the same side
    of the guard). That is far inside any threshold the guards use and far outside a
    numeric-fidelity tolerance. Publishing only one of them scores
    the convention rather than the competence, which is exactly what ``TruthEntry.accepts``
    exists to prevent (see its docstring and the Yates'-correction case that motivated it). So
    the second convention is computed here and published as an accepted window at ITS OWN
    precision, rather than by widening the primary tolerance until it admits anything.
    """
    x = np.asarray([payload["measurements"][k] for k in payload["measurements"]], dtype=float)
    o, p, r = x.shape
    grand = x.mean()
    op_means, part_means = x.mean(axis=(1, 2)), x.mean(axis=(0, 2))
    cell_means = x.mean(axis=2)
    ss_op = p * r * float(np.sum((op_means - grand) ** 2))
    ss_part = o * r * float(np.sum((part_means - grand) ** 2))
    ss_int = r * float(np.sum(
        (cell_means - op_means[:, None] - part_means[None, :] + grand) ** 2))
    ss_err = float(np.sum((x - cell_means[:, :, None]) ** 2))
    df_part, df_op = p - 1, o - 1
    df_int, df_err = df_part * df_op, o * p * (r - 1)
    ms_int = ss_int / df_int if df_int > 0 else 0.0
    ms_err = ss_err / df_err if df_err > 0 else 0.0
    p_int = float(stats.f.sf(ms_int / ms_err, df_int, df_err)) if ms_err > 0 and df_int > 0 else 1.0
    if p_int > 0.25:
        ss_err += ss_int
        df_err += df_int
        ms_err = ss_err / df_err if df_err > 0 else 0.0
        ms_int = ms_err
        df_int = 0
    ms_part = ss_part / df_part if df_part > 0 else 0.0
    ms_op = ss_op / df_op if df_op > 0 else 0.0
    v_rep = max(ms_err, 0.0)
    v_int = max((ms_int - ms_err) / r, 0.0) if df_int > 0 else 0.0
    v_op = max((ms_op - (ms_int if df_int > 0 else ms_err)) / (p * r), 0.0)
    v_part = max((ms_part - (ms_int if df_int > 0 else ms_err)) / (o * r), 0.0)
    v_grr = v_rep + v_op + v_int
    v_total = v_grr + v_part
    pct = 100.0 * math.sqrt(v_grr / v_total) if v_total > 0 else float("nan")
    ndc = math.floor(math.sqrt(2.0) * math.sqrt(v_part / v_grr)) if v_grr > 0 else 0
    return pct, int(ndc)


def _pooled_pct_sv(payload) -> float:
    """The percentage alone, kept for callers that only want it."""
    return _pooled_stats(payload)[0]


def gage_rr_study(rng, *, parts: int = 10, operators: int = 3, replicates: int = 3,
                  part_sd: float = 2.0, repeat_sd: float = 0.30, operator_sd: float = 0.15,
                  center: float = 20.0, tolerance: float = 16.0,
                  window: tuple = (0.08, 0.28), min_ndc: int = 5, tries: int = 200,
                  pooled_window: tuple = None, max_ndc: int = None):
    """A crossed Gage R&R study whose %StudyVariation lands inside *window* (as a fraction).

    Returns ``(payload, stats)`` where *payload* is the batch the steward hands out --
    ``measurements`` as the operator -> per-part replicate lists that
    :func:`verifiers.gage_rr_crossed` and the reference solution both read -- and *stats* is
    ``{"pctSV": <fraction>, "ndc": <int>}``, computed from that payload, never asserted.

    ``pooled_window`` constrains the SECOND admissible convention (:func:`_pooled_pct_sv`, the
    AIAG alpha-to-remove pooling the reference solution uses) to its own window. It exists for
    the gauge-REJECTION shapes: the acceptance windows above keep both conventions comfortably
    on the same side of the 30% guard, but a study drawn to fail has to fail under BOTH, or the
    reference solution walks a different branch from the one the truth package derives and the
    oracle ceiling drops below 1.000 for a reason that is a task defect. ``None`` (the default)
    leaves the draw exactly as it was, so every previously-realised study is unchanged.
    """
    lo, hi = window
    for _ in range(tries):
        true_part = [rng.gauss(center, part_sd) for _ in range(parts)]
        op_bias = [rng.gauss(0.0, operator_sd) for _ in range(operators)]
        meas = {}
        for o in range(operators):
            rows = []
            for p in range(parts):
                rows.append([round(true_part[p] + op_bias[o] + rng.gauss(0.0, repeat_sd), 4)
                             for _ in range(replicates)])
            meas["operator%d" % (o + 1)] = rows
        payload = {"measurements": meas, "numParts": parts, "numOperators": operators,
                   "numReplicates": replicates, "tolerance": tolerance}
        out = verifiers.gage_rr_crossed(payload)
        pct = out["percentStudyVariation"] / 100.0
        ndc = int(out["ndc"]) if out["ndc"] == out["ndc"] else 0
        if max_ndc is not None and ndc > max_ndc:
            continue
        if lo <= pct <= hi and ndc >= min_ndc:
            # the second admissible convention, as a fraction like pctSV
            pooled, pooled_ndc = _pooled_stats(payload)
            pooled = round(pooled / 100.0, 6)
            if pooled_window is not None:
                plo, phi = pooled_window
                if not (plo <= pooled <= phi):
                    continue
            return payload, {"pctSV": round(pct, 4), "ndc": ndc, "pctSVPooled": pooled,
                             "ndcPooled": pooled_ndc}
    raise RuntimeError("gage_rr_study: could not realise a study inside the target window")


#: A gauge study drawn to FAIL the 30% acceptance limit, in the units the guards use.
#: ``repeat_sd``/``operator_sd`` are set per case relative to ``part_sd``; the windows are
#: shared so every project's rejection shape means the same thing. ``min_ndc`` is 0 because a
#: gauge this coarse resolves barely one distinct category -- that IS the finding.
GRR_FAIL_WINDOW = (0.35, 0.55)
GRR_FAIL_POOLED_WINDOW = (0.34, 0.65)

#: The gauge that PASSES the headline screen and is still unusable. AIAG MSA-4 asks two
#: questions of a measurement system, and %StudyVariation is only the first: the number of
#: distinct categories must also be at least 5, because a gauge that cannot resolve five
#: groups across the part spread cannot be used to control the process however small its
#: percentage looks. The two criteria part company in a narrow band -- ndc is
#: ``1.41 * PV/GRR``, so at %SV near 0.28 it lands on 4 while the 30% screen still reads
#: "acceptable". A system that checks only the percentage proceeds and is wrong; the correct
#: route is the same terminal remediation node the outright failures take.
GRR_NDC_TRAP_WINDOW = (0.275, 0.298)
GRR_NDC_TRAP_MAX = 4
#: ...and the SECOND admissible convention has to land in the band too. The pooled estimate runs
#: a little lower than the primary one, and ndc is 1.41 * PV/GRR, so a study whose primary %SV
#: sits at 0.278 can pool to 0.268 and read ndc = 5 -- acceptable on the convention the reference
#: solution happens to use, unusable on the other. The routing decision then depends on which
#: admissible convention the contestant picked, which is a task defect and not a hard task:
#: measured on the oracle, adb_c31 seed 4 walked M_stability where the truth derived M_msa_fix
#: and the ceiling fell to 0.000. Both estimates must therefore imply ndc < 5.
GRR_NDC_TRAP_POOLED_WINDOW = (0.276, 0.298)


#: The two verdicts an appraiser records. English, because these strings travel in blocks.json
#: into the agent container and the released benchmark is English-only.
_LABELS = ("pass", "fail")


def attribute_agreement_study(rng, *, parts: int = 20, appraisers: int = 3, trials: int = 2,
                              error_rate: float = 0.05, bad_share: float = 0.35,
                              window: tuple = (0.65, 0.95), tries: int = 300):
    """An attribute agreement study (appraisers vs a known standard) inside a kappa window.

    Returns ``(payload, stats)``; *stats* is ``{"kappaMin": ..., "agreementPct": ...}`` from
    :func:`verifiers.attribute_agreement`, computed from the emitted ratings.
    """
    lo, hi = window
    for _ in range(tries):
        standard = [_LABELS[1] if rng.random() < bad_share else _LABELS[0]
                    for _ in range(parts)]
        ratings = {}
        for a in range(appraisers):
            per_trial = []
            for _t in range(trials):
                per_trial.append([
                    (_LABELS[1] if s == _LABELS[0] else _LABELS[0])
                    if rng.random() < error_rate else s
                    for s in standard])
            ratings["appraiser%d" % (a + 1)] = per_trial
        payload = {"standard": list(standard), "ratings": ratings}
        out = verifiers.attribute_agreement(payload)
        if lo <= out["kappaMin"] <= hi:
            return payload, {"kappaMin": round(float(out["kappaMin"]), 4),
                             "agreementPct": round(float(out["agreementPct"]), 4)}
    raise RuntimeError("attribute_agreement_study: could not realise a study in the window")


# --------------------------------------------------------------------------- field sources
# How a contestant's OWN trace reveals a dotted result field the graph's guards read. Consumed
# by V2Case.field_map (see its docstring) and by the verifier's Self-Consistency diagnostic.
# `scale` converts the trace output into the units the guard is written in: a Gage R&R reports
# %StudyVariation in PERCENT while the guard is a fraction, and that silent unit mismatch is
# exactly what makes an arithmetic slip look like a judgement failure.

SRC_GRR_PCT = ({"method_id": "msa.gage_rr_crossed", "output": "percentStudyVariation",
                "scale": 0.01},)
#: The numeric truth for %StudyVariation, with the AIAG pooled-interaction convention admitted
#: at its own precision. Shared by every project that hands out a gauge study.
TRUTH_GRR_PCT = {"field": "msa.pctSV", "method_id": "msa.gage_rr_crossed",
                 "output": "percentStudyVariation", "scale": 0.01, "tol": 0.05,
                 "accepts": ({"convention": "aiag_pooled_interaction",
                              "field": "msa.pctSVPooled", "scale": 0.01, "tol": 0.05},)}
SRC_GRR_NDC = ({"method_id": "msa.gage_rr_crossed", "output": "ndc", "scale": 1.0},)
#: The numeric truth for the distinct-category count, with the SAME second convention admitted
#: that :data:`TRUTH_GRR_PCT` admits. It was published at tol 0.0 against the retained-interaction
#: decomposition alone, which scores the convention rather than the competence: the two
#: decompositions differ by a fraction of a category and `floor` turns that into a whole one.
#: Measured on a live containerised run of the REFERENCE SOLUTION, which uses the pooled
#: convention: adb_c34 seed 2 reported 8 against a published 7, adb_c37 seed 2 reported 10
#: against 9. Both are correct counts; only one was admitted.
TRUTH_GRR_NDC = {"field": "msa.ndc", "method_id": "msa.gage_rr_crossed", "output": "ndc",
                 "scale": 1.0, "tol": 0.0,
                 "accepts": ({"convention": "aiag_pooled_interaction",
                              "field": "msa.ndcPooled", "scale": 1.0, "tol": 0.0},)}
SRC_IMR_OOC = ({"method_id": "control_chart.imr", "output": "flaggedCount", "scale": 1.0},)
#: normality is reported by the dedicated test and, as a by-product, by normal capability.
#: The Anderson-Darling p-value is the SAME statistic wherever it is reported from. Listing only
#: the dedicated test made a contestant that read it off a descriptive summary look as though it
#: had never computed normality -- which costs the numeric axis a value and, worse, turns every
#: number on a normality line into a FABRICATION.
SRC_NORMALITY = ({"method_id": "basic.normality", "output": "pValue", "scale": 1.0},
                 {"method_id": "capability.normal", "output": "adPValue", "scale": 1.0},
                 {"method_id": "basic.descriptive_summary", "output": "adPValue", "scale": 1.0})
#: whichever capability route the contestant actually walked supplies its own Ppk.
SRC_PPK = ({"method_id": "capability.normal", "output": "ppk", "scale": 1.0},
           {"method_id": "capability.nonnormal", "output": "ppk", "scale": 1.0})
SRC_PP = ({"method_id": "capability.normal", "output": "pp", "scale": 1.0},)
