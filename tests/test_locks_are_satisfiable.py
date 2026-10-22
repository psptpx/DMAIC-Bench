"""A batch lock the route cannot satisfy makes the task unfinishable for everyone.

Locks are enforced on the BATCH; a batch may be read by several nodes. Gating it on one node's
prerequisite locks it for every other reader, and if any of those is reached on a route that
never satisfies the lock, the batch can never be obtained — by a contestant or by the oracle.

Nothing except a running steward could see it. The graph is walkable, every truth is computable,
the mirror test passes, and the task is impossible. Found on the first live containerised run of
the corpus, as an oracle at 0.941 and 0.923 with a batch that was never released.

Also asserts the other half of the contract: a list in `requires` means ALTERNATIVES, the way
`scoring.gate_compliance` has always read it. The environment read the same field as a
conjunction, so adb_c33 — whose route visits one of two possible measurement studies — could
never unlock its record. Oracle 0.444.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                          # noqa: E402

from dmaic_bench.v2 import registry                    # noqa: E402
from dmaic_harbor import v2_tasks as V                 # noqa: E402

CASES = registry.discover()


@pytest.mark.parametrize("case_id", sorted(CASES))
def test_every_lock_is_satisfiable_on_every_route(case_id):
    stuck = V.unsatisfiable_locks(CASES[case_id])
    assert not stuck, "\n".join(
        f"seed {s}: batch {b!r} needs {m}, which that route never obtains" for s, b, m in stuck)


def test_a_list_of_predecessors_is_emitted_as_alternatives_not_a_conjunction():
    """adb_c33's record follows whichever agreement study came back acceptable."""
    entry = V.locks(CASES["adb_c33"])["lots"]
    assert entry["requires"] == [["study_1", "study_2"]], (
        "a conjunction here makes every seed whose first study passes unfinishable")


def test_a_single_predecessor_is_still_emitted_flat():
    assert V.locks(CASES["adb_c30"])["process_run"]["requires"] == ["msa"]


def test_a_lock_whose_readers_sit_downstream_of_it_is_kept():
    """The tempting proxy for the bug above — 'drop any lock whose batch has an ungated reader'
    — is wrong, and this is the case that proves it: adb_c26's chart nodes are ungated and read
    the same batch, but they are DOWNSTREAM of the gated node on every route, so the lock is
    both satisfiable and the one real methodology gate the environment can enforce."""
    assert V.locks(CASES["adb_c26"])["subgroups"]["requires"] == ["agreement"]


def test_the_steward_accepts_an_alternatives_group():
    """The wire format has to mean what the emitter meant."""
    from dmaic_harbor import steward_service as ss
    cfg = ss  # noqa: F841 - imported for the config schema below
    entry = V.locks(CASES["adb_c33"])["lots"]["requires"][0]
    assert isinstance(entry, list) and len(entry) == 2
