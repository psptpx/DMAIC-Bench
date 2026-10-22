"""DMAIC-Bench v3 — fair evaluation of heterogeneous DMAIC agents.

v3 adds, on top of v2's graph task-model: (1) method-selection-under-ambiguity (no fed methods;
the agent picks from the full vocabulary), (2) two-channel scoring (outcome × method-validity),
(3) a system-agnostic adapter + fact-scoped provisioning simulator so a one-shot LLM agent, a
tool-agent, and an operator-supplied HITL decision-graph engine compete fairly, and (4) an
autonomy-axis
Pareto leaderboard. See docs/archive/dmaic-bench-v3-fair-heterogeneous-design.md.
"""
