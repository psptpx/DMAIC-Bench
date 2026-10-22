#!/usr/bin/env python3
"""t-intervals and wild-bootstrap intervals for the main-campaign pooled rates (15 cases), from the
per-decision records dumped by extract_dec.py (same records restraint_analysis.py uses for
\\stopRightCI, \\goRightCI, \\mStopRightCI, \\mGoRightCI, \\mGapCI).

    python3 main_intervals.py dec.json
"""
import json, math, random, sys
import numpy as np
from scipy import stats

d = json.load(open(sys.argv[1]))
DEC, matched = d["DEC"], set(d["matched"])
recs = [(c, f"{c}|{p}", k, w) for n in DEC for (c, p, k, w) in DEC[n]]
cases = sorted({r[0] for r in recs}); G = len(cases); tq = stats.t.ppf(0.975, G - 1)
print(f"systems {len(DEC)}, decisions {len(recs)}, cases {G}, matched forks {len(matched)}, t({G-1})={tq:.3f}")

def pct(xs, a=0.025):
    xs = np.sort(xs); n = len(xs); return xs[int(a * n)], xs[int((1 - a) * n) - 1]

def totals(kind, only_matched):
    sel = [r for r in recs if r[2] == kind and (not only_matched or r[1] in matched)]
    A = np.array([sum(1 - r[3] for r in sel if r[0] == c) for c in cases], float)   # correct per case
    B = np.array([sum(1 for r in sel if r[0] == c) for c in cases], float)          # decisions per case
    return A, B

def paper_boot(fn, draws=4000, seed=20260919):
    """restraint_analysis._boot: python random, seed 20260919, sorted case list."""
    rng = random.Random(seed); vals = []
    for _ in range(draws):
        idx = [cases.index(c) for c in rng.choices(cases, k=G)]
        v = fn(np.array(idx))
        if v is not None: vals.append(v)
    return np.array(vals)

def ratio(A, B, idx):
    b = B[idx].sum(); return None if b == 0 else A[idx].sum() / b

def se_ratio(A, B):
    R = A.sum() / B.sum(); U = A - R * B
    return R, math.sqrt(G / (G - 1) * (U ** 2).sum()) / B.sum()

def wild_t(A, B, R, se, draws=4000, seed=20260919):
    rng = np.random.default_rng(seed)
    pts = np.array([-math.sqrt(1.5), -1, -math.sqrt(0.5), math.sqrt(0.5), 1, math.sqrt(1.5)])
    v = pts[rng.integers(0, 6, size=(draws, G))]
    Ae = A - R * B                                  # per-case residual totals
    Astar = B[None, :] * R + v * Ae[None, :]
    Rs = Astar.sum(1) / B.sum(); Us = Astar - Rs[:, None] * B[None, :]
    ses = np.sqrt(G / (G - 1) * (Us ** 2).sum(1)) / B.sum()
    qlo, qhi = pct((Rs - R) / ses)
    return R - qhi * se, R - qlo * se

def report(label, A, B, macro):
    R, se = se_ratio(A, B)
    lo, hi = pct(paper_boot(lambda idx: ratio(A, B, idx)))
    used = B > 0
    rc = A[used] / B[used]; m = rc.mean(); sem = rc.std(ddof=1) / math.sqrt(used.sum()); tqm = stats.t.ppf(0.975, used.sum() - 1)
    wlo, whi = wild_t(A, B, R, se)
    print(f"\n{label}: {int(A.sum())}/{int(B.sum())} correct = {R*100:.1f}%   (paper macro {macro})")
    print(f"  per-case n: {B.astype(int).tolist()}")
    print(f"  per-case rates: {[round(x, 2) for x in rc]}")
    print(f"  [1] percentile cluster bootstrap (4000, seed 20260919): [{lo*100:.1f}, {hi*100:.1f}]")
    print(f"  [2] case-mean t (df {used.sum()-1}): {m*100:.1f}% [{(m-tqm*sem)*100:.1f}, {(m+tqm*sem)*100:.1f}]  se {sem*100:.1f}")
    print(f"  [3] linearized ratio cluster-t (df {G-1}): [{(R-tq*se)*100:.1f}, {(R+tq*se)*100:.1f}]  se {se*100:.1f}")
    print(f"  [5] wild cluster bootstrap-t (Webb, 4000): [{wlo*100:.1f}, {whi*100:.1f}]")
    return R, se, A, B

out = {}
for kind, om, macro in (("NO-GO", False, "stopRightCI 8--30"), ("GO", False, "goRightCI 75--84"),
                        ("NO-GO", True, "mStopRightCI 8--30"), ("GO", True, "mGoRightCI 86--97")):
    A, B = totals(kind, om)
    out[(kind, om)] = report(f"{'matched ' if om else 'all '}{kind} right", A, B, macro)

# matched gap GO - NO-GO (paper mGapCI 59--87), paired within case
Rs_, ses_, As, Bs = out[("NO-GO", True)]; Rg, seg, Ag, Bg = out[("GO", True)]
gap = Rg - Rs_
def gap_boot(idx):
    s = ratio(As, Bs, idx); g = ratio(Ag, Bg, idx)
    return None if s is None or g is None else g - s
lo, hi = pct(paper_boot(gap_boot))
# linearized: influence per case U_c = (Ag_c - Rg Bg_c)/sum Bg - (As_c - Rs Bs_c)/sum Bs
U = (Ag - Rg * Bg) / Bg.sum() - (As - Rs_ * Bs) / Bs.sum()
se_gap = math.sqrt(G / (G - 1) * (U ** 2).sum())
used = (Bs > 0) & (Bg > 0)
dc = Ag[used] / Bg[used] - As[used] / Bs[used]; md = dc.mean(); sed = dc.std(ddof=1) / math.sqrt(used.sum()); tqd = stats.t.ppf(0.975, used.sum() - 1)
print(f"\nmatched gap GO - NO-GO: {gap*100:.1f} points (paper macro mGapCI 59--87)")
print(f"  [1] percentile cluster bootstrap: [{lo*100:.1f}, {hi*100:.1f}]")
print(f"  [2] case-mean t on per-case differences (df {used.sum()-1}, {used.sum()} cases with both sides): {md*100:.1f} [{(md-tqd*sed)*100:.1f}, {(md+tqd*sed)*100:.1f}]")
print(f"  [3] linearized cluster-t (df {G-1}): [{(gap-tq*se_gap)*100:.1f}, {(gap+tq*se_gap)*100:.1f}]  se {se_gap*100:.1f}")
# per-case profile dump for the coverage simulation (matched NO-GO and GO)
prof = {"cases": cases,
        "matched_nogo": {"n": Bs.astype(int).tolist(), "k": As.astype(int).tolist()},
        "matched_go": {"n": Bg.astype(int).tolist(), "k": Ag.astype(int).tolist()},
        "all_nogo": {"n": out[("NO-GO", False)][3].astype(int).tolist(), "k": out[("NO-GO", False)][2].astype(int).tolist()}}
json.dump(prof, open(sys.argv[1].replace("dec.json", "profiles_main.json"), "w"))
