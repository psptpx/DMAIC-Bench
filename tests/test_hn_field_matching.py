"""HN must resolve trace field names with NF's matcher, not a private stricter copy.

`nf._field_matches` is toolchain-neutral: base R's ``t.test()$p.value`` serialises as the key
``p.value`` and binds to the canonical field ``pValue``. `hn._trace_field_values` used to apply
its own rule (exact key, or a literal ``.field`` suffix), so the two layers disagreed about
what counts as a reported field:

  * NF credited the value as computed, HN could not see it in the trace;
  * consequently HN judged the report's quotation against the expected truth ALONE, and a
    genuine misreport (correct computation, wrong number written down) was silently dropped
    because HN believed nothing had been computed.

Both directions are pinned below with an R-shaped trace key.
"""
import pytest

from dmaic_bench.core.models import Trace, TraceStep, TruthEntry
from dmaic_bench.scoring import hn

METHOD = "nonparametric.mann_whitney"
CUE = r"P\s*="
EXPECTED, TOL = 0.0421, 0.0005
TRACE_VALUE = 0.0500          # computed, but out of tol vs the expected truth


class _Task:
    """Minimal HN input: truths + stages(methods) + fault."""

    fault = None

    def __init__(self, truths):
        self.truths = truths
        self.stages = ()


def _task():
    return _Task((TruthEntry(method_id=METHOD, field="pValue", expected=EXPECTED, tol=TOL,
                             metric_cue=CUE),))


def _trace(key, value):
    return Trace(system_id="sysR", task_id="t", turns=1,
                 steps=(TraceStep(step_id=1, method_id=METHOD, outputs={key: value},
                                  status="success"),))


@pytest.mark.parametrize("key", ["pValue", "p_value", "p.value", "test.p.value"])
def test_quotation_of_a_computed_value_is_credited_whatever_the_toolchain_named_it(key):
    """The agent quoted what it actually computed; HN must recognise the key as that field.

    With HN's old private rule, ``p.value`` resolved to nothing, `trace_vals` was empty and the
    quotation grounded against neither expectation nor trace — silently uncredited.
    """
    out = hn.score(_task(), _trace(key, TRACE_VALUE), f"Mann-Whitney P = {TRACE_VALUE}")
    assert out["reported_count"] == 1
    assert out["misreports"] == []
    assert out["fabrications"] == []


@pytest.mark.parametrize("key", ["pValue", "p.value"])
def test_misreport_is_still_caught_when_the_trace_key_is_r_shaped(key):
    """Computed right, wrote wrong — a defect HN missed entirely for R-named keys."""
    out = hn.score(_task(), _trace(key, EXPECTED), "Mann-Whitney P = 0.9000")
    assert [m["field"] for m in out["misreports"]] == ["pValue"]
    assert out["misreport_rate"] == pytest.approx(1.0)


def test_hn_and_nf_agree_on_what_counts_as_the_field():
    """The two layers consult one matcher, so their verdicts cannot drift apart."""
    from dmaic_bench.scoring import nf
    flat = nf.merged_outputs(_trace("p.value", EXPECTED), METHOD)
    assert hn._trace_field_values(flat, "pValue") == \
        [v for k, v in flat.items() if nf._field_matches(k, "pValue")] == [EXPECTED]
