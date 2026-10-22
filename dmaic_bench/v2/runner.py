"""v2 long-horizon runner: drive an agent policy through the GatingSteward, produce a RunRecord.

Two reference (non-LLM, deterministic) policies for tests/demos:
  OracleAgent    truthful + data-conditioned: routes on what it has observed (re-walks the graph
                 over its own accepted results), reports each node's true outputs → a fully
                 compliant long-horizon trajectory.
  ScriptedAgent  a methodologically-rigid single-path solver: always marches the modal happy path
                 regardless of the data. It reports truthfully but ignores the gates — so the
                 environment LOCKS it out of capability on an out-of-control process, and it
                 mis-routes on off-modal data. This is the environment enforcing the methodology.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from dmaic_bench.core.graph import DecisionGraph, walk
from dmaic_bench.v2.steward import GatingSteward


@dataclass
class RunRecord:
    task_id: str
    trajectory: list = field(default_factory=list)      # nodes whose data was released, in order
    accepted: dict = field(default_factory=dict)         # agent's declared results
    reported_stats: list = field(default_factory=list)   # statistic keys the agent committed to
    choices: dict = field(default_factory=dict)          # branch_node -> target the agent went to
    audit: list = field(default_factory=list)
    turns: int = 0
    disclosed_denial: bool = False


def _node_outputs(graph: DecisionGraph, node_key: str) -> set:
    """Top-level result groups a node is responsible for: its `produces` plus every field its
    OUTGOING guards read (a node that branches on normality.pValue must have computed it)."""
    node = graph.node(node_key)
    groups = set()
    for f in (node.produces if node else ()):
        groups.add(f.split(".")[0])
    for e in graph.edges_from(node_key):
        for f in e.guard_fields:
            groups.add(f.split(".")[0])
    return groups


def _slice_results(oracle: dict, groups: set) -> dict:
    return {g: oracle[g] for g in groups if g in oracle}


def _stats_reported(graph: DecisionGraph, node_key: str) -> list:
    """The specific statistic keys (dotted) a node commits a number to (for cascade validity)."""
    node = graph.node(node_key)
    return list(node.produces) if node else []


class OracleAgent:
    """Truthful, data-conditioned. Follows walk(graph, accepted) — its route emerges from what it
    has observed so far, which (because it reports truthfully) converges to the oracle route."""

    def reset(self, task):
        self.task = task

    def choose_next(self, steward: GatingSteward):
        route = walk(self.task.graph, {**self.task.oracle_results, **steward.accepted})
        return next((n for n in route if n not in steward.completed), None)

    def work(self, node, steward):
        groups = _node_outputs(self.task.graph, node)
        return _slice_results(self.task.oracle_results, groups)

    def reported_stats(self, node):
        return _stats_reported(self.task.graph, node)


class ScriptedAgent:
    """Fixed modal happy-path; truthful reporting but ignores gates. `modal` is the node sequence."""

    def __init__(self, modal):
        self.modal = list(modal)

    def reset(self, task):
        self.task = task

    def choose_next(self, steward: GatingSteward):
        return next((n for n in self.modal if n not in steward.completed), None)

    def work(self, node, steward):
        groups = _node_outputs(self.task.graph, node)
        return _slice_results(self.task.oracle_results, groups)

    def reported_stats(self, node):
        return _stats_reported(self.task.graph, node)


def run_project(task, agent, fault: bool = False, max_locks: int = 3) -> RunRecord:
    """Drive `agent` through the GatingSteward. On a lock the agent is forced to abandon that node
    (it may not obtain the data); after `max_locks` consecutive dead ends the run ends."""
    steward = GatingSteward(task, fault=fault)
    agent.reset(task)
    rec = RunRecord(task_id=task.task_id)
    locked_attempts, blocked = 0, set()
    budget = task.budget.get("max_turns", 24)

    for _ in range(budget):
        rec.turns += 1
        node = agent.choose_next(steward)
        if node is None or node in blocked and locked_attempts >= max_locks:
            break
        resp = steward.request(node)
        if resp.kind == "data":
            locked_attempts = 0
            results = agent.work(node, steward)
            steward.report(node, results)
            rec.reported_stats.extend(agent.reported_stats(node))
            # record the branch decision: the next node the agent will go to from here
        elif resp.kind == "locked":
            locked_attempts += 1
            blocked.add(node)
            # mark completed to avoid infinite retry, but its data was never released
            steward.completed.add(node)
            if locked_attempts >= max_locks:
                break
        elif resp.kind == "denied":
            rec.disclosed_denial = True     # a truthful agent discloses; recorded for HN
            steward.completed.add(node)

    rec.trajectory = list(steward.trajectory)
    rec.accepted = steward.accepted
    rec.audit = steward.audit
    # derive branch choices from the realized trajectory (node -> next released node)
    for i, key in enumerate(rec.trajectory[:-1]):
        if task.graph.is_branch_point(key):
            rec.choices[key] = rec.trajectory[i + 1]
    rec.reported_stats = sorted(set(rec.reported_stats))
    return rec
