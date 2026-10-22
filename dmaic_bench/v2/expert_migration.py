"""Migrate the frozen expert-case FLAT decision-point ground truth into a v2 conditional
``DecisionGraph``.

v1 froze each ``DecisionPoint.correct_branch`` at authoring time, so an expert case carries a
single scripted trajectory — there is no runtime guard telling the walker *when* the correct
branch differs. This module reconstructs a conditional graph from that flat truth:

* a ``GraphNode`` per stage (methods pulled from ``NODE_METHOD_MAP``);
* stages chained in DMAIC phase order (Define→Measure→Analyze→Improve→Control) as the linear
  backbone, with ``order_constraints`` (before→after) respected inside each phase;
* for every ``DecisionPoint`` a guard is *synthesized* from the rule/point-id keywords onto a
  known template (stability / normality / capability / curvature / MSA / attribute-route). A
  multi-branch decision point becomes a decision node with one ``GuardedEdge`` per branch; a
  single-branch gate conditions the backbone edge leaving its stage.

The legacy DecisionPoint has NO runtime guard expression, so where no template matches we emit
the frozen ``correct_branch`` as the non-default edge and record the point in an ``unmapped``
list — the function is honest about which points got a real data-conditioned guard vs a
documented placeholder.

Frozen expert data ⇒ a single determinate oracle route (expected for reconstructed cases). The
value of the migration is the *shape*: the same graph would fork on different results, so a
scripted single-path solver no longer trivially aces the routing.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge
from dmaic_bench.core.models import PHASES
from dmaic_bench.v2.models import V2Case


# --------------------------------------------------------------------------- guard templates

# Each template is a *real* data-conditioned gate over the nested-dict result shape graph.walk
# reads (control_chart.imr -> imr.outOfControl, normality -> normality.pValue, capability ->
# cap.ppk, doe curvature -> doe.curvature_pValue, msa/gage/kappa -> msa.pctTol, attribute-route
# -> y.type). Matching is intent-first: a point's id tokens (`id_keys`, e.g. `_msa_gate`,
# `_attr_capability_route`) are checked before its rule prose (`rule_keys`), so an MSA gate whose
# rule mentions "capability" (the downstream capability step it unlocks) still binds to the MSA template
# rather than the capability template. Templates are ordered most-specific first.
GUARD_TEMPLATES = (
    # (id_keys, rule_keys, guard_expr, guard_fields, template_id)
    (("msa", "gage", "grr", "kappa", "agreement"),
     ("kappa", "agreement", "gage r&r", "%grr", "%studyvar", "ndc", "grr", "gauge", "measurement system"),
     "msa.pctTol <= 0.30", ("msa.pctTol",), "msa"),
    (("stability", "stable"),
     ("i-mr", "statistical control", "in control", "out of control", "stability"),
     "imr.outOfControl == 0", ("imr.outOfControl",), "stability"),
    (("curvature",),
     ("curvature", "axial points", "ccd", "response surface", "second-order response", "sequential experimentation"),
     "doe.curvature_pValue < 0.05", ("doe.curvature_pValue",), "curvature"),
    # attribute vs continuous capability routing (a genuine data-type fork)
    (("attr_capability", "attr_route", "capability_route"),
     ("attribute proportion", "binomial capability analysis", "attribute studies"),
     "y.type == attribute", ("y.type",), "attribute_route"),
    (("normality",),
     ("normality", "ad normality", "anderson"),
     "normality.pValue >= 0.05", ("normality.pValue",), "normality"),
    (("capability", "cap_gate"),
     ("capability index", "ppk", "cpk", "process capability"),
     "cap.ppk >= 1.33", ("cap.ppk",), "capability"),
)

# The nested keys each template's guard reads, plus the value that makes an EXPERT case (which
# took the correct branch) satisfy the guard — used to seed oracle_results so walk() reproduces
# the expert's route on frozen data.
TEMPLATE_ORACLE_SEED = {
    "stability":       ("imr", "outOfControl", 0),
    "normality":       ("normality", "pValue", 0.5),
    "curvature":       ("doe", "curvature_pValue", 0.01),   # significant curvature -> augment
    "capability":      ("cap", "ppk", 1.5),
    "msa":             ("msa", "pctTol", 0.15),
    "attribute_route": ("y", "type", "attribute"),
}


def _match_template(point) -> Optional[tuple]:
    """(guard_expr, guard_fields, template_id) for the first template that matches — id tokens
    first (highest precedence), then rule prose. None if nothing matches (placeholder path)."""
    pid = point.point_id.lower()
    rule = point.rule.lower()
    for id_keys, _rule_keys, expr, fields, tid in GUARD_TEMPLATES:
        if any(k in pid for k in id_keys):
            return expr, fields, tid
    for _id_keys, rule_keys, expr, fields, tid in GUARD_TEMPLATES:
        if any(k in rule for k in rule_keys):
            return expr, fields, tid
    return None


# --------------------------------------------------------------------------- migration report

@dataclass(frozen=True)
class MigratedPoint:
    point_id: str
    stage_id: Optional[str]
    correct_branch: str
    guard: Optional[str]        # the synthesized guard expr (None = placeholder)
    template_id: Optional[str]  # which template matched (None = placeholder)
    branch_node: Optional[str]  # decision-node key when a multi-branch node was inserted
    real: bool                  # True = real data-conditioned guard, False = documented placeholder


@dataclass(frozen=True)
class Migration:
    """The reconstructed graph plus an honest audit of every decision point."""
    graph: DecisionGraph
    mapped: tuple = ()      # tuple[MigratedPoint] — points with a real data-conditioned guard
    unmapped: tuple = ()    # tuple[MigratedPoint] — points that got a documented placeholder

    def points(self) -> tuple:
        return self.mapped + self.unmapped


# --------------------------------------------------------------------------- ordering helpers

def _phase_rank(phase: str) -> int:
    try:
        return PHASES.index(phase)
    except ValueError:
        return len(PHASES)


def _order_stages(stages, node_method_map, case_id, order_constraints) -> list:
    """Return stage keys in DMAIC phase order, applying before→after constraints as a stable
    topological nudge inside the linear backbone. `stages` is a list of (stage_key, phase)."""
    ordered = sorted(range(len(stages)), key=lambda i: (_phase_rank(stages[i][1]), i))
    keys = [stages[i][0] for i in ordered]

    # method_id -> first stage key that owns it (for translating method-level constraints)
    method_host = {}
    for skey, _ in stages:
        for m in node_method_map.get((case_id, skey), []):
            method_host.setdefault(m, skey)

    # Apply before→after: if both map to stages and after currently precedes before, move after
    # to just after before. Family / unknown methods are skipped (they may live case-level).
    for oc in order_constraints:
        b = method_host.get(getattr(oc, "before", None))
        a = method_host.get(getattr(oc, "after", None))
        if not b or not a or a == b or b not in keys or a not in keys:
            continue
        if keys.index(a) < keys.index(b):
            keys.remove(a)
            keys.insert(keys.index(b) + 1, a)
    return keys


# template_id -> method_id prefixes that identify the stage a gate should anchor to (the stage
# that PRODUCES the gate quantity, so the gate conditions the edge leaving it).
_TEMPLATE_STAGE_METHOD = {
    "msa": ("msa.",),
    "stability": ("control_chart.imr",),
    "curvature": ("doe.factorial",),
    "attribute_route": ("capability.binomial", "capability."),
    "capability": ("capability.",),
    "normality": ("capability.normal", "basic.normality"),
}


def _stage_for_point(point, template_id, ordered_keys, node_method_map, case_id,
                     claimed) -> Optional[str]:
    """The backbone stage a decision point anchors to. Precedence:
    1. a same-phase stage whose methods match the template's gate domain (the stage that PRODUCES
       the gate quantity — e.g. an MSA gate anchors on the MSA stage, not the capability step it
       unlocks) — this keeps distinct points on distinct anchors;
    2. a same-phase stage whose methods appear in the point's correct-branch evidence;
    3. the last stage of the point's phase.
    `claimed` accumulates already-used anchors so two gates in one phase don't collide."""
    same_phase = [k for k in ordered_keys if _STAGE_PHASE.get(k, "") == point.phase]

    prefixes = _TEMPLATE_STAGE_METHOD.get(template_id, ())
    for k in same_phase:
        methods = node_method_map.get((case_id, k), [])
        if any(m.startswith(p) for m in methods for p in prefixes) and k not in claimed:
            return k

    ev_methods = set()
    for methods in (point.branch_evidence or {}).values():
        ev_methods.update(m for m in methods if not str(m).startswith("family:"))
    for k in same_phase:
        if set(node_method_map.get((case_id, k), [])) & ev_methods and k not in claimed:
            return k

    for k in reversed(same_phase):
        if k not in claimed:
            return k
    return same_phase[-1] if same_phase else None


_STAGE_PHASE = {}


# --------------------------------------------------------------------------- core migration

def to_decision_graph(case_id, stages, decision_points, order_constraints,
                      node_method_map) -> Migration:
    """Convert flat expert ground truth into a conditional DecisionGraph.

    Parameters
    ----------
    stages : list[(stage_key, phase)]         backbone stages in declaration order
    decision_points : list[DecisionPoint]     flat frozen decision points
    order_constraints : list[OrderConstraint] before→after partial order
    node_method_map : dict[(case_id, key)->[method_id]]

    Returns a ``Migration`` (graph + mapped/unmapped audit).
    """
    stages = list(stages)
    _STAGE_PHASE.clear()
    _STAGE_PHASE.update({k: p for k, p in stages})

    ordered = _order_stages(stages, node_method_map, case_id, order_constraints)

    nodes = []
    for key in ordered:
        phase = _STAGE_PHASE.get(key, "")
        methods = tuple(node_method_map.get((case_id, key), []))
        nodes.append(GraphNode(key=key, phase=phase, methods=methods, label=key))

    # linear backbone edges
    edges = []
    for i in range(len(ordered) - 1):
        edges.append(GuardedEdge(ordered[i], ordered[i + 1]))

    entry = ordered[0] if ordered else ""

    mapped, unmapped = [], []
    claimed = set()

    for dp in decision_points:
        tmpl = _match_template(dp)
        tid = tmpl[2] if tmpl else None
        anchor = _stage_for_point(dp, tid, ordered, node_method_map, case_id, claimed)
        if anchor is not None:
            claimed.add(anchor)
        multi = len((dp.branch_evidence or {})) > 1

        if multi:
            rec = _apply_branch(dp, anchor, ordered, nodes, edges, tmpl)
        else:
            rec = _apply_gate(dp, anchor, ordered, edges, tmpl)

        (mapped if rec.real else unmapped).append(rec)

    graph = DecisionGraph(nodes=tuple(nodes), edges=tuple(edges), entry=entry)
    return Migration(graph=graph, mapped=tuple(mapped), unmapped=tuple(unmapped))


def _successor(key, ordered) -> Optional[str]:
    if key is None or key not in ordered:
        return None
    i = ordered.index(key)
    return ordered[i + 1] if i + 1 < len(ordered) else None


def _out_edge(edges, source):
    """The current non-default forward edge leaving `source` (the one carrying the backbone),
    as (index, edge) or (None, None)."""
    for i, e in enumerate(edges):
        if e.source == source and not e.is_default and e.target != source:
            return i, e
    return None, None


def _apply_branch(dp, anchor, ordered, nodes, edges, tmpl) -> MigratedPoint:
    """Insert a decision node with one GuardedEdge per branch. The correct branch is guarded by the
    synthesized guard (or, without a template, a documented placeholder that still resolves true on
    frozen expert data); the other branches are the documented alternative routes (default). All
    branches rejoin the backbone successor so nothing dangles."""
    bnode_key = f"{anchor or 'BRANCH'}__decide_{dp.point_id}"
    nodes.append(GraphNode(key=bnode_key, phase=dp.phase, label=f"decision:{dp.point_id}"))

    # route the anchor's current forward edge through the decision node
    idx, edge = _out_edge(edges, anchor) if anchor is not None else (None, None)
    succ = edge.target if edge is not None else _successor(anchor, ordered)
    if idx is not None:
        edges[idx] = GuardedEdge(anchor, bnode_key)
    elif anchor is not None:
        edges.append(GuardedEdge(anchor, bnode_key))

    guard_expr = tmpl[0] if tmpl else f"placeholder.{dp.point_id} == {dp.correct_branch}"
    guard_fields = tmpl[1] if tmpl else (f"placeholder.{dp.point_id}",)

    branches = list((dp.branch_evidence or {}).items())
    for bname, methods in branches:
        leaf = f"{bnode_key}__{bname}"
        bmethods = tuple(m for m in methods if not str(m).startswith("family:"))
        nodes.append(GraphNode(key=leaf, phase=dp.phase, methods=bmethods, label=bname))
        if bname == dp.correct_branch:
            edges.append(GuardedEdge(bnode_key, leaf, guard_expr, guard_fields=guard_fields))
        else:
            edges.append(GuardedEdge(bnode_key, leaf, is_default=True))
        if succ:
            edges.append(GuardedEdge(leaf, succ))

    return MigratedPoint(dp.point_id, anchor, dp.correct_branch,
                         tmpl[0] if tmpl else None, tmpl[2] if tmpl else None,
                         bnode_key, bool(tmpl))


def _apply_gate(dp, anchor, ordered, edges, tmpl) -> MigratedPoint:
    """Condition the anchor's forward backbone edge on the synthesized gate guard, and add a
    default self-loop (gate failed → rework/stay). With a template this is a real data-conditioned
    gate; without one the correct branch is emitted as a documented placeholder guard (reported
    unmapped) that still resolves true on frozen expert data so the reconstructed route holds."""
    idx, edge = _out_edge(edges, anchor) if anchor is not None else (None, None)
    if idx is None:
        return MigratedPoint(dp.point_id, anchor, dp.correct_branch,
                             tmpl[0] if tmpl else None, tmpl[2] if tmpl else None,
                             None, bool(tmpl))
    succ = edge.target
    if tmpl:
        edges[idx] = GuardedEdge(anchor, succ, tmpl[0], guard_fields=tmpl[1])
    else:
        edges[idx] = GuardedEdge(
            anchor, succ, f"placeholder.{dp.point_id} == {dp.correct_branch}",
            guard_fields=(f"placeholder.{dp.point_id}",))
    edges.append(GuardedEdge(anchor, anchor, is_default=True))  # gate-fail rework self-loop
    return MigratedPoint(dp.point_id, anchor, dp.correct_branch,
                         tmpl[0] if tmpl else None, tmpl[2] if tmpl else None,
                         None, bool(tmpl))


# --------------------------------------------------------------------------- V2Case assembly

def _stages_of(case) -> list:
    return [(s.stage_id, s.phase) for s in case.meta.stages]


def _legacy_case(case_id):
    from dmaic_bench.cases import legacy_bridge as lb
    for c in lb.legacy_cases():
        if c.case_id == case_id:
            return c
    raise KeyError(f"legacy case {case_id!r} not found in legacy_bridge.legacy_cases()")


def _legacy_bridge_available() -> bool:
    """True when the originating harness's assets that the legacy bridge wraps are
    importable (else the expert cases degrade to []); used by tests to skip cleanly.
    Always False in this repository: the bridge module is held out (docs/HELD_OUT.md)."""
    try:
        from dmaic_bench.cases import legacy_bridge as lb
        return bool(lb.legacy_cases())
    except Exception:
        return False


def _assemble_oracle_results(case, migration) -> dict:
    """Assemble the nested-dict oracle_results the graph guards read. Values come from (a) the
    case's frozen TruthEntry values, keyed into the guard field shape, and (b) template oracle
    seeds for every mapped gate/route (the expert took the correct branch, so the gate passes)."""
    res: dict = {}

    def put(section, key, value):
        res.setdefault(section, {})[key] = value

    # (a) seed each mapped point's guard so walk() reproduces the expert route
    for mp in migration.mapped:
        seed = TEMPLATE_ORACLE_SEED.get(mp.template_id)
        if seed:
            section, key, value = seed
            put(section, key, value)

    # (a') placeholder points: seed placeholder.<point_id> = <correct_branch> so the documented
    # placeholder guard resolves true on frozen expert data (the expert took the correct branch).
    for mp in migration.points():
        if not mp.real:
            put("placeholder", mp.point_id, mp.correct_branch)

    # (b) overlay real frozen truth values where they line up with a guard field
    for t in case.generate(0).truths:
        # capability ppk / processZ -> cap.ppk (only if a capability gate exists)
        if t.method_id.startswith("capability") and t.field.lower() in ("ppk", "pp"):
            put("cap", t.field.lower(), t.expected)
        if t.method_id == "control_chart.imr" and "outofcontrol" in t.field.lower():
            put("imr", "outOfControl", int(t.expected))
        if t.method_id == "basic.normality" and "pvalue" in t.field.lower():
            put("normality", "pValue", t.expected)
    return res


def to_v2_case(case_id: str) -> V2Case:
    """Build a V2Case from an expert legacy case: reconstruct the conditional graph and wrap a
    generate(seed) returning the frozen expert blocks + oracle_results assembled from the case's
    truths keyed into the guard-field shape. Frozen data ⇒ a single determinate route."""
    case = _legacy_case(case_id)
    migration = build_migration(case_id)
    graph = migration.graph

    frozen_blocks = case.generate(0).blocks
    oracle_results = _assemble_oracle_results(case, migration)
    oracle_results["_shape"] = "expert-frozen (single determinate route)"

    industry = case.meta.industry
    title = case.meta.title

    def generate(seed: int, _blocks=frozen_blocks, _res=oracle_results):
        import copy
        return copy.deepcopy(_blocks), copy.deepcopy(_res)

    gate_policy = tuple(
        {"stage": mp.stage_id or mp.branch_node or mp.point_id,
         "guard": mp.guard, "point_id": mp.point_id, "template": mp.template_id}
        for mp in migration.mapped
    )

    return V2Case(
        case_id=case_id,
        title=title,
        industry=industry,
        graph=graph,
        gate_policy=gate_policy,
        generate=generate,
        seeds=(0,),
        shapes={0: "expert-frozen"},
        node_data={n.key: n.key for n in graph.nodes},
        fault_targets=(),
        budget={"max_turns": len(graph.nodes) + 4},
    )


def build_migration(case_id: str) -> Migration:
    """Convenience: pull the expert case from legacy_bridge and run `to_decision_graph`."""
    case = _legacy_case(case_id)
    return to_decision_graph(
        case_id,
        _stages_of(case),
        list(case.meta.decision_points),
        list(case.meta.order_constraints),
        # rebuild the (case,key)->methods map from the case's stages so the migration is
        # self-contained (it mirrors NODE_METHOD_MAP for this case).
        {(case_id, s.stage_id): [m.method_id for m in s.methods] for s in case.meta.stages},
    )
