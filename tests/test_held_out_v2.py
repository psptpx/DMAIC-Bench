"""The v2 held-out split: what a public artifact must not contain.

A v2 case IS its decision graph. The data regenerates from a seed, so withholding seeds from a
published generator withholds nothing — the routing logic, which is what a contestant would
have to have memorised, is in the module. Holding out therefore means holding out whole cases.

The split was drawn on STRUCTURAL criteria alone (task count, tier proportions, industry and
y_type coverage) from 536 valid candidates, with a published seed. No contestant score entered
the selection: choosing the split that best matched measured difficulty would be choosing it
with the test data.

These tests are about the ARTIFACT, not the intention. A constant naming five cases is worth
nothing if a build still emits their truth packages.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                              # noqa: E402

from dmaic_bench.v2 import registry                        # noqa: E402


def test_the_split_is_five_cases_and_they_exist():
    assert len(registry.HELD_OUT_CASES) == 5
    every = set(registry.discover(include_held_out=True))
    missing = registry.HELD_OUT_CASES - every
    if missing:
        pytest.skip(f"public checkout: {sorted(missing)} absent, which is the point")
    assert registry.HELD_OUT_CASES <= every


def test_the_public_view_drops_exactly_those_cases():
    if not registry.held_out_present():
        pytest.skip("public checkout")
    full = set(registry.discover(include_held_out=True))
    public = set(registry.discover(include_held_out=False))
    assert full - public == registry.HELD_OUT_CASES
    assert len(public) == 10


def test_the_public_view_is_still_a_usable_benchmark():
    """A split that guts the corpus is not a split, it is a deletion. The public half must keep
    all three tiers, more than one y_type, and enough tasks to be worth running."""
    from dmaic_bench.core.graph import walk
    from dmaic_harbor.analysis import tier_of_route

    public = registry.discover(include_held_out=False)
    tiers, y_types, n = set(), set(), 0
    for case in public.values():
        y_types.add(case.y_type)
        for seed in case.seeds:
            n += 1
            _b, res = case.generate(seed)
            tiers.add(tier_of_route(case.graph, walk(case.graph, res)))
    assert n >= 60, f"only {n} public tasks"
    assert tiers == {"A-proceed", "B-divert", "C-stop"}, tiers
    assert len(y_types) >= 2


@pytest.mark.parametrize("case_id", sorted(registry.HELD_OUT_CASES))
def test_a_public_build_emits_nothing_of_a_held_out_case(tmp_path, case_id):
    """The test that matters. A build made under the public view must contain the held-out
    identifier NOWHERE — not in a task directory name, not in a truth package, not in an
    instruction, not in the dataset manifest."""
    if not registry.held_out_present():
        pytest.skip("public checkout")
    from dmaic_harbor import build as B

    cases = sorted(registry.discover(include_held_out=False))
    B.build_v2(tmp_path, cases=cases, verifier_base=None)
    hits = []
    for path in tmp_path.rglob("*"):
        if not path.is_file():
            continue
        if case_id in path.name:
            hits.append(str(path.relative_to(tmp_path)))
            continue
        try:
            if case_id in path.read_text(encoding="utf-8", errors="ignore"):
                hits.append(str(path.relative_to(tmp_path)))
        except OSError:
            pass
    assert not hits, f"{case_id} leaks into a public build: {hits[:5]}"


def test_the_env_switch_gives_the_public_view_without_deleting_anything(monkeypatch):
    """So a maintainer can check a build the way a third party sees it, on a tree that still
    has every case. A switch nobody can exercise is a switch nobody tests."""
    if not registry.held_out_present():
        pytest.skip("public checkout")
    monkeypatch.setenv(registry._PUBLIC_ONLY_ENV, "1")
    assert set(registry.discover()) == set(registry.discover(include_held_out=False))
    monkeypatch.delenv(registry._PUBLIC_ONLY_ENV)
    assert len(registry.discover()) == 15
