#!/usr/bin/env python3
"""Reproduce Figure 5A--C from retained expert and control-replication results.

The 396 pt canvas is included at the paper's native text width: regular text
therefore remains 7 pt. Panel C counts joint correctness at the SAME matched
fork, not the product of the two marginal accuracies shown in panel B.
"""
import hashlib
import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.font_manager import FontProperties
from matplotlib.colors import to_rgb, to_hex
from matplotlib.patches import FancyArrowPatch
from matplotlib.transforms import blended_transform_factory
import numpy as np

from fig_study2 import SRC as EXPERT_SOURCE, figure_data, INK
from figure_pair_style import apply_style

ROOT = Path(__file__).resolve().parents[1]
CONTROL_SOURCE = ROOT / "output/research/control-replication-20260922.json"
OUT = ROOT / "paper/iclr/figures/figure05_expert_controls"


def require_input(path, producer):
    """Exit with a plain message when a run-artifact input is absent from the checkout."""
    if not Path(path).exists():
        sys.exit(f"missing input {path}: this file is not part of the tracked tree. It comes from "
                 f"the run-artifact archive ({producer}); see scripts/README.md, Analysis inputs.")
WIDTH, HEIGHT = 396, 136
PLOT_BOTTOM, PLOT_HEIGHT = 26, 80
CONDITIONS = [("plain", "Plain"), ("permit-stop", "Permit-stop"),
              ("permit-paraphrase", "Paraphrase"), ("normative", "Normative"),
              ("remind", "Remind")]
MODELS = [("GPT-6-astra", "GPT-6 Astra", "o", .25),
          ("DeepSeek-v4-pro", "DeepSeek-v4-pro", "s", -.25)]
GREY, GRID = "#596570", "#E8EDF1"
# Match the model swatches in the main-text Figure 4, not the older appendix palette.
MODEL_COLORS = {"GPT-6-astra": "#237E78", "DeepSeek-v4-pro": "#919ED0"}
EXPERT_COLORS = {"no_go": "#78838D", "go": "#34414B"}
LEGEND_FONT = FontProperties(family="Helvetica", size=7, weight="normal", style="normal")


def text(fig, x, y, value, **kwargs):
    return fig.text(x / WIDTH, y / HEIGHT, value, fontsize=7,
                    ha="left", va="center", **kwargs)


def legend(fig, handles, x, y):
    """Draw identical 7 pt labels on one explicit baseline, independent of glyphs.

    Separate automatic legend boxes vertically center their contents differently
    depending on ascenders/descenders. Fixed text baselines avoid that variation.
    All legend symbols also use the same physical size and label spacing.
    """
    renderer = fig.canvas.get_renderer()
    cursor = x
    for handle in handles:
        fig.add_artist(Line2D([(cursor+3.15)/WIDTH], [y/HEIGHT],
                              transform=fig.transFigure, linestyle="none",
                              marker=handle.get_marker(), markersize=3,
                              markerfacecolor=handle.get_markerfacecolor(),
                              markeredgecolor=handle.get_markeredgecolor(),
                              markeredgewidth=.65))
        label = handle.get_label()
        fig.text((cursor+9.1)/WIDTH, (y-2)/HEIGHT, label,
                 fontproperties=LEGEND_FONT, color=INK, ha="left", va="baseline")
        width, _, _ = renderer.get_text_width_height_descent(label, LEGEND_FONT, ismath=False)
        cursor += 9.1 + width*72/fig.dpi + 8


def outcome_handles():
    # Open versus filled symbols also distinguish outcomes in grayscale.
    return [Line2D([], [], marker="o", color=c, linestyle="none", markersize=3,
                   markerfacecolor="white" if label == "NO-GO" else c,
                   markeredgewidth=.65, label=label)
            for label, c in [("NO-GO", EXPERT_COLORS["no_go"]),
                             ("GO", EXPERT_COLORS["go"])]]


def model_handles(colored=False):
    return [Line2D([], [], marker=m, color=MODEL_COLORS[system] if colored else INK,
                   linestyle="none", markersize=3,
                   markerfacecolor=MODEL_COLORS[system] if colored else "white",
                   markeredgewidth=.65, label=label)
            for system, label, m, _ in MODELS]


def axes(fig, left, right, maximum, ticks, ylim):
    ax = fig.add_axes([left / WIDTH, PLOT_BOTTOM / HEIGHT,
                      (right-left) / WIDTH, PLOT_HEIGHT / HEIGHT])
    ax.set_xlim(0, maximum)
    ax.set_ylim(*ylim)
    ax.set_xticks(ticks)
    ax.set_yticks([])
    ax.tick_params(axis="x", length=2, pad=2.5, width=.45)
    ax.xaxis.grid(True, color=GRID, linewidth=.4)
    ax.set_axisbelow(True)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#AFBAC3")
    ax.spines["bottom"].set_linewidth(.45)
    return ax


def draw(expert, controls):
    apply_style()
    plt.rcParams["svg.hashsalt"] = "dmaic-expert-controls-triptych"
    fig = plt.figure(figsize=(WIDTH / 72, HEIGHT / 72))
    for x, title in [
        (2, "(A) Expert assessment"),
        (138, "(B) Instruction controls"),
        (272, "(C) Paired-fork success"),
    ]:
        t = text(fig, x, 128, title, fontweight="bold")
        t.set_fontsize(8)
    for x in [132, 266]:
        fig.add_artist(Line2D([x/WIDTH]*2, [4/HEIGHT, 133/HEIGHT],
                              transform=fig.transFigure, color="#D8E1E8", linewidth=.6))
    # One aligned row: outcomes for A and identical model-color keys for B/C.
    # The caption explains B's open/filled outcomes and C's marker sizes.
    legend(fig, outcome_handles(), 20, 116)
    legend(fig, model_handles(colored=True), 138, 116)
    legend(fig, model_handles(colored=True), 272, 116)

    aa = axes(fig, 51, 125, 100, [0, 50, 100], (-.55, 2.55))
    ab = axes(fig, 188, 259, 100, [0, 50, 100], (-.55, 4.55))
    ac = axes(fig, 322, 389, 16, [0, 8, 16], (-.55, 4.55))
    ta = blended_transform_factory(fig.transFigure, aa.transData)
    for metric, y, label, upward in [
        ("route", 2, "Route\naccuracy", True),
        ("semantic", 1, "Expert-rated\naccuracy", True),
        ("violations", 0, "Report\nviolations", False),
    ]:
        aa.text(2/WIDTH, y, label, transform=ta, fontsize=7, va="center",
                ha="left", linespacing=1.05)
        yp = PLOT_BOTTOM + PLOT_HEIGHT * (y+.55)/3.1
        start, end = yp-2.5, yp+2.5
        if not upward:
            start, end = end, start
        fig.add_artist(FancyArrowPatch((46/WIDTH, start/HEIGHT), (46/WIDTH, end/HEIGHT),
                       transform=fig.transFigure, arrowstyle="->", mutation_scale=5,
                       linewidth=.55, color=GREY, shrinkA=0, shrinkB=0))
        for group, dy, offset in [("no_go", .15, 2.2), ("go", -.15, -2.2)]:
            color = EXPERT_COLORS[group]
            item = expert[group][metric]
            value = 100 * item["rate"]
            low, high = np.array(item["ci95_case_clustered"]) * 100
            aa.errorbar(value, y+dy, xerr=[[value-low], [high-value]], fmt="o",
                        markersize=3, color=color, markeredgewidth=.65,
                        markerfacecolor="white" if group=="no_go" else color,
                        elinewidth=.65, capsize=1.5, capthick=.55, zorder=3)
            aa.annotate(f"{value:.0f}", (value, y+dy), xytext=(0,offset),
                        textcoords="offset points", ha="center",
                        va="bottom" if offset>0 else "top", fontsize=7, color=color)
    for y in [.5, 1.5]:
        aa.axhline(y, color=GRID, linewidth=.4, zorder=0)
    records_b, records_c = [], []
    for ax, label_x in [(ab, 138), (ac, 272)]:
        transform = blended_transform_factory(fig.transFigure, ax.transData)
        ax.axhspan(3.5, 4.55, color="#F1F5F9", zorder=0)
        for row, (_, label) in enumerate(CONDITIONS):
            y = 4-row
            ax.text(label_x/WIDTH, y, label, transform=transform, fontsize=7,
                    va="center", ha="left", fontweight="bold" if row==0 else "normal")
            if row<4:
                ax.axhline(y-.5, color=GRID, linewidth=.4, zorder=0)
    for row, (condition, _) in enumerate(CONDITIONS):
        for system, _, marker, offset in MODELS:
            item = controls["systems"][system][condition]
            assert (item["tasks"], item["trials"], item["attempts_per_task"]) == (32,96,3)
            y = 4-row+offset
            for key in ["stop_right", "go_right"]:
                color = MODEL_COLORS[system]
                value = item[key]*100
                point_y = y + (.11 if key=="stop_right" else -.11)
                ab.plot(value, point_y, marker=marker, markersize=3.2, linestyle="none",
                        markeredgecolor=color, markeredgewidth=.65,
                        markerfacecolor="white" if key=="stop_right" else color, zorder=3)
                records_b.append(dict(system=system, condition=condition,
                                      metric=key, accuracy_percent=value))
            attempts = item["both"]
            assert len(attempts)==3 and all(0<=v<=16 for v in attempts)
            mean = float(np.mean(attempts))
            model_color = MODEL_COLORS[system]
            attempt_color = to_hex(.55*np.array(to_rgb(model_color)) + .45)
            # Attempt markers sit above their corresponding mean, with tiny
            # deterministic vertical offsets so coincident counts remain visible.
            ac.plot(attempts, [y+.12+v for v in [-.06,0,.06]], linestyle="none",
                    marker=marker, markersize=1.8, markerfacecolor=attempt_color,
                    markeredgecolor=attempt_color, markeredgewidth=.3, zorder=3)
            ac.plot(mean, y-.12, marker=marker, markersize=3.3, linestyle="none",
                    color=model_color, markeredgewidth=.5, zorder=4)
            records_c.append(dict(system=system, condition=condition,
                                  attempts=attempts, mean_pairs_correct=mean, pairs_per_attempt=16))
    text(fig, 64, 5, "Rate (%)", color=INK)
    text(fig, 192, 5, "Accuracy (%)", color=INK)
    text(fig, 311, 5, "Pairs correct / 16", color=INK)
    return fig, records_b, records_c


def main():
    require_input(CONTROL_SOURCE, "written by scripts/control_replicated.py from the retained harbor/jobs/ctl-* trials")
    expert = figure_data(json.loads(EXPERT_SOURCE.read_text()))
    controls = json.loads(CONTROL_SOURCE.read_text())
    fig, panel_b, panel_c = draw(expert, controls)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT.with_suffix(".pdf"), metadata={"CreationDate":None,"ModDate":None})
    fig.savefig(OUT.with_suffix(".svg"), metadata={"Date":None})
    fig.savefig(OUT.with_suffix(".png"), dpi=300)
    plt.close(fig)
    svg_path = OUT.with_suffix(".svg")
    svg_path.write_text("\n".join(s.rstrip() for s in svg_path.read_text().splitlines())+"\n")
    svg = ET.parse(svg_path)
    texts = svg.findall(".//{http://www.w3.org/2000/svg}text")
    assert len(texts)>40 and not svg.findall(".//{http://www.w3.org/2000/svg}image")
    report = {
        "sources": [{"path":str(p.relative_to(ROOT)), "sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
                    for p in [EXPERT_SOURCE, CONTROL_SOURCE]],
        "figure_size_pdf_pt":[WIDTH,HEIGHT], "font":"Helvetica", "text_size_pt":7,
        "panel_heading_size_pt":8, "svg_editable_text_elements":len(texts), "raster_elements":0,
        "header_layout":"Panel titles and one aligned shared legend row; no subtitles.",
        "plot_height_pt":PLOT_HEIGHT,
        "legend_typography":{"family":"Helvetica", "size_pt":7, "weight":"normal",
                             "baseline_from_bottom_pt":114, "marker_size_pt":3},
        "model_display_names":{system:label for system,label,_,_ in MODELS},
        "A":{"estimates":expert, "outcome_colors":EXPERT_COLORS,
             "outcome_markers":{"no_go":"open", "go":"filled"},
             "intervals":"case-clustered percentile 95% CIs",
             "bootstrap_draws":4000,"bootstrap_seed":20260919},
        "B":{"estimates":panel_b, "model_colors":MODEL_COLORS,
             "outcome_markers":{"no_go":"open", "go":"filled"},
             "intervals":"Contrasts against plain are in Appendix H."},
        "C":{"estimates":panel_c,
             "model_colors":MODEL_COLORS,
             "palette_source":"paper/iclr/figures/figure04_results_summary.svg (main-text Figure 4)",
             "definition":"Within each attempt index, of 16 matched forks, count those correct on both the no-go task and its go twin.",
             "markers":"Small pale model-colored markers: individual attempts. Large saturated markers: three-attempt mean. No confidence intervals encoded."},
    }
    (ROOT/"output/research/figure5-triptych-data-20260923.json").write_text(json.dumps(report,indent=2)+"\n")
    print(OUT.with_suffix(".svg"))


if __name__=="__main__":
    main()
