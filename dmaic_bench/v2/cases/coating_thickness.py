"""coating_thickness — a stable, well-behaved process that makes nothing but scrap.

Onboarded from a black-belt project on an enamelled-component line. The scenario, the
characteristic and the failure modes are drawn from that work; the data is generated from the
seed and the case names nobody. The source project's capability sixpacks are what this case is
built around: one characteristic at Cp 1.37, another at Cpk -1.56 with 1000000 PPM.

**A negative Cpk is not a bad Cpk.** It is the arithmetic saying the process mean sits on the
wrong side of a specification limit, which means the process is not marginal, it is producing
nothing that conforms — and it can be doing that while perfectly in control, perfectly normal,
and with a spread that is better than the specification needs. Seed 6 is exactly that process.
A contestant that reads capability as a single number on a scale from bad to good will file it
next to the merely incapable seed 2 and prescribe the same thing.

What separates them is the pair, not the index: Cp asks whether the spread could fit inside the
specification and Cpk asks whether it does. Where Cp is adequate and Cpk is not, the spread is
not the problem and no amount of variation reduction will fix it; the mean has to move. Where
neither is adequate, centring alone cannot succeed. So the capability node forks three ways on
the two indices together, and the route the project takes past it is the prescription.

The gauge is checked on both AIAG criteria first, and the run is charted before either index is
computed, for the ordinary reason: an index computed on an unstable run is a number about
nothing (Montgomery ISQC 6e 8.2).
"""
from __future__ import annotations

import math
import random

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import verifiers
from dmaic_bench.v2.cases import _fixtures
from dmaic_bench.v2.cases import _fixtures as _f
from dmaic_bench.v2.models import V2Case

_LSL, _USL, _TARGET = 180.0, 260.0, 220.0
_SUBGROUP, _SUBGROUPS = 5, 25
_NOZZLES = ("nozzle A", "nozzle B", "nozzle C", "nozzle D")

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define",
                  label="Scope: coating thickness and the range it is accepted in"),
        GraphNode("M_msa", "measure", methods=("msa.gage_rr_crossed",),
                  produces=("msa.pctSV", "msa.ndc"),
                  label="Thickness gauge study (crossed, several operators over the same parts)"),
        GraphNode("M_msa_fix", "measure",
                  label="Correct the thickness gauge and re-run the study (readings cannot "
                        "support any downstream conclusion)"),
        GraphNode("M_stability", "measure", methods=("control_chart.xbar_r",),
                  produces=("xbar.outOfControl", "xbar.rangeOutOfControl"),
                  label="Run stability across the subgrouped record"),
        GraphNode("A_special_cause", "analyze", methods=("control_chart.xbar_r",),
                  label="Special-cause investigation (no index applies to this run yet)"),
        GraphNode("A_route", "analyze", methods=("basic.normality",),
                  produces=("normality.pValue",),
                  label="Which capability route the distribution allows"),
        GraphNode("A_cap_normal", "analyze", methods=("capability.normal",),
                  produces=("cap.cp", "cap.cpk"),
                  label="Capability against the accepted range"),
        GraphNode("A_cap_nonnormal", "analyze", methods=("capability.nonnormal",),
                  produces=("cap.ppk",),
                  label="Capability on a distribution that is not normal"),
        GraphNode("I_center", "improve", methods=("basic.one_sample_t",),
                  produces=("centre.pValue",),
                  label="Move the mean: the spread already fits, the level does not"),
        GraphNode("A_variation", "analyze", methods=("anova.sov",),
                  produces=("sov.betweenVariance",),
                  label="Where the spread comes from (thickness by applicator)"),
        GraphNode("I_reduce", "improve",
                  label="Improve (narrow the dominant source of spread)"),
        GraphNode("C_route", "control",
                  label="Control plan: which chart sustains the gain?"),
        GraphNode("C_control", "control", methods=("control_chart.xbar_r",),
                  produces=("sustain.outOfControl",),
                  label="Sustain on a subgrouped chart (the handover record is subgrouped)"),
        GraphNode("C_individuals", "control", methods=("control_chart.imr",),
                  produces=("sustain.outOfControl",),
                  label="Sustain on an individuals chart (the handover record is one piece "
                        "per sampling point)"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_msa"),
        GuardedEdge("M_msa", "M_stability", "msa.pctSV <= 0.30 and msa.ndc >= 5",
                    guard_fields=("msa.pctSV", "msa.ndc")),
        GuardedEdge("M_msa", "M_msa_fix", is_default=True),
        GuardedEdge("M_stability", "A_route",
                    "xbar.outOfControl == 0 and xbar.rangeOutOfControl == 0",
                    guard_fields=("xbar.outOfControl", "xbar.rangeOutOfControl")),
        GuardedEdge("M_stability", "A_special_cause", is_default=True),
        GuardedEdge("A_route", "A_cap_normal", "normality.pValue >= 0.05",
                    guard_fields=("normality.pValue",)),
        GuardedEdge("A_route", "A_cap_nonnormal", is_default=True),
        # THE THREE-WAY READING. Order matters: capable first, then the pair.
        GuardedEdge("A_cap_normal", "C_route", "cap.cpk >= 1.33",
                    guard_fields=("cap.cpk",)),
        # Cp adequate and Cpk not: the spread fits, the level is wrong. Includes the process
        # whose mean has crossed a limit entirely and whose Cpk is negative.
        GuardedEdge("A_cap_normal", "I_center", "cap.cp >= 1.33",
                    guard_fields=("cap.cp", "cap.cpk")),
        GuardedEdge("A_cap_normal", "A_variation", is_default=True),
        GuardedEdge("A_cap_nonnormal", "A_variation"),
        GuardedEdge("A_variation", "I_reduce"),
        GuardedEdge("I_reduce", "C_route"),
        GuardedEdge("I_center", "C_route"),
        GuardedEdge("A_special_cause", "C_route"),
        # The sustaining chart family is fixed by the handover record, not by preference: an
        # X-bar/R chart needs a subgroup, and a record kept one piece per sampling point does
        # not have one -- there is no within-subgroup range to estimate sigma from, so the
        # individuals/moving-range pair is the only admissible chart. A structural reading of
        # the batch, exactly as in adb_c32.
        GuardedEdge("C_route", "C_control", "sustain.pointSize >= 2",
                    guard_fields=("sustain.pointSize",)),
        GuardedEdge("C_route", "C_individuals", is_default=True),
    ),
)

GATE_POLICY = (
    {"stage": "M_stability", "requires": "M_msa",
     "unlock_when": "msa.pctSV <= 0.30 and msa.ndc >= 5",
     "rule": "the gauge must be acceptable on BOTH AIAG criteria before the run is released"},
    {"stage": "M_msa_fix", "requires": "M_msa", "unlock_when": "msa.pctSV > 0.30 or msa.ndc < 5",
     "rule": "remediation only once the gauge has been judged unusable"},
    {"stage": "A_route", "requires": "M_stability",
     "unlock_when": "xbar.outOfControl == 0 and xbar.rangeOutOfControl == 0",
     "rule": "no capability study on a run that is not in control -- on BOTH charts"},
    {"stage": "A_cap_normal", "requires": "M_stability",
     "unlock_when": "xbar.outOfControl == 0 and xbar.rangeOutOfControl == 0",
     "rule": "no capability study on a run that is not in control -- on BOTH charts"},
    {"stage": "A_cap_nonnormal", "requires": "M_stability",
     "unlock_when": "xbar.outOfControl == 0 and xbar.rangeOutOfControl == 0",
     "rule": "no capability study on a run that is not in control -- on BOTH charts"},
    {"stage": "A_special_cause", "requires": "M_stability",
     "unlock_when": "xbar.outOfControl > 0 or xbar.rangeOutOfControl > 0",
     "rule": "special-cause work once the run is shown unstable on either chart"},
    {"stage": "A_variation", "requires": ["A_cap_normal", "A_cap_nonnormal"],
     "rule": "the spread is only worth decomposing once it is known to be the binding problem"},
    {"stage": "C_route", "requires": "M_stability",
     "rule": "a sustaining chart is chosen for a process whose behaviour is already known"},
)

NODE_DATA = {"D_scope": "define", "M_msa": "msa", "M_stability": "process_run",
             "A_special_cause": "process_run", "A_route": "process_run",
             "A_cap_normal": "process_run", "A_cap_nonnormal": "process_run",
             # I_center reads the same run: "how far off the target is this mean, really?"
             "I_center": "process_run", "A_variation": "applicators",
             "C_route": "sustaining", "C_control": "sustaining",
             "C_individuals": "sustaining"}

#: Pieces per sampling point in the HANDOVER record, by shape. Not a preference: once the mean
#: has been moved the line relaxes to one piece per point, and that removes the subgroup the
#: X-bar/R pair needs. Both branches are exercised across the shipped seeds.
_SUSTAIN_SIZE = {0: 5, 1: 1, 2: 5, 3: 5, 4: 5, 5: 5, 6: 1, 7: 5}

SHAPES = {0: "capable",
          1: "off-centre(spread fits)",
          2: "spread-too-wide",
          3: "unstable",
          4: "gauge-unacceptable",
          5: "skewed",
          6: "mean-outside-the-limit(Cpk<0)",
          7: "ranges-unstable(means-in-control)"}


def _percentile_ppk(data):
    xs = sorted(data); n = len(xs)
    q = lambda p: (lambda i, lo: xs[lo] + (xs[min(lo + 1, n - 1)] - xs[lo]) * (i - lo))(
        p * (n - 1), int(p * (n - 1)))
    med = q(0.5)
    return min((_USL - med) / (q(0.99865) - med), (med - _LSL) / (med - q(0.00135)))


def _msa_for(shape, seed):
    rng = random.Random(seed * 7_919 + 20260921)
    common = dict(center=_TARGET, tolerance=_USL - _LSL, part_sd=12.0, operator_sd=1.2)
    if shape == 4:
        return _fixtures.gage_rr_study(rng, repeat_sd=9.5, **common,
                                       window=_fixtures.GRR_FAIL_WINDOW, min_ndc=0,
                                       pooled_window=_fixtures.GRR_FAIL_POOLED_WINDOW)
    return _fixtures.gage_rr_study(rng, repeat_sd=1.6, **common)


def _applicator_groups(rng, base_mean, spread, dominant):
    """Thickness by applicator. *dominant* widens one applicator's offset, which is what makes
    the decomposition worth running where the spread is the binding problem."""
    offsets = [-0.35 * dominant, 0.0, 0.20 * dominant, 0.90 * dominant]
    return {name: [round(base_mean + off + rng.gauss(0.0, spread), 2) for _ in range(15)]
            for name, off in zip(_NOZZLES, offsets)}


def generate(seed: int):
    shape = seed if seed in SHAPES else seed % 4
    rng = random.Random(seed * 1_000_003 + 20260921)
    n = _SUBGROUP * _SUBGROUPS
    msa_block, msa_stats = _msa_for(shape, seed)
    gauge_ok = msa_stats["pctSV"] <= 0.30 and msa_stats["ndc"] >= 5

    for _ in range(500):
        if shape == 1:                                    # spread fits, level is high
            data = [234.0 + 8.0 * max(-2.6, min(2.6, rng.gauss(0, 1))) for _ in range(n)]
        elif shape == 2:                                  # centred, spread too wide
            data = [220.0 + 13.5 * max(-2.6, min(2.6, rng.gauss(0, 1))) for _ in range(n)]
        elif shape == 3:                                  # a step change part-way through
            data = [219.0 + 7.0 * max(-2.4, min(2.4, rng.gauss(0, 1))) for _ in range(n)]
            for i in range(n // 2, n):
                data[i] += 26.0
        elif shape == 5:                                  # a long right tail
            data = [196.0 + 9.0 * math.exp(0.45 * rng.gauss(0, 1)) for _ in range(n)]
            data = [min(x, 258.0) for x in data]
        elif shape == 6:                                  # the mean has crossed the upper limit
            data = [292.0 + 8.0 * max(-2.6, min(2.6, rng.gauss(0, 1))) for _ in range(n)]
        elif shape == 7:
            # Subgroup by subgroup, so the two charts can be made to disagree on purpose: every
            # subgroup is centred on the same level, and the last seven are given four times the
            # within-subgroup spread. The X-bar chart does not flag -- its limits are x-bar-bar
            # +- A2*Rbar and the wide subgroups are what inflate Rbar, so the run widens its own
            # limits faster than the means wander outside them. The R chart flags them.
            data = []
            for g in range(_SUBGROUPS):
                centre = 220.0 + rng.gauss(0.0, 1.4)
                sd = 12.0 if g >= _SUBGROUPS - 7 else 3.0
                data += [centre + sd * max(-2.4, min(2.4, rng.gauss(0, 1)))
                         for _ in range(_SUBGROUP)]
        else:                                             # 0 and 4: centred and capable
            data = [220.0 + 8.0 * max(-2.6, min(2.6, rng.gauss(0, 1))) for _ in range(n)]
        # Round first, then derive, so every routing value is one a contestant can reproduce
        # from the batch it was handed.
        data = [round(x, 2) for x in data]

        chart = verifiers.control_chart_xbar_r({"data": data, "subgroupSize": _SUBGROUP})
        ooc = int(chart["flaggedCount"])
        rooc = int(chart["flaggedRangeCount"])
        pval = float(verifiers.normality({"data": data})["pValue"])

        if shape == 3:
            ok = ooc > 0
        elif shape == 5:
            ok = ooc == 0 and rooc == 0 and pval < 0.05
        elif shape == 7:
            ok = ooc == 0 and rooc > 0          # the disagreement IS the shape
        else:
            ok = ooc == 0 and rooc == 0 and pval >= 0.05
        if not ok:
            continue

        res = {"msa": dict(msa_stats),
               "xbar": {"outOfControl": ooc, "rangeOutOfControl": rooc},
               "normality": {"pValue": round(pval, 4)}, "_shape": SHAPES[shape]}
        stable = ooc == 0 and rooc == 0

        if gauge_ok and stable and pval >= 0.05:
            cap = verifiers.capability_normal({"data": data, "lsl": _LSL, "usl": _USL})
            cp, cpk = round(float(cap["cp"]), 4), round(float(cap["cpk"]), 4)
            want = {0: cpk >= 1.33,
                    1: cpk < 1.33 and cp >= 1.33 and cpk > 0,
                    2: cp < 1.33,
                    4: True,
                    6: cpk < 0 and cp >= 1.33}.get(shape, True)
            if not want:
                continue
            res["cap"] = {"cp": cp, "cpk": cpk,
                          "ppk": round(float(cap["ppk"]), 4),
                          "mean": round(float(cap["mean"]), 4)}
        elif gauge_ok and stable:
            res["cap"] = {"ppk": round(_percentile_ppk(data), 4)}

        srng = random.Random(seed * 104_729 + 20260923)
        groups = _applicator_groups(srng, base_mean=sum(data) / len(data),
                                    spread=5.0 if shape != 2 else 6.5,
                                    dominant=1.0 if shape != 2 else 4.2)
        sov = verifiers.anova_sov({"groups": groups})
        res["sov"] = {"betweenVariance": round(float(sov["betweenVariance"]), 4),
                      "totalVariance": round(float(sov["totalVariance"]), 4)}
        res["centre"] = {"pValue": round(float(verifiers.one_sample_t(
            {"data": data, "mu": _TARGET})["pValue"]), 6)}

        # The record kept since the change. Its sampling plan is what the Control fork reads.
        size = _SUSTAIN_SIZE[shape]
        crng = random.Random(seed * 15_485_863 + 20260929)
        s_points = 20
        s_data = [round(_TARGET + 6.0 * max(-2.4, min(2.4, crng.gauss(0, 1))), 2)
                  for _ in range(s_points * size)]
        if size >= 2:
            s_chart = verifiers.control_chart_xbar_r(
                {"data": s_data, "subgroupSize": size})
        else:
            s_chart = verifiers.control_chart_imr({"data": s_data})
        res["sustain"] = {"pointSize": size,
                          "outOfControl": int(s_chart["flaggedCount"])}

        blocks = {
            "define": {"goal": "hold coating thickness inside the accepted range and on target",
                       "lsl": _LSL, "usl": _USL, "target": _TARGET, "unit": "um"},
            "msa": dict(msa_block),
            "process_run": {"data": list(data), "subgroupSize": _SUBGROUP,
                            "lsl": _LSL, "usl": _USL, "target": _TARGET},
            "applicators": {"groups": {k: list(v) for k, v in groups.items()}},
            "sustaining": {"data": list(s_data), "subgroupSize": size,
                           "subgroupSizes": [size] * s_points,
                           "note": "readings kept since the change, in sampling order"},
        }
        return blocks, res

    raise RuntimeError(f"coating_thickness: could not realise shape {shape} for seed {seed}")


CASE = V2Case(
    case_id="adb_c34",
    title="Coating thickness against the range it is accepted in",
    industry="discrete_manufacturing",
    y_type="continuous",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    seeds=(0, 1, 2, 3, 4, 5, 6, 7),
    shapes=dict(SHAPES), node_data=NODE_DATA,
    fault_targets=(("M_msa", "msa.gage_rr_crossed",
                    "the repeat-reading study for this gauge was not archived"),),
    budget={"max_turns": 24},
    context=(
        "We are the process team on an enamelled-component line. Coating thickness is accepted "
        "between 180 and 260 um with 220 um as the target. The line records five consecutive "
        "pieces at each of twenty-five sampling points through the run, the archive holds the "
        "study in which the same pieces were measured several times over by several operators "
        "on the thickness gauge, and a separate sample records thickness piece by piece for "
        "each of the four applicators."),
    goal=(
        "Work through the batches the data steward will release and report where this project "
        "stands: whether the recorded readings can carry a conclusion, how the line has behaved "
        "across the run, where coating thickness sits against the range it is accepted in, and "
        "what specifically should change next. Every number in your report must come from a "
        "computation you ran on this task; where something could not be computed, say so "
        "rather than inventing it."),
    blocks_meta={
        "define": {"label": "Project charter and the accepted thickness range", "phase": "define",
                   "topics": ("charter", "accepted range", "target thickness")},
        "msa": {"label": "Repeat readings of the same pieces", "phase": "measure",
                "topics": ("repeat readings", "operator study")},
        "process_run": {"label": "Thickness readings in sampling order, five to a point",
                        "phase": "measure", "topics": ("thickness readings", "sampling order")},
        "applicators": {"label": "Thickness sampled separately for each applicator",
                        "phase": "analyze", "topics": ("applicator by applicator",
                                                       "applicator sample")},
        "sustaining": {"label": "The monitoring record kept since the change",
                       "phase": "control", "topics": ("monitoring record", "since the change",
                                                      "control plan")},
    },
    batch_facts={
        # Structural: how many pieces the handover record holds at each sampling point. No
        # method reports it; an analyst reads it off the batch, and the sustaining chart
        # family follows from it.
        "sustain.pointSize": {"node": "C_route", "key": "subgroupSizes", "kind": "min"},
    },
    field_map={
        "msa.pctSV": _f.SRC_GRR_PCT, "msa.ndc": _f.SRC_GRR_NDC,
        # Occurrence-pinned: control_chart.xbar_r runs twice now -- once on the baseline run
        # and once on the handover record -- and the default last-wins merge would let the
        # sustaining chart answer for the baseline. `sustain.outOfControl` is deliberately
        # NOT in this table for the same reason: it is a published truth, not a guard field.
        "xbar.outOfControl": ({"method_id": "control_chart.xbar_r", "output": "flaggedCount",
                               "scale": 1.0, "occurrence": 0},
                              {"method_id": "control_chart.xbar_s", "output": "flaggedCount",
                               "scale": 1.0, "occurrence": 0}),
        "xbar.rangeOutOfControl": ({"method_id": "control_chart.xbar_r",
                                    "output": "flaggedRangeCount", "scale": 1.0,
                                    "occurrence": 0},),
        "normality.pValue": _f.SRC_NORMALITY,
        "cap.cp": ({"method_id": "capability.normal", "output": "cp", "scale": 1.0},),
        "cap.cpk": ({"method_id": "capability.normal", "output": "cpk", "scale": 1.0},),
        "cap.ppk": ({"method_id": "capability.normal", "output": "ppk", "scale": 1.0},
                    {"method_id": "capability.nonnormal", "output": "ppk", "scale": 1.0}),
        "sov.betweenVariance": ({"method_id": "anova.sov", "output": "betweenVariance",
                                 "scale": 1.0},),
        "centre.pValue": ({"method_id": "basic.one_sample_t", "output": "pValue", "scale": 1.0},),
    },
    truth_fields=(
        _f.TRUTH_GRR_PCT,
        _f.TRUTH_GRR_NDC,
        {"field": "xbar.outOfControl", "method_id": "control_chart.xbar_r",
         "node": "M_stability", "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "xbar.rangeOutOfControl", "method_id": "control_chart.xbar_r",
         "node": "M_stability", "output": "flaggedRangeCount", "scale": 1.0, "tol": 0.0},
        {"field": "sustain.outOfControl", "method_id": "control_chart.xbar_r",
         "node": "C_control", "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "sustain.outOfControl", "method_id": "control_chart.imr",
         "node": "C_individuals", "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "normality.pValue", "method_id": "basic.normality", "output": "pValue",
         "scale": 1.0, "tol": 0.01},
        {"field": "cap.cp", "method_id": "capability.normal", "output": "cp",
         "scale": 1.0, "tol": 0.02},
        {"field": "cap.cpk", "method_id": "capability.normal", "output": "cpk",
         "scale": 1.0, "tol": 0.02},
        # cap.ppk is NOT published on the non-normal route: this corpus takes the ISO percentile
        # index and the reference solution fits a distribution, and the two disagree by more
        # than any tolerance. Pinning it would score the convention, not the competence.
        {"field": "sov.betweenVariance", "method_id": "anova.sov", "output": "betweenVariance",
         "scale": 1.0, "tol": 0.5},
        {"field": "centre.pValue", "method_id": "basic.one_sample_t", "output": "pValue",
         "scale": 1.0, "tol": 0.002},
    ),
)

if __name__ == "__main__":
    for s in CASE.seeds:
        _, r = generate(s)
        cap = r.get("cap", {})
        print(f"seed {s} [{r['_shape']:30s}] pctSV={r['msa']['pctSV']:.3f} ndc={r['msa']['ndc']} "
              f"ooc={r['xbar']['outOfControl']} p={r['normality']['pValue']:.3f} "
              f"cp={cap.get('cp')} cpk={cap.get('cpk')}\n    {' -> '.join(walk(GRAPH, r))}")
