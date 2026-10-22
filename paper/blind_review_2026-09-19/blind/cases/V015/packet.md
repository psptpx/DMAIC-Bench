# Blind item V015

Focal assessment: Whether the absolute post-change business level supports target attainment or closure.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

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
# Capacitor defect-share project report

## Executive summary

The baseline was stable but not compliant. Across **25** baseline lots, **546** defective units were found in **100000** inspected units, for a defect share of **0.00546**. The p-chart flagged **0** of the **25** lots. Thus the process was predictable, but its center was **2.184** times the committed share of **0.0025**; the exact one-sided comparison produced a p-value of **4.220242209124989e-59**.

The line improvement coincided with a substantial reduction. The before/after windows fell from **0.005925** to **0.003375**, a **43.0379746835443%** reduction, with a two-sided p-value of **1.1530117357517475e-07**. The **20** lots since the change are also stable, with **0** chart flags and a pooled share of **0.0034375**. However, they still contain **75** more defectives than the same **80000** units would contain at target, and the current share must fall another **27.272727272727273%** to reach the commitment. The change helped, but it did not close the gap.

## What the data show

### Baseline condition

The baseline aggregate was **546** defectives out of **100000** units. Its p-chart center line was **0.00546**, and no individual lot crossed the chart limits, so common-cause variation—not one isolated assignable lot—characterized the period. The aggregate share was significantly above **0.0025** (p-value **4.220242209124989e-59**), with **296** excess defectives relative to that commitment.

### Settings associated with the baseline response

A model using the supplied paste thickness, reflow peak, and their interaction was fitted to **40** records. Its overall p-value was **1.20039199680057e-06**, and it accounted for **56.426363457132034%** of response variation (adjusted **52.795227078559705%**). All three supplied model terms were significant: paste thickness p-value **1.5878687634538685e-05**, reflow peak p-value **3.647421126578713e-05**, and interaction p-value **1.2151358677491888e-05**. This identifies line-settings information that is on file and statistically associated with defect share; because these are observational lot records, it does not by itself prove a causal effect or identify an optimum.

### Effect of the change

The before window had **237** defectives in **40000** units (**0.005925**), while the after window had **135** in **40000** (**0.003375**). The two-proportion test gave z **-5.300792345784441** and p-value **1.1530117357517475e-07**, or **43.0379746835443%** relative improvement. The separate aggregate of lots since the change was also **37.04212454212454%** below the baseline share (p-value **2.48636583545256e-10**).

The trial was planned at **40000** units per group with alpha **0.05** to detect a change from **0.0059** to **0.0025**. Its computed power was **0.9999999914471074**, so lack of statistical evidence is not a concern; the detected before/after difference was nevertheless smaller than the target improvement.

### Current hold and remaining gap

The post-change lot set has **275** defectives out of **80000**, giving **0.0034375**. Its p-chart again showed **0** outliers, so the new level appears to be holding, but at **1.375** times the committed **0.0025**. The one-sided target comparison gave p-value **2.847837963216255e-07**. The computed Wilson interval was **0.003055072228494698** to **0.003867613591607647**, entirely above target. Meeting the commitment requires a further **27.272727272727273%** reduction from the current lot-share level.

## Limitation that stops a conclusion

No released data identifies the specific physical or procedural change. Process-owner requests were unroutable, and the steward reported no recorded process topics. Therefore, we cannot state what was changed, verify it was implemented as intended, or attribute the improvement specifically to that change rather than to another concurrent condition. That conclusion stops at the available data.

## Recommended actions

1. Obtain and document the actual change and its implementation evidence, then use a controlled confirmation trial to establish causation.
2. Use the significant settings relationship to guide a designed optimization; confirm the selected settings on independently inspected lots before rollout.
3. Continue the lot-level p-chart after the next intervention. Do not declare success until the stable center is at or below **0.0025**, not merely below the old baseline.
4. If the current settings do not reach the remaining **27.272727272727273%** reduction, escalate to the next identified design or material lever and recheck capability after the new lots accumulate.

One initial settings-model implementation failed before producing output; it is recorded as a failed trace step. The conclusions above use only the subsequently successful computations. No steward batch containing the process-change fact was denied outright, but none could be routed or released.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"source":"baseline.json","lots":25,"inspected":100000},"method_id":"control_chart.p","outputs":{"centerLine":0.00546,"outOfControlCount":0,"lowerControlLimitMin":0.001964585303572693,"upperControlLimitMax":0.008955414696427307,"observedProportion":0.00546,"defectives":546.0,"inspected":100000.0,"lotCount":25},"decision":"No plotted lot crossed three-sigma limits.","status":"success"}
{"step_id":2,"inputs_digest":{"source":"baseline.json","aggregateGroups":1,"defectives":546,"inspected":100000},"method_id":"basic.one_proportion","outputs":{"pValue":4.220242209124989e-59,"observedProportion":0.00546,"nullProportion":0.0025,"defectives":546,"inspected":100000,"ratioToTarget":2.184,"excessDefectivesVsTarget":296.0},"decision":"Observed share is significantly greater than the commitment.","status":"success"}
{"step_id":3,"inputs_digest":{"source":"settings.json","records":40,"predictors":2,"modelTerms":3},"method_id":"regression.ols","outputs":{},"status":"failed","decision":"First implementation failed on an internal import path; no result was produced."}
{"step_id":4,"inputs_digest":{"source":"baseline.json","lots":25,"inspected":100000},"method_id":"control_chart.p","outputs":{"centerLine":0.00546,"outOfControlCount":0,"lowerControlLimitMin":0.001964585303572693,"upperControlLimitMax":0.008955414696427307,"observedProportion":0.00546,"defectives":546.0,"inspected":100000.0,"lotCount":25},"decision":"No plotted lot crossed three-sigma limits.","status":"success"}
{"step_id":5,"inputs_digest":{"source":"after_lots.json","lots":20,"defectiveLots":20,"inspected":80000},"method_id":"control_chart.p","outputs":{"centerLine":0.0034375,"outOfControlCount":0,"lowerControlLimitMin":0.0006612096538838918,"upperControlLimitMax":0.006213790346116108,"observedProportion":0.0034375,"defectives":275.0,"inspected":80000.0,"lotCount":20},"decision":"No plotted post-change lot crossed its three-sigma limits.","status":"success"}
{"step_id":6,"inputs_digest":{"source":"baseline.json","aggregateGroups":1,"defectives":546,"inspected":100000},"method_id":"basic.one_proportion","outputs":{"pValue":4.220242209124989e-59,"observedProportion":0.00546,"nullProportion":0.0025,"defectives":546,"inspected":100000,"ratioToTarget":2.184,"excessDefectivesVsTarget":296.0},"decision":"Observed share is significantly greater than the commitment.","status":"success"}
{"step_id":7,"inputs_digest":{"source":"after.json","aggregateGroups":1,"defectives":275,"inspected":80000},"method_id":"basic.one_proportion","outputs":{"pValue":2.847837963216255e-07,"observedProportion":0.0034375,"nullProportion":0.0025,"defectives":275,"inspected":80000},"decision":"Observed share is significantly greater than the commitment.","status":"success"}
{"step_id":8,"inputs_digest":{"source":"before_after.json","groups":2,"inspectedPerGroup":40000},"method_id":"basic.two_proportions","outputs":{"pValue":1.1530117357517475e-07,"zStatistic":-5.300792345784441,"beforeProportion":0.005925,"afterProportion":0.003375,"differenceAfterMinusBefore":-0.0025499999999999997,"percentReductionFromBefore":43.0379746835443,"beforeDefectives":237,"afterDefectives":135,"beforeInspected":40000,"afterInspected":40000},"decision":"The post-change window is significantly lower than the before window.","status":"success"}
{"step_id":9,"inputs_digest":{"source":"trial_size.json","groups":2,"plannedNPerGroup":40000},"method_id":"power.two_proportions","outputs":{"power":0.9999999914471074,"alpha":0.05,"plannedBeforeProportion":0.0059,"plannedAfterProportion":0.0025,"nPerGroup":40000},"decision":"The design had essentially certain power for the planned 0.0059-to-0.0025 change.","status":"success"}
{"step_id":10,"inputs_digest":{"source":"settings.json","records":40,"predictors":2,"modelTerms":3},"method_id":"regression.ols","outputs":{"modelPValue":1.20039199680057e-06,"rSquaredPct":56.426363457132034,"rSquaredAdjPct":52.795227078559705,"fStatistic":15.539588044698402,"residualStandardError":0.0006013889412062952,"maximumTermPValue":3.647421126578713e-05,"pasteThicknessPValue":1.5878687634538685e-05,"reflowPeakPValue":3.647421126578713e-05,"interactionPValue":1.2151358677491888e-05,"pasteThicknessEstimate":-0.14070740096043682,"reflowPeakEstimate":-0.0008648128403685798,"interactionEstimate":0.0005832562392927196,"sampleSize":40,"predictorCount":2,"modelTermCount":3},"decision":"All specified model terms are significant; this is association, not proof of causation.","status":"success"}
{"step_id":11,"inputs_digest":{"source":"baseline_vs_after.json","groups":2,"inspected":[100000,80000]},"method_id":"basic.two_proportions","outputs":{"pValue":2.48636583545256e-10,"zStatistic":-6.327827674758111,"baselineProportionPct":0.5459999999999999,"afterProportionPct":0.34375,"differenceAfterMinusBaselinePct":-0.20224999999999996,"percentReductionFromBaseline":37.04212454212454},"decision":"The post-change lot aggregate is significantly below baseline.","status":"success"}
{"step_id":12,"inputs_digest":{"source":"after_lots.json","aggregateGroups":1,"defectives":275,"inspected":80000},"method_id":"basic.one_proportion","outputs":{"pValue":2.847837963216255e-07,"observedProportion":0.0034375,"nullProportion":0.0025,"ratioToTarget":1.375,"excessDefectivesVsTarget":75.0,"furtherReductionToTargetPct":27.272727272727273,"wilson95Lower":0.003055072228494698,"wilson95Upper":0.003867613591607647},"decision":"The post-change share remains significantly above target; the Wilson interval also excludes target.","status":"success"}
```

## Submitted route declarations
```json
[{"point":"baseline_stability_gate","chosen_branch":"stable","observed":{"outOfControlCount":0,"centerLine":0.00546}},{"point":"settings_factor_gate","chosen_branch":"any_factor_significant","observed":{"maximumTermPValue":3.647421126578713e-05,"modelPValue":1.20039199680057e-06}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
