"""Native parametric ports of adb_c06 / adb_c21.

Upgraded from the legacy frozen bridge versions — the native directories must shadow the
bridge cases in registry.discover(). Mirrors the TestExemplarCase discipline (test_core.py):
validate 0 ERROR, seed actually changes data AND truths, reproducibility, 30-seed invariant
sweep (the full 500-seed sweep lives in each generator's __main__).
"""
import pytest

from dmaic_bench.core import registry, validation
from dmaic_bench.core.models import data_fingerprint

CASE_IDS = ("adb_c06", "adb_c21")


@pytest.fixture(scope="module")
def native_cases():
    return registry.discover(include_legacy=False)


@pytest.mark.parametrize("case_id", CASE_IDS)
class TestOnboarding:
    def test_validation_zero_errors(self, case_id):
        findings = validation.validate_case_dir(f"{registry.CASES_DIR}/{case_id}")
        assert validation.errors(findings) == [], \
            "; ".join(str(f) for f in validation.errors(findings))

    def test_five_stages_parametric(self, native_cases, case_id):
        case = native_cases[case_id]
        assert case.meta.parametric is True
        assert len(case.meta.stages) == 5

    def test_seed_changes_data_and_truths(self, native_cases, case_id):
        case = native_cases[case_id]
        d1, d2 = case.generate(1), case.generate(2)
        assert data_fingerprint(d1.blocks) != data_fingerprint(d2.blocks)
        t1 = {(t.method_id, t.field): t.expected for t in d1.truths}
        t2 = {(t.method_id, t.field): t.expected for t in d2.truths}
        assert t1 != t2  # Truths are derived from the generated data and change with it.

    def test_same_seed_reproducible(self, native_cases, case_id):
        case = native_cases[case_id]
        assert data_fingerprint(case.generate(7).blocks) == \
            data_fingerprint(case.generate(7).blocks)

    def test_hard_truths_carry_derivation(self, native_cases, case_id):
        for t in native_cases[case_id].generate(1).truths:
            if not t.soft:
                assert t.derivation, f"{t.method_id}.{t.field} missing derivation"

    def test_native_shadows_legacy_bridge(self, case_id):
        # discover(include_legacy=True) must return the parametric native port, not the
        # frozen bridge version (registry setdefault semantics).
        all_cases = registry.discover(include_legacy=True)
        assert all_cases[case_id].meta.parametric is True


class TestInvariants30Seeds:
    """Conclusion invariants must hold for EVERY seed (spot-check 30; 500 in __main__)."""

    def test_controlcharts(self, native_cases):
        case = native_cases["adb_c06"]
        for seed in range(1, 31):
            by = {(t.method_id, t.field): t.expected for t in case.generate(seed).truths}
            assert by[("control_chart.ewma", "flaggedCount")] >= 1
            assert by[("control_chart.cusum", "flaggedCount")] >= 1
            assert 0.5 < by[("capability.nonnormal", "ppk")] < 2.0

    def test_countrate(self, native_cases):
        case = native_cases["adb_c21"]
        for seed in range(1, 31):
            by = {(t.method_id, t.field): t.expected for t in case.generate(seed).truths}
            assert by[("capability.poisson", "dpu")] > 0.05          # clearly above target
            assert by[("control_chart.laney_u", "sigmaZ")] > 1.5     # overdispersed
            assert by[("tables.chisquare_gof", "pValue")] < 0.01     # decisive GOF
