"""Regenerate the canonical compact Task breakdown figure.

Run from the repository root: python3 scripts/fig_task_breakdown.py
Requires matplotlib, Pillow, PyMuPDF, Inkscape, and the full local case registry.
The accepted v5 preview supplies the hierarchy, four industry colors, and regular type.
The compact revision removes the duplicate title and uses 44% of the text width,
while keeping scenario labels at 7 pt in the final manuscript.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, to_rgb
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, Wedge
from PIL import Image
import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper/iclr/figures"
AUDIT = ROOT / "output/figures/figure3_task_breakdown"
STEM = "figure03_task_breakdown"
SVG = OUT / f"{STEM}.svg"
PDF = OUT / f"{STEM}.pdf"
PNG = OUT / f"{STEM}.png"
SOURCE = ROOT / "paper/iclr/dmaic_bench.tex"
sys.path.insert(0, str(ROOT))
from dmaic_bench.v2.registry import discover

SCALE = 0.88
W = H = 198 * SCALE
CX = CY = W / 2
R0, R1, R2 = (radius * SCALE for radius in (16, 49, 96))
BLUE, INK = "#263747", "#26313c"
INNER_INK = "#142431"
GROUPS = OrderedDict([
    ("discrete", {"label": "Discrete manufacturing", "color": "#669CCD",
                  "cases": [25, 29, 30, 34, 35, 37, 39]}),
    ("electronics", {"label": "Electronics", "color": "#CA866E",
                     "cases": [28, 31, 33, 36, 38]}),
    ("process", {"label": "Process industry", "color": "#79A597", "cases": [27, 32]}),
    ("services", {"label": "Services", "color": "#A38BB8", "cases": [26]}),
])
SCENARIOS = {
    25: ("Moulded dimension", ["Moulded", "dimension"]),
    29: ("Critical-characteristic capability", ["Capability"]),
    30: ("Bore surface finish", ["Bore", "finish"]),
    34: ("Coating thickness", ["Coating", "thickness"]),
    35: ("Dual dimensions", ["Dual", "dimensions"]),
    37: ("Heat-treatment hardness", ["Heat-treat", "hardness"]),
    39: ("Seal strength", ["Seal", "strength"]),
    28: ("Display brightness", ["Display", "brightness"]),
    31: ("BGA solder voids", ["BGA", "voids"]),
    33: ("Visual inspection agreement", ["Visual", "inspection"]),
    36: ("Wave-solder fillet height", ["Solder", "height"]),
    38: ("Capacitor defect rate", ["Capacitor", "defects"]),
    27: ("Batch yield", ["Batch", "yield"]),
    32: ("Appearance defect rate", ["Appearance", "defects"]),
    26: ("Service response compliance", ["Service", "response"]),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


protected = [SOURCE]  # inputs the script must leave byte-identical
before = {str(p.relative_to(ROOT)): sha(p) for p in protected}
table = SOURCE.read_text().split(r"\label{tab:corpus}", 1)[1].split(r"\end{table}", 1)[0]
rows = {}
for line in table.splitlines():
    if re.match(r"^\s*\d+\s*&", line):
        fields = [v.strip() for v in line.split("&")]
        case = int(fields[0])
        routes = [int(v) for v in fields[7].split("/")]
        rows[case] = {"case": case, "industry": fields[2], "tasks": int(fields[6]),
                      "route_counts": routes, "source_scenario": fields[1]}
        assert sum(routes) == rows[case]["tasks"]
cases = discover(include_held_out=True)
assert set(rows) == set(SCENARIOS)
assert sum(row["tasks"] for row in rows.values()) == 97
assert len(cases) == len(rows) == 15
for case, row in rows.items():
    assert len(cases[f"adb_c{case}"].seeds) == row["tasks"]
for industry, group in GROUPS.items():
    assert all(rows[case]["industry"] == industry for case in group["cases"])
    group["tasks"] = sum(rows[case]["tasks"] for case in group["cases"])
assert [g["tasks"] for g in GROUPS.values()] == [48, 31, 12, 6]

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 7, "svg.fonttype": "none", "svg.hashsalt": "task-breakdown-compact-v6",
    "axes.unicode_minus": False, "savefig.facecolor": "white", "path.simplify": False,
})
fig = plt.figure(figsize=(W / 72, H / 72), dpi=144, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set(xlim=(0, W), ylim=(H, 0), aspect="equal")
ax.axis("off")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
labels, sectors, polygons = [], [], []


def point(radius, angle):
    theta = math.radians(angle)
    return CX + radius * SCALE * math.cos(theta), CY + radius * SCALE * math.sin(theta)


def measure(value, size, weight="normal"):
    fp = FontProperties(family="Helvetica", size=size, weight=weight)
    width, height, descent = renderer.get_text_width_height_descent(value, fp, False)
    return width * 72 / fig.dpi, height * 72 / fig.dpi


def text(x, y, value, size=7, color=INK, weight="normal", angle=0, group="", gid=None):
    artist = ax.text(x, y, value, fontsize=size, color=color, fontweight=weight,
                     ha="center", va="center", rotation=-angle, rotation_mode="anchor",
                     clip_on=False)
    if gid:
        artist.set_gid(gid)
    width, height = measure(value, size, weight)
    # Conservative oriented rectangles, including a little inter-label clearance.
    width += 0.8
    height = max(height, size * 0.9) + 0.5
    a = math.radians(angle)
    poly = [(x + u * math.cos(a) - v * math.sin(a),
             y + u * math.sin(a) + v * math.cos(a))
            for u, v in [(-width/2, -height/2), (width/2, -height/2),
                         (width/2, height/2), (-width/2, height/2)]]
    polygons.append({"text": value, "group": group, "poly": poly})
    labels.append((artist, group))
    return artist


def curved(value, radius, angle, group, size=7.3, weight="normal"):
    width = measure(value, size, weight)[0]
    direction = -1 if math.sin(math.radians(angle)) > 0 else 1
    for i, char in enumerate(value):
        if char == " ":
            continue
        advance = (measure(value[:i], size, weight)[0] +
                   measure(value[:i + 1], size, weight)[0]) / 2 - width / 2
        a = angle + direction * math.degrees(advance / (radius * SCALE))
        x, y = point(radius, a)
        tangent = a + 90 if direction == 1 else a - 90
        text(x, y, char, size, INNER_INK, weight, tangent, group)


def lighten(color, white_fraction):
    return to_hex(tuple(c * (1-white_fraction) + white_fraction for c in to_rgb(color)))


angle = -180.0
for industry, group in GROUPS.items():
    stop = angle + 360 * group["tasks"] / 97
    inner = Wedge((CX, CY), R1, angle, stop, width=R1 - R0,
                  facecolor=group["color"], edgecolor="white", linewidth=0.85)
    inner.set_gid(f"industry-{industry}")
    ax.add_patch(inner)
    sectors.append({"id": industry, "level": "industry", "count": group["tasks"],
                    "start_deg": angle, "end_deg": stop, "inner_r": R0, "outer_r": R1})
    midpoint = (angle + stop) / 2
    if industry == "discrete":
        curved("Discrete", 41.0, midpoint, industry, 7.5, "normal")
        curved("manufacturing", 29.0, midpoint, industry, 7.2)
    elif industry == "electronics":
        curved("Electronics", 34.0, midpoint, industry, 7.6, "normal")
    elif industry == "process":
        label_angle = midpoint - 3.0
        radial = label_angle + 180
        rad = math.radians(radial)
        x, y = point(34.0, label_angle)
        for j, line in enumerate(["Process", "industry"]):
            offset = (j - 0.5) * 7.9
            text(x - offset * math.sin(rad), y + offset * math.cos(rad), line,
                 7.0, INNER_INK, angle=radial, group=industry)
    else:
        radial = midpoint + 180
        text(*point(32.5, midpoint), "Services", 7.0, INNER_INK, angle=radial, group=industry)

    child_start = angle
    for i, case in enumerate(group["cases"]):
        row = rows[case]
        child_stop = child_start + 360 * row["tasks"] / 97
        shade = [0.38, 0.49, 0.43, 0.55, 0.34, 0.47, 0.40][i % 7]
        patch = Wedge((CX, CY), R2, child_start, child_stop, width=R2 - R1,
                      facecolor=lighten(group["color"], shade), edgecolor="white", linewidth=0.65)
        patch.set_gid(f"scenario-adb_c{case}")
        ax.add_patch(patch)
        mid = (child_start + child_stop) / 2
        readable = mid if math.cos(math.radians(mid)) >= 0 else mid + 180
        rad = math.radians(readable)
        x, y = point(71.5 if case in (32, 35) else 69.0, mid)
        name, lines = SCENARIOS[case]
        for j, line in enumerate(lines):
            offset = (j - (len(lines)-1)/2) * 7.9
            text(x - offset * math.sin(rad), y + offset * math.cos(rad), line,
                 7.0, INK, angle=readable, group=f"case-{case}", gid=f"label-adb_c{case}-{j}")
        count_x, count_y = point(92.0, mid)
        if case == 32:
            count_x -= 6.0 * math.sin(rad)
            count_y += 6.0 * math.cos(rad)
        elif case == 35:
            count_x += 4.0 * math.sin(rad)
            count_y -= 4.0 * math.cos(rad)
        text(count_x, count_y, str(row["tasks"]), 7.3, BLUE, "normal",
             group=f"count-{case}", gid=f"count-adb_c{case}")
        sectors.append({"id": f"adb_c{case}", "level": "scenario", "parent": industry,
                        "name": name, "count": row["tasks"], "label_lines": lines,
                        "start_deg": child_start, "end_deg": child_stop,
                        "inner_r": R1, "outer_r": R2})
        child_start = child_stop
    assert abs(child_start - stop) < 1e-9
    angle = stop
assert abs(angle - 180) < 1e-9

ax.add_patch(Circle((CX, CY), R0, facecolor="white", edgecolor="white", linewidth=0.65))
text(CX, CY - 3.3, "97", 13.0, BLUE, "normal", group="total", gid="total-tasks")
text(CX, CY + 8.2, "tasks", 7.2, INK, group="total", gid="total-unit")


def intersect(a, b):
    # Separating-axis test for the rotated text rectangles.
    for poly in [a, b]:
        for i in range(len(poly)):
            p, q = poly[i], poly[(i + 1) % len(poly)]
            axis = (-(q[1] - p[1]), q[0] - p[0])
            pa = [x*axis[0] + y*axis[1] for x, y in a]
            pb = [x*axis[0] + y*axis[1] for x, y in b]
            if max(pa) <= min(pb) or max(pb) <= min(pa):
                return False
    return True


overlaps = []
for i, a in enumerate(polygons):
    for b in polygons[:i]:
        if a["group"] != b["group"] and intersect(a["poly"], b["poly"]):
            overlaps.append([a["group"], a["text"], b["group"], b["text"]])
outside = [p["group"] for p in polygons if any(x < 0 or x > W or y < 0 or y > H for x, y in p["poly"])]

OUT.mkdir(parents=True, exist_ok=True)
AUDIT.mkdir(parents=True, exist_ok=True)
fig.savefig(SVG, format="svg", metadata={"Title": "Task breakdown", "Date": None,
              "Description": "97 task instances grouped into four industries and fifteen case scenarios. Every sector angle is proportional to task count. Four industry hues extend to lighter child sectors. All labels use regular font weight."})
ET.register_namespace("", "http://www.w3.org/2000/svg")
tree = ET.parse(SVG)
root = tree.getroot()
root.set("role", "img")
root.set("aria-label", "Task breakdown: 97 tasks across 4 industries and 15 scenarios")
title = ET.Element("{http://www.w3.org/2000/svg}title")
title.text = "Task breakdown"
root.insert(0, title)
desc = ET.Element("{http://www.w3.org/2000/svg}desc")
desc.text = "; ".join(f"{g['label']}: {g['tasks']} tasks" for g in GROUPS.values()) + ". Sector angles show task counts. All fifteen scenario labels are editable text."
root.insert(1, desc)
tree.write(SVG, encoding="utf-8", xml_declaration=True)
subprocess.run(["/opt/homebrew/bin/inkscape", str(SVG), "--export-background=white",
                f"--export-filename={PNG}", "--export-width=1584"], check=True)
subprocess.run(["/opt/homebrew/bin/inkscape", str(SVG),
                f"--export-filename={PDF}"], check=True)
with Image.open(PNG) as im:
    im.convert("L").save(AUDIT / "grayscale_check.png")
    im.resize((round(W * 2), round(H * 2)), Image.Resampling.LANCZOS).save(AUDIT / "single_column_check.png")

with (AUDIT / "scenario_map.csv").open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["case_id", "industry", "scenario", "tasks", "go", "divert", "stop"])
    for g in GROUPS.values():
        for case in g["cases"]:
            r = rows[case]
            writer.writerow([f"adb_c{case}", r["industry"], SCENARIOS[case][0], r["tasks"], *r["route_counts"]])

pdf = fitz.open(PDF)
assert len(pdf) == 1
assert abs(pdf[0].rect.width - W) < 0.01 and abs(pdf[0].rect.height - H) < 0.01
pdf_spans = [span for block in pdf[0].get_text("dict")["blocks"]
             for line in block.get("lines", []) for span in line["spans"]]
assert pdf_spans and all(not (span["flags"] & 16) for span in pdf_spans)
assert not pdf[0].get_images(full=True)
report = {
    "preview_only": False, "approved_preview": "figure3_task_breakdown_preview_v5",
    "revision": "compact-v6", "visible_title": False,
    "size_pt": [W, H], "target_manuscript_width": "0.44 textwidth",
    "task_count": 97, "industry_count": 4, "scenario_count": 15,
    "industry_colors": {k: v["color"] for k, v in GROUPS.items()},
    "font_weights": sorted({a.get_fontweight() for a, _ in labels}),
    "color_rule": "Each industry has one hue; scenario sectors use lighter shades of the same hue.",
    "count_sources": ["manuscript corpus table", "V2Case.seeds, all 15 cases"],
    "sectors": sectors, "minimum_font_pt": min(a.get_fontsize() for a, _ in labels),
    "text_overlaps": overlaps, "outside_canvas": outside,
    "pdf_font_names": sorted({span["font"] for span in pdf_spans}),
    "pdf_image_count": len(pdf[0].get_images(full=True)),
    "svg_embedded_images": len(root.findall(".//{http://www.w3.org/2000/svg}image")),
    "source_sha256": before,
    "protected_files_unchanged": all(sha(ROOT / p) == value for p, value in before.items()),
}
(AUDIT / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: report[k] for k in ["size_pt", "task_count", "scenario_count", "minimum_font_pt", "text_overlaps", "outside_canvas", "svg_embedded_images", "protected_files_unchanged"]}, indent=2))
assert not overlaps, overlaps
assert not outside, outside
