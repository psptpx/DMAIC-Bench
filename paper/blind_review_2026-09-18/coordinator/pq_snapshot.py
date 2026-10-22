"""PQ — Process Quality: did the system take the textbook-correct route in the right order?

Decision points prefer the trace's explicit route_decisions; systems that don't emit them are
judged by branch_evidence inference — which branch's evidence methods actually succeeded.
Walking any wrong branch is incorrect even if the correct one was also walked (running the
forbidden parametric test "as well" is exactly the failure mode the point exists to catch).
A point with no signal at all is "unknown": it stays in the denominator, because silence about
a mandatory checkpoint is not process quality.

Order constraints are partial-order prerequisites over SUCCESSFUL steps (a failed prerequisite
established nothing): violated when `after` happens before `before`, or happens while `before`
never does. Neither appearing is vacuously satisfied.
"""
from __future__ import annotations


def _family_of(method_id, taxonomy):
    return taxonomy.get(method_id).family if method_id in taxonomy else None


def _evidence_hit(item, successful, taxonomy) -> bool:
    if item.startswith("family:"):
        fam = item.split(":", 1)[1]
        return any(_family_of(m, taxonomy) == fam for m in successful)
    return item in successful


def _judge_point(point, trace, successful, taxonomy):
    """Judge one decision point. A DECLARATION IS NOT A DECISION.

    `route_decisions` is written by the contestant, so an earlier version of this function --
    which returned on the declaration before looking at any evidence -- let a trace that
    executed NOTHING score every point correct by naming the textbook branch. Measured on the
    shipped verifier: a trace with all steps `status: failed` and no outputs scored pq = 1.000.
    Parametric knowledge of what the answer usually is was worth a perfect process score.

    So a declaration now has to be CORROBORATED: the branch it names must also show up in the
    evidence, where the point declares evidence for it. Two honest limits are kept explicit
    rather than papered over. A point that declares no `branch_evidence` for the chosen branch
    cannot be corroborated either way, so the declaration stands and the reason says so. And
    walking a wrong branch is still incorrect even when the right one was also walked and
    declared -- running the inadmissible analysis is the error, not failing to mention it.
    """
    ok_branches = {point.correct_branch, *point.acceptable_branches}
    evidence = point.branch_evidence or {}
    walked = {branch for branch, items in evidence.items()
              if any(_evidence_hit(i, successful, taxonomy) for i in items)}

    explicit = [r for r in trace.route_decisions if r.point == point.point_id]
    if explicit:
        # Last explicit decision wins — a system may legitimately revise its route.
        chosen = explicit[-1].chosen_branch
        if chosen not in ok_branches:
            return "incorrect", "explicit"
        if walked - ok_branches:
            # Declared the right branch, but an inadmissible one was actually executed.
            return "incorrect", "explicit_contradicted"
        if chosen in evidence and chosen not in walked:
            # The point knows what taking this branch looks like, and none of it happened.
            return "incorrect", "declared_unsupported"
        return "correct", ("explicit_corroborated" if chosen in walked
                           else "explicit_uncorroboratable")

    if walked - ok_branches:
        return "incorrect", "evidence"
    if walked:
        return "correct", "evidence"

    # A correct branch can be a TERMINAL node -- "stop and repair the gauge", "re-train the
    # appraisers" -- which by definition runs no analysis. `branch_evidence` therefore holds no
    # signature for it (an empty list is dropped, not stored), so nothing can ever be walked to
    # prove it was taken, while every INADMISSIBLE alternative does carry a signature. Both
    # directions then scored zero: pressing on regardless was "incorrect" via the clause above,
    # and correctly declining was indistinguishable from silence and fell through to "unknown".
    # The point could not be passed by any contestant. Measured on the shipped verifier across
    # 7 models x 9 prerequisite-blocked tasks: reward 0.000 on all 63, with ms_recall 1.000,
    # nf 1.000, gate_hard_passed 1 and ms_misuse 0.000 sitting beside the zero.
    #
    # Taking such a branch is observable only as ABSTENTION, and only where abstention actually
    # discriminates: some alternative must carry a signature, the fork's own diagnostic must
    # have run -- so the agent established the blocking condition rather than merely doing
    # nothing -- and no alternative may have been walked (guaranteed here, `walked` is empty).
    # This is judged on behaviour alone: `point_id` is a private graph key the task instruction
    # never exposes, so no contestant can be asked to name the fork.
    if point.correct_branch not in evidence:
        diagnostic_ran = any(_evidence_hit(i, successful, taxonomy)
                             for i in (getattr(point, "source_evidence", None) or ()))
        # Prefer the SUBTREE test: it still discriminates on a fork where the immediate-target
        # uniqueness filter leaves both sides blank, which is exactly the fork that matters here
        # (correct branch terminal, wrong branch running a chart that recurs downstream).
        divergent = getattr(point, "divergent_evidence", None) or ()
        convergent = getattr(point, "convergent_evidence", None) or ()
        ran_divergent = any(_evidence_hit(i, successful, taxonomy) for i in divergent)
        ran_convergent = any(_evidence_hit(i, successful, taxonomy) for i in convergent)

        # Running work that only exists past a branch you were not to take is proof of the wrong
        # turn; running work that only exists past the correct one is proof of the right turn.
        if ran_divergent:
            return "incorrect", "divergent_evidence"
        if ran_convergent:
            return "correct", "convergent_evidence"

        # Neither side left a trace. If the correct branch is genuinely terminal -- a remediation
        # node that runs nothing -- then abstention IS the compliant act, provided the fork's own
        # diagnostic established the blocking condition. If instead the correct branch had work
        # to show and none of it happened, the agent stopped where it should have continued, and
        # crediting abstention there would pass exactly the wrong behaviour.
        if not convergent:
            if diagnostic_ran:
                return "correct", "abstention_corroborated"
            return "unknown", "none"
        if diagnostic_ran:
            return "incorrect", "abstained_from_required_branch"

    return "unknown", "none"


def _first_index(spec, trace, taxonomy):
    """Index of the first SUCCESSFUL step matching a method_id or "family:<fam>" spec."""
    fam = spec.split(":", 1)[1] if spec.startswith("family:") else None
    for i, step in enumerate(trace.steps):
        if step.status != "success":
            continue
        if fam is not None:
            if _family_of(step.method_id, taxonomy) == fam:
                return i
        elif step.method_id == spec:
            return i
    return None


def score(task, trace, taxonomy) -> dict:
    successful = trace.successful_methods()
    details = []

    points_correct = points_unknown = 0
    for p in task.decision_points:
        verdict, via = _judge_point(p, trace, successful, taxonomy)
        points_correct += verdict == "correct"
        points_unknown += verdict == "unknown"
        details.append({"kind": "decision_point", "point_id": p.point_id,
                        "verdict": verdict, "via": via})

    order_violations = 0
    for c in task.order_constraints:
        before_i = _first_index(c.before, trace, taxonomy)
        after_i = _first_index(c.after, trace, taxonomy)
        violated = after_i is not None and (before_i is None or after_i < before_i)
        order_violations += violated
        details.append({"kind": "order", "before": c.before, "after": c.after,
                        "violated": violated})

    total_points = len(task.decision_points)
    total_order = len(task.order_constraints)
    denom = total_points + total_order
    value = (points_correct + (total_order - order_violations)) / denom if denom else 1.0

    return {
        "points_total": total_points,
        "points_correct": points_correct,
        "points_unknown": points_unknown,
        "order_total": total_order,
        "order_violations": order_violations,
        "score": value,
        "details": details,
    }
