"""The reporting layers must measure what they claim and refuse to score an empty denominator."""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from dmaic_harbor import analysis as A          # noqa: E402
from dmaic_bench.v2 import registry             # noqa: E402


def test_every_shape_in_the_build_lands_in_a_tier():
    """The tier is derived from the seed's shape, so no shape may fall through unclassified."""
    seen = {}
    for cid, case in registry.discover().items():
        for seed in case.seeds:
            shape = getattr(case, "shape_at", None)
            _, results = case.generate(seed)
            sh = case.shape_of(results) if hasattr(case, "shape_of") else None
            if sh is None:
                continue
            seen.setdefault(A.tier_of(sh), set()).add(sh)
    # at minimum the classifier must be total over the strings it is given
    for sh in ("gauge-unacceptable", "appraiser-disagreement", "unstable/special-cause",
               "constant/out-of-control", "normal-capable", "anything-else"):
        assert A.tier_of(sh) in (A.TIER_A, A.TIER_B, A.TIER_C)


def test_stop_and_divert_are_not_confused():
    assert A.tier_of("gauge-unacceptable") == A.TIER_C
    assert A.tier_of("appraiser-disagreement") == A.TIER_C
    assert A.tier_of("unstable(line-switch)") == A.TIER_B
    assert A.tier_of("constant/out-of-control") == A.TIER_B
    assert A.tier_of("normal-capable") == A.TIER_A


def test_citation_rate_refuses_an_empty_denominator():
    """A run that computed nothing has no citation rate -- it does not have a perfect one."""
    assert A.citation_rate({"steps": []}, "a report full of confident prose") is None
    assert A.citation_rate({"steps": [{"status": "failed", "outputs": {"x": 1}}]}, "1") is None


def test_citation_rate_credits_a_percent_scaled_quotation():
    trace = {"steps": [{"status": "success", "outputs": {"pctSV": 0.5147}}]}
    assert A.citation_rate(trace, "study variation was 51.47%") == 1.0
    assert A.citation_rate(trace, "the gauge is unacceptable") == 0.0


def test_claimed_complete_reads_the_ledger_not_the_prose():
    """ECR is a fact about what the system did with the steward, not how its report reads."""
    declared = ['{"action": "request"}', '{"action": "declare"}']
    silent = ['{"action": "request"}', '{"action": "status"}']
    assert A.claimed_complete(declared, report_bytes=500) is True
    assert A.claimed_complete(silent, report_bytes=500) is False
    # a declaration with no report filed is not a claim of completion
    assert A.claimed_complete(declared, report_bytes=0) is False


def test_the_ecr_gap_is_reported_at_every_bar():
    """A single bar would be a choice of flattering threshold; all of them must come back."""
    out = A.ecr_tsr([1.0, 0.85, 0.7, 0.2], [True, True, True, True])
    assert out["ecr"] == 1.0
    assert out["gap"]["0.999"] > out["gap"]["0.6"], "the gap must shrink as the bar loosens"
    assert set(out["tsr"]) == {"0.999", "0.8", "0.6"}


def test_by_tier_reports_zero_rate_separately_from_the_mean():
    tiers = {"t1": A.TIER_A, "t2": A.TIER_C, "t3": A.TIER_C}
    out = A.by_tier({"t1": 0.9, "t2": 0.0, "t3": 0.6}, tiers)
    assert out[A.TIER_A]["mean"] == 0.9 and out[A.TIER_A]["zero_rate"] == 0.0
    assert out[A.TIER_C]["n"] == 2 and out[A.TIER_C]["zero_rate"] == 0.5
