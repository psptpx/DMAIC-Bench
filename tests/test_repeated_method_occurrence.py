"""A study that is re-run after remediation must be readable as TWO verdicts, not one.

``merged_outputs`` flattens every successful step of a method with last-wins. That is right
while a method runs once, and destroys the earlier value when it runs twice — which
``adb_c33`` does on purpose: the whole project turns on an original judgement study failing
and the repaired one passing. Under the merge the repaired verdict answers for both, the
re-walk skips the remediation it watched the contestant perform, and Self-Consistency charges
a correct trace for a decision it made correctly.

The numeric axis already resolved this per step (``nf._claim_step``). Self-Consistency did
not, so these tests state the property for the path that did not have it, and show what the
unpinned resolution would have concluded on the same trace.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from dmaic_bench.core.models import Trace, TraceStep      # noqa: E402
from dmaic_bench.scoring import nf as nf_mod              # noqa: E402
from dmaic_bench.v2 import harbor_truth as HT             # noqa: E402
from dmaic_bench.v2 import registry                       # noqa: E402

_MID = "msa.attribute_agreement"
_FAILED, _REPAIRED = 0.4231, 0.9714


def _two_study_trace():
    """One trace that ran the agreement study twice: it failed, then it passed."""
    return Trace(system_id="t", task_id="t",
                 steps=(TraceStep(step_id=1, method_id=_MID,
                                  outputs={"kappaMin": _FAILED}, status="success"),
                        TraceStep(step_id=2, method_id=_MID,
                                  outputs={"kappaMin": _REPAIRED}, status="success")))


def _resolve(field_map):
    trace = _two_study_trace()
    by_method = {_MID: nf_mod.merged_outputs(trace, _MID)}
    by_occurrence = {(_MID, i): outs
                     for i, outs in enumerate(nf_mod.step_outputs(trace, _MID) or ())}
    results, seen, _unobs = HT.observed_results(field_map, by_method, None, by_occurrence)
    return results, seen


def test_a_pinned_source_reads_its_own_invocation():
    results, seen = _resolve({
        "agree1.kappaMin": ({"method_id": _MID, "output": "kappaMin", "occurrence": 0},),
        "agree2.kappaMin": ({"method_id": _MID, "output": "kappaMin", "occurrence": 1},)})
    assert sorted(seen) == ["agree1.kappaMin", "agree2.kappaMin"]
    assert results["agree1"]["kappaMin"] == _FAILED
    assert results["agree2"]["kappaMin"] == _REPAIRED


def test_without_the_pin_the_second_study_answers_for_the_first():
    """The behaviour being fixed, stated so the fix cannot be quietly reverted."""
    results, _seen = _resolve({
        "agree1.kappaMin": ({"method_id": _MID, "output": "kappaMin"},),
        "agree2.kappaMin": ({"method_id": _MID, "output": "kappaMin"},)})
    assert results["agree1"]["kappaMin"] == _REPAIRED != _FAILED


def test_the_unpinned_read_would_route_past_the_remediation_the_agent_performed():
    """End to end on the shipped case: the merge does not merely lose a number, it loses a step.

    Walked on the pinned reading, the seed goes through the disagreement breakdown and the
    second study. Walked on the merged reading, the first study looks acceptable and the whole
    remediation disappears from the route.
    """
    case = registry.discover()["adb_c33"]
    _blocks, results = case.generate(2)             # study 1 fails, the repair holds
    pinned, _s = _resolve(dict(case.field_map))
    unpinned = {k: ({**dict(s[0]), "occurrence": None},) for k, s in case.field_map.items()
                if s and s[0].get("method_id") == _MID}
    merged, _s2 = _resolve(unpinned)

    assert pinned["agree1"]["kappaMin"] < 0.60 <= pinned["agree2"]["kappaMin"]
    assert merged["agree1"]["kappaMin"] >= 0.60
    assert results["agree1"]["kappaMin"] < 0.60, "the oracle's own first study must fail here"

# The end-to-end statement -- SC == 1.0 for a trace that reports both verdicts and walks the
# oracle route -- is covered per case by
# harbor/tests/test_v2_build.py::test_sc_is_perfect_for_a_run_that_reports_the_oracle_numbers_
# and_walks_the_oracle_route, which builds the real truth package. It is not repeated here.
