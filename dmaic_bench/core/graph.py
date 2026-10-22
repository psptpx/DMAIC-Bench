"""Conditional decision-graph ground truth — the v2 core primitive.

v1's `DecisionPoint.correct_branch` is a constant frozen at case-authoring time, so two data
draws can never demand two different correct routes (a scripted single-path solver aces it). v2
replaces it with a **decision graph whose edges are guards over the observed results**: the
correct next node is `f(results)`. This ports the backend's battle-tested runtime model
(`GraphEdge.when` + `guardFields`, `JourneyGuardEvaluator`) into a ground-truth schema, so the
oracle walk `walk(graph, results⋆)` yields a *data-conditioned* correct trajectory.

The guard DSL is evaluated by a small recursive-descent parser (NO Python eval), supporting:
    comparisons   >=  <=  >  <  ==  !=            e.g.  normality.pValue >= 0.05
    membership    <field> in [a, b, c]           e.g.  cap.verdict in [good, marginal]
    boolean       and  or  not  ( )               e.g.  msa.ndc >= 5 and msa.pctTol < 0.30
    fields        dotted paths                    resolved flat ("a.b") then nested (a→b)
    literals      numbers, 'quoted' or bare idents (bare idents are string constants for enums)

See docs/archive/dmaic-bench-v2-longhorizon-design.md §3.1.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Optional


# --------------------------------------------------------------------------- data model

@dataclass(frozen=True)
class GuardedEdge:
    """An edge whose `when` guard (a DSL string) must hold for the transition to be correct.

    `when=None` is an unconditional (linear) edge. `is_default=True` is taken only when no
    guarded sibling matches (mirrors the backend's default branch). `guard_fields` names the
    result fields the guard reads — used for audit/export and to check the agent even observed
    the values its route depends on.
    """
    source: str
    target: str
    when: Optional[str] = None
    is_default: bool = False
    guard_fields: tuple = ()


@dataclass(frozen=True)
class GraphNode:
    """A stage obligation: a phase, the admissible methods, and the artifact it must produce."""
    key: str
    phase: str = ""
    methods: tuple = ()            # admissible method_ids at this node
    produces: tuple = ()           # result keys this node is expected to compute (for CF/NF)
    label: str = ""


@dataclass(frozen=True)
class DecisionGraph:
    nodes: tuple = ()              # tuple[GraphNode]
    edges: tuple = ()              # tuple[GuardedEdge]
    entry: str = ""

    def node(self, key: str) -> Optional[GraphNode]:
        return next((n for n in self.nodes if n.key == key), None)

    def edges_from(self, key: str) -> list:
        return [e for e in self.edges if e.source == key]

    def is_branch_point(self, key: str) -> bool:
        return len(self.edges_from(key)) > 1


# --------------------------------------------------------------------------- guard DSL

_TOKEN = re.compile(r"""
    \s*(?:
      (?P<num>-?\d+\.?\d*(?:[eE][-+]?\d+)?)     # number
    | (?P<str>'[^']*'|"[^"]*")                   # quoted string
    | (?P<op>>=|<=|==|!=|>|<)                     # comparison
    | (?P<lb>\[) | (?P<rb>\]) | (?P<lp>\() | (?P<rp>\)) | (?P<comma>,)
    | (?P<ident>[A-Za-z_][A-Za-z0-9_.]*)          # identifier / dotted field / keyword
    )
""", re.VERBOSE)

_KEYWORDS = {"and", "or", "not", "in", "true", "false"}
_MISSING = object()


def _tokenize(expr: str) -> list:
    toks, pos = [], 0
    while pos < len(expr):
        m = _TOKEN.match(expr, pos)
        if not m or m.end() == pos:
            if expr[pos:].strip() == "":
                break
            raise ValueError(f"guard parse error near {expr[pos:]!r}")
        pos = m.end()
        kind = m.lastgroup
        val = m.group(kind)
        toks.append((kind, val))
    toks.append(("end", ""))
    return toks


def _resolve_field(path: str, results: dict):
    """Flat key ('a.b') first, then nested (results['a']['b']). Missing → _MISSING."""
    if path in results:
        return results[path]
    cur: Any = results
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return _MISSING
    return cur


class _Parser:
    """Recursive-descent: or_expr := and_expr ('or' and_expr)*; and_expr := not_expr ('and' ...)*;
    not_expr := 'not' not_expr | primary; primary := '(' or_expr ')' | comparison | atom."""

    def __init__(self, toks, results):
        self.toks, self.i, self.results = toks, 0, results

    def _peek(self):
        return self.toks[self.i]

    def _next(self):
        t = self.toks[self.i]; self.i += 1; return t

    def parse(self) -> bool:
        v = self._or()
        if self._peek()[0] != "end":
            raise ValueError(f"trailing tokens: {self.toks[self.i:]}")
        return bool(v)

    def _or(self):
        v = self._and()
        while self._peek() == ("ident", "or"):
            self._next(); r = self._and(); v = bool(v) or bool(r)
        return v

    def _and(self):
        v = self._not()
        while self._peek() == ("ident", "and"):
            self._next(); r = self._not(); v = bool(v) and bool(r)
        return v

    def _not(self):
        if self._peek() == ("ident", "not"):
            self._next(); return not bool(self._not())
        return self._primary()

    def _primary(self):
        kind, val = self._peek()
        if kind == "lp":
            self._next(); v = self._or()
            if self._next()[0] != "rp":
                raise ValueError("expected )")
            return v
        return self._comparison()

    def _comparison(self):
        left = self._value()
        kind, val = self._peek()
        if kind == "op":
            self._next(); right = self._value()
            return self._apply(val, left, right)
        if (kind, val) == ("ident", "in"):
            self._next(); members = self._list()
            return any(self._eq(left, m) for m in members)
        # bare truthy atom (e.g. a boolean field or literal on its own)
        if left is _MISSING:
            return False
        return bool(left)

    def _list(self):
        if self._next()[0] != "lb":
            raise ValueError("expected [")
        members = []
        if self._peek()[0] != "rb":
            members.append(self._value())
            while self._peek()[0] == "comma":
                self._next(); members.append(self._value())
        if self._next()[0] != "rb":
            raise ValueError("expected ]")
        return members

    def _value(self):
        kind, val = self._next()
        if kind == "num":
            return float(val)
        if kind == "str":
            return val[1:-1]
        if kind == "ident":
            low = val.lower()
            if low == "true":
                return True
            if low == "false":
                return False
            if val in _KEYWORDS:
                raise ValueError(f"unexpected keyword {val!r}")
            # dotted field if it resolves; otherwise a bare-ident string constant (enum branch)
            resolved = _resolve_field(val, self.results)
            return resolved if resolved is not _MISSING else _EnumConst(val)
        raise ValueError(f"unexpected token {(kind, val)!r}")

    @staticmethod
    def _eq(a, b):
        a = a.name if isinstance(a, _EnumConst) else a
        b = b.name if isinstance(b, _EnumConst) else b
        try:
            return float(a) == float(b)
        except (TypeError, ValueError):
            return str(a) == str(b)

    def _apply(self, op, a, b):
        if a is _MISSING or b is _MISSING:
            return False           # a comparison over an unobserved field is never satisfied
        if op == "==":
            return self._eq(a, b)
        if op == "!=":
            return not self._eq(a, b)
        try:
            a, b = float(a.name if isinstance(a, _EnumConst) else a), \
                   float(b.name if isinstance(b, _EnumConst) else b)
        except (TypeError, ValueError):
            return False
        return {">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}[op]


@dataclass(frozen=True)
class _EnumConst:
    name: str


def evaluate(expr: str, results: dict) -> bool:
    """Evaluate a guard expression against an observed-results mapping. Missing fields → False."""
    if not expr or not expr.strip():
        return True
    return _Parser(_tokenize(expr), results or {}).parse()


# --------------------------------------------------------------------------- walk + scoring

def walk(graph: DecisionGraph, results: dict) -> list:
    """The data-conditioned correct trajectory: at each node take the first guarded edge whose
    guard holds (default last). Cycle-guarded. Returns the list of node keys visited."""
    path, node, visited = [graph.entry], graph.entry, {graph.entry}
    while True:
        out = graph.edges_from(node)
        if not out:
            break
        chosen = next((e for e in out
                       if not e.is_default and evaluate(e.when or "", results)), None)
        if chosen is None:
            chosen = next((e for e in out if e.is_default), None)
        if chosen is None or chosen.target in visited:
            break
        node = chosen.target
        visited.add(node)
        path.append(node)
    return path


def branch_decisions(graph: DecisionGraph, path: list, results: dict) -> dict:
    """{branch_node_key: correct_target} for every branch point on the walked path."""
    out = {}
    for i, key in enumerate(path[:-1]):
        if graph.is_branch_point(key):
            out[key] = path[i + 1]
    return out


def score_path(graph: DecisionGraph, oracle_results: dict, agent_choices: dict) -> dict:
    """Path Correctness: at each branch point on the oracle walk, did the agent take the
    oracle-correct edge? `agent_choices` maps branch_node_key -> the target the agent went to.

    Returns {pc, points_total, points_correct, per_point}. A branch point the agent never
    addressed counts against it (silence at a fork is not correct routing).
    """
    oracle_path = walk(graph, oracle_results)
    correct_at = branch_decisions(graph, oracle_path, oracle_results)
    per_point, correct = {}, 0
    for node_key, correct_target in correct_at.items():
        chosen = agent_choices.get(node_key)
        ok = (chosen == correct_target)
        per_point[node_key] = {"correct_target": correct_target, "chosen": chosen, "ok": ok}
        correct += int(ok)
    total = len(correct_at)
    return {"pc": (correct / total) if total else 1.0,
            "points_total": total, "points_correct": correct,
            "oracle_path": oracle_path, "per_point": per_point}
