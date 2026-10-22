# Hint probes: telling a hard task from a broken one

A task no system solves is ambiguous, and the ambiguity has already cost this benchmark a
campaign. Nine tasks floored every model at reward 0.000 beside `ms_recall` 1.000; they were
reported as difficulty and they were **unscoreable** — Path Quality compared a decision-graph
node key that reaches no instruction, no batch and no steward reply. It took an offline re-score
to find. Nothing in the pipeline could have told the two cases apart while the campaign ran,
because from the outside they look identical: every contestant scores zero.

A hint probe is the instrument that separates them, and it is causal rather than descriptive.

## The procedure

1. Take a failed trajectory and form a hypothesis about the root cause. A derived failure mode
   (`docs/FAILURE_MODES.md`) is a good hypothesis and is not yet evidence.
2. Phrase a hint that addresses **that cause**, at the altitude set out below.
3. Add the hint to the brief and rerun, as a separate task.
4. Read the outcome:

| what happened | what it means |
|---|---|
| the calibrated hint gets the agent past the point it failed at | the failure mode is **real and causally confirmed** — a capability gap |
| the calibrated hint changes nothing | suspect a broken environment, or a false negative (a good answer the verifier rejects) |
| only the over-specified hint works | suspect a knowledge gap, or a task solvable only when handed the answer |
| the under-specified hint alone works | the failure was inattention, not the labelled cause; the finding does not stand |

**Partial success still validates.** The agent may clear the previously-failing step and fail
somewhere later. That confirms the mode — the claim is about the specific point it could not get
past, not about finishing.

## Calibration: the altitude is the whole thing

- **Over-specified** — the hint contains the answer. It proves the agent can transcribe and
  destroys the causal signal: you can no longer tell whether it overcame its own limitation or
  simply followed directions.
- **Under-specified** — too generic to change behaviour. The mode stays unconfirmed and nothing
  has been learned.
- **Calibrated** — names the DIMENSION the agent must attend to, and stops short of naming what
  it will find there.

There is no universal wording; the same sentence is calibrated for one task and a giveaway for
another. So rather than ship one hint and argue about where it sits, **every probe ships three
rungs, and the outer two are controls** — in the same sense that `nop` and `oracle` bound the
reward scale:

```
L0  deliberately under-specified   if this alone works, the failure was inattention
L1  the calibrated hint            the one a finding may rest on
L2  deliberately over-specified    if ONLY this works, suspect a knowledge gap or a defect
```

A result is quotable as "mode confirmed" only when **L1 moves the agent past the failure point
and L0 does not**. `hints.REPORTABLE_RUNGS` excludes L2, and an L2 pass is never counted as a
resolve.

## What is machine-checked, and what is not

`hints.check_hint` refuses a hint that contains a private graph node key or any rendering of a
value from that seed's own results, matched on word boundaries so a single digit — which is
exactly the shape of the answer in the probe below — cannot slip through. `build.assert_no_method_leak`
independently refuses a rendered instruction that names any method or alias in the taxonomy.

Neither can judge **altitude**. Rung L2 is over-specified in substance and passes both checks
cleanly, because it names the quantity in words and no number appears in it. Numeric leakage is
machine-checkable; conceptual over-specification is not, which is why every rung ships a written
rationale and why the three-rung design exists at all: the calibration argument is settled by the
L0/L2 controls at run time rather than by an assertion at build time.

## Building and running a probe

```
# the four probe tasks at the calibrated rung
python3 -m dmaic_harbor.build --v2 --out <dir> --cases adb_c30,adb_c31 --hint L1

# the two controls
python3 -m dmaic_harbor.build --v2 --out <dir> --cases adb_c30,adb_c31 --hint L0
python3 -m dmaic_harbor.build --v2 --out <dir> --cases adb_c30,adb_c31 --hint L2
```

Only seeds carrying a probe are emitted. Each is a separate task id (`…-clean-hp01l1`), so a
hinted run can never pool with the plain one — a run that was told where to look is not evidence
about a run that was not. Stages and truths are byte-identical to the plain task, asserted by
`tests/test_hint_probes.py`: the probe changes the brief and nothing else, so the hint is the
only variable.

## Probe hp01 — the distinct-categories trap

**Tasks**: `adb_c30` seeds 4, 5 and `adb_c31` seeds 3, 4. On each, the gauge study lands under
the familiar 30% study-variation screen and resolves too few distinct groups to control the
process, under **both** admissible conventions. The oracle route stops at the gauge.

**Observation.** Twelve trials across three frontier models, twelve zeros. Every model computed
the percentage, saw a number below 30, and proceeded to a capability index it had no basis for.

**Hypothesis.** The contestant applies one remembered acceptance criterion and stops checking.
Not that it cannot compute the second quantity — that reaching a familiar threshold ends the
enquiry. In the taxonomy this is `route_wrong_branch` at the gauge decision.

**Why this probe is owed.** `docs/archive/TIER_RESULTS.md` defends these four tasks with three arguments:
the oracle scores 1.000 on all of them through the behaviour-based route, both conventions agree
the gauge fails, and a documented human project met the same situation and stopped. All three are
**static** — properties of the task, not observations of what a hinted contestant does. They
establish that the task is not known to be broken, which is not the same as evidence that it is
hard. This probe is the missing dynamic evidence, and it is cheap: four tasks, three rungs.

### Result, GLM-5.3-Flash, k = 1, 2026-09-10

| task | no hint | L0 under-specified | L1 calibrated | L2 giveaway |
|---|---|---|---|---|
| adb_c30 s4 | 0.000 | 0.000 | 0.000 | 0.000 |
| adb_c30 s5 | 0.000 | 0.000 | 0.000 | 0.000 |
| adb_c31 s3 | 0.000 | 0.000 | 0.000 | 0.000 |
| adb_c31 s4 | 0.000 | 0.000 | 0.000 | 0.000 |

Twelve trials, twelve zeros, and the gauge decision answered wrongly in all twelve.

**The outcome table above did not anticipate this row.** It offered "a calibrated hint that does
not help" as evidence of a broken environment or a false negative, and neither is what happened.
Under L2 — the rung that states the criterion and its threshold outright — the contestant:

1. ran the gauge study and obtained **ndc = 4**;
2. **reported that number correctly** (both numeric truths passed, `nf` = 1.000, `ms_recall` =
   1.000, no gate violation);
3. and then went on to an individuals chart, a normality test and a capability index of
   **Cpk 1.94** on the gauge it had just measured as unusable.

So the reward is 0.000 with every axis but one at its maximum: `pq` = 0.000, one decision point,
taken wrongly with the answer in hand. This is not a knowledge gap and not a task defect. It is
a failure to ACT on a criterion the contestant can compute, state and quote.

That is a fifth outcome, and it belongs in the table:

| what happened | what it means |
|---|---|
| not even the over-specified hint changes the branch, while the numeric axes stay perfect | the contestant is not missing the rule; it is not applying it. A capability claim on a **stated** ndc of 4 is the finding, and the task is measuring exactly what it was built to measure |

### Why these four tasks are ungated, deliberately

Their guard is compound — `msa.pctSV <= 0.30 and msa.ndc >= 5` — and `v2_tasks._GUARD_TO_GATE`
maps only the simple form, so the steward emits **no gate** for them and releases the process run
as soon as the gauge study is done. Their siblings with a single-criterion guard DO get
`gates: ['msa_pass']` and are refused.

That asymmetry was an accident of a lookup table. It is now a deliberate choice, because closing
it would destroy what the tasks measure: a trap that tests whether a contestant STOPS when
nothing stops it cannot be graded in an environment that stops it. Extending the table so the
steward enforced the compound criterion would make all four tasks trivially passable and
measure nothing.

The consequence has to be reported rather than absorbed: **these four tasks measure unenforced
self-restraint, and the other 91 do not.** They are a named subset with their own count in
`TIER_RESULTS.md`, never pooled into a tier mean, and that separation is now load-bearing rather
than presentational.
