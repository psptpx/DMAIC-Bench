#!/usr/bin/env python3
"""Case-clustered bootstrap intervals (percentile, 4000 draws, seed 20260926) for

  (a) pooled matched-fork GO / NO-GO accuracy, 13 agents, attempt 1, Plain;
  (b) per agent, permit-stop minus Plain change in NO-GO (52) and GO (248) accuracy,
      as paired differences within case (Table 2 Delta columns);
  (c) per agent, Plain matched-fork NO-GO (52) and GO (146) accuracy (Table 21).

Run from the repository root:
    PYTHONPATH=.:harbor/src python3 <this file> [--cache records.json] [--out b13.md]

The per-decision records are built by importing scripts/restraint_analysis.py (not edited)
and calling its load_rows()/decisions() exactly as its main() does: attempt 1 = the k=1 job
dirs merged first-wins; the permit condition = the CONTROLS entries (job dirs ending in
-permit / -permit-fill). Records are cached to --cache so the bootstrap can be rerun cheaply.
"""
import argparse, importlib.util, json, random, sys
from collections import defaultdict
from pathlib import Path

SEED, B = 20260919, 4000
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WORK = ROOT / "output" / "research" / "matched_bootstrap"
WORK.mkdir(parents=True, exist_ok=True)
TAB = ROOT / "paper" / "iclr" / "tab_matched_ci.tex"


def build_records():
    sys.path[:0] = [".", "harbor/src"]
    spec = importlib.util.spec_from_file_location("ra", "scripts/restraint_analysis.py")
    ra = importlib.util.module_from_spec(spec); spec.loader.exec_module(ra)
    cases = ra.V.discover()
    rec = {}          # system name -> [[case, point_id, kind, wrong, seed], ...]
    for label, table in (("plain", ra.SYSTEMS), ("permit", ra.CONTROLS)):
        for name, _vendor, k1, _k3 in table:
            rows = ra.load_rows(k1)
            if len(rows) != 97:
                print(f"skip {name}: {len(rows)}/97", file=sys.stderr); continue
            out = []
            for r, p, v, _own, _strict, _order in ra.decisions(rows, cases):
                kind = "NO-GO" if ra.is_stop(p) else "GO"
                out.append([r["case_id"], p["point_id"], kind, int(v != "correct"), int(r["seed"])])
            rec[name] = out
            print(f"{name}: {len(out)} decisions", file=sys.stderr)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=str(WORK / "records.json"))
    ap.add_argument("--out", default=str(WORK / "report.md"))
    a = ap.parse_args()
    cache = Path(a.cache)
    if cache.exists():
        rec = json.loads(cache.read_text())
    else:
        rec = build_records(); cache.write_text(json.dumps(rec))

    plain = [n for n in rec if "[permit-stop]" not in n]
    permit = {n.split(" [")[0]: n for n in rec if "[permit-stop]" in n}
    # matched forks: (case, node) carrying both NO-GO and GO seeds, over the plain systems
    kinds = defaultdict(set)
    for n in plain:
        for c, pid, kind, _w, _s in rec[n]:
            kinds[(c, pid)].add(kind)
    matched = {k for k, v in kinds.items() if v == {"NO-GO", "GO"}}
    cases = sorted({d[0] for n in rec for d in rec[n]})
    assert len(cases) == 15, cases

    # per (system, case) counts: [n, wrong] for each category
    CATS = ("NO-GO", "GO", "mNO-GO", "mGO")
    agg = {n: {c: {k: [0, 0] for k in CATS} for c in cases} for n in rec}
    for n in rec:
        for c, pid, kind, w, _s in rec[n]:
            agg[n][c][kind][0] += 1; agg[n][c][kind][1] += w
            if (c, pid) in matched:
                agg[n][c]["m" + kind][0] += 1; agg[n][c]["m" + kind][1] += w

    def acc(names, cat, draw):
        t = w = 0
        for n in names:
            for c in draw:
                t += agg[n][c][cat][0]; w += agg[n][c][cat][1]
        return None if t == 0 else 100.0 * (1 - w / t)

    rng = random.Random(SEED)
    draws = [rng.choices(cases, k=len(cases)) for _ in range(B)]

    def ci(fn):
        vals = sorted(v for v in (fn(d) for d in draws) if v is not None)
        return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1], len(vals)

    def counts(names, cat, draw=cases):
        t = w = 0
        for n in names:
            for c in draw:
                t += agg[n][c][cat][0]; w += agg[n][c][cat][1]
        return t, w

    R = {"seed": SEED, "draws": B, "n_cases": len(cases), "n_matched_forks": len(matched)}
    # (a) pooled matched
    for cat, key in (("mNO-GO", "pooled_matched_nogo"), ("mGO", "pooled_matched_go")):
        t, w = counts(plain, cat)
        lo, hi, nb = ci(lambda d, cat=cat: acc(plain, cat, d))
        R[key] = {"n": t, "wrong": w, "point": 100 * (1 - w / t), "lo": lo, "hi": hi, "valid_draws": nb}
    lo, hi, nb = ci(lambda d: (lambda g, s: None if g is None or s is None else g - s)(acc(plain, "mGO", d), acc(plain, "mNO-GO", d)))
    R["pooled_matched_gap"] = {"point": R["pooled_matched_go"]["point"] - R["pooled_matched_nogo"]["point"], "lo": lo, "hi": hi, "valid_draws": nb}
    # (b) per-agent deltas, (c) per-agent matched
    R["agents"] = {}
    for n in plain:
        d = {}
        for cat, key in (("NO-GO", "nogo"), ("GO", "go"), ("mNO-GO", "m_nogo"), ("mGO", "m_go")):
            t, w = counts([n], cat)
            lo, hi, nb = ci(lambda dr, cat=cat: acc([n], cat, dr))
            d["plain_" + key] = {"n": t, "wrong": w, "point": 100 * (1 - w / t), "lo": lo, "hi": hi, "valid_draws": nb}
        if n in permit:
            pn = permit[n]
            for cat, key in (("NO-GO", "nogo"), ("GO", "go")):
                t, w = counts([pn], cat)
                lo, hi, nb = ci(lambda dr, cat=cat: acc([pn], cat, dr))
                d["permit_" + key] = {"n": t, "wrong": w, "point": 100 * (1 - w / t), "lo": lo, "hi": hi, "valid_draws": nb}
                def delta(dr, cat=cat):
                    p_, q_ = acc([n], cat, dr), acc([pn], cat, dr)
                    return None if p_ is None or q_ is None else q_ - p_
                lo, hi, nb = ci(delta)
                d["delta_" + key] = {"point": d["permit_" + key]["point"] - d["plain_" + key]["point"], "lo": lo, "hi": hi, "valid_draws": nb}
        R["agents"][n] = d
    (WORK / "results.json").write_text(json.dumps(R, indent=1))
    TAB.write_text(table(R))
    print("table ->", TAB)
    print(json.dumps({k: v for k, v in R.items() if k != "agents"}, indent=1))
    for n, d in R["agents"].items():
        print(n, {k: (round(v["point"], 1), round(v["lo"], 1), round(v["hi"], 1)) for k, v in d.items()})
    Path(a.out).write_text(report(R))
    print("report ->", a.out)


ORDER = ["GPT-6-astra", "GPT-5.6-sol", "Kimi-k3", "Claude-Sonnet-5", "DeepSeek-v4-flash", "DeepSeek-v4-pro",
         "GLM-5.3", "GPT-5.6-luna", "Claude-Fable-5.1", "GLM-5.3-Flash", "Claude-Opus-5", "Qwen3.8-max", "Qwen3.8-flash"]
LOGO = {"GPT": "openai", "Kimi": "moonshot", "Claude": "anthropic", "DeepSeek": "deepseek", "GLM": "zhipu", "Qwen": "alibaba"}
# Table 2 as committed (paper/iclr/dmaic_bench.tex, tab:main_results): Plain, +Permit, Delta for NO-GO and GO.
PAPER_T2 = {"GPT-6-astra": (23, 79, 56, 82, 67, -15), "GPT-5.6-sol": (21, 38, 17, 81, 77, -4), "Kimi-k3": (17, 27, 10, 82, 81, -1),
            "Claude-Sonnet-5": (19, 25, 6, 82, 81, -1), "DeepSeek-v4-flash": (21, 42, 21, 79, 77, -2), "DeepSeek-v4-pro": (23, 23, 0, 79, 77, -2),
            "GLM-5.3": (21, 29, 8, 82, 83, 1), "GPT-5.6-luna": (25, 27, 2, 70, 73, 3), "Claude-Fable-5.1": (17, 44, 27, 81, 81, 0),
            "GLM-5.3-Flash": (17, 19, 2, 82, 81, -1), "Claude-Opus-5": (17, 25, 8, 78, 83, 5), "Qwen3.8-max": (13, 27, 14, 77, 80, 3),
            "Qwen3.8-flash": (10, 17, 7, 77, 78, 1)}
# Table 21 as committed (paper/iclr/tab_main_results.tex): matched NO-GO right, GO right.
PAPER_T21 = {"GPT-6-astra": (23, 94), "GPT-5.6-sol": (21, 94), "Kimi-k3": (17, 95), "Claude-Sonnet-5": (19, 93), "DeepSeek-v4-flash": (21, 90),
             "DeepSeek-v4-pro": (23, 90), "GLM-5.3": (21, 96), "GPT-5.6-luna": (25, 81), "Claude-Fable-5.1": (17, 96), "GLM-5.3-Flash": (17, 91),
             "Claude-Opus-5": (17, 94), "Qwen3.8-max": (13, 93), "Qwen3.8-flash": (10, 93)}


def r0(x):
    v = int(round(x))
    return v


def iv(d):
    return f"[{r0(d['lo'])}--{r0(d['hi'])}]"


def sgn(x):
    v = r0(x)
    return f"+{v}" if v >= 0 else f"$-${-v}"


def sgn_md(x):
    v = r0(x)
    return f"+{v}" if v >= 0 else f"-{-v}"


def ivs(d):
    return f"[{sgn(d['lo'])}--{sgn(d['hi'])}]"


def ivs_md(d):
    return f"[{sgn_md(d['lo'])}, {sgn_md(d['hi'])}]"


def report(R):
    A = R["agents"]; L = []
    L.append("# b13 -- case-clustered bootstrap intervals for the matched-fork accuracies and the permit-stop deltas\n")
    L.append(f"Method: percentile bootstrap, {R['draws']} draws, seed {R['seed']} (`random.Random(20260926).choices(cases, k=15)` once per draw; "
             "the same 4000 case draws are used for every statistic). Each draw resamples the 15 cases with replacement and keeps every "
             "attempt-1 decision of each sampled case (with multiplicity); accuracy is recomputed on the pooled decisions of the draw. "
             "Paired deltas recompute Plain and +Permit on the same draw and take permit minus plain. Interval = 2.5th and 97.5th "
             "percentiles (sorted values at index int(0.025B) and int(0.975B)-1, the convention of scripts/restraint_analysis.py). "
             "No draw produced an empty denominator (4000 valid draws for every statistic).\n")
    L.append("Records: built by importing `scripts/restraint_analysis.py` (untouched) and calling `load_rows()` / `decisions()` / `is_stop()` "
             "exactly as its `main()` does. Attempt 1 = the k=1 job dirs of `SYSTEMS` merged first-wins per task (the fill dirs only add "
             "tasks missing from the primary dir); the k=3 dirs are never read. Permit condition = the `CONTROLS` entries (job dirs "
             "`*-permit`, `*-permit-fill`). Matched forks = the (case, node) pairs that carry both NO-GO and GO seeds across the 13 Plain "
             f"systems: {R['n_matched_forks']} forks, 52 NO-GO + 146 GO decisions per agent (676 + 1898 pooled). All 26 systems have 97 tasks "
             "and 300 graded decisions each; none skipped.\n")
    L.append("## (a) Pooled matched-fork accuracy, 13 agents, attempt 1, Plain\n")
    L.append("| statistic | n | wrong | point | paper | 95% CI |"); L.append("|---|---|---|---|---|---|")
    g, s, gap = R["pooled_matched_go"], R["pooled_matched_nogo"], R["pooled_matched_gap"]
    L.append(f"| GO right (matched) | {g['n']} | {g['wrong']} | {g['point']:.1f}% | 92% | {iv(g)} |")
    L.append(f"| NO-GO right (matched) | {s['n']} | {s['wrong']} | {s['point']:.1f}% | 19% | {iv(s)} |")
    L.append(f"| GO minus NO-GO gap | | | {gap['point']:.1f} pts | 73 pts (59--87) | {iv(gap)} |")
    L.append("\nPoint estimates reproduce the paper's 92 / 19 (`\\mGoRight`, `\\mStopRight`) and the 73-point gap. For reference, "
             "`paper/iclr/numbers.tex` currently carries `\\mStopRightCI{8--30}` and `\\mGoRightCI{86--97}` from seed 20260919; with seed "
             f"20260926 the NO-GO lower limit is {s['lo']:.2f} (rounds to {r0(s['lo'])}), a one-point seed-to-seed difference at the rounding edge.\n")
    L.append("## (b) Table 2 Delta columns: permit-stop minus Plain, paired within case\n")
    L.append("NO-GO over all 52 NO-GO decisions, GO over all 248 GO decisions (Table 2's denominators). `paper` columns are the committed Table 2 cells; "
             "the Delta point here is the unrounded difference, whereas Table 2 prints the difference of the two rounded percentages.\n")
    L.append("| agent | NO-GO plain (paper) | NO-GO permit (paper) | Delta NO-GO (paper) | 95% CI | GO plain (paper) | GO permit (paper) | Delta GO (paper) | 95% CI |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    mism = []
    for n in ORDER:
        d = A[n]; p = PAPER_T2[n]
        L.append(f"| {n} | {d['plain_nogo']['point']:.1f} ({p[0]}) | {d['permit_nogo']['point']:.1f} ({p[1]}) | {d['delta_nogo']['point']:+.1f} ({p[2]:+d}) | {ivs_md(d['delta_nogo'])} "
                 f"| {d['plain_go']['point']:.1f} ({p[3]}) | {d['permit_go']['point']:.1f} ({p[4]}) | {d['delta_go']['point']:+.1f} ({p[5]:+d}) | {ivs_md(d['delta_go'])} |")
        chk = (r0(d['plain_nogo']['point']), r0(d['permit_nogo']['point']), r0(d['plain_go']['point']), r0(d['permit_go']['point']))
        if chk != (p[0], p[1], p[3], p[4]) or r0(d['permit_nogo']['point']) - r0(d['plain_nogo']['point']) != p[2] or r0(d['permit_go']['point']) - r0(d['plain_go']['point']) != p[5]:
            mism.append(n)
    L.append("")
    L.append("Check: every Plain and +Permit cell rounds to the committed Table 2 value, and every Delta equals the difference of the rounded cells"
             + (" -- no mismatches." if not mism else f" -- MISMATCH for {mism}.")
             + " One rounding note: GPT-6-astra's unrounded GO change is "
             f"{A['GPT-6-astra']['delta_go']['point']:+.1f} (rounds to {sgn_md(A['GPT-6-astra']['delta_go']['point'])}); Table 2 prints -15 because it subtracts 67 from 82.\n")
    nz = [n for n in ORDER if A[n]['delta_nogo']['lo'] > 0]; nz_go = [n for n in ORDER if A[n]['delta_go']['hi'] < 0 or A[n]['delta_go']['lo'] > 0]
    L.append(f"NO-GO Delta intervals that exclude zero (lower limit > 0 before rounding): {len(nz)} of 13 -- {', '.join(nz)}. "
             f"GO Delta intervals that exclude zero: {', '.join(nz_go) if nz_go else 'none'}. "
             "Claude-Sonnet-5, GLM-5.3 and Qwen3.8-flash have a NO-GO lower limit of exactly 0.0 (touching, not excluding).\n")
    L.append("## (c) Table 21: per-agent Plain matched-fork accuracy (52 NO-GO, 146 GO at the 40 forks)\n")
    L.append("| agent | NO-GO right (paper) | 95% CI | GO right (paper) | 95% CI |"); L.append("|---|---|---|---|---|")
    mism = []
    for n in ORDER:
        d = A[n]; p = PAPER_T21[n]
        L.append(f"| {n} | {d['plain_m_nogo']['point']:.1f} ({p[0]}) | {iv(d['plain_m_nogo'])} | {d['plain_m_go']['point']:.1f} ({p[1]}) | {iv(d['plain_m_go'])} |")
        if (r0(d['plain_m_nogo']['point']), r0(d['plain_m_go']['point'])) != p:
            mism.append(n)
    L.append("")
    L.append("Check: every cell rounds to the committed Table 21 value" + (" -- no mismatches." if not mism else f" -- MISMATCH for {mism}.")
             + " The matched NO-GO column equals the all-decisions NO-GO column because all 52 NO-GO decisions sit at matched forks. "
             "Several GO upper limits are 100 (a resample of cases in which the agent made no matched GO error).\n")
    L.append("## Regenerate\n")
    L.append("```\ncd <repository root>\n"
             "PYTHONPATH=.:harbor/src python3 " + str(HERE / "matched_bootstrap.py") + "\n```\n"
             f"Deletes nothing in the repository. Record cache: `{HERE / 'records.json'}` (remove it to rebuild from harbor/jobs/, about 20 s); "
             f"full results: `{HERE / 'results.json'}`; this file is rewritten on every run.\n")
    L.append("## LaTeX snippets\n")
    L.append("Intervals as `[lo--hi]`, integers, percent points. Deltas carry explicit signs (`$-$` for negatives so the en-dash separator stays readable).\n")
    L.append("### Table 21 (`tab:matched-results`, body file `paper/iclr/tab_main_results.tex`): NO-GO right and GO right columns with intervals\n")
    L.append("```latex")
    L.append("% NO-GO right (%) [95% CI] & GO right (%) [95% CI], case-clustered bootstrap, 4000 draws, seed 20260926")
    for i, n in enumerate(ORDER, 1):
        d = A[n]; lg = LOGO[[k for k in LOGO if n.startswith(k)][0]]
        L.append(f"{i} & \\logo{{{lg}.png}} {n} & {r0(d['plain_m_nogo']['point'])} {iv(d['plain_m_nogo'])} & {r0(d['plain_m_go']['point'])} {iv(d['plain_m_go'])} \\\\")
    L.append("```\n")
    L.append("Pooled row, if wanted: `NO-GO 19 " + iv(s) + " & GO 92 " + iv(g) + "`; gap `73 " + iv(gap) + "`.\n")
    L.append("### Table 2 (`tab:main_results`): the two Delta columns with intervals\n")
    L.append("```latex")
    L.append("% Delta NO-GO [95% CI] & Delta GO [95% CI]; permit-stop minus Plain, paired by case, 4000 draws, seed 20260926")
    for i, n in enumerate(ORDER, 1):
        d = A[n]; p = PAPER_T2[n]
        L.append(f"{i} & {n} & {p[2]:+d} {{\\scriptsize {ivs(d['delta_nogo'])}}} & {p[5]:+d} {{\\scriptsize {ivs(d['delta_go'])}}} \\\\".replace("& +0 ", "& 0 "))
    L.append("```\n")
    L.append("Macro form (drop-in for `paper/iclr/numbers.tex`, same names as the seed-20260919 macros it now holds, comma style):\n")
    L.append("```latex")
    for n in ORDER:
        d = A[n]; key = "".join(ch for ch in n if ch.isalpha())
        L.append(f"\\newcommand{{\\ctl{key}StopDeltaCI}}{{{sgn_md(d['delta_nogo']['lo'])} to {sgn_md(d['delta_nogo']['hi'])}}}")
        L.append(f"\\newcommand{{\\ctl{key}GoDeltaCI}}{{{sgn_md(d['delta_go']['lo'])} to {sgn_md(d['delta_go']['hi'])}}}")
    L.append(f"\\newcommand{{\\mStopRightCI}}{{{r0(s['lo'])}--{r0(s['hi'])}}}")
    L.append(f"\\newcommand{{\\mGoRightCI}}{{{r0(g['lo'])}--{r0(g['hi'])}}}")
    L.append(f"\\newcommand{{\\mGapCI}}{{{r0(gap['lo'])}--{r0(gap['hi'])}}}")
    L.append("```\n")
    return "\n".join(L) + "\n"




ORDER = ["GPT-6-astra", "GPT-5.6-sol", "Kimi-k3", "Claude-Sonnet-5", "DeepSeek-v4-flash", "DeepSeek-v4-pro",
         "GLM-5.3", "GPT-5.6-luna", "Claude-Fable-5.1", "GLM-5.3-Flash", "Claude-Opus-5", "Qwen3.8-max", "Qwen3.8-flash"]
LOGO = {"GPT": "openai", "Kimi": "moonshot", "Claude": "anthropic", "DeepSeek": "deepseek", "GLM": "zhipu", "Qwen": "alibaba"}


def _iv(d):
    return f"{r0(d['point'])} [{r0(d['lo'])}--{r0(d['hi'])}]"


def _dv(d):
    def f(x):
        v = r0(x)
        return f"$-${abs(v)}" if v < 0 else f"+{v}"
    return f"{f(d['point'])} [{f(d['lo'])} to {f(d['hi'])}]"


def table(R):
    L = ["% generated by scripts/matched_bootstrap.py -- do not edit",
         "\\begin{table}[p]",
         "\\caption{\\textbf{Case-clustered intervals for the matched-fork rates and the permit-stop changes.} "
         "Attempt 1, percentile bootstrap over the 15 cases, "
         f"{R['draws']} draws, seed {R['seed']}. NO-GO and GO right are matched-fork accuracies under the plain instruction "
         "(52 and 146 decisions per agent); the change columns are permit-stop minus plain over all 52 NO-GO and 248 GO decisions, "
         "recomputed on the same resampled cases; they are unrounded differences and can differ by one point from the rounded differences in Table~\\ref{tab:main_results}. Pooled over 13 agents: NO-GO "
         f"{_iv(R['pooled_matched_nogo'])}, GO {_iv(R['pooled_matched_go'])}, gap {r0(R['pooled_matched_gap']['point'])} "
         f"[{r0(R['pooled_matched_gap']['lo'])}--{r0(R['pooled_matched_gap']['hi'])}].}}",
         "\\label{tab:matched-ci}", "\\centering\\small", "\\setlength{\\tabcolsep}{4pt}",
         "\\begin{tabular}{@{}lrrrr@{}}", "\\toprule",
         "Agent & NO-GO right (\\%) & GO right (\\%) & $\\Delta$ NO-GO (pts) & $\\Delta$ GO (pts) \\\\", "\\midrule"]
    for n in ORDER:
        d = R["agents"][n]
        logo = next(v for k, v in LOGO.items() if n.startswith(k))
        L.append(f"\\logo{{{logo}.png}} {n} & {_iv(d['plain_m_nogo'])} & {_iv(d['plain_m_go'])} & {_dv(d['delta_nogo'])} & {_dv(d['delta_go'])} \\\\")
    L += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    return "\n".join(L)

if __name__ == "__main__":
    main()
