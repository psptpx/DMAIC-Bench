"""v2 case discovery: every module under v2/cases/ that exposes `CASE: V2Case` is a project."""
from __future__ import annotations

import importlib
import os
import pkgutil

from dmaic_bench.v2 import cases as _cases_pkg

#: The v2 held-out split. Five of the fifteen project cases, 32 of the 97 tasks.
#:
#: WHY WHOLE CASES AND NOT SEEDS. A v2 case is its decision graph, and the graph is what a
#: contestant would have to have memorised: the data regenerates from a seed, so withholding
#: seeds from a published generator withholds nothing. Holding out a case means its graph, its
#: guards, its truth fields and its generator never enter the public artifact.
#:
#: HOW THESE FIVE WERE CHOSEN. Exhaustive enumeration of 5-case splits that satisfy STRUCTURAL
#: criteria only -- 28-35 tasks, tier proportions within 6 points of the corpus (47/21/32), both
#: splits keeping at least three industries, the public split keeping every y_type -- gave 536
#: candidates, and one was drawn from them with `random.Random(20260916)`. **No contestant score
#: was consulted in the selection.** Choosing among candidates by how well they matched measured
#: difficulty would be selecting the split with the test data, which is the thing a held-out
#: split exists to prevent.
#:
#: WHAT THE DRAW GAVE, MEASURED AFTERWARDS. Tier mix 50/19/31 against the corpus 47/21/32. The
#: held-out half is somewhat EASIER than the public half: GLM-5.3-Flash 0.575 against 0.549,
#: GPT-5.6-sol 0.685 against 0.622. That is reported rather than re-drawn -- re-drawing until
#: the halves matched would be exactly the selection-on-outcome avoided above -- and a held-out
#: score should be read as roughly 0.03-0.06 optimistic relative to a public one.
HELD_OUT_CASES = frozenset({
    "adb_c25",   # moulded fitting dimension        continuous / discrete manufacturing
    "adb_c26",   # service-level breach rate        attribute proportion / services
    "adb_c28",   # electronics dimensional          continuous / electronics
    "adb_c34",   # coating thickness                continuous / discrete manufacturing
    "adb_c39",   # seal strength (RSM)              continuous / discrete manufacturing
})

#: Set to opt a local tree into the public view, so a build can be checked the way a third
#: party would see it without deleting anything.
_PUBLIC_ONLY_ENV = "DMAIC_PUBLIC_ONLY"


def held_out_present() -> bool:
    """Whether this working tree actually carries the held-out cases.

    A public checkout does not, and every caller that reports on the corpus needs to be able
    to say which of the two it is looking at rather than silently reporting 65 tasks as 97.
    """
    return bool(HELD_OUT_CASES & set(_discover_all()))


def discover(include_held_out: bool | None = None) -> dict:
    """``{case_id: V2Case}``.

    *include_held_out* defaults to True on a tree that has them, unless ``DMAIC_PUBLIC_ONLY``
    is set. The default is permissive because every internal caller -- the builder, the
    validation gates, the report -- needs the whole corpus; the PUBLIC ARTIFACT is produced by
    excluding them from the export, not by hoping a default holds.
    """
    if include_held_out is None:
        include_held_out = not os.environ.get(_PUBLIC_ONLY_ENV)
    out = _discover_all()
    if not include_held_out:
        out = {k: v for k, v in out.items() if k not in HELD_OUT_CASES}
    return out


#: Set to include the second-domain portability pilot (RNA-seq, GWAS) in discovery. Off by
#: default so the 97-task DMAIC corpus, its held-out split and every count-pinning test stay
#: exactly what the paper reports; the pilot is built and scored as its own dataset.
_PILOT_ENV = "DMAIC_PILOT_DOMAINS"


def _discover_all() -> dict:
    out = {}
    packages = [("dmaic_bench.v2.cases", _cases_pkg.__path__)]
    if os.environ.get(_PILOT_ENV):
        from dmaic_bench.v2 import pilot_cases as _pilot_pkg
        packages.append(("dmaic_bench.v2.pilot_cases", _pilot_pkg.__path__))
    for pkg_name, path in packages:
        for m in pkgutil.iter_modules(path):
            if m.name.startswith("_"):
                continue
            mod = importlib.import_module(f"{pkg_name}.{m.name}")
            case = getattr(mod, "CASE", None)
            if case is not None:
                out[case.case_id] = case
    return out
