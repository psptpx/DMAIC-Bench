"""v2 long-horizon: conditional decision-graph, data-conditioned routing, gate/cascade scoring.

The load-bearing test is `test_single_path_baseline_fails_off_modal_seeds`: it encodes the
reviewer's first attack — "a scripted single-path solver would ace this" — and proves it does NOT,
because two seeds' data shapes demand routes the scripted agent cannot take.
"""
import sys, os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from dmaic_bench.core.graph import (DecisionGraph, GraphNode, GuardedEdge, evaluate,
                                        walk, score_path)
from dmaic_bench.v2 import poc_project as P
from dmaic_bench.v2 import scoring


# --------------------------------------------------------------------------- guard DSL

@pytest.mark.parametrize("expr,results,want", [
    ("normality.pValue >= 0.05", {"normality": {"pValue": 0.42}}, True),
    ("normality.pValue >= 0.05", {"normality": {"pValue": 0.001}}, False),
    ("msa.ndc >= 5 and msa.pctTol < 0.30", {"msa": {"ndc": 6, "pctTol": 0.28}}, True),
    ("msa.ndc >= 5 and msa.pctTol < 0.20", {"msa": {"ndc": 6, "pctTol": 0.28}}, False),
    ("cap.verdict in [good, marginal]", {"cap": {"verdict": "marginal"}}, True),
    ("cap.verdict in [good, capable]", {"cap": {"verdict": "marginal"}}, False),
    ("not (imr.outOfControl == 0)", {"imr": {"outOfControl": 0}}, False),
    ("imr.outOfControl == 0", {"imr": {"outOfControl": 2}}, False),
    ("missing.field >= 1", {}, False),                       # unobserved field → never satisfied
    ("cap.ppk >= 1.33", {"cap.ppk": 1.55}, True),            # flat dotted key also resolves
])
def test_guard_dsl(expr, results, want):
    assert evaluate(expr, results) is want


def test_guard_missing_field_never_true():
    # A guard over a field the agent never observed must not fire — else silence would route.
    assert evaluate("cap.ppk >= 1.33", {}) is False
    assert evaluate("cap.ppk < 1.33", {}) is False


# --------------------------------------------------------------------------- data-conditioned walk

EXPECTED_ROUTES = {
    0: ["D_scope", "M_msa", "M_stability", "A_route", "A_cap_normal", "C_control"],
    1: ["D_scope", "M_msa", "M_stability", "A_route", "A_cap_normal", "A_root_cause",
        "I_doe", "I_confirm", "C_control"],
    2: ["D_scope", "M_msa", "M_stability", "A_route", "A_cap_nonnormal", "A_root_cause",
        "I_doe", "I_confirm", "C_control"],
    3: ["D_scope", "M_msa", "M_stability", "A_special_cause", "C_control"],
}


@pytest.mark.parametrize("seed", [0, 1, 2, 3])
def test_seed_shape_drives_route(seed):
    """Same graph, four seeds → four distinct oracle-correct routes computed from the data."""
    assert P.oracle_route(seed) == EXPECTED_ROUTES[seed]


def test_all_four_routes_are_distinct():
    routes = {tuple(P.oracle_route(s)) for s in range(4)}
    assert len(routes) == 4


def test_unstable_seed_never_computes_capability():
    # The methodological gate: an out-of-control process must NOT be routed to capability.
    _, res = P.generate(3)
    assert res["imr"]["outOfControl"] > 0
    assert "A_cap_normal" not in P.oracle_route(3)
    assert "A_cap_nonnormal" not in P.oracle_route(3)
    assert "A_special_cause" in P.oracle_route(3)


# --------------------------------------------------------------------------- PC scoring

def _choices_from_route(graph: DecisionGraph, route: list) -> dict:
    """{branch_node -> next_node_on_route} for every branch point the route passes through."""
    return {k: route[i + 1] for i, k in enumerate(route[:-1]) if graph.is_branch_point(k)}


@pytest.mark.parametrize("seed", [0, 1, 2, 3])
def test_oracle_agent_scores_perfect_pc(seed):
    _, res = P.generate(seed)
    agent = _choices_from_route(P.PROJECT_GRAPH, P.oracle_route(seed))
    assert score_path(P.PROJECT_GRAPH, res, agent)["pc"] == 1.0


def test_misroute_penalized():
    _, res = P.generate(2)                              # non-normal: correct branch is cap_nonnormal
    bad = {"A_route": "A_cap_normal"}                   # agent wrongly ran normal capability
    sc = score_path(P.PROJECT_GRAPH, res, bad)
    assert sc["pc"] < 1.0
    assert sc["per_point"]["A_route"]["ok"] is False


# --------------------------------------------------------------------------- the anti-scripting proof

# A scripted single-path agent that always walks the modal "happy path" regardless of the data.
SCRIPTED_CHOICES = {"M_msa": "M_stability", "M_stability": "A_route",
                    "A_route": "A_cap_normal", "A_cap_normal": "C_control"}
SCRIPTED_TRAJECTORY = ["D_scope", "M_msa", "M_stability", "A_route", "A_cap_normal", "C_control"]


def test_single_path_baseline_fails_off_modal_seeds():
    """THE release gate: a scripted modal-route solver aces the modal seed but FAILS the seeds
    whose data demands a different route. If this ever passes on all seeds, the graph is not
    genuinely data-conditioned and the benchmark is scriptable — a hard reject."""
    pcs = {}
    for seed in range(4):
        _, res = P.generate(seed)
        pcs[seed] = score_path(P.PROJECT_GRAPH, res, SCRIPTED_CHOICES)["pc"]
    assert pcs[0] == 1.0                                 # modal seed: scripted happens to be right
    assert pcs[2] < 1.0                                  # non-normal: scripted mis-routes
    assert pcs[3] < 1.0                                  # unstable: scripted mis-routes
    # an oracle-following agent, by contrast, is perfect on every seed
    for seed in range(4):
        _, res = P.generate(seed)
        agent = _choices_from_route(P.PROJECT_GRAPH, P.oracle_route(seed))
        assert score_path(P.PROJECT_GRAPH, res, agent)["pc"] == 1.0


def test_scripted_agent_is_cascade_invalid_on_unstable_seed():
    """The scripted agent reports a capability index on the unstable process — arithmetically it
    may be 'right', but it is cascade-INVALID (Cpk on an out-of-control process is meaningless)."""
    _, res = P.generate(3)
    cv = scoring.cascade_validity(res, reported_stats=["cap.ppk"])
    assert cv["cv"] == 0.0
    assert cv["hard_violation"] is True
    # on a stable seed the same reported stat is cascade-valid
    _, res0 = P.generate(0)
    assert scoring.cascade_validity(res0, ["cap.ppk"])["cv"] == 1.0


# --------------------------------------------------------------------------- gate compliance

def test_gate_compliance_rewards_correct_order():
    gc = scoring.gate_compliance(P.GATE_POLICY, EXPECTED_ROUTES[1])
    assert gc["gc"] == 1.0
    assert gc["violations"] == []


def test_gate_compliance_catches_capability_before_msa():
    # Agent jumps to the capability-routing stage before doing MSA/stability → hard violation.
    bad = ["D_scope", "A_route", "A_cap_normal", "M_msa", "M_stability", "C_control"]
    gc = scoring.gate_compliance(P.GATE_POLICY, bad)
    assert gc["gc"] < 1.0
    assert gc["hard_violation"] is True
    assert any(v["stage"] == "A_route" for v in gc["violations"])


def test_full_project_score_scripted_vs_oracle_on_unstable():
    _, res = P.generate(3)
    oracle_agent = _choices_from_route(P.PROJECT_GRAPH, P.oracle_route(3))
    good = scoring.score_project(P.PROJECT_GRAPH, res, P.GATE_POLICY,
                                 oracle_agent, EXPECTED_ROUTES[3], reported_stats=[])
    bad = scoring.score_project(P.PROJECT_GRAPH, res, P.GATE_POLICY,
                                SCRIPTED_CHOICES, SCRIPTED_TRAJECTORY, reported_stats=["cap.ppk"])
    assert good["pc"] == 1.0 and good["hard"] is False
    assert bad["pc"] < 1.0 and bad["hard"] is True       # mis-routed AND cascade-invalid
