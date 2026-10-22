#!/usr/bin/env python3
"""Coverage of the case-clustered percentile bootstrap and of alternatives at 12 and 15 clusters.

Population: case PROFILES are the observed cases (unit count n_c, unit weights, and a centre rate
m_c = (k_c + pbar)/(n_c + 1), the observed per-case rate shrunk by one pseudo-unit at the pooled rate).
Each replication samples G profiles with replacement, draws each sampled case's true rate
p_c ~ Beta(kappa*m_c, kappa*(1-m_c)) (kappa=inf: p_c = m_c), then binary unit outcomes ~ Bernoulli(p_c)
with the profile's unit weights. Estimators and targets:
  ratio  R = sum(w y)/sum(w)              target  theta_R = sum_prof W_c m_c / sum_prof W_c
  case mean  M = mean_c (A_c/B_c)          target  theta_M = mean_prof m_c
Intervals (nominal 95%):
  pct-R   percentile case-cluster bootstrap of R          (the paper's method)
  pct-M   percentile case-cluster bootstrap of the case mean
  t-M     case-mean t interval, df G-1
  t-R     linearized cluster-robust t interval for R (CR1 factor G/(G-1)), df G-1
  wild-R  wild cluster bootstrap-t for R, Webb six-point weights
Usage: python3 coverage_sim.py profiles_main.json [reps] [draws]
"""
import json, math, sys, time
import numpy as np
from scipy import stats

import pathlib
ROOT = str(pathlib.Path(__file__).resolve().parents[1])  # repository root
reps = int(sys.argv[2]) if len(sys.argv) > 2 else 500
draws = int(sys.argv[3]) if len(sys.argv) > 3 else 2000

def audit_profiles():
    units = json.load(open(f"{ROOT}/paper/blind_review_2026-09-19/coordinator/results_study2.json"))["units"]
    stop = [u for u in units if u["kind"] == "STOP"]
    cases = sorted({u["case"] for u in stop}); pbar = np.mean([u["acted"] for u in stop])
    prof = []
    for c in cases:
        us = [u for u in stop if u["case"] == c]
        k = sum(u["acted"] for u in us); n = len(us)
        prof.append({"w": np.array([u["weight"] for u in us]), "m": (k + pbar) / (n + 1)})
    return prof

def main_profiles(key):
    P = json.load(open(sys.argv[1]))[key]
    n, k = np.array(P["n"]), np.array(P["k"]); pbar = k.sum() / n.sum()
    return [{"w": np.ones(int(n_)), "m": (k_ + pbar) / (n_ + 1)} for n_, k_ in zip(n, k)]

def simulate(prof, G, kappa, seed=20260926):
    rng = np.random.default_rng(seed)
    W = np.array([p["w"].sum() for p in prof]); m = np.array([p["m"] for p in prof])
    theta_R = (W * m).sum() / W.sum(); theta_M = m.mean()
    tq = stats.t.ppf(0.975, G - 1)
    webb = np.array([-math.sqrt(1.5), -1, -math.sqrt(0.5), math.sqrt(0.5), 1, math.sqrt(1.5)])
    cov = {k: 0 for k in ("pct-R", "pct-M", "t-M", "t-R", "wild-R")}; wid = {k: 0.0 for k in cov}
    degenerate = 0
    for _ in range(reps):
        g = rng.integers(0, len(prof), size=G)
        if np.isinf(kappa):
            p = m[g]
        else:
            p = rng.beta(np.clip(kappa * m[g], 1e-6, None), np.clip(kappa * (1 - m[g]), 1e-6, None))
        A = np.empty(G); B = np.empty(G)
        for j in range(G):
            w = prof[g[j]]["w"]; y = rng.random(len(w)) < p[j]
            A[j] = (w * y).sum(); B[j] = w.sum()
        R = A.sum() / B.sum(); rc = A / B; M = rc.mean()
        # percentile cluster bootstrap (ratio and case mean)
        idx = rng.integers(0, G, size=(draws, G))
        Rb = A[idx].sum(1) / B[idx].sum(1); Mb = rc[idx].mean(1)
        lo, hi = np.quantile(Rb, [0.025, 0.975]); cov["pct-R"] += lo <= theta_R <= hi; wid["pct-R"] += hi - lo
        lo, hi = np.quantile(Mb, [0.025, 0.975]); cov["pct-M"] += lo <= theta_M <= hi; wid["pct-M"] += hi - lo
        if lo == hi: degenerate += 1
        # case-mean t
        se = rc.std(ddof=1) / math.sqrt(G); lo, hi = M - tq * se, M + tq * se
        cov["t-M"] += lo <= theta_M <= hi; wid["t-M"] += hi - lo
        # linearized ratio cluster t
        U = A - R * B; seR = math.sqrt(G / (G - 1) * (U ** 2).sum()) / B.sum()
        lo, hi = R - tq * seR, R + tq * seR; cov["t-R"] += lo <= theta_R <= hi; wid["t-R"] += hi - lo
        # wild cluster bootstrap-t (Webb)
        v = webb[rng.integers(0, 6, size=(draws, G))]
        Astar = B[None, :] * R + v * U[None, :]
        Rs = Astar.sum(1) / B.sum(); Us = Astar - Rs[:, None] * B[None, :]
        ses = np.sqrt(G / (G - 1) * (Us ** 2).sum(1)) / B.sum()
        with np.errstate(divide="ignore", invalid="ignore"):
            ts = (Rs - R) / ses
        ts = ts[np.isfinite(ts)]
        if seR > 0 and len(ts) > 100:
            qlo, qhi = np.quantile(ts, [0.025, 0.975]); lo, hi = R - qhi * seR, R - qlo * seR
        else:
            lo, hi = R, R
        cov["wild-R"] += lo <= theta_R <= hi; wid["wild-R"] += hi - lo
    return theta_R, theta_M, {k: cov[k] / reps for k in cov}, {k: wid[k] / reps for k in cov}, degenerate

designs = [
    ("audit acted rate, 12 profiles", audit_profiles(), 12, 20.0),
    ("audit acted rate, 12 profiles", audit_profiles(), 15, 20.0),
    ("audit acted rate, 12 profiles", audit_profiles(), 12, 5.0),
    ("audit acted rate, 12 profiles", audit_profiles(), 12, float("inf")),
    ("main matched NO-GO right, 15 profiles", main_profiles("matched_nogo"), 15, 20.0),
    ("main matched NO-GO right, 15 profiles", main_profiles("matched_nogo"), 15, float("inf")),
    ("main matched NO-GO right, 15 profiles", main_profiles("matched_nogo"), 12, 20.0),
    ("main matched GO right, 15 profiles", main_profiles("matched_go"), 15, 20.0),
]
mc = 1.96 * math.sqrt(0.95 * 0.05 / reps)
print(f"reps {reps}, bootstrap draws {draws}, MC half-width at 95% coverage +-{mc*100:.1f} points\n")
print(f"{'design':40s} {'G':>2s} {'kappa':>5s} {'theta_R':>7s} {'theta_M':>7s} | " + " ".join(f"{k:>7s}" for k in ("pct-R", "pct-M", "t-M", "t-R", "wild-R")) + " | mean width (pts)")
t0 = time.time()
for label, prof, G, kappa in designs:
    thR, thM, cov, wid, deg = simulate(prof, G, kappa)
    ks = ("pct-R", "pct-M", "t-M", "t-R", "wild-R")
    print(f"{label:40s} {G:2d} {kappa:5.0f} {thR*100:6.1f}% {thM*100:6.1f}% | " + " ".join(f"{cov[k]*100:6.1f}%" for k in ks)
          + " | " + " ".join(f"{wid[k]*100:5.1f}" for k in ks) + (f"  ({deg} degenerate pct-M)" if deg else "") + f"   [{time.time()-t0:.0f}s]", flush=True)
