#!/usr/bin/env python3
"""Decision-breakdown table: where each system's decisions go wrong, and how.

    PYTHONPATH=.:harbor/src python3 scripts/fig_breakdown.py

Reads the same rescored campaigns as scripts/restraint_analysis.py (same SYSTEMS, same
first-wins row merge, same decision enumeration) so every cell agrees with Table 2. Writes
paper/iclr/tab_decision_breakdown.tex and paper/iclr/breakdown.tex (macros).
Pass --legacy-figure to additionally export the historical PDF/PNG heatmap.

Panel (a): decision correctness by DMAIC phase, no-go and go decisions apart. The phase
is the graph node's prefix (D/M/A/I/C). Panel (b): the wrong decisions of each system, split
by the scorer's verdict pathway (dmaic_bench/scoring/pq.py):
  E1  no-go fork, ran work that only exists past the inadmissible branch ("evidence" or
      "divergent_evidence" incorrect) -- continued past a failed precondition;
  E2  no-go fork never reached / no evidence either way ("unknown");
  E3  go fork, ran an inadmissible branch's work;
  E4  go fork never reached;
  E5  stopped where the route continues ("abstained_from_required_branch"), either class.
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path[:0] = [".", "harbor/src", "scripts"]
import restraint_analysis as RA                       # noqa: E402

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
from figure_palette import heatmap_cmap, text_on_color
from matplotlib import colors as mcolors              # noqa: E402
from matplotlib.offsetbox import OffsetImage, AnnotationBbox  # noqa: E402

OUT = Path("paper/iclr")
#: full-resolution vendor marks (paper/logo); paper/iclr/logos holds the small table copies
FIG_LOGOS = {"OpenAI": "chatgpt.png", "Anthropic": "claude.png", "DeepSeek": "deepseek.png",
             "Zhipu": "zhipu.png", "Alibaba": "qwen.png", "Moonshot": "KIMI.png"}
LOGO_DIR = Path("paper/logo")
STUDY2 = Path("paper/blind_review_2026-09-19/coordinator/results_study2.json")
PHASES = "DMAIC"
PHASE_NAME = {"D": "Define", "M": "Measure", "A": "Analyze", "I": "Improve", "C": "Control"}
RAN = {"evidence", "divergent_evidence", "explicit", "explicit_contradicted", "declared_unsupported"}
A_COLS = [("NOGO", "all"), ("NOGO", "M"), ("NOGO", "A"), ("NOGO", "I"),
          ("GO", "all"), ("GO", "D"), ("GO", "M"), ("GO", "A"), ("GO", "I"), ("GO", "C")]
B_COLS = ["E1", "E2", "E3", "E4", "E5"]


def collect():
    cases = RA.V.discover()
    systems = []
    for name, vendor, k1, _k3 in RA.SYSTEMS:
        rows = RA.load_rows(k1)
        if len(rows) != 97:
            continue
        c = Counter(); err = Counter()
        for r, p, v, _own, _strict, _order in RA.decisions(rows, cases):
            kind = "NOGO" if RA.is_stop(p) else "GO"
            ph = p["point_id"][0]
            card = r["card"].get("scorecard") or {}
            via = next((d.get("via") for d in (card.get("pq") or {}).get("details", [])
                        if d.get("kind") == "decision_point" and d.get("point_id") == p["point_id"]), None)
            c[(kind, ph, "n")] += 1; c[(kind, "all", "n")] += 1
            if v == "correct":
                c[(kind, ph, "ok")] += 1; c[(kind, "all", "ok")] += 1
                continue
            if via == "abstained_from_required_branch":
                err["E5"] += 1
            elif v == "unknown" or via in (None, "none"):
                err["E2" if kind == "NOGO" else "E4"] += 1
            elif via in RAN:
                err["E1" if kind == "NOGO" else "E3"] += 1
            else:
                raise SystemExit(f"unclassified verdict pathway {v}/{via} for {name}")
        mean = sum(r["reward"] for r in rows) / len(rows)
        systems.append(dict(name=name, vendor=vendor, mean=mean, c=c, err=err))
    # order as Table 2: mean over all complete attempts where a system has them
    try:
        import json as _json
        rep = _json.load(open("docs/result_restraint.json"))
        for s in systems:
            if s["name"] in rep:
                s["mean"] = rep[s["name"]]["mean"]
    except (OSError, ValueError, KeyError):
        pass
    systems.sort(key=lambda s: -s["mean"])
    return systems


def experts():
    """Majority gate of the three blind reviewers on the study-2 units, against the benchmark
    label: the human decision at the same forks, by phase (unweighted counts)."""
    import json
    c = Counter()
    for u in json.load(open(STUDY2))["units"]:
        kind = "NOGO" if RA.decision_label(u["kind"]) == "NO-GO" else "GO"
        ok = (RA.decision_label(u["gate_verdict"]) == "NO-GO") == (RA.decision_label(u["kind"]) == "NO-GO")
        for ph in (u["point"][0], "all"):
            c[(kind, ph, "n")] += 1; c[(kind, ph, "ok")] += ok
    return c


def pct(c, kind, ph):
    n = c[(kind, ph, "n")]
    return 100.0 * c[(kind, ph, "ok")] / n if n else float("nan"), n


def truncated(name, lo, hi):
    base = plt.get_cmap(name)
    return mcolors.LinearSegmentedColormap.from_list(f"{name}_t", base(__import__("numpy").linspace(lo, hi, 256)))


def table_data(systems):
    """Unrounded values shared by the editable table and historical heatmap."""
    rows = []
    for s in systems:
        wrong = sum(s["err"].values())
        rows.append({
            "name": s["name"], "vendor": s["vendor"],
            "accuracy": [pct(s["c"], *p)[0] if pct(s["c"], *p)[1] else None for p in A_COLS],
            "n": [pct(s["c"], *p)[1] for p in A_COLS],
            "errors": [100.0 * s["err"][e] / wrong if wrong else None for e in B_COLS],
        })
    exp = experts()
    return {"systems": rows, "experts": {
        "accuracy": [pct(exp, *p)[0] if pct(exp, *p)[1] else None for p in A_COLS],
        "n": [pct(exp, *p)[1] for p in A_COLS],
    }}


def latex_table(data):
    """Native LaTeX cells: selectable text, original values and continuous colors."""
    blues = reds = heatmap_cmap()

    def color(value, cmap):
        if value is None:
            return "F4F4F4", "gray", r"\textemdash"
        return mcolors.to_hex(cmap(value / 100)).lstrip("#").upper(), text_on_color(cmap(value / 100)), f"{value:.0f}"

    def cell(value, cmap):
        bg, fg, text = color(value, cmap)
        return rf"\bdcell{{{bg}}}{{{fg}}}{{{text}}}"

    L = [
        "% Generated by scripts/fig_breakdown.py; editable native LaTeX table.",
        r"\begingroup",
        r"\fontsize{7.5}{9}\selectfont",
        r"\setlength{\tabcolsep}{1.2pt}",
        r"\renewcommand{\arraystretch}{1.06}",
        r"\newcommand{\bdcell}[3]{\cellcolor[HTML]{#1}\textcolor{#2}{#3}}",
        r"\newcommand{\bdhead}[2]{\begin{tabular}[c]{@{}c@{}}\textbf{#1}\\[-0.4pt]{\fontsize{6}{7}\selectfont\color{black!55}\textit{n}=#2}\end{tabular}}",
        r"\newcommand{\bderrhead}[1]{\begin{tabular}[c]{@{}c@{}}\textbf{#1}\\[-0.4pt]{\fontsize{6}{7}\selectfont\phantom{\textit{n}=00}}\end{tabular}}",
        r"\begin{tabular}{@{}>{\centering\arraybackslash}p{18pt}@{\hspace{4pt}}>{\raggedright\arraybackslash}p{80pt}@{\hspace{4pt}}*{4}{>{\centering\arraybackslash}p{\dimexpr(\linewidth-144.8pt)/15\relax}}@{\hspace{5pt}}*{6}{>{\centering\arraybackslash}p{\dimexpr(\linewidth-144.8pt)/15\relax}}@{\hspace{5pt}}*{5}{>{\centering\arraybackslash}p{\dimexpr(\linewidth-144.8pt)/15\relax}}@{}}",
        r"\toprule",
        r" & & \multicolumn{4}{c}{\textcolor[HTML]{08519C}{\textbf{NO-GO accuracy (\%)}}} & \multicolumn{6}{c}{\textcolor[HTML]{08519C}{\textbf{GO accuracy (\%)}}} & \multicolumn{5}{c@{}}{\textcolor[HTML]{A50F15}{\textbf{Error share (\%)}}} \\",
        r"\cmidrule(lr){3-6}\cmidrule(lr){7-12}\cmidrule(l){13-17}",
        r"\textbf{Rank} & \textbf{Agent} & "
        + " & ".join(rf"\bdhead{{{'all' if phase == 'all' else phase}}}{{{n}}}"
                     for (_, phase), n in zip(A_COLS, data["systems"][0]["n"]))
        + " & " + " & ".join(rf"\bderrhead{{{name}}}" for name in B_COLS) + r" \\",
        r"\midrule",
    ]
    for rank, s in enumerate(data["systems"], 1):
        values = [cell(v, blues) for v in s["accuracy"]] + [cell(v, reds) for v in s["errors"]]
        L.append(rf"{rank} & {RA.logo(s['vendor'])}{s['name']} & " + " & ".join(values) + r" \\")
    L.append(r"\midrule")
    values = [cell(v, blues) for v in data["experts"]["accuracy"]] + [cell(None, reds)] * 5
    L.append(r"\textemdash & \emph{Expert labels (blind)} & " + " & ".join(values) + r" \\")
    L.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\par\vspace{3pt}",
        r"\begin{minipage}{\linewidth}",
        r"\fontsize{6.7}{8}\selectfont\raggedright",
        r"\textbf{E1}: continued past a failed no-go precondition; \textbf{E2/E4}: no-go/go fork unreached (diagnostic unrun).\\",
        r"\textbf{E3}: took an inadmissible go branch; \textbf{E5}: stopped where the route continues.\\",
        r"\textit{n}: decisions per model; experts: \bdExpertNogoN{} no-go and \bdExpertGoN{} go forks, against benchmark labels; \textemdash: not evaluated.",
        r"\par\vspace{2pt}",
    ])
    def key(cmap):
        items = []
        for v in (0, 50, 100):
            bg, fg, text = color(v, cmap)
            items.append(r"\colorbox[HTML]{" + bg + r"}{\makebox[13pt]{\textcolor{" + fg + "}{" + text + "}}}")
        return "".join(items)
    L.append(r"\setlength{\fboxsep}{1.5pt} Correct (\%): " + key(blues)
             + r"\hfill Share of errors (\%): " + key(reds))
    L.extend([r"\end{minipage}", r"\endgroup"])
    return "\n".join(L) + "\n"


def draw(systems):
    plt.rcParams.update({"font.family": "Helvetica", "font.size": 6.2, "pdf.fonttype": 42})
    a_cols = A_COLS
    b_cols = B_COLS
    exp = experts()
    n_rows = len(systems) + 1                      # + expert row
    # geometry (inches)
    label_w, cell_w, gap_w, row_h = 1.40, 0.245, 0.14, 0.138
    rank_x, logo_x = 0.16, 0.30
    head_h, foot_h = 0.46, 0.54
    fig_w = label_w + cell_w * (len(a_cols) + len(b_cols)) + gap_w
    fig_h = head_h + row_h * n_rows + foot_h
    fig = plt.figure(figsize=(fig_w, fig_h))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, fig_w); ax.set_ylim(0, fig_h); ax.axis("off")

    blues = heatmap_cmap(); reds = heatmap_cmap()
    x_a = label_w; x_b = label_w + cell_w * len(a_cols) + gap_w
    y_top = fig_h - head_h

    def cell(x, y, val, cmap, text, vmax=100.0):
        if val != val:                         # nan
            fc = "#f4f4f4"; tc = "#888888"
        else:
            fc = cmap(min(val, vmax) / vmax); tc = text_on_color(fc)
        ax.add_patch(plt.Rectangle((x, y), cell_w, row_h, facecolor=fc, edgecolor="white", linewidth=0.6))
        ax.text(x + cell_w / 2, y + row_h / 2, text, ha="center", va="center", fontsize=6.2, color=tc)

    # column headers
    for j, (kind, ph) in enumerate(a_cols):
        x = x_a + j * cell_w
        n = systems[0]["c"][(kind, ph, "n")]
        ax.text(x + cell_w / 2, y_top + 0.04, "all" if ph == "all" else ph, ha="center", va="bottom", fontsize=6.4, fontweight="bold")
        ax.text(x + cell_w / 2, y_top + 0.15, f"n={n}", ha="center", va="bottom", fontsize=5.2, color="#555555")
    for j, e in enumerate(b_cols):
        x = x_b + j * cell_w
        ax.text(x + cell_w / 2, y_top + 0.04, e, ha="center", va="bottom", fontsize=6.4, fontweight="bold")
    # group headers with rules
    def group(x0, ncol, text, color):
        x1 = x0 + ncol * cell_w
        ax.plot([x0 + 0.02, x1 - 0.02], [y_top + 0.30, y_top + 0.30], color=color, linewidth=0.8)
        ax.text((x0 + x1) / 2, y_top + 0.33, text, ha="center", va="bottom", fontsize=6.6, fontweight="bold", color=color)
    group(x_a, 4, "No-go correct (%)", "#08519c")
    group(x_a + 4 * cell_w, 6, "Go correct (%)", "#08519c")
    group(x_b, 5, "Wrong, by pathway (%)", "#a50f15")
    ax.text(x_a - 0.04, y_top + 0.04, "Agent", ha="right", va="bottom", fontsize=6.4, fontweight="bold")
    ax.text(rank_x, y_top + 0.04, "Rank", ha="center", va="bottom", fontsize=6.4, fontweight="bold")
    ax.text(0.04, y_top + 0.15, "by mean reward", ha="left", va="bottom", fontsize=5.2, color="#555555")

    # rows
    for i, s in enumerate(systems):
        y = y_top - (i + 1) * row_h
        ax.text(x_a - 0.04, y + row_h / 2, s["name"], ha="right", va="center", fontsize=6.4)
        ax.text(rank_x, y + row_h / 2, str(i + 1), ha="center", va="center", fontsize=6.4, fontweight="bold")
        lf = LOGO_DIR / FIG_LOGOS.get(s["vendor"], "")
        if lf.is_file():
            img = plt.imread(lf)
            zoom = 7.0 / img.shape[0]                       # ~7 pt tall
            ab = AnnotationBbox(OffsetImage(img, zoom=zoom), (logo_x, y + row_h / 2),
                                frameon=False, box_alignment=(0.0, 0.5))
            ax.add_artist(ab)
        for j, (kind, ph) in enumerate(a_cols):
            v, n = pct(s["c"], kind, ph)
            cell(x_a + j * cell_w, y, v, blues, f"{v:.0f}" if n else "–")
        wrong = sum(s["err"].values())
        for j, e in enumerate(b_cols):
            v = 100.0 * s["err"][e] / wrong if wrong else float("nan")
            cell(x_b + j * cell_w, y, v, reds, f"{v:.0f}" if wrong else "–")
        if i == 0:
            ax.plot([0.02, fig_w - 0.02], [y + row_h, y + row_h], color="#222222", linewidth=0.6)
    # expert row: the reviewers' own gate decisions at the sampled forks
    y = y_top - n_rows * row_h
    ax.plot([0.02, fig_w - 0.02], [y + row_h + 0.004, y + row_h + 0.004], color="#222222", linewidth=0.5)
    ax.text(x_a - 0.04, y + row_h / 2, "Expert labels (blind)", ha="right", va="center", fontsize=6.4, fontstyle="italic")
    ax.text(rank_x, y + row_h / 2, "–", ha="center", va="center", fontsize=6.4, color="#555555")
    for j, (kind, ph) in enumerate(a_cols):
        v, n = pct(exp, kind, ph)
        cell(x_a + j * cell_w, y, v, blues, f"{v:.0f}" if n else "–")
    for j in range(len(b_cols)):
        cell(x_b + j * cell_w, y, float("nan"), reds, "–")
    # footer legend + colour bars
    leg1 = "E1: continued past a failed precondition (no-go fork)     E2: no-go fork never reached     E3: took an inadmissible branch (go fork)"
    leg2 = "E4: go fork never reached     E5: stopped where the route continues"
    ax.text(0.04, foot_h - 0.05, leg1, ha="left", va="top", fontsize=5.6, color="#333333")
    ax.text(0.04, foot_h - 0.16, leg2, ha="left", va="top", fontsize=5.6, color="#333333")
    import numpy as np
    for x0, cmap, lab in ((x_a, blues, "correct"), (x_b, reds, "share of wrong")):
        w = cell_w * (4 if cmap is blues else 3)
        grad = np.linspace(0, 1, 128).reshape(1, -1)
        ax.imshow(grad, aspect="auto", cmap=cmap, extent=(x0, x0 + w, 0.13, 0.20), zorder=2)
        ax.text(x0 - 0.03, 0.165, lab, ha="right", va="center", fontsize=5.4, color="#333333")
        for t in (0, 50, 100):
            ax.text(x0 + w * t / 100, 0.11, f"{t}", ha="center", va="top", fontsize=5.0, color="#333333")
    ax.set_xlim(0, fig_w); ax.set_ylim(0, fig_h)
    legacy_dir = OUT / "figure_archive" / "generated"
    legacy_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(legacy_dir / "figure3_breakdown.pdf", dpi=600)   # dpi governs the embedded marks
    fig.savefig(legacy_dir / "figure3_breakdown.png", dpi=300)
    return fig_w, fig_h


def macros(systems):
    L = []
    def rng(kind, ph, tag):
        vals = [pct(s["c"], kind, ph)[0] for s in systems]
        L.append(f"\\newcommand{{\\bd{tag}Min}}{{{min(vals):.0f}}}")
        L.append(f"\\newcommand{{\\bd{tag}Max}}{{{max(vals):.0f}}}")
    rng("NOGO", "M", "NogoMeasure"); rng("NOGO", "A", "NogoAnalyze"); rng("NOGO", "I", "NogoImprove")
    rng("GO", "M", "GoMeasure"); rng("GO", "A", "GoAnalyze"); rng("GO", "I", "GoImprove"); rng("GO", "C", "GoControl")
    tot = Counter()
    for s in systems:
        tot.update(s["err"])
    nogo_wrong = tot["E1"] + tot["E2"]
    L.append(f"\\newcommand{{\\bdContinuedShare}}{{{100.0 * tot['E1'] / nogo_wrong:.0f}}}")
    L.append(f"\\newcommand{{\\bdNogoUnreached}}{{{tot['E2']}}}")
    L.append(f"\\newcommand{{\\bdStoppedShortN}}{{{tot['E5']}}}")
    L.append(f"\\newcommand{{\\bdGoUnreachedShare}}{{{100.0 * tot['E4'] / (tot['E3'] + tot['E4'] ):.0f}}}")
    L.append(f"\\newcommand{{\\bdSystems}}{{{len(systems)}}}")
    e = experts()
    L.append(f"\\newcommand{{\\bdExpertNogo}}{{{pct(e, 'NOGO', 'all')[0]:.0f}}}")
    L.append(f"\\newcommand{{\\bdExpertGo}}{{{pct(e, 'GO', 'all')[0]:.0f}}}")
    L.append(f"\\newcommand{{\\bdExpertNogoN}}{{{e[('NOGO', 'all', 'n')]}}}")
    L.append(f"\\newcommand{{\\bdExpertGoN}}{{{e[('GO', 'all', 'n')]}}}")
    (OUT / "breakdown.tex").write_text("% generated by scripts/fig_breakdown.py\n" + "\n".join(L) + "\n")
    return tot


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy-figure", action="store_true", help="also export the historical heatmap PDF/PNG")
    args = parser.parse_args()
    S = collect()
    (OUT / "tab_decision_breakdown.tex").write_text(latex_table(table_data(S)))
    if args.legacy_figure:
        draw(S)
    tot = macros(S)
    for s in S:
        print(f"{s['name']:16s} mean={s['mean']:.3f} nogo A={pct(s['c'],'NOGO','A')[0]:.0f} go A={pct(s['c'],'GO','A')[0]:.0f} err={dict(s['err'])}")
    print("pooled errors", dict(tot), "table", OUT / "tab_decision_breakdown.tex")
