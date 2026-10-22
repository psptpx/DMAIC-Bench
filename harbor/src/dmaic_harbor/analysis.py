"""Reporting layers that sit beside the reward: difficulty tier, ECR-TSR gap, citation rate.

None of these change ``reward``. They exist because a single scalar hides three things the
campaign data says are true and separable.

**Difficulty tier.** Pooling every task into one mean hid a monotone ladder. Splitting by what
the data asks of the route -- proceed, divert, or stop -- separates 0.749 / 0.530 / 0.337 with
zero-rates of 3% / 17% / 61%. The tier is derived from the seed's ``shape``, never authored, so
a task cannot be filed under the wrong difficulty by hand.

**ECR - TSR.** SOP-Bench's sharpest discriminator is that a system almost always reports having
finished and is often wrong (ECR near 1.00 against TSR 0.27). The same gap is present here and
is worth reporting because the reward alone cannot show it. The gap depends on where the success
bar sits, so ``ecr_tsr`` returns it at several bars rather than at one flattering one.

**Citation rate.** What fraction of the values a system computed actually appear in its report.
Measured across the campaign this discriminates between systems far more sharply than the reward
does (between-model sd 0.151 against 0.040) while being almost independent of correctness
(trial-level r = +0.10). That combination is the argument for reporting it and against gating
it: it is a real and separate quality, not a proxy for getting the analysis right.
"""
from __future__ import annotations

import json
import os
import re

#: The keyword heuristic this module started with. It is kept ONLY as the fallback for run
#: records whose shape label predates the table below; it is not the definition of a tier and
#: must not be extended. A keyword list over free-text labels fails silently by design: a case
#: whose author wrote "tester-unacceptable" instead of "gauge-unacceptable" matched nothing and
#: fell through to A-proceed. Measured when the corpus grew from 40 tasks to 95: it put 20 of
#: the 33 stop-tier tasks in the proceed tier, which understates the hardest tier -- the one
#: number the difficulty claim rests on -- by nearly two thirds.
STOP_SHAPES = ("gauge-unacceptable", "appraiser-disagreement")
DIVERT_SHAPES = ("unstable", "out-of-control")

#: shape label -> tier, derived from each shipped seed's ORACLE ROUTE by
#: :func:`tier_of_route` and pinned here so campaign analysis needs only the label a run record
#: already carries. Regenerated deliberately; `tests/test_tier_classification.py` fails if it
#: drifts from the routes, and if any shipped shape is missing from it.
_SHAPE_TIERS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "shape_tiers.json")
with open(_SHAPE_TIERS_PATH, encoding="utf-8") as _fh:
    _SHAPE_TIERS = json.load(_fh)

TIER_A = "A-proceed"    # prerequisites hold -> run the standard route
TIER_B = "B-divert"     # a prerequisite fails -> divert to special-cause work
TIER_C = "C-stop"       # a prerequisite fails -> terminate and remediate


def divert_targets(graph) -> set:
    """The nodes a fork routes to when a stability check FAILS.

    Found from the guards rather than from node names: for every fork with an outgoing guard
    that reads an ``outOfControl`` field, evaluate that fork with the field set to zero -- an
    in-control run -- and whichever edge is satisfied is the PROCEED branch. Every other target
    of that fork is a divert. Reading it this way rather than "the default edge is the divert"
    matters because the corpus writes the fork both ways round: most cases guard the proceed
    edge and default to special-cause work, and ``adb_c38`` guards ``outOfControl > 0`` and
    defaults to proceeding.
    """
    from dmaic_bench.core.graph import evaluate

    out = set()
    for node in graph.nodes:
        edges = list(graph.edges_from(node.key))
        stability = [e for e in edges if "outOfControl" in (e.when or "")]
        if not stability:
            continue
        in_control: dict = {}
        for edge in stability:
            for field in edge.guard_fields or ():
                cur, parts = in_control, field.split(".")
                for part in parts[:-1]:
                    cur = cur.setdefault(part, {})
                cur[parts[-1]] = 0
        proceed = next((e.target for e in edges if e.when and evaluate(e.when, in_control)), None)
        if proceed is None:
            proceed = next((e.target for e in edges if e.is_default), None)
        # A divert is where the fork goes when the stability check FAILS: the other stability
        # edge, or the default edge (most cases guard the proceed edge and default to
        # special-cause work). A fork can also carry guarded edges that have nothing to do with
        # control -- adb_c38's M_pchart routes a run already at the committed level straight to
        # C_control -- and counting those made two ordinary proceed seeds B-divert (2026-09-18
        # review). Those edges are neither stability edges nor the default, so they are skipped.
        candidates = stability + [e for e in edges if e.is_default]
        out |= {e.target for e in candidates if e.target != proceed}
    return out


def tier_of_route(graph, route) -> str:
    """**The definition.** Which kind of routing decision this seed's data forced.

    C-stop   the route never reaches a control plan -- a prerequisite failed and the project
             terminates or goes back
    B-divert it reaches one, but through the branch a failed stability check opens
    A-proceed it reaches one having done the assessment

    Structural, so a case cannot land in the wrong tier by how its author worded a label.
    Reproduces the hand-classified tier of all 40 tasks that predate it, exactly.
    """
    if not (set(route) & {n.key for n in graph.nodes if getattr(n, "phase", "") == "control"}):
        return TIER_C
    return TIER_B if (set(route) & divert_targets(graph)) else TIER_A


def tier_of(shape: str) -> str:
    """The tier of a run record, from the shape label it carries.

    A lookup into :data:`_SHAPE_TIERS`, which :func:`tier_of_route` produced. The keyword
    fallback below applies only to labels from before that table existed.
    """
    key = str(shape or "")
    if key in _SHAPE_TIERS:
        return _SHAPE_TIERS[key]
    if any(k in key for k in STOP_SHAPES):
        return TIER_C
    if any(k in key for k in DIVERT_SHAPES):
        return TIER_B
    return TIER_A


def _numbers(text: str) -> set:
    return set(re.findall(r"-?\d+\.?\d*", text))


def _renderings(value) -> set:
    """Plausible ways a report might print a computed value, including percent-scaled."""
    try:
        f = float(value)
    except (TypeError, ValueError):
        return set()
    out = set()
    for scale in (1.0, 100.0):
        g = f * scale
        for places in (0, 1, 2, 3, 4):
            s = "%.*f" % (places, g)
            out.add(s)
            if "." in s:
                out.add(s.rstrip("0").rstrip("."))
    return out


def _scalars(node, sink) -> None:
    if isinstance(node, dict):
        for v in node.values():
            _scalars(v, sink)
    elif isinstance(node, list):
        for v in node:
            _scalars(v, sink)
    elif isinstance(node, (int, float)) and not isinstance(node, bool):
        sink.append(node)


def citation_rate(trace: dict, report_text: str):
    """Fraction of the values the system COMPUTED that it also printed in its report.

    ``None`` when the run computed nothing -- an empty denominator is not a perfect score, the
    same rule the reward axes follow.
    """
    computed = []
    for step in (trace or {}).get("steps", ()):
        if step.get("status") == "success":
            _scalars(step.get("outputs", {}), computed)
    if not computed:
        return None
    tokens = _numbers(report_text or "")
    hit = sum(1 for v in computed if _renderings(v) & tokens)
    return hit / len(computed)


def claimed_complete(audit_lines, report_bytes: int) -> bool:
    """The ECR side: the system declared a verdict AND filed a report.

    Read from the steward's own append-only ledger, not from the contestant's prose, so this is
    a fact about what it did rather than a reading of what it said.
    """
    if not report_bytes:
        return False
    for line in audit_lines or ():
        try:
            entry = json.loads(line) if isinstance(line, str) else line
        except ValueError:
            continue
        if entry.get("action") == "declare":
            return True
    return False


def ecr_tsr(rewards, claims, bars=(0.999, 0.8, 0.6)) -> dict:
    """Self-claimed completion against actual success, at several success bars.

    The gap is highly sensitive to the bar -- on the campaign data it runs from +0.81 at "fully
    correct" down to roughly zero at 0.6 -- so a single headline number here would be a choice
    of flattering threshold rather than a measurement. All bars are returned.
    """
    n = len(rewards)
    if not n:
        return {"n": 0}
    ecr = sum(1 for c in claims if c) / n
    out = {"n": n, "ecr": ecr, "tsr": {}, "gap": {}}
    for bar in bars:
        tsr = sum(1 for r in rewards if r >= bar) / n
        out["tsr"][str(bar)] = tsr
        out["gap"][str(bar)] = ecr - tsr
    return out


def by_tier(rewards_by_task: dict, tiers: dict) -> dict:
    """Mean reward and zero-rate per difficulty tier."""
    out = {}
    for tier in (TIER_A, TIER_B, TIER_C):
        vals = [r for t, r in rewards_by_task.items() if tiers.get(t) == tier]
        if not vals:
            continue
        out[tier] = {"n": len(vals), "mean": sum(vals) / len(vals),
                     "zero_rate": sum(1 for v in vals if v <= 0.001) / len(vals)}
    return out
