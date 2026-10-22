#!/usr/bin/env python3
"""Second interval families for the study-2 acted rate (population-weighted NO-GO units, 12 cases).

Same units and weights as scripts/study2_rescoring.py / scripts/fig_study2.py:
  rate = sum(w_i * acted_i) / sum(w_i) over the 40 NO-GO units, w = manifest weight.

Intervals reported
  1. percentile case-cluster bootstrap (paper's method; seed 20260919, 4000 draws; also 2000 draws)
  2. case-mean t: mean of the 12 per-case weighted rates +- t(11) * sd/sqrt(12)  (different estimand: each case weighted equally)
  3. linearized ratio cluster-t: ratio estimator with cluster-robust (CR1, G/(G-1)) SE, t(11)
  4. cluster bootstrap-t: percentile-t with the per-draw linearized SE (case resampling)
  5. wild cluster bootstrap-t: Webb six-point and Rademacher weights on case-level residuals, 4000 draws
  6. BCa over the case-cluster bootstrap (jackknife-over-cases acceleration)
Run: python3 audit_intervals.py  (from anywhere; paths resolved from the repo root)
"""
import json, math, random, sys
import numpy as np
from scipy import stats

import pathlib
ROOT = str(pathlib.Path(__file__).resolve().parents[1])  # repository root
SRC = f"{ROOT}/paper/blind_review_2026-09-19/coordinator/results_study2.json"
units = json.load(open(SRC))["units"]
stop = [u for u in units if u["kind"] == "STOP"]
cases = sorted({u["case"] for u in stop})
G = len(cases)
w = np.array([u["weight"] for u in stop]); y = np.array([1.0 if u["acted"] else 0.0 for u in stop])
cid = np.array([cases.index(u["case"]) for u in stop])
R = (w * y).sum() / w.sum()
print(f"units {len(stop)} NO-GO, cases {G}, acted k={int(y.sum())}, weighted rate {R:.4f} (unweighted {y.mean():.3f})")
A = np.array([(w * y)[cid == g].sum() for g in range(G)])   # per-case sum w*y
Bw = np.array([w[cid == g].sum() for g in range(G)])         # per-case sum w
n_c = np.array([(cid == g).sum() for g in range(G)])
k_c = np.array([y[cid == g].sum() for g in range(G)])
r_c = A / Bw
print("per case: n, acted, sum w, weighted rate")
for g in range(G):
    print(f"  {cases[g]:8s} n={n_c[g]} k={int(k_c[g])} W={Bw[g]:6.1f} r={r_c[g]:.3f}")

def pct(xs, a=0.025):
    xs = np.sort(xs); n = len(xs)
    return xs[int(a * n)], xs[int((1 - a) * n) - 1]

# 1. percentile case-cluster bootstrap, exactly as fig_study2.estimate (python random, seed 20260919)
def perc_boot(draws, seed=20260919):
    rng = random.Random(seed); vals = []
    for _ in range(draws):
        idx = rng.choices(range(G), k=G)
        vals.append(A[idx].sum() / Bw[idx].sum())
    return np.array(vals)
b4000 = perc_boot(4000); lo, hi = pct(b4000)
print(f"\n[1] percentile cluster bootstrap, 4000 draws:   {R*100:.1f}% [{lo*100:.1f}, {hi*100:.1f}]  (paper: 47% [31, 61])")
b2000 = perc_boot(2000); lo2, hi2 = pct(b2000)
print(f"    percentile cluster bootstrap, 2000 draws:   {R*100:.1f}% [{lo2*100:.1f}, {hi2*100:.1f}]")

# 2. case-mean t-interval
tq = stats.t.ppf(0.975, G - 1)
m = r_c.mean(); se_m = r_c.std(ddof=1) / math.sqrt(G)
print(f"[2] case-mean t (df {G-1}, t={tq:.3f}):            {m*100:.1f}% [{(m-tq*se_m)*100:.1f}, {(m+tq*se_m)*100:.1f}]  (mean of per-case rates, se {se_m*100:.1f})")

# 3. linearized ratio cluster-robust t-interval
def ratio_se(A_, B_):
    R_ = A_.sum() / B_.sum(); U = A_ - R_ * B_
    g = len(A_)
    return R_, math.sqrt(g / (g - 1) * (U ** 2).sum()) / B_.sum()
_, se_r = ratio_se(A, Bw)
print(f"[3] linearized ratio cluster-t (df {G-1}):        {R*100:.1f}% [{(R-tq*se_r)*100:.1f}, {(R+tq*se_r)*100:.1f}]  (se {se_r*100:.1f})")
# same with a normal quantile, to show the t-vs-z difference
print(f"    same with z=1.96:                            {R*100:.1f}% [{(R-1.96*se_r)*100:.1f}, {(R+1.96*se_r)*100:.1f}]")

# 4. cluster bootstrap-t (case resampling, percentile-t)
rng = np.random.default_rng(20260919)
idx = rng.integers(0, G, size=(4000, G))
Rb = A[idx].sum(1) / Bw[idx].sum(1)
Ub = A[idx] - Rb[:, None] * Bw[idx]
seb = np.sqrt(G / (G - 1) * (Ub ** 2).sum(1)) / Bw[idx].sum(1)
tb = (Rb - R) / seb
tlo, thi = pct(tb)
print(f"[4] cluster bootstrap-t (percentile-t):          {R*100:.1f}% [{(R-thi*se_r)*100:.1f}, {(R-tlo*se_r)*100:.1f}]")

# 5. wild cluster bootstrap-t (residuals from the weighted ratio, cluster-level auxiliary weights)
def wild(kind, draws=4000, seed=20260919):
    rng = np.random.default_rng(seed)
    e = y - R                                  # unit residuals
    if kind == "webb":
        pts = np.array([-math.sqrt(1.5), -1, -math.sqrt(0.5), math.sqrt(0.5), 1, math.sqrt(1.5)])
        v = pts[rng.integers(0, 6, size=(draws, G))]
    else:
        v = rng.choice([-1.0, 1.0], size=(draws, G))
    # y* = R + v_c e_i  ->  per-case A*_c = Bw_c R + v_c * sum_c w e
    Ae = np.array([(w * e)[cid == g].sum() for g in range(G)])
    Astar = Bw[None, :] * R + v * Ae[None, :]
    Rs = Astar.sum(1) / Bw.sum()
    Us = Astar - Rs[:, None] * Bw[None, :]
    ses = np.sqrt(G / (G - 1) * (Us ** 2).sum(1)) / Bw.sum()
    ts = (Rs - R) / ses
    qlo, qhi = pct(ts)
    return R - qhi * se_r, R - qlo * se_r, pct(Rs)
for kind in ("webb", "rademacher"):
    lo_, hi_, (plo, phi) = wild(kind)
    print(f"[5] wild cluster bootstrap-t ({kind:10s}):       {R*100:.1f}% [{lo_*100:.1f}, {hi_*100:.1f}]   (wild percentile of R*: [{plo*100:.1f}, {phi*100:.1f}])")

# 6. BCa on the case-cluster bootstrap
z0 = stats.norm.ppf((b4000 < R).mean())
jack = np.array([np.delete(A, g).sum() / np.delete(Bw, g).sum() for g in range(G)])
jm = jack.mean(); acc = ((jm - jack) ** 3).sum() / (6 * (((jm - jack) ** 2).sum()) ** 1.5)
def bca_q(alpha):
    z = stats.norm.ppf(alpha)
    return stats.norm.cdf(z0 + (z0 + z) / (1 - acc * (z0 + z)))
a1, a2 = bca_q(0.025), bca_q(0.975)
bs = np.sort(b4000)
print(f"[6] BCa cluster bootstrap (z0={z0:+.3f}, a={acc:+.3f}):    {R*100:.1f}% [{bs[int(a1*4000)]*100:.1f}, {bs[min(int(a2*4000),3999)]*100:.1f}]")
print(f"\nbootstrap sd of R* (case resampling) {b4000.std(ddof=1)*100:.1f} vs linearized se {se_r*100:.1f}")
