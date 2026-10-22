"""adb_c21 generator — native parametric port of the legacy frozen bridge case.

"derive, never hand-write": every truth entry is DERIVED from the freshly generated data. Where a reference
implementation exists in truth/verifiers.py (capability.poisson, regression.poisson,
tables.chisquare_gof) the truth comes from it (and V7 re-verifies); methods without one
(control_chart.u processMean, control_chart.laney_u sigmaZ) are derived by SELF-IMPLEMENTED
algorithms documented below and in each TruthEntry.derivation.

Self-implemented derivation conventions:
  - U chart processMean: pooled DPU = Σcounts / Σunits (center line ū, closed form);
    the plain-U payload is redrawn until no daily rate leaves ū ± 3√(ū/n_i) — "in control"
    is structural, so the plain-U branch narrative stays clean for every seed.
  - Laney σ_Z: z_i = (u_i - ū) / √(ū/n_i); σ_Z = mean moving range of z / 1.128
    (Laney 2002 / Minitab U′ convention). Overdispersion is generated structurally: the
    true daily rate itself varies day-to-day (rate_i = base·exp(N(0, σ_ln)), a Poisson-
    lognormal mixture => variance >> mean), and the payload is redrawn until σ_Z > 1.6.

Data design invariants (hold for every seed, asserted below):
  - pooled baseline DPU >= 0.07, clearly above the 0.05 target;
  - Laney payload is overdispersed: σ_Z > 1.5 (overdispersion_gate determinate);
  - Poisson regression slope is significantly POSITIVE (counts ~ Poisson(exp(a + b·temp)),
    b > 0 with a large effect; Wald p < 0.001 enforced by redraw);
  - defect-category GOF is decisive: dominant category >= 50% of records, chi-square
    p < 1e-6 (< 0.01 asserted).
"""
import math
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402
from dmaic_bench.truth import verifiers  # noqa: E402

_TARGET_DPU = 0.05
_CATEGORIES = ('cold joint', 'solder bridge', 'misplacement', 'insufficient solder', 'tombstoning')
_CAT_PROBS = (0.55, 0.18, 0.11, 0.09, 0.07)


def _poisson(rng, lam):
    """Knuth Poisson draw from the case-local Random (keeps count payloads deterministic)."""
    limit, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1


def _pooled_dpu(counts, units):
    return sum(counts) / sum(units)


def _u_chart_in_control(counts, units):
    """True iff no daily rate leaves the plain-U 3σ limits ū ± 3√(ū/n_i)."""
    ubar = _pooled_dpu(counts, units)
    return all(abs(c / u - ubar) <= 3.0 * math.sqrt(ubar / u) for c, u in zip(counts, units))


def _laney_sigma_z(counts, units):
    """Laney σ_Z: z-scores of daily rates under the Poisson model, moving-range estimate
    σ_Z = MR̄(z)/1.128 (Laney 2002; Minitab U′ chart)."""
    ubar = _pooled_dpu(counts, units)
    z = [(c / u - ubar) / math.sqrt(ubar / u) for c, u in zip(counts, units)]
    mrbar = sum(abs(b - a) for a, b in zip(z, z[1:])) / (len(z) - 1)
    return mrbar / 1.128


def _poisson_slope(x, y):
    """(slope, Wald p) of the GLM Poisson fit counts ~ exp(a + b·x) — invariant check only."""
    import numpy as np
    import statsmodels.api as sm
    fit = sm.GLM(np.asarray(y, float), sm.add_constant(np.asarray(x, float)),
                 family=sm.families.Poisson()).fit()
    return float(fit.params[1]), float(fit.pvalues[1])


def _derive(method_id, block, entries, stage_id, seed):
    """Run the reference implementation and turn selected outputs into TruthEntry rows."""
    ref = verifiers.REFERENCE_IMPLS[method_id](block)
    out = []
    for field, tol, soft, cue in entries:
        out.append(TruthEntry(
            method_id=method_id, field=field, expected=round(ref[field], 6), tol=tol, soft=soft,
            stage_id=stage_id, metric_cue=cue,
            derivation=f"derived from generated payload via truth.verifiers.{method_id} "
                       f"(scipy/statsmodels), seed={seed}",
            verified_by=("scipy",),
        ))
    return out


# ---------------------------------------------------------------- block generators

def _baseline_counts(rng, days=20, rate=0.09):
    """Main-shop 20-day counts/units at true DPU ~0.09; redraw until pooled DPU >= 0.07
    (clearly above the 0.05 target for every seed)."""
    for _ in range(200):
        units = [rng.randint(45, 60) for _ in range(days)]
        counts = [_poisson(rng, rate * u) for u in units]
        if _pooled_dpu(counts, units) >= 0.07:
            return counts, units
    raise AssertionError("baseline DPU never reached 0.07 in 200 tries")


def _u_chart_counts(rng, days=25, rate=0.09):
    """Second-shop 25-day counts/units, same true rate; redraw until in control (plain U)."""
    for _ in range(200):
        units = [rng.randint(40, 55) for _ in range(days)]
        counts = [_poisson(rng, rate * u) for u in units]
        if _u_chart_in_control(counts, units):
            return counts, units
    raise AssertionError("u-chart payload never in control in 200 tries")


def _laney_counts(rng, days=25, base=0.35, sigma_ln=0.45):
    """Outsourced-line daily counts with STRUCTURAL day-to-day rate variation (Poisson-
    lognormal mixture => variance >> mean); redraw until σ_Z > 1.6 (asserted > 1.5)."""
    for _ in range(200):
        units = [rng.randint(40, 60) for _ in range(days)]
        counts = [_poisson(rng, base * math.exp(rng.gauss(0.0, sigma_ln)) * u) for u in units]
        if _laney_sigma_z(counts, units) > 1.6:
            return counts, units
    raise AssertionError("Laney payload never overdispersed enough in 200 tries")


def _regression_counts(rng, batches=24):
    """Reflow preheat temperature vs batch defect counts with a REAL positive effect:
    counts ~ Poisson(exp(-6.4 + 0.05·temp)), temps 150..196; redraw until Wald p < 0.001."""
    temps = [round(150.0 + 2.0 * i, 1) for i in range(batches)]
    for _ in range(200):
        counts = [_poisson(rng, math.exp(-6.4 + 0.05 * t)) for t in temps]
        slope, p = _poisson_slope(temps, counts)
        if slope > 0 and p < 0.001:
            return temps, counts
    raise AssertionError("regression slope never significantly positive in 200 tries")


def _gof_counts(rng, total=120):
    'Defect-category tally: dominant category (cold joint) true share 55%; redraw until the\n observed dominant share >= 50%, it is the max, no empty cell, and GOF p < 1e-6.'
    cum = []
    acc = 0.0
    for p in _CAT_PROBS:
        acc += p
        cum.append(acc)
    for _ in range(200):
        counts = [0] * len(_CAT_PROBS)
        for _ in range(total):
            r = rng.random()
            counts[next(i for i, c in enumerate(cum) if r <= c)] += 1
        ref = verifiers.chisquare_gof({"observed": counts})
        if (counts[0] == max(counts) and counts[0] * 2 >= total
                and min(counts) >= 1 and ref["pValue"] < 1e-6):
            return counts
    raise AssertionError("GOF tally never decisive in 200 tries")


# ---------------------------------------------------------------- generate

def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 70_800_019)

    cap_counts, cap_units = _baseline_counts(rng)
    u_counts, u_units = _u_chart_counts(rng)
    laney_counts, laney_units = _laney_counts(rng)
    temps, reg_counts = _regression_counts(rng)
    gof_counts = _gof_counts(rng)

    blocks = {
        "P_PoissonCapability": {"defectCounts": cap_counts, "inspectionUnits": cap_units,
                                "target": _TARGET_DPU, "confidenceLevel": 0.95},
        "P_UChart": {"defectCounts": u_counts, "unitCounts": u_units},
        "P_LaneyU": {"defectCounts": laney_counts, "unitCounts": laney_units},
        "P_PoissonRegression": {"x": temps, "counts": reg_counts,
                                "xName": 'reflow oven temperature (degC)', "yName": 'defects in the batch'},
        "P_GOF": {"observed": gof_counts, "categoryNames": list(_CATEGORIES),
                  "testType": "EQUAL_PROPORTIONS"},
    }

    truths = []
    truths += _derive("capability.poisson", blocks["P_PoissonCapability"], [
        ("dpu", 0.005, False, r"DPU"),
    ], "P_PoissonCapability", seed)
    truths.append(TruthEntry(
        method_id="control_chart.u", field="processMean",
        expected=round(_pooled_dpu(u_counts, u_units), 6), tol=0.005, soft=False,
        stage_id="P_UChart", metric_cue=r"ū|0\.0|cent(?:re|er)\s*line|centre-?line|center-?line|u-?bar|average defects per|defects per board",
        derivation=f"closed-form pooled DPU (U chart center line ū = Σcounts/Σunits), "
                   f"seed={seed}",
        verified_by=("closed-form",),
    ))
    truths.append(TruthEntry(
        method_id="control_chart.laney_u", field="sigmaZ",
        expected=round(_laney_sigma_z(laney_counts, laney_units), 6), tol=1.0, soft=False,
        stage_id="P_LaneyU", metric_cue=r"sigma|σ",
        derivation=f"self-implemented Laney σ_Z: z_i=(u_i-ū)/√(ū/n_i), σ_Z=MR̄(z)/1.128 "
                   f"(Laney 2002 / Minitab U′ convention), seed={seed}",
        verified_by=("generator-selfimpl",),
    ))
    truths += _derive("regression.poisson", blocks["P_PoissonRegression"], [
        ("deviance", 2.0, False, r"deviance"),
    ], "P_PoissonRegression", seed)
    truths += _derive("tables.chisquare_gof", blocks["P_GOF"], [
        ("chiSquare", 0.01, False, r"χ|chi"),
        ("pValue", 0.005, False, r"P\s*[=＝<＜]|goodness[- ]of[- ]fit|defect class|significan"),
    ], "P_GOF", seed)

    truths = tuple(truths)
    _assert_invariants(blocks, truths)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(blocks, truths):
    by = {(t.method_id, t.field): t.expected for t in truths}
    assert by[("capability.poisson", "dpu")] >= 0.07 > _TARGET_DPU, \
        "baseline DPU must be clearly above target"
    assert _u_chart_in_control(blocks["P_UChart"]["defectCounts"],
                               blocks["P_UChart"]["unitCounts"]), \
        "second-shop payload must be in control on a plain U chart"
    assert by[("control_chart.laney_u", "sigmaZ")] > 1.5, \
        "Laney payload must be overdispersed (σ_Z > 1.5)"
    assert by[("tables.chisquare_gof", "pValue")] < 0.01, "GOF must be decisive"
    obs = blocks["P_GOF"]["observed"]
    assert obs[0] == max(obs) and obs[0] * 2 >= sum(obs), 'cold joint must dominate (>= 50%)'
    slope, p = _poisson_slope(blocks["P_PoissonRegression"]["x"],
                              blocks["P_PoissonRegression"]["counts"])
    assert slope > 0 and p < 0.001, "temperature effect must be significantly positive"


if __name__ == "__main__":
    for s in range(1, 501):
        d = generate(s)
        if s <= 3 or s % 100 == 0:
            print(s, "ok:", {(t.method_id.split(".")[-1], t.field): t.expected for t in d.truths})
    print("500-seed sweep clean")
