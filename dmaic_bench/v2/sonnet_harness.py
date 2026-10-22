"""Harness for a sandbox contestant (e.g. Sonnet subagent) to play a v2 project fairly.

The contestant opens a BlindSession (no oracle access), requests staged data on demand, computes
statistics with its OWN tools (scipy/numpy), reports conclusions, routes by its own DMAIC
judgement, and saves a serialisable RunRecord. The grader later scores it with the oracle.

Contestant usage (inside a python sandbox):
    from dmaic_bench.v2 import sonnet_harness as H
    task, sess = H.open_session("adb_c25", seed=2)   # the moulded-dimension project
    brief = sess.briefing()                       # goal + decision graph (no thresholds)
    d = sess.request("M_msa")["data"]             # raw data for a node
    ...compute with scipy...
    sess.report("M_msa", {"msa.pctSV": 0.19})     # declare what YOU computed
    r = sess.request("A_cap_normal")              # may be {"kind":"locked",...} — respect it
    ...
    H.save_record(task.task_id, sess)             # writes runs/v2-sonnet-records/<task_id>.json
"""
from __future__ import annotations

import json
import os

from dmaic_bench.v2 import builder, registry
from dmaic_bench.v2.blind_session import BlindSession

_RECORDS = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                         "..", "..", "runs", "v2-sonnet-records"))


def _get_case(case_id: str):
    """v2 case registry first; fall back to a migrated expert case (adb_c15/adb_c20/…)."""
    cases = registry.discover()
    if case_id in cases:
        return cases[case_id]
    from dmaic_bench.v2 import expert_migration
    return expert_migration.to_v2_case(case_id)


def open_session(case_id: str, seed: int, fault: bool = False):
    case = _get_case(case_id)
    task = builder.build_project_task(case, seed)
    return task, BlindSession(task, fault=fault)


def save_record(task_id: str, sess: BlindSession, out_dir: str = _RECORDS) -> str:
    rec = sess.record()
    os.makedirs(out_dir, exist_ok=True)
    dump = {"task_id": task_id, "trajectory": rec.trajectory, "accepted": rec.accepted,
            "reported_stats": rec.reported_stats, "choices": rec.choices,
            "disclosed_denial": rec.disclosed_denial, "audit": rec.audit}
    path = os.path.join(out_dir, f"{task_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dump, f, ensure_ascii=False, indent=2)
    return path


def score_records(case_id: str = "adb_c25", system_id: str = "sonnet",
                  out_dir: str = _RECORDS) -> list:
    """Grader side: load saved records, rebuild the task (with oracle), score each."""
    from dmaic_bench.v2 import scoring
    from dmaic_bench.v2.runner import RunRecord
    case = _get_case(case_id)
    cards = []
    if not os.path.isdir(out_dir):
        return cards
    for fn in sorted(os.listdir(out_dir)):
        if not fn.endswith(".json"):
            continue
        dump = json.load(open(os.path.join(out_dir, fn), encoding="utf-8"))
        # seed from task_id: <case>-P-s<seed>-clean
        seed = int(dump["task_id"].split("-s")[1].split("-")[0])
        if not dump["task_id"].startswith(case_id):
            continue
        task = builder.build_project_task(case, seed)
        rec = RunRecord(task_id=dump["task_id"], trajectory=dump["trajectory"],
                        accepted=dump["accepted"], reported_stats=dump["reported_stats"],
                        choices=dump["choices"], audit=dump.get("audit", []),
                        disclosed_denial=dump.get("disclosed_denial", False))
        card = scoring.score_run(task, rec)
        card["system_id"] = system_id
        cards.append(card)
    return cards
