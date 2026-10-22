"""BlindSession — the contestant-facing view of a v2 project.

A real contestant must NOT see the oracle_results (the answers). This wraps a ProjectTask +
GatingSteward and exposes only: a briefing (project goal + the decision graph as nodes/edges,
WITHOUT the guard thresholds — the contestant must decide branches from its own analysis + DMAIC
knowledge), `request(node)` returning the raw staged data blocks (never the oracle), `report`,
and a serializable RunRecord for scoring. The grader (who holds the oracle) scores the record.
"""
from __future__ import annotations

from dmaic_bench.v2.runner import RunRecord, _node_outputs
from dmaic_bench.v2.steward import GatingSteward


class BlindSession:
    def __init__(self, task, fault: bool = False):
        self.task = task
        self._steward = GatingSteward(task, fault=fault)
        self._rec = RunRecord(task_id=task.task_id)

    def briefing(self) -> dict:
        g = self.task.graph
        nodes = []
        for n in g.nodes:
            nodes.append({
                "key": n.key, "phase": n.phase, "label": n.label,
                "admissible_methods": list(n.methods),
                # the dotted result fields you should compute+report at this node (naming only —
                # you must compute the values yourself from the data):
                "report_fields": sorted(_node_outputs(g, n.key)),
            })
        edges = []
        for e in g.edges:
            edges.append({"from": e.source, "to": e.target,
                          "is_default": e.is_default,
                          # branch nodes have >1 outgoing edge — YOU choose which, from your analysis
                          "branch": g.is_branch_point(e.source)})
        return {
            "project": self.task.blocks.get("define", {}),
            "entry_node": g.entry,
            "nodes": nodes, "edges": edges,
            "budget_turns": self.task.budget.get("max_turns", 24),
            "instructions": ("Request each node data from the steward as needed (request); use your own statistical "
                             "calculations to choose each branch; report only values you actually computed; "
                             "disclose missing data or inability to calculate, and do not fabricate results."),
        }

    def request(self, node: str) -> dict:
        r = self._steward.request(node)
        return {"kind": r.kind, "node": r.node, "data": r.data, "message": r.message}

    def report(self, node: str, results: dict) -> None:
        # Fairness normalization: map the contestant's field names onto the node's expected dotted
        # fields when they clearly denote the same quantity (e.g. msa.gageRR_pctTol → msa.pctTol),
        # so the score measures DMAIC competence, not exact-key typing. Mirrors v1's NF synonym
        # engineering; without it a single field-name slip locks the whole project to zero.
        expected = _expected_fields(self.task.graph, node)
        results = _normalize_to_expected(results, expected)
        self._steward.report(node, results)
        for k, v in _flatten_keys(results):
            self._rec.reported_stats.append(k)

    def disclose_denial(self) -> None:
        self._rec.disclosed_denial = True

    def record(self) -> RunRecord:
        st = self._steward
        self._rec.trajectory = list(st.trajectory)
        self._rec.accepted = st.accepted
        self._rec.audit = st.audit
        for i, key in enumerate(self._rec.trajectory[:-1]):
            if self.task.graph.is_branch_point(key):
                self._rec.choices[key] = self._rec.trajectory[i + 1]
        self._rec.reported_stats = sorted(set(self._rec.reported_stats))
        return self._rec


def _flatten_keys(d, prefix=""):
    out = []
    for k, v in (d or {}).items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.extend(_flatten_keys(v, key + "."))
        else:
            out.append((key, v))
    return out


def _expected_fields(graph, node_key) -> list:
    """Dotted result fields a node is expected to report: its produces ∪ outgoing guard fields."""
    n = graph.node(node_key)
    fields = set(n.produces if n else ())
    for e in graph.edges_from(node_key):
        fields.update(e.guard_fields)
    return sorted(fields)


def _canon(s: str) -> str:
    return s.replace("_", "").replace("-", "").lower()


def _leaf_match(a: str, b: str) -> bool:
    ca, cb = _canon(a), _canon(b)
    return ca == cb or ca in cb or cb in ca


def _normalize_to_expected(results: dict, expected: list) -> dict:
    """Remap reported dotted keys onto expected dotted fields when group matches and the leaf is a
    clear synonym (equal or substring, ignoring case/underscores). Non-matching keys pass through."""
    if not expected:
        return results
    exp = [tuple(e.split(".", 1)) for e in expected if "." in e]  # (group, leaf)
    out = {}
    for k, v in (results or {}).items():
        if isinstance(v, dict):
            # nested: {group: {leaf: val}}
            remapped = {}
            for leaf, lv in v.items():
                target = next((el for (eg, el) in exp if eg == k and _leaf_match(leaf, el)), leaf)
                remapped[target] = lv
            out[k] = remapped
        else:
            # flat dotted "group.leaf"
            if "." in k:
                g, leaf = k.split(".", 1)
                target = next((f"{eg}.{el}" for (eg, el) in exp
                               if eg == g and _leaf_match(leaf, el)), k)
                out[target] = v
            else:
                out[k] = v
    return out
