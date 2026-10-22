"""The v3 fair environment: one interface every contestant touches, plus a fact-scoped,
method-blind provisioning simulator behind an INFORMATION FIREWALL.

Any agent that needs turn-paced provisioning (notably an operator-supplied HITL decision-graph
engine, which pauses at decision nodes) calls `env.provision(text)`; a one-shot autonomous agent just calls
`env.request(node)` a few times and never provisions. Both run behind the identical `Env`, so the
Deliverable is scored uniformly and such an engine is no longer penalized by an autonomous-only
protocol
(design doc §4; τ²-bench dual-control).

FIREWALL (the critical fairness property): the simulator can see only what a real process engineer
POSSESSES — raw data tables + non-answer process facts + a persona. It is NEVER given, and STRUCTURALLY
CANNOT return, a method choice, a target value, or a conclusion. Those live only in the grader's
disjoint store (the oracle). A provisioning request for the *answer* is refused. This is τ-bench's
"constrained to observable state" hardened into a two-store firewall.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


# Requests that ask for the ANSWER rather than data/facts — always refused by the firewall.
_ANSWER_REQUEST = re.compile(
    r"(which method|what method|which one|correct answer|is it significant|"
    r"should I|target|correct value|the answer|conclusion)",
    re.IGNORECASE)


@dataclass
class ProvisioningSimulator:
    """Scripted (deterministic → no LLM leak) process-engineer persona. Holds ONLY the data store and
    non-answer facts; never the oracle."""
    task: object
    facts: dict = field(default_factory=dict)         # spec limits, "special causes removed", etc.
    persona: str = "Process engineer: I hold shop-floor data and process facts, but will not choose methods or provide conclusions for you."

    def respond(self, text: str) -> dict:
        t = (text or "").strip()
        if _ANSWER_REQUEST.search(t):
            return {"kind": "refused",
                    "message": "As the process engineer, I can provide data and process facts only; choose methods and draw conclusions yourself."}
        # keyword-route to a staged data block. Topics are SHORT distinctive tokens (the first label
        # segment, node key), so "Please provide baseline data" matches the "baseline per-stick weight" node — we check whether
        # a node topic appears in the request, not whether the whole label does.
        low = t.lower()
        for node, key in getattr(self.task, "node_data", {}).items():
            block = self.task.blocks.get(key) if key else {}
            n = self.task.graph.node(node) if hasattr(self.task, "graph") else None
            node_label = (n.label if n is not None else "") or ""
            block_label = block.get("label", "") if isinstance(block, dict) else ""
            topics = [node.lower(), (key or "").lower()]
            for lbl in (node_label, block_label):
                seg = re.split(r"[· ((\s/]", lbl)[0].strip().lower()
                if seg:
                    topics.append(seg)
            if any(tok and len(tok) >= 2 and tok in low for tok in topics):
                return {"kind": "data", "node": node, "data": block}
        # fall through to non-answer facts
        for fk, fv in self.facts.items():
            if fk.lower() in low:
                return {"kind": "fact", "key": fk, "value": fv}
        return {"kind": "unavailable",
                "message": "No matching data or fact found. Specify the stage data you need (e.g. baseline, gauge, variance analysis, or trial)."}


@dataclass
class Env:
    """The single interface every contestant uses. `request` pulls a stage's data directly (metered
    as a data pull); `provision` goes through the firewall simulator (metered as an autonomy turn)."""
    task: object
    simulator: ProvisioningSimulator
    max_provision_turns: int = 40
    _data_pulls: int = 0
    _provision_turns: int = 0
    log: list = field(default_factory=list)

    def request(self, node: str) -> dict:
        self._data_pulls += 1
        key = getattr(self.task, "node_data", {}).get(node)
        data = self.task.blocks.get(key) if key else {}
        self.log.append(("request", node))
        return {"kind": "data", "node": node, "data": data}

    def provision(self, text: str) -> dict:
        if self._provision_turns >= self.max_provision_turns:
            return {"kind": "budget_exhausted", "message": "provisioning turn budget exhausted"}
        self._provision_turns += 1
        r = self.simulator.respond(text)
        self.log.append(("provision", r["kind"]))
        return r

    @property
    def autonomy_cost(self) -> int:
        return self._provision_turns

    @property
    def data_pulls(self) -> int:
        return self._data_pulls


def make_env(task, facts: dict | None = None, max_provision_turns: int = 40) -> Env:
    return Env(task=task, simulator=ProvisioningSimulator(task=task, facts=facts or {}),
               max_provision_turns=max_provision_turns)
