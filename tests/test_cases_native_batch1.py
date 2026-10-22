"""Native T1 batch-1 cases (adb_c23 / adb_c02 / adb_c12 / adb_c04 /
adb_c18 / adb_c17): onboarding validation is clean, and each case's
central data-design invariant holds across a 30-seed spot check (the full 500-seed sweep
lives in each generator's __main__).

Loads each case directory directly (not registry.discover) so this file stays independent of
any other case directories in the dataset.
"""
import os

import pytest

from dmaic_bench.core import registry, validation

CASE_IDS = ("adb_c23", "adb_c02", "adb_c12", "adb_c04",
            "adb_c18", "adb_c17")
SEEDS = range(1, 31)


def _case(case_id):
    return registry.load_native_case(os.path.join(registry.CASES_DIR, case_id))


def _truth_map(data):
    return {(t.method_id, t.field): t.expected for t in data.truths}


@pytest.mark.parametrize("case_id", CASE_IDS)
def test_validation_clean(case_id):
    findings = validation.validate_case_dir(os.path.join(registry.CASES_DIR, case_id))
    assert validation.errors(findings) == []


def test_mini_msa_measurement_system_acceptable():
    case = _case("adb_c23")
    for seed in SEEDS:
        by = _truth_map(case.generate(seed))
        assert by[("msa.gage_rr_crossed", "percentStudyVariation")] < 30.0
        assert by[("msa.attribute_agreement", "kappaMin")] > 0.75


def test_mini_ttests_normal_baseline_with_significant_shifts():
    case = _case("adb_c02")
    for seed in SEEDS:
        by = _truth_map(case.generate(seed))
        assert by[("basic.normality", "pValue")] > 0.10  # parametric gate determinate
        assert by[("basic.two_sample_t", "pValue")] < 0.01


def test_mini_proportions_power_in_range_and_improvement_real():
    case = _case("adb_c12")
    for seed in SEEDS:
        data = case.generate(seed)
        by = _truth_map(data)
        assert 0.5 < by[("power.two_proportions", "power")] < 0.999
        baseline = data.blocks["P_OneProp"]["events"] / data.blocks["P_OneProp"]["trials"]
        assert by[("capability.binomial", "avgP")] < baseline


def test_mini_anova_homogeneity_holds_and_furnace_effect_significant():
    case = _case("adb_c04")
    for seed in SEEDS:
        by = _truth_map(case.generate(seed))
        assert by[("anova.equal_variances", "pValue")] > 0.05
        assert by[("anova.oneway", "factorPValue")] < 0.01


def test_mini_capability_in_control_and_worst_station_below_overall():
    case = _case("adb_c18")
    for seed in SEEDS:
        data = case.generate(seed)
        by = _truth_map(data)
        series = data.blocks["C_IMR"]["data"]
        assert all(by[("control_chart.imr", "individualsLCL")] - 0.5 < x
                   < by[("control_chart.imr", "individualsUCL")] + 0.5 for x in series)
        assert by[("capability.grouped", "ppk")] < by[("capability.normal", "ppk")]


def test_mini_attribute_charts_overdispersion_determinate():
    case = _case("adb_c17")
    for seed in SEEDS:
        by = _truth_map(case.generate(seed))
        assert by[("control_chart.laney_p", "sigmaZ")] > 1.5
        assert 0.01 < by[("control_chart.p", "centerLine")] < 0.15
