"""capacitor_defect — an 82% reduction that does not meet the requirement.

Onboarded from a black-belt project on a chip-capacitor line, where two defect rates were
followed and the improvement was verified before and after: 0.59% to 0.21% on one, 0.18% to
0.03% on the other. The scenario and the verification structure are drawn from that work; the
data is generated from the seed and the case names nobody.

An improvement raises TWO questions and they are independent of each other.

  Did it do anything?      -- a comparison of the before and after windows
  Is that enough?          -- the after level against what the project committed to

A change can pass the first and fail the second, and seed 6 is the seed that matters: the
defect share falls from 1.80% to 0.32%, a reduction of 82% that no comparison could call
noise, and the requirement is 0.25%. The project has succeeded at improving and has not
finished. Conversely a change can look right in the point estimate and be indistinguishable
from noise at the trial size that was actually run, which is a different failure with a
different next step -- and the next step there is to ask what the trial could have detected,
not to re-argue the numbers.

Nothing else in this corpus separates these two questions. Where an improvement was verified at
all it was verified once, so "the change worked" and "we are done" were the same claim.
"""
from __future__ import annotations

import random

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import verifiers
from dmaic_bench.v2.models import V2Case

#: What the project committed to, as a share of units inspected.
_REQUIRED = 0.0025
_K, _N_LOT = 25, 4000            # baseline lots
_K_AFTER = 20                    # lots after the change

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define",
                  label="Scope: the defect share and the level committed to"),
        GraphNode("M_pchart", "measure", methods=("control_chart.p",),
                  produces=("pchart.outOfControl", "pchart.centerLine"),
                  label="Lot-by-lot defect share across the baseline record"),
        GraphNode("A_special", "analyze", methods=("control_chart.laney_p",),
                  produces=("laney.outOfControl",),
                  label="Special-cause investigation, and whether the record is overdispersed"),
        GraphNode("A_factors", "analyze", methods=("regression.ols",),
                  produces=("factors.modelPValue",),
                  label="Do the two settings, and their combination, account for the share?"),
        GraphNode("A_more_x", "analyze",
                  label="The settings on file do not account for the share; the project returns "
                        "to identifying candidate causes"),
        GraphNode("I_change", "improve", methods=("basic.two_proportions",),
                  produces=("effect.pValue",),
                  label="Did the change do anything? The window before against the window after"),
        GraphNode("A_change_not_shown", "analyze", methods=("power.two_proportions",),
                  produces=("power.power",),
                  label="The change cannot be shown to have done anything: what could a trial "
                        "this size have detected?"),
        GraphNode("I_level", "improve", methods=("capability.binomial",),
                  produces=("after.avgP",),
                  label="Is that enough? The level after the change against what was committed"),
        GraphNode("A_shortfall", "analyze", methods=("power.two_proportions",),
                  produces=("power.power",),
                  label="A real reduction that still misses the commitment: what the next trial "
                        "would have to detect"),
        GraphNode("C_control", "control", label="Control plan (attribute chart monitoring)"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_pchart"),
        GuardedEdge("M_pchart", "A_special", "pchart.outOfControl > 0",
                    guard_fields=("pchart.outOfControl",)),
        GuardedEdge("M_pchart", "C_control", "pchart.centerLine <= 0.0025",
                    guard_fields=("pchart.centerLine",)),
        GuardedEdge("M_pchart", "A_factors", is_default=True),
        GuardedEdge("A_factors", "I_change", "factors.modelPValue < 0.05",
                    guard_fields=("factors.modelPValue",)),
        GuardedEdge("A_factors", "A_more_x", is_default=True),
        # QUESTION ONE: did it do anything?
        GuardedEdge("I_change", "I_level", "effect.pValue < 0.05",
                    guard_fields=("effect.pValue",)),
        GuardedEdge("I_change", "A_change_not_shown", is_default=True),
        # QUESTION TWO, asked only once the first is answered yes: is that enough?
        GuardedEdge("I_level", "C_control", "after.avgP <= 0.0025",
                    guard_fields=("after.avgP",)),
        GuardedEdge("I_level", "A_shortfall", is_default=True),
        GuardedEdge("A_special", "C_control"),
    ),
)

GATE_POLICY = (
    {"stage": "A_factors", "requires": "M_pchart", "unlock_when": "pchart.outOfControl == 0",
     "rule": "a defect share is only one number once the run is stable "
             "(Montgomery ISQC 6e 7.2)"},
    {"stage": "A_special", "requires": "M_pchart", "unlock_when": "pchart.outOfControl > 0",
     "rule": "special-cause work only once the run is shown to be unstable"},
    {"stage": "I_change", "requires": "A_factors", "unlock_when": "factors.modelPValue < 0.05",
     "rule": "no change is made until something on file accounts for the share"},
    {"stage": "I_level", "requires": "I_change", "unlock_when": "effect.pValue < 0.05",
     "rule": "the level after a change is only worth reading once the change is shown to have "
             "moved it"},
    # NO RULE FOR A_shortfall, for the reason set out in fillet_height's policy: it shares its
    # batch with A_change_not_shown, which is reached on a route that never reads the new level,
    # so a lock here makes that route's batch unobtainable. Seed 3, oracle 0.923 before this was
    # removed. The route still encodes the obligation and Path Quality still scores it.
)

NODE_DATA = {"D_scope": "define", "M_pchart": "baseline", "A_special": "baseline",
             "A_factors": "settings", "I_change": "before_after", "I_level": "after_lots",
             "A_change_not_shown": "trial_size", "A_shortfall": "trial_size"}

SHAPES = {0: "already-at-the-committed-level",
          1: "reduced-and-committed-level-met",
          2: "reduced-but-short-of-the-commitment",
          3: "change-cannot-be-shown",
          4: "settings-account-for-nothing",
          5: "baseline-unstable",
          6: "82%-reduction-still-short"}

#: (baseline share, after share) per shape.
_LEVELS = {0: (0.0020, 0.0018), 1: (0.0059, 0.0021), 2: (0.0059, 0.0034),
           3: (0.0059, 0.0052), 4: (0.0059, 0.0048), 5: (0.0059, 0.0040),
           6: (0.0180, 0.0032)}
_WEAK_MODEL = {4}
_SMALL_TRIAL = {3}


def _draw(rng, p, n, k):
    return [sum(1 for _ in range(n) if rng.random() < p) for _ in range(k)]


def _settings(rng, weak):
    """Per-lot record of two line settings and the lot's defect share."""
    a = [round(1.60 + rng.gauss(0, 0.18), 3) for _ in range(40)]
    b = [round(245.0 + rng.gauss(0, 6.0), 2) for _ in range(40)]
    if weak:
        y = [round(0.0059 + rng.gauss(0, 0.0012), 6) for _ in range(40)]
    else:
        y = [round(0.0059 + 0.0021 * (ai - 1.60) + 0.000075 * (bi - 245.0)
                   + 0.00060 * (ai - 1.60) * (bi - 245.0) + rng.gauss(0, 0.00055), 6)
             for ai, bi in zip(a, b)]
    return {"paste_thickness": a, "reflow_peak": b, "lot_defect_share": y}


def generate(seed: int):
    shape = seed if seed in SHAPES else seed % 5
    rng = random.Random(seed * 1_000_003 + 20260945)
    p_before, p_after = _LEVELS[shape]

    for _ in range(600):
        sizes = [_N_LOT] * _K
        defects = _draw(rng, p_before, _N_LOT, _K)
        if shape == 5:
            defects[_K // 2] = int(_N_LOT * 0.021)

        chart = verifiers.control_chart_p(
            {"defectCounts": defects, "subgroupSizes": sizes})
        ooc = int(chart["outOfControlCount"])
        centre = round(float(chart["centerLine"]), 6)

        if shape == 5:
            ok = ooc > 0
        elif shape == 0:
            ok = ooc == 0 and centre <= _REQUIRED
        else:
            ok = ooc == 0 and centre > _REQUIRED
        if not ok:
            continue

        # The trial that was actually run. Seed 3 runs a small one on purpose: the point
        # estimate falls and the comparison cannot tell it from noise.
        n_trial = 6000 if shape in _SMALL_TRIAL else 40000
        e_before = sum(1 for _ in range(n_trial) if rng.random() < p_before)
        e_after = sum(1 for _ in range(n_trial) if rng.random() < p_after)
        effect_p = round(float(verifiers.two_proportions(
            {"events1": e_before, "trials1": n_trial,
             "events2": e_after, "trials2": n_trial})["pValue"]), 6)

        after_sizes = [_N_LOT] * _K_AFTER
        after_defects = _draw(rng, p_after, _N_LOT, _K_AFTER)
        after_binom = verifiers.capability_binomial(
            {"defectCounts": after_defects, "subgroupSizes": after_sizes})
        after_p = round(float(after_binom["avgP"]), 6)

        srng = random.Random(seed * 7_919 + 20260947)
        settings = _settings(srng, weak=shape in _WEAK_MODEL)
        reg = verifiers.ols({"data": settings, "responseColumn": "lot_defect_share",
                             "termsInModel": ["paste_thickness", "reflow_peak",
                                              "paste_thickness*reflow_peak"]})
        model_p = round(float(reg["modelPValue"]), 6)

        want = {
            0: True,
            1: model_p < 0.05 and effect_p < 0.05 and after_p <= _REQUIRED,
            2: model_p < 0.05 and effect_p < 0.05 and after_p > _REQUIRED,
            3: model_p < 0.05 and effect_p >= 0.05,
            4: model_p >= 0.05,
            5: True,
            6: model_p < 0.05 and effect_p < 0.05 and after_p > _REQUIRED,
        }[shape]
        if not want:
            continue

        trial = {"p1": p_before, "p2": _REQUIRED, "nPerGroup": n_trial, "alpha": 0.05}
        power = round(float(verifiers.power_two_proportions(trial)["power"]), 6)

        blocks = {
            "define": {"goal": "bring the defect share to the committed level and hold it",
                       "required_share": _REQUIRED,
                       "note": "the commitment is written as a share of units inspected"},
            "baseline": {"defectCounts": list(defects), "subgroupSizes": list(sizes),
                         "required_share": _REQUIRED},
            "settings": {"data": {k: list(v) for k, v in settings.items()},
                         "responseColumn": "lot_defect_share",
                         "termsInModel": ["paste_thickness", "reflow_peak",
                                          "paste_thickness*reflow_peak"]},
            "before_after": {"events1": e_before, "trials1": n_trial,
                             "events2": e_after, "trials2": n_trial,
                             "groupLabels": ["the window before the change",
                                             "the window after it"]},
            "after_lots": {"defectCounts": list(after_defects),
                           "subgroupSizes": list(after_sizes),
                           "required_share": _REQUIRED},
            "trial_size": dict(trial),
        }
        res = {"pchart": {"outOfControl": ooc, "centerLine": centre},
               "laney": {"outOfControl": int(verifiers.control_chart_laney_p(
                   {"defectCounts": defects, "subgroupSizes": sizes})["flaggedCount"])},
               "factors": {"modelPValue": model_p,
                           "rSquaredPct": round(float(reg["rSquaredPct"]), 4)},
               "effect": {"pValue": effect_p},
               "after": {"avgP": after_p,
                         "processZ": round(float(after_binom["processZ"]), 4)},
               "power": {"power": power},
               "_shape": SHAPES[shape]}
        return blocks, res

    raise RuntimeError(f"capacitor_defect: could not realise shape {shape} for seed {seed}")


CASE = V2Case(
    case_id="adb_c38",
    title="A reduction that is real, and a commitment that is still not met",
    industry="electronics",
    y_type="mixed",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    seeds=(0, 1, 2, 3, 4, 5, 6),
    shapes=dict(SHAPES), node_data=NODE_DATA,
    fault_targets=(("A_factors", "regression.ols",
                    "the per-lot settings record for this window was checked and is genuinely "
                    "not on file"),),
    budget={"max_turns": 26},
    context=(
        "We are the improvement team on a chip-capacitor line. Every unit is inspected and the "
        "project has committed to holding the defect share at or below 0.25% of units "
        "inspected. On file are the inspected and defective counts for twenty-five consecutive "
        "baseline lots; a per-lot record of two line settings alongside that lot's defect "
        "share; the inspected and defective totals for one window before a change was made to "
        "the line and one window after it; the inspected and defective counts for twenty lots "
        "run since the change; and the size and risk level the before-and-after trial was run "
        "at."),
    goal=(
        "Work through the batches the data steward will release and report where this project "
        "stands: whether the defect share held steady across the baseline, how it compares with "
        "what was committed to, whether anything on file accounts for it, whether the change "
        "that was made can be shown to have done anything, whether the level reached since is "
        "enough, and what should happen next. Every number in your report must come from a "
        "computation you ran on this task; where something could not be computed, say so "
        "rather than inventing it."),
    blocks_meta={
        "define": {"label": "Project charter and the committed defect share", "phase": "define",
                   "topics": ("charter", "committed share", "improvement target")},
        "baseline": {"label": "Per-lot inspected and defective counts, baseline",
                     "phase": "measure",
                     "topics": ("baseline lots", "inspected and defective counts")},
        "settings": {"label": "Per-lot line settings alongside that lot's defect share",
                     "phase": "analyze", "topics": ("line settings", "per-lot settings record")},
        "before_after": {"label": "Inspected and defective totals either side of the change",
                         "phase": "improve",
                         "topics": ("before and after the change", "trial totals")},
        "after_lots": {"label": "Per-lot inspected and defective counts since the change",
                       "phase": "improve", "topics": ("lots since the change", "new level")},
        "trial_size": {"label": "The size and risk level the trial was run at", "phase":
                       "improve", "topics": ("trial size", "risk level")},
    },
    field_map={
        "pchart.outOfControl": ({"method_id": "control_chart.p",
                                 "output": "outOfControlCount", "scale": 1.0},),
        "pchart.centerLine": ({"method_id": "control_chart.p", "output": "centerLine",
                               "scale": 1.0},),
        "laney.outOfControl": ({"method_id": "control_chart.laney_p", "output": "flaggedCount",
                                "scale": 1.0},),
        "factors.modelPValue": ({"method_id": "regression.ols", "output": "modelPValue",
                                 "scale": 1.0},),
        "effect.pValue": ({"method_id": "basic.two_proportions", "output": "pValue",
                           "scale": 1.0},),
        "after.avgP": ({"method_id": "capability.binomial", "output": "avgP", "scale": 1.0},),
        "power.power": ({"method_id": "power.two_proportions", "output": "power",
                         "scale": 1.0},),
    },
    truth_fields=(
        {"field": "pchart.outOfControl", "method_id": "control_chart.p",
         "output": "outOfControlCount", "scale": 1.0, "tol": 0.0},
        {"field": "pchart.centerLine", "method_id": "control_chart.p", "output": "centerLine",
         "scale": 1.0, "tol": 0.0001},
        {"field": "factors.modelPValue", "method_id": "regression.ols", "output": "modelPValue",
         "scale": 1.0, "tol": 0.002},
        {"field": "factors.rSquaredPct", "method_id": "regression.ols", "output": "rSquaredPct",
         "scale": 1.0, "tol": 0.5},
        {"field": "effect.pValue", "method_id": "basic.two_proportions", "output": "pValue",
         "scale": 1.0, "tol": 0.002},
        {"field": "after.avgP", "method_id": "capability.binomial", "output": "avgP",
         "scale": 1.0, "tol": 0.0001},
        {"field": "power.power", "method_id": "power.two_proportions", "output": "power",
         "scale": 1.0, "tol": 0.01},
    ),
)

if __name__ == "__main__":
    for s in CASE.seeds:
        _, r = generate(s)
        print(f"seed {s} [{r['_shape']:34s}] ooc={r['pchart']['outOfControl']} "
              f"pbar={r['pchart']['centerLine']:.5f} regP={r['factors']['modelPValue']:.4f} "
              f"effP={r['effect']['pValue']:.4f} after={r['after']['avgP']:.5f}"
              f"\n    {' -> '.join(walk(GRAPH, r))}")
