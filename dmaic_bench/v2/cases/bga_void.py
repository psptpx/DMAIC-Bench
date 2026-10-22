"""bga_void — solder void area under BGA joints on an SMT line. CTQ = void area fraction (%),
upper limit 25.0 with no lower limit of interest.

Onboarded from a black-belt electronics project whose measurement study read the same twelve
joints three times over with three operators on an automated X-ray inspector. The scenario, the
instrument and the failure modes come from that work; the data is generated and the case names
nobody.

Void fraction is bounded below by zero and has a long right tail, so the distribution check is
load-bearing here in a way it is not on a centred dimensional characteristic: the capability
route itself depends on reading the shape correctly. Three of its five seeds end at the X-ray
inspector, two of them on the criterion a percentage screen alone will miss --

  3, 4  gauge PASSES the headline screen and is still unusable.

AIAG MSA-4 asks two questions of a measurement system and %StudyVariation is only the first.
The number of distinct categories must also reach 5, because a gauge that cannot resolve five
groups across the part spread cannot be used to control the process however small its
percentage reads. The two criteria separate in a narrow band: ndc is 1.41 * PV/GRR, so around
%SV = 0.28 it lands on 4 while the 30% screen still says "acceptable". A system that checks the
percentage and stops checking proceeds to a capability index it has no right to compute. The
process record underneath those seeds is deliberately unremarkable, so a contestant cannot stop
in the right place for the wrong reason.
"""
from __future__ import annotations

import math
import random

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import verifiers
from dmaic_bench.v2.cases import _fixtures
from dmaic_bench.v2.cases import _fixtures as _f
from dmaic_bench.v2.models import V2Case

_LSL, _USL = 0.0, 25.0

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define", label="Scope: BGA void fraction and its acceptance limit"),
        GraphNode("M_msa", "measure", methods=("msa.gage_rr_crossed",),
                  produces=("msa.pctSV", "msa.ndc"),
                  label="X-ray inspector study (crossed Gage R&R)"),
        GraphNode("M_msa_fix", "measure",
                  label="Correct the X-ray inspector and re-run the study "
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
        GraphNode("I_improve", "improve", label="Improve (reflow profile and paste volume)"),
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
     "rule": "the X-ray inspector must be acceptable on BOTH AIAG criteria first"},
    {"stage": "M_msa_fix", "requires": "M_msa",
     "unlock_when": "msa.pctSV > 0.30 or msa.ndc < 5",
     "rule": "remediation only once the inspector has been judged unusable"},
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

SHAPES = {0: "skewed(void-tail)", 1: "unstable(reflow-drift)", 2: "gauge-unacceptable",
          3: "gauge-unacceptable(resolution)", 4: "gauge-unacceptable(resolution)"}


def _percentile_ppk(data):
    """Ppk from the 0.135/99.865 percentiles -- the admissible index for a skewed characteristic."""
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
    rng = random.Random(seed * 7_919 + 20260907)
    common = dict(parts=12, operators=3, replicates=3, center=11.0, tolerance=_USL - _LSL,
                  part_sd=3.20, operator_sd=0.42)
    if shape == 2:            # outright failure under both conventions
        return _fixtures.gage_rr_study(rng, repeat_sd=2.55, **common,
                                       window=_fixtures.GRR_FAIL_WINDOW, min_ndc=0,
                                       pooled_window=_fixtures.GRR_FAIL_POOLED_WINDOW)
    if shape in (3, 4):       # passes the 30% screen, ndc = 4
        return _fixtures.gage_rr_study(rng, repeat_sd=0.92, **common,
                                       window=_fixtures.GRR_NDC_TRAP_WINDOW, min_ndc=0,
                                       max_ndc=_fixtures.GRR_NDC_TRAP_MAX,
                                       pooled_window=_fixtures.GRR_NDC_TRAP_POOLED_WINDOW)
    return _fixtures.gage_rr_study(rng, repeat_sd=0.58, **common)


def generate(seed: int):
    shape = seed if seed in SHAPES else seed % 3
    rng = random.Random(seed * 1_000_003 + 20260907)
    n = 50
    msa_block, msa_stats = _msa_for(shape, seed)
    gauge_ok = msa_stats["pctSV"] <= 0.30 and msa_stats["ndc"] >= 5
    for _ in range(400):
        if shape == 1:                                    # reflow profile drifts -> step up
            data = [9.0 + 1.5 * max(-2.2, min(2.2, rng.gauss(0, 1))) for _ in range(n)]
            for i in range(n // 2, n):
                data[i] += 5.4
        elif shape == 0:                                  # voiding has a long right tail
            data = [2.0 + 5.5 * math.exp(0.45 * rng.gauss(0, 1)) for _ in range(n)]
            data = [min(x, 24.4) for x in data]
        else:                                             # ordinary record; the gauge is the fault
            data = [10.0 + 2.4 * max(-2.4, min(2.4, rng.gauss(0, 1))) for _ in range(n)]
        # Round first, then derive, so every routing value is one a contestant can reproduce
        # from the batch it was handed.
        data = [round(x, 2) for x in data]
        pval = verifiers.normality({"data": data})["pValue"]
        ooc = _imr_ooc(data)
        if shape == 0:                                    # must READ as non-normal
            ok = ooc == 0 and pval < 0.05
        elif shape == 1:
            ok = ooc > 0
        else:                                             # gauge is the only thing wrong
            ok = ooc == 0 and pval >= 0.05
        if not ok:
            continue
        # No capability index is published on the skewed seed. The admissible index there is a
        # percentile Ppk, and the taxonomy's non-normal capability entry does not pin which
        # percentile convention it reports, so the truth could not be matched under a single
        # named convention -- the oracle computed the route correctly and still missed the
        # field. The seed exists to test the DISTRIBUTION ROUTE, and that is scored by pq
        # without it, so the unverifiable number is dropped rather than given a soft tolerance
        # wide enough to hide a real error.
        ppk = None
        blocks = {"define": {"goal": "void fraction under the acceptance limit and holding steady",
                             "lsl": _LSL, "usl": _USL, "unit": "percent void area"},
                  "msa": dict(msa_block),
                  "process_run": {"data": list(data), "lsl": _LSL, "usl": _USL}}
        res = {"imr": {"outOfControl": ooc}, "normality": {"pValue": round(pval, 4)},
               "msa": dict(msa_stats), "_shape": SHAPES[shape]}
        if ppk is not None:
            res["cap"] = {"ppk": ppk}
        return blocks, res
    raise RuntimeError(f"bga_void: could not realise shape {shape} for seed {seed}")


CASE = V2Case(
    case_id="adb_c31", title="Solder void fraction under BGA joints",
    industry="electronics", y_type="continuous",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    seeds=(0, 1, 2, 3, 4),
    shapes=dict(SHAPES), node_data=NODE_DATA,
    fault_targets=(("M_msa", "msa.gage_rr_crossed",
                    "the repeat X-ray study for this batch was not archived"),),
    budget={"max_turns": 22},
    context=(
        "We are the process team on a surface-mount line that reflows BGA packages. Field "
        "returns have been traced to solder voids under the BGA joints, and the acceptance "
        "limit is 25 percent void area per joint, the lower the better. The line records a "
        "void-area reading for every joint in the order it is inspected, and the archive holds "
        "the study in which the same joints were measured several times over by several "
        "operators on the automated X-ray inspector."),
    goal=(
        "Work through the batches the data steward will release and report where this project "
        "stands: whether the recorded readings can carry a conclusion at all, how the line has "
        "behaved across the run, where voiding sits against its acceptance limit today, and "
        "what should change next. Every number in your report must come from a computation you "
        "ran on this task; where something could not be computed, say so rather than "
        "inventing it."),
    blocks_meta={
        "define": {"label": "Project charter and voiding limit", "phase": "define",
                   "topics": ("charter", "voiding limit", "improvement target")},
        "msa": {"label": "Repeat X-ray readings of the same joints", "phase": "measure",
                "topics": ("repeat readings", "operator study")},
        "process_run": {"label": "Per-joint void fraction in build order",
                        "phase": "measure", "topics": ("void fraction", "build order")},
    },
    field_map={
        "msa.pctSV": _f.SRC_GRR_PCT, "msa.ndc": _f.SRC_GRR_NDC,
        "imr.outOfControl": _f.SRC_IMR_OOC, "normality.pValue": _f.SRC_NORMALITY,
        "cap.ppk": ({"method_id": "capability.nonnormal", "output": "ppk", "scale": 1.0},
                    {"method_id": "capability.normal", "output": "ppk", "scale": 1.0}),
    },
    truth_fields=(
        _f.TRUTH_GRR_PCT,
        _f.TRUTH_GRR_NDC,
        {"field": "imr.outOfControl", "method_id": "control_chart.imr",
         "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "normality.pValue", "method_id": "basic.normality",
         "output": "pValue", "scale": 1.0, "tol": 0.01},
        {"field": "cap.ppk", "method_id": "capability.nonnormal",
         "output": "ppk", "scale": 1.0, "tol": 0.02},
    ),
)

if __name__ == "__main__":
    for s in CASE.seeds:
        _, r = generate(s)
        print(f"seed {s} [{r['_shape']:32s}] pctSV={r['msa']['pctSV']:.4f} ndc={r['msa']['ndc']} "
              f"ooc={r['imr']['outOfControl']} p={r['normality']['pValue']:.3f} "
              f"route={' -> '.join(walk(GRAPH, r))}")
