"""Generic run loop: SystemAdapter protocol + a reference task-driving loop.

``run_task`` is a REFERENCE implementation, not a mandate: an adapter may fully
self-manage its own conversation loop (e.g. a system with its own data-request
protocol) as long as ``finalize()`` returns a RunResult with a schema-conformant
trace. The simplification here is deliberate: every agent reply is fed verbatim to
the steward, whose deterministic topic routing decides whether it was a data request.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..core.models import RunResult, TaskInstance
from .steward import DataSteward

CLOSING_INSTRUCTION = "All data has been provided. Complete the remaining analysis and submit the final report."


@runtime_checkable
class SystemAdapter(Protocol):
    """Contract a contestant system must implement to be driven by run_task."""
    system_id: str

    def start(self, task: TaskInstance) -> str:
        """Deliver the initial prompt to the system; return its first reply."""
        ...

    def send(self, message: str) -> str:
        """Send one follow-up message (data batch / instruction); return the reply."""
        ...

    def finalize(self) -> RunResult:
        """Close the run and return the structured trace + final report text."""
        ...


def initial_prompt(task: TaskInstance) -> str:
    """First message for the system: context + goal + how to obtain data."""
    parts = [task.context.strip()]
    if task.prior_facts:
        parts.append(f"Facts already established: {task.prior_facts}")
    parts.append(f"Task goal: {task.goal.strip()}")
    parts.append(
        "Data access: batches are provided on demand, not all at once. Describe the "
        "data topic you need (or say “next batch”). Analyze each batch before requesting the next."
    )
    return "\n\n".join(parts)


def run_task(adapter: SystemAdapter, task: TaskInstance) -> RunResult:
    """Reference loop: adapter.start -> (steward route -> adapter.send)* -> finalize."""
    steward = DataSteward(task)
    reply = adapter.start(task)
    unavailable_streak = 0
    for _ in range(task.max_turns):
        resp = steward.request(reply)
        if resp.kind in ("data", "denied"):
            unavailable_streak = 0
            reply = adapter.send(resp.message)
        elif resp.kind == "exhausted":
            adapter.send(CLOSING_INSTRUCTION)
            break
        else:  # unavailable
            unavailable_streak += 1
            if unavailable_streak >= 2:
                break
            reply = adapter.send(resp.message)
    return adapter.finalize()
