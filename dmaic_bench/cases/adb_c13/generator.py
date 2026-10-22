"""adb_c13 generator — the reference example of a fully parametric native case.

"derive, never hand-write": every truth entry is DERIVED from the freshly generated data through the shared
reference implementations (truth/verifiers.py, scipy-backed), never hand-written. Changing the
seed changes both data and truths together — this is what makes the case contamination-proof.

Data design invariants (hold for every seed, asserted below):
  - baseline thickness is right-skewed enough that AD normality fails (p < 0.05) -> the
    normality_gate decision point has a determinate correct branch;
  - supplier B is shifted ~+1.2σ vs supplier A -> Mann-Whitney significant;
  - line 3 is shifted vs lines 1/2 -> Kruskal-Wallis significant;
  - target-median stage data sits clearly above the declared target -> Wilcoxon significant;
  - thickness rises with bath temperature (r ≈ 0.75–0.95) -> correlation strong.
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

_TARGET_MEDIAN = 8.0


def _lognormal(rng, n, base, sigma, shift=0.0):
    return [round(base * math.exp(rng.gauss(0.0, sigma)) + shift, 4) for _ in range(n)]


def _derive(method_id, block, entries, stage_id, seed):
    """Run the reference implementation and turn selected outputs into TruthEntry rows."""
    ref = verifiers.REFERENCE_IMPLS[method_id](block)
    out = []
    for field, tol, soft, cue in entries:
        out.append(TruthEntry(
            method_id=method_id, field=field, expected=round(ref[field], 6), tol=tol, soft=soft,
            stage_id=stage_id, metric_cue=cue,
            derivation=f"derived from generated payload via truth.verifiers.{method_id} "
                       f"(scipy), seed={seed}",
            verified_by=("scipy",),
        ))
    return out


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260707)

    # 30 body points + 6 structural heavy-tail excursions (>=2.7x body scale) — guarantees the
    # baseline fails AD normality for EVERY seed, keeping the normality_gate branch determinate.
    baseline = _lognormal(rng, 30, base=7.4, sigma=0.30, shift=0.3) + [
        round(7.4 * math.exp(1.0 + abs(rng.gauss(0.0, 0.35))) + 0.3, 4) for _ in range(6)
    ]
    rng.shuffle(baseline)
    supplier_a = _lognormal(rng, 30, base=7.2, sigma=0.25, shift=0.2)
    supplier_b = _lognormal(rng, 30, base=12.8, sigma=0.25, shift=0.2)
    lines = {
        "line1": _lognormal(rng, 24, base=7.3, sigma=0.25, shift=0.2),
        "line2": _lognormal(rng, 24, base=7.5, sigma=0.25, shift=0.2),
        "line3": _lognormal(rng, 24, base=13.2, sigma=0.25, shift=0.2),
    }
    target_sample = _lognormal(rng, 26, base=11.4, sigma=0.22, shift=0.3)
    temps = [round(52.0 + 8.0 * i / 19 + rng.gauss(0, 0.35), 3) for i in range(20)]
    thickness = [round(0.32 * (t - 52.0) + 7.0 + rng.gauss(0, 0.40), 4) for t in temps]

    blocks = {
        "N_Summary": {"data": baseline, "unit": "um"},
        "N_MannWhitney": {"group1": supplier_a, "group2": supplier_b,
                          "group1Name": 'Supplier A', "group2Name": 'Supplier B', "unit": "um"},
        "N_KruskalWallis": {"groups": lines, "unit": "um"},
        "N_Wilcoxon": {"data": target_sample, "hypothesizedMedian": _TARGET_MEDIAN, "unit": "um"},
        "N_Correlation": {"x": temps, "y": thickness,
                          "xName": 'bath temperature (degC)', "yName": 'plating thickness (um)'},
    }

    truths = []
    truths += _derive("basic.descriptive_summary", blocks["N_Summary"], [
        ("mean", 1e-3, False, r"mean"),
        ("median", 1e-3, False, r"median"),
        # Both hard: the adjusted (G1) and biased (b1) skewness conventions differ by <0.09
        # here, inside the window; the AD p-value has no second convention at this scale.
        ("skewness", 0.15, False, r"skew"),
        ("adPValue", 0.01, False, r"AD|anderson"),
    ], "N_Summary", seed)
    truths += _derive("nonparametric.mann_whitney", blocks["N_MannWhitney"], [
        ("pValue", 0.01, False, r"Mann|P\s*[=＝<＜]"),
    ], "N_MannWhitney", seed)
    truths += _derive("nonparametric.kruskal_wallis", blocks["N_KruskalWallis"], [
        ("pValue", 0.01, False, r"Kruskal|P\s*[=＝<＜]"),
    ], "N_KruskalWallis", seed)
    truths += _derive("nonparametric.one_sample_wilcoxon", blocks["N_Wilcoxon"], [
        ("pValue", 0.01, False, r"Wilcoxon|P\s*[=＝<＜]"),
    ], "N_Wilcoxon", seed)
    truths += _derive("basic.correlation", blocks["N_Correlation"], [
        ("correlationCoefficient", 0.02, False, r"correlation|r\s*[=＝]"),
        ("pValue", 0.005, False, None),
    ], "N_Correlation", seed)

    _assert_invariants(blocks, truths)
    return CaseData(seed=seed, blocks=blocks, truths=tuple(truths))


def _assert_invariants(blocks, truths):
    by = {(t.method_id, t.field): t.expected for t in truths}
    assert by[("basic.descriptive_summary", "adPValue")] < 0.05, "baseline must fail normality"
    assert by[("nonparametric.mann_whitney", "pValue")] < 0.01, "supplier shift must be significant"
    assert by[("nonparametric.kruskal_wallis", "pValue")] < 0.01, "line shift must be significant"
    assert by[("nonparametric.one_sample_wilcoxon", "pValue")] < 0.01, "target shift must be significant"
    assert by[("basic.correlation", "correlationCoefficient")] > 0.6, "temp correlation must be strong"


if __name__ == "__main__":
    for s in (1, 2, 3, 20260707):
        d = generate(s)
        print(s, "ok:", {(t.method_id.split('.')[-1], t.field): t.expected for t in d.truths})
