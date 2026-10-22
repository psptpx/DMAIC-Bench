"""adb_c17 generator — P / NP / Laney-P′ / C monitoring-baseline chain.

None of these four methods has a reference implementation in truth/verifiers.py, so every
truth is self-derived in this generator with the algorithm spelled out in its derivation:
  * P chart:  centerLine = pooled p̄ = Σdefects/Σn (unequal daily n);
  * NP chart: centerLine = n·p̄ where p̄ = Σdefects/(days·n) (equal daily n);
  * Laney P′: z_i = (p̂_i - p̄)/sqrt(p̄(1-p̄)/n_i); σ_Z = (mean moving range of z)/1.128
    (Laney 2002, Quality Engineering 14(4) — Minitab's P′ convention);
  * C chart:  centerLine = c̄ = mean daily defect count (equal inspection area).

Data design invariants (hold for every seed, asserted below):
  - the camera full-inspection line's daily rate carries a REAL day effect
    (p_i ~ N(0.06, 0.012) clamped, n_i ≈ 1800-3200) -> binomial-only sampling theory
    underestimates the day-to-day spread and σ_Z > 1.5 — the overdispersion_gate is
    determinate (redraw-guarded);
  - pooled p̄ of the manual sampling line and of the camera line both live in (0.01, 0.15).
"""
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402


def _binom(rng, n, p):
    return sum(1 for _ in range(n) if rng.random() < p)


def _poisson(rng, lam):
    # Knuth's algorithm — deterministic given the rng stream, no numpy dependency.
    limit, k, prod = pow(2.718281828459045, -lam), 0, rng.random()
    while prod > limit:
        k += 1
        prod *= rng.random()
    return k


def _laney_sigma_z(defects, sizes):
    total_d, total_n = sum(defects), sum(sizes)
    pbar = total_d / total_n
    z = [(d / n - pbar) / (pbar * (1 - pbar) / n) ** 0.5 for d, n in zip(defects, sizes)]
    mrbar = sum(abs(z[i] - z[i - 1]) for i in range(1, len(z))) / (len(z) - 1)
    return mrbar / 1.128, pbar


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260406)

    # P chart: 25 days, unequal n, honest binomial at a stable rate.
    for _ in range(200):
        p_sizes = [rng.randint(180, 320) for _ in range(25)]
        p_rate = rng.uniform(0.05, 0.075)
        p_defects = [_binom(rng, n, p_rate) for n in p_sizes]
        p_bar = sum(p_defects) / sum(p_sizes)
        if 0.02 < p_bar < 0.12:
            break
    else:
        raise AssertionError("adb_c17: could not construct sane P-chart data")

    # NP chart: 20 days, equal n.
    np_n = 240
    np_defects = [_binom(rng, np_n, rng.uniform(0.045, 0.06)) for _ in range(20)]
    np_center = np_n * (sum(np_defects) / (20 * np_n))

    # Laney P′: 30 days, large n, real day-to-day rate variation (overdispersion by design).
    for _ in range(200):
        lp_sizes = [rng.randint(1800, 3200) for _ in range(30)]
        lp_defects = [_binom(rng, n, min(max(rng.gauss(0.06, 0.012), 0.02), 0.12))
                      for n in lp_sizes]
        sigma_z, lp_pbar = _laney_sigma_z(lp_defects, lp_sizes)
        if sigma_z > 1.8 and 0.02 < lp_pbar < 0.12:
            break
    else:
        raise AssertionError("adb_c17: could not construct overdispersed data")

    # C chart: 22 days, equal inspection area, Poisson defect counts.
    c_counts = [_poisson(rng, rng.uniform(5.5, 6.5)) for _ in range(22)]
    c_bar = sum(c_counts) / len(c_counts)

    blocks = {
        "AC_P": {"defectCounts": p_defects, "sampleSizes": p_sizes,
                 "note": 'manual sampling line, 25 consecutive days; the quantity checked differs each day'},
        "AC_NP": {"defectCounts": np_defects, "sampleSize": np_n,
                  "note": 'automatic inspection line, 20 consecutive days; a fixed 240 checked each day'},
        "AC_LaneyP": {"defectCounts": lp_defects, "sampleSizes": lp_sizes,
                      "note": 'in-line camera 100% line, 30 consecutive days; several thousand checked each day'},
        "AC_C": {"defectCounts": c_counts,
                 "note": 'appearance-blemish register, 22 consecutive days; the count of blemishes on the same printed area each day'},
    }

    truths = (
        TruthEntry(method_id="control_chart.p", field="centerLine",
                   expected=round(p_bar, 6), tol=1e-4, soft=False,
                   stage_id="AC_P", metric_cue=r"CL|p̄|cent(?:re|er)\s*line|centre-?line|center-?line|p-?bar|average defect rate",
                   derivation=("self-derived in generator: pooled p̄ = Σdefects/Σn over the "
                               f"25 unequal daily samples (AIAG SPC-2 P chart), seed={seed}"),
                   verified_by=("python-closed-form",)),
        TruthEntry(method_id="control_chart.np", field="centerLine",
                   expected=round(np_center, 6), tol=1e-3, soft=False,
                   stage_id="AC_NP", metric_cue=r"CL|cent(?:re|er)\s*line|centre-?line|center-?line|np-?bar|average number non-?conforming",
                   derivation=("self-derived in generator: centerLine = n·p̄ with "
                               f"p̄ = Σdefects/(20·240) (AIAG SPC-2 NP chart), seed={seed}"),
                   verified_by=("python-closed-form",)),
        TruthEntry(method_id="control_chart.laney_p", field="sigmaZ",
                   expected=round(sigma_z, 6), tol=1.0, soft=False,
                   stage_id="AC_LaneyP", metric_cue=r"[Σσ]\s*_?Z|Sigma\s*Z",
                   derivation=("self-derived in generator: Laney σ_Z — z_i = (p̂_i-p̄)/"
                               "sqrt(p̄(1-p̄)/n_i), σ_Z = (mean moving range of z)/1.128 "
                               f"(Laney 2002 QE 14(4), Minitab P′ convention), seed={seed}"),
                   verified_by=("python-closed-form",)),
        TruthEntry(method_id="control_chart.c", field="centerLine",
                   expected=round(c_bar, 6), tol=1e-3, soft=False,
                   stage_id="AC_C", metric_cue=r"CL|c̄|cent(?:re|er)\s*line|centre-?line|center-?line|c-?bar|average blemish",
                   derivation=("self-derived in generator: centerLine = c̄ = mean daily defect "
                               f"count over 22 equal-area days (AIAG SPC-2 C chart), seed={seed}"),
                   verified_by=("python-closed-form",)),
    )

    _assert_invariants(blocks, truths)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(blocks, truths):
    by = {(t.method_id, t.field): t.expected for t in truths}
    assert by[("control_chart.laney_p", "sigmaZ")] > 1.5, \
        "camera line must be clearly overdispersed (Laney gate determinate)"
    assert 0.01 < by[("control_chart.p", "centerLine")] < 0.15, "sampling-line p̄ in (0.01,0.15)"
    lp = blocks["AC_LaneyP"]
    assert 0.01 < sum(lp["defectCounts"]) / sum(lp["sampleSizes"]) < 0.15, \
        "camera-line p̄ in (0.01,0.15)"


if __name__ == "__main__":
    bad = []
    for s in range(1, 501):
        try:
            generate(s)
        except AssertionError as e:
            bad.append((s, str(e)))
    print("failed seeds:", bad if bad else "NONE (500/500)")
