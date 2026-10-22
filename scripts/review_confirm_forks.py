#!/usr/bin/env python3
"""Panel B, items 17/18: confirmation-fork decisions per agent/seed with error codes, and the
Table 7 counting basis. Run from the repo root: PYTHONPATH=.:harbor/src:scripts python3 <this>."""
import json, sys
from collections import Counter, defaultdict
sys.path[:0] = [".", "harbor/src", "scripts"]
import restraint_analysis as RA
from dmaic_harbor import v2_tasks as V

RAN = {"evidence", "divergent_evidence", "explicit", "explicit_contradicted", "declared_unsupported"}
def ecode(kind, v, via):
    if v == "correct": return "ok"
    if via == "abstained_from_required_branch": return "E5"
    if v == "unknown" or via in (None, "none"): return "E2" if kind == "NO-GO" else "E4"
    if via in RAN: return "E1" if kind == "NO-GO" else "E3"
    return f"?{v}/{via}"

cases = RA.V.discover()
CASES = ("adb_c36", "adb_c39", "adb_c38")
# ---- Part A: confirmation forks -------------------------------------------------------------
seeds_by_fork = defaultdict(lambda: defaultdict(set))      # (case, node) -> kind -> seeds
dec = []                                                   # per decision
for name, vendor, k1, _k3 in RA.SYSTEMS:
    rows = [r for r in RA.load_rows(k1) if r["case_id"] in CASES]
    for r, p, v, own, strict, order in RA.decisions(rows, cases):
        pid = p["point_id"]
        if "confirm" not in pid.lower() and pid != "I_level":
            continue
        kind = "NO-GO" if RA.is_stop(p) else "GO"
        seeds_by_fork[(r["case_id"], pid)][kind].add(int(r["seed"]))
        card = r["card"].get("scorecard") or {}
        det = next(d for d in (card.get("pq") or {}).get("details", [])
                   if d.get("kind") == "decision_point" and d.get("point_id") == pid)
        # what did the trace run after the fork? (methods on each branch)
        ran = set((card.get("ms") or {}).get("attempted") or [])
        dec.append(dict(system=name, case=r["case_id"], seed=int(r["seed"]), task=r["task_id"], fork=pid,
                        kind=kind, correct_branch=p["correct_branch"], verdict=v, via=det.get("via"),
                        code=ecode(kind, v, det.get("via")), own=own, strict=strict,
                        detail={k: det[k] for k in det if k not in ("kind", "point_id")},
                        ran=sorted(ran)))

print("== confirmation forks (and I_level for contrast): seeds by kind, correct branch per seed")
for key in sorted(seeds_by_fork):
    cb = {d["seed"]: d["correct_branch"] for d in dec if (d["case"], d["fork"]) == key}
    print(key, {k: sorted(s) for k, s in seeds_by_fork[key].items()}, "matched" if len(seeds_by_fork[key]) == 2 else "ONE-SIDED", cb)

print("\n== per fork x kind: n, wrong, error codes")
agg = defaultdict(Counter)
for d in dec:
    agg[(d["case"], d["fork"], d["kind"])]["n"] += 1
    if d["code"] != "ok":
        agg[(d["case"], d["fork"], d["kind"])]["wrong"] += 1
        agg[(d["case"], d["fork"], d["kind"])][d["code"] + ":" + str(d["via"])] += 1
for k in sorted(agg):
    print(k, dict(agg[k]))

print("\n== the wrong confirmation-fork decisions, one per line")
for d in sorted(dec, key=lambda d: (d["case"], d["fork"], d["kind"], d["seed"], d["system"])):
    if "confirm" in d["fork"].lower() and d["code"] != "ok":
        print(f"{d['case']} {d['fork']} seed{d['seed']} {d['kind']:5} {d['system']:18} verdict={d['verdict']} via={d['via']} code={d['code']} own={d['own']} strict={d['strict']}")
        print("     detail:", json.dumps(d["detail"], default=str)[:600])
        print("     ran:", [m for m in d["ran"] if m.startswith(("regression", "basic", "doe", "rsm", "opt"))])

print("\n== confirmation GO decisions by agent (n, wrong, codes)")
per = defaultdict(Counter)
for d in dec:
    if "confirm" in d["fork"].lower() and d["kind"] == "GO":
        per[d["system"]]["n"] += 1
        if d["code"] != "ok": per[d["system"]]["wrong"] += 1; per[d["system"]][d["code"]] += 1
for s in per: print(f"  {s:18} {dict(per[s])}")

# ---- Part B: Table 7 basis ------------------------------------------------------------------
print("\n== Part B: lockability basis (gpt6astra-97 campaign)")
rows = RA.load_rows(["gpt6astra-97"])
forks = defaultdict(lambda: {"nogo": 0, "go": 0, "types": None})
import lockability as LK
for r, p, *_ in RA.decisions(rows, cases):
    c = cases[r["case_id"]]; key = (r["case_id"], p["point_id"]); f = forks[key]
    if RA.is_stop(p): f["nogo"] += 1
    else: f["go"] += 1
    if f["types"] is None:
        atoms = set()
        for e in c.graph.edges_from(p["point_id"]):
            for a in RA._FIELD_RE.findall(e.when or ""):
                if not a[0].isdigit(): atoms.add(a.split(".")[-1].lower())
        f["types"] = {LK.atom_type(a) for a in atoms}
nogo_forks = {k: f for k, f in forks.items() if f["nogo"]}
print("graded forks:", len(forks), " forks with >=1 no-go seed:", len(nogo_forks),
      " sum of no-go seeds over those forks:", sum(f["nogo"] for f in nogo_forks.values()),
      " total no-go decisions per episode:", sum(f["nogo"] for f in forks.values()),
      " total go decisions:", sum(f["go"] for f in forks.values()))
print("forks with >=1 no-go seed but NO go seed:", [k for k, f in nogo_forks.items() if not f["go"]])
rowsum_f = sum(len(f["types"]) for f in nogo_forks.values())
rowsum_d = sum(len(f["types"]) * f["nogo"] for f in nogo_forks.values())
print("Table 7 row-sum basis: forks", rowsum_f, " decisions", rowsum_d)
print("forks whose guard spans >1 precondition type (counted once per type row):")
for k, f in sorted(nogo_forks.items()):
    if len(f["types"]) > 1:
        print("  ", k, "no-go seeds", f["nogo"], "types", sorted(t for t, _g in f["types"]))
