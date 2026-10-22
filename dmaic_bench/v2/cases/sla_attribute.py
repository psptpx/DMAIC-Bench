"""sla_attribute — a data-conditioned ATTRIBUTE/proportion DMAIC project (v2).

Domain: a service desk (or QA line) tracks the per-subgroup DEFECTIVE-UNIT / SLA-BREACH rate.
The unit of analysis is a proportion p = defects / subgroup_size, one point per subgroup. ONE
decision graph; `seed % 4` drives the statistical shape so four seeds walk four distinct
oracle-correct routes.

Attribute-data forks (the analogue of injection_molding's normality/stability forks):

  shape 0  constant subgroup size · in-control · MEETS target rate
             → p-chart is the right control chart; process is stable and already at/below the
               target breach rate → binomial capability confirms it → straight to Control.
  shape 1  constant subgroup size · in-control · MISSES target rate
             → stable but the breach rate is too high → capability route flags it → root-cause
               (compare two operators / periods with a two-proportions test) → improve → Control.
  shape 2  VARYING subgroup size · in-control
             → constant-n p-chart is inappropriate; varying n routes to a Laney-P′ / U-chart
               style analysis (variable-limits attribute chart) → then capability → root-cause.
  shape 3  constant subgroup size · OUT-of-control (special cause)
             → an out-of-control attribute process cannot be assessed for capability; the correct
               move is special-cause investigation, NOT computing a binomial Z (Montgomery ISQC
               6e §7.2 — capability presumes a stable process). Data forks away from capability.
  shape 4  APPRAISERS DISAGREE WITH THE STANDARD
             → kappa against the standard is below the acceptance limit, so a "breach / no breach"
               judgement is not repeatable and nothing computed FROM those judgements means
               anything (AIAG MSA-4 §III-C). The correct move is to fix the judgement criteria
               and re-run the study; the chart, the capability and the team comparison are all
               downstream of a measurement that does not work, and the project stops here.

WHY SHAPE 4 NEEDED A NEW NODE. The disagreement branch used to be the self-loop
``M_agree -> M_agree``, which ``walk`` (cycle-guarded) terminates ON the fork, so
``branch_decisions`` never records the decision and ``harbor_truth.branch_evidence`` excludes it
by rule. The fork was unmeasurable no matter what the data did. It now leads to a real node with
no batch: stopping IS the finding.

Every routing field in `oracle_results` is COMPUTED from the generated data. Where a REAL verifier
exists (`capability.binomial`, `basic.two_proportions`) it is used; the p-chart out-of-control
count and the subgroup-size-variation flag have no verifier, so they are computed INLINE with the
standard textbook formula (documented below), exactly as poc_project does for `_imr_out_of_control`.
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[3])
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.graph import (DecisionGraph, GraphNode,  # noqa: E402
                                        GuardedEdge, walk)
from dmaic_bench.truth import verifiers  # noqa: E402
from dmaic_bench.v2.cases import _fixtures
from dmaic_bench.v2.cases import _fixtures as _f
from dmaic_bench.v2.models import V2Case  # noqa: E402

# Target breach/defective rate the project must hold the process at or below.
_TARGET_P = 0.05

# --------------------------------------------------------------------------- the decision graph

PROJECT_GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define", label="Scope: the SLA breach-rate problem and its target"),
        GraphNode("M_agree", "measure", methods=("msa.attribute_agreement",),
                  produces=("agree.kappaMin",), label="Attribute agreement analysis (appraiser against standard)"),
        GraphNode("M_agree_fix", "measure",
                  label="Rewrite the judging criteria and re-run the study (ratings cannot support any downstream conclusion)"),
        GraphNode("M_chart_route", "measure",
                  label="Chart route (is the subgroup size constant?)"),
        GraphNode("M_pchart", "measure", methods=("control_chart.p",),
                  produces=("pchart.outOfControl",),
                  label="P chart (constant subgroup size)"),
        # NO control_chart.u. This project's y is DEFECTIVES out of an inspected count, which is
        # binomial; the u chart is for defects per unit and cannot be computed from this batch at
        # all (it looks for `unitCounts`, which is not in it). Declaring it made the reference
        # solution miss a required method it had no way to run, and charged it for misuse.
        GraphNode("M_laney", "measure", methods=("control_chart.laney_p",),
                  produces=("pchart.outOfControl",),
                  label="Laney P' chart (varying subgroup size)"),
        GraphNode("A_special_cause", "analyze", methods=("control_chart.p",),
                  label="Special-cause investigation (capability does not apply)"),
        GraphNode("A_cap_binomial", "analyze", methods=("capability.binomial",),
                  produces=("cap.avgP",), label="Binomial capability (breach rate against target)"),
        GraphNode("A_root_cause", "analyze", methods=("basic.two_proportions",),
                  label="Root-cause analysis (two-proportion test across shift and period)"),
        GraphNode("I_improve", "improve", methods=("basic.two_proportions",),
                  label="Improve (reduce the dominant breach source)"),
        GraphNode("I_confirm", "improve", methods=("capability.binomial",),
                  label="Improvement confirmation (breach rate re-assessed)"),
        GraphNode("C_control", "control", methods=("control_chart.p",),
                  label="Control plan (attribute chart monitoring)"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_agree"),
        # MSA gate: an attribute study is meaningless if appraisers can't agree with the standard.
        GuardedEdge("M_agree", "M_chart_route", "agree.kappaMin >= 0.60",
                    guard_fields=("agree.kappaMin",)),
        # agreement fails → fix the judgement criteria; nothing downstream of it is meaningful.
        GuardedEdge("M_agree", "M_agree_fix", is_default=True),
        # Chart route: constant subgroup size → classic P chart; varying n → Laney-P′/U style.
        GuardedEdge("M_chart_route", "M_pchart", "chart.varyingN == 0",
                    guard_fields=("chart.varyingN",)),
        GuardedEdge("M_chart_route", "M_laney", is_default=True),
        # Stability gate (constant-n branch): out-of-control → special cause, not capability.
        GuardedEdge("M_pchart", "A_cap_binomial", "pchart.outOfControl == 0",
                    guard_fields=("pchart.outOfControl",)),
        GuardedEdge("M_pchart", "A_special_cause", is_default=True),
        # Varying-n branch: same stability gate.
        GuardedEdge("M_laney", "A_cap_binomial", "pchart.outOfControl == 0",
                    guard_fields=("pchart.outOfControl",)),
        GuardedEdge("M_laney", "A_special_cause", is_default=True),
        # Capability gate: at/below target rate → monitor; above target → improve.
        GuardedEdge("A_cap_binomial", "C_control", "cap.avgP <= 0.05",
                    guard_fields=("cap.avgP",)),
        GuardedEdge("A_cap_binomial", "A_root_cause", is_default=True),
        GuardedEdge("A_special_cause", "C_control"),
        GuardedEdge("A_root_cause", "I_improve"),
        GuardedEdge("I_improve", "I_confirm"),
        GuardedEdge("I_confirm", "C_control"),
    ),
)

# The methodology gates the environment enforces (conclusion-dependent unlocks).
GATE_POLICY = (
    {"stage": "M_chart_route", "requires": "M_agree", "unlock_when": "agree.kappaMin >= 0.60",
     "rule": "attribute agreement must be acceptable before any control chart"},
    {"stage": "M_agree_fix", "requires": "M_agree", "unlock_when": "agree.kappaMin < 0.60",
     "rule": "criteria remediation only once appraiser-to-standard agreement has been judged unacceptable"},
    {"stage": "A_cap_binomial", "requires": ["M_pchart", "M_laney"], "unlock_when": "pchart.outOfControl == 0",
     "rule": "binomial capability is not valid until the process is shown to be in control (Montgomery ISQC 6e 7.2)"},
    {"stage": "A_special_cause", "requires": ["M_pchart", "M_laney"], "unlock_when": "pchart.outOfControl > 0",
     "rule": "special-cause work only once the attribute run is shown to be unstable"},
    {"stage": "I_improve", "requires": "A_root_cause", "rule": "no improvement work until a root cause is confirmed"},
)

# Which staged data block each node consumes (what the steward hands out on arrival).
NODE_DATA = {
    "D_scope": "define", "M_agree": "agreement",
    "M_chart_route": "subgroups", "M_pchart": "subgroups", "M_laney": "subgroups",
    "A_special_cause": "subgroups", "A_cap_binomial": "subgroups",
    "A_root_cause": "root_cause",
    # NOTE the absence of I_improve / I_confirm. They are real obligations on the route, but this
    # project ships no POST-improvement batch: pointing them at the baseline batches made the
    # improvement step a re-run of the root-cause comparison and the confirmation a re-run of the
    # baseline capability, on the very data they are supposed to be compared against.
}


# --------------------------------------------------------------------------- inline statistics

def _pchart_out_of_control(defects, sizes) -> int:
    """Number of subgroups outside 3-sigma P-chart control limits.

    Standard Shewhart P chart (Montgomery ISQC 6e §7.2): centre line pbar = Σd / Σn; each
    subgroup i has its OWN limits (variable-width chart handles both constant and varying n):
        UCL_i / LCL_i = pbar ± 3 * sqrt(pbar (1 - pbar) / n_i),  LCL floored at 0.
    A subgroup is out-of-control if its observed proportion p_i is outside [LCL_i, UCL_i].
    """
    total_d, total_n = float(sum(defects)), float(sum(sizes))
    pbar = total_d / total_n
    ooc = 0
    for d, n in zip(defects, sizes):
        p = d / n
        sd = math.sqrt(pbar * (1.0 - pbar) / n)
        ucl = pbar + 3.0 * sd
        lcl = max(0.0, pbar - 3.0 * sd)
        if p > ucl or p < lcl:
            ooc += 1
    return ooc


def _varying_n(sizes, tol=0.001) -> int:
    """1 if subgroup sizes vary (max deviates from min by > tol fraction of the mean), else 0.

    Constant subgroup size ⇒ a classic P chart with a single pair of limits is appropriate; a
    materially varying size ⇒ variable-limit charting (Laney P′ / U chart) is the correct tool.
    """
    lo, hi, mean = min(sizes), max(sizes), sum(sizes) / len(sizes)
    return 1 if (hi - lo) > tol * mean else 0


def _series_stats(defects, sizes, rc_payload, agree_stats):
    """Compute the routing fields the graph reads (real verifiers where available)."""
    ooc = _pchart_out_of_control(defects, sizes)
    varying = _varying_n(sizes)
    binom = verifiers.capability_binomial(
        {"defectCounts": list(defects), "subgroupSizes": list(sizes)})   # {"avgP","processZ"}
    twoprop = verifiers.two_proportions(rc_payload)                       # {"pValue","zStatistic"}
    return {
        "agree": dict(agree_stats),                    # appraisers agree in this project
        "chart": {"varyingN": varying},
        "pchart": {"outOfControl": ooc},
        "cap": {"avgP": round(binom["avgP"], 5),
                "processZ": round(binom["processZ"], 4),
                "target": _TARGET_P},
        "rootcause": {"twoPropPValue": round(twoprop["pValue"], 5)},
    }


# --------------------------------------------------------------------------- data generation

def _draw_subgroups(rng, p, n_sizes):
    """One binomial draw of defect counts for the given per-subgroup sizes at true rate p."""
    defects = []
    for n in n_sizes:
        d = sum(1 for _ in range(int(n)) if rng.random() < p)
        defects.append(d)
    return defects


SHAPES = {0: "constant·in-control·meets-target",
          1: "constant·in-control·misses-target",
          2: "varying-n·in-control",
          3: "constant·out-of-control",
          4: "appraiser-disagreement"}

#: Seeds whose shape is NOT ``seed % 4`` -- see poc_project._EXTRA_SHAPES for why the modulus
#: is extended by a table rather than widened.
#: seed -> shape for the seeds that are not ``seed % 4``. A table rather than a wider modulus,
#: so a rejection shape can be given more than one seed without renumbering the others.
_EXTRA_SHAPES = {4: 4, 5: 4}


def _shape_for(seed: int) -> int:
    return _EXTRA_SHAPES.get(seed, seed % 4)


_K = 25            # number of subgroups
_N_CONST = 200     # constant subgroup size


def generate(seed: int):
    """Return (blocks, oracle_results). Seed's shape drives the data so the oracle route differs."""
    shape = _shape_for(seed)
    rng = random.Random(seed * 1_000_003 + 20260709)
    if shape == 4:
        # Reviewers who cannot reproduce the answer key: roughly one judgement in five is wrong,
        # which drives kappa against the standard below the 0.60 acceptance limit. The verdict
        # is computed from the emitted ratings by verifiers.attribute_agreement, never asserted.
        agree_block, agree_stats = _fixtures.attribute_agreement_study(
            random.Random(seed * 7_919 + 20260711), error_rate=0.22, window=(0.25, 0.55))
    else:
        agree_block, agree_stats = _fixtures.attribute_agreement_study(
            random.Random(seed * 7_919 + 20260711), error_rate=0.04, window=(0.72, 0.95))

    # Root-cause two-proportions comparison (shift A vs shift B) — kept fixed per shape so the
    # improve branch always has a real, verifier-computed effect where it is reached.
    for _ in range(400):
        if shape == 0:                                  # constant n, stable, at/below target
            sizes = [_N_CONST] * _K
            defects = _draw_subgroups(rng, 0.030, sizes)
            rc = {"events1": 22, "trials1": 600, "events2": 16, "trials2": 600}
        elif shape == 1:                                # constant n, stable, above target
            sizes = [_N_CONST] * _K
            defects = _draw_subgroups(rng, 0.090, sizes)
            rc = {"events1": 70, "trials1": 600, "events2": 38, "trials2": 600}
        elif shape == 2:                                # varying n, stable
            sizes = [int(rng.choice([120, 160, 200, 240, 300])) for _ in range(_K)]
            defects = _draw_subgroups(rng, 0.060, sizes)
            rc = {"events1": 40, "trials1": 600, "events2": 26, "trials2": 600}
        elif shape == 3:                                # constant n, one injected special cause
            sizes = [_N_CONST] * _K
            defects = _draw_subgroups(rng, 0.040, sizes)
            defects[_K // 2] = int(_N_CONST * 0.22)     # a clear out-of-control spike
            rc = {"events1": 30, "trials1": 600, "events2": 24, "trials2": 600}
        else:                                           # appraisers disagree: the record is plain
            # The per-period record is deliberately ordinary. What makes this seed's route
            # correct is the agreement study, and a record that was ALSO out of control would
            # let a contestant stop in the right place for the wrong reason.
            sizes = [_N_CONST] * _K
            defects = _draw_subgroups(rng, 0.040, sizes)
            rc = {"events1": 30, "trials1": 600, "events2": 24, "trials2": 600}

        res = _series_stats(defects, sizes, rc, agree_stats)
        ooc = res["pchart"]["outOfControl"]
        varying = res["chart"]["varyingN"]
        avg_p = res["cap"]["avgP"]
        ok = {
            0: ooc == 0 and varying == 0 and avg_p <= _TARGET_P,
            1: ooc == 0 and varying == 0 and avg_p > _TARGET_P,
            2: ooc == 0 and varying == 1,
            3: ooc > 0 and varying == 0,
            4: res["agree"]["kappaMin"] < 0.60 and ooc == 0 and varying == 0,
        }[shape]
        if ok:
            blocks = {
                "define": {"goal": "hold the breach share at or below the internal requirement "
                                   "and keep it steady",
                           "target_rate": _TARGET_P},
                "agreement": dict(agree_block),
                "subgroups": {"defectCounts": list(defects), "subgroupSizes": list(sizes),
                              "target_rate": _TARGET_P},
                "root_cause": dict(rc),
            }
            res["_shape"] = SHAPES[shape]
            return blocks, res

    raise RuntimeError(f"generator could not realize shape {shape} for seed {seed}")


def oracle_route(seed: int) -> list:
    _, res = generate(seed)
    return walk(PROJECT_GRAPH, res)


CASE = V2Case(
    case_id="adb_c26",
    title="Bringing a service desk back inside its response commitment",
    industry="services",
    y_type="attribute_proportion",
    graph=PROJECT_GRAPH,
    gate_policy=GATE_POLICY,
    generate=generate,
    # Seed 4 is the agreement-REJECTION seed: it exercises the ``M_agree`` fork's other edge,
    # which no seed reached while that edge was a self-loop the walk could not record.
    seeds=(0, 1, 2, 3, 4, 5),
    shapes={s: SHAPES[_shape_for(s)] for s in (0, 1, 2, 3, 4, 5)},
    node_data=NODE_DATA,
    fault_targets=(("M_agree", "msa.attribute_agreement",
                    "the raw appraiser ratings for this agreement study were checked and are genuinely not on file"),),
    budget={"max_turns": 24},
    context=(
        "We are the improvement team in a shared-services centre. The response commitment "
        "written into the customer contract is missed too often; internally we require that no "
        "more than 5% of tickets breach it. Twenty-five consecutive periods of ticket volume "
        "and breach counts have been exported. The archive also holds a study in which several "
        "reviewers each judged the same tickets against a known answer key, and a summary of "
        "two teams' intake and breaches over one common window."),
    goal=(
        "Work through the batches the data steward can release and say where this project "
        "stands: whether a breach judgement can be relied on at all, whether the breach share "
        "has been steady across the periods, how far today's level sits from the internal "
        "requirement, and what should be done about it next. Every number in your report must "
        "come from a computation you ran on this task; where nothing was computed, draw no "
        "conclusion."),
    blocks_meta={
        "define": {"label": "Project charter and breach requirement", "phase": "define",
                   "topics": ("charter", "breach requirement", "improvement target")},
        "agreement": {"label": "Reviewer judgements against the answer key", "phase": "measure",
                      "topics": ("reviewer judgements", "answer key")},
        "subgroups": {"label": "Per-period ticket volume and breach counts", "phase": "measure",
                      "topics": ("ticket volume", "breach counts")},
        "root_cause": {"label": "Team-by-team intake and breach summary", "phase": "analyze",
                       "topics": ("team comparison", "intake summary")},
    },
    batch_facts={
        # the fork this project turns on: constant vs varying subgroup size. No method in the
        # taxonomy reports it; an analyst reads it off the batch, and so does the oracle.
        "chart.varyingN": {"node": "M_chart_route", "key": "subgroupSizes", "kind": "varies"},
    },
    field_map={
        "agree.kappaMin": ({"method_id": "msa.attribute_agreement", "output": "kappaMin",
                            "scale": 1.0},),
        "pchart.outOfControl": ({"method_id": "control_chart.p", "output": "outOfControlCount",
                                 "scale": 1.0},
                                {"method_id": "control_chart.laney_p", "output": "flaggedCount",
                                 "scale": 1.0},
                                {"method_id": "control_chart.u", "output": "flaggedCount",
                                 "scale": 1.0}),
        # The average defective share is Sigma d / Sigma n, which is also the p chart's centre
        # line. A contestant that read it there computed it; listing only one producer made that
        # a fabrication.
        "cap.avgP": ({"method_id": "capability.binomial", "output": "avgP", "scale": 1.0},
                     {"method_id": "control_chart.p", "output": "centerLine", "scale": 1.0},),
        "cap.processZ": ({"method_id": "capability.binomial", "output": "processZ",
                          "scale": 1.0},),
        "rootcause.twoPropPValue": ({"method_id": "basic.two_proportions", "output": "pValue",
                                     "scale": 1.0},),
    },
    truth_fields=(
        {"field": "agree.kappaMin", "method_id": "msa.attribute_agreement",
         "output": "kappaMin", "scale": 1.0, "tol": 0.01},
        {"field": "pchart.outOfControl", "method_id": "control_chart.p",
         "output": "outOfControlCount", "scale": 1.0, "tol": 0.0},
        {"field": "pchart.outOfControl", "method_id": "control_chart.laney_p",
         "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "cap.avgP", "method_id": "capability.binomial",
         "output": "avgP", "scale": 1.0, "tol": 0.001},
        {"field": "cap.processZ", "method_id": "capability.binomial",
         "output": "processZ", "scale": 1.0, "tol": 0.02},
        {"field": "rootcause.twoPropPValue", "method_id": "basic.two_proportions",
         "output": "pValue", "scale": 1.0, "tol": 0.002},
    ),
)


if __name__ == "__main__":
    for s in CASE.seeds:
        _, res = generate(s)
        print(f"seed {s} [{res['_shape']:32s}] avgP={res['cap']['avgP']:.4f} "
              f"varyN={res['chart']['varyingN']} ooc={res['pchart']['outOfControl']}  "
              f"route: {' → '.join(walk(PROJECT_GRAPH, res))}")
