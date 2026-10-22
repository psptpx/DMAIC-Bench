# Blind item B030

Focal assessment: Selection of analysis methods after distribution diagnosis.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the process engineering group at a fine-chemicals plant. Yield on one intermediate has been low and swings from batch to batch; the internally accepted range is 80 to 100 percent. Production has recorded every batch's yield in charge order, and the archive holds the laboratory's study in which the same samples were assayed repeatedly by several analysts. Separately, an earlier run of charges was made deliberately at a high and a low setting, with the resulting yields recorded. Continuing to run charges is expensive, so we need to know whether the setting is worth pursuing at all before we commit to more of them.

## 2. What you are asked to do

Work through the batches the data steward can release and say where this project stands: whether the assay readings can be relied on, how the line has behaved over the run, where yield sits against its accepted range today, and whether the evidence justifies spending more charges on the setting or sends us back to look elsewhere. Every number in your report must come from a computation you ran on this task.


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
{"msa_pass":{"field":"grr_pct","op":"<=","value":30.0,"source":"AIAG MSA-4 Ch. II Sec. D"}}
```

## Submitted report (complete, identifiers removed)
# Intermediate Yield Project Report

## Executive decision

The assay is fit for use, the historical run is individually in control but capable of only modest yield protection, and the high setting is worth a controlled production confirmation. This is not yet authorization to make a permanent setting change: the trial was recorded in coded units, and the process-fact request could not identify the corresponding physical setting. The strength of the effect and the high-setting prediction justify spending additional charges on confirmation before commitment elsewhere.

## Data basis and integrity

The released data comprised a crossed assay study of 90 measurements (3 operators, 10 samples, 3 replicates), 30 consecutive production yields, and 12 deliberate high/low setting charges. The accepted range is 80.0–100.0 percent. No requested data batch was denied. A process-owner question about the physical identity of the coded high setting was unroutable, so that operational detail remains unresolved.

## Can the assay readings be relied on?
**Yes.** The operator-by-sample interaction was not significant (F = 0.9907, p = 0.4824), so it was pooled with repeatability. Its unconstrained GRR estimate was 16.3906% of study variation. For the final report model, the small negative operator component (-0.000916) was constrained to zero, giving:

- GRR = 16.4643% of study variation
- GRR = 9.4789% of the 20.0-unit tolerance
- Distinct categories = 8

The assay therefore contributes variation but does not explain the low-yield problem. Differences among the sample parts dominate the study, so the measurement system can distinguish materially different batches.

## How has the line behaved?
Across the 30-batch record, mean yield was 86.6207%, median 86.4873%, standard deviation 2.6779%, minimum 80.8876%, maximum 91.8143%, and latest yield 91.7100%. Every recorded batch was inside the accepted range (out-of-specification count = 0). Normality was not rejected (Anderson–Darling p = 0.9201), supporting the normal capability calculations.

The individuals chart had center line 86.6207%, UCL 93.2672%, and LCL 79.9743%; no individual point was flagged. The moving-range chart also had no flagged ranges. A median runs test found 11 runs versus 16.0000 expected, z = -1.8581 and p = 0.0632, so randomness was not rejected at alpha 0.05, although clustering remains a watch item.

The within-standard-deviation estimate was 2.2155%, while the overall standard deviation was 2.6779%. Consequently Cp = 1.5046 and Cpk = 0.9961, but Pp = 1.2448 and Ppk = 0.8241- Mean yield was significantly above the lower limit (t = 13.5418, p = 0.0000000000000455), with a 0.95 confidence interval of 85.6208% to 87.6207%. The issue is not specification failures; it is an average near the low side plus enough batch-to-batch variation to leave limited margin.

## Is the setting worth pursuing?
**Yes—but only through a controlled confirmation.** Across 12 charges, the coded high setting averaged 93.2597% versus 86.8450% at low, an improvement of 6.4147 percentage points. The setting effect was highly significant (F = 72.4061, p = 0.000006831) and explained 87.8650% of yield variation (adjusted R-squared = 86.6515%). Within-level standard deviations were 1.0772 at low and 1.4998 at high.

At coded high, the fitted prediction was 93.2597%, with a 0.95 prediction interval of 90.1173% to 96.4021%. Thus the modeled lower prediction bound is 10.1173 points above the lower accepted limit and the upper bound is 3.5979 points below the upper limit. This is the evidence that the setting is worth additional charges; it would be premature to abandon the setting and return elsewhere.

No permanent production change is supported yet. The study levels are coded, and the attempt to obtain the corresponding physical process fact was unroutable. Confirmation must stop at that operational gap until a process engineer translates +1 into a documented set point. The confirmation should then be run under planned charge-order control, with acceptance criteria defined before the first charge.

## What changed and what it achieved
The data show no permanent line change; they show a deliberate earlier screen. Moving that screen from its low to high coded level achieved the 6.4147-point mean gain above. Because this was a setting screen rather than an implemented change, the achievement is evidence of a promising lever—not a claim of permanent performance. The analysis therefore changed the project focus: the assay is not the cause, while the setting is the dominant identified lever.

## How the change will be held

1. Resolve and document the physical high setting before any confirmation charge.
- Run a predefined confirmation sequence at that setting, preserving charge order and all assay records.
- Monitor confirmation yields on an I-MR chart and investigate any individual or moving-range signal before continuing.
- Recalculate mean, Ppk, and Cpk after confirmation; retain the accepted limits 80.0–100.0.
- Maintain the current assay method and repeat the crossed GRR if analysts, method, or equipment change.
- Make implementation conditional on both confirmed performance and demonstrated control—not on the screening result alone.

## Limitations and final position
The measurement evidence and baseline record are complete for this decision. The setting evidence is strong but coded and comes from 12 deliberate charges; it is not a production implementation trial. No requested data batch was denied. Until the physical setting is identified and confirmed under routine control, the project should spend further charges on the setting rather than looking elsewhere, while preserving the current I-MR and capability monitoring.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"source_batch":"msa","sample_size":90,"operators":3,"parts":10,"replicates":3},"method_id":"msa.gage_rr_crossed","outputs":{},"status":"failed","decision":"The first execution failed on dictionary iteration before producing a quantitative result."}
{"step_id":2,"inputs_digest":{"source_batch":"msa","sample_size":90,"operators":3,"parts":10,"replicates":3},"method_id":"msa.gage_rr_crossed","outputs":{"n":90,"operators":3,"parts":10,"replicates":3,"interactionF":0.9906958443479115,"interactionPValue":0.4823963600469747,"unconstrainedEquipmentVariance":0.09983240666382005,"unconstrainedOperatorVariance":-0.0009162314406453644,"unconstrainedPartVariance":3.583040246591534,"unconstrainedGrrVariance":0.09891617522317468,"unconstrainedTotalVariance":3.6819564218147085,"unconstrainedPercentStudyVariation":16.39058051752204,"unconstrainedPercentTolerance":9.435282597827008,"unconstrainedNdcContinuous":8.511521165390628,"unconstrainedNdcInteger":8,"percentStudyVariation":16.39058051752204,"percentTolerance":9.435282597827008,"ndc":8},"status":"success","decision":"The operator-by-part interaction was not significant, so it was pooled with repeatability; the declared gate value was the unconstrained pooled estimate."}
{"step_id":3,"inputs_digest":{"source_batch":"msa","sample_size":90,"operators":3,"parts":10,"replicates":3},"method_id":"msa.gage_rr_crossed","outputs":{"equipmentVariance":0.09983240666382297,"grrVariance":0.09983240666382297,"interactionF":0.9906958443478963,"interactionPValue":0.4823963600469904,"n":90,"ndc":8,"ndcContinuous":8.472373060773215,"operatorVariance":0.0,"operators":3,"partVariance":3.583040246591533,"parts":10,"percentStudyVariation":16.464267719415062,"percentTolerance":9.478879996995463,"replicates":3,"tolerance":20.0,"totalVariance":3.6828726532553557},"status":"success","decision":"The assay is acceptable: GRR is below 30% of study variation and below 10% of tolerance, with at least five distinct categories."}
{"step_id":4,"inputs_digest":{"source_batch":"process_run","sample_size":30,"specification_limits":[80.0,100.0]},"method_id":"basic.descriptive_summary","outputs":{"adPValue":0.9200568200458585,"adStatistic":0.17302375806803383,"latestValue":91.71,"lsl":80.0,"maximum":91.8143,"mean":86.62074333333334,"median":86.4873,"minimum":80.8876,"n":30,"outOfSpecCount":0,"skewness":0.11748189743704592,"stdDev":2.677871793908214,"usl":100.0},"status":"success","decision":"All 30 recorded yields were inside 80–100; the distribution is approximately normal."}
{"step_id":5,"inputs_digest":{"source_batch":"process_run","sample_size":30,"lsl":80.0,"usl":100.0},"method_id":"capability.normal","outputs":{"centerLine":86.62074333333334,"cp":1.5045540909548762,"cpk":0.9961266467328895,"flaggedCount":0,"individualsLCL":79.9742558058205,"individualsUCL":93.26723086084617,"mean":86.62074333333334,"movingRangeBar":2.4990793103448263,"movingRangeFlaggedCount":0,"movingRangeUCL":8.164492106896548,"overallStdDev":2.677871793908214,"pp":1.2447695744494576,"ppk":0.8241299861572421,"withinStdDev":2.215495842504279},"status":"success","decision":"Short-term capability is near 1.00, while overall Ppk is lower because between-batch variation inflates the total standard deviation."}
{"step_id":6,"inputs_digest":{"source_batch":"process_run","sample_size":30,"chart":"individuals and moving range"},"method_id":"control_chart.imr","outputs":{"centerLine":86.62074333333334,"cp":1.5045540909548762,"cpk":0.9961266467328895,"flaggedCount":0,"individualsLCL":79.9742558058205,"individualsUCL":93.26723086084617,"mean":86.62074333333334,"movingRangeBar":2.4990793103448263,"movingRangeFlaggedCount":0,"movingRangeUCL":8.164492106896548,"overallStdDev":2.677871793908214,"pp":1.2447695744494576,"ppk":0.8241299861572421,"withinStdDev":2.215495842504279},"status":"success","decision":"No individual or moving-range point was outside its computed 3-sigma limits."}
{"step_id":7,"inputs_digest":{"source_batch":"process_run","sample_size":30,"datum":"median"},"method_id":"nonparametric.runs_test","outputs":{"alpha":0.05,"expectedRuns":16.0,"nAboveMedian":15,"nBelowMedian":15,"observedRuns":11,"pValue":0.06316072400287963,"statistic":-1.8580583823930164},"status":"success","decision":"The runs test does not reject randomness at alpha 0.05, although the small p-value and negative z indicate fewer runs than expected."}
{"step_id":8,"inputs_digest":{"source_batch":"process_run","sample_size":30,"hypothesized_mean":80.0},"method_id":"basic.one_sample_t","outputs":{"confidenceLevel":0.95,"degreesOfFreedom":29,"hypothesizedMean":80.0,"meanCILower":85.62080957203659,"meanCIUpper":87.62067709463008,"pValue":4.5527287104331214e-14,"sampleMean":86.62074333333334,"tStatistic":13.541837512042255},"status":"success","decision":"Mean yield is statistically above the lower accepted limit."}
{"step_id":9,"inputs_digest":{"source_batch":"screening_doe","sample_size":12,"levels":2,"runs_per_level":6},"method_id":"doe.factorial_analysis","outputs":{"effectHighMinusLow":6.414649999999995,"fStatistic":72.40607023799876,"highLevelMean":93.25966666666666,"highLevelStdDev":1.499809395445527,"intercept":90.05234166666668,"lowLevelMean":86.84501666666667,"lowLevelStdDev":1.0771811127506234,"modelPValue":6.831448800224623e-06,"n":12,"rSquaredAdjPct":86.65146879564738,"rSquaredPct":87.86497163240671,"residualMeanSquare":1.704873686166674,"slopeCoded":3.207325000000001},"status":"success","decision":"The coded setting has a large, statistically significant positive effect on yield."}
{"step_id":10,"inputs_digest":{"source_batch":"screening_doe","sample_size":12,"prediction_x_coded":1.0,"confidence_level":0.95},"method_id":"doe.factorial_prediction","outputs":{"confidenceLevel":0.95,"lowerMarginToLSL":10.117264611463611,"piLower":90.11726461146361,"piUpper":96.40206872186974,"predictedValue":93.25966666666667,"predictionSe":1.4103259554187415,"upperMarginToUSL":3.597931278130261,"xNewCoded":1.0},"status":"success","decision":"The high-setting prediction lies inside the accepted range, and even the lower prediction bound exceeds 90; controlled confirmation is warranted."}
```

## Submitted route declarations
```json
[{"point":"msa_interaction_model","chosen_branch":"pool operator-by-part interaction with repeatability","observed":{"interactionPValue":0.4823963600469904,"interactionF":0.9906958443478963,"alpha":0.05}},{"point":"setting_next_action","chosen_branch":"pursue controlled confirmation at coded high level","observed":{"modelPValue":6.831448800224623e-06,"effectHighMinusLow":6.414649999999995,"piLower":90.11726461146361}},{"point":"baseline_control_action","chosen_branch":"hold current controls and monitor I-MR","observed":{"flaggedCount":0,"movingRangeFlaggedCount":0,"runsTestPValue":0.06316072400287963}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
