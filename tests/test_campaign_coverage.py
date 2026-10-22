"""A campaign reports a mean over the trials it FOUND; nothing said what it expected to find.

So a task that drops out — an agent container gone at artifact collection, a job interrupted,
a trial never scheduled — shrinks n silently and the report still reads as a whole-corpus
result. One trial in roughly 390 was lost that way on the campaign this was written against.
It was caught by hand; nothing in the report would have caught it.

The aggregate layer already refuses to average a crashed trial in as a zero, which is the
right call and is precisely what turns a false zero into a MISSING OBSERVATION. These tests
cover the other half: saying so out loud, and naming the tasks to re-run.

The bias is directional, not random: infrastructure failures land on the long, slow, verbose
trials, so the tasks that drop out are not a random sample of the corpus.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from dmaic_harbor import campaign_report as CR         # noqa: E402
from dmaic_harbor import failure_modes as FM           # noqa: E402
from dmaic_harbor import v2_tasks as V                 # noqa: E402

#: The distribution of an empty campaign, so these tests exercise `render` end to end rather
#: than a hand-shaped stub that could drift from what `report()` actually emits.
EMPTY_MODES = FM.distribution([])

CASES = V.discover()
SHIPPED = sorted({V.task_id(case, seed) for case in CASES.values() for seed in case.seeds})


def _players(task_ids, agent="terminus-2"):
    return [{"agent": agent, "task_id": t} for t in task_ids]


def test_a_complete_campaign_says_so():
    cov = CR.coverage(_players(SHIPPED))
    assert cov["shipped"] == len(SHIPPED)
    assert cov["complete"] is True
    assert cov["by_agent"]["terminus-2"]["missing"] == []
    assert "whole corpus" in CR.render({
        "job": "j", "models": [], "controls": {}, "coverage": cov, "clustered": {},
        "contestant_trials": len(SHIPPED), "overall_mean": 0.5, "zero_rate": 0.1,
        "resolve_rate": 0.0, "resolved_at": 1.0, "tiers": {}, "clustered_by_tier": {},
        "decision_rate_by_tier": {}, "axes": {}, "per_case": {}, "failure_modes": EMPTY_MODES,
        "floored": [], "trials": len(SHIPPED)})


def test_a_dropped_task_is_named_not_averaged_over():
    """The failure this exists for: one task lost to the harness, 94 reported as if complete."""
    lost = SHIPPED[7]
    cov = CR.coverage(_players([t for t in SHIPPED if t != lost]))
    assert cov["complete"] is False
    entry = cov["by_agent"]["terminus-2"]
    assert entry["missing"] == [lost]
    assert entry["observed"] == len(SHIPPED) - 1


def test_the_rendered_report_refuses_to_read_as_a_corpus_result_when_it_is_not_one():
    lost = set(SHIPPED[:3])
    cov = CR.coverage(_players([t for t in SHIPPED if t not in lost]))
    text = CR.render({
        "job": "j", "models": [], "controls": {}, "coverage": cov, "clustered": {},
        "contestant_trials": len(SHIPPED) - 3, "overall_mean": 0.5, "zero_rate": 0.1,
        "resolve_rate": 0.0, "resolved_at": 1.0, "tiers": {}, "clustered_by_tier": {},
        "decision_rate_by_tier": {}, "axes": {}, "per_case": {}, "failure_modes": EMPTY_MODES,
        "floored": [], "trials": len(SHIPPED) - 3})
    assert "INCOMPLETE" in text
    for t in lost:
        assert t in text, "a missing task must be named, so it can be re-run"
    assert "not a random sample" in text, (
        "the report must say WHY a missing observation is not a neutral loss")


def test_a_variant_run_is_counted_as_extra_and_never_as_coverage():
    """Fault and hint variants are real tasks but they are not the clean corpus. Counting one
    as coverage would let a campaign that ran probes instead of the corpus look complete."""
    cov = CR.coverage(_players([t.replace("-clean", "-fault") for t in SHIPPED]))
    assert cov["complete"] is False
    entry = cov["by_agent"]["terminus-2"]
    assert entry["observed"] == 0
    assert entry["extra"] == len(SHIPPED)


def test_every_agent_is_held_to_the_corpus_separately():
    """A campaign is complete only if EVERY contestant covered it: pooling the agents would let
    one model's coverage paper over another's gap."""
    rows = _players(SHIPPED, "a") + _players(SHIPPED[:-2], "b")
    cov = CR.coverage(rows)
    assert cov["by_agent"]["a"]["complete"] is True
    assert cov["by_agent"]["b"]["complete"] is False
    assert cov["complete"] is False
