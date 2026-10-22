"""pass^k must read every attempt, and `report()` exists to throw repeated attempts away.

`report()` keeps one row per (task, agent) so a trial re-run after a harness fault is not
counted twice. That is right for a single-attempt campaign and exactly wrong for a reliability
claim: pass^k IS a statement about repeats. Every number this repository has published so far
is k = 1, so run-to-run variance has never been estimable and the pre-registered pass^k
analysis has never been computable.

Two criteria, because one of them is nearly dead. At a resolve rate near 1% a pass^k on
`reward >= 1.0` is almost all zeros and separates nothing; what a DMAIC task asks is whether
every decision was answered correctly, and that is where the tiers differ (A 35% / B 5% /
C 16% at k = 1).
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from dmaic_harbor import campaign_report as CR         # noqa: E402


def _row(task, reward, pq_score, points=2, shape="capable", agent="terminus-2"):
    return {"trial": f"{task}__x", "agent": agent, "model": "m", "task_id": task,
            "case_id": "adb_c34", "seed": 0, "shape": shape, "reward": reward,
            "card": {"task_id": task, "case_id": "adb_c34", "seed": 0,
                     "scorecard": {"shape": shape,
                                   "pq": {"score": pq_score, "points_total": points}}}}


SHAPES = {}


def test_a_task_attempted_fewer_than_k_times_is_excluded_not_counted():
    """A partial campaign must not read as a completed pass^k."""
    rows = [_row("t1", 1.0, 1.0), _row("t1", 1.0, 1.0)]          # only 2 attempts
    out = CR.passk(rows, SHAPES, k=3)
    assert out["tasks"] == 1
    assert out["eligible"] == 0
    assert out["complete"] is False


def test_pass_k_requires_every_attempt_to_succeed():
    rows = [_row("t1", 1.0, 1.0)] * 3 + [_row("t2", 1.0, 1.0), _row("t2", 0.4, 0.5),
                                         _row("t2", 1.0, 1.0)]
    out = CR.passk(rows, SHAPES, k=3)["by_tier"]["A-proceed"]
    assert out["eligible"] == 2
    assert out["passk_decisions"] == 0.5, "t2 got one decision wrong; pass^3 must not credit it"
    assert out["pass_at_k_decisions"] == 1.0, "both tasks succeeded at least once"


def test_the_decision_criterion_is_not_the_reward_criterion():
    """A trial can answer every decision correctly and still score below 1.0 on the numeric
    axes. Conflating the two is what makes a pass^k on reward uninformative here."""
    rows = [_row("t1", 0.8, 1.0)] * 3
    out = CR.passk(rows, SHAPES, k=3)["by_tier"]["A-proceed"]
    assert out["passk_decisions"] == 1.0
    assert out["passk_resolved"] == 0.0


def test_a_task_with_no_graded_decision_points_never_counts_as_right():
    """`pq` on a task with no fork is vacuous; crediting it would inflate every tier."""
    rows = [_row("t1", 1.0, 0.0, points=0)] * 3
    out = CR.passk(rows, SHAPES, k=3)["by_tier"]["A-proceed"]
    assert out["passk_decisions"] == 0.0


def test_spread_measures_run_to_run_variance():
    """The direct answer to 'is this tier's mean a capability or a coin flip'."""
    rows = [_row("t1", 0.9, 1.0), _row("t1", 0.3, 0.5), _row("t1", 0.6, 0.5)]
    out = CR.passk(rows, SHAPES, k=3)["by_tier"]["A-proceed"]
    assert out["max_spread"] == 0.6
    assert out["mean_spread"] == 0.6


def test_only_the_first_k_attempts_count():
    """Otherwise a task that happened to be re-run more often than its neighbours is held to a
    stricter standard, and the tier mixes k = 3 with k = 5."""
    rows = [_row("t1", 1.0, 1.0)] * 3 + [_row("t1", 0.0, 0.0)]
    out = CR.passk(rows, SHAPES, k=3)["by_tier"]["A-proceed"]
    assert out["passk_decisions"] == 1.0


def test_controls_are_not_in_the_passk_population():
    """The oracle passes everything by construction; including it would report ~1.0."""
    from dmaic_harbor import failure_modes as FM
    assert "oracle" in FM.CONTROL_AGENTS and "nop" in FM.CONTROL_AGENTS
    rows = [_row("t1", 1.0, 1.0, agent="oracle")] * 3
    players = [r for r in rows if r["agent"] not in FM.CONTROL_AGENTS]
    assert CR.passk(players, SHAPES, k=3)["eligible"] == 0


def test_the_headline_keeps_the_FIRST_attempt_not_the_last(tmp_path):
    """Merging a pass^k job into the headline must not change it.

    `report()` dedupes to one row per (task, agent). Last-wins was written for the re-run case,
    where the second instance replaces a trial lost to a harness fault. It is wrong for pass^k,
    where later instances are ADDITIONAL attempts: merging the k=3 job under last-wins moved
    B-divert from 0.437 to 0.316 with no re-scoring at all, just a different one of three
    attempts being reported as the result.
    """
    import json

    def _trial(root, task, suffix, reward, pq):
        d = root / f"{task}__{suffix}"
        (d / "verifier").mkdir(parents=True)
        (d / "config.json").write_text(json.dumps(
            {"agent": {"name": "terminus-2", "model_name": "m"}, "trial_name": d.name}))
        (d / "verifier" / "scorecard.json").write_text(json.dumps(
            {"task_id": task, "case_id": "adb_c34", "seed": 0,
             "scorecard": {"shape": "capable", "reward": {"reward": reward},
                           "pq": {"score": pq, "points_total": 2}},
             "reward": {"reward": reward}}))
        (d / "verifier" / "reward.json").write_text(json.dumps({"reward": reward}))

    first, second = tmp_path / "job1", tmp_path / "job2"
    first.mkdir()
    second.mkdir()
    _trial(first, "adb_c34-T3-s0-clean", "aaa", 0.9, 1.0)
    _trial(second, "adb_c34-T3-s0-clean", "bbb", 0.1, 0.0)

    one = CR.report([first])
    both = CR.report([first, second])
    assert one["overall_mean"] == both["overall_mean"], (
        "adding a second attempt changed the headline; the dedupe is not keeping the first")
    assert both["contestant_trials"] == 1
