"""A job tree must describe itself on the axis its results are reported over.

Every difficulty number this benchmark publishes is per ROUTING TIER — A-proceed / B-divert /
C-stop. The scorecard carried `tier`, which is the harbor task tier (T3 on every v2 project) and
says nothing about difficulty, so the axis had to be re-derived from the registry to read a
campaign at all. A run whose corpus has since changed could not be re-read correctly, and an
analysis run without the bench package could not be read at all.

The shape goes in the SCORECARD and not in task.toml, deliberately: a shape names the finding
outright — "gauge-unacceptable", "surface-does-NOT-fit" — and task.toml sits beside the agent's
build context, while the scorecard is written by the verifier in its own container after the
agent is gone.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                          # noqa: E402

from dmaic_bench.v2 import registry                    # noqa: E402
from dmaic_harbor import verify as VF                  # noqa: E402


def test_the_routing_tier_is_derived_for_every_shipped_shape():
    bad = []
    for cid, case in sorted(registry.discover().items()):
        for seed in case.seeds:
            shape = case.shapes.get(seed)
            tier = VF._routing_tier(shape)
            if tier not in ("A-proceed", "B-divert", "C-stop"):
                bad.append((cid, seed, shape, tier))
    assert not bad, f"shapes with no routing tier: {bad}"


def test_a_non_v2_task_gets_an_empty_tier_rather_than_a_wrong_one():
    """v1 tasks have no routing shape; guessing one would put them in a tier they are not in."""
    assert VF._routing_tier(None) == "" and VF._routing_tier("") == ""


def test_the_tier_derivation_never_raises():
    """It runs inside the verifier, where an exception costs the whole trial its verdict."""
    for value in (object(), 3, [], {"a": 1}, "not-a-shape-anyone-shipped"):
        assert isinstance(VF._routing_tier(value), str)


@pytest.mark.parametrize("case_id", ["adb_c30", "adb_c33", "adb_c39"])
def test_the_shape_the_scorecard_will_publish_is_the_one_the_case_declares(case_id):
    """The value comes from the truth package's v2 block, which is built from the case."""
    from dmaic_harbor import v2_tasks as V
    case = registry.discover()[case_id]
    for seed in case.seeds:
        block = V.graph_truth(case, seed)
        assert block["shape"] == case.shapes.get(seed), (
            f"{case_id} seed {seed}: the scorecard would publish {block['shape']!r} where the "
            f"case declares {case.shapes.get(seed)!r}")
        assert VF._routing_tier(block["shape"]) in ("A-proceed", "B-divert", "C-stop")
