'adb_c11 generator — 2^3 full-factorial injection-molding warpage case.\n\n"derive, never hand-write": every numeric truth is re-derived from the exact (rounded) block payload by the\nin-file OLS below (numpy/scipy only; truth/verifiers.py is NOT touched). Algorithm conventions,\nstated once here and referenced by every TruthEntry.derivation:\n\n doe.factorial_analysis y ~ [1, A, B, C, AB, AC, BC] OLS on the coded ±1 design via\n np.linalg.lstsq; rSquaredPct = 100*(1 - SSres/SStot);\n modelPValue = overall F-test, F = (R2/k)/((1-R2)/(n-k-1)),\n k=6, n=16, p = scipy.stats.f.sf(F, k, n-k-1).\n doe.factorial_prediction predictedValue = x*\' @ beta_hat at coded settings A=+1, B=-1, C=0\n from the SAME fitted model (all C-involving terms vanish at C=0).\n\nData design invariants (hold for every seed, asserted below):\n - A(holding pressure)/B(melt temperature) main effects and the AB interaction are strong (|t| >> 3, p < 0.01);\n - C(cooling time) is inert BY CONSTRUCTION: the noise vector is orthogonalized against the\n C, AC, BC design columns and C carries only a tiny true coefficient (|bC| <= 0.012),\n so p_C > 0.2 for every seed -> the effect_screen decision point (drop C) is determinate;\n - overall model p < 0.01 and R^2 > 70%.'
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402

_FACTORS = (
    {"name": 'holding pressure', "code": "A", "low": 60.0, "high": 90.0, "unit": "MPa"},
    {"name": 'melt temperature', "code": "B", "low": 220.0, "high": 250.0, "unit": 'degC'},
    {"name": 'cooling time', "code": "C", "low": 15.0, "high": 25.0, "unit": "s"},
)
_SETTINGS = {"A": 1, "B": -1, "C": 0}
_DERIV_NOTE = ("in-generator OLS on coded design [1,A,B,C,AB,AC,BC] (np.linalg.lstsq + "
               "scipy.stats overall F-test), recomputed from the rounded block payload")


def _design_row(a, b, c):
    return [1.0, a, b, c, a * b, a * c, b * c]


def _fit(runs):
    """Main effects + all two-way interactions OLS; returns (beta, r2, modelP, term p-values)."""
    x_mat = np.array([_design_row(r["A"], r["B"], r["C"]) for r in runs], dtype=float)
    y = np.array([r["y"] for r in runs], dtype=float)
    beta, *_ = np.linalg.lstsq(x_mat, y, rcond=None)
    resid = y - x_mat @ beta
    n, k = len(y), x_mat.shape[1] - 1
    ss_res = float(resid @ resid)
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot
    f = (r2 / k) / ((1.0 - r2) / (n - k - 1))
    model_p = float(stats.f.sf(f, k, n - k - 1))
    mse = ss_res / (n - k - 1)
    se = float(np.sqrt(mse / n))  # orthogonal ±1 design: Var(b_j) = MSE/n for every j
    pvals = 2.0 * stats.t.sf(np.abs(beta / se), n - k - 1)
    return beta, r2, model_p, pvals


def _predict(beta, settings):
    return float(np.array(_design_row(settings["A"], settings["B"], settings["C"])) @ beta)


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260601)

    b0 = 2.10 + rng.uniform(-0.15, 0.15)
    b_a = -0.45 + rng.uniform(-0.05, 0.05)   # higher packing pressure -> less warpage
    b_b = 0.35 + rng.uniform(-0.04, 0.04)    # higher melt temperature -> more warpage
    b_ab = 0.26 + rng.uniform(-0.03, 0.03)
    b_c = rng.uniform(-0.012, 0.012)         # cooling time: inert by design

    cells = [(a, b, c) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)] * 2  # 2 replicates
    rng.shuffle(cells)
    x_mat = np.array([_design_row(*cell) for cell in cells], dtype=float)
    noise = np.array([rng.gauss(0.0, 0.11) for _ in cells])
    # Orthogonalize noise against every C-involving column (C, AC, BC are mutually orthogonal
    # in the full factorial) so the C terms stay deterministically negligible for every seed.
    for col in (3, 5, 6):
        v = x_mat[:, col]
        noise = noise - v * float(noise @ v) / float(v @ v)
    y = x_mat @ np.array([b0, b_a, b_b, b_c, b_ab, 0.0, 0.0]) + noise
    runs = [{"A": a, "B": b, "C": c, "y": round(float(val), 4)}
            for (a, b, c), val in zip(cells, y)]

    blocks = {
        "D_Create": {
            "factors": [dict(f) for f in _FACTORS],
            "replicates": 2,
            "centerPoints": 0,
            "objective": 'warpage (mm), smaller is better',
            "constraint": 'one round may run at most twenty trials, must cover every high/low combination of the three settings, and must include repeats',
        },
        "D_Analyze": {
            "response": 'warpage (mm)',
            "coding": {"A": 'holding pressure 60 MPa -> -1 / 90 MPa -> +1',
                       "B": 'melt temperature 220 degC -> -1 / 250 degC -> +1',
                       "C": 'cooling time 15 s -> -1 / 25 s -> +1'},
            "runs": runs,
        },
        "D_Predict": {
            "model_from": "D_Analyze",
            "settings": dict(_SETTINGS),
            "note": 'recommended combination: A=+1 (holding pressure 90 MPa), B=-1 (melt temperature 220 degC), C=0 (cooling 20 s, mid-range is fine)',
        },
    }

    beta, r2, model_p, pvals = _fit(runs)
    pred = _predict(beta, _SETTINGS)

    truths = (
        TruthEntry("doe.factorial_analysis", "rSquaredPct", round(100.0 * r2, 6), 5.0,
                   soft=False, stage_id="D_Analyze", metric_cue=r"R.?2|R²|R-?squared|R-?sq|explain",
                   derivation=f"{_DERIV_NOTE}; seed={seed}", verified_by=("numpy", "scipy")),
        TruthEntry("doe.factorial_analysis", "modelPValue", round(model_p, 6), 0.01,
                   soft=False, stage_id="D_Analyze", metric_cue=r"P\s*[=＝<＜]|model|warpage",
                   derivation=f"{_DERIV_NOTE}; seed={seed}", verified_by=("numpy", "scipy")),
        TruthEntry("doe.factorial_prediction", "predictedValue", round(pred, 6),
                   round(0.10 * abs(pred), 6),  # relative 10%
                   soft=False, stage_id="D_Predict", metric_cue=r"predicted",
                   derivation=f"point prediction x*'beta at A=+1,B=-1,C=0 from the same "
                              f"fitted model ({_DERIV_NOTE}); seed={seed}",
                   verified_by=("numpy",)),
    )

    _assert_invariants(model_p, r2, pvals)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(model_p, r2, pvals):
    assert model_p < 0.01, f"model must be significant, got p={model_p}"
    assert r2 > 0.70, f"R^2 must exceed 70%, got {100 * r2:.1f}%"
    assert pvals[1] < 0.01, f"A main effect must be significant, p={pvals[1]}"
    assert pvals[2] < 0.01, f"B main effect must be significant, p={pvals[2]}"
    assert pvals[4] < 0.01, f"AB interaction must be significant, p={pvals[4]}"
    assert pvals[3] > 0.2, f"C main effect must be inert, p={pvals[3]}"


if __name__ == "__main__":
    worst = {"modelP": 0.0, "r2": 100.0}
    for s in range(1, 501):
        d = generate(s)
        by = {(t.method_id, t.field): t.expected for t in d.truths}
        worst["modelP"] = max(worst["modelP"], by[("doe.factorial_analysis", "modelPValue")])
        worst["r2"] = min(worst["r2"], by[("doe.factorial_analysis", "rSquaredPct")])
    print("500 seeds ok; worst modelP =", worst["modelP"], "min R2% =", worst["r2"])
