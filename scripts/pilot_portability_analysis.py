#!/usr/bin/env python3
"""Second-domain portability pilot: read the pilot jobs, grade every fork, export trajectories.

    DMAIC_PILOT_DOMAINS=1 PYTHONPATH=.:harbor/src python3 scripts/pilot_portability_analysis.py \
        [--jobs pilot-gpt6astra pilot-gpt56sol pilot-gpt56luna] \
        [--md docs/RESULT_PORTABILITY_PILOT.md] [--out output/research/portability_pilot]

Same grading as scripts/restraint_analysis.py (Section 6 of the paper), applied to the two
life-sciences cases: every graded fork on the oracle walk is NO-GO (the correct branch is a
stop) or GO (the correct branch runs the next analysis; a GO whose correct branch is a divert
is reported as DIVERT as well). Every attempt is kept, labelled by attempt index, so k = 1 is
the first attempt and pass^3 / pass@3 read all three.

The export copies, per trial: the contestant's trace.json, report.md, the steward audit log,
the verifier scorecard and reward, the agent's trajectory.json and terminal recording, and the
harness trial.log -- everything needed to re-read a run without the job tree.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

os.environ.setdefault("DMAIC_PILOT_DOMAINS", "1")
sys.path[:0] = [".", "harbor/src"]
from dmaic_harbor import campaign_report as CR                    # noqa: E402
from dmaic_harbor.analysis import tier_of                          # noqa: E402
from dmaic_bench.v2 import harbor_truth as HT, registry             # noqa: E402

JOBS = Path("harbor/jobs")
STOPW = ("fix", "escalate", "remeasure", "special", "reconsider", "not_a", "shortfall",
         "not_shown", "augment", "widen", "more_")
DIVERTW = ("blocked", "adjusted")
#: Trap seeds: the headline check passes and the second criterion fails (6), or the stop comes
#: after the project has produced a convincing result (7). Reported apart.
TRAP_SEEDS = {6, 7}
DEFAULT_JOBS = ["pilot-gpt6astra-v2", "pilot-gpt56sol-v2", "pilot-gpt56luna-v2",
                "pilot-gpt6astra-v2-bare", "pilot-gpt56sol-v2-bare",
                "pilot-gpt56sol-v2-bare-fill", "pilot-gpt56luna-v2-bare"]
#: v1 = the first 12-task build (two forks per task, protocol brief), kept as a first round.
V1_JOBS = ["pilot-gpt6astra", "pilot-gpt56sol", "pilot-gpt56luna"]
LABEL = {"pilot-gpt6astra": "GPT-6-astra [v1]", "pilot-gpt56sol": "GPT-5.6-sol [v1]",
         "pilot-gpt56luna": "GPT-5.6-luna [v1]",
         "pilot-gpt6astra-v2": "GPT-6-astra", "pilot-gpt56sol-v2": "GPT-5.6-sol",
         "pilot-gpt56luna-v2": "GPT-5.6-luna",
         "pilot-gpt6astra-v2-bare": "GPT-6-astra [thresholds-only]",
         "pilot-gpt56sol-v2-bare": "GPT-5.6-sol [thresholds-only]",
         # one trial lost to a gateway 524 and re-run alone; same system, same brief
         "pilot-gpt56sol-v2-bare-fill": "GPT-5.6-sol [thresholds-only]",
         "pilot-gpt56luna-v2-bare": "GPT-5.6-luna [thresholds-only]"}
DOMAIN = {"adb_c40": "RNA-seq (batch structure)", "adb_c41": "GWAS (cohort structure)"}


def is_stop(branch: str) -> bool:
    return any(w in branch.lower() for w in STOPW)


def is_divert(branch: str) -> bool:
    return any(w in branch.lower() for w in DIVERTW)


def load_rows(job: str) -> list:
    """Every scored trial of a job, with an attempt index per task (trial dirs sort by name,
    which carries a random suffix; order attempts by their start time instead)."""
    job_dir = JOBS / job
    if not job_dir.exists():
        return []
    rows = CR._rows(job_dir)
    for r in rows:
        r["job"] = job
        r["job_dir"] = job_dir
        res = job_dir / r["trial"] / "result.json"
        started = ""
        if res.is_file():
            try:
                started = str(json.load(open(res)).get("started_at") or "")
            except (ValueError, OSError):
                pass
        r["started_at"] = started
    by_task = defaultdict(list)
    for r in rows:
        by_task[r["task_id"]].append(r)
    for task, rs in by_task.items():
        rs.sort(key=lambda r: (r["started_at"], r["trial"]))
        for i, r in enumerate(rs):
            r["attempt"] = i + 1
    return [r for r in rows if r["agent"] not in ("oracle", "nop")]


def grade(rows: list, cases: dict) -> list:
    """One record per graded fork per trial."""
    cache = {}
    out = []
    for r in rows:
        cid, seed = r["case_id"], int(r["seed"])
        if cid not in cases:
            continue
        c = cases[cid]
        if (cid, seed) not in cache:
            _b, res = c.generate(seed)
            nm = {k: tuple(c.methods_at(k, res)) for k in c.node_data}
            cache[(cid, seed)] = {p["point_id"]: p for p in
                                  HT.decision_points(c.graph, res, nm, c.method_policy,
                                                     c.accepted_methods)}
        pts = cache[(cid, seed)]
        card = r["card"].get("scorecard") or {}
        pq = card.get("pq") or {}
        sc = card.get("sc") or {}
        per = sc.get("per_point") or {}
        choices = sc.get("choices") or {}
        for det in pq.get("details") or []:
            if det.get("kind") != "decision_point":
                continue
            p = pts.get(det["point_id"])
            if not p:
                continue
            correct = p["correct_branch"]
            kind = "NO-GO" if is_stop(correct) else ("DIVERT" if is_divert(correct) else "GO")
            sp = per.get(det["point_id"])
            own = "none" if not sp or not sc.get("axis_valid") else (
                "agree" if sp["correct_target"] == correct else "disagree")
            out.append({"job": r["job"], "system": LABEL.get(r["job"], r["job"]),
                        "task_id": r["task_id"], "case_id": cid, "seed": seed,
                        "shape": c.shapes.get(seed, ""), "tier": tier_of(c.shapes.get(seed, "")),
                        "attempt": r["attempt"], "point": det["point_id"], "kind": kind,
                        "correct": correct, "chosen": choices.get(det["point_id"]),
                        "verdict": det.get("verdict"), "own_numbers": own,
                        "reward": r["reward"]})
    return out


def trial_table(rows: list, cases: dict) -> list:
    out = []
    for r in rows:
        card = r["card"].get("scorecard") or {}
        c = cases.get(r["case_id"])
        shape = c.shapes.get(int(r["seed"]), "") if c else ""
        ms = card.get("ms") or {}
        nf = (card.get("nf") or {}).get("summary") or {}
        pq = card.get("pq") or {}
        sc = card.get("sc") or {}
        out.append({"system": LABEL.get(r["job"], r["job"]), "job": r["job"],
                    "trial": r["trial"], "task_id": r["task_id"], "case_id": r["case_id"],
                    "seed": int(r["seed"]), "shape": shape, "tier": tier_of(shape),
                    "attempt": r["attempt"], "reward": round(float(r["reward"]), 4),
                    "pq": pq.get("score"), "pq_points": pq.get("points_total"),
                    "nf": nf.get("ratio"), "nf_checked": nf.get("checked"),
                    "nf_failed": nf.get("failed"),
                    "ms_recall": ms.get("recall"), "ms_precision": ms.get("precision"),
                    "ms_misuse": ms.get("misuse_rate"), "sc": sc.get("sc"),
                    "attempted": sorted(ms.get("attempted") or []),
                    "implied_path": sc.get("implied_path") or []})
    return out


def export(rows: list, out_dir: Path) -> int:
    n = 0
    for r in rows:
        src = r["job_dir"] / r["trial"]
        dst = out_dir / "trajectories" / r["job"] / f"{r['task_id']}__attempt{r['attempt']}"
        dst.mkdir(parents=True, exist_ok=True)
        for rel in ("artifacts/trace.json", "artifacts/report.md", "artifacts/steward-audit.jsonl",
                    "verifier/scorecard.json", "verifier/reward.json", "verifier/test-stdout.txt",
                    "agent/trajectory.json", "agent/recording.cast", "agent/terminus_2.pane",
                    "trial.log", "result.json", "config.json"):
            f = src / rel
            if f.is_file():
                shutil.copy2(f, dst / f.name)
                n += 1
    return n


def _pct(w, n):
    return f"{100.0 * w / n:.0f}%" if n else "n/a"


def _ci(vals):
    if len(vals) < 2:
        return ""
    sd = statistics.pstdev(vals)
    return f" (sd {sd:.3f})"


def render(rows, forks, cases, jobs) -> str:
    systems = list(dict.fromkeys(LABEL.get(j, j) for j in jobs
                                 if any(r["job"] == j for r in rows)))
    L = ["# Second-domain portability pilot: RNA-seq and GWAS", "",
         "Two life-sciences decision-graph cases, eight seeds each (sixteen tasks), three "
         "OpenAI-family agents, three attempts under the protocol brief and one under the "
         "thresholds-only brief, the same scaffold and scorer as the 97-task DMAIC corpus. "
         "Generated by `scripts/pilot_portability_analysis.py`; the per-trial evidence (scorecards, "
         "trace, report, steward audit) is in `output/research/portability_pilot/evidence/`, "
         "anonymised by `scripts/pilot_export_release.py`.", ""]
    L.append("## Cases")
    L.append("")
    L.append("| case | domain | seeds | routes |")
    L.append("|---|---|---|---|")
    for cid in sorted(DOMAIN):
        c = cases.get(cid)
        if not c:
            continue
        routes = Counter(tier_of(c.shapes.get(s, "")) for s in c.seeds)
        L.append(f"| {cid} | {DOMAIN[cid]} | {len(c.seeds)} | "
                 + ", ".join(f"{k} x{v}" for k, v in sorted(routes.items())) + " |")
    L.append("")
    L.append("## Reward by system (all attempts; first attempt in brackets)")
    L.append("")
    L.append("| system | trials | mean reward | first-attempt mean | RNA-seq | GWAS | A-proceed | B-divert | C-stop |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for s in systems:
        rs = [r for r in rows if r["system"] == s]
        k1 = [r for r in rs if r["attempt"] == 1]
        def m(sub):
            return f"{statistics.fmean(x['reward'] for x in sub):.3f}" if sub else "n/a"
        L.append(f"| {s} | {len(rs)} | {m(rs)} | {m(k1)} | "
                 f"{m([r for r in rs if r['case_id'] == 'adb_c40'])} | "
                 f"{m([r for r in rs if r['case_id'] == 'adb_c41'])} | "
                 f"{m([r for r in rs if r['tier'] == 'A-proceed'])} | "
                 f"{m([r for r in rs if r['tier'] == 'B-divert'])} | "
                 f"{m([r for r in rs if r['tier'] == 'C-stop'])} |")
    L.append("")
    L.append("## Fork accuracy by decision class (all attempts)")
    L.append("")
    L.append("Correct = the verifier's verdict on the fork is `correct`; wrong pools "
             "`incorrect` (another branch taken) and `unknown` (the fork never reached, or no "
             "evidence either way).")
    L.append("")
    L.append("| system | NO-GO right | GO right | DIVERT right | NO-GO right, first attempt | own numbers said NO-GO, went anyway |")
    L.append("|---|---|---|---|---|---|")
    for s in systems:
        fs = [f for f in forks if f["system"] == s]
        def acc(sub):
            n = len(sub)
            w = sum(1 for f in sub if f["verdict"] == "correct")
            return f"{w}/{n} ({_pct(w, n)})" if n else "n/a"
        nogo = [f for f in fs if f["kind"] == "NO-GO"]
        went = sum(1 for f in nogo if f["verdict"] != "correct" and f["own_numbers"] == "agree")
        wrong = sum(1 for f in nogo if f["verdict"] != "correct")
        L.append(f"| {s} | {acc(nogo)} | {acc([f for f in fs if f['kind'] == 'GO'])} | "
                 f"{acc([f for f in fs if f['kind'] == 'DIVERT'])} | "
                 f"{acc([f for f in nogo if f['attempt'] == 1])} | "
                 f"{went}/{wrong} |")
    L.append("")
    L.append("## Fork accuracy by case and fork")
    L.append("")
    L.append("| case | fork | class | " + " | ".join(systems) + " |")
    L.append("|---|---|---|" + "---|" * len(systems))
    keys = sorted({(f["case_id"], f["point"], f["kind"]) for f in forks})
    for cid, point, kind in keys:
        cells = []
        for s in systems:
            sub = [f for f in forks if f["system"] == s and f["case_id"] == cid
                   and f["point"] == point and f["kind"] == kind]
            w = sum(1 for f in sub if f["verdict"] == "correct")
            cells.append(f"{w}/{len(sub)}" if sub else "-")
        L.append(f"| {cid} | {point} | {kind} | " + " | ".join(cells) + " |")
    L.append("")
    L.append("## pass^3 and pass@3 by routing tier")
    L.append("")
    L.append("A task passes an attempt when every graded fork on it is correct.")
    L.append("")
    L.append("| system | tier | tasks | pass^3 | pass@3 | mean pass rate |")
    L.append("|---|---|---|---|---|---|")
    for s in systems:
        for tier in ("A-proceed", "B-divert", "C-stop"):
            by_task = defaultdict(dict)
            for f in forks:
                if f["system"] != s or f["tier"] != tier:
                    continue
                by_task[f["task_id"]].setdefault(f["attempt"], True)
                if f["verdict"] != "correct":
                    by_task[f["task_id"]][f["attempt"]] = False
            if not by_task:
                continue
            three = {t: a for t, a in by_task.items() if len(a) >= 3}
            all3 = sum(1 for a in three.values() if all(a.values()))
            any3 = sum(1 for a in three.values() if any(a.values()))
            rate = statistics.fmean(statistics.fmean(a.values()) for a in by_task.values())
            p3 = f"{all3}/{len(three)}" if three else "n/a (k = 1)"
            pa = f"{any3}/{len(three)}" if three else "n/a (k = 1)"
            L.append(f"| {s} | {tier} | {len(by_task)} | {p3} | {pa} | {rate:.2f} |")
    L.append("")
    L.append("## The trap seeds (6: second criterion; 7: late stop), all attempts")
    L.append("")
    L.append("| system | case | seed | shape | forks right / graded | NO-GO fork right |")
    L.append("|---|---|---|---|---|---|")
    for s in systems:
        for cid in sorted(DOMAIN):
            for seed in sorted(TRAP_SEEDS):
                sub = [f for f in forks if f["system"] == s and f["case_id"] == cid
                       and f["seed"] == seed]
                if not sub:
                    continue
                w = sum(1 for f in sub if f["verdict"] == "correct")
                ng = [f for f in sub if f["kind"] == "NO-GO"]
                nw = sum(1 for f in ng if f["verdict"] == "correct")
                L.append(f"| {s} | {cid} | {seed} | {sub[0]['shape']} | {w}/{len(sub)} | "
                         f"{nw}/{len(ng)} |")
    L.append("")
    L.append("## Brief control: protocol versus thresholds-only (first attempt)")
    L.append("")
    L.append("The protocol brief states each rule and what a failed one forbids (the regime of "
             "the paper's normative instruction); the thresholds-only brief states the same "
             "numbers and nothing about consequences (the plain regime). Same tasks, same data.")
    L.append("")
    L.append("| system | brief | NO-GO right | DIVERT right | GO right | mean reward |")
    L.append("|---|---|---|---|---|---|")
    for s in systems:
        j = next(jj for jj in jobs if LABEL.get(jj, jj) == s)
        fs = [f for f in forks if f["system"] == s and f["attempt"] == 1]
        rs = [r for r in rows if r["system"] == s and r["attempt"] == 1]
        if not fs:
            continue
        def acc(kind):
            sub = [f for f in fs if f["kind"] == kind]
            w = sum(1 for f in sub if f["verdict"] == "correct")
            return f"{w}/{len(sub)}" if sub else "-"
        brief = "thresholds-only" if j.endswith("-bare") else "protocol"
        base = s.replace(" [thresholds-only]", "")
        L.append(f"| {base} | {brief} | {acc('NO-GO')} | {acc('DIVERT')} | {acc('GO')} | "
                 f"{statistics.fmean(r['reward'] for r in rs):.3f} |")
    L.append("")
    L.append("## Every trial")
    L.append("")
    L.append("| system | task | shape | tier | attempt | reward | pq | nf | ms recall | ms precision | misuse | implied path |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: (r["system"], r["task_id"], r["attempt"])):
        def f3(v):
            return "n/a" if v is None else f"{float(v):.2f}"
        L.append(f"| {r['system']} | {r['task_id']} | {r['shape']} | {r['tier']} | {r['attempt']} | "
                 f"{r['reward']:.3f} | {f3(r['pq'])} | {f3(r['nf'])} | {f3(r['ms_recall'])} | "
                 f"{f3(r['ms_precision'])} | {f3(r['ms_misuse'])} | "
                 f"{' > '.join(r['implied_path'])} |")
    L.append("")
    return "\n".join(L)


def render_tex(rows, forks, jobs) -> str:
    """tab_portability.tex: one row per system, fork accuracy by class over all attempts and
    mean reward by routing tier; counts carry their denominators."""
    systems = list(dict.fromkeys(LABEL.get(j, j) for j in jobs
                                 if any(r["job"] == j for r in rows)))
    L = [r"\begin{table}[t]", r"\centering", r"\small",
         r"\caption{\textbf{Second-domain pilot.} Fork accuracy by decision class and mean "
         r"reward by routing tier on the sixteen life-sciences tasks (RNA-seq case 40, GWAS case "
         r"41): three attempts under the protocol brief, one under the thresholds-only brief. "
         r"Counts are correct forks over graded forks.}",
         r"\label{tab:portability}",
         r"\begin{tabular}{llcccccc}", r"\toprule",
         r"system & brief & no-go & divert & go & A-proceed & B-divert & C-stop \\",
         r"\midrule"]
    for s in systems:
        fs = [f for f in forks if f["system"] == s]
        rs = [r for r in rows if r["system"] == s]
        def acc(kind):
            sub = [f for f in fs if f["kind"] == kind]
            w = sum(1 for f in sub if f["verdict"] == "correct")
            return f"{w}/{len(sub)}" if sub else "--"
        def m(tier):
            sub = [r for r in rs if r["tier"] == tier]
            return f"{statistics.fmean(x['reward'] for x in sub):.2f}" if sub else "--"
        brief = "thresholds" if "thresholds-only" in s else "protocol"
        name = s.replace(" [thresholds-only]", "")
        L.append(f"{name} & {brief} & {acc('NO-GO')} & {acc('DIVERT')} & {acc('GO')} & "
                 f"{m('A-proceed')} & {m('B-divert')} & {m('C-stop')} \\\\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", nargs="+", default=DEFAULT_JOBS)
    ap.add_argument("--md", default="docs/RESULT_PORTABILITY_PILOT.md")
    ap.add_argument("--out", default="output/research/portability_pilot")
    ap.add_argument("--no-export", action="store_true")
    ap.add_argument("--tex", default=None, help="write tab_portability.tex here")
    a = ap.parse_args()
    cases = registry.discover()
    rows = []
    for j in a.jobs:
        rows += load_rows(j)
    if not rows:
        print("no scored trials found under", [str(JOBS / j) for j in a.jobs])
        return 1
    forks = grade(rows, cases)
    table = trial_table(rows, cases)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "trials.json").write_text(json.dumps(table, indent=1), encoding="utf-8")
    (out / "forks.json").write_text(json.dumps(forks, indent=1), encoding="utf-8")
    md = render(table, forks, cases, a.jobs)
    Path(a.md).write_text(md, encoding="utf-8")
    if a.tex:
        Path(a.tex).write_text(render_tex(table, forks, a.jobs), encoding="utf-8")
    n = 0 if a.no_export else export(rows, out)
    print(f"{len(rows)} trials, {len(forks)} graded forks; wrote {a.md}; exported {n} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
