"""A rejection seed must reject under EVERY admissible convention, not just the one the truth
package happened to compute.

Measured on the oracle: adb_c31 seed 4 had %StudyVariation 0.2784 under the primary estimate,
which puts the number of distinct categories at 4 and routes the project to the terminal
remediation node. The reference solution computes the AIAG pooled-interaction estimate instead,
read 0.2681, and ndc came back 5 -- so it walked M_stability where the truth derived M_msa_fix,
and the oracle ceiling on that task fell to 0.000.

That is a task defect wearing the costume of a hard task. Which branch is correct must not
depend on which admissible convention a contestant picked, and a benchmark cannot mark a
contestant wrong for using the idiomatic call of a supported toolchain.

``ndc`` is ``1.41 * PV/GRR``, so it crosses 5 at roughly %SV = 0.275 -- the two estimates only
have to differ by about a point for the routing to flip. These assertions pin the property for
every rejection seed in the build, at the criterion each seed rejects on.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dmaic_bench.v2 import registry   # noqa: E402

GRR_LIMIT = 0.30
NDC_LIMIT = 5


def _ndc_from(pct_sv: float) -> int:
    """The distinct-category count implied by a %StudyVariation, as AIAG defines it."""
    if pct_sv <= 0:
        return 10 ** 6
    return int(1.41 * math.sqrt(max(1e-12, 1.0 - pct_sv * pct_sv)) / pct_sv)


def _msa_seeds():
    for cid, case in registry.discover().items():
        for seed in case.seeds:
            shape = str(case.shapes.get(seed, ""))
            if "gauge-unacceptable" not in shape:
                continue
            _, results = case.generate(seed)
            msa = (results or {}).get("msa") or {}
            if "pctSV" in msa:
                yield cid, seed, shape, msa


def test_every_gauge_rejection_rejects_under_both_conventions():
    """Whatever the seed rejects on, it must reject on BOTH estimates of %StudyVariation."""
    split = []
    for cid, seed, shape, msa in _msa_seeds():
        primary = float(msa["pctSV"])
        pooled = float(msa.get("pctSVPooled", primary))
        if "resolution" in shape:
            # rejects on the distinct-category criterion while passing the 30% screen
            ok = (msa["ndc"] < NDC_LIMIT and _ndc_from(pooled) < NDC_LIMIT
                  and primary <= GRR_LIMIT and pooled <= GRR_LIMIT)
        else:
            # rejects on the headline screen outright
            ok = primary > GRR_LIMIT and pooled > GRR_LIMIT
        if not ok:
            split.append((cid, seed, shape, round(primary, 4), round(pooled, 4),
                          msa.get("ndc"), _ndc_from(pooled)))
    assert not split, (
        "rejection seeds whose verdict depends on which admissible convention is used "
        f"(case, seed, shape, primary, pooled, ndc_primary, ndc_pooled): {split}")


def test_the_resolution_seeds_really_do_pass_the_headline_screen():
    """Otherwise the trap is not a trap -- it would be caught by the percentage alone."""
    trivial = []
    for cid, seed, shape, msa in _msa_seeds():
        if "resolution" not in shape:
            continue
        if float(msa["pctSV"]) > GRR_LIMIT:
            trivial.append((cid, seed, round(float(msa["pctSV"]), 4)))
    assert not trivial, f"resolution seeds already failing the 30% screen: {trivial}"


def test_at_least_one_seed_carries_the_resolution_criterion():
    """The corpus must actually contain the case this criterion exists to test."""
    found = [(cid, seed) for cid, seed, shape, _ in _msa_seeds() if "resolution" in shape]
    assert found, "no gauge-unacceptable(resolution) seed in the build"
