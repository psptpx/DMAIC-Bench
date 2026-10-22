# Blind item V026

Focal assessment: Causal judgments and next steps after candidate machine-difference analysis.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

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
# Project status report

## 1. Can the sound/defective judgement be relied on?

The inspector study against the answer key gives an overall agreement of `93.33%` and an overall appraiser-vs-standard kappa of `0.855` (step 1). The minimum appraiser-vs-standard kappa is `0.681`, and the minimum within-appraiser kappa is `0.659`. That is moderate but below the common desirable kappa threshold of 0.75, so the judgement can be used for this investigation, but the inspection process should be improved before it is considered reliable enough for long-term routine decision-making.

## 2. Has the defective share held steady across the lots?

The 25-lot record contains `25` lots of `5000` inspected units each, with a total of `322` defective units and `125000` inspected units (step 2). The p-chart center line is `0.002576` (`2576` DPMO), with control limits `0.000425` and `0.004727`. The number of out-of-control lots is `0`. The defective share is therefore stable across the lots at an average above the charter target.

## 3. How does the 25-lot period compare with the charter?

The charter target is 1500 DPMO. The 25-lot average is `2576` DPMO, and a one-proportion test against 1500 DPMO gives `z = 9.830` and `p = 0.000000` (step 3). The lot record is significantly worse than the committed maximum level.

## 4. What is causing the defects?

The reject-category tally shows that `loose end` is the largest category, accounting for `30.42%` of the recorded reject count (step 4). The risk-rated failure-mode table gives the highest RPN to `seam split`, with `maxRpn = 360` (step 5). So the biggest observed category is loose end, while the highest-risk failure mode by RPN is seam split.

## 5. Are machine differences driving the defect share?

The machine-by-machine defective/sound tally yields a chi-square statistic of `2.578` with `p = 0.461` (step 6). There is no statistically significant association between machine identity and defect outcome in this window; the machine differences alone do not explain the charter miss.

## 6. What did the change achieve?

On the one machine with before/after data, the defect share moved from `1500` DPMO before the change to `2750` DPMO after the change, with `z = 1.214` and `p = 0.225` (step 7). The difference is not statistically significant and is numerically worse after the change, so this single before/after snapshot does not demonstrate an improvement from that change.

## 7. Where does the process stand today?

The sustaining record kept since the change has `100000` inspected and `104` defective units, for `1040` DPMO (step 8). Against the 1500 DPMO charter target, the test yields `z = -3.759` and `p = 0.000171`. The current sustaining record is therefore below the committed level, and the difference is statistically significant.

## 8. What should be done next?

Although current sustaining data are below the 1500 DPMO target, the historical 25-lot period was stable but above target, the measurement system is only moderately reliable, and the immediate before/after change snapshot did not show a significant improvement. The next steps should be:

1. Improve the inspection method, focusing on within-appraiser and appraiser-vs-standard agreement, then rerun the measurement system study before relying on counts for routine disposition.
2. Investigate `loose end`, the top reject category, and `seam split`, the highest-RPN failure mode, through process and defect-data investigations.
3. Use the sustaining record as a provisional control metric but validate with the improved measurement system.
4. Continue sampling after the change to confirm the current below-target level is sustainable rather than a short-run fluctuation.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"agreement","n_referents":20,"n_appraisers":3,"n_trials":2},"method_id":"msa.attribute_agreement","outputs":{"kappaMin":0.6808510638297872,"agreementPct":93.33333333333333,"withinKappaMin":0.6590909090909091,"overallKappaVsStandard":0.855072463768116,"correct":112,"comparisons":120},"status":"success","decision":"The sound/defective judgement has moderate reliability: high overall agreement but minimum appraiser-vs-standard kappa is below the usual 0.75 threshold."}
{"step_id":2,"inputs_digest":{"batch":"lots","n_lots":25,"lot_size":5000},"method_id":"control_chart.p","outputs":{"centerLine":0.002576,"outOfControlCount":0,"individualsUCL":0.004726547744924535,"individualsLCL":0.00042545225507546573,"pBarDpmo":2576.0,"totalInspected":125000,"totalDefects":322,"nLots":25},"status":"success","decision":"No lot is outside the 3-sigma p-chart limits; the defective share is stable across the 25 lots."}
{"step_id":3,"inputs_digest":{"batch":"lots","comparison":"1500 DPMO charter target"},"method_id":"basic.one_proportion","outputs":{"pValue":0.0,"zStatistic":9.829866364424648,"pBarDpmo":2576.0,"targetDpmo":1500,"totalDefects":322,"totalInspected":125000},"status":"success","decision":"The overall lot defective share is above the charter target, with p < 0.0001 against 1500 DPMO."}
{"step_id":4,"inputs_digest":{"batch":"candidates","n_categories":5},"method_id":"quality.pareto","outputs":{"topCategoryPct":30.416666666666668,"topCategoryCount":73,"totalCategoryCount":240},"status":"success","decision":"The top reject category is loose end at about 30.4% of the recorded reject count."}
{"step_id":5,"inputs_digest":{"batch":"failure_modes","n_modes":5},"method_id":"quality.fmea_rpn","outputs":{"maxRpn":360},"status":"success","decision":"Seam split has the highest RPN (360), driven by severity 9 and detection 8."}
{"step_id":6,"inputs_digest":{"batch":"machines","n_machines":4,"n_outcome_categories":2},"method_id":"tables.chisquare_assoc","outputs":{"statistic":2.578196336812705,"pValue":0.4613248388721344,"degreesOfFreedom":3},"status":"success","decision":"No statistically significant machine-to-defect association was found; machine differences alone do not explain the defect pattern."}
{"step_id":7,"inputs_digest":{"batch":"after_change","n_before":4000,"n_after":4000},"method_id":"basic.two_proportions","outputs":{"pValue":0.22475969475491575,"zStatistic":1.2139686528327227,"pBefore":0.0015,"pAfter":0.00275,"dBefore":6,"dAfter":11,"nBefore":4000,"nAfter":4000},"status":"success","decision":"Before-vs-after on the changed machine is not statistically significant, and the after period is numerically higher in defect share."}
{"step_id":8,"inputs_digest":{"batch":"sustaining","n_records":20,"record_size":5000,"comparison":"1500 DPMO charter target"},"method_id":"basic.one_proportion","outputs":{"pValue":0.00017079550662235654,"zStatistic":-3.758704358465586,"pBarDpmo":1040.0,"targetDpmo":1500,"totalDefects":104,"totalInspected":100000,"nRecords":20},"status":"success","decision":"The current sustaining record is below the charter target and the difference against 1500 DPMO is statistically significant."}
```

## Submitted route declarations
```json
[{"point":"proceed_after_measurement_system_assessment","chosen_branch":"proceed_with_available_data","observed":{"kappaMin":0.6808510638297872,"agreementPct":93.33333333333333}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
