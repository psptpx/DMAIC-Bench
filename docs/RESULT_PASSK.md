# pass^3 — reliability is a property of the QUESTION, not of the model

GLM-5.3-Flash, all 97 tasks, three attempts each, one build, one scorer. Controls on that same
build and scorer: oracle 109/109 at 1.000, nop 109/109 at 0.000.

## The result

| tier | n | pass^1 | **pass^3** | pass@3 | mean spread | max spread |
|---|---|---|---|---|---|---|
| A-proceed | 46 | — | **0.348** | 0.457 | 0.168 | 0.849 |
| B-divert | 20 | 0.050 | **0.050** | 0.050 | 0.214 | 0.675 |
| C-stop | 31 | 0.183 | **0.097** | 0.323 | 0.198 | **1.000** |

`spread` is max minus min reward across one task's three attempts. "pass" here is *every
decision answered correctly*, not `reward = 1.0`: at a resolve rate of 1% a pass^k on reward is
almost all zeros and separates nothing.

## Three shapes, one model, one corpus

**B-divert: 0.050 = 0.050 = 0.050.** pass^1, pass^3 and pass@3 are the same number. What it
gets right it gets right every time; what it gets wrong it gets wrong every time. There is no
randomness to average over — this is a capability boundary, and k = 1 measured it correctly.
One task in twenty.

**C-stop: pass^3 is a third of pass@3** (0.097 against 0.323). The single-run figure of 0.183
is neither the capability (0.097, what it does reliably) nor the reach (0.323, what it has ever
done). It is a point between two real quantities that corresponds to nothing. Max spread is
1.000: one task scored a perfect 1.0 on one attempt and 0.0 on another.

**A-proceed: 0.348 against 0.457.** About a quarter of the tasks it has ever routed correctly,
it does not route correctly reliably.

**The finding is the contrast.** Same model, same corpus, same scorer: on one tier a single run
tells you everything, on another it tells you almost nothing. Reliability is not a scalar
property of a system that a benchmark can report once. It depends on what the task asks. A
benchmark that reports one pass rate is averaging over that difference and hiding it.

## What this cost, and what it bought

Two 17-hour runs. It bought:

* the B-divert claim, which k = 1 could not have made — 0.050 at k = 1 could have been noise,
  and now it is known not to be;
* the retraction of part of the C-stop difficulty claim. The k = 1 report named 22 tasks "no
  contestant solved"; seven of the C-stop ones were solved on a later attempt. "Never solved"
  and "solved unreliably" are different results and the first one was partly an artefact.

## Limits

One model. k = 3, which bounds pass^3 loosely: 0/20 on B-divert has a 95% upper bound near 14%
by the rule of three, and 46/20/31 per tier is a small corpus. And `spread` is computed on
reward, which mixes the decision axes with the numeric ones; a decision-only spread would be
the cleaner statistic and is not yet reported.

## Full report

# Campaign report — glm53flash-97-2026-09-12 + glm53flash-bc-k3 + glm53flash-a-k3

Model(s): anthropic/glm-5.3-flash

## Controls

| agent | n | mean | min | max |
|---|---|---|---|---|
| `nop` | 109 | 0.0 | 0.0 | 0.0 |
| `oracle` | 109 | 1.0 | 1.0 | 1.0 |

**Read the controls first.** An oracle below 1.000 or a nop above 0.000 means the scale is not bounded and nothing below is interpretable.

## Corpus coverage

Every one of the **97** shipped tasks has an observation from every contestant. The means below are over the whole corpus.

## pass^3

97 of 97 tasks were attempted at least 3 times.

| tier | tasks at k=3 | pass^3 (every decision right) | pass@3 | pass^3 (reward = 1) | mean spread | max spread |
|---|---|---|---|---|---|---|
| A-proceed | 46 | **0.3478** | 0.4565 | 0.0 | 0.1678 | 0.8485 |
| B-divert | 20 | **0.05** | 0.05 | 0.0 | 0.2135 | 0.6747 |
| C-stop | 31 | **0.0968** | 0.3226 | 0.0 | 0.1977 | 1.0 |

**Read the decision column, not the reward one.** At a resolve rate near 1% a pass^k on `reward = 1` is almost all zeros and distinguishes nothing; what a DMAIC task asks is whether every decision was answered correctly, and pass^k on THAT is the reliability claim. `spread` is max-minus-min reward across the attempts of one task — the direct answer to whether a tier's mean is a capability or a coin flip.

## Result — 97 contestant trials

mean **0.5575**, zero-rate **0.2268**, resolve-rate **0.0103** at reward >= 1.0

Case-clustered 95% CI: **[0.5028, 0.614]** (ICC 0.132, design effect 1.72, 97 trials over 15 cases -> effective n **56.3**).  
Seeds of one case share its graph, brief and generator, so they are not independent; an interval computed as though they were is about 1.31x too narrow.

| tier | n | mean | 95% CI (clustered) | zero-rate | perfect-rate |
|---|---|---|---|---|---|
| A-proceed | 46 | 0.7149 | [0.6563, 0.7748] | 0.0435 | 0.0 |
| B-divert | 20 | 0.4369 | [0.2903, 0.5728] | 0.3 | 0.0 |
| C-stop | 31 | 0.4018 | [0.1912, 0.5803] | 0.4516 | 0.0323 |

### Every decision answered correctly

| tier | the question it asks | n | all decisions right | mean |
|---|---|---|---|---|
| A-proceed | did the project walk the route the data called for? | 46 | **18/46** (39%) | 0.7149 |
| B-divert | did it divert when the run proved unstable? | 20 | **1/20** (5%) | 0.4369 |
| C-stop | did it stop when the prerequisite failed? | 31 | **6/31** (19%) | 0.4018 |

Reported for every tier because the gap is informative everywhere, not only where the mean misleads. A contestant can carry a high mean on a long route while getting a decision wrong: the numeric axes pay for the arithmetic it did correctly on the way past the branch it should not have taken.

What differs between the tiers is whether the MEAN is also worth reading. A-proceed averages 3.6 decision points over a 7.2-node route, so its mean is real granularity. B-divert and C-stop average 1.9 and 2.5 points over routes of 4.8 and 4.6 nodes; their score is near-binary by construction and the mean is reported beside the rate rather than instead of it.

The tier is the number a difficulty claim rests on; the pooled mean is not.

## Axes

| axis | mean |
|---|---|
| `ms_recall` | 0.9684 |
| `ms_precision` | 0.6203 |
| `nf` | 0.6827 |
| `pq` | 0.5899 |
| `sc` | 0.5354 |
| `gate_hard_passed` | 1.0 |
| `hn_fabrication_rate` | 0.0026 |
| `ms_misuse` | 0.0097 |

## Failure modes

96 failed trials of 97 across 97 tasks (failed = reward < 1).

| mode | first cause | present anywhere | what it means |
|---|---|---|---|
| `method_misuse` | 10 | 10 | a method was run on data its type does not admit |
| `method_omission` | 9 | 11 | a method the route requires was never run |
| `route_wrong_branch` | 52 | 67 | a decision point was answered, and answered wrongly |
| `route_not_addressed` | 1 | 13 | a decision point was never answered either way |
| `fabrication` | 0 | 1 | a number appears in the report that no computation produced |
| `misreport` | 9 | 26 | a computed number is reported as something other than what was computed |
| `numeric_error` | 11 | 61 | the right method was run and the value reported is outside tolerance |
| `value_not_reported` | 0 | 20 | a graded value was never reported at all |
| `method_spam` | 4 | 94 | methods were run that no node on the route calls for |

### Distinct modes per task

| distinct modes | tasks |
|---|---|
| 0 | 1 |
| 1 | 5 |
| 2 | 25 |
| 3 | 34 |
| 4 | 20 |
| 5 | 8 |
| 6 | 2 |
| 7 | 2 |

**Concentrated** (1-2 modes): 30 tasks — a stable evaluation signal.  
**Diverse** (3+): 66 tasks — a richer training signal.

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
| adb_c35 | 8 | 0.6185 |
| adb_c36 | 7 | 0.5437 |
| adb_c37 | 8 | 0.6357 |
| adb_c38 | 7 | 0.524 |
| adb_c39 | 7 | 0.4466 |

