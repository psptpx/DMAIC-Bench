"""Shared physical size and typography for the adjacent Figures 5 and 6."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# LaTeX includes each panel at height=145pt. Matching that physical height here
# prevents two nominally identical font sizes from receiving different scaling.
DISPLAY_HEIGHT_TEX_PT = 145
FIGURE_SIZE = (2.53, DISPLAY_HEIGHT_TEX_PT / 72.27)
FONT_SIZE = 7
AXES_BOTTOM = 0.20
AXES_HEIGHT = 0.60
LEGEND_TOP = 0.998
FOOTER_Y = 0.048


def apply_style():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": FONT_SIZE,
        "font.weight": "normal",
        "axes.labelsize": FONT_SIZE,
        "xtick.labelsize": FONT_SIZE,
        "ytick.labelsize": FONT_SIZE,
        "legend.fontsize": FONT_SIZE,
        "text.color": "#202830",
        "axes.labelcolor": "#202830",
        "xtick.color": "#596570",
        "ytick.color": "#202830",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "savefig.facecolor": "white",
    })


def direction_arrow(fig, x, y, *, upward):
    """A fixed 6 pt vector arrow; Helvetica has no up/down arrow glyphs."""
    half_height = 3 / (FIGURE_SIZE[1] * 72)
    start, end = y - half_height, y + half_height
    if not upward:
        start, end = end, start
    fig.add_artist(FancyArrowPatch(
        (x, start), (x, end), transform=fig.transFigure,
        arrowstyle="->", mutation_scale=6, linewidth=0.65,
        color="#596570", shrinkA=0, shrinkB=0,
    ))
