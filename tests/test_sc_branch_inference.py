"""Self-Consistency must be able to see the branch the contestant took.

``agent_choices`` had the same two-part defect as PQ (``test_pq_terminal_branches``):

* it keys declarations by the name the CONTESTANT gave the fork and then looks them up by the
  graph's private node key, which the task instruction never exposes -- so a declaration binds
  for the oracle and for nobody else;
* its fallback is ``branch_evidence``, which is empty on both sides of exactly the prerequisite
  forks that matter, so no branch could be inferred and the fork recorded NO choice at all.

``score_path`` counts a fork the agent "never addressed" against it, so both failures landed as
wrong routing. Measured across the campaign: SC 0.288 with a 46% zero rate, unchanged by the PQ
fix because it binds through a different path. After inferring the branch from downstream work:
SC 0.606, zero rate 16%, with ``reward`` byte-identical on all 182 cells -- SC is reported and
never gated, so this moves no headline number.
"""
from __future__ import annotations

import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[1])
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.graph import branch_decisions, walk   # noqa: E402
from dmaic_bench.v2 import harbor_truth as HT               # noqa: E402
from dmaic_bench.v2 import registry                         # noqa: E402

CASES = registry.discover()

KNOWN_UNOBSERVABLE = {
    # Forks where EVERY target lacks a data batch or runs no method at all, so no execution can
    # distinguish the branches. These are not scoring bugs; they are points the benchmark cannot
    # observe, and they are listed rather than silently tolerated.
    ("adb_c25", "A_cap_normal"),   # -> C_control | A_root_cause, neither carries a data batch
    ("adb_c28", "A_cap_normal"),   # same fork, same reason
    ("adb_c27", "A_screen"),       # -> I_doe (no data batch) | A_remeasure (no methods)
    ("adb_c30", "A_cap_normal"),   # -> C_control | A_root_cause, neither carries a data batch
}


def _node_methods(case, results):
    return {k: tuple(case.methods_at(k, results)) for k in case.node_data}


def test_the_oracle_route_is_recoverable_from_behaviour_alone():
    """Replay each oracle walk as pure execution -- no declarations -- and re-infer the route.

    This is the property a contestant needs and could not have: the walk must be recoverable
    from what was RUN, because the fork's own identifier is not knowable. Before the fix the
    prerequisite forks resolved to None and the route could not be reconstructed at all.

    Anything outside KNOWN_UNOBSERVABLE that fails here is a scoring defect, not a hard task.
    """
    unrecoverable = []
    for cid, case in CASES.items():
        for seed in case.seeds:
            _, results = case.generate(seed)
            nm = _node_methods(case, results)
            path = walk(case.graph, results)
            executed = {m for key in path for m in nm.get(key, ())}
            choices = HT.agent_choices(case.graph, nm, (), executed)
            for fork, correct in branch_decisions(case.graph, path, results).items():
                if choices.get(fork) != correct and (cid, fork) not in KNOWN_UNOBSERVABLE:
                    unrecoverable.append((cid, seed, fork, correct, choices.get(fork)))
    assert not unrecoverable, (
        "forks whose correct branch cannot be recovered from execution alone: "
        f"{unrecoverable[:8]} ({len(unrecoverable)} total)")


def test_the_unobservable_set_does_not_grow():
    """Every entry above must still be genuinely unobservable -- all targets without methods.

    If a fork lands in that set for any other reason it is a defect wearing an exemption, so
    this re-derives the justification instead of trusting the comment.
    """
    wrongly_exempt = []
    for cid, fork in KNOWN_UNOBSERVABLE:
        case = CASES[cid]
        _, results = case.generate(list(case.seeds)[0])
        nm = _node_methods(case, results)
        targets = [e.target for e in case.graph.edges_from(fork) if e.target != fork]
        if any(nm.get(t) for t in targets):
            wrongly_exempt.append((cid, fork, {t: nm.get(t) for t in targets}))
    assert not wrongly_exempt, f"exempted but actually observable: {wrongly_exempt}"


def test_a_trace_that_ran_nothing_infers_no_branch():
    """Silence is not a choice. No fallback may hand a route to an empty trace."""
    invented = []
    for cid, case in CASES.items():
        for seed in case.seeds:
            _, results = case.generate(seed)
            choices = HT.agent_choices(case.graph, _node_methods(case, results), (), set())
            if choices:
                invented.append((cid, seed, choices))
    assert not invented, f"branches inferred from an empty trace: {invented[:5]}"
