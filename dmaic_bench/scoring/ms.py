"""MS — Method Selection.

Recall: did the system run every required method (or a case-blessed alternative)?
Precision: of everything it attempted, how much was relevant to this case?
Misuse: attempts that are not merely irrelevant but data-type-incompatible with the case's y —
the "ran a t-test on defect counts" class of error, judged against the taxonomy.

The relevant set is deliberately generous: all stage methods (required or not), all declared
alternatives, plus the always-defensible diagnostic trio (profiling / normality / descriptive) —
exploring the data is never an act of imprecision.
"""
from __future__ import annotations

# Diagnostic methods that are legitimate on ANY case, so never count against precision.
#
# The principle, stated because the boundary is a judgement and the list will be argued about:
# a method that CHECKS AN ASSUMPTION is exempt; a method that ASSERTS A FINDING is not. Looking
# at your data, testing it for normality, testing a series for a non-random pattern and testing
# groups for equal spread are all things a competent analyst does before choosing what to
# conclude, and none of them concludes anything. Comparing two means, fitting a regression or
# running an ANOVA does conclude something, and doing it where the decision did not call for it
# is exactly the imprecision this axis exists to measure.
#
# Measured on a 95-trial campaign: precision is the smallest of the four averaged axes in 47% of
# trials — so it drives the harmonic mean more than any other — while `method_spam` is the FIRST
# cause of failure in only 6 of 93 failed trials. An axis with that much leverage and that little
# diagnostic weight has to be exact about what it charges for.
ALWAYS_RELEVANT = frozenset({
    "meta.data_profiling", "basic.normality", "basic.descriptive_summary",
    "anova.equal_variances",          # the precondition of a means comparison
    "nonparametric.runs_test",        # a non-random-pattern check on a series
})

# data_types that are compatible with every y_type (categorical Xs appear in any project).
_TYPE_EXEMPT = frozenset({"any", "categorical"})


def _relevant_set(task) -> set:
    rel = set(ALWAYS_RELEVANT)
    for stage in task.stages:
        for m in stage.methods:
            rel.add(m.method_id)
            rel.update(m.alternatives)
    return rel


def score(task, trace, taxonomy, y_type: str = "continuous") -> dict:
    successful = trace.successful_methods()
    attempted = trace.attempted_methods()
    relevant = _relevant_set(task)

    required = task.required_methods()
    hit, miss = [], []
    for req in required:
        if req.method_id in successful or any(a in successful for a in req.alternatives):
            hit.append(req.method_id)
        else:
            miss.append(req.method_id)

    # Misuse: attempted, off-plan, AND taxonomy says its data_type conflicts with the case y.
    # Unknown method_ids can't be judged for misuse (they still hurt precision).
    misuse = []
    if y_type != "mixed":  # mixed cases legitimately span data types — no misuse call possible
        for m in sorted(attempted - relevant):
            if m in taxonomy:
                dt = taxonomy.get(m).data_type
                if dt not in _TYPE_EXEMPT and dt != y_type:
                    misuse.append(m)

    return {
        "recall": len(hit) / len(required) if required else 1.0,
        "precision": len(attempted & relevant) / len(attempted) if attempted else 1.0,
        "misuse_rate": len(misuse) / len(attempted) if attempted else 0.0,
        "hit": sorted(hit),
        "miss": sorted(miss),
        "misuse": misuse,
        "attempted": sorted(attempted),
    }
