# Response-commitment breach project - status report

Task: `[TASK]`. Every figure below comes from a computation run on this dataset and is recorded in `/workspace/trace.json`.

## Headline

The breach share is stable and, as currently measured, sits below the 5% internal requirement - but the breach judgement itself does not survive scrutiny, so that reassurance is provisional. Fix the judging before acting on the rate.

## 1. Can a breach judgement be relied on? No.

Three reviewers each judged the same 20 tickets twice against a known answer key (120 judgements in total).

| Measure | Result |
|---|---|
| Lowest reviewer kappa vs the key | 0.362 |
| Highest reviewer kappa vs the key | 0.738 |
| Mean reviewer kappa | 0.538 |
| Tickets all reviewers judged correctly every time | 15.0% |
| Reviewers agreeing with each other on a ticket | 15.0% |
| Accuracy of an individual judgement | 78.3% |

Repeatability - the same reviewer reaching the same verdict on a second look - was 55.0%, 50.0% and 75.0%. Reviewer 2 agreed with the key on only 45.0% of tickets.

The usual acceptance bar for an attribute system is kappa of 0.90, with 0.70 the marginal floor. The weakest reviewer is at 0.362 and none reach 0.90. Roughly one judgement in five is wrong, and reviewers do not even reproduce their own verdicts. **Every breach count in the rest of this report was produced by that system**, so the rates that follow carry an unquantified misclassification error. They are the best available estimates, not settled facts.

## 2. Has the breach share been steady? Yes.

Twenty-five consecutive periods, 200 tickets each, 5000 tickets and 196 breaches in total.

| Measure | Result |
|---|---|
| Centre line (p-chart) | 3.92% |
| Upper control limit | 8.04% |
| Lower control limit | 0% |
| Points outside the limits | 0 |
| Runs test about the centre line | p = 0.670 |
| Laney sigma-Z (overdispersion check) | 1.023 |

No point breaches a control limit and there is no non-random run pattern. Sigma-Z of 1.023 is effectively 1, confirming no overdispersion at this subgroup size, so the ordinary p-chart limits are the right ones and no Laney correction was needed.

Period rates average 3.92% with a standard deviation of 1.63 percentage points, ranging from 0.5% to 8.0%, near-symmetric (skewness 0.12) and consistent with normality (Shapiro-Wilk p = 0.496).

The practical reading: the swings between periods, including the worst period at 8.0%, are common cause. There is no special-cause event to investigate. Chasing individual bad weeks would be tampering.

## 3. How far is today's level from the requirement?

| Measure | Result |
|---|---|
| Observed breach share | 3.92% |
| Internal requirement | 5% |
| Exact binomial test vs 5% | p = 0.000314 |
| 95% confidence interval | 3.40% to 4.50% |
| Process Z | 1.76 |
| Defect level | 39,200 ppm |

The share is significantly below the 5% ceiling and the whole confidence interval sits under it. On the measured data the requirement is being met on aggregate.

Two caveats belong next to that conclusion. First, section 1: the measurement system that produced these counts is not trustworthy, so the true level could sit either side of the measured one. Second, the margin is thin. With a centre line of 3.92% and an upper control limit of 8.04%, individual periods can and do land above 5% without the process having changed at all. "Missed too often" as experienced on the floor is consistent with a stable 3.92% system: the average clears the bar while single periods do not.

## 4. What is driving it?

The only cause data released was a two-team intake and breach summary over one common window: team 1 with 30 breaches in 600 tickets (5.0%), team 2 with 24 in 600 (4.0%).

| Measure | Result |
|---|---|
| Two-proportion test | z = 0.836, p = 0.403 |
| Chi-square cross-check | chi-square = 0.698, p = 0.403 |
| Power at the observed 1-point gap | 0.133 |

The chi-square cross-check reproduces the two-proportion test exactly.

The one-point gap is not statistically detectable. But power was only 0.133, so this test would have missed a real difference of that size roughly seven times in eight. **This is an inconclusive result, not evidence that the teams perform alike.** Team is neither confirmed nor ruled out as a driver.

No other cause data exists. No batch relating the breach rate to arrival volume, staffing, shift, ticket type, queue time or priority was available. The steward holds four batches in total - charter, reviewer study, per-period counts, team summary - and confirmed nothing further exists.

## 5. What was changed, and what did the change achieve?

**Nothing was changed, and there is no data on which to claim any achievement.** No improvement, pilot, designed-experiment or post-change batch exists; requests for them were refused as unroutable against a list of the only four topics held. The project therefore stops at the analyse stage. Any statement in this report about a gain delivered or a level held would be invention, so none is made. There is likewise no control-phase monitoring data, so no verified holding mechanism can be reported.

## 6. What should be done next

1. **Fix the breach judgement first.** With the weakest reviewer at kappa 0.362 and only 15.0% of tickets judged correctly by everyone, no improvement measured against this system can be believed - an apparent gain could be reviewers drifting. Clarify the breach definition, retrain on the answer key with the worst-disagreeing tickets as the teaching set, and re-run this study. Do not accept improvement work until kappa clears 0.90.
2. **Do not chase individual periods.** The chart is stable, so period-to-period variation is common cause. Reducing the level means changing the system, not reacting to bad weeks.
3. **Re-run the team comparison on a longer window before ruling team out.** At 0.133 power the current window settles nothing; a longer window is needed to detect a gap of this size.
4. **Ask for the cause data the project lacks.** Volume, staffing, shift, ticket type and queue-time detail are needed to locate the drivers of a 3.92% common-cause level.
5. **Build the margin, then hold it.** At a 3.92% centre line with an 8.04% upper limit, single periods will keep crossing 5%. Holding the average below the ceiling reliably means lowering the centre line, then monitoring on this p-chart with the limits recomputed once the measurement system is sound.

## Honest limits of this report

- All breach rates rest on a measurement system that failed its check; treat them as provisional.
- The team comparison is underpowered and settles nothing either way.
- There is no improvement data and no control data. Nothing is claimed about a change delivered, a gain achieved, or a gain held.
