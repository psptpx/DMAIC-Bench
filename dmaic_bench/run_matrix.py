"""Batch evaluation matrix for API-form contestants (the private contestant adapter today).

Runs (task instance × rep) cells sequentially or with a small thread pool, scoring each run
and appending one JSON line per cell to the output file. Resume-safe: existing (task_id, rep)
cells in the JSONL are skipped, so a crashed/interrupted campaign continues with
the exact same command. Errors are recorded as cells too — a backend hiccup must show up in
the ledger, not silently shrink the denominator.

JSONL cell: {"task_id", "rep", "ok", "card"?: scorecard, "error"?: str,
             "turns"?, "wall_clock_s"?, "ts"}
"""
from __future__ import annotations

import json
import os
import threading
import time

from . import taxonomy as taxonomy_mod
from .core.models import _to_jsonable


def load_done(out_path: str) -> set:
    done = set()
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if row.get("ok"):  # error cells re-run on resume
                    done.add((row["task_id"], row["rep"]))
    return done


def load_cards(out_path: str) -> list:
    cards = []
    with open(out_path, encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if row.get("ok") and row.get("card"):
                card = row["card"]
                card.setdefault("rep", row.get("rep"))
                cards.append(card)
    return cards


def run_matrix(cases: dict, tasks: list, adapter_factory, out_path: str, k: int = 3,
               parallel: int = 1, log=print, max_consecutive_errors: int = 8) -> dict:
    from .harness.steward import DataSteward
    from .scoring import scorer

    tax = taxonomy_mod.load()
    done = load_done(out_path)
    cells = [(t, rep) for t in tasks for rep in range(1, k + 1)
             if (t.task_id, rep) not in done]
    log(f"[matrix] {len(tasks)} tasks x k={k} -> {len(cells)} cells to run "
        f"({len(done)} already done)")
    lock = threading.Lock()
    # Circuit breaker: a wedged backend fails every cell in seconds — without this the campaign
    # burns the whole matrix into error rows (observed live: 1133 login timeouts in one run).
    stats = {"ok": 0, "error": 0, "consecutive_errors": 0, "aborted": False}

    def write_row(row):
        with lock:
            with open(out_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(_to_jsonable(row), ensure_ascii=False) + "\n")

    def run_cell(task, rep):
        started = time.time()
        try:
            adapter = adapter_factory()
            result = adapter.run(task, DataSteward(task))
            card = scorer.score_run(task, result.trace, result.report, tax,
                                    y_type=cases[task.case_id].meta.y_type)
            write_row({"task_id": task.task_id, "rep": rep, "ok": True, "card": card,
                       "turns": result.trace.turns,
                       "wall_clock_s": round(time.time() - started, 1),
                       "ts": time.strftime("%Y-%m-%dT%H:%M:%S")})
            with lock:
                stats["ok"] += 1
                stats["consecutive_errors"] = 0
            log(f"[matrix] OK  {task.task_id} rep{rep} "
                f"tgs={card.get('tgs'):.3f} ({time.time() - started:.0f}s)")
        except Exception as e:  # noqa: BLE001 — campaign must survive any single-cell failure
            write_row({"task_id": task.task_id, "rep": rep, "ok": False,
                       "error": f"{type(e).__name__}: {e}",
                       "wall_clock_s": round(time.time() - started, 1),
                       "ts": time.strftime("%Y-%m-%dT%H:%M:%S")})
            with lock:
                stats["error"] += 1
                stats["consecutive_errors"] += 1
                if stats["consecutive_errors"] >= max_consecutive_errors:
                    stats["aborted"] = True
            log(f"[matrix] ERR {task.task_id} rep{rep}: {type(e).__name__}: {e}")

    if parallel <= 1:
        for task, rep in cells:
            if stats["aborted"]:
                log(f"[matrix] ABORT: {max_consecutive_errors} consecutive errors — "
                    "backend likely down; resume the same command after it recovers")
                break
            run_cell(task, rep)
    else:
        sem = threading.Semaphore(parallel)
        threads = []

        def worker(task, rep):
            with sem:
                if stats["aborted"]:
                    return
                run_cell(task, rep)

        for task, rep in cells:
            th = threading.Thread(target=worker, args=(task, rep), daemon=True)
            th.start()
            threads.append(th)
        for th in threads:
            th.join()
    log(f"[matrix] done: {stats['ok']} ok, {stats['error']} errors -> {out_path}")
    return stats
