"""Two properties that were documented in a comment and enforced by nothing.

Both were found by an audit rather than by the suite, which is the argument for writing them
down as tests: a constraint whose only statement is a docstring is not a constraint.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                    # noqa: E402

from dmaic_bench.v2 import registry, scoring     # noqa: E402

#: `V2Case.industry` says: "One of the four COARSE public values ... A fine-grained industry is
#: itself an identifier." The vocabulary is a DE-IDENTIFICATION control, not a style preference:
#: the value reaches `task.toml` as both metadata and a keyword, so a fine-grained value would
#: publish a re-identification handle on every task built from that case.
PUBLIC_INDUSTRIES = {"process_industry", "electronics", "discrete_manufacturing", "services"}


def test_no_case_publishes_a_fine_grained_industry():
    """Caught in review: a case shipped `industry="machining"`, finer than the public vocabulary."""
    offenders = {cid: c.industry for cid, c in registry.discover().items()
                 if c.industry not in PUBLIC_INDUSTRIES}
    assert not offenders, (
        f"industry values outside the coarse public vocabulary {sorted(PUBLIC_INDUSTRIES)}: "
        f"{offenders} -- a fine-grained industry is itself an identifier and reaches task.toml")


def test_gate_compliance_accepts_alternative_predecessors():
    """A gate may be satisfied by whichever of several predecessors the data called for.

    The binomial-capability gate on the attribute case ships `requires: ["M_pchart", "M_laney"]`,
    because which attribute chart is admissible depends on whether the subgroup size varies.
    Indexing that list raised `TypeError: unhashable type: 'list'` and took the whole scorer down
    on adb_c26 rather than scoring it -- the case could not be scored at all through this path.
    """
    policy = [{"stage": "A_cap", "requires": ["M_pchart", "M_laney"], "rule": "chart first"}]
    ok = scoring.gate_compliance(policy, ["M_pchart", "A_cap"])
    assert ok["hard_violation"] is False and ok["checked"] == 1
    # satisfied by the OTHER alternative
    ok2 = scoring.gate_compliance(policy, ["M_laney", "A_cap"])
    assert ok2["hard_violation"] is False
    # neither predecessor ran -> violation
    bad = scoring.gate_compliance(policy, ["A_cap"])
    assert bad["hard_violation"] is True
    # predecessor ran too late -> violation
    late = scoring.gate_compliance(policy, ["A_cap", "M_pchart"])
    assert late["hard_violation"] is True


@pytest.mark.parametrize("cid", sorted(registry.discover()))
def test_every_case_can_be_gate_scored_on_its_own_oracle_route(cid):
    """The scorer must not raise on any shipped case. adb_c26 raised TypeError before the fix."""
    case = registry.discover()[cid]
    for seed in case.seeds:
        route = case.oracle_route(seed)
        out = scoring.gate_compliance(case.gate_policy, route)
        assert out["hard_violation"] is False, (
            f"{cid} seed {seed}: the ORACLE route violates this case's own gate policy: "
            f"{out['violations']}")
