"""Two silent-failure modes that a leaderboard cannot survive, locked down.

Both were found by running a real evaluation, not by reading code, and both are invisible:
they produce no error, no warning, and a plausible-looking score.

1. FIELD NAMING. Truths inherited from ``eval/`` carried the solver's Java accessor
   (``getPValue``) while every consumer matches truths to reported outputs by the TAXONOMY
   name (``pValue``). Such an entry can never be matched: it scores as un-reported for every
   contestant, and the V7 verification gate skips it. Eight entries, across eight methods in five
   cases, were affected. Seven were ``soft``, so they cost no score -- soft entries are
   excluded from the NF denominator -- but were equally invisible to the V7 gate. The one
   HARD entry (``adb_c06 / control_chart.xbar_r / getXBarChartCenterLine``) was the only
   truth on its task, so those 6 of 372 tasks returned reward 0.000 to any answer.

2. ALTERNATIVE HYPOTHESIS. The V7 reference implementations computed two-sided
   unconditionally, ignoring a payload that declares otherwise. That is a factor-of-two
   error which reports a CORRECT truth as unreproducible.

The two interact, which is why they are tested together: the naming defect is what kept
V7 from ever reaching the one-sided truth, so defect 2 stayed hidden behind defect 1.
"""
from __future__ import annotations

import json
import pathlib
import re
import warnings

import pytest

from dmaic_bench import taxonomy
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

from dmaic_bench.cases.legacy_bridge import canonical_field
from dmaic_bench.truth import verifiers

CASES = pathlib.Path(__file__).resolve().parent.parent / "dmaic_bench" / "cases"
ACCESSOR = re.compile(r"^get[A-Z]")


class TestTruthFieldNames:
    def test_no_frozen_truth_carries_a_java_accessor(self):
        offenders = [
            (p.parent.name, t["method_id"], t["field"])
            for p in sorted(CASES.glob("*/frozen.json"))
            for t in json.loads(p.read_text(encoding="utf-8")).get("truths", [])
            if ACCESSOR.match(str(t.get("field", "")))
        ]
        assert offenders == [], (
            "these truths can never be matched by the scorer and are skipped by V7: "
            + "; ".join(f"{c}:{m}.{f}" for c, m, f in offenders))

    def test_every_frozen_truth_field_is_a_canonical_output(self):
        tax = taxonomy.load()
        bad = []
        for p in sorted(CASES.glob("*/frozen.json")):
            for t in json.loads(p.read_text(encoding="utf-8")).get("truths", []):
                method = tax.methods.get(t["method_id"])
                if method is None:
                    continue
                names = {getattr(o, "name", o) for o in (method.canonical_outputs or ())}
                if names and t["field"] not in names:
                    bad.append(f"{p.parent.name}:{t['method_id']}.{t['field']} not in {sorted(names)}")
        assert bad == [], "; ".join(bad)

    def test_accessor_is_rewritten_only_when_the_taxonomy_confirms_it(self):
        assert canonical_field("basic.one_sample_t", "getPValue") == "pValue"
        assert canonical_field("basic.one_sample_t", "pValue") == "pValue"
        # A non-mechanical rename cannot be derived, so it is listed explicitly.
        assert canonical_field("msa.gage_rr_crossed",
                               "getPercentSVTotalGage") == "percentStudyVariation"

    def test_an_unconfirmed_accessor_warns_and_is_left_alone(self):
        # Guessing here would recreate the silent mismatch the rewrite exists to remove.
        with pytest.warns(UserWarning, match="not a canonical output"):
            assert canonical_field("basic.one_sample_t", "getNoSuchThing") == "getNoSuchThing"


CREEPAGE = [3.03, 2.98, 3.00, 2.97, 3.02, 3.00, 3.02, 2.99, 3.00, 2.96,
            2.97, 2.96, 2.95, 3.02, 2.96, 2.96, 3.06, 2.97, 3.03, 2.97,
            2.94, 3.01, 2.98, 2.96, 3.02, 2.99, 2.98, 3.04, 2.99, 2.96]


class TestDeclaredAlternative:
    def test_one_sided_payload_is_not_computed_two_sided(self):
        base = {"data": CREEPAGE, "hypothesizedMean": 3.0}
        one = verifiers.one_sample_t({**base, "alternativeHypothesis": "LESS_THAN"})["pValue"]
        two = verifiers.one_sample_t(base)["pValue"]
        assert one == pytest.approx(0.0351270, abs=1e-6)
        assert two == pytest.approx(0.0702541, abs=1e-6)
        assert two == pytest.approx(2 * one, rel=1e-9), "the failure mode is exactly a factor of 2"

    def test_absent_declaration_still_means_two_sided(self):
        assert verifiers.one_sample_t({"data": CREEPAGE, "hypothesizedMean": 3.0})["pValue"] \
            == pytest.approx(0.0702541, abs=1e-6)

    @pytest.mark.parametrize("declared,expected", [
        ("LESS_THAN", "less"), ("GREATER_THAN", "greater"), ("NOT_EQUAL", "two-sided"),
        ("TWO_SIDED", "two-sided"), ("less", "less"), ("greater", "greater"),
    ])
    def test_spellings_seen_in_the_corpus_all_resolve(self, declared, expected):
        assert verifiers._alternative({"alternativeHypothesis": declared}) == expected

    def test_an_unrecognised_alternative_refuses_rather_than_defaulting(self):
        # Defaulting to two-sided here is the original defect: a payload was telling us
        # something and we silently overrode it.
        with pytest.raises(verifiers.NotVerifiable, match="refusing to assume two-sided"):
            verifiers._alternative({"alternativeHypothesis": "MUCH_LESS_THAN"})

    def test_the_corpus_truth_that_exposed_this_now_reproduces(self):
        doc = json.loads((CASES / "adb_c03" / "frozen.json").read_text(encoding="utf-8"))
        truth = next(t for t in doc["truths"]
                     if t["method_id"] == "basic.one_sample_t" and t["field"] == "pValue")
        got = verifiers.one_sample_t(
            {"data": CREEPAGE, "hypothesizedMean": 3.0,
             "alternativeHypothesis": "LESS_THAN"})["pValue"]
        assert abs(got - truth["expected"]) <= truth["tol"]
