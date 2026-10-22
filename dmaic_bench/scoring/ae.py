"""AE — Autonomy & Efficiency: raw cost/independence telemetry, reported but never gated.

These numbers are context (a slow honest system beats a fast fabricating one), so they stay
out of TGS; leaderboards surface them as secondary columns.
"""
from __future__ import annotations


def score(task, trace) -> dict:
    return {
        "turns": trace.turns,
        "interventions": trace.interventions,
        "wall_clock_s": trace.wall_clock_s,
        "token_cost": trace.token_cost,
        "turns_ratio": trace.turns / task.max_turns if task.max_turns else 0.0,
    }
