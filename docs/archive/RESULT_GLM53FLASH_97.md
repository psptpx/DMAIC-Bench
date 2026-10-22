# Result — GLM-5.3-Flash, all 97 tasks, one build, k = 1

The first campaign on a single, current build with the controls run against that same build.
Nothing here is spliced: the 97 clean tasks, the oracle and the nop all come from the corpus at
`af49215`.

**Controls.** oracle 109/109 at 1.000, nop 109/109 at 0.000, containerised
(`docs/archive/RESULT_G3_2026-09-12.md`). 97/97 contestant trials scored, **zero harness exceptions**,
and the report's coverage section confirms every shipped task has an observation — the check
added after the previous campaign lost one trial to a vanished container and nothing noticed.

**Provenance.** Agent `terminus-2`, provider `zai` over the Anthropic wire, 6 concurrent (the
measured ceiling; 14 produces rate-limit errors that land inside a trajectory as model
failures). Images built offline from a prebuilt verifier base, so no trial depended on the
network (`scripts/build-verifier-base.sh`).

**What it cannot support.** k = 1. Run-to-run variance is not estimable and no pass^k figure
may be computed from it.

## Against the previous campaign

Not a clean comparison — 37 of the 97 tasks differ from the build that one measured, and most of
that is the P0 gate derivation changing what the steward enforces. Stated for orientation only.

| | 2026-09-11 (95 tasks, old build) | now (97 tasks) |
|---|---|---|
| pooled mean | 0.5276 | **0.5536** |
| zero-rate | 0.2737 | **0.2268** |
| A-proceed | 0.6923 (n 44) | **0.7125** (n 46) |
| B-divert | 0.3695 (n 18) | **0.4369** (n 20) |
| C-stop | 0.3942 (n 33) | **0.3932** (n 31) |

The rise is not the benchmark getting easier. Three defects fixed between the runs were each
costing honest trials: a batch locked behind a declaration no method could make, a reference
solution testing every process against zero, and a truth package that graded evidence it had
itself made impossible. Some of the old zero-rate was ours.

## Two things the axes say that the mean does not

**Nobody violated a methodology gate. Not once in 97 trials.** `gate_hard_passed` is 1.000 and
`gate_violation_count` is 0 everywhere. The steward's locks are not a test the contestant can
fail — they are a wall it cannot walk through, so the gate axis carries no information about
this model. That is the right design for the DATA (a capability index on an unstable run should
be impossible, not merely penalised) and it means the axis should not be reported as a
capability result.

**`ms_recall` 0.968 against `ms_precision` 0.620.** The model runs nearly everything the route
requires and a great deal besides: `method_spam` appears in **94 of 97** trials. It is not
failing to find the work; it is failing to stop. That is a different deficiency from the one
the pooled mean suggests, and it is the single most common failure mode in the corpus.

## The decision, per tier

| tier | n | mean | every decision right |
|---|---|---|---|
| A-proceed | 46 | 0.7125 | 16/46 (35%) |
| B-divert | 20 | 0.4369 | **1/20 (5%)** |
| C-stop | 31 | 0.3932 | 5/31 (16%) |

`route_wrong_branch` is the first cause of failure in 54 of 96 failed trials and present in 68.
The model computes well and routes badly, which is the thing this benchmark was built to
measure.

**The two dispersion diverts added this round behaved as designed.** `adb_c34-T3-s7` (0.526) and
`adb_c35-T3-s7` (0.747) both scored pq 0.667 with ms_recall 1.000: the model ran every method,
read the location chart, and proceeded — exactly the mistake the seed exists to catch, since the
ranges were out of control and the limits it trusted were built from them.

## Full report

# Campaign report — glm53flash-97-2026-09-12

Model(s): anthropic/glm-5.3-flash

## Controls

| agent | n | mean | min | max |
|---|---|---|---|---|
| `nop` | 109 | 0.0 | 0.0 | 0.0 |
| `oracle` | 109 | 1.0 | 1.0 | 1.0 |

**Read the controls first.** An oracle below 1.000 or a nop above 0.000 means the scale is not bounded and nothing below is interpretable.

## Corpus coverage

Every one of the **97** shipped tasks has an observation from every contestant. The means below are over the whole corpus.

## Result — 97 contestant trials

mean **0.5536**, zero-rate **0.2268**, resolve-rate **0.0103** at reward >= 1.0

Case-clustered 95% CI: **[0.5, 0.61]** (ICC 0.131, design effect 1.71, 97 trials over 15 cases -> effective n **56.6**).  
Seeds of one case share its graph, brief and generator, so they are not independent; an interval computed as though they were is about 1.31x too narrow.

| tier | n | mean | 95% CI (clustered) | zero-rate | perfect-rate |
|---|---|---|---|---|---|
| A-proceed | 46 | 0.7125 | [0.6544, 0.7722] | 0.0435 | 0.0 |
| B-divert | 20 | 0.4369 | [0.2903, 0.5728] | 0.3 | 0.0 |
| C-stop | 31 | 0.3932 | [0.1883, 0.5717] | 0.4516 | 0.0323 |

### Every decision answered correctly

| tier | the question it asks | n | all decisions right | mean |
|---|---|---|---|---|
| A-proceed | did the project walk the route the data called for? | 46 | **16/46** (35%) | 0.7125 |
| B-divert | did it divert when the run proved unstable? | 20 | **1/20** (5%) | 0.4369 |
| C-stop | did it stop when the prerequisite failed? | 31 | **5/31** (16%) | 0.3932 |

Reported for every tier because the gap is informative everywhere, not only where the mean misleads. A contestant can carry a high mean on a long route while getting a decision wrong: the numeric axes pay for the arithmetic it did correctly on the way past the branch it should not have taken.

What differs between the tiers is whether the MEAN is also worth reading. A-proceed averages 3.6 decision points over a 7.2-node route, so its mean is real granularity. B-divert and C-stop average 1.9 and 2.5 points over routes of 4.8 and 4.6 nodes; their score is near-binary by construction and the mean is reported beside the rate rather than instead of it.

The tier is the number a difficulty claim rests on; the pooled mean is not.

## Axes

| axis | mean |
|---|---|
| `ms_recall` | 0.9684 |
| `ms_precision` | 0.6203 |
| `nf` | 0.6827 |
| `pq` | 0.577 |
| `sc` | 0.538 |
| `gate_hard_passed` | 1.0 |
| `hn_fabrication_rate` | 0.0026 |
| `ms_misuse` | 0.0097 |

## Failure modes

96 failed trials of 97 across 97 tasks (failed = reward < 1).

| mode | first cause | present anywhere | what it means |
|---|---|---|---|
| `method_misuse` | 10 | 10 | a method was run on data its type does not admit |
| `method_omission` | 9 | 11 | a method the route requires was never run |
| `route_wrong_branch` | 54 | 68 | a decision point was answered, and answered wrongly |
| `route_not_addressed` | 2 | 16 | a decision point was never answered either way |
| `fabrication` | 0 | 1 | a number appears in the report that no computation produced |
| `misreport` | 7 | 26 | a computed number is reported as something other than what was computed |
| `numeric_error` | 10 | 61 | the right method was run and the value reported is outside tolerance |
| `value_not_reported` | 0 | 20 | a graded value was never reported at all |
| `method_spam` | 4 | 94 | methods were run that no node on the route calls for |

### Distinct modes per task

| distinct modes | tasks |
|---|---|
| 0 | 1 |
| 1 | 5 |
| 2 | 24 |
| 3 | 34 |
| 4 | 19 |
| 5 | 10 |
| 6 | 2 |
| 7 | 2 |

**Concentrated** (1-2 modes): 29 tasks — a stable evaluation signal.  
**Diverse** (3+): 67 tasks — a richer training signal.

## Tasks no contestant solved

22 task(s). A task nobody solves is hard OR broken, and the two are not distinguishable from the score alone.

| task | tier | oracle | failure modes | hint probe |
|---|---|---|---|---|
| adb_c25-T3-s4-clean | C-stop | 1.000 | `route_wrong_branch`×1, `method_spam`×1 | none |
| adb_c26-T3-s4-clean | C-stop | 1.000 | `route_wrong_branch`×1, `numeric_error`×1, `method_spam`×1 | none |
| adb_c26-T3-s5-clean | C-stop | 1.000 | `method_misuse`×1, `route_wrong_branch`×1, `method_spam`×1 | none |
| adb_c27-T3-s0-clean | A-proceed | 1.000 | `method_omission`×1, `route_wrong_branch`×1, `route_not_addressed`×1, `numeric_error`×1, `value_not_reported`×1, `method_spam`×1 | none |
| adb_c27-T3-s4-clean | C-stop | 1.000 | `route_wrong_branch`×1, `numeric_error`×1, `method_spam`×1 | none |
| adb_c29-T3-s4-clean | B-divert | 1.000 | `numeric_error`×1, `value_not_reported`×1, `method_spam`×1 | none |
| adb_c30-T3-s3-clean | C-stop | 1.000 | `route_wrong_branch`×1, `misreport`×1, `numeric_error`×1, `method_spam`×1 | none |
| adb_c30-T3-s4-clean | C-stop | 1.000 | `route_wrong_branch`×1, `numeric_error`×1, `method_spam`×1 | `hp01` |
| adb_c30-T3-s5-clean | C-stop | 1.000 | `route_wrong_branch`×1, `method_spam`×1 | `hp01` |
| adb_c31-T3-s2-clean | C-stop | 1.000 | `route_wrong_branch`×1, `method_spam`×1 | none |
| adb_c31-T3-s3-clean | C-stop | 1.000 | `route_wrong_branch`×1, `method_spam`×1 | `hp01` |
| adb_c31-T3-s4-clean | C-stop | 1.000 | `route_wrong_branch`×1, `numeric_error`×1, `method_spam`×1 | `hp01` |
| adb_c33-T3-s4-clean | B-divert | 1.000 | `method_misuse`×1, `route_wrong_branch`×1, `misreport`×1, `numeric_error`×1, `method_spam`×1 | none |
| adb_c34-T3-s4-clean | C-stop | 1.000 | `route_wrong_branch`×1, `numeric_error`×1, `method_spam`×1 | none |
| adb_c35-T3-s4-clean | C-stop | 1.000 | `route_wrong_branch`×1, `method_spam`×1 | none |
| adb_c36-T3-s0-clean | A-proceed | 1.000 | `route_wrong_branch`×1, `numeric_error`×1, `method_spam`×1 | none |
| adb_c36-T3-s4-clean | B-divert | 1.000 | `method_misuse`×1, `route_wrong_branch`×1, `numeric_error`×1, `method_spam`×1 | none |
| adb_c37-T3-s5-clean | C-stop | 1.000 | `route_wrong_branch`×1, `numeric_error`×1, `method_spam`×1 | none |
| adb_c38-T3-s0-clean | B-divert | 1.000 | `route_wrong_branch`×1, `method_spam`×1 | none |
| adb_c38-T3-s5-clean | B-divert | 1.000 | `route_not_addressed`×1, `method_spam`×1 | none |
| adb_c39-T3-s4-clean | C-stop | 1.000 | `route_wrong_branch`×1, `numeric_error`×1, `method_spam`×1 | none |
| adb_c39-T3-s5-clean | B-divert | 1.000 | `route_wrong_branch`×1, `numeric_error`×1, `method_spam`×1 | none |

Every one has an oracle at 1.000, so none is unsolvable by construction. That is necessary and not sufficient: it bounds the scale, it does not show a contestant could get there. Where a hint probe exists, run it (docs/archive/HINT_PROTOCOL.md).

## Per case

| case | n | mean |
|---|---|---|
| adb_c25 | 5 | 0.6416 |
| adb_c26 | 6 | 0.4907 |
| adb_c27 | 6 | 0.4608 |
| adb_c28 | 6 | 0.8205 |
| adb_c29 | 5 | 0.6698 |
| adb_c30 | 7 | 0.4512 |
| adb_c31 | 5 | 0.3027 |
| adb_c32 | 6 | 0.6625 |
| adb_c33 | 6 | 0.5685 |
| adb_c34 | 8 | 0.5248 |
| adb_c35 | 8 | 0.6126 |
| adb_c36 | 7 | 0.5356 |
| adb_c37 | 8 | 0.6013 |
| adb_c38 | 7 | 0.524 |
| adb_c39 | 7 | 0.4466 |

