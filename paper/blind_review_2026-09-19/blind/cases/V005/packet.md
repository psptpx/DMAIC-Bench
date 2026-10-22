# Blind item V005

Focal assessment: Applicability of the response-surface model and the basis for subsequent optimization.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the development team on an assembled optical module. The seal between the two housings must hold at least 45 N, and the product margin the programme committed to needs it above 55 N. Sixty consecutive assemblies have been pulled and tested in the order they were built. The archive also holds a screening run in which three assembly settings were each taken to a low and a high level twice over; a later composite design over two of those settings, with the centre setting run five times; and twenty seals made at the settings that design work recommended.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: how the line has behaved across the baseline, where seal strength sits against what the product requires, whether the settings that were varied account for it, what the design work supports concluding, and what should happen next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
{"screening_significant":{"field":"any_factor_significant","op":"==","value":true,"source":"Montgomery DAOE 6e 11.2"}}
```

## Submitted report (complete, identifiers removed)
# Seal-strength project status

## Executive conclusion

The baseline line was statistically quiet but not performing the business objective. Its mean was **52.076 N**, versus the product lower specification of **45 N** and the programme requirement of **55 N**. The recommended-setting confirmation improved the observed mean to **59.275 N**, an increase of **7.199 N** with a confidence interval from **5.784 N** to **8.615 N**. All **20** confirmation seals exceeded both thresholds.

The improvement is real in the available sample, but the project should not yet be closed as fully capable against the programme margin. Confirmation overall lower performance was **Ppk 0.720** against **55 N**, despite **Ppk 2.404** against **45 N**. Hold the recommended settings, verify their identity in controlled documentation, and continue sequential monitoring before making a long-term capability claim.

## Baseline behavior and requirement gap

The **60** consecutive baseline assemblies averaged **52.076 N**, with median **51.805 N** and standard deviation **4.298 N**. The observed range was **41.080 N** to **62.920 N**. There were **4** results below **45 N**, or **6.667%**, and **41** below **55 N**, or **68.333%**.

The I-MR centre line was **52.076 N**, with limits **39.400 N** and **64.752 N**; **0** observations crossed them. The runs-test p-value was **0.795**, and the Anderson-Darling p-value was **0.380**. Thus the available sequence gives no signal of a time-order upset or nonnormality. This matters because the weakness is not explained by a few chart signals: the stable baseline itself is centred too low and too widely spread.

The baseline mean was below **55 N** with t statistic **-5.270** and p-value **0.00000202**. Lower capability against **45 N** was only **Cpk 0.558** and **Ppk 0.549**. The line therefore did not reliably meet the product specification and clearly missed the committed margin.

## What accounts for strength

The screening experiment used **16** observations over **3** factors with **2** replicates per treatment combination. The full factorial model had p-value **0.000142** and explained **94.912%** of response variation.

Increasing coded bond angle produced an estimated **4.386 N** effect with p-value **0.0000161**. Increasing coded bead spacing produced **3.081 N** with p-value **0.000200**. Their interaction contributed **2.193 N** with p-value **0.00179**, so the settings should be managed jointly rather than independently. Cure temperature's estimated effect was **0.182 N**, with p-value **0.713**; this experiment does not support it as a driver over the studied range.

## What the response-surface work supports

The quadratic model on **13** design runs explained **98.017%** of observed variation and had model p-value **0.00000832**. Both curvature terms were supported: bond-angle squared had p-value **0.00166**, and bead-spacing squared had p-value **0.00395**. The fitted stationary response was **64.587 N**, but its coded bond angle was **1.817**, outside the circular design radius of **1.414**; it is extrapolative and is not the recommended operating claim.

Within the circular design region, constrained optimization produced a candidate at coded bond angle **1.274** and coded bead spacing **0.614**, with predicted response **63.923 N** and prediction interval **60.719 N** to **67.127 N**. This is model guidance, not proof of production performance. The lack-of-fit p-value was **0.00190**, so the quadratic surface misses structure relative to centre-point repeatability and should not be used for unsupported extrapolation.

The archive says the confirmation seals were made at the recommended settings, but neither the released batch nor the process owner supplied the settings' identity or physical-unit mapping. Consequently, this report cannot state which physical setpoints were changed or prove that the implemented settings equal the computed coded candidate. That documentation gap must be closed before standard work is revised.

## What the change achieved

For the **20** confirmation seals, the mean was **59.275 N**, median **59.040 N**, and standard deviation **1.980 N**. Results ranged from **56.410 N** to **63.240 N**. There were **0** observations below **45 N** and **0** below **55 N**.

The confirmation I-MR limits were **53.352 N** and **65.198 N**, with **0** flagged observations. The runs-test p-value was **0.358**, and the normality p-value was **0.510**. These are encouraging short-run stability results, not evidence covering future shifts, materials, or operators.

Against **55 N**, the one-sided t statistic was **9.657** with p-value **0.00000000460**, supporting a mean above the programme requirement. Compared with baseline, the Welch t statistic was **10.142** with p-value **0.00000000000000223**. The variance test p-value was **0.00105**, supporting the use of the unequal-variance comparison.

## Hold plan and next action

* Freeze the recommended recipe pending verification, and place the actual bond-angle, bead-spacing, and cure-temperature setpoints under revision-controlled standard work. The missing setpoint identity is the immediate documentation action.
* Continue an individuals and moving-range chart using build order. Investigate chart signals and do not recalculate limits after an upset without cause review.
* Keep both requirements visible: **45 N** is the product lower specification; **55 N** is the programme margin. A passing short run against the first does not establish durable capability against the second.
* Extend confirmation across normal sources of variation before closure. Re-estimate capability against **55 N** only after stability is demonstrated on that broader sample.
* Because response-surface lack of fit is significant, augment or refit the design before moving beyond the studied region. Do not pursue the extrapolated stationary point on the present model.

**Disposition:** retain the improved condition under controlled verification. The project has demonstrated a substantial and statistically supported strength increase, but closure awaits documented setpoints and broader evidence of stable capability against the programme margin.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"baseline","sampleSize":60},"method_id":"basic.descriptive_summary","outputs":{"mean":52.07566666666666,"median":51.805,"stdDev":4.2984961369702335,"skewness":-0.14758060977391452,"adPValue":0.3800271170510971,"minimum":41.08,"maximum":62.92,"sampleSize":60,"lsl":45.0,"requiredLevel":55.0,"belowLSLCount":4,"belowLSLPct":6.666666666666667,"belowRequiredCount":41,"belowRequiredPct":68.33333333333333},"status":"success","decision":"Baseline centre is below the programme requirement and observed failures occurred below both thresholds."}
{"step_id":2,"inputs_digest":{"batch":"baseline","sampleSize":60},"method_id":"basic.normality","outputs":{"statistic":0.3861460530137535,"pValue":0.3800271170510971,"alpha":0.05},"status":"success","decision":"Normality not rejected at the computed alpha."}
{"step_id":3,"inputs_digest":{"batch":"baseline","orderedIndividuals":60},"method_id":"control_chart.imr","outputs":{"individualsUCL":64.75169378531074,"individualsLCL":39.39963954802259,"centerLine":52.07566666666666,"flaggedCount":0,"movingRangeMean":4.765423728813559,"withinSigma":4.2246664262531555},"status":"success","decision":"No individual exceeded the calculated limits."}
{"step_id":4,"inputs_digest":{"batch":"baseline","orderedIndividuals":60},"method_id":"nonparametric.runs_test","outputs":{"pValue":0.7945434963754624,"statistic":0.2604152298810939,"runs":32},"status":"success","decision":"No evidence of nonrandom ordering around the median."}
{"step_id":5,"inputs_digest":{"batch":"baseline","sampleSize":60,"reference":"lsl"},"method_id":"basic.one_sample_t","outputs":{"pValue":1.3385987688318038e-18,"tStatistic":12.750477511249048,"referenceValue":45.0},"status":"success","decision":"Baseline mean is above the lower specification, but this does not establish item-level conformance."}
{"step_id":6,"inputs_digest":{"batch":"baseline","sampleSize":60,"reference":"programme requirement"},"method_id":"basic.one_sample_t","outputs":{"pValue":2.024484174071137e-06,"tStatistic":-5.2697008152912845,"referenceValue":55.0},"status":"success","decision":"Baseline mean is significantly below the programme requirement."}
{"step_id":7,"inputs_digest":{"batch":"baseline","sampleSize":60,"oneSidedLowerSpecification":45.0},"method_id":"capability.grouped","outputs":{"cpk":0.5582820790060223,"ppk":0.5486931895251083,"lsl":45.0},"status":"success","decision":"Lower capability against the specification is inadequate; only a lower limit was supplied, so Cp and Pp were not computed."}
{"step_id":8,"inputs_digest":{"batch":"screening_run","sampleSize":16,"factorCount":3,"replicatesPerCell":2},"method_id":"doe.factorial_analysis","outputs":{"modelPValue":0.0001417792462045015,"rSquaredPct":94.9115904373612,"fStatistic":21.31714983552114,"rSquaredAdjPct":90.45923207005224,"residualStdDev":0.9565267573361449,"bondAngleEffect":4.38612499999998,"bondAnglePValue":1.6133893323495207e-05,"beadSpacingEffect":3.081125000000008,"beadSpacingPValue":0.00019993241547936803,"cureTemperatureEffect":0.1821250000000042,"cureTemperaturePValue":0.7132611114928761,"bondAngleBeadSpacingEffect":2.1926250000000143,"bondAngleBeadSpacingPValue":0.0017912880490681346,"alpha":0.05,"anyFactorSignificant":true},"status":"success","decision":"Bond angle and bead spacing, plus their interaction, are significant; cure temperature is not. Declared any_factor_significant true."}
{"step_id":9,"inputs_digest":{"batch":"composite_design","sampleSize":13,"factorCount":2,"centerReplicates":5},"method_id":"doe.rsm_analysis","outputs":{"rSquaredPct":98.01737641449876,"lackOfFitPValue":0.0018986454618481292,"modelPValue":8.319937285038634e-06,"modelFStatistic":69.21350476399473,"rSquaredAdjPct":96.6012167105693,"lackOfFitFStatistic":40.34160786968324,"pureErrorStdDev":0.2514963916242127,"residualStdDev":1.0628717486851087,"bondAngleLinearPValue":6.436966385163061e-07,"beadSpacingLinearPValue":0.0019971028469455915,"bondAngleSquaredPValue":0.001664574422606535,"beadSpacingSquaredPValue":0.003945465890083153,"alpha":0.05},"status":"success","decision":"Quadratic response is strong, but significant lack of fit limits confidence in the surface."}
{"step_id":10,"inputs_digest":{"batch":"composite_design","factorCount":2},"method_id":"doe.rsm_canonical","outputs":{"predictedAtStationary":64.58718079009292,"stationaryBondAngle":1.8173160589514112,"stationaryBeadSpacing":1.0156909443798037,"canonicalEigenvalue1":-2.3245897379823983,"canonicalEigenvalue2":-1.3682352682240748,"designRadius":1.4142135623730951},"status":"success","decision":"Both eigenvalues indicate a fitted maximum, but the stationary point is outside the circular design region."}
{"step_id":11,"inputs_digest":{"batch":"composite_design","constraint":"circular design region"},"method_id":"doe.rsm_optimizer","outputs":{"compositeDesirability":1.0,"predictedResponse":63.9232134932709,"bondAngle":1.2737320973425303,"beadSpacing":0.6144969846943314,"radius":1.414213562372751,"meanCILower":61.93628145697024,"meanCIUpper":65.91014552957157,"piLower":60.71938185461723,"piUpper":67.12704513192458},"status":"success","decision":"Constrained model candidate only; confirmation data, not this estimate, determine achievement."}
{"step_id":12,"inputs_digest":{"batch":"confirmation_runs","sampleSize":20},"method_id":"basic.descriptive_summary","outputs":{"mean":59.27499999999999,"median":59.04,"stdDev":1.9797301783190986,"skewness":0.6007215186410805,"adPValue":0.5101447105824561,"minimum":56.41,"maximum":63.24,"sampleSize":20,"belowLSLCount":0,"belowLSLPct":0.0,"belowRequiredCount":0,"belowRequiredPct":0.0,"lsl":45.0,"requiredLevel":55.0},"status":"success","decision":"All observed confirmation seals exceeded both thresholds."}
{"step_id":13,"inputs_digest":{"batch":"confirmation_runs","sampleSize":20},"method_id":"basic.normality","outputs":{"statistic":0.3191504675061658,"pValue":0.5101447105824561,"alpha":0.05},"status":"success","decision":"Normality not rejected at the computed alpha."}
{"step_id":14,"inputs_digest":{"batch":"confirmation_runs","orderedIndividuals":20},"method_id":"control_chart.imr","outputs":{"individualsUCL":65.19839999999999,"individualsLCL":53.35159999999999,"centerLine":59.27499999999999,"flaggedCount":0,"movingRangeMean":2.226842105263158,"withinSigma":1.974150802538261},"status":"success","decision":"No individual exceeded the calculated limits in the short confirmation sequence."}
{"step_id":15,"inputs_digest":{"batch":"confirmation_runs","orderedIndividuals":20},"method_id":"nonparametric.runs_test","outputs":{"pValue":0.35812874339351886,"statistic":-0.9189365834726815,"runs":9},"status":"success","decision":"No evidence of nonrandom ordering around the median."}
{"step_id":16,"inputs_digest":{"batch":"confirmation_runs","sampleSize":20,"alternative":"greater","reference":"programme requirement"},"method_id":"basic.one_sample_t","outputs":{"pValue":4.60281743722586e-09,"tStatistic":9.65706408731706,"referenceValue":55.0},"status":"success","decision":"Confirmation mean is significantly above the programme requirement."}
{"step_id":17,"inputs_digest":{"batch":"confirmation_runs","sampleSize":20,"oneSidedLowerSpecification":45.0},"method_id":"capability.grouped","outputs":{"cpk":2.4103190735050797,"ppk":2.403526190308126,"lsl":45.0},"status":"success","decision":"Strong observed lower capability against the product specification in this short confirmation run."}
{"step_id":18,"inputs_digest":{"batch":"confirmation_runs","sampleSize":20,"oneSidedLowerSpecification":55.0},"method_id":"capability.grouped","outputs":{"cpk":0.7218293547624659,"ppk":0.7197950587437636,"lsl":55.0},"status":"success","decision":"Despite all observed results passing, capability against the more demanding programme margin is not yet strong."}
{"step_id":19,"inputs_digest":{"groups":2,"baselineSampleSize":60,"confirmationSampleSize":20},"method_id":"anova.equal_variances","outputs":{"statistic":11.584918360378822,"pValue":0.0010523717921275457,"alpha":0.05},"status":"success","decision":"Variances differ; use Welch comparison."}
{"step_id":20,"inputs_digest":{"groups":2,"baselineSampleSize":60,"confirmationSampleSize":20,"equalVariances":false},"method_id":"basic.two_sample_t","outputs":{"pValue":2.2252665764921152e-15,"tStatistic":10.141739773219124,"meanDifference":7.199333333333328,"differenceCILower":5.783532532597239,"differenceCIUpper":8.615134134069418,"welchDf":69.98178331320437},"status":"success","decision":"Confirmation mean is significantly higher than baseline."}
```

## Submitted route declarations
```json
[{"point":"screening_factor_gate","chosen_branch":"significant_factors_continue_to_response_surface","observed":{"anyFactorSignificant":true,"alpha":0.05,"bondAnglePValue":1.6133893323495207e-05,"beadSpacingPValue":0.00019993241547936803,"cureTemperaturePValue":0.7132611114928761}},{"point":"rsm_recommendation","chosen_branch":"constrained_candidate_then_confirmation","observed":{"lackOfFitPValue":0.0018986454618481292,"stationaryBondAngle":1.8173160589514112,"designRadius":1.4142135623730951}},{"point":"control_readiness","chosen_branch":"hold_settings_and_extend_monitoring","observed":{"confirmationPpkAtRequired":0.7197950587437636,"confirmationFlaggedCount":0}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
