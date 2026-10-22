"""Case onboarding validator — the quality gate every case passes before entering the dataset.

`validate_case_dir` / `validate_case` return a list of Finding objects; empty ERROR set = admitted.
Checks (this docstring is the authoritative list; docs/CASE_ONBOARDING.md step 4 and
CONTRIBUTING.md each summarise it, and must be updated with it):

  V1  case.yaml parses and satisfies schemas/case.schema.json
  V2  every method_id (stages, alternatives, decision branches, faults) exists in the taxonomy
  V3  context/goal contain no method leakage (a case must not tell the agent which test to run)
  V4  generator determinism: generate(seed) twice -> byte-identical blocks and truths
  V5  parametric cases: generate(seed) and generate(seed+1) differ (the seed actually matters)
  V6  every truth entry references a stage in the case and a taxonomy method; tol > 0;
      hard (non-soft) entries must carry a non-empty derivation
  V7  truth verification: EVERY truth entry is put to an independent reference
      implementation in truth/verifiers.py. A mismatch is an ERROR. A truth that CANNOT be
      re-derived (no reference implementation, an unrecognised payload shape, or a reference
      that does not emit the named field) is a WARNING that names the method and the field —
      never a silent skip — and the run reports the verified fraction, so coverage cannot
      quietly rot again. See ``verification_coverage``.
  V10 truth/stage binding: one method may not carry truths from two different stages of the
      same case unless their field sets are disjoint (the downstream NF scorer merges a
      method's outputs across the whole trace by method_id alone, last-write-wins, so two
      stages binding the same method+field to different values cannot both be scored)
  V8  every stage payload is JSON-serializable and non-empty; topics unique enough to route
  V9  fault targets reference existing stages/methods; decision points reference valid phases
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Optional

import jsonschema
import yaml

from .. import taxonomy as taxonomy_mod
from .models import PHASES, Case, CaseData
from .registry import load_native_case

_HERE = os.path.dirname(os.path.abspath(__file__))
CASE_SCHEMA_PATH = os.path.normpath(os.path.join(_HERE, "..", "schemas", "case.schema.json"))

# Method-name leakage patterns: a case description naming the test to run destroys the MS metric.
_LEAKAGE_PATTERNS = [
    r"anova", r"cpk?\b", r"gage\s*r&?r", r"kappa",
    r"regression", r"chi-?squ", r"pareto", r"control\s*chart",
    r"t-?test", r"\b(?:doe|rsm)\b", r"mann-?whitney|kruskal|wilcoxon",
    r"RunSolverSpec|specKey|journey",
]

SEVERITIES = ("ERROR", "WARN", "INFO")

#: Outcome of putting one truth entry to a reference implementation. Only "verified" means
#: the number was independently reproduced; every other value is a hole in the V7 gate and is
#: reported as such.
VERIFICATION_STATUSES = (
    "verified",              # a reference impl recomputed the field and it matched
    "mismatch",              # a reference impl recomputed the field and it did NOT match
    "no_reference_impl",     # the method has no entry in verifiers.REFERENCE_IMPLS
    "field_not_emitted",     # the impl ran but returns no key matching the truth's field
    "payload_unrecognized",  # the impl refused the payload shape (NotVerifiable)
    "no_block",              # no stage payload could be resolved for this truth
    "reference_crash",       # the impl raised on a payload it did not refuse
)


@dataclass(frozen=True)
class Finding:
    check: str
    severity: str
    message: str

    def __str__(self):
        return f"[{self.severity}] {self.check}: {self.message}"


def _err(check, msg):
    return Finding(check, "ERROR", msg)


def _warn(check, msg):
    return Finding(check, "WARN", msg)


def _info(check, msg):
    return Finding(check, "INFO", msg)


def validate_yaml_dict(raw: dict) -> list:
    findings = []
    with open(CASE_SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    try:
        jsonschema.validate(raw, schema)
    except jsonschema.ValidationError as e:
        findings.append(_err("V1-schema", f"{'/'.join(str(p) for p in e.absolute_path)}: {e.message}"))
    return findings


def _check_leakage(meta) -> list:
    findings = []
    text = meta.context + "\n" + meta.goal
    for pat in _LEAKAGE_PATTERNS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            findings.append(_err("V3-leakage",
                                 f"context/goal leaks the method name {m.group(0)!r} — a case description must not hint at the statistical method"))
    return findings


def _check_method_ids(meta, tax) -> list:
    findings = []
    seen = []
    for s in meta.stages:
        for m in s.methods:
            seen.append((f"stage {s.stage_id}", m.method_id))
            seen.extend((f"stage {s.stage_id} alternative", a) for a in m.alternatives)
    seen.extend((f"fault {f.stage_id}", f.method_id) for f in meta.fault_targets)
    seen.extend(("case_level", m.method_id) for m in meta.case_level_methods)
    for where, mid in seen:
        if mid not in tax:
            findings.append(_err("V2-taxonomy", f"{where}: unknown method_id {mid!r}"))
    return findings


def _check_generated(case: Case, data: CaseData, tax) -> list:
    findings = []
    stage_ids = {s.stage_id for s in case.meta.stages}
    missing = stage_ids - set(data.blocks)
    if missing:
        findings.append(_err("V8-blocks", f"the generator produced no data block for stage(s): {sorted(missing)}"))
    for sid, payload in data.blocks.items():
        if sid not in stage_ids:
            findings.append(_warn("V8-blocks", f"the generator produced block {sid!r}, which case.yaml does not declare"))
        try:
            body = json.dumps(payload, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            findings.append(_err("V8-blocks", f"block {sid} is not JSON-serializable: {e}"))
            continue
        if len(body) < 10:
            findings.append(_err("V8-blocks", f"block {sid} is empty or too short"))
    for t in data.truths:
        if t.method_id not in tax:
            findings.append(_err("V6-truth", f"truth {t.field}: unknown method_id {t.method_id!r}"))
        if t.stage_id and t.stage_id not in stage_ids:
            findings.append(_err("V6-truth", f"truth {t.method_id}.{t.field}: unknown stage {t.stage_id!r}"))
        if t.tol < 0:
            findings.append(_err("V6-truth", f"truth {t.method_id}.{t.field}: tol must be >= 0"))
        if not t.soft and not t.derivation:
            findings.append(_err("V6-truth",
                                 f"truth {t.method_id}.{t.field}: a HARD truth must carry a derivation citing its source"))
    if not data.truths:
        findings.append(_warn("V6-truth", "the case carries no truth entries — the NF and HN layers cannot score it"))
    return findings


@dataclass(frozen=True)
class TruthVerification:
    """The record of putting ONE truth entry to an independent reference implementation.

    Produced whether or not the check succeeded — a truth the gate could not check is a
    result, not an absence, and this is the object that says so.
    """
    method_id: str
    field: str
    stage_id: Optional[str]          # as declared on the TruthEntry (None = unanchored)
    expected: float
    tol: float
    soft: bool
    status: str                      # one of VERIFICATION_STATUSES
    computed: Optional[float] = None
    resolved_stage: Optional[str] = None   # the block actually used
    candidate_stages: tuple = ()     # blocks tried for an unanchored truth
    convention: Optional[str] = None  # named alternative convention that matched, if any
    detail: str = ""

    @property
    def verified(self) -> bool:
        return self.status == "verified"


def _candidate_stages(case: Case, data: CaseData, t) -> list:
    """Blocks a truth could plausibly have been computed from, most specific first.

    A truth that names its stage has exactly one candidate. A truth with ``stage_id=None``
    (the legacy bridge writes that whenever a method is hosted by zero or by two-plus stages)
    is resolved to the stages that DECLARE the method — never to every block in the case,
    which would let an unrelated payload accidentally "confirm" a number.
    """
    if t.stage_id:
        return [t.stage_id] if t.stage_id in data.blocks else []
    return [s.stage_id for s in case.meta.stages
            if s.stage_id in data.blocks
            and any(m.method_id == t.method_id for m in s.methods)]


def _accepted_windows(t) -> list:
    """[(convention-name, expected, tol)] — the primary window plus any declared variants.

    ``TruthEntry.accepts`` records alternative conventions that are also correct statistics
    (Yates-corrected vs uncorrected, pooled vs Welch). A reference implementation that lands
    on one of them reproduced the truth under a named convention; it did not fail.
    """
    windows = [(None, float(t.expected), float(t.tol))]
    for entry in getattr(t, "accepts", ()) or ():
        try:
            if isinstance(entry, dict):
                windows.append((entry.get("convention"), float(entry["expected"]),
                                float(entry["tol"])))
            else:
                name, exp, tol = entry
                windows.append((str(name), float(exp), float(tol)))
        except (KeyError, TypeError, ValueError):
            continue
    return windows


def _match(t, value: float):
    """(matched?, convention-name) for a computed value against every accepted window."""
    for name, expected, tol in _accepted_windows(t):
        if abs(value - expected) <= max(tol, 1e-12):
            return True, name
    return False, None


def _verify_one(case: Case, data: CaseData, t, verifiers) -> TruthVerification:
    base = dict(method_id=t.method_id, field=t.field, stage_id=t.stage_id,
                expected=float(t.expected), tol=float(t.tol), soft=bool(t.soft))
    fn = verifiers.REFERENCE_IMPLS.get(t.method_id)
    if fn is None:
        return TruthVerification(**base, status="no_reference_impl",
                                 detail=f"truth/verifiers.py has no reference implementation for {t.method_id}")
    cands = _candidate_stages(case, data, t)
    if not cands:
        why = (f"stage {t.stage_id!r} has no data block" if t.stage_id
               else f"no stage declares {t.method_id} — this truth has nothing to attach to")
        return TruthVerification(**base, status="no_block", detail=why)

    wants_blocks = verifiers.wants_blocks(fn)
    outcome, notes = None, []
    for sid in cands:
        try:
            ref = fn(data.blocks[sid], data.blocks) if wants_blocks else fn(data.blocks[sid])
        except verifiers.NotVerifiable as e:
            notes.append(f"{sid}: payload shape not recognised ({e})")
            outcome = outcome or ("payload_unrecognized", None, sid, None)
            continue
        except Exception as e:  # a crash on a payload the impl did NOT refuse is a real bug
            return TruthVerification(**base, status="reference_crash", resolved_stage=sid,
                                     candidate_stages=tuple(cands),
                                     detail=f"the {t.method_id} reference implementation crashed on block {sid}: {e!r}")
        val = _suffix_lookup(ref, t.field)
        if val is None:
            notes.append(f"{sid}: the reference implementation does not emit field {t.field!r}")
            if outcome is None or outcome[0] == "payload_unrecognized":
                outcome = ("field_not_emitted", None, sid, None)
            continue
        ok, convention = _match(t, val)
        if ok:
            return TruthVerification(**base, status="verified", computed=val,
                                     resolved_stage=sid, candidate_stages=tuple(cands),
                                     convention=convention,
                                     detail="; ".join(notes))
        notes.append(f"{sid}: computed {val!r}")
        outcome = ("mismatch", val, sid, None)
    status, val, sid, _ = outcome
    return TruthVerification(**base, status=status, computed=val, resolved_stage=sid,
                             candidate_stages=tuple(cands), detail="; ".join(notes))


def verification_coverage(case: Case, data: Optional[CaseData] = None, seed: int = 1) -> list:
    """[TruthVerification] for every truth of a case — the V7 gate's full result set.

    Exposed so the verified fraction is a number anything can read (tests, the CLI, a corpus
    audit) rather than a side effect buried in a findings list.
    """
    from ..truth import verifiers
    if data is None:
        data = case.generate(seed)
    return [_verify_one(case, data, t, verifiers) for t in data.truths]


def verified_fraction(records) -> tuple:
    """(verified, total, fraction) over TruthVerification records; fraction is 1.0 when empty."""
    records = list(records)
    total = len(records)
    good = sum(1 for r in records if r.verified)
    return good, total, (good / total if total else 1.0)


def _check_truth_verification(case: Case, data: CaseData) -> list:
    """V7 — recompute every truth independently, and SAY SO when that was not possible.

    The previous implementation skipped an unverifiable truth with a bare ``continue``: no
    error, no warning, no count. A third of the corpus went through the gate untouched and the
    gate reported success. Every skip now becomes a WARNING naming the method and the field,
    and the run ends with the verified fraction, so the coverage number cannot silently rot.

    A mismatch stays an ERROR. Nothing here widens a tolerance or drops a check to make a
    number agree; a disagreement between a truth and an independent implementation is a
    finding to investigate, and burying it is the failure mode this gate exists to prevent.
    """
    records = verification_coverage(case, data)
    findings = []
    for r in records:
        if r.status == "verified":
            if len(r.candidate_stages) > 1:
                findings.append(_warn(
                    "V7-ambiguous",
                    f"{r.method_id}.{r.field}: the truth is bound to no stage; of the "
                    f"candidates {list(r.candidate_stages)} it was reproduced from "
                    f"{r.resolved_stage!r} — whether it holds equally for the other "
                    f"candidate blocks cannot be told apart"))
            if r.convention:
                findings.append(_info(
                    "V7-verify",
                    f"{r.method_id}.{r.field}: reproduced by the reference implementation "
                    f"under the alternative convention {r.convention!r}"))
        elif r.status == "mismatch":
            findings.append(_err(
                "V7-verify",
                f"{r.method_id}.{r.field}: the generator claims {r.expected}, the reference "
                f"implementation computed {r.computed} (tol={r.tol}) — the truth did not "
                f"pass independent re-derivation"))
        elif r.status == "reference_crash":
            findings.append(_err("V7-verify", r.detail))
        else:
            findings.append(_warn(
                "V7-unverified",
                f"{r.method_id}.{r.field} (stage={r.stage_id}, expected={r.expected}) "
                f"could not be independently re-derived [{r.status}]: {r.detail or '—'}"))
    good, total, frac = verified_fraction(records)
    findings.append(_info(
        "V7-coverage",
        f"independent re-derivation coverage {good}/{total} = {frac:.1%}"
        + ("" if total else " (the case carries no truth entries)")))
    return findings


def _check_truth_stage_binding(case: Case, data: CaseData) -> list:
    """V10 — one method may not carry truths from two stages unless the fields are disjoint.

    The NF scorer merges a trace's outputs per method_id ACROSS THE WHOLE TRACE, ignoring
    stage_id, last write wins. As long as no method binds truths at two stages, that merge is
    harmless. The moment a Control-stage capability confirmation is scored against a target
    set in Define — the planned design — the second stage's outputs silently overwrite the
    first's and one of the two truths is scored against the wrong numbers. This rule refuses
    the collision at onboarding instead of waiting for the corruption.
    """
    by_method = {}
    for t in data.truths:
        if not t.stage_id:
            continue
        by_method.setdefault(t.method_id, {}).setdefault(t.stage_id, set()).add(t.field)
    findings = []
    for mid, per_stage in by_method.items():
        if len(per_stage) < 2:
            continue
        stages = sorted(per_stage)
        for i, a in enumerate(stages):
            for b in stages[i + 1:]:
                shared = per_stage[a] & per_stage[b]
                if shared:
                    # Was an ERROR while `merged_outputs`' last-wins merge made this
                    # unscoreable. `nf.check_values` now matches a multi-truth method
                    # step-by-step and CLAIMS a step once, so two stages' truths can both be
                    # scored — provided the contestant emits one step per analysis. It is still
                    # a smell: a contestant that conflates both analyses into a single step
                    # leaves only one value visible and legitimately fails the other.
                    findings.append(_warn(
                        "V10-stage-binding",
                        f"{mid} binds field(s) {sorted(shared)} on stage {a!r} and on {b!r} "
                        f"— the contestant must write one step per analysis; conflating "
                        f"them into a single step leaves only one value visible and the "
                        f"other truth is (correctly) judged failed"))
                else:
                    findings.append(_info(
                        "V10-stage-binding",
                        f"{mid} carries truths on {len(per_stage)} stages "
                        f"({a!r}: {sorted(per_stage[a])}; {b!r}: {sorted(per_stage[b])}) — "
                        f"the field sets are disjoint, so merging is safe"))

    # The same collision, one level down: two truths on the SAME method+field with DIFFERENT
    # expected values. When both carry a stage the loop above already caught it; when neither
    # does (the legacy bridge writes stage_id=None whenever a method is hosted by two stages)
    # it slips past a stage-keyed rule while being exactly as unscoreable — the NF merge keeps
    # one set of outputs per method_id and cannot satisfy two different values of one field.
    by_field = {}
    for t in data.truths:
        by_field.setdefault((t.method_id, t.field), []).append(t)
    for (mid, field), entries in by_field.items():
        values = {round(float(t.expected), 12) for t in entries}
        if len(values) < 2:
            continue
        # Scoreable since `nf.check_values` began matching a multi-truth method step-by-step
        # and claiming each step once. It stays a WARN because it constrains the contestant's
        # trace shape: the values are only separable if each analysis is reported as its own
        # step. An unanchored pair is the weaker case -- nothing records which stage each value
        # belongs to -- so it warns too, and `_disambiguate_stage` in the legacy bridge exists
        # to shrink that set by binding whichever candidate payload actually reproduces a value.
        msg = (f"{mid}.{field} carries {len(values)} different truth values "
               f"{sorted(values)} in the same case "
               f"(stage: {[t.stage_id for t in entries]}) — the contestant must write one "
               f"step per analysis; otherwise the merge keeps only one value and the other "
               f"truth is judged failed")
        findings.append(_warn("V10-stage-binding", msg))
    return findings


def _suffix_lookup(d: dict, field: str):
    for k, v in d.items():
        if (k == field or k.endswith("." + field)) and isinstance(v, (int, float)):
            return float(v)
    return None


# --------------------------------------------------------------------------- V11 phase coverage

def _check_phase_coverage(case, data) -> list:
    """Report, per DMAIC phase, whether anything in it is actually GRADED.

    A stage that carries no truth and no decision point earns nothing: a contestant can skip it
    entirely and forfeit nothing. That is not hypothetical. Measured across all 372 built tasks
    before this rule existed:

        phase     stages   truths   decision points
        define         6        0        0      <- graded nowhere in the corpus
        measure      222      150      110
        analyze      294      236       56
        improve      112       52       26
        control       24       18        0      <- numbers only, never routing

    So a benchmark named for the full cycle graded Measure/Analyze/Improve. Nobody noticed for as
    long as nothing computed this table, which is the recurring shape of every defect this file
    now guards: the gap was silent, not subtle.

    Reported at INFO, per case, rather than enforced. A single case legitimately need not span
    all five phases -- an atomic-tier case is one stage by construction. The claim that must hold
    is about the CORPUS, and `tests/test_phase_coverage.py` asserts it there, where it is
    meaningful.
    """
    stage_phase = {s.stage_id: s.phase for s in case.meta.stages}
    per = {ph: {"stages": 0, "truths": 0, "points": 0} for ph in PHASES}
    for ph in stage_phase.values():
        if ph in per:
            per[ph]["stages"] += 1
    for t in data.truths:
        ph = stage_phase.get(t.stage_id)
        if ph in per and not t.soft:
            per[ph]["truths"] += 1
    for dp in case.meta.decision_points:
        ph = stage_phase.get(getattr(dp, "stage_id", None)) or getattr(dp, "phase", None)
        if ph in per:
            per[ph]["points"] += 1

    present = [ph for ph in PHASES if per[ph]["stages"]]
    graded = [ph for ph in present if per[ph]["truths"] or per[ph]["points"]]
    ungraded = [ph for ph in present if ph not in graded]
    out = [_info("V11-phase-coverage",
                 f"phase scoring coverage {len(graded)}/{len(present)}: "
                 + ", ".join(f"{ph}(hard truths {per[ph]['truths']}/"
                             f"decision points {per[ph]['points']})"
                             for ph in present))]
    if ungraded:
        out.append(_warn(
            "V11-phase-coverage",
            f"these phases exist but are not scored, so skipping them costs nothing: "
            f"{ungraded} — if a phase is meant to be assessed it needs at least one hard "
            f"truth or one decision point"))
    return out


def validate_case(case: Case, seeds=(1, 2)) -> list:
    tax = taxonomy_mod.load()
    findings = []
    findings += _check_method_ids(case.meta, tax)
    findings += _check_leakage(case.meta)

    d1 = case.generate(seeds[0])
    findings += _check_phase_coverage(case, d1)
    d1b = case.generate(seeds[0])
    if json.dumps(d1.blocks, sort_keys=True, ensure_ascii=False) != \
       json.dumps(d1b.blocks, sort_keys=True, ensure_ascii=False):
        findings.append(_err("V4-determinism", f"generate({seeds[0]}) gave different results on two calls"))
    if case.meta.parametric:
        d2 = case.generate(seeds[1])
        if json.dumps(d1.blocks, sort_keys=True, ensure_ascii=False) == \
           json.dumps(d2.blocks, sort_keys=True, ensure_ascii=False):
            findings.append(_err("V5-parametric",
                                 "parametric=true but changing the seed does not change the data — either honour the "
                                 "seed or declare parametric: false"))
    findings += _check_generated(case, d1, tax)
    findings += _check_truth_stage_binding(case, d1)
    findings += _check_truth_verification(case, d1)
    return findings


def validate_case_dir(case_dir: str) -> list:
    yaml_path = os.path.join(case_dir, "case.yaml")
    if not os.path.exists(yaml_path):
        return [_err("V1-schema", f"{case_dir} has no case.yaml")]
    with open(yaml_path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    findings = validate_yaml_dict(raw)
    if any(f.severity == "ERROR" for f in findings):
        return findings
    if not os.path.exists(os.path.join(case_dir, "generator.py")):
        return findings + [_err("V4-determinism", f"{case_dir} has no generator.py")]
    case = load_native_case(case_dir)
    return findings + validate_case(case)


def errors(findings: list) -> list:
    return [f for f in findings if f.severity == "ERROR"]
