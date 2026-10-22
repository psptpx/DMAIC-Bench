"""Batch-2 native parametric cases: adb_c11 / adb_c01 / adb_c14 / adb_c22 /
adb_c09 — onboarding validation (0 errors) + 30-seed invariant spot checks.

The generators assert their own design invariants on every call, so simply generating a seed
range exercises them; the explicit assertions below re-check the headline facts from the truth
entries so a silent generator regression cannot slip through."""
import pytest

from dmaic_bench.core import registry, validation

CASES_DIR = registry.CASES_DIR
CASE_IDS = ["adb_c11", "adb_c01", "adb_c14", "adb_c22", "adb_c09"]
SPOT_SEEDS = range(1, 31)

# the 14 methods this batch adds coverage for
BATCH2_METHODS = {
    "adb_c11": {"doe.create_factorial", "doe.factorial_analysis", "doe.factorial_prediction"},
    "adb_c01": {"doe.rsm_analysis", "doe.rsm_canonical", "doe.rsm_optimizer"},
    "adb_c14": {"regression.ols", "regression.binary_logistic"},
    "adb_c22": {"nonparametric.runs_test", "nonparametric.moods_median"},
    "adb_c09": {"meta.data_profiling", "quality.pareto", "quality.fmea_rpn",
                     "tables.chisquare_assoc"},
}


@pytest.fixture(scope="module")
def native_cases():
    return registry.discover(include_legacy=False)


def _truths_by_key(data):
    return {(t.method_id, t.field): t.expected for t in data.truths}


class TestOnboarding:
    @pytest.mark.parametrize("cid", CASE_IDS)
    def test_validate_zero_errors(self, cid):
        findings = validation.validate_case_dir(f"{CASES_DIR}/{cid}")
        assert validation.errors(findings) == [], [str(f) for f in findings]

    @pytest.mark.parametrize("cid", CASE_IDS)
    def test_registered_and_parametric(self, native_cases, cid):
        assert cid in native_cases
        assert native_cases[cid].meta.parametric is True

    @pytest.mark.parametrize("cid", CASE_IDS)
    def test_declared_method_coverage(self, native_cases, cid):
        meta = native_cases[cid].meta
        declared = {m.method_id for s in meta.stages for m in s.methods if m.required}
        assert declared == BATCH2_METHODS[cid]

    def test_batch_covers_14_methods(self):
        all_methods = set().union(*BATCH2_METHODS.values())
        assert len(all_methods) == 14

    @pytest.mark.parametrize("cid", CASE_IDS)
    def test_every_case_has_a_fault_target(self, native_cases, cid):
        assert len(native_cases[cid].meta.fault_targets) >= 1

    @pytest.mark.parametrize("cid", CASE_IDS)
    def test_topics_disjoint_across_stages(self, native_cases, cid):
        seen = set()
        for s in native_cases[cid].meta.stages:
            assert not (set(s.topics) & seen), f"topic overlap in {cid}/{s.stage_id}"
            seen |= set(s.topics)

    def test_decision_points_declared(self, native_cases):
        doe_points = {p.point_id: p for p in native_cases["adb_c11"].meta.decision_points}
        assert doe_points["effect_screen"].correct_branch == "drop_C"
        assert doe_points["effect_screen"].branch_evidence["drop_C"] == \
            ["doe.factorial_prediction"]
        q_points = {p.point_id: p for p in native_cases["adb_c09"].meta.decision_points}
        assert q_points["vital_few"].correct_branch == "pareto_first"
        assert q_points["vital_few"].branch_evidence["pareto_first"] == ["quality.pareto"]

    def test_order_constraints_declared(self, native_cases):
        doe_oc = native_cases["adb_c11"].meta.order_constraints
        assert ("doe.factorial_analysis", "doe.factorial_prediction") in \
            {(o.before, o.after) for o in doe_oc}
        rsm_oc = native_cases["adb_c01"].meta.order_constraints
        assert ("doe.rsm_analysis", "doe.rsm_canonical") in \
            {(o.before, o.after) for o in rsm_oc}


class TestInvariants30Seeds:
    def test_mini_doe(self, native_cases):
        for seed in SPOT_SEEDS:
            by = _truths_by_key(native_cases["adb_c11"].generate(seed))
            assert by[("doe.factorial_analysis", "modelPValue")] < 0.01
            assert by[("doe.factorial_analysis", "rSquaredPct")] > 70.0
            assert by[("doe.factorial_prediction", "predictedValue")] > 0.0

    def test_mini_rsm(self, native_cases):
        for seed in SPOT_SEEDS:
            data = native_cases["adb_c01"].generate(seed)
            by = _truths_by_key(data)
            assert by[("doe.rsm_analysis", "rSquaredPct")] > 85.0
            # constrained maximum equals the stationary-point prediction by construction
            assert by[("doe.rsm_optimizer", "predictedResponse")] == \
                by[("doe.rsm_canonical", "predictedAtStationary")]

    def test_mini_regression(self, native_cases):
        for seed in SPOT_SEEDS:
            by = _truths_by_key(native_cases["adb_c14"].generate(seed))
            assert by[("regression.ols", "modelPValue")] < 0.001
            assert by[("regression.binary_logistic", "modelPValue")] < 0.01

    def test_mini_sequence(self, native_cases):
        for seed in SPOT_SEEDS:
            by = _truths_by_key(native_cases["adb_c22"].generate(seed))
            assert by[("nonparametric.runs_test", "pValue")] > 0.05
            assert by[("nonparametric.moods_median", "pValue")] < 0.01

    def test_mini_quality(self, native_cases):
        for seed in SPOT_SEEDS:
            by = _truths_by_key(native_cases["adb_c09"].generate(seed))
            assert by[("quality.pareto", "topCategoryPct")] > 50.0
            assert by[("quality.fmea_rpn", "maxRpn")] > 125
            assert by[("tables.chisquare_assoc", "pValue")] < 0.01
