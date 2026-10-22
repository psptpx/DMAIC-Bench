# Blind item B002

Focal assessment: Whether the absolute post-change business level supports target attainment or closure.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team on a chip-capacitor line. Every unit is inspected and the project has committed to holding the defect share at or below 0.25% of units inspected. On file are the inspected and defective counts for twenty-five consecutive baseline lots; a per-lot record of two line settings alongside that lot's defect share; the inspected and defective totals for one window before a change was made to the line and one window after it; the inspected and defective counts for twenty lots run since the change; and the size and risk level the before-and-after trial was run at.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the defect share held steady across the baseline, how it compares with what was committed to, whether anything on file accounts for it, whether the change that was made can be shown to have done anything, whether the level reached since is enough, and what should happen next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
{"screening_significant":{"field":"any_factor_significant","op":"==","value":true,"source":"Montgomery DAOE 6e 11.2"},"stability_pass":{"field":"stable","op":"==","value":true,"source":"AIAG SPC-2 Ch. I Sec. F; Montgomery ISQC 6e 8.1"}}
```

## Submitted report (complete, identifiers removed)
# Project Report: Chip-Capacitor Defect Share

## Bottom line
The line is currently stable and its defect share is below the committed level. The baseline was stable but not capable against the commitment. The settings model identifies paste thickness, reflow peak, and their interaction as strongly associated with lot defect share. The change was followed by a significant reduction, and the post-change lots have remained below target.

## Baseline
Across 25 baseline lots of 4000 units each, there were 599 defects in 100000 inspected units, a defect share of 0.00599 (0.599%). The p chart centerline was 0.00599 and 0 lots were outside the control limits. Against the required share of 0.0025 (0.25%), the one-proportion test gave z = 22.10034078145949, normal-approximation p = 3.136907093091575e-108, and exact binomial p = 3.7306979805640508e-78. The baseline was statistically stable but well above the commitment.

## What accounts for the baseline level
An OLS model on 40 lots from the line-settings batch related lot defect share to paste thickness, reflow peak, and their interaction. The model p-value was 8.381756185366018e-14, with R-squared = 82.72578038855498% and adjusted R-squared = 81.28626208760123%. The paste-thickness p-value was 1.0930398582646995e-11, the reflow-peak p-value was 8.322450533508093e-11, and the interaction p-value was 7.095312426248794e-12. These settings terms are strongly associated with the lot defect share.

## What the change achieved
The before window had 235 defects in 40000 units (0.005875, or 0.5875%). The after window had 77 defects in 40000 units (0.001925, or 0.1925%). The absolute reduction was 0.00395 (0.395 percentage points), with a two-proportion z = 8.962482483814625 and p = 3.174494287484549e-19. The planned comparison used alpha = 0.05, 40000 units per group, p1 = 0.0059, and p2 = 0.0025; its computed power was 0.9999999914471074. The change was followed by a statistically significant improvement.

## Since the change
The 20 post-change lots contained 80000 inspected units and 147 defects, a share of 0.0018375 (0.18375%). The post-change p chart had centerline 0.0018375 and 0 out-of-control lots. Against the required share of 0.0025, the exact one-proportion p-value was 9.717173745815809e-05. The post-change lots were not detectably different from the immediate post-change trial window (z = -0.3310280176820626, p = 0.7406233224472969). Combining all post-change data gives 224 defects in 120000 inspected units, a share of 0.0018666666666666666 (0.18666666666666668%); the test against the required share gave z = -4.393357178922209 and p = 1.1161352409798517e-05. The level reached since the change is below the commitment.

## Recommended next step
Hold the changed line settings and continue to monitor the defect share with the p chart. All requested data batches were released, so no conclusion here is blocked by missing data. The before/after data establish a statistically significant improvement, but they are not a randomized trial, so the evidence supports association rather than definitive causal proof.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"baseline","nLots":25,"subgroupSize":4000},"method_id":"meta.data_profiling","outputs":{"nLots":25,"subgroupSize":4000,"totalDefects":599,"totalInspected":100000,"defectShare":0.00599,"defectSharePct":0.599,"requiredShare":0.0025,"requiredSharePct":0.25},"status":"success","decision":null}
{"step_id":2,"inputs_digest":{"batch":"baseline","nLots":25,"subgroupSize":4000},"method_id":"control_chart.p","outputs":{"centerLine":0.00599,"outOfControlCount":0,"uclCount":38.600639207357034,"lclCount":9.319360792642964},"status":"success","decision":"stable_above_commitment"}
{"step_id":3,"inputs_digest":{"batch":"baseline","defects":599,"inspected":100000,"target":0.0025},"method_id":"basic.one_proportion","outputs":{"pValue":3.136907093091575e-108,"exactPValue":3.7306979805640508e-78,"zStatistic":22.10034078145949,"observedShare":0.00599,"requiredShare":0.0025},"status":"success","decision":"above_commitment"}
{"step_id":4,"inputs_digest":{"batch":"settings","nObservations":40,"terms":["paste_thickness","reflow_peak","paste_x_reflow"]},"method_id":"regression.ols","outputs":{"modelPValue":8.381756185366018e-14,"rSquaredPct":82.72578038855498,"rSquaredAdjPct":81.28626208760123,"nObservations":40,"pastePValue":1.0930398582646995e-11,"reflowPValue":8.322450533508093e-11,"interactionPValue":7.095312426248794e-12,"pasteCoefficient":-0.13285132585922493,"reflowCoefficient":-0.0007886359111256776,"interactionCoefficient":0.0005487401951439041},"status":"success","decision":"any_factor_significant"}
{"step_id":5,"inputs_digest":{"p1":0.0059,"p2":0.0025,"nPerGroup":40000,"alpha":0.05},"method_id":"power.two_proportions","outputs":{"power":0.9999999914471074,"effectSize":0.0537326663641023,"alpha":0.05,"nPerGroup":40000,"p1":0.0059,"p2":0.0025},"status":"success","decision":"adequate_power"}
{"step_id":6,"inputs_digest":{"beforeEvents":235,"beforeTrials":40000,"afterEvents":77,"afterTrials":40000},"method_id":"basic.two_proportions","outputs":{"zStatistic":8.962482483814625,"pValue":3.174494287484549e-19,"events1":235,"trials1":40000,"events2":77,"trials2":40000,"p1":0.005875,"p2":0.001925,"p1Pct":0.5875,"p2Pct":0.1925,"absoluteReduction":0.00395,"absoluteReductionPctPoints":0.395},"status":"success","decision":"after_lower_than_before"}
{"step_id":7,"inputs_digest":{"window":"after_trial","events":77,"trials":40000,"target":0.0025},"method_id":"basic.one_proportion","outputs":{"pValue":0.02128557311974885,"zStatistic":-2.3028804018800906,"observedShare":0.001925,"events":77,"trials":40000,"target":0.0025},"status":"success","decision":"below_target"}
{"step_id":8,"inputs_digest":{"batch":"after_lots","nLots":20,"subgroupSize":4000},"method_id":"control_chart.p","outputs":{"centerLine":0.0018375,"outOfControlCount":0,"uclCount":15.475789153983753,"lclCount":0,"nLots":20,"subgroupSize":4000,"totalDefects":147,"totalInspected":80000,"defectShare":0.0018375,"defectSharePct":0.18375},"status":"success","decision":"stable"}
{"step_id":9,"inputs_digest":{"batch":"after_lots","defects":147,"inspected":80000,"target":0.0025},"method_id":"basic.one_proportion","outputs":{"pValue":9.717173745815809e-05,"exactPValue":9.717173745815809e-05,"observedShare":0.0018375,"requiredShare":0.0025},"status":"success","decision":"below_commitment"}
{"step_id":10,"inputs_digest":{"afterLotsEvents":147,"afterLotsTrials":80000,"trialAfterEvents":77,"trialAfterTrials":40000},"method_id":"basic.two_proportions","outputs":{"zStatistic":-0.3310280176820626,"pValue":0.7406233224472969,"p1":0.0018375,"p2":0.001925,"events1":147,"trials1":80000,"events2":77,"trials2":40000},"status":"success","decision":"no_detectable_difference"}
{"step_id":11,"inputs_digest":{"combinedPostEvents":224,"combinedPostTrials":120000,"target":0.0025},"method_id":"basic.one_proportion","outputs":{"pValue":1.1161352409798517e-05,"zStatistic":-4.393357178922209,"observedShare":0.0018666666666666666,"events":224,"trials":120000,"target":0.0025,"observedSharePct":0.18666666666666668},"status":"success","decision":"below_commitment"}
```

## Submitted route declarations
```json
[{"point":"baseline_stability","chosen_branch":"stable","observed":{"outOfControlCount":0,"centerLine":0.00599}},{"point":"settings_significance","chosen_branch":"any_factor_significant","observed":{"modelPValue":8.381756185366018e-14,"rSquaredPct":82.72578038855498}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
