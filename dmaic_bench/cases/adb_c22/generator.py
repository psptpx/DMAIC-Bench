"""adb_c22 generator — machining bore-diameter sequence + 3-machine comparison case.

"derive, never hand-write": all truths are re-derived from the exact (rounded) block payloads by the in-file
implementations below (numpy/scipy only; truth/verifiers.py is NOT touched). Payload shapes
are verifier-compatible so V7 re-verifies both stages:

  nonparametric.runs_test     {data: [...]} with the default aboutMean=True convention —
                              classify each value against the SAMPLE MEAN, count runs, normal
                              approximation z = (R - mu_R)/sd_R, two-sided p (identical formula
                              to truth/verifiers.runs_test).
  nonparametric.moods_median  {groups: {name: [...]}} — scipy.stats.median_test(*groups) with
                              library defaults (ties='below'; the 2x3 table gets no Yates
                              correction), identical call to truth/verifiers.moods_median.

Data design invariants (hold for every seed, asserted below):
  - the sequence is genuinely random BY CONSTRUCTION: iid Gaussian draws are accepted only
    when the runs-test p exceeds 0.2 (deterministic per seed; ~80% acceptance rate), so the
    "random fluctuation" conclusion is determinate for every seed (p > 0.05 guaranteed);
  - machine C runs ~3 sigma above machines A/B (n=25 each) -> Mood's median p < 0.01.
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

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402


def _runs_pvalue(data):
    """Identical convention to truth/verifiers.runs_test (aboutMean=True default)."""
    x = np.asarray(data, float)
    center = float(np.mean(x))
    signs = x > center
    if np.any(x == center):
        signs = signs[x != center]
    n1, n2 = int(np.sum(signs)), int(np.sum(~signs))
    runs = 1 + int(np.sum(signs[1:] != signs[:-1]))
    mu = 2 * n1 * n2 / (n1 + n2) + 1
    var = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
    z = (runs - mu) / math.sqrt(var)
    return float(2 * stats.norm.sf(abs(z)))


def _moods_pvalue(groups):
    """Identical call to truth/verifiers.moods_median: scipy.stats.median_test defaults."""
    res = stats.median_test(*[np.asarray(v, float) for v in groups.values()])
    return float(res.pvalue)


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260604)

    # --- S_Runs: one machine, 40 consecutive bore diameters (mm) ----------------------------
    # Accept only sequences whose runs-test p > 0.2 -> genuinely random by construction.
    sequence = None
    for _ in range(400):
        cand = [round(rng.gauss(16.020, 0.012), 4) for _ in range(40)]
        if _runs_pvalue(cand) > 0.2:
            sequence = cand
            break
    assert sequence is not None, "failed to draw a random-looking sequence in 400 tries"

    # --- S_Moods: three machines, machine C shifted ~3 sigma up -----------------------------
    shift_c = 0.034 + rng.uniform(0.0, 0.008)
    groups = {
        'Lathe A': [round(rng.gauss(16.020, 0.012), 4) for _ in range(25)],
        'Lathe B': [round(rng.gauss(16.022, 0.012), 4) for _ in range(25)],
        'Lathe C': [round(rng.gauss(16.020 + shift_c, 0.012), 4) for _ in range(25)],
    }

    blocks = {
        "S_Runs": {"data": sequence, "aboutMean": True, "unit": "mm",
                   "note": 'bore diameters from one lathe, recorded consecutively in machining order'},
        "S_Moods": {"groups": groups, "unit": "mm",
                    "note": 'bore diameters cut on each of three lathes of the same model'},
    }

    p_runs = _runs_pvalue(blocks["S_Runs"]["data"])
    p_moods = _moods_pvalue(blocks["S_Moods"]["groups"])

    truths = (
        # HARD: the payload declares `aboutMean`, so the mean-vs-median centring that would
        # otherwise be a real convention split is specified rather than guessed.
        TruthEntry("nonparametric.runs_test", "pValue", round(p_runs, 6), 0.1,
                   soft=False, stage_id="S_Runs", metric_cue=r"P\s*[=＝<＜]|random|sequence|pattern|machining order",
                   derivation=f"in-generator runs test about the sample mean (normal "
                              f"approximation, same convention as truth/verifiers.runs_test), "
                              f"recomputed from block payload; seed={seed}",
                   verified_by=("scipy",)),
        TruthEntry("nonparametric.moods_median", "pValue", round(p_moods, 6), 0.01,
                   soft=False, stage_id="S_Moods", metric_cue=r"P\s*[=＝<＜]|lathe|median|central level",
                   derivation=f"scipy.stats.median_test with library defaults (identical call "
                              f"to truth/verifiers.moods_median), recomputed from block "
                              f"payload; seed={seed}", verified_by=("scipy",)),
    )

    _assert_invariants(p_runs, p_moods)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(p_runs, p_moods):
    assert p_runs > 0.05, f"sequence must look random, runs p={p_runs}"
    assert p_moods < 0.01, f"machine shift must be significant, Mood's p={p_moods}"


if __name__ == "__main__":
    worst = {"runsP": 1.0, "moodsP": 0.0}
    for s in range(1, 501):
        d = generate(s)
        by = {t.method_id: t.expected for t in d.truths}
        worst["runsP"] = min(worst["runsP"], by["nonparametric.runs_test"])
        worst["moodsP"] = max(worst["moodsP"], by["nonparametric.moods_median"])
    print("500 seeds ok; min runs p =", worst["runsP"], "max moods p =", worst["moodsP"])
