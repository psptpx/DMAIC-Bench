"""v3 harness: open a method-blind session for a contestant, persist its Deliverable (incl. the
declared methods), and grade it with two-channel scoring against the grounded oracle + method policy.
"""
from __future__ import annotations

import json
import os

from dmaic_bench.v2 import builder, sonnet_harness
from dmaic_bench.v3.method_policy import POLICY
from dmaic_bench.v3.scoring import score_run_v3
from dmaic_bench.v3.session import MethodBlindSession

_REC = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "runs", "v3-records"))


def open_session_v3(case_id: str, seed: int, fault: bool = False):
    case = sonnet_harness._get_case(case_id)
    task = builder.build_project_task(case, seed)
    return task, MethodBlindSession(task, fault=fault)


def save_record_v3(task_id: str, sess: MethodBlindSession, system_id: str, out_dir: str = _REC):
    rec = sess.record()
    os.makedirs(out_dir, exist_ok=True)
    dump = {"task_id": task_id, "system_id": system_id, "trajectory": rec.trajectory,
            "accepted": rec.accepted, "reported_stats": rec.reported_stats, "choices": rec.choices,
            "audit": rec.audit, "disclosed_denial": rec.disclosed_denial,
            "declared_methods": getattr(rec, "declared_methods", {})}
    path = os.path.join(out_dir, f"{system_id}__{task_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dump, f, ensure_ascii=False, indent=2)
    return path


#: adb_c15 is scored against an independently-grounded oracle so NF is fair. That oracle
#: (`ground_adb_c15`) lives in a `baselines/` directory beside the package in the authors'
#: workspace; it is NOT part of this repository, and neither is adb_c15 itself, which is one
#: of the nine held-out cases (docs/HELD_OUT.md). The branch below is therefore unreachable
#: from the public corpus and fails loudly rather than half-working if it is ever reached.
_GROUNDED_ORACLE_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "baselines"))
_GROUNDED_CASES = {"adb_c15": "ground_adb_c15"}


def _grounded_task(case_id: str, seed: int):
    """Open a v3 task, substituting the independently-grounded oracle where one exists."""
    import dataclasses
    import sys
    task, _ = open_session_v3(case_id, seed)
    module = _GROUNDED_CASES.get(case_id)
    if module is None:
        return task
    if not os.path.isdir(_GROUNDED_ORACLE_DIR):
        raise FileNotFoundError(
            f"{case_id} is scored against the grounded oracle {module!r}, which is expected "
            f"in {_GROUNDED_ORACLE_DIR!r}. That directory is not part of this repository "
            f"(see docs/HELD_OUT.md). Scoring this case against the ordinary oracle would "
            f"silently change what NF measures, so it is refused rather than approximated."
        )
    if _GROUNDED_ORACLE_DIR not in sys.path:
        sys.path.insert(0, _GROUNDED_ORACLE_DIR)
    ground = getattr(__import__(module), "ground")
    return dataclasses.replace(task, oracle_results={**ground(task), "_shape": task.shape})


def score_records_v3(case_id: str, seed: int | None = None, system_filter: str = "",
                     out_dir: str = _REC):
    from dmaic_bench.v2.runner import RunRecord
    decisions = POLICY.get(case_id, ())
    cards = []
    if not os.path.isdir(out_dir):
        return cards
    for fn in sorted(os.listdir(out_dir)):
        if not fn.endswith(".json") or case_id not in fn or (system_filter and system_filter not in fn):
            continue
        d = json.load(open(os.path.join(out_dir, fn), encoding="utf-8"))
        rec_seed = int(d["task_id"].split("-s")[1].split("-")[0])
        if seed is not None and rec_seed != seed:
            continue
        task = _grounded_task(case_id, rec_seed)         # score each record against ITS OWN seed
        rec = RunRecord(task_id=d["task_id"], trajectory=d["trajectory"], accepted=d["accepted"],
                        reported_stats=d["reported_stats"], choices=d["choices"],
                        audit=d.get("audit", []), disclosed_denial=d.get("disclosed_denial", False))
        rec.declared_methods = d.get("declared_methods", {})
        # reconstruct the route the agent's reported values entail (credits reused-data / router-node
        # skips that the data-release log under-counts) — see MethodBlindSession.record rationale
        from dmaic_bench.core.graph import walk
        if rec.accepted:
            route = walk(task.graph, rec.accepted)
            if len(route) > len(rec.trajectory):
                rec.trajectory = route
                rec.choices = {k: route[i + 1] for i, k in enumerate(route[:-1])
                               if task.graph.is_branch_point(k)}
        card = score_run_v3(task, rec, decisions,
                            autonomy_level=d.get("autonomy_level", "L4"),
                            autonomy_cost=d.get("autonomy_cost", 0))
        card["system_id"] = d.get("system_id", fn)
        cards.append(card)
    return cards
