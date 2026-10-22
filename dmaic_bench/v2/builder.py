"""v2 builder: resolve V2Cases × seeds into runnable ProjectTasks.

Each case ships canonical seeds proven to force *distinct* routes; the builder emits one
ProjectTask per (case, seed). A release invariant (checked by tests) is that a case's seeds
produce ≥2 distinct oracle routes — otherwise the case is not genuinely data-conditioned.
"""
from __future__ import annotations

from dmaic_bench.v2 import registry
from dmaic_bench.v2.models import ProjectTask, build_project_task


def build_all(cases: dict | None = None, seeds=None) -> list:
    cases = cases if cases is not None else registry.discover()
    tasks = []
    for cid in sorted(cases):
        case = cases[cid]
        for seed in (seeds if seeds is not None else case.seeds):
            tasks.append(build_project_task(case, seed))
    return tasks


def build_index(cases: dict | None = None, seeds=None) -> dict:
    return {t.task_id: t for t in build_all(cases, seeds)}


def distinct_routes(case) -> int:
    """How many distinct oracle routes the case's canonical seeds produce (data-conditioning proof)."""
    return len({tuple(case.oracle_route(s)) for s in case.seeds})
