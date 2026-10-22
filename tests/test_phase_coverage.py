"""A phase nobody grades is a phase the benchmark does not measure.

DMAIC-Bench is named for the full Define-Measure-Analyze-Improve-Control cycle. Measured
across the corpus before anything computed this table:

    phase     cases  stages  hard truths  decision points
    define        1       1            0                0     <- graded nowhere
    measure      20      48           17               26
    analyze      21      61           28                7
    improve      13      25            3                6
    control       5       5            2                0     <- numbers only, never routing

A stage carrying neither a hard truth nor a decision point earns nothing, so a contestant can
skip it and forfeit nothing. On that evidence the benchmark grades M-A-I and its title
overclaims. The gap survived because nothing asserted it — the same shape as every other defect
this suite now guards: silent, not subtle.

Closed on 2026-09-04 by `adb_c24`, the first case carrying a hard truth and an
evidence-observable decision point in all five phases; the table above is the measured BEFORE
and is kept because it is the finding, not the status.

These tests are a RATCHET. The numbers below are today's floor; raising them is the work, and
lowering one means a phase lost its grading. `validation._check_phase_coverage` reports the same
thing per case at INFO, with a WARN when a case has a stage nobody grades.
"""
from __future__ import annotations

import warnings

import pytest

from dmaic_bench.core import registry
from dmaic_bench.core.models import PHASES


def _coverage():
    agg = {p: {"stages": 0, "truths": 0, "points": 0, "cases": 0} for p in PHASES}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for case in registry.discover().values():
            stage_phase = {s.stage_id: s.phase for s in case.meta.stages}
            data = case.generate(1)
            for ph in set(stage_phase.values()):
                if ph in agg:
                    agg[ph]["cases"] += 1
            for ph in stage_phase.values():
                if ph in agg:
                    agg[ph]["stages"] += 1
            for t in data.truths:
                ph = stage_phase.get(t.stage_id)
                if ph in agg and not t.soft:
                    agg[ph]["truths"] += 1
            for dp in case.meta.decision_points:
                ph = (stage_phase.get(getattr(dp, "stage_id", None))
                      or getattr(dp, "phase", None))
                if ph in agg:
                    agg[ph]["points"] += 1
    return agg


@pytest.fixture(scope="module")
def coverage():
    return _coverage()


#: Today's floor, re-measured 2026-09-04 after adb_c24. A RATCHET: these may only go up.
#:
#: adb_c24 is the first case in the corpus that carries a hard truth AND an
#: evidence-observable decision point in every one of the five phases. It is what moved
#: define off 0/0 (3 truths, 1 point) and gave control its first routing decision
#: (chart selection on the released line). Everything else here moved with it as well,
#: because a five-phase case adds to every column at once.

def _full_corpus():
    """True when the nine held-out expert cases are present (an operator checkout).

    Two corpora, two sets of expectations. A single number would either fail every public
    checkout or be so loose it pins nothing for an operator, so the expectation is selected by
    what is actually present -- and both remain ratchets. See docs/HELD_OUT.md.
    """
    from dmaic_bench.v2.expert_migration import _legacy_bridge_available
    return _legacy_bridge_available()

FLOOR_PUBLIC = {
    "measure": {"truths": 24, "points": 4},
    "analyze": {"truths": 37, "points": 6},
    "improve": {"truths": 10, "points": 2},
    "control": {"truths": 7, "points": 1},
    "define": {"truths": 3, "points": 1},
}


FLOOR_FULL = {
    "measure": {"truths": 21, "points": 27},
    "analyze": {"truths": 32, "points": 8},
    "improve": {"truths": 6, "points": 7},
    "control": {"truths": 6, "points": 1},
    "define": {"truths": 3, "points": 1},   # the gap this file existed to close — now closed
}

FLOOR = FLOOR_FULL if _full_corpus() else FLOOR_PUBLIC


@pytest.mark.parametrize("phase", sorted(FLOOR))
def test_no_phase_loses_grading(coverage, phase):
    for kind, floor in FLOOR[phase].items():
        assert coverage[phase][kind] >= floor, (
            f"{phase} lost {kind}: {coverage[phase][kind]} < {floor}. "
            "This is a ratchet — raise it when a phase gains grading, never lower it.")


def test_no_phase_that_exists_in_the_corpus_is_ungraded(coverage):
    """The gap is closed: every phase a case declares now earns or forfeits something.

    This test used to read ``assert ungraded == ["define"]`` — Define existed in the corpus and
    was graded nowhere, so an agent could skip it and forfeit nothing. adb_c24 closed it. The
    expectation is now the empty set, which is the only form of this assertion that cannot be
    satisfied by a phase quietly falling out of grading again.
    """
    ungraded = sorted(ph for ph in PHASES
                      if coverage[ph]["stages"] and not
                      (coverage[ph]["truths"] or coverage[ph]["points"]))
    assert ungraded == [], (
        f"these phases exist in the corpus but nothing grades them: {ungraded}. A stage that "
        "carries neither a hard truth nor a decision point can be skipped for free, so a "
        "benchmark named for the full cycle would again be measuring only part of it.")


def test_control_is_graded_on_routing_as_well_as_on_numbers(coverage):
    """The second half of the finding, which was easy to lose sight of behind Define.

    Control carried truths, so it looked graded — but with zero decision points it never asked
    whether the agent chose the right sustaining strategy, which for this phase is most of the
    skill. adb_c24's ``sustaining_chart_route`` is the first one: the released line's build
    quantity varies period to period and its record is homogeneous, so the chart family is
    fixed by the data (docs/archive/control-phase-design-2026-09-04.md §1), and the two wrong branches
    route to methods no other stage of that case requires — which is what makes the choice
    visible to ``pq.branch_evidence`` rather than only to an adapter that emits route_decisions.
    """
    assert coverage["control"]["truths"] > 0
    assert coverage["control"]["points"] > 0, (
        "Control lost its routing decisions and is back to being graded on numbers alone")


def test_every_phase_that_exists_has_at_least_one_stage(coverage):
    # Guards the degenerate way to satisfy the ratchet: deleting a phase's stages entirely.
    for ph in ("measure", "analyze", "improve", "control"):
        assert coverage[ph]["stages"] > 0, f"{ph} has no stages at all"
