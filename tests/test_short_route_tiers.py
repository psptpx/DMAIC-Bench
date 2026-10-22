"""A tier whose correct route is short asks a yes/no question, and a mean over it misleads.

Measured on the first complete 95-task campaign, and the gap is a factor of five in the
impression it gives:

    B-divert   mean 0.309   decisions answered correctly 1 of 18   (6%)
    C-stop     mean 0.409   decisions answered correctly 6 of 33   (18%)

The mean is inflated by partial credit from the numeric axes on tasks where the decision itself
was wrong — a contestant can compute every number correctly, take the wrong branch, and still
carry a mean of 0.4 into a tier summary that reads as "got about 40% of the way".

Why these tiers and not A-proceed: a task has few decision points because its correct route is
short, and a route that correctly terminates at the gauge has exactly one fork on it. Per tier,
mean route length and mean decision points — A-proceed 7.2 / 3.6, B-divert 4.8 / 1.9,
C-stop 4.6 / 2.5. A-proceed has real granularity and keeps its continuous mean.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                          # noqa: E402

from dmaic_harbor import campaign_report as CR         # noqa: E402


def _row(points_total, score):
    return {"card": {"scorecard": {"pq": {"points_total": points_total, "score": score}}}}


def test_a_decision_is_correct_only_when_every_point_is():
    rows = [_row(1, 1.0), _row(2, 0.5), _row(4, 1.0), _row(1, 0.0)]
    out = CR.decision_rate(rows)
    assert out == {"n": 4, "correct": 2, "rate": 0.5}, (
        "a project that got half its decisions right did not make the call correctly")


def test_a_task_with_no_decision_points_is_not_counted():
    """It asks no question, so it cannot answer one; including it would dilute the rate."""
    assert CR.decision_rate([_row(0, 0.0), _row(0, 1.0)]) == {}
    out = CR.decision_rate([_row(0, 1.0), _row(2, 1.0)])
    assert out["n"] == 1


def test_partial_credit_does_not_count_as_a_correct_decision():
    """The whole point: a contestant that computed every number right and branched wrong has
    NOT made the call, however high its reward."""
    assert CR.decision_rate([_row(3, 0.999)])["correct"] == 0


def test_only_the_short_route_tiers_are_reported_this_way():
    assert set(CR.NEAR_BINARY_TIERS) == {"B-divert", "C-stop"}
    assert "A-proceed" not in CR.NEAR_BINARY_TIERS, (
        "A-proceed averages 3.6 decision points over a 7.2-node route; a continuous mean there "
        "is real granularity, not false precision")


@pytest.mark.parametrize("tier", sorted(CR.NEAR_BINARY_TIERS))
def test_each_short_route_tier_has_a_question_it_names(tier):
    assert CR.NEAR_BINARY_TIERS[tier].endswith("-correct")
