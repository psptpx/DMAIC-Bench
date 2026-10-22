"""Two properties an axis must have to be worth reporting, and one boundary that is a judgement.

An axis that cannot fire measures nothing, and a constant value in a results table is
indistinguishable from the result everyone hopes for. Measured on a 95-trial campaign,
`gate_hard_passed` read 1.0000 with standard deviation 0.0000 — and the first thing to establish
is whether that is a dead axis or a real finding. It is a real finding: an agent CAN violate a
methodology gate, because several nodes share a batch, so a contestant that already holds the
process run can compute a capability index without ever charting it. This test proves the axis is
falsifiable, so a future change that quietly makes it unfalsifiable fails here rather than in a
paper.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                          # noqa: E402

from dmaic_bench.scoring import ms as MS               # noqa: E402
from dmaic_bench.v2 import registry, scoring           # noqa: E402

CASES = registry.discover()


def test_a_methodology_gate_can_actually_be_violated():
    """Skipping the stability chart and computing capability on the batch already held."""
    case = CASES["adb_c30"]
    compliant = ["D_scope", "M_msa", "M_stability", "A_route", "A_cap_normal", "C_control"]
    violating = ["D_scope", "M_msa", "A_route", "A_cap_normal", "C_control"]
    ok = scoring.gate_compliance(case.gate_policy, compliant)
    bad = scoring.gate_compliance(case.gate_policy, violating)
    assert ok["hard_violation"] is False and ok["gc"] == 1.0
    assert bad["hard_violation"] is True and bad["gc"] == 0.0, (
        "the gate axis cannot fire, so a perfect score on it is a property of the environment "
        "rather than a result about the contestant")


@pytest.mark.parametrize("case_id", sorted(CASES))
def test_every_case_has_at_least_one_violable_gate(case_id):
    """A case whose gates no trajectory can breach contributes a free 1.0 to every contestant."""
    case = CASES[case_id]
    if not case.gate_policy:
        pytest.skip("no gate policy")
    for rule in case.gate_policy:
        stage = rule["stage"]
        req = rule["requires"]
        req = [req] if isinstance(req, str) else list(req)
        # Enter the gated stage without any of its predecessors.
        bad = scoring.gate_compliance([rule], [stage])
        if bad["hard_violation"]:
            return
    pytest.fail(f"{case_id}: no rule in its gate policy can be violated by any trajectory")


def test_precision_exempts_assumption_checks_and_charges_for_conclusions():
    """The stated boundary, pinned so the list is not quietly widened into meaninglessness.

    A method that CHECKS AN ASSUMPTION is exempt; one that ASSERTS A FINDING is not. Precision is
    the smallest averaged axis in 47% of trials, so it drives the harmonic mean more than any
    other, while method spam is the first cause of failure in only 6 of 93 — an axis with that
    much leverage has to be exact about what it charges for.
    """
    for exempt in ("meta.data_profiling", "basic.normality", "basic.descriptive_summary",
                   "anova.equal_variances", "nonparametric.runs_test"):
        assert exempt in MS.ALWAYS_RELEVANT
    for charged in ("basic.two_sample_t", "basic.one_sample_t", "anova.oneway",
                    "regression.ols", "capability.normal", "doe.factorial_analysis"):
        assert charged not in MS.ALWAYS_RELEVANT, (
            f"{charged} asserts a finding; exempting it would stop precision measuring anything")
