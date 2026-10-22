"""shaft_hardness — which comparison the data admits, and a candidate that turns out not to matter.

Onboarded from a black-belt project on a gear-shaft heat-treatment line. The scenario, the
candidate factor and the negative result are drawn from that work; the data is generated from
the seed and the case names nobody. The source project screened several candidate causes and
reported that one of them did not survive testing (p > 0.05) -- and then said so, rather than
finding a way to keep it.

Two things are being asked here at once.

**Which comparison the data admits.** Three recipes are to be compared, and what may be
compared depends on what the characteristic does: a run that is not normal is compared with a
rank test, and a set of groups whose SPREADS differ is not a means problem at all. Unequal
spread across recipes is a finding, not an obstacle to the finding -- the recipes are not
producing the same level of consistency, and the project acts on that rather than pressing on
to a comparison of averages whose assumption it has just watched fail. The distribution check
is made on the baseline run, which is one population and where the question is well posed; a
normality test on the pooled comparison sample answers a different question and rejects
whenever the recipes differ, which is the case it is supposed to detect.

**A candidate that does not survive.** Two seeds end at "this factor is not a driver". One of
them (seed 7) has recipe averages that are visibly apart -- a full point of hardness between
the lowest and the highest -- and a spread and sample size that make that difference
indistinguishable from noise. Reporting the gap and calling it an effect is the error the seed
exists to catch, and the honest route out of it is backwards, to candidate causes, not forwards
to an improvement.
"""
from __future__ import annotations

import math
import random

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import verifiers
from dmaic_bench.v2.cases import _fixtures
from dmaic_bench.v2.cases import _fixtures as _f
from dmaic_bench.v2.models import V2Case

_N_BASELINE = 60
_PER_RECIPE = 15
_RECIPES = ("recipe A", "recipe B", "recipe C")

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define",
                  label="Scope: case-surface hardness and the candidate being tested"),
        GraphNode("M_msa", "measure", methods=("msa.gage_rr_crossed",),
                  produces=("msa.pctSV", "msa.ndc"),
                  label="Hardness tester study (crossed, several operators over the same parts)"),
        GraphNode("M_msa_fix", "measure",
                  label="Correct the hardness tester and re-run the study (readings cannot "
                        "support any downstream conclusion)"),
        GraphNode("M_stability", "measure", methods=("control_chart.imr",),
                  produces=("imr.outOfControl",),
                  label="Run stability across the baseline record"),
        GraphNode("A_special", "analyze", methods=("control_chart.imr",),
                  label="Special-cause investigation (nothing is compared against a moving "
                        "baseline)"),
        GraphNode("A_route", "analyze", methods=("basic.normality",),
                  produces=("normality.pValue",),
                  label="What the baseline distribution allows"),
        GraphNode("A_variances", "analyze", methods=("anova.equal_variances",),
                  produces=("variances.pValue",),
                  label="Do the three recipes hold the same spread?"),
        GraphNode("A_anova", "analyze", methods=("anova.oneway",),
                  produces=("recipes.factorPValue",),
                  label="Do the three recipes hold the same level?"),
        GraphNode("A_kruskal", "analyze", methods=("nonparametric.kruskal_wallis",),
                  produces=("kruskal.pValue",),
                  label="Do the three recipes hold the same level (rank comparison)?"),
        GraphNode("A_spread", "analyze", methods=("anova.sov",),
                  produces=("sov.betweenVariance",),
                  label="The recipes differ in consistency: where the spread sits"),
        GraphNode("I_stabilise", "improve",
                  label="Improve (bring the inconsistent recipe onto the others' spread)"),
        GraphNode("I_select", "improve", methods=("basic.two_sample_t",),
                  produces=("select.pValue",),
                  label="Improve (the two leading recipes against each other)"),
        GraphNode("A_not_a_driver", "analyze",
                  label="This candidate does not account for the response; the project returns "
                        "to identifying candidate causes"),
        GraphNode("C_control", "control", label="Control plan"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_msa"),
        GuardedEdge("M_msa", "M_stability", "msa.pctSV <= 0.30 and msa.ndc >= 5",
                    guard_fields=("msa.pctSV", "msa.ndc")),
        GuardedEdge("M_msa", "M_msa_fix", is_default=True),
        GuardedEdge("M_stability", "A_route", "imr.outOfControl == 0",
                    guard_fields=("imr.outOfControl",)),
        GuardedEdge("M_stability", "A_special", is_default=True),
        GuardedEdge("A_route", "A_variances", "normality.pValue >= 0.05",
                    guard_fields=("normality.pValue",)),
        GuardedEdge("A_route", "A_kruskal", is_default=True),
        GuardedEdge("A_variances", "A_anova", "variances.pValue >= 0.05",
                    guard_fields=("variances.pValue",)),
        GuardedEdge("A_variances", "A_spread", is_default=True),
        GuardedEdge("A_anova", "I_select", "recipes.factorPValue < 0.05",
                    guard_fields=("recipes.factorPValue",)),
        GuardedEdge("A_anova", "A_not_a_driver", is_default=True),
        GuardedEdge("A_kruskal", "I_select", "kruskal.pValue < 0.05",
                    guard_fields=("kruskal.pValue",)),
        GuardedEdge("A_kruskal", "A_not_a_driver", is_default=True),
        GuardedEdge("A_spread", "I_stabilise"),
        GuardedEdge("I_stabilise", "C_control"),
        GuardedEdge("I_select", "C_control"),
        GuardedEdge("A_special", "C_control"),
    ),
)

GATE_POLICY = (
    {"stage": "M_stability", "requires": "M_msa",
     "unlock_when": "msa.pctSV <= 0.30 and msa.ndc >= 5",
     "rule": "the tester must be acceptable on BOTH AIAG criteria before anything is compared"},
    {"stage": "M_msa_fix", "requires": "M_msa", "unlock_when": "msa.pctSV > 0.30 or msa.ndc < 5",
     "rule": "remediation only once the tester has been judged unusable"},
    {"stage": "A_route", "requires": "M_stability", "unlock_when": "imr.outOfControl == 0",
     "rule": "nothing is compared against a baseline that is still moving"},
    {"stage": "A_special", "requires": "M_stability", "unlock_when": "imr.outOfControl > 0",
     "rule": "special-cause work only once the run is shown to be unstable"},
    {"stage": "A_variances", "requires": "A_route", "unlock_when": "normality.pValue >= 0.05",
     "rule": "the parametric route is only opened once the distribution allows it"},
    {"stage": "A_kruskal", "requires": "A_route", "unlock_when": "normality.pValue < 0.05",
     "rule": "the rank comparison is the route the distribution leaves"},
    {"stage": "A_anova", "requires": "A_variances", "unlock_when": "variances.pValue >= 0.05",
     "rule": "a comparison of averages presumes the spreads it is averaging over are alike"},
    {"stage": "A_spread", "requires": "A_variances", "unlock_when": "variances.pValue < 0.05",
     "rule": "the spread is the finding once the recipes are shown not to share one"},
)

NODE_DATA = {"D_scope": "define", "M_msa": "msa",
             "M_stability": "baseline", "A_special": "baseline", "A_route": "baseline",
             "A_variances": "recipes", "A_anova": "recipes", "A_kruskal": "recipes",
             "A_spread": "recipes", "I_select": "leading_two"}

SHAPES = {0: "normal/equal-spread/recipe-matters",
          1: "normal/equal-spread/NOT-a-driver",
          2: "normal/unequal-spread",
          3: "not-normal/recipe-matters",
          4: "not-normal/NOT-a-driver",
          5: "tester-unacceptable",
          6: "baseline-unstable",
          7: "normal/equal-spread/visible-gap-that-is-noise"}

_NOT_NORMAL = {3, 4}
_NO_EFFECT = {1, 4, 7}


def _baseline(rng, shape):
    if shape == 6:
        xs = [58.9 + 1.05 * max(-2.4, min(2.4, rng.gauss(0, 1))) for _ in range(_N_BASELINE)]
        for i in range(_N_BASELINE // 2, _N_BASELINE):
            xs[i] += 3.6
    elif shape in _NOT_NORMAL:
        xs = [56.5 + 1.5 * math.exp(0.48 * rng.gauss(0, 1)) for _ in range(_N_BASELINE)]
    else:
        xs = [58.9 + 1.05 * max(-2.6, min(2.6, rng.gauss(0, 1))) for _ in range(_N_BASELINE)]
    return [round(x, 2) for x in xs]


def _recipes(rng, shape):
    """Three recipes. Means and spreads per shape; every verdict is derived, never asserted."""
    if shape == 2:                       # same level, three different spreads
        spec = ((59.0, 0.45), (59.1, 1.05), (58.9, 2.55))
        n = _PER_RECIPE
    elif shape == 7:                     # a full point between the extremes, and it is noise
        spec = ((58.4, 2.60), (59.2, 2.60), (60.0, 2.60))
        n = 8
    elif shape in _NO_EFFECT:
        spec = ((58.9, 1.10), (59.05, 1.10), (59.2, 1.10))
        n = _PER_RECIPE
    else:
        spec = ((58.0, 0.95), (59.7, 0.95), (61.3, 0.95))
        n = _PER_RECIPE
    if shape in _NOT_NORMAL:             # the same levels, on a skewed characteristic
        out = {}
        for name, (mu, sd) in zip(_RECIPES, spec):
            out[name] = [round(mu - 1.4 + sd * 1.35 * math.exp(0.42 * rng.gauss(0, 1)), 2)
                         for _ in range(n)]
        return out
    return {name: [round(mu + sd * rng.gauss(0, 1), 2) for _ in range(n)]
            for name, (mu, sd) in zip(_RECIPES, spec)}


def generate(seed: int):
    shape = seed if seed in SHAPES else seed % 5
    rng = random.Random(seed * 1_000_003 + 20260941)

    grng = random.Random(seed * 7_919 + 20260943)
    common = dict(center=59.0, tolerance=6.0, part_sd=1.4, operator_sd=0.10)
    if shape == 5:
        msa_block, msa_stats = _fixtures.gage_rr_study(
            grng, repeat_sd=1.10, **common, window=_fixtures.GRR_FAIL_WINDOW, min_ndc=0,
            pooled_window=_fixtures.GRR_FAIL_POOLED_WINDOW)
    else:
        msa_block, msa_stats = _fixtures.gage_rr_study(grng, repeat_sd=0.20, **common)

    for _ in range(600):
        base = _baseline(rng, shape)
        ooc = int(verifiers.control_chart_imr({"data": base})["flaggedCount"])
        pval = float(verifiers.normality({"data": base})["pValue"])
        if shape == 6:
            ok = ooc > 0
        elif shape in _NOT_NORMAL:
            ok = ooc == 0 and pval < 0.05
        else:
            ok = ooc == 0 and pval >= 0.05
        if not ok:
            continue

        groups = _recipes(rng, shape)
        var_p = round(float(verifiers.equal_variances({"groups": groups})["pValue"]), 6)
        anova_p = round(float(verifiers.anova_oneway({"groups": groups})["factorPValue"]), 6)
        kw_p = round(float(verifiers.kruskal_wallis({"groups": groups})["pValue"]), 6)

        if shape == 2:
            ok = var_p < 0.05
        elif shape in _NOT_NORMAL:
            ok = (kw_p >= 0.05) if shape in _NO_EFFECT else (kw_p < 0.05)
        elif shape in (0, 1, 7):
            ok = var_p >= 0.05 and (
                (anova_p >= 0.05) if shape in _NO_EFFECT else (anova_p < 0.05))
        else:
            ok = True
        if not ok:
            continue

        ordered = sorted(groups.items(), key=lambda kv: sum(kv[1]) / len(kv[1]), reverse=True)
        leading = {"group1": list(ordered[0][1]), "group2": list(ordered[1][1]),
                   "groupLabels": [ordered[0][0], ordered[1][0]]}

        res = {"msa": dict(msa_stats), "imr": {"outOfControl": ooc},
               "normality": {"pValue": round(pval, 4)},
               "variances": {"pValue": var_p},
               "recipes": {"factorPValue": anova_p},
               "kruskal": {"pValue": kw_p},
               "sov": {"betweenVariance": round(float(
                   verifiers.anova_sov({"groups": groups})["betweenVariance"]), 4)},
               "select": {"pValue": round(float(
                   verifiers.two_sample_t(leading)["pValue"]), 6)},
               "_shape": SHAPES[shape]}

        blocks = {
            "define": {"goal": "establish whether the heat-treat recipe accounts for "
                               "case-surface hardness",
                       "unit": "HRC",
                       "candidate": "three heat-treat recipes currently in use"},
            "msa": dict(msa_block),
            "baseline": {"data": list(base),
                         "note": "one population, recorded shaft by shaft in the order run"},
            # THE BATCH DECLARES WHICH EQUAL-VARIANCE TEST IT IS READ UNDER. Several are
            # defensible and they disagree: on this seed Levene/median gives 0.879 and
            # Bartlett 0.573, against a 0.08 tolerance. The reference solution defaults to
            # Bartlett when no convention is declared, so an undeclared batch drops the
            # oracle ceiling for a reason that is a task defect rather than a hard task --
            # measured, on a live containerised run: 0.952 instead of 1.000.
            "recipes": {"groups": {k: list(v) for k, v in groups.items()},
                        "varianceTestCentering": "median"},
            "leading_two": dict(leading),
        }
        return blocks, res

    raise RuntimeError(f"shaft_hardness: could not realise shape {shape} for seed {seed}")


CASE = V2Case(
    case_id="adb_c37",
    # Welch ANOVA on the recipe means is a defensible alternative to a sources-of-variation
    # analysis when the spreads differ (Minitab one-way ANOVA options; 2026-09-18 expert review
    # B022, three of three reviewers). It is neither a wrong turn nor proof of the reference
    # branch at this fork.
    accepted_methods={"A_variances": ("anova.welch",)},
    title="Whether the recipe accounts for hardness, and what the data lets us ask",
    industry="discrete_manufacturing",
    y_type="continuous",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    seeds=(0, 1, 2, 3, 4, 5, 6, 7),
    shapes=dict(SHAPES), node_data=NODE_DATA,
    fault_targets=(("A_variances", "anova.equal_variances",
                    "the recipe-by-recipe sample for this window was checked and is genuinely "
                    "not on file"),),
    budget={"max_turns": 26},
    context=(
        "We are the improvement team on a gear-shaft heat-treatment line. Case-surface hardness "
        "is the characteristic under study and the heat-treat recipe is the candidate cause "
        "currently on the table; three recipes are in use. Sixty consecutive shafts from one "
        "population have been recorded in the order they were run, a separate sample records "
        "hardness for shafts made under each of the three recipes, the archive holds the study "
        "in which the same shafts were measured several times over by several operators on the "
        "hardness tester, and the two recipes with the highest averages have been pulled out "
        "into a sample of their own."),
    goal=(
        "Work through the batches the data steward will release and report where this project "
        "stands: whether the recorded hardness readings can carry a conclusion, how the "
        "baseline has behaved, what kind of comparison these readings admit, what that "
        "comparison says about the recipe, and what should happen next. Every number in your "
        "report must come from a computation you ran on this task; where something could not "
        "be computed, say so rather than inventing it."),
    blocks_meta={
        "define": {"label": "Project charter and the candidate under test", "phase": "define",
                   "topics": ("charter", "candidate cause", "hardness requirement")},
        "msa": {"label": "Repeat readings of the same shafts", "phase": "measure",
                "topics": ("repeat readings", "operator study")},
        "baseline": {"label": "Hardness shaft by shaft, in the order run", "phase": "measure",
                     "topics": ("baseline record", "shaft order")},
        "recipes": {"label": "Hardness sampled separately under each recipe", "phase": "analyze",
                    "topics": ("recipe by recipe", "three recipes")},
        "leading_two": {"label": "The two recipes with the highest averages, side by side",
                        "phase": "improve", "topics": ("leading two", "head to head sample")},
    },
    field_map={
        "msa.pctSV": _f.SRC_GRR_PCT, "msa.ndc": _f.SRC_GRR_NDC,
        "imr.outOfControl": _f.SRC_IMR_OOC,
        "normality.pValue": _f.SRC_NORMALITY,
        "variances.pValue": ({"method_id": "anova.equal_variances", "output": "pValue",
                              "scale": 1.0},),
        "recipes.factorPValue": ({"method_id": "anova.oneway", "output": "factorPValue",
                                  "scale": 1.0},),
        "kruskal.pValue": ({"method_id": "nonparametric.kruskal_wallis", "output": "pValue",
                            "scale": 1.0},),
        "sov.betweenVariance": ({"method_id": "anova.sov", "output": "betweenVariance",
                                 "scale": 1.0},),
        "select.pValue": ({"method_id": "basic.two_sample_t", "output": "pValue",
                           "scale": 1.0},),
    },
    truth_fields=(
        _f.TRUTH_GRR_PCT,
        _f.TRUTH_GRR_NDC,
        {"field": "imr.outOfControl", "method_id": "control_chart.imr",
         "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "normality.pValue", "method_id": "basic.normality", "output": "pValue",
         "scale": 1.0, "tol": 0.01},
        # anova.equal_variances is Levene/median here; Bartlett answers the same question and
        # lands inside this deliberately wide tolerance on near-normal groups.
        {"field": "variances.pValue", "method_id": "anova.equal_variances", "output": "pValue",
         "scale": 1.0, "tol": 0.08},
        {"field": "recipes.factorPValue", "method_id": "anova.oneway",
         "output": "factorPValue", "scale": 1.0, "tol": 0.002},
        {"field": "kruskal.pValue", "method_id": "nonparametric.kruskal_wallis",
         "output": "pValue", "scale": 1.0, "tol": 0.002},
        {"field": "select.pValue", "method_id": "basic.two_sample_t", "output": "pValue",
         "scale": 1.0, "tol": 0.01},
    ),
)

if __name__ == "__main__":
    for s in CASE.seeds:
        _, r = generate(s)
        print(f"seed {s} [{r['_shape']:42s}] ooc={r['imr']['outOfControl']} "
              f"AD={r['normality']['pValue']:.3f} var={r['variances']['pValue']:.3f} "
              f"anova={r['recipes']['factorPValue']:.4f} kw={r['kruskal']['pValue']:.4f}"
              f"\n    {' -> '.join(walk(GRAPH, r))}")
