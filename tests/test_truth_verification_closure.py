"""V7 verification-closure tests.

Two things are guarded here:

1.  The reference implementations added to close the V7 gap — SPC constants, the eleven
    control charts, within-subgroup capability, the DOE layer — compute what they say they
    compute. The SPC constants are checked against the PUBLISHED table (AIAG SPC-2 Appendix;
    Montgomery ISQC 6e Appendix VI) precisely because this module derives them by numerical
    integration instead of hardcoding them: the integral is the definition, the table is the
    independent check.

2.  The gate no longer skips silently, and its COVERAGE CANNOT SILENTLY FALL. The corpus test
    at the bottom pins both the verified fraction and the exact identity of every truth the
    gate still cannot re-derive. Closing a gap or opening one both fail that test until
    somebody updates it on purpose — which is the whole point: the previous 66.8% was invisible
    because nothing anywhere asserted a number.
"""
from __future__ import annotations

import math

import numpy as np
import pytest

from dmaic_bench.core import registry, validation
from dmaic_bench.core.models import (Case, CaseData, CaseMeta, Stage, StageMethod,
                                         TruthEntry)
from dmaic_bench.truth import verifiers as V


# --------------------------------------------------------------------------- SPC constants

#: n -> (d2, d3, c4, A2, A3, D3, D4, B3, B4) exactly as printed in the AIAG SPC-2 /
#: Montgomery ISQC 6e control-chart constant tables. Four decimals is the table's precision.
PUBLISHED_CONSTANTS = {
    2:  (1.1284, 0.8525, 0.7979, 1.8800, 2.6587, 0.0000, 3.2665, 0.0000, 3.2665),
    3:  (1.6926, 0.8884, 0.8862, 1.0233, 1.9544, 0.0000, 2.5746, 0.0000, 2.5682),
    4:  (2.0588, 0.8798, 0.9213, 0.7286, 1.6281, 0.0000, 2.2821, 0.0000, 2.2660),
    5:  (2.3259, 0.8641, 0.9400, 0.5768, 1.4273, 0.0000, 2.1145, 0.0000, 2.0890),
    6:  (2.5344, 0.8480, 0.9515, 0.4832, 1.2871, 0.0000, 2.0038, 0.0304, 1.9696),
    7:  (2.7044, 0.8332, 0.9594, 0.4193, 1.1819, 0.0757, 1.9243, 0.1177, 1.8823),
    8:  (2.8472, 0.8198, 0.9650, 0.3725, 1.0991, 0.1362, 1.8638, 0.1851, 1.8149),
    9:  (2.9700, 0.8078, 0.9693, 0.3367, 1.0317, 0.1840, 1.8160, 0.2391, 1.7609),
    10: (3.0775, 0.7971, 0.9727, 0.3083, 0.9754, 0.2230, 1.7770, 0.2837, 1.7163),
}


class TestSpcConstants:
    @pytest.mark.parametrize("n", sorted(PUBLISHED_CONSTANTS))
    def test_quadrature_reproduces_the_published_table(self, n):
        d2, d3, c4, a2, a3, dd3, dd4, b3, b4 = PUBLISHED_CONSTANTS[n]
        assert V.d2(n) == pytest.approx(d2, abs=5e-5)
        assert V.d3(n) == pytest.approx(d3, abs=5e-5)
        assert V.c4(n) == pytest.approx(c4, abs=5e-5)
        assert V.A2(n) == pytest.approx(a2, abs=5e-5)
        assert V.A3(n) == pytest.approx(a3, abs=5e-5)
        assert V.D3(n) == pytest.approx(dd3, abs=5e-5)
        assert V.D4(n) == pytest.approx(dd4, abs=5e-5)
        assert V.B3(n) == pytest.approx(b3, abs=5e-5)
        assert V.B4(n) == pytest.approx(b4, abs=5e-5)

    def test_d2_is_the_expected_range_of_n_normals(self):
        """Monte-Carlo cross-check of the quadrature against the quantity it is meant to be."""
        rng = np.random.default_rng(20260904)
        for n in (2, 5, 8):
            draws = rng.standard_normal((400_000, n))
            assert float(np.mean(np.ptp(draws, axis=1))) == pytest.approx(V.d2(n), abs=0.01)

    def test_e2_is_three_over_d2(self):
        assert V.E2(2) == pytest.approx(3.0 / V.d2(2))
        assert V.E2(2) == pytest.approx(2.6587, abs=5e-5)

    def test_a_subgroup_of_one_is_refused_not_defaulted(self):
        for fn in (V.d2, V.d3, V.c4):
            with pytest.raises(V.NotVerifiable):
                fn(1)


# --------------------------------------------------------------------------- control charts

class TestVariablesControlCharts:
    def test_imr_limits_are_xbar_plus_minus_three_mrbar_over_d2(self):
        x = [10.0, 12.0, 11.0, 13.0, 9.0, 11.0, 12.0, 10.0]
        out = V.control_chart_imr({"data": x})
        mrbar = float(np.mean(np.abs(np.diff(x))))
        sigma = mrbar / V.d2(2)
        assert out["centerLine"] == pytest.approx(np.mean(x))
        assert out["individualsUCL"] == pytest.approx(np.mean(x) + 3 * sigma)
        assert out["individualsLCL"] == pytest.approx(np.mean(x) - 3 * sigma)
        assert out["movingRangeCenterLine"] == pytest.approx(mrbar)
        assert out["movingRangeUCL"] == pytest.approx(V.D4(2) * mrbar)
        assert out["movingRangeLCL"] == pytest.approx(0.0)

    def test_imr_flags_only_points_outside_the_limits(self):
        x = [10.0] * 12 + [10.5, 9.5, 40.0]
        out = V.control_chart_imr({"data": x})
        assert out["flaggedCount"] == 1.0

    def test_xbar_r_centre_line_is_the_grand_mean_and_limits_use_a2(self):
        g = [[1.0, 2.0, 3.0], [2.0, 3.0, 4.0], [0.0, 1.0, 2.0], [3.0, 4.0, 5.0]]
        out = V.control_chart_xbar_r({"data": g})
        flat = np.array(g, float)
        rbar = float(np.mean(np.ptp(flat, axis=1)))
        assert out["xBarChartCenterLine"] == pytest.approx(flat.mean())
        assert out["xBarUCL"] == pytest.approx(flat.mean() + V.A2(3) * rbar)
        assert out["rUCL"] == pytest.approx(V.D4(3) * rbar)
        assert out["sigmaWithin"] == pytest.approx(rbar / V.d2(3))

    def test_xbar_s_uses_a3_and_sbar_over_c4(self):
        g = [[1.0, 2.0, 3.0, 4.0], [2.0, 3.0, 4.0, 5.0], [0.0, 2.0, 3.0, 4.0]]
        out = V.control_chart_xbar_s({"data": g})
        flat = np.array(g, float)
        sbar = float(np.mean(flat.std(axis=1, ddof=1)))
        assert out["xBarChartCenterLine"] == pytest.approx(flat.mean())
        assert out["xBarUCL"] == pytest.approx(flat.mean() + V.A3(4) * sbar)
        assert out["sUCL"] == pytest.approx(V.B4(4) * sbar)
        assert out["sigmaWithin"] == pytest.approx(sbar / V.c4(4))

    def test_a_flat_series_that_does_not_divide_is_refused_not_truncated(self):
        with pytest.raises(V.NotVerifiable, match="do not split"):
            V.control_chart_xbar_r({"data": list(range(11)), "subgroupSize": 5})

    def test_flat_and_nested_subgroups_agree(self):
        flat = {"data": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0], "subgroupSize": 2}
        nested = {"data": [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]]}
        assert (V.control_chart_xbar_r(flat)["xBarChartCenterLine"]
                == pytest.approx(V.control_chart_xbar_r(nested)["xBarChartCenterLine"]))

    def test_ewma_centres_on_the_declared_target_not_the_sample_mean(self):
        x = [10.0, 11.0, 9.0, 10.5, 9.5, 10.0, 11.0, 9.0]
        assert V.control_chart_ewma({"data": x, "target": 5.0, "ewmaWeight": 0.2}
                                    )["centerLine"] == 5.0
        assert V.control_chart_ewma({"data": x, "ewmaWeight": 0.2}
                                    )["centerLine"] == pytest.approx(np.mean(x))

    def test_ewma_limits_widen_to_the_steady_state_value(self):
        x = list(np.linspace(9.0, 11.0, 40))
        out = V.control_chart_ewma({"data": x, "target": 10.0, "ewmaWeight": 0.2})
        lam, sigma = 0.2, out["sigmaWithin"]
        assert out["steadyStateUCL"] == pytest.approx(
            10.0 + 3 * sigma * math.sqrt(lam / (2 - lam)))

    def test_ewma_refuses_a_weight_outside_the_unit_interval(self):
        with pytest.raises(V.NotVerifiable, match="outside"):
            V.control_chart_ewma({"data": [1.0, 2.0, 3.0], "ewmaWeight": 1.5})

    def test_cusum_accumulates_a_sustained_shift_and_flags_it(self):
        x = [10.0] * 10 + [10.2, 9.8] * 3 + [20.0] * 8
        out = V.control_chart_cusum({"data": x, "target": 10.0, "kValue": 0.5, "hValue": 4.0})
        assert out["flaggedCount"] > 0
        assert out["maxCusumPlus"] > out["decisionInterval"]

    def test_cusum_on_an_on_target_series_flags_nothing(self):
        rng = np.random.default_rng(7)
        x = 10.0 + rng.standard_normal(60) * 0.05
        x = x - x.mean() + 10.0          # exactly on target: nothing for the arms to accumulate
        out = V.control_chart_cusum({"data": x.tolist(), "target": 10.0,
                                     "kValue": 0.5, "hValue": 4.0})
        assert out["flaggedCount"] == 0.0

    def test_cusum_flags_a_small_sustained_offset_from_target(self):
        """A series that is stable but sits 0.23 sigma off the DECLARED target is exactly
        what a k=0.5 / h=4 CUSUM exists to catch — the individuals chart would not see it."""
        rng = np.random.default_rng(7)
        x = 10.0 + rng.standard_normal(60) * 0.05
        x = x - x.mean() + 9.99
        out = V.control_chart_cusum({"data": x.tolist(), "target": 10.0,
                                     "kValue": 0.5, "hValue": 4.0})
        assert out["flaggedCount"] > 0
        assert V.control_chart_imr({"data": x.tolist()})["flaggedCount"] == 0.0


class TestAttributeControlCharts:
    def test_p_chart_centre_line_is_the_pooled_not_the_averaged_proportion(self):
        payload = {"defectCounts": [1, 10], "sampleSizes": [10, 1000]}
        out = V.control_chart_p(payload)
        assert out["centerLine"] == pytest.approx(11 / 1010)
        assert out["centerLine"] != pytest.approx(np.mean([1 / 10, 10 / 1000]))

    def test_np_chart_requires_a_constant_subgroup_size(self):
        with pytest.raises(V.NotVerifiable, match="constant subgroup size"):
            V.control_chart_np({"defectCounts": [1, 2, 3], "sampleSizes": [10, 20, 30]})

    def test_np_chart_centre_line_is_n_pbar(self):
        out = V.control_chart_np({"defectCounts": [2, 4, 6], "sampleSize": 100})
        assert out["pBar"] == pytest.approx(12 / 300)
        assert out["centerLine"] == pytest.approx(4.0)
        assert out["ucl"] == pytest.approx(4.0 + 3 * math.sqrt(100 * 0.04 * 0.96))

    def test_c_chart_limits_are_cbar_plus_minus_three_root_cbar(self):
        out = V.control_chart_c({"defectCounts": [4, 6, 5, 9, 6]})
        assert out["centerLine"] == pytest.approx(6.0)
        assert out["ucl"] == pytest.approx(6.0 + 3 * math.sqrt(6.0))
        assert out["lcl"] == pytest.approx(max(6.0 - 3 * math.sqrt(6.0), 0.0))

    def test_c_chart_lcl_is_floored_at_zero(self):
        assert V.control_chart_c({"defectCounts": [1, 0, 2, 1]})["lcl"] == 0.0

    def test_u_chart_centre_line_is_pooled_dpu(self):
        out = V.control_chart_u({"defectCounts": [4, 6], "unitCounts": [40, 60]})
        assert out["processMean"] == pytest.approx(10 / 100)


    def test_a_p_chart_ucl_cannot_exceed_one(self):
        out = V.control_chart_p({"defectCounts": [8, 9, 7, 10], "sampleSizes": [10] * 4})
        assert out["meanUCL"] <= 1.0

    def test_defects_mislabelled_as_defectives_are_refused(self):
        with pytest.raises(V.NotVerifiable, match="DEFECTIVES"):
            V.control_chart_p({"defectCounts": [12, 3, 4], "sampleSizes": [10, 10, 10]})

    def test_a_degenerate_constant_series_is_refused_not_charted(self):
        with pytest.raises(V.NotVerifiable, match="degenerate"):
            V.control_chart_imr({"data": [5.0] * 20})

    def test_laney_sigma_z_is_one_when_dispersion_is_binomial(self):
        """A p chart whose z-series is a pure random walk of unit steps has sigma_Z ~ 1."""
        rng = np.random.default_rng(11)
        n = np.full(400, 2000)
        c = rng.binomial(2000, 0.05, size=400)
        out = V.control_chart_laney_p({"defectCounts": c.tolist(), "sampleSizes": n.tolist()})
        assert out["sigmaZ"] == pytest.approx(1.0, abs=0.08)

    def test_laney_sigma_z_exceeds_one_under_overdispersion(self):
        rng = np.random.default_rng(12)
        p = rng.uniform(0.02, 0.12, size=200)          # batch-to-batch drift
        c = rng.binomial(3000, p)
        out = V.control_chart_laney_p({"defectCounts": c.tolist(),
                                       "sampleSizes": [3000] * 200})
        assert out["sigmaZ"] > 2.0

    def test_laney_u_matches_the_hand_computation(self):
        payload = {"defectCounts": [4, 9, 2, 7, 5], "unitCounts": [40, 45, 38, 50, 42]}
        out = V.control_chart_laney_u(payload)
        c = np.array(payload["defectCounts"], float)
        n = np.array(payload["unitCounts"], float)
        ubar = c.sum() / n.sum()
        z = (c / n - ubar) / np.sqrt(ubar / n)
        assert out["sigmaZ"] == pytest.approx(np.mean(np.abs(np.diff(z))) / V.d2(2))


class TestRunRules:
    def test_flagged_count_is_test_one_only(self):
        """A shifted-but-in-limits series trips a Nelson zone test and no beyond-limit test.

        This is the whole reason the two counts are reported separately: ``flaggedCount``
        follows the corpus's own stated convention (points outside the limits), and reporting
        the stricter Nelson total under that name would make this reference disagree with
        correct truths."""
        rng = np.random.default_rng(21)
        x = 100.0 + rng.standard_normal(40)
        x[25:] += 1.2
        out = V.control_chart_imr({"data": x.tolist()})
        assert out["flaggedCount"] == 0.0
        assert out["nelsonFlaggedCount"] > 0.0

    def test_nine_on_one_side_is_test_two(self):
        v = [0.0, 10.0] * 6 + [6.0] * 9
        flags = V.nelson_flags(v, center=5.0, sigma=1.0)
        assert flags["nelsonTest2Count"] >= 9

    def test_six_increasing_is_test_three(self):
        flags = V.nelson_flags([0, 1, 2, 3, 4, 5, 6], center=3.0, sigma=10.0)
        assert flags["nelsonTest3Count"] >= 6
        assert flags["nelsonTest1Count"] == 0

    def test_fifteen_hugging_the_centre_is_test_seven(self):
        flags = V.nelson_flags([0.1, -0.1] * 10, center=0.0, sigma=1.0)
        assert flags["nelsonTest7Count"] >= 15

    def test_a_flat_series_trips_nothing_when_sigma_is_zero(self):
        flags = V.nelson_flags([1.0] * 20, center=1.0, sigma=0.0)
        assert flags["nelsonFlaggedCount"] == 0


# --------------------------------------------------------------------------- capability

class TestCapabilityWithinSigma:
    def test_cpk_is_emitted_and_uses_within_sigma(self):
        """The defect this closes: capability.normal returned pp/ppk only, so every cpk truth
        in the corpus fell through the gate as 'field not produced'."""
        rng = np.random.default_rng(3)
        x = (100.0 + np.repeat(rng.standard_normal(20) * 2.0, 5)
             + rng.standard_normal(100) * 0.3).tolist()   # strong between-subgroup drift
        out = V.capability_normal({"data": x, "lsl": 90.0, "usl": 110.0})
        assert "cpk" in out and "cp" in out
        assert out["sigmaWithin"] < out["sigmaOverall"]
        assert out["cpk"] > out["ppk"]                     # short-term sigma is the smaller one

    def test_within_sigma_of_an_ungrouped_series_is_mrbar_over_d2(self):
        x = [10.0, 12.0, 11.0, 13.0, 9.0, 11.0]
        out = V.capability_normal({"data": x, "lsl": 0.0, "usl": 20.0})
        assert out["sigmaWithin"] == pytest.approx(
            float(np.mean(np.abs(np.diff(x)))) / V.d2(2))

    def test_small_subgroups_use_rbar_over_d2(self):
        """House rule, docs/archive/control-phase-design-2026-09-04.md §4.1: R-bar/d2 for 2 <= n <= 8."""
        g = [[10.0, 10.4, 9.8], [12.0, 12.3, 11.9], [8.0, 8.2, 7.7], [11.0, 11.4, 10.6]]
        out = V.capability_normal({"data": g, "lsl": 0.0, "usl": 20.0})
        arr = np.array(g, float)
        assert out["sigmaWithinMethod"] == "rBar"
        assert out["sigmaWithin"] == pytest.approx(
            float(np.mean(np.ptp(arr, axis=1))) / V.d2(3))

    def test_large_subgroups_use_sbar_over_c4(self):
        """House rule: s-bar/c4 once n >= 9, where the range loses efficiency."""
        rng = np.random.default_rng(4)
        arr = 10.0 + rng.standard_normal((6, 10))
        out = V.capability_normal({"data": arr.tolist(), "lsl": 0.0, "usl": 20.0})
        assert out["sigmaWithinMethod"] == "sBar"
        assert out["sigmaWithin"] == pytest.approx(
            float(np.mean(arr.std(axis=1, ddof=1))) / V.c4(10))

    def test_the_pooled_alternative_is_reported_not_discarded(self):
        g = [[10.0, 10.4, 9.8], [12.0, 12.3, 11.9], [8.0, 8.2, 7.7], [11.0, 11.4, 10.6]]
        out = V.capability_normal({"data": g, "lsl": 0.0, "usl": 20.0})
        arr = np.array(g, float)
        dof = arr.shape[0] * (arr.shape[1] - 1)
        s_p = math.sqrt(float(np.sum((arr.shape[1] - 1) * arr.var(axis=1, ddof=1))) / dof)
        assert out["sigmaWithinPooled"] == pytest.approx(s_p / V.c4(dof + 1))

    def test_pp_and_ppk_still_use_the_overall_sigma(self):
        x = [9.0, 11.0, 10.0, 12.0, 8.0, 10.0, 11.0, 9.0]
        out = V.capability_normal({"data": x, "lsl": 4.0, "usl": 16.0})
        sd = float(np.std(x, ddof=1))
        assert out["pp"] == pytest.approx(12.0 / (6 * sd))
        assert out["ppk"] == pytest.approx(min((16 - np.mean(x)) / (3 * sd),
                                               (np.mean(x) - 4) / (3 * sd)))

    def test_one_sided_specs_give_only_the_one_sided_indices(self):
        out = V.capability_normal({"data": [1.0, 2.0, 3.0, 2.0, 1.5], "usl": 10.0})
        assert "cpu" in out and "cpl" not in out and "cp" not in out
        assert out["cpk"] == out["cpu"]

    def test_no_spec_limit_refuses(self):
        with pytest.raises(V.NotVerifiable, match="spec limits"):
            V.capability_normal({"data": [1.0, 2.0, 3.0]})


class TestCapabilityGroupedAndNonNormal:
    def test_grouped_ppk_is_the_worst_group(self):
        payload = {"groups": {"a": [10.0, 10.1, 9.9, 10.05],
                              "b": [10.0, 12.0, 8.0, 11.0]},
                   "lsl": 5.0, "usl": 15.0}
        out = V.capability_grouped(payload)
        assert out["ppk"] == out["ppkWorstGroup"] < out["ppkBest"]

    def test_grouped_deliberately_does_not_emit_cpk(self):
        """Group strata carry no time order, so a within-subgroup sigma is not identified.
        Emitting a cpk here would be an invented number wearing a reference value's clothes;
        the V7 gate reports the absence as a named warning instead."""
        out = V.capability_grouped({"groups": {"a": [1.0, 2.0, 3.0], "b": [2.0, 3.0, 4.0]},
                                    "lsl": 0.0, "usl": 6.0})
        assert "cpk" not in out

    def test_grouped_refuses_a_single_group(self):
        with pytest.raises(V.NotVerifiable, match=">=2 groups"):
            V.capability_grouped({"groups": {"a": [1.0, 2.0]}, "lsl": 0.0, "usl": 5.0})

    def test_nonnormal_uses_percentiles_not_sigma(self):
        rng = np.random.default_rng(5)
        x = rng.lognormal(1.0, 0.5, size=200).tolist()
        out = V.capability_nonnormal({"data": x, "usl": 30.0,
                                      "autoSelectDistribution": True})
        assert out["ppu"] == pytest.approx((30.0 - out["median"])
                                           / (out["p99865"] - out["median"]))

    def test_distribution_selection_is_by_anderson_darling_not_log_likelihood(self):
        """Regression guard for a MEASURED defect.

        On adb_c06 seed 3, ranking the candidate distributions by log-likelihood puts gamma
        0.09 nats ahead of lognormal and yields Ppk = 1.369 against a lognormal-derived truth
        of 0.993 — a 38% error produced purely by the selection rule. Anderson-Darling, which
        is what a Minitab-family ``autoSelectDistribution`` means, ranks lognormal first on
        every seed. The truth was right; the first verifier was wrong.
        """
        case = registry.discover()["adb_c06"]
        for seed in (1, 2, 3):
            data = case.generate(seed)
            out = V.capability_nonnormal(data.blocks["CC_NonnormalCap"])
            truth = next(t for t in data.truths if t.method_id == "capability.nonnormal")
            assert out["selectedDistribution"] == "lognormal"
            assert out["ppk"] == pytest.approx(truth.expected, abs=truth.tol)
        # and the near-tie that makes the guard necessary is real, not hypothetical
        out3 = V.capability_nonnormal(case.generate(3).blocks["CC_NonnormalCap"])
        assert out3["runnerUpDistribution"] == "gamma"
        assert out3["runnerUpAD"] - out3["selectedDistributionAD"] < 0.1

    def test_an_explicitly_named_distribution_overrides_selection(self):
        rng = np.random.default_rng(5)
        x = rng.lognormal(1.0, 0.5, size=100).tolist()
        out = V.capability_nonnormal({"data": x, "usl": 30.0, "distribution": "weibull"})
        assert out["selectedDistribution"] == "weibull"

    def test_an_unsupported_distribution_is_refused_not_ignored(self):
        with pytest.raises(V.NotVerifiable, match="unsupported distribution"):
            V.capability_nonnormal({"data": [1.0, 2.0, 3.0, 4.0], "usl": 9.0,
                                    "distribution": "pearson6"})


# --------------------------------------------------------------------------- DOE

class TestDoeLayer:
    def test_prediction_interval_is_wider_than_the_confidence_interval(self):
        payload = {"data": {"A": [-1, 1, -1, 1, -1, 1], "B": [-1, -1, 1, 1, 0, 0],
                            "Y": [2.0, 4.0, 3.0, 6.0, 2.5, 5.0]},
                   "responseColumn": "Y", "termsInModel": ["A", "B"],
                   "predictionPoints": [{"A": 1, "B": 0}], "confidenceLevel": 0.95}
        out = V.doe_factorial_prediction(payload)
        assert out["piUpper"] - out["piLower"] > out["ciUpper"] - out["ciLower"]
        assert out["ciLower"] < out["predictedValue"] < out["ciUpper"]

    def test_a_multi_point_prediction_is_refused_rather_than_guessed(self):
        payload = {"data": {"A": [-1, 1, -1, 1], "Y": [1.0, 2.0, 1.5, 2.5]},
                   "responseColumn": "Y", "termsInModel": ["A"],
                   "predictionPoints": [{"A": 1}, {"A": -1}]}
        with pytest.raises(V.NotVerifiable, match="does not say which one"):
            V.doe_factorial_prediction(payload)

    def test_model_from_needs_the_sibling_blocks_and_says_so(self):
        with pytest.raises(V.NotVerifiable, match="was not supplied"):
            V.doe_factorial_prediction({"model_from": "D_Analyze", "settings": {"A": 1}})

    def test_model_from_refits_the_referenced_stage(self):
        data = registry.discover()["adb_c11"].generate(1)
        out = V.doe_factorial_prediction(data.blocks["D_Predict"], data.blocks)
        truth = next(t for t in data.truths
                     if t.method_id == "doe.factorial_prediction"
                     and t.field == "predictedValue")
        assert out["predictedValue"] == pytest.approx(truth.expected, abs=truth.tol)

    def test_the_prediction_verifier_declares_that_it_wants_blocks(self):
        assert V.wants_blocks(V.REFERENCE_IMPLS["doe.factorial_prediction"])
        assert not V.wants_blocks(V.REFERENCE_IMPLS["control_chart.imr"])

    def test_rsm_fits_the_full_quadratic_and_finds_the_interior_optimum(self):
        """A concave surface with its stationary point inside the bounds: the constrained
        maximum IS the stationary point, which the closed form and the search must agree on."""
        pts = []
        for x1 in (-1.0, 0.0, 1.0):
            for x2 in (-1.0, 0.0, 1.0):
                pts.append({"x1": x1, "x2": x2,
                            "y": 50.0 - 2 * (x1 - 0.25) ** 2 - 3 * (x2 + 0.5) ** 2})
        analysis = V.doe_rsm_analysis({"runs": pts})
        assert analysis["rSquaredPct"] == pytest.approx(100.0, abs=1e-6)
        opt = V.doe_rsm_optimizer({"surface_data": pts, "goal": "maximize",
                                   "bounds": [[-1.0, 1.0], [-1.0, 1.0]]})
        assert opt["predictedResponse"] == pytest.approx(50.0, abs=1e-6)
        assert opt["optimal_x1"] == pytest.approx(0.25, abs=1e-4)
        assert opt["optimal_x2"] == pytest.approx(-0.5, abs=1e-4)
        canon = V.doe_rsm_canonical({"runs": pts})
        assert canon["predictedAtStationary"] == pytest.approx(50.0, abs=1e-6)
        assert canon["maxEigenvalue"] < 0                     # concave => a maximum

    def test_minimise_finds_the_other_end(self):
        pts = [{"x1": a, "x2": b, "y": (a - 0.3) ** 2 + (b + 0.2) ** 2}
               for a in (-1.0, 0.0, 1.0) for b in (-1.0, 0.0, 1.0)]
        opt = V.doe_rsm_optimizer({"surface_data": pts, "goal": "minimize",
                                   "bounds": [[-1.0, 1.0], [-1.0, 1.0]]})
        assert opt["optimal_x1"] == pytest.approx(0.3, abs=1e-4)
        assert opt["predictedResponse"] == pytest.approx(0.0, abs=1e-6)

    def test_an_unsupported_goal_is_refused(self):
        pts = [{"x1": a, "x2": b, "y": a + b}
               for a in (-1.0, 0.0, 1.0) for b in (-1.0, 0.0, 1.0)]
        with pytest.raises(V.NotVerifiable, match="unsupported goal"):
            V.doe_rsm_optimizer({"surface_data": pts, "goal": "satisfy",
                                 "bounds": [[-1, 1], [-1, 1]]})

    def test_lack_of_fit_needs_replicates_and_is_omitted_without_them(self):
        pts = [{"x1": a, "x2": b, "y": a + 2 * b + 0.1 * a * b}
               for a in (-1.0, 0.0, 1.0) for b in (-1.0, 0.0, 1.0)]
        assert "lackOfFitPValue" not in V.doe_rsm_analysis({"runs": pts})


# --------------------------------------------------------------------------- misc verifiers

class TestOtherClosures:
    def test_normality_now_emits_the_statistic_the_corpus_binds(self):
        out = V.normality({"data": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]})
        assert "statistic" in out and "pValue" in out
        assert out["statistic"] == pytest.approx(out["adStatistic"])

    def test_fmea_rpn_is_severity_times_occurrence_times_detection(self):
        out = V.fmea_rpn({"items": [{"severity": 8, "occurrence": 7, "detection": 6},
                                    {"severity": 2, "occurrence": 2, "detection": 2}]})
        assert out["maxRpn"] == 336.0
        assert out["totalRpn"] == 344.0

    def test_fmea_invents_no_threshold(self):
        out = V.fmea_rpn({"items": [{"severity": 5, "occurrence": 5, "detection": 5}]})
        assert "aboveThresholdCount" not in out
        out2 = V.fmea_rpn({"items": [{"severity": 5, "occurrence": 5, "detection": 5}],
                           "rpnThreshold": 100})
        assert out2["aboveThresholdCount"] == 1.0

    def test_binary_logistic_reports_the_likelihood_ratio_p_value(self):
        rng = np.random.default_rng(9)
        x = rng.uniform(0, 30, size=200)
        y = (rng.uniform(size=200) < 1 / (1 + np.exp(-(x - 15) / 3))).astype(int)
        out = V.binary_logistic({"x": x.tolist(), "outcomes": y.tolist()})
        assert out["modelPValue"] < 1e-6
        assert out["llrStatistic"] > 0

    def test_binary_logistic_refuses_a_degenerate_response(self):
        with pytest.raises(V.NotVerifiable, match="non-degenerate"):
            V.binary_logistic({"x": [1.0, 2.0, 3.0, 4.0], "outcomes": [1, 1, 1, 1]})

    def test_anova_sov_total_variance_is_the_pooled_sample_variance(self):
        payload = {"groups": {"a": [1.0, 2.0, 3.0], "b": [7.0, 8.0, 9.0]}}
        out = V.anova_sov(payload)
        assert out["totalVariance"] == pytest.approx(
            float(np.var([1, 2, 3, 7, 8, 9], ddof=1)))
        assert out["betweenVariance"] > out["withinVariance"]

    def test_negative_variance_components_are_floored_at_zero(self):
        payload = {"groups": {"a": [1.0, 9.0, 2.0, 8.0], "b": [1.5, 8.5, 2.5, 7.5]}}
        assert V.anova_sov(payload)["betweenVariance"] >= 0.0

    def test_a_flat_gage_list_needs_declared_dimensions(self):
        with pytest.raises(V.NotVerifiable, match="numParts"):
            V.gage_rr_crossed({"measurements": [1.0] * 60})

    def test_a_flat_gage_list_that_does_not_fill_the_design_is_refused(self):
        with pytest.raises(V.NotVerifiable, match="do not fill"):
            V.gage_rr_crossed({"measurements": [1.0] * 59, "numParts": 10,
                               "numOperators": 3, "numReplicates": 2})

    def test_the_flat_gage_layout_is_operator_major(self):
        """Identified, not assumed: only operator-major reproduces adb_c05/M_GRR_4's stored
        %StudyVariation of 6.76 (as 6.765); part-major gives 94.6."""
        cases = registry.discover()
        if "adb_c05" not in cases:
            pytest.skip("held-out case adb_c05 absent (public release) -- see docs/HELD_OUT.md")
        data = cases["adb_c05"].generate(1)
        out = V.gage_rr_crossed(data.blocks["M_GRR_4"])
        assert out["percentStudyVariation"] == pytest.approx(6.765, abs=0.01)

    def test_a_json_string_payload_is_unwrapped(self):
        payload = {"label": "x", "text": '{"Yield": [1,2,3,4,5,6,7,8,9],'
                                         ' "Speed": ["a","a","a","b","b","b","c","c","c"]}'}
        groups = V._all_groups(payload)
        assert [list(g) for g in groups] == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_two_continuous_columns_are_refused_rather_than_guessed(self):
        with pytest.raises(V.NotVerifiable, match="refusing to guess"):
            V._inferred_long_format({"x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                                     "y": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0]})

    def test_three_columns_are_refused(self):
        with pytest.raises(V.NotVerifiable, match="exactly 2 columns"):
            V._inferred_long_format({"a": [1.0] * 6, "b": [2.0] * 6, "c": [3.0] * 6})


# --------------------------------------------------------------------------- the gate itself

def _mini_case(truths, blocks=None, methods=("basic.descriptive_summary",)):
    stages = tuple(Stage(stage_id=f"S{i}", phase="measure", label=f"S{i}",
                         methods=(StageMethod(method_id=m),))
                   for i, m in enumerate(methods))
    meta = CaseMeta(case_id="unit_case", title="t", tier="T1", industry="x",
                    provenance="SIMULATED", y_type="continuous",
                    context="A batch of data.", goal="Report the conclusion.", stages=stages,
                    parametric=False, schema_version=1)
    blocks = blocks if blocks is not None else {
        s.stage_id: {"data": [1.0, 2.0, 3.0, 4.0, 5.0]} for s in stages}
    return Case(meta=meta,
                generate=lambda seed: CaseData(seed=seed, blocks=blocks, truths=truths))


class TestGateReportsWhatItCannotCheck:
    def test_a_method_with_no_reference_impl_produces_a_named_warning(self):
        t = TruthEntry(method_id="msa.linearity_bias", field="bias", expected=1.0, tol=0.1,
                       stage_id="S0", derivation="d")
        case = _mini_case((t,), methods=("msa.linearity_bias",))
        findings = validation.validate_case(case)
        warns = [f for f in findings if f.check == "V7-unverified"]
        assert len(warns) == 1
        assert "msa.linearity_bias" in warns[0].message and "bias" in warns[0].message
        assert "no_reference_impl" in warns[0].message
        assert warns[0].severity == "WARN"          # not an ERROR yet, but never silent

    def test_a_field_the_reference_does_not_emit_produces_a_named_warning(self):
        t = TruthEntry(method_id="basic.descriptive_summary", field="kurtosis",
                       expected=1.0, tol=0.1, stage_id="S0", derivation="d")
        findings = validation.validate_case(_mini_case((t,)))
        warns = [f for f in findings if f.check == "V7-unverified"]
        assert len(warns) == 1 and "field_not_emitted" in warns[0].message

    def test_an_unreadable_payload_produces_a_named_warning(self):
        t = TruthEntry(method_id="basic.descriptive_summary", field="mean",
                       expected=1.0, tol=0.1, stage_id="S0", derivation="d")
        case = _mini_case((t,), blocks={"S0": {"unrelated": "no series here at all"}})
        warns = [f for f in validation.validate_case(case) if f.check == "V7-unverified"]
        assert len(warns) == 1 and "payload_unrecognized" in warns[0].message

    def test_every_case_reports_a_coverage_line(self):
        findings = validation.validate_case(_mini_case(()))
        cov = [f for f in findings if f.check == "V7-coverage"]
        assert len(cov) == 1 and cov[0].severity == "INFO"

    def test_a_real_mismatch_is_still_an_error(self):
        t = TruthEntry(method_id="basic.descriptive_summary", field="mean",
                       expected=99.0, tol=0.01, stage_id="S0", derivation="d")
        errs = validation.errors(validation.validate_case(_mini_case((t,))))
        assert any(f.check == "V7-verify" for f in errs)

    def test_a_correct_truth_verifies(self):
        t = TruthEntry(method_id="basic.descriptive_summary", field="mean",
                       expected=3.0, tol=1e-9, stage_id="S0", derivation="d")
        recs = validation.verification_coverage(_mini_case((t,)))
        assert [r.status for r in recs] == ["verified"]
        assert validation.verified_fraction(recs) == (1, 1, 1.0)

    def test_verified_fraction_of_an_empty_case_is_one(self):
        assert validation.verified_fraction([]) == (0, 0, 1.0)

    def test_an_unanchored_truth_is_resolved_only_against_declaring_stages(self):
        t = TruthEntry(method_id="basic.descriptive_summary", field="mean",
                       expected=30.0, tol=1e-9, stage_id=None, derivation="d")
        case = _mini_case(
            (t,),
            blocks={"S0": {"data": [1.0, 2.0, 3.0]}, "S1": {"data": [10.0, 30.0, 50.0]}},
            methods=("basic.descriptive_summary", "basic.descriptive_summary"))
        findings = validation.validate_case(case)
        assert not validation.errors(findings)
        amb = [f for f in findings if f.check == "V7-ambiguous"]
        assert len(amb) == 1 and "S0" in amb[0].message and "S1" in amb[0].message

    def test_an_unanchored_truth_with_no_host_stage_is_reported_as_orphaned(self):
        t = TruthEntry(method_id="basic.two_proportions", field="pValue", expected=0.0,
                       tol=0.001, stage_id=None, derivation="d")
        recs = validation.verification_coverage(_mini_case((t,)))
        assert recs[0].status == "no_block"
        assert "no stage declares" in recs[0].detail

    def test_a_reference_crash_is_an_error_not_a_skip(self):
        boom = lambda payload: (_ for _ in ()).throw(RuntimeError("boom"))
        V.REFERENCE_IMPLS["unit.boom"] = boom
        try:
            t = TruthEntry(method_id="unit.boom", field="x", expected=1.0, tol=0.1,
                           stage_id="S0", derivation="d")
            case = _mini_case((t,), methods=("unit.boom",))
            recs = validation.verification_coverage(case)
            assert recs[0].status == "reference_crash"
        finally:
            V.REFERENCE_IMPLS.pop("unit.boom")


class TestStageBindingRule:
    """V10 — the latent NF defect, gated at onboarding."""

    def _two_stage_case(self, fields_a, fields_b):
        truths = tuple(
            TruthEntry(method_id="capability.normal", field=f, expected=1.0, tol=99.0,
                       stage_id=sid, soft=True, derivation="d")
            for sid, fields in (("S0", fields_a), ("S1", fields_b)) for f in fields)
        blocks = {"S0": {"data": [1.0, 2.0, 3.0, 2.0], "lsl": 0.0, "usl": 5.0},
                  "S1": {"data": [1.0, 2.0, 3.0, 2.5], "lsl": 0.0, "usl": 5.0}}
        return _mini_case(truths, blocks=blocks,
                          methods=("capability.normal", "capability.normal"))

    def test_the_same_method_and_field_at_two_stages_is_warned_not_blocked(self):
        """Downgraded deliberately: `nf.check_values` can now score this, so it is a smell.

        While `merged_outputs` merged last-wins, two truths on one method were genuinely
        unscoreable and ERROR was right. The scorer now matches a multi-truth method
        step-by-step and claims each step once, so both can score — as long as the contestant
        reports each analysis as its own step. That residual constraint is what the warning
        is for. `test_two_stage_truths_are_now_actually_scoreable` below is the other half:
        without it, downgrading this would just be weakening a check.
        """
        case = self._two_stage_case(["ppk"], ["ppk"])
        findings = validation.validate_case(case)
        assert not [f for f in validation.errors(findings) if f.check == "V10-stage-binding"]
        warns = [f for f in findings
                 if f.check == "V10-stage-binding" and f.severity == "WARN"]
        assert warns, "the constraint on trace shape must still be reported"
        assert "capability.normal" in warns[0].message and "ppk" in warns[0].message

    def test_two_stage_truths_are_now_actually_scoreable(self):
        """The claim the downgrade above rests on, measured through the real scorer."""
        from types import SimpleNamespace as NS

        from dmaic_bench.scoring import nf as nf_mod
        truths = (TruthEntry(method_id="regression.ols", field="rSquaredAdjPct",
                             expected=93.84, tol=1.5, stage_id="S0", derivation="d"),
                  TruthEntry(method_id="regression.ols", field="rSquaredAdjPct",
                             expected=98.21, tol=1.5, stage_id="S1", derivation="d"))
        step = lambda v: NS(method_id="regression.ols", status="success",
                            outputs={"rSquaredAdjPct": v})
        det = nf_mod.check_values(NS(truths=truths), NS(steps=[step(93.9), step(98.2)]))
        assert [d["status"] for d in det] == ["passed", "passed"], det
        # Reporting order must not matter, and one number must not satisfy two truths.
        det = nf_mod.check_values(NS(truths=truths), NS(steps=[step(98.2), step(93.9)]))
        assert [d["status"] for d in det] == ["passed", "passed"], det
        det = nf_mod.check_values(NS(truths=truths), NS(steps=[step(93.9), step(93.9)]))
        assert sorted(d["status"] for d in det) == ["failed", "passed"], det

    def test_disjoint_field_sets_at_two_stages_are_allowed(self):
        case = self._two_stage_case(["ppk"], ["pp"])
        findings = validation.validate_case(case)
        assert not [f for f in validation.errors(findings)
                    if f.check == "V10-stage-binding"]
        assert [f for f in findings
                if f.check == "V10-stage-binding" and f.severity == "INFO"]

    def test_one_stage_per_method_says_nothing(self):
        case = _mini_case((TruthEntry(method_id="basic.descriptive_summary", field="mean",
                                      expected=3.0, tol=1e-9, stage_id="S0",
                                      derivation="d"),))
        assert not [f for f in validation.validate_case(case)
                    if f.check == "V10-stage-binding"]

    def test_two_different_values_for_one_method_field_are_flagged(self):
        """The same collision one level down. adb_c19 carries regression.ols.rSquaredAdjPct
        twice, 93.84 and 98.21, both with stage_id=None — a stage-keyed rule alone misses it,
        and the NF merge can satisfy at most one of the two."""
        truths = tuple(
            TruthEntry(method_id="regression.ols", field="rSquaredAdjPct", expected=v,
                       tol=1.0, stage_id=None, soft=True, derivation="d")
            for v in (93.84, 98.21))
        case = _mini_case(truths, methods=("regression.ols", "regression.ols"),
                          blocks={"S0": {"x": [1.0, 2.0, 3.0, 4.0], "y": [1.0, 2.1, 2.9, 4.2]},
                                  "S1": {"x": [1.0, 2.0, 3.0, 4.0], "y": [1.0, 2.0, 3.0, 4.1]}})
        hits = [f for f in validation.validate_case(case)
                if f.check == "V10-stage-binding"]
        assert len(hits) == 1 and hits[0].severity == "WARN"
        assert "93.84" in hits[0].message and "98.21" in hits[0].message

    def test_two_different_values_at_two_named_stages_are_warned(self):
        """Also downgraded, for the same measured reason, and reported rather than dropped.

        Two stage-anchored values on one method+field constrain the contestant's trace shape:
        they separate only if each analysis is its own step. That is worth reporting and no
        longer worth blocking on, because the scorer resolves it —
        `test_two_stage_truths_are_now_actually_scoreable` proves it does.
        """
        truths = tuple(
            TruthEntry(method_id="capability.normal", field="ppk", expected=v, tol=0.01,
                       stage_id=sid, soft=True, derivation="d")
            for sid, v in (("S0", 1.0), ("S1", 2.0)))
        case = _mini_case(truths, methods=("capability.normal", "capability.normal"),
                          blocks={"S0": {"data": [1.0, 2.0, 3.0, 2.0], "lsl": 0.0, "usl": 5.0},
                                  "S1": {"data": [1.0, 2.0, 3.0, 2.5], "lsl": 0.0, "usl": 5.0}})
        findings = validation.validate_case(case)
        assert not [f for f in validation.errors(findings) if f.check == "V10-stage-binding"]
        assert [f for f in findings
                if f.check == "V10-stage-binding" and f.severity == "WARN"], (
            "a trace-shape constraint that is silently dropped is how this class of defect "
            "survived in the first place")

    def test_the_live_corpus_has_no_stage_binding_collision(self):
        for cid, case in sorted(registry.discover().items()):
            errs = [f for f in validation.validate_case(case)
                    if f.check == "V10-stage-binding" and f.severity == "ERROR"]
            assert not errs, f"{cid}: {[str(e) for e in errs]}"


# --------------------------------------------------------------------------- corpus coverage

#: (case_id, method_id, field) -> why the V7 gate still cannot re-derive it.
#: This list is the audit trail. Closing one of these, or opening a new one, must fail this
#: test until somebody edits this dict on purpose — the previous 66.8% coverage was invisible
#: precisely because no test anywhere asserted a number.
KNOWN_UNVERIFIABLE = {
    ("adb_c16", "basic.two_proportions", "pValue"):
        "orphan truth: the legacy bridge carried a two-proportions ground truth into a case "
        "whose stages declare no such method and whose blocks contain no events/trials data, "
        "so there is nothing to recompute it from. A corpus defect, not a verifier gap.",
}

MIN_CORPUS_COVERAGE = 0.98


class TestCorpusCoverage:
    def test_the_corpus_verified_fraction_is_pinned(self):
        cases = registry.discover()
        records = {}
        for cid, case in sorted(cases.items()):
            for r in validation.verification_coverage(case):
                records[(cid, r.method_id, r.field, r.expected)] = r
        good = sum(1 for r in records.values() if r.verified)
        total = len(records)
        # Guards against a corpus that silently shrank. Two floors because the public release
        # holds 15 of the 24 cases: 83 verification records public, 96 full. Neither is a
        # target; both are floors that must not fall.
        from dmaic_bench.v2.expert_migration import _legacy_bridge_available
        floor = 90 if _legacy_bridge_available() else 80
        assert total > floor, (
            f"the corpus shrank unexpectedly: {total} verification records, floor {floor}")
        assert good / total >= MIN_CORPUS_COVERAGE, (
            f"V7 coverage fell to {good}/{total} = {good / total:.1%}; "
            f"unverified: {[(k[0], k[1], k[2], v.status) for k, v in records.items() if not v.verified]}"
        )

    def test_every_remaining_hole_is_a_declared_known_gap(self):
        cases = registry.discover()
        holes = set()
        for cid, case in sorted(cases.items()):
            for r in validation.verification_coverage(case):
                if not r.verified:
                    holes.add((cid, r.method_id, r.field))
        # KNOWN_UNVERIFIABLE is written against the FULL corpus. An entry naming a held-out
        # case is out of scope in a public checkout, not a "closed hole still listed". Entries
        # for cases that ARE present stay enforced exactly.
        present = set(cases)
        expected = {k for k in KNOWN_UNVERIFIABLE if k[0] in present}
        assert holes == expected, (
            f"unexpected holes {holes - expected}; "
            f"closed holes still listed {expected - holes}")

    def test_no_corpus_truth_contradicts_its_reference_implementation(self):
        bad = []
        for cid, case in sorted(registry.discover().items()):
            for r in validation.verification_coverage(case):
                if r.status == "mismatch":
                    bad.append((cid, r.method_id, r.field, r.expected, r.computed))
        assert not bad, bad

    def test_no_reference_implementation_crashes_on_the_corpus(self):
        bad = []
        for cid, case in sorted(registry.discover().items()):
            for r in validation.verification_coverage(case):
                if r.status == "reference_crash":
                    bad.append((cid, r.method_id, r.field, r.detail))
        assert not bad, bad

    def test_every_control_chart_method_has_a_reference_implementation(self):
        """The measured starting point: REFERENCE_IMPLS had 26 entries and zero
        control_chart.*, so all eleven control-chart methods were unverified."""
        from dmaic_bench import taxonomy as taxonomy_mod
        tax = taxonomy_mod.load()
        charts = [m for m in tax.methods if m.startswith("control_chart.")]
        assert len(charts) == 11
        missing = [m for m in charts if m not in V.REFERENCE_IMPLS]
        assert not missing, missing

    def test_every_capability_and_doe_method_has_a_reference_implementation(self):
        from dmaic_bench import taxonomy as taxonomy_mod
        tax = taxonomy_mod.load()
        wanted = [m for m in tax.methods
                  if m.startswith(("capability.", "doe."))
                  and tax.get(m).canonical_outputs]        # design creation emits nothing
        missing = [m for m in wanted if m not in V.REFERENCE_IMPLS]
        assert not missing, missing

    def test_every_method_a_corpus_truth_binds_has_a_reference_implementation(self):
        bound = set()
        for case in registry.discover().values():
            bound.update(t.method_id for t in case.generate(1).truths)
        missing = sorted(bound - set(V.REFERENCE_IMPLS))
        assert not missing, missing
