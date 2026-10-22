"""Case registry — the single entry point through which cases join the benchmark dataset.

Two sources, one contract:
  1. Native cases: any directory under dmaic_bench/cases/<case_id>/ containing
     `case.yaml` + `generator.py` (with a module-level `generate(seed) -> CaseData`).
     Directories starting with "_" are skipped (e.g. cases/_template).
  2. Legacy-bridge cases: the 12 frozen cases of the originating evaluation harness,
     adapted read-only through `cases/legacy_bridge.py`. They register through the SAME
     Case model, marked parametric=False.
     HISTORICAL: that harness is a separate, unpublished codebase. Neither it nor
     `legacy_bridge.py` is part of this repository, so this source contributes nothing
     here and `discover()` returns the native cases alone. See docs/HELD_OUT.md.

Adding a new expert/mini case therefore never touches harness/scorer code: drop a
directory, run `python -m dmaic_bench validate <case_id>`, done.
"""
from __future__ import annotations

import importlib.util
import os

import yaml

from . import i18n
from .models import (Case, CaseMeta, DecisionPoint, FaultTarget, OrderConstraint, Stage,
                     StageMethod)

#: The held-out legacy bridge, addressed by name so :func:`discover` can ask whether it
#: exists without importing it. Absent in this repository (docs/HELD_OUT.md).
_LEGACY_BRIDGE = f"{__package__.rsplit('.', 1)[0]}.cases.legacy_bridge"

_HERE = os.path.dirname(os.path.abspath(__file__))
CASES_DIR = os.path.normpath(os.path.join(_HERE, "..", "cases"))


def _stage_from_dict(d: dict) -> Stage:
    return Stage(
        stage_id=d["stage_id"],
        phase=d["phase"],
        label=d["label"],
        topics=tuple(t.lower() for t in d.get("topics", [])),
        methods=tuple(StageMethod(
            method_id=m["method_id"],
            required=m.get("required", True),
            alternatives=tuple(m.get("alternatives", [])),
        ) for m in d.get("methods", [])),
        summary_fact=d.get("summary_fact", ""),
    )


def meta_from_yaml(path: str) -> CaseMeta:
    with open(path, encoding="utf-8") as f:
        d = yaml.safe_load(f)
    cases_dir = os.path.dirname(os.path.dirname(os.path.abspath(path)))
    return CaseMeta(
        case_id=d["case_id"],
        title=d["title"],
        tier=d["tier"],
        industry=d["industry"],
        provenance=d["provenance"],
        y_type=d["y_type"],
        context=d["context"].strip(),
        goal=d["goal"].strip(),
        stages=tuple(_stage_from_dict(s) for s in d["stages"]),
        decision_points=tuple(DecisionPoint(
            point_id=p["point_id"], phase=p["phase"], rule=p["rule"], source=p["source"],
            correct_branch=p["correct_branch"],
            acceptable_branches=tuple(p.get("acceptable_branches", [])),
            branch_evidence={k: list(v) for k, v in p.get("branch_evidence", {}).items()},
        ) for p in d.get("decision_points", [])),
        fault_targets=tuple(FaultTarget(f["stage_id"], f["method_id"])
                            for f in d.get("faults", [])),
        order_constraints=tuple(OrderConstraint(o["before"], o["after"], o.get("source", ""))
                                for o in d.get("order_constraints", [])),
        parametric=d.get("parametric", True),
        language=i18n.require_language(d.get("language", "en")),
        translations={},  # Canonical English sources; no implicit overlay loading.
        # Observed human effort — the difficulty axis. Read explicitly like every other field,
        # which is why they were inert until this line existed: `case.yaml` carried them and
        # `meta_from_yaml` silently dropped them. None is meaningful here and must survive: a
        # SIMULATED case has no human project to observe, and inventing a number would convert
        # an observed axis back into an estimate.
        expert_hours=d.get("expert_hours"),
        junior_hours=d.get("junior_hours"),
        effort_source=d.get("effort_source", ""),
        schema_version=d["schema_version"],
    )


def _load_generator(case_dir: str, case_id: str):
    gen_path = os.path.join(case_dir, "generator.py")
    spec = importlib.util.spec_from_file_location(f"dmaic_case_{case_id}", gen_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "generate"):
        raise ValueError(f"{gen_path} must define generate(seed) -> CaseData")
    return mod.generate


def load_native_case(case_dir: str) -> Case:
    meta = meta_from_yaml(os.path.join(case_dir, "case.yaml"))
    return Case(meta=meta, generate=_load_generator(case_dir, meta.case_id))


def discover(include_legacy: bool = True, cases_dir: str = CASES_DIR) -> dict:
    """Return {case_id: Case} for every registered case."""
    out = {}
    for name in sorted(os.listdir(cases_dir)):
        d = os.path.join(cases_dir, name)
        if name.startswith("_") or not os.path.isdir(d):
            continue
        if not os.path.exists(os.path.join(d, "case.yaml")):
            continue
        case = load_native_case(d)
        if case.case_id in out:
            raise ValueError(f"duplicate case_id {case.case_id}")
        out[case.case_id] = case
    if include_legacy:
        # The bridge module is HELD OUT of this repository (docs/HELD_OUT.md), so this branch
        # is normally a no-op and the native cases above are the whole corpus. Its absence is
        # tolerated; a bridge that exists but is BROKEN is not, because "12 cases quietly
        # became 0" is exactly the failure mode tests/test_public_corpus.py exists to catch.
        # Presence is probed rather than caught: `except ImportError` around the import
        # cannot tell "the module is not here" from "the module is here and raised", and
        # swallowing the second is how a corpus silently shrinks.
        try:
            present = importlib.util.find_spec(_LEGACY_BRIDGE) is not None
        except (ImportError, ValueError):        # parent package itself unimportable
            present = False
        if present:
            from ..cases import legacy_bridge    # failures INSIDE the bridge propagate
            for case in legacy_bridge.legacy_cases():
                # a native port of a legacy case shadows the bridge version
                out.setdefault(case.case_id, case)
    return out
