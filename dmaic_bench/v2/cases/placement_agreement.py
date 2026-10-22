"""placement_agreement — a visual accept/reject judgement that has to be REPAIRED AND RE-PROVED.

Onboarded from a black-belt project on an electronic-assembly line where the same characteristic
was judged at several inspection stations. The scenario, the remediation and the two-study
structure are drawn from that work; the data is generated from the seed and the case names
nobody.

Every other project in this corpus that fails its measurement study stops there: the finding is
"the measurement system cannot carry a conclusion", and stopping IS the answer. That is only half
of what AIAG MSA-4 asks. A judgement that has been repaired has NOT been shown to work; it has
been shown to have been changed. The obligation is to re-run the study and read the second
verdict, and the second verdict is allowed to fail -- in the source project the first study ran
at kappa 0.44 and the repaired one at 1.00, and there was no way to know that in advance.

So this project routes on TWO measurement verdicts, and its remediation node is not a dead end:

  study 1 acceptable                      -> straight on to the record
  study 1 fails -> repair -> study 2 acceptable  -> on to the record, four steps later
  study 1 fails -> repair -> study 2 fails       -> the characteristic cannot be judged by eye
                                                    at all, and the project escalates

The repair node carries a real computation of its own -- which reject category the judgements
actually split on -- for two reasons. It is what an analyst does before rewriting a criterion,
and it is the only thing that distinguishes the two branches out of the first study to a scorer:
both of them eventually run the same agreement analysis and the same charts, so without it a
contestant that walked either one looks identical from the outside.

The two studies also share a ``method_id``, which is why their ``field_map`` sources pin
themselves to an INVOCATION. The default merge is last-wins, and last-wins here would let the
repaired study's verdict answer for the original one -- turning the decision this project is
built on into a decision no trace can express.
"""
from __future__ import annotations

import random

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import verifiers
from dmaic_bench.v2.cases import _fixtures
from dmaic_bench.v2.models import V2Case

_TARGET_P = 0.02          # the reject share the line is required to hold
_K = 25                   # boards inspected per lot, lots in the record
_N_LOT = 400

#: The reject categories the judgement splits on. Named, not numbered, because the repair step
#: is "rewrite the criterion for THIS category" and a contestant has to be able to say which.
_CATEGORIES = ("insufficient solder", "component offset", "tombstone", "solder bridge",
               "wrong polarity")

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define",
                  label="Scope: the reject share at visual inspection and its required level"),
        GraphNode("M_agree1", "measure", methods=("msa.attribute_agreement",),
                  produces=("agree1.kappaMin",),
                  label="Inspector judgements against the retained answer key"),
        GraphNode("M_disagree", "measure", methods=("quality.pareto",),
                  produces=("disagree.topCategoryPct",),
                  label="Where the judgements split: disagreements by reject category"),
        GraphNode("M_agree2", "measure", methods=("msa.attribute_agreement",),
                  produces=("agree2.kappaMin",),
                  label="The judgement study re-run after the criteria were rewritten"),
        GraphNode("M_escalate", "measure",
                  label="The characteristic cannot be judged by eye at all; the project "
                        "escalates to an instrumented check"),
        GraphNode("M_pchart", "measure", methods=("control_chart.p",),
                  produces=("pchart.outOfControl",),
                  label="Lot-by-lot reject share across the record"),
        GraphNode("A_special_cause", "analyze", methods=("control_chart.p",),
                  label="Special-cause investigation (the level is not one number yet)"),
        GraphNode("A_cap", "analyze", methods=("capability.binomial",),
                  produces=("cap.avgP",),
                  label="Where the reject share sits against the required level"),
        GraphNode("A_root_cause", "analyze", methods=("basic.two_proportions",),
                  produces=("rootcause.pValue",),
                  label="Root-cause analysis (the two placement heads compared)"),
        GraphNode("I_improve", "improve",
                  label="Improve (bring the outlying head onto the other's level)"),
        GraphNode("C_control", "control", methods=("control_chart.p",),
                  label="Control plan (attribute chart monitoring)"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_agree1"),
        GuardedEdge("M_agree1", "M_pchart", "agree1.kappaMin >= 0.60",
                    guard_fields=("agree1.kappaMin",)),
        GuardedEdge("M_agree1", "M_disagree", is_default=True),
        GuardedEdge("M_disagree", "M_agree2"),
        # THE RE-PROOF. The repaired judgement is not acceptable because it was repaired.
        GuardedEdge("M_agree2", "M_pchart", "agree2.kappaMin >= 0.60",
                    guard_fields=("agree2.kappaMin",)),
        GuardedEdge("M_agree2", "M_escalate", is_default=True),
        GuardedEdge("M_pchart", "A_cap", "pchart.outOfControl == 0",
                    guard_fields=("pchart.outOfControl",)),
        GuardedEdge("M_pchart", "A_special_cause", is_default=True),
        GuardedEdge("A_cap", "C_control", "cap.avgP <= 0.02", guard_fields=("cap.avgP",)),
        GuardedEdge("A_cap", "A_root_cause", is_default=True),
        GuardedEdge("A_special_cause", "C_control"),
        GuardedEdge("A_root_cause", "I_improve"),
        GuardedEdge("I_improve", "C_control"),
    ),
)

GATE_POLICY = (
    {"stage": "M_disagree", "requires": "M_agree1", "unlock_when": "agree1.kappaMin < 0.60",
     "rule": "the disagreement breakdown is only owed once the judgement has been found "
             "unusable"},
    {"stage": "M_agree2", "requires": "M_disagree",
     "rule": "the study is only re-run once what the judgements split on has been established"},
    {"stage": "M_pchart", "requires": ["M_agree1", "M_agree2"],
     "rule": "nothing is charted until a judgement study has come back acceptable"},
    {"stage": "A_cap", "requires": "M_pchart", "unlock_when": "pchart.outOfControl == 0",
     "rule": "a reject share is only one number once the run is stable "
             "(Montgomery ISQC 6e 7.2)"},
    {"stage": "A_special_cause", "requires": "M_pchart", "unlock_when": "pchart.outOfControl > 0",
     "rule": "special-cause work only once the run is shown to be unstable"},
    {"stage": "A_root_cause", "requires": "A_cap", "unlock_when": "cap.avgP > 0.02",
     "rule": "root-cause work is only owed while the share misses the required level"},
)

NODE_DATA = {"D_scope": "define", "M_agree1": "study_1", "M_disagree": "disagreements",
             "M_agree2": "study_2", "M_pchart": "lots", "A_special_cause": "lots",
             "A_cap": "lots", "A_root_cause": "heads"}

SHAPES = {0: "study-1-ok/meets-level",
          1: "study-1-ok/misses-level",
          2: "study-1-fails/repair-holds/misses-level",
          3: "study-1-fails/repair-fails",
          4: "study-1-ok/out-of-control",
          5: "study-1-fails/repair-holds/meets-level"}

_STUDY1_FAILS = {2, 3, 5}


def _draw(rng, p, n, k):
    return [sum(1 for _ in range(n) if rng.random() < p) for _ in range(k)]


def _disagreement_counts(rng, dominant_share=0.46, total=90):
    """Disagreements tallied by reject category, drawn (never asserted) from one dominant one."""
    weights = [dominant_share] + [(1.0 - dominant_share) / (len(_CATEGORIES) - 1)] * (
        len(_CATEGORIES) - 1)
    counts = {c: 0 for c in _CATEGORIES}
    for _ in range(total):
        u, acc = rng.random(), 0.0
        for cat, w in zip(_CATEGORIES, weights):
            acc += w
            if u <= acc:
                counts[cat] += 1
                break
    return counts


def generate(seed: int):
    shape = seed if seed in SHAPES else seed % 4
    rng = random.Random(seed * 1_000_003 + 20260909)
    a1rng = random.Random(seed * 7_919 + 20260913)
    a2rng = random.Random(seed * 7_919 + 20260917)

    if shape in _STUDY1_FAILS:
        study1, s1 = _fixtures.attribute_agreement_study(
            a1rng, error_rate=0.22, window=(0.25, 0.55))
    else:
        study1, s1 = _fixtures.attribute_agreement_study(
            a1rng, error_rate=0.04, window=(0.72, 0.95))

    if shape == 3:            # the rewrite does not rescue the judgement
        study2, s2 = _fixtures.attribute_agreement_study(
            a2rng, error_rate=0.19, window=(0.30, 0.58))
    else:
        study2, s2 = _fixtures.attribute_agreement_study(
            a2rng, error_rate=0.02, window=(0.85, 1.00))

    for _ in range(600):
        if shape in (0, 5):                     # inside the required level
            defects = _draw(rng, 0.0135, _N_LOT, _K)
            heads = {"events1": 54, "trials1": 3000, "events2": 47, "trials2": 3000}
        elif shape in (1, 2):                   # above the required level, one head worse
            defects = _draw(rng, 0.0330, _N_LOT, _K)
            heads = {"events1": 128, "trials1": 3000, "events2": 74, "trials2": 3000}
        elif shape == 4:                        # a single lot blows the limits
            defects = _draw(rng, 0.0140, _N_LOT, _K)
            defects[_K // 2] = 38
            heads = {"events1": 56, "trials1": 3000, "events2": 49, "trials2": 3000}
        else:                                   # 3: the record never gets looked at
            defects = _draw(rng, 0.0140, _N_LOT, _K)
            heads = {"events1": 56, "trials1": 3000, "events2": 49, "trials2": 3000}
        sizes = [_N_LOT] * _K

        ooc = int(verifiers.control_chart_p(
            {"defectCounts": defects, "subgroupSizes": sizes})["outOfControlCount"])
        binom = verifiers.capability_binomial(
            {"defectCounts": defects, "subgroupSizes": sizes})
        avg_p = round(float(binom["avgP"]), 6)

        ok = {
            0: ooc == 0 and avg_p <= _TARGET_P,
            1: ooc == 0 and avg_p > _TARGET_P,
            2: ooc == 0 and avg_p > _TARGET_P,
            3: True,
            4: ooc > 0,
            5: ooc == 0 and avg_p <= _TARGET_P,
        }[shape]
        if not ok:
            continue

        counts = _disagreement_counts(random.Random(seed * 104_729 + 20260919))
        blocks = {
            "define": {"goal": "hold the reject share at or below the required level and keep "
                               "the level steady",
                       "required_reject_share": _TARGET_P},
            "study_1": dict(study1),
            "disagreements": {"counts": dict(counts),
                              "note": "items on which an inspector's call differed from the "
                                      "answer key, tallied by the category the item was "
                                      "rejected under"},
            "study_2": dict(study2),
            "lots": {"defectCounts": list(defects), "subgroupSizes": list(sizes),
                     "required_reject_share": _TARGET_P},
            "heads": dict(heads),
        }
        res = {
            "agree1": dict(s1),
            "agree2": dict(s2),
            "disagree": {"topCategoryPct": round(
                float(verifiers.pareto({"counts": counts})["topCategoryPct"]), 4)},
            "pchart": {"outOfControl": ooc},
            "cap": {"avgP": avg_p, "processZ": round(float(binom["processZ"]), 4),
                    "required": _TARGET_P},
            "rootcause": {"pValue": round(float(
                verifiers.two_proportions(heads)["pValue"]), 5)},
            "_shape": SHAPES[shape],
        }
        return blocks, res

    raise RuntimeError(f"placement_agreement: could not realise shape {shape} for seed {seed}")


CASE = V2Case(
    case_id="adb_c33",
    title="A visual accept/reject judgement, repaired and put to the test again",
    industry="electronics",
    y_type="attribute_proportion",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    seeds=(0, 1, 2, 3, 4, 5),
    shapes=dict(SHAPES), node_data=NODE_DATA,
    fault_targets=(("M_disagree", "quality.pareto",
                    "the item-by-item disagreement tally was checked and is genuinely not "
                    "on file"),),
    budget={"max_turns": 26},
    context=(
        "We are the improvement team on an electronic-assembly line. Boards are accepted or "
        "rejected by eye at final inspection, and the line is required to hold the reject share "
        "at or below 2%. The archive holds the inspected and rejected counts for twenty-five "
        "consecutive lots, a study in which several inspectors judged the same retained boards "
        "against an agreed answer key, a tally of the items those inspectors called differently "
        "from the key broken out by the category the item was rejected under, a second study "
        "run on retained boards after the accept/reject criteria were rewritten, and one "
        "window's rejected and placed counts for each of the two placement heads."),
    goal=(
        "Work through the batches the data steward will release and report where this project "
        "stands: whether an accept/reject call can be relied on, what had to happen before it "
        "could be, whether the reject share has held steady across the lots, how today's level "
        "compares with what the line is required to hold, and what should be done next. Every "
        "number in your report must come from a computation you ran on this task; where "
        "something could not be computed, say so rather than inventing it."),
    blocks_meta={
        "define": {"label": "Project charter and the required reject level", "phase": "define",
                   "topics": ("charter", "required level", "improvement target")},
        "study_1": {"label": "Inspector judgements of retained boards against the answer key",
                    "phase": "measure", "topics": ("inspector judgements", "answer key")},
        "disagreements": {"label": "Items called differently from the key, by reject category",
                          "phase": "measure",
                          "topics": ("disagreement tally", "reject categories")},
        "study_2": {"label": "A second study on retained boards after the criteria were "
                             "rewritten", "phase": "measure",
                    "topics": ("second study", "rewritten criteria")},
        "lots": {"label": "Per-lot inspected and rejected counts", "phase": "measure",
                 "topics": ("lot record", "boards inspected per lot", "lot order")},
        "heads": {"label": "Placed and rejected counts for each placement head", "phase":
                  "analyze", "topics": ("placement heads", "head by head")},
    },
    field_map={
        # Both studies run the SAME method. Pinned to their invocation, because the default
        # last-wins merge would let the repaired study answer for the original one.
        "agree1.kappaMin": ({"method_id": "msa.attribute_agreement", "output": "kappaMin",
                             "scale": 1.0, "occurrence": 0},),
        "agree2.kappaMin": ({"method_id": "msa.attribute_agreement", "output": "kappaMin",
                             "scale": 1.0, "occurrence": 1},),
        "disagree.topCategoryPct": ({"method_id": "quality.pareto", "output": "topCategoryPct",
                                     "scale": 1.0},),
        "pchart.outOfControl": ({"method_id": "control_chart.p", "output": "outOfControlCount",
                                 "scale": 1.0},
                                {"method_id": "control_chart.laney_p", "output": "flaggedCount",
                                 "scale": 1.0}),
        # The average defective share is Sigma d / Sigma n, which is also the p chart's centre
        # line. A contestant that read it there computed it; listing only one producer made that
        # a fabrication.
        "cap.avgP": ({"method_id": "capability.binomial", "output": "avgP", "scale": 1.0},
                     {"method_id": "control_chart.p", "output": "centerLine", "scale": 1.0},),
        "cap.processZ": ({"method_id": "capability.binomial", "output": "processZ",
                          "scale": 1.0},),
        "rootcause.pValue": ({"method_id": "basic.two_proportions", "output": "pValue",
                              "scale": 1.0},),
    },
    truth_fields=(
        # `node` scopes these to the study that actually happened. Both are produced by the
        # same method, so the method-level filter publishes both on every seed; on a seed whose
        # first study passes there IS no second study, and the unscoped truth claimed the first
        # study's kappa against the second's expected value.
        {"field": "agree1.kappaMin", "method_id": "msa.attribute_agreement", "node": "M_agree1",
         "output": "kappaMin", "scale": 1.0, "tol": 0.01},
        {"field": "agree2.kappaMin", "method_id": "msa.attribute_agreement", "node": "M_agree2",
         "output": "kappaMin", "scale": 1.0, "tol": 0.01},
        {"field": "disagree.topCategoryPct", "method_id": "quality.pareto",
         "output": "topCategoryPct", "scale": 1.0, "tol": 0.05},
        {"field": "pchart.outOfControl", "method_id": "control_chart.p",
         "output": "outOfControlCount", "scale": 1.0, "tol": 0.0},
        {"field": "cap.avgP", "method_id": "capability.binomial",
         "output": "avgP", "scale": 1.0, "tol": 0.0001},
        {"field": "cap.processZ", "method_id": "capability.binomial",
         "output": "processZ", "scale": 1.0, "tol": 0.02},
        {"field": "rootcause.pValue", "method_id": "basic.two_proportions",
         "output": "pValue", "scale": 1.0, "tol": 0.002},
    ),
)

if __name__ == "__main__":
    for s in CASE.seeds:
        _, r = generate(s)
        print(f"seed {s} [{r['_shape']:42s}] k1={r['agree1']['kappaMin']:.3f} "
              f"k2={r['agree2']['kappaMin']:.3f} ooc={r['pchart']['outOfControl']} "
              f"avgP={r['cap']['avgP']:.5f}\n    {' -> '.join(walk(GRAPH, r))}")
