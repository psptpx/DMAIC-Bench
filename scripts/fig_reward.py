#!/usr/bin/env python3
"""The anatomy of the reward, as a picture (replaces the component table in Section 3.3).

    python3 scripts/fig_reward.py   ->  paper/iclr/figures/figure10_reward_components.{pdf,png}
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

OUT = Path("paper/iclr/figures")
INK, GREY = "#222222", "#6a6a6a"
SRC_C, COMP_C, PEN_C, GATE_C, OUT_C = "#e8e8e8", "#d6e6f5", "#f6d5d0", "#fbe3d3", "#dff0da"


def box(ax, x, y, w, h, title, body, fc, tsize=6.6, bsize=5.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.04", fc=fc, ec="#444444", lw=0.6))
    ax.text(x + w / 2, y + h - 0.075, title, ha="center", va="top", fontsize=tsize, fontweight="bold", color=INK)
    if body:
        ax.text(x + w / 2, y + 0.06, body, ha="center", va="bottom", fontsize=bsize, color=INK, linespacing=1.2)


def arrow(ax, p, q, color="#444444", lw=0.7, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=6, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=1, shrinkB=1, zorder=3))


def main():
    """Three aligned columns, straight arrows only: what is read -> what is scored -> the reward."""
    plt.rcParams.update({"font.family": "Helvetica", "pdf.fonttype": 42})
    W, H = 5.5, 2.12
    fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    rows = [1.62, 1.33, 1.04, 0.75, 0.46, 0.17]            # six score rows, top to bottom (card bottoms)
    rh = 0.25
    # column headers
    for x, txt in ((0.50, "what is read"), (2.30, "what is scored"), (4.52, "how it combines")):
        ax.text(x, 2.09, txt, ha="center", va="top", fontsize=6.4, color=GREY, style="italic")

    # column 1: inputs. The trace spans the four rows it feeds.
    def card(x, y, w, h, title, sub, fc, ts=6.4, ss=5.2):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.035", fc=fc, ec="#555555", lw=0.5))
        if sub:
            ax.text(x + 0.07, y + h / 2 + 0.055, title, ha="left", va="center", fontsize=ts, fontweight="bold", color=INK)
            ax.text(x + 0.07, y + h / 2 - 0.06, sub, ha="left", va="center", fontsize=ss, color=INK)
        else:
            ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=ts, fontweight="bold", color=INK)
    x1, w1 = 0.06, 0.90
    card(x1, rows[3], w1, rows[0] + rh - rows[3], "trace", "the analyses run,\nwith their outputs", SRC_C)
    card(x1, rows[4], w1, rh, "report", "the numbers it states", SRC_C)
    card(x1, rows[5], w1, rh, "access log", "every steward reply", SRC_C)

    # column 2: scores, one card per row
    x2, w2 = 1.42, 1.78
    scores = [("method recall", "the required analyses were run", COMP_C),
              ("method precision", "and little else (sanity checks exempt)", COMP_C),
              ("route", "each fork branched as the evidence licensed", COMP_C),
              ("method misuse", "a method whose assumptions the data violate", PEN_C),
              ("numeric fidelity", "reported values match recomputed truth", COMP_C),
              ("integrity gate", "0 if data the steward withheld was consumed", GATE_C)]
    for y, (tt, sub, fc) in zip(rows, scores):
        card(x2, y, w2, rh, tt, sub, fc, ts=6.2, ss=5.0)
        arrow(ax, (x1 + w1, y + rh / 2), (x2, y + rh / 2), color="#666666", lw=0.6)

    # column 3: the reward
    x3, w3 = 3.62, 1.82
    y3, h3 = rows[5], rows[0] + rh - rows[5]
    ax.add_patch(FancyBboxPatch((x3, y3), w3, h3, boxstyle="round,pad=0.01,rounding_size=0.035", fc=OUT_C, ec="#555555", lw=0.5))
    ax.text(x3 + w3 / 2, y3 + h3 - 0.16, "reward  $\\in$ [0, 1]", ha="center", va="center", fontsize=7.0, fontweight="bold", color=INK)
    ax.text(x3 + w3 / 2, y3 + h3 - 0.50, "harmonic mean of the four\ncompetencies (blue)", ha="center", va="center", fontsize=5.6, color=INK, linespacing=1.25)
    ax.text(x3 + w3 / 2, y3 + h3 - 0.84, "$\\times$ (1 $-$ misuse)   $\\times$ gate", ha="center", va="center", fontsize=6.2, color=INK)
    ax.plot([x3 + 0.18, x3 + w3 - 0.18], [y3 + 0.62, y3 + 0.62], color="#8aa889", lw=0.5)
    ax.text(x3 + w3 / 2, y3 + 0.44, "any competency at zero pulls the\nreward to zero", ha="center", va="center", fontsize=5.2, color=INK, linespacing=1.25)
    ax.text(x3 + w3 / 2, y3 + 0.14, "reference solution 1.000 on every task;\nnull agent 0.000", ha="center", va="center", fontsize=5.2, color=GREY, linespacing=1.25)
    # one bracket from the score column into the reward card
    ax.plot([x2 + w2 + 0.10, x2 + w2 + 0.10], [rows[5] + rh / 2, rows[0] + rh / 2], color="#666666", lw=0.6)
    for y in rows:
        ax.plot([x2 + w2, x2 + w2 + 0.10], [y + rh / 2, y + rh / 2], color="#666666", lw=0.6)
    arrow(ax, (x2 + w2 + 0.10, (rows[0] + rows[5] + rh) / 2), (x3, (rows[0] + rows[5] + rh) / 2), color="#666666", lw=0.8)

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "figure10_reward_components.pdf"); fig.savefig(OUT / "figure10_reward_components.png", dpi=300); print("ok")


if __name__ == "__main__":
    main()
