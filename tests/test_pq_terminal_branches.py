"""A contestant that correctly declines to go on must be able to SCORE that decision.

The defect these tests pin, measured on the shipped verifier across 7 models x 9
prerequisite-blocked tasks: reward 0.000 on all 63, with ms_recall 1.000, nf 1.000,
gate_hard_passed 1 and ms_misuse 0.000 sitting beside the zero. The models had run the right
methods, got the right numbers and correctly stopped; PQ scored them zero anyway and the
harmonic mean carried the zero into the reward.

Two independent causes, both of which had to be fixed:

* ``point_id`` and ``correct_branch`` are PRIVATE GRAPH NODE KEYS ("M_msa", "M_msa_fix") that
  the task instruction never exposes -- it asks only for "identifier of the fork". The explicit
  ``route_decisions`` path compares them with string equality, so it can never match for any
  contestant. Only the oracle, generated from the truth, speaks that vocabulary; that is why
  G3 stayed green while every real system scored zero.
* the correct branch of such a fork is a TERMINAL remediation node that runs no analysis, so
  ``branch_evidence`` holds no signature for it and nothing can be "walked" to prove it taken.

So the compliant route was indistinguishable from silence, while pressing on regardless was
"incorrect" -- both directions scored zero and the point was unpassable. These tests assert the
axis now separates the two, judged on BEHAVIOUR, never on the name the contestant gave the fork.
"""
from __future__ import annotations

import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[1])
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench import taxonomy as taxmod                      # noqa: E402
from dmaic_bench.core.models import DecisionPoint, Trace, TraceStep  # noqa: E402
from dmaic_bench.scoring import pq as pqmod                     # noqa: E402
from dmaic_bench.v2 import harbor_truth as HT                   # noqa: E402
from dmaic_bench.v2 import registry                             # noqa: E402

TAX = taxmod.load()
CASES = registry.discover()


def _trace(*method_ids, routes=()):
    return Trace(system_id="t", task_id="t",
                 steps=tuple(TraceStep(step_id=i, method_id=m)
                             for i, m in enumerate(method_ids)),
                 route_decisions=tuple(routes))


def _judge(point, trace):
    return pqmod._judge_point(point, trace, trace.successful_methods(), TAX)


def _stop_point():
    """A fork whose correct branch is terminal: run the gauge study, then stop."""
    return DecisionPoint(
        point_id="M_msa", phase="measure", rule="pctSV > 0.30", source="test",
        correct_branch="M_msa_fix",
        branch_evidence={},                       # neither side is uniquely identifiable
        source_evidence=("msa.gage_rr_crossed",),
        divergent_evidence=("capability.normal", "basic.normality"),
        convergent_evidence=(),                   # terminal: nothing to run
    )


def _proceed_point():
    """The mirror: the correct branch carries the work, the wrong one is terminal."""
    return DecisionPoint(
        point_id="M_msa", phase="measure", rule="pctSV <= 0.30", source="test",
        correct_branch="M_stability",
        branch_evidence={},
        source_evidence=("msa.gage_rr_crossed",),
        divergent_evidence=(),
        convergent_evidence=("control_chart.imr", "capability.normal"),
    )


# ------------------------------------------------------- the fork that must be STOPPED at

def test_correctly_stopping_scores_correct():
    """The whole point. Ran the diagnostic, declined to analyse further -> credited."""
    verdict, via = _judge(_stop_point(), _trace("msa.gage_rr_crossed"))
    assert verdict == "correct", (verdict, via)
    assert via == "abstention_corroborated"


def test_pressing_on_regardless_scores_incorrect():
    """Analysis work downstream of the branch it should not have taken."""
    verdict, via = _judge(_stop_point(),
                          _trace("msa.gage_rr_crossed", "basic.normality"))
    assert verdict == "incorrect", (verdict, via)
    assert via == "divergent_evidence"


def test_stopping_without_running_the_diagnostic_is_not_credited():
    """Doing nothing is not the same act as establishing the blocker and then stopping."""
    verdict, _ = _judge(_stop_point(), _trace())
    assert verdict == "unknown"


def test_the_contestants_own_fork_name_is_never_required():
    """No contestant can name a private graph key, so scoring must not depend on it."""
    from dmaic_bench.core.models import RouteDecision
    invented = RouteDecision(point="measurement_system_gate",
                             chosen_branch="stop_and_remediate_measurement_system")
    verdict, via = _judge(_stop_point(),
                          _trace("msa.gage_rr_crossed", routes=(invented,)))
    assert verdict == "correct", (verdict, via)


# ------------------------------------------------------- the fork that must be CONTINUED past

def test_correctly_proceeding_scores_correct():
    verdict, via = _judge(_proceed_point(),
                          _trace("msa.gage_rr_crossed", "control_chart.imr"))
    assert verdict == "correct", (verdict, via)
    assert via == "convergent_evidence"


def test_stopping_where_the_route_required_work_scores_incorrect():
    """Abstention must NOT be a free pass -- only terminal branches earn it."""
    verdict, via = _judge(_proceed_point(), _trace("msa.gage_rr_crossed"))
    assert verdict == "incorrect", (verdict, via)
    assert via == "abstained_from_required_branch"


# ------------------------------------------------------- the corpus property

def test_every_terminal_branch_point_in_the_build_is_passable():
    """No decision point may be unpassable: some trace must be able to score it correct.

    This is the corpus-level form of the defect. A point whose correct branch is terminal and
    which carries no source diagnostic can never be credited, whatever the contestant does.
    """
    unpassable = []
    for cid, case in CASES.items():
        for seed in case.seeds:
            _, results = case.generate(seed)
            node_methods = {k: tuple(case.methods_at(k, results)) for k in case.node_data}
            for p in HT.decision_points(case.graph, results, node_methods):
                terminal = not p.get("convergent_evidence") and not p.get("branch_evidence")
                if terminal and not p.get("source_evidence"):
                    unpassable.append((cid, seed, p["point_id"]))
    assert not unpassable, f"decision points no contestant can score: {unpassable}"
