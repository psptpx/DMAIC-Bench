"""adb_c12 generator — attribute-proportion chain (one-prop → two-prop → power → binomial cap).

"derive, never hand-write": every truth is DERIVED from the freshly generated data through the reference
implementations in truth/verifiers.py (one_proportion: normal-approx z test; two_proportions:
pooled z; power_two_proportions: statsmodels NormalIndPower with Cohen's h;
capability_binomial: pooled p + processZ = Φ⁻¹(1-p̄)).

Data design invariants (hold for every seed, asserted below):
  - acceptance-lot defect rate ≈8.5% vs the 5% contractual cap, n≈1200 -> one-prop p < 0.01;
  - old (~8.5%) vs new (~3%) sealing process, n≈900 per line -> two-prop p < 0.01;
  - planned confirmation trial (p1≈8.5%, p2≈3%, 160-260 per group, α=0.05) -> power in
    (0.5, 0.999) — adequate but not saturated;
  - post-switch 20 production lots run at ~3% -> avgP strictly below the pre-improvement
    acceptance-lot rate.
"""
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402
from dmaic_bench.truth import verifiers  # noqa: E402

_CONTRACT_CAP = 0.05


def _binom(rng, n, p):
    return sum(1 for _ in range(n) if rng.random() < p)


def _redraw(rng, draw_fn, ok_fn, what, tries=300):
    for _ in range(tries):
        block = draw_fn(rng)
        if ok_fn(block):
            return block
    raise AssertionError(f"adb_c12: could not construct {what} in {tries} draws")


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260403)

    def _draw_oneprop(r):
        n = r.randint(1100, 1400)
        p = r.uniform(0.075, 0.095)
        return {"events": _binom(r, n, p), "trials": n, "hypothesizedP": _CONTRACT_CAP,
                "unit": 'pieces', "note": "this month's acceptance lots, seal-check totals"}
    one_prop = _redraw(
        rng, _draw_oneprop,
        lambda b: verifiers.one_proportion(b)["pValue"] < 0.005
        and 0.06 < b["events"] / b["trials"] < 0.12,
        "acceptance lot clearly above the 5% cap")
    baseline_rate = one_prop["events"] / one_prop["trials"]

    def _draw_twoprops(r):
        n1, n2 = r.randint(850, 1000), r.randint(850, 1000)
        return {"events1": _binom(r, n1, r.uniform(0.075, 0.095)), "trials1": n1,
                "events2": _binom(r, n2, r.uniform(0.024, 0.036)), "trials2": n2,
                "group1Name": 'old sealing process', "group2Name": 'new sealing process'}
    two_props = _redraw(
        rng, _draw_twoprops,
        lambda b: verifiers.two_proportions(b)["pValue"] < 0.005
        and b["events1"] / b["trials1"] > b["events2"] / b["trials2"],
        "old-vs-new process separation")

    def _draw_power(r):
        return {"p1": round(r.uniform(0.078, 0.092), 4),
                "p2": round(r.uniform(0.026, 0.034), 4),
                "nPerGroup": r.randint(160, 260),
                "alpha": 0.05,
                "note": 'agreed plan for the formal comparison: the level each of the two lines is expected to run at and the sample count planned for each'}
    power_block = _redraw(
        rng, _draw_power,
        lambda b: 0.55 < verifiers.power_two_proportions(b)["power"] < 0.99,
        "planned trial with adequate-but-unsaturated power")

    def _draw_cap(r):
        sizes = [r.randint(420, 580) for _ in range(20)]
        p_new = r.uniform(0.024, 0.036)
        return {"defectCounts": [_binom(r, n, p_new) for n in sizes],
                "subgroupSizes": sizes, "note": 'check totals for twenty consecutive production lots after the changeover'}
    cap_block = _redraw(
        rng, _draw_cap,
        lambda b: 0.015 < verifiers.capability_binomial(b)["avgP"] < baseline_rate - 0.02,
        "post-switch lots clearly below the pre-improvement rate")

    blocks = {"P_OneProp": one_prop, "P_TwoProps": two_props,
              "P_Power": power_block, "P_BinomialCap": cap_block}

    op_ref = verifiers.one_proportion(one_prop)
    tp_ref = verifiers.two_proportions(two_props)
    pw_ref = verifiers.power_two_proportions(power_block)
    cap_ref = verifiers.capability_binomial(cap_block)
    truths = (
        TruthEntry(method_id="basic.one_proportion", field="pValue",
                   expected=round(op_ref["pValue"], 6), tol=0.01, soft=False,
                   stage_id="P_OneProp", metric_cue=r"P\s*[=＝<＜]|acceptance lot|agreed cap|above the cap|above the limit",
                   derivation=("derived via truth.verifiers.one_proportion: normal-approximation "
                               "z test (p̂-p0)/sqrt(p0(1-p0)/n), two-sided, no continuity "
                               f"correction, seed={seed}"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="basic.two_proportions", field="pValue",
                   expected=round(tp_ref["pValue"], 6), tol=0.01, soft=False,
                   stage_id="P_TwoProps", metric_cue=r"P\s*[=＝<＜]|old sealing|new sealing|trial line|old against new",
                   derivation=("derived via truth.verifiers.two_proportions: pooled-proportion "
                               f"two-sided z test, seed={seed}"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="power.two_proportions", field="power",
                   # HARD: the arcsine-h and pooled-normal power conventions differ by
                   # <0.03 here, i.e. both land inside the window — nothing to be soft about.
                   expected=round(pw_ref["power"], 6), tol=0.05, soft=False,
                   stage_id="P_Power", metric_cue=r"[Pp]ower",
                   derivation=("derived via truth.verifiers.power_two_proportions: statsmodels "
                               "NormalIndPower, Cohen's h = 2asin√p1 - 2asin√p2, two-sided "
                               f"α=0.05, equal n per group, seed={seed}"),
                   verified_by=("statsmodels",)),
        TruthEntry(method_id="capability.binomial", field="avgP",
                   expected=round(cap_ref["avgP"], 6), tol=1e-4, soft=False,
                   stage_id="P_BinomialCap", metric_cue=r"P̄|p-?bar",
                   derivation=("derived via truth.verifiers.capability_binomial: pooled "
                               f"p̄ = Σdefects/Σn over the 20 lots, seed={seed}"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="capability.binomial", field="processZ",
                   expected=round(cap_ref["processZ"], 6), tol=0.05, soft=False,
                   stage_id="P_BinomialCap", metric_cue=r"Z|process Z|sigma level|process level",
                   derivation=("derived via truth.verifiers.capability_binomial: "
                               f"processZ = Φ⁻¹(1-p̄), seed={seed}"),
                   verified_by=("scipy",)),
    )

    _assert_invariants(blocks, truths)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(blocks, truths):
    by = {(t.method_id, t.field): t.expected for t in truths}
    assert by[("basic.one_proportion", "pValue")] < 0.01, "cap exceedance must be significant"
    assert by[("basic.two_proportions", "pValue")] < 0.01, "process difference must be significant"
    assert 0.5 < by[("power.two_proportions", "power")] < 0.999, "planned trial power in (0.5,0.999)"
    baseline_rate = blocks["P_OneProp"]["events"] / blocks["P_OneProp"]["trials"]
    assert by[("capability.binomial", "avgP")] < baseline_rate, \
        "post-switch avgP must beat the pre-improvement rate"


if __name__ == "__main__":
    bad = []
    for s in range(1, 501):
        try:
            generate(s)
        except AssertionError as e:
            bad.append((s, str(e)))
    print("failed seeds:", bad if bad else "NONE (500/500)")
