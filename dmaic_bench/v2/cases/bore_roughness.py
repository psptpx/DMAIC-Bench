"""bore_roughness — cylinder-bore surface finish on a honing line. CTQ = roughness Ra (um),
accepted band 0.40-1.60, target 1.00.

Onboarded from a black-belt engine-machining project; the scenario, the instrument and the
failure modes are drawn from that work, the data is generated and the case names nobody.

This case exists to carry the routing decision the corpus was thinnest on: **the measurement
system is the finding**. Three of its six seeds end at the gauge, and one of those three is the
reason the case was written --

  4, 5  gauge PASSES the headline screen and is still unusable.

AIAG MSA-4 asks two questions of a measurement system and %StudyVariation is only the first.
The number of distinct categories must also reach 5, because a gauge that cannot resolve five
groups across the part spread cannot be used to control the process however small its
percentage reads. The two criteria separate in a narrow band: ndc is 1.41 * PV/GRR, so around
%SV = 0.28 it lands on 4 while the 30% screen still says "acceptable". A system that checks the
percentage and stops checking proceeds to a capability index it has no right to compute. The
process data underneath those seeds is deliberately unremarkable -- in control, normal, capable
-- so a contestant cannot stop in the right place for the wrong reason.
"""
from __future__ import annotations

import math
import random

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import verifiers
from dmaic_bench.v2.cases import _fixtures
from dmaic_bench.v2.cases import _fixtures as _f
from dmaic_bench.v2.models import V2Case

_LSL, _USL = 0.40, 1.60

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define", label="Scope: bore surface finish and its accepted band"),
        GraphNode("M_msa", "measure", methods=("msa.gage_rr_crossed",),
                  produces=("msa.pctSV", "msa.ndc"),
                  label="Roughness tester study (crossed Gage R&R)"),
        GraphNode("M_msa_fix", "measure",
                  label="Correct the roughness tester and re-run the study "
                        "(readings cannot support any downstream conclusion)"),
        GraphNode("M_stability", "measure", methods=("control_chart.imr",),
                  produces=("imr.outOfControl",), label="Run stability (individuals chart)"),
        GraphNode("A_route", "analyze", methods=("basic.normality",),
                  produces=("normality.pValue",), label="Capability route (distribution check)"),
        GraphNode("A_cap_normal", "analyze", methods=("capability.normal",),
                  produces=("cap.ppk",), label="Normal capability"),
        GraphNode("A_cap_nonnormal", "analyze", methods=("capability.nonnormal",),
                  produces=("cap.ppk",), label="Non-normal capability"),
        GraphNode("A_special_cause", "analyze", methods=("control_chart.imr",),
                  label="Special-cause investigation (capability does not apply)"),
        GraphNode("A_root_cause", "analyze", label="Root-cause analysis"),
        GraphNode("I_improve", "improve", label="Improve (stone dressing and feed)"),
        GraphNode("C_control", "control", label="Control plan"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_msa"),
        # BOTH AIAG criteria, not just the headline percentage.
        GuardedEdge("M_msa", "M_stability", "msa.pctSV <= 0.30 and msa.ndc >= 5",
                    guard_fields=("msa.pctSV", "msa.ndc")),
        GuardedEdge("M_msa", "M_msa_fix", is_default=True),
        # DELIBERATELY UNENFORCED. `v2_tasks._GUARD_TO_GATE` maps the single-criterion form of
        # this guard and not the compound one, so the steward emits no gate here and releases
        # the process run as soon as the gauge study is done -- where a sibling case with a
        # simple guard would refuse it. Closing that gap would destroy what these seeds measure:
        # a trap that asks whether a contestant stops when NOTHING stops it cannot be graded in
        # an environment that stops it. Measured under the hp01 probe (docs/archive/HINT_PROTOCOL.md):
        # handed the criterion and its threshold outright, the contestant computed ndc = 4,
        # quoted it correctly, and reported Cpk 1.94 on the gauge anyway.
        GuardedEdge("M_stability", "A_route", "imr.outOfControl == 0",
                    guard_fields=("imr.outOfControl",)),
        GuardedEdge("M_stability", "A_special_cause", is_default=True),
        GuardedEdge("A_route", "A_cap_normal", "normality.pValue >= 0.05",
                    guard_fields=("normality.pValue",)),
        GuardedEdge("A_route", "A_cap_nonnormal", is_default=True),
        GuardedEdge("A_cap_normal", "C_control", "cap.ppk >= 1.33",
                    guard_fields=("cap.ppk",)),
        GuardedEdge("A_cap_normal", "A_root_cause", is_default=True),
        GuardedEdge("A_cap_nonnormal", "A_root_cause"),
        GuardedEdge("A_special_cause", "C_control"),
        GuardedEdge("A_root_cause", "I_improve"),
        GuardedEdge("I_improve", "C_control"),
    ),
)

GATE_POLICY = (
    {"stage": "M_stability", "requires": "M_msa",
     "unlock_when": "msa.pctSV <= 0.30 and msa.ndc >= 5",
     # NOT ENFORCED BY THE ENVIRONMENT, and this is the whole design of the case. The steward
     # can derive both AIAG gates from this guard and hold the process run against them, and
     # doing so would make these seeds trivially unfailable: a contestant that declares ndc = 4
     # would simply be refused the next batch. A trap that asks whether a project STOPS when
     # nothing stops it cannot be graded in an environment that stops it. Path Quality still
     # scores the decision, so the obligation is measured; only the padlock is withheld.
     # Measured under hp01 (docs/archive/HINT_PROTOCOL.md): handed the criterion and its threshold
     # outright, the contestant computed ndc = 4, quoted it correctly, and reported Cpk 1.94.
     "enforce": False,
     "rule": "the roughness tester must be acceptable on BOTH AIAG criteria first"},
    {"stage": "M_msa_fix", "requires": "M_msa",
     "unlock_when": "msa.pctSV > 0.30 or msa.ndc < 5",
     "rule": "remediation only once the tester has been judged unusable"},
    {"stage": "A_route", "requires": "M_stability", "unlock_when": "imr.outOfControl == 0",
     "rule": "no capability study on a process that is not in control"},
    {"stage": "A_cap_normal", "requires": "M_stability", "unlock_when": "imr.outOfControl == 0",
     "rule": "no capability study on a process that is not in control"},
    {"stage": "A_cap_nonnormal", "requires": "M_stability", "unlock_when": "imr.outOfControl == 0",
     "rule": "no capability study on a process that is not in control"},
    {"stage": "A_special_cause", "requires": "M_stability", "unlock_when": "imr.outOfControl > 0",
     "rule": "special-cause work only once the run is shown to be unstable"},
)

NODE_DATA = {"D_scope": "define", "M_msa": "msa", "M_stability": "process_run",
             "A_route": "process_run", "A_cap_normal": "process_run",
             "A_cap_nonnormal": "process_run", "A_special_cause": "process_run"}

SHAPES = {0: "normal-capable", 1: "normal-incapable", 2: "unstable(stone-wear)",
          3: "gauge-unacceptable", 4: "gauge-unacceptable(resolution)",
          5: "gauge-unacceptable(resolution)", 6: "skewed(plateau-honing)"}


def _percentile_ppk(data):
    """Ppk from the 0.135/99.865 percentiles -- the admissible index on a skewed characteristic."""
    xs = sorted(data); n = len(xs)
    q = lambda p: (lambda i, lo: xs[lo] + (xs[min(lo + 1, n - 1)] - xs[lo]) * (i - lo))(
        p * (n - 1), int(p * (n - 1)))
    med = q(0.5)
    return min((_USL - med) / (q(0.99865) - med), (med - _LSL) / (med - q(0.00135)))


def _imr_ooc(data):
    n = len(data); c = sum(data) / n
    mr = sum(abs(data[i] - data[i - 1]) for i in range(1, n)) / (n - 1)
    return sum(1 for x in data if x > c + 2.66 * mr or x < c - 2.66 * mr)


def _msa_for(shape, seed):
    rng = random.Random(seed * 7_919 + 20260906)
    common = dict(center=1.00, tolerance=_USL - _LSL,
                  part_sd=0.30, operator_sd=0.040)
    if shape == 3:            # outright failure under both conventions
        return _fixtures.gage_rr_study(rng, repeat_sd=0.240, **common,
                                       window=_fixtures.GRR_FAIL_WINDOW, min_ndc=0,
                                       pooled_window=_fixtures.GRR_FAIL_POOLED_WINDOW)
    if shape in (4, 5):       # passes the 30% screen, ndc = 4
        return _fixtures.gage_rr_study(rng, repeat_sd=0.085, **common,
                                       window=_fixtures.GRR_NDC_TRAP_WINDOW, min_ndc=0,
                                       max_ndc=_fixtures.GRR_NDC_TRAP_MAX,
                                       pooled_window=_fixtures.GRR_NDC_TRAP_POOLED_WINDOW)
    return _fixtures.gage_rr_study(rng, repeat_sd=0.055, **common)


def generate(seed: int):
    shape = seed if seed in SHAPES else seed % 3
    rng = random.Random(seed * 1_000_003 + 20260906)
    n = 50
    msa_block, msa_stats = _msa_for(shape, seed)
    gauge_ok = msa_stats["pctSV"] <= 0.30 and msa_stats["ndc"] >= 5
    for _ in range(400):
        if shape == 1:                                    # centred high, spread too wide
            data = [1.16 + 0.20 * max(-2.4, min(2.4, rng.gauss(0, 1))) for _ in range(n)]
        elif shape == 2:                                  # honing stone wears -> upward step
            data = [0.95 + 0.10 * max(-2.2, min(2.2, rng.gauss(0, 1))) for _ in range(n)]
            for i in range(n // 2, n):
                data[i] += 0.34
        elif shape == 6:                                  # plateau honing -> long right tail
            data = [0.62 + 0.30 * math.exp(0.40 * rng.gauss(0, 1)) for _ in range(n)]
            data = [min(x, 1.58) for x in data]
        else:                                             # ordinary, in-control, capable run
            data = [1.00 + 0.11 * max(-2.4, min(2.4, rng.gauss(0, 1))) for _ in range(n)]
        # Round first, then derive, so every routing value is one a contestant can reproduce
        # from the batch it was handed.
        data = [round(x, 3) for x in data]
        pval = verifiers.normality({"data": data})["pValue"]
        ooc = _imr_ooc(data)
        if shape == 6:                                    # must READ as non-normal
            ok = ooc == 0 and pval < 0.05
        elif shape in (0, 1, 4, 5):
            ok = ooc == 0 and pval >= 0.05
        elif shape == 2:
            ok = ooc > 0
        else:                                             # 3: gauge is the only thing wrong
            ok = ooc == 0 and pval >= 0.05
        if not ok:
            continue
        ppk = None
        if shape in (0, 1) and gauge_ok:
            cap = verifiers.capability_normal({"data": data, "lsl": _LSL, "usl": _USL})
            ppk = round(cap["ppk"], 4)
            want = (shape == 0 and ppk >= 1.33) or (shape == 1 and ppk < 1.33)
            if not want:
                continue
        elif shape == 6 and gauge_ok:
            ppk = round(_percentile_ppk(data), 4)
        blocks = {"define": {"goal": "bore finish inside the accepted band and holding steady",
                             "lsl": _LSL, "usl": _USL, "unit": "um Ra"},
                  "msa": dict(msa_block),
                  "process_run": {"data": list(data), "lsl": _LSL, "usl": _USL}}
        res = {"imr": {"outOfControl": ooc}, "normality": {"pValue": round(pval, 4)},
               "msa": dict(msa_stats), "_shape": SHAPES[shape]}
        if ppk is not None:
            res["cap"] = {"ppk": ppk}
        return blocks, res
    raise RuntimeError(f"bore_roughness: could not realise shape {shape} for seed {seed}")


CASE = V2Case(
    case_id="adb_c30", title="Bore surface finish on a honing line",
    industry="discrete_manufacturing", y_type="continuous",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    seeds=(0, 1, 2, 3, 4, 5, 6),
    shapes=dict(SHAPES), node_data=NODE_DATA,
    fault_targets=(("M_msa", "msa.gage_rr_crossed",
                    "the repeat-reading study for this batch was not archived"),),
    budget={"max_turns": 22},
    context=(
        "We are the process team on a honing line that finishes cylinder bores. Assembly has "
        "returned units for bore finish, and the accepted band for roughness is 0.40 to 1.60 "
        "um Ra with 1.00 as the target. The line records a roughness reading for every bore in "
        "the order it is finished, and the archive holds the study in which the same bores were "
        "measured several times over by several operators on the roughness tester."),
    goal=(
        "Work through the batches the data steward will release and report where this project "
        "stands: whether the recorded readings can carry a conclusion at all, how the line has "
        "behaved across the run, where bore finish sits against its accepted band today, and "
        "what should change next. Every number in your report must come from a computation you "
        "ran on this task; where something could not be computed, say so rather than "
        "inventing it."),
    blocks_meta={
        "define": {"label": "Project charter and bore finish requirement", "phase": "define",
                   "topics": ("charter", "finish requirement", "improvement target")},
        "msa": {"label": "Repeat readings of the same bores", "phase": "measure",
                "topics": ("repeat readings", "operator study")},
        "process_run": {"label": "Per-bore roughness record in finishing order",
                        "phase": "measure", "topics": ("bore roughness", "finishing order")},
    },
    field_map={
        "msa.pctSV": _f.SRC_GRR_PCT, "msa.ndc": _f.SRC_GRR_NDC,
        "imr.outOfControl": _f.SRC_IMR_OOC, "normality.pValue": _f.SRC_NORMALITY,
        "cap.ppk": _f.SRC_PPK,
    },
    truth_fields=(
        _f.TRUTH_GRR_PCT,
        _f.TRUTH_GRR_NDC,
        {"field": "imr.outOfControl", "method_id": "control_chart.imr",
         "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "normality.pValue", "method_id": "basic.normality",
         "output": "pValue", "scale": 1.0, "tol": 0.01},
        {"field": "cap.ppk", "method_id": "capability.normal",
         "output": "ppk", "scale": 1.0, "tol": 0.01},
    ),
)

if __name__ == "__main__":
    for s in CASE.seeds:
        _, r = generate(s)
        print(f"seed {s} [{r['_shape']:30s}] pctSV={r['msa']['pctSV']:.4f} ndc={r['msa']['ndc']} "
              f"ooc={r['imr']['outOfControl']} p={r['normality']['pValue']:.3f} "
              f"route={' -> '.join(walk(GRAPH, r))}")
