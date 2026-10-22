"""A phase nobody grades is a phase the benchmark does not measure — now for the corpus that ships.

`tests/test_phase_coverage.py` asserts exactly this property and imports `dmaic_bench.core
.registry`, which is the v1 corpus. The v2 projects are a different 15 cases with **zero
overlap**, and they are what every campaign in this repository has run. So the ratchet guarded a
corpus nobody was measuring while the one being measured drifted — the same shape as every other
defect found in this sequence: a contract with two implementations, and a test that exercises
the one that is not shipping.

Measured on the 95 v2 tasks before anything here was written:

    phase     graph nodes   routes reaching it   graded work on those routes
    define            15          95 (100%)            0     <- graded nowhere
    measure           42          95 (100%)          158
    analyze           76          77  (81%)          157
    improve           22          33  (35%)           17
    control           15          62  (65%)            0     <- graded nowhere

315 of 332 graded acts, 95%, fell in Measure and Analyze. A benchmark named for the full cycle
was grading three of its five phases, and two of those three thinly.

Closed structurally on 2026-09-12 by extending `adb_c32`: Define 0 -> 9 graded acts, Control
0 -> 5, and the Measure-plus-Analyze share 95% -> 91%. The STRUCTURAL gap is what is closed —
no phase is ungraded now — and the PROPORTION is what this ratchet exists to keep improving.
adb_c32 is the worked pattern for both phases; every case that adopts it lowers the share.

`adb_c34` adopted the Control half of that pattern the same day, taking Control 5 -> 12 and the
share 91% -> 89%. It was not voluntary: two divert seeds were added to that case and to
`adb_c35`, and a divert route cannot carry Improve or Control work by construction, so growing
the B tier mechanically raises this share. The ceiling and the tier rebalance pull against each
other, which is the point — more stop-and-divert tasks are owed more graded Define and Control
elsewhere, not a looser ceiling.

These tests are a RATCHET, like their v1 sibling: the floors are today's measurement, raising
them is the work, and lowering one means a phase lost its grading.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                          # noqa: E402

from dmaic_bench.core.graph import walk                # noqa: E402
from dmaic_bench.v2 import registry                    # noqa: E402

PHASES = ("define", "measure", "analyze", "improve", "control")


def _coverage():
    """``{phase: {nodes, reached, graded}}`` over every shipped (case, seed)."""
    agg = {p: {"nodes": 0, "reached": 0, "graded": 0} for p in PHASES}
    cases = registry.discover()
    for case in cases.values():
        for node in case.graph.nodes:
            if node.phase in agg:
                agg[node.phase]["nodes"] += 1
        for seed in case.seeds:
            _blocks, res = case.generate(seed)
            route = walk(case.graph, res)
            seen = set()
            for key in route:
                node = case.graph.node(key)
                if node is None or node.phase not in agg:
                    continue
                seen.add(node.phase)
                # Graded = the steward releases a batch here AND a method is required on it.
                if case.node_data.get(key) and tuple(case.methods_at(key, res)):
                    agg[node.phase]["graded"] += 1
            for phase in seen:
                agg[phase]["reached"] += 1
    return agg


@pytest.fixture(scope="module")
def coverage():
    return _coverage()


#: Today's measurement. Raise when a phase gains grading; never lower.
FLOOR = {
    "define": {"graded": 9},
    "measure": {"graded": 163},
    "analyze": {"graded": 159},
    "improve": {"graded": 17},
    "control": {"graded": 12},
}


@pytest.mark.parametrize("phase", sorted(FLOOR))
def test_no_phase_loses_grading(coverage, phase):
    got = coverage[phase]["graded"]
    assert got >= FLOOR[phase]["graded"], (
        f"{phase} lost grading: {got} < {FLOOR[phase]['graded']}. This is a ratchet — raise it "
        "when a phase gains grading, never lower it.")


def test_every_phase_in_the_graph_is_reached_by_some_route():
    """A phase no route reaches is a phase the corpus declares and never exercises."""
    cov = _coverage()
    never = [p for p in PHASES if cov[p]["nodes"] and not cov[p]["reached"]]
    assert never == [], f"declared but never reached: {never}"


def test_no_phase_that_exists_in_the_corpus_is_ungraded():
    """Closed on 2026-09-12 by adb_c32, which is the worked pattern for both phases.

    Define became a DECISION rather than a preamble: a Pareto over the reject categories the
    charter tallies, forking on whether one dominates — scope to it, or rank the candidate
    failure modes by risk and scope to the worst. Control became one too: the sustaining chart
    family is fixed by whether the monitoring record's inspected count holds constant, which is
    a property of the batch and not a preference.

    Both were chosen because they are things a project actually does in those phases. Filling a
    coverage table with work nobody would do is a worse failure than the gap.
    """
    cov = _coverage()
    ungraded = sorted(p for p in PHASES if cov[p]["nodes"] and not cov[p]["graded"])
    assert ungraded == [], (
        f"these phases exist in the v2 corpus but nothing grades them: {ungraded}. A node that "
        "releases no batch, or releases one no method is required on, can be skipped for free.")


#: The share of all graded work that falls in Measure and Analyze. A CEILING, and the only
#: ratchet in this file that moves DOWNWARD: it was 0.950 before adb_c32 was extended and every
#: case that adopts that pattern lowers it further. Lowering it is the work; raising it means a
#: phase lost grading or the corpus grew in M and A alone.
MA_SHARE_CEILING = 0.895


def test_measure_and_analyze_do_not_carry_the_whole_benchmark(coverage):
    """The claim the title makes. Recorded as the number it currently is."""
    total = sum(coverage[p]["graded"] for p in PHASES)
    ma = coverage["measure"]["graded"] + coverage["analyze"]["graded"]
    share = ma / total
    assert share <= MA_SHARE_CEILING, (
        f"Measure and Analyze carry {share:.1%} of all graded work, above the "
        f"{MA_SHARE_CEILING:.1%} ceiling. Either a phase lost grading or the corpus grew in M "
        "and A alone; a benchmark named for the full DMAIC cycle cannot do either quietly.")
