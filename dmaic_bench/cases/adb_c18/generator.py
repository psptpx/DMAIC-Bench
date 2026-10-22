"""adb_c18 generator — stability check → overall capability → grouped (worst-station) chain.

derive, never hand-write: capability truths are DERIVED through truth/verifiers.py capability_normal
(Pp=(USL-LSL)/6s, Ppk=min((USL-μ)/3s,(μ-LSL)/3s), overall s with ddof=1). control_chart.imr and
capability.grouped have no reference implementation — they are self-derived here:
  * I-MR: centerLine = x̄; individuals limits = x̄ ± 2.66·MR̄ where MR̄ is the mean moving range
    of consecutive points (Montgomery ISQC 6e §6.4 / AIAG SPC-2 convention, d2=1.128 for n=2);
  * grouped capability: per-group Ppk with each group's OWN mean and sample std (ddof=1) against
    the shared spec limits; the reported truth is the WORST (minimum) group Ppk — the "worst-group"
    convention documented in the derivation.

Data design invariants (hold for every seed, asserted below):
  - the run-order series is truncated Gaussian (|x-μ|<2.5σ) and REDRAWN until no individual
    falls outside its own estimated x̄±2.66·MR̄ limits -> process demonstrably in control,
    stability_gate branch determinate;
  - overall Ppk lands in (0.8, 2.5) — a sane, non-degenerate capability;
  - station 3 runs ≈1.9σ toward the USL -> worst-station Ppk strictly below overall Ppk.
"""
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402
from dmaic_bench.truth import verifiers  # noqa: E402

_LSL, _USL = 12.0, 28.0
_MU, _SIGMA = 20.0, 2.0


def _truncated_gauss(rng, mu, sigma, cut=2.5):
    while True:
        g = rng.gauss(0.0, 1.0)
        if abs(g) < cut:
            return mu + sigma * g


def _imr_stats(data):
    n = len(data)
    center = sum(data) / n
    mrbar = sum(abs(data[i] - data[i - 1]) for i in range(1, n)) / (n - 1)
    return center, center + 2.66 * mrbar, center - 2.66 * mrbar


def _group_ppk(vals):
    m = sum(vals) / len(vals)
    s = (sum((x - m) ** 2 for x in vals) / (len(vals) - 1)) ** 0.5
    return min((_USL - m) / (3 * s), (m - _LSL) / (3 * s))


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260405)

    for _ in range(300):
        series = [round(_truncated_gauss(rng, _MU, _SIGMA), 3) for _ in range(40)]
        center, ucl, lcl = _imr_stats(series)
        if all(lcl < x < ucl for x in series):
            break
    else:
        raise AssertionError("adb_c18: could not construct in-control I-MR series")

    for _ in range(300):
        overall = [round(rng.gauss(_MU, _SIGMA), 3) for _ in range(50)]
        cap_block = {"data": overall, "lsl": _LSL, "usl": _USL, "unit": "μm"}
        cap_ref = verifiers.capability_normal(cap_block)
        if 0.9 < cap_ref["ppk"] < 2.3:
            break
    else:
        raise AssertionError("adb_c18: could not construct sane overall capability")

    station_mus = {'Station 1': 20.0, 'Station 2': 20.6, 'Station 3': 23.8}
    for _ in range(300):
        groups = {st: [round(rng.gauss(mu, _SIGMA), 3) for _ in range(25)]
                  for st, mu in station_mus.items()}
        worst_ppk = min(_group_ppk(v) for v in groups.values())
        if 0.3 < worst_ppk < cap_ref["ppk"] - 0.15:
            break
    else:
        raise AssertionError("adb_c18: could not construct a clearly weakest station")
    grouped_block = {"groups": groups, "lsl": _LSL, "usl": _USL, "unit": "μm"}

    blocks = {
        "C_IMR": {"data": series, "unit": "μm", "order": 'recorded piece by piece in machining order'},
        "C_NormalCap": cap_block,
        "C_GroupedCap": grouped_block,
    }

    _imr_deriv = ("self-derived in generator: I-MR individuals chart, centerLine = x̄, "
                  "limits = x̄ ± 2.66·MR̄ (mean moving range, d2=1.128 for n=2; Montgomery "
                  f"ISQC 6e §6.4 / AIAG SPC-2), seed={seed}")
    truths = (
        TruthEntry(method_id="control_chart.imr", field="centerLine",
                   expected=round(center, 6), tol=1e-3, soft=False,
                   stage_id="C_IMR", metric_cue=r"CL|cent(?:re|er)\s*line|centre-?line|center-?line|mean",
                   derivation=_imr_deriv, verified_by=("python-closed-form",)),
        TruthEntry(method_id="control_chart.imr", field="individualsUCL",
                   expected=round(ucl, 6), tol=0.5, soft=False,
                   stage_id="C_IMR", metric_cue=r"UCL",
                   derivation=_imr_deriv, verified_by=("python-closed-form",)),
        TruthEntry(method_id="control_chart.imr", field="individualsLCL",
                   expected=round(lcl, 6), tol=0.5, soft=False,
                   stage_id="C_IMR", metric_cue=r"LCL",
                   derivation=_imr_deriv, verified_by=("python-closed-form",)),
        TruthEntry(method_id="capability.normal", field="ppk",
                   expected=round(cap_ref["ppk"], 6), tol=0.05, soft=False,
                   stage_id="C_NormalCap", metric_cue=r"Ppk",
                   derivation=("derived via truth.verifiers.capability_normal: "
                               "Ppk = min((USL-μ)/3s, (μ-LSL)/3s), overall s (ddof=1), "
                               f"seed={seed}"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="capability.normal", field="pp",
                   expected=round(cap_ref["pp"], 6), tol=0.05, soft=False,
                   stage_id="C_NormalCap", metric_cue=r"Pp\b|overall capability|process performance",
                   derivation=("derived via truth.verifiers.capability_normal: "
                               f"Pp = (USL-LSL)/6s, overall s (ddof=1), seed={seed}"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="capability.grouped", field="ppk",
                   # STAYS SOFT. Nothing in the payload says the grouped index is the WORST
                   # group rather than the pooled or the average one, and the three answers
                   # are 1.019 / 1.109 / 1.398 on seed 1 — a genuine unstated convention.
                   # Declaring it in the payload would change the task, so it is reported
                   # rather than forced.
                   expected=round(worst_ppk, 6), tol=0.1, soft=True,
                   stage_id="C_GroupedCap", metric_cue=r"Ppk",
                   derivation=("self-derived in generator: per-group Ppk with each group's own "
                               "mean and sample std (ddof=1) vs shared spec limits; truth is the "
                               f"WORST (minimum) group Ppk — worst-group convention, seed={seed}"),
                   verified_by=("python-closed-form",)),
    )

    _assert_invariants(blocks, truths)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(blocks, truths):
    by = {(t.method_id, t.field): t.expected for t in truths}
    series = blocks["C_IMR"]["data"]
    center, ucl, lcl = _imr_stats(series)
    assert all(lcl < x < ucl for x in series), "run-order series must be in control"
    assert 0.8 < by[("capability.normal", "ppk")] < 2.5, "overall Ppk must be sane"
    assert by[("capability.grouped", "ppk")] < by[("capability.normal", "ppk")], \
        "worst station must be below overall capability"


if __name__ == "__main__":
    bad = []
    for s in range(1, 501):
        try:
            generate(s)
        except AssertionError as e:
            bad.append((s, str(e)))
    print("failed seeds:", bad if bad else "NONE (500/500)")
