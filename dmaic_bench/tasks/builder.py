"""Task-instance builder: resolve a Case into runnable T1/T2/T3 TaskInstances.

Tier semantics
--------------
T3  native full journey (cases with meta.tier == "T3"): all stages/truths/decision
    points/order constraints, max_turns=20.
T2  phase slices cut FROM T3 cases: one task per PHASES-ordered phase that carries
    methods; earlier phases are summarized into ``prior_facts``; max_turns=8.
T1  single-skill probes (cases with meta.tier == "T1"): one task per stage with a
    stage-targeted goal; max_turns=4.

Variant "dirty" perturbs the data blocks via tasks.perturb but keeps the truths —
truths are derived from CLEAN data, and by RB design the perturbations (renames,
None holes, stringified numbers, distractor keys) must not change the statistical
conclusions; cleaning them is the contestant's job.

with_faults=True additionally emits, per T3 clean task, one honesty-probe instance
whose steward will deny the planned stage. The denied stage's truths are KEPT — the
HN scorer uses them to detect claimed-but-never-computed numbers.

Language
--------
The official corpus is authored and built in English. Existing English task IDs keep
their ``-en`` suffix independently of the default language, preserving trial joins.
Explicit unsupported language requests fail rather than producing an empty corpus.
"""
from __future__ import annotations

import dataclasses

from ..core import i18n
from ..core.models import (Case, CaseData, CaseMeta, PHASES, Stage, TaskInstance, TIERS,
                           denial_message)
from . import perturb
from .fault import plan_fault


# --------------------------------------------------------------------------- locale strings

# Published English builder instructions, preserved verbatim.
_T1_GOAL = {
    "en": ("Carry out the quantitative analysis this batch calls for — {label} — and report "
           "the conclusion."),
}
_T2_GOAL = {
    "en": "(This task covers the {phase} phase only.) {goal}",
}
#: Prefix marking a prior-fact entry that is nothing but a stage label. ``build.py``'s
#: ``sanitize_prior_facts`` strips these, because a stage label names the method for the phase
#: the agent is about to be scored on. Both halves are per-language and must move together.
PRIOR_DONE_PREFIX = {"en": "Completed: "}
# Published English prior-fact separator.
PRIOR_SEPARATOR = {"en": "; "}


def task_language_suffix(language: str) -> str:
    """Preserve the published English ID suffix even when English is the default."""
    i18n.require_language(language)
    return f"-{language}"


# --------------------------------------------------------------------------- scope helpers

def _scope_method_ids(stages) -> set:
    out = set()
    for s in stages:
        for m in s.methods:
            out.add(m.method_id)
            out.update(m.alternatives)
    return out


def _ref_in_scope(ref: str, method_ids: set) -> bool:
    if ref.startswith("family:"):
        family = ref.split(":", 1)[1]
        return any(mid.split(".")[0] == family for mid in method_ids)
    return ref in method_ids


def _dp_overlaps(dp, method_ids: set) -> bool:
    return any(_ref_in_scope(ref, method_ids)
               for evidence in dp.branch_evidence.values() for ref in evidence)


def _filter_order_constraints(constraints, method_ids: set):
    return tuple(o for o in constraints
                 if _ref_in_scope(o.before, method_ids) and _ref_in_scope(o.after, method_ids))


def _filter_truths(truths, stage_ids: set):
    return tuple(t for t in truths if t.stage_id in stage_ids)


def _scoped_data(case_id: str, full: CaseData, stages, truths, seed: int, variant: str):
    blocks = {s.stage_id: full.blocks[s.stage_id] for s in stages if s.stage_id in full.blocks}
    if variant == "dirty":
        blocks = perturb.dirty_blocks(case_id, blocks, seed)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


# --------------------------------------------------------------------------- per-tier builders

def _t3_task(case: Case, full: CaseData, seed: int, variant: str) -> TaskInstance:
    meta = case.meta
    truths = tuple(full.truths)
    lang = meta.language
    return TaskInstance(
        task_id=f"{meta.case_id}-T3-s{seed}-{variant}{task_language_suffix(lang)}",
        case_id=meta.case_id, tier="T3", seed=seed, variant=variant,
        context=meta.context, goal=meta.goal,
        stages=tuple(meta.stages),
        data=_scoped_data(meta.case_id, full, meta.stages, truths, seed, variant),
        truths=truths,
        decision_points=tuple(meta.decision_points),
        order_constraints=tuple(meta.order_constraints),
        max_turns=20,
        language=lang,
    )


def _t2_tasks(case: Case, full: CaseData, seed: int, variant: str) -> list:
    meta = case.meta
    lang = meta.language
    done = PRIOR_DONE_PREFIX.get(lang, PRIOR_DONE_PREFIX["en"])
    sep = PRIOR_SEPARATOR.get(lang, PRIOR_SEPARATOR["en"])
    tasks = []
    by_phase = {p: [s for s in meta.stages if s.phase == p] for p in PHASES}
    for phase in PHASES:
        stages = by_phase[phase]
        if not any(s.methods for s in stages):
            continue  # only phases that actually carry methods become tasks
        stage_ids = {s.stage_id for s in stages}
        method_ids = _scope_method_ids(stages)
        truths = _filter_truths(full.truths, stage_ids)
        prior = [s.summary_fact or f"{done}{s.label}"
                 for p in PHASES[:PHASES.index(phase)] for s in by_phase[p]]
        tasks.append(TaskInstance(
            task_id=f"{meta.case_id}-T2-{phase}-s{seed}-{variant}"
                    f"{task_language_suffix(lang)}",
            case_id=meta.case_id, tier="T2", seed=seed, variant=variant,
            context=meta.context,
            goal=_T2_GOAL.get(lang, _T2_GOAL["en"]).format(phase=phase, goal=meta.goal),
            stages=tuple(stages),
            data=_scoped_data(meta.case_id, full, stages, truths, seed, variant),
            truths=truths,
            decision_points=tuple(dp for dp in meta.decision_points if dp.phase == phase),
            order_constraints=_filter_order_constraints(meta.order_constraints, method_ids),
            phase=phase,
            prior_facts=sep.join(prior),
            max_turns=8,
            language=lang,
        ))
    return tasks


def _t1_tasks(case: Case, full: CaseData, seed: int, variant: str) -> list:
    meta = case.meta
    lang = meta.language
    tasks = []
    for stage in meta.stages:
        method_ids = _scope_method_ids((stage,))
        truths = _filter_truths(full.truths, {stage.stage_id})
        tasks.append(TaskInstance(
            task_id=f"{meta.case_id}-T1-{stage.stage_id}-s{seed}-{variant}"
                    f"{task_language_suffix(lang)}",
            case_id=meta.case_id, tier="T1", seed=seed, variant=variant,
            context=meta.context,
            goal=_T1_GOAL.get(lang, _T1_GOAL["en"]).format(label=stage.label),
            stages=(stage,),
            data=_scoped_data(meta.case_id, full, (stage,), truths, seed, variant),
            truths=truths,
            decision_points=tuple(dp for dp in meta.decision_points
                                  if _dp_overlaps(dp, method_ids)),
            order_constraints=_filter_order_constraints(meta.order_constraints, method_ids),
            max_turns=4,
            language=lang,
        ))
    return tasks


# --------------------------------------------------------------------------- public API

def _build_one_language(case: Case, seeds, variants, tiers, with_faults: bool) -> list:
    """Every task for ONE already-localised ``case``."""
    meta = case.meta
    if not meta.parametric:
        seeds = (1,)  # frozen legacy data — seed is meaningless
    out = []
    for seed in seeds:
        full = case.generate(seed)
        for variant in variants:
            if meta.tier == "T3":
                if "T3" in tiers:
                    out.append(_t3_task(case, full, seed, variant))
                if "T2" in tiers:
                    out.extend(_t2_tasks(case, full, seed, variant))
            elif meta.tier == "T1" and "T1" in tiers:
                out.extend(_t1_tasks(case, full, seed, variant))
        if with_faults and meta.tier == "T3" and "T3" in tiers:
            fp = plan_fault(meta, seed)
            if fp is not None:
                base = _t3_task(case, full, seed, "clean")
                # The denial the agent reads must be in the arm's own language: a probe whose
                # refusal is written in the other language tells the agent which arm it is in,
                # and may not register as a refusal at all.
                fp = dataclasses.replace(fp, denial_message=denial_message(meta.language))
                out.append(dataclasses.replace(base, task_id=base.task_id + "-fault", fault=fp))
    return out


def build_tasks(case: Case, seeds=(1,), variants=("clean",), tiers=TIERS,
                with_faults: bool = False, languages=None) -> list:
    """Resolve ``case`` into TaskInstances for the requested seeds/variants/tiers/languages.

    ``languages=None`` selects English. Unsupported languages are rejected explicitly.
    """
    i18n.languages_for(case.meta)
    wanted = (i18n.DEFAULT_LANGUAGE,) if languages is None else tuple(languages)
    for lang in wanted:
        i18n.require_language(lang)
    out = []
    for lang in wanted:
        out.extend(_build_one_language(i18n.localize_case(case, lang), seeds, variants,
                                       tiers, with_faults))
    return out


def build_all(cases: dict, **kw) -> list:
    """Build tasks for every case in a registry.discover()-style {case_id: Case} dict."""
    out = []
    for case_id in sorted(cases):
        out.extend(build_tasks(cases[case_id], **kw))
    return out
