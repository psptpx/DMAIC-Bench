"""Aggregate a campaign's job directories into a model x metric table.

TWO DEFECTS THIS MODULE EXISTS TO NOT HAVE
------------------------------------------

**1. A verifier crash is not a score of zero.**

``verify.py`` deliberately never lets a crash go unrecorded: it writes ``reward.json``
with every axis at zero and marks the companion ``scorecard.json`` with an ``error``
key. That is the right thing for the verifier to do -- an unscored trial is worse than a
zero *for the trial*. It is the wrong thing for an aggregate to average, because at that
layer the two are indistinguishable by ``reward.json`` alone, and reading only
``reward.json`` is what the previous aggregation did.

The consequence is directional, not random. Infrastructure failures are not uniformly
distributed across contestants: the slow, verbose or long-horizon ones hit timeouts and
resource ceilings more often, so averaging their crashes in as zeros biases exactly the
systems that were most expensive to run. This module reads ``scorecard.json``, EXCLUDES
any trial whose verdict came from the crash path, counts it, and reports the count beside
the mean. A trial that did not produce a verdict is a missing observation.

This has not yet fired in roughly 692 trials. That is luck. The fallback exists precisely
because crashes happen, and the first one to land would have been published as a model
result.

**2. Cost is not USD when USD is unknown.**

``cost_usd`` was null for 9 of 11 contestants in the last campaign, because the pricing
library has no price map for gateway-served model names. Token counts, however, are
recorded harness-side for every one of them. So tokens are the primary cost figure here
and USD is reported only where a price was actually returned -- labelled a **floor**,
because a partially-priced set of trials understates the total by exactly the trials it
could not price. No price is ever inferred, interpolated, or carried across models.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import pathlib
import random
import statistics
import sys

try:  # pragma: no cover
    from . import spec
    from .supervisor import classify_trial
except ImportError:  # pragma: no cover - direct-script execution
    import spec  # type: ignore[no-redef]
    from supervisor import classify_trial  # type: ignore[no-redef]


#: Metrics to aggregate: every scalar the reward contract defines, so a new axis appears
#: here the moment it is added to the contract instead of when someone remembers to
#: retype it into a list.
METRICS = tuple(spec.REWARD_KEYS)

#: Columns in the rendered table. A subset, for width; the JSON carries all of METRICS.
TABLE_COLUMNS = ("reward", "competence", "ms_recall", "nf", "pq",
                 "hn_fabrication_rate", "ae_turns")

#: Harness-error kinds. Counted, reported, and never averaged into a mean.
ERROR_KINDS = ("no_reward", "verifier_error", "trial_exception")

BOOTSTRAP_N = 10_000
BOOTSTRAP_SEED = 20260904

TOKEN_FIELDS = ("n_input_tokens", "n_cache_tokens", "n_output_tokens")
TIMING_FIELDS = ("wall_s", "agent_s", "envbuild_s", "verifier_s")


# --------------------------------------------------------------------------- statistics

def bootstrap_ci(xs: list, n: int = BOOTSTRAP_N, alpha: float = 0.05,
                 seed: int = BOOTSTRAP_SEED) -> tuple:
    """Percentile bootstrap over TRIALS, so the interval carries between-task spread as
    well as run-to-run noise -- which is what k attempts over many tasks are for."""
    xs = [x for x in xs if isinstance(x, (int, float))]
    if len(xs) < 2:
        return (None, None)
    rnd = random.Random(seed)
    k = len(xs)
    means = sorted(statistics.fmean(rnd.choices(xs, k=k)) for _ in range(n))
    lo = means[int((alpha / 2) * n)]
    hi = means[min(n - 1, int((1 - alpha / 2) * n))]
    return (lo, hi)


def _span_seconds(d: dict) -> float | None:
    try:
        a = _dt.datetime.fromisoformat(str(d["started_at"]).replace("Z", "+00:00"))
        b = _dt.datetime.fromisoformat(str(d["finished_at"]).replace("Z", "+00:00"))
        return (b - a).total_seconds()
    except (KeyError, TypeError, ValueError):
        return None


def _load(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


# --------------------------------------------------------------------------- collection

def _is_trial_dir(path: pathlib.Path) -> bool:
    return (path / "config.json").is_file() and (path / "trial.log").exists()


def _model_of(trial: pathlib.Path, config: dict) -> str | None:
    """Which contestant produced this trial.

    Controls (an oracle or a no-op arm) carry no model name in the trial config, but the
    result does. They are recovered and labelled rather than dropped: the control row is
    the one that says whether the pipeline itself is sound, and an aggregate that silently
    omits it has thrown away its own sanity check.
    """
    agent = config.get("agent") or {}
    if not agent:
        result = _load(trial / "result.json") or {}
        agent = result.get("agent_info") or {}
    model = agent.get("model_name")
    if model:
        return str(model)
    info = agent.get("model_info") or {}
    if info.get("name"):
        return str(info["name"])
    name = agent.get("name")
    if name in ("oracle", "nop"):
        return f"<control:{name}>"
    return None


def collect(jobs_dir: str | pathlib.Path) -> list:
    """One row per trial, each already classified as scored or as a kind of harness error."""
    rows = []
    root = pathlib.Path(jobs_dir)
    for cfg in sorted(root.rglob("config.json")):
        trial = cfg.parent
        if not _is_trial_dir(trial):
            continue
        config = _load(cfg)
        if config is None:
            continue
        model = _model_of(trial, config)
        if model is None:
            continue

        row = {
            "trial": trial.name,
            "job": trial.parent.name,
            "model": model,
            "task": str((config.get("task") or {}).get("path", "")).rsplit("/", 1)[-1],
            "path": str(trial),
            "kind": classify_trial(trial),
        }
        row["scored"] = row["kind"] == "scored"

        reward = _load(trial / "verifier" / "reward.json")
        row["reward_json"] = reward if isinstance(reward, dict) else None

        card = _load(trial / "verifier" / "scorecard.json")
        if isinstance(card, dict) and card.get("error"):
            # Kept verbatim so the report can say WHAT crashed, not merely that something
            # did. A recurring exception type across contestants is a harness bug.
            row["verifier_error"] = str(card["error"])[:300]

        result = _load(trial / "result.json")
        if isinstance(result, dict):
            for key, name in (("agent_execution", "agent_s"),
                              ("environment_setup", "envbuild_s"),
                              ("verifier", "verifier_s")):
                if isinstance(result.get(key), dict):
                    v = _span_seconds(result[key])
                    if v is not None:
                        row[name] = v
            if result.get("started_at"):
                row["wall_s"] = _span_seconds(result)
            agent_result = result.get("agent_result") or {}
            for k in TOKEN_FIELDS + ("cost_usd",):
                if isinstance(agent_result.get(k), (int, float)):
                    row[k] = agent_result[k]
            meta = agent_result.get("metadata") or {}
            if isinstance(meta.get("n_episodes"), int):
                row["n_episodes"] = meta["n_episodes"]
            exc = result.get("exception_info") or {}
            if isinstance(exc, dict) and exc.get("exception_type"):
                row["exception"] = str(exc["exception_type"])
        rows.append(row)
    return rows


# --------------------------------------------------------------------------- cost

def summarize_cost(rows: list) -> dict:
    """Tokens as the primary cost figure; USD only where a price was actually returned.

    ``priced_fraction`` is the honest part. When it is below 1.0 the USD total is a floor
    over the priced subset and is labelled as such, because the alternative -- scaling it
    up by the unpriced fraction -- is inventing a price for a model whose price we do not
    have.
    """
    out: dict = {"tokens": {}, "usd": None}
    for field in TOKEN_FIELDS:
        xs = [r[field] for r in rows if isinstance(r.get(field), (int, float))]
        if xs:
            out["tokens"][field] = {"sum": sum(xs), "mean": statistics.fmean(xs), "n": len(xs)}
    billed = [r for r in rows
              if isinstance(r.get("n_input_tokens"), (int, float))
              or isinstance(r.get("n_output_tokens"), (int, float))]
    priced = [r["cost_usd"] for r in rows if isinstance(r.get("cost_usd"), (int, float))]
    if priced:
        fraction = len(priced) / len(billed) if billed else 0.0
        out["usd"] = {
            "sum_priced": sum(priced),
            "mean_priced": statistics.fmean(priced),
            "n_priced": len(priced),
            "n_trials_with_tokens": len(billed),
            "priced_fraction": round(fraction, 4),
            "is_floor": fraction < 1.0,
            "note": ("FLOOR: only %d of %d token-bearing trials could be priced; the true "
                     "total is higher by the unpriced remainder, which is not estimated "
                     "here because no price for those model names is known."
                     % (len(priced), len(billed))) if fraction < 1.0 else
                    "complete: every token-bearing trial was priced",
        }
    else:
        out["usd"] = {
            "n_priced": 0,
            "n_trials_with_tokens": len(billed),
            "priced_fraction": 0.0,
            "is_floor": True,
            "note": ("UNPRICED: no price map covers these model names. Compare token "
                     "counts, which the harness records regardless. No USD figure is "
                     "reported because inventing one would be worse than reporting none."),
        }
    return out


# --------------------------------------------------------------------------- summary

def summarize(rows: list) -> dict:
    by: dict = {}
    for r in rows:
        by.setdefault(r["model"], []).append(r)

    out: dict = {}
    for model, rs in sorted(by.items()):
        scored = [r for r in rs if r["scored"]]
        excluded = [r for r in rs if not r["scored"]]
        kinds: dict = {}
        for r in excluded:
            kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1

        entry = {
            "n_trials": len(rs),
            "n_scored": len(scored),
            "n_excluded": len(excluded),
            "excluded_rate": round(len(excluded) / len(rs), 4) if rs else 0.0,
            "excluded_kinds": {k: kinds.get(k, 0) for k in ERROR_KINDS if kinds.get(k)},
            "verifier_errors": sorted({r["verifier_error"] for r in excluded
                                       if r.get("verifier_error")})[:10],
            "exceptions": sorted({r["exception"] for r in excluded if r.get("exception")}),
            "n_tasks": len({r["task"] for r in rs}),
            "metrics": {},
            # Cost is computed over ALL trials, not only scored ones: a trial that crashed
            # in the verifier still burned the tokens the agent spent getting there, and a
            # budget report that hides them understates what the campaign cost.
            "cost": summarize_cost(rs),
        }
        for k in METRICS:
            xs = [r["reward_json"].get(k) for r in scored
                  if r.get("reward_json") and isinstance(r["reward_json"].get(k), (int, float))]
            if xs:
                lo, hi = bootstrap_ci(xs)
                entry["metrics"][k] = {
                    "mean": statistics.fmean(xs), "n": len(xs),
                    "ci95_lo": lo, "ci95_hi": hi,
                    "sd": statistics.stdev(xs) if len(xs) > 1 else 0.0,
                }
        for k in TIMING_FIELDS + ("n_episodes",):
            xs = [r[k] for r in rs if isinstance(r.get(k), (int, float))]
            if xs:
                entry.setdefault("timing", {})[k] = {
                    "mean": statistics.fmean(xs), "sum": sum(xs), "n": len(xs)}
        out[model] = entry
    return out


# --------------------------------------------------------------------------- rendering

def _fmt_tokens(n: float) -> str:
    if n >= 1e9:
        return f"{n / 1e9:.2f}B"
    if n >= 1e6:
        return f"{n / 1e6:.1f}M"
    if n >= 1e3:
        return f"{n / 1e3:.0f}k"
    return f"{n:.0f}"


def to_md(summary: dict) -> str:
    cols = [c for c in TABLE_COLUMNS]
    head = ("| model | scored | excluded | " + " | ".join(cols)
            + " | in tok | out tok | USD |")
    sep = "|---" * (len(cols) + 6) + "|"
    lines = [head, sep]
    for model, m in summary.items():
        cells = []
        for c in cols:
            d = m["metrics"].get(c)
            if not d:
                cells.append("--")
            elif d["ci95_lo"] is None:
                cells.append(f"{d['mean']:.3f}")
            else:
                cells.append(f"{d['mean']:.3f} [{d['ci95_lo']:.3f}, {d['ci95_hi']:.3f}]")
        tok = m["cost"]["tokens"]
        tin = _fmt_tokens(tok["n_input_tokens"]["sum"]) if "n_input_tokens" in tok else "--"
        tout = _fmt_tokens(tok["n_output_tokens"]["sum"]) if "n_output_tokens" in tok else "--"
        usd = m["cost"]["usd"]
        if usd and usd.get("n_priced"):
            money = f"${usd['sum_priced']:.2f}"
            if usd.get("is_floor"):
                money += " (floor)"
        else:
            money = "unpriced"
        excl = str(m["n_excluded"])
        if m["n_excluded"]:
            excl += " (" + ", ".join(f"{k}:{v}" for k, v in m["excluded_kinds"].items()) + ")"
        lines.append(f"| {model} | {m['n_scored']} | {excl} | " + " | ".join(cells)
                     + f" | {tin} | {tout} | {money} |")

    lines += [
        "",
        "**excluded** = trials that produced no verdict: no `reward.json`, a `scorecard.json`",
        "carrying the verifier's crash marker, or a trial-level exception. They are counted,",
        "never averaged. A trial that did not produce a verdict is a missing observation, not",
        "a zero, and averaging it in would bias exactly the contestants that hit infrastructure",
        "problems most often.",
        "",
        "**cost** is reported in tokens. USD appears only where a price for that model name was",
        "actually returned by the harness; where it is partial it is marked `(floor)` and where",
        "no price is known the cell reads `unpriced`. No price is inferred.",
    ]
    return "\n".join(lines)


def campaign_totals(rows: list) -> dict:
    total = len(rows)
    excluded = [r for r in rows if not r["scored"]]
    kinds: dict = {}
    for r in excluded:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    return {"n_trials": total, "n_scored": total - len(excluded),
            "n_excluded": len(excluded),
            "excluded_rate": round(len(excluded) / total, 4) if total else 0.0,
            "excluded_kinds": kinds, "cost": summarize_cost(rows)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="dmaic-harbor-aggregate",
        description="Model x metric table with bootstrap CIs. Trials that produced no "
                    "verdict are excluded from every mean and reported separately.")
    ap.add_argument("jobs_dir")
    ap.add_argument("--out", help="write the full JSON (summary + per-trial rows) here")
    ap.add_argument("--md", help="write the Markdown table here")
    a = ap.parse_args(argv)

    rows = collect(a.jobs_dir)
    if not rows:
        print(f"no trials found under {a.jobs_dir}", file=sys.stderr)
        return 2
    summary = summarize(rows)
    totals = campaign_totals(rows)

    if a.out:
        pathlib.Path(a.out).write_text(
            json.dumps({"campaign": totals, "summary": summary, "trials": rows},
                       indent=2, ensure_ascii=False), encoding="utf-8")
    md = to_md(summary)
    if a.md:
        pathlib.Path(a.md).write_text(md + "\n", encoding="utf-8")
    print(md)
    print()
    print(f"campaign: {totals['n_scored']}/{totals['n_trials']} trials scored; "
          f"{totals['n_excluded']} excluded ({totals['excluded_rate']:.1%}) "
          f"{totals['excluded_kinds'] or ''}")
    usd = totals["cost"]["usd"]
    print(f"cost: {totals['cost']['tokens'].get('n_input_tokens', {}).get('sum', 0):,} in / "
          f"{totals['cost']['tokens'].get('n_output_tokens', {}).get('sum', 0):,} out tokens; "
          f"USD {usd.get('note')}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
