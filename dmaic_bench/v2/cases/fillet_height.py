"""fillet_height — the improvement is allowed to fail, and the project has to say so.

Onboarded from a black-belt project on a wave-soldering line. The scenario, the screened
factors and the confirmation step are drawn from that work; the data is generated from the seed
and the case names nobody.

Every improvement in this corpus so far has worked. A project reached its improvement node and
the route ran on to the control plan, so a contestant could treat "improve" as a label to apply
rather than a claim to test. In a real project the settings the experiment recommends are run,
the result is compared with the baseline, and the comparison is allowed to come back saying
nothing happened -- and then the project is not finished, it is back at the question of which
factors matter. Seed 2 is that project: the screening model is significant, the recommended
settings are run, and the confirmation cannot distinguish the new mean from the old one.

Two other routes this case carries. Where the screening model as a whole is not significant, the
factors that were varied do not account for the response and the honest move is the same one --
back to identifying candidates, this time against the variables that were logged but never
designed into anything. And where the run is not normal, the two-sided specification still has
to be answered, which is the percentile route rather than the normal one; the index it yields is
deliberately NOT published as a numeric truth, because this corpus takes the ISO percentile
index and a competent contestant may fit a distribution instead, and the two disagree by more
than any tolerance worth setting.
"""
from __future__ import annotations

import math
import random

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import verifiers
from dmaic_bench.v2.cases import _fixtures as _f
from dmaic_bench.v2.models import V2Case

_LSL, _USL, _TARGET = 6.80, 7.50, 7.15
_N = 60

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define",
                  label="Scope: fillet height and the range it is accepted in"),
        GraphNode("M_stability", "measure", methods=("control_chart.imr",),
                  produces=("imr.outOfControl",),
                  label="Run stability across the baseline record"),
        GraphNode("A_special", "analyze", methods=("control_chart.imr",),
                  label="Special-cause investigation (no index applies to this run yet)"),
        GraphNode("A_route", "analyze", methods=("basic.normality",),
                  produces=("normality.pValue",),
                  label="Which capability route the distribution allows"),
        GraphNode("A_cap_normal", "analyze", methods=("capability.normal",),
                  produces=("cap.ppk",), label="Capability against the accepted range"),
        GraphNode("A_cap_nonnormal", "analyze", methods=("capability.nonnormal",),
                  label="Capability on a distribution that is not normal"),
        GraphNode("A_screen", "analyze", methods=("doe.factorial_analysis",),
                  produces=("screen.modelPValue",),
                  label="The designed run: do the varied settings account for the response?"),
        GraphNode("I_optimise", "improve",
                  label="Improve (run the line at the settings the experiment points to)"),
        GraphNode("I_confirm", "improve", methods=("basic.two_sample_t",),
                  produces=("confirm.pValue",),
                  label="Confirmation: the run after the change against the baseline"),
        # Two nodes, one computation. "The settings we varied explain nothing" and "the change
        # we made did nothing" are different findings that happen to send the project to the
        # same batch, and collapsing them into one node makes the earlier fork unreadable: the
        # route that goes on to a failed confirmation passes through the node anyway, so the
        # evidence for the branch NOT taken is present in the trace of the branch that was.
        GraphNode("A_more_factors", "analyze", methods=("regression.ols",),
                  produces=("covariates.modelPValue",),
                  label="The settings that were varied account for nothing: back to candidate "
                        "causes, against what was logged but never designed into anything"),
        GraphNode("A_reconsider", "analyze", methods=("regression.ols",),
                  produces=("covariates.modelPValue",),
                  label="The change cannot be shown to have done anything: back to candidate "
                        "causes, against what was logged but never designed into anything"),
        GraphNode("C_control", "control", label="Control plan"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_stability"),
        GuardedEdge("M_stability", "A_route", "imr.outOfControl == 0",
                    guard_fields=("imr.outOfControl",)),
        GuardedEdge("M_stability", "A_special", is_default=True),
        GuardedEdge("A_route", "A_cap_normal", "normality.pValue >= 0.05",
                    guard_fields=("normality.pValue",)),
        GuardedEdge("A_route", "A_cap_nonnormal", is_default=True),
        GuardedEdge("A_cap_normal", "C_control", "cap.ppk >= 1.33", guard_fields=("cap.ppk",)),
        GuardedEdge("A_cap_normal", "A_screen", is_default=True),
        GuardedEdge("A_cap_nonnormal", "A_screen"),
        GuardedEdge("A_screen", "I_optimise", "screen.modelPValue < 0.05",
                    guard_fields=("screen.modelPValue",)),
        GuardedEdge("A_screen", "A_more_factors", is_default=True),
        GuardedEdge("I_optimise", "I_confirm"),
        # THE CONFIRMATION IS ALLOWED TO FAIL, and failing sends the project backwards.
        GuardedEdge("I_confirm", "C_control", "confirm.pValue < 0.05",
                    guard_fields=("confirm.pValue",)),
        GuardedEdge("I_confirm", "A_reconsider", is_default=True),
        GuardedEdge("A_special", "C_control"),
    ),
)

GATE_POLICY = (
    {"stage": "A_route", "requires": "M_stability", "unlock_when": "imr.outOfControl == 0",
     "rule": "no capability study on a run that is not in control"},
    {"stage": "A_cap_normal", "requires": "M_stability", "unlock_when": "imr.outOfControl == 0",
     "rule": "no capability study on a run that is not in control"},
    {"stage": "A_cap_nonnormal", "requires": "M_stability",
     "unlock_when": "imr.outOfControl == 0",
     "rule": "no capability study on a run that is not in control"},
    {"stage": "A_special", "requires": "M_stability", "unlock_when": "imr.outOfControl > 0",
     "rule": "special-cause work only once the run is shown to be unstable"},
    {"stage": "A_screen", "requires": ["A_cap_normal", "A_cap_nonnormal"],
     "rule": "no experiment is designed until the baseline has been shown to fall short"},
    {"stage": "I_confirm", "requires": "A_screen", "unlock_when": "screen.modelPValue < 0.05",
     "rule": "a change is only confirmed once the experiment gave grounds for making it"},
    # NO RULE FOR A_reconsider. It reads the same batch as A_more_factors, and a lock is
    # enforced on the BATCH: gating it on the confirmation would lock that batch on every route
    # that reaches A_more_factors WITHOUT a confirmation, which is exactly what seeds 3 and 6
    # do. Measured on a live run before this was removed: the batch was never released and the
    # oracle scored 0.941 on both. The obligation is not lost -- the route already encodes it,
    # and Path Quality scores the fork that leads there.
)

NODE_DATA = {"D_scope": "define", "M_stability": "baseline", "A_special": "baseline",
             "A_route": "baseline", "A_cap_normal": "baseline", "A_cap_nonnormal": "baseline",
             "A_screen": "design", "I_confirm": "after_change",
             "A_more_factors": "logged_variables", "A_reconsider": "logged_variables"}

SHAPES = {0: "capable",
          1: "incapable/experiment-holds/change-confirmed",
          2: "incapable/experiment-holds/change-NOT-confirmed",
          3: "incapable/experiment-explains-nothing",
          4: "unstable",
          5: "skewed/experiment-holds/change-confirmed",
          6: "skewed/experiment-explains-nothing"}

_SKEWED = {5, 6}
_WEAK_DESIGN = {3, 6}
_WEAK_CONFIRM = {2}


def _baseline(rng, shape):
    if shape == 4:                                    # a step change part-way through
        xs = [7.14 + 0.070 * max(-2.4, min(2.4, rng.gauss(0, 1))) for _ in range(_N)]
        for i in range(_N // 2, _N):
            xs[i] += 0.26
    elif shape in _SKEWED:                            # a long right tail inside the range
        xs = [6.90 + 0.115 * math.exp(0.50 * rng.gauss(0, 1)) for _ in range(_N)]
        xs = [min(x, 7.48) for x in xs]
    elif shape == 0:                                  # centred and comfortably capable
        xs = [7.15 + 0.070 * max(-2.6, min(2.6, rng.gauss(0, 1))) for _ in range(_N)]
    else:                                             # centred, spread too wide
        xs = [7.15 + 0.132 * max(-2.6, min(2.6, rng.gauss(0, 1))) for _ in range(_N)]
    return [round(x, 3) for x in xs]


def _design(rng, weak):
    """A replicated 2^3 run table. *weak* varies the same settings over pure noise."""
    b = (0.006, 0.004, 0.003, 0.002) if weak else (0.115, 0.086, 0.010, 0.048)
    runs = []
    for a in (-1, 1):
        for bb in (-1, 1):
            for c in (-1, 1):
                for _ in range(2):
                    y = (7.15 + b[0] * a + b[1] * bb + b[2] * c + b[3] * a * bb
                         + rng.gauss(0, 0.055))
                    runs.append({"chain_speed": a, "rail_angle": bb, "air_pressure": c,
                                 "y": round(y, 4)})
    return runs


def _after_change(rng, weak):
    """Baseline-window and after-window samples. *weak* moves the mean by almost nothing."""
    before = [round(7.15 + 0.132 * rng.gauss(0, 1), 3) for _ in range(30)]
    shift = 0.012 if weak else 0.145
    after = [round(7.15 + shift + (0.132 if weak else 0.072) * rng.gauss(0, 1), 3)
             for _ in range(30)]
    return before, after


def _logged(rng):
    """Three variables that were logged through the run and designed into nothing."""
    v1 = [round(232.0 + rng.gauss(0, 4.0), 2) for _ in range(48)]
    v2 = [round(1.85 + rng.gauss(0, 0.12), 3) for _ in range(48)]
    v3 = [round(46.0 + rng.gauss(0, 2.5), 2) for _ in range(48)]
    y = [round(7.15 + 0.0028 * (a - 232.0) + 0.055 * (b - 1.85) + rng.gauss(0, 0.10), 4)
         for a, b in zip(v1, v2)]
    return {"v1": v1, "v2": v2, "v3": v3, "y": y}


def generate(seed: int):
    shape = seed if seed in SHAPES else seed % 4
    rng = random.Random(seed * 1_000_003 + 20260933)

    for _ in range(500):
        data = _baseline(rng, shape)
        ooc = int(verifiers.control_chart_imr({"data": data})["flaggedCount"])
        pval = float(verifiers.normality({"data": data})["pValue"])

        if shape == 4:
            ok = ooc > 0
        elif shape in _SKEWED:
            ok = ooc == 0 and pval < 0.05
        else:
            ok = ooc == 0 and pval >= 0.05
        if not ok:
            continue

        res = {"imr": {"outOfControl": ooc}, "normality": {"pValue": round(pval, 4)},
               "_shape": SHAPES[shape]}

        if ooc == 0 and pval >= 0.05:
            cap = verifiers.capability_normal({"data": data, "lsl": _LSL, "usl": _USL})
            ppk = round(float(cap["ppk"]), 4)
            want = (shape == 0 and ppk >= 1.33) or (shape not in (0, 4) and ppk < 1.33)
            if shape != 4 and not want:
                continue
            res["cap"] = {"ppk": ppk, "pp": round(float(cap["pp"]), 4)}

        drng = random.Random(seed * 7_919 + 20260935)
        runs = _design(drng, weak=shape in _WEAK_DESIGN)
        doe = verifiers.doe_factorial_analysis({"runs": runs})
        model_p = round(float(doe["modelPValue"]), 6)
        if (shape in _WEAK_DESIGN) != (model_p >= 0.05):
            continue

        crng = random.Random(seed * 104_729 + 20260937)
        before, after = _after_change(crng, weak=shape in _WEAK_CONFIRM)
        conf_p = round(float(verifiers.two_sample_t(
            {"group1": before, "group2": after})["pValue"]), 6)
        if (shape in _WEAK_CONFIRM) != (conf_p >= 0.05):
            continue

        lrng = random.Random(seed * 15_485_863 + 20260939)
        logged = _logged(lrng)
        reg = verifiers.ols({"data": logged, "responseColumn": "y",
                             "termsInModel": ["v1", "v2", "v3"]})

        res["screen"] = {"modelPValue": model_p,
                         "rSquaredPct": round(float(doe["rSquaredPct"]), 4)}
        res["confirm"] = {"pValue": conf_p}
        res["covariates"] = {"modelPValue": round(float(reg["modelPValue"]), 6),
                             "rSquaredPct": round(float(reg["rSquaredPct"]), 4)}

        blocks = {
            "define": {"goal": "hold fillet height inside the accepted range",
                       "lsl": _LSL, "usl": _USL, "target": _TARGET, "unit": "mm"},
            "baseline": {"data": list(data), "lsl": _LSL, "usl": _USL, "target": _TARGET},
            "design": {"runs": [dict(r) for r in runs],
                       "coding": "-1 / +1, low and high setting of each",
                       "columns": ["chain_speed", "rail_angle", "air_pressure", "y"]},
            "after_change": {"group1": list(before), "group2": list(after),
                             "groupLabels": ["the window before the change",
                                             "the window after it"]},
            "logged_variables": {"data": {k: list(v) for k, v in logged.items()},
                                 "responseColumn": "y",
                                 "termsInModel": ["v1", "v2", "v3"],
                                 "columnNotes": {
                                     "v1": "preheat zone temperature (C)",
                                     "v2": "conveyor width setting (index)",
                                     "v3": "solder pot dwell (s)"}},
        }
        return blocks, res

    raise RuntimeError(f"fillet_height: could not realise shape {shape} for seed {seed}")


CASE = V2Case(
    case_id="adb_c36",
    title="A change that was made, and a confirmation that would not confirm it",
    industry="electronics",
    y_type="continuous",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    seeds=(0, 1, 2, 3, 4, 5, 6),
    shapes=dict(SHAPES), node_data=NODE_DATA,
    fault_targets=(("I_confirm", "basic.two_sample_t",
                    "the after-change window for this line was checked and is genuinely not "
                    "on file"),),
    budget={"max_turns": 26},
    context=(
        "We are the process team on a wave-soldering line. Fillet height is accepted between "
        "6.80 and 7.50 mm with 7.15 mm as the target. Sixty consecutive joints have been "
        "recorded in the order they were made. The archive also holds a designed run in which "
        "three line settings were each taken to a low and a high level, twice over; two "
        "windows of fillet height, one before a change to the line and one after it; and a log "
        "of three further process variables that were recorded throughout but were not varied "
        "in any experiment."),
    goal=(
        "Work through the batches the data steward will release and report where this project "
        "stands: how the line has behaved across the baseline record, where fillet height sits "
        "against the range it is accepted in, whether the settings that were varied account "
        "for it, whether the change that was made can be shown to have done anything, and what "
        "should happen next. Every number in your report must come from a computation you ran "
        "on this task; where something could not be computed, say so rather than inventing it."),
    blocks_meta={
        "define": {"label": "Project charter and the accepted fillet-height range",
                   "phase": "define",
                   "topics": ("charter", "accepted range", "target height")},
        "baseline": {"label": "Fillet height joint by joint, in the order made",
                     "phase": "measure", "topics": ("baseline record", "joint order")},
        "design": {"label": "The designed run: three settings at a low and a high level",
                   "phase": "analyze", "topics": ("designed run", "line settings", "run table")},
        "after_change": {"label": "Fillet height in the window before the change and the "
                                  "window after it", "phase": "improve",
                         "topics": ("before and after the change", "two windows")},
        "logged_variables": {"label": "Three process variables logged through the run",
                             "phase": "analyze",
                             "topics": ("logged variables", "process log")},
    },
    field_map={
        "imr.outOfControl": _f.SRC_IMR_OOC,
        "normality.pValue": _f.SRC_NORMALITY,
        "cap.ppk": _f.SRC_PPK,
        "screen.modelPValue": ({"method_id": "doe.factorial_analysis",
                                "output": "modelPValue", "scale": 1.0},),
        "confirm.pValue": ({"method_id": "basic.two_sample_t", "output": "pValue",
                            "scale": 1.0},),
        "covariates.modelPValue": ({"method_id": "regression.ols", "output": "modelPValue",
                                    "scale": 1.0},),
    },
    truth_fields=(
        {"field": "imr.outOfControl", "method_id": "control_chart.imr",
         "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "normality.pValue", "method_id": "basic.normality", "output": "pValue",
         "scale": 1.0, "tol": 0.01},
        {"field": "cap.ppk", "method_id": "capability.normal", "output": "ppk",
         "scale": 1.0, "tol": 0.01},
        {"field": "screen.modelPValue", "method_id": "doe.factorial_analysis",
         "output": "modelPValue", "scale": 1.0, "tol": 0.002},
        {"field": "screen.rSquaredPct", "method_id": "doe.factorial_analysis",
         "output": "rSquaredPct", "scale": 1.0, "tol": 0.5},
        {"field": "confirm.pValue", "method_id": "basic.two_sample_t", "output": "pValue",
         "scale": 1.0, "tol": 0.01},
        {"field": "covariates.modelPValue", "method_id": "regression.ols",
         "output": "modelPValue", "scale": 1.0, "tol": 0.002},
        {"field": "covariates.rSquaredPct", "method_id": "regression.ols",
         "output": "rSquaredPct", "scale": 1.0, "tol": 0.5},
    ),
)

if __name__ == "__main__":
    for s in CASE.seeds:
        _, r = generate(s)
        print(f"seed {s} [{r['_shape']:48s}] ooc={r['imr']['outOfControl']} "
              f"p={r['normality']['pValue']:.3f} ppk={r.get('cap', {}).get('ppk')} "
              f"doeP={r['screen']['modelPValue']:.4f} confP={r['confirm']['pValue']:.4f}"
              f"\n    {' -> '.join(walk(GRAPH, r))}")
