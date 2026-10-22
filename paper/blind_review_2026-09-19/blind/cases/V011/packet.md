# Blind item V011

Focal assessment: Baseline temporal stability and the analyses and conclusions that may follow.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the line-improvement team for a display module. Set makers report that some units look dim or patchy in low light; the internally accepted range is 350 to 550 cd/m2. The line records a brightness reading for every unit in the order it comes off, and the archive holds the study in which the same units were read several times over by several operators.

## 2. What you are asked to do

Work through the batches the data steward can release and say where this project stands: whether the recorded readings can be relied on, how the line has behaved over the run, where brightness sits against its accepted range today, and what should be changed next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
# Brightness line review

## Executive conclusion

The brightness record can be used for directional process decisions, but the measurement system is only marginal rather than strong. Crossed gage R&R was **15.276% of study variation**, **15.373% of tolerance**, and **ndc was 9**. Operator reproducibility variance was **9.414**, compared with repeatability variance of **16.844**, so standardization and operator follow-up remain warranted.

The line did not hold one steady level over the released run. The best least-squares split puts the start of the current regime at production position **26** (source index **25**), after **25** observations in the earlier regime. The current segment is stable under the basic Individuals–Moving Range beyond-limit rule, but it is centered too close to the upper specification. Its mean is **523.740**, while the accepted limits are **350.000** and **550.000**. Current **Cpk is 0.484** and **Ppk is 0.493**; **2** of the current **25** readings were above the upper limit.

No process facts are recorded that identify an intentional change, its cause, or its owner. The upward shift therefore must be treated as an unexplained special cause, not claimed as a verified improvement.

## Measurement reliability

The crossed study used **90** readings from **3** operators, **10** parts, and **3** replicates. Gage standard deviation was **5.124**. Gage R&R consumed **15.276%** of total study variation and **15.373%** of the specification tolerance; **ndc was 9**. The operator effect had p-value **0.001215**, while operator-by-part interaction had p-value **0.160203**.

Conclusion: the system distinguishes multiple part categories, but measurement error is material. Keep using it with caution for this investigation; standardize setup and reading practice, check calibration, retrain operators, and repeat the crossed study before relying on small shifts.

## Behavior over the run

Across all **50** units, mean brightness was **486.826**, standard deviation was **43.052**, and the observed range was **401.600** to **556.900**. The whole-run Anderson–Darling p-value was **0.023433**, so one normal-population interpretation is not supported.

The whole-run I-MR center line was **486.826**, with limits **412.694** and **560.958**; **2** points were beyond those limits, at positions **14** and **23**. The runs test found only **6** runs and p-value **0.00000001094**, showing strong non-random sequence structure. Brightness correlated with production order at **0.751**, with p-value **0.000000000346** and fitted slope **2.217** per unit. These diagnostics establish instability; whole-run capability values are not decision-grade.

The least-squares split starts the later regime at position **26**. Mean brightness rose from **449.912** to **523.740**, a computed increase of **73.828**. The Welch comparison gave t-statistic **-12.006**, p-value **0.000000000000002357**, and an interval for the increase from **61.429** to **86.227**. This is an observed shift, not proof of a known intervention or mechanism.

## Where brightness sits today

The latest regime contains **25** observations. Its Anderson–Darling p-value was **0.431300**, and its basic I-MR chart had center line **523.740**, limits **469.474** and **578.006**, and **0** beyond-limit points. This supports using the segment for a provisional current capability estimate, although the short run and unexplained transition limit confidence.

Current **Cp is 1.843** but **Cpk is 0.484**; **Pp is 1.877** but **Ppk is 0.493**. The large gap between potential spread and one-sided capability shows a centering problem, not primarily excessive within-regime spread. Of the latest **25** readings, **23** were inside specification and **2** were above **550.000**. None were below the lower limit.

The earlier regime had mean **449.912**, **Cpk 1.093**, **Ppk 1.327**, and all **25** readings inside specification. The later regime reduced standard deviation from **25.102** to **17.754**, but the unverified upward shift moved the center dangerously close to the upper boundary and produced the observed high-side failures. It must not be described as a successful change.

## Actions now

- Contain current output and review the **2** high-side units against the accepted upper limit.
- Trace the transition beginning at position **26** through machine settings, material lots, recipes, maintenance, calibration, and operator records. No released fact currently identifies the cause, so the causal conclusion stops here.
- Re-center brightness away from the upper boundary while retaining the lower recent variation. Verify the adjustment with a fresh ordered run before releasing normal production.
- Improve the measurement process by standardizing fixture/setup and operator technique, confirming calibration, and repeating the crossed gage study. Focus first on operator reproducibility because its effect was detected at p-value **0.001215**.
- Hold the gain with an I-MR chart built only after the new center is verified; maintain reaction rules for limit signals and specification breaches. Recalculate capability only from a stable regime rather than combining both levels.

## Evidence limitations

The steward released the charter, measurement study, and ordered production run. A process-owner query returned no matching recorded process fact. Consequently, what changed physically, whether anyone intended the shift, and what any intervention achieved **could not be computed or verified**. There is also no post-corrective-action batch, so sustained improvement cannot yet be demonstrated.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"msa","readings":90,"operators":3,"parts":10,"replicates":3},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":15.27598427840658,"percentTolerance":15.372771160648602,"ndc":9,"gageRRStdDev":5.124257053549534,"repeatabilityVariance":16.84406321244445,"reproducibilityVariance":9.4139471384077,"partToPartVariance":1098.977449405003,"operatorPValue":0.0012145154289969773,"interactionPValue":0.1602033390060479,"readings":90,"operators":3,"parts":10,"replicates":3},"status":"success","decision":"Marginal measurement system; use for directional decisions with caution and improve operator reproducibility."}
{"step_id":2,"inputs_digest":{"batch":"process_run"},"method_id":"meta.data_profiling","outputs":{},"status":"failed","decision":"Initial production analysis failed because the script referenced a nonexistent file; no results were produced."}
{"step_id":3,"inputs_digest":{"batch":"process_run","observations":50},"method_id":"basic.descriptive_summary","outputs":{"mean":486.8260000000001,"median":495.35,"stdDev":43.05201320282626,"skewness":-0.2212920225419272,"adPValue":0.023432616695939844,"minimum":401.6,"maximum":556.9,"sampleSize":50,"lsl":350.0,"usl":550.0,"insideCount":48,"belowCount":0,"aboveCount":2},"status":"success","decision":"Whole-run summary mixes distinct process levels and is not a current-state estimate."}
{"step_id":4,"inputs_digest":{"batch":"process_run","observations":50},"method_id":"basic.normality","outputs":{"statistic":0.8727839851680201,"pValue":0.023432616695939844},"status":"success","decision":"Whole-run normality rejected; do not treat the mixed run as one normal population."}
{"step_id":5,"inputs_digest":{"batch":"process_run","observations":50,"subgroupSize":1},"method_id":"control_chart.imr","outputs":{"individualsUCL":560.9575675206254,"individualsLCL":412.69443247937477,"centerLine":486.8260000000001,"flaggedCount":2,"movingRangeMean":27.87346938775511,"withinSigma":24.7105225068751,"firstFlagPosition":14,"secondFlagPosition":23},"status":"success","decision":"Whole run is not in statistical control."}
{"step_id":6,"inputs_digest":{"batch":"process_run","observations":50,"lsl":350.0,"usl":550.0},"method_id":"capability.normal","outputs":{"cp":1.3489529945819292,"cpk":0.8521875647971869,"pp":0.7742572496271808,"ppk":0.48912927487947455},"status":"success","decision":"Whole-run normal capability indices are diagnostic only because stability and normality prerequisites fail."}
{"step_id":7,"inputs_digest":{"batch":"process_run","observations":50},"method_id":"basic.correlation","outputs":{"correlationCoefficient":0.7506009823761327,"pValue":3.4603189884799097e-10,"slopePerUnit":2.216782713085234,"firstHalfMean":449.91200000000003,"secondHalfMean":523.74},"status":"success","decision":"Brightness has a strong positive association with production order, driven by a level shift."}
{"step_id":8,"inputs_digest":{"batch":"process_run","observations":50},"method_id":"nonparametric.runs_test","outputs":{"pValue":1.0939731836650465e-08,"runs":6,"zStatistic":-5.715476066494082},"status":"success","decision":"Sequence is non-random about its median."}
{"step_id":9,"inputs_digest":{"batch":"process_run","observations":50,"candidateSplits":31},"method_id":"regression.ols","outputs":{"modelPValue":2.356935328671203e-15,"rSquaredPct":75.01864412139099,"rSquaredAdjPct":74.4981992072533,"postStartsAtPosition":26,"sourceIndex":25,"preCount":25,"postCount":25,"combinedWithinSSE":22688.146399999994},"status":"success","decision":"Closest canonical method: least-squares one-change-point search, not a conventional OLS model; fit percentages were not calculated and placeholder fields are omitted from the report."}
{"step_id":10,"inputs_digest":{"batch":"process_run","segment":"pre-shift","observations":25},"method_id":"basic.descriptive_summary","outputs":{"mean":449.91200000000003,"median":451.0,"stdDev":25.102229648645416,"skewness":0.010788138910668066,"adPValue":0.8979897872810353,"minimum":401.6,"maximum":498.4,"sampleSize":25,"insideCount":25,"aboveCount":0},"status":"success","decision":"Pre-shift segment summary."}
{"step_id":11,"inputs_digest":{"batch":"process_run","segment":"post-shift","observations":25},"method_id":"basic.descriptive_summary","outputs":{"mean":523.74,"median":525.8,"stdDev":17.754365660310143,"skewness":0.020608280227971155,"adPValue":0.4313002006877085,"minimum":491.4,"maximum":556.9,"sampleSize":25,"insideCount":23,"aboveCount":2},"status":"success","decision":"Post-shift segment is the best available representation of current production."}
{"step_id":12,"inputs_digest":{"batch":"process_run","segment":"post-shift","observations":25},"method_id":"basic.normality","outputs":{"statistic":0.3555060264918204,"pValue":0.4313002006877085},"status":"success","decision":"Post-shift segment does not reject normality."}
{"step_id":13,"inputs_digest":{"batch":"process_run","groups":2,"observations":50},"method_id":"anova.equal_variances","outputs":{"statistic":1.5323414562248499,"pValue":0.2217821917810666},"status":"success","decision":"No detected pre/post variance difference by median-centered Levene test."}
{"step_id":14,"inputs_digest":{"batch":"process_run","groups":2,"observations":50},"method_id":"basic.two_sample_t","outputs":{"pValue":2.356935328671203e-15,"tStatistic":-12.005969086904225,"meanDifference":73.82799999999997,"ciLower":61.42851337048823,"ciUpper":86.22748662951172,"degreesFreedom":43.205721454641434},"status":"success","decision":"Welch test detects a material upward shift; sign of t reflects pre-minus-post ordering."}
{"step_id":15,"inputs_digest":{"batch":"process_run","segment":"post-shift","observations":25,"subgroupSize":1},"method_id":"control_chart.imr","outputs":{"individualsUCL":578.0064007092199,"individualsLCL":469.4735992907801,"centerLine":523.74,"flaggedCount":0,"movingRangeMean":20.404166666666683,"withinSigma":18.088800236406634},"status":"success","decision":"No beyond-limit points in the post-shift segment under the basic I-MR point rule."}
{"step_id":16,"inputs_digest":{"batch":"process_run","segment":"pre-shift","observations":25,"lsl":350.0,"usl":550.0},"method_id":"capability.normal","outputs":{"cp":1.0936856138649858,"cpk":1.092723170524785,"pp":1.3279032898630219,"ppk":1.3267347349679428},"status":"success","decision":"Pre-shift baseline capability."}
{"step_id":17,"inputs_digest":{"batch":"process_run","segment":"post-shift","observations":25,"lsl":350.0,"usl":550.0},"method_id":"capability.normal","outputs":{"cp":1.8427608740044912,"cpk":0.4839090055135792,"pp":1.8774725028813588,"ppk":0.49302427925664466},"status":"success","decision":"Current segment has ample potential spread capability but poor upper-side centering."}
```

## Submitted route declarations
```json
[{"point":"measurement_gate","chosen_branch":"release_process_run_after_computed_grr","observed":{"grr_pct":15.27598427840658,"ndc":9}},{"point":"stability_before_capability","chosen_branch":"segment_at_computed_level_shift","observed":{"wholeRunFlaggedCount":2,"runsPValue":1.0939731836650465e-08,"postStartsAtPosition":26}},{"point":"current_capability_model","chosen_branch":"normal_capability_on_post_shift_segment","observed":{"normalityPValue":0.4313002006877085,"flaggedCount":0}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
