"""The data-conditioned half of a v2 task's truth package, and the two things a verifier does
with it: derive the correct branch at every fork, and ask whether the contestant's route
followed from the contestant's OWN numbers.

WHY THIS MODULE IS IN ``dmaic_bench`` AND NOT IN ``dmaic_harbor``
----------------------------------------------------------------
Both halves of the contract need it. The builder writes the graph into ``truth.json``; the
verifier -- a SEPARATE image that carries only ``verify.py``, ``spec.py`` and the
``dmaic_bench`` wheel -- reads it back and recomputes. Putting the recomputation in the
harbor package would mean shipping a second copy into the verifier image, and two copies of a
ground-truth rule drift. There is exactly one implementation and it travels in the wheel.

WHAT CHANGES, AND WHAT DELIBERATELY DOES NOT
--------------------------------------------
The Process-Quality axis stays exactly where it is, with the same formula and the same scorer.
What changes is where ``DecisionPoint.correct_branch`` COMES FROM. In the v1 corpus it is a
string an author typed into ``case.yaml``, so two data draws cannot demand two different
correct routes -- measured on the shipped English build, 19 of 79 decision-point instances
recur at more than one seed and **none** of them changes branch. Here the correct branch is
``walk(graph, oracle_results)``: the guards are evaluated against the results the oracle
actually computed for THIS seed, so the same decision point genuinely forks between seeds.

Self-Consistency is added as a DIAGNOSTIC and never enters the reward. It answers a different
question from PQ. PQ asks "was the route right?"; SC asks "did the route follow from the
numbers this contestant itself observed?". The two separate a numeric failure (wrong numbers
-> wrong-but-consistent route) from a judgement failure (right numbers -> wrong route), which
one score cannot do -- and it is a diagnostic rather than a gate precisely because a
contestant is free to be consistently wrong and that is already priced by NF.
"""
from __future__ import annotations

from dmaic_bench.core.graph import (DecisionGraph, GraphNode, GuardedEdge, branch_decisions,
                                    score_path, walk)

SCHEMA = "dmaic-graph-truth/1"


# --------------------------------------------------------------------------- (de)serialisation

def graph_to_payload(graph: DecisionGraph) -> dict:
    return {
        "entry": graph.entry,
        "nodes": [{"key": n.key, "phase": n.phase, "methods": list(n.methods),
                   "produces": list(n.produces), "label": n.label} for n in graph.nodes],
        "edges": [{"source": e.source, "target": e.target, "when": e.when,
                   "is_default": bool(e.is_default), "guard_fields": list(e.guard_fields)}
                  for e in graph.edges],
    }


def graph_from_payload(payload) -> DecisionGraph:
    """Rebuild a graph from ``truth.json``. Untrusted input: malformed entries are dropped
    rather than allowed to raise, because an unscored trial is worse than a scored zero."""
    payload = payload if isinstance(payload, dict) else {}
    nodes = []
    for n in payload.get("nodes") or ():
        if not isinstance(n, dict) or not isinstance(n.get("key"), str):
            continue
        nodes.append(GraphNode(
            key=n["key"], phase=str(n.get("phase") or ""),
            methods=tuple(m for m in (n.get("methods") or ()) if isinstance(m, str)),
            produces=tuple(p for p in (n.get("produces") or ()) if isinstance(p, str)),
            label=str(n.get("label") or "")))
    edges = []
    for e in payload.get("edges") or ():
        if not isinstance(e, dict) or not isinstance(e.get("source"), str) \
                or not isinstance(e.get("target"), str):
            continue
        when = e.get("when")
        edges.append(GuardedEdge(
            source=e["source"], target=e["target"],
            when=when if isinstance(when, str) else None,
            is_default=bool(e.get("is_default")),
            guard_fields=tuple(g for g in (e.get("guard_fields") or ())
                               if isinstance(g, str))))
    return DecisionGraph(nodes=tuple(nodes), edges=tuple(edges),
                         entry=str(payload.get("entry") or (nodes[0].key if nodes else "")))


# --------------------------------------------------------------------------- decision points

#: Methods that can never be evidence of a BRANCH, because running one is uninformative about
#: intent. `scoring.ms.ALWAYS_RELEVANT` already declares these legitimate anywhere and exempts
#: them from the precision penalty: they are the precondition checks a careful analyst runs
#: before committing to anything. The two positions cannot both hold, and this one gives.
#:
#: It mattered in one specific, common place. On the stability fork the correct branch is the
#: special-cause investigation, which runs the same chart the fork itself ran and so carries no
#: unique signature; the WRONG branch carried `basic.normality` as its only signature, in 8 of
#: the 15 cases. A contestant that diverted correctly and ran a normality check -- a thing this
#: repository elsewhere calls always legitimate -- was recorded as having failed to divert.
#:
#: 58 of 331 branch-evidence entries on shipped routes were entirely these methods. It changed
#: no verdict for the first model measured, because that model always computed a capability
#: index as well, which is the real error and still convicts. It would have bitten a more
#: disciplined one -- which is the system a benchmark exists to tell apart.
try:                                      # pragma: no cover - import shape, not behaviour
    from dmaic_bench.scoring.ms import ALWAYS_RELEVANT as _NOT_BRANCH_EVIDENCE
except ImportError:                       # pragma: no cover
    _NOT_BRANCH_EVIDENCE = frozenset()


def branch_evidence(graph: DecisionGraph, source: str, node_methods: dict) -> dict:
    """``{target: [method_id]}`` -- what TAKING each branch of *source* looks like in a trace.

    A method is evidence for a branch only when it is UNIQUE to that branch's node among the
    nodes that have a data batch at all. Everything else is excluded, and each exclusion closes
    a measured false positive:

    * **the self-loop is not a branch.** ``M_msa -> M_msa`` ("the gauge failed, go back and fix
      it") is walked by re-running the gauge study, which is byte-identical in a trace to doing
      the gauge study correctly the first time. Scored as evidence it convicts every compliant
      agent of taking the retry branch.
    * **a method the SOURCE node also runs** cannot say which edge was taken: ``M_stability``
      runs the individuals chart and so does ``A_special_cause``.
    * **a method shared with a sibling target** cannot tell the siblings apart.
    * **a method that appears ANYWHERE ELSE in the graph on a node with data.** This one is not
      hypothetical and not local: on ``chem_yield`` seed 3 the correct route is the NON-normal
      capability branch and then, four nodes later, an improvement-confirmation node that runs
      normal capability. Scoring that later, legitimate run as evidence at the earlier fork
      records the compliant agent as having walked the normal-capability branch and marks its
      correct route incorrect.
    * **a node with no data batch contributes nothing.** Its methods cannot be computed from
      anything the steward holds, so requiring them as corroboration would fail every honest
      agent; PQ falls back to the contestant's declaration for such a branch.
    * **a method REACHABLE FROM A SIBLING BRANCH is not unique to this one.** The exclusions
      above are all node-local, and branches nest: ``D_scope -> D_stratify -> M_agree`` means
      that taking the stratify branch runs everything the other branch runs, a step later. The
      agreement study is unique to ``M_agree`` as a NODE and is not evidence of having gone
      there directly. Measured on adb_c32 seed 2, where the correct branch is D_stratify and a
      run that executed exactly the on-route methods was recorded as having taken the other one.
      ``convergent_evidence`` has always reasoned over subtrees; this is the same correction on
      the path PQ consults first.

    ``node_methods`` is the resolved ``{node_key: methods}`` for the data-bearing nodes only --
    the builder passes exactly that set, and it doubles as the exclusion universe.
    """
    targets = [e.target for e in graph.edges_from(source) if e.target != source]
    source_methods = set(node_methods.get(source, ()))
    per_target = {t: set(node_methods.get(t, ())) for t in targets}
    elsewhere = {}
    for key, methods in node_methods.items():
        for m in methods:
            elsewhere.setdefault(m, set()).add(key)
    reachable_from = {t: _reachable(graph, t, source) for t in targets}
    out = {}
    for t, methods in per_target.items():
        shared = {m for m in methods if elsewhere.get(m, set()) - {t}}
        # Everything a SIBLING branch can reach, including the sibling itself.
        sibling_reach = set()
        for other in targets:
            if other != t:
                sibling_reach |= reachable_from[other]
        nested = {m for key in sibling_reach for m in node_methods.get(key, ())}
        unique = sorted(methods - source_methods - shared - nested
                        - _NOT_BRANCH_EVIDENCE)
        # A branch with an EMPTY evidence list is omitted, not stored as an empty list. It is
        # not a cosmetic difference: `pq._judge_point` reads `chosen in evidence` as "this point
        # knows what taking that branch looks like", and an empty list makes it say yes and then
        # find nothing, which convicts a correct declaration of being unsupported. Measured on
        # injection_molding seed 3, where the correct branch (special-cause investigation) runs
        # only a chart the previous node already ran: the compliant route scored PQ 0.5.
        if unique:
            out[t] = unique
    return out


def _reachable(graph: DecisionGraph, start: str, blocked: str) -> set:
    """Nodes reachable from *start* without passing back through *blocked* (the fork itself)."""
    seen, stack = set(), [start]
    while stack:
        k = stack.pop()
        if k in seen or k == blocked:
            continue
        seen.add(k)
        stack.extend(e.target for e in graph.edges_from(k))
    return seen


def convergent_evidence(graph: DecisionGraph, source: str, target: str,
                        node_methods: dict) -> list:
    """Methods that exist ONLY downstream of *target* -- proof the correct branch WAS taken.

    The mirror of :func:`divergent_evidence`, and needed for the opposite shape of fork: where
    the CORRECT branch carries the work and the wrong one is the terminal node. There the
    divergent set is empty (a remediation node runs nothing), so a wrong turn leaves no trace
    and abstention alone cannot be credited -- crediting it would pass the agent that wrongly
    stopped. What separates them is whether the correct branch's own downstream work happened.
    """
    correct = _reachable(graph, target, source)
    wrong = set()
    for e in graph.edges_from(source):
        if e.target in (target, source):
            continue
        wrong |= _reachable(graph, e.target, source)
    wrong_methods = {m for k in wrong for m in node_methods.get(k, ())}
    source_methods = set(node_methods.get(source, ()))
    out = {m for k in (correct - wrong) for m in node_methods.get(k, ())}
    return sorted(out - wrong_methods - source_methods - _NOT_BRANCH_EVIDENCE)


def divergent_evidence(graph: DecisionGraph, source: str, target: str,
                       node_methods: dict, method_policy: dict = None) -> list:
    """Methods that exist ONLY downstream of a branch other than *target*.

    ``branch_evidence`` asks what the immediate target node runs, and drops any method shared
    with another node anywhere in the graph. On a fork whose correct branch is a terminal
    remediation node that runs nothing, and whose wrong branch runs a chart that recurs later in
    the graph, that leaves the point with NO signature on either side -- the correct route and
    the wrong one are byte-identical to the scorer, and every contestant scores zero whatever it
    does. (Measured: 4 of 26 tasks, all seven models, reward 0.000 with ms_recall 1.000.)

    Looking at the whole SUBTREE instead restores the distinction. Running a method that only
    exists past a branch you were not supposed to take is proof you took it; running none of
    them, having performed the fork's own diagnostic, is proof you did not.

    **Nodes WITHOUT a data batch count here.** ``node_methods`` holds only the batch-bearing
    ones, because a method whose data the steward never releases cannot be required as
    corroboration. But this set is used the other way round -- as proof the agent went somewhere
    it should not have -- and running an analysis the steward gave you no data for is at least
    as damning. Measured: on ``adb_c27`` seed 4 the gauge is unusable and the correct branch is
    to stop, and a contestant ran ``doe.factorial_analysis`` (declared on ``I_doe``, which has
    no batch) on it. Every other wrong-branch method was covered, so the one it happened to run
    was the one nothing watched, and abstention was credited to a run that did not abstain.
    """
    correct = _reachable(graph, target, source)
    wrong = set()
    for e in graph.edges_from(source):
        if e.target in (target, source):
            continue
        wrong |= _reachable(graph, e.target, source)

    policy = method_policy or {}

    def _declared(key):
        """Every method this node could call, batch-bearing or not, on ANY seed.

        Not just the one `method_policy` resolved for THIS seed. A node that chooses between
        `capability.normal` and `capability.nonnormal` by the distribution is asking one
        question -- "is this process capable?" -- and asking it past a fork that said not to is
        the same error whichever variant is used.

        Measured, and it cost a finding. On `adb_c29` seed 4 the policy resolves A_capability
        to `capability.nonnormal`, so `capability.normal` was in no divergent set. All three
        contestants computed `capability.normal` on a run their own chart had just flagged as
        unstable, and all three were scored as having correctly diverted. That was the single
        B-divert task any system "solved", and it was a scoring artefact: the error was made,
        and the corpus was not watching for that spelling of it.
        """
        node = graph.node(key)
        out = set(node_methods.get(key) or ()) | set((node.methods if node else ()) or ())
        for clause in policy.get(key) or ():
            out |= set(clause.get("methods") or ())
        return out

    correct_methods = {m for k in correct for m in _declared(k)}
    source_methods = _declared(source)
    out = {m for k in (wrong - correct) for m in _declared(k)}
    return sorted(out - correct_methods - source_methods - _NOT_BRANCH_EVIDENCE)


def decision_points(graph: DecisionGraph, results: dict, node_methods: dict,
                    method_policy: dict = None, accepted_methods: dict = None) -> list:
    """The data-conditioned decision points for one seed, as plain dicts.

    One entry per branch point ON THE ORACLE WALK -- the same set ``core.graph.score_path``
    scores, so the two cannot disagree about what was asked. ``correct_branch`` is computed,
    never authored.
    """
    path = walk(graph, results)
    correct_at = branch_decisions(graph, path, results)
    out = []
    for source, target in correct_at.items():
        node = graph.node(source)
        evidence = branch_evidence(graph, source, node_methods)
        alternatives = sorted({e.target for e in graph.edges_from(source)}
                              - {target, source})
        out.append({
            "point_id": source,
            "phase": node.phase if node is not None else "",
            "rule": _rule_for(graph, source, target),
            "source": "decision graph guard, evaluated on this seed's oracle results",
            "correct_branch": target,
            "acceptable_branches": [],
            "branch_evidence": evidence,
            "source_evidence": sorted(node_methods.get(source, ())),
            "divergent_evidence": divergent_evidence(graph, source, target, node_methods,
                                                     method_policy),
            "convergent_evidence": convergent_evidence(graph, source, target, node_methods),
            "alternatives": alternatives,
            "acceptable_methods": sorted((accepted_methods or {}).get(source, ())),
        })
    return out


def _rule_for(graph: DecisionGraph, source: str, target: str) -> str:
    for e in graph.edges_from(source):
        if e.target == target:
            return e.when or ("(default branch)" if e.is_default else "(unconditional)")
    return ""


# --------------------------------------------------------------------------- observed results

def _norm(name) -> str:
    return "".join(c for c in str(name).lower() if c.isalnum())


def _set_dotted(target: dict, dotted: str, value) -> None:
    parts = dotted.split(".")
    cur = target
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    cur[parts[-1]] = value


def observed_results(field_map: dict, outputs_by_method: dict, fallback: dict | None = None,
                     outputs_by_occurrence: dict | None = None):
    """Rebuild the guard-field namespace from the CONTESTANT's own reported outputs.

    ``outputs_by_method`` is ``{method_id: {flattened output key: float}}`` for the methods the
    contestant ran successfully. Each ``field_map`` entry names candidate producers in priority
    order; the first one the contestant actually ran supplies the value, scaled into the units
    the guard is written in.

    ``fallback`` (the oracle's results) is consulted ONLY for guard fields that no ``field_map``
    entry describes -- a structural observation such as "were the subgroup sizes constant?"
    that no method in the taxonomy reports. Those fields are not something a trace can be
    inconsistent about, so charging a contestant for them would measure the field map's
    coverage rather than the contestant. They are returned in ``unobservable`` so the gap is
    reported rather than hidden.

    A source may pin itself to one INVOCATION of its method with ``"occurrence": n`` (0-based,
    in execution order), resolved out of ``outputs_by_occurrence`` keyed by ``(method_id, n)``.
    ``outputs_by_method`` merges every successful step of a method with last-wins, which is
    correct while a method runs once and destroys the earlier value when it runs twice -- and a
    project that re-runs a measurement study after remediation runs it twice ON PURPOSE, with
    the whole decision resting on the two verdicts being different. Without the pin, the second
    study's number answers for the first and the re-walk takes a branch the contestant did not.

    Returns ``(results, seen_fields, unobservable_fields)``.
    """
    results: dict = {}
    seen, unobservable = [], []
    for dotted, sources in sorted((field_map or {}).items()):
        value = None
        for src in sources or ():
            if not isinstance(src, dict):
                continue
            mid = src.get("method_id")
            occ = src.get("occurrence")
            if occ is None:
                outs = outputs_by_method.get(mid)
            else:
                try:
                    outs = (outputs_by_occurrence or {}).get((mid, int(occ)))
                except (TypeError, ValueError):
                    outs = None
            if not outs:
                continue
            want = _norm(src.get("output"))
            hit = None
            for key, val in outs.items():
                segs = str(key).split(".")
                if any(_norm(".".join(segs[i:])) == want for i in range(len(segs))):
                    hit = val
                    break
            if hit is None:
                continue
            scale = src.get("scale", 1.0)
            try:
                value = float(hit) * float(scale if scale else 1.0)
            except (TypeError, ValueError):
                continue
            break
        if value is not None:
            _set_dotted(results, dotted, value)
            seen.append(dotted)
    for dotted in sorted(_guard_fields_needed(fallback)):
        if dotted not in (field_map or {}):
            resolved = _read_dotted(fallback or {}, dotted)
            if resolved is not None:
                _set_dotted(results, dotted, resolved)
                unobservable.append(dotted)
    return results, seen, unobservable


def _guard_fields_needed(fallback) -> list:
    """Every dotted leaf of the oracle results (minus the private ``_shape`` marker)."""
    out = []

    def walk_dict(node, prefix):
        if isinstance(node, dict):
            for k, v in node.items():
                if str(k).startswith("_"):
                    continue
                walk_dict(v, f"{prefix}.{k}" if prefix else str(k))
        elif isinstance(node, (int, float)) and not isinstance(node, bool):
            out.append(prefix)

    walk_dict(fallback or {}, "")
    return out


def _read_dotted(source: dict, dotted: str):
    cur = source
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur if isinstance(cur, (int, float)) and not isinstance(cur, bool) else None


# --------------------------------------------------------------------------- agent's route

def infer_branch(graph: DecisionGraph, source: str, node_methods: dict, successful) -> str:
    """Which edge out of *source* the trace actually took, judged on downstream work.

    ``branch_evidence`` only looks at the immediate target and drops any method shared with
    another node anywhere in the graph, so on the forks that decide a prerequisite it is empty
    on BOTH sides and no branch can be inferred. Looking at what is reachable past each edge
    restores the distinction, and lets a terminal branch -- "stop and repair the gauge", which
    runs nothing by definition -- be inferred from the absence of every other branch's work.
    """
    targets = [e.target for e in graph.edges_from(source) if e.target != source]
    hit, terminal = [], []
    for t in targets:
        con = convergent_evidence(graph, source, t, node_methods)
        if con:
            if any(m in successful for m in con):
                hit.append(t)
        else:
            terminal.append(t)
    if len(hit) == 1:
        return hit[0]
    if not hit and len(terminal) == 1:
        # No branch that entails work shows any; the only edge that entails none is the one
        # taken -- but only if the fork's own diagnostic ran, so this is a decision and not
        # merely a trace that did nothing.
        if any(m in successful for m in node_methods.get(source, ())):
            return terminal[0]

    # A pure ROUTING node ("which attribute chart applies?") carries no diagnostic of its own,
    # so the guard above can never fire for it, and where the siblings' subtrees merge again a
    # step later the convergent sets come back empty for both. Their OWN methods still tell them
    # apart, so compare those directly -- the narrowest signal that still distinguishes.
    own = {t: set(node_methods.get(t, ())) for t in targets}
    ran = [t for t in targets
           if own[t] and (own[t] - set().union(*(own[o] for o in targets if o != t)))
           & set(successful)]
    if len(ran) == 1:
        return ran[0]
    return None


def agent_choices(graph: DecisionGraph, node_methods: dict, route_decisions, successful) -> dict:
    """``{branch_node: target}`` -- the edge the contestant took at each fork.

    Its own DECLARATION wins where it made one; otherwise the branch is inferred from what it
    actually executed, and only when exactly one branch's unique evidence appears (two branches
    walked is not a choice, it is running both, and PQ already charges for that).

    Covers every branch point in the graph, not only those on the oracle walk: Self-Consistency
    asks about the contestant's OWN walk, which may fork somewhere the oracle's does not.
    """
    declared = {}
    for r in route_decisions or ():
        point = getattr(r, "point", None) or (r.get("point") if isinstance(r, dict) else None)
        chosen = (getattr(r, "chosen_branch", None)
                  or (r.get("chosen_branch") if isinstance(r, dict) else None))
        if point and chosen:
            declared[str(point)] = str(chosen)      # last declaration wins
    successful = set(successful or ())
    out = {}
    for node in graph.nodes:
        if not graph.is_branch_point(node.key):
            continue
        if node.key in declared:
            out[node.key] = declared[node.key]
            continue
        evidence = branch_evidence(graph, node.key, node_methods)
        walked = [b for b, items in evidence.items()
                  if items and any(i in successful for i in items)]
        if len(walked) == 1:
            out[node.key] = walked[0]
            continue
        # `declared` is keyed by the name the CONTESTANT gave the fork, and this loop looks it
        # up by the graph's private node key, which the task instruction never exposes -- so a
        # declaration can only ever bind for the oracle. Where the immediate-target evidence is
        # also blank, which is the norm on prerequisite forks, the fork recorded no choice at
        # all and `score_path` counted the silence against the contestant.
        inferred = infer_branch(graph, node.key, node_methods, successful)
        if inferred is not None:
            out[node.key] = inferred
    return out


# --------------------------------------------------------------------------- the two scores

def process_quality(graph: DecisionGraph, oracle_results: dict, agent_choices: dict) -> dict:
    """PQ over the graph: at each fork on the ORACLE walk, did the agent take the right edge?"""
    return score_path(graph, oracle_results, agent_choices)


def self_consistency(graph: DecisionGraph, agent_results: dict, choices: dict) -> dict:
    """SC: at each fork on the AGENT'S OWN walk, did the agent take the edge its own numbers
    demand? Reported, never gated -- see the module docstring.

    ``score_path``'s first argument is the results the walk is computed from, so passing the
    AGENT's results here is the whole difference between this and PQ. The key it returns is
    still called ``oracle_path`` because that is the function's own vocabulary; here it is the
    path the contestant's own numbers imply, which is renamed on the way out."""
    card = score_path(graph, agent_results, choices)
    return {"sc": card["pc"], "sc_points_total": card["points_total"],
            "sc_points_correct": card["points_correct"],
            "implied_path": card["oracle_path"], "per_point": card["per_point"]}
