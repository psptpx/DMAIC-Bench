"""DMAIC-Bench scoring package — system-agnostic, trace/report-in, scorecard-out.

Axes: MS (method selection), NF (numeric fidelity), HN (honesty/grounding), PQ (process
quality), AE (autonomy/efficiency), TGS (trust-gated headline), RB (clean/dirty robustness).
"""
from . import ae, hn, ms, nf, pq, rb, tgs  # noqa: F401
from .rb import pair_key, robustness_delta  # noqa: F401
from .scorer import AGGREGATE_METRICS, SCHEMA, aggregate, paired_bootstrap, score_run  # noqa: F401
from .tgs import harmonic  # noqa: F401

__all__ = [
    "ae", "hn", "ms", "nf", "pq", "rb", "tgs",
    "score_run", "aggregate", "paired_bootstrap",
    "harmonic", "pair_key", "robustness_delta",
    "AGGREGATE_METRICS", "SCHEMA",
]
