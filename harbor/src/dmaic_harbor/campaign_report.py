"""One command from a finished job tree to the numbers a conclusion can be written from.

Reads a harbor job directory and prints: the controls (so the scale is bounded before anything
else is read), the per-tier result, the axis breakdown, and the failure-mode distribution. Every
piece already existed — `analysis.tier_of_route`, `failure_modes.distribution`, the scorecards —
and nothing put them in one place, so reading a campaign meant three ad-hoc scripts and a memory
of which trials were controls.

    python3 -m dmaic_harbor.campaign_report harbor/jobs/<job> [--json]
"""
from __future__ import annotations

import argparse
import json
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from . import failure_modes as FM


#: A trial counts as RESOLVED at or above this reward.
#:
#: The benchmark's reward is continuous, and no threshold had ever been declared — so pass@k, the
#: pre-registered k=3 analysis and every comparison with a pass/fail benchmark were uncomputable.
#: 1.0 is chosen rather than a softer bar because it is the only value that needs no defending:
#: it is exactly the oracle's score, so "resolved" means "did everything the reference solution
#: did, to tolerance". Any lower number is a judgement about how much of a DMAIC project may be
#: wrong and still count, and this corpus has no basis for making that judgement yet. Reported
#: alongside the mean, never instead of it: at 1.0 the measure is severe (2 of 95 here) and a
#: severe measure has poor resolution near the floor.
RESOLVED_AT = 1.0


def _cluster_bootstrap(by_case: dict, iters: int = 10000, seed: int = 20260910) -> dict:
    """A case-clustered bootstrap CI for the mean.

    Seeds of one case are NOT independent observations: they share the decision graph, the brief,
    the domain and the generator. Measured on this corpus, the intraclass correlation is 0.206
    over 15 cases averaging 6.3 seeds, which is a design effect of 2.10 — a nominal n of 95
    carries about as much information as 45 independent tasks, and an interval computed as though
    the 95 were independent is roughly 1.45x too narrow.

    So the bootstrap resamples CASES with replacement, not trials, which is the standard
    correction and the one this corpus's own plan called for.
    """
    rng = random.Random(seed)
    cases = list(by_case)
    if len(cases) < 2:
        return {}
    means = []
    for _ in range(iters):
        drawn = [x for c in (rng.choice(cases) for _ in cases) for x in by_case[c]]
        if drawn:
            means.append(statistics.fmean(drawn))
    means.sort()
    lo = means[int(0.025 * len(means))]
    hi = means[int(0.975 * len(means)) - 1]
    grand = statistics.fmean([x for v in by_case.values() for x in v])
    between = statistics.pvariance([statistics.fmean(v) for v in by_case.values()])
    within = statistics.fmean([statistics.pvariance(v) if len(v) > 1 else 0.0
                               for v in by_case.values()])
    icc = between / (between + within) if (between + within) else 0.0
    k = statistics.fmean([len(v) for v in by_case.values()])
    deff = 1 + (k - 1) * icc
    n = sum(len(v) for v in by_case.values())
    return {"mean": round(grand, 4), "ci95": [round(lo, 4), round(hi, 4)],
            "icc": round(icc, 3), "design_effect": round(deff, 2),
            "n_trials": n, "n_cases": len(cases), "effective_n": round(n / deff, 1)}


def _rows(job_dir: Path, rescored: bool = True) -> list:
    """*rescored* prefers `verifier-rescored/` where `scripts/rescore.py` has written one.

    A scorer fix makes numbers measured before it incomparable with numbers measured after, so
    a campaign that spans one has to be read through a single scorer. The re-score never
    overwrites `verifier/` — that is the record of what was reported at the time — so choosing
    between them is a read-side decision, and the default is the current scorer.
    """
    out = []
    for trial in sorted(job_dir.iterdir()):
        card_path = trial / "verifier" / "scorecard.json"
        if rescored and (trial / "verifier-rescored" / "scorecard.json").is_file():
            card_path = trial / "verifier-rescored" / "scorecard.json"
        cfg_path = trial / "config.json"
        if not card_path.is_file() or not cfg_path.is_file():
            continue
        try:
            card = json.loads(card_path.read_text(encoding="utf-8"))
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        agent = str((cfg.get("agent") or {}).get("name") or "unknown")
        model = str((cfg.get("agent") or {}).get("model_name") or "")
        seed = card.get("seed")
        out.append({"trial": trial.name, "agent": agent, "model": model, "card": card,
                    "task_id": str(card.get("task_id") or trial.name),
                    "case_id": str(card.get("case_id") or ""),
                    "seed": int(seed) if isinstance(seed, (int, float)) else None,
                    "shape": str((card.get("scorecard") or {}).get("shape")
                                 or card.get("shape") or ""),
                    "reward": FM.reward_of(card)})
    return out


def _shape_lookup() -> dict:
    """``(case_id, seed) -> shape``, from the registry.

    The scorecard carries case_id, seed and tier but NOT the shape, and `tier` there is the
    harbor task tier (T3), not the routing tier this analysis means. So the routing shape is
    looked up rather than read out of the artifact — deterministic given (case, seed), and the
    registry is its source of truth. Publishing it into task.toml would make a job tree
    self-describing and is worth doing; it is not done here because it would mean rebuilding a
    corpus mid-campaign.
    """
    try:
        from dmaic_bench.v2 import registry
    except ImportError:
        return {}
    return {(cid, seed): case.shapes.get(seed)
            for cid, case in registry.discover().items() for seed in case.seeds}


def _tier(row, shapes) -> str:
    from .analysis import tier_of
    shape = row["shape"] or shapes.get((row["case_id"], row["seed"]))
    return tier_of(shape) if shape else "unknown"


def floored(rows, controls_rows, shapes) -> list:
    """Tasks every contestant scored 0 on, with what is known about WHY.

    A task nobody solves is ambiguous, and this benchmark has already published nine such tasks
    as difficulty when they were unscoreable. Three things separate the cases, and all three are
    available without running anything else:

    * did the ORACLE score 1.000 on it? If not, the ceiling is broken and the zero says nothing
      about the contestant;
    * what failure mode did the contestants hit? A shared mode is a capability claim; a spread
      of unrelated modes is a task that fails for many reasons, which is usually a defect;
    * is there a HINT PROBE for it? Then the ambiguity is resolvable by experiment rather than
      argument (docs/archive/HINT_PROTOCOL.md).

    None of that PROVES a task is hard. It says which question is still open.
    """
    from .analysis import tier_of
    try:
        from dmaic_bench.v2 import hints as hints_mod
    except ImportError:                              # pragma: no cover
        hints_mod = None

    by_task = defaultdict(list)
    for row in rows:
        by_task[row["task_id"]].append(row)
    oracle = {r["task_id"]: r["reward"] for r in controls_rows if r["agent"] == "oracle"}

    out = []
    for task_id, trials in sorted(by_task.items()):
        if any(t["reward"] > 0.0 for t in trials):
            continue
        modes = Counter(m for t in trials for m in FM.modes_of(t["card"]))
        case_id = trials[0]["case_id"]
        seed = trials[0]["seed"]
        probe = None
        if hints_mod is not None and seed is not None:
            probe = hints_mod.probe_for(case_id, seed)[0]
        shape = trials[0]["shape"] or shapes.get((case_id, seed)) or ""
        out.append({
            "task_id": task_id, "case_id": case_id, "seed": seed,
            "shape": shape, "tier": tier_of(shape) if shape else "unknown",
            "trials": len(trials),
            "oracle": oracle.get(task_id),
            "modes": dict(modes.most_common()),
            "hint_probe": probe,
        })
    return out


#: Tiers whose correct route is short, so their score is near-binary by construction and a mean
#: over it is false precision.
#:
#: Measured on the first complete 95-task campaign: a task with ONE decision point averages 0.219
#: and floors 76% of the time, and it has one decision point because its correct route is three
#: or four nodes long — 17 of those 25 tasks have a route of length 3, and 16 are C-stop. A route
#: that correctly terminates at the gauge has exactly one fork on it. Per tier, mean route length
#: and mean decision points: A-proceed 7.2 / 3.6, B-divert 4.8 / 1.9, C-stop 4.6 / 2.5.
#:
#: So A-proceed has real granularity and keeps its continuous mean, while these two are reported
#: with a RATE beside it: did the project make its one or two decisions correctly, yes or no.
NEAR_BINARY_TIERS = {"B-divert": "divert-correct", "C-stop": "stop-correct"}

#: What each tier is actually asking, in one clause.
QUESTION_OF_TIER = {
    "A-proceed": "did the project walk the route the data called for?",
    "B-divert": "did it divert when the run proved unstable?",
    "C-stop": "did it stop when the prerequisite failed?",
}


def coverage(players) -> dict:
    """What the corpus SHIPS against what this campaign actually observed.

    Every other number in this report is computed over the trials that were found. Nothing
    said what was expected to be there, so a task that drops out -- a container gone at
    artifact collection, a job interrupted, a trial never scheduled -- shrinks n silently and
    the report still reads as a complete corpus. The aggregate layer already refuses to score
    a crashed trial as a zero (`aggregate.py`), which is the right call and is exactly what
    turns a false zero into a missing observation; this is the half that says so out loud.

    Measured once, on the campaign this was written for: one trial in roughly 390 lost its
    agent container at collection. It was caught by hand. Nothing would have caught it.
    """
    try:
        from dmaic_harbor import v2_tasks as V
        cases = V.discover()
    except Exception:  # noqa: BLE001 - a v1-only campaign has no v2 corpus to compare against
        return {}
    shipped = {V.task_id(case, seed) for case in cases.values() for seed in case.seeds}
    if not shipped:
        return {}
    out = {"shipped": len(shipped), "by_agent": {}}
    for agent in sorted({r["agent"] for r in players}):
        seen = {r["task_id"] for r in players if r["agent"] == agent}
        # A campaign may deliberately run fault or hint variants, or a single case. Only the
        # CLEAN shipped ids are held against it, and extras are reported rather than ignored.
        missing = sorted(shipped - seen)
        out["by_agent"][agent] = {
            "observed": len(seen & shipped), "missing": missing,
            "extra": len(seen - shipped),
            "complete": not missing}
    out["complete"] = all(v["complete"] for v in out["by_agent"].values())
    return out


def decision_rate(rows) -> dict:
    """``{n, correct, rate}`` -- trials whose decision points were ALL answered correctly.

    The question a short-route task actually asks. It is read off `pq`, which is the fraction of
    this seed's decision points the contestant got right, so `pq == 1.0` is "made every call
    correctly" and anything else is "did not".
    """
    graded = [r for r in rows
              if int(((r["card"].get("scorecard") or {}).get("pq") or {}).get("points_total") or 0)]
    if not graded:
        return {}
    correct = sum(1 for r in graded
                  if float((r["card"]["scorecard"]["pq"]).get("score") or 0) >= 1.0)
    return {"n": len(graded), "correct": correct, "rate": round(correct / len(graded), 4)}


def _all_decisions_right(row) -> bool:
    """`pq == 1.0` on a task that HAS graded decision points. The question a task asks."""
    pq = ((row["card"].get("scorecard") or {}).get("pq") or {})
    if not int(pq.get("points_total") or 0):
        return False
    return float(pq.get("score") or 0) >= 1.0


def passk(rows, shapes, k: int = 3) -> dict:
    """pass^k and run-to-run spread, over EVERY attempt rather than the deduplicated last one.

    `report()` keeps one row per (task, agent) because a task re-run after a harness fault must
    not be counted twice. That is right for a single-attempt campaign and it is exactly wrong
    here: pass^k is a statement about repeated attempts, so this reads them all.

    Two criteria, because they answer different questions and one of them is nearly dead:

    * ``reward >= RESOLVED_AT`` -- the SWE-bench-shaped "solved it". At a resolve rate near 1%
      pass^3 on this is almost all zeros and says little.
    * **every decision answered correctly** (`pq == 1.0`) -- what a DMAIC task actually asks,
      and where the tier means something. This is the one to read.

    ``spread`` is max-minus-min reward per task, the direct measure of whether a tier's mean is
    a capability or a coin flip. A task attempted fewer than *k* times is reported as such
    rather than counted, so a partial campaign cannot masquerade as a completed pass^k.
    """
    by_task = defaultdict(list)
    for row in rows:
        by_task[(row["task_id"], row["agent"])].append(row)

    tiers = defaultdict(lambda: {"tasks": 0, "eligible": 0,
                                 "passk_resolved": 0, "passk_decisions": 0,
                                 "passat_k_decisions": 0, "spreads": []})
    for (_task, _agent), attempts in sorted(by_task.items()):
        tier = _tier(attempts[0], shapes)
        bucket = tiers[tier]
        bucket["tasks"] += 1
        if len(attempts) < k:
            continue
        bucket["eligible"] += 1
        first_k = attempts[:k]
        if all(a["reward"] >= RESOLVED_AT for a in first_k):
            bucket["passk_resolved"] += 1
        rights = [_all_decisions_right(a) for a in first_k]
        if all(rights):
            bucket["passk_decisions"] += 1
        if any(rights):
            bucket["passat_k_decisions"] += 1
        rewards = [a["reward"] for a in first_k]
        bucket["spreads"].append(round(max(rewards) - min(rewards), 4))

    out = {"k": k, "by_tier": {}}
    for tier, b in sorted(tiers.items()):
        n = b["eligible"]
        out["by_tier"][tier] = {
            "tasks": b["tasks"], "eligible": n,
            "passk_resolved": (round(b["passk_resolved"] / n, 4) if n else None),
            "passk_decisions": (round(b["passk_decisions"] / n, 4) if n else None),
            "pass_at_k_decisions": (round(b["passat_k_decisions"] / n, 4) if n else None),
            "mean_spread": (round(statistics.fmean(b["spreads"]), 4) if b["spreads"] else None),
            "max_spread": (max(b["spreads"]) if b["spreads"] else None),
        }
    total = sum(b["eligible"] for b in tiers.values())
    out["complete"] = total > 0 and total == sum(b["tasks"] for b in tiers.values())
    out["eligible"] = total
    out["tasks"] = sum(b["tasks"] for b in tiers.values())
    return out


def report(job_dirs, controls_dir=None) -> dict:
    """*job_dirs* is one directory or several.

    Several, because a campaign does not always live in one: a run interrupted for any reason
    cannot be resumed once its job config changes (`harbor job resume` reconciles the persisted
    trial configs against the planned one and refuses), so the remainder is finished as a second
    job. Reading only one of them would silently report a partial corpus as the whole.
    """
    if isinstance(job_dirs, (str, Path)):
        job_dirs = [job_dirs]
    job_dirs = [Path(d) for d in job_dirs]
    rows = [r for d in job_dirs for r in _rows(d)]
    # Kept before the dedupe below, because pass^k is a statement about repeated attempts and
    # the dedupe exists to throw repeats away.
    all_rows = list(rows)
    # One task may appear more than once: an interrupted trial re-run in a second job dir, or
    # the SAME task attempted again for pass^k. Keep exactly one instance per (task, agent).
    #
    # The FIRST, not the last. Last-wins was written for the re-run case, where the later
    # instance is the good one; it is wrong for the pass^k case, where the later instances are
    # additional attempts and "last" means an arbitrary one of k. Merging a k=3 job into the
    # headline under last-wins silently moved B-divert from 0.437 to 0.316 — not a re-score,
    # just a different attempt being reported. The headline is a k=1 figure and must be the
    # first attempt of each task; repeats belong to `passk()`, which reads them all.
    seen = {}
    for row in rows:
        seen.setdefault((row["task_id"], row["agent"]), row)
    rows = list(seen.values())
    shapes = _shape_lookup()
    controls = [r for r in rows if r["agent"] in FM.CONTROL_AGENTS]
    players = [r for r in rows if r["agent"] not in FM.CONTROL_AGENTS]
    if controls_dir:
        # Controls usually live in their own job: G3 is run before a campaign, not beside it.
        controls = [r for r in _rows(Path(controls_dir)) if r["agent"] in FM.CONTROL_AGENTS]

    ctrl = {}
    for name in sorted({r["agent"] for r in controls}):
        vals = [r["reward"] for r in controls if r["agent"] == name]
        ctrl[name] = {"n": len(vals), "mean": round(statistics.fmean(vals), 4),
                      "min": round(min(vals), 4), "max": round(max(vals), 4)}

    per_tier = defaultdict(list)
    for r in players:
        per_tier[_tier(r, shapes)].append(r["reward"])
    tiers = {t: {"n": len(v), "mean": round(statistics.fmean(v), 4),
                 "zero_rate": round(sum(1 for x in v if x == 0.0) / len(v), 4),
                 "perfect_rate": round(sum(1 for x in v if x >= 1.0) / len(v), 4)}
             for t, v in sorted(per_tier.items())}

    axes = {}
    for axis in ("ms_recall", "ms_precision", "nf", "pq", "sc", "gate_hard_passed",
                 "hn_fabrication_rate", "ms_misuse"):
        vals = [float((r["card"].get("reward") or {}).get(axis) or 0.0) for r in players]
        if vals:
            axes[axis] = round(statistics.fmean(vals), 4)

    per_case = defaultdict(list)
    for r in players:
        per_case[r["case_id"]].append(r["reward"])

    resolved = [r for r in players if r["reward"] >= RESOLVED_AT]
    per_case_tier = defaultdict(lambda: defaultdict(list))
    rows_by_tier = defaultdict(list)
    for r in players:
        t = _tier(r, shapes)
        per_case_tier[t][r["case_id"]].append(r["reward"])
        rows_by_tier[t].append(r)
    return {
        "job": " + ".join(d.name for d in job_dirs),
        "resolved_at": RESOLVED_AT,
        "resolve_rate": round(len(resolved) / len(players), 4) if players else None,
        "clustered": _cluster_bootstrap({k: v for k, v in per_case.items()}) if players else {},
        "clustered_by_tier": {t: _cluster_bootstrap(dict(cs))
                              for t, cs in sorted(per_case_tier.items())},
        "decision_rate_by_tier": {t: decision_rate(rs)
                                  for t, rs in sorted(rows_by_tier.items())},
        "models": sorted({r["model"] for r in players if r["model"]}),
        "trials": len(rows), "contestant_trials": len(players),
        "coverage": coverage(players),
        "passk": passk([r for r in all_rows if r["agent"] not in FM.CONTROL_AGENTS],
                       shapes, k=3),
        "controls": ctrl,
        "overall_mean": round(statistics.fmean([r["reward"] for r in players]), 4) if players
                        else None,
        "zero_rate": round(sum(1 for r in players if r["reward"] == 0.0) / len(players), 4)
                     if players else None,
        "tiers": tiers,
        "axes": axes,
        "per_case": {k: {"n": len(v), "mean": round(statistics.fmean(v), 4)}
                     for k, v in sorted(per_case.items())},
        "failure_modes": FM.distribution([(r["task_id"], r["card"]) for r in players]),
        "floored": floored(players, controls, shapes),
    }


def render(rep: dict) -> str:
    lines = [f"# Campaign report — {rep['job']}", ""]
    if rep["models"]:
        lines += [f"Model(s): {', '.join(rep['models'])}", ""]
    lines += ["## Controls", "", "| agent | n | mean | min | max |", "|---|---|---|---|---|"]
    for name, c in rep["controls"].items():
        lines.append(f"| `{name}` | {c['n']} | {c['mean']} | {c['min']} | {c['max']} |")
    if not rep["controls"]:
        lines.append("| _none in this job_ | | | | |")
    lines += ["", "**Read the controls first.** An oracle below 1.000 or a nop above 0.000 "
                  "means the scale is not bounded and nothing below is interpretable.", ""]
    cov = rep.get("coverage") or {}
    if cov:
        lines += ["## Corpus coverage", ""]
        if cov.get("complete"):
            lines += [f"Every one of the **{cov['shipped']}** shipped tasks has an observation "
                      "from every contestant. The means below are over the whole corpus.", ""]
        else:
            lines += ["**This campaign is INCOMPLETE and every mean below is over a subset.** "
                      f"The corpus ships {cov['shipped']} tasks.", "",
                      "| agent | observed | missing | missing task ids |",
                      "|---|---|---|---|"]
            for agent, c in sorted(cov.get("by_agent", {}).items()):
                ids = ", ".join(f"`{t}`" for t in c["missing"][:8]) or "—"
                if len(c["missing"]) > 8:
                    ids += f", … (+{len(c['missing']) - 8})"
                lines.append(f"| `{agent}` | {c['observed']}/{cov['shipped']} | "
                             f"{len(c['missing'])} | {ids} |")
            lines += ["", "A missing task is not a zero — the aggregate layer excludes trials "
                      "that produced no verdict rather than averaging them in as failures, "
                      "which is correct. It does mean n is smaller than it looks, and that the "
                      "tasks that dropped out are not a random sample of the corpus: an "
                      "infrastructure failure correlates with the long, slow trials. Re-run "
                      "the ids above before quoting anything below as a corpus result.", ""]
    pk = rep.get("passk") or {}
    if pk.get("eligible"):
        k = pk["k"]
        lines += [f"## pass^{k}", "",
                  f"{pk['eligible']} of {pk['tasks']} tasks were attempted at least {k} times.",
                  "",
                  f"| tier | tasks at k={k} | pass^{k} (every decision right) | "
                  f"pass@{k} | pass^{k} (reward = 1) | mean spread | max spread |",
                  "|---|---|---|---|---|---|---|"]
        for tier, b in sorted(pk["by_tier"].items()):
            if not b["eligible"]:
                continue
            lines.append(f"| {tier} | {b['eligible']} | **{b['passk_decisions']}** | "
                         f"{b['pass_at_k_decisions']} | {b['passk_resolved']} | "
                         f"{b['mean_spread']} | {b['max_spread']} |")
        lines += ["", "**Read the decision column, not the reward one.** At a resolve rate near "
                  "1% a pass^k on `reward = 1` is almost all zeros and distinguishes nothing; "
                  "what a DMAIC task asks is whether every decision was answered correctly, and "
                  "pass^k on THAT is the reliability claim. `spread` is max-minus-min reward "
                  "across the attempts of one task — the direct answer to whether a tier's mean "
                  "is a capability or a coin flip.", ""]
        if not pk.get("complete"):
            lines += [f"**Partial.** {pk['tasks'] - pk['eligible']} task(s) have fewer than {k} "
                      "attempts and are excluded above rather than counted, so this is a pass^k "
                      "over a subset and is not a corpus-level reliability figure.", ""]
    cl = rep.get("clustered") or {}
    lines += [f"## Result — {rep['contestant_trials']} contestant trials", "",
              f"mean **{rep['overall_mean']}**, zero-rate **{rep['zero_rate']}**, "
              f"resolve-rate **{rep.get('resolve_rate')}** at reward >= "
              f"{rep.get('resolved_at')}", ""]
    if cl:
        lines += [f"Case-clustered 95% CI: **[{cl['ci95'][0]}, {cl['ci95'][1]}]** "
                  f"(ICC {cl['icc']}, design effect {cl['design_effect']}, "
                  f"{cl['n_trials']} trials over {cl['n_cases']} cases -> effective n "
                  f"**{cl['effective_n']}**).  ",
                  "Seeds of one case share its graph, brief and generator, so they are not "
                  "independent; an interval computed as though they were is about "
                  f"{cl['design_effect'] ** 0.5:.2f}x too narrow.", ""]
    lines += ["| tier | n | mean | 95% CI (clustered) | zero-rate | perfect-rate |",
              "|---|---|---|---|---|---|"]
    for tier, t in rep["tiers"].items():
        c = (rep.get("clustered_by_tier") or {}).get(tier) or {}
        ci = f"[{c['ci95'][0]}, {c['ci95'][1]}]" if c else "—"
        lines.append(f"| {tier} | {t['n']} | {t['mean']} | {ci} | {t['zero_rate']} | "
                     f"{t['perfect_rate']} |")
    rates = rep.get("decision_rate_by_tier") or {}
    if any(rates.values()):
        lines += ["", "### Every decision answered correctly", "",
                  "| tier | the question it asks | n | all decisions right | mean |",
                  "|---|---|---|---|---|"]
        for tier in ("A-proceed", "B-divert", "C-stop"):
            d = rates.get(tier)
            if not d:
                continue
            q = QUESTION_OF_TIER[tier]
            m = (rep["tiers"].get(tier) or {}).get("mean")
            lines.append(f"| {tier} | {q} | {d['n']} | **{d['correct']}/{d['n']}** "
                         f"({d['rate']:.0%}) | {m} |")
        lines += ["",
                  "Reported for every tier because the gap is informative everywhere, not only "
                  "where the mean misleads. A contestant can carry a high mean on a long route "
                  "while getting a decision wrong: the numeric axes pay for the arithmetic it "
                  "did correctly on the way past the branch it should not have taken.",
                  "",
                  "What differs between the tiers is whether the MEAN is also worth reading. "
                  "A-proceed averages 3.6 decision points over a 7.2-node route, so its mean is "
                  "real granularity. B-divert and C-stop average 1.9 and 2.5 points over routes "
                  "of 4.8 and 4.6 nodes; their score is near-binary by construction and the mean "
                  "is reported beside the rate rather than instead of it."]
    lines += ["", "The tier is the number a difficulty claim rests on; the pooled mean is not.",
              "", "## Axes", "", "| axis | mean |", "|---|---|"]
    for axis, value in rep["axes"].items():
        lines.append(f"| `{axis}` | {value} |")
    lines += ["", FM.render_markdown(rep["failure_modes"], "Failure modes")]
    fl = rep.get("floored") or []
    lines += ["## Tasks no contestant solved", ""]
    if not fl:
        lines.append("None.")
    else:
        lines += [f"{len(fl)} task(s). A task nobody solves is hard OR broken, and the two are "
                  "not distinguishable from the score alone.", "",
                  "| task | tier | oracle | failure modes | hint probe |",
                  "|---|---|---|---|---|"]
        for f in fl:
            oracle = "—" if f["oracle"] is None else f"{f['oracle']:.3f}"
            modes = ", ".join(f"`{m}`×{n}" for m, n in f["modes"].items()) or "—"
            probe = f"`{f['hint_probe']}`" if f["hint_probe"] else "none"
            lines.append(f"| {f['task_id']} | {f['tier']} | {oracle} | {modes} | {probe} |")
        broken = [f for f in fl if f["oracle"] is not None and f["oracle"] < 1.0]
        if broken:
            lines += ["", f"**{len(broken)} of these have an oracle below 1.000** — the ceiling "
                          "is broken there and the zero says nothing about the contestant."]
        else:
            lines += ["", "Every one has an oracle at 1.000, so none is unsolvable by "
                          "construction. That is necessary and not sufficient: it bounds the "
                          "scale, it does not show a contestant could get there. Where a hint "
                          "probe exists, run it (docs/archive/HINT_PROTOCOL.md)."]
    lines += ["", "## Per case", "", "| case | n | mean |", "|---|---|---|"]
    for case_id, c in rep["per_case"].items():
        lines.append(f"| {case_id} | {c['n']} | {c['mean']} |")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="read a finished harbor job into one report")
    ap.add_argument("job_dir", type=Path, nargs="+",
                    help="one or more job directories; trials are merged and de-duplicated "
                         "per (task, agent)")
    ap.add_argument("--controls", type=Path, default=None,
                    help="job directory holding the oracle/nop controls (usually the G3 run), "
                         "so a floored task can be read against its own ceiling")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    rep = report(args.job_dir, controls_dir=args.controls)
    print(json.dumps(rep, indent=1) if args.json else render(rep))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
