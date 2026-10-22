"""Non-canonical method ids observed in retained traces resolve to exactly one taxonomy id.

Motivating case: GPT-5.6-luna on adb_c25 seed 3 ran `capability.capability_normal` on a
flagged run and was credited with abstaining from capability, because the scorer's divergent
evidence names `capability.normal`. Every string below was seen in a real trace.
"""
import pytest
from dmaic_bench.core.models import canonical_method_id

OBSERVED = {
    "basic_test.basic.descriptive_summary": "basic.descriptive_summary",
    "basic_test.basic.normality": "basic.normality",
    "capability.capability_normal": "capability.normal",
    "basic.basic_descriptive_summary": "basic.descriptive_summary",
    "basic_test.basic.two_sample_t": "basic.two_sample_t",
    "control_chart.control_chart_imr": "control_chart.imr",
    "basic_test.basic_descriptive_summary": "basic.descriptive_summary",
    "basic.basic_normality": "basic.normality",
    "basic.basic_one_sample_t": "basic.one_sample_t",
    "nonparametric.nonparametric_runs_test": "nonparametric.runs_test",
    "basic.basic.normality": "basic.normality",
    "basic_test.basic.correlation": "basic.correlation",
    "basic_test.basic.one_sample_t": "basic.one_sample_t",
    "basic_test.basic_normality": "basic.normality",
    "basic_test.basic_one_sample_t": "basic.one_sample_t",
    "basic.basic.descriptive_summary": "basic.descriptive_summary",
    "basic.basic.two_sample_t": "basic.two_sample_t",
    "control_chart.control_chart.imr": "control_chart.imr",
    "nonparametric.nonparametric.runs_test": "nonparametric.runs_test",
    "msa.msa.gage_rr_crossed": "msa.gage_rr_crossed",
    "msa.msa_gage_rr_crossed": "msa.gage_rr_crossed",
    "regression.regression_ols": "regression.ols",
    "basic_test.normality": "basic.normality",
    "meta.meta_data_profiling": "meta.data_profiling",
}


@pytest.mark.parametrize("slip,canonical", sorted(OBSERVED.items()))
def test_observed_slip_resolves(slip, canonical):
    assert canonical_method_id(slip) == canonical


@pytest.mark.parametrize("mid", ["meta.data_profile", "anova.factorial_analysis", "nonsense"])
def test_unknown_stays_unknown(mid):
    assert canonical_method_id(mid) == mid


def test_canonical_ids_are_fixed_points():
    from dmaic_bench import taxonomy
    for mid in taxonomy.load().methods:
        assert canonical_method_id(mid) == mid
