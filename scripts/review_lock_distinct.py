"""Count the distinct lockable no-go forks per precondition type on the retained baseline job.

    PYTHONPATH=.:harbor/src:scripts python3 scripts/review_lock_distinct.py
"""
import sys
from collections import defaultdict
sys.path[:0] = [".", "harbor/src", "scripts"]
import restraint_analysis as RA, lockability as LK
from dmaic_harbor import v2_tasks as V
cases = RA.V.discover(); rows = RA.load_rows(["gpt6astra-97"])
forks = defaultdict(lambda: {"nogo": 0, "types": None})
for r, p, *_ in RA.decisions(rows, cases):
    c = cases[r["case_id"]]; f = forks[(r["case_id"], p["point_id"])]
    if RA.is_stop(p): f["nogo"] += 1
    if f["types"] is None:
        atoms = set()
        for e in c.graph.edges_from(p["point_id"]):
            for a in RA._FIELD_RE.findall(e.when or ""):
                if not a[0].isdigit(): atoms.add(a.split(".")[-1].lower())
        f["types"] = {LK.atom_type(a) for a in atoms}
        blocks = V.data_nodes(c); src = blocks.get(p["point_id"])
        targets = [e.target for e in c.graph.edges_from(p["point_id"])]
        f["cross"] = any(blocks.get(t) not in (None, src) for t in targets)
        lk = V.locks(c); own = {g for _t, g in f["types"] if g}
        f["locked"] = any(own & set(lk.get(blocks.get(t), {}).get("gates") or []) for t in targets)
ng = {k: f for k, f in forks.items() if f["nogo"]}
print("distinct: forks", len(ng), "decisions", sum(f["nogo"] for f in ng.values()),
      "cross", sum(f["cross"] for f in ng.values()), "locked", sum(f["locked"] for f in ng.values()))
print("row-sum: forks", sum(len(f["types"]) for f in ng.values()), "decisions", sum(len(f["types"])*f["nogo"] for f in ng.values()),
      "cross", sum(len(f["types"])*f["cross"] for f in ng.values()), "locked", sum(len(f["types"])*f["locked"] for f in ng.values()))
