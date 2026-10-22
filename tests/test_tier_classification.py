"""A task's tier must come from its route, not from how its author worded a label.

The tier is the number the difficulty claim rests on -- TIER_RESULTS reports C-stop separately
and never pools it -- so a task that lands in the wrong tier moves the headline quietly.

The classifier was a keyword match over the free-text `shape` label: "gauge-unacceptable" and
"appraiser-disagreement" meant stop, "unstable" and "out-of-control" meant divert, and anything
else meant proceed. Adding eight cases whose authors wrote "tester-unacceptable",
"surface-does-NOT-fit" and "change-cannot-be-shown" put **20 of the 33 stop-tier tasks in the
proceed tier**, with nothing anywhere reporting a problem.

`tier_of_route` replaces the heuristic with the structure: did the route reach a control plan
at all, and if so did it get there through the branch a failed stability check opens. It
reproduces the hand-classified tier of every task that predates it, which is why it could be
adopted without re-labelling anything.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                          # noqa: E402

from dmaic_bench.core.graph import walk                # noqa: E402
from dmaic_bench.v2 import registry                    # noqa: E402
from dmaic_harbor import analysis                      # noqa: E402

CASES = registry.discover()

#: The tiers of the 40 tasks that predate `tier_of_route`, hand-classified and reported in
#: docs/archive/TIER_RESULTS.md. The new definition has to reproduce these exactly or the published
#: per-tier numbers stop meaning what they said.
PRE_EXISTING = {"adb_c25", "adb_c26", "adb_c27", "adb_c28", "adb_c29", "adb_c30", "adb_c31"}
PRE_EXISTING_TIERS = {"A-proceed": 21, "B-divert": 7, "C-stop": 12}


def _tiers():
    out = {}
    for cid, case in CASES.items():
        for seed in case.seeds:
            _blocks, res = case.generate(seed)
            out[(cid, seed)] = (case.shapes.get(seed),
                                analysis.tier_of_route(case.graph, walk(case.graph, res)))
    return out


@pytest.fixture(scope="module")
def tiers():
    return _tiers()


def test_the_route_definition_reproduces_the_hand_classified_tiers(tiers):
    counts = {"A-proceed": 0, "B-divert": 0, "C-stop": 0}
    for (cid, _seed), (_shape, tier) in tiers.items():
        if cid in PRE_EXISTING:
            counts[tier] += 1
    assert counts == PRE_EXISTING_TIERS, (
        "the route-derived tier no longer agrees with the published per-tier split; "
        "docs/archive/TIER_RESULTS.md reports those tasks under the old classification")


def test_every_shipped_shape_is_in_the_lookup_table(tiers):
    """The failure mode being closed: a new label that silently classifies as A-proceed."""
    missing = sorted({shape for shape, _t in tiers.values()
                      if shape not in analysis._SHAPE_TIERS})
    assert not missing, (
        f"shape labels with no entry in shape_tiers.json: {missing} -- they would fall through "
        "the keyword fallback and be reported in whatever tier it happens to guess")


def test_the_lookup_table_agrees_with_the_routes(tiers):
    """`tier_of(shape)` is a cache of `tier_of_route`; a stale cache is a wrong headline."""
    wrong = [(cid, seed, shape, analysis.tier_of(shape), tier)
             for (cid, seed), (shape, tier) in sorted(tiers.items())
             if analysis.tier_of(shape) != tier]
    assert not wrong, f"shape_tiers.json disagrees with the oracle routes: {wrong}"


def test_the_table_holds_no_label_two_cases_disagree_about():
    """Two cases may share a label only if they share a tier -- the lookup is keyed on it."""
    seen = {}
    for (cid, seed), (shape, tier) in sorted(_tiers().items()):
        if shape in seen and seen[shape][0] != tier:
            pytest.fail(f"{shape!r} is {seen[shape][0]} for {seen[shape][1]} and {tier} for "
                        f"{cid} seed {seed}; one of them has to be renamed")
        seen[shape] = (tier, cid)


def test_a_fork_that_guards_the_failing_side_is_read_correctly():
    """adb_c38 guards `outOfControl > 0` and DEFAULTS to proceeding -- the other way round from
    every other case. "the default edge is the divert" would put its unstable seed in A."""
    case = CASES["adb_c38"]
    diverts = analysis.divert_targets(case.graph)
    assert "A_special" in diverts and "A_factors" not in diverts
    _b, res = case.generate(5)
    assert analysis.tier_of_route(case.graph, walk(case.graph, res)) == "B-divert"


def test_the_stop_tier_is_not_a_rounding_error(tiers):
    """It is reported on its own, so it has to be large enough to report."""
    stop = sum(1 for _s, t in tiers.values() if t == "C-stop")
    assert stop >= 20, f"only {stop} stop-tier tasks; the tier cannot carry a difficulty claim"
