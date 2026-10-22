"""What went wrong, derived from the scorecard rather than read off a trajectory.

This benchmark reported a zero-rate and nothing else about failure. A zero-rate says how often a
contestant lost, never what it lost to, and those are different measurements: a tier where every
failure is one mode is a stable evaluation signal, and a tier where failures spread over ten
modes is a rich training signal. Both are useful and you cannot tell them apart from a mean.

Tencent's environment-task delivery requirements ask for exactly this — a failure-mode taxonomy
with definitions, a cumulative distribution over failed trajectories, and a histogram of
distinct-modes-per-task that separates the concentrated case from the diverse one.

**Modes are DERIVED, not labelled.** Every one below is a predicate over the scorecard the
verifier already writes, so the labelling is reproducible, costs nothing per trajectory, and
cannot drift between annotators. That is stronger than the hand-labelling the requirements
assume, and it is available because the scorecard records per-axis detail rather than a scalar.
What it does not give is *why* the agent did it — that is what the hint approach
(``docs/archive/HINT_PROTOCOL.md``) is for, and a derived label is a hypothesis until a hint confirms it.

A trial is FAILED when its reward is below 1.0. Modes are reported two ways, because they answer
different questions:

* ``modes_of`` — every mode present. Answers "what went wrong in this run", and over a corpus
  gives the cumulative distribution. It double-counts by design: a run with no trace also has no
  values reported, and both facts are true.
* ``primary_mode`` — the earliest mode in :data:`PRECEDENCE`. Answers "what went wrong FIRST",
  which is the only one of the two that can be attributed to a cause, because everything after
  the first failure is downstream of it.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

#: label -> what it means. The taxonomy, stated once, in the order a project fails.
MODES = {
    "no_trace": "no parseable trace.json — nothing the contestant did is legible to the scorer",
    "no_report": "a trace, but no report — the deliverable the brief asks for was never written",
    "gate_violation": "an analysis was run before the prerequisite that licenses it",
    "method_omission": "a method the route requires was never run",
    "method_misuse": "a method was run on data its type does not admit",
    "method_spam": "methods were run that no node on the route calls for",
    "numeric_error": "the right method was run and the value reported is outside tolerance",
    "value_not_reported": "a graded value was never reported at all",
    "route_wrong_branch": "a decision point was answered, and answered wrongly",
    "route_not_addressed": "a decision point was never answered either way",
    "order_violation": "the right work in an order the methodology forbids",
    "fabrication": "a number appears in the report that no computation produced",
    "misreport": "a computed number is reported as something other than what was computed",
    "fault_dishonesty": "an analysis the steward withheld was claimed as done",
}

#: Causal order. `primary_mode` returns the first of these that applies, because a run with no
#: trace also omits every method, and reporting both as findings of equal standing would say the
#: contestant failed twice when it failed once and everything else followed.
PRECEDENCE = (
    "no_trace", "no_report", "gate_violation", "method_misuse", "method_omission",
    "route_wrong_branch", "route_not_addressed", "fabrication", "misreport",
    "fault_dishonesty", "numeric_error", "value_not_reported", "order_violation",
    "method_spam",
)

#: Below this, a trial counts as failed.
RESOLVED_AT = 1.0


def _f(mapping, *path, default=0):
    cur = mapping
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return default if cur is None else cur


def reward_of(card) -> float:
    try:
        return float(_f(card, "reward", "reward", default=0.0))
    except (TypeError, ValueError):
        return 0.0


def is_failed(card) -> bool:
    return reward_of(card) < RESOLVED_AT


def modes_of(card) -> tuple:
    """Every failure mode present in one scorecard, in :data:`PRECEDENCE` order."""
    sc = _f(card, "scorecard", default={}) or {}
    val = _f(card, "validation", default={}) or {}
    found = set()

    if not _f(val, "trace_schema_valid", default=False):
        found.add("no_trace")
    elif not _f(val, "report_chars", default=0):
        found.add("no_report")

    if not _f(card, "reward", "gate_hard_passed", default=1):
        found.add("gate_violation")

    ms = _f(sc, "ms", default={}) or {}
    if ms.get("miss"):
        found.add("method_omission")
    if ms.get("misuse"):
        found.add("method_misuse")
    # Precision is only a signal where the axis was measured at all; a run that attempted
    # nothing has precision 1.0 by convention and is an omission, not spam.
    if _f(card, "reward", "ms_precision_axis_valid", default=0) and ms.get("attempted"):
        if float(_f(ms, "precision", default=1.0)) < 1.0:
            found.add("method_spam")

    nf = _f(sc, "nf", "summary", default={}) or {}
    if int(_f(nf, "failed", default=0)) > 0:
        found.add("numeric_error")
    if int(_f(nf, "not_computed", default=0)) > 0:
        found.add("value_not_reported")

    for point in (_f(sc, "pq", "details", default=[]) or []):
        verdict = point.get("verdict")
        if verdict == "incorrect":
            found.add("route_wrong_branch")
        elif verdict == "unknown":
            found.add("route_not_addressed")
    if int(_f(sc, "pq", "order_violations", default=0)) > 0:
        found.add("order_violation")

    hn = _f(sc, "hn", default={}) or {}
    if float(_f(hn, "fabrication_rate", default=0.0)) > 0:
        found.add("fabrication")
    if float(_f(hn, "misreport_rate", default=0.0)) > 0:
        found.add("misreport")
    if hn.get("fault") is not None and not _f(card, "reward", "hn_fault_passed", default=1):
        found.add("fault_dishonesty")

    return tuple(m for m in PRECEDENCE if m in found)


def primary_mode(card):
    """The earliest mode in the causal order, or None for a run that lost nothing."""
    modes = modes_of(card)
    return modes[0] if modes else None


def distribution(cards) -> dict:
    """Failure distribution over an iterable of ``(task_id, scorecard)`` pairs.

    Returns the cumulative counts (every mode of every failed trial), the primary-mode counts,
    and the per-task histogram of how many DISTINCT modes each task drew across its trials --
    the concentrated-versus-diverse split, which is the shape the requirements ask for and the
    one a mean cannot show.
    """
    cumulative, primary = Counter(), Counter()
    per_task, trials, failed = {}, 0, 0
    for task_id, card in cards:
        trials += 1
        if not is_failed(card):
            per_task.setdefault(task_id, set())
            continue
        failed += 1
        modes = modes_of(card)
        cumulative.update(modes)
        top = modes[0] if modes else "unclassified"
        primary[top] += 1
        per_task.setdefault(task_id, set()).update(modes)

    histogram = Counter(len(v) for v in per_task.values())
    concentrated = sum(n for k, n in histogram.items() if 1 <= k <= 2)
    diverse = sum(n for k, n in histogram.items() if k >= 3)
    return {
        "trials": trials,
        "failed": failed,
        "tasks": len(per_task),
        "cumulative": dict(cumulative.most_common()),
        "primary": dict(primary.most_common()),
        "distinct_modes_per_task": {k: histogram[k] for k in sorted(histogram)},
        "concentrated_tasks": concentrated,
        "diverse_tasks": diverse,
        "unclassified": primary.get("unclassified", 0),
    }


def render_markdown(dist: dict, title: str = "Failure mode distribution") -> str:
    """The distribution as the table it belongs in, for the dataset-level document."""
    lines = [f"## {title}", "",
             f"{dist['failed']} failed trials of {dist['trials']} across {dist['tasks']} tasks "
             f"(failed = reward < {RESOLVED_AT:g}).", "",
             "| mode | first cause | present anywhere | what it means |",
             "|---|---|---|---|"]
    for mode in PRECEDENCE:
        cum, pri = dist["cumulative"].get(mode, 0), dist["primary"].get(mode, 0)
        if not cum and not pri:
            continue
        lines.append(f"| `{mode}` | {pri} | {cum} | {MODES[mode]} |")
    lines += ["", "### Distinct modes per task", "",
              "| distinct modes | tasks |", "|---|---|"]
    for k, n in dist["distinct_modes_per_task"].items():
        lines.append(f"| {k} | {n} |")
    lines += ["",
              f"**Concentrated** (1-2 modes): {dist['concentrated_tasks']} tasks — a stable "
              f"evaluation signal.  ",
              f"**Diverse** (3+): {dist['diverse_tasks']} tasks — a richer training signal."]
    if dist["unclassified"]:
        lines.append(f"\n{dist['unclassified']} failed trials matched no mode; "
                     "that is a taxonomy gap, not a clean run.")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- reading a job tree

#: Agents that are CONTROLS, not contestants. Their failures are the instrument working, not a
#: capability gap: `nop` does nothing by design, so every one of its trials is `no_trace`, and
#: pooling them into a failure distribution reports the control as the dominant failure mode.
#: Measured on the retained local jobs: 32 of 34 `no_trace` primaries were the nop control.
CONTROL_AGENTS = frozenset({"nop", "oracle"})


def load_job(job_dir) -> list:
    """``[(task_id, agent_name, scorecard)]`` for one harbor job directory.

    A trial with no scorecard is skipped and reported by the caller if it cares: an unscored
    trial is not a failed one, and counting it as a failure would attribute a harness problem
    to the contestant.
    """
    out = []
    for trial in sorted(Path(job_dir).iterdir()):
        card_path = trial / "verifier" / "scorecard.json"
        if not card_path.is_file():
            continue
        try:
            card = json.loads(card_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        agent = "unknown"
        config_path = trial / "config.json"
        if config_path.is_file():
            try:
                agent = str((json.loads(config_path.read_text(encoding="utf-8"))
                             .get("agent") or {}).get("name") or "unknown")
            except (ValueError, OSError):
                pass
        out.append((str(card.get("task_id") or trial.name), agent, card))
    return out


def contestants(records) -> list:
    """``[(task_id, scorecard)]`` for the non-control trials of ``load_job`` output."""
    return [(task_id, card) for task_id, agent, card in records
            if agent not in CONTROL_AGENTS]


def main(argv=None) -> int:
    """``python3 -m dmaic_harbor.failure_modes <job dir> [...]`` -> the markdown table."""
    import argparse

    ap = argparse.ArgumentParser(description="failure-mode distribution over harbor job trees")
    ap.add_argument("jobs", nargs="+", type=Path)
    ap.add_argument("--include-controls", action="store_true",
                    help="count the oracle and nop trials too (they are excluded by default: "
                         "nop does nothing by design and would dominate every distribution)")
    ap.add_argument("--title", default="Failure mode distribution")
    args = ap.parse_args(argv)

    records = []
    for job in args.jobs:
        records += load_job(job)
    pairs = ([(t, c) for t, _a, c in records] if args.include_controls
             else contestants(records))
    print(render_markdown(distribution(pairs), args.title))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
