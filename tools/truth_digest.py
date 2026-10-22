"""Digest of the corpus's numeric ground floor: every ``(method_id, field, expected, tol)``.

Why a digest rather than a test that reads a number: the localisation touched the builder, the
registry, the legacy bridge and the case files, and none of those may move a truth. A digest is
the cheapest statement of that invariant that a reviewer can re-run — and unlike a diff it does
not care which file the number lives in, which is exactly the property needed when the same
truths are reached through two different renderings of the same case.

Recipe, stated so it can be reproduced independently:

* every case in ``registry.discover()``, in case-id order;
* seeds 1, 2 and 3 for a parametric case, seed 1 only for a frozen one (a frozen generator
  ignores the seed, so the other two would just triple the same rows);
* for each generated truth, the 4-tuple ``(method_id, field, expected, tol)``, with the floats
  formatted by ``repr`` so the digest is exact rather than rounded;
* rows sorted, joined by newline, SHA-256, first 16 hex digits.

Run: ``python3 tools/truth_digest.py`` (from the repository root); ``--per-case``
localises a change.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dmaic_bench.core import registry  # noqa: E402

SEEDS = (1, 2, 3)


def truth_rows(cases: dict | None = None) -> list:
    """Sorted ``"method_id|field|expected|tol"`` rows for the whole corpus."""
    cases = registry.discover() if cases is None else cases
    rows = []
    for case_id in sorted(cases):
        case = cases[case_id]
        seeds = SEEDS if case.meta.parametric else (1,)
        for seed in seeds:
            for t in case.generate(seed).truths:
                rows.append(f"{t.method_id}|{t.field}|{t.expected!r}|{t.tol!r}")
    return sorted(rows)


def digest(cases: dict | None = None) -> str:
    body = "\n".join(truth_rows(cases))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


def per_case(cases: dict | None = None) -> dict:
    cases = registry.discover() if cases is None else cases
    return {case_id: digest({case_id: case}) for case_id, case in sorted(cases.items())}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--per-case", action="store_true")
    args = ap.parse_args(argv)
    if args.per_case:
        for case_id, d in per_case().items():
            print(f"{case_id} {d}")
    rows = truth_rows()
    print(f"{len(rows)} truth tuples")
    print(f"digest {digest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
