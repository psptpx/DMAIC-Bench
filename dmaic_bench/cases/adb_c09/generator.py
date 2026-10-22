"""adb_c09 generator — furniture surface-defect quality-tools case (4 stages).

"derive, never hand-write": all numeric truths are re-derived from the exact block payloads by the in-file
implementations below (numpy/scipy only; truth/verifiers.py is NOT touched). Payload shapes for
quality.pareto ({counts: dict}) and tables.chisquare_assoc ({table: [[...]]}) are
verifier-compatible so V7 re-verifies them. Algorithm conventions:

  quality.pareto          topCategoryPct = 100 * max(counts) / sum(counts) — top single category share
                          after the first (largest) Pareto category, closed-form arithmetic.
  quality.fmea_rpn        maxRpn = max(severity * occurrence * detection) over the scored
                          failure items — closed-form arithmetic.
  tables.chisquare_assoc  scipy.stats.chi2_contingency(table, correction=False) — identical
                          call to truth/verifiers.chisquare_assoc.
  meta.data_profiling     no numeric truth (method-selection-only stage).

Data design invariants (hold for every seed, asserted below):
  - the top defect category is built as 1.4-1.8x the SUM of all other categories -> its share
    is >55% for every seed (vital_few decision point determinate);
  - each shift gets a dominant defect type boost (+26..45 on a base of 8-14 counts) -> the
    shift x defect-type association p << 0.01;
  - the top failure item is scored S>=8, O>=6, D>=5 -> maxRpn >= 240 > 125.
"""
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402

_SHIFTS = ('day shift', 'swing shift', 'night shift')
_DEFECTS = ('scratch', 'edge-band chipping', 'colour mismatch', 'blistering')


def _pareto_top_pct(counts):
    """Same convention as truth/verifiers.pareto."""
    vals = sorted(counts.values(), reverse=True)
    return 100.0 * vals[0] / sum(vals)


def _max_rpn(items):
    return max(it["severity"] * it["occurrence"] * it["detection"] for it in items)


def _chi_assoc(table):
    """Identical call to truth/verifiers.chisquare_assoc."""
    r = stats.chi2_contingency(np.asarray(table, float), correction=False)
    return float(r.statistic), float(r.pvalue)


def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260605)

    # --- Q_Pareto: monthly counts per defect category; top category dominates ----------------
    rest = {
        'edge-band chipping': rng.randint(24, 40),
        'colour mismatch': rng.randint(18, 30),
        'blistering': rng.randint(10, 20),
        'wrong or missing hardware': rng.randint(6, 14),
    }
    counts = {'scratch': int(sum(rest.values()) * rng.uniform(1.4, 1.8)), **rest}

    # --- Q_ChiAssoc: shift x defect-type cross table with one dominant type per shift --------
    table = [[rng.randint(8, 14) for _ in _DEFECTS] for _ in _SHIFTS]
    table[0][0] += rng.randint(30, 45)   # day shift -> scratch
    table[1][2] += rng.randint(26, 40)   # swing shift -> colour mismatch
    table[2][1] += rng.randint(26, 40)   # night shift -> edge-band chipping

    # --- Q_FMEA: failure-item S/O/D scoring; the first item is the built-in top risk ---------
    items = [
        {"mode": 'temperature control of the edge-band hot melt has failed', "severity": 8,
         "occurrence": rng.randint(6, 8), "detection": rng.randint(5, 7)},
        {"mode": 'the cutting blade is worn and was not changed on schedule', "severity": rng.randint(6, 7),
         "occurrence": rng.randint(5, 6), "detection": rng.randint(4, 5)},
        {"mode": 'the protective film on incoming board stock is torn', "severity": rng.randint(5, 6),
         "occurrence": rng.randint(4, 6), "detection": rng.randint(3, 4)},
        {"mode": 'dust control in the spray booth is inadequate', "severity": rng.randint(4, 5),
         "occurrence": rng.randint(3, 5), "detection": rng.randint(4, 6)},
        {"mode": 'hardware part numbers stored mixed together', "severity": rng.randint(4, 5),
         "occurrence": rng.randint(2, 3), "detection": rng.randint(3, 4)},
        {"mode": 'too little cushioning in the packaging', "severity": rng.randint(3, 4),
         "occurrence": rng.randint(2, 4), "detection": rng.randint(2, 3)},
    ]

    sample_rows = [{'date': f"2026-06-{rng.randint(1, 28):02d}",
                    'shift': rng.choice(_SHIFTS),
                    'defect class': rng.choice(_DEFECTS),
                    'quantity': rng.randint(1, 6)} for _ in range(6)]

    blocks = {
        "Q_Profile": {
            "summary": {"yType": 'counted defect', "period": 'the past month',
                        "columns": ['date', 'shift', 'defect class', 'quantity'],
                        "totalRecords": rng.randint(420, 560)},
            "sample": sample_rows,
        },
        "Q_Pareto": {"counts": counts, "unit": 'occurrences', "period": 'the past month'},
        "Q_FMEA": {"items": items,
                   "scale": 'severity, occurrence and detection are each scored 1-10; a higher number is a higher risk'},
        "Q_ChiAssoc": {"table": table,
                       "row_labels": list(_SHIFTS), "col_labels": list(_DEFECTS),
                       "unit": 'occurrences'},
    }

    top_pct = _pareto_top_pct(counts)
    max_rpn = _max_rpn(items)
    chi_stat, chi_p = _chi_assoc(table)

    truths = (
        TruthEntry("quality.pareto", "topCategoryPct", round(top_pct, 6), 1e-3,
                   soft=False, stage_id="Q_Pareto", metric_cue=r"%|vital few|largest share|largest|accounts? for|top categor|cumulative",
                   derivation=f"closed-form 100*max(counts)/sum(counts) (same convention as "
                              f"truth/verifiers.pareto), recomputed from block payload; "
                              f"seed={seed}", verified_by=("arithmetic",)),
        TruthEntry("quality.fmea_rpn", "maxRpn", float(max_rpn), 1e-6,
                   soft=False, stage_id="Q_FMEA", metric_cue=r"risk|RPN|highest|priority|failure point",
                   derivation=f"closed-form max(severity*occurrence*detection) over the scored "
                              f"items, recomputed from block payload; seed={seed}",
                   verified_by=("arithmetic",)),
        # HARD: the table is 3x4, so R's only divergent default (Yates, 2x2 only) does not
        # apply and there is no second convention for this statistic.
        TruthEntry("tables.chisquare_assoc", "statistic", round(chi_stat, 6), 0.5,
                   soft=False, stage_id="Q_ChiAssoc", metric_cue=r"χ|chi-?squared?|statistic",
                   derivation=f"scipy.stats.chi2_contingency(correction=False), identical call "
                              f"to truth/verifiers.chisquare_assoc; seed={seed}",
                   verified_by=("scipy",)),
        TruthEntry("tables.chisquare_assoc", "pValue", round(chi_p, 6), 0.01,
                   soft=False, stage_id="Q_ChiAssoc", metric_cue=r"P\s*[=＝<＜]|shift|association|cross-?tab",
                   derivation=f"scipy.stats.chi2_contingency(correction=False), identical call "
                              f"to truth/verifiers.chisquare_assoc; seed={seed}",
                   verified_by=("scipy",)),
    )

    _assert_invariants(top_pct, max_rpn, chi_p)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(top_pct, max_rpn, chi_p):
    assert top_pct > 50.0, f"top defect share must exceed 50%, got {top_pct:.1f}%"
    assert max_rpn > 125, f"top risk must exceed RPN 125, got {max_rpn}"
    assert chi_p < 0.01, f"shift x defect association must be significant, p={chi_p}"


if __name__ == "__main__":
    worst = {"topPct": 100.0, "maxRpn": 10**9, "chiP": 0.0}
    for s in range(1, 501):
        d = generate(s)
        by = {(t.method_id, t.field): t.expected for t in d.truths}
        worst["topPct"] = min(worst["topPct"], by[("quality.pareto", "topCategoryPct")])
        worst["maxRpn"] = min(worst["maxRpn"], by[("quality.fmea_rpn", "maxRpn")])
        worst["chiP"] = max(worst["chiP"], by[("tables.chisquare_assoc", "pValue")])
    print("500 seeds ok; min top share % =", round(worst["topPct"], 3),
          "min maxRpn =", worst["maxRpn"], "max chi p =", worst["chiP"])
