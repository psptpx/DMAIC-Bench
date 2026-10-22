"""adb_c01 generator — 2-factor CCD reactor-yield case (maximum-type quadratic surface).

"derive, never hand-write": all truths are re-derived from the exact (rounded) block payload by the in-file
quadratic OLS + closed-form canonical analysis below (numpy/scipy only; truth/verifiers.py is
NOT touched). Algorithm conventions, referenced by every TruthEntry.derivation:

  doe.rsm_analysis    y ~ [1, x1, x2, x1^2, x2^2, x1*x2] full-quadratic OLS via
                      np.linalg.lstsq on the coded CCD; rSquaredPct = 100*(1 - SSres/SStot).
  doe.rsm_canonical   b = [beta1, beta2], B = [[beta11, beta12/2], [beta12/2, beta22]];
                      stationary point xs = solve(B, -b/2); predictedAtStationary =
                      beta0 + b'xs + xs'B xs; surface type from np.linalg.eigvalsh(B).
  doe.rsm_optimizer   the true surface is constructed negative-definite with its stationary
                      point inside |xi| <= 0.6, i.e. the interior maximum of the fitted surface
                      over the bounds [-1.414, 1.414]^2 IS the stationary point ->
                      predictedResponse = predictedAtStationary.

Design: 13 runs = 4 corners (±1, ±1) + 4 axial (±1.414, 0)/(0, ±1.414) + 5 center points.

Data design invariants (hold for every seed, asserted below):
  - fitted quadratic eigenvalues are all negative (MAXIMUM-type surface);
  - fitted stationary point lies inside [-1.2, 1.2]^2 (true point drawn inside ±0.5);
  - R^2 > 85% (noise sd 0.45 vs quadratic signal spanning >10 yield points).
"""
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

import numpy as np  # noqa: E402

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402

_ALPHA = 1.414
_FACTORS = (
    {"name": 'reaction temperature', "code": "x1", "center": 150.0, "halfWidth": 10.0, "unit": 'degC'},
    {"name": 'catalyst charge', "code": "x2", "center": 2.0, "halfWidth": 0.5, "unit": "wt%"},
)
_DERIV_NOTE = ("in-generator full-quadratic OLS [1,x1,x2,x1^2,x2^2,x1x2] (np.linalg.lstsq) "
               "recomputed from the rounded block payload")


def _xrow(x1, x2):
    return [1.0, x1, x2, x1 * x1, x2 * x2, x1 * x2]


def _fit(runs):
    x_mat = np.array([_xrow(r["x1"], r["x2"]) for r in runs], dtype=float)
    y = np.array([r["y"] for r in runs], dtype=float)
    beta, *_ = np.linalg.lstsq(x_mat, y, rcond=None)
    resid = y - x_mat @ beta
    r2 = 1.0 - float(resid @ resid) / float(np.sum((y - y.mean()) ** 2))
    return beta, r2


def _canonical(beta):
    """Closed-form stationary-point analysis: xs = -B^{-1} b / 2, ys = beta0 + b'xs + xs'B xs."""
    b = np.array([beta[1], beta[2]])
    b_mat = np.array([[beta[3], beta[5] / 2.0], [beta[5] / 2.0, beta[4]]])
    xs = np.linalg.solve(b_mat, -b / 2.0)
    y_s = float(beta[0] + b @ xs + xs @ b_mat @ xs)
    eig = np.linalg.eigvalsh(b_mat)
    return xs, y_s, eig


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260602)

    q11 = -6.0 + rng.uniform(-0.8, 0.8)
    q22 = -5.0 + rng.uniform(-0.8, 0.8)
    q12 = 1.0 + rng.uniform(-0.4, 0.4)
    b_mat = np.array([[q11, q12 / 2.0], [q12 / 2.0, q22]])
    xs_true = np.array([rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)])
    bvec = -2.0 * b_mat @ xs_true            # puts the true stationary point at xs_true
    beta0 = 82.0 + rng.uniform(-3.0, 3.0)

    pts = ([(-1.0, -1.0), (1.0, -1.0), (-1.0, 1.0), (1.0, 1.0),
            (-_ALPHA, 0.0), (_ALPHA, 0.0), (0.0, -_ALPHA), (0.0, _ALPHA)]
           + [(0.0, 0.0)] * 5)
    rng.shuffle(pts)
    runs = []
    for x1, x2 in pts:
        mean = (beta0 + bvec[0] * x1 + bvec[1] * x2
                + q11 * x1 * x1 + q22 * x2 * x2 + q12 * x1 * x2)
        runs.append({"x1": x1, "x2": x2, "y": round(mean + rng.gauss(0.0, 0.45), 3)})

    blocks = {
        "R_Analyze": {
            "response": 'yield (%)',
            "design": 'combinations of the two settings plus centre points plus outer points, thirteen charges in all (coded units)',
            "factors": [dict(f) for f in _FACTORS],
            "runs": runs,
        },
        "R_Canonical": {
            "model_from": "R_Analyze",
            "runs": runs,
            "question": 'at which coded coordinates does the yield turn over, what kind of turning point is it, and what yield is predicted there?',
        },
        "R_Optimize": {
            "surface_data": runs,
            "goal": "maximize",
            "bounds": [[-_ALPHA, _ALPHA], [-_ALPHA, _ALPHA]],
            "response": 'yield (%)',
        },
    }

    beta, r2 = _fit(runs)
    xs, y_s, eig = _canonical(beta)

    truths = (
        # HARD: R^2 of the stated full-quadratic model is a single defined quantity — the
        # adjusted variant is a different FIELD, not another convention for this one.
        TruthEntry("doe.rsm_analysis", "rSquaredPct", round(100.0 * r2, 6), 5.0,
                   soft=False, stage_id="R_Analyze", metric_cue=r"R.?2|R²|R-?squared|R-?sq|explain",
                   derivation=f"{_DERIV_NOTE}; seed={seed}", verified_by=("numpy",)),
        TruthEntry("doe.rsm_canonical", "predictedAtStationary", round(y_s, 6),
                   round(0.05 * abs(y_s), 6),  # relative 5%
                   soft=False, stage_id="R_Canonical", metric_cue=r"stationary",
                   derivation=f"closed-form canonical analysis xs=-B^-1 b/2 on coefficients "
                              f"from {_DERIV_NOTE}; eigenvalues via np.linalg.eigvalsh; "
                              f"seed={seed}", verified_by=("numpy",)),
        TruthEntry("doe.rsm_optimizer", "predictedResponse", round(y_s, 6),
                   round(0.05 * abs(y_s), 6),  # relative 5%
                   soft=False, stage_id="R_Optimize", metric_cue=r"recommend|optimal|optimum|predicted",
                   derivation=f"surface built negative-definite with stationary point inside "
                              f"the bounds, so the constrained maximum equals "
                              f"predictedAtStationary ({_DERIV_NOTE}); seed={seed}",
                   verified_by=("numpy",)),
    )

    _assert_invariants(r2, xs, eig)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(r2, xs, eig):
    assert np.all(eig < 0), f"fitted surface must be MAXIMUM-type, eigenvalues={eig}"
    assert np.all(np.abs(xs) <= 1.2), f"stationary point must stay in [-1.2,1.2]^2, xs={xs}"
    assert r2 > 0.85, f"R^2 must exceed 85%, got {100 * r2:.1f}%"


if __name__ == "__main__":
    worst = {"r2": 1.0, "maxAbsXs": 0.0, "maxEig": -1e9}
    for s in range(1, 501):
        d = generate(s)
        beta, r2 = _fit(d.blocks["R_Analyze"]["runs"])
        xs, _, eig = _canonical(beta)
        worst["r2"] = min(worst["r2"], r2)
        worst["maxAbsXs"] = max(worst["maxAbsXs"], float(np.max(np.abs(xs))))
        worst["maxEig"] = max(worst["maxEig"], float(np.max(eig)))
    print("500 seeds ok; min R2 =", round(worst["r2"], 4),
          "max |xs| =", round(worst["maxAbsXs"], 4),
          "max eigenvalue =", round(worst["maxEig"], 4))
