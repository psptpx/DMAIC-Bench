"""The payload shapes the V7 reference implementations must be able to READ.

WHY THIS FILE EXISTS. V7 is the gate that says a benchmark truth is trustworthy because an
implementation which did not produce it can reproduce it. A verifier that cannot parse the
payload does not fail — it raises NotVerifiable and the gate SKIPS, silently. So a reader gap
and a genuinely unverifiable truth look identical from the outside, and 16 legacy truths sat
excluded from scoring for exactly that reason: the corpus writes ``assessments`` row tables,
long-format response/factor columns, ``sample1``/``sample2``, ``testMedian``,
``proportion1``/``proportion2Values``, ``data``/``responseColumn``/``termsInModel``,
``responseData``/``continuousData`` and ``contingencyTable``, and the verifiers only knew the
other spellings.

Two classes of assertion here, and both matter:
  * every NEW shape is read, and read the same way as the shape it is equivalent to (a reader
    that parses without erroring but mis-assembles the data is worse than one that refuses);
  * every OLD shape still works — the readers are additive, never a replacement.

The refusal tests are as important as the acceptance ones. Guessing (taking the first two of k
long-format levels, zipping a truncated response column, picking a point off a power curve)
would let V7 "verify" a number that answers a different question than the truth asks.
"""
from __future__ import annotations

import math

import numpy as np
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

from dmaic_bench.cases.legacy_bridge import legacy_cases
from dmaic_bench.core.validation import _suffix_lookup
from dmaic_bench.truth import verifiers as V


# --------------------------------------------------------------------- group readers

LONG = {
    "response": [1.0, 2.0, 3.0, 10.0, 11.0, 12.0, 20.0, 21.0, 22.0],
    "factor": ["line 1", "line 1", "line 1", "line 2", "line 2", "line 2", "line 3", "line 3", "line 3"],
    "responseName": "coating thickness",
    "factorName": "production line",
}


class TestLongFormat:
    def test_response_factor_columns_are_grouped_by_level(self):
        got = V._long_format_groups(LONG)
        assert [list(g) for g in got] == [[1, 2, 3], [10, 11, 12], [20, 21, 22]]

    def test_levels_keep_first_appearance_order_not_sorted_order(self):
        # "10" sorts before "2" as a string; sorting here would silently analyse a different
        # partition than the truth was derived from.
        payload = {"response": [5.0, 6.0, 7.0, 8.0],
                   "factor": ["10", "10", "2", "2"]}
        assert [list(g) for g in V._long_format_groups(payload)] == [[5, 6], [7, 8]]

    def test_the_label_columns_are_not_mistaken_for_data(self):
        # responseName/factorName are strings, not parallel columns — they must be ignored.
        assert len(V._long_format_groups(LONG)) == 3

    def test_a_length_mismatch_refuses_instead_of_zipping_to_the_shorter_column(self):
        bad = {"response": [1.0, 2.0, 3.0], "factor": ["a", "a"]}
        with pytest.raises(V.NotVerifiable, match="length mismatch"):
            V._long_format_groups(bad)

    def test_a_single_level_refuses(self):
        with pytest.raises(V.NotVerifiable, match="single factor level"):
            V._long_format_groups({"response": [1.0, 2.0], "factor": ["a", "a"]})

    def test_no_pair_present_refuses(self):
        with pytest.raises(V.NotVerifiable, match="no long-format"):
            V._long_format_groups({"data": [1.0, 2.0, 3.0]})

    @pytest.mark.parametrize("ykey,fkey", [("response", "factor"), ("values", "group"),
                                           ("data", "factor"), ("y", "group")])
    def test_every_declared_key_pair_is_read(self, ykey, fkey):
        payload = {ykey: [1.0, 2.0, 3.0, 4.0], fkey: ["a", "a", "b", "b"]}
        assert [list(g) for g in V._long_format_groups(payload)] == [[1, 2], [3, 4]]


class TestTwoGroups:
    def test_sample1_sample2_is_read(self):
        a, b = V._two_groups({"sample1": [1.0, 2.0], "sample2": [3.0, 4.0]})
        assert list(a) == [1, 2] and list(b) == [3, 4]

    def test_long_format_with_exactly_two_levels_is_read(self):
        a, b = V._two_groups({"response": [1.0, 2.0, 3.0, 4.0], "factor": ["a", "a", "b", "b"]})
        assert list(a) == [1, 2] and list(b) == [3, 4]

    def test_long_format_with_three_levels_refuses_rather_than_taking_the_first_two(self):
        with pytest.raises(V.NotVerifiable, match="3 levels, not 2"):
            V._two_groups(LONG)

    # ---- the shapes that already worked must keep working
    def test_group1_group2_still_works(self):
        a, b = V._two_groups({"group1": [1.0, 2.0], "group2": [3.0, 4.0]})
        assert list(a) == [1, 2] and list(b) == [3, 4]

    def test_groups_dict_still_works(self):
        a, b = V._two_groups({"groups": {"x": [1.0, 2.0], "y": [3.0, 4.0]}})
        assert list(a) == [1, 2] and list(b) == [3, 4]

    def test_nothing_recognisable_still_refuses(self):
        with pytest.raises(V.NotVerifiable, match="no two-group structure"):
            V._two_groups({"data": [1.0, 2.0]})


class TestAllGroups:
    def test_numbered_samples_are_read(self):
        got = V._all_groups({"sample1": [1.0], "sample2": [2.0], "sample3": [3.0]})
        assert [list(g) for g in got] == [[1], [2], [3]]

    def test_long_format_is_read(self):
        assert len(V._all_groups(LONG)) == 3

    def test_groups_dict_and_numbered_groups_still_work(self):
        assert len(V._all_groups({"groups": {"a": [1.0], "b": [2.0], "c": [3.0]}})) == 3
        assert len(V._all_groups({"group1": [1.0], "group2": [2.0]})) == 2

    def test_nothing_recognisable_still_refuses(self):
        with pytest.raises(V.NotVerifiable, match="no k-group structure"):
            V._all_groups({"data": [1.0, 2.0]})


class TestGroupTestsOnTheNewShapes:
    def test_mann_whitney_reads_sample1_sample2(self):
        a, b = [1.0, 2.0, 3.0, 4.0, 5.0], [6.0, 7.0, 8.0, 9.0, 10.0]
        got = V.mann_whitney({"sample1": a, "sample2": b})
        exp = stats.mannwhitneyu(a, b, alternative="two-sided")
        assert got["pValue"] == pytest.approx(exp.pvalue)
        assert got["statistic"] == pytest.approx(exp.statistic)

    def test_kruskal_wallis_reads_long_format_identically_to_pre_grouped(self):
        pre = {"groups": {"line 1": [1.0, 2.0, 3.0], "line 2": [10.0, 11.0, 12.0],
                          "line 3": [20.0, 21.0, 22.0]}}
        assert V.kruskal_wallis(LONG) == V.kruskal_wallis(pre)

    def test_anova_and_levene_also_reach_the_long_format(self):
        assert V.anova_oneway(LONG)["factorPValue"] < 1.0
        assert 0.0 <= V.equal_variances(LONG)["pValue"] <= 1.0


# --------------------------------------------------------------------- one-sample null

class TestWilcoxonNull:
    DATA = [7.5, 10.0, 9.9, 7.2, 12.7, 8.8, 8.6, 9.1, 10.5, 8.6, 11.4]

    def test_test_median_is_the_same_null_as_hypothesized_median(self):
        a = V.one_sample_wilcoxon({"data": self.DATA, "testMedian": 8.0})
        b = V.one_sample_wilcoxon({"data": self.DATA, "hypothesizedMedian": 8.0})
        assert a == b

    def test_median0_still_works(self):
        assert V.one_sample_wilcoxon({"data": self.DATA, "median0": 8.0}) == \
            V.one_sample_wilcoxon({"data": self.DATA, "testMedian": 8.0})

    def test_no_null_at_all_still_refuses(self):
        with pytest.raises(V.NotVerifiable, match="no hypothesized median"):
            V.one_sample_wilcoxon({"data": self.DATA})

    def test_the_declared_alternative_is_still_honoured_on_the_new_key(self):
        one = V.one_sample_wilcoxon({"data": self.DATA, "testMedian": 8.0,
                                     "alternative": "GREATER_THAN"})["pValue"]
        two = V.one_sample_wilcoxon({"data": self.DATA, "testMedian": 8.0})["pValue"]
        assert two == pytest.approx(2 * one, rel=1e-9)


# --------------------------------------------------------------------- tables

class TestTables:
    TABLE = [[94, 99, 100], [6, 1, 0]]

    def test_contingency_table_is_read_like_table(self):
        assert V.chisquare_assoc({"contingencyTable": self.TABLE}) == \
            V.chisquare_assoc({"table": self.TABLE})

    def test_neither_key_still_refuses(self):
        with pytest.raises(V.NotVerifiable, match="no table/contingencyTable"):
            V.chisquare_assoc({"rowLabels": ["a", "b"]})

    def test_observed_counts_is_read_like_observed(self):
        counts = [58, 25, 15, 12, 10]
        assert V.chisquare_gof({"observedCounts": counts}) == \
            V.chisquare_gof({"observed": counts})


# --------------------------------------------------------------------- power

class TestPowerTwoProportions:
    MINITAB = {"proportion1": 0.004583, "proportion2Values": [0.001917],
               "sampleSizes": [12000], "computationType": "POWER", "alpha": 0.05}

    def test_the_minitab_shape_matches_the_explicit_one(self):
        explicit = {"p1": 0.004583, "p2": 0.001917, "nPerGroup": 12000, "alpha": 0.05}
        assert V.power_two_proportions(self.MINITAB) == V.power_two_proportions(explicit)

    def test_the_value_is_the_arcsine_effect_size_power(self):
        from statsmodels.stats.power import NormalIndPower
        h = abs(2 * math.asin(math.sqrt(0.004583)) - 2 * math.asin(math.sqrt(0.001917)))
        exp = NormalIndPower().power(effect_size=h, nobs1=12000, alpha=0.05, ratio=1.0,
                                     alternative="two-sided")
        assert V.power_two_proportions(self.MINITAB)["power"] == pytest.approx(exp)

    @pytest.mark.parametrize("key,value", [("proportion2Values", [0.001917, 0.003]),
                                           ("sampleSizes", [12000, 18000])])
    def test_a_power_curve_refuses_rather_than_picking_a_point(self, key, value):
        # More than one sweep point means the payload does not say which point the scalar
        # truth refers to; answering anyway would verify a different number.
        with pytest.raises(V.NotVerifiable, match="power curve has no single truth value"):
            V.power_two_proportions({**self.MINITAB, key: value})

    def test_a_sample_size_computation_refuses(self):
        with pytest.raises(V.NotVerifiable, match="does not ask for power"):
            V.power_two_proportions({**self.MINITAB, "computationType": "SAMPLE_SIZE"})

    def test_missing_proportion1_refuses(self):
        with pytest.raises(V.NotVerifiable, match="no p1/proportion1"):
            V.power_two_proportions({"proportion2Values": [0.1], "sampleSizes": [100]})


# --------------------------------------------------------------------- regression

X = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
Y = [2.1, 4.4, 9.2, 15.8, 25.1, 36.4, 48.9, 64.2, 81.3, 100.6]


class TestOls:
    def test_the_column_table_reproduces_the_x_y_form(self):
        table = {"data": {"A": X, "resp": Y}, "responseColumn": "resp",
                 "continuousPredictors": ["A"], "termsInModel": ["A", "A*A"]}
        assert V.ols(table) == pytest.approx(V.ols({"x": X, "y": Y, "degree": 2}))

    def test_a_cubic_term_list_builds_a_cubic_model(self):
        table = {"data": {"A": X, "resp": Y}, "responseColumn": "resp",
                 "continuousPredictors": ["A"], "termsInModel": ["A", "A*A", "A*A*A"]}
        assert V.ols(table) == pytest.approx(V.ols({"x": X, "y": Y, "degree": 3}))

    def test_an_interaction_term_is_the_product_of_its_columns(self):
        b = [1.0, 3.0, 2.0, 5.0, 4.0, 7.0, 6.0, 9.0, 8.0, 11.0]
        table = {"data": {"A": X, "B": b, "resp": Y}, "responseColumn": "resp",
                 "continuousPredictors": ["A", "B"], "termsInModel": ["A", "B", "A*B"]}
        Xd, y = V._ols_design(table)
        assert list(y) == Y
        assert Xd[:, 2] == pytest.approx(np.asarray(X) * np.asarray(b))

    def test_absent_terms_in_model_means_the_predictors_enter_linearly(self):
        table = {"data": {"A": X, "resp": Y}, "responseColumn": "resp",
                 "continuousPredictors": ["A"]}
        assert V.ols(table) == pytest.approx(V.ols({"x": X, "y": Y, "degree": 1}))

    def test_a_term_naming_an_unknown_column_refuses(self):
        table = {"data": {"A": X, "resp": Y}, "responseColumn": "resp",
                 "continuousPredictors": ["A"], "termsInModel": ["A", "Ghost"]}
        with pytest.raises(V.NotVerifiable, match="unknown column"):
            V.ols(table)

    def test_a_response_column_missing_from_the_table_refuses(self):
        with pytest.raises(V.NotVerifiable, match="no simple x/y regression structure"):
            V.ols({"data": {"A": X}, "responseColumn": "resp", "continuousPredictors": ["A"]})

    def test_the_plain_x_y_form_still_works(self):
        got = V.ols({"x": X, "y": Y})
        assert got["rSquaredPct"] > 90.0
        assert 0.0 <= got["modelPValue"] <= 1.0


class TestPoissonRegression:
    COUNTS = [3, 1, 2, 4, 0, 2, 3, 2, 1, 0, 2, 1]
    PRED = [140.0, 142.2, 144.4, 146.6, 148.8, 151.0,
            153.2, 155.4, 157.6, 159.8, 162.0, 164.2]

    def test_the_column_table_reproduces_the_y_x_form(self):
        table = {"responseData": self.COUNTS, "responseColumn": "n",
                 "continuousPredictors": ["T"], "continuousData": {"T": self.PRED}}
        assert V.poisson_regression(table)["deviance"] == \
            pytest.approx(V.poisson_regression({"y": self.COUNTS, "x": self.PRED})["deviance"])

    def test_a_predictor_absent_from_the_data_refuses(self):
        table = {"responseData": self.COUNTS, "continuousPredictors": ["T", "Ghost"],
                 "continuousData": {"T": self.PRED}}
        with pytest.raises(V.NotVerifiable, match="not in continuousData"):
            V.poisson_regression(table)

    def test_neither_shape_still_refuses(self):
        with pytest.raises(V.NotVerifiable, match="no y/x"):
            V.poisson_regression({"data": [1, 2, 3]})


# --------------------------------------------------------------------- attribute MSA

def _rows(appraisers, parts, standards, trials, overrides=()):
    """A crossed assessments row table; `overrides` are (appraiser, part, trial, result)."""
    bad = {(a, p, t): r for a, p, t, r in overrides}
    return [{"appraiserId": a, "partId": p, "trial": t,
             "result": bad.get((a, p, t), standards[p]), "standard": standards[p]}
            for a in appraisers for p in parts for t in range(1, trials + 1)]


class TestAttributeAgreementRowTable:
    PARTS = ["P1", "P2", "P3", "P4"]
    STD = {"P1": "OK", "P2": "NG", "P3": "OK", "P4": "NG"}

    def test_a_perfect_row_table_pivots_to_perfect_agreement(self):
        payload = {"assessments": _rows(["A", "B"], self.PARTS, self.STD, 2)}
        got = V.attribute_agreement(payload)
        assert got["kappaMin"] == pytest.approx(1.0)
        assert got["agreementPct"] == pytest.approx(100.0)

    def test_the_pivot_matches_the_explicit_standard_ratings_shape(self):
        payload = {"assessments": _rows(["A", "B"], self.PARTS, self.STD, 2,
                                        overrides=[("B", "P2", 2, "OK")])}
        std, ratings = V._pivot_assessments(payload)
        assert std == ["OK", "NG", "OK", "NG"]
        assert ratings["B"] == [["OK", "NG", "OK", "NG"], ["OK", "OK", "OK", "NG"]]
        assert V.attribute_agreement(payload) == \
            V.attribute_agreement({"standard": std, "ratings": ratings})

    def test_items_keep_first_appearance_order_not_string_sorted_order(self):
        # "P10" sorts before "P2"; sorting would misalign every rating against the standard.
        parts = ["P1", "P2", "P10"]
        std = {"P1": "OK", "P2": "NG", "P10": "OK"}
        got, _ = V._pivot_assessments({"assessments": _rows(["A"], parts, std, 1)})
        assert got == ["OK", "NG", "OK"]

    def test_trials_are_ordered_by_trial_number_whatever_the_row_order(self):
        # P1's trial 3 is the only miss; it must land in trial slot 3 at P1's item index,
        # and that must hold when the table is emitted in a different row order.
        rows = _rows(["A"], self.PARTS, self.STD, 3, overrides=[("A", "P1", 3, "NG")])
        for table in (rows, list(reversed(rows))):
            std, ratings = V._pivot_assessments({"assessments": table})
            order = [p for p in self.PARTS]
            order.sort(key=lambda p: [r["partId"] for r in table].index(p))
            i = order.index("P1")
            assert std[i] == "OK"
            assert [t[i] for t in ratings["A"]] == ["OK", "OK", "NG"]

    def test_conflicting_standards_for_one_part_refuse(self):
        rows = _rows(["A"], self.PARTS, self.STD, 1)
        rows.append({"appraiserId": "B", "partId": "P1", "trial": 1,
                     "result": "NG", "standard": "NG"})
        with pytest.raises(V.NotVerifiable, match="conflicting standards"):
            V._pivot_assessments({"assessments": rows})

    def test_an_incomplete_appraiser_refuses_rather_than_scoring_a_short_trial(self):
        rows = [r for r in _rows(["A", "B"], self.PARTS, self.STD, 2)
                if not (r["appraiserId"] == "B" and r["partId"] == "P3")]
        with pytest.raises(V.NotVerifiable, match="missing parts"):
            V._pivot_assessments({"assessments": rows})

    def test_a_duplicate_reading_refuses(self):
        rows = _rows(["A"], self.PARTS, self.STD, 1)
        rows.append(dict(rows[0]))
        with pytest.raises(V.NotVerifiable, match="duplicate reading"):
            V._pivot_assessments({"assessments": rows})

    def test_a_row_missing_a_field_refuses(self):
        rows = _rows(["A"], self.PARTS, self.STD, 1)
        del rows[0]["standard"]
        with pytest.raises(V.NotVerifiable, match="missing"):
            V._pivot_assessments({"assessments": rows})

    def test_the_explicit_shape_still_works_and_an_unusable_payload_still_refuses(self):
        assert V.attribute_agreement(
            {"standard": ["OK", "NG"], "ratings": {"A": [["OK", "NG"]]}})["kappaMin"] == 1.0
        with pytest.raises(V.NotVerifiable, match="assessments row table"):
            V.attribute_agreement({"confidenceLevel": 0.95})


# --------------------------------------------------------------------- the corpus itself

def _v7_status(case, truth):
    """(computed value, reproduced?) for one truth, or (None, None) when V7 cannot reach it."""
    fn = V.REFERENCE_IMPLS.get(truth.method_id)
    if fn is None or not truth.stage_id:
        return None, None
    block = case.generate(1).blocks.get(truth.stage_id)
    if block is None:
        return None, None
    try:
        ref = fn(block)
    except V.NotVerifiable:
        return None, None
    val = _suffix_lookup(ref, truth.field)
    if val is None:
        return None, None
    return val, abs(val - truth.expected) <= max(truth.tol, 1e-12)


class TestCorpusIsIndependentlyReproduced:
    """The anti-regression lock: a reader that stops reading a shape must FAIL here rather
    than quietly reverting those truths to 'skipped' the way the original gap did."""

    def test_every_hard_legacy_truth_v7_can_reach_reproduces(self):
        bad = []
        for case in legacy_cases():
            for t in case.generate(1).truths:
                if t.soft:
                    continue
                val, ok = _v7_status(case, t)
                if val is not None and not ok:
                    bad.append(f"{case.meta.case_id}:{t.method_id}.{t.field} "
                               f"claims {t.expected} (tol {t.tol}), V7 computes {val}")
        assert bad == [], "; ".join(bad)

    def test_the_corpus_shapes_stay_readable(self):
        reached = sum(1 for case in legacy_cases() for t in case.generate(1).truths
                      if _v7_status(case, t)[0] is not None)
        # 25 as of the shape work: 21 hardened here + 4 already-hard entries V7 also confirms.
        assert reached >= 25, f"V7 reaches only {reached} legacy truths — a reader regressed"

    @pytest.mark.parametrize("case_id,method_id,field", [
        ("adb_c03", "msa.attribute_agreement", "kappaMin"),       # assessments row table
        ("adb_c13", "nonparametric.mann_whitney", "pValue"),      # sample1/sample2
        ("adb_c13", "nonparametric.kruskal_wallis", "pValue"),    # long format
        ("adb_c13", "nonparametric.one_sample_wilcoxon", "pValue"),  # testMedian
        ("adb_c07", "power.two_proportions", "power"),            # proportion1/*Values
        ("adb_c07", "regression.ols", "rSquaredPct"),             # data/termsInModel
        ("adb_c19", "tables.chisquare_assoc", "statistic"),       # contingencyTable
        ("adb_c21", "regression.poisson", "deviance"),            # responseData/continuousData
    ])
    def test_each_newly_readable_shape_hardened_a_real_truth(self, case_id, method_id, field):
        case = next(c for c in legacy_cases() if c.meta.case_id == case_id)
        truth = next(t for t in case.generate(1).truths
                     if t.method_id == method_id and t.field == field)
        assert not truth.soft, "this truth was hardened — it must not drift back to soft"
        val, ok = _v7_status(case, truth)
        assert val is not None, "V7 must be able to read this payload shape"
        assert ok, f"claims {truth.expected} (tol {truth.tol}), V7 computes {val}"
