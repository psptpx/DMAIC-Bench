"""seal_strength — an optimum is only worth having if the surface it came from fits.

Onboarded from a design-for-six-sigma project on an assembled optical module, where two
geometric factors were taken to a response surface and the recommended settings were run and
confirmed. The scenario and the sequence -- screen, fit a surface, optimise, confirm -- are
drawn from that work; the data is generated from the seed and the case names nobody.

A fitted response surface hands back a set of settings and a predicted response whatever the
data looked like. Three separate things have to be true before that prediction is worth acting
on, and this project can fail at each of them independently:

  the second-order model must DESCRIBE the region     -- lack of fit against the centre runs
  its optimum must reach what the project needs       -- the prediction against the requirement
  the process must actually deliver it                -- a confirmation run at those settings

Seed 2 fails the first: R-Sq near 97% and a lack-of-fit test that rejects, which is the case
worth having, because a high R-Sq is exactly what makes a contestant stop looking. Seed 6 fails
the second: the surface fits, its constrained optimum is found, and the best it can reach
inside the region that was explored is nowhere near what the project needs -- the design has to
move, not the settings. Seed 3 fails the third: the surface fits, the optimum clears the bar,
the confirmation runs are made, and they cannot be shown to reach the level the project
requires. The three failures have three different next steps, and none of them is the control
plan.

The confirmation is tested against the level the CHARTER requires, not against the surface's own
prediction, so nothing in that batch hands over a number the optimiser was supposed to produce.
"""
from __future__ import annotations

import random

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import verifiers
from dmaic_bench.v2.cases import _fixtures as _f
from dmaic_bench.v2.models import V2Case

_LSL = 45.0            # the seal must hold at least this, in N
_NEEDED = 55.0         # the level the project has to reach for the margin it committed to
_N_BASELINE = 60
_ALPHA = 1.41421356    # the axial distance of the composite design
_CCD_POINTS = ([(-1, -1), (1, -1), (-1, 1), (1, 1),
                (-_ALPHA, 0), (_ALPHA, 0), (0, -_ALPHA), (0, _ALPHA)] + [(0, 0)] * 5)

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define", label="Scope: seal strength and the level required"),
        GraphNode("M_stability", "measure", methods=("control_chart.imr",),
                  produces=("imr.outOfControl",),
                  label="Run stability across the baseline record"),
        GraphNode("A_special", "analyze", methods=("control_chart.imr",),
                  label="Special-cause investigation (no index applies to this run yet)"),
        GraphNode("A_cap", "analyze", methods=("capability.normal",),
                  produces=("cap.ppk",),
                  label="Where seal strength sits against the level it must hold"),
        GraphNode("A_screen", "analyze", methods=("doe.factorial_analysis",),
                  produces=("screen.modelPValue",),
                  label="The screening run: do the varied settings account for the response?"),
        GraphNode("A_more_x", "analyze",
                  label="The settings that were varied account for nothing; the project returns "
                        "to identifying candidate causes"),
        GraphNode("A_rsm", "analyze", methods=("doe.rsm_analysis",),
                  produces=("rsm.lackOfFitPValue",),
                  label="The composite design: does a second-order model describe this region?"),
        GraphNode("A_augment", "analyze", methods=("doe.rsm_canonical",),
                  produces=("canonical.predictedAtStationary",),
                  label="The model does not describe the region: where the surface actually "
                        "turns, and where the design has to go next"),
        GraphNode("A_optimise", "analyze", methods=("doe.rsm_optimizer",),
                  produces=("opt.predictedResponse",),
                  label="The best the fitted surface can reach inside the region explored"),
        GraphNode("A_widen", "analyze", methods=("doe.rsm_canonical",),
                  produces=("canonical.predictedAtStationary",),
                  label="What was explored cannot deliver what is needed: where the surface "
                        "turns, and where the design region has to move"),
        GraphNode("I_confirm", "improve", methods=("basic.one_sample_t",),
                  produces=("confirm.pValue",),
                  label="Confirmation runs at the recommended settings, against the level "
                        "required"),
        GraphNode("C_control", "control", label="Control plan"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_stability"),
        GuardedEdge("M_stability", "A_cap", "imr.outOfControl == 0",
                    guard_fields=("imr.outOfControl",)),
        GuardedEdge("M_stability", "A_special", is_default=True),
        GuardedEdge("A_cap", "C_control", "cap.ppk >= 1.33", guard_fields=("cap.ppk",)),
        GuardedEdge("A_cap", "A_screen", is_default=True),
        GuardedEdge("A_screen", "A_rsm", "screen.modelPValue < 0.05",
                    guard_fields=("screen.modelPValue",)),
        GuardedEdge("A_screen", "A_more_x", is_default=True),
        # ONE: does the model describe the region? A high R-Sq does not answer this.
        GuardedEdge("A_rsm", "A_optimise", "rsm.lackOfFitPValue >= 0.05",
                    guard_fields=("rsm.lackOfFitPValue",)),
        GuardedEdge("A_rsm", "A_augment", is_default=True),
        # TWO: can the best point in the region explored reach what the project needs?
        GuardedEdge("A_optimise", "I_confirm", "opt.predictedResponse >= 55",
                    guard_fields=("opt.predictedResponse",)),
        GuardedEdge("A_optimise", "A_widen", is_default=True),
        # THREE: does the process deliver it when it is run?
        GuardedEdge("I_confirm", "C_control", "confirm.pValue < 0.05",
                    guard_fields=("confirm.pValue",)),
        GuardedEdge("I_confirm", "A_widen", is_default=True),
        GuardedEdge("A_special", "C_control"),
    ),
)

GATE_POLICY = (
    {"stage": "A_cap", "requires": "M_stability", "unlock_when": "imr.outOfControl == 0",
     "rule": "no capability study on a run that is not in control"},
    {"stage": "A_special", "requires": "M_stability", "unlock_when": "imr.outOfControl > 0",
     "rule": "special-cause work only once the run is shown to be unstable"},
    {"stage": "A_screen", "requires": "A_cap", "unlock_when": "cap.ppk < 1.33",
     "rule": "no experiment is designed until the baseline has been shown to fall short"},
    {"stage": "A_rsm", "requires": "A_screen", "unlock_when": "screen.modelPValue < 0.05",
     "rule": "a surface is only fitted over factors the screening run found to matter"},
    {"stage": "A_optimise", "requires": "A_rsm", "unlock_when": "rsm.lackOfFitPValue >= 0.05",
     "rule": "an optimum is only read off a surface that has been shown to describe the region"},
    {"stage": "A_augment", "requires": "A_rsm", "unlock_when": "rsm.lackOfFitPValue < 0.05",
     "rule": "the design is only augmented once the model has been shown not to fit"},
    {"stage": "I_confirm", "requires": "A_optimise",
     "unlock_when": "opt.predictedResponse >= 55",
     "rule": "settings are only run for confirmation once the surface says they can reach the "
             "level required"},
)

NODE_DATA = {"D_scope": "define", "M_stability": "baseline", "A_special": "baseline",
             "A_cap": "baseline", "A_screen": "screening_run",
             "A_rsm": "composite_design", "A_optimise": "composite_design",
             "A_augment": "composite_design", "A_widen": "composite_design",
             "I_confirm": "confirmation_runs"}

SHAPES = {0: "already-holds-the-level",
          1: "surface-fits/optimum-clears/confirmed",
          2: "surface-does-NOT-fit",
          3: "surface-fits/optimum-clears/NOT-confirmed",
          4: "screening-accounts-for-nothing",
          5: "baseline-unstable",
          6: "surface-fits/region-cannot-reach-the-level"}

_WEAK_SCREEN = {4}
_LACK_OF_FIT = {2}
_LOW_REGION = {6}
_CONFIRM_FAILS = {3}


def _baseline(rng, shape):
    if shape == 5:
        xs = [52.5 + 4.0 * max(-2.4, min(2.4, rng.gauss(0, 1))) for _ in range(_N_BASELINE)]
        for i in range(_N_BASELINE // 2, _N_BASELINE):
            xs[i] += 13.0
    elif shape == 0:
        xs = [58.0 + 2.6 * max(-2.6, min(2.6, rng.gauss(0, 1))) for _ in range(_N_BASELINE)]
    else:
        xs = [52.0 + 4.2 * max(-2.6, min(2.6, rng.gauss(0, 1))) for _ in range(_N_BASELINE)]
    return [round(x, 2) for x in xs]


def _screening(rng, weak):
    b = (0.10, 0.08, 0.05, 0.04) if weak else (2.30, 1.55, 0.20, 0.85)
    runs = []
    for a in (-1, 1):
        for bb in (-1, 1):
            for c in (-1, 1):
                for _ in range(2):
                    y = (53.0 + b[0] * a + b[1] * bb + b[2] * c + b[3] * a * bb
                         + rng.gauss(0, 1.05))
                    runs.append({"bond_angle": a, "bead_spacing": bb, "cure_temperature": c,
                                 "y": round(y, 3)})
    return runs


def _ccd(rng, shape):
    out = []
    for a, b in _CCD_POINTS:
        if shape in _LACK_OF_FIT:
            y = 58 + 3.0 * a + 1.8 * b - 2.2 * a * a - 1.6 * b * b + 0.9 * a * b + 2.2 * a ** 3
        elif shape in _LOW_REGION:
            y = 48 + 0.8 * a + 0.5 * b - 1.5 * a * a - 1.2 * b * b
        else:
            y = 58 + 3.0 * a + 1.8 * b - 2.2 * a * a - 1.6 * b * b + 0.9 * a * b
        out.append({"bond_angle": a, "bead_spacing": b, "y": round(y + rng.gauss(0, 0.45), 4)})
    return out


def generate(seed: int):
    shape = seed if seed in SHAPES else seed % 5
    rng = random.Random(seed * 1_000_003 + 20260949)

    for _ in range(800):
        base = _baseline(rng, shape)
        ooc = int(verifiers.control_chart_imr({"data": base})["flaggedCount"])
        if shape == 5:
            if ooc == 0:
                continue
        elif ooc != 0:
            continue

        res = {"imr": {"outOfControl": ooc}, "_shape": SHAPES[shape]}
        if ooc == 0:
            cap = verifiers.capability_normal({"data": base, "lsl": _LSL})
            ppk = round(float(cap["ppk"]), 4)
            if (shape == 0) != (ppk >= 1.33):
                continue
            res["cap"] = {"ppk": ppk}

        screen_runs = _screening(rng, weak=shape in _WEAK_SCREEN)
        doe = verifiers.doe_factorial_analysis({"runs": screen_runs})
        screen_p = round(float(doe["modelPValue"]), 6)
        if (shape in _WEAK_SCREEN) != (screen_p >= 0.05):
            continue

        ccd = _ccd(rng, shape)
        rsm = verifiers.doe_rsm_analysis({"runs": ccd})
        lof_p = round(float(rsm["lackOfFitPValue"]), 6)
        if (shape in _LACK_OF_FIT) != (lof_p < 0.05):
            continue

        opt = verifiers.doe_rsm_optimizer(
            {"surface_data": ccd, "goal": "maximize",
             "bounds": [[-_ALPHA, _ALPHA], [-_ALPHA, _ALPHA]]})
        pred = round(float(opt["predictedResponse"]), 4)
        if (shape in _LOW_REGION) != (pred < _NEEDED):
            continue

        crng = random.Random(seed * 7_919 + 20260951)
        mu = 55.2 if shape in _CONFIRM_FAILS else 59.6
        confirm = [round(mu + 2.0 * crng.gauss(0, 1), 2) for _ in range(20)]
        conf_p = round(float(verifiers.one_sample_t(
            {"data": confirm, "mu": _NEEDED})["pValue"]), 6)
        if (shape in _CONFIRM_FAILS) != (conf_p >= 0.05):
            continue

        canon = verifiers.doe_rsm_canonical({"runs": ccd})

        res["screen"] = {"modelPValue": screen_p,
                         "rSquaredPct": round(float(doe["rSquaredPct"]), 4)}
        res["rsm"] = {"lackOfFitPValue": lof_p,
                      "rSquaredPct": round(float(rsm["rSquaredPct"]), 4)}
        res["opt"] = {"predictedResponse": pred}
        res["canonical"] = {"predictedAtStationary": round(
            float(canon["predictedAtStationary"]), 4)}
        res["confirm"] = {"pValue": conf_p}

        blocks = {
            "define": {"goal": "hold seal strength above the level the product requires",
                       "lsl": _LSL, "required_level": _NEEDED, "unit": "N"},
            "baseline": {"data": list(base), "lsl": _LSL, "required_level": _NEEDED},
            "screening_run": {"runs": [dict(r) for r in screen_runs],
                              "coding": "-1 / +1, low and high setting of each",
                              "columns": ["bond_angle", "bead_spacing", "cure_temperature",
                                          "y"]},
            "composite_design": {"runs": [dict(r) for r in ccd],
                                 "coding": "coded units; the centre setting was run five times",
                                 "columns": ["bond_angle", "bead_spacing", "y"]},
            "confirmation_runs": {"data": list(confirm), "mu": _NEEDED,
                                  "note": "seals made at the settings the design work "
                                          "recommended"},
        }
        return blocks, res

    raise RuntimeError(f"seal_strength: could not realise shape {shape} for seed {seed}")


CASE = V2Case(
    case_id="adb_c39",
    title="A response surface, its optimum, and three ways of not being finished",
    industry="discrete_manufacturing",
    y_type="continuous",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    seeds=(0, 1, 2, 3, 4, 5, 6),
    shapes=dict(SHAPES), node_data=NODE_DATA,
    fault_targets=(("A_screen", "doe.factorial_analysis",
                    "the screening run table for this build was checked and is genuinely not "
                    "on file"),),
    budget={"max_turns": 28},
    context=(
        "We are the development team on an assembled optical module. The seal between the two "
        "housings must hold at least 45 N, and the product margin the programme committed to "
        "needs it above 55 N. Sixty consecutive assemblies have been pulled and tested in the "
        "order they were built. The archive also holds a screening run in which three assembly "
        "settings were each taken to a low and a high level twice over; a later composite "
        "design over two of those settings, with the centre setting run five times; and twenty "
        "seals made at the settings that design work recommended."),
    goal=(
        "Work through the batches the data steward will release and report where this project "
        "stands: how the line has behaved across the baseline, where seal strength sits against "
        "what the product requires, whether the settings that were varied account for it, what "
        "the design work supports concluding, and what should happen next. Every number in your "
        "report must come from a computation you ran on this task; where something could not be "
        "computed, say so rather than inventing it."),
    blocks_meta={
        "define": {"label": "Programme charter and the seal-strength requirement",
                   "phase": "define",
                   "topics": ("charter", "seal requirement", "product margin")},
        "baseline": {"label": "Seal strength assembly by assembly, in the order built",
                     "phase": "measure", "topics": ("baseline record", "build order")},
        "screening_run": {"label": "The screening run: three settings at a low and a high level",
                          "phase": "analyze",
                          "topics": ("screening run", "assembly settings", "screening table")},
        "composite_design": {"label": "The composite design over two settings, centre run five "
                                      "times", "phase": "analyze",
                             "topics": ("composite design", "centre runs", "design table")},
        "confirmation_runs": {"label": "Seals made at the recommended settings",
                              "phase": "improve",
                              "topics": ("recommended settings", "confirmation seals")},
    },
    field_map={
        "imr.outOfControl": _f.SRC_IMR_OOC,
        "cap.ppk": _f.SRC_PPK,
        "screen.modelPValue": ({"method_id": "doe.factorial_analysis",
                                "output": "modelPValue", "scale": 1.0},),
        "rsm.lackOfFitPValue": ({"method_id": "doe.rsm_analysis",
                                 "output": "lackOfFitPValue", "scale": 1.0},),
        "opt.predictedResponse": ({"method_id": "doe.rsm_optimizer",
                                   "output": "predictedResponse", "scale": 1.0},),
        "canonical.predictedAtStationary": ({"method_id": "doe.rsm_canonical",
                                             "output": "predictedAtStationary", "scale": 1.0},),
        "confirm.pValue": ({"method_id": "basic.one_sample_t", "output": "pValue",
                            "scale": 1.0},),
    },
    truth_fields=(
        {"field": "imr.outOfControl", "method_id": "control_chart.imr",
         "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "cap.ppk", "method_id": "capability.normal", "output": "ppk",
         "scale": 1.0, "tol": 0.01},
        {"field": "screen.modelPValue", "method_id": "doe.factorial_analysis",
         "output": "modelPValue", "scale": 1.0, "tol": 0.002},
        {"field": "rsm.rSquaredPct", "method_id": "doe.rsm_analysis", "output": "rSquaredPct",
         "scale": 1.0, "tol": 0.5},
        {"field": "rsm.lackOfFitPValue", "method_id": "doe.rsm_analysis",
         "output": "lackOfFitPValue", "scale": 1.0, "tol": 0.01},
        # opt.predictedResponse is NOT published: it is the number the confirmation batch would
        # otherwise hand over, and the point of that batch is that it was RUN, not predicted.
        {"field": "confirm.pValue", "method_id": "basic.one_sample_t", "output": "pValue",
         "scale": 1.0, "tol": 0.01},
    ),
)

if __name__ == "__main__":
    for s in CASE.seeds:
        _, r = generate(s)
        print(f"seed {s} [{r['_shape']:44s}] ooc={r['imr']['outOfControl']} "
              f"ppk={r.get('cap', {}).get('ppk')} scrP={r['screen']['modelPValue']:.4f} "
              f"LOF={r['rsm']['lackOfFitPValue']:.4f} pred={r['opt']['predictedResponse']:.2f} "
              f"confP={r['confirm']['pValue']:.4f}\n    {' -> '.join(walk(GRAPH, r))}")
