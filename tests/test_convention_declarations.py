"""A defensible convention difference must not be scored as a wrong answer.

Two toolchains can compute the same statistic correctly and disagree, because they take
different defaults. R's `prop.test()` applies Yates' continuity correction; statsmodels'
`proportions_ztest` does not. Both are right. Measured on a corpus truth --
15/150 vs 4/150 against a window of 0.0065 +/- 0.0045:

    statsmodels pooled z   0.009121   inside the window
    R prop.test (Yates)    0.017766   OUTSIDE -> scored `failed`

Not `not_computed`. The agent computed correctly and was marked wrong, so the benchmark was
measuring toolchain choice. Two mechanisms fix it, and this file pins both:

  * the STAGE PAYLOAD declares the convention the stored truth used, which makes the task
    well-specified -- an agent that reads the payload knows which default to take; and
  * `TruthEntry.accepts` admits a named variant at ITS OWN precision, for corpora where no
    declaration exists. Widening the primary tolerance is the wrong tool: stretching that
    window to admit Yates needs +/-0.0113, which then admits nearly anything.

The convention actually used is recorded on the verdict, so "which default did this model
take" becomes a measurement instead of a hidden penalty.
"""
from __future__ import annotations

import math
from types import SimpleNamespace as NS

import pytest
from scipy import stats

import pytest

# The nine expert-derived cases and their bridge module are held out of the public
# release (docs/HELD_OUT.md), so this module exercises material a public checkout does
# not carry. It SKIPS there and RUNS for an operator holding the full corpus. The public
# corpus is not left unchecked by the skip: tests/test_public_corpus.py pins the exact
# 15-case public set, so an accidental omission still fails.
pytest.importorskip(
    "dmaic_bench.cases.legacy_bridge",
    reason="held-out expert cases absent (public release) -- see docs/HELD_OUT.md",
)

from dmaic_bench.cases import legacy_bridge
from dmaic_bench.core.models import TruthEntry
from dmaic_bench.scoring import nf


def _two_prop(e1, n1, e2, n2, yates):
    p1, p2, p = e1 / n1, e2 / n2, (e1 + e2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    d = abs(p1 - p2)
    if yates:
        d = max(0.0, d - 0.5 * (1 / n1 + 1 / n2))
    return 2 * stats.norm.sf(abs(d / se))


TRUTH = TruthEntry(
    method_id="basic.two_proportions", field="pValue", expected=0.0065, tol=0.0045,
    accepts=(("yates_continuity", _two_prop(15, 150, 4, 150, True), 0.0006),))


def _score(reported_key, reported_value, truth=TRUTH):
    trace = NS(steps=[NS(method_id=truth.method_id, status="success",
                         outputs={reported_key: reported_value})])
    return nf.check_values(NS(truths=[truth]), trace)[0]


class TestBothConventionsScoreAsCorrect:
    def test_the_declared_convention_passes(self):
        d = _score("pValue", _two_prop(15, 150, 4, 150, yates=False))
        assert d["status"] == "passed"
        assert "convention" not in d, "the primary answer is not a variant"

    def test_the_r_default_passes_and_is_recorded_as_a_variant(self):
        d = _score("p.value", _two_prop(15, 150, 4, 150, yates=True))
        assert d["status"] == "passed", (
            "idiomatic prop.test() was scored wrong; the benchmark is measuring toolchain choice")
        assert d["convention"] == "yates_continuity", (
            "a variant must be recorded, or 'which default did this model take' is unmeasurable")

    def test_an_actually_wrong_number_still_fails(self):
        # The mechanism must not become a way to pass by being approximately anything.
        assert _score("pValue", 0.5)["status"] == "failed"

    def test_a_variant_is_admitted_at_its_own_precision_not_a_widened_one(self):
        # Halfway between the two conventions is neither, and must not pass.
        midpoint = 0.5 * (_two_prop(15, 150, 4, 150, False) + _two_prop(15, 150, 4, 150, True))
        assert _score("pValue", midpoint)["status"] == "failed"

    def test_a_truth_without_accepts_is_unaffected(self):
        plain = TruthEntry(method_id="basic.two_proportions", field="pValue",
                           expected=0.0065, tol=0.0045)
        assert _score("pValue", 0.017766, truth=plain)["status"] == "failed"


class TestThePayloadDeclaresTheConvention:
    """A well-specified task states the acceptable answer rather than relying on a tolerance."""

    def test_two_proportion_payloads_declare_the_continuity_convention(self):
        declared = 0
        for case in legacy_bridge.legacy_cases():
            for block in case.generate(seed=1).blocks.values():
                if isinstance(block, dict) and {"events1", "trials1", "events2", "trials2"} <= set(block):
                    assert "continuityCorrection" in block, (
                        "a two-proportion payload must say which convention its truth used")
                    declared += 1
        assert declared, "fixture found no two-proportion payloads; this test proves nothing"

    def test_an_explicit_declaration_is_never_overridden(self):
        payload = {"events1": 1, "trials1": 2, "events2": 3, "trials2": 4,
                   "continuityCorrection": True}
        assert legacy_bridge._declare_conventions(payload)["continuityCorrection"] is True

    def test_declaring_conventions_adds_no_truth_and_changes_no_value(self):
        # The declaration is metadata about how a number was computed, never the number.
        before = {"events": 5, "trials": 100, "hypothesizedP": 0.1}
        after = legacy_bridge._declare_conventions(dict(before))
        assert all(after[k] == v for k, v in before.items())
