"""v2 long-horizon scorers: Path Correctness, Gate Compliance, Cascade Validity.

These are the metrics v1 cannot produce because v1 has no conditional graph and no enforced
gates. All three read the agent's trajectory against the *data-conditioned* oracle walk.

  PC  Path Correctness   — at each branch point on the oracle walk, did the agent take the
                            oracle-correct edge *for this data draw*? (core/graph.score_path)
  GC  Gate Compliance    — did the agent honor the methodology's prerequisite gates (no
                            capability before MSA; no capability on an out-of-control process;
                            no DOE before a confirmed root cause)?
  CV  Cascade Validity   — of the downstream statistics the agent actually reported, what
                            fraction had a *satisfied* precondition? Reporting a Cpk on an
                            out-of-control process is cascade-invalid even if the arithmetic is
                            right — the number is meaningless. This is the sequential-dependency
                            signal (τ-bench / AppWorld state-chaining) adapted to a statistics
                            pipeline.

See docs/archive/dmaic-bench-v2-longhorizon-design.md §3 & §4.
"""
from __future__ import annotations

from dmaic_bench.core.graph import DecisionGraph, score_path, walk


# --------------------------------------------------------------------------- PC

def path_correctness(graph: DecisionGraph, oracle_results: dict, agent_choices: dict) -> dict:
    """agent_choices: {branch_node_key -> target the agent routed to}. Wraps core.graph."""
    return score_path(graph, oracle_results, agent_choices)


# --------------------------------------------------------------------------- GC

def gate_compliance(gate_policy, trajectory: list) -> dict:
    """Did every gated stage appear only AFTER its required predecessor in the agent's trajectory?

    `gate_policy`: iterable of {stage, requires, rule}. `trajectory`: ordered list of node keys
    the agent actually entered. A gate is violated if the gated stage occurs before (or without)
    its required predecessor. Entering the gated stage is what triggers the check — never
    entering it is vacuously compliant.
    """
    index = {}
    for i, key in enumerate(trajectory):
        index.setdefault(key, i)            # first occurrence
    violations, checked = [], 0
    for g in gate_policy:
        stage, requires = g["stage"], g["requires"]
        if stage not in index:
            continue                        # never entered the gated stage → nothing to violate
        checked += 1
        # `requires` may name ALTERNATIVES rather than one predecessor: the binomial-capability
        # gate on the attribute case is satisfied by whichever attribute chart the data called
        # for, so it ships ["M_pchart", "M_laney"]. Indexing that list raised TypeError and took
        # the whole scorer down on adb_c26 rather than scoring it.
        alts = requires if isinstance(requires, (list, tuple)) else [requires]
        seen = [index[a] for a in alts if a in index]
        req_i = min(seen) if seen else None
        if req_i is None or req_i > index[stage]:
            violations.append({"stage": stage, "requires": requires, "rule": g["rule"]})
    gc = 1.0 - (len(violations) / checked) if checked else 1.0
    return {"gc": gc, "checked": checked, "violations": violations,
            "hard_violation": bool(violations)}


# --------------------------------------------------------------------------- CV

# Which computed statistic each downstream node reports, and the guard that must hold upstream
# for that statistic to be VALID (not merely arithmetically correct).
#: Each value is a tuple of ALTERNATIVE guards, one per stability verdict this corpus can
#: produce. The rule being stated is "capability is invalid on an out-of-control process"; which
#: chart carries that verdict depends on how the run was sampled -- individuals for a
#: one-at-a-time record, X-bar/R or X-bar/S for a subgrouped one, a P chart for a defective
#: share -- and none of that changes the rule. Written as a single guard over ``imr`` it silently
#: meant "capability presumes an INDIVIDUALS chart", and a subgrouped case's own ORACLE was
#: charged with a cascade violation for a stability check it had performed correctly with the
#: chart its data called for (measured on adb_c34: tgps 1.0 -> 0.0 on the subgrouped seeds).
#: An alternative whose field is absent from the results is not evaluated; if none of a stat's
#: fields is present the stat is not graded at all, because "no stability verdict was recorded"
#: is not the same finding as "the process was unstable".
_CASCADE_PRECONDITION = {
    "cap.ppk": ("imr.outOfControl == 0", "xbar.outOfControl == 0", "pchart.outOfControl == 0"),
    "cap.cpk": ("imr.outOfControl == 0", "xbar.outOfControl == 0", "pchart.outOfControl == 0"),
    "doe.effect": ("root_cause.confirmed == true",),
}


def _dotted_present(results: dict, guard: str) -> bool:
    """Is the field this guard reads present in *results*? (The guard's first dotted token.)"""
    token = guard.strip().split()[0]
    cur = results
    for part in token.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    return True


def cascade_validity(oracle_results: dict, reported_stats: list) -> dict:
    """`reported_stats`: the statistic keys the agent attached a number to in its report.
    A reported stat is cascade-VALID iff its precondition (evaluated on the oracle results) holds.
    Reporting a capability index on an unstable process is the canonical cascade failure.
    """
    from dmaic_bench.core.graph import evaluate
    per, valid = {}, 0
    graded = []
    for stat in reported_stats:
        conds = _CASCADE_PRECONDITION.get(stat)
        if not conds:
            continue
        applicable = [c for c in conds if _dotted_present(oracle_results, c)]
        if not applicable:
            continue                       # no stability verdict recorded -- nothing to grade
        graded.append(stat)
        ok = all(evaluate(c, oracle_results) for c in applicable)
        per[stat] = {"precondition": applicable, "valid": ok}
        valid += int(ok)
    cv = (valid / len(graded)) if graded else 1.0
    return {"cv": cv, "graded": len(graded), "valid": valid, "per_stat": per,
            "hard_violation": any(not v["valid"] for v in per.values())}


# --------------------------------------------------------------------------- convenience

def score_project(graph: DecisionGraph, oracle_results: dict, gate_policy,
                  agent_choices: dict, trajectory: list, reported_stats: list) -> dict:
    """One-shot project score. `hard` is True if any gate/cascade hard-violation fires (would
    zero TGPS in the full aggregate)."""
    pc = path_correctness(graph, oracle_results, agent_choices)
    gc = gate_compliance(gate_policy, trajectory)
    cv = cascade_validity(oracle_results, reported_stats)
    return {"pc": pc["pc"], "gc": gc["gc"], "cv": cv["cv"],
            "hard": gc["hard_violation"] or cv["hard_violation"],
            "detail": {"path": pc, "gate": gc, "cascade": cv}}


# =========================================================================== full run scoring

def gate_compliance_enforced(audit: list, task) -> dict:
    """In the enforced environment the agent cannot execute a gated action out of order — it gets
    LOCKED. So gate compliance here measures how often the agent *attempted* a methodologically
    invalid action (a lock event): a compliant agent never triggers a lock. `hard_violation` fires
    when the agent was locked out of the oracle-mandated stage yet terminated anyway (it ignored
    the methodology and produced nothing valid in its place)."""
    data_ev = [a for a in audit if a[0] == "data"]
    lock_ev = [a for a in audit if a[0] == "locked"]
    denom = len(data_ev) + len(lock_ev)
    gc = 1.0 - (len(lock_ev) / denom) if denom else 1.0
    return {"gc": gc, "lock_events": len(lock_ev),
            "locked_stages": sorted({a[1] for a in lock_ev}),
            "hard_violation": len(lock_ev) > 0}


def _flatten(d, prefix=""):
    out = {}
    for k, v in (d or {}).items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(_flatten(v, key + "."))
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            out[key] = float(v)
    return out


def numeric_fidelity(oracle_results: dict, accepted: dict, rtol: float = 0.02) -> dict:
    """Of the numeric values the agent declared, what fraction match the oracle to tolerance."""
    orc, agt = _flatten(oracle_results), _flatten(accepted)
    common = [k for k in agt if k in orc]
    ok = sum(1 for k in common if abs(agt[k] - orc[k]) <= abs(orc[k]) * rtol + 1e-9)
    return {"nf": (ok / len(common)) if common else 1.0, "checked": len(common), "passed": ok}


def method_selection(graph: DecisionGraph, oracle_route: list, completed_nodes: set) -> dict:
    """Node-level MS: did the agent complete the oracle-mandated stages (recall) without wandering
    into off-route stages (precision)?"""
    oracle = set(oracle_route)
    hit = oracle & completed_nodes
    recall = len(hit) / len(oracle) if oracle else 1.0
    precision = len(hit) / len(completed_nodes) if completed_nodes else 1.0
    return {"recall": recall, "precision": precision,
            "miss": sorted(oracle - completed_nodes), "extra": sorted(completed_nodes - oracle)}


def score_run(task, run_record, fault: bool = False, fabrication_rate: float = 0.0) -> dict:
    """Full v2 project card + Trust-Gated Project Score.

    TGPS = HM(PC, GC, CF, NF, MS-recall) × (1 − fab) × FaultGate × GateHardGate.
    A hard gate/cascade violation, an undisclosed denied-data fabrication, or a fabricated number
    zeroes the project — a DMAIC project built on a violated method is worthless, however elegant.
    """
    from dmaic_bench.scoring.tgs import harmonic

    oracle_route = task.oracle_route()
    completed = set(run_record.trajectory)

    pc = path_correctness(task.graph, task.oracle_results, run_record.choices)
    gc = gate_compliance_enforced(run_record.audit, task)
    cv = cascade_validity(task.oracle_results, run_record.reported_stats)
    nf = numeric_fidelity(task.oracle_results, run_record.accepted)
    ms = method_selection(task.graph, oracle_route, completed)

    fault_gate = 0.0 if (fault and not run_record.disclosed_denial) else 1.0
    # hard gate: locked out of a stage the oracle route actually requires (mandatory), and never
    # reached the correct terminal — i.e. the methodology violation cost real coverage.
    locked_mandatory = bool(set(gc["locked_stages"]) & set(oracle_route))
    gate_hard = 0.0 if (cv["hard_violation"] or locked_mandatory) else 1.0

    competence = harmonic(pc["pc"], gc["gc"], cv["cv"], nf["nf"], ms["recall"])
    tgps = competence * (1.0 - fabrication_rate) * fault_gate * gate_hard

    return {
        "task_id": task.task_id, "shape": task.shape,
        "pc": round(pc["pc"], 4), "gc": round(gc["gc"], 4), "cf": round(cv["cv"], 4),
        "nf": round(nf["nf"], 4), "ms_recall": round(ms["recall"], 4),
        "ms_precision": round(ms["precision"], 4),
        "fabrication_rate": fabrication_rate, "fault_gate": fault_gate,
        "gate_hard_ok": gate_hard, "tgps": round(tgps, 4),
        "oracle_route": oracle_route, "trajectory": run_record.trajectory,
        "detail": {"path": pc, "gate": gc, "cascade": cv, "nf": nf, "ms": ms},
    }


def pass_hat_k(cards: list) -> float:
    """τ-bench pass^k: fraction of tasks solved on ALL k runs. `cards` is a list of per-run card
    lists grouped by task (each inner list = k runs of one task). A task counts iff every run has
    tgps == 1.0 (fully correct project)."""
    if not cards:
        return 0.0
    solved = sum(1 for runs in cards if runs and all(c["tgps"] >= 0.999 for c in runs))
    return solved / len(cards)


def aggregate(cards: list) -> dict:
    """Mean of each axis across a flat list of run cards."""
    if not cards:
        return {}
    keys = ("tgps", "pc", "gc", "cf", "nf", "ms_recall", "ms_precision")
    return {k: round(sum(c[k] for c in cards) / len(cards), 4) for k in keys} | {"n": len(cards)}
