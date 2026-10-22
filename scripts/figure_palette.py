"""Shared heatmap palette: cold blue to hot red, matching Figures 1 and 2."""
from matplotlib.colors import LinearSegmentedColormap

HEAT_BLUE = '#3182BD'
HEAT_RED = '#A50F15'

def heatmap_cmap():
    return LinearSegmentedColormap.from_list('paper_cold_to_hot', [HEAT_BLUE, '#F7F7F7', HEAT_RED], N=256)

def text_on_color(rgba):
    """Choose black/white text by relative-luminance contrast."""
    channels = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgba[:3]]
    luminance = sum(w * c for w, c in zip([.2126, .7152, .0722], channels))
    return 'black' if luminance > .179 else 'white'
