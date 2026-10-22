"""A correct answer must score the same whichever toolchain computed it.

The benchmark compares ten models on statistical work. If a model that prefers R scores lower
than one that prefers Python for reasons of NAMING, the score measures toolchain fluency rather
than statistical competence -- the same class of confound as an all-Chinese corpus measuring
reading ability.

That was live. `flatten` joins nested keys with ".", so `_field_matches` read a dot as a
namespace separator and compared only the last segment. In base R the dot is a WORD separator:
`t.test()` returns `$p.value`, which normalised to `value` and matched nothing. The verdict was
`failed` -- not `not_computed` -- with reason "no suffix-matching numeric key", on 37 of the 49
canonical fields and 81% of corpus truth instances. An R agent that computed everything
correctly scored near zero on Numeric Fidelity.

These tests pin both directions: every mainstream convention must bind, and the two negatives
`_norm`'s docstring calls out must still be refused. The negatives matter as much as the
positives -- a matcher loose enough to accept anything turns "absent" into "failed" just as
silently, in the other direction.
"""
from __future__ import annotations

import re

import pytest

from dmaic_bench import taxonomy
from dmaic_bench.scoring.nf import _field_matches

CANONICAL = sorted({
    getattr(o, "name", o)
    for m in taxonomy.load().methods.values()
    for o in (getattr(m, "canonical_outputs", None) or ())
})


def _r_style(field: str) -> str:
    """camelCase -> base-R dotted lower case: pValue -> p.value, centerLine -> center.line."""
    return re.sub(r"(?<!^)(?=[A-Z])", ".", field).lower()


def _snake(field: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", field).lower()


class TestEveryToolchainBinds:
    def test_the_corpus_has_canonical_fields_to_check(self):
        assert len(CANONICAL) > 40, "taxonomy did not load; the rest of this file proves nothing"

    @pytest.mark.parametrize("field", CANONICAL)
    def test_r_dotted_naming_binds(self, field):
        # `jsonlite::toJSON(t.test(x))` writes p.value verbatim. This is the failure that was live.
        assert _field_matches(_r_style(field), field), f"R idiom {_r_style(field)!r} lost {field!r}"

    @pytest.mark.parametrize("field", CANONICAL)
    def test_python_snake_case_binds(self, field):
        assert _field_matches(_snake(field), field)

    @pytest.mark.parametrize("field", CANONICAL)
    def test_julia_and_octave_flat_lowercase_bind(self, field):
        assert _field_matches(field.lower(), field)
        assert _field_matches(field.upper(), field)

    @pytest.mark.parametrize("field", CANONICAL)
    def test_canonical_spelling_still_binds(self, field):
        assert _field_matches(field, field)

    def test_a_namespace_path_still_resolves_to_its_leaf(self):
        # The reading the dot originally had, which must survive: flattened solver output.
        assert _field_matches("getCapability.processZ", "processZ")
        assert _field_matches("results.summary.p.value", "pValue")


class TestTheDocumentedNegativesStillRefuse:
    """`_norm`'s docstring names these; loosening the matcher must not reach them."""

    def test_a_group_scoped_p_is_not_the_overall_p(self):
        assert not _field_matches("group1_p", "pValue")

    def test_mann_whitney_u_is_not_a_generic_statistic(self):
        assert not _field_matches("U_statistic", "statistic")

    def test_a_wrong_scale_twin_is_refused(self):
        # rSquared (fraction) vs rSquaredPct (percent): a name hit with an out-of-scale value
        # converts "absent" into "failed", which is worse than not matching.
        assert not _field_matches("rSquared", "rSquaredPct")
        assert not _field_matches("r.squared", "rSquaredPct")

    def test_a_different_quantity_sharing_a_stem_is_refused(self):
        assert not _field_matches("topCumulativePct", "topCategoryPct")


def test_no_canonical_field_is_unreachable_from_any_mainstream_convention():
    """The regression this file exists for, stated as one number rather than 49 cases."""
    broken = [f for f in CANONICAL
              if not all(_field_matches(v, f) for v in (f, _snake(f), _r_style(f), f.lower()))]
    assert broken == [], (
        f"{len(broken)} of {len(CANONICAL)} canonical fields are unreachable from a mainstream "
        f"naming convention, so the benchmark scores toolchain choice: {broken[:8]}")


class TestEndToEndScoringIsIdentical:
    """Matching field names is necessary; scoring the same is the claim.

    A matcher test can pass while the verdict still differs, so this scores one correct answer
    written in four toolchain idioms through the real `check_values` / `summarize` path and
    requires a single verdict. Verified in the built image: Python's scipy and R's `t.test`
    both return 0.03512704 for the same one-sided t-test, so any divergence here is the
    benchmark's, not the toolchain's.
    """

    ANSWER = 0.03512704
    IDIOMS = {
        "python-scipy": {"pValue": ANSWER, "tStatistic": -1.879532},
        "r-t.test": {"p.value": ANSWER, "t.statistic": -1.879532},
        "julia-hypothesistests": {"pvalue": ANSWER, "tstatistic": -1.879532},
        "jvm-commons-math3": {"p_value": ANSWER, "t_statistic": -1.879532},
    }

    def _verdict(self, outputs):
        from types import SimpleNamespace as NS

        from dmaic_bench.core.models import TruthEntry
        from dmaic_bench.scoring import nf as nf_mod
        truth = TruthEntry(method_id="basic.one_sample_t", field="pValue",
                           expected=0.035, tol=0.01)
        trace = NS(steps=[NS(method_id="basic.one_sample_t", status="success",
                             outputs=outputs)])
        detail = nf_mod.check_values(NS(truths=[truth]), trace)[0]
        return detail["status"], nf_mod.summarize([detail])["ratio"]

    def test_all_four_idioms_reach_the_same_verdict(self):
        verdicts = {name: self._verdict(out) for name, out in self.IDIOMS.items()}
        assert len(set(verdicts.values())) == 1, (
            f"the same correct answer scores differently by toolchain: {verdicts}")

    def test_and_that_verdict_is_a_pass(self):
        # Guards the degenerate way to satisfy the test above: all four failing identically.
        for name, out in self.IDIOMS.items():
            status, ratio = self._verdict(out)
            assert (status, ratio) == ("passed", 1.0), f"{name} scored {status} / {ratio}"

    def test_a_wrong_answer_fails_in_every_idiom_too(self):
        wrong = {k: {kk: (0.9 if "p" in kk.lower() and "t" not in kk.lower() else vv)
                     for kk, vv in v.items()} for k, v in self.IDIOMS.items()}
        for name, out in wrong.items():
            status, _ = self._verdict(out)
            assert status == "failed", f"{name} passed with a wrong p-value"
