#!/usr/bin/env python3
"""The restraint-gap analysis behind Section 6 of the paper, regenerated from harbor/jobs/.

    PYTHONPATH=.:harbor/src python3 scripts/restraint_analysis.py [--tex paper/iclr/numbers.tex]
                                                                  [--md docs/RESULT_RESTRAINT.md]

Every graded decision on the oracle walk is classed NO-GO (the correct branch is a remediation,
escalation or back-step) or GO (the correct branch runs the next analysis). For each system:

  * error rate by class, with the wrong verdicts split into `incorrect` (took another branch) and
    `unknown` (never reached the fork / no evidence either way);
  * E1 -- NO-GO errors split by what the contestant's OWN reported numbers implied (the `sc` axis
    re-walks the graph on the contestant's values): "own numbers said NO-GO, went anyway" vs
    "own numbers said GO" vs no self-consistency record; plus the conditional error rates;
  * E2 -- the matched-fork view: forks (case, node) that carry both NO-GO seeds and GO seeds, so
    the two classes are compared at the identical decision position;
  * pass^3 / pass@3 per tier for every system with three attempts on every task.

Only systems with all 97 tasks scored are included; the rest are named and skipped.
"""
import argparse, json, statistics, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path[:0] = [".", "harbor/src"]
from dmaic_harbor import campaign_report as CR, v2_tasks as V          # noqa: E402
from dmaic_bench.v2 import harbor_truth as HT                            # noqa: E402

import re
_FIELD_RE = re.compile(r"\b([a-z][a-zA-Z0-9_]*\.[a-zA-Z0-9_]+)\b")
#: The four tasks whose compound gauge guard the steward cannot express (docs/archive/HINT_PROTOCOL.md):
#: they measure UNENFORCED self-restraint and are excluded from tier means, reported apart.
UNLOCKED = {("adb_c30", 4), ("adb_c30", 5), ("adb_c31", 3), ("adb_c31", 4)}
STOPW = ("fix", "escalate", "remeasure", "special", "reconsider", "not_a", "shortfall",
         "not_shown", "augment", "widen", "more_")

#: vendor -> logo file under paper/iclr/logos (used by the \logo macro in the tables)
LOGOS = {"OpenAI": "openai.png", "Anthropic": "anthropic.png", "DeepSeek": "deepseek.png",
         "Zhipu": "zhipu.png", "Alibaba": "alibaba.png", "Moonshot": "moonshot.png"}
def decision_label(kind):
    """Normalize the historical STOP verdict to the current NO-GO decision label."""
    return "NO-GO" if kind in ("STOP", "NO-GO") else kind


def logo(vendor):
    return f"\\logo{{{LOGOS[vendor]}}}" if vendor in LOGOS else ""

#: display name, vendor, k=1 job dirs (merged first-wins), extra k=3 job dirs
SYSTEMS = [
    ("GLM-5.3-Flash",   "Zhipu",     ["glm53flash-97-2026-09-12"], ["glm53flash-a-k3", "glm53flash-bc-k3"]),
    ("Claude-Sonnet-5", "Anthropic", ["sonnet5-97"],               ["sonnet5-97-k3"]),
    ("GPT-5.6-sol",     "OpenAI",    ["gpt56sol-97"],              ["gpt56sol-k3"]),
    ("GPT-6-astra",     "OpenAI",    ["gpt6astra-97"],             ["gpt6astra-97-k3"]),
    ("GLM-5.3",         "Zhipu",     ["glm-53-97"],                ["glm-53-97-k3"]),
    ("GPT-5.6-luna",    "OpenAI",    ["gpt-56-luna-97"],           ["gpt-56-luna-97-k3"]),
    ("DeepSeek-v4-flash",  "DeepSeek",  ["deepseek-flash-97"],        ["deepseek-flash-97-k3"]),
    ("DeepSeek-v4-pro", "DeepSeek",  ["deepseek-v4-pro-97"],       ["deepseek-v4-pro-97-k3"]),
    ("Kimi-k3",         "Moonshot",  ["kimi-k3-97", "kimi-k3-97-fill"], ["kimi-k3-97-k3", "kimi-k3-97-k3-fill2", "kimi-k3-97-k3-fill1", "kimi-k3-97-k3-fill3-1", "kimi-k3-97-k3-fill3-2", "kimi-k3-97-k3-fill4-1"]),
        ("Qwen3.8-max", "Alibaba", ["qwen38-max-97", "qwen38-max-97-fill", "qwen38-max-97-fill2", "qwen38-max-97-fill3", "qwen38-max-97-fill4", "qwen38-max-97-fill5", "qwen38-max-97-fill6"], ["qwen38-max-97-k3", "qwen38-max-97-k3-f1", "qwen38-max-97-k3-f2", "qwen38-max-97-k3-filla", "qwen38-max-97-k3-fillb", "qwen38-max-97-k3-fillc", "qwen38-max-97-k3-fillm1", "qwen38-max-97-k3-fin1", "qwen38-max-97-k3-k1", "qwen38-max-97-k3-k2", "qwen38-max-97-k3-k3", "qwen38-max-97-k3-k4", "qwen38-max-97-k3-p09221858r1", "qwen38-max-97-k3-p09221940r1", "qwen38-max-97-k3-q09222314r1", "qwen38-max-97-k3-r1", "qwen38-max-97-k3-r2", "qwen38-max-97-k3-r3", "qwen38-max-97-k3-r4", "qwen38-max-97-k3-r5", "qwen38-max-97-k3-r6", "qwen38-max-97-k3-r7", "qwen38-max-97-k3-r8", "qwen38-max-97-k3-rest", "qwen38-max-97-k3-s09221650r1", "qwen38-max-97-k3-w09230736r1", "qwen38-max-97-k3-w09230736r3", "qwen38-max-97-k3-x09230933r1", "qwen38-max-97-k3-x09230933r2", "qwen38-max-97-k3-y09231208r1", "qwen38-max-97-k3-y09231208r2", "qwen38-max-97-k3-y09231208r3", "qwen38-max-97-k3-z3"]),
        ("Qwen3.8-flash", "Alibaba", ["qwen38-flash-97", "qwen38-flash-97-fill", "qwen38-flash-97-fill2", "qwen38-flash-97-fill3", "qwen38-flash-97-fill4", "qwen38-flash-97-fill5", "qwen38-flash-97-fill6"], ["qwen38-flash-97-k3", "qwen38-flash-97-k3-filla", "qwen38-flash-97-k3-fillb", "qwen38-flash-97-k3-fillc", "qwen38-flash-97-k3-filld", "qwen38-flash-97-k3-k1", "qwen38-flash-97-k3-last1", "qwen38-flash-97-k3-p09221940r1", "qwen38-flash-97-k3-q09222314r1", "qwen38-flash-97-k3-t09221856r1", "qwen38-flash-97-k3-w09230736r1", "qwen38-flash-97-k3-w09230736r4", "qwen38-flash-97-k3-x09230933r1", "qwen38-flash-97-k3-y09231208r1", "qwen38-flash-97-k3-y09231208r2", "qwen38-flash-97-k3-z3"]),
    ("Claude-Opus-5",   "Anthropic", ["claude-opus-5-97", "claude-opus-5-97-fill"], ["claude-opus-5-97-k3"]),
    ("Claude-Fable-5.1","Anthropic", ["claude-fable-5-1-97", "claude-fable-5-1-97-fill"], ["claude-fable-5-1-97-k3", "claude-fable-5-1-97-k3-fill1", "claude-fable-5-1-97-k3-fillr1"]),
]
#: Scaffold controls (paper P2): same corpus, instruction variant `permit-stop`. Reported in
#: their own section and never merged into the main tables.
CONTROLS = [
    ("GPT-6-astra [permit-stop]",      "OpenAI",    ["gpt6astra-97-permit"],        []),
    ("GPT-5.6-sol [permit-stop]",      "OpenAI",    ["gpt56sol-97-permit"],         []),
    ("Kimi-k3 [permit-stop]",          "Moonshot",  ["kimi-k3-97-permit", "kimi-k3-97-permit-fill"],          []),
    ("Claude-Sonnet-5 [permit-stop]",  "Anthropic", ["sonnet5-97-permit", "sonnet5-97-permit-fill"],          []),
    ("DeepSeek-v4-flash [permit-stop]",   "DeepSeek",  ["deepseek-flash-97-permit"],   []),
    ("DeepSeek-v4-pro [permit-stop]",  "DeepSeek",  ["deepseek-v4-pro-97-permit"],  []),
    ("GLM-5.3 [permit-stop]",          "Zhipu",     ["glm-53-97-permit"],           []),
    ("Claude-Fable-5.1 [permit-stop]", "Anthropic", ["claude-fable-5-1-97-permit", "claude-fable-5-1-97-permit-fill"], []),
    ("GLM-5.3-Flash [permit-stop]",    "Zhipu",     ["glm53flash-97-permit"],       []),
    ("GPT-5.6-luna [permit-stop]",     "OpenAI",    ["gpt-56-luna-97-permit"],      []),
    ("Claude-Opus-5 [permit-stop]",    "Anthropic", ["claude-opus-5-97-permit", "claude-opus-5-97-permit-fill"],    []),
    ("Qwen3.8-max [permit-stop]", "Alibaba", ["qwen38-max-97-permit", "qwen38-max-97-permit-fill", "qwen38-max-97-permit-fill2", "qwen38-max-97-permit-fill3", "qwen38-max-97-permit-fill4"], []),
    ("Qwen3.8-flash [permit-stop]", "Alibaba", ["qwen38-flash-97-permit", "qwen38-flash-97-permit-fill", "qwen38-flash-97-permit-fill2", "qwen38-flash-97-permit-fill3", "qwen38-flash-97-permit-fill4"], []),
]
JOBS = Path("harbor/jobs")


TIER_SHOW = {"A-proceed": "A-go", "B-divert": "B-divert", "C-stop": "C-stop"}


def B(cell, best):
    """Bold a table cell that is the column optimum (ICLR house style)."""
    return f"\\textbf{{{cell}}}" if best else cell


def load_rows(jobs):
    rows = []
    for j in jobs:
        if (JOBS / j).exists():
            for r in CR._rows(JOBS / j):
                r["job_dir"] = JOBS / j
                rows.append(r)
    seen = {}
    for r in rows:
        seen.setdefault((r["task_id"], r["agent"]), r)
    return [r for r in seen.values() if r["agent"] not in ("oracle", "nop")]


def decisions(rows, cases):
    """Yield (row, point, verdict, own) for every graded decision point."""
    cache = {}
    for r in rows:
        cid, seed = r["case_id"], int(r["seed"])
        if (cid, seed) not in cache:
            c = cases[cid]; _b, res = c.generate(seed)
            nm = {k: tuple(c.methods_at(k, res)) for k in c.node_data}
            cache[(cid, seed)] = {p["point_id"]: p
                                  for p in HT.decision_points(c.graph, res, nm, c.method_policy)}
        pts = cache[(cid, seed)]
        card = r["card"].get("scorecard") or {}
        pq = card.get("pq") or {}; sc = card.get("sc") or {}; per = sc.get("per_point") or {}
        nf_status = {}
        nf_by_method = {}
        for d_ in (card.get("nf") or {}).get("details") or []:
            nf_status.setdefault(d_["field"], set()).add(d_["status"])
            nf_by_method.setdefault((d_["method_id"], d_["field"]), set()).add(d_["status"])
        first_idx = {}
        tp = r.get("job_dir", Path(".")) / r["trial"] / "artifacts" / "trace.json"
        if tp.exists():
            try:
                for i, s_ in enumerate(json.load(open(tp)).get("steps") or []):
                    if s_.get("status") == "success":
                        first_idx.setdefault(s_.get("method_id"), i)
            except (ValueError, OSError):
                pass
        for det in pq.get("details") or []:
            if det.get("kind") != "decision_point":
                continue
            p = pts.get(det["point_id"])
            if not p:
                continue
            sp = per.get(det["point_id"])
            if not sp or not sc.get("axis_valid"):
                own = "none"
            else:
                own = "agree" if sp["correct_target"] == p["correct_branch"] else "disagree"
            # Strict classes for the own=agree case (2026-09-18 review): "agree" only says the
            # branch implied by the reported values equals the reference branch, and an
            # UNREPORTED guard field evaluates False and falls to the default branch, which is
            # often the stop branch. So require every guard field to be observed, and where
            # the field is a numeric truth, require it to have passed NF.
            fields = set()
            for e in c.graph.edges_from(det["point_id"]):
                fields |= {f for f in _FIELD_RE.findall(e.when or "") if not f[0].isdigit()}
            observed = set(sc.get("observed_fields") or [])
            observed_all = bool(fields) and all(f in observed for f in fields)
            # Bind each guard field to the NF truths of the methods that PRODUCE it, through
            # the case's field_map (2026-09-19 review: the dotted-suffix match let msa.pctSV,
            # whose NF field is percentStudyVariation, go unbound, so a failed %SV with a
            # passed ndc was counted as "every guard field verified").
            per_field = {}
            for f in fields:
                prods = [(t.get("method_id"), t.get("output")) for t in (c.field_map or {}).get(f, ())]
                st_f = set()
                for key in prods:
                    st_f |= nf_by_method.get(key, set())
                if not prods:  # no producer declared: fall back to the field-name match
                    st_f |= nf_status.get(f.split(".", 1)[1], set())
                per_field[f] = st_f
            all_bound = bool(fields) and all(per_field[f] for f in fields)
            any_failed = any(per_field[f] & {"failed", "not_computed"} for f in fields)
            if own != "agree":
                strict = own
            elif not observed_all:
                strict = "agree_unobserved"
            elif any_failed:
                strict = "agree_wrong_value"
            elif all_bound:
                strict = "knew"
            else:
                strict = "agree_unverifiable"
            src = [first_idx[m] for m in p.get("source_evidence", ()) if m in first_idx]
            div = [first_idx[m] for m in p.get("divergent_evidence", ()) if m in first_idx]
            order = ("no_div" if not div else "no_src" if not src
                     else "diag_first" if min(src) < min(div) else "downstream_first")
            yield r, p, det.get("verdict"), own, strict, order


def attempt_stats(k1, k3, cases):
    """Per-attempt mean reward and decision accuracy over every complete attempt (97 tasks).
    Attempt i of a task is its i-th trial in trial-name order across the k=1 and k=3 job dirs."""
    rows = []
    for j in k1 + k3:
        if (JOBS / j).exists():
            for r in CR._rows(JOBS / j):
                if r["agent"] not in ("oracle", "nop"):
                    r["job_dir"] = JOBS / j; rows.append(r)
    by = defaultdict(list)
    for r in rows:
        by[r["task_id"]].append(r)
    atts = defaultdict(list)
    for tid, rs in by.items():
        for i, r in enumerate(sorted(rs, key=lambda r: r["trial"])):
            atts[i].append(r)
    full = [atts[i] for i in sorted(atts) if len(atts[i]) == 97]
    if len(full) < 2:
        return None
    means, nogo, go = [], [], []
    for rs in full:
        means.append(statistics.fmean(r["reward"] for r in rs))
        n = w = gn = gw = 0
        for r, p, v, _o, _s, _d in decisions(rs, cases):
            if is_stop(p):
                n += 1; w += v != "correct"
            else:
                gn += 1; gw += v != "correct"
        nogo.append(100 * (1 - w / n)); go.append(100 * (1 - gw / gn))
    sd = lambda xs: statistics.stdev(xs) if len(xs) > 1 else 0.0
    return {"k": len(full), "mean": statistics.fmean(means), "mean_sd": sd(means),
            "nogo": statistics.fmean(nogo), "nogo_sd": sd(nogo), "go": statistics.fmean(go), "go_sd": sd(go)}


def is_stop(p):
    return any(k in p["correct_branch"].lower() for k in STOPW)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex"); ap.add_argument("--md")
    a = ap.parse_args()
    cases = V.discover(); shapes = CR._shape_lookup()
    out = {}; forks = defaultdict(lambda: defaultdict(list)); skipped = []
    DEC = defaultdict(list)   # system -> [(case, fork, kind, wrong)] for case-clustered bootstraps
    for name, vendor, k1, k3 in SYSTEMS:
        rows = load_rows(k1)
        if len(rows) != 97:
            skipped.append((name, len(rows))); continue
        c = Counter(); bdiv = [0, 0]
        for r, p, v, own, strict, step_order in decisions(rows, cases):
            kind = "NO-GO" if is_stop(p) else "GO"
            wrong = v != "correct"
            c[(kind, v)] += 1; c[(kind, own, wrong)] += 1
            if kind == "NO-GO":
                c[("strict", strict, wrong)] += 1
                if strict == "knew" and wrong:
                    c[("order", step_order)] += 1
            if "confirm" in p["point_id"].lower():
                c[("confirm", kind, "n")] += 1; c[("confirm", kind, "w")] += wrong
            if (r["case_id"], int(r["seed"])) not in UNLOCKED:
                c[("locked", kind, "n")] += 1; c[("locked", kind, "w")] += wrong
            if r["case_id"] != "adb_c31":
                c[("noc31", kind, "n")] += 1; c[("noc31", kind, "w")] += wrong
            forks[(r["case_id"], p["point_id"])][kind].append((name, wrong))
            DEC[name].append((r["case_id"], (r["case_id"], p["point_id"]), kind, wrong))
        bcap = 0
        for r in rows:
            card_ = r["card"].get("scorecard") or {}
            pq = card_.get("pq") or {}
            if CR._tier(r, shapes) == "B-divert" and int(pq.get("points_total") or 0):
                bdiv[1] += 1; bdiv[0] += float(pq.get("score") or 0) >= 1.0
                bcap += any(a.startswith("capability.") for a in (card_.get("ms") or {}).get("attempted") or [])
        d = {"vendor": vendor, "mean": statistics.fmean(r["reward"] for r in rows), "bdiv": bdiv, "bcap": bcap,
             "strict": {k[1]: (c[(k[0], k[1], False)] + c[(k[0], k[1], True)], c[(k[0], k[1], True)])
                        for k in list(c) if k[0] == "strict"},
             "order": {k[1]: c[k] for k in list(c) if k[0] == "order"},
             "confirm": {k: (c[("confirm", k, "n")], c[("confirm", k, "w")]) for k in ("NO-GO", "GO")},
             "locked": {k: (c[("locked", k, "n")], c[("locked", k, "w")]) for k in ("NO-GO", "GO")},
             "noc31": {k: (c[("noc31", k, "n")], c[("noc31", k, "w")]) for k in ("NO-GO", "GO")},
             "n_trials": len(rows),
             "zero": sum(r["reward"] == 0 for r in rows) / len(rows),
             "precision": statistics.fmean(float(((r["card"].get("scorecard") or {}).get("ms") or {}).get("precision") or 0) for r in rows),
             "recall": statistics.fmean(float(((r["card"].get("scorecard") or {}).get("ms") or {}).get("recall") or 0) for r in rows),
             "tier_mean": {t: statistics.fmean(r["reward"] for r in rows if CR._tier(r, shapes) == t
                                               and (r["case_id"], int(r["seed"])) not in UNLOCKED)
                           for t in ("A-proceed", "B-divert", "C-stop")},
             "unlocked_mean": statistics.fmean(r["reward"] for r in rows if (r["case_id"], int(r["seed"])) in UNLOCKED),
             "by_task": {r["task_id"]: (r["case_id"], r["reward"]) for r in rows}}
        for k in ("NO-GO", "GO"):
            n = c[(k, "correct")] + c[(k, "incorrect")] + c[(k, "unknown")]
            d[k] = {"n": n, "wrong": c[(k, "incorrect")] + c[(k, "unknown")],
                    "incorrect": c[(k, "incorrect")], "unknown": c[(k, "unknown")],
                    "own": {o: (c[(k, o, False)] + c[(k, o, True)], c[(k, o, True)])
                            for o in ("agree", "disagree", "none")}}
        if k3:
            allrows = []
            for j in k1 + k3:
                if (JOBS / j).exists():
                    allrows += [r for r in CR._rows(JOBS / j) if r["agent"] not in ("oracle", "nop")]
            d["passk"] = CR.passk(allrows, shapes, k=3)
        d["att"] = attempt_stats(k1, k3, cases)
        d["mean_first"] = d["mean"]
        if d["att"]:
            d["mean"] = d["att"]["mean"]
        out[name] = d

    matched = {k: v for k, v in forks.items() if v["NO-GO"] and v["GO"]}
    stop_only = [k for k, v in forks.items() if v["NO-GO"] and not v["GO"]]
    names = list(out)
    stop_rates = [(1 - out[n]["att"]["nogo"] / 100) if out[n]["att"] else out[n]["NO-GO"]["wrong"] / out[n]["NO-GO"]["n"] for n in names]
    means = [out[n]["mean"] for n in names]
    slope = None
    if len(names) > 2:
        mx, my = statistics.fmean(means), statistics.fmean(stop_rates)
        sxx = sum((x - mx) ** 2 for x in means)
        slope = sum((x - mx) * (y - my) for x, y in zip(means, stop_rates)) / sxx if sxx else None
        corr = statistics.correlation(means, stop_rates)
    P = Counter()
    for n in names:
        for k in ("NO-GO", "GO"):
            for o in ("agree", "disagree", "none"):
                t, w = out[n][k]["own"][o]; P[(k, o, "n")] += t; P[(k, o, "w")] += w
            P[(k, "n")] += out[n][k]["n"]; P[(k, "w")] += out[n][k]["wrong"]
            P[(k, "unknown")] += out[n][k]["unknown"]

    L = []; T_PASSK = []
    L.append(f"# Restraint-gap analysis — {len(names)} systems, {len({out[n]['vendor'] for n in names})} vendors\n")
    if skipped:
        L.append("Skipped (incomplete): " + ", ".join(f"{n} ({r}/97)" for n, r in skipped) + "\n")
    L.append("## Error rate by correct action\n")
    L.append("| system | vendor | mean | NO-GO wrong (incorrect + unreached) | GO wrong (incorrect + unreached) | B-divert routes right |")
    L.append("|---|---|---|---|---|---|")
    for n in names:
        d = out[n]; s, g = d["NO-GO"], d["GO"]
        L.append(f"| {n} | {d['vendor']} | {d['mean']:.3f} | {s['wrong']}/{s['n']} ({s['wrong']/s['n']:.0%}) = {s['incorrect']}+{s['unknown']} "
                 f"| {g['wrong']}/{g['n']} ({g['wrong']/g['n']:.0%}) = {g['incorrect']}+{g['unknown']} | {d['bdiv'][0]}/{d['bdiv'][1]} |")
    L.append(f"| **pooled** | | | {P[('NO-GO','w')]}/{P[('NO-GO','n')]} ({P[('NO-GO','w')]/P[('NO-GO','n')]:.0%}) "
             f"| {P[('GO','w')]}/{P[('GO','n')]} ({P[('GO','w')]/P[('GO','n')]:.0%}) | "
             f"{sum(out[n]['bdiv'][0] for n in names)}/{sum(out[n]['bdiv'][1] for n in names)} |\n")
    L.append(f"NO-GO error rate range {min(stop_rates):.0%}–{max(stop_rates):.0%} (sd {statistics.pstdev(stop_rates)*100:.1f} pts) over a mean-reward range "
             f"{min(means):.3f}–{max(means):.3f} ({(max(means)-min(means))*100:.0f} pts). corr(mean, NO-GO rate) = {corr:+.2f}; "
             f"slope {slope*100:+.1f} NO-GO-rate points per 1.00 of mean, i.e. {slope*(max(means)-min(means))*100:+.1f} pts across the observed range.\n")
    L.append("## E1. NO-GO errors by what the contestant's own numbers said\n")
    L.append("| system | NO-GO wrong | own numbers said NO-GO, went anyway | own numbers said GO | no sc record |")
    L.append("|---|---|---|---|---|")
    for n in names:
        s = out[n]["NO-GO"]; w = s["wrong"]; o = s["own"]
        L.append(f"| {n} | {w} | {o['agree'][1]} ({o['agree'][1]/w:.0%}) | {o['disagree'][1]} ({o['disagree'][1]/w:.0%}) | {o['none'][1]} ({o['none'][1]/w:.0%}) |")
    w = P[("NO-GO", "w")]
    L.append(f"| **pooled** | {w} | {P[('NO-GO','agree','w')]} ({P[('NO-GO','agree','w')]/w:.0%}) | {P[('NO-GO','disagree','w')]} ({P[('NO-GO','disagree','w')]/w:.0%}) | {P[('NO-GO','none','w')]} ({P[('NO-GO','none','w')]/w:.0%}) |\n")
    L.append("Conditional error rates (denominator includes decisions answered correctly):\n")
    L.append("| condition | n | wrong | rate | per-system range |")
    L.append("|---|---|---|---|---|")
    for k in ("NO-GO", "GO"):
        for o in ("agree", "disagree", "none"):
            n_, w_ = P[(k, o, "n")], P[(k, o, "w")]
            rr = [out[n][k]["own"][o][1] / out[n][k]["own"][o][0] for n in names if out[n][k]["own"][o][0]]
            L.append(f"| {decision_label(k)}, own numbers {o} | {n_} | {w_} | {w_/max(n_,1):.0%} | {min(rr):.0%}–{max(rr):.0%} |")
    L.append("\n### E1-strict. Own-number classes with the guard fields checked\n")
    L.append("`agree` only means the branch implied by the reported values equals the reference branch; an unreported guard field evaluates False and falls to the default (often NO-GO) branch. Strict classes: `knew` = every guard field reported AND numerically verified (NF passed); `agree_unverifiable` = reported, field is not a numeric truth; `agree_wrong_value` = reported but failed NF; `agree_unobserved` = branch matched only because a guard field was missing.\n")
    L.append("| class | n | wrong | rate |"); L.append("|---|---|---|---|")
    S = Counter()
    for n in names:
        for k, (t_, w_) in out[n]["strict"].items():
            S[(k, "n")] += t_; S[(k, "w")] += w_
    for k in ("knew", "agree_unverifiable", "agree_wrong_value", "agree_unobserved", "disagree", "none"):
        L.append(f"| {k} | {S[(k,'n')]} | {S[(k,'w')]} | {S[(k,'w')]/max(S[(k,'n')],1):.0%} |")
    O = Counter()
    for n in names:
        for k, v in out[n]["order"].items():
            O[k] += v
    L.append(f"\nStep order among `knew` errors (guard-producing method vs first divergent method): {dict(O)}\n")
    CF = Counter()
    for n in names:
        for k in ("NO-GO", "GO"):
            CF[(k, "n")] += out[n]["confirm"][k][0]; CF[(k, "w")] += out[n]["confirm"][k][1]
    L.append(f"Confirmation forks (`I_confirm`), both sides: NO-GO {CF[('NO-GO','w')]}/{CF[('NO-GO','n')]} wrong, GO {CF[('GO','w')]}/{CF[('GO','n')]} wrong -- the systems take the go-back branch regardless of whether the confirmation succeeded, so this is NOT evidence of outcome judgement.\n")
    LK = Counter(); NC = Counter()
    for n in names:
        for k in ("NO-GO", "GO"):
            LK[(k, "n")] += out[n]["locked"][k][0]; LK[(k, "w")] += out[n]["locked"][k][1]
            NC[(k, "n")] += out[n]["noc31"][k][0]; NC[(k, "w")] += out[n]["noc31"][k][1]
    L.append(f"Locked tasks only (the four unlocked tasks excluded): NO-GO {LK[('NO-GO','w')]}/{LK[('NO-GO','n')]} ({LK[('NO-GO','w')]/LK[('NO-GO','n')]:.0%}), GO {LK[('GO','w')]}/{LK[('GO','n')]} ({LK[('GO','w')]/LK[('GO','n')]:.0%}).")
    L.append(f"Sensitivity, adb_c31 excluded (its narrative was wrong until 2026-09-18): NO-GO {NC[('NO-GO','w')]}/{NC[('NO-GO','n')]} ({NC[('NO-GO','w')]/NC[('NO-GO','n')]:.0%}), GO {NC[('GO','w')]}/{NC[('GO','n')]} ({NC[('GO','w')]/NC[('GO','n')]:.0%}).")
    su = P[("NO-GO", "unknown")]; gu = P[("GO", "unknown")]
    reached_stop_rate = (P[("NO-GO", "w")] - su) / (P[("NO-GO", "n")] - su)
    reached_go_rate = (P[("GO", "w")] - gu) / (P[("GO", "n")] - gu)
    L.append(f"Reached forks only (unknown verdicts excluded): NO-GO {P[('NO-GO','w')]-su}/{P[('NO-GO','n')]-su} ({(P[('NO-GO','w')]-su)/(P[('NO-GO','n')]-su):.0%}), GO {P[('GO','w')]-gu}/{P[('GO','n')]-gu} ({(P[('GO','w')]-gu)/(P[('GO','n')]-gu):.0%}).")
    L.append(f"B-divert attempts that ran any capability method: {sum(out[n]['bcap'] for n in names)}/{sum(out[n]['bdiv'][1] for n in names)}.\n")
    L.append("\n## E2. Matched forks: same case, same node, seeds on both sides\n")
    L.append(f"{len(forks)} graded forks; {len(matched)} carry both NO-GO and GO seeds; {len(stop_only)} are NO-GO-only.\n")
    L.append("| system | NO-GO wrong (matched) | GO wrong (matched) | forks both sides right |")
    L.append("|---|---|---|---|")
    M = Counter()
    for n in names:
        sn = sw = gn = gw = both = nf = 0
        for k, v in matched.items():
            s = [x for x in v["NO-GO"] if x[0] == n]; g = [x for x in v["GO"] if x[0] == n]
            if not s or not g:
                continue
            nf += 1; sn += len(s); sw += sum(x[1] for x in s); gn += len(g); gw += sum(x[1] for x in g)
            both += (not any(x[1] for x in s)) and (not any(x[1] for x in g))
        M.update(sn=sn, sw=sw, gn=gn, gw=gw)
        out[n]["matched"] = (sn, sw, gn, gw, both, nf)
        L.append(f"| {n} | {sw}/{sn} ({sw/sn:.0%}) | {gw}/{gn} ({gw/gn:.0%}) | {both}/{nf} |")
    L.append(f"| **pooled** | {M['sw']}/{M['sn']} ({M['sw']/M['sn']:.0%}) | {M['gw']}/{M['gn']} ({M['gw']/M['gn']:.0%}) | |\n")
    L.append("Per fork, pooled over systems:\n")
    L.append("| case | fork | NO-GO n / wrong | GO n / wrong |"); L.append("|---|---|---|---|")
    for k in sorted(matched):
        v = matched[k]; sn, sw = len(v["NO-GO"]), sum(x[1] for x in v["NO-GO"]); gn, gw = len(v["GO"]), sum(x[1] for x in v["GO"])
        L.append(f"| {k[0]} | {k[1]} | {sn} / {sw} ({sw/sn:.0%}) | {gn} / {gw} ({gw/gn:.0%}) |")
    import random
    order = sorted(names, key=lambda n: -out[n]["mean"])
    rng = random.Random(20260917); cases_ids = sorted({c for n in names for c, _ in out[n]["by_task"].values()})
    boot = []
    for hi, lo in zip(order, order[1:]):
        tasks = sorted(set(out[hi]["by_task"]) & set(out[lo]["by_task"]))
        by_case = defaultdict(list)
        for t in tasks:
            by_case[out[hi]["by_task"][t][0]].append(out[hi]["by_task"][t][1] - out[lo]["by_task"][t][1])
        obs = statistics.fmean(v for vs in by_case.values() for v in vs)
        diffs = []
        for _ in range(4000):
            sample = [v for c in rng.choices(cases_ids, k=len(cases_ids)) for v in by_case.get(c, [])]
            diffs.append(statistics.fmean(sample) if sample else 0.0)
        diffs.sort(); lo_ci, hi_ci = diffs[int(0.025 * len(diffs))], diffs[int(0.975 * len(diffs)) - 1]
        boot.append((hi, lo, obs, lo_ci, hi_ci))
    L.append("\n## Ranking (mean reward, zero rate, tier means, method precision)\n")
    L.append("| system | mean | zero | A-go | B-divert | C-stop | recall | precision |"); L.append("|---|---|---|---|---|---|---|---|")
    for n in order:
        d = out[n]; tm = d["tier_mean"]
        L.append(f"| {n} | {d['mean']:.4f} | {d['zero']:.1%} | {tm['A-proceed']:.3f} | {tm['B-divert']:.3f} | {tm['C-stop']:.3f} | {d['recall']:.3f} | {d['precision']:.3f} |")
    L.append("\nCase-clustered paired bootstrap (4000 resamples of the 15 cases), adjacent pairs in mean order:\n")
    for hi, lo, obs, a_, b_ in boot:
        L.append(f"- {hi} − {lo}: {obs:+.3f} [{a_:+.3f}, {b_:+.3f}]{'' if a_ > 0 or b_ < 0 else '  (not separated)'}")
    n_sep = sum(1 for _, _, _, a_, b_ in boot if a_ > 0 or b_ < 0)
    L.append(f"\n{n_sep} of {len(boot)} adjacent pairs exclude zero.\n")
    L.append("\n## pass^3 (every decision right on all three attempts) / pass@3\n")
    L.append("| system | tier | tasks at k=3 | pass^3 | pass@3 | gap | mean spread |"); L.append("|---|---|---|---|---|---|---|")
    for n in names:
        pk = out[n].get("passk")
        if not pk:
            continue
        for tier in ("A-proceed", "B-divert", "C-stop"):
            b = (pk.get("by_tier") or {}).get(tier) or {}
            e = b.get("eligible") or 0
            if not e or b.get("passk_decisions") is None:
                continue
            p3, pa, sp = b["passk_decisions"], b["pass_at_k_decisions"], b["mean_spread"]
            L.append(f"| {n} | {TIER_SHOW[tier]} | {e} | {p3:.3f} | {pa:.3f} | {pa-p3:.3f} | {sp:.3f} |")
            T_PASSK.append((n, tier, e, p3, pa, sp))
    # ---- scaffold controls (P2), reported apart
    ctl = {}; CTL_MACROS = []
    for name, vendor, k1, _k3 in CONTROLS:
        rows = load_rows(k1)
        if len(rows) != 97:
            L.append(f"\n## Scaffold control: {name} — incomplete ({len(rows)}/97), not reported\n"); continue
        c = Counter(); bdiv = [0, 0]
        cf = defaultdict(lambda: defaultdict(list))
        for r, p, v, own, strict, step_order in decisions(rows, cases):
            kind = "NO-GO" if is_stop(p) else "GO"
            c[(kind, v)] += 1; c[(kind, own, v != "correct")] += 1
            cf[(r["case_id"], p["point_id"])][kind].append(v != "correct")
            DEC[name].append((r["case_id"], (r["case_id"], p["point_id"]), kind, v != "correct"))
        for r in rows:
            pq = (r["card"].get("scorecard") or {}).get("pq") or {}
            if CR._tier(r, shapes) == "B-divert" and int(pq.get("points_total") or 0):
                bdiv[1] += 1; bdiv[0] += float(pq.get("score") or 0) >= 1.0
        c[("both",)] = sum((not any(v["NO-GO"])) and (not any(v["GO"])) for k, v in cf.items() if k in matched)
        c[("go_unknown",)] = c[("GO", "unknown")]
        ctl[name] = (c, bdiv, statistics.fmean(r["reward"] for r in rows))
    if ctl:
        L.append("\n## Scaffold control (P2): instruction states that stopping is a complete answer\n")
        L.append("| system | instruction | mean | NO-GO wrong | GO wrong | GO wrong, fork never reached | own said NO-GO, went | B-divert right | forks both sides right |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        T_CTL = []
        for name, (c, bdiv, mean) in ctl.items():
            base = name.split(" [")[0]
            if base in out:
                d = out[base]; sd, gd = d["NO-GO"], d["GO"]
                L.append(f"| {base} | plain | {d['mean']:.3f} | {sd['wrong']}/{sd['n']} ({sd['wrong']/sd['n']:.0%}) | {gd['wrong']}/{gd['n']} ({gd['wrong']/gd['n']:.0%}) | {gd['unknown']} | {sd['own']['agree'][1]}/{sd['own']['agree'][0]} | {d['bdiv'][0]}/{d['bdiv'][1]} | {d['matched'][4]}/{d['matched'][5]} |")
                T_CTL.append((base, "plain", d["mean"], sd["wrong"], sd["n"], gd["wrong"], gd["n"], gd["unknown"], sd["own"]["agree"][1], sd["own"]["agree"][0], d["bdiv"][0], d["bdiv"][1], d["matched"][4], d["matched"][5]))
            sn = c[("NO-GO","correct")] + c[("NO-GO","incorrect")] + c[("NO-GO","unknown")]; sw = c[("NO-GO","incorrect")] + c[("NO-GO","unknown")]
            gn = c[("GO","correct")] + c[("GO","incorrect")] + c[("GO","unknown")]; gw = c[("GO","incorrect")] + c[("GO","unknown")]
            an = c[("NO-GO","agree",False)] + c[("NO-GO","agree",True)]; aw = c[("NO-GO","agree",True)]
            L.append(f"| {base} | permit-stop | {mean:.3f} | {sw}/{sn} ({sw/max(sn,1):.0%}) | {gw}/{gn} ({gw/max(gn,1):.0%}) | {c[('go_unknown',)]} | {aw}/{an} | {bdiv[0]}/{bdiv[1]} | {c[('both',)]}/{len(matched)} |")
            T_CTL.append((base, "permit-stop", mean, sw, sn, gw, gn, c[("go_unknown",)], aw, an, bdiv[0], bdiv[1], c[("both",)], len(matched)))
        by_sys = {}
        for (b_, ins, mean_, sw, sn, gw, gn, gu, aw, an, b0, b1, both, nm) in T_CTL:
            by_sys.setdefault(b_, {})[ins] = (mean_, sw, sn, gw, gn, aw, an, b0, both, nm)
        rows_ = []
        pairs = [(b_, d_["plain"], d_["permit-stop"]) for b_, d_ in by_sys.items() if "plain" in d_ and "permit-stop" in d_]
        pairs.sort(key=lambda t: -(t[1][1] / t[1][2] - t[2][1] / t[2][2]))   # largest NO-GO-accuracy gain first
        max_drop = max((P_[1] / P_[2] - Q_[1] / Q_[2]) for _, P_, Q_ in pairs) if pairs else 0
        max_gain = max((Q_[8] - P_[8]) for _, P_, Q_ in pairs) if pairs else 0
        for b_, P_, Q_ in pairs:
            drop = P_[1] / P_[2] - Q_[1] / Q_[2]
            sr = lambda X: 1 - X[1] / X[2]; gr = lambda X: 1 - X[3] / X[4]
            rows_.append(f"{logo(out[b_]['vendor']) if b_ in out else ''}{b_} & {B(f'{sr(P_):.0%} $\\rightarrow$ {sr(Q_):.0%}', drop == max_drop)} & {gr(P_):.0%} $\\rightarrow$ {gr(Q_):.0%} "
                         f"& {B(f'{P_[8]} $\\rightarrow$ {Q_[8]}', Q_[8] - P_[8] == max_gain and max_gain > 0)} & {P_[7]} $\\rightarrow$ {Q_[7]} & {P_[0]:.3f} $\\rightarrow$ {Q_[0]:.3f} \\\\")
        # Match Table 2: aligned two-row headings and full text width.
        n_control_diverts = sum(
            1 for (cid_, sd_), sh_ in shapes.items()
            if CR._tier({"shape": sh_, "case_id": cid_, "seed": sd_}, shapes) == "B-divert"
        )
        control_preamble = (
            '{\\footnotesize\\setlength{\\tabcolsep}{4pt}\n'
            '\\begin{tabular*}{\\linewidth}{@{\\extracolsep{\\fill}}lrrrrr@{}}\n'
            '\\toprule\n'
            '\\raisebox{-0.5\\normalbaselineskip}[0pt][0pt]{Agent}\n'
            ' & \\multicolumn{1}{c}{NO-GO right $\\uparrow$}\n'
            ' & \\multicolumn{1}{c}{GO right $\\uparrow$}\n'
            ' & \\multicolumn{1}{c}{Both sides $\\uparrow$}\n'
            ' & \\multicolumn{1}{c}{B-divert $\\uparrow$}\n'
            ' & \\multicolumn{1}{c@{}}{\\raisebox{-0.5\\normalbaselineskip}[0pt][0pt]{Mean reward $\\uparrow$}} \\\\\n'
            ' & \\multicolumn{1}{c}{(\\%)}\n'
            ' & \\multicolumn{1}{c}{(\\%)}\n'
            ' & \\multicolumn{1}{c}{(of ' + str(len(matched)) + ')}\n'
            ' & \\multicolumn{1}{c}{(of ' + str(n_control_diverts) + ')} & \\\\\n'
            '\\midrule\n'
        )
        Path("paper/iclr/tab_control.tex").write_text(
            control_preamble + "\n".join(rows_).replace("%", "\\%")
            + "\n\\bottomrule\n\\end{tabular*}}\n"
        )
        m_ctl_n = len(rows_)
        CTL_MACROS = []
        for (b_, ins, mean_, sw, sn, gw, gn, gu, aw, an, b0, b1, both, nm) in T_CTL:
            key = "".join(ch for ch in b_ if ch.isalpha()) + ("Plain" if ins == "plain" else "Permit")
            CTL_MACROS += [(f"ctl{key}Stop", f"{sw/sn*100:.0f}"), (f"ctl{key}Go", f"{gw/gn*100:.0f}"), (f"ctl{key}Both", f"{both}"), (f"ctl{key}Bdiv", f"{b0}"), (f"ctl{key}Unreached", f"{gu}"),
                           (f"ctl{key}StopRight", f"{(1-sw/sn)*100:.0f}"), (f"ctl{key}GoRight", f"{(1-gw/gn)*100:.0f}")]
    md = "\n".join(L) + "\n"
    print(md)
    if a.md:
        Path(a.md).write_text(md)
    if a.tex:
        T = []
        def m(k, v): T.append(f"\\newcommand{{\\{k}}}{{{v}}}")
        WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        word = lambda k: WORDS[k] if 0 <= k < 10 else str(k)   # ICLR house style: spell out below ten
        m("nSystems", len(names)); m("nVendors", len({out[n]['vendor'] for n in names}))
        m("nSystemsWord", word(len(names))); m("nVendorsWord", word(len({out[n]['vendor'] for n in names})))
        m("stopN", P[("NO-GO", "n")]); m("stopW", P[("NO-GO", "w")]); m("stopRate", f"{P[('NO-GO','w')]/P[('NO-GO','n')]*100:.0f}")
        m("goN", P[("GO", "n")]); m("goW", P[("GO", "w")]); m("goRate", f"{P[('GO','w')]/P[('GO','n')]*100:.0f}")
        m("stopRateMin", f"{min(stop_rates)*100:.0f}"); m("stopRateMax", f"{max(stop_rates)*100:.0f}"); m("stopRateSd", f"{statistics.pstdev(stop_rates)*100:.1f}")
        m("meanMin", f"{min(means):.3f}"); m("meanMax", f"{max(means):.3f}"); m("meanRangePts", f"{(max(means)-min(means))*100:.0f}")
        m("stopMeanCorr", f"{corr:+.2f}"); m("stopSlopePts", f"{slope*(max(means)-min(means))*100:+.1f}")
        # the same over the frontier subset (every vendor but Alibaba): the range the invariance claim is made on
        top = [n for n in names if out[n]["vendor"] != "Alibaba"]
        tm_ = [out[n]["mean"] for n in top]; ts_ = [stop_rates[names.index(n)] for n in top]
        mx_, my_ = statistics.fmean(tm_), statistics.fmean(ts_); sxx_ = sum((x - mx_) ** 2 for x in tm_)
        sl_ = sum((x - mx_) * (y - my_) for x, y in zip(tm_, ts_)) / sxx_ if sxx_ else 0.0
        m("nTop", len(top)); m("nTopWord", word(len(top)))
        m("meanRangePtsTop", f"{(max(tm_)-min(tm_))*100:.0f}"); m("stopSlopePtsTop", f"{sl_*(max(tm_)-min(tm_))*100:+.1f}")
        m("stopMeanCorrTop", f"{statistics.correlation(tm_, ts_):+.2f}" if len(top) > 2 else "")
        m("stopRightMinTop", f"{(1-max(ts_))*100:.0f}"); m("stopRightMaxTop", f"{(1-min(ts_))*100:.0f}")
        low = [n for n in names if n not in top]
        if low:
            m("lowSystems", " and ".join(low)); m("lowMeanGapPts", f"{(min(tm_) - max(out[n]['mean'] for n in low))*100:.0f}")
            m("lowStopRightMax", f"{(1-min(stop_rates[names.index(n)] for n in low))*100:.0f}")
        m("knewW", P[("NO-GO", "agree", "w")]); m("knewPct", f"{P[('NO-GO','agree','w')]/P[('NO-GO','w')]*100:.0f}")
        m("strictKnewN", S[("knew", "n")]); m("strictKnewW", S[("knew", "w")]); m("strictKnewRate", f"{S[('knew','w')]/max(S[('knew','n')],1)*100:.0f}")
        m("strictKnewPct", f"{S[('knew','w')]/P[('NO-GO','w')]*100:.0f}")
        m("unverW", S[("agree_unverifiable", "w")]); m("unverPct", f"{S[('agree_unverifiable','w')]/P[('NO-GO','w')]*100:.0f}")
        m("wrongValW", S[("agree_wrong_value", "w")]); m("wrongValPct", f"{S[('agree_wrong_value','w')]/P[('NO-GO','w')]*100:.0f}")
        m("unobsW", S[("agree_unobserved", "w")]); m("unobsPct", f"{S[('agree_unobserved','w')]/P[('NO-GO','w')]*100:.0f}")
        m("disagreeW", S[("disagree", "w")]); m("disagreePct", f"{S[('disagree','w')]/P[('NO-GO','w')]*100:.0f}")
        m("noneW", S[("none", "w")]); m("nonePct", f"{S[('none','w')]/P[('NO-GO','w')]*100:.0f}")
        m("knewDiagFirst", O.get("diag_first", 0)); m("knewDownstreamFirst", O.get("downstream_first", 0))
        m("confirmStopW", CF[("NO-GO", "w")]); m("confirmStopN", CF[("NO-GO", "n")]); m("confirmGoW", CF[("GO", "w")]); m("confirmGoN", CF[("GO", "n")])
        m("reachedGoRate", f"{reached_go_rate*100:.0f}"); m("reachedStopRate", f"{reached_stop_rate*100:.0f}")
        m("lockedStopRate", f"{LK[('NO-GO','w')]/LK[('NO-GO','n')]*100:.0f}"); m("lockedGoRate", f"{LK[('GO','w')]/LK[('GO','n')]*100:.0f}")
        m("nocStopRate", f"{NC[('NO-GO','w')]/NC[('NO-GO','n')]*100:.0f}"); m("nocGoRate", f"{NC[('GO','w')]/NC[('GO','n')]*100:.0f}")
        m("bdivCap", sum(out[n]["bcap"] for n in names))
        tiers_ = Counter(shapes_t for shapes_t in (CR._tier({"shape": sh, "case_id": cid, "seed": sd}, shapes) for (cid, sd), sh in shapes.items()))
        m("nTierA", tiers_.get("A-proceed", 0)); m("nTierB", tiers_.get("B-divert", 0)); m("nTierC", tiers_.get("C-stop", 0))
        m("nStopTasks", tiers_.get("B-divert", 0) + tiers_.get("C-stop", 0)); m("stopTaskPct", f"{(tiers_.get('B-divert', 0) + tiers_.get('C-stop', 0))/97*100:.0f}")
        m("miscW", P[("NO-GO", "disagree", "w")]); m("miscPct", f"{P[('NO-GO','disagree','w')]/P[('NO-GO','w')]*100:.0f}")
        m("noscW", P[("NO-GO", "none", "w")]); m("noscPct", f"{P[('NO-GO','none','w')]/P[('NO-GO','w')]*100:.0f}")
        m("condStopN", P[("NO-GO", "agree", "n")]); m("condStopRate", f"{P[('NO-GO','agree','w')]/P[('NO-GO','agree','n')]*100:.0f}")
        rr = [out[n]["NO-GO"]["own"]["agree"][1] / out[n]["NO-GO"]["own"]["agree"][0] for n in names]
        m("condStopMin", f"{min(rr)*100:.0f}"); m("condStopMax", f"{max(rr)*100:.0f}")
        m("condGoN", P[("GO", "agree", "n")]); m("condGoRate", f"{P[('GO','agree','w')]/P[('GO','agree','n')]*100:.0f}")
        m("nForks", len(forks)); m("nMatched", len(matched)); m("nStopOnly", len(stop_only))
        m("mStopW", M["sw"]); m("mStopN", M["sn"]); m("mStopRate", f"{M['sw']/M['sn']*100:.0f}")
        m("mGoW", M["gw"]); m("mGoN", M["gn"]); m("mGoRate", f"{M['gw']/M['gn']*100:.0f}")
        m("bdivRight", sum(out[n]["bdiv"][0] for n in names)); m("bdivN", sum(out[n]["bdiv"][1] for n in names))
        m("goUnreached", P[("GO", "unknown")]); m("stopUnreached", P[("NO-GO", "unknown")])
        for k_, v_ in CTL_MACROS:
            m(k_, v_)
        n_ctl = len([1 for b_, d_ in ({} if not ctl else by_sys).items() if "permit-stop" in d_]) if ctl else 0
        m("nControls", n_ctl); m("nControlsWord", word(n_ctl))
        if ctl:
            drops = []
            for b_, d_ in by_sys.items():
                if "plain" in d_ and "permit-stop" in d_:
                    P_, Q_ = d_["plain"], d_["permit-stop"]
                    drops.append((P_[1] / P_[2] - Q_[1] / Q_[2], b_, P_[1] / P_[2], Q_[1] / Q_[2], P_[8], Q_[8], P_[7], Q_[7]))
            drops.sort(reverse=True)
            for tag, dd in (("Max", drops[0]), ("Min", drops[-1])):
                m(f"ctl{tag}DropSys", dd[1]); m(f"ctl{tag}DropFrom", f"{dd[2]*100:.0f}"); m(f"ctl{tag}DropTo", f"{dd[3]*100:.0f}")
                m(f"ctl{tag}RightFrom", f"{(1-dd[2])*100:.0f}"); m(f"ctl{tag}RightTo", f"{(1-dd[3])*100:.0f}")
                m(f"ctl{tag}DropBothFrom", dd[4]); m(f"ctl{tag}DropBothTo", dd[5]); m(f"ctl{tag}DropPts", f"{dd[0]*100:.0f}")
            m("ctlNoMove", sum(1 for dd in drops if abs(dd[0]) < 0.03)); m("ctlBigMove", sum(1 for dd in drops if dd[0] >= 0.15))
            m("ctlBothUp", sum(1 for dd in drops if dd[5] > dd[4]))
        for n_, tier, e, p3, pa, sp in T_PASSK:
            key = "".join(ch for ch in n_ + tier if ch.isalpha())
            m("pk" + key + "Three", f"{p3:.3f}"); m("pk" + key + "At", f"{pa:.3f}"); m("pk" + key + "Spread", f"{sp:.3f}")
        bd_ = [(p3, n_) for n_, tier, e, p3, pa, sp in T_PASSK if tier == "B-divert"]
        if bd_:
            mx = max(bd_); m("pkBdivThreeMax", f"{mx[0]:.3f}"); m("pkBdivThreeMaxSys", mx[1])
            m("pkBdivZeroCount", sum(1 for p3, _ in bd_ if p3 == 0)); m("pkSystemsThree", len(bd_))
        m("nAdjacent", len(boot)); m("nAdjacentSep", n_sep)
        # accuracy forms (100 - error) so the prose can read higher-is-better
        # ---- case-clustered bootstrap intervals (2026-09-19 review: uncertainty over the 15 cases,
        # not over systems or decisions). 4000 draws, seed fixed; rates as accuracy in percent.
        import random as _rnd
        _cases = sorted({d[0] for n_ in names for d in DEC[n_]})
        def _rate(recs, kind, only_matched=False):
            sel = [d for d in recs if d[2] == kind and (not only_matched or d[1] in matched)]
            return (1 - sum(d[3] for d in sel) / len(sel)) if sel else None
        def _boot(fn, B_=4000, seed=20260919):
            rng_ = _rnd.Random(seed); vals = []
            for _ in range(B_):
                draw = rng_.choices(_cases, k=len(_cases))
                v = fn(draw)
                if v is not None: vals.append(v)
            vals.sort(); return vals[int(0.025*len(vals))], vals[int(0.975*len(vals))-1]
        main_recs = [d for n_ in names for d in DEC[n_]]
        def _by_case(recs):
            bc = defaultdict(list)
            for d in recs: bc[d[0]].append(d)
            return bc
        MBC = _by_case(main_recs)
        def _pooled(draw, kind, only_matched=False):
            return _rate([d for c_ in draw for d in MBC.get(c_, [])], kind, only_matched)
        for key, fn in (("stopRightCI", lambda dr: _pooled(dr, "NO-GO")),
                        ("goRightCI", lambda dr: _pooled(dr, "GO")),
                        ("mStopRightCI", lambda dr: _pooled(dr, "NO-GO", True)),
                        ("mGoRightCI", lambda dr: _pooled(dr, "GO", True)),
                        ("mGapCI", lambda dr: (lambda g_, s_: None if g_ is None or s_ is None else g_ - s_)(_pooled(dr, "GO", True), _pooled(dr, "NO-GO", True)))):
            lo_, hi_ = _boot(fn); m(key, f"{lo_*100:.0f}--{hi_*100:.0f}")
        for name_ in ctl:
            base_ = name_.split(" [")[0]
            if base_ not in out: continue
            PB, CB = _by_case(DEC[base_]), _by_case(DEC[name_])
            key_ = "".join(ch for ch in base_ if ch.isalpha())
            for kind_ in ("NO-GO", "GO"):
                def _delta(dr, kind_=kind_):
                    a_ = _rate([d for c_ in dr for d in CB.get(c_, [])], kind_); b_ = _rate([d for c_ in dr for d in PB.get(c_, [])], kind_)
                    return None if a_ is None or b_ is None else a_ - b_
                lo_, hi_ = _boot(_delta); m(f"ctl{key_}{'Stop' if kind_ == 'NO-GO' else 'Go'}DeltaCI", f"{lo_*100:+.0f} to {hi_*100:+.0f}")
        same_ = tie_ = rev_ = 0
        for k_, v_ in matched.items():
            se_ = sum(x[1] for x in v_["NO-GO"]) / len(v_["NO-GO"]); ge_ = sum(x[1] for x in v_["GO"]) / len(v_["GO"])
            same_ += se_ > ge_; tie_ += se_ == ge_; rev_ += se_ < ge_
        m("nForkSame", same_); m("nForkTie", tie_); m("nForkRev", rev_)
        m("stopRight", f"{100 - P[('NO-GO','w')]/P[('NO-GO','n')]*100:.0f}"); m("goRight", f"{100 - P[('GO','w')]/P[('GO','n')]*100:.0f}")
        m("stopRightMin", f"{(1-max(stop_rates))*100:.0f}"); m("stopRightMax", f"{(1-min(stop_rates))*100:.0f}")
        m("mStopRight", f"{100 - M['sw']/M['sn']*100:.0f}"); m("mGoRight", f"{100 - M['gw']/M['gn']*100:.0f}")
        m("reachedGoRight", f"{(1-reached_go_rate)*100:.0f}"); m("reachedStopRight", f"{(1-reached_stop_rate)*100:.0f}")
        m("lockedStopRight", f"{100 - LK[('NO-GO','w')]/LK[('NO-GO','n')]*100:.0f}"); m("lockedGoRight", f"{100 - LK[('GO','w')]/LK[('GO','n')]*100:.0f}")
        m("nocStopRight", f"{100 - NC[('NO-GO','w')]/NC[('NO-GO','n')]*100:.0f}"); m("nocGoRight", f"{100 - NC[('GO','w')]/NC[('GO','n')]*100:.0f}")
        m("strictKnewStopped", S[("knew", "n")] - S[("knew", "w")]); m("strictKnewStopRate", f"{(1 - S[('knew','w')]/max(S[('knew','n')],1))*100:.0f}")
        m("condStopRight", f"{100 - P[('NO-GO','agree','w')]/P[('NO-GO','agree','n')]*100:.0f}"); m("condGoRight", f"{100 - P[('GO','agree','w')]/P[('GO','agree','n')]*100:.0f}")
        rec = sorted(out[n]["recall"] for n in names)
        m("recallMin", f"{rec[0]:.3f}"); m("recallSecond", f"{rec[1]:.3f}"); m("recallMax", f"{rec[-1]:.3f}")
        m("nTrials", sum(out[n]["n_trials"] for n in names))
        m("improveN", CF[("NO-GO", "n")]); m("improveW", CF[("NO-GO", "w")])   # retained for old text; see confirmGo*
        m("meanTop", f"{out[order[0]]['mean']:.3f}"); m("meanBottom", f"{out[order[-1]]['mean']:.3f}")
        atts_ = [out[n]["att"] for n in names if out[n]["att"]]
        m("nAttMulti", len(atts_)); m("nAttMultiWord", word(len(atts_)))
        m("nAttThree", sum(1 for a_ in atts_ if a_["k"] >= 3)); m("nAttThreeWord", word(sum(1 for a_ in atts_ if a_["k"] >= 3)))
        m("attSdMeanMax", f"{max(a_['mean_sd'] for a_ in atts_):.3f}"); m("attSdStopMax", f"{max(a_['nogo_sd'] for a_ in atts_):.1f}")
        m("attSdGoMax", f"{max(a_['go_sd'] for a_ in atts_):.1f}")
        m("attSingle", ", ".join(n for n in order if not out[n]["att"]))
        m("topSystem", order[0]); m("bottomSystem", order[-1])
        m("condStopMinSys", min(names, key=lambda n: out[n]["NO-GO"]["own"]["agree"][1] / out[n]["NO-GO"]["own"]["agree"][0]))
        tex_dir = Path(a.tex).parent
        body = []
        # Reported as ACCURACY (higher is better) so every column reads the same way.
        acc = lambda blk: (blk["n"] - blk["wrong"]) / blk["n"]
        rep_stop = lambda n: out[n]["att"]["nogo"] / 100 if out[n]["att"] else acc(out[n]["NO-GO"])
        rep_go = lambda n: out[n]["att"]["go"] / 100 if out[n]["att"] else acc(out[n]["GO"])
        best_stop = max(rep_stop(n) for n in order)
        best_go = max(rep_go(n) for n in order)
        def pm(val, sd_, fmt, single):
            return f"{fmt(val)}$^\\ddagger$" if single else f"{fmt(val)}\\,$\\pm$\\,{fmt(sd_)}"
        best_bd = max(out[n]["bdiv"][0] for n in order)
        kacc = lambda n: (out[n]["strict"].get("knew", (0, 0))[0] - out[n]["strict"].get("knew", (0, 0))[1]) / max(out[n]["strict"].get("knew", (0, 0))[0], 1)
        best_kn = max(kacc(n) for n in order)
        # Table 2 order: mean reward, best first (rank column = this order).
        t2_order = list(order)
        for n in t2_order:
            d = out[n]; sd, gd = d["NO-GO"], d["GO"]
            kn = d["strict"].get("knew", (0, 0)); ks = kn[0] - kn[1]
            rank_ = order.index(n) + 1
            at = d["att"]; single = not at
            mean_cell = pm(d["mean"], at["mean_sd"] if at else 0, lambda x: f"{x:.3f}", single)
            stop_cell = pm(rep_stop(n) * 100, at["nogo_sd"] if at else 0, lambda x: f"{x:.0f}", single) + "\\%"
            go_cell = pm(rep_go(n) * 100, at["go_sd"] if at else 0, lambda x: f"{x:.0f}", single) + "\\%"
            body.append(f"{logo(d['vendor'])}{n} & {B(mean_cell, n == order[0])} & "
                        f"{B(stop_cell, rep_stop(n) == best_stop)} & "
                        f"{B(go_cell, rep_go(n) == best_go)} & "
                        f"{B(f'{ks}/{kn[0]}', kacc(n) == best_kn and best_kn > 0)} & "
                        f"{B(f'{d['bdiv'][0]}/{d['bdiv'][1]}', d['bdiv'][0] == best_bd and best_bd > 0)} & {rank_} \\\\")
        n_bd = sum(1 for (cid_, sd_), sh_ in shapes.items() if CR._tier({"shape": sh_, "case_id": cid_, "seed": sd_}, shapes) == "B-divert")
        anchor = [("Human black belts$^\\dagger$ & --- & by constr. & by constr. & --- & --- & --- \\\\"),
                  (f"Reference solution & 1.000 & 100\\% & 100\\% & --- & {n_bd}/{n_bd} & --- \\\\"), "\\midrule"]
        body = anchor + body
        wrap = lambda spec, head, rows: ("\\begin{tabular}{" + spec + "}\n\\toprule\n" + head + " \\\\\n\\midrule\n"
                                         + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")
        # Two aligned header rows; fill the text width without scaling the data.
        restraint_preamble = (
            '\\setlength{\\tabcolsep}{4pt}\n'
            '\\begin{tabular*}{\\linewidth}{@{\\extracolsep{\\fill}}lrrrrrr@{}}\n'
            '\\toprule\n'
            '\\raisebox{-0.5\\normalbaselineskip}[0pt][0pt]{Agent}\n'
            ' & \\multicolumn{1}{c}{\\raisebox{-0.5\\normalbaselineskip}[0pt][0pt]{Mean reward $\\uparrow$}}\n'
            ' & \\multicolumn{1}{c}{NO-GO right $\\uparrow$}\n'
            ' & \\multicolumn{1}{c}{GO right $\\uparrow$}\n'
            ' & \\multicolumn{1}{c}{Stopped $\\uparrow$}\n'
            ' & \\multicolumn{1}{c}{B-divert $\\uparrow$}\n'
            ' & \\multicolumn{1}{c@{}}{\\raisebox{-0.5\\normalbaselineskip}[0pt][0pt]{Rank}} \\\\\n'
            ' & & \\multicolumn{1}{c}{(of 52)}\n'
            ' & \\multicolumn{1}{c}{(of 248)}\n'
            ' & \\multicolumn{1}{c}{(of verified)}\n'
            ' & \\multicolumn{1}{c}{(of 18)} & \\\\\n'
            '\\midrule\n'
        )
        (tex_dir / "tab_restraint.tex").write_text(
            restraint_preamble + "\n".join(body) + "\n\\bottomrule\n\\end{tabular*}\n"
        )
        body = []
        bm = max(out[n]["mean"] for n in order); bz = min(out[n]["zero"] for n in order)
        bt = {t: max(out[n]["tier_mean"][t] for n in order) for t in ("A-proceed", "B-divert", "C-stop")}
        br = max(out[n]["recall"] for n in order); bp = max(out[n]["precision"] for n in order)
        for n in order:
            d = out[n]; tm = d["tier_mean"]
            mean_cell = pm(d["mean"], d["att"]["mean_sd"] if d["att"] else 0, lambda x: f"{x:.3f}", not d["att"])
            body.append(f"{n} & {B(mean_cell, d['mean'] == bm)} & {B(f'{d['zero']*100:.1f}\\%', d['zero'] == bz)} & "
                        f"{B(f'{tm['A-proceed']:.3f}', tm['A-proceed'] == bt['A-proceed'])} & {B(f'{tm['B-divert']:.3f}', tm['B-divert'] == bt['B-divert'])} & "
                        f"{B(f'{tm['C-stop']:.3f}', tm['C-stop'] == bt['C-stop'])} & {B(f'{d['recall']:.3f}', d['recall'] == br)} & {B(f'{d['precision']:.3f}', d['precision'] == bp)} \\\\")
        (tex_dir / "tab_ranking.tex").write_text(
            '\\setlength{\\tabcolsep}{3pt}\n\\begin{tabular*}{\\linewidth}{@{\\extracolsep{\\fill}}lrrrrrrr@{}}\n\\toprule\n\\thead{Agent} & \\multicolumn{1}{c}{\\thead{Mean reward\\\\$\\uparrow$}} & \\multicolumn{1}{c}{\\thead{Zero score\\\\(\\%) $\\downarrow$}} & \\multicolumn{1}{c}{\\thead{A-go\\\\$\\uparrow$}} & \\multicolumn{1}{c}{\\thead{B-divert\\\\$\\uparrow$}} & \\multicolumn{1}{c}{\\thead{C-stop\\\\$\\uparrow$}} & \\multicolumn{1}{c}{\\thead{Recall\\\\$\\uparrow$}} & \\multicolumn{1}{c@{}}{\\thead{Precision\\\\$\\uparrow$}} \\\\\n\\midrule\n'
            + "\n".join(body) + "\n\\bottomrule\n\\end{tabular*}\n")
        body = []
        for n in order:
            sn, sw, gn, gw, both, nf = out[n]["matched"]
            body.append(f"{n} & {sw}/{sn} ({sw/sn:.0%}) & {gw}/{gn} ({gw/gn:.0%}) & {both}/{nf} \\\\")
        (tex_dir / "tab_matched.tex").write_text(wrap("@{}lrrr@{}",
            " & NO-GO wrong & GO wrong & forks both sides right", [b.replace("%", "\\%") for b in body]))
        body = [f"{hi} $-$ {lo} & ${obs:+.3f}$ & $[{a_:+.3f}, {b_:+.3f}]$ & {'yes' if (a_ > 0 or b_ < 0) else 'no'} \\\\" for hi, lo, obs, a_, b_ in boot]
        (tex_dir / "tab_boot.tex").write_text(wrap("@{}lrrl@{}", "pair & difference & 95\\% CI & separated", body))
        body = []; last = None
        best3 = {t: max(x[3] for x in T_PASSK if x[1] == t) for t in {x[1] for x in T_PASSK}}
        bestat = {t: max(x[4] for x in T_PASSK if x[1] == t) for t in {x[1] for x in T_PASSK}}
        for n_, tier, e, p3, pa, sp in T_PASSK:
            lab = n_ if n_ != last else ""; last = n_
            body.append(f"{lab} & {TIER_SHOW[tier]} & {e} & {B(f'{p3:.3f}', p3 == best3[tier] and p3 > 0)} & {B(f'{pa:.3f}', pa == bestat[tier] and pa > 0)} & {pa-p3:.3f} & {sp:.3f} \\\\")
        # Keep a system's three tiers together while allowing page breaks between systems.
        pass_head = ("\\toprule\n"
                     "Agent & Tier & Tasks & pass$^3$ $\\uparrow$ & pass@3 $\\uparrow$ & Gap $\\downarrow$ & Mean spread $\\downarrow$ \\\\\n"
                     "\\midrule\n")
        pass_rows = [row + ("*" if i + 1 < len(body) and body[i + 1].startswith(" &") else "")
                     for i, row in enumerate(body)]
        (tex_dir / "tab_passk.tex").write_text(
            "\\begin{longtable}{@{}llrrrrr@{}}\n"
            "\\caption{Reliability across three attempts, by agent and routing tier.}\\label{tab:passk}\\\\\n"
            + pass_head + '\\endfirsthead\n\\multicolumn{7}{c}{\\normalfont\\normalsize Table \\thetable{} (continued)} \\\\\n\\noalign{\\vskip 6pt}\n' + pass_head + "\\endhead\n"
            "\\midrule\n\\endfoot\n\\bottomrule\n\\endlastfoot\n"
            + "\n".join(pass_rows) + "\n\\end{longtable}\n")
        Path(a.tex).write_text("% generated by scripts/restraint_analysis.py -- do not edit\n" + "\n".join(T) + "\n")
    json.dump({n: {k: v for k, v in d.items() if k != "passk"} for n, d in out.items()},
              open("docs/result_restraint.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
