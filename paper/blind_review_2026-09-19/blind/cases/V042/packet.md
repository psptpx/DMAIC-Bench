# Blind item V042

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
# Chip-capacitor defect-rate review

## Bottom line

The line is now stable, but it is not at the committed defect share. The baseline was also stable—this was a common-cause process operating far above commitment, not a special-cause outbreak. The later change is strongly associated with a large reduction, and the reduction persisted across the confirmation lots. Nevertheless, the confirmed level remains above commitment, so this is not a project close-out.

No process fact identifying the actual change was available. The measured before-and-after effect is established, but the available evidence does not support a named causal statement such as “changing parameter X caused the gain.”

## Baseline: steady, but not good

The commitment is a defect share of **0.0025** (0.25%). Across **25** consecutive baseline lots, inspection totaled **100,000** units and produced **1,785** defects. The p-chart center line was **0.01785** (1.785%), with 3-sigma limits of **0.011569426827510089** and **0.024130573172489914**. No lot was outside those limits (`outOfControlCount = 0`).

Thus, the baseline held steady, but at **7.14 times** commitment—**0.01535** above the required share. The capability calculation gave `processZ = 97.20350458321009`; here the positive Z indicates adverse performance above the committed maximum. The exact-test routine's p-value underflowed to zero, so the more stable evidence is the Z score and the directly measured excess.

## What the settings record accounts for

A separate record of **40** lots contains paste thickness, reflow peak, and lot defect share. The specified model with both settings and their interaction explained **74.49988903608033%** of lot-to-lot variation (adjusted R-squared **72.37487978908703%**; model p-value **8.844474875407327e-11**). Paste thickness, reflow peak, and their interaction were all significant, with coefficient p-values of **1.3832726192588158e-05**, **6.056350416391993e-05**, and **9.507904201668252e-06**, respectively. Residual normality was not contradicted (Shapiro-Wilk p-value **0.29056822668248805**).

This file therefore accounts statistically for variation in its own defect-share record, but it is observational. It cannot by itself prove causality, and its **40** rows cannot be merged row-for-row with the **25**-lot baseline count series.

## What the change achieved

The trial metadata specified **40000** units per window, alpha **0.05**, planning share **0.018** before, and planning share **0.0025** after; the computed effect size (Cohen h) was **0.1690980192630125** and nominal power was **1.0**.

Observed results were **731** defects among **40000** inspections before (**0.018275**) and **134** among **40000** after (**0.00335**). The absolute reduction was **0.014925**, or **81.66894664842681%**. The Newcombe 95% interval for after-minus-before was **-0.016380877730109874** to **-0.013516114185988718**. The two-proportion test gave z = **-20.409246334850078** and p = **1.3840232699771407e-92**.

So the change can be shown to have coincided with a large, statistically detectable reduction. However, this was a before-and-after comparison, not a randomized comparison, and the identity of the change is absent. The strong observed result supports that something happened; it does not identify which physical action was responsible.

The immediate after window itself was still above commitment: **0.0008500000000000001** above the **0.0025** target, **1.34** times target (exact two-sided p-value **0.0011121688607600864**).

## Level reached since the change

The separate confirmation record had **20** lots and **80000** inspections, with **269** defects. Its center line was **0.0033625** (0.33625%), with p-chart limits of **0.000616560163452684** and **0.006108439836547316**; no lot was outside the limits (`outOfControlCount = 0`). Thus, the new level also held steady under the pointwise control-chart criterion.

It was consistent with the separate immediate after window (z = **0.03528279319945898**, p = **0.9718542438256355**). But it remained **0.0008625** above commitment—**1.345** times the target. The exact 95% share interval was **0.0029732061340359667** to **0.0037884650838915165**, entirely above **0.0025**; the one-sided greater-than-target p-value was **1.936949216991863e-06**. Compared with the allowed count, those **80000** inspections included **69** excess defects. A further reduction of **25.650557620817843%** in the current defect rate is needed to reach **0.0025**. The post-change binomial capability calculation remained adverse, with `processZ = 4.885147045293041`.

## What should happen next

- **Keep the changed configuration in place.** It is strongly associated with a reduction from **0.018275** to **0.00335**, and the **20**-lot record confirms a steady new level.
- **Do not close against the commitment.** The confirmed level is **0.0033625**, not **0.0025**; **69** excess defects occurred in **80000** inspections.
- **Record and verify the actual change and its mechanism.** The process fact needed to identify the change was unavailable. Without that record, the team cannot transfer, standardize, or defend a causal operating recipe.
- **Treat paste thickness and reflow peak as improvement hypotheses, not as a proven recipe.** Their significant association is useful, but the observational surface's in-range minimum predicted **0.00554728662682953** (prediction interval **0.004371384319129843** to **0.006723188934529218**), still above target. A designed, randomized confirmation is required before changing settings.
- **Continue the 3-sigma p-chart by lot and investigate the remaining common-cause gap.** Add a documented reaction plan and only recognize close-out when evidence demonstrates **0.0025 or less**, not merely a stable process.

## Data and computation limits

All requested shop-floor batches were released; none was denied. The process-owner request for the change identity was `unroutable`, so the conclusion stops at “a detectable before-and-after improvement,” not at a named causal change. The settings model is a separate **40**-row observational record and cannot establish causality. The initial post-lot and supplemental computations failed and were rerun successfully; their final reported results come from the corrected computations.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"define","fields":3},"method_id":"meta.data_profiling","outputs":{"committedShare":0.0025,"committedSharePct":0.25,"fieldCount":3},"status":"success"}
{"step_id":2,"inputs_digest":{"batch":"baseline","lots":25,"groups":25},"method_id":"control_chart.p","outputs":{"lots":25,"defects":1785,"inspected":100000,"centerLine":0.01785,"centerLinePct":1.7850000000000001,"uclMax":0.024130573172489914,"lclMin":0.011569426827510089,"outOfControlCount":0,"shareMinusTarget":0.01535,"ratioToTarget":7.140000000000001,"defectsPer100k":1785.0000000000002,"sigmaLimit":3.0},"status":"success","decision":"Stable at a high level: no lot outside the 3-sigma limits"}
{"step_id":3,"inputs_digest":{"batch":"baseline","successes":1785,"trials":100000,"nullShare":0.0025},"method_id":"basic.one_proportion","outputs":{"pValue":0.0,"processZ":97.20350458321009,"avgP":0.01785},"status":"success","decision":"Baseline share exceeds commitment; exact routine p-value underflowed to zero"}
{"step_id":4,"inputs_digest":{"batch":"settings","records":40,"predictors":2,"interactions":1},"method_id":"regression.ols","outputs":{"records":40,"modelPValue":8.844474875407327e-11,"fStatistic":35.05861875259643,"rSquaredPct":74.49988903608033,"rSquaredAdjPct":72.37487978908703,"pasteCoefficientPValue":1.3832726192588158e-05,"reflowCoefficientPValue":6.056350416391993e-05,"interactionCoefficientPValue":9.507904201668252e-06,"pasteThicknessMean":1.589325,"reflowPeakMean":246.30625},"status":"success","decision":"The specified model has significant setting effects, but is observational"}
{"step_id":5,"inputs_digest":{"batch":"settings","records":40,"predictors":2},"method_id":"basic.correlation","outputs":{"correlationCoefficient":0.5306308398777916,"pValue":0.0004278728475205763,"reflowCorrelationCoefficient":0.5565582198118245,"reflowPValue":0.0001919146042032785,"interactionCorrelationCoefficient":0.637346798804197,"interactionPValue":9.753060886918743e-06},"status":"success","decision":"Both settings have significant marginal correlations with defect share"}
{"step_id":6,"inputs_digest":{"batch":"settings","records":40,"values":"OLS residuals"},"method_id":"basic.normality","outputs":{"pValue":0.29056822668248805,"statistic":0.9671180108574411},"status":"success","decision":"No evidence against residual normality"}
{"step_id":7,"inputs_digest":{"batch":"trial_size","fields":4},"method_id":"meta.data_profiling","outputs":{"nPerGroup":40000,"alpha":0.05,"planningP1":0.018,"planningP2":0.0025,"sampleSize":2},"status":"success"}
{"step_id":8,"inputs_digest":{"beforeEvents":731,"beforeTrials":40000,"afterEvents":134,"afterTrials":40000},"method_id":"basic.two_proportions","outputs":{"beforeDefects":731,"afterDefects":134,"beforeShare":0.018275,"afterShare":0.00335,"riskDifference":-0.014924999999999999,"absoluteReduction":0.014924999999999999,"relativeReductionPct":81.66894664842681,"differenceLower95":-0.016380877730109874,"differenceUpper95":-0.013516114185988718,"zStatistic":-20.409246334850078,"pValue":1.3840232699771407e-92},"status":"success","decision":"The reduction is statistically significant"}
{"step_id":9,"inputs_digest":{"batch":"before_after","successes":134,"trials":40000,"nullShare":0.0025},"method_id":"basic.one_proportion","outputs":{"pValue":0.0011121688607600864,"avgP":0.00335,"shareMinusTarget":0.0008500000000000001,"ratioToTarget":1.34},"status":"success","decision":"The immediate post-change window remains above commitment"}
{"step_id":10,"inputs_digest":{"records":2,"nPerGroup":40000,"alpha":0.05,"p1":0.018,"p2":0.0025},"method_id":"power.two_proportions","outputs":{"power":1.0,"effectSize":0.1690980192630125},"status":"success","decision":"Planned power computation is effectively one, subject to the stated design assumptions"}
{"step_id":11,"inputs_digest":{"batch":"after_lots","lots":20,"groups":20},"method_id":"control_chart.p","outputs":{},"status":"failed","decision":"The initial computation failed before results because subgroup size was referenced outside scope"}
{"step_id":12,"inputs_digest":{"batch":"after_lots","lots":20,"groups":20},"method_id":"control_chart.p","outputs":{"lots":20,"defects":269,"inspected":80000,"centerLine":0.0033625,"centerLinePct":0.33625,"uclMax":0.006108439836547316,"lclMin":0.000616560163452684,"outOfControlCount":0,"sigmaLimit":3.0,"targetOneSidedPValue":1.936949216991863e-06,"targetTwoSidedPValue":3.37957497531701e-06,"shareMinusTarget":0.0008625,"ratioToTarget":1.345,"ciLower":0.0029732061340359667,"ciUpper":0.0037884650838915165,"confidenceLevelPct":95.0,"vsAfterWindowZ":0.03528279319945898,"vsAfterWindowPValue":0.9718542438256355},"status":"success","decision":"The 20-lot confirmation is in control but significantly above commitment"}
{"step_id":13,"inputs_digest":{"batches":["baseline","after_lots"],"baselineLots":25,"postLots":20},"method_id":"capability.binomial","outputs":{},"status":"failed","decision":"The first supplemental script failed because runs_test was unavailable in this SciPy build"}
{"step_id":14,"inputs_digest":{"batch":"baseline","lots":25,"postBatch":"after_lots","postLots":20},"method_id":"capability.binomial","outputs":{"baselineProcessZ":97.20350458321009,"baselineAvgP":0.01785,"postProcessZ":4.885147045293041,"postAvgP":0.0033625},"status":"success","decision":"Capability remains positive Z because both observed levels are above the committed maximum"}
{"step_id":15,"inputs_digest":{"batch":"settings","records":40,"terms":3},"method_id":"doe.factorial_prediction","outputs":{"predictedValue":0.00554728662682953,"piLower":0.004371384319129843,"piUpper":0.006723188934529218,"pasteThicknessAtStationary":1.4339722782791404,"reflowPeakAtStationary":240.93452162837494,"withinObservedRangesBool":true},"status":"success","decision":"The in-range stationary point is still above target; it is not a causal process recipe or demonstrated optimum"}
{"step_id":16,"inputs_digest":{"batch":"after_lots","purpose":"business_impact"},"method_id":"meta.data_profiling","outputs":{"excessDefectsVsTarget":69.0,"furtherReductionPct":25.650557620817843},"status":"success","decision":"Quantifies the remaining business shortfall against commitment"}
```

## Submitted route declarations
```json
[{"point":"baseline_stability_gate","chosen_branch":"stable","observed":{"lots":25,"outOfControlCount":0}},{"point":"settings_significance_gate","chosen_branch":"any_factor_significant","observed":{"pastePValue":1.3832726192588158e-05,"reflowPValue":6.056350416391993e-05,"interactionPValue":9.507904201668252e-06}},{"point":"post_lot_routing","chosen_branch":"retry_with_exact_topic","observed":{"firstStage":"baseline","targetStage":"after_lots"}},{"point":"change_identity","chosen_branch":"not_available","observed":{"provisionOutcome":"unroutable"}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
