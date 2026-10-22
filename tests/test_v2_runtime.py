"""v2 runtime integration: GatingSteward + runner + full scorer, across all data-conditioned cases.

Proves the environment enforces the methodology (locks capability on an out-of-control process),
a compliant data-conditioned agent scores TGPS=1.0, a rigid single-path agent degrades on
off-modal seeds, and the honesty fault gate zeroes an undisclosed denial.
"""
import sys, os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from dmaic_bench.v2 import builder, registry, runner, scoring
from dmaic_bench.v2.cases.injection_molding import CASE as INJ
from dmaic_bench.v2.runner import OracleAgent, ScriptedAgent, RunRecord

MODAL = ["D_scope", "M_msa", "M_stability", "A_route", "A_cap_normal", "C_control"]


# --------------------------------------------------------------------------- compliant agent

@pytest.mark.parametrize("seed", [0, 1, 2, 3])
def test_oracle_agent_is_fully_compliant(seed):
    task = builder.build_project_task(INJ, seed)
    rec = runner.run_project(task, OracleAgent())
    assert rec.trajectory == task.oracle_route()      # walked the data-conditioned correct route
    card = scoring.score_run(task, rec)
    assert card["tgps"] == 1.0
    assert card["pc"] == 1.0 and card["gc"] == 1.0 and card["cf"] == 1.0


def test_oracle_agent_compliant_across_all_parametric_cases():
    """Every discovered data-conditioned case: the oracle agent scores TGPS 1.0 on every seed."""
    for case_id, case in registry.discover().items():
        for seed in case.seeds:
            task = builder.build_project_task(case, seed)
            card = scoring.score_run(task, runner.run_project(task, OracleAgent()))
            assert card["tgps"] == 1.0, f"{case_id} seed {seed} tgps={card['tgps']}"


# --------------------------------------------------------------------------- the environment enforces

def test_environment_locks_capability_on_unstable_process():
    """The scripted agent tries to compute capability on an out-of-control process and is LOCKED
    out of both the router and the capability node — the methodology, enforced by the environment."""
    task = builder.build_project_task(INJ, 3)          # unstable
    rec = runner.run_project(task, ScriptedAgent(MODAL))
    locked = {a[1] for a in rec.audit if a[0] == "locked"}
    assert "A_route" in locked and "A_cap_normal" in locked
    assert "A_cap_normal" not in rec.trajectory        # never got the data
    assert rec.trajectory == ["D_scope", "M_msa", "M_stability", "C_control"]


def test_scripted_agent_degrades_on_off_modal_seeds():
    tg = {}
    for seed in range(4):
        task = builder.build_project_task(INJ, seed)
        tg[seed] = scoring.score_run(task, runner.run_project(task, ScriptedAgent(MODAL)))["tgps"]
    assert tg[0] == 1.0                                 # modal: scripted is right by luck
    assert tg[2] < tg[0] and tg[3] < tg[0]              # off-modal: degrades
    assert tg[3] < 0.9                                  # unstable: locked out → real penalty


# --------------------------------------------------------------------------- honesty fault gate

def test_fault_disclosed_keeps_gate_fabricated_zeroes():
    task = builder.build_project_task(INJ, 0)
    # disclosed (truthful runner sets disclosed_denial on a denied response)
    disclosed = runner.run_project(task, OracleAgent(), fault=True)
    assert disclosed.disclosed_denial is True
    assert scoring.score_run(task, disclosed, fault=True)["fault_gate"] == 1.0
    # fabricated: a run that never disclosed the denial → fault gate 0 → TGPS 0
    fab = RunRecord(task_id=task.task_id, trajectory=["D_scope"], accepted={},
                    reported_stats=[], choices={}, disclosed_denial=False)
    card = scoring.score_run(task, fab, fault=True)
    assert card["fault_gate"] == 0.0 and card["tgps"] == 0.0


# --------------------------------------------------------------------------- pass^k + aggregate

def test_pass_hat_k_and_aggregate():
    # deterministic oracle → every run identical → pass^k = 1.0
    grouped = []
    for seed in range(4):
        task = builder.build_project_task(INJ, seed)
        runs = [scoring.score_run(task, runner.run_project(task, OracleAgent())) for _ in range(3)]
        grouped.append(runs)
    assert scoring.pass_hat_k(grouped) == 1.0
    flat = [c for runs in grouped for c in runs]
    agg = scoring.aggregate(flat)
    assert agg["tgps"] == 1.0 and agg["n"] == 12


def test_numeric_fidelity_and_method_selection_helpers():
    task = builder.build_project_task(INJ, 1)
    rec = runner.run_project(task, OracleAgent())
    nf = scoring.numeric_fidelity(task.oracle_results, rec.accepted)
    assert nf["nf"] == 1.0 and nf["checked"] > 0
    ms = scoring.method_selection(task.graph, task.oracle_route(), set(rec.trajectory))
    assert ms["recall"] == 1.0 and ms["miss"] == []
