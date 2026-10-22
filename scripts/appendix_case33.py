#!/usr/bin/env python3
"""Appendix F material for case 33: the case graph, two timelines of one system (GPT-6-astra)
on seed 2 (the full walk) and seed 3 (the walk that must stop), and the two reports in full.

    python3 scripts/appendix_case33.py

Reads harbor/jobs/gpt6astra-97 (plain) and gpt6astra-97-permit; writes
paper/iclr/figures/figure09_case33_routes.pdf (Graphviz), paper/iclr/tab_c33_timeline.tex and
paper/iclr/lst_c33_reports.tex. Node membership of each trace step is the case's own
(method, batch) pairing (Table nodes of case 33); guard verdicts are evaluated on the
run's reported values with the guards of the case.
"""
import glob, json
from pathlib import Path
from listing_layout import reflow_latex_listings

OUT = Path("paper/iclr")
JOB = {"plain": "harbor/jobs/gpt6astra-97", "permit": "harbor/jobs/gpt6astra-97-permit"}


def trial(job, seed):
    d = glob.glob(f"{JOB[job]}/dmaic-adb_c33-t3-s{seed}-clean__*/")[0]
    audit = [json.loads(l) for l in open(d + "artifacts/steward-audit.jsonl")]
    trace = json.load(open(d + "artifacts/trace.json"))
    card = json.load(open(d + "verifier-rescored/scorecard.json"))["scorecard"]
    reward = json.load(open(d + "verifier-rescored/reward.json"))["reward"]
    report = open(d + "artifacts/report.md").read()
    res = json.load(open(d + "result.json"))
    return dict(dir=d, audit=audit, trace=trace, card=card, reward=reward, report=report, res=res)


# ---- the case (mirrors Tables nodes/edges of case 33) ---------------------------------------
NODE_OF = {("meta.data_profiling", "define"): "D_scope",
           ("msa.attribute_agreement", "study_1"): "M_agree1",
           ("quality.pareto", "disagreements"): "M_disagree",
           ("msa.attribute_agreement", "study_2"): "M_agree2",
           ("control_chart.p", "lots"): "M_pchart",
           ("capability.binomial", "lots"): "A_cap",
           ("basic.two_proportions", "heads"): "A_root_cause"}
GUARD = {"M_agree1": ("$\\kappa_1 \\geq 0.60$", "kappaMin", lambda v: v >= 0.60, "M_pchart", "M_disagree"),
         "M_agree2": ("$\\kappa_2 \\geq 0.60$", "kappaMin", lambda v: v >= 0.60, "M_pchart", "M_escalate"),
         "M_pchart": ("OOC $= 0$", "outOfControlCount", lambda v: v == 0, "A_cap", "A_special_cause"),
         "A_cap": ("$\\bar p \\leq 0.02$", "avgP", lambda v: v <= 0.02, "C_control", "A_root_cause")}
NEXT = {"D_scope": "M_agree1", "M_disagree": "M_agree2", "A_root_cause": "I_improve (terminal), then C_control"}
LABEL = {"msa.attribute_agreement": "attribute agreement", "quality.pareto": "Pareto of disagreements",
         "control_chart.p": "$p$ chart", "capability.binomial": "binomial capability",
         "basic.one_proportion": "one-proportion test", "basic.two_proportions": "two-proportion test",
         "meta.data_profiling": "read the charter"}


def esc(s):
    return s.replace("_", "\\_").replace("%", "\\%").replace("&", "\\&")


def value_text(step):
    o = step["outputs"] or {}
    m = step["method_id"]
    if m == "msa.attribute_agreement":
        return f"$\\kappa_{{\\min}}$ {o['kappaMin']:.4f}, agreement {o['agreementPct']:.2f}\\%"
    if m == "quality.pareto":
        return f"top category {o['topCategoryPct']:.2f}\\%"
    if m == "control_chart.p":
        return f"CL {o['centerLine']:.4f}, out of limits {o['outOfControlCount']}"
    if m == "capability.binomial":
        return f"$\\bar p$ {o['avgP']:.4f}, $Z$ {o['processZ']:.3f}"
    if m == "basic.one_proportion":
        return f"$p$ = {o['pValue']:.1e}".replace("e-", "e$-$")
    if m == "basic.two_proportions":
        return f"{o['head1Pct']:.2f}\\% vs {o['head2Pct']:.2f}\\%, $p$ = {o['pValue']:.2g}"
    if m == "meta.data_profiling":
        return "required share 0.02" if o.get("requiredRejectShare") else "profile"
    return ""


def batch_of(step):
    d = step.get("inputs_digest") or {}
    return d.get("source") or d.get("batch") or (d.get("batches") or [""])[0]


def audit_index(audit, batch):
    for a in audit:
        if a.get("action") == "request" and a.get("outcome") == "data" and a.get("stage_id") == batch:
            return a["seq"]
    return None


def timeline_rows(t, stop_after=None):
    """Rows: step, node, batch (audit #), analysis, value, guard reading, route."""
    rows = []
    seen_batches = set()
    pq = {d["point_id"]: d for d in t["card"]["pq"]["details"]}
    route_open = True
    for i, s in enumerate(t["trace"]["steps"], 1):
        b = batch_of(s)
        node = NODE_OF.get((s["method_id"], b))
        idx = audit_index(t["audit"], b)
        bcell = f"\\texttt{{{esc(b)}}} (\\#{idx})" if b and b not in seen_batches and idx else (f"\\texttt{{{esc(b)}}}" if b else "---")
        seen_batches.add(b)
        analysis = LABEL.get(s["method_id"], s["method_id"])
        val = value_text(s)
        guard = route = ""
        if node in GUARD and route_open:
            expr, key, fn, yes, no = GUARD[node]
            v = s["outputs"][key]
            holds = fn(v)
            guard = f"{expr}: {'holds' if holds else 'fails'}"
            target = yes if holds else no
            verdict = pq.get(node, {}).get("verdict")
            if verdict == "incorrect":
                route = f"correct: $\\to$ {esc(target)}, the project ends; taken: went on $\\times$"
            else:
                route = f"$\\to$ {esc(target)}" + (" \\checkmark" if verdict == "correct" else "")
        elif node in NEXT and route_open:
            route = f"$\\to$ {esc(NEXT[node])}"
        elif not route_open:
            guard = "---"; route = "\\emph{past the closed fork}"
        elif node is None:
            route = "\\emph{off route}"
        rows.append((i, esc(node) if node else "---", bcell, analysis, val, guard, route))
        if stop_after and node == stop_after:
            route_open = False
    return rows


def write_timeline(t2, t3):
    L = [
        '% generated by scripts/appendix_case33.py',
        '\\setlength{\\tabcolsep}{2pt}',
        '\\begin{longtable}{@{}R{0.04\\linewidth}P{0.13\\linewidth}P{0.16\\linewidth}P{0.14\\linewidth}P{0.17\\linewidth}P{0.16\\linewidth}P{0.135\\linewidth}@{}}',
        '\\caption{GPT-6-astra on case 33, seeds 2 and 3, under the plain instruction (first attempt). Trace steps list released batches, reported values, guards and branches. \\checkmark: correct fork; $\\times$: incorrect fork.}\\label{tab:c33-timeline}\\\\',
        '\\toprule',
        'Step & Node & Batch (steward \\#) & Analysis & Reported value & Guard read on it & Route taken \\\\',
        '\\endfirsthead',
        '\\multicolumn{7}{c}{\\normalfont\\normalsize Table \\thetable{} (continued)} \\\\',
        '\\noalign{\\vskip 6pt}',
        '\\toprule',
        'Step & Node & Batch (steward \\#) & Analysis & Reported value & Guard read on it & Route taken \\\\',
        '\\midrule',
        '\\endhead',
        '\\bottomrule',
        '\\endfoot',
    ]
    def block(title, rows, foot):
        L.append("\\midrule")
        L.append(f"\\multicolumn{{7}}{{@{{}}l}}{{\\textbf{{{title}}}}} \\\\*")
        L.append("\\midrule")
        for r in rows:
            L.append(" & ".join(str(x) for x in r) + " \\\\")
    def stats(t):
        a = t["audit"]; n_req = sum(x["action"] == "request" and x["outcome"] == "data" for x in a)
        n_ref = sum(x["outcome"] == "refused" for x in a)
        st = t["res"]["started_at"][11:19]; en = t["res"]["finished_at"][11:19]
        secs = (int(en[0:2]) * 3600 + int(en[3:5]) * 60 + int(en[6:8])) - (int(st[0:2]) * 3600 + int(st[3:5]) * 60 + int(st[6:8]))
        ms = t["card"]["ms"]; pq = t["card"]["pq"]
        return (f"{len(a)} steward interactions ({n_req} batches released, {n_ref} refused), "
                f"{len(t['trace']['steps'])} trace steps, {t['report'].count(chr(10)) + 1} report lines, "
                f"{secs // 60} min {secs % 60} s wall clock; pq {pq['points_correct']}/{pq['points_total']}, "
                f"ms\\_precision {ms['precision']:.3f}, reward {t['reward']:.3f}.")
    block("Seed 2: the study fails, the repair holds, the level is missed --- the full walk (tier A)",
          timeline_rows(t2), stats(t2))
    block("Seed 3: the study fails, the repair fails --- the walk that must stop (tier C)",
          timeline_rows(t3, stop_after="M_agree2"), stats(t3))
    L += ["\\end{longtable}",
          r"\par\normalsize\noindent\textbf{Run accounting.} Seed 2: " + stats(t2)
          + r"\par\noindent Seed 3: " + stats(t3) + r"\par"]
    (OUT / "tab_c33_timeline.tex").write_text("\n".join(L) + "\n")


def write_graph():
    """The case graph, hand-laid: the main line left to right, terminals and the divert node
    off it. Shared prefix purple, seed-2 walk blue, seed-3 no-go red, unused edges grey, the
    seed-3 run's continuation red dashed."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    plt.rcParams.update({"font.family": "Helvetica", "pdf.fonttype": 42})
    W, H = 5.5, 2.05
    fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    col = lambda c: 0.30 + c * 0.6125
    Y0, YU, YD = 1.08, 1.70, 0.46
    pos = {"D_scope": (col(0), Y0), "M_agree1": (col(1), Y0), "M_disagree": (col(2), Y0), "M_agree2": (col(3), Y0),
           "M_pchart": (col(4), Y0), "A_cap": (col(5), Y0), "A_root_cause": (col(6), Y0), "I_improve": (col(7), Y0),
           "C_control": (col(8), Y0), "M_escalate": (col(4), YD), "A_special_cause": (col(5), YU)}
    phase = {"D": "#ececec", "M": "#d6e6f5", "A": "#fbe3d3", "I": "#dff0da", "C": "#e8dff2"}
    bw, bh = 0.46, 0.21
    for n, (x, y) in pos.items():
        term = n in ("M_escalate", "I_improve")
        w = max(bw, 0.075 + 0.037 * len(n))          # long names get a wider box
        if term:
            ax.add_patch(FancyBboxPatch((x - w / 2 - 0.025, y - bh / 2 - 0.025), w + 0.05, bh + 0.05, boxstyle="round,pad=0.01,rounding_size=0.05", fc="none", ec="#333333", lw=0.6))
        ax.add_patch(FancyBboxPatch((x - w / 2, y - bh / 2), w, bh, boxstyle="round,pad=0.01,rounding_size=0.05", fc=phase[n[0]], ec="#333333", lw=0.6))
        ax.text(x, y, n, ha="center", va="center", fontsize=4.8)
    def edge(a, b, color, lw, label="", style="-", rad=0.0, lab_dy=0.05, lab_dx=0.0, shrink=18):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=6, color=color, lw=lw,
                                     linestyle=style, connectionstyle=f"arc3,rad={rad}", shrinkA=shrink, shrinkB=shrink, zorder=3))
        if label:
            mx, my = (x1 + x2) / 2 + lab_dx, (y1 + y2) / 2 + lab_dy
            # offset the label along the arc's bulge
            if rad:
                dx, dy = x2 - x1, y2 - y1
                mx += rad * dy * 0.5; my += -rad * dx * 0.5
            ax.text(mx, my, label, ha="center", va="center", fontsize=4.6, color="#222222",
                    bbox=dict(fc="white", ec="none", pad=0.4), zorder=4)
    P, B, R, G = "#4a2d82", "#1f5fa8", "#b3261e", "#9a9a9a"
    edge("D_scope", "M_agree1", P, 1.8)
    edge("M_agree1", "M_disagree", P, 1.8, "default", lab_dy=-0.165)
    edge("M_disagree", "M_agree2", P, 1.8)
    edge("M_agree2", "M_pchart", B, 1.8, r"$\kappa_2 \geq 0.60$", lab_dy=0.165)
    edge("M_pchart", "A_cap", B, 1.8, "OOC = 0", lab_dy=0.165)
    edge("A_cap", "A_root_cause", B, 1.8, "default", lab_dy=0.165)
    edge("A_root_cause", "I_improve", B, 1.8)
    edge("I_improve", "C_control", B, 1.8)
    edge("M_agree2", "M_escalate", R, 1.8, "default", lab_dy=0.0, lab_dx=-0.17)
    edge("M_agree1", "M_pchart", G, 0.7, r"$\kappa_1 \geq 0.60$", rad=-0.34)
    edge("M_pchart", "A_special_cause", G, 0.7, "default", lab_dx=-0.17, lab_dy=0.04)
    edge("A_special_cause", "C_control", G, 0.7, rad=-0.22)
    edge("A_cap", "C_control", G, 0.7, r"$\bar p \leq 0.02$", rad=0.34)
    for a, b in (("M_agree2", "M_pchart"), ("M_pchart", "A_cap"), ("A_cap", "A_root_cause")):
        edge(a, b, R, 1.0, style=(0, (3, 2)), rad=0.7, shrink=11)
    # legend
    ly = 0.10; lx = 0.10
    for text, color, style in (("both routes", P, "-"), ("seed 2, the full walk", B, "-"), ("seed 3, the no-go", R, "-"),
                               ("the seed-3 run's continuation", R, (0, (3, 2))), ("edges no seed took", G, "-")):
        ax.plot([lx, lx + 0.2], [ly, ly], color=color, lw=1.6 if color != G else 0.7, linestyle=style)
        ax.text(lx + 0.24, ly, text, va="center", fontsize=4.8, color="#222222")
        lx += 0.24 + 0.029 * len(text) + 0.11
    ax.text(lx, ly, "double border: terminal", va="center", fontsize=4.8, color="#222222")
    (OUT / "figures").mkdir(exist_ok=True)
    fig.savefig(OUT / "figures" / "figure09_case33_routes.pdf")
    fig.savefig(OUT / "figures" / "figure09_case33_routes.png", dpi=300)


KEEP_KEYS = ("kappaMin", "agreementPct", "topCategoryPct", "centerLine", "outOfControlCount", "avgP",
             "processZ", "pValue", "zStatistic", "head1Pct", "head2Pct")


def _abridge_commands(ks):
    """Keystrokes -> printable command lines; heredocs collapse to one line naming what they add."""
    import re
    out = []; lines = ks.splitlines(); i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"cat >>? *(\S+) <<'(\w+)'", ln)
        if m:
            fname, tag = m.group(1), m.group(2); body = []; i += 1
            while i < len(lines) and lines[i].strip() != tag:
                body.append(lines[i]); i += 1
            methods = re.findall(r"add\('([\w.]+)'", "\n".join(body))
            what = ", ".join(dict.fromkeys(methods)) if methods else ("the report" if fname.endswith(".md") else "helper code")
            out.append(f"$ {ln}   [{len(body)} line{'s' if len(body) != 1 else ''}: {what}]")
        elif ln.strip():
            out.append(f"$ {ln}")
        i += 1
    return out


def _abridge_observation(text):
    """Terminal output -> the lines that carry information: steward replies and printed results."""
    import ast, re
    out = []
    # printed dicts are wrapped at the terminal width: pull them out whole first
    dicts = []
    for blob in re.findall(r"\{'[^{}]*\}", text, re.S):
        try:
            dicts.append(ast.literal_eval(blob.replace("\n", "")))
        except Exception:
            pass
    for d in dicts:
        kv = [f"{k} {d[k]:.4g}" if isinstance(d[k], float) else f"{k} {d[k]}" for k in KEEP_KEYS if k in d]
        if kv:
            out.append("> " + ", ".join(kv))
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("# ") and "stage_id=" in s:
            m = re.search(r"stage_id=(\w+)", s); title = s[2:s.index("[")].strip()
            out.append(f"> released {m.group(1)}: {title}")
        elif s.startswith("[refused:"):
            out.append(f"> {s}")
        elif s.startswith("Unknown declaration key") or s.startswith("I have no process fact") or s.startswith("Process engineer:"):
            out.append(f"> {s}")
    # drop exact duplicates that a re-run of the whole script reprints
    seen = set(); dedup = []
    for o in out:
        if o not in seen:
            seen.add(o); dedup.append(o)
    return dedup


def _tex(s):
    """Escape prose for LaTeX."""
    for a, b in (("\\", "\\textbackslash{}"), ("&", "\\&"), ("%", "\\%"), ("$", "\\$"), ("#", "\\#"),
                 ("_", "\\_"), ("{", "\\{"), ("}", "\\}"), ("~", "\\textasciitilde{}"), ("^", "\\textasciicircum{}"),
                 ("—", "---"), ("–", "--"), ("’", "'"), ("\u201c", "``"), ("\u201d", "''")):
        s = s.replace(a, b)
    return s


METHOD_SIG = [("msa.attribute_agreement", ("kappaMin",)), ("quality.pareto", ("topCategoryPct",)),
              ("control_chart.p", ("centerLine", "outOfControlCount")), ("capability.binomial", ("avgP",)),
              ("basic.two_proportions", ("head1Pct",)), ("basic.one_proportion", ("pValue",))]
METHOD_LABEL = {"msa.attribute_agreement": "attribute agreement", "quality.pareto": "Pareto of the disagreements",
                "control_chart.p": "$p$ chart", "capability.binomial": "binomial capability",
                "basic.one_proportion": "one-proportion test", "basic.two_proportions": "two-proportion test",
                "meta.data_profiling": "data profile"}


def _result_line(d):
    for m, sig in METHOD_SIG:
        if all(k in d for k in sig):
            if m == "msa.attribute_agreement":
                return m, f"$\\kappa_{{\\min}}$ {d['kappaMin']:.4f}, agreement {d['agreementPct']:.2f}\\%"
            if m == "quality.pareto":
                return m, f"top category {d['topCategoryPct']:.2f}\\%"
            if m == "control_chart.p":
                return m, f"centre line {d['centerLine']:.4f}, {d['outOfControlCount']} lot(s) out of limits"
            if m == "capability.binomial":
                return m, f"$\\bar p$ {d['avgP']:.4f}, $Z$ {d['processZ']:.3f}"
            if m == "basic.two_proportions":
                return m, f"{d['head1Pct']:.2f}\\% vs {d['head2Pct']:.2f}\\%, $p$ = {d['pValue']:.2g}"
            if m == "basic.one_proportion":
                return m, f"$p$ = {d['pValue']:.2g}"
    return None, None


def _typed_text(cmd, typed):
    """The quoted text of a steward command as the agent typed it (the echo may be wrapped)."""
    import re
    head = cmd[:40]
    for k in typed:
        if k.startswith(head):
            m = re.search(r'"([^"]*)"', k)
            if m:
                return m.group(1)
    return ""


def _segments(text):
    """Split terminal output into (command, output) pairs; text before the first prompt is
    the tail of the previous turn's command and is returned under command None."""
    import re
    parts = re.split(r"root@\w+:/workspace# ", text)
    segs = []
    if parts and parts[0].strip():
        segs.append((None, parts[0]))
    for chunk in parts[1:]:
        cmd, _, out = chunk.partition("\n")
        segs.append((cmd.strip(), out))
    return segs


def _summarise(cmd, out, shown, typed=()):
    """One or more typeset action lines for a command and what came back."""
    import re
    L = []
    def outcome(o):
        m = re.search(r"stage_id=(\w+)", o)
        if m and "[refused" not in o.split("stage_id")[0]:
            return f"$\\to$ released \\texttt{{{_tex(m.group(1))}}}", m.group(1)
        m = re.search(r"\[refused: (\w+)\]", o)
        if m:
            return f"$\\to$ refused (\\texttt{{{m.group(1)}}})", None
        return "", None
    def rel(text, batch):
        return (text, ("released", batch)) if batch else (text, None)
    if cmd is None:
        oc, batch = outcome(out)
        return [rel(f"\\quad {oc}", batch)] if oc else []
    if cmd.startswith("steward status"):
        L.append(("\\texttt{status}: two batches available, four locked", None))
    elif cmd.startswith("steward request"):
        q = re.search(r'"([^"]*)"', cmd); q = q.group(1) if q else _typed_text(cmd, typed)
        oc, batch = outcome(out); L.append(rel(f"\\texttt{{request}} ``{_tex(q)}'' {oc}", batch))
    elif cmd.startswith("steward provision"):
        q = re.search(r'"([^"]*)"', cmd); q = q.group(1) if q else _typed_text(cmd, typed)
        oc, batch = outcome(out); L.append((f"\\texttt{{provision}} ``{_tex(q)}'' {oc}", None))
    elif cmd.startswith("steward declare"):
        key = cmd.split()[2] if len(cmd.split()) > 2 else ""
        L.append((f"\\texttt{{declare}} \\texttt{{{_tex(key)}}} $\\to$ refused: no such lock on this case", None))
    elif re.match(r"cat >>? *\S+ <<'", cmd):
        fname = cmd.split()[2] if cmd.startswith("cat >>") else cmd.split()[2]
        body = [l[2:] for l in out.splitlines() if l.startswith("> ")]
        methods = list(dict.fromkeys(re.findall(r"add\('([\w.]+)'", "\n".join(body))))
        if fname.endswith(".md"):
            L.append((f"writes the report ({len(body)} lines)", None))
        elif methods:
            L.append(("codes " + ", ".join(METHOD_LABEL.get(m, m) for m in methods), ("coded", tuple(methods))))
    elif cmd.startswith("python3 analyze.py") or cmd.startswith("python3 "):
        for blob in re.findall(r"\{'[^{}]*\}", out, re.S):
            try:
                import ast; d = ast.literal_eval(blob.replace("\n", ""))
            except Exception:
                continue
            m, line = _result_line(d)
            if m and (m, line) not in shown:
                shown.add((m, line)); L.append((f"runs {METHOD_LABEL[m]} $\\to$ {line}", ("ran", m, line)))
    elif cmd.startswith("cat data/"):
        L.append((f"reads \\texttt{{{_tex(cmd.split()[1].split('/')[-1])}}}", None))
    return L


DATASET = Path("harbor/datasets/dmaic-bench-r3")
STUDY2 = Path("paper/blind_review_2026-09-19/coordinator/results_study2.json")


def batch_summaries(seed):
    """One line per released batch, from the task's own blocks.json."""
    b = json.load(open(DATASET / f"dmaic-adb_c33-t3-s{seed}-clean/environment/task/blocks.json"))
    S = {}
    S["define"] = f"the goal and the required share {b['define']['required_reject_share']:g}"
    for k in ("study_1", "study_2"):
        r = b[k]["ratings"]; na = len(r); rep = len(next(iter(r.values()))); nb = len(b[k]["standard"])
        S[k] = f"{na} appraisers $\\times$ {rep} repeats $\\times$ {nb} boards, pass/fail, with the answer key"
    c = b["disagreements"]["counts"]
    S["disagreements"] = f"{sum(c.values())} items in {len(c)} categories (" + ", ".join(f"{_tex(k)} {v}" for k, v in sorted(c.items(), key=lambda kv: -kv[1])) + ")"
    x = b["lots"]["defectCounts"]; n = b["lots"]["subgroupSizes"]
    S["lots"] = f"{len(x)} lots of {n[0]}: rejects " + ", ".join(str(v) for v in x)
    h = b["heads"]
    S["heads"] = f"{h['events1']} of {h['trials1']:,} and {h['events2']} of {h['trials2']:,}"
    return S


def expert_verdicts():
    """(seed, point) -> (majority gate, model whose run the experts read) for case 33 in study 2."""
    d = json.load(open(STUDY2))
    return {(u["seed"], u["point"]): (u["gate_verdict"], u["model"]) for u in d["units"] if u["case"] == "adb_c33"}


ROUTE_NODES = {2: ["D_scope", "M_agree1", "M_disagree", "M_agree2", "M_pchart", "A_cap", "A_root_cause", "I_improve", "C_control"],
               3: ["D_scope", "M_agree1", "M_disagree", "M_agree2", "M_escalate"]}
FORK_OF_RESULT = [("msa.attribute_agreement", "study_1", "M_agree1"), ("msa.attribute_agreement", "study_2", "M_agree2"),
                  ("control_chart.p", "lots", "M_pchart"), ("capability.binomial", "lots", "A_cap")]


def transcript_rows(t):
    tj = json.load(open(t["dir"] + "agent/trajectory.json"))
    turns = [s for s in tj["steps"] if s.get("source") == "agent"]
    rows = []; shown = set(); cost = 0.0; ptok = ctok = 0
    seed = int(t["dir"].split("-s")[1].split("-")[0])
    summ = batch_summaries(seed); experts = expert_verdicts(); route = ROUTE_NODES[seed]
    ref_pairs = {(m, b) for (m, b), n in NODE_OF.items() if n in route}
    ref_batches = {b for _m, b in ref_pairs}
    pq = {d["point_id"]: d for d in t["card"]["pq"]["details"]}
    events = []                         # (turn, kind, payload) in order, for the fork rows
    for k, s in enumerate(turns, 1):
        msg = s.get("message", "")
        ana = plan = ""
        for ln in msg.splitlines():
            if ln.startswith("Analysis:"): ana = ln[9:].strip()
            elif ln.startswith("Plan:"): plan = ln[5:].strip()
            elif ana and not plan: ana += " " + ln.strip()
            elif plan: plan += " " + ln.strip()
        acts = []; typed = []
        for tc in s.get("tool_calls") or []:
            if tc.get("function_name") == "mark_task_complete":
                acts.append(("marks the task complete", None))
            typed += [l for l in (tc.get("arguments", {}).get("keystrokes") or "").splitlines() if l.startswith("steward ")]
        for r in (s.get("observation") or {}).get("results", []):
            for cmd, out in _segments(r.get("content", "")):
                lines = _summarise(cmd, out, shown, typed)
                if cmd is None and lines and rows:
                    rows[-1][2].extend(lines)      # the reply belongs to the previous turn
                    for _, tag in lines:
                        if tag: events.append((k - 1, tag))
                else:
                    acts.extend(lines)
                    for _, tag in lines:
                        if tag: events.append((k, tag))
        m = s.get("metrics") or {}
        cost += m.get("cost_usd") or 0; ptok += m.get("prompt_tokens") or 0; ctok += m.get("completion_tokens") or 0
        rows.append([k, (ana, plan), acts])
    # expand action tuples to text, adding the data summary under each release; where a run
    # printed nothing the scorer could read, take the value the trace recorded for that method
    trace_steps = [s_ for s_ in t["trace"]["steps"]]; used = set()
    for r in rows:
        out = []; ran_here = {tag[1] for _, tag in r[2] if tag and tag[0] == "ran"}
        for text, tag in r[2]:
            out.append(text)
            if tag and tag[0] == "released" and tag[1] in summ:
                out.append(f"\\quad\\textcolor{{gray!70!black}}{{data: {summ[tag[1]]}}}")
            if tag and tag[0] == "coded":
                for m in tag[1]:
                    if m in ran_here or m not in METHOD_LABEL or m == "meta.data_profiling":
                        continue
                    for i, s_ in enumerate(trace_steps):
                        if i not in used and s_["method_id"] == m:
                            mm, line = _result_line(s_["outputs"] or {})
                            if line:
                                used.add(i); out.append(f"computes {METHOD_LABEL[m]} $\\to$ {line}")
                                events.append((r[0], ("ran", m, line)))
                            break
        r[2] = out
    events.sort(key=lambda e: e[0])
    # fork rows: the turn a guard field first appears decides the fork; the agent's next
    # off-route event (a batch the route never reads, or an analysis it never runs) is named
    forks = []
    seen_forks = set()
    for k, tag in events:
        if tag[0] != "ran": continue
        for m, b, node in FORK_OF_RESULT:
            if tag[1] == m and node not in seen_forks and node in route:
                seen_forks.add(node)
                expr, key, fn, yes, no = GUARD[node]
                # the reported value: parse it back from the line text is fragile; re-read the trace
                val = next(s_["outputs"][key] for s_ in t["trace"]["steps"] if NODE_OF.get((s_["method_id"], batch_of(s_))) == node)
                holds = fn(val); target = yes if holds else no
                verdict = pq.get(node, {}).get("verdict")
                ref = f"$\\to$ {_tex(target)}" + (", the project ends here" if target == "M_escalate" else "")
                ev = experts.get((seed, node))
                if ev:
                    gate, model = ev
                    gate_label = "NO-GO" if gate in ("STOP", "NO-GO") else gate
                    exp = f"human experts (study 2, majority of three, reading {_tex(model)}'s run of this seed and fork): {gate_label}"
                    if (gate in ("STOP", "NO-GO")) != (target in ("M_escalate", "M_disagree", "A_special_cause", "A_root_cause")):
                        exp += " --- one of the four go-side disagreements of \\S\\ref{sec:study2}"
                else:
                    exp = "human experts: no study-2 unit at this fork"
                if verdict == "correct":
                    agent = "agent: the same \\checkmark"
                else:
                    later = [(kk, tg) for kk, tg in events if kk >= k and ((tg[0] == "released" and tg[1] not in ref_batches) or (tg[0] == "ran" and (tg[1], None) and tg[1] not in {m_ for m_, _b in ref_pairs}))]
                    parts = []
                    rel_ = next(((kk, tg) for kk, tg in later if tg[0] == "released"), None)
                    ran_ = next(((kk, tg) for kk, tg in later if tg[0] == "ran"), None)
                    if rel_: parts.append(f"requests \\texttt{{{_tex(rel_[1][1])}}} at turn {rel_[0]}")
                    if ran_: parts.append(f"runs the {METHOD_LABEL[ran_[1][1]]} at turn {ran_[0]}")
                    agent = "agent: " + " and ".join(parts) + " $\\times$"
                val_txt = f"{val:.4f}" if isinstance(val, float) else str(val)
                forks.append((k, node, f"\\textbf{{Fork {_tex(node)}}}: {expr} reads {val_txt}, {'holds' if holds else 'fails'}. Reference route {ref}. " + exp + ". " + agent, verdict == "correct"))
                break
    # forks the printed output never showed: place them at the turn their batch was released
    # (or the following turn if the previous fork sits there), with the trace's value
    for m, b, node in FORK_OF_RESULT:
        if node in route and node not in seen_forks:
            rel_turn = next((kk for kk, tg in events if tg == ("released", b)), None)
            if rel_turn is None: continue
            k = min(rel_turn + 1, len(rows))      # the agent computes on the turn after the release
            step = next((s_ for s_ in t["trace"]["steps"] if NODE_OF.get((s_["method_id"], batch_of(s_))) == node), None)
            if step is None: continue
            mm, line = _result_line(step["outputs"] or {})
            rows[k - 1][2].append(f"computes {METHOD_LABEL[m]} $\\to$ {line}")
            events.append((k, ("ran", m, line))); events.sort(key=lambda e: e[0])
            seen_forks.add(node)
            expr, key, fn, yes, no = GUARD[node]; val = step["outputs"][key]; holds = fn(val); target = yes if holds else no
            verdict = pq.get(node, {}).get("verdict")
            ref = f"$\\to$ {_tex(target)}" + (", the project ends here" if target == "M_escalate" else "")
            ev = experts.get((seed, node))
            exp = (f"human experts (study 2, majority of three, reading {_tex(ev[1])}'s run of this seed and fork): {ev[0]}" if ev
                   else "human experts: no study-2 unit at this fork")
            agent = "agent: the same \\checkmark" if verdict == "correct" else "agent: went on $\\times$"
            val_txt = f"{val:.4f}" if isinstance(val, float) else str(val)
            forks.append((k, node, f"\\textbf{{Fork {_tex(node)}}}: {expr} reads {val_txt}, {'holds' if holds else 'fails'}. Reference route {ref}. " + exp + ". " + agent, verdict == "correct"))
    order = {node: i for i, (_m, _b, node) in enumerate(FORK_OF_RESULT)}
    forks.sort(key=lambda f: (f[0], order[f[1]]))
    return rows, forks, dict(turns=len(turns), ptok=ptok, ctok=ctok, cost=cost)


def write_transcripts(t2, t3):
    def table(t, caption, label):
        rows, forks, tot = transcript_rows(t)
        bad_turns = set()
        for k, node, text, ok in forks:
            if not ok:
                import re as _re
                bad_turns |= {int(x) for x in _re.findall(r"at turn (\d+)", text)}
        L = ["\\begin{longtable}{@{}r@{\\hskip 6pt}>{\\raggedright\\arraybackslash}p{0.42\\linewidth}@{\\hskip 8pt}>{\\raggedright\\arraybackslash}p{0.48\\linewidth}@{}}",
             f"\\caption{{{caption}}}\\label{{{label}}}\\\\",
             "\\toprule", "Turn & The agent's stated analysis and plan & What it did, and what came back \\\\", "\\midrule", '\\endfirsthead\n\\multicolumn{3}{c}{\\normalfont\\normalsize Table \\thetable{} (continued)} \\\\\n\\noalign{\\vskip 6pt}',
             "\\toprule", "Turn & The agent's stated analysis and plan & What it did, and what came back \\\\", "\\midrule", "\\endhead",
             "\\bottomrule", "\\endfoot"]
        for k, (ana, plan), acts in rows:
            shade = "\\rowcolor{red!9}" if k in bad_turns else ("\\rowcolor{gray!7}" if k % 2 else "")
            left = _tex(ana) + (f" \\emph{{Plan: {_tex(plan)}}}" if plan else "")
            right = " \\newline ".join(acts) if acts else "---"
            L.append(f"{shade}{k} & {left} & {right} \\\\")
            for fk, node, text, ok in forks:
                if fk == k:
                    L.append(f"\\rowcolor{{{'green!10' if ok else 'red!14'}}}\\multicolumn{{3}}{{@{{}}p{{\\linewidth}}@{{}}}}{{\\small {text}}} \\\\")
        L.append(f"\\midrule\n\\multicolumn{{3}}{{@{{}}l}}{{\\emph{{{tot['turns']} agent turns, {tot['ptok']:,} prompt and {tot['ctok']:,} completion tokens, \\${tot['cost']:.2f}; pq {t['card']['pq']['points_correct']}/{t['card']['pq']['points_total']}, reward {t['reward']:.3f}.}}}} \\\\")
        L.append("\\end{longtable}")
        return "\n".join(L)
    body = ["% generated by scripts/appendix_case33.py", "{\\small\\setlength{\\tabcolsep}{0pt}\\renewcommand{\\arraystretch}{1.15}",
            table(t3, "GPT-6-astra, seed 3, plain instruction, by turn. Left: verbatim analysis and plan. Right: steward exchanges and executed analyses. Shading marks route decisions.", "lst:c33-s3-turns"),
            "", table(t2, "GPT-6-astra on seed 2, plain instruction, turn by turn (same conventions).", "lst:c33-s2-turns"), "}"]
    (OUT / "lst_c33_transcripts.tex").write_text("\n".join(body) + "\n")


def write_reports(t2, t3p):
    def clean(s):
        return (s.replace("—", "--").replace("–", "-").replace("’", "'").replace("×", "x")
                 .replace("≤", "<=").replace("≥", ">=").replace("κ", "kappa").encode("ascii", "replace").decode())
    L = ["% generated by scripts/appendix_case33.py",
         "\\begin{lstlisting}[caption={GPT-6-astra on seed 2 under the plain instruction, the report in full.},label={lst:c33-s2-report}]",
         clean(t2["report"]).rstrip(), "\\end{lstlisting}",
         "\\begin{lstlisting}[basicstyle=\\ttfamily\\fontsize{9}{9.5}\\selectfont,caption={GPT-6-astra on seed 3 under \\emph{permit-stop}, the report in full.},label={lst:c33-s3p-report}]",
         clean(t3p["report"]).rstrip(), "\\end{lstlisting}"]
    (OUT / "lst_c33_reports.tex").write_text(reflow_latex_listings("\n".join(L) + "\n"))


if __name__ == "__main__":
    t2, t3, t3p = trial("plain", 2), trial("plain", 3), trial("permit", 3)
    write_timeline(t2, t3); write_graph(); write_reports(t2, t3p); write_transcripts(t2, t3)
    print("ok", t2["reward"], t3["reward"], t3p["reward"])
