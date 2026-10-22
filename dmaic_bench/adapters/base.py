"""Contestant adapter contract + shared trace-assembly helpers.

An adapter owns its interaction loop (API-form systems talk SSE/chat; framework-form systems
work off a file scaffold). The only hard requirement is producing a RunResult whose Trace speaks
the canonical method_id vocabulary — nothing downstream knows which system ran.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..core.models import RunResult, TaskInstance, TraceStep


@runtime_checkable
class SystemAdapter(Protocol):
    system_id: str

    def run(self, task: TaskInstance, steward) -> RunResult:  # steward: harness.steward.DataSteward
        ...


def steps_from_flat_results(results: dict, failed: list, spec_to_method) -> tuple:
    """Assemble TraceSteps from a {specKey: {flatField: scalar}} result map + failed spec list.

    ``spec_to_method`` maps a foreign spec key to a canonical method_id (None -> unknown).
    Returns (steps, warnings): unknown spec keys are skipped but reported so adapter bugs and
    taxonomy gaps stay visible instead of silently deflating MS scores.
    """
    steps, warnings, step_id = [], [], 0
    for spec_key, outputs in (results or {}).items():
        method_id = spec_to_method(spec_key)
        if method_id is None:
            warnings.append(f"unknown spec key {spec_key!r} — no taxonomy mapping, step dropped")
            continue
        step_id += 1
        steps.append(TraceStep(
            step_id=step_id, method_id=method_id,
            outputs=dict(outputs) if isinstance(outputs, dict) else {"value": outputs},
            status="success",
        ))
    for spec_key in failed or []:
        method_id = spec_to_method(spec_key)
        if method_id is None:
            warnings.append(f"unknown failed spec key {spec_key!r}")
            continue
        step_id += 1
        steps.append(TraceStep(step_id=step_id, method_id=method_id, status="failed"))
    return tuple(steps), warnings
