#!/usr/bin/env python3
"""The replicated instruction control (pre-registered in docs/control_pairs_2026-09-19.json).

Two systems x five instruction conditions x 32 paired tasks x three attempts (the fifth,
*remind*, is the steward stating on declaration whether a handbook precondition holds). For every
(system, condition): route NO-GO/GO accuracy over all attempts, forks never reached on the
proceed side, both-sides-right pairs per attempt, and within-task disagreement across the
three attempts; deltas against the plain condition with a paired bootstrap over the 16
pairs' cases. Writes paper/iclr/tab_ctlrep.tex and paper/iclr/ctlrep.tex.
Also exports the figure's numeric source and exploratory remind-minus-normative
contrasts; these contrasts were added after the registered campaigns were complete.
"""
import json, sys, random, statistics, collections
from pathlib import Path
sys.path[:0] = ['.', 'harbor/src']
from scripts import restraint_analysis as R
from dmaic_harbor import campaign_report as CR
from dmaic_harbor import v2_tasks as V

SYSTEMS = [("GPT-6-astra", "astra"), ("DeepSeek-v4-pro", "dsv4")]
CONDS = [("plain", "plain"), ("permit-stop", "permit"), ("permit-paraphrase", "paraphrase"), ("normative", "normative"), ("remind", "remind")]
PAIRS = json.load(open('docs/control_pairs_2026-09-19.json'))
STOP_TASKS = {(p['case'], p['seed']): p for p in PAIRS['pairs']}
TWIN_OF = {(p['case'], p['twin_seed']): (p['case'], p['seed']) for p in PAIRS['pairs']}
cases = V.discover()

def load_all(job):
    """Every attempt (no first-wins dedupe), over the job dir and its -fill* continuations."""
    import glob as _g
    rows = []
    for d in sorted(_g.glob(str(R.JOBS / job)) + _g.glob(str(R.JOBS / (job + "-fill*")))):
        d = R.JOBS / pathlib_name(d)
        for r in CR._rows(d):
            r["job_dir"] = d; rows.append(r)
    return [r for r in rows if r["agent"] not in ("oracle", "nop")]
def pathlib_name(p):
    from pathlib import Path
    return Path(p).name

def analyse(job):
    rows = load_all(job)
    if not rows: return None
    per = collections.defaultdict(list)       # (task, attempt_idx) -> [(kind, wrong, fork, verdict)]
    att = collections.defaultdict(int)
    order = {}
    for r in rows:
        key = (r["case_id"], int(r["seed"]))
        idx = att[key]; att[key] += 1; order[(key, idx)] = r["trial"]
    recs = []
    for r, p, v, own, strict, step_order in R.decisions(rows, cases):
        kind = "NO-GO" if R.is_stop(p) else "GO"
        recs.append(dict(case=r["case_id"], seed=int(r["seed"]), trial=r["trial"], fork=(r["case_id"], p["point_id"]),
                         kind=kind, wrong=(v != "correct"), verdict=v))
    return rows, recs, att

def rates(recs):
    st = [x for x in recs if x["kind"] == "NO-GO"]; go = [x for x in recs if x["kind"] == "GO"]
    return dict(stop_n=len(st), stop_right=(1 - sum(x["wrong"] for x in st) / len(st)) if st else None,
                go_n=len(go), go_right=(1 - sum(x["wrong"] for x in go) / len(go)) if go else None,
                go_unreached=sum(1 for x in go if x["verdict"] == "unknown"))

def both_sides(recs, rows_by_trial):
    """Per attempt index, the number of the 16 pairs where the stop seed's stop fork AND the twin's
    same fork were both right in that attempt."""
    # attempt index per (task): order trials by name within task
    by_task = collections.defaultdict(list)
    for x in recs: by_task[(x["case"], x["seed"])].append(x)
    trials_per_task = {t: sorted({x["trial"] for x in xs}) for t, xs in by_task.items()}
    out = []
    for k in range(3):
        n = 0
        for (case, seed), pr in STOP_TASKS.items():
            fork = (case, pr["fork"])
            s_tr = trials_per_task.get((case, seed), []); t_tr = trials_per_task.get((case, pr["twin_seed"]), [])
            if k >= len(s_tr) or k >= len(t_tr): continue
            s_ok = any(x["fork"] == fork and not x["wrong"] for x in by_task[(case, seed)] if x["trial"] == s_tr[k])
            t_ok = any(x["fork"] == fork and not x["wrong"] for x in by_task[(case, pr["twin_seed"])] if x["trial"] == t_tr[k])
            n += s_ok and t_ok
        out.append(n)
    return out

def disagreement(recs):
    """Share of (task, fork) with three attempts whose three verdicts are not all equal."""
    g = collections.defaultdict(list)
    for x in recs: g[(x["case"], x["seed"], x["fork"])].append(x["wrong"])
    full = [v for v in g.values() if len(v) >= 3]
    return (sum(1 for v in full if len(set(v[:3])) > 1) / len(full)) if full else None, len(full)

def boot_delta(a, b, kind, B=4000, seed=20260919):
    rng = random.Random(seed); cs = sorted({x["case"] for x in a + b}); vals = []
    def rate(recs, draw):
        sel = [x for c in draw for x in recs if x["case"] == c and x["kind"] == kind]
        return (1 - sum(x["wrong"] for x in sel) / len(sel)) if sel else None
    for _ in range(B):
        d = rng.choices(cs, k=len(cs)); ra, rb = rate(a, d), rate(b, d)
        if ra is not None and rb is not None: vals.append(ra - rb)
    vals.sort(); return (vals[int(0.025*len(vals))], vals[int(0.975*len(vals))-1]) if vals else (None, None)

res = {}
for sysname, tag in SYSTEMS:
    for cname, ctag in CONDS:
        got = analyse(f"ctl-{tag}-{cname}")
        if got is None: continue
        rows, recs, att = got
        expected_tasks = set(STOP_TASKS) | set(TWIN_OF)
        assert set(att) == expected_tasks, (sysname, cname, "task coverage")
        assert len(rows) == 96 and all(n == 3 for n in att.values()), (sysname, cname, "attempt coverage")
        rt = rates(recs); bs = both_sides(recs, None); dis, nfull = disagreement(recs)
        res[(sysname, cname)] = dict(rt, trials=len(rows), tasks=len(att), attempts_per_task=statistics.fmean(att.values()) if att else 0,
                                     both=bs, disagree=dis, disagree_n=nfull, recs=recs)
lines = ['\\setlength{\\tabcolsep}{3pt}', '\\begin{tabular*}{\\linewidth}{@{\\extracolsep{\\fill}}lrrrrr@{}}', '\\toprule', '\\thead{Condition} & \\multicolumn{1}{c}{\\thead{Trials}} & \\multicolumn{1}{c}{\\thead{NO-GO right\\\\change; 95\\% CI}} & \\multicolumn{1}{c}{\\thead{GO right\\\\change; 95\\% CI}} & \\multicolumn{1}{c}{\\thead{Both sides\\\\of 16 / attempt}} & \\multicolumn{1}{c@{}}{\\thead{Within-task\\\\disagreement}} \\\\', '\\midrule']
macros = []
for sysname, tag in SYSTEMS:
    base = res.get((sysname, "plain"))
    if any((sysname, cname) in res for cname, _ in CONDS):
        if lines[-1] != '\\midrule':
            lines.append('\\midrule')
        lines.append('\\multicolumn{6}{@{}l}{\\textbf{' + sysname + '}} \\\\')
    for cname, ctag in CONDS:
        d = res.get((sysname, cname))
        if not d: continue
        key = "".join(ch for ch in sysname if ch.isalpha()) + ctag.title()
        sr = f"{d['stop_right']*100:.0f}\\%" if d['stop_right'] is not None else "--"
        gr = f"{d['go_right']*100:.0f}\\%" if d['go_right'] is not None else "--"
        bsx = "/".join(str(b) for b in d['both']) if d['both'] else "--"
        dg = f"{d['disagree']*100:.0f}\\%" if d['disagree'] is not None else "--"
        delta = ""; gdelta = ""
        if base and cname != "plain" and d['stop_right'] is not None:
            lo, hi = boot_delta(d['recs'], base['recs'], "NO-GO")
            if lo is not None: delta = f" ({(d['stop_right']-base['stop_right'])*100:+.0f}; {lo*100:+.0f} to {hi*100:+.0f})"
            macros.append(f"\\newcommand{{\\rep{key}StopDelta}}{{{(d['stop_right']-base['stop_right'])*100:+.0f}}}")
            macros.append(f"\\newcommand{{\\rep{key}StopDeltaCI}}{{{lo*100:+.0f} to {hi*100:+.0f}}}" if lo is not None else "")
            glo, ghi = boot_delta(d['recs'], base['recs'], "GO")
            if glo is not None and d['go_right'] is not None and base['go_right'] is not None:
                gdelta = f" ({(d['go_right']-base['go_right'])*100:+.0f}; {glo*100:+.0f} to {ghi*100:+.0f})"
                macros.append(f"\\newcommand{{\\rep{key}GoDelta}}{{{(d['go_right']-base['go_right'])*100:+.0f}}}")
                macros.append(f"\\newcommand{{\\rep{key}GoDeltaCI}}{{{glo*100:+.0f} to {ghi*100:+.0f}}}")
        stop_cell = r"\tcellr{" + sr + r"\\" + delta.strip() + "}" if delta else sr
        go_cell = r"\tcellr{" + gr + r"\\" + gdelta.strip() + "}" if gdelta else gr
        lines.append(f"{cname} & {d['trials']} & {stop_cell} & {go_cell} & {bsx} & {dg} \\\\")
        macros.append(f"\\newcommand{{\\rep{key}StopRight}}{{{d['stop_right']*100:.0f}}}" if d['stop_right'] is not None else "")
        macros.append(f"\\newcommand{{\\rep{key}GoRight}}{{{d['go_right']*100:.0f}}}" if d['go_right'] is not None else "")
        macros.append(f"\\newcommand{{\\rep{key}Trials}}{{{d['trials']}}}")
lines += ["\\bottomrule", "\\end{tabular*}"]

# The original table compares every condition with plain. A direct contrast is
# required to assess the additional runtime channel on top of the normative rule.
# Retain all attempts and resample the same cases on both sides of the contrast.
direct_contrasts = {}
for sysname, tag in SYSTEMS:
    a, b = res[(sysname, "remind")], res[(sysname, "normative")]
    key = "".join(ch for ch in sysname if ch.isalpha())
    direct_contrasts[sysname] = {}
    for kind, rate_key, macro_key in (("NO-GO", "stop_right", "Stop"), ("GO", "go_right", "Go")):
        lo, hi = boot_delta(a["recs"], b["recs"], kind)
        delta = a[rate_key] - b[rate_key]
        direct_contrasts[sysname][kind] = dict(
            delta_pp=100 * delta,
            ci95_case_clustered_pp=[100 * lo, 100 * hi],
            case_clusters=len({r["case"] for r in a["recs"] + b["recs"]}),
        )
        prefix = f"rep{key}RemindVsNormative{macro_key}"
        macros += [f"\\newcommand{{\\{prefix}Delta}}{{{delta * 100:+.0f}}}",
                   f"\\newcommand{{\\{prefix}DeltaCI}}{{{lo * 100:+.0f} to {hi * 100:+.0f}}}"]

# --- the remind condition's mechanism: did the agent declare, and did the reminder fire?
import glob as _glob
for sysname, tag in SYSTEMS:
    key = "".join(ch for ch in sysname if ch.isalpha())
    files = _glob.glob(f"harbor/jobs/ctl-{tag}-remind/dmaic-*/artifacts/steward-audit.jsonl")
    if not files:
        continue
    n = declared = fired = held = 0; total = 0
    for f in files:
        ev = [json.loads(l) for l in open(f) if l.strip()]
        n += 1
        ds = [e for e in ev if e.get("action") == "declare"]
        declared += bool(ds); total += len(ds)
        states = [v for e in ds for v in (e.get("preconditions") or {}).values()]
        fired += any(v is False for v in states); held += any(v is True for v in states)
    macros += [f"\\newcommand{{\\rem{key}Trials}}{{{n}}}",
               f"\\newcommand{{\\rem{key}DeclaredPct}}{{{100*declared/n:.0f}}}",
               f"\\newcommand{{\\rem{key}DeclaresPerTrial}}{{{total/n:.1f}}}",
               f"\\newcommand{{\\rem{key}Fired}}{{{fired}}}",
               f"\\newcommand{{\\rem{key}Held}}{{{held}}}"]
    print(f"remind mechanism {sysname}: trials {n}, declared>=1 {declared}, mean declares {total/n:.1f}, fired {fired}, held {held}")
Path("paper/iclr/tab_ctlrep.tex").write_text("\n".join(lines) + "\n")
Path("paper/iclr/ctlrep.tex").write_text("% generated by scripts/control_replicated.py\n" + "\n".join(m for m in macros if m) + "\n")
summary_path = Path("output/research/control-replication-20260922.json")
summary_path.parent.mkdir(parents=True, exist_ok=True)
summary_path.write_text(json.dumps({
    "source": "Retained harbor/jobs/ctl-* trial artifacts, scored by scripts/restraint_analysis.py",
    "design": "docs/control_pairs_2026-09-19.json",
    "bootstrap": {"unit": "case", "paired": True, "draws": 4000, "seed": 20260919},
    "conditions": [c for c, _ in CONDS],
    "systems": {sysname: {c: {k: v for k, v in res[(sysname, c)].items() if k != "recs"}
                           for c, _ in CONDS} for sysname, _ in SYSTEMS},
    "exploratory_remind_minus_normative": direct_contrasts,
}, indent=2) + "\n")
print("Exploratory remind-minus-normative contrasts:", json.dumps(direct_contrasts))
for k, d in res.items():
    print(k, {x: d[x] for x in ('trials','tasks','stop_n','stop_right','go_n','go_right','go_unreached','both','disagree','disagree_n')})
