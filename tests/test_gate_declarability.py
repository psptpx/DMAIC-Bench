"""A batch locked behind a gate nothing can declare is a batch nobody opens — the oracle too.

Found by G3, after it had already cost a full control run. The gate derivation added in P0
reads a guard like `settings.modelPValue < 0.05` and emits `screening_significant`, whose
declare key is `any_factor_significant`. In `adb_c38` the method producing that p-value is
`regression.ols`, and only `doe.factorial_analysis` declared the key. So the steward held
`before_after` shut against a declaration no method on that route could make: the reference
solution requested it twice, was refused twice, and scored 0.706 on a task that had been
1.000 in three prior G3 runs.

The check reads the declare keys out of the reference solution, because that is the thing
that has to satisfy the gate. Nothing else is authoritative about what a run can declare.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                              # noqa: E402

from dmaic_bench.v2 import correspondence as C             # noqa: E402
from dmaic_bench.v2 import registry                        # noqa: E402
from dmaic_harbor import spec, v2_tasks as V               # noqa: E402

CASES = registry.discover()


def test_the_shipping_corpus_has_no_undeclarable_gate():
    findings = {cid: [f for f in fs if f[0] == "C7"]
                for cid, fs in C.check_corpus(CASES).items()}
    bad = {cid: fs for cid, fs in findings.items() if fs}
    assert not bad, f"batches locked behind a gate nothing on their route declares: {bad}"


def test_c7_is_an_error_so_it_fails_a_build():
    assert C.SEVERITY["C7"] == "ERROR"


def test_the_declare_table_is_read_from_the_reference_solution():
    keys = C._declarable_keys()
    assert keys, "nothing parsed out of solve.sh; the scan has drifted from the template"
    # The exact pair the defect turned on.
    assert "regression.ols" in keys.get("any_factor_significant", set()), (
        "regression.ols no longer declares any_factor_significant; adb_c38's before_after "
        "batch becomes unopenable again")
    assert "doe.factorial_analysis" in keys.get("any_factor_significant", set())
    assert "msa.gage_rr_crossed" in keys.get("ndc", set())


def test_c7_fires_when_a_gate_key_loses_its_declarer(monkeypatch):
    """The regression test proper: take the declaration away and the check must object.

    Guards against a C7 that passes because it silently found nothing to check.
    """
    real = C._declarable_keys()
    without = {k: (v - {"regression.ols", "doe.factorial_analysis"}) if k ==
               "any_factor_significant" else v for k, v in real.items()}
    monkeypatch.setattr(C, "_declarable_keys", lambda: without)
    findings = [f for f in C.check_case(CASES["adb_c38"]) if f[0] == "C7"]
    assert findings, "C7 did not fire on a gate whose declare key nothing produces"
    assert "screening_significant" in findings[0][2]


def test_every_gate_the_corpus_locks_on_is_a_public_gate():
    """A lock naming a gate that is not in PUBLIC_GATES would be invisible to C7 and to the
    contestant, who reads the thresholds from that same table."""
    for cid, case in sorted(CASES.items()):
        for block, rule in sorted(V.locks(case).items()):
            for gate in rule.get("gates") or ():
                assert gate in spec.PUBLIC_GATES, (
                    f"{cid}: batch {block!r} is locked behind {gate!r}, which is not a "
                    "published gate")
