# Blind item V051

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
# Chip-capacitor defect-share project report

## Executive conclusion

The baseline process was statistically steady but not capable of meeting the commitment. Across **25** baseline lots, there were **599** defects in **100000** inspected, for a pooled share of **0.00599**, versus the committed maximum of **0.0025**. After the line change, the trial and subsequent lots both show a materially lower level. Across the subsequent **20** lots, the pooled share is **0.0018375**, and the available evidence supports that it is below the commitment. The result should now be held with a documented settings plan and a continuing p chart.

## Baseline: steady, but at the wrong level

The baseline p chart had center line **0.00599**, lower limit **0.002329840198160741**, upper limit **0.009650159801839258**, and **0** out-of-control lots. Thus the lot sequence is consistent with a stable common-cause process at the observed level; stability does not imply acceptable performance.

An exact one-sided one-proportion test against the required share of **0.0025** returned **2.73393804200261e-78**. The baseline is therefore demonstrably above the commitment. Its binomial performance summary is average defect share **0.00599** and process Z **2.5127328988583177**.

## What on file accounts for variation

The specified OLS model used **40** per-lot records and included paste thickness, reflow peak, and their interaction. The overall model p-value was **8.381756185366403e-14**, with R-squared **82.72578038855495** and adjusted R-squared **81.28626208760119**. The paste-thickness, reflow-peak, and interaction p-values were respectively **1.0930398582647192e-11**, **8.322450533508334e-11**, and **7.095312426248996e-12**, all below the analysis alpha of **0.05**. These settings strongly account for recorded lot-to-lot variation in an associational model; observational regression alone does not establish causation.

The records do not identify the exact setting values implemented as the line change. A process-owner query found no recorded process fact, so the precise intervention and its documented hold mechanism could not be established and are not guessed here.

## Did the change do anything?

The trial design used **40000** units per group, alpha **0.05**, and planning shares **0.0059** and **0.0025**. Computed two-sided power was **0.9999999914471074**.

In the actual trial, the before window had **235** defects in **40000** inspected, or **0.005875**; the after window had **77** in **40000**, or **0.001925**. The absolute reduction was **0.00395**, the relative reduction was **0.672340425531915**, and the pooled two-proportion z statistic was **8.962482483814625** with p-value **3.1744942874845076e-19**. The confidence interval for the before-minus-after difference was **0.003086626479392266** to **0.004813373520607734**. The trial therefore provides strong evidence that the change reduced defects.

## Is the level reached enough, and is it holding?

The subsequent run contained **147** defects in **80000** inspected, giving **0.0018375**. Its p chart center line was **0.0018375**, lower limit **0**, upper limit **0.0038689472884959383**, with **0** out-of-control lots. On these **20** lots, the new level is statistically stable.

Against the commitment of **0.0025**, the exact one-sided test p-value is **5.060125914974411e-05**, supporting that the current defect share is below the required maximum. The post-change binomial process Z is **2.9047896420453334** at average defect share **0.0018375**.

## Recommended next actions

- Treat the current level as meeting the commitment on the available evidence, while continuing per-lot p-chart monitoring.
- Recover and approve the missing change record: exact paste-thickness and reflow-peak settings, allowed operating ranges, owners, reaction plan, and change-control requirements.
- Lock the approved settings into standard work and verify them at lot release. Because the fitted interaction is significant, manage the two settings jointly rather than one at a time.
- Investigate any future p-chart signal under the reaction plan and continue periodic pooled comparison with the committed share.
- Do not claim the regression proves the settings caused the improvement until the exact intervention is documented and, if needed, confirmed through a controlled experiment.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"baseline","groups":25,"totalInspected":100000},"method_id":"control_chart.p","outputs":{"centerLine":0.00599,"outOfControlCount":0,"lcl":0.002329840198160741,"ucl":0.009650159801839258,"lotCount":25,"totalDefects":599,"totalInspected":100000},"status":"success","decision":"No points beyond three-sigma limits; baseline treated as stable."}
{"step_id":2,"inputs_digest":{"batch":"baseline","totalInspected":100000},"method_id":"basic.one_proportion","outputs":{"pValue":2.73393804200261e-78,"observedShare":0.00599,"requiredShare":0.0025},"status":"success","decision":"One-sided exact binomial test finds baseline defect share above the commitment."}
{"step_id":3,"inputs_digest":{"batch":"baseline","totalInspected":100000},"method_id":"capability.binomial","outputs":{"processZ":2.5127328988583177,"avgP":0.00599},"status":"success","decision":"Baseline binomial defect performance summarized as long-term yield Z without shift."}
{"step_id":4,"inputs_digest":{"batch":"settings","groups":40,"terms":3},"method_id":"regression.ols","outputs":{},"status":"failed","decision":"Initial computation failed because a dictionary was passed where a numeric design matrix was required; no numerical result was produced."}
{"step_id":5,"inputs_digest":{"batch":"settings","groups":40,"terms":3},"method_id":"regression.ols","outputs":{"modelPValue":8.381756185366403e-14,"rSquaredPct":82.72578038855495,"rSquaredAdjPct":81.28626208760119,"fStatistic":57.467682302993225,"pastePValue":1.0930398582647192e-11,"reflowPValue":8.322450533508334e-11,"interactionPValue":7.095312426248996e-12,"alpha":0.05,"observationCount":40},"status":"success","decision":"Specified model is significant and each supplied term is significant at alpha; evidence is associational, not proof of causation."}
{"step_id":6,"inputs_digest":{"batch":"trial_size","nPerGroup":40000},"method_id":"power.two_proportions","outputs":{"power":0.9999999914471074,"alpha":0.05,"nPerGroup":40000,"planningP1":0.0059,"planningP2":0.0025},"status":"success","decision":"Planned two-sided two-proportion trial had essentially complete power for its specified difference."}
{"step_id":7,"inputs_digest":{"batch":"before_after","groups":2,"totalInspected":80000},"method_id":"basic.two_proportions","outputs":{"pValue":3.1744942874845076e-19,"zStatistic":8.962482483814625,"beforeShare":0.005875,"afterShare":0.001925,"absoluteReduction":0.00395,"relativeReduction":0.672340425531915,"differenceCiLower":0.003086626479392266,"differenceCiUpper":0.004813373520607734,"beforeDefects":235,"afterDefects":77,"nPerGroup":40000},"status":"success","decision":"Two-sided pooled z-test shows a statistically significant reduction after the change."}
{"step_id":8,"inputs_digest":{"batch":"after_lots","groups":20,"totalInspected":80000},"method_id":"control_chart.p","outputs":{"centerLine":0.0018375,"outOfControlCount":0,"lcl":0,"ucl":0.0038689472884959383,"lotCount":20,"totalDefects":147,"totalInspected":80000},"status":"success","decision":"No post-change lots exceed three-sigma p-chart limits; current level is stable on this evidence."}
{"step_id":9,"inputs_digest":{"batch":"after_lots","totalInspected":80000},"method_id":"basic.one_proportion","outputs":{"pValue":5.060125914974411e-05,"observedShare":0.0018375,"requiredShare":0.0025},"status":"success","decision":"One-sided exact binomial test supports that the post-change defect share is below the commitment."}
{"step_id":10,"inputs_digest":{"batch":"after_lots","totalInspected":80000},"method_id":"capability.binomial","outputs":{"processZ":2.9047896420453334,"avgP":0.0018375},"status":"success","decision":"Post-change binomial defect performance summarized as long-term yield Z without shift."}
```

## Submitted route declarations
```json
[{"point":"baseline_stability_gate","chosen_branch":"stable","observed":{"outOfControlCount":0,"centerLine":0.00599,"lcl":0.002329840198160741,"ucl":0.009650159801839258}},{"point":"settings_significance_gate","chosen_branch":"any_factor_significant_true","observed":{"alpha":0.05,"modelPValue":8.381756185366403e-14,"pastePValue":1.0930398582647192e-11,"reflowPValue":8.322450533508334e-11,"interactionPValue":7.095312426248996e-12}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
