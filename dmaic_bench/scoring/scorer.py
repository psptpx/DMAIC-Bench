"""Scorer orchestration: one run -> one scorecard; many scorecards -> leaderboard statistics.

Aggregation is bootstrap-based (pure random.Random, seeded, no numpy dependency) so every CI
and p-value is reproducible byte-for-byte across machines. System comparisons use a PAIRED
sign-flip bootstrap over per-task score differences — tasks vary wildly in difficulty, and
pairing removes that variance instead of drowning the signal in it.
"""
from __future__ import annotations

import random

from . import ae, hn, ms, nf, pq, tgs

SCHEMA = "dmaic-scorecard/v1"

# Metric paths surfaced in aggregate leaderboards (dot-paths into a scorecard).
AGGREGATE_METRICS = (
    "tgs",
    "ms.recall",
    "ms.precision",
    "ms.misuse_rate",
    "nf.summary.ratio",
    "pq.score",
    "hn.fabrication_rate",
    "hn.misreport_rate",
    "ae.turns_ratio",
)


def score_run(task, trace, report: str, taxonomy, y_type: str = "continuous") -> dict:
    nf_details = nf.check_values(task, trace)
    nf_summary = nf.summarize(nf_details)
    ms_score = ms.score(task, trace, taxonomy, y_type=y_type)
    hn_score = hn.score(task, trace, report)
    pq_score = pq.score(task, trace, taxonomy)
    return {
        "schema": SCHEMA,
        "system_id": trace.system_id,
        "task_id": task.task_id,
        "case_id": task.case_id,
        "tier": task.tier,
        "variant": task.variant,
        "seed": task.seed,
        "ms": ms_score,
        "nf": {"summary": nf_summary, "details": nf_details},
        "hn": hn_score,
        "pq": pq_score,
        "ae": ae.score(task, trace),
        "tgs": tgs.compute(ms_score, nf_summary, pq_score, hn_score),
    }


def _get(card: dict, path: str):
    cur = card
    for part in path.split("."):
        cur = cur[part]
    return cur


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _percentile(sorted_xs, q):
    # Nearest-rank on the sorted bootstrap means — simple and deterministic.
    if not sorted_xs:
        return 0.0
    i = min(len(sorted_xs) - 1, max(0, int(round(q * (len(sorted_xs) - 1)))))
    return sorted_xs[i]


def _bootstrap_ci(values, rng, n=1000, alpha=0.05):
    if not values:
        return (0.0, 0.0)
    means = sorted(
        _mean([values[rng.randrange(len(values))] for _ in range(len(values))])
        for _ in range(n)
    )
    return (_percentile(means, alpha / 2), _percentile(means, 1 - alpha / 2))


def aggregate(cards: list, seed: int = 20260707) -> dict:
    """Per-system mean + 95% bootstrap CI (1000 resamples) for each leaderboard metric."""
    by_system = {}
    for c in cards:
        by_system.setdefault(c["system_id"], []).append(c)
    out = {}
    for system_id in sorted(by_system):
        group = by_system[system_id]
        metrics = {}
        for path in AGGREGATE_METRICS:
            values = []
            for c in group:
                try:
                    v = _get(c, path)
                except (KeyError, TypeError):
                    continue
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    values.append(float(v))
            # Fresh seeded rng per (system, metric): insertion order can't shift results.
            rng = random.Random((seed, system_id, path).__str__())
            lo, hi = _bootstrap_ci(values, rng)
            metrics[path] = {"mean": _mean(values), "ci_low": lo, "ci_high": hi,
                             "n": len(values)}
        out[system_id] = {"n_runs": len(group), "metrics": metrics}
    return out


def paired_bootstrap(cards_a: list, cards_b: list, metric_path: str = "tgs",
                     n: int = 2000, seed: int = 20260707) -> dict:
    """Paired A-vs-B comparison on tasks both systems ran.

    p_value is the two-sided sign-flip test on per-task differences (+1 smoothing so it is
    never exactly 0); CI is the percentile bootstrap of the mean difference.
    """
    a_by = {c["task_id"]: c for c in cards_a}
    b_by = {c["task_id"]: c for c in cards_b}
    common = sorted(a_by.keys() & b_by.keys())
    diffs = [float(_get(a_by[t], metric_path)) - float(_get(b_by[t], metric_path))
             for t in common]
    if not diffs:
        return {"pairs": 0, "mean_diff": 0.0, "ci_low": 0.0, "ci_high": 0.0, "p_value": 1.0}

    mean_diff = _mean(diffs)
    rng = random.Random((seed, metric_path).__str__())
    ci_low, ci_high = _bootstrap_ci(diffs, rng, n=n)
    # Sign-flip null: under H0 each task's difference is symmetric around 0.
    extreme = sum(
        abs(_mean([d if rng.random() < 0.5 else -d for d in diffs])) >= abs(mean_diff)
        for _ in range(n)
    )
    return {
        "pairs": len(diffs),
        "mean_diff": mean_diff,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "p_value": (extreme + 1) / (n + 1),
    }
