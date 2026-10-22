"""A precondition check cannot be evidence of a BRANCH, because running one shows no intent.

`scoring.ms.ALWAYS_RELEVANT` declares these methods legitimate anywhere and exempts them from
the precision penalty: they are what a careful analyst runs before committing to anything. The
branch inference simultaneously used them as proof of which edge was taken. Both positions
cannot hold.

It mattered in one common place. On the stability fork the correct branch is the special-cause
investigation, which runs the same chart the fork itself ran and therefore carries no unique
signature; the WRONG branch carried `basic.normality` as its ONLY signature in 8 of 15 cases.
A contestant that diverted correctly and ran a normality check was recorded as having failed to
divert — and that is the disciplined contestant, which is the one a benchmark exists to tell
apart from the undisciplined one.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from dmaic_bench.core.graph import walk                    # noqa: E402
from dmaic_bench.scoring.ms import ALWAYS_RELEVANT         # noqa: E402
from dmaic_bench.v2 import harbor_truth as HT              # noqa: E402
from dmaic_bench.v2 import registry                        # noqa: E402

CASES = registry.discover()


def _points(case, seed):
    _b, res = case.generate(seed)
    nm = {k: tuple(case.methods_at(k, res)) for k in case.node_data}
    return HT.decision_points(case.graph, res, nm), case.graph, res, nm


def test_no_branch_is_proved_by_a_precondition_check_alone():
    offenders = []
    for cid, case in sorted(CASES.items()):
        for seed in case.seeds:
            _pts, graph, res, nm = _points(case, seed)
            for src in walk(graph, res):
                for target, methods in HT.branch_evidence(graph, src, nm).items():
                    if methods and set(methods) <= ALWAYS_RELEVANT:
                        offenders.append((cid, seed, src, target, methods))
    assert not offenders, (
        "running a check this repository calls always legitimate would be read as taking a "
        f"branch: {offenders[:5]}")


def test_the_subtree_evidence_excludes_them_too():
    """Removing them from `branch_evidence` alone is not enough: the fallback path reads
    `divergent_evidence`, which reasons over subtrees and carried the same methods."""
    for cid, case in sorted(CASES.items()):
        for seed in case.seeds:
            pts, *_ = _points(case, seed)
            for p in pts:
                assert not (set(p["divergent_evidence"]) & ALWAYS_RELEVANT), (cid, seed, p)
                assert not (set(p["convergent_evidence"]) & ALWAYS_RELEVANT), (cid, seed, p)


def test_the_exclusion_created_no_new_unscoreable_point():
    """The risk of the fix: strip a fork's only signature and nobody can be judged either way.

    9 before the exclusion, 9 after it, and **7** once `divergent_evidence` began counting
    methods declared on nodes that carry no data batch — that widening gave two previously
    signature-less forks a signal. A rise above 9 is the regression this guards; a fall is the
    corpus gaining discrimination and the floor moves down with it.
    """
    dead = 0
    for case in CASES.values():
        for seed in case.seeds:
            pts, *_ = _points(case, seed)
            for p in pts:
                if not (p["divergent_evidence"] or p["convergent_evidence"]
                        or p["branch_evidence"]):
                    dead += 1
    assert dead <= 7, f"{dead} points have no evidence of any kind; it was 7 after the widening"


def test_the_real_error_still_convicts():
    """Capability computed on a run that was never shown stable must remain proof of the wrong
    turn — that is the error the benchmark exists to detect, and the fix must not soften it."""
    case = CASES["adb_c25"]
    for seed in case.seeds:
        pts, graph, res, _nm = _points(case, seed)
        for p in pts:
            if p["point_id"] != "M_stability" or p["correct_branch"] == "A_route":
                continue
            div = set(p["divergent_evidence"])
            assert div, "the divert fork lost all of its signal"
            assert any(m.startswith("capability.") for m in div), (
                f"seed {seed}: capability is no longer evidence of having pressed on: {div}")
