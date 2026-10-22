"""dual_characteristic — one part, two characteristics, and only one of them is the answer.

Onboarded from a black-belt project on a precision-turned part where two dimensions were
followed through the whole project. The scenario and the two-characteristic structure are drawn
from that work; the data is generated from the seed and the case names nobody. The source
project's two capability studies are the shape this case reproduces: one characteristic at
Cpk 0.71, the other at Cpk 1.63, on the same parts, from the same run.

**A project is not finished because a characteristic passed.** Both were charted, both were
assessed, and what the project does next is decided by the WORSE of the two -- which cannot be
known without computing both. This corpus had no task where a contestant could be right about
everything it looked at and still be wrong, because it had stopped looking one characteristic
early. Here that is the whole point: the brief names both dimensions, the steward will release
both records, and on half the seeds the one that fails is not the one named first.

The two capability studies also share a method, and so do the two control charts. Their
``field_map`` sources are pinned to an INVOCATION for the reason set out in
``placement_agreement``: under the default last-wins merge the second characteristic's numbers
answer for the first, and a contestant that assessed both correctly is re-walked as though it
had assessed one twice.

Which root cause the project goes on to is decided by which characteristic binds, so the two
branches out of the capability reading do genuinely different work: the diameter is followed
back to the fixtures it was turned on, the wall thickness to a continuously varying setting.
"""
from __future__ import annotations

import random

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import verifiers
from dmaic_bench.v2.cases import _fixtures
from dmaic_bench.v2.cases import _fixtures as _f
from dmaic_bench.v2.models import V2Case

_D_LSL, _D_USL, _D_TGT = 24.80, 25.20, 25.00      # outer diameter, mm
_W_LSL, _W_USL, _W_TGT = 1.20, 1.60, 1.40         # wall thickness, mm
_SUBGROUP, _SUBGROUPS = 5, 25
_FIXTURES = ("fixture 1", "fixture 2", "fixture 3", "fixture 4")

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define",
                  label="Scope: the two characteristics and the ranges they are accepted in"),
        GraphNode("M_msa", "measure", methods=("msa.gage_rr_crossed",),
                  produces=("msa.pctSV", "msa.ndc"),
                  label="Study of the instrument both characteristics are recorded on"),
        GraphNode("M_msa_fix", "measure",
                  label="Correct the instrument and re-run the study (readings cannot support "
                        "any downstream conclusion)"),
        GraphNode("M_chart_1", "measure", methods=("control_chart.xbar_s",),
                  produces=("chart1.outOfControl", "chart1.sOutOfControl"),
                  label="Run stability, first characteristic"),
        GraphNode("A_special_1", "analyze",
                  methods=("control_chart.xbar_s", "nonparametric.runs_test"),
                  produces=("runs1.pValue",),
                  label="Special-cause investigation on the first characteristic"),
        GraphNode("M_chart_2", "measure", methods=("control_chart.xbar_s",),
                  produces=("chart2.outOfControl", "chart2.sOutOfControl"),
                  label="Run stability, second characteristic"),
        # The two special-cause investigations do different work on purpose. The first
        # characteristic's record is all there is to go on, so it is tested for a non-random
        # pattern in place; the second has a continuously varying setting logged beside it over
        # the same window, so the question there is whether the excursion tracks that setting.
        # It is also what makes the two branches out of the first chart distinguishable: with
        # both investigations running the same pair of methods, a seed whose only downstream
        # work is a runs test is indistinguishable from one that stopped at the first chart.
        GraphNode("A_special_2", "analyze", methods=("basic.correlation",),
                  produces=("special2.correlationCoefficient",),
                  label="Special-cause investigation on the second characteristic "
                        "(against the setting logged beside it)"),
        GraphNode("A_cap_1", "analyze", methods=("capability.normal",),
                  produces=("cap1.cpk",),
                  label="Capability of the first characteristic"),
        GraphNode("A_cap_2", "analyze", methods=("capability.normal",),
                  produces=("cap2.cpk",),
                  label="Capability of the second characteristic"),
        GraphNode("A_rc_first", "analyze",
                  methods=("anova.equal_variances", "anova.oneway"),
                  produces=("fixtures.factorPValue",),
                  label="Root cause of the first characteristic (turned on which fixture?)"),
        GraphNode("A_rc_second", "analyze", methods=("basic.correlation",),
                  produces=("setting.correlationCoefficient",),
                  label="Root cause of the second characteristic (against a varying setting)"),
        GraphNode("I_improve", "improve",
                  label="Improve (act on the source the binding characteristic pointed at)"),
        GraphNode("C_control", "control",
                  label="Control plan (both characteristics monitored)"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_msa"),
        GuardedEdge("M_msa", "M_chart_1", "msa.pctSV <= 0.30 and msa.ndc >= 5",
                    guard_fields=("msa.pctSV", "msa.ndc")),
        GuardedEdge("M_msa", "M_msa_fix", is_default=True),
        GuardedEdge("M_chart_1", "M_chart_2",
                    "chart1.outOfControl == 0 and chart1.sOutOfControl == 0",
                    guard_fields=("chart1.outOfControl", "chart1.sOutOfControl")),
        GuardedEdge("M_chart_1", "A_special_1", is_default=True),
        GuardedEdge("M_chart_2", "A_cap_1",
                    "chart2.outOfControl == 0 and chart2.sOutOfControl == 0",
                    guard_fields=("chart2.outOfControl", "chart2.sOutOfControl")),
        GuardedEdge("M_chart_2", "A_special_2", is_default=True),
        # Unconditional: the second characteristic is assessed whatever the first one said.
        GuardedEdge("A_cap_1", "A_cap_2"),
        # THE PAIR DECIDES. Both acceptable finishes the project; otherwise the project goes
        # after the characteristic that is further from acceptable, whichever one that is.
        GuardedEdge("A_cap_2", "C_control", "cap1.cpk >= 1.33 and cap2.cpk >= 1.33",
                    guard_fields=("cap1.cpk", "cap2.cpk")),
        GuardedEdge("A_cap_2", "A_rc_first", "cap1.cpk < cap2.cpk",
                    guard_fields=("cap1.cpk", "cap2.cpk")),
        GuardedEdge("A_cap_2", "A_rc_second", is_default=True),
        GuardedEdge("A_rc_first", "I_improve"),
        GuardedEdge("A_rc_second", "I_improve"),
        GuardedEdge("I_improve", "C_control"),
        GuardedEdge("A_special_1", "C_control"),
        GuardedEdge("A_special_2", "C_control"),
    ),
)

GATE_POLICY = (
    {"stage": "M_chart_1", "requires": "M_msa",
     "unlock_when": "msa.pctSV <= 0.30 and msa.ndc >= 5",
     "rule": "the instrument must be acceptable on BOTH AIAG criteria before either record "
             "is released"},
    {"stage": "M_msa_fix", "requires": "M_msa", "unlock_when": "msa.pctSV > 0.30 or msa.ndc < 5",
     "rule": "remediation only once the instrument has been judged unusable"},
    {"stage": "A_cap_1", "requires": "M_chart_1",
     "unlock_when": "chart1.outOfControl == 0 and chart1.sOutOfControl == 0",
     "rule": "no capability study on a run that is not in control"},
    {"stage": "A_cap_2", "requires": "M_chart_2",
     "unlock_when": "chart2.outOfControl == 0 and chart2.sOutOfControl == 0",
     "rule": "no capability study on a run that is not in control"},
    {"stage": "A_special_1", "requires": "M_chart_1",
     "unlock_when": "chart1.outOfControl > 0 or chart1.sOutOfControl > 0",
     "rule": "special-cause work only once that run is shown to be unstable"},
    {"stage": "A_special_2", "requires": "M_chart_2",
     "unlock_when": "chart2.outOfControl > 0 or chart2.sOutOfControl > 0",
     "rule": "special-cause work only once that run is shown to be unstable"},
    {"stage": "A_rc_first", "requires": "A_cap_2",
     "rule": "which characteristic to chase is not known until both have been assessed"},
    {"stage": "A_rc_second", "requires": "A_cap_2",
     "rule": "which characteristic to chase is not known until both have been assessed"},
)

NODE_DATA = {"D_scope": "define", "M_msa": "msa",
             "M_chart_1": "run_diameter", "A_special_1": "run_diameter",
             "A_cap_1": "run_diameter",
             "M_chart_2": "run_thickness", "A_special_2": "setting",
             "A_cap_2": "run_thickness",
             "A_rc_first": "fixtures", "A_rc_second": "setting"}

SHAPES = {0: "both-acceptable",
          1: "first-binds",
          2: "second-binds",
          3: "both-short/first-binds",
          4: "instrument-unacceptable",
          5: "first-run-unstable",
          6: "second-run-unstable",
          7: "second-run-spread-unstable(means-in-control)"}

#: (diameter sd, thickness sd) per shape. 0.041 lands Cpk near 1.63, 0.094 near 0.71 --
#: the two the source project reported.
_SD = {0: (0.041, 0.041), 1: (0.094, 0.041), 2: (0.041, 0.094), 3: (0.100, 0.072),
       4: (0.041, 0.041), 5: (0.048, 0.041), 6: (0.041, 0.048), 7: (0.041, 0.030)}


def _run(rng, mean, sd, n, step_at=None, step=0.0, widen_from=None, widen=1.0, sub=None):
    """A run of *n* readings.

    ``step_at``/``step`` shift the LEVEL part-way through -- the X-bar chart catches that.
    ``widen_from``/``widen`` instead inflate the spread WITHIN each subgroup from that
    subgroup onward while holding its centre, which the X-bar chart does not catch: its
    limits are built out of sbar, so the wide subgroups widen the very limits that would
    have to flag them. The S chart catches it. Both are instabilities; only one of them is
    visible on the chart most projects look at first.
    """
    xs = [mean + sd * max(-2.6, min(2.6, rng.gauss(0, 1))) for _ in range(n)]
    if step_at is not None:
        for i in range(step_at, n):
            xs[i] += step
    if widen_from is not None and sub:
        for g in range(widen_from, n // sub):
            block = xs[g * sub:(g + 1) * sub]
            centre = sum(block) / len(block)
            xs[g * sub:(g + 1) * sub] = [centre + (x - centre) * widen for x in block]
    return [round(x, 4) for x in xs]


def _fixture_groups(rng, base, spread, offset):
    offs = [-offset, -0.15 * offset, 0.20 * offset, offset]
    return {name: [round(base + o + rng.gauss(0.0, spread), 4) for _ in range(15)]
            for name, o in zip(_FIXTURES, offs)}


def generate(seed: int):
    shape = seed if seed in SHAPES else seed % 4
    rng = random.Random(seed * 1_000_003 + 20260925)
    n = _SUBGROUP * _SUBGROUPS
    sd_d, sd_w = _SD[shape]

    grng = random.Random(seed * 7_919 + 20260927)
    if shape == 4:
        msa_block, msa_stats = _fixtures.gage_rr_study(
            grng, center=_D_TGT, tolerance=_D_USL - _D_LSL, part_sd=0.060,
            operator_sd=0.006, repeat_sd=0.047,
            window=_fixtures.GRR_FAIL_WINDOW, min_ndc=0,
            pooled_window=_fixtures.GRR_FAIL_POOLED_WINDOW)
    else:
        msa_block, msa_stats = _fixtures.gage_rr_study(
            grng, center=_D_TGT, tolerance=_D_USL - _D_LSL, part_sd=0.060,
            operator_sd=0.005, repeat_sd=0.008)
    gauge_ok = msa_stats["pctSV"] <= 0.30 and msa_stats["ndc"] >= 5

    for _ in range(500):
        diam = _run(rng, _D_TGT, sd_d, n,
                    step_at=(n // 2 if shape == 5 else None), step=0.13)
        thick = _run(rng, _W_TGT, sd_w, n,
                     step_at=(n // 2 if shape == 6 else None), step=0.13,
                     widen_from=(_SUBGROUPS - 7 if shape == 7 else None), widen=4.2,
                     sub=_SUBGROUP)

        c1 = verifiers.control_chart_xbar_s({"data": diam, "subgroupSize": _SUBGROUP})
        c2 = verifiers.control_chart_xbar_s({"data": thick, "subgroupSize": _SUBGROUP})
        ooc1, ooc2 = int(c1["flaggedCount"]), int(c2["flaggedCount"])
        sooc1, sooc2 = int(c1["flaggedSCount"]), int(c2["flaggedSCount"])

        if shape == 5:
            ok = ooc1 > 0
        elif shape == 6:
            ok = ooc1 == 0 and sooc1 == 0 and ooc2 > 0
        elif shape == 7:
            ok = ooc1 == 0 and sooc1 == 0 and ooc2 == 0 and sooc2 > 0
        else:
            ok = ooc1 == 0 and ooc2 == 0 and sooc1 == 0 and sooc2 == 0
        if not ok:
            continue

        res = {"msa": dict(msa_stats),
               "chart1": {"outOfControl": ooc1, "sOutOfControl": sooc1},
               "chart2": {"outOfControl": ooc2, "sOutOfControl": sooc2},
               "_shape": SHAPES[shape]}
        stable = ooc1 == 0 and ooc2 == 0 and sooc1 == 0 and sooc2 == 0

        if gauge_ok and stable:
            cap1 = verifiers.capability_normal(
                {"data": diam, "lsl": _D_LSL, "usl": _D_USL})
            cap2 = verifiers.capability_normal(
                {"data": thick, "lsl": _W_LSL, "usl": _W_USL})
            k1, k2 = round(float(cap1["cpk"]), 4), round(float(cap2["cpk"]), 4)
            want = {0: k1 >= 1.33 and k2 >= 1.33,
                    1: k1 < 1.33 <= k2 and k1 < k2,
                    2: k2 < 1.33 <= k1 and k2 < k1,
                    3: k1 < 1.33 and k2 < 1.33 and k1 < k2,
                    4: True}.get(shape, True)
            if not want:
                continue
            res["cap1"] = {"cpk": k1, "cp": round(float(cap1["cp"]), 4),
                           "ppk": round(float(cap1["ppk"]), 4)}
            res["cap2"] = {"cpk": k2, "cp": round(float(cap2["cp"]), 4),
                           "ppk": round(float(cap2["ppk"]), 4)}

        res["runs1"] = {"pValue": round(float(
            verifiers.runs_test({"data": diam})["pValue"]), 5)}

        frng = random.Random(seed * 104_729 + 20260929)
        groups = _fixture_groups(frng, _D_TGT, spread=sd_d * 0.8,
                                 offset=0.085 if shape in (1, 3) else 0.010)
        srng = random.Random(seed * 15_485_863 + 20260931)
        xs = [round(2.0 + 0.06 * i + srng.gauss(0, 0.05), 3) for i in range(60)]
        slope = 0.055 if shape in (2,) else 0.004
        ys = [round(_W_TGT + slope * (x - 3.8) + srng.gauss(0, sd_w * 0.7), 4) for x in xs]

        res["fixtures"] = {"factorPValue": round(float(
            verifiers.anova_oneway({"groups": groups})["factorPValue"]), 6)}
        r_setting = round(float(
            verifiers.correlation({"x": xs, "y": ys})["correlationCoefficient"]), 4)
        res["setting"] = {"correlationCoefficient": r_setting}
        res["special2"] = {"correlationCoefficient": r_setting}

        blocks = {
            "define": {"goal": "hold both characteristics inside the ranges they are accepted in",
                       "characteristics": {
                           "outer diameter": {"lsl": _D_LSL, "usl": _D_USL, "target": _D_TGT,
                                              "unit": "mm"},
                           "wall thickness": {"lsl": _W_LSL, "usl": _W_USL, "target": _W_TGT,
                                              "unit": "mm"}}},
            "msa": dict(msa_block),
            "run_diameter": {"data": list(diam), "subgroupSize": _SUBGROUP,
                             "lsl": _D_LSL, "usl": _D_USL, "target": _D_TGT},
            "run_thickness": {"data": list(thick), "subgroupSize": _SUBGROUP,
                              "lsl": _W_LSL, "usl": _W_USL, "target": _W_TGT},
            "fixtures": {"groups": {k: list(v) for k, v in groups.items()}},
            "setting": {"x": list(xs), "y": list(ys),
                        "columns": ["coolant delivery pressure (bar)", "wall thickness (mm)"]},
        }
        return blocks, res

    raise RuntimeError(f"dual_characteristic: could not realise shape {shape} for seed {seed}")


CASE = V2Case(
    case_id="adb_c35",
    title="Two characteristics on one part, and the worse of them decides",
    industry="discrete_manufacturing",
    y_type="continuous",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    seeds=(0, 1, 2, 3, 4, 5, 6, 7),
    shapes=dict(SHAPES), node_data=NODE_DATA,
    fault_targets=(("A_rc_second", "basic.correlation",
                    "the delivery-pressure log for this window was checked and is genuinely "
                    "not on file"),),
    budget={"max_turns": 28},
    context=(
        "We are the process team on a precision-turning cell. Two dimensions on the same part "
        "are followed: the outer diameter, accepted between 24.80 and 25.20 mm, and the wall "
        "thickness, accepted between 1.20 and 1.60 mm. Both are recorded five consecutive "
        "pieces at a time at twenty-five sampling points through one run, both on the same "
        "instrument, and the archive holds the study in which that instrument measured the "
        "same pieces several times over under several operators. Two further samples are on "
        "file: the diameter recorded separately for each of the four turning fixtures, and one "
        "window's paired record of coolant delivery pressure and wall thickness."),
    goal=(
        "Work through the batches the data steward will release and report where this project "
        "stands: whether the recorded readings can carry a conclusion, how each characteristic "
        "has behaved across the run, where each sits against the range it is accepted in, "
        "which of them decides what this project does next, and what that is. Every number in "
        "your report must come from a computation you ran on this task; where something could "
        "not be computed, say so rather than inventing it."),
    blocks_meta={
        "define": {"label": "Project charter and the two accepted ranges", "phase": "define",
                   "topics": ("charter", "accepted ranges", "both characteristics")},
        "msa": {"label": "Repeat readings of the same pieces on the instrument",
                "phase": "measure", "topics": ("repeat readings", "operator study")},
        "run_diameter": {"label": "Outer diameter in sampling order, five to a point",
                         "phase": "measure",
                         "topics": ("outer diameter", "diameter sampling order")},
        "run_thickness": {"label": "Wall thickness in sampling order, five to a point",
                          "phase": "measure",
                          "topics": ("wall thickness", "thickness sampling order")},
        "fixtures": {"label": "Diameter sampled separately for each turning fixture",
                     "phase": "analyze", "topics": ("fixture by fixture", "turning fixtures")},
        "setting": {"label": "Paired coolant delivery pressure and wall thickness",
                    "phase": "analyze", "topics": ("delivery pressure", "paired record")},
    },
    field_map={
        "msa.pctSV": _f.SRC_GRR_PCT, "msa.ndc": _f.SRC_GRR_NDC,
        # Two charts and two capability studies, one method each. Pinned to their invocation:
        # the default last-wins merge lets the second characteristic answer for the first.
        "chart1.sOutOfControl": ({"method_id": "control_chart.xbar_s",
                                  "output": "flaggedSCount", "scale": 1.0,
                                  "occurrence": 0},),
        "chart2.sOutOfControl": ({"method_id": "control_chart.xbar_s",
                                  "output": "flaggedSCount", "scale": 1.0,
                                  "occurrence": 1},),
        "chart1.outOfControl": ({"method_id": "control_chart.xbar_s", "output": "flaggedCount",
                                 "scale": 1.0, "occurrence": 0},),
        "chart2.outOfControl": ({"method_id": "control_chart.xbar_s", "output": "flaggedCount",
                                 "scale": 1.0, "occurrence": 1},),
        "cap1.cpk": ({"method_id": "capability.normal", "output": "cpk", "scale": 1.0,
                      "occurrence": 0},),
        "cap2.cpk": ({"method_id": "capability.normal", "output": "cpk", "scale": 1.0,
                      "occurrence": 1},),
        "runs1.pValue": ({"method_id": "nonparametric.runs_test", "output": "pValue",
                          "scale": 1.0},),
        "special2.correlationCoefficient": ({"method_id": "basic.correlation",
                                             "output": "correlationCoefficient",
                                             "scale": 1.0},),
        "fixtures.factorPValue": ({"method_id": "anova.oneway", "output": "factorPValue",
                                   "scale": 1.0},),
        "setting.correlationCoefficient": ({"method_id": "basic.correlation",
                                            "output": "correlationCoefficient", "scale": 1.0},),
    },
    truth_fields=(
        _f.TRUTH_GRR_PCT,
        _f.TRUTH_GRR_NDC,
        # Scoped to their node: both charts and both capability studies run the same method,
        # and a seed that stops at the first characteristic never reaches the second.
        {"field": "chart1.sOutOfControl", "method_id": "control_chart.xbar_s",
         "node": "M_chart_1", "output": "flaggedSCount", "scale": 1.0, "tol": 0.0},
        {"field": "chart2.sOutOfControl", "method_id": "control_chart.xbar_s",
         "node": "M_chart_2", "output": "flaggedSCount", "scale": 1.0, "tol": 0.0},
        {"field": "chart1.outOfControl", "method_id": "control_chart.xbar_s",
         "node": "M_chart_1", "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "chart2.outOfControl", "method_id": "control_chart.xbar_s",
         "node": "M_chart_2", "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "cap1.cpk", "method_id": "capability.normal", "node": "A_cap_1",
         "output": "cpk", "scale": 1.0, "tol": 0.02},
        {"field": "cap2.cpk", "method_id": "capability.normal", "node": "A_cap_2",
         "output": "cpk", "scale": 1.0, "tol": 0.02},
        {"field": "fixtures.factorPValue", "method_id": "anova.oneway",
         "output": "factorPValue", "scale": 1.0, "tol": 0.002},
        {"field": "setting.correlationCoefficient", "method_id": "basic.correlation",
         "output": "correlationCoefficient", "scale": 1.0, "tol": 0.01},
    ),
)

if __name__ == "__main__":
    for s in CASE.seeds:
        _, r = generate(s)
        c1, c2 = r.get("cap1", {}), r.get("cap2", {})
        print(f"seed {s} [{r['_shape']:24s}] ooc1={r['chart1']['outOfControl']} "
              f"ooc2={r['chart2']['outOfControl']} cpk1={c1.get('cpk')} cpk2={c2.get('cpk')}"
              f"\n    {' -> '.join(walk(GRAPH, r))}")
