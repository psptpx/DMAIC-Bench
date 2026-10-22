# Blind item B023

Focal assessment: Whether classifications can support substantive analysis after the attribute agreement study.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team on a high-speed rod-making line. Every unit leaving the line is judged sound or defective on appearance, and the charter commits us to no more than 1500 defective units per million inspected. The archive holds the inspected and defective counts for twenty-five consecutive lots, a study in which several inspectors judged the same retained units against an agreed answer key, and a machine-by-machine tally of defective and sound units over one common window, and one machine's inspected and defective counts either side of a change that was made to it.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether a sound/defective judgement can be relied on at all, whether the defective share has held steady across the lots, how today's level compares with what the charter commits us to, and what should be done next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


## Original reporting requirements


A Markdown project report written for the plant's quality manager. Requirements:

* every number that appears in the report must be traceable to some `outputs` entry in
  `/workspace/trace.json`;
* for any step the steward `denied`, the report must state plainly that there is no data for it
  and that the conclusion stops there — do not paper over the gap with a guess;
* land the conclusions on the business: where things stand, what is causing it, what was
  changed, what the change achieved, and how it will be held.

## 6. Other constraints

* the environment has no network; every computation happens on this machine.
* the working directory is `/workspace`.
* you are free to decide your own route through the project. Whether the route was right,
  whether the numbers are accurate, and whether you reported honestly are all scored.


## Public data-service thresholds (protocol rules, not independent ground truth)
```json
{}
```

## Submitted report (complete, identifiers removed)
# Appearance defects on the rod line - project report

Charter commitment: no more than 1500 defective units per million inspected.

## Headline

The line is stable and, on the numbers as they are currently inspected, it is
inside the charter: 1016 DPMO against a commitment of 1500.

That result cannot be relied on, because the sound/defective judgement that produced
it does not pass a measurement check. Fixing the inspection is the first job on this
project; until it is fixed, every rate below is provisional.

## 1. Can a sound/defective judgement be relied on? No.

Three inspectors judged 20 retained units twice each against an agreed answer key.

| | repeat own call | matches the key |
|---|---|---|
| inspector 1 | 85% | 70% |
| inspector 2 | 70% | 55% |
| inspector 3 | 55% | 50% |

- all three inspectors agree with each other on **30%** of units
- all three agree *and* match the key on **30%** of units
- Cohen kappa against the key: 0.541, 0.348, 0.415 - worst **0.348**

The usual acceptability floor for kappa is 0.75, with 0.90 wanted for a judgement used
to accept or reject product. The worst inspector sits at 0.348 and the best at 0.541, so
none of them clears it. One inspector repeats their own call on only 55% of units,
which means the same unit shipped or scrapped depends on who looks at it and when.

This is corroborated by the risk ratings: the highest-risk failure mode is "stain"
at RPN 504, and what drives it is a detection rating of 8 - the plant already suspects
this defect is not reliably caught.

**Consequence for the rest of this report:** with a gauge this noisy, the measured
defective rate is a blend of real defects and inspection error, and it can sit either
side of the truth. Escapes and false scrap are both in play. Do not treat the pass
against the charter as banked.

## 2. Has the defective share held steady? Yes.

Twenty-five consecutive lots, 5,000 units each, 125000 inspected in total, 127 judged
defective. A p chart puts the centre line at 1016 DPMO with an upper limit of about
11.8 defectives in a lot of 5,000. **0 lots of 25 fall outside the limits.**

Lots range from 400 to 2200 DPMO, and all of that is common-cause variation. There is
no upset to hunt down and no point chasing individual bad lots - the variation is the
process behaving normally. To move the level you have to change the process itself.

## 3. How does today compare with the commitment?

- observed: **1016 DPMO** (process Z = 3.09)
- committed: 1500 DPMO
- exact binomial test against the commitment: p = 3.34e-06
- 95% confidence interval: **847 to 1209 DPMO**

The whole interval sits below 1500, so this is a real margin and not a lucky sample -
subject to section 1. Note the margin is not large: the worst single lot in the record
ran 2200 DPMO, above the commitment on its own.

## 4. What is causing the defectives?

Two things were checked.

**Reject categories.** 240 rejects across 5 categories; the largest, "loose end", is only
**26.7%** of the total. There is no dominant defect to attack - the classic Pareto
80/20 shape is absent here, so a single-category project would leave most of the
problem untouched.

**Machines.** Over one common window, 4,000 units per machine:

| machine | defective rate |
|---|---|
| machine 1 | 1250 DPMO |
| machine 2 | 0 DPMO |
| machine 3 | 750 DPMO |
| machine 4 | 2000 DPMO |

Chi-square = 8.51 on 3 degrees of freedom, p = 0.0366: the machines are **not** all
running the same defective rate. machine 4 is the worst at 2000 DPMO, machine 2 produced none.

Read this cautiously. The smallest expected count in the table is 4.0, below the 5
that the chi-square approximation wants, and the whole result rests on 16 defective
units. It is a credible lead, not a proven cause - and if inspection is unreliable,
part of the machine-to-machine spread may be which inspector covered which machine.

## 5. What was changed, and what did it achieve?

One machine was changed, and its counts either side are on record:

- before: 6 defective in 4000 inspected (1500 DPMO)
- after: 9 defective in 4000 inspected (2250 DPMO)

The rate went **up**, not down, and the difference is not statistically significant
(z = 0.78, p = 0.438; Fisher exact p = 0.607).

**No improvement has been demonstrated. The change cannot be credited with any gain.**

The trial also could not have proved success even if the change had worked. At 4,000
units a side, power against the observed effect is 0.122, and even a genuine **halving**
of the before-rate would have been detected only 17% of the time. So the null result
is uninformative rather than evidence that the change did nothing - the trial was too
small to settle the question either way. At rates near 1,000 DPMO a fair test needs
tens of thousands of units per side, or a measured variable instead of a pass/fail call.

**What the change physically was, I cannot report.** I asked the process owner and no
process facts are recorded for this project, so the record shows a change with no
description of what was done to which machine. That is a gap in the project record,
not something I will fill with a guess - and it means the change is not reproducible
even if it had worked.

## 6. How is it being held?

The monitoring record since the change covers 20 subgroups of 5,000, 100000 units, 107
defective:

- centre line **1070 DPMO**, process Z = 3.07
- **0 of 20 subgroups outside the control limits** - in control
- worst subgroup 2400 DPMO
- still below the commitment: p = 2.71e-04, 95% CI 877 to 1293 DPMO

Against the baseline: 1016 DPMO before, 1070 DPMO since (z = 0.39, p = 0.693).
**No significant difference - the line is exactly where it started.** The monitoring
record shows a process being held, not improved.

## 7. Where this project stands, and what to do next

Position: stable, inside the charter as inspected, with no demonstrated improvement
and an inspection system that is not fit to certify any of it.

1. **Fix the appearance judgement first.** Written standard with boundary samples for
   each reject category, retrain and requalify all three inspectors, then repeat this
   study and require kappa at or above 0.90 before trusting any rate. Everything else
   on this project is waiting on this; the current worst kappa is 0.348.
2. **Do not roll out the machine change.** It showed 1500 DPMO going to 2250 DPMO with
   power of 0.122. Get the change documented, then retest properly once inspection is
   trustworthy, sized to the effect you actually need to see.
3. **Keep machine 4 as the lead** (2000 DPMO against 0 on machine 2), but confirm it on a bigger
   window after the gauge is fixed, and make sure inspector is not confounded with
   machine when you do.
4. **Hold with the p chart** at a centre line of 1070 DPMO and react to points outside
   the limits rather than to ordinary lot-to-lot movement. Recompute the limits once
   inspection has been requalified, because today's centre line partly reflects
   measurement error.
5. **Do not run a single-category improvement** on the current tally: the biggest
   category is 26.7% of rejects, so the gain available is limited. Revisit the split
   after requalification, since some of the current categorisation is unreliable too.

## Data I could not obtain

All seven data batches held by the steward were released and analysed; none was denied.
The process owner holds no process facts for this project, so two questions went
unanswered: what the change to the machine actually was, and whether inspectors work to
a written standard with boundary samples. Both are stated as gaps above rather than
assumed. Every number in this report is computed on this run and traceable to
`/workspace/trace.json`.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"quality.pareto","inputs_digest":{"batch":"candidates","nCategories":5,"totalRejects":240},"outputs":{"topCategoryPct":26.666666666666668},"status":"success","decision":"Largest reject category is \"loose end\" at 26.7% of 240 rejects. No single category dominates, so a Pareto-led attack on one category is not justified."}
{"step_id":2,"method_id":"quality.fmea_rpn","inputs_digest":{"batch":"failure_modes","nModes":5},"outputs":{"maxRpn":504},"status":"success","decision":"Highest risk mode is \"stain\" at RPN 504, driven by a detection rating of 8 - i.e. the top risk is that the defect is not reliably caught by inspection, pointing at the measurement system."}
{"step_id":3,"method_id":"msa.attribute_agreement","inputs_digest":{"batch":"agreement","nParts":20,"nAppraisers":3,"nTrials":2,"standardKnown":true},"outputs":{"kappaMin":0.3478260869565216,"agreementPct":30.0,"allVsStandardPct":30.0,"withinAppraiser1Pct":85.0,"withinAppraiser2Pct":70.0,"withinAppraiser3Pct":55.0,"appraiser1VsStandardPct":70.0,"appraiser2VsStandardPct":55.0,"appraiser3VsStandardPct":50.0,"msaAcceptable":false},"status":"success","decision":"FAIL. Worst Cohen kappa vs the answer key is 0.348, far below the 0.75 acceptability floor; all three appraisers agree with each other on only 30% of units and repeatability is as low as 55%. The pass/fail judgement cannot be relied on, so every downstream defective rate in this project inherits that doubt."}
{"step_id":4,"method_id":"control_chart.p","inputs_digest":{"batch":"lots","nSubgroups":25,"subgroupSize":5000,"totalInspected":125000.0},"outputs":{"centerLine":0.001016,"outOfControlCount":0,"centerLineDpmo":1016.0,"uclCounts":11.838220807283525,"maxLotDpmo":2200.0,"minLotDpmo":400.0},"status":"success","decision":"Stable. 0 of 25 lots outside the limits, so the defective share has held steady across the twenty-five lots at a centre line of 1016 DPMO. Lot-to-lot variation is common cause."}
{"step_id":5,"method_id":"capability.binomial","inputs_digest":{"batch":"lots","totalInspected":125000.0,"totalDefective":127.0},"outputs":{"avgP":0.001016,"processZ":3.085514962525518,"avgPDpmo":1016.0},"status":"success","decision":"Baseline capability: average defective share 1016 DPMO, process Z = 3.09."}
{"step_id":6,"method_id":"basic.one_proportion","inputs_digest":{"batch":"lots","defective":127.0,"inspected":125000.0,"requirementDpmo":1500,"test":"exact binomial"},"outputs":{"pValue":3.343274718111073e-06,"pValueOneSidedLess":1.7104055691204832e-06,"observedDpmo":1016.0,"requirementDpmo":1500,"ci95LowDpmo":847.0616299858289,"ci95HighDpmo":1208.7306576750684},"status":"success","decision":"Observed 1016 DPMO is significantly below the 1500 DPMO commitment (exact binomial p = 3.34e-06 two-sided; 95% CI 847 to 1209 DPMO, entirely below the limit). The charter is being met on the numbers as inspected."}
{"step_id":7,"method_id":"tables.chisquare_assoc","inputs_digest":{"batch":"machines","nGroups":4,"totalUnits":16000.0,"dof":3,"minExpectedCount":4.0},"outputs":{"statistic":8.508508508508509,"pValue":0.036592216119949804,"worstMachineDpmo":2000.0,"bestMachineDpmo":0.0,"machineTotalUnits":16000.0,"machineTotalDefective":16.0,"dof":3,"minExpectedCount":4.0,"machine1Dpmo":1250.0,"machine2Dpmo":0.0,"machine3Dpmo":750.0,"machine4Dpmo":2000.0},"status":"success","decision":"Defective share is not the same on all four machines (chi-square = 8.51, dof 3, p = 0.0366): machine 4 runs at 2000 DPMO against 0 DPMO on machine 2. Caveat: the smallest expected count is 4.0, below the usual 5, so the p-value is approximate and this is a lead rather than a proven cause."}
{"step_id":8,"method_id":"basic.two_proportions","inputs_digest":{"batch":"after_change","events1":6,"n1":4000,"events2":9,"n2":4000},"outputs":{"pValue":0.4381483041479318,"zStatistic":0.77532387641392,"fisherPValue":0.6068946732696925,"beforeDpmo":1500.0,"afterDpmo":2250.0},"status":"success","decision":"No improvement demonstrated. The machine ran 1500 DPMO before the change and 2250 DPMO after - the wrong direction - and the difference is not significant (z = 0.78, p = 0.438; Fisher exact p = 0.607). The change cannot be credited with any gain."}
{"step_id":9,"method_id":"power.two_proportions","inputs_digest":{"batch":"after_change","n1":4000,"n2":4000,"alpha":0.05,"alternative":"two-sided"},"outputs":{"power":0.12194034803316639,"powerToDetectHalving":0.17384688429477152},"status":"success","decision":"The change trial was badly underpowered: power at the observed effect is 0.122, and even a genuine halving of the before-rate would have been caught only 17% of the time at 4000 units per side. The trial could not have proved success even if the change had worked, so its null result is uninformative rather than evidence of no effect."}
{"step_id":10,"method_id":"control_chart.p","inputs_digest":{"batch":"sustaining","nSubgroups":20,"subgroupSize":5000,"totalInspected":100000.0},"outputs":{"centerLine":0.00107,"outOfControlCount":0,"centerLineDpmo":1070.0,"uclCounts":12.285306734384571,"maxSubgroupDpmo":2400.0},"status":"success","decision":"Monitoring record since the change is in control: 0 of 20 subgroups outside the limits, centre line 1070 DPMO. Holding, not improving."}
{"step_id":11,"method_id":"capability.binomial","inputs_digest":{"batch":"sustaining","totalInspected":100000.0,"totalDefective":107.0},"outputs":{"avgP":0.00107,"processZ":3.0700820102708946,"avgPDpmo":1070.0},"status":"success","decision":"Post-change capability 1070 DPMO, process Z = 3.07, against baseline Z = 3.09. Essentially unchanged."}
{"step_id":12,"method_id":"basic.two_proportions","inputs_digest":{"batches":"lots vs sustaining","n1":125000.0,"n2":100000.0},"outputs":{"pValue":0.692930343326612,"zStatistic":0.3948815004841737,"baselineDpmo":1016.0,"sustainingDpmo":1070.0},"status":"success","decision":"Baseline 1016 DPMO vs 1070 DPMO since the change: no significant difference (z = 0.39, p = 0.693). The line is where it was."}
{"step_id":13,"method_id":"basic.one_proportion","inputs_digest":{"batch":"sustaining","defective":107.0,"inspected":100000.0,"requirementDpmo":1500,"test":"exact binomial"},"outputs":{"pValue":0.000270879290475796,"observedDpmo":1070.0,"requirementDpmo":1500,"ci95LowDpmo":876.9711323137236,"ci95HighDpmo":1292.8412876225486},"status":"success","decision":"Since the change the line runs 1070 DPMO, still significantly below the 1500 DPMO commitment (p = 2.71e-04; 95% CI 877 to 1293 DPMO)."}
```

## Submitted route declarations
```json
[{"point":"measurement_system_trustworthy","chosen_branch":"no - attribute agreement fails, all later rates are provisional","observed":{"kappaMin":0.3478260869565216,"agreementPct":30.0,"threshold":0.75}},{"point":"lot_stability","chosen_branch":"stable - treat variation as common cause, do not chase individual lots","observed":{"outOfControlCount":0,"nSubgroups":25,"centerLineDpmo":1016.0}},{"point":"capability_vs_charter","chosen_branch":"commitment met on the numbers as inspected","observed":{"observedDpmo":1016.0,"requirementDpmo":1500,"pValue":3.343274718111073e-06}},{"point":"source_of_defectives","chosen_branch":"machine-to-machine difference pursued as the lead","observed":{"pValue":0.036592216119949804,"statistic":8.508508508508509,"minExpectedCount":4.0}},{"point":"did_the_change_work","chosen_branch":"not demonstrated - underpowered trial, rate moved the wrong way","observed":{"beforeDpmo":1500.0,"afterDpmo":2250.0,"pValue":0.4381483041479318,"power":0.12194034803316639}},{"point":"control_plan","chosen_branch":"p chart on the monitoring record; hold, and fix the gauge first","observed":{"outOfControlCount":0,"centerLineDpmo":1070.0,"pValue":0.692930343326612}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
