"""adb_c06 generator — native parametric port of the legacy frozen bridge case.

"derive, never hand-write": every truth entry is DERIVED from the freshly generated data. Methods without a
reference implementation in truth/verifiers.py (Xbar center lines, EWMA/CUSUM flag counts,
nonnormal Ppk) are derived by SELF-IMPLEMENTED algorithms documented below and in each
TruthEntry.derivation; capability.nonnormal / control_chart.* have no verifiers entry, so V7
skips them by design — the derivation string is the audit trail.

Self-implemented derivation conventions (all standard Minitab/Montgomery conventions):
  - Xbar-R / Xbar-S center line: CL = grand mean of ALL observations (closed form).
  - "in control" is STRUCTURAL, not a lucky draw: subgrouped payloads are redrawn until the
    mean chart passes a full Western-Electric screen (beyond 3σ / 2of3>2σ / 4of5>1σ /
    9 same side / 6 trending / 14 alternating / 15 within 1σ) with estimated limits
    (σ̂ = R̄/d2/√n or S̄/c4/√n) AND the dispersion chart (R or S) stays inside D3/D4 (B3/B4).
  - EWMA flaggedCount: λ=0.2, L=3, z0 = target(=nominal 500g, carried in the payload),
    σ̂ = mean moving range / 1.128, exact time-varying limits; count of points outside.
  - CUSUM flaggedCount: tabular CUSUM, k=0.5σ, h=4σ, target = nominal 500g (in payload),
    σ̂ = mean moving range / 1.128; count of points with C+>h or C-<-h.
  - nonnormal Ppk (upper spec only): scipy lognormal MLE fit (floc=0), percentile method
    Ppk = Ppu = (USL - x50) / (x99.865 - x50)   (ISO 22514-4 / Minitab nonnormal convention).

Data design invariants (hold for every seed, asserted below):
  - both subgrouped payloads pass the Western-Electric screen — zero violations by construction
    (stable mean, no drift injected, redraw until clean);
  - both individual-value series carry a sustained +1.5σ end drift over 9 points (>= 8 required)
    -> EWMA and CUSUM flaggedCount >= 1 each (redraw guard);
  - overfill data is lognormal: AD normality p < 0.05 (nonnormal_gate determinate) and the
    percentile-method Ppk stays inside (0.5, 2.0).
"""
import math
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from scipy import stats  # noqa: E402

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402
from dmaic_bench.truth import verifiers  # noqa: E402

_NOMINAL = 500.0          # filling-line nominal net content (g) — EWMA/CUSUM target
_USL_OVERFILL = 12.0      # contract single-sided upper limit on overfill (g)

# Shewhart chart constants (Montgomery ISQC 6e, Appendix VI)
_D2 = {5: 2.326, 8: 2.847}
_D3 = {5: 0.0, 8: 0.136}
_D4 = {5: 2.114, 8: 1.864}
_C4 = {8: 0.9650}
_B3 = {8: 0.185}
_B4 = {8: 1.815}


def _stdev(values):
    m = sum(values) / len(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


# ---------------------------------------------------------------- Western-Electric screen

def _we_violation_free(points, center, sigma):
    """True iff the point series triggers NONE of the Western-Electric rules:
    beyond 3σ / 2of3 beyond 2σ same side / 4of5 beyond 1σ same side / 9 in a row same side /
    6 in a row trending / 14 alternating up-down / 15 in a row within 1σ."""
    z = [(p - center) / sigma for p in points]
    n = len(z)
    if any(abs(v) > 3 for v in z):
        return False
    for i in range(n - 2):
        w = z[i:i + 3]
        if sum(v > 2 for v in w) >= 2 or sum(v < -2 for v in w) >= 2:
            return False
    for i in range(n - 4):
        w = z[i:i + 5]
        if sum(v > 1 for v in w) >= 4 or sum(v < -1 for v in w) >= 4:
            return False
    for i in range(n - 8):
        w = z[i:i + 9]
        if all(v > 0 for v in w) or all(v < 0 for v in w):
            return False
    for i in range(n - 5):
        w = z[i:i + 6]
        if all(a < b for a, b in zip(w, w[1:])) or all(a > b for a, b in zip(w, w[1:])):
            return False
    diffs = [1 if b > a else -1 if b < a else 0 for a, b in zip(z, z[1:])]
    run = 1
    for a, b in zip(diffs, diffs[1:]):
        run = run + 1 if (a != 0 and b == -a) else 1
        if run >= 13:  # 13 alternating differences = 14 alternating points
            return False
    for i in range(n - 14):
        if all(abs(v) <= 1 for v in z[i:i + 15]):
            return False
    return True


def _subgroup_chart_clean(flat, n, chart):
    """WE screen on the Xbar chart + 3σ screen on the dispersion (R or S) chart."""
    k = len(flat) // n
    groups = [flat[i * n:(i + 1) * n] for i in range(k)]
    xbars = [sum(g) / n for g in groups]
    grand = sum(flat) / len(flat)
    if chart == "s":
        s_vals = [_stdev(g) for g in groups]
        sbar = sum(s_vals) / k
        sigma_xbar = sbar / _C4[n] / math.sqrt(n)
        disp_ok = all(_B3[n] * sbar <= s <= _B4[n] * sbar for s in s_vals)
    else:
        r_vals = [max(g) - min(g) for g in groups]
        rbar = sum(r_vals) / k
        sigma_xbar = rbar / _D2[n] / math.sqrt(n)
        disp_ok = all(_D3[n] * rbar <= r <= _D4[n] * rbar for r in r_vals)
    return disp_ok and _we_violation_free(xbars, grand, sigma_xbar)


def _subgrouped_incontrol(rng, k, n, mean, sd, chart):
    """k subgroups of n, redrawn until in-control is a structural property of the payload."""
    for _ in range(200):
        flat = [round(rng.gauss(mean, sd), 2) for _ in range(k * n)]
        if _subgroup_chart_clean(flat, n, chart):
            return flat
    raise AssertionError("could not draw an in-control subgrouped series in 200 tries")


# ---------------------------------------------------------------- time-weighted charts

def _sigma_mr(data):
    """σ̂ from the average moving range of an individuals series (MR̄ / 1.128)."""
    mrbar = sum(abs(b - a) for a, b in zip(data, data[1:])) / (len(data) - 1)
    return mrbar / 1.128


def _ewma_flagged(data, target, lam=0.2, big_l=3.0):
    """EWMA flag count: z0=target, exact time-varying L-sigma limits, σ̂ from moving range."""
    sigma = _sigma_mr(data)
    z, flags = target, 0
    for i, x in enumerate(data, 1):
        z = lam * x + (1 - lam) * z
        half = big_l * sigma * math.sqrt(lam / (2 - lam) * (1 - (1 - lam) ** (2 * i)))
        flags += abs(z - target) > half
    return flags


def _cusum_flagged(data, target, h=4.0, k=0.5):
    """Tabular CUSUM flag count: standardized deviations, C+>h or C-<-h, σ̂ from moving range."""
    sigma = _sigma_mr(data)
    cp = cm = 0.0
    flags = 0
    for x in data:
        u = (x - target) / sigma
        cp = max(0.0, cp + u - k)
        cm = min(0.0, cm + u + k)
        flags += (cp > h) or (cm < -h)
    return flags


def _drift_series(rng, flag_fn, n_ic=21, n_shift=9, mean=_NOMINAL, sd=2.0, shift_sigma=1.5):
    """21 in-control points + 9 points with a sustained +1.5σ shift; redraw until the target
    time-weighted chart flags at least one point (flaggedCount >= 1 for EVERY seed)."""
    for _ in range(200):
        s = ([round(rng.gauss(mean, sd), 2) for _ in range(n_ic)]
             + [round(rng.gauss(mean + shift_sigma * sd, sd), 2) for _ in range(n_shift)])
        if flag_fn(s) >= 1:
            return s
    raise AssertionError("drift series never flagged in 200 tries — increase the shift")


# ---------------------------------------------------------------- nonnormal capability

def _lognorm_ppk_upper(data, usl):
    """Percentile-method Ppk with only an upper spec: scipy lognormal MLE fit (floc=0),
    Ppk = Ppu = (USL - x50) / (x99.865 - x50)."""
    shape, _loc, scale = stats.lognorm.fit(data, floc=0)
    x50 = float(stats.lognorm.ppf(0.5, shape, loc=0, scale=scale))
    x_hi = float(stats.lognorm.ppf(0.99865, shape, loc=0, scale=scale))
    return (usl - x50) / (x_hi - x50)


def _overfill_block(rng, n=60, scale=3.0, sigma=0.45, usl=_USL_OVERFILL):
    """Right-skewed overfill grams: scale*exp(N(0,σ)). Redrawn until AD normality fails
    (p<0.05, keeps nonnormal_gate determinate) and Ppk sits safely inside (0.5, 2.0)."""
    for _ in range(200):
        data = [round(scale * math.exp(rng.gauss(0.0, sigma)), 3) for _ in range(n)]
        ppk = _lognorm_ppk_upper(data, usl)
        ad_p = verifiers.descriptive_summary({"data": data})["adPValue"]
        if ad_p < 0.05 and 0.55 <= ppk <= 1.9:
            return data, ppk
    raise AssertionError("overfill block never met AD/Ppk gates in 200 tries")


# ---------------------------------------------------------------- generate

def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 70_500_017)

    xbar_r_flat = _subgrouped_incontrol(rng, 20, 5, _NOMINAL, 2.0, chart="r")
    xbar_s_flat = _subgrouped_incontrol(rng, 22, 8, _NOMINAL + 0.3, 1.6, chart="s")
    ewma_series = _drift_series(rng, lambda s: _ewma_flagged(s, _NOMINAL))
    cusum_series = _drift_series(rng, lambda s: _cusum_flagged(s, _NOMINAL))
    overfill, ppk = _overfill_block(rng)

    blocks = {
        "CC_XbarR": {"data": xbar_r_flat, "subgroupSize": 5, "unit": "g"},
        "CC_XbarS": {"data": xbar_s_flat, "subgroupSize": 8, "unit": "g"},
        "CC_EWMA": {"data": ewma_series, "target": _NOMINAL, "ewmaWeight": 0.2, "unit": "g"},
        "CC_CUSUM": {"data": cusum_series, "target": _NOMINAL,
                     "hValue": 4.0, "kValue": 0.5, "unit": "g"},
        "CC_NonnormalCap": {"data": overfill, "usl": _USL_OVERFILL,
                            "autoSelectDistribution": True, "confidenceLevel": 0.95,
                            "unit": "g"},
    }

    truths = (
        TruthEntry(
            method_id="control_chart.xbar_r", field="xBarChartCenterLine",
            expected=round(sum(xbar_r_flat) / len(xbar_r_flat), 6), tol=0.05, soft=False,
            stage_id="CC_XbarR", metric_cue=r"CL|cent(?:re|er)\s*line|centre-?line|center-?line|mean",
            derivation=f"closed-form grand mean of all 20x5 observations (Xbar chart CL "
                       f"convention), seed={seed}",
            verified_by=("closed-form",),
        ),
        TruthEntry(
            method_id="control_chart.xbar_s", field="xBarChartCenterLine",
            expected=round(sum(xbar_s_flat) / len(xbar_s_flat), 6), tol=0.05, soft=False,
            stage_id="CC_XbarS", metric_cue=r"CL|cent(?:re|er)\s*line|centre-?line|center-?line|mean",
            derivation=f"closed-form grand mean of all 22x8 observations (Xbar chart CL "
                       f"convention), seed={seed}",
            verified_by=("closed-form",),
        ),
        TruthEntry(
            method_id="control_chart.ewma", field="flaggedCount",
            expected=float(_ewma_flagged(ewma_series, _NOMINAL)), tol=4.0, soft=False,
            stage_id="CC_EWMA", metric_cue=r"drift|out[- ]of[- ]control|signal|beyond|outside",
            derivation=f"self-implemented EWMA λ=0.2 L=3, z0=target=500g (payload field), "
                       f"σ̂=MR̄/1.128, exact time-varying limits; count of points outside, "
                       f"seed={seed}",
            verified_by=("generator-selfimpl",),
        ),
        TruthEntry(
            method_id="control_chart.cusum", field="flaggedCount",
            expected=float(_cusum_flagged(cusum_series, _NOMINAL)), tol=4.0, soft=False,
            stage_id="CC_CUSUM", metric_cue=r"cumulative|out[- ]of[- ]control|signal|drift|beyond",
            derivation=f"self-implemented tabular CUSUM k=0.5σ h=4σ, target=500g (payload "
                       f"field), σ̂=MR̄/1.128; count of points with C+>h or C-<-h, seed={seed}",
            verified_by=("generator-selfimpl",),
        ),
        TruthEntry(
            method_id="capability.nonnormal", field="ppk",
            expected=round(ppk, 6), tol=0.3, soft=False,
            stage_id="CC_NonnormalCap", metric_cue=r"Ppk",
            derivation=f"scipy lognorm MLE fit (floc=0), percentile method "
                       f"Ppk=Ppu=(USL-x50)/(x99.865-x50), USL={_USL_OVERFILL}, seed={seed}",
            verified_by=("scipy",),
        ),
    )

    _assert_invariants(blocks, truths)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(blocks, truths):
    by = {(t.method_id, t.field): t.expected for t in truths}
    assert _subgroup_chart_clean(blocks["CC_XbarR"]["data"], 5, "r"), \
        "Xbar-R payload must be Western-Electric violation-free"
    assert _subgroup_chart_clean(blocks["CC_XbarS"]["data"], 8, "s"), \
        "Xbar-S payload must be Western-Electric violation-free"
    assert by[("control_chart.ewma", "flaggedCount")] >= 1, "EWMA must flag the drift"
    assert by[("control_chart.cusum", "flaggedCount")] >= 1, "CUSUM must flag the drift"
    assert 0.5 < by[("capability.nonnormal", "ppk")] < 2.0, "nonnormal Ppk must stay in (0.5, 2)"
    ad_p = verifiers.descriptive_summary({"data": blocks["CC_NonnormalCap"]["data"]})["adPValue"]
    assert ad_p < 0.05, "overfill data must fail AD normality (nonnormal_gate determinate)"


if __name__ == "__main__":
    for s in range(1, 501):
        d = generate(s)
        if s <= 3 or s % 100 == 0:
            print(s, "ok:", {(t.method_id.split(".")[-1], t.field): t.expected for t in d.truths})
    print("500-seed sweep clean")
