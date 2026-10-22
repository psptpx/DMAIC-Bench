"""v3 method-selection contract + two-channel scoring."""
import sys, os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from dmaic_bench.v3.method_policy import ADB_C15_DECISIONS as D, score_method_selection
from dmaic_bench.v3.session import MethodBlindSession, method_space
from dmaic_bench.v2 import builder, sonnet_harness

import pytest  # noqa: E402
from dmaic_bench.v2.expert_migration import _legacy_bridge_available  # noqa: E402

# These exercises are pinned to an expert-derived case held out of the public
# release (docs/HELD_OUT.md). Repointing them at a public case is tracked work;
# until then the skip is reported, never silent.
pytestmark = pytest.mark.skipif(
    not _legacy_bridge_available(),
    reason="held-out expert case absent (public release) -- see docs/HELD_OUT.md",
)

OBS = {"doe": {"curvature_pValue": 0.00115}}


def test_method_space_is_full_menu():
    ms = method_space()
    assert len(ms) >= 40                                  # the whole vocabulary, not a shortlist
    assert any(m["method_id"] == "capability.nonnormal" for m in ms)


def test_correct_selection_scores_full():
    correct = {"M_Baseline": ["control_chart.imr", "capability.normal"],
               "M_GRR": "msa.gage_rr_crossed", "A_ANOVA": "anova.oneway",
               "I_Factorial": "doe.factorial_analysis", "I_CCD": "doe.rsm_analysis"}
    r = score_method_selection(correct, D, OBS)
    assert r["ms_sel"] == 1.0 and r["misuse_rate"] == 0.0 and r["applicable"] == 6


def test_misuse_is_caught():
    bad = {"M_Baseline": ["control_chart.xbar_r", "capability.binomial"],   # wrong chart + wrong cap
           "M_GRR": "msa.attribute_agreement",                             # attribute on continuous
           "A_ANOVA": "basic.two_sample_t",                               # 2-sample on 3 groups
           "I_Factorial": "doe.factorial_analysis", "I_CCD": "doe.rsm_analysis"}
    r = score_method_selection(bad, D, OBS)
    assert r["misuse_rate"] > 0.5 and r["ms_sel"] < 0.5


def test_silence_is_not_selection():
    r = score_method_selection({}, D, OBS)
    assert r["ms_sel"] == 0.0 and r["misuse_rate"] == 0.0


def test_data_conditioned_decision_only_scored_when_applicable():
    # rsm_method applies only when curvature is significant; with no signal it's not graded
    r2 = score_method_selection({}, D, observed={"doe": {"curvature_pValue": 0.9}})
    assert "rsm_method" not in r2["per_decision"]


def test_method_blind_briefing_strips_admissible_methods():
    case = sonnet_harness._get_case("adb_c15")
    task = builder.build_project_task(case, 0)
    b = MethodBlindSession(task).briefing()
    assert "method_space" in b and "policy_doc" in b
    for n in b["nodes"]:
        assert "admissible_methods" not in n              # the v2 method-feed is gone


def test_session_captures_declared_method():
    case = sonnet_harness._get_case("adb_c15")
    task = builder.build_project_task(case, 0)
    s = MethodBlindSession(task)
    s.request("M_Baseline")
    s.report("M_Baseline", {"imr": {"outOfControl": 0}}, method="control_chart.imr")
    assert s.record().declared_methods["M_Baseline"] == "control_chart.imr"


def test_d2_trap_is_data_conditioned():
    """The SAME method (capability.normal) is correct on normal data but MISUSE on skewed data —
    an agent that skips the normality check is trapped. This is the discriminating axis."""
    from dmaic_bench.v3.method_policy import INJECTION_DECISIONS as DI
    from dmaic_bench.v2.cases.injection_molding import CASE
    _, skew = CASE.generate(2)                       # non-normal seed
    obs_skew = {"normality": {"pValue": skew["normality"]["pValue"]}}
    assert obs_skew["normality"]["pValue"] < 0.05
    careful = score_method_selection({"A_cap_nonnormal": "capability.nonnormal"}, DI, obs_skew)
    naive = score_method_selection({"A_cap_nonnormal": "capability.normal"}, DI, obs_skew)
    assert careful["misuse_rate"] == 0.0 and naive["misuse_rate"] > 0.0   # trap fires on naive
    _, norm = CASE.generate(0)                       # normal seed
    obs_norm = {"normality": {"pValue": norm["normality"]["pValue"]}}
    ok = score_method_selection({"A_cap_normal": "capability.normal"}, DI, obs_norm)
    assert ok["misuse_rate"] == 0.0                  # same method is correct on normal data
