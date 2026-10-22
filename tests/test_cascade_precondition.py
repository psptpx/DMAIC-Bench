""""Capability presumes stability" must not quietly mean "presumes an individuals chart".

The cascade precondition was one guard, `imr.outOfControl == 0`. Which chart carries a
stability verdict depends on how the run was sampled — individuals for a one-at-a-time
record, X-bar/R for a subgrouped one, a P chart for a defective share — and none of that
changes the rule. Written over `imr` alone it charged the first subgrouped case's own oracle
with a cascade violation for a stability check it had performed correctly (adb_c34, tgps
1.0 -> 0.0 on every seed that reached a capability index).

A precondition that fires on a correct trace is worse than no precondition: it is a hard
violation, so it zeroes the run.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest                                            # noqa: E402

from dmaic_bench.v2 import registry, runner, scoring     # noqa: E402
from dmaic_bench.v2.models import build_project_task     # noqa: E402


def test_a_subgrouped_stability_verdict_satisfies_the_capability_precondition():
    out = scoring.cascade_validity({"xbar": {"outOfControl": 0}}, ["cap.ppk"])
    assert out["graded"] == 1 and out["cv"] == 1.0 and out["hard_violation"] is False


def test_the_individuals_verdict_still_satisfies_it():
    out = scoring.cascade_validity({"imr": {"outOfControl": 0}}, ["cap.ppk"])
    assert out["graded"] == 1 and out["cv"] == 1.0


@pytest.mark.parametrize("field", ["imr", "xbar", "pchart"])
def test_the_rule_still_bites_when_the_run_is_unstable(field):
    """The point of the precondition, which the widening must not soften."""
    out = scoring.cascade_validity({field: {"outOfControl": 3}}, ["cap.ppk"])
    assert out["graded"] == 1 and out["cv"] == 0.0 and out["hard_violation"] is True


def test_no_stability_verdict_at_all_is_not_graded():
    """"Nothing was charted" is not the same finding as "the process was unstable"."""
    out = scoring.cascade_validity({"cap": {"ppk": 1.4}}, ["cap.ppk"])
    assert out["graded"] == 0 and out["cv"] == 1.0 and out["hard_violation"] is False


def test_cpk_is_held_to_the_same_rule_as_ppk():
    assert scoring.cascade_validity({"xbar": {"outOfControl": 2}},
                                    ["cap.cpk"])["hard_violation"] is True


def test_every_shipped_case_oracle_clears_the_cascade_on_every_seed():
    """The end-to-end statement: no case's own oracle may trip a hard cascade violation."""
    bad = []
    for cid, case in registry.discover().items():
        for seed in case.seeds:
            task = build_project_task(case, seed)
            card = scoring.score_run(task, runner.run_project(task, runner.OracleAgent()))
            if card["detail"]["cascade"]["hard_violation"]:
                bad.append((cid, seed, card["detail"]["cascade"]["per_stat"]))
    assert not bad, f"oracle traces charged with a cascade violation: {bad}"
