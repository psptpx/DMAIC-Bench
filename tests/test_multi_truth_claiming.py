"""One method, several truths: each analysis must be scoreable on its own.

A case may legitimately run the same method more than once — two regressions on different
responses, or a capability study in Measure and again in Control to confirm the improvement.
That last one is not an edge case: coupling Control's pass criterion to the target set in
Define is the cross-phase dependency the project tier exists to test.

`merged_outputs` merges every step of a method last-wins, so the earlier result vanished and at
most one of those truths could ever score, however good the contestant was. `check_values` now
matches such a method step-by-step and CLAIMS each step, so two truths cannot be satisfied by
one reported number.

Both halves of the claim key matter, and getting it wrong is silent:

  * claim per METHOD only and a method's first field consumes every step — measured on
    `adb_c24`, whose two `avgP` truths claimed both capability steps before `processZ` was
    reached, so a perfect answer scored 0.952;
  * claim per FIELD only and two stages' values for one field would each satisfy the other.

So the key is (method, field), and these tests pin it from both sides.
"""
from __future__ import annotations

from types import SimpleNamespace as NS

import pytest

from dmaic_bench.core.models import TruthEntry
from dmaic_bench.scoring import nf


def _score(truths, steps):
    trace = NS(steps=[NS(method_id=m, status="success", outputs=o) for m, o in steps])
    detail = nf.check_values(NS(truths=truths), trace)
    return [d["status"] for d in detail], nf.summarize(detail)["ratio"]


class TestOneMethodSeveralStages:
    TRUTHS = (
        TruthEntry(method_id="regression.ols", field="rSquaredAdjPct", expected=93.84,
                   tol=1.5, stage_id="A_Frame"),
        TruthEntry(method_id="regression.ols", field="rSquaredAdjPct", expected=98.21,
                   tol=1.5, stage_id="A_LightAngle"),
    )

    def test_both_analyses_score_when_reported_as_separate_steps(self):
        statuses, ratio = self._run([93.9, 98.2])
        assert statuses == ["passed", "passed"] and ratio == 1.0

    def test_reporting_order_does_not_matter(self):
        statuses, _ = self._run([98.2, 93.9])
        assert statuses == ["passed", "passed"]

    def test_one_number_cannot_satisfy_two_truths(self):
        statuses, ratio = self._run([93.9, 93.9])
        assert sorted(statuses) == ["failed", "passed"] and ratio == 0.5

    def test_doing_only_one_of_the_two_analyses_scores_half(self):
        statuses, ratio = self._run([93.9])
        assert sorted(statuses) == ["failed", "passed"] and ratio == 0.5

    def test_both_wrong_scores_zero(self):
        statuses, ratio = self._run([10.0, 20.0])
        assert statuses == ["failed", "failed"] and ratio == 0.0

    def _run(self, values):
        return _score(self.TRUTHS,
                      [("regression.ols", {"rSquaredAdjPct": v}) for v in values])


class TestSeveralFieldsOfOneMethod:
    """The bug that made a correct answer score 0.952 on the first five-phase case."""

    TRUTHS = (
        TruthEntry(method_id="capability.binomial", field="avgP", expected=0.101017,
                   tol=0.001, stage_id="D_Charter"),
        TruthEntry(method_id="capability.binomial", field="processZ", expected=1.275777,
                   tol=0.01, stage_id="D_Charter"),
        TruthEntry(method_id="capability.binomial", field="avgP", expected=0.017498,
                   tol=0.001, stage_id="C_Confirmation"),
        TruthEntry(method_id="capability.binomial", field="processZ", expected=2.108396,
                   tol=0.01, stage_id="C_Confirmation"),
    )

    def test_one_step_satisfies_several_fields_of_the_same_method(self):
        statuses, ratio = _score(self.TRUTHS, [
            ("capability.binomial", {"avgP": 0.101017, "processZ": 1.275777}),
            ("capability.binomial", {"avgP": 0.017498, "processZ": 2.108396}),
        ])
        assert statuses == ["passed"] * 4, (
            "a claim set keyed by method alone lets the first field consume every step")
        assert ratio == 1.0

    def test_a_field_still_cannot_be_double_counted_across_stages(self):
        # Same capability reported twice: the Define pair passes, the Control pair does not.
        statuses, ratio = _score(self.TRUTHS, [
            ("capability.binomial", {"avgP": 0.101017, "processZ": 1.275777}),
            ("capability.binomial", {"avgP": 0.101017, "processZ": 1.275777}),
        ])
        assert sorted(statuses) == ["failed", "failed", "passed", "passed"]
        assert ratio == 0.5


def test_a_single_truth_method_still_uses_the_merged_view():
    """Unchanged for the common case: a contestant may split one analysis across steps."""
    truths = (TruthEntry(method_id="basic.one_sample_t", field="pValue",
                         expected=0.035, tol=0.01),)
    statuses, ratio = _score(truths, [
        ("basic.one_sample_t", {"tStatistic": -1.88}),
        ("basic.one_sample_t", {"pValue": 0.0351}),
    ])
    assert statuses == ["passed"] and ratio == 1.0
