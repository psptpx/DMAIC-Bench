"""adb_c23 generator — measurement-system trust case (crossed GRR + attribute agreement).

derive, never hand-write: both truths are DERIVED from the freshly generated data through the reference
implementations in truth/verifiers.py (gage_rr_crossed: two-way ANOVA with interaction,
Minitab 6σ %StudyVar convention; attribute_agreement: per-appraiser Cohen kappa vs the
standard, minimum over appraisers).

Data design invariants (hold for every seed, asserted below):
  - part-to-part variation (σ≈30 μm) >> gage repeatability (σ≈3 μm) + operator bias (σ≈2 μm)
    -> %StudyVariation < 30 (measurement system acceptable, AIAG MSA-4);
  - each inspector gets a deterministically bounded 1–3 wrong calls out of 60 ratings
    (>=95% per-appraiser agreement by construction) -> kappaMin > 0.75.
"""
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402
from dmaic_bench.truth import verifiers  # noqa: E402

_OPERATORS = ('Operator A', 'Operator B', 'Operator C')
_INSPECTORS = ('Inspector A', 'Inspector B', 'Inspector C')
_TRIALS = 2
_ITEMS = 30


def _draw_grr(rng):
    """3 operators x 10 parts x 3 replicates; part spread dominates gage error."""
    part_true = [round(28.0 + rng.gauss(0.0, 0.030), 6) for _ in range(10)]
    op_bias = {op: rng.gauss(0.0, 0.002) for op in _OPERATORS}
    meas = {
        op: [[round(pt + op_bias[op] + rng.gauss(0.0, 0.003), 4) for _ in range(3)]
             for pt in part_true]
        for op in _OPERATORS
    }
    return {"measurements": meas, "unit": "mm",
            "parts": 10, "operators": len(_OPERATORS), "replicatesPerPart": 3}


def _draw_attr(rng):
    """30 items (1/3 NG by standard), 3 inspectors x 2 trials; each inspector makes exactly
    1-3 deterministic errors across their 60 ratings -> >=95% agreement, kappa > 0.75."""
    standard = ["NG" if i % 3 == 0 else "OK" for i in range(_ITEMS)]
    rng.shuffle(standard)
    ratings = {}
    for insp in _INSPECTORS:
        trials = [list(standard) for _ in range(_TRIALS)]
        n_err = rng.randint(1, 3)
        slots = rng.sample(range(_ITEMS * _TRIALS), n_err)
        for s in slots:
            t, i = divmod(s, _ITEMS)
            trials[t][i] = "NG" if trials[t][i] == "OK" else "OK"
        ratings[insp] = trials
    return {"standard": standard, "ratings": ratings, "categories": ["OK", "NG"],
            "trialsPerInspector": _TRIALS}


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260401)

    for _ in range(100):  # bounded redraw: construction almost always passes first time
        grr_block = _draw_grr(rng)
        if verifiers.gage_rr_crossed(grr_block)["percentStudyVariation"] < 28.0:
            break
    else:
        raise AssertionError("adb_c23: could not construct %SV<28 GRR data in 100 draws")
    attr_block = _draw_attr(rng)

    blocks = {"M_GRR": grr_block, "M_AttrAgreement": attr_block}

    grr_ref = verifiers.gage_rr_crossed(grr_block)
    attr_ref = verifiers.attribute_agreement(attr_block)
    truths = (
        TruthEntry(
            method_id="msa.gage_rr_crossed", field="percentStudyVariation",
            expected=round(grr_ref["percentStudyVariation"], 6), tol=5.0, soft=False,
            stage_id="M_GRR", metric_cue=r"%\s*SV|Study\s*Var|R&R",
            derivation=("derived via truth.verifiers.gage_rr_crossed: two-way ANOVA variance "
                        "decomposition WITH operator*part interaction always retained, negative "
                        "components floored at 0, %StudyVar=100*sqrt(GRR/Total) (Minitab 6σ "
                        f"study-variation convention), seed={seed}"),
            verified_by=("numpy",),
        ),
        TruthEntry(
            method_id="msa.attribute_agreement", field="kappaMin",
            expected=round(attr_ref["kappaMin"], 6), tol=0.1, soft=False,
            stage_id="M_AttrAgreement", metric_cue=r"[Kk]appa",
            derivation=("derived via truth.verifiers.attribute_agreement: per-appraiser Cohen "
                        "kappa vs the known standard (all trials pooled, standard repeated per "
                        f"trial), kappaMin = minimum over appraisers, seed={seed}"),
            verified_by=("python-closed-form",),
        ),
    )

    _assert_invariants(truths)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(truths):
    by = {(t.method_id, t.field): t.expected for t in truths}
    assert by[("msa.gage_rr_crossed", "percentStudyVariation")] < 30.0, \
        "measurement system must be acceptable (%SV<30, AIAG MSA-4)"
    assert by[("msa.attribute_agreement", "kappaMin")] > 0.75, \
        "attribute agreement must pass (kappa>0.75)"


if __name__ == "__main__":
    bad = []
    for s in range(1, 501):
        try:
            generate(s)
        except AssertionError as e:
            bad.append((s, str(e)))
    print("failed seeds:", bad if bad else "NONE (500/500)")
