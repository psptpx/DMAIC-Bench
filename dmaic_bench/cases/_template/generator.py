"""New-case generator template. Copy this together with case.yaml and fill it in.

The contract, enforced item by item by the onboarding gates:
  1. generate(seed) -> CaseData. The keys of `blocks` correspond one-to-one with the
     stage_ids declared in case.yaml (V8).
  2. Two calls with the same seed are byte-identical (V4); with parametric=true, a different
     seed must produce different data (V5).
  3. Truths are DERIVED AT GENERATION TIME, never hand-written (V7). Anything a reference
     implementation in truth/verifiers.py can compute must be computed by it.
     - SIMULATED cases: deriving from verifiers is sufficient; record it in `derivation`.
     - TRUE / RECONSTRUCTED cases: `expected` comes from the source project report, and the
       verifiers only re-check it. `derivation` must cite where the value came from.
  4. Every HARD (soft=False) truth carries a `derivation` (V6).
  5. Conclusion invariants -- which test must be significant, which branch must be
     determinate -- have to hold for EVERY seed, not just the one you tried. Assert them in
     _assert_invariants and sweep a few hundred seeds before onboarding. A case whose effect
     is not powered to survive every seed is a case whose route truth is sometimes wrong.

A worked example to read first: cases/adb_c13/generator.py
"""
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402
from dmaic_bench.truth import verifiers  # noqa: E402


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260707)  # an isolated RNG; never the global one

    data = [round(10 + rng.gauss(0, 1), 4) for _ in range(50)]
    blocks = {
        "M1_Baseline": {"data": data, "lsl": 7.0, "usl": 13.0, "unit": "mm"},
    }

    ref = verifiers.REFERENCE_IMPLS["capability.normal"](blocks["M1_Baseline"])
    truths = (
        TruthEntry(
            method_id="capability.normal", field="ppk",
            expected=round(ref["ppk"], 6), tol=0.05, soft=True,
            stage_id="M1_Baseline", metric_cue=r"Ppk|capability|process capability",
            derivation=f"derived via truth.verifiers.capability_normal (scipy), seed={seed}",
            verified_by=("scipy",),
        ),
    )

    _assert_invariants(truths)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(truths):
    by = {(t.method_id, t.field): t.expected for t in truths}
    assert by[("capability.normal", "ppk")] > 0.5, "example invariant"


if __name__ == "__main__":
    bad = []
    for s in range(1, 501):
        try:
            generate(s)
        except AssertionError as e:
            bad.append((s, str(e)))
    print("failed seeds:", bad if bad else "NONE (500/500)")
