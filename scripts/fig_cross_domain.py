#!/usr/bin/env python3
"""Plot the frozen portability results; no experiment or scorer is rerun."""
from pathlib import Path
import hashlib
import json
import re
import statistics

import fitz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "output/research/portability_pilot"
OUT = ROOT / "paper/iclr/figures/figure15_cross_domain"
MODELS = ["GPT-6-astra", "GPT-5.6-sol", "GPT-5.6-luna"]
KINDS = ["NO-GO", "DIVERT", "GO"]
FORKS = json.loads((DATA / "forks.json").read_text())
TRIALS = json.loads((DATA / "trials.json").read_text())


def count(rows):
    return [sum(r["verdict"] == "correct" for r in rows), len(rows)]


def select(model=None, brief="protocol", attempt=None, case=None, point=None, kind=None):
    return [r for r in FORKS
            if (model is None or r["system"].split(" [")[0] == model)
            and ("[thresholds-only]" in r["system"]) == (brief == "thresholds")
            and (attempt is None or r["attempt"] == attempt)
            and (case is None or r["case_id"] == case)
            and (point is None or r["point"] == point)
            and (kind is None or r["kind"] == kind)]


protocol = [[count(select(model=m, kind=k)) for k in KINDS] for m in MODELS]
assert protocol == [[[22, 24], [12, 12], [102, 102]],
                    [[23, 24], [11, 12], [96, 102]],
                    [[17, 24], [6, 12], [90, 102]]]
strata = [("RNA-seq", "adb_c40", None), ("GWAS", "adb_c41", None),
          ("GWAS structure", "adb_c41", "M_strat")]
control = [[count(select(brief=b, attempt=1, case=c, point=p, kind="NO-GO"))
            for b in ["protocol", "thresholds"]] for _, c, p in strata]
assert control == [[[12, 12], [12, 12]], [[8, 12], [5, 12]], [[4, 6], [0, 6]]]
assert [count(select(brief=b, attempt=1, kind="NO-GO"))
        for b in ["protocol", "thresholds"]] == [[20, 24], [17, 24]]
wrong = [r for r in select(kind="NO-GO") if r["verdict"] != "correct"]
assert len(wrong) == 10 and sum(r["own_numbers"] == "agree" for r in wrong) == 9
assert len(TRIALS) == 192 and len(FORKS) == 552
assert len({r["task_id"] for r in TRIALS}) == 16
assert len({(r["system"], r["task_id"], r["attempt"]) for r in TRIALS}) == 192

# Cross-check every original appendix-table count and reward against frozen records.
table = (ROOT / "paper/iclr/tab_portability.tex").read_text()
for line in table.splitlines():
    if not line.startswith("GPT-") or " & " not in line:
        continue
    cells = [s.strip().rstrip("\\").strip() for s in line.split("&")]
    if len(cells) != 8 or cells[1] not in {"protocol", "thresholds"}:
        continue
    model, brief = cells[:2]
    for kind, cell in zip(KINDS, cells[2:5]):
        assert count(select(model=model, brief=brief, kind=kind)) == list(map(int, cell.split("/")))
    key = model + (" [thresholds-only]" if brief == "thresholds" else "")
    for tier, cell in zip(["A-proceed", "B-divert", "C-stop"], cells[5:]):
        values = [r["reward"] for r in TRIALS if r["system"] == key and r["tier"] == tier]
        assert f"{statistics.mean(values):.2f}" == cell

oracle_logs = sorted((DATA / "e2e-v2").glob("*.log"))
assert len(oracle_logs) == 16
for path in oracle_logs:
    text = path.read_text()
    assert re.search(r'"reward":\s*1\.0\b', text) and "== PASS" in text

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "pdf.fonttype": 42, "svg.fonttype": "none",
                     "axes.spines.top": False, "axes.spines.right": False})
fig = plt.figure(figsize=(7.2, 2.05), facecolor="white")
ax = fig.add_axes([.205, .25, .285, .55])
bx = fig.add_axes([.69, .25, .28, .55])
fig.text(.015, .935, "(a) Decision accuracy", fontsize=11.4, weight="bold", color="#203545")
fig.text(.53, .935, "(b) Brief control", fontsize=11.4, weight="bold", color="#203545")
fig.text(.015, .825, "Protocol brief · 3 attempts", fontsize=9.2, color="#5a6974")
fig.text(.53, .825, "NO-GO · first attempt only", fontsize=9.2, color="#5a6974")
cmap = LinearSegmentedColormap.from_list("cross_domain", ["#edf4fc", "#21679b"])
rates = np.array([[100*w/n for w, n in row] for row in protocol])
ax.imshow(rates, cmap=cmap, vmin=0, vmax=100, aspect="auto")
ax.set_xticks(range(3), KINDS, fontsize=9.6)
ax.set_yticks(range(3), MODELS, fontsize=9.8)
ax.tick_params(length=0, pad=6)
ax.set_xticks(np.arange(-.5, 3, 1), minor=True)
ax.set_yticks(np.arange(-.5, 3, 1), minor=True)
ax.grid(which="minor", color="white", linewidth=2)
ax.tick_params(which="minor", bottom=False, left=False)
for spine in ax.spines.values(): spine.set_visible(False)
for row in range(3):
    for col in range(3):
        w, n = protocol[row][col]
        ax.text(col, row, f"{w}/{n}", ha="center", va="center", fontsize=10.2,
                color="white" if rates[row, col] >= 70 else "#18354b")
cax = fig.add_axes([.205, .10, .285, .025])
cb = fig.colorbar(matplotlib.cm.ScalarMappable(norm=Normalize(0, 100), cmap=cmap),
                  cax=cax, orientation="horizontal", ticks=[0, 50, 100])
cb.outline.set_visible(False)
cb.ax.tick_params(length=0, labelsize=8, pad=2)
fig.text(.015, .095, "Correct (%)", fontsize=9, color="#5a6974")
colors = ["#157e79", "#d38b4f"]
for i, row in enumerate(control):
    for j, (w, n) in enumerate(row):
        y = i + (-.17 if j == 0 else .17)
        value = 100*w/n
        bx.barh(y, value, height=.32, color=colors[j], edgecolor="none")
        if w:
            bx.text(value-2.5, y, f"{w}/{n}", ha="right", va="center", fontsize=9.1,
                    color="white" if j == 0 else "#242f35")
        else:
            bx.plot(0, y, "o", color=colors[j], markersize=3, clip_on=False)
            bx.text(3, y, f"{w}/{n}", va="center", fontsize=9.1, color="#242f35")
bx.set_yticks(range(3), [x[0] for x in strata], fontsize=9.2)
bx.set_ylim(2.5, -.5)
bx.set_xlim(0, 101)
bx.set_xticks([0, 50, 100], ["0%", "50%", "100%"])
bx.tick_params(axis="both", labelsize=9, length=2, color="#bbc4ca")
bx.tick_params(axis="y", length=0, pad=5)
bx.set_axisbelow(True)
bx.grid(axis="x", color="#e4e9ec", linewidth=.65)
bx.spines["left"].set_visible(False)
bx.spines["bottom"].set_color("#c6cdd2")
for x, label, color in [(.575, "Protocol", colors[0]), (.765, "Thresholds only", colors[1])]:
    fig.patches.append(matplotlib.patches.Rectangle((x, .07), .015, .04,
                       transform=fig.transFigure, color=color, clip_on=False))
    fig.text(x+.025, .075, label, fontsize=9.1)
OUT.parent.mkdir(exist_ok=True)
for ext in ["pdf", "svg"]:
    fig.savefig(OUT.with_suffix("."+ext), facecolor="white")
plt.close(fig)
pdf = fitz.open(OUT.with_suffix(".pdf"))
pdf[0].get_pixmap(dpi=240).save(OUT.with_suffix(".png"))

detail = []
for model in MODELS:
    row = {"model": model, "counts": []}
    for _, case, point in strata:
        row["counts"].extend(count(select(model=model, brief=b, attempt=1,
                                         case=case, point=point, kind="NO-GO"))
                             for b in ["protocol", "thresholds"])
    detail.append(row)
report = {"source_sha256": {name: hashlib.sha256((DATA/name).read_bytes()).hexdigest()
                           for name in ["forks.json", "trials.json"]},
          "trials": len(TRIALS), "forks": len(FORKS), "reference_tasks_checked": 16,
          "reference_reward_all_one": True, "protocol": protocol, "control": control,
          "first_attempt_detail": detail, "wrong_no_go": 10, "diagnostics_imply_stop": 9,
          "statistics": "Descriptive counts; repeated forks are not treated as independent samples."}
(ROOT / "output/research/cross-domain-figure-data-20260924.json").write_text(json.dumps(report, indent=2)+"\n")
print("Verified 192 trials, 552 forks, 16 reference runs and all original table cells; figure exported.")
