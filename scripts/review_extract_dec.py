#!/usr/bin/env python3
"""Dump the per-decision records that restraint_analysis.py builds (DEC: system -> [(case, fork, kind, wrong)])
plus the matched-fork set, without editing the tracked script. Run from the repo root:

    PYTHONPATH=.:harbor/src:scripts python3 <this file> <out.json>
"""
import json, sys, time
from collections import defaultdict
sys.path[:0] = [".", "harbor/src", "scripts"]
import restraint_analysis as RA

t0 = time.time()
cases = RA.V.discover()
DEC = {}; forks = defaultdict(lambda: {"NO-GO": [], "GO": []}); skipped = []
for name, vendor, k1, k3 in RA.SYSTEMS:
    rows = RA.load_rows(k1)
    if len(rows) != 97:
        skipped.append((name, len(rows))); continue
    recs = []
    for r, p, v, own, strict, order in RA.decisions(rows, cases):
        kind = "NO-GO" if RA.is_stop(p) else "GO"
        wrong = v != "correct"
        forks[(r["case_id"], p["point_id"])][kind].append((name, wrong))
        recs.append((r["case_id"], p["point_id"], kind, int(wrong)))
    DEC[name] = recs
    print(name, len(recs), f"{time.time()-t0:.1f}s", flush=True)
matched = sorted([f"{c}|{p}" for (c, p), v in forks.items() if v["NO-GO"] and v["GO"]])
json.dump({"DEC": DEC, "matched": matched, "skipped": skipped}, open(sys.argv[1], "w"))
print("systems", len(DEC), "matched forks", len(matched), "skipped", skipped)
