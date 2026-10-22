"""GatingSteward — the policy-enforcing v2 environment.

Two novel behaviours v1's steward lacks (see design doc §3.2):

  prerequisite locks       a stage's data is WITHHELD until its `requires` predecessor is
                           completed AND its `unlock_when` guard holds over the agent's ACCEPTED
                           results — so declaring "unstable" keeps the capability route locked.
  conclusion-dependent     because `unlock_when` reads the agent's own reported conclusions, the
  forking                  environment forks: the same request yields different availability
                           depending on what the agent concluded upstream.

Plus fault injection (deny a stage's data for the honesty probe). The steward records a full
audit trajectory the scorer consumes. It never routes for the agent — it gates and serves; the
agent chooses where to go, and the trajectory records what actually happened.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from dmaic_bench.core.graph import evaluate


@dataclass
class StewardResponse:
    kind: str                      # "data" | "locked" | "denied" | "unknown"
    node: str
    data: Optional[dict] = None
    message: str = ""


def _deep_merge(dst: dict, src: dict) -> dict:
    for k, v in (src or {}).items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            _deep_merge(dst[k], v)
        else:
            dst[k] = v
    return dst


class GatingSteward:
    def __init__(self, task, fault: bool = False):
        self.task = task
        self.accepted: dict = {}                 # the agent's declared results (drives unlock_when)
        self.completed: set = set()              # nodes the agent has reported
        self.trajectory: list = []               # nodes whose data was actually released, in order
        self.audit: list = []                    # (kind, node) log
        self._fault_stages = {ft[0] for ft in (task.fault_targets or ())} if fault else set()
        self._fault_msg = {ft[0]: ft[2] for ft in (task.fault_targets or ())}

    # -- agent → steward -----------------------------------------------------
    def request(self, node: str) -> StewardResponse:
        """Ask for a node's data. Gated by fault → prerequisite → unlock_when."""
        if node in self._fault_stages:
            self.audit.append(("denied", node))
            return StewardResponse("denied", node,
                                   message=self._fault_msg.get(node, "Data for this stage are missing and cannot be provided"))
        gate = self._gate_for(node)
        if gate and not self._unlocked(gate):
            self.audit.append(("locked", node))
            return StewardResponse("locked", node, message=gate.get("rule", "Prerequisites are not satisfied"))
        block_key = self.task.node_data.get(node)
        data = self.task.blocks.get(block_key) if block_key else {}
        self.trajectory.append(node)
        self.audit.append(("data", node))
        return StewardResponse("data", node, data=data)

    def report(self, node: str, results: dict) -> None:
        """The agent declares the conclusions it computed at `node` (drives later unlock guards)."""
        _deep_merge(self.accepted, results or {})
        self.completed.add(node)

    # -- internals -----------------------------------------------------------
    def _gate_for(self, node: str):
        return next((g for g in self.task.gate_policy if g["stage"] == node), None)

    def _unlocked(self, gate) -> bool:
        req = gate.get("requires")
        if req:
            # `requires` may be a single stage or an any-of list (the predecessor that establishes
            # the precondition can itself be route-dependent, e.g. P-chart vs Laney chart).
            reqs = req if isinstance(req, (list, tuple)) else [req]
            if not any(r in self.completed for r in reqs):
                return False
        when = gate.get("unlock_when")
        return evaluate(when, self.accepted) if when else True

    def remaining_locked(self) -> list:
        return [g["stage"] for g in self.task.gate_policy
                if g["stage"] not in self.completed and not self._unlocked(g)]
