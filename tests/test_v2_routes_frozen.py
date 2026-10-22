"""Every shipped (case, seed) pair, pinned so a refactor has to prove it changed nothing.

Frozen at 40 pairs before the eight black-belt projects were onboarded and extended to all 95
once they were green: a pinned route is only useful if it covers what is actually shipped, and
the eight new cases reuse the same fixtures and the same guard vocabulary as the original
seven, so a change to either now has to declare itself against all of them.

Every case ships its own decision graph today, and those graphs are near-duplicates of one
another: three of them are byte-identical in node set. Merging them into one methodology graph
is the obvious next move and the dangerous one, because a naive union is NOT route-preserving --
eight forks have an out-degree in the union that no single case has, and two of them carry
identical guards. A refactor that quietly re-routes one seed would be invisible in a model
score; it would just look like a slightly different number.

So the route, the branch decisions, the decision points and a digest of the generated data are
frozen here, and equality against this file is the acceptance criterion for any structural
change. Regenerate it deliberately, never to make a failing test pass.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from dmaic_bench.core.graph import branch_decisions, walk   # noqa: E402
from dmaic_bench.v2 import harbor_truth as HT               # noqa: E402
from dmaic_bench.v2 import registry                         # noqa: E402

GOLDEN = json.loads((_ROOT / "tests" / "data" / "v2_routes_golden.json").read_text("utf-8"))
CASES = registry.discover()


def _live(cid, seed):
    case = CASES[cid]
    blocks, res = case.generate(seed)
    nm = {k: tuple(case.methods_at(k, res)) for k in case.node_data}
    path = walk(case.graph, res)
    dps = HT.decision_points(case.graph, res, nm)
    return {
        "shape": case.shapes.get(seed),
        "route": path,
        "branch_decisions": branch_decisions(case.graph, path, res),
        "decision_points": [{"point_id": p["point_id"], "correct_branch": p["correct_branch"]}
                            for p in dps],
        "blocks_digest": hashlib.sha256(
            json.dumps(blocks, sort_keys=True, default=str).encode()).hexdigest()[:16],
        "results_digest": hashlib.sha256(
            json.dumps(res, sort_keys=True, default=str).encode()).hexdigest()[:16],
    }


@pytest.mark.parametrize("key", sorted(GOLDEN))
def test_route_is_unchanged(key):
    cid, seed = key.split(":")
    if cid not in CASES:
        pytest.fail(f"{cid} disappeared from the registry; the golden set covers it")
    got = _live(cid, int(seed))
    want = GOLDEN[key]
    assert got["route"] == want["route"], f"{key}: route moved"
    assert got["branch_decisions"] == want["branch_decisions"], f"{key}: a fork changed branch"
    assert got["decision_points"] == want["decision_points"], f"{key}: decision points changed"


@pytest.mark.parametrize("key", sorted(GOLDEN))
def test_generated_data_is_unchanged(key):
    """A generator that drifts silently would move every truth under it."""
    cid, seed = key.split(":")
    if cid not in CASES:
        pytest.skip(f"{cid} not registered")
    got = _live(cid, int(seed))
    assert got["blocks_digest"] == GOLDEN[key]["blocks_digest"], f"{key}: batches changed"
    assert got["results_digest"] == GOLDEN[key]["results_digest"], f"{key}: oracle results changed"


def test_the_golden_set_still_covers_every_pre_existing_case():
    """New cases may be added; the pinned ones may not quietly leave."""
    pinned = {k.split(":")[0] for k in GOLDEN}
    missing = pinned - set(CASES)
    assert not missing, f"cases in the golden set that no longer exist: {sorted(missing)}"
