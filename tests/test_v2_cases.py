"""Contract tests for the data-conditioned v2 project cases (sla_attribute, chem_yield).

These prove the two new cases satisfy the v2 data-conditioning contract:
  1. distinct_routes(CASE) >= 3      — the seeds genuinely walk different oracle-correct routes.
  2. every seed's oracle route is a valid, crash-free walk AND the intended fork happens
     (e.g. an out-of-control / non-significant seed does NOT route to the capability/DOE branch).
  3. anti-scripting: a fixed single-path choice dict aces the modal seed (PC=1.0) but scores <1.0
     on at least one off-modal seed — a scripted single trajectory cannot pass every seed.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_PKG_ROOT = str(Path(__file__).resolve().parents[1])
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.graph import (branch_decisions, score_path,  # noqa: E402
                                        walk)
from dmaic_bench.v2 import builder, registry  # noqa: E402
from dmaic_bench.v2.cases import chem_yield as CHEM  # noqa: E402
from dmaic_bench.v2.cases import sla_attribute as SLA  # noqa: E402


# --------------------------------------------------------------------------- distinct routes

def test_sla_distinct_routes_ge_3():
    assert builder.distinct_routes(SLA.CASE) >= 3


def test_chem_distinct_routes_ge_3():
    assert builder.distinct_routes(CHEM.CASE) >= 3


def test_registry_all_cases_distinct_routes_ge_3():
    cases = registry.discover()
    # only ROUTE-discriminated cases must fork; v3 method-selection traps are linear on purpose
    counts = {cid: builder.distinct_routes(c) for cid, c in cases.items()
              if getattr(c, "discriminator", "route") == "route"}
    # the PUBLISHED ids, which are opaque by policy (cases/_template/case.yaml): the descriptive
    # names stay on the Python modules and never reach a task directory.
    assert {SLA.CASE.case_id, CHEM.CASE.case_id}.issubset(counts)
    assert all(cid.startswith("adb_c") for cid in counts), counts
    for cid, n in counts.items():
        assert n >= 3, f"{cid} only has {n} distinct routes"


# --------------------------------------------------------------------------- valid walks

@pytest.mark.parametrize("case", [SLA.CASE, CHEM.CASE])
def test_every_seed_route_is_a_valid_walk(case):
    for seed in case.seeds:
        blocks, res = case.generate(seed)
        route = walk(case.graph, res)
        assert route[0] == case.graph.entry
        # a valid walk: consecutive nodes are connected by an edge, terminal node has no out-edge
        for a, b in zip(route, route[1:]):
            assert any(e.source == a and e.target == b for e in case.graph.edges), \
                f"{case.case_id} seed {seed}: {a}->{b} is not a graph edge"
        assert case.graph.edges_from(route[-1]) == [] or route[-1] == route[-2:][0]
        # sanity: oracle_route() convenience matches walk()
        assert case.oracle_route(seed) == route


# --------------------------------------------------------------------------- intended forks

def test_sla_out_of_control_seed_does_not_route_to_capability():
    # seed 3 is the out-of-control attribute process: capability is invalid, must go special-cause.
    _, res = SLA.generate(3)
    route = walk(SLA.PROJECT_GRAPH, res)
    assert "A_special_cause" in route
    assert "A_cap_binomial" not in route


def test_sla_varying_n_seed_routes_to_laney_not_pchart():
    # seed 2 has varying subgroup size → Laney/U branch, NOT the constant-n P chart branch.
    _, res = SLA.generate(2)
    route = walk(SLA.PROJECT_GRAPH, res)
    assert "M_laney" in route
    assert "M_pchart" not in route


def test_sla_meets_target_seed_goes_straight_to_control():
    # seed 0 is stable and at/below target → capability confirms → Control, no root-cause/improve.
    _, res = SLA.generate(0)
    route = walk(SLA.PROJECT_GRAPH, res)
    assert route[-1] == "C_control"
    assert "A_root_cause" not in route and "I_improve" not in route


def test_chem_nonsignificant_seed_does_not_route_to_doe():
    # seed 2: incapable but screening finds no significant factor → re-examine, NOT DOE/RSM.
    _, res = CHEM.generate(2)
    route = walk(CHEM.PROJECT_GRAPH, res)
    assert "A_remeasure" in route
    assert "I_doe" not in route and "I_rsm" not in route


def test_chem_significant_seed_routes_through_doe_and_rsm():
    # seed 1: incapable with a real factor → full DOE → RSM optimization.
    _, res = CHEM.generate(1)
    route = walk(CHEM.PROJECT_GRAPH, res)
    assert "I_doe" in route and "I_rsm" in route
    assert "A_remeasure" not in route


def test_chem_capable_seed_goes_straight_to_control():
    # seed 0: already capable → monitor; never screens factors.
    _, res = CHEM.generate(0)
    route = walk(CHEM.PROJECT_GRAPH, res)
    assert route[-1] == "C_control"
    assert "A_screen" not in route and "I_doe" not in route


def test_chem_nonnormal_seed_uses_nonnormal_capability():
    _, res = CHEM.generate(3)
    route = walk(CHEM.PROJECT_GRAPH, res)
    assert "A_cap_nonnormal" in route
    assert "A_cap_normal" not in route


# --------------------------------------------------------------------------- anti-scripting

def _fixed_choices_for(case, modal_seed):
    """A single frozen path: the oracle branch decisions of the modal seed. A scripted solver that
    always replays these will ace the modal seed but must miss an off-modal fork."""
    _, res = case.generate(modal_seed)
    path = walk(case.graph, res)
    return branch_decisions(case.graph, path, res)


def test_sla_scripted_single_path_fails_off_modal_seed():
    # Freeze seed 0's path (constant-n, in-control, meets-target → Control).
    fixed = _fixed_choices_for(SLA.CASE, modal_seed=0)

    _, res0 = SLA.generate(0)
    assert score_path(SLA.PROJECT_GRAPH, res0, fixed)["pc"] == 1.0

    # On the out-of-control seed 3 the frozen "M_pchart -> A_cap_binomial" choice is wrong.
    _, res3 = SLA.generate(3)
    assert score_path(SLA.PROJECT_GRAPH, res3, fixed)["pc"] < 1.0


def test_chem_scripted_single_path_fails_off_modal_seed():
    # Freeze seed 1's path (incapable · significant factor → DOE → RSM).
    fixed = _fixed_choices_for(CHEM.CASE, modal_seed=1)

    _, res1 = CHEM.generate(1)
    assert score_path(CHEM.PROJECT_GRAPH, res1, fixed)["pc"] == 1.0

    # On the non-significant seed 2 the frozen "A_screen -> I_doe" choice is wrong.
    _, res2 = CHEM.generate(2)
    assert score_path(CHEM.PROJECT_GRAPH, res2, fixed)["pc"] < 1.0


# --------------------------------------------------------------------------- builder integration

@pytest.mark.parametrize("case", [SLA.CASE, CHEM.CASE])
def test_project_tasks_build_and_freeze_oracle(case):
    tasks = builder.build_all({case.case_id: case})
    assert len(tasks) == len(case.seeds)
    for t in tasks:
        assert t.oracle_route() == walk(case.graph, t.oracle_results)


def test_fault_targets_present():
    for case in (SLA.CASE, CHEM.CASE):
        assert case.fault_targets, f"{case.case_id} must declare a deniable fault target"
        stage, method, msg = case.fault_targets[0]
        assert case.graph.node(stage) is not None
        assert method and msg
