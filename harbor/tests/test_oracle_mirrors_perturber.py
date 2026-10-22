"""The reference solution hand-copies the perturber's tables; this stops the copy drifting.

`solution/solve.sh` runs inside the AGENT container, which deliberately does not carry the bench
package, so it cannot import `dmaic_bench.tasks.perturb`. Its distractor keys and its
"original" suffix are therefore a hand-copy of the canonical English perturbation table.

It carried only the Chinese half. That was invisible while the corpus was Chinese and would have
degraded silently the moment an English corpus existed: the oracle would have treated
`recorder`/`remark`/`shift`/`ambient` as real data columns and failed to see `_original`
renames. A reference solution that quietly scores below its ceiling is the one defect that makes
every other number on the leaderboard unreadable, because the ceiling itself has moved.

This is the same guard `test_dependency_pins_are_single_sourced` applies to the pinned wheels:
the copy is allowed, drifting from its source is not.
"""
from __future__ import annotations

import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
HARBOR_ROOT = os.path.dirname(HERE)
BENCH_ROOT = os.path.dirname(HARBOR_ROOT)
for _p in (os.path.join(HARBOR_ROOT, "src"), BENCH_ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

SOLVE_SH = os.path.join(HARBOR_ROOT, "templates", "solution", "solve.sh")


def _oracle_namespace():
    """Execute just the mirrored block out of solve.sh, without running the oracle."""
    src = open(SOLVE_SH, encoding="utf-8").read()
    start, end = src.index("_DISTRACTOR_KEYS = {"), src.index("def pick(")
    ns: dict = {}
    exec(src[start:end], ns)          # noqa: S102 - executing our own template, by design
    return ns


@pytest.fixture(scope="module")
def oracle():
    return _oracle_namespace()


@pytest.fixture(scope="module")
def perturber():
    from dmaic_bench.tasks import perturb
    return perturb


def test_every_distractor_the_perturber_injects_is_known_to_the_oracle(oracle, perturber):
    injected = {key for pairs in perturber._DISTRACTORS_BY_LOCALE.values() for key, _ in pairs}
    assert injected, "the perturber declares no distractors; this test proves nothing"
    unknown = sorted(injected - set(oracle["_DISTRACTOR_KEYS"]))
    assert not unknown, (
        f"solve.sh would treat these injected distractors as data: {unknown}. "
        "Mirror dmaic_bench.tasks.perturb._DISTRACTORS_BY_LOCALE.")


def test_every_locale_is_mirrored_not_just_the_authored_one(perturber, oracle):
    # Every supported perturbation key must be mirrored in the oracle.
    for locale, pairs in perturber._DISTRACTORS_BY_LOCALE.items():
        missing = sorted({k for k, _ in pairs} - set(oracle["_DISTRACTOR_KEYS"]))
        assert not missing, f"locale {locale!r} is unmirrored in solve.sh: {missing}"


def test_every_original_suffix_is_stripped_by_the_oracle(oracle, perturber):
    for locale, suffix in perturber._ORIGINAL_SUFFIX.items():
        renamed = oracle["_norm"](f"flow{suffix}")
        assert renamed == "flow", (
            f"solve.sh does not strip the {locale!r} original-suffix {suffix!r}: "
            f"flow{suffix} normalised to {renamed!r}")


def test_stripping_suffixes_does_not_mangle_ordinary_snake_case(oracle):
    # Over-eager stripping would be its own silent defect, in the other direction.
    assert oracle["_norm"]("mean_value") == "meanvalue"
    assert oracle["_norm"]("subgroup_size") == "subgroupsize"
