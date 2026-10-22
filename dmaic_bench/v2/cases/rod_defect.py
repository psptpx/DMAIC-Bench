"""rod_defect — appearance defects on a high-speed rod-making line, judged unit by unit.

Onboarded from a black-belt project in a continuous-process plant: the scenario, the inspection
regime and the failure modes are drawn from that work; the data is generated from the seed and
the case names nobody.

Two things in this project are not in any other case in this corpus.

**The requirement arrives in DPMO and the record arrives in counts.** The charter commits the
line to no more than 1500 defective units per million. The batch the steward releases is a
per-lot inspected count and a per-lot defective count. Nothing converts one into the other for
the contestant, and the gate that decides whether this project is finished or has work left to
do sits exactly on that conversion: 1500 DPMO is 0.0015, and a defective share of 0.0026 is
above it however small it looks written down. The source project got this wrong in the other
direction -- percent was entered where a proportion was expected and a genuinely capable
process was reported at 133060 PPM against a true 1331 -- which is why the conversion is the
gate rather than a footnote.

**The follow-up question is asked of attribute data.** When the share misses the requirement,
the next question is whether it is the same on every machine. On a defective/inspected count
that is a contingency table, not a means comparison: four machines against two outcomes. A
contestant who reaches for a means test here is answering a question this batch cannot support.
Where the table says the machines differ, the project has something to improve; where it says
they do not, the honest finding is that the recorded factors do not explain the level and the
project owes itself another pass at identifying what does -- a terminal that is a real result,
not a failure to finish.
"""
from __future__ import annotations

import random

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import verifiers
from dmaic_bench.v2.cases import _fixtures
from dmaic_bench.v2.models import V2Case

#: The charter's commitment, as it is written in the charter: defective units per million.
_REQUIREMENT_DPMO = 1500
_REQUIREMENT_P = _REQUIREMENT_DPMO / 1_000_000.0     # 0.0015 -- what the guard compares against

_K = 25            # lots in the record
_N_LOT = 5000      # units inspected per lot

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define", methods=("quality.pareto",),
                  produces=("scope.topCategoryPct",),
                  label="Scope: which reject category this project is about"),
        GraphNode("D_stratify", "define", methods=("quality.fmea_rpn",),
                  produces=("stratify.maxRpn",),
                  label="No category dominates; rank the candidate failure modes by risk and "
                        "scope to the worst of them"),
        GraphNode("M_agree", "measure", methods=("msa.attribute_agreement",),
                  produces=("agree.kappaMin",),
                  label="Inspector judgements against the retained answer key"),
        GraphNode("M_agree_fix", "measure",
                  label="Rewrite the accept/reject criteria and re-run the study "
                        "(judgements cannot support any downstream conclusion)"),
        GraphNode("M_pchart", "measure", methods=("control_chart.p",),
                  produces=("pchart.outOfControl",),
                  label="Lot-by-lot defective share across the record"),
        GraphNode("A_special_cause", "analyze", methods=("control_chart.p",),
                  label="Special-cause investigation (the level is not one number yet)"),
        GraphNode("A_cap", "analyze", methods=("capability.binomial",),
                  produces=("cap.avgP",),
                  label="Where the defective share sits against the commitment"),
        GraphNode("A_machine", "analyze", methods=("tables.chisquare_assoc",),
                  produces=("machine.pValue",),
                  label="Is the share the same on every machine?"),
        GraphNode("A_more_x", "analyze",
                  label="The recorded factors do not account for the level; return to "
                        "identifying candidate causes, and monitor meanwhile"),
        GraphNode("I_improve", "improve", methods=("basic.two_proportions",),
                  produces=("improve.pValue",),
                  label="Improve: the outlying machine before and after the change"),
        GraphNode("C_route", "control",
                  label="Control plan: which chart sustains the gain?"),
        GraphNode("C_control", "control", methods=("control_chart.p",),
                  produces=("sustain.outOfControl",),
                  label="Sustaining chart, constant inspected count"),
        GraphNode("C_laney", "control", methods=("control_chart.laney_p",),
                  produces=("sustain.outOfControl",),
                  label="Sustaining chart, inspected count varies period to period"),
    ),
    edges=(
        # DEFINE IS A DECISION, not a preamble. A project scopes to one dominant category or,
        # when the tally is diffuse, stratifies before it scopes -- the Pareto step every DMAIC
        # charter begins with. Before this, Define released a batch nobody had to compute
        # anything from: 95 of 95 routes passed through it and it graded nothing at all.
        GuardedEdge("D_scope", "M_agree", "scope.topCategoryPct >= 50",
                    guard_fields=("scope.topCategoryPct",)),
        GuardedEdge("D_scope", "D_stratify", is_default=True),
        GuardedEdge("D_stratify", "M_agree"),
        GuardedEdge("M_agree", "M_pchart", "agree.kappaMin >= 0.60",
                    guard_fields=("agree.kappaMin",)),
        GuardedEdge("M_agree", "M_agree_fix", is_default=True),
        GuardedEdge("M_pchart", "A_cap", "pchart.outOfControl == 0",
                    guard_fields=("pchart.outOfControl",)),
        GuardedEdge("M_pchart", "A_special_cause", is_default=True),
        # THE CONVERSION GATE. 1500 DPMO is 0.0015; the batch reports counts.
        GuardedEdge("A_cap", "C_route", "cap.avgP <= 0.0015", guard_fields=("cap.avgP",)),
        GuardedEdge("A_cap", "A_machine", is_default=True),
        GuardedEdge("A_machine", "I_improve", "machine.pValue < 0.05",
                    guard_fields=("machine.pValue",)),
        GuardedEdge("A_machine", "A_more_x", is_default=True),
        # A project that cannot name the cause still puts monitoring in place. Semantically
        # right, and it is also what makes the fork above readable: with A_more_x terminal, the
        # sustaining chart downstream of I_improve was the only evidence either branch had, and
        # that chart's method already ran back at the lot record.
        GuardedEdge("A_more_x", "C_route"),
        GuardedEdge("A_special_cause", "C_route"),
        GuardedEdge("I_improve", "C_route"),
        # The sustaining chart family is fixed by the monitoring record, not by preference: a
        # constant inspected count takes the ordinary p chart, a varying one takes the
        # variable-limit form. Control used to be a terminal node with a method nothing
        # required -- it graded nothing on any of the 62 routes that reached it.
        GuardedEdge("C_route", "C_control", "sustain.varyingN == 0",
                    guard_fields=("sustain.varyingN",)),
        GuardedEdge("C_route", "C_laney", is_default=True),
    ),
)

GATE_POLICY = (
    {"stage": "M_pchart", "requires": "M_agree", "unlock_when": "agree.kappaMin >= 0.60",
     "rule": "the accept/reject judgement must be shown repeatable before anything is charted"},
    {"stage": "M_agree_fix", "requires": "M_agree", "unlock_when": "agree.kappaMin < 0.60",
     "rule": "criteria remediation only once the judgement has been found unusable"},
    {"stage": "A_cap", "requires": "M_pchart", "unlock_when": "pchart.outOfControl == 0",
     "rule": "a defective share is only one number once the run is stable "
             "(Montgomery ISQC 6e 7.2)"},
    {"stage": "A_special_cause", "requires": "M_pchart", "unlock_when": "pchart.outOfControl > 0",
     "rule": "special-cause work only once the run is shown to be unstable"},
    {"stage": "A_machine", "requires": "A_cap", "unlock_when": "cap.avgP > 0.0015",
     "rule": "the machine comparison is only owed while the share misses the commitment"},
    {"stage": "I_improve", "requires": "A_machine", "unlock_when": "machine.pValue < 0.05",
     "rule": "no change is made to a machine until the tally says that machine is different"},
    {"stage": "C_route", "requires": "M_pchart",
     "rule": "a sustaining chart is chosen for a process whose behaviour is already known"},
)

NODE_DATA = {"D_scope": "candidates", "D_stratify": "failure_modes",
             "M_agree": "agreement", "M_pchart": "lots",
             "C_route": "sustaining", "C_control": "sustaining", "C_laney": "sustaining",
             "A_special_cause": "lots", "A_cap": "lots", "A_machine": "machines",
             # I_improve carries its own POST-change batch. Without it the fork below it is
             # invisible to scoring: both branches out of A_machine would run nothing that the
             # other does not, and a contestant that walked either one would look identical.
             "I_improve": "after_change"}

#: seed -> whether the monitoring record's inspected count varies period to period. A property
#: of how the line was sampled after the change, not of how well it performs, so it is drawn
#: independently of the shape that decides the rest of the route.
_SUSTAIN_VARIES = {1, 3, 5}

SHAPES = {0: "meets-commitment",
          1: "misses-commitment/machine-differs",
          2: "misses-commitment/machines-alike",
          3: "out-of-control",
          4: "inspector-disagreement",
          5: "misses-commitment/machines-alike"}


def _pchart_ooc(defects, sizes) -> int:
    """Subgroups outside 3-sigma variable-width P-chart limits (Montgomery ISQC 6e 7.2)."""
    return int(verifiers.control_chart_p(
        {"defectCounts": list(defects), "subgroupSizes": list(sizes)})["outOfControlCount"])


def _draw(rng, p, n, k):
    return [sum(1 for _ in range(n) if rng.random() < p) for _ in range(k)]


def _machine_table(rng, rates, per_machine=4000):
    """A defective/sound contingency table drawn at the given per-machine true rates."""
    rows = []
    for r in rates:
        d = sum(1 for _ in range(per_machine) if rng.random() < r)
        rows.append([d, per_machine - d])
    return rows


def generate(seed: int):
    shape = SHAPES_INDEX.get(seed, seed % 4)
    rng = random.Random(seed * 1_000_003 + 20260909)
    arng = random.Random(seed * 7_919 + 20260911)
    if shape == 4:
        agree_block, agree_stats = _fixtures.attribute_agreement_study(
            arng, error_rate=0.22, window=(0.25, 0.55))
    else:
        agree_block, agree_stats = _fixtures.attribute_agreement_study(
            arng, error_rate=0.04, window=(0.72, 0.95))

    # The Define batch: which reject category the project is about. A dominant category scopes
    # the project; a diffuse tally means stratifying first.
    prng = random.Random(seed * 15_485_863 + 20260953)
    dominant = 0.62 if shape in (0, 1, 3) else 0.33
    cats = ("loose end", "soft spot", "off-weight", "seam split", "stain")
    weights = [dominant] + [(1 - dominant) / (len(cats) - 1)] * (len(cats) - 1)
    tally = {c: 0 for c in cats}
    for _ in range(240):
        u, acc = prng.random(), 0.0
        for c, w in zip(cats, weights):
            acc += w
            if u <= acc:
                tally[c] += 1
                break
    top_pct = round(float(verifiers.pareto({"counts": tally})["topCategoryPct"]), 4)

    # What a diffuse tally sends the project to: the candidate failure modes, ranked by risk.
    modes = []
    for name in cats:
        modes.append({"mode": name,
                      "severity": prng.randint(4, 9), "occurrence": prng.randint(2, 8),
                      "detection": prng.randint(2, 8)})
    fmea = verifiers.fmea_rpn({"items": modes})

    # The Control batch: the record the line is monitored on after the change. Its inspected
    # count either holds constant or varies, and that fixes the sustaining chart family.
    srng = random.Random(seed * 32_452_843 + 20260957)
    varies = seed in _SUSTAIN_VARIES
    s_sizes = ([int(srng.choice([3200, 4100, 5000, 5800, 6400])) for _ in range(20)] if varies
               else [_N_LOT] * 20)
    s_defects = [sum(1 for _ in range(n) if srng.random() < 0.0012) for n in s_sizes]
    sustain_stats = verifiers.control_chart_laney_p(
        {"defectCounts": s_defects, "subgroupSizes": s_sizes}) if varies else \
        verifiers.control_chart_p({"defectCounts": s_defects, "subgroupSizes": s_sizes})
    sustain_ooc = int(sustain_stats.get("flaggedCount", sustain_stats.get("outOfControlCount", 0)))

    for _ in range(600):
        if shape == 0:                                   # comfortably inside 1500 DPMO
            sizes = [_N_LOT] * _K
            defects = _draw(rng, 0.00105, _N_LOT, _K)
            rates = [0.0011, 0.0012, 0.0010, 0.0011]
        elif shape == 1:                                 # above the commitment, one machine worse
            sizes = [_N_LOT] * _K
            defects = _draw(rng, 0.00260, _N_LOT, _K)
            rates = [0.0018, 0.0052, 0.0019, 0.0017]
        elif shape == 3:                                 # a single lot blows the limits
            sizes = [_N_LOT] * _K
            defects = _draw(rng, 0.00110, _N_LOT, _K)
            defects[_K // 2] = 42
            rates = [0.0011, 0.0012, 0.0010, 0.0011]
        elif shape == 4:                                 # the record is ordinary; judgement is not
            sizes = [_N_LOT] * _K
            defects = _draw(rng, 0.00110, _N_LOT, _K)
            rates = [0.0011, 0.0012, 0.0010, 0.0011]
        else:                                            # 2: above the commitment, machines alike
            sizes = [_N_LOT] * _K
            defects = _draw(rng, 0.00260, _N_LOT, _K)
            rates = [0.0026, 0.0027, 0.0025, 0.0026]

        table = _machine_table(rng, rates)
        # The outlying machine before the change and after it, on equal inspected counts. Drawn
        # at the same true rate on every shape where the machines are alike, so this batch never
        # hints at which branch the tally will call for.
        worst = max(range(len(rates)), key=lambda i: rates[i])
        before_r = rates[worst]
        after_r = min(before_r, sum(rates) / len(rates)) if before_r > 1.5 * (
            sum(rates) / len(rates)) else before_r
        n_after = 4000
        before_d = sum(1 for _ in range(n_after) if rng.random() < before_r)
        after_d = sum(1 for _ in range(n_after) if rng.random() < after_r)
        ooc = _pchart_ooc(defects, sizes)
        binom = verifiers.capability_binomial(
            {"defectCounts": list(defects), "subgroupSizes": list(sizes)})
        avg_p = round(float(binom["avgP"]), 6)
        chi = verifiers.chisquare_assoc({"table": table})
        chi_p = round(float(chi["pValue"]), 5)

        ok = {
            0: ooc == 0 and avg_p <= _REQUIREMENT_P,
            1: ooc == 0 and avg_p > _REQUIREMENT_P and chi_p < 0.01,
            2: ooc == 0 and avg_p > _REQUIREMENT_P and chi_p > 0.20,
            3: ooc > 0,
            4: ooc == 0 and agree_stats["kappaMin"] < 0.60,
        }[shape]
        if not ok:
            continue

        blocks = {
            "define": {"goal": "hold appearance defects at or below the committed level and "
                               "keep the level steady",
                       "requirement_dpmo": _REQUIREMENT_DPMO,
                       "unit": "defective units per million inspected"},
            "agreement": dict(agree_block),
            "lots": {"defectCounts": list(defects), "subgroupSizes": list(sizes),
                     "requirement_dpmo": _REQUIREMENT_DPMO},
            "after_change": {"events1": before_d, "trials1": n_after,
                             "events2": after_d, "trials2": n_after,
                             "groupLabels": ["before the change", "after the change"]},
            "candidates": {"counts": dict(tally),
                           "goal": "hold appearance defects at or below the committed level",
                           "requirement_dpmo": _REQUIREMENT_DPMO,
                           "unit": "defective units per million inspected"},
            "failure_modes": {"items": [dict(m) for m in modes],
                              "note": "severity, occurrence and detection ratings recorded for "
                                      "each candidate failure mode"},
            "sustaining": {"defectCounts": list(s_defects), "subgroupSizes": list(s_sizes),
                           "note": "the monitoring record kept since the change"},
            "machines": {"table": [list(r) for r in table],
                         "rowLabels": ["machine 1", "machine 2", "machine 3", "machine 4"],
                         "columnLabels": ["defective", "sound"]},
        }
        res = {"agree": dict(agree_stats),
               "pchart": {"outOfControl": ooc},
               "cap": {"avgP": avg_p, "processZ": round(float(binom["processZ"]), 4),
                       "requirementDpmo": _REQUIREMENT_DPMO},
               "machine": {"pValue": chi_p,
                           "statistic": round(float(chi["statistic"]), 4)},
               "improve": {"pValue": round(float(verifiers.two_proportions(
                   {"events1": before_d, "trials1": n_after,
                    "events2": after_d, "trials2": n_after})["pValue"]), 5)},
               "scope": {"topCategoryPct": top_pct},
               "stratify": {"maxRpn": round(float(fmea["maxRpn"]), 4)},
               "sustain": {"varyingN": 1 if varies else 0, "outOfControl": sustain_ooc},
               "_shape": SHAPES[shape]}
        return blocks, res

    raise RuntimeError(f"rod_defect: could not realise shape {shape} for seed {seed}")


#: seed -> shape for the seeds that are not ``seed % 4`` (a table rather than a wider modulus,
#: so a shape can be given a second seed without renumbering the others).
SHAPES_INDEX = {4: 4, 5: 2}


CASE = V2Case(
    case_id="adb_c32",
    title="Holding an appearance-defect level against a committed rate",
    industry="process_industry",
    y_type="attribute_proportion",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    seeds=(0, 1, 2, 3, 4, 5),
    shapes=dict(SHAPES), node_data=NODE_DATA,
    fault_targets=(("M_agree", "msa.attribute_agreement",
                    "the inspector-by-inspector judgement sheets for this study were checked "
                    "and are genuinely not on file"),),
    budget={"max_turns": 22},
    context=(
        "We are the improvement team on a high-speed rod-making line. Every unit leaving the "
        "line is judged sound or defective on appearance, and the charter commits us to no "
        "more than 1500 defective units per million inspected. The archive holds the inspected "
        "and defective counts for twenty-five consecutive lots, a study in which several "
        "inspectors judged the same retained units against an agreed answer key, and a "
        "machine-by-machine tally of defective and sound units over one common window, and "
        "one machine's inspected and defective counts either side of a change that was made "
        "to it."),
    goal=(
        "Work through the batches the data steward will release and report where this project "
        "stands: whether a sound/defective judgement can be relied on at all, whether the "
        "defective share has held steady across the lots, how today's level compares with what "
        "the charter commits us to, and what should be done next. Every number in your report "
        "must come from a computation you ran on this task; where something could not be "
        "computed, say so rather than inventing it."),
    blocks_meta={
        "candidates": {"label": "Reject categories tallied for the charter", "phase": "define",
                       "topics": ("charter", "reject categories", "committed level")},
        "failure_modes": {"label": "Candidate failure modes with their risk ratings",
                          "phase": "define",
                          "topics": ("failure modes", "risk ratings")},
        "sustaining": {"label": "The monitoring record kept since the change", "phase": "control",
                       "topics": ("monitoring record", "since the change")},
        "agreement": {"label": "Inspector judgements of retained units against the answer key",
                      "phase": "measure", "topics": ("inspector judgements", "answer key")},
        "lots": {"label": "Per-lot inspected and defective counts", "phase": "measure",
                 "topics": ("lot record", "inspected units per lot", "lot order")},
        "machines": {"label": "Machine-by-machine defective and sound tally", "phase": "analyze",
                     "topics": ("machine tally", "machine by machine")},
        "after_change": {"label": "One machine's inspected and defective counts either side of "
                                  "a change", "phase": "improve",
                         "topics": ("before and after a change", "the change trial")},
    },
    field_map={
        "agree.kappaMin": ({"method_id": "msa.attribute_agreement", "output": "kappaMin",
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
        "machine.pValue": ({"method_id": "tables.chisquare_assoc", "output": "pValue",
                            "scale": 1.0},),
        "improve.pValue": ({"method_id": "basic.two_proportions", "output": "pValue",
                            "scale": 1.0},),
        "scope.topCategoryPct": ({"method_id": "quality.pareto", "output": "topCategoryPct",
                                  "scale": 1.0},),
        "stratify.maxRpn": ({"method_id": "quality.fmea_rpn", "output": "maxRpn",
                             "scale": 1.0},),
        # `sustain.outOfControl` is deliberately ABSENT. It is a published truth and not a
        # guard field -- the Control fork turns on `sustain.varyingN`, a structural reading of
        # the batch -- and mapping it here would have put a second `control_chart.p` producer
        # in the table. `merged_outputs` is last-wins, so the sustaining chart's count silently
        # overwrote the lot record's and the Self-Consistency re-walk took the in-control branch
        # on a seed whose record is out of control. A field_map entry is for routing; a truth is
        # for numbers.
    },
    batch_facts={
        # Structural: does the monitoring record's inspected count vary? No method reports it;
        # an analyst reads it off the batch, and the sustaining chart family follows from it.
        "sustain.varyingN": {"node": "C_route", "key": "subgroupSizes", "kind": "varies"},
    },
    truth_fields=(
        {"field": "agree.kappaMin", "method_id": "msa.attribute_agreement",
         "output": "kappaMin", "scale": 1.0, "tol": 0.01},
        {"field": "pchart.outOfControl", "method_id": "control_chart.p",
         "output": "outOfControlCount", "scale": 1.0, "tol": 0.0},
        {"field": "cap.avgP", "method_id": "capability.binomial",
         "output": "avgP", "scale": 1.0, "tol": 0.0001},
        {"field": "cap.processZ", "method_id": "capability.binomial",
         "output": "processZ", "scale": 1.0, "tol": 0.02},
        {"field": "machine.pValue", "method_id": "tables.chisquare_assoc",
         "output": "pValue", "scale": 1.0, "tol": 0.002},
        {"field": "improve.pValue", "method_id": "basic.two_proportions",
         "output": "pValue", "scale": 1.0, "tol": 0.002},
        {"field": "scope.topCategoryPct", "method_id": "quality.pareto", "node": "D_scope",
         "output": "topCategoryPct", "scale": 1.0, "tol": 0.05},
        {"field": "stratify.maxRpn", "method_id": "quality.fmea_rpn", "node": "D_stratify",
         "output": "maxRpn", "scale": 1.0, "tol": 0.0},
        {"field": "sustain.outOfControl", "method_id": "control_chart.p", "node": "C_control",
         "output": "outOfControlCount", "scale": 1.0, "tol": 0.0},
        {"field": "sustain.outOfControl", "method_id": "control_chart.laney_p",
         "node": "C_laney", "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
    ),
)

if __name__ == "__main__":
    for s in CASE.seeds:
        _, r = generate(s)
        print(f"seed {s} [{r['_shape']:34s}] kappa={r['agree']['kappaMin']:.3f} "
              f"ooc={r['pchart']['outOfControl']} avgP={r['cap']['avgP']:.5f} "
              f"chiP={r['machine']['pValue']:.4f}\n    {' -> '.join(walk(GRAPH, r))}")
