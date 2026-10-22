"""adb_c02 generator — the parametric mirror of adb_c13 (t-family case).

"derive, never hand-write": every truth is DERIVED from the freshly generated data through the reference
implementations in truth/verifiers.py (scipy-backed: AD normality approximation, one-sample t,
Welch two-sample t, paired t).

Data design invariants (hold for every seed, asserted below):
  - baseline fill volume is genuinely Gaussian (n=40) and REDRAWN until AD normality p > 0.12
    -> the normality_gate decision point has a determinate correct branch (parametric, the
    mirror image of adb_c13);
  - fill volume sits ~1.25σ above the 250 ml label value -> one-sample t significant (p<0.01);
  - filler #1 vs filler #2 are separated by ~2σ -> Welch two-sample t significant (p<0.01);
  - nozzle adjustment lowers each paired batch by ~1.6 ml (pair σ≈0.5) -> paired t
    significant (p<0.01).
"""
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402
from dmaic_bench.truth import verifiers  # noqa: E402

_LABEL_ML = 250.0


def _gauss_series(rng, n, mu, sigma, nd=3):
    return [round(rng.gauss(mu, sigma), nd) for _ in range(n)]


def _redraw(rng, draw_fn, ok_fn, what, tries=300):
    for _ in range(tries):
        block = draw_fn(rng)
        if ok_fn(block):
            return block
    raise AssertionError(f"adb_c02: could not construct {what} in {tries} draws")


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260402)

    baseline = _redraw(
        rng,
        lambda r: {"data": _gauss_series(r, 40, 251.0, 1.2), "unit": "ml"},
        lambda b: verifiers.normality(b)["pValue"] > 0.12,
        "Gaussian baseline with AD p>0.12")
    one_sample = _redraw(
        rng,
        lambda r: {"data": _gauss_series(r, 30, 251.5, 1.2), "mu": _LABEL_ML, "unit": "ml"},
        lambda b: verifiers.one_sample_t(b)["pValue"] < 0.005,
        "one-sample shift above label value")
    two_sample = _redraw(
        rng,
        lambda r: {"group1": _gauss_series(r, 25, 251.6, 1.1),
                   "group2": _gauss_series(r, 25, 249.4, 1.1),
                   "group1Name": 'Machine 1', "group2Name": 'Machine 2', "unit": "ml"},
        lambda b: verifiers.two_sample_t(b)["pValue"] < 0.005,
        "two-machine separation")

    def _draw_paired(r):
        before = _gauss_series(r, 20, 251.8, 1.0)
        after = [round(x - r.gauss(1.6, 0.5), 3) for x in before]
        return {"before": before, "after": after, "unit": "ml",
                "pairing": 'matched records from one batch, before and after the adjustment'}
    paired = _redraw(rng, _draw_paired,
                     lambda b: verifiers.paired_t(b)["pValue"] < 0.005,
                     "paired improvement drop")

    blocks = {"T_Normality": baseline, "T_OneSample": one_sample,
              "T_TwoSample": two_sample, "T_Paired": paired}

    norm_ref = verifiers.normality(baseline)
    t1_ref = verifiers.one_sample_t(one_sample)
    t2_ref = verifiers.two_sample_t(two_sample)
    tp_ref = verifiers.paired_t(paired)
    _base_deriv = "derived from generated payload via truth.verifiers.{} (scipy), seed={}"
    # Which normality TEST is not declared by this payload, and Minitab (Anderson-Darling)
    # and R (`shapiro.test`) disagree well outside the 0.05 window. That was the whole
    # reason the p-value was carried soft — which made it unfailable, so a contestant
    # reporting nonsense scored the same as one reporting either correct answer. Admitting
    # Shapiro-Wilk at its own precision discharges the doubt and lets the entry go hard.
    _norm_p = round(norm_ref["pValue"], 6)
    _norm_accepts = verifiers.convention_windows(
        "basic.normality", "pValue", baseline, _norm_p, 0.05)
    truths = (
        TruthEntry(method_id="basic.normality", field="pValue",
                   expected=_norm_p, tol=0.05, soft=False, accepts=_norm_accepts,
                   stage_id="T_Normality", metric_cue=r"AD|[Aa]nderson|P\s*[=＝>＞]",
                   derivation=_base_deriv.format(
                       "normality (Anderson-Darling with D'Agostino p approximation)", seed),
                   verified_by=("scipy",)),
        TruthEntry(method_id="basic.normality", field="statistic",
                   expected=round(verifiers.anderson_statistic(
                       [float(v) for v in baseline["data"]], dist="norm"), 6),
                   # STAYS SOFT. A-squared and Shapiro-Wilk's W are different quantities on
                   # different scales, so no variant window can admit the second toolchain
                   # without admitting an unrelated number under the name `statistic`.
                   # Softness here is a real convention gap, not an undischarged note.
                   tol=0.15, soft=True,
                   stage_id="T_Normality", metric_cue=r"AD|Anderson|statistic",
                   derivation=_base_deriv.format("normality (raw AD A² statistic)", seed),
                   verified_by=("scipy",)),
        TruthEntry(method_id="basic.one_sample_t", field="pValue",
                   expected=round(t1_ref["pValue"], 6), tol=0.01, soft=False,
                   stage_id="T_OneSample", metric_cue=r"P\s*[=＝<＜]|declared value|running over|filling over|over-?filling",
                   derivation=_base_deriv.format("one_sample_t (scipy.stats.ttest_1samp)", seed),
                   verified_by=("scipy",)),
        TruthEntry(method_id="basic.one_sample_t", field="tStatistic",
                   expected=round(t1_ref["tStatistic"], 6), tol=0.5, soft=False,
                   stage_id="T_OneSample", metric_cue=r"t\s*[=＝]|t-?statistic",
                   derivation=_base_deriv.format("one_sample_t (scipy.stats.ttest_1samp)", seed),
                   verified_by=("scipy",)),
        TruthEntry(method_id="basic.two_sample_t", field="pValue",
                   expected=round(t2_ref["pValue"], 6), tol=0.01, soft=False,
                   stage_id="T_TwoSample", metric_cue=r"P\s*[=＝<＜]|machine 1|machine 2|both machines|two fillers",
                   derivation=_base_deriv.format(
                       "two_sample_t (scipy.stats.ttest_ind, equal_var=False i.e. Welch)", seed),
                   verified_by=("scipy",)),
        TruthEntry(method_id="basic.paired_t", field="pValue",
                   expected=round(tp_ref["pValue"], 6), tol=0.01, soft=False,
                   stage_id="T_Paired", metric_cue=r"P\s*[=＝<＜]|nozzle|before and after|matched record|paired",
                   derivation=_base_deriv.format("paired_t (scipy.stats.ttest_rel)", seed),
                   verified_by=("scipy",)),
    )

    _assert_invariants(truths)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(truths):
    by = {(t.method_id, t.field): t.expected for t in truths}
    assert by[("basic.normality", "pValue")] > 0.10, "baseline must be convincingly normal"
    assert by[("basic.one_sample_t", "pValue")] < 0.01, "overfill vs label must be significant"
    assert by[("basic.two_sample_t", "pValue")] < 0.01, "machine difference must be significant"
    assert by[("basic.paired_t", "pValue")] < 0.01, "paired improvement must be significant"


if __name__ == "__main__":
    bad = []
    for s in range(1, 501):
        try:
            generate(s)
        except AssertionError as e:
            bad.append((s, str(e)))
    print("failed seeds:", bad if bad else "NONE (500/500)")
