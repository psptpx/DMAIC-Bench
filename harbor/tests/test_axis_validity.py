"""An axis with nothing to measure is dropped from the headline, never imputed.

Every component scorer defines an empty denominator as 1.0:

    ms.py   len(hit) / len(required)              if required else 1.0
    nf.py   passed   / (passed + failed)          if denom    else 1.0
    pq.py   (correct + satisfied) / (pts + order) if denom    else 1.0

Averaged in, that free 1.0 is indistinguishable from an earned one. It is also not rare —
measured over the 372-task public build, NF is vacuous on 172 tasks (46.2%), PQ on 248
(66.7%), and both on 110 (29.6%), so a "three-axis harmonic mean" was frequently MS-Recall
wearing two borrowed marks. It is the axis on which a sign-flipped processZ = -7.894 against
an expected 2.25 scored nf = 1.000.

The contract is therefore: the headline is the harmonic mean over the axes that were actually
measured, and each axis publishes a `*_axis_valid` flag saying whether it was. A benchmark may
honestly say "this task does not test process quality"; it may not say "this system has perfect
process quality" on the strength of having asked nothing.
"""
from __future__ import annotations

import inspect
import os
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.abspath(os.path.join(_HERE, os.pardir, "src")),
           os.path.abspath(os.path.join(_HERE, os.pardir, os.pardir))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dmaic_harbor import spec, verify                       # noqa: E402

FLAGS = ("ms_axis_valid", "nf_axis_valid", "pq_axis_valid")


def _reward(*, required=2, hit=2, nf_passed=1, nf_failed=0, pq_points=1, pq_order=0,
            pq_score=1.0):
    """Build a scorecard whose axes are individually measurable or vacuous."""
    checked = nf_passed + nf_failed
    card = {
        "ms": {"recall": (hit / required) if required else 1.0,
               "precision": 1.0, "misuse_rate": 0.0,
               "hit": [f"m{i}" for i in range(hit)],
               "miss": [f"x{i}" for i in range(required - hit)]},
        "nf": {"summary": {"checked": checked, "passed": nf_passed, "failed": nf_failed,
                           "ratio": (nf_passed / checked) if checked else 1.0}},
        "pq": {"score": pq_score if (pq_points + pq_order) else 1.0,
               "points_total": pq_points, "order_total": pq_order, "order_violations": 0},
        "hn": {"fabrication_rate": 0.0, "misreport_rate": 0.0},
    }
    return verify.build_reward(card, {}, 1, 0)


class TestContract:
    def test_all_three_flags_are_part_of_the_reward_contract(self):
        for f in FLAGS:
            assert f in spec.REWARD_KEYS
            assert f in _reward()

    def test_formula_string_says_the_mean_ranges_over_measured_axes(self):
        assert "axis_is_measured" in spec.REWARD_FORMULA

    def test_spec_records_the_measured_corpus_shares_beside_the_formula(self):
        # The share is the reason the rule exists; it belongs next to the rule, not in a
        # commit message where the next reader will not find it.
        src = inspect.getsource(spec)
        for share in ("53.8%", "33.3%", "29.6%"):
            assert share in src, f"{share} missing from the REWARD_FORMULA rationale"


class TestFlagsTrackMeasurement:
    @pytest.mark.parametrize("kwargs,expected", [
        (dict(required=2), 1),
        (dict(required=0, hit=0), 0),
    ])
    def test_ms(self, kwargs, expected):
        assert _reward(**kwargs)["ms_axis_valid"] == expected

    @pytest.mark.parametrize("passed,failed,expected", [(1, 0, 1), (0, 1, 1), (0, 0, 0)])
    def test_nf(self, passed, failed, expected):
        assert _reward(nf_passed=passed, nf_failed=failed)["nf_axis_valid"] == expected

    @pytest.mark.parametrize("pts,order,expected", [(1, 0, 1), (0, 1, 1), (0, 0, 0)])
    def test_pq(self, pts, order, expected):
        assert _reward(pq_points=pts, pq_order=order)["pq_axis_valid"] == expected


class TestVacuousAxesAreDropped:
    def test_a_vacuous_axis_does_not_lift_the_headline(self):
        # MS 0.5 measured; NF and PQ vacuous. Old contract: HM(0.5, 1, 1) = 0.75.
        r = _reward(required=2, hit=1, nf_passed=0, nf_failed=0, pq_points=0, pq_order=0)
        assert (r["nf"], r["pq"]) == (1.0, 1.0), "the components still report their vacuous 1.0"
        assert (r["nf_axis_valid"], r["pq_axis_valid"]) == (0, 0)
        assert r["reward"] == pytest.approx(0.5), "the headline is the one measured axis alone"

    def test_a_vacuous_axis_does_not_lower_it_either(self):
        r = _reward(required=2, hit=2, nf_passed=0, nf_failed=0, pq_points=0, pq_order=0)
        assert r["reward"] == pytest.approx(1.0)

    def test_a_measured_axis_still_gates_the_others(self):
        # The harmonic mean's whole point: a measured zero cannot be bought back.
        r = _reward(required=2, hit=2, nf_passed=0, nf_failed=1, pq_points=1)
        assert r["nf_axis_valid"] == 1 and r["nf"] == 0.0
        assert r["reward"] == 0.0

    def test_measured_failure_and_no_measurement_are_distinguishable(self):
        unmeasured = _reward(nf_passed=0, nf_failed=0)
        wrong = _reward(nf_passed=0, nf_failed=1)
        assert (unmeasured["nf"], unmeasured["nf_axis_valid"]) == (1.0, 0)
        assert (wrong["nf"], wrong["nf_axis_valid"]) == (0.0, 1)
        assert unmeasured["reward"] > 0.0 and wrong["reward"] == 0.0

    def test_nothing_measurable_scores_zero_not_one(self):
        # No task in the shipped build reaches this (MS is measurable on 372/372), but a
        # future one might, and a free perfect score is the wrong failure direction.
        r = _reward(required=0, hit=0, nf_passed=0, nf_failed=0, pq_points=0, pq_order=0)
        assert all(r[f] == 0 for f in FLAGS)
        assert r["reward"] == 0.0
