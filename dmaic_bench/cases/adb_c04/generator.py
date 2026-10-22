"""adb_c04 generator — equal-variances gate → one-way ANOVA → sources-of-variation chain.

derive, never hand-write: equal-variances and one-way truths are DERIVED through truth/verifiers.py
(equal_variances: Levene with median centering / Brown-Forsythe; anova_oneway: scipy
f_oneway). anova.sov has no reference implementation — totalVariance is self-derived in this
generator as the pooled sample variance Σ(x-x̄)²/(n-1) over ALL stratified observations
(derivation documents the algorithm; entry is soft).

Data design invariants (hold for every seed, asserted below):
  - the four furnaces share one σ (=1.2 HRC) by construction and the sample is REDRAWN until
    Levene(median) p > 0.15 -> equal-variances premise clearly holds (p > 0.05 invariant);
  - furnace D runs ≈2σ hot in mean hardness -> one-way factor p < 0.01;
  - heat-to-heat (melt lot) effect σ≈2.0 dominates within-batch σ≈0.8 -> totalVariance
    is clearly larger than the within-batch variance alone.

Note: A_EqualVar and A_Oneway intentionally carry the SAME four-furnace dataset — the spread
check and the mean comparison are two questions asked of one sample, which is exactly why the
order constraint (premise check first) is meaningful.
"""
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402
from dmaic_bench.truth import verifiers  # noqa: E402

_FURNACES = ('Tempering furnace A', 'Tempering furnace B', 'Tempering furnace C', 'Tempering furnace D')


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260404)

    def _draw_furnaces(r):
        mus = {'Tempering furnace A': 42.0, 'Tempering furnace B': 41.8, 'Tempering furnace C': 42.2, 'Tempering furnace D': 44.5}
        return {"groups": {f: [round(r.gauss(mus[f], 1.2), 2) for _ in range(15)]
                           for f in _FURNACES}, "unit": "HRC"}

    for _ in range(300):
        furnace_block = _draw_furnaces(rng)
        if (verifiers.equal_variances(furnace_block)["pValue"] > 0.15
                and verifiers.anova_oneway(furnace_block)["factorPValue"] < 0.005):
            break
    else:
        raise AssertionError("adb_c04: could not construct equal-variance shifted groups")

    for _ in range(300):
        heat_means = [43.0 + rng.gauss(0.0, 2.0) for _ in range(6)]
        sov_block = {
            "groups": {f"Melt lot {i + 1}": [round(rng.gauss(hm, 0.8), 2) for _ in range(6)]
                       for i, hm in enumerate(heat_means)},
            "unit": "HRC",
            "note": 'hardness, sampled in strata by raw-material melt lot',
        }
        pooled = [x for vals in sov_block["groups"].values() for x in vals]
        n = len(pooled)
        mean = sum(pooled) / n
        total_variance = sum((x - mean) ** 2 for x in pooled) / (n - 1)
        within_var = _pooled_within_variance(sov_block["groups"])
        if total_variance > 1.5 * within_var:  # between-heat effect visibly dominates
            break
    else:
        raise AssertionError("adb_c04: could not construct dominant between-heat effect")

    # A_EqualVar and A_Oneway share the same dataset (see module docstring).
    blocks = {"A_EqualVar": furnace_block, "A_Oneway": dict(furnace_block),
              "A_SOV": sov_block}

    ev_ref = verifiers.equal_variances(furnace_block)
    ow_ref = verifiers.anova_oneway(furnace_block)
    # This payload declares no centring, and the three defensible equal-variance tests
    # disagree past the 0.1 window (Bartlett 0.410 vs Levene/median 0.860 on seed 1), which
    # is why the p-value was soft — and therefore unfailable. Both alternatives are
    # admitted at their own precision instead, and the entry goes hard.
    _ev_p = round(ev_ref["pValue"], 6)
    _ev_accepts = verifiers.convention_windows(
        "anova.equal_variances", "pValue", furnace_block, _ev_p, 0.1)
    _f_stat = round(ow_ref["fStatistic"], 6)
    _f_tol = round(0.1 * ow_ref["fStatistic"], 6)
    _f_accepts = verifiers.convention_windows(
        "anova.oneway", "fStatistic", furnace_block, _f_stat, _f_tol)
    truths = (
        TruthEntry(method_id="anova.equal_variances", field="pValue",
                   expected=_ev_p, tol=0.1, soft=False, accepts=_ev_accepts,
                   stage_id="A_EqualVar", metric_cue=r"[Ll]evene|[Bb]artlett|P\s*[=＝>＞]",
                   derivation=("derived via truth.verifiers.equal_variances: Levene test with "
                               "median centering (Brown-Forsythe); Bartlett lands within the "
                               f"soft tolerance for this near-normal data, seed={seed}"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="anova.oneway", field="factorPValue",
                   expected=round(ow_ref["factorPValue"], 6), tol=0.01, soft=False,
                   stage_id="A_Oneway", metric_cue=r"P\s*[=＝<＜]|furnace|mean hardness|hardness level",
                   derivation=("derived via truth.verifiers.anova_oneway "
                               f"(scipy.stats.f_oneway), seed={seed}"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="anova.oneway", field="fStatistic",
                   expected=_f_stat, tol=_f_tol, soft=False, accepts=_f_accepts,
                   stage_id="A_Oneway", metric_cue=r"F\s*[=＝]|F-?statistic|F-?ratio",
                   derivation=("derived via truth.verifiers.anova_oneway "
                               f"(scipy.stats.f_oneway); tol = 10% of F, seed={seed}"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="anova.sov", field="totalVariance",
                   expected=round(total_variance, 6),
                   # HARD: every source-of-variation convention decomposes the SAME total.
                   # The components are convention-variant; their sum is not.
                   tol=round(0.15 * total_variance, 6), soft=False,
                   stage_id="A_SOV", metric_cue=r"variance",
                   derivation=("self-derived in generator: total variance = Σ(x-x̄)²/(n-1) over "
                               "all 36 stratified observations pooled (sample variance, ddof=1); "
                               f"tol = 15% (convention-variant decompositions welcome), seed={seed}"),
                   verified_by=("python-closed-form",)),
    )

    _assert_invariants(truths, total_variance, within_var)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _pooled_within_variance(groups):
    num, den = 0.0, 0
    for vals in groups.values():
        m = sum(vals) / len(vals)
        num += sum((x - m) ** 2 for x in vals)
        den += len(vals) - 1
    return num / den


def _assert_invariants(truths, total_variance, within_var):
    by = {(t.method_id, t.field): t.expected for t in truths}
    assert by[("anova.equal_variances", "pValue")] > 0.05, "variance homogeneity must hold"
    assert by[("anova.oneway", "factorPValue")] < 0.01, "furnace effect must be significant"
    assert total_variance > within_var, "between-heat effect must inflate total variance"


if __name__ == "__main__":
    bad = []
    for s in range(1, 501):
        try:
            generate(s)
        except AssertionError as e:
            bad.append((s, str(e)))
    print("failed seeds:", bad if bad else "NONE (500/500)")
