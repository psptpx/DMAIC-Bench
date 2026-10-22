"""C6 had never fired once, and the reason was that it flagged the ordinary case.

The module header called it an ERROR; `SEVERITY` never listed it; `errors()` therefore dropped
every finding it made. Promoting it as written fires on 10 cases, all of them the same shape:
one method feeding several fields. That is not a collision — one Gage R&R run reports `pctSV`
AND `ndc`, one capability run reports `cp`, `cpk` and `ppk`, from ONE invocation, through
DIFFERENT output keys.

The real hazard is narrower. `merged_outputs` is last-wins over INVOCATIONS, so two fields
reading one method's ONE output can only be told apart by an `occurrence` pin — and only need
to be when their nodes can actually be on one route together.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from dmaic_bench.v2 import correspondence as C         # noqa: E402
from dmaic_bench.v2 import registry                    # noqa: E402

CASES = registry.discover()


def _c6(case_id):
    return [f for f in C.check_case(CASES[case_id]) if f[0] in ("C6", "C6W")]


def test_c6_is_an_error_and_its_latent_form_is_a_warning():
    assert C.SEVERITY["C6"] == "ERROR"
    assert C.SEVERITY["C6W"] == "WARN"


def test_no_case_has_a_live_last_wins_collision():
    live = {cid: [f for f in C.check_case(c) if f[0] == "C6"]
            for cid, c in sorted(CASES.items())}
    bad = {cid: fs for cid, fs in live.items() if fs}
    assert not bad, f"two fields bound to one invocation on a route they share: {bad}"


def test_a_method_feeding_several_DIFFERENT_outputs_is_not_a_collision():
    """The false positive that kept C6 inert. One invocation, several output keys."""
    for case_id in ("adb_c25", "adb_c27", "adb_c34"):
        for finding in _c6(case_id):
            assert "correlationCoefficient" in finding[2], (
                f"{case_id}: C6 fired on a multi-output method again: {finding[2]}")


def test_the_latent_collision_in_adb_c35_is_reported_and_named():
    """Two correlation studies, one output key, no pin. Safe today only because the two nodes
    sit on mutually exclusive branches — a fact about the seeds, not about the design."""
    findings = [f for f in _c6("adb_c35") if f[0] == "C6W"]
    assert len(findings) == 1, findings
    msg = findings[0][2]
    assert "setting.correlationCoefficient" in msg
    assert "special2.correlationCoefficient" in msg
    assert "no shipped seed reaches their nodes together" in msg


def test_the_two_correlation_nodes_really_are_mutually_exclusive():
    """The premise the WARN rests on. If a seed ever reaches both, C6 must become an ERROR —
    and this test is what turns that from a silent change into a failure."""
    from dmaic_bench.core.graph import walk

    case = CASES["adb_c35"]
    for seed in case.seeds:
        route = set(walk(case.graph, case.generate(seed)[1]))
        assert not {"A_special_2", "A_rc_second"} <= route, (
            f"seed {seed} reaches both correlation nodes; the C6W in adb_c35 is now live and "
            "the fields need distinguishing")


def test_pinned_repeats_are_not_flagged():
    """adb_c33 and adb_c35 read one output at two nodes and pin the invocations. That is the
    fix C6 exists to require, so it must not then complain about it."""
    for case_id in ("adb_c33", "adb_c35"):
        for finding in _c6(case_id):
            assert "kappaMin" not in finding[2]
            assert "flaggedCount" not in finding[2]
            assert "cpk" not in finding[2]
