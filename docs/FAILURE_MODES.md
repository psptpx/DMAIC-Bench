# Failure modes

A zero-rate says how often a contestant lost. It never says what it lost to, and those are
different measurements: a task whose failures are all one mode is a stable evaluation signal, a
task whose failures spread over six is a rich training signal, and a mean cannot tell them apart.
This page is the taxonomy, how a label is assigned, what the assignment does and does not
establish, and a worked distribution.

## The labels are DERIVED

Every mode below is a predicate over the `scorecard.json` the verifier already writes. Nothing is
hand-labelled, so the assignment is reproducible, costs nothing per trajectory, and cannot drift
between annotators. `dmaic_harbor.failure_modes` is the implementation and
`tests/test_failure_modes.py` holds one minimal triggering card per mode — a label nothing can
trigger is decoration, and the test set is the taxonomy's operational definition.

What a derived label does **not** give is *why* the agent did it. `route_not_addressed` says the
contestant never answered a decision; it does not say whether it did not know the decision was
there, ran out of budget before reaching it, or judged it not worth making. Establishing that is
what the hint approach (`docs/archive/HINT_PROTOCOL.md`) is for, and **a derived label is a hypothesis
until a hint confirms it.**

## The taxonomy

Listed in causal order — the order a project fails in. `modes_of` reports every mode present;
`primary_mode` reports the first one, because everything after the first failure is downstream of
it, and a run with no trace also omits every method.

| # | mode | what it means |
|---|---|---|
| 1 | `no_trace` | no parseable trace.json — nothing the contestant did is legible to the scorer |
| 2 | `no_report` | a trace, but no report — the deliverable the brief asks for was never written |
| 3 | `gate_violation` | an analysis was run before the prerequisite that licenses it |
| 4 | `method_misuse` | a method was run on data its type does not admit |
| 5 | `method_omission` | a method the route requires was never run |
| 6 | `route_wrong_branch` | a decision point was answered, and answered wrongly |
| 7 | `route_not_addressed` | a decision point was never answered either way |
| 8 | `fabrication` | a number appears in the report that no computation produced |
| 9 | `misreport` | a computed number is reported as something other than what was computed |
| 10 | `fault_dishonesty` | an analysis the steward withheld was claimed as done |
| 11 | `numeric_error` | the right method was run and the value reported is outside tolerance |
| 12 | `value_not_reported` | a graded value was never reported at all |
| 13 | `order_violation` | the right work in an order the methodology forbids |
| 14 | `method_spam` | methods were run that no node on the route calls for |

A trial counts as **failed** when its reward is below 1.0. That is deliberately the strictest
reading: this benchmark's reward is continuous, no resolve threshold has ever been declared for
it, and inventing one here would put a free parameter under every number on this page. "Did not
score full marks" needs no threshold.

## Controls are not contestants

`nop` does nothing by design, so every one of its trials is `no_trace`, and `oracle` scores 1.000
by construction. Pooling them reports the control as the dominant failure mode — measured on the
retained trials, **32 of 34 `no_trace` primaries were the nop control**. `contestants()` drops
them and the CLI does so by default.

## Running it

```
python3 -m dmaic_harbor.failure_modes <job dir> [<job dir> ...] [--title ...]
```

## Worked distribution: the retained local trials

70 failed trials of 70 across 26 tasks (failed = reward < 1).

| mode | first cause | present anywhere | what it means |
|---|---|---|---|
| `no_trace` | 2 | 2 | no parseable trace.json — nothing the contestant did is legible to the scorer |
| `method_misuse` | 5 | 5 | a method was run on data its type does not admit |
| `method_omission` | 4 | 9 | a method the route requires was never run |
| `route_wrong_branch` | 18 | 22 | a decision point was answered, and answered wrongly |
| `route_not_addressed` | 34 | 63 | a decision point was never answered either way |
| `numeric_error` | 3 | 35 | the right method was run and the value reported is outside tolerance |
| `value_not_reported` | 0 | 9 | a graded value was never reported at all |
| `method_spam` | 4 | 61 | methods were run that no node on the route calls for |

### Distinct modes per task

| distinct modes | tasks |
|---|---|
| 1 | 1 |
| 2 | 3 |
| 3 | 9 |
| 4 | 5 |
| 5 | 4 |
| 6 | 4 |

**Concentrated** (1-2 modes): 4 tasks — a stable evaluation signal.  
**Diverse** (3+): 22 tasks — a richer training signal.

### What this shows, and what it does not

**Scope first.** These are the trials retained on the author's machine — one agent harness
(terminus-2) over 26 tasks from the 40-task era, not the gateway campaign that produced
`archive/TIER_RESULTS.md`, and not the 95-task corpus. Nothing here is a headline number. It is here to
show the instrument working on real data and to state the one finding that is robust to the
scope.

**The failures are navigation failures, not arithmetic failures.** Of 70 failed trials,
`route_not_addressed` and `route_wrong_branch` are the FIRST cause in 52 (74%). `numeric_error`
is present in 35 (50%) and is the first cause in 3 (4%): contestants get numbers wrong all the
time, and it is almost never what loses them the run. This is the first direct evidence for the
claim the benchmark was built on — that the hard part is knowing which analysis the data calls
for next, not performing it.

**Method spam is loud and cheap.** `method_spam` is present in 61 of 70 runs (87%) and is the
first cause in 4. Contestants run a great deal of work the route never asks for; it costs them
precision and almost never costs them the run. Whether that should be priced more heavily is a
scoring question this measurement raises and does not answer.

**Every mode that fires is one the taxonomy names.** No failed contestant trial fell outside it,
asserted by `test_no_failed_contestant_trial_falls_outside_the_taxonomy`. Six of the fourteen
modes did not occur at all in this set — `gate_violation`, `fabrication`, `misreport`,
`fault_dishonesty`, `order_violation` and `no_report` — which is a fact about these 26 tasks and
this agent, not evidence that they cannot occur.

## Concentrated or diverse

The requirement this page answers in full is the split between the two useful shapes. On the
retained trials 4 tasks drew one or two distinct modes across their trials and 22 drew three or
more. The histogram above is the reportable form; it is per task, over that task's failed trials,
and it is the measurement a per-tier mean cannot substitute for.
