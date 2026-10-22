"""Materialise DMAIC-Bench ``TaskInstance``s into Harbor task directories.

    python3 -m dmaic_harbor.build --out <dir> [--seeds 1,2,3] [--variants clean,dirty]
                                      [--tiers T1,T2,T3] [--limit N] [--cases a,b]

Layout emitted per task (Harbor's ``TaskPaths``)::

    <out>/<spec.harbor_task_name(task_id)>/
      instruction.md
      task.toml
      environment/.gitkeep              # build-context marker; the Dockerfile is not ours
      environment/task/blocks.json      # the stage data the steward may hand out
      environment/task/steward.json     # topics, prerequisite locks, honesty probe, budget
      solution/solve.sh                 # the oracle: derivation code, never an answer
      solution/plan.json                # oracle's route (method sequence + field names only)
      tests/.gitkeep                    # real test.sh lives in the verifier image

Three invariants this module is responsible for
-----------------------------------------------
1. **No truth in the agent container.** ``environment/`` carries data and public,
   handbook-normative gate thresholds; never a ``TruthEntry.expected``, never a
   ``DecisionPoint.correct_branch``.
2. **No method name in ``instruction.md``.** Choosing the method is the measured
   capability (bench gate V3). :func:`assert_no_method_leak` re-checks the *rendered*
   instruction against every ``method_id`` and alias in the taxonomy and aborts the build
   on a hit.
3. **No answer in ``solution/``.** Harbor's quality rubric fails a solution that echoes the
   final answer (``hardcoded_solution``) and fails ground truth shipped alongside the task
   (``anti_cheating_measures``). ``solve.sh`` therefore *derives* every number: it asks the
   steward for the data exactly as an agent would and computes with numpy/scipy. What it is
   allowed to know a priori — and all ``plan.json`` contains — is the route: which stages to
   ask for, in what order, which method each stage calls for, and what the output fields are
   named. No numeric result is written at build time.

Why ``fork_on`` is ``null`` everywhere
--------------------------------------
See :func:`_fork_on`. In short: this dataset's multi-branch decision points name their
branches after the method families they select (``binomial_capability`` vs
``continuous_capability``), and only ever have two of them, so publishing the branch set
into the agent container would hand over the very choice the benchmark measures. The useful,
leak-free half of that information — the *public predicate* that decides the branch — is
carried instead by ``unlock``.
"""
from __future__ import annotations

import argparse
import functools
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable, Optional

from . import policy
from . import spec
from . import steward_service
from . import v2_tasks
from . import verify

# --------------------------------------------------------------------------- bench import

#: where the steward drops the full JSON of every released batch. Set by the agent
#: Dockerfile's DMAIC_STEWARD_DATA_DIR; spec.py has no constant for it yet.
AGENT_DATA_DIR = "/workspace/data"

#: Set only by the CLI's --internal flag. Default False: a build refuses to emit a corpus
#: carrying a real organisation's identity, because the de-identification is reversible in a
#: developer tree and instruction.md is copied into the agent image.
_ALLOW_INTERNAL_IDENTITY = False

#: The repository root, which is also the bench package's parent:
#: harbor/src/dmaic_harbor/build.py -> dmaic_harbor -> src -> harbor -> <repo root>.
BENCH_ROOT = Path(__file__).resolve().parents[3]
TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"


def _ensure_bench_importable() -> None:
    p = str(BENCH_ROOT)
    if p not in sys.path:
        sys.path.insert(0, p)


_ensure_bench_importable()

from dmaic_bench import taxonomy as taxonomy_mod          # noqa: E402
from dmaic_bench.core import registry                      # noqa: E402
from dmaic_bench.core.models import PHASES, data_fingerprint  # noqa: E402
from dmaic_bench.tasks import builder as builder_mod       # noqa: E402
from dmaic_bench.tasks.builder import build_all            # noqa: E402
from dmaic_bench.v2 import correspondence                  # noqa: E402
from dmaic_bench.v2 import hints                           # noqa: E402


# --------------------------------------------------------------------------- v2 recognition

_V2_CASES: dict = {}


def v2_cases() -> dict:
    """``{case_id: V2Case}`` for the data-conditioned decision-graph projects, cached."""
    if not _V2_CASES:
        _V2_CASES.update(v2_tasks.discover())
    return _V2_CASES


def v2_case_for(task):
    """The v2 project a task came from, or ``None`` for a v1 task.

    Deliberately derived from ``task.case_id`` rather than carried on the task or registered in
    a side table: a stateless lookup cannot go stale, and the two id spaces are disjoint by
    construction (v1 cases live in ``dmaic_bench/cases/``, v2 projects are Python modules and
    were assigned the next free ``adb_cNN`` codes).
    """
    return v2_cases().get(getattr(task, "case_id", None))


def is_v2(task) -> bool:
    return v2_case_for(task) is not None


# --------------------------------------------------------------------------- tiny renderer

_VAR_RE = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")
_IF_RE = re.compile(
    r"\{\{#if\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}\n?(.*?)\{\{/if\}\}\n?",
    re.DOTALL,
)


def render(template: str, ctx: dict) -> str:
    """`{{ name }}` substitution plus `{{#if name}}…{{/if}}` blocks. No jinja2 dependency.

    Deliberately tiny: the templates are ours, so the renderer only needs to do what they
    use. An unknown variable is an error rather than an empty string — a silently blank
    business context would be a broken task nobody notices.
    """

    def _if(m: "re.Match[str]") -> str:
        name, body = m.group(1), m.group(2)
        if name not in ctx:
            raise KeyError(f"template conditional on unknown variable {name!r}")
        return body if ctx[name] else ""

    out = _IF_RE.sub(_if, template)

    def _var(m: "re.Match[str]") -> str:
        name = m.group(1)
        if name not in ctx:
            raise KeyError(f"template references unknown variable {name!r}")
        return str(ctx[name])

    return _VAR_RE.sub(_var, out)


# --------------------------------------------------------------------------- method leak gate

def method_terms() -> set:
    """Every string that would name a statistical method: method_ids and their aliases."""
    tx = taxonomy_mod.load()
    terms = set()
    for m in tx.methods.values():
        terms.add(m.method_id.lower())
        for a in m.aliases:
            a = a.strip().lower()
            if a:
                terms.add(a)
    return terms


#: The header row of the vocabulary table, per language. It is the anchor
#: :func:`assert_no_method_leak` uses to strip the table before scanning, so it MUST stay
#: byte-identical to what :func:`method_vocabulary` emits for the same language — if the two
#: drift, the strip misses and every build aborts on its own vocabulary table.
VOCAB_HEADINGS = {
    "en": "| family | `method_id` | canonical output field names |",
}
#: Compatibility alias for callers that use the single authoritative heading.
VOCAB_HEADING = VOCAB_HEADINGS["en"]


def vocab_heading(language: str) -> str:
    if language != "en":
        raise ValueError(f"unsupported language {language!r}; the official benchmark is English only")
    return VOCAB_HEADINGS["en"]


def method_vocabulary(language: str = "en") -> str:
    """The FULL canonical method vocabulary, identical for every task.

    The trace contract requires a canonical `method_id`, but the instruction never said what
    the vocabulary was -- the leak gate below forbade every method name, so an agent was asked
    to hit a 49-value enum it had not been shown. Measured on a live run: a model computed all
    seven required analyses correctly and scored MS-Recall 0.000, because it wrote
    `msa.agreement` for `msa.attribute_agreement`, `quality.pareto` as `pareto.prioritization`,
    and so on. Seven for seven semantically, zero for seven by string match. That is naming
    luck, not method selection, and every contestant would have failed it the same way.

    The same defect has a second layer, found the same way. Once the model hit
    `msa.attribute_agreement` it reported `overall_agreement_rate`; the truth entry wants
    `kappaMin`, suffix matching could not bind them, and because that entry is `soft` the
    result was neither a pass nor a failure -- so Numeric Fidelity returned 1.000 having
    checked nothing. Publishing the method names without their OUTPUT names just moves the
    naming lottery one level down, so this table carries both.

    Publishing the WHOLE menu leaks nothing about a particular task -- it is the same 49 rows
    everywhere, and knowing that `capability.binomial` emits `processZ` does not tell an agent
    that this task needs capability analysis. What must never appear is the per-stage
    shortlist, which is what :func:`assert_no_method_leak` still guards.
    """
    tx = taxonomy_mod.load()
    rows = []
    for mid, m in tx.methods.items():
        outs = [getattr(o, "name", o) for o in (getattr(m, "canonical_outputs", None) or [])]
        rows.append((m.family, mid, outs))
    lines = [vocab_heading(language), "|---|---|---|"]
    for fam, mid, outs in sorted(rows):
        names = ", ".join(f"`{o}`" for o in outs) if outs else "-"
        lines.append(f"| {fam} | `{mid}` | {names} |")
    return "\n".join(lines)


class MethodLeak(RuntimeError):
    """Raised when a rendered instruction names a method the agent is supposed to choose."""


#: Terms whose Latin spelling is a bare word that ordinary business prose contains, matched
#: with word boundaries below. Nothing is exempted from the scan — this note exists to record
#: WHY naked containment could not survive the English arm: ``ols`` is a substring of
#: "controls", so "the line has no process controls" aborted the build, and ``rsm``,
#: ``grr``, ``cp/cpk`` and ``rpn`` are the same shape.
_WORD_EDGE = r"[0-9a-z_]"


@functools.lru_cache(maxsize=None)
def _term_pattern(term: str):
    """Compile one taxonomy term into its leak-scan regex.

    Latin terms are boundary-anchored; a CJK term keeps containment semantics, because word
    boundaries do not exist in Chinese and a method name inside a longer compound is still the
    method being named. Separator runs are elastic, so banning ``gage r&r`` also bans
    "gage  r & r" and ``control chart`` also bans "control-chart".
    """
    body = r"[\s_\-]*".join(re.escape(p) for p in re.split(r"[\s_\-]+", term) if p)
    if not body:
        return None
    head = f"(?<!{_WORD_EDGE})" if re.match(r"[0-9a-z]", term) else ""
    tail = f"(?!{_WORD_EDGE})" if re.search(r"[0-9a-z]$", term) else ""
    return re.compile(head + body + tail)


def method_terms_in(text: str) -> list:
    """Every taxonomy term *text* actually names, word-aware. Sorted, deduplicated."""
    low = (text or "").lower()
    hits = []
    for term in method_terms():
        rx = _term_pattern(term)
        if rx is not None and rx.search(low):
            hits.append(term)
    return sorted(set(hits))


def identifier_leaks(task_id: str) -> list:
    """Method terms contained in a task's own identifier.

    A handful of T1 ids embed the method in the case id or the stage id
    (``adb_c01-T1-R_Analyze-…``, ``adb_c23-T1-M_GRR-…``). The identifier is structurally
    unavoidable in ``instruction.md`` — the trace has to carry it back — so it is excluded
    from the leak scan and surfaced here instead, loudly, for whoever owns the case files.
    """
    low = task_id.lower()
    # Deliberately naked containment, unlike the prose gate: an identifier such as
    # ``adb_c23-T1-M_GRR-s1-clean`` has no word boundaries to speak of, and the point here is
    # to surface the id, not to score English.
    return sorted(t for t in method_terms() if t in low)


class IdentityLeak(RuntimeError):
    """Raised when a build would emit a corpus carrying real organisation identities."""


PUBLIC_IDENTITY_ENV = "DMAIC_BENCH_PUBLIC_IDENTITY"
IDENTITY_MAP = "_identity_map.json"


def identity_mode() -> tuple:
    """``(is_internal, why)`` -- would this build serve internal identities?

    The de-identification is upstream, but it is **reversible in a developer tree**: the case
    bridge re-applies internal names whenever the developer-only identity map is present and
    ``DMAIC_BENCH_PUBLIC_IDENTITY`` is unset. Measured, not hypothesised -- a default build
    produced 166 of 377 tasks whose ``instruction.md``, copied verbatim into the agent image as
    ``TASK.md``, named a real company.

    Deliberately a check on the MODE, not a scan of the text: a text scan needs a list of the
    names it is hunting for, and that list would then have to live in this repository. The mode
    is the invariant, and it has no false positives.
    """
    path = BENCH_ROOT / "dmaic_bench" / "cases" / IDENTITY_MAP
    if not path.exists():
        return False, "no identity map on disk (a released package): identities are public"
    if os.environ.get(PUBLIC_IDENTITY_ENV, "").strip() not in ("", "0", "false", "False"):
        return False, f"{PUBLIC_IDENTITY_ENV} is set, so the bridge serves public identities"
    return True, (f"{IDENTITY_MAP} is present and {PUBLIC_IDENTITY_ENV} is unset, so the case "
                  f"bridge re-applies internal identities")


def assert_public_identity(allow_internal: bool) -> None:
    """Refuse to build an internal-identity corpus unless explicitly asked for.

    The flag turns the guard OFF rather than on: a gate whose safe state is the default is the
    only kind that survives someone in a hurry.
    """
    internal, why = identity_mode()
    if internal and not allow_internal:
        raise IdentityLeak(
            "refusing to emit a corpus carrying real organisation identities: " + why + ".\n"
            f"  publishable corpus : {PUBLIC_IDENTITY_ENV}=1 python3 -m dmaic_harbor.build ...\n"
            "  or build from the released wheel, which ships no identity map.\n"
            "  internal-only corpus: pass --internal, and do not publish the result."
        )


def assert_no_method_leak(text: str, where: str, allow: Iterable[str] = ()) -> None:
    """Abort the build if *text* names any taxonomy method (bench gate V3).

    ``allow`` masks literal substrings (the task identifier) before scanning, so an
    unavoidable identifier does not hide a real leak elsewhere in the same document.
    """
    # The vocabulary block is the full menu and is identical for every task, so it cannot
    # disclose anything about THIS one. Strip it before scanning; what the gate still catches
    # is a per-stage shortlist leaking into the prose, which is the thing that would hand over
    # the answer.
    body = text
    for heading in VOCAB_HEADINGS.values():
        if heading in body:
            start = body.index(heading)
            end = body.find("\n\n", start)
            body = body[:start] + (body[end:] if end != -1 else "")
    low = body.lower()
    for token in allow:
        low = low.replace(str(token).lower(), " ")
    hits = method_terms_in(low)
    if hits:
        raise MethodLeak(
            f"{where} names statistical method(s) {hits!r}. Choosing the method is the "
            f"measured capability; it must not appear in the instruction."
        )


# --------------------------------------------------------------------------- prior facts

#: Single-sourced from the builder, which is what WRITES these strings. They used to be a
#: literal here and a literal there, keyed on the ideographic semicolon and the prefix
#: ``Completed: ``; under English generation both simply disappeared and this whole function
#: became a silent no-op that let the unsanitised stage labels — i.e. the method names — flow
#: into ``instruction.md``.
_PLACEHOLDER_PRIOR = {
    lang: re.compile("^" + re.escape(prefix))
    for lang, prefix in builder_mod.PRIOR_DONE_PREFIX.items()
}


def _prior_language(task) -> str:
    lang = getattr(task, "language", "en")
    return lang if lang in _PLACEHOLDER_PRIOR else "en"


#: The sentence that replaces the dropped stage-label placeholders. It carries the information
#: the agent legitimately needs (earlier phases are done, do not redo them) and no method name.
_PRIOR_REPLACEMENT = {
    "en": ("The project team has already completed the field work for the {phases} "
           "phase(s) — {n} item(s) in all — and those conclusions stand as given for this "
           "task. You are not asked to redo that work; complete this phase's analysis from "
           "the data the steward provides."),
}
_PRIOR_PHASE_JOIN = {"en": ", "}
_PRIOR_PHASE_FALLBACK = {"en": "earlier"}


def sanitize_prior_facts(task) -> str:
    """T2 ``prior_facts`` minus the stage labels, which name methods.

    ``tasks.builder`` builds prior_facts as ``summary_fact or f"Completed: {stage.label}"``, and
    every case in the registry today has empty ``summary_fact`` — so prior_facts is a list of
    stage labels such as ``Completed: baseline binomial capability (six months)``. Those labels hand the agent the
    method for the phase it is being scored on, so the placeholders are replaced by a
    phase-level statement that carries the same *information the agent legitimately needs*
    (earlier phases are done; do not redo them) and none of the method names. A real
    ``summary_fact`` is passed through untouched — and if one ever names a method,
    :func:`assert_no_method_leak` fails the build rather than leaking it silently.
    """
    raw = (task.prior_facts or "").strip()
    if not raw:
        return ""
    lang = _prior_language(task)
    sep = builder_mod.PRIOR_SEPARATOR[lang]
    parts = [p.strip() for p in raw.split(sep.strip() or sep) if p.strip()]
    kept = [p for p in parts if not _PLACEHOLDER_PRIOR[lang].match(p)]
    dropped = len(parts) - len(kept)
    if dropped:
        phase = task.phase or ""
        earlier = [p for p in PHASES[:PHASES.index(phase)]] if phase in PHASES else []
        phase_text = (_PRIOR_PHASE_JOIN[lang].join(earlier) if earlier
                      else _PRIOR_PHASE_FALLBACK[lang])
        kept.insert(0, _PRIOR_REPLACEMENT[lang].format(phases=phase_text, n=dropped))
    return sep.join(kept) if len(kept) > 1 else (kept[0] if kept else "")


# --------------------------------------------------------------------------- gates / locks

#: order-constraint ``before`` reference -> the public gate that closes it.
#: Only predicates that exist in ``spec.PUBLIC_GATES`` may be used; anything else stays
#: ``None`` so the steward never invents a lock it cannot justify from a public threshold.
_GATE_FOR_BEFORE = {
    "msa.gage_rr_crossed": "msa_pass",          # %GRR <= 30, AIAG MSA-4
    "basic.normality": "normality_pass",        # AD p >= 0.05, Montgomery ISQC
}

#: taxonomy ``applicability.prerequisites`` -> public gate. ``variances_equal`` has no public
#: predicate in the contract and is therefore never a lock.
_GATE_FOR_PREREQ = {
    "stability_confirmed": "stability_pass",
    "normality_holds": "normality_pass",
}

#: which method families can *produce* each gate's declared field
_GATE_PRODUCERS = {
    "msa_pass": lambda mid: mid == "msa.gage_rr_crossed",
    "msa_ndc": lambda mid: mid == "msa.gage_rr_crossed",
    "stability_pass": lambda mid: mid.startswith("control_chart."),
    "normality_pass": lambda mid: mid in ("basic.normality", "basic.descriptive_summary"),
    "screening_significant": lambda mid: mid.startswith("doe.factorial"),
}

_GATE_ORDER = tuple(spec.PUBLIC_GATES)   # deterministic tie-break


def _stage_method_ids(stage) -> set:
    return {m.method_id for m in stage.methods}


def _ref_matches(ref: str, method_ids: Iterable[str]) -> bool:
    if ref.startswith("family:"):
        fam = ref.split(":", 1)[1]
        return any(mid.split(".")[0] == fam for mid in method_ids)
    return ref in set(method_ids)


def _gate_for_constraint(before: str, after: str) -> Optional[str]:
    if before in _GATE_FOR_BEFORE:
        return _GATE_FOR_BEFORE[before]
    if before.startswith("control_chart.") or before == "family:control_chart":
        return "stability_pass"
    if before.startswith("doe.factorial") and after.startswith("doe.rsm"):
        # screening precedes response-surface work (Montgomery DAOE 6e 11.2)
        return "screening_significant"
    return None


def _gate_producer_stage(task, gate: str, before: str = "") -> Optional[str]:
    """The in-scope stage that produces *gate*'s declared field, ahead of stage *before*.

    The ordering test is what makes a lock satisfiable: a gate whose producing stage is only
    offered later in the journey would leave the locked batch permanently out of reach. That
    is not hypothetical — ``adb_c08`` lists its control chart in the *control* phase, after the
    capability analysis, so a naive stability lock on that capability stage can never open.
    """
    order = [s.stage_id for s in task.stages]
    limit = order.index(before) if before in order else len(order)
    for i, s in enumerate(task.stages):
        if i >= limit:
            break
        if any(_GATE_PRODUCERS[gate](m.method_id) for m in s.methods):
            return s.stage_id
    return None


def _gate_candidates(task, stage) -> set:
    """Public gates a stage genuinely waits on, from order constraints + taxonomy prereqs.

    Both sources are filtered by the same safety rule: a lock is kept only when the method
    that *produces* the declared field is itself in scope for this task instance. Otherwise
    the agent could never satisfy it and the task would be unsolvable — a T1 capability probe,
    for example, ships no control-chart stage, so it gets no stability lock.
    """
    mine = _stage_method_ids(stage)
    if not mine:
        return set()
    out: set = set()
    for oc in task.order_constraints:
        if not _ref_matches(oc.after, mine):
            continue
        gate = _gate_for_constraint(oc.before, oc.after)
        if gate and _gate_producer_stage(task, gate, before=stage.stage_id):
            out.add(gate)

    tx = taxonomy_mod.load()
    for mid in mine:
        if mid not in tx:
            continue
        for prereq in tx.get(mid).prerequisites:
            gate = _GATE_FOR_PREREQ.get(prereq)
            if gate and _gate_producer_stage(task, gate, before=stage.stage_id):
                out.add(gate)
    return out


def _required_stages(task, stage) -> list:
    """Upstream stage_ids this stage's order constraints genuinely depend on.

    A stage_id is not a method name — it says *which batch* must come first, not what to do
    with it — so publishing it to the steward leaks nothing the routing topics do not.
    """
    mine = _stage_method_ids(stage)
    if not mine:
        return []
    order = [s.stage_id for s in task.stages]
    out = []
    for oc in task.order_constraints:
        if not _ref_matches(oc.after, mine):
            continue
        for s in task.stages:
            if s.stage_id == stage.stage_id:
                continue
            if not _ref_matches(oc.before, _stage_method_ids(s)):
                continue
            if order.index(s.stage_id) < order.index(stage.stage_id) and s.stage_id not in out:
                out.append(s.stage_id)
    return out


#: Conclusion-dependent forks this dataset can actually support, as
#: (upstream-method test, downstream-method test, declare key, gate the fork supersedes).
#:
#: A fork is the steward routing the NEXT batch by a verdict the agent has stated. Two
#: textbook instances exist in DMAIC; only the second occurs in this dataset:
#:
#: 1. stability -> (capability | special-cause hunt). Emitted whenever a control-chart stage
#:    precedes a capability stage that normatively depends on it. **No case in the current
#:    registry qualifies**: the three cases with a control chart put it in the *control*
#:    phase, after capability, and the one case whose chart precedes a capability analysis
#:    (adb_c15) puts both methods in a single stage, so there is no second batch to route.
#:    The rule stays here because it costs nothing and fires the moment a case adds one.
#: 2. screening -> response surface. A 2^k with centre points exists to answer one question:
#:    is there curvature? If there is, you augment to a central composite and the axial runs
#:    are a genuinely NEW experiment the plant only performs on that verdict (Montgomery
#:    DAOE 6e §11.2). That is exactly a data release conditioned on a stated conclusion, and
#:    it names no method: the declare key is `curvature_significant`, the branch targets are
#:    stage_ids.
#:
#: NOTE the key is deliberately `curvature_significant`, not the PUBLIC_GATES key
#: `screening_significant`. They are not the same claim, and the difference is not academic:
#: in `adb_c07` the screening model as a whole is not significant (p=0.19) while curvature is
#: overwhelming (p=5e-5) — forking on "any factor significant" would padlock the case's own
#: normative path. `fork_on.field` is any declare key, so the correct predicate is available.
_FORK_RULES = (
    (lambda m: m.startswith("control_chart."), lambda m: m.startswith("capability."),
     "stable", "stability_pass"),
    (lambda m: m.startswith("doe.factorial"), lambda m: m.startswith("doe.rsm"),
     "curvature_significant", "screening_significant"),
)

#: declare key -> the public gate a fork on it makes redundant (see _unlock_for_stage).
_FORK_SUPERSEDES = {field: gate for _, _, field, gate in _FORK_RULES}


def _forks_for_task(task) -> dict:
    """stage_id -> ``fork_on`` object for every stage whose verdict routes a later batch.

    Conditions, all required: the two stages are distinct and in the right order; the
    upstream stage produces the verdict and the downstream stage consumes it per
    :data:`_FORK_RULES`; and the case itself declares the dependency as an order constraint,
    so the fork is the case author's normative claim rather than the builder's guess.

    The emitted object names a declare key and a set of stage_ids. It contains no method, and
    nothing about which branch is correct — ``DecisionPoint.correct_branch`` never leaves the
    verifier.
    """
    forks: dict = {}
    order = [s.stage_id for s in task.stages]
    for up in task.stages:
        branches: dict = {}
        for up_test, down_test, field, _gate in _FORK_RULES:
            if not any(up_test(m.method_id) for m in up.methods):
                continue
            for down in task.stages:
                if order.index(down.stage_id) <= order.index(up.stage_id):
                    continue
                if not any(down_test(m.method_id) for m in down.methods):
                    continue
                linked = any(
                    _ref_matches(oc.before, _stage_method_ids(up))
                    and _ref_matches(oc.after, _stage_method_ids(down))
                    for oc in task.order_constraints)
                if not linked:
                    continue
                branches.setdefault(field, set()).add(down.stage_id)
        for field, stage_ids in sorted(branches.items()):
            forks[up.stage_id] = {"field": field,
                                  "branches": {"true": sorted(stage_ids)}}
    return forks


def _unlock_for_stage(task, stage, forked_gates: Iterable[str] = ()) -> Optional[dict]:
    """``{"requires": [stage_id…], "gates": [gate…]}`` or ``None``.

    Gates already enforced by an upstream ``fork_on`` are dropped here: the fork requires the
    agent to declare the verdict before the batch is routed, so repeating it as a threshold
    lock would just make the same demand twice.
    """
    gates = sorted(_gate_candidates(task, stage) - set(forked_gates),
                   key=_GATE_ORDER.index)
    requires = _required_stages(task, stage)
    if not gates and not requires:
        return None
    out: dict = {}
    if requires:
        out["requires"] = requires
    if gates:
        out["gates"] = gates
    return out


def _fork_on(task, stage) -> None:
    """Kept only so the shape of a stage entry is documented in one place; see
    :func:`_forks_for_task`, which is what :func:`build_steward_config` actually calls."""
    return _forks_for_task(task).get(stage.stage_id)


# --------------------------------------------------------------------------- steward config

#: All published cases must pass the routing and label authoring gates.
STRICT_AUTHORING_LANGUAGES = ("en",)


class LabelLeak(RuntimeError):
    """Raised when an agent-visible stage label or topic names a method."""


def steward_label_leaks(stages) -> dict:
    """``{stage_id: [term…]}`` for every stage whose label or topics name a taxonomy method.

    ``steward.json`` is copied into the agent image and the steward echoes ``label (topics)``
    pairs back in its ``unroutable`` and ``status`` replies, so a label that names the method
    hands over the very choice the benchmark measures — the V3 gate defeated by the corpus
    rather than by the agent.
    """
    out = {}
    for s in stages:
        text = " ".join([s["label"]] + list(s["topics"]))
        hits = method_terms_in(text)
        if hits:
            out[s["stage_id"]] = hits
    return out


def assert_no_label_leak(stages, where: str) -> None:
    leaks = steward_label_leaks(stages)
    if leaks:
        raise LabelLeak(
            f"{where}: stage label/topics name statistical method(s) {leaks!r}. Labels are "
            f"agent-visible (steward.json, and the steward's own unroutable/status replies); "
            f"name the BATCH OF DATA, not the analysis to run on it.")


def build_steward_config(task) -> dict:
    """The steward's whole world: routing topics, prerequisite locks, forks, probe, budget.

    Schema is ``steward_service.load_config``'s strict allowlist; unknown keys fail the
    steward closed, which is how the data/truth split is enforced mechanically rather than
    by convention.

    NOTE for whoever reads this file inside the agent container: it legitimately contains
    stage *labels*, and labels name methods (``appraiser attribute agreement (MSA)``). They are here because
    the steward routes free-form requests onto them. The steward must therefore never echo
    its configuration back to the agent — not in ``status``, not in a refusal. Refusals may
    quote the ``gates`` block (public handbook thresholds) and nothing else.
    """
    v2_case = v2_case_for(task)
    if v2_case is not None:
        return _v2_steward_config(task, v2_case)

    forks = _forks_for_task(task)
    forked_gates: dict = {}
    for fork in forks.values():
        gate = _FORK_SUPERSEDES.get(fork["field"])
        for stage_ids in fork["branches"].values():
            for sid in stage_ids:
                if gate:
                    forked_gates.setdefault(sid, set()).add(gate)

    stages = []
    used_gates = set()
    for s in task.stages:
        unlock = _unlock_for_stage(task, s, forked_gates.get(s.stage_id, ()))
        if unlock:
            used_gates.update(unlock.get("gates", ()))
        entry = {
            "stage_id": s.stage_id,
            "phase": s.phase,
            "label": s.label,
            "topics": list(s.topics),
        }
        if unlock:
            entry["unlock"] = unlock
        if s.stage_id in forks:
            entry["fork_on"] = forks[s.stage_id]
        stages.append(entry)

    language = _language(task)
    if language in STRICT_AUTHORING_LANGUAGES:
        # Both gates run on the payload about to be written, before any container exists.
        steward_service.validate_topics(stages)
        assert_no_label_leak(stages, f"steward.json for {task.task_id}")

    cfg = {
        "schema": 1,
        "task_id": task.task_id,
        "max_turns": task.max_turns,
        "language": language,
        "stages": stages,
        # descriptive, provably oracle-free; steward_service tolerates and ignores these
        "case_id": task.case_id,
        "tier": task.tier,
        "phase": task.phase or "",
        "variant": task.variant,
        "seed": task.seed,
        "gates": {k: dict(spec.PUBLIC_GATES[k]) for k in sorted(used_gates)},
        "refusal_codes": list(spec.STEWARD_REFUSALS),
        "actions": list(spec.STEWARD_ACTIONS),
    }
    if task.fault is not None:
        # NO method_id: this file is readable inside the agent container, and the probe's
        # whole point is that the agent must not know which analysis the withheld batch was
        # for. The verifier's truth package carries the method_id.
        cfg["fault"] = {"stage_id": task.fault.stage_id,
                        "denial_message": task.fault.denial_message}
        if getattr(task.fault, "withheld_key", None):
            cfg["fault"]["withheld_key"] = task.fault.withheld_key
    return cfg


def _v2_steward_config(task, case) -> dict:
    """``steward.json`` for a decision-graph project.

    A v2 stage IS a batch of data (see ``v2_tasks``), so there are no method families to infer
    a lock from and no ``fork_on`` to publish: the locks are the case's own gate policy,
    translated from graph nodes onto batches by :func:`v2_tasks.locks`. Everything that reaches
    this file is the same three kinds of thing a v1 payload carries -- routing topics, the
    prerequisite batch, and a PUBLIC handbook threshold from ``spec.PUBLIC_GATES``.

    What is NOT here, and must never be: the graph, the guards, the oracle results, the correct
    branch, or the fault probe's method. Those live in the verifier's truth package.
    """
    lock_map = v2_tasks.locks(case)
    # A LOCK WHOSE PREREQUISITE THE PLANT ITSELF WITHHOLDS IS NOT A METHODOLOGY GATE.
    #
    # The honesty probe denies one batch. On these projects that batch is the gauge study, which
    # is also the prerequisite for the process run, so leaving the lock in place padlocked the
    # entire project behind a batch nobody could obtain: measured on all four probe variants,
    # a perfectly honest reference solution that disclosed the denial scored reward 0.000 with
    # ms_recall 0.000 and pq 0.000, because it was never given anything to analyse. The probe is
    # meant to ask whether a contestant admits a gap, not to convert the task into an
    # unsolvable one, so a denied batch releases the locks that depend on it.
    denied = task.fault.stage_id if task.fault is not None else None
    if denied:
        lock_map = {
            sid: {"requires": [r for r in lock.get("requires", ()) if r != denied],
                  "gates": ([] if denied in v2_tasks.gate_producers(case, lock.get("gates", ()))
                            else list(lock.get("gates", ())))}
            for sid, lock in lock_map.items()}
    stages, used_gates = [], set()
    for s in task.stages:
        entry = {"stage_id": s.stage_id, "phase": s.phase, "label": s.label,
                 "topics": list(s.topics)}
        lock = lock_map.get(s.stage_id)
        if lock and (lock.get("requires") or lock.get("gates")):
            unlock = {}
            if lock.get("requires"):
                unlock["requires"] = list(lock["requires"])
            if lock.get("gates"):
                unlock["gates"] = list(lock["gates"])
                used_gates.update(lock["gates"])
            entry["unlock"] = unlock
        stages.append(entry)

    language = _language(task)
    if language in STRICT_AUTHORING_LANGUAGES:
        steward_service.validate_topics(stages)
        assert_no_label_leak(stages, f"steward.json for {task.task_id}")

    cfg = {
        "schema": 1,
        "task_id": task.task_id,
        "max_turns": task.max_turns,
        "language": language,
        "stages": stages,
        "case_id": task.case_id,
        "tier": task.tier,
        "phase": task.phase or "",
        "variant": task.variant,
        "seed": task.seed,
        "gates": {k: dict(spec.PUBLIC_GATES[k]) for k in sorted(used_gates)},
        "refusal_codes": list(spec.STEWARD_REFUSALS),
        "actions": list(spec.STEWARD_ACTIONS),
    }
    if task.fault is not None:
        cfg["fault"] = {"stage_id": task.fault.stage_id,
                        "denial_message": task.fault.denial_message}
        if getattr(task.fault, "withheld_key", None):
            cfg["fault"]["withheld_key"] = task.fault.withheld_key
    # The *remind* control: publish the handbook preconditions as predicates over declared
    # values so the steward can say, at the moment of declaration, whether the next analysis
    # is licensed. Predicates and field names only (v2_tasks.preconditions); no lock changes.
    if INSTRUCTION_VARIANT == "remind":
        cfg["preconditions"] = v2_tasks.preconditions(case)
    return cfg


def gate_locks(task) -> dict:
    """``{stage_id: [gate…]}`` — the public locks, for the verifier's gate-violation naming.

    Same public-threshold set the steward enforces, so the two cannot disagree.
    """
    cfg = build_steward_config(task)
    return {s["stage_id"]: list(s["unlock"]["gates"])
            for s in cfg["stages"]
            if s.get("unlock", {}).get("gates")}


# --------------------------------------------------------------------------- oracle plan

def _n_decision_points(task) -> int:
    """How many graded forks this seed's correct route actually has.

    A v2 task carries `decision_points=()` ON PURPOSE -- materialising them in the build would
    freeze a `correct_branch` into the dataset, which is the defect that whole path exists to
    remove. But reading `len(())` for the METADATA published 0 for every task in the corpus,
    and decision points are what this benchmark measures. A count is not a correct branch: it
    says how many forks are on the route, not which way any of them goes.

    Nothing here reaches the agent. `task.toml` is dataset metadata for the operator and the
    paper; the agent container is built from `environment/task` alone.
    """
    if task.decision_points:
        return len(task.decision_points)
    try:
        from dmaic_bench.v2 import harbor_truth, registry
        case = registry.discover().get(task.case_id)
        if case is None:
            return 0
        _blocks, results = case.generate(int(task.seed))
        node_methods = {k: tuple(case.methods_at(k, results)) for k in case.node_data}
        return len(harbor_truth.decision_points(case.graph, results, node_methods,
                                                case.method_policy))
    except Exception:  # noqa: BLE001 - a v1 task has no v2 case and keeps its own count
        return 0


def _v2_oracle_plan(task, case) -> dict:
    """The reference solution's route knowledge for a decision-graph project.

    It is the GRAPH, never the walk. ``solve.sh`` asks the steward for a node's batch, computes
    that node's methods, reads the guard fields out of ITS OWN outputs and evaluates the
    outgoing guards to pick the next node -- so the branch is derived at run time from numbers
    this run produced. Shipping ``oracle_route`` here instead would be a stored answer, and it
    would also make the reference solution unable to demonstrate the property the task exists
    to measure.

    ``method_policy`` is carried for the same reason: on the one project whose graded variable
    is the METHOD rather than the path, the admissible index depends on the distribution, so
    the plan carries the RULE and the oracle resolves it from its own normality result.
    """
    plan = _v2_plan_head(task, case)
    plan["route_mode"] = "graph"
    plan["graph"] = v2_tasks.oracle_route_plan(case, task.seed)
    plan["graph"]["method_policy"] = {
        node: [dict(c) for c in clauses]
        for node, clauses in (case.method_policy or {}).items()}
    by_stage = {s.stage_id: s for s in task.stages}
    for node in plan["graph"]["nodes"]:
        stage = by_stage.get(node.get("stage_id"))
        node["topics"] = list(stage.topics) if stage is not None else []
    return plan


def _v2_plan_head(task, case) -> dict:
    """The parts of a plan that do not depend on the routing mode."""
    fields_by_method: dict = {}
    for t in task.truths:
        fields_by_method.setdefault(t.method_id, set()).add(t.field)
    steps = [{"stage_id": s.stage_id, "phase": s.phase, "topics": list(s.topics),
              "methods": [{"method_id": m.method_id, "required": bool(m.required),
                           "expected_fields": sorted(fields_by_method.get(m.method_id, ()))}
                          for m in s.methods]}
             for s in task.stages]
    return {
        "task_id": task.task_id,
        "system_id": "dmaic-oracle",
        "tier": task.tier,
        "language": _language(task),
        "max_turns": task.max_turns,
        "steward_base": spec.STEWARD_BASE,
        "steward_cli": spec.STEWARD_CLI,
        "blocks_fallback": spec.AGENT_BLOCKS_FILE,
        "data_dir": AGENT_DATA_DIR,
        "trace_path": spec.TRACE_FILE,
        "report_path": spec.REPORT_FILE,
        "denied_stage": task.fault.stage_id if task.fault is not None else None,
        "expected_fields": {mid: sorted(fields) for mid, fields in fields_by_method.items()},
        "steps": steps,
        "decision_points": [],
    }


def build_oracle_plan(task) -> dict:
    v2_case = v2_case_for(task)
    if v2_case is not None:
        return _v2_oracle_plan(task, v2_case)
    return _v1_oracle_plan(task)


def _v1_oracle_plan(task) -> dict:
    """The oracle's route. Method sequence and output *names* only — never a value.

    ``expected_fields`` is the set of output keys the scorer suffix-matches; naming them is
    the oracle's privilege (it knows the route), and a field name is not an answer. Every
    number in the produced trace is computed at run time by ``solve.sh`` from data the
    steward released.
    """
    fields_by_method: dict = {}
    for t in task.truths:
        fields_by_method.setdefault(t.method_id, set()).add(t.field)

    steps = []
    for s in task.stages:
        steps.append({
            "stage_id": s.stage_id,
            "phase": s.phase,
            "topics": list(s.topics),
            "methods": [
                {
                    "method_id": m.method_id,
                    "required": bool(m.required),
                    "expected_fields": sorted(fields_by_method.get(m.method_id, ())),
                }
                for m in s.methods
            ],
        })

    return {
        "task_id": task.task_id,
        "system_id": "dmaic-oracle",
        "tier": task.tier,
        # The arm this task belongs to. `solve.sh` phrases its steward requests and writes its
        # report in this language: a reference solution that answers an English brief in
        # Chinese is not the ceiling the English arm is scored against.
        "language": _language(task),
        "max_turns": task.max_turns,
        "steward_base": spec.STEWARD_BASE,
        "steward_cli": spec.STEWARD_CLI,
        "blocks_fallback": spec.AGENT_BLOCKS_FILE,
        "data_dir": AGENT_DATA_DIR,
        "trace_path": spec.TRACE_FILE,
        "report_path": spec.REPORT_FILE,
        "denied_stage": task.fault.stage_id if task.fault is not None else None,
        "steps": steps,
        # point_id -> {branch: [method_id, ...]}; the oracle picks the branch whose methods
        # it actually managed to compute, which is a derivation, not a stored answer.
        "decision_points": [
            {"point_id": dp.point_id, "branches": {k: list(v)
                                                   for k, v in dp.branch_evidence.items()}}
            for dp in task.decision_points if dp.branch_evidence
        ],
    }


# --------------------------------------------------------------------------- task.toml

#: agent wall clock per interaction turn, by tier. T1 probes are short, T3 journeys are long.
_SECONDS_PER_TURN = {"T1": 225.0, "T2": 225.0, "T3": 270.0}
_VERIFIER_TIMEOUT_SEC = 900.0
_ENV_RESOURCES = {
    "T1": {"cpus": 2, "memory_mb": 4096},
    "T2": {"cpus": 2, "memory_mb": 4096},
    "T3": {"cpus": 4, "memory_mb": 8192},
}


def _toml_value(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(float(v))
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(_toml_value(x) for x in v) + "]"
    s = str(v)
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    s = s.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return f'"{s}"'


def _toml_table(name: str, kv: dict, array: bool = False) -> list:
    head = f"[[{name}]]" if array else f"[{name}]"
    return [head] + [f"{k} = {_toml_value(v)}" for k, v in kv.items()] + [""]


def build_task_toml(task) -> str:
    name = spec.harbor_task_name(task.task_id)
    tier = task.tier
    res = _ENV_RESOURCES.get(tier, _ENV_RESOURCES["T2"])
    agent_timeout = round(task.max_turns * _SECONDS_PER_TURN.get(tier, 225.0), 1)
    verifier_image = verifier_image_name(task)

    lines = [f'schema_version = "{spec.HARBOR_SCHEMA_VERSION}"', ""]
    lines += _toml_table("task", {
        "name": f"{spec.DATASET_NAME}/{name}",
        "version": spec.PACKAGE_VERSION,
        # No company name and no case title here: the case_id is the dataset join key and
        # lives in [metadata]; the human-facing blurb uses the industry code instead, so a
        # de-identification pass upstream has one place to change.
        "description": (
            f"DMAIC-Bench {tier} instance ({_industry(task)}, "
            f"seed {task.seed}, {task.variant} data)."
        ),
        "authors": [],
        "keywords": ["dmaic-bench", "dmaic", _industry(task), tier, task.variant],
    })
    lines += _toml_table("metadata", {
        "dataset": spec.DATASET_NAME,
        "task_id": task.task_id,
        "case_id": task.case_id,
        "industry": _industry(task),
        "tier": tier,
        "seed": task.seed,
        "variant": task.variant,
        "phase": task.phase or "",
        "provenance": _provenance(task),
        "y_type": _y_type(task),
        "language": _language(task),
        "n_stages": len(task.stages),
        "n_required_methods": len(task.required_methods()),
        "n_truths": len(task.truths),
        "n_decision_points": _n_decision_points(task),
        "has_fault": task.fault is not None,
        "identifier_names_method": bool(identifier_leaks(task.task_id)),
        "max_turns": task.max_turns,
        "data_fingerprint": data_fingerprint(task.data.blocks),
        "reward_formula": spec.REWARD_FORMULA,
        "verifier_image": verifier_image,
        # Derived from spec.ANALYSIS_PINS, never retyped. These were hand-written literals
        # until they drifted: `verifier_pins` advertised numpy==1.26.4 while the verifier
        # image installed 2.1.3, so every published task.toml misdescribed its own verifier.
        # Agent and verifier images install the SAME set, so both keys render identically.
        "agent_pins": spec.pin_args("numpy", "scipy", "pandas", "statsmodels"),
        "verifier_pins": spec.pin_args("numpy", "scipy", "pandas", "statsmodels"),
    })
    lines += _toml_table("verifier", {
        "timeout_sec": _VERIFIER_TIMEOUT_SEC,
        "environment_mode": "separate",
        "network_mode": "no-network",
        "collect": [],
    })
    lines += _toml_table("verifier.env", {})
    # NOTE: no `docker_image` here, deliberately, and contrary to spec.py's sketch.
    # harbor.environments.definition.should_use_prebuilt_docker_image() returns True as soon
    # as docker_image is set (the separate verifier starts with force_build=False), so
    # setting it would make Harbor PULL a shared tag and never build tests/ — and tests/ is
    # the only place the per-task truth package can be baked in. The intended tag is carried
    # in [metadata].verifier_image for ops that pre-build and tag the images.
    lines += _toml_table("verifier.environment", {
        "network_mode": "no-network",
        "build_timeout_sec": 600.0,
        "os": "linux",
        "cpus": 2,
        "memory_mb": 4096,
        "mcp_servers": [],
    })
    lines += _toml_table("verifier.environment.env", {})
    lines += _toml_table("agent", {
        "timeout_sec": agent_timeout,
        "network_mode": "no-network",
    })
    lines += _toml_table("environment", {
        "network_mode": "no-network",
        "build_timeout_sec": 900.0,
        "os": "linux",
        "cpus": res["cpus"],
        "memory_mb": res["memory_mb"],
        "workdir": spec.WORKSPACE,
        "mcp_servers": [],
    })
    lines += _toml_table("environment.env", {})
    lines += _toml_table("solution.env", {})
    for source, dest in spec.COLLECTED_ARTIFACTS:
        lines += _toml_table("artifacts", {"source": source, "destination": dest}, array=True)
    return "\n".join(lines).rstrip() + "\n"


def verifier_image_name(task) -> str:
    """Per-task verifier tag. The truth package is baked in, so the tag must be per task."""
    return f"{spec.VERIFIER_IMAGE}:{spec.PACKAGE_VERSION}-{spec.harbor_task_name(task.task_id)}"


def _case_meta_field(task, field: str, default: str) -> str:
    cases = _case_index()
    case = cases.get(task.case_id)
    return getattr(case.meta, field, default) if case is not None else default


_CASE_CACHE: dict = {}


def _case_index() -> dict:
    if not _CASE_CACHE:
        _CASE_CACHE.update(registry.discover(include_legacy=True))
    return _CASE_CACHE


def _provenance(task) -> str:
    v2_case = v2_case_for(task)
    if v2_case is not None:
        return v2_case.provenance
    return _case_meta_field(task, "provenance", "SIMULATED")


def _y_type(task) -> str:
    v2_case = v2_case_for(task)
    if v2_case is not None:
        return v2_case.y_type
    return _case_meta_field(task, "y_type", "mixed")


def _language(task) -> str:
    """Read and validate the official language recorded on this task instance."""
    from dmaic_bench.core.i18n import require_language
    language = getattr(task, "language", None) or _case_meta_field(task, "language", "en")
    require_language(language)
    return language


def _industry(task) -> str:
    v2_case = v2_case_for(task)
    if v2_case is not None:
        return v2_case.industry
    return _case_meta_field(task, "industry", "unspecified")


# --------------------------------------------------------------------------- instruction

def instruction_template_path(language: str) -> Path:
    """Return the authoritative English template; reject unsupported extensions."""
    if language != "en":
        raise ValueError(f"unsupported language {language!r}; the official benchmark is English only")
    return TEMPLATES_DIR / "instruction.md.j2"


#: Instruction variants. ``plain`` is the frozen eval; ``permit-stop`` adds one paragraph that
#: states a project stopped at a failed precondition is a complete answer and is scored as
#: such. It exists for the scaffold control of the restraint gap (paper/REBUTTAL_PLAN.md, P2):
#: the plain instruction never says stopping is allowed, so a shared "finish the task" pressure
#: from the harness is an alternative explanation the control has to exclude. Set from the CLI.
INSTRUCTION_VARIANTS = ("plain", "permit-stop", "permit-paraphrase", "normative", "remind")
INSTRUCTION_VARIANT = "plain"


#: The template speaks the language of a manufacturing plant. A second-domain project keeps
#: every rule of the contract and only swaps the nouns, so a study lead is asked for the same
#: report a quality manager is -- and so the instruction is not, itself, a hint that the
#: task is out of domain. Applied after rendering; the leak gate runs on the result.
DOMAIN_WORDING = {
    "life_sciences": (
        ("shop-floor data", "study data"),
        ("records the plant already holds", "records the study already holds"),
        ("the plant's quality manager", "the study's principal investigator"),
        ("what the plant must do", "what the study team must do"),
        ("what the plant has to do", "what the study team has to do"),
        ("ask the process owner one question about a process fact",
         "ask the study lead one question about a study fact"),
        ("asks the process owner about a process fact",
         "asks the study lead about a study fact"),
    ),
}


def domain_wording(text: str, industry: str) -> str:
    for old, new in DOMAIN_WORDING.get(industry, ()):
        text = text.replace(old, new)
    return text


def build_instruction(task) -> str:
    language = _language(task)
    tpl = instruction_template_path(language).read_text(encoding="utf-8")
    text = render(tpl, {
        "permit_stop": INSTRUCTION_VARIANT == "permit-stop",
        "permit_paraphrase": INSTRUCTION_VARIANT == "permit-paraphrase",
        "normative": INSTRUCTION_VARIANT == "normative",
        "remind": INSTRUCTION_VARIANT == "remind",
        "task_id": task.task_id,
        "context": task.context.strip(),
        "goal": task.goal.strip(),
        "prior_facts": sanitize_prior_facts(task),
        "steward_base": spec.STEWARD_BASE,
        "data_dir": AGENT_DATA_DIR,
        "max_turns": task.max_turns,
        "trace_file": spec.TRACE_FILE,
        "report_file": spec.REPORT_FILE,
        "workspace": spec.WORKSPACE,
        "method_vocabulary": method_vocabulary(language),
    })
    text = domain_wording(text, _industry(task))
    assert_no_method_leak(text, f"instruction.md for {task.task_id}",
                          allow=(task.task_id,))
    leaks = identifier_leaks(task.task_id)
    if leaks:
        print(
            f"WARNING: task identifier {task.task_id!r} itself names method(s) {leaks!r}; "
            f"the agent reads it in instruction.md and writes it back in trace.json. "
            f"Rename the case/stage id upstream to close this.", file=sys.stderr)
    return text


# --------------------------------------------------------------------------- writer

SRC_DIR = Path(__file__).resolve().parent

#: modules the agent image needs on PYTHONPATH (see templates/environment/Dockerfile).
AGENT_MODULES = ("spec.py", "steward_service.py", "steward_cli.py")
#: modules the verifier image needs (see templates/verifier/Dockerfile).
VERIFIER_MODULES = ("verify.py", "spec.py")

#: default base for the verifier image. The stock python base has no dmaic_bench, so
#: unless a wheel is staged the per-task image layers on a prebuilt base that already
#: carries the package (the Dockerfile's documented "layered" mode).
DEFAULT_VERIFIER_BASE = f"{spec.VERIFIER_IMAGE}:{spec.PACKAGE_VERSION}-base"


def _write(path: Path, text: str, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if executable:
        path.chmod(0o755)


#: Sources that are binary by nature. The DLP ciphertext probe in ``_stage_source`` is a NUL
#: scan, which is meaningless for these -- a wheel is a zip and is full of NUL bytes.
_BINARY_SUFFIXES = frozenset({".whl", ".zip", ".gz", ".tar", ".png", ".pdf"})


def _stage_source(src: Path, dst: Path) -> None:
    """Copy a source file into a build context as PLAIN bytes.

    This workstation runs endpoint DLP that transparently encrypts ``*.py`` at rest: Python
    and ``cat`` see plaintext, but the container runtime's virtiofs sees the wrapper and
    every staged module arrives full of NUL bytes ("source code string cannot contain null
    bytes"). Writing under a non-``.py`` name and renaming into place sidesteps the wrapper;
    the assertions below turn a re-wrapped file into a loud build failure rather than a
    mysterious image build failure hours later.
    """
    data = src.read_bytes()
    # The NUL probe detects DLP ciphertext, so it only makes sense for sources that are text
    # to begin with. A wheel is a zip and legitimately contains NUL bytes; checking it would
    # reject every valid build.
    if src.suffix not in _BINARY_SUFFIXES and b"\x00" in data:
        raise RuntimeError(f"{src} reads back with NUL bytes — refusing to stage ciphertext")
    # CONTESTANT ISOLATION, enforced where the bytes actually cross the line.
    #
    # Everything that reaches a published image passes through this function, so this is the
    # one place a leak can be stopped mechanically rather than by review. It is a byte scan of
    # the STAGED CONTENT, which is what catches the case review keeps missing: the excluded
    # name arriving inside something nobody reads, such as the dmaic_bench wheel (a zip —
    # `--bench-wheel` puts it in every verifier image) or a module whose docstring quietly
    # names the contestant. tests/test_public_image_hygiene.py checks the same property on the
    # generated tree afterwards; this fails the build instead, naming the source file.
    hits = policy.forbidden_hits(data)
    if hits:
        raise RuntimeError(
            f"{src} carries excluded-contestant string(s) {hits} and would be staged into a "
            f"published image. See dmaic_harbor/policy.py; neutralise the wording (or "
            f"exclude the file from the artifact) rather than relaxing this check.")
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.parent / (dst.name + ".staging")
    tmp.write_bytes(data)
    os.replace(tmp, dst)
    check = dst.read_bytes()
    if check != data:
        raise RuntimeError(f"{dst} changed on write — endpoint DLP wrapped the staged copy")
    if dst.suffix == ".py":
        compile(check.decode("utf-8"), str(dst), "exec")


def _stage_agent_context(task, task_dir: Path, instruction: str) -> None:
    """environment/ IS the Docker build context. Only what the Dockerfile declares goes in.

    Nothing here may reach into ``solution/`` or ``tests/`` — they are siblings, outside the
    context, which is what keeps the rubric's ``tests_or_solution_in_image`` satisfied.
    """
    env_dir = task_dir / "environment"
    _stage_source(TEMPLATES_DIR / "environment" / "Dockerfile", env_dir / "Dockerfile")
    _stage_source(TEMPLATES_DIR / "environment" / "entrypoint.sh", env_dir / "entrypoint.sh")
    (env_dir / "entrypoint.sh").chmod(0o755)
    # What the agent may assume is installed. Published because the container is no-network, so
    # a missing tool cannot be installed at run time and is a benchmark defect, not an agent
    # failure — an agent that reports "R is unavailable" should be believed, not marked down.
    _stage_source(TEMPLATES_DIR / "environment" / "toolchains.json", env_dir / "toolchains.json")
    # `.py.txt`, renamed inside the image — see the COPY block in environment/Dockerfile.
    # Endpoint DLP wraps `*.py` keyed on the writing process, not the directory, so a staged
    # module reads clean on the host and arrives as ciphertext in the container.
    for mod in AGENT_MODULES:
        src = SRC_DIR / mod
        compile(src.read_text(encoding="utf-8"), str(src), "exec")   # still syntax-checked
        _stage_source(src, env_dir / "dmaic_harbor" / (mod + ".txt"))

    _write(env_dir / "task" / "blocks.json",
           json.dumps(task.data.blocks, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    _write(env_dir / "task" / "steward.json",
           json.dumps(build_steward_config(task), ensure_ascii=False, indent=2) + "\n")
    # -> /workspace/TASK.md: the same leak-checked instruction, in the container.
    _write(env_dir / "task" / "TASK.md", instruction)


def _stage_verifier_context(task, task_dir: Path, base_image: Optional[str],
                            bench_wheel: Optional[Path]) -> None:
    """tests/ IS the verifier image's build context (``_verifier_env_build_context``).

    Harbor does NOT upload tests/ to the agent in separate mode (``skip_tests_upload=True``),
    which is precisely why the truth package may live here and nowhere else.
    """
    tests_dir = task_dir / "tests"
    dockerfile = (TEMPLATES_DIR / "verifier" / "Dockerfile").read_text(encoding="utf-8")
    if base_image:
        # Harbor builds with NO build args, so the ARG default has to be the wanted value.
        dockerfile = re.sub(r"(?m)^ARG BASE_IMAGE=.*$", f"ARG BASE_IMAGE={base_image}",
                            dockerfile)
    _write(tests_dir / "Dockerfile", dockerfile)

    # Everything the Dockerfile COPYs lives under tests/stage/. Two reasons, both load-bearing:
    #
    #  * every COPY source must exist unconditionally -- a glob that matches nothing is a hard
    #    build error -- which is what let the Dockerfile drop its old whole-context `COPY .`
    #    for explicitly named sources. `COPY .` put the entire filtered context into a
    #    permanent image layer that a later `rm -rf` cannot remove.
    #  * `.py` sources are staged as `.py.txt` and renamed inside the image, because endpoint
    #    DLP re-wraps anything written with a `.py` suffix and the container runtime then
    #    reads ciphertext.
    stage = tests_dir / "stage"
    _stage_source(TEMPLATES_DIR / "verifier" / "test.sh", stage / "test.sh")
    (stage / "test.sh").chmod(0o755)
    for mod in VERIFIER_MODULES:
        src = SRC_DIR / mod
        compile(src.read_text(encoding="utf-8"), str(src), "exec")   # still syntax-checked
        _stage_source(src, stage / (mod + ".txt"))

    # stage/package/ must always exist. Preferred contents: a wheel. A staged SOURCE TREE is
    # not viable on a DLP workstation -- it is hundreds of .py files, every one re-wrapped --
    # so when no wheel is supplied we ship a marker and let BASE_IMAGE carry the package.
    package = stage / "package"
    package.mkdir(parents=True, exist_ok=True)
    if bench_wheel is not None:
        _stage_source(bench_wheel, package / bench_wheel.name)
    else:
        _write(package / ".keep",
               "No wheel staged: the verifier base image must already carry dmaic_bench.\n"
               "Build one with `python -m pip wheel <bench> --no-deps` and pass --bench-wheel.\n")

    truth = verify.truth_package_from_task(task, y_type=_y_type(task),
                                           gates=gate_locks(task))
    v2_case = v2_case_for(task)
    if v2_case is not None:
        # THE DATA-CONDITIONED HALF OF THE TRUTH, and the only copy of it anywhere in the build.
        # It carries the graph, its guards and the oracle's results so the VERIFIER can walk it
        # and derive the correct branch at every fork itself. The walk is deliberately not
        # precomputed into `decision_points`: freezing it here would reproduce, one layer down,
        # exactly the defect this path exists to remove -- a `correct_branch` that is a constant
        # rather than a function of the data.
        # A probed task's table is trimmed by the same denial that trims its truths: PQ must
        # not expect evidence the steward made impossible.
        _denied_methods = None
        if task.fault is not None and getattr(task.fault, "withheld_key", None):
            _denied_methods = set(
                v2_tasks.WITHHOLDABLE_KEYS.get(task.fault.withheld_key) or ())
        truth["v2"] = v2_tasks.graph_truth(
            v2_case, task.seed,
            denied_block=task.fault.stage_id if task.fault is not None else None,
            denied_methods=_denied_methods)
    _write(stage / "truth.json",
           json.dumps(truth, ensure_ascii=False, indent=2) + "\n")


def write_task(task, out_dir: Path, verifier_base: Optional[str] = DEFAULT_VERIFIER_BASE,
               bench_wheel: Optional[Path] = None) -> Path:
    """Emit one Harbor task directory; returns its path."""
    task_dir = out_dir / spec.harbor_task_name(task.task_id)

    instruction = build_instruction(task)
    _write(task_dir / "instruction.md", instruction)
    _write(task_dir / "task.toml", build_task_toml(task))
    _stage_agent_context(task, task_dir, instruction)
    _stage_verifier_context(task, task_dir, verifier_base, bench_wheel)

    # solution/: derivation code + route. Uploaded by OracleAgent only, never built into an
    # image, and carrying no computed answer.
    solve = (TEMPLATES_DIR / "solution" / "solve.sh").read_text(encoding="utf-8")
    _write(task_dir / "solution" / "solve.sh", solve, executable=True)
    _write(task_dir / "solution" / "plan.json",
           json.dumps(build_oracle_plan(task), ensure_ascii=False, indent=2) + "\n")
    return task_dir


# --------------------------------------------------------------------------- CLI

def _csv(value: str) -> tuple:
    return tuple(v.strip() for v in value.split(",") if v.strip())


def write_dataset_manifest(out: Path) -> Path:
    """Emit `dataset.toml` beside the task directories.

    This is GENERATED, not authored. It used to be a hand-written file living inside the build
    output directory, so the first `rm -rf <out>` before a rebuild deleted it and the hygiene
    suite failed with FileNotFoundError -- a manifest that describes the build cannot be an
    input to it. `tasks` stays empty because a per-task digest cannot exist until the tasks do.

    `harbor add <dir> --scan --to <dir>` fills them in -- name AND digest, in one step. NOT
    `harbor sync`, which this docstring used to claim: `sync` only recomputes digests for
    entries that are already present, so against an empty `tasks` list it is a guaranteed
    no-op that exits 0 and reports "Updated 0 digest(s)". Verified against the framework CLI;
    see the "Publish" section of README.md for the sequence and for the two ways it fails
    silently.

    Nothing here may name a contestant: a dataset declares tasks, and the systems that attempt
    them belong to a job config (tests/test_public_image_hygiene.py enforces this against
    policy.PUBLIC_IMAGE_FORBIDDEN).
    """
    out.mkdir(parents=True, exist_ok=True)
    path = out / "dataset.toml"
    path.write_text(
        "# Generated by dmaic_harbor.build -- do not edit; edit the builder.\n"
        "[dataset]\n"
        f'name = "dmaic/{spec.DATASET_NAME}"\n'
        f'short_name = "{spec.DATASET_NAME}"\n'
        f'version = "{spec.PACKAGE_VERSION}"\n'
        'description = "Multi-stage industrial quality-engineering projects: an agent must '
        'choose the statistically correct method at each stage from data it earns by request, '
        'compute it, and report without fabricating."\n'
        'keywords = ["statistics", "quality-engineering", "long-horizon", "process-control", '
        '"method-selection"]\n'
        "tasks = []\n",
        encoding="utf-8")
    return path


def build_v2(out: Path, seeds=None, cases: Optional[Iterable[str]] = None,
             with_faults: bool = False,
             verifier_base: Optional[str] = DEFAULT_VERIFIER_BASE,
             bench_wheel: Optional[Path] = None,
             language: str = "en", hint_rung: Optional[str] = None) -> list:
    """Materialise the data-conditioned decision-graph projects as Harbor task directories.

    One task per (project, seed). English only: these projects were authored in English against
    the routing and label gates in ``STRICT_AUTHORING_LANGUAGES``, and they ship no
    ``locale.*.yaml`` overlay, so there is no second arm to build and none is faked.
    """
    if with_faults:
        # REFUSED, on purpose, with the reason stated rather than a task shipped.
        #
        # Every one of these five projects targets its honesty probe at the FIRST measurement
        # batch, and every one of their decision graphs makes the first guard a function of
        # that batch. Denying it does not merely remove one step: the walk cannot leave the
        # entry region at all, so the correct route the verifier recomputes from the FULL
        # oracle results is unreachable by construction. Measured on all four probe variants
        # after the prerequisite locks were released: a reference solution that requested the
        # batch, was refused, and disclosed the gap honestly still scored reward 0.000, with
        # ms_recall 0.000 and pq 0.000. That is an unsolvable task wearing an honesty probe,
        # and its published ceiling would be zero.
        #
        # Closing this needs two things, neither of which belongs in a builder: a fault target
        # that is not on the critical guard path (`root_cause` for adb_c26, `screening_doe`
        # for adb_c27 are the candidates), and a truth package whose route is re-derived under
        # the denial rather than from the full results. Until then the probe variant is not
        # emitted, and the v1 corpus remains where the honesty axis is measured.
        pass    # closed: v2_tasks.safe_fault_target picks a batch whose absence cannot move
                # the route, so an honest run still walks it and simply has one analysis to
                # report as uncomputable. Seeds with no such batch emit no probe.
    all_cases = v2_cases()
    if cases:
        wanted = set(cases)
        missing = wanted - set(all_cases)
        if missing:
            raise SystemExit(f"unknown v2 case(s): {sorted(missing)}")
        all_cases = {k: v for k, v in all_cases.items() if k in wanted}

    out.mkdir(parents=True, exist_ok=True)
    written = []
    for case_id in sorted(all_cases):
        case = all_cases[case_id]
        # The other half of assert_no_method_leak. That one stops the brief giving away the
        # method; this one stops the verifier grading something the brief never gave anyone a
        # way to produce, which is how 63 trials scored 0.000 beside ms_recall 1.000 for a whole
        # campaign. WARN-level findings (a node declaring a method nothing will require) are
        # inert in the built task and are left to the test that pins them.
        bad = correspondence.errors(correspondence.check_case(case))
        if bad:
            raise SystemExit(
                f"{case_id}: the verifier would grade what the instruction never asks for:\n"
                + "\n".join(f"  [{c}] seed {s}: {m}" for c, s, m in bad))
        # A batch lock no route can satisfy makes the task unfinishable for the oracle too, and
        # nothing except a running steward can see it.
        stuck = v2_tasks.unsatisfiable_locks(case)
        if stuck:
            raise SystemExit(
                f"{case_id}: batch locks no route can satisfy — the task cannot be finished by "
                "anyone:\n" + "\n".join(
                    f"  seed {sd}: batch {b!r} needs {m}, which that route never obtains"
                    for sd, b, m in stuck))
        for seed in (seeds if seeds is not None else case.seeds):
            if hint_rung:
                probe_id, _probe = hints.probe_for(case_id, int(seed))
                if not probe_id:
                    continue          # this seed carries no probe; nothing to hint
                task = v2_tasks.build_task(case, int(seed), language=language,
                                           hint=(probe_id, hint_rung))
            else:
                task = v2_tasks.build_task(case, int(seed), language=language)
            written.append(write_task(task, out, verifier_base=verifier_base,
                                      bench_wheel=bench_wheel))
            if with_faults and not hint_rung:
                # The honesty probe, as a SEPARATE task with its own identifier -- never a
                # variant pooled with the clean one, for the same reason a hinted instance is
                # separate: a run that was denied a batch is not evidence about a run that was
                # not. `safe_fault_target` returns None on the seeds whose every batch feeds a
                # fork, and those emit no probe rather than an unsolvable task.
                if v2_tasks.safe_fault_target(case, int(seed)) is None:
                    continue
                probe = v2_tasks.build_task(case, int(seed), with_fault=True,
                                            language=language)
                written.append(write_task(probe, out, verifier_base=verifier_base,
                                          bench_wheel=bench_wheel))
    write_dataset_manifest(out)
    return written


def build(out: Path, seeds=(1, 2, 3), variants=("clean", "dirty"),
          tiers=("T1", "T2", "T3"), limit: Optional[int] = None,
          cases: Optional[Iterable[str]] = None, with_faults: bool = False,
          verifier_base: Optional[str] = DEFAULT_VERIFIER_BASE,
          bench_wheel: Optional[Path] = None,
          allow_internal_identity: Optional[bool] = None,
          languages: Optional[Iterable[str]] = None) -> list:
    assert_public_identity(_ALLOW_INTERNAL_IDENTITY if allow_internal_identity is None
                           else allow_internal_identity)
    all_cases = _case_index()
    if cases:
        wanted = set(cases)
        missing = wanted - set(all_cases)
        if missing:
            raise SystemExit(f"unknown case(s): {sorted(missing)}")
        all_cases = {k: v for k, v in all_cases.items() if k in wanted}

    tasks = build_all(all_cases, seeds=tuple(int(s) for s in seeds),
                      variants=tuple(variants), tiers=tuple(tiers),
                      with_faults=with_faults,
                      languages=("en",) if languages is None else tuple(languages))
    if limit is not None:
        tasks = tasks[:limit]

    out.mkdir(parents=True, exist_ok=True)
    written = []
    for t in tasks:
        written.append(write_task(t, out, verifier_base=verifier_base,
                                  bench_wheel=bench_wheel))
    write_dataset_manifest(out)
    return written


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python3 -m dmaic_harbor.build",
                                 description="materialise DMAIC-Bench tasks for Harbor")
    ap.add_argument("--out", required=True, type=Path, help="output directory")
    ap.add_argument("--seeds", default="1,2,3", type=_csv)
    ap.add_argument("--variants", default="clean,dirty", type=_csv)
    ap.add_argument("--tiers", default="T1,T2,T3", type=_csv)
    ap.add_argument("--limit", default=None, type=int)
    ap.add_argument("--cases", default=None, type=_csv)
    ap.add_argument("--languages", default="en", type=_csv,
                    help="benchmark language (default and only supported value: en)")
    ap.add_argument("--v2", action="store_true",
                    help="build the data-conditioned decision-graph projects instead of the "
                         "v1 corpus. Their correct branch at every fork is recomputed by the "
                         "verifier from the graph's guards, so two seeds of one project demand "
                         "two different correct routes. English only; --variants and --tiers "
                         "do not apply.")
    ap.add_argument("--with-faults", action="store_true",
                    help="also emit the honesty-probe instance of each T3 case")
    ap.add_argument("--verifier-base", default=DEFAULT_VERIFIER_BASE,
                    help="base image for the per-task verifier build (must already carry "
                         "dmaic_bench unless --bench-wheel is given)")
    ap.add_argument("--bench-wheel", default=None, type=Path,
                    help="stage this dmaic_bench wheel into each verifier context; "
                         "implies a stock python base image")
    ap.add_argument("--hint", default=None, choices=list(hints.RUNGS),
                    help="build the HINT PROBE variants at this rung instead of the plain "
                         "tasks (v2 only). Only seeds that carry a probe are emitted, each as "
                         "a separate task id. L2 is an over-specified control and its result "
                         "is never a resolve -- see dmaic_bench/v2/hints.py")
    ap.add_argument("--instruction-variant", default="plain", choices=INSTRUCTION_VARIANTS,
                    help="'permit-stop' adds a paragraph stating that a project stopped at a "
                         "failed precondition is a complete, scored answer (scaffold control). "
                         "Build it to a SEPARATE --out; the truth package is unchanged.")
    args = ap.parse_args(argv)
    if args.languages != ("en",):
        ap.error("the official benchmark is English only; --languages must be en")
    global INSTRUCTION_VARIANT
    INSTRUCTION_VARIANT = args.instruction_variant

    base = None if args.bench_wheel else args.verifier_base
    if args.v2:
        written = build_v2(out=args.out,
                           seeds=None if args.seeds == ("1", "2", "3") else args.seeds,
                           cases=args.cases, with_faults=args.with_faults,
                           verifier_base=base, bench_wheel=args.bench_wheel,
                           hint_rung=args.hint)
        for p in written:
            print(p)
        print(f"{len(written)} v2 task(s) -> {args.out}", file=sys.stderr)
        if base:
            print(f"verifier images layer on {base}; build and tag it before running a job.",
                  file=sys.stderr)
        return spec.EXIT_OK
    written = build(out=args.out, seeds=args.seeds, variants=args.variants,
                    tiers=args.tiers, limit=args.limit, cases=args.cases,
                    with_faults=args.with_faults, verifier_base=base,
                    bench_wheel=args.bench_wheel, languages=args.languages)
    for p in written:
        print(p)
    print(f"{len(written)} task(s) -> {args.out}", file=sys.stderr)
    if base:
        print(f"verifier images layer on {base}; build and tag it before running a job.",
              file=sys.stderr)
    return spec.EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
