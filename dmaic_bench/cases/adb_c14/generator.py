"""adb_c14 generator — bank branch waiting time vs satisfaction / complaint case.

"derive, never hand-write": all truths are re-derived from the exact (rounded) block payloads by the in-file
implementations below (numpy/scipy/statsmodels only; truth/verifiers.py is NOT touched).
Algorithm conventions, referenced by every TruthEntry.derivation:

  regression.ols              simple OLS with the SAME convention as truth/verifiers.ols so V7
                              re-verifies: X = np.vander(x, degree+1, increasing=True) lstsq;
                              rSquaredPct = 100*(1 - SSres/SStot); modelPValue = overall F-test
                              F = (R2/k)/((1-R2)/(n-k-1)), k=degree=1, p = scipy.stats.f.sf.
                              Payload shape {x, y, degree} is verifier-compatible.
  regression.binary_logistic  statsmodels Logit(outcomes ~ const + x) MLE; modelPValue =
                              likelihood-ratio test p-value (fit.llr_pvalue).

Data design invariants (hold for every seed, asserted below):
  - satisfaction drops strongly with waiting time -> OLS model p < 1e-4 and R^2 > 60%;
  - complaint odds rise with waiting time (true log-odds slope ~ +0.28 over a 1-30 min
    range, n=90) -> Logit LR p < 0.01 and fitted slope > 0, with MLE convergence asserted.
"""
import math
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402
import statsmodels.api as sm  # noqa: E402

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402


def _ols(x, y, degree=1):
    """Same convention as truth/verifiers.ols (vander + lstsq + overall F-test)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    x_mat = np.vander(x, degree + 1, increasing=True)
    beta, *_ = np.linalg.lstsq(x_mat, y, rcond=None)
    resid = y - x_mat @ beta
    ss_res, ss_tot = float(resid @ resid), float(np.sum((y - y.mean()) ** 2))
    n, k = len(y), degree
    r2 = 1.0 - ss_res / ss_tot
    f = (r2 / k) / ((1.0 - r2) / (n - k - 1))
    return {"rSquaredPct": 100.0 * r2, "modelPValue": float(stats.f.sf(f, k, n - k - 1))}


def _logit_lr(x, outcomes):
    fit = sm.Logit(np.asarray(outcomes, float),
                   sm.add_constant(np.asarray(x, float))).fit(disp=0)
    assert fit.mle_retvals["converged"], "Logit MLE must converge"
    return {"modelPValue": float(fit.llr_pvalue), "slope": float(fit.params[1])}


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260603)

    # --- G_OLS: waiting time (min) vs immediate satisfaction score (0-100), n=40 ------------
    wait_sat = [round(rng.uniform(1.0, 30.0), 1) for _ in range(40)]
    sat = [round(88.0 - 1.2 * w + rng.gauss(0.0, 3.0), 2) for w in wait_sat]

    # --- G_Logistic: waiting time vs 30-day complaint outcome (0/1), n=90 --------------------
    b0_true = -3.4 + rng.uniform(-0.2, 0.2)
    b1_true = 0.28 + rng.uniform(-0.03, 0.03)
    wait_cmp = [round(rng.uniform(1.0, 30.0), 1) for _ in range(90)]
    outcomes = [1 if rng.random() < 1.0 / (1.0 + math.exp(-(b0_true + b1_true * w))) else 0
                for w in wait_cmp]

    blocks = {
        "G_OLS": {"x": wait_sat, "y": sat, "degree": 1,
                  "xName": 'wait time (minutes)', "yName": 'satisfaction score (0-100)'},
        "G_Logistic": {"x": wait_cmp, "outcomes": outcomes,
                       "xName": 'wait time (minutes)', "outcomeName": 'complaint within 30 days (1 = complained)'},
    }

    ols = _ols(blocks["G_OLS"]["x"], blocks["G_OLS"]["y"], blocks["G_OLS"]["degree"])
    logit = _logit_lr(blocks["G_Logistic"]["x"], blocks["G_Logistic"]["outcomes"])

    truths = (
        TruthEntry("regression.ols", "rSquaredPct", round(ols["rSquaredPct"], 6), 3.0,
                   soft=False, stage_id="G_OLS", metric_cue=r"R.?2|R²|R-?squared|R-?sq|explain",
                   derivation=f"in-generator OLS with the verifiers.ols convention (vander + "
                              f"lstsq + overall F-test), recomputed from block payload; "
                              f"seed={seed}", verified_by=("numpy", "scipy")),
        TruthEntry("regression.ols", "modelPValue", round(ols["modelPValue"], 6), 0.001,
                   soft=False, stage_id="G_OLS", metric_cue=r"P\s*[=＝<＜]|satisfaction|significan",
                   derivation=f"in-generator OLS overall F-test (verifiers.ols convention, "
                              f"k=1, n=40, scipy.stats.f.sf); seed={seed}",
                   verified_by=("numpy", "scipy")),
        TruthEntry("regression.binary_logistic", "modelPValue",
                   round(logit["modelPValue"], 6), 0.01,
                   soft=False, stage_id="G_Logistic", metric_cue=r"P\s*[=＝<＜]|complaint|logistic",
                   derivation=f"statsmodels Logit(outcomes ~ const + x) likelihood-ratio "
                              f"test p-value (fit.llr_pvalue), recomputed from block payload; "
                              f"seed={seed}", verified_by=("statsmodels",)),
    )

    _assert_invariants(ols, logit)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(ols, logit):
    assert ols["modelPValue"] < 1e-4, f"OLS model must be significant, p={ols['modelPValue']}"
    assert ols["rSquaredPct"] > 60.0, f"OLS R^2 must exceed 60%, got {ols['rSquaredPct']:.1f}%"
    assert logit["modelPValue"] < 0.01, f"Logit LR must be significant, p={logit['modelPValue']}"
    assert logit["slope"] > 0.0, f"complaint odds must rise with waiting, slope={logit['slope']}"


if __name__ == "__main__":
    worst = {"olsP": 0.0, "r2": 100.0, "logitP": 0.0, "slope": 1e9}
    for s in range(1, 501):
        d = generate(s)
        by = {(t.method_id, t.field): t.expected for t in d.truths}
        worst["olsP"] = max(worst["olsP"], by[("regression.ols", "modelPValue")])
        worst["r2"] = min(worst["r2"], by[("regression.ols", "rSquaredPct")])
        worst["logitP"] = max(worst["logitP"], by[("regression.binary_logistic", "modelPValue")])
    print("500 seeds ok; worst olsP =", worst["olsP"], "min R2% =", round(worst["r2"], 2),
          "worst logitP =", worst["logitP"])
