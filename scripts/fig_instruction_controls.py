#!/usr/bin/env python3
"""One compact panel for the replicated instruction controls, matching Figure 5.

Run scripts/control_replicated.py first to regenerate the numeric source from
retained trials. The SVG retains editable Helvetica labels and no raster assets.
The PDF is the vector export included by LaTeX; PNG is a review preview.
"""
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from figure_pair_style import (
    FIGURE_SIZE, FONT_SIZE, AXES_BOTTOM, AXES_HEIGHT, LEGEND_TOP, FOOTER_Y,
    DISPLAY_HEIGHT_TEX_PT, apply_style,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "output/research/control-replication-20260922.json"
OUT = ROOT / "paper/iclr/figure_archive/generated/figure_instruction_controls"


def require_input(path, producer):
    """Exit with a plain message when a run-artifact input is absent from the checkout."""
    if not Path(path).exists():
        sys.exit(f"missing input {path}: this file is not part of the tracked tree. It comes from "
                 f"the run-artifact archive ({producer}); see scripts/README.md, Analysis inputs.")
NO_GO, GO, INK = "#B85E21", "#0072B2", "#202830"
CONDITIONS = [
    ("plain", "Plain"),
    ("permit-stop", "Permit-stop"),
    ("permit-paraphrase", "Paraphrase"),
    ("normative", "Normative"),
    ("remind", "Remind"),
]


def main():
    require_input(SOURCE, "written by scripts/control_replicated.py from the retained harbor/jobs/ctl-* trials")
    data = json.loads(SOURCE.read_text())
    apply_style()
    plt.rcParams["svg.hashsalt"] = "dmaic-instruction-controls"
    fig = plt.figure(figsize=FIGURE_SIZE)
    ax = fig.add_axes([0.325, AXES_BOTTOM, 0.64, AXES_HEIGHT])
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 4.6)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_yticks([])
    ax.tick_params(axis="x", labelsize=FONT_SIZE, length=2, pad=2.5, width=0.45)
    ax.xaxis.grid(True, color="#E8EDF1", linewidth=0.4)
    ax.set_axisbelow(True)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#AFBAC3")
    ax.spines["bottom"].set_linewidth(0.45)
    # A quiet baseline band and two concentric rings establish the reading focus.
    # Ring size is decorative emphasis; it does not encode uncertainty or counts.
    ax.add_patch(Rectangle((-0.475, 3.5), 1.495, 1.1,
                           transform=ax.get_yaxis_transform(),
                           facecolor="#F1F5F9", edgecolor="none",
                           clip_on=False, zorder=0.1))
    ax.plot([-0.475, -0.475], [3.5, 4.6], transform=ax.get_yaxis_transform(),
            color="#9BB1C3", linewidth=1.0, solid_capstyle="butt", clip_on=False)
    baseline = data["systems"]["GPT-6-astra"]["plain"]
    baseline_gap = 100 * (baseline["go_right"] - baseline["stop_right"])
    ax.text(51, 4.25, f"{baseline_gap:.0f} pp gap", ha="center", va="center",
            fontsize=FONT_SIZE, fontweight="normal", color="#596570", zorder=4)
    records = []
    models = (("GPT-6-astra", "o", 0.25), ("DeepSeek-v4-pro", "s", -0.25))
    for row, (condition, label) in enumerate(CONDITIONS):
        y = 4 - row
        ax.text(-0.09, y, label, transform=ax.get_yaxis_transform(),
                ha="right", va="center", fontsize=FONT_SIZE,
                fontweight="bold" if condition == "plain" else "normal",
                color="#08519c" if condition == "plain" else INK)
        for system, marker, model_offset in models:
            item = data["systems"][system][condition]
            assert item["tasks"] == 32 and item["trials"] == 96 and item["attempts_per_task"] == 3
            for key, color, dy, dx, align in (("stop_right", NO_GO, 0.09, -3.5, "right"),
                                               ("go_right", GO, -0.09, 3.5, "left")):
                value = item[key] * 100
                point_y = y + model_offset + dy
                focused = condition == "plain" and system == "GPT-6-astra"
                if focused:
                    ax.plot(value, point_y, marker="o", markersize=7.0,
                            markerfacecolor="white", markeredgecolor=color,
                            markeredgewidth=0.65, linestyle="none", zorder=3,
                            clip_on=False)
                ax.plot(value, point_y, marker=marker, markersize=2.7,
                        markerfacecolor="white" if key == "stop_right" else color,
                        markeredgecolor=color, markeredgewidth=0.55, linestyle="none", zorder=4)
                label_dx = (-6.2 if key == "stop_right" else 6.2) if focused else dx
                ax.annotate(f"{value:.0f}", (value, point_y), xytext=(label_dx, 0),
                            textcoords="offset points", ha=align, va="center",
                            fontsize=FONT_SIZE, fontweight="bold" if focused else "normal", color=color)
                records.append({"system": system, "condition": condition, "metric": key,
                                "accuracy_percent": value, "display": f"{value:.0f}"})
        if row < 4:
            ax.axhline(y - 0.5, color="#E8EDF1", linewidth=0.4, zorder=0)
    fig.legend(handles=[
        Line2D([], [], color=INK, marker=marker, markerfacecolor="white", linestyle="none",
               markeredgewidth=0.55, markersize=2.7, label=system)
        for system, marker, _ in models
    ], loc="upper center", bbox_to_anchor=(0.51, LEGEND_TOP), ncol=2, frameon=False,
        fontsize=FONT_SIZE, handlelength=0.7, handletextpad=0.45, columnspacing=1.1, borderaxespad=0)
    fig.legend(handles=[
        Line2D([], [], color=NO_GO, linewidth=0.8, label="NO-GO"),
        Line2D([], [], color=GO, linewidth=0.8, label="GO"),
    ], loc="upper center", bbox_to_anchor=(0.55, 0.902), ncol=2, frameon=False,
        fontsize=FONT_SIZE, handlelength=1.0, handletextpad=0.5, columnspacing=1.3, borderaxespad=0)
    fig.text(0.645, FOOTER_Y, "Decision accuracy (%)", ha="center", va="center", fontsize=FONT_SIZE)
    assert len(fig.axes) == 1, "Figure must remain a single panel"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT.with_suffix(".svg"), metadata={"Date": None})
    fig.savefig(OUT.with_suffix(".pdf"), metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(OUT.with_suffix(".png"), dpi=260)
    plt.close(fig)
    svg = ET.parse(OUT.with_suffix(".svg"))
    assert not svg.findall(".//{http://www.w3.org/2000/svg}image"), "Raster image in SVG"
    assert len(svg.findall(".//{http://www.w3.org/2000/svg}text")) == 36, "Editable labels missing"
    report = {
        "source": str(SOURCE.relative_to(ROOT)),
        "figure_size_pt": [v * 72 for v in FIGURE_SIZE],
        "panels": 1, "placement_height_tex_pt": DISPLAY_HEIGHT_TEX_PT,
        "font": "Helvetica", "label_size_pt": [FONT_SIZE, FONT_SIZE],
        "font_weight": "regular, with the Plain label and two focused values bold",
        "model_markers": {system: marker for system, marker, _ in models},
        "marker_size_pt": 2.7, "rule_width_pt": 0.4,
        "no_go_color": NO_GO, "go_color": GO,
        "style_reference": "scripts/figure_pair_style.py and paper/figure_design/styles/DMAIC_PAPER_BLUE.md",
        "svg_editable_text": True, "raster_elements": 0,
        "focus": {"condition": "plain", "system": "GPT-6-astra",
                  "metrics": ["stop_right", "go_right"], "ring_diameter_pt": 7.0,
                  "gap_percentage_points": baseline_gap,
                  "gap_label": f"{baseline_gap:.0f} pp gap",
                  "band_color": "#F1F5F9", "note": "Visual emphasis only, not a confidence interval."},
        "note": "Point estimates. Case-clustered intervals for changes are in Appendix H.",
        "values": records,
    }
    (ROOT / "output/research/instruction-controls-figure-verification.json").write_text(
        json.dumps(report, indent=2) + "\n")
    print(OUT.with_suffix(".svg"))


if __name__ == "__main__":
    main()
