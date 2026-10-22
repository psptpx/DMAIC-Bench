# Blind item V012

Focal assessment: Baseline defect-rate chart stability, business performance, and next steps.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team in a shared-services centre. The response commitment written into the customer contract is missed too often; internally we require that no more than 5% of tickets breach it. Twenty-five consecutive periods of ticket volume and breach counts have been exported. The archive also holds a study in which several reviewers each judged the same tickets against a known answer key, and a summary of two teams' intake and breaches over one common window.

## 2. What you are asked to do

Work through the batches the data steward can release and say where this project stands: whether a breach judgement can be relied on at all, whether the breach share has been steady across the periods, how far today's level sits from the internal requirement, and what should be done about it next. Every number in your report must come from a computation you ran on this task; where nothing was computed, draw no conclusion.


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
# Project Report: Breach Share and Response Commitment
## Data obtained
The steward released four batches: project charter/breach requirement (`define`), reviewer judgements against the answer key (`agreement`), team-by-team intake and breach summary (`root_cause`), and per-period ticket volume and breach counts (`subgroups`).
## Reliability of breach judgement
The reviewer study contained 120 appraiser-to-standard comparisons across 3 appraisers. The overall agreement was 95.0 percent and the minimum appraiser kappa was 0.7647058823529412. This supports relying on breach judgement, though appraiser-level agreement should continue to be monitored.
## Steadiness of breach share across periods
A p-chart was run on 25 consecutive periods with subgroup size 200. The center line was 0.0456 (4.56 percent). The upper control limit was 0.089854 and the lower control limit was 0.001346. The p-chart flags 1 out-of-control point, period 13, where the breach share was 0.22 (44 breaches in 200 tickets). Therefore the breach share has not been perfectly steady across the periods; one special-cause period is evident.
## Today's level versus the internal requirement
The latest period (25) had 4 breaches in 200 tickets. That is a breach share of 0.02 (2.00 percent), which is 0.030000000000000002 percentage points below the internal requirement of 0.05. An exact one-sided binomial test against 0.05 gives p = 0.0264. Current performance is below the 5 percent requirement with moderate statistical evidence.
## Team comparison
In the common window, team 1 had 30 breaches in 600 tickets (5.00 percent) and team 2 had 24 breaches in 600 tickets (4.00 percent). A two-proportion test gives z = 0.8355 and p = 0.4034. This indicates no statistically significant overall difference between the two teams in the common window.
## Cause, change, achievement, and control
We attempted to obtain process facts about the period-13 special cause and the current control plan, but both provision requests were refused as `unroutable`; the process engineer reported that no known process topics were recorded. Therefore no data is available to compute a specific cause, confirm what was changed, quantify what the change achieved, or confirm how the improvement will be held. The only data-based next step is to investigate the period-13 special cause and continue monitoring subsequent periods on the p-chart.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"source":"agreement.json","sample_size":120,"number_of_groups":3},"method_id":"msa.attribute_agreement","outputs":{"agreementPct":95.0,"kappaMin":0.7647058823529412,"totalComparisons":120,"matches":114},"status":"success","decision":"Overall agreement is high, and the minimum reviewer kappa is above 0.75; breach judgement can be relied on with caution."}
{"step_id":2,"inputs_digest":{"source":"root_cause.json","group_count":2,"group1_count":30,"group1_trials":600,"group2_count":24,"group2_trials":600},"method_id":"basic.two_proportions","outputs":{"pValue":0.40342950102782804,"zStatistic":0.8355119862887138,"group1Rate":0.05,"group2Rate":0.04,"group1Count":30,"group1Trials":600,"group2Count":24,"group2Trials":600},"status":"success","decision":"The two teams do not differ significantly in breach share over the common comparison window."}
{"step_id":3,"inputs_digest":{"source":"subgroups.json","period_count":25,"subgroup_size":200},"method_id":"control_chart.p","outputs":{"centerLine":0.0456,"outOfControlCount":1,"upperControlLimit":0.08985413878949629,"lowerControlLimit":0.0013458612105037154,"periodCount":25,"subgroupSize":200,"flaggedSubgroupIndex":13,"flaggedDefectCount":44,"flaggedProportion":0.22},"status":"success","decision":"The breach share is not perfectly steady; one period is outside the p-chart control limits."}
{"step_id":4,"inputs_digest":{"source":"subgroups.json","period":25,"defect_count":4,"sample_size":200,"target_rate":0.05},"method_id":"basic.one_proportion","outputs":{"pValue":0.026446800009119878,"proportion":0.02,"gapToTarget":0.030000000000000002,"defectCount":4,"sampleSize":200,"targetRate":0.05},"status":"success","decision":"The latest period is below the 5 percent requirement; exact one-sided test gives p=0.0264."}
```

## Submitted route declarations
```json
[]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
