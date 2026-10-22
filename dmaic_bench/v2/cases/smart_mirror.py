"""smart_mirror — a NEW-domain onboarded case: intelligent (streaming) rear-view mirror display
module. CTQ = display luminance uniformity (cd/m²), spec 350–550, target 450. Tests whether the
benchmark generalizes beyond the discrete-manufacturing cases to an optics/display project, and
whether an agent selects the right method when the data shape varies (backlight decay → right-skew).

seed % 4 drives the shape so the correct DMAIC route AND the correct capability method both depend
on the data:
  0  normal · capable      → normal capability, monitor
  1  normal · incapable    → normal capability → root-cause → improve
  2  skewed (backlight decay) → NON-normal capability route → improve   [method trap]
  3  unstable (line switch)   → special-cause investigation, NOT capability
  4  photometer unacceptable  → %GRR above the 30% acceptance limit voids every downstream
                               comparison (AIAG MSA-4 §II-B); correct the photometer and re-study
                               it. Nothing about the line may be concluded from readings this
                               coarse, so the project stops at the gauge.

Shape 4 is why ``M_msa_fix`` exists. The rejection branch used to be the self-loop
``M_msa -> M_msa``, and ``walk`` is cycle-guarded: a failing gauge terminated the walk ON the
fork, so ``branch_decisions`` never recorded the decision and ``harbor_truth.branch_evidence``
excluded it by rule. The fork could not fork whatever the data did.
"""
from __future__ import annotations

import math
import random

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import verifiers
from dmaic_bench.v2.cases import _fixtures
from dmaic_bench.v2.cases import _fixtures as _f
from dmaic_bench.v2.models import V2Case

_LSL, _USL = 350.0, 550.0

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define", label="Scope: display brightness uniformity"),
        GraphNode("M_msa", "measure", methods=("msa.gage_rr_crossed",),
                  produces=("msa.pctSV",), label="Photometer study (crossed Gage R&R)"),
        GraphNode("M_stability", "measure", methods=("control_chart.imr",),
                  produces=("imr.outOfControl",), label="Run stability (individuals chart)"),
        GraphNode("M_msa_fix", "measure",
                  label="Correct the photometer and re-run the study (readings cannot support any downstream conclusion)"),
        GraphNode("A_route", "analyze", methods=("basic.normality",),
                  produces=("normality.pValue",), label="Capability route (distribution check)"),
        GraphNode("A_cap_normal", "analyze", methods=("capability.normal",),
                  produces=("cap.ppk",), label="Normal capability"),
        GraphNode("A_cap_nonnormal", "analyze", methods=("capability.nonnormal",),
                  produces=("cap.ppk",), label="Non-normal capability"),
        GraphNode("A_special_cause", "analyze", methods=("control_chart.imr",),
                  label="Special-cause investigation (capability does not apply)"),
        GraphNode("A_root_cause", "analyze", label="Root-cause analysis"),
        GraphNode("I_improve", "improve", label="Improve (backlight and diffuser film)"),
        GraphNode("C_control", "control", label="Control plan"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_msa"),
        GuardedEdge("M_msa", "M_stability", "msa.pctSV <= 0.30",
                    guard_fields=("msa.pctSV",)),
        GuardedEdge("M_msa", "M_msa_fix", is_default=True),
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
    {"stage": "M_stability", "requires": "M_msa", "unlock_when": "msa.pctSV <= 0.30",
     "rule": "the photometer must be judged acceptable first"},
    {"stage": "M_msa_fix", "requires": "M_msa", "unlock_when": "msa.pctSV > 0.30",
     "rule": "remediation only once the photometer has been judged unusable"},
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
SHAPES = {0: "normal·capable", 1: "normal·incapable", 2: "skewed(backlight-decay)",
          3: "unstable(line-switch)", 4: "gauge-unacceptable"}

#: Seeds whose shape is NOT ``seed % 4`` -- see poc_project._EXTRA_SHAPES.
#: seed -> shape for the seeds that are not ``seed % 4``. A table rather than a wider modulus,
#: so the gauge-rejection shape can carry more than one seed without renumbering the others.
_EXTRA_SHAPES = {4: 4, 5: 4}


def _shape_for(seed: int) -> int:
    return _EXTRA_SHAPES.get(seed, seed % 4)


def _imr_ooc(data):
    n = len(data); c = sum(data) / n
    mr = sum(abs(data[i] - data[i - 1]) for i in range(1, n)) / (n - 1)
    return sum(1 for x in data if x > c + 2.66 * mr or x < c - 2.66 * mr)


def _percentile_ppk(data):
    xs = sorted(data); n = len(xs)
    q = lambda p: (lambda i, lo: xs[lo] + (xs[min(lo + 1, n - 1)] - xs[lo]) * (i - lo))(p * (n - 1), int(p * (n - 1)))
    med = q(0.5)
    return min((_USL - med) / (q(0.99865) - med), (med - _LSL) / (med - q(0.00135)))


def generate(seed: int):
    shape = _shape_for(seed)
    rng = random.Random(seed * 1_000_003 + 20260709)
    n = 50
    if shape == 4:
        # A photometer that cannot discriminate: repeatability/reproducibility swamp the
        # unit-to-unit spread, so %StudyVariation lands above 30% under BOTH admissible
        # conventions. Scaled to this case's part_sd; the verdict is computed, never asserted.
        msa_block, msa_stats = _fixtures.gage_rr_study(
            random.Random(seed * 7_919 + 20260710), center=450.0, tolerance=200.0,
            part_sd=30.0, repeat_sd=19.5, operator_sd=10.5,
            window=_fixtures.GRR_FAIL_WINDOW, min_ndc=0,
            pooled_window=_fixtures.GRR_FAIL_POOLED_WINDOW)
    else:
        msa_block, msa_stats = _fixtures.gage_rr_study(
            random.Random(seed * 7_919 + 20260710), center=450.0, tolerance=200.0,
            part_sd=30.0, repeat_sd=4.5, operator_sd=2.2)
    for _ in range(300):
        if shape == 0:
            data = [450 + 28 * max(-2.4, min(2.4, rng.gauss(0, 1))) for _ in range(n)]
        elif shape == 1:
            data = [415 + 52 * max(-2.4, min(2.4, rng.gauss(0, 1))) for _ in range(n)]
        elif shape == 2:                                  # backlight decay → right skew
            data = [360 + 60 * math.exp(0.5 * rng.gauss(0, 1)) for _ in range(n)]
            data = [min(x, 549.0) for x in data]
        elif shape == 3:                                  # line switch → step change (unstable)
            data = [450 + 22 * max(-2.2, min(2.2, rng.gauss(0, 1))) for _ in range(n)]
            for i in range(n // 2, n):
                data[i] += 70
        else:                                             # gauge unusable; the run is ordinary
            # The end-of-line record is deliberately unremarkable: the gauge is the only thing
            # wrong, so a contestant cannot stop in the right place for the wrong reason.
            data = [450 + 28 * max(-2.4, min(2.4, rng.gauss(0, 1))) for _ in range(n)]
        # ROUND FIRST, then derive. The batch handed out is rounded to 0.1 cd/m2; deriving the
        # routing value from the unrounded draw made the guard read a number no contestant --
        # not even the reference solution -- can reproduce (measured: p = 0.9197 stored against
        # 0.9180 recomputable, on data rounded after the fact).
        data = [round(x, 1) for x in data]
        pval = verifiers.normality({"data": data})["pValue"]
        ooc = _imr_ooc(data)
        ok = {0: ooc == 0 and pval >= 0.05, 1: ooc == 0 and pval >= 0.05,
              2: ooc == 0 and pval < 0.05, 3: ooc > 0,
              4: (msa_stats["pctSV"] > 0.30 and msa_stats["pctSVPooled"] > 0.30
                  and ooc == 0 and pval >= 0.05)}[shape]
        if shape in (0, 1) and ok:
            cap = verifiers.capability_normal({"data": data, "lsl": _LSL, "usl": _USL})
            ppk = round(cap["ppk"], 4)
            want = (shape == 0 and ppk >= 1.33) or (shape == 1 and ppk < 1.33)
            if not want:
                continue
        elif shape == 2 and ok:
            ppk = round(_percentile_ppk(data), 4)
        elif shape in (3, 4) and ok:
            # No capability index: on shape 3 the process is out of control, on shape 4 the
            # readings it would be computed from cannot be trusted. Either way the number would
            # be arithmetic without meaning, and the case does not publish one.
            ppk = None
        else:
            continue
        blocks = {"define": {"goal": "brightness inside the accepted range and holding steady",
                             "lsl": _LSL, "usl": _USL, "unit": "cd/m2"},
                  # NO `label` on the batch: blocks.json is read INSIDE the agent container, so
                  # a batch label is agent-visible text and this one named the analysis.
                  "msa": dict(msa_block),
                  "process_run": {"data": list(data),
                                  "lsl": _LSL, "usl": _USL}}
        res = {"imr": {"outOfControl": ooc}, "normality": {"pValue": round(pval, 4)},
               "msa": dict(msa_stats), "_shape": SHAPES[shape]}
        if ppk is not None:
            res["cap"] = {"ppk": ppk}
        return blocks, res
    raise RuntimeError(f"smart_mirror: could not realize shape {shape} for seed {seed}")


CASE = V2Case(
    # The published identity is deliberately generic. The product category this module was
    # drafted around is close enough to one of the nine held-out expert projects that a reader
    # could link them; the case content is synthetic and names nobody, but the id, the title and
    # a fine-grained industry together were the weakest link in the batch. The module keeps its
    # working name; nothing that ships carries it.
    case_id="adb_c28", title="Brightness uniformity on a display module line",
    industry="electronics", y_type="continuous",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    # Seed 4 is the gauge-REJECTION seed: it exercises the ``M_msa`` fork's other edge, which
    # no seed reached while that edge was a self-loop the walk could not record.
    seeds=(0, 1, 2, 3, 4, 5),
    shapes={s: SHAPES[_shape_for(s)] for s in (0, 1, 2, 3, 4, 5)}, node_data=NODE_DATA,
    fault_targets=(("M_msa", "msa.gage_rr_crossed", "the photometer R&R raw data for this batch was checked and is genuinely not on file"),),
    budget={"max_turns": 20},
    context=(
        "We are the line-improvement team for a display module. Set makers report that some "
        "units look dim or patchy in low light; the internally accepted range is 350 to 550 "
        "cd/m2. The line records a brightness reading for every unit in the order it comes off, "
        "and the archive holds the study in which the same units were read several times over "
        "by several operators."),
    goal=(
        "Work through the batches the data steward can release and say where this project "
        "stands: whether the recorded readings can be relied on, how the line has behaved over "
        "the run, where brightness sits against its accepted range today, and what should be "
        "changed next. Every number in your report must come from a computation you ran on "
        "this task; where something could not be computed, say so rather than inventing it."),
    blocks_meta={
        "define": {"label": "Project charter and brightness requirement", "phase": "define",
                   "topics": ("charter", "brightness requirement", "improvement target")},
        "msa": {"label": "Repeat readings of the same units", "phase": "measure",
                "topics": ("repeat readings", "operator study")},
        "process_run": {"label": "Per-unit end-of-line brightness record", "phase": "measure",
                        "topics": ("unit brightness", "end of line")},
    },
    field_map={
        "msa.pctSV": _f.SRC_GRR_PCT, "msa.ndc": _f.SRC_GRR_NDC,
        "imr.outOfControl": _f.SRC_IMR_OOC, "normality.pValue": _f.SRC_NORMALITY,
        "cap.ppk": _f.SRC_PPK,
    },
    truth_fields=(
        _f.TRUTH_GRR_PCT,
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
        cap = r.get("cap", {}).get("ppk")
        print(f"seed {s} [{r['_shape']:24s}] p={r['normality']['pValue']:.3f} ooc={r['imr']['outOfControl']} "
              f"ppk={cap} route={' → '.join(x.split('_')[0] for x in walk(GRAPH, r))}")
