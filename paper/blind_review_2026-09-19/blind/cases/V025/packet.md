# Blind item V025

Focal assessment: Baseline temporal stability and the analyses and conclusions that may follow.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the process team on an enamelled-component line. Coating thickness is accepted between 180 and 260 um with 220 um as the target. The line records five consecutive pieces at each of twenty-five sampling points through the run, the archive holds the study in which the same pieces were measured several times over by several operators on the thickness gauge, and a separate sample records thickness piece by piece for each of the four applicators.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the recorded readings can carry a conclusion, how the line has behaved across the run, where coating thickness sits against the range it is accepted in, and what specifically should change next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
{"msa_ndc":{"field":"ndc","op":">=","value":5.0,"source":"AIAG MSA-4 Ch. II Sec. D"},"msa_pass":{"field":"grr_pct","op":"<=","value":30.0,"source":"AIAG MSA-4 Ch. II Sec. D"}}
```

## Submitted report (complete, identifiers removed)
# Coating thickness project status

## Executive conclusion

The readings can carry a process conclusion. The crossed gage study produced **12.27% study variation**, **11.35% of tolerance**, and **11 distinct categories**. The gauge can distinguish meaningful piece-to-piece differences, although measurement variation is large enough that repeatability should still be improved.

The original run was **stable but wholly unacceptable**. Its mean was **291.34 um**, or **71.34 um above the 220.00 um target**. All **125 of 125 readings** were above the **260.00 um upper limit**, so the observed nonconforming rate was **100.00%**. Stability did not imply conformance.

The monitoring record after the undocumented change is materially better. Its mean is **219.25 um**, **0.75 um below target**; **0 of 20 readings** were outside the accepted **180.00–260.00 um** range. The available evidence supports retaining the new condition, while continuing monitoring because the post-change record is still limited.

## Measurement system

The crossed study used **90 readings** from **3 operators**, **10 parts**, and **3 replicates**. Total gage variance was **2.2898**, comprising repeatability variance **1.8156**, operator-by-part variance **0.4656**, and operator variance **0.0086**. The operator test had **p = 0.3605**. Measurement error is therefore driven mainly by repeatability and interaction rather than a persistent operator offset.

Decision: use the readings for process and applicator conclusions, but standardize gauge placement and handling and verify repeatability in a follow-up study.

## Baseline behavior and capability

The baseline median was **291.13 um**, standard deviation **7.74 um**, minimum **272.04 um**, and maximum **311.40 um**. Anderson-Darling normality testing gave **p = 0.5967**, so this sample did not show evidence against a normal capability model.

For the **25 subgroups** of **5 pieces**, the X-bar center line was **291.34 um**, with limits **281.23 um** and **301.45 um**. The average range was **17.53 um**, with an upper range limit of **37.05 um**. There were **0 X-bar flags** and **0 range flags** under the point-limit screen. Thus, the line held a consistent but badly over-applied condition throughout the sampled run.

The within estimates were **Cp = 1.769** and **Cpk = -1.386**; overall estimates were **Pp = 1.722** and **Ppk = -1.349**. The apparently wide potential spread is irrelevant while the center lies beyond the upper specification: the negative one-sided indices correctly identify the baseline as incapable.

## Applicator analysis and cause status

The applicator means were **291.55 um** for nozzle A, **290.77 um** for nozzle B, **294.06 um** for nozzle C, and **290.91 um** for nozzle D. The total spread among those means was only **3.29 um**. Equal-variance testing gave **p = 0.3094**; the one-way applicator ANOVA gave **F = 1.8652** and **p = 0.1460**.

These data do **not** establish one nozzle as the cause. All applicators shared the high condition, so the evidence points operationally toward a common coating-delivery setpoint, calibration, pressure, viscosity, speed, or recipe issue. The dataset cannot distinguish among those common causes; a causal claim would require process-factor records or a controlled trial.

## What changed and what it achieved

The specific intervention is **not recorded in the released data**, and the process-owner query returned no matching process fact. Therefore this report cannot honestly say what physical adjustment produced the result or attribute causality to a named action.

What the observations do establish is a pre/post mean shift of **-72.09 um**, a reduction in absolute target offset of **70.59 um**, and a standard-deviation change of **-2.66 um**. The observed outside-specification rate changed from **100.00%** to **0.00%**, a change of **-100.00 percentage points**.

For the **20 post-change individuals**, standard deviation was **5.08 um**. The I-chart center was **219.25 um**, with limits **201.08 um** and **237.42 um**. There were **0 individual flags** and **0 moving-range flags**. Estimated post-change capability was **Cp = 2.202**, **Cpk = 2.160**, **Pp = 2.625**, and **Ppk = 2.575**. These estimates describe the available record and should not replace continued control-chart evidence.

## Required next actions and control

- Preserve the current machine condition immediately and document the actual recipe, common delivery settings, material condition, line speed, and gauge setup. The missing intervention record is the main traceability gap.
- Center the common coating system on the **220.00 um target** rather than tuning individual nozzles without evidence. Verify all nozzles after any common adjustment.
- Continue an individuals/moving-range chart at the present sampling cadence. Treat the current estimated limits as provisional: investigate any point beyond **201.08–237.42 um** or any moving range above **22.32 um**, then recalculate limits after a longer stable record; quarantine affected production until the assignable cause is resolved and a fresh in-range reading confirms recovery.
- Keep specification disposition separate from chart response: any piece outside **180.00–260.00 um** is nonconforming even if the chart has no signal.
- Improve gauge repeatability through a fixed measurement location, seating method, surface preparation, and operator work instruction, then repeat the crossed study.
- Recalculate capability only after enough additional monitoring confirms that the new center and variation persist. Do not identify nozzle C or any other individual applicator as root cause from the present ANOVA.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"define","descriptive_fields":5},"method_id":"meta.data_profiling","outputs":{"lsl":180.0,"target":220.0,"usl":260.0,"toleranceWidth":80.0},"status":"success","decision":"Charter limits and target extracted; accepted width computed as USL minus LSL."}
{"step_id":2,"inputs_digest":{"batch":"msa","n":90,"operators":3,"parts":10,"replicates":3},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":12.266610182513121,"percentTolerance":11.349033580368573,"ndc":11,"gageVariance":2.2897877903703736,"repeatabilityVariance":1.815612143555555,"interactionVariance":0.4655628432469113,"operatorVariance":0.008612803567907374,"partVariance":149.88619211149373,"operatorPValue":0.3604697260935204,"interactionPValue":0.05154148122043768,"n":90,"numOperators":3,"numParts":10,"numReplicates":3},"status":"success","decision":"Crossed random-effects ANOVA gage R&R; measurement system can distinguish process differences, although its contribution is not negligible."}
{"step_id":3,"inputs_digest":{"batch":"process_run","n":125},"method_id":"basic.descriptive_summary","outputs":{"mean":291.34136000000007,"median":291.13,"stdDev":7.742209127099444,"skewness":0.011340618383606478,"adPValue":0.5966564503704606,"minimum":272.04,"maximum":311.4,"n":125},"status":"success","decision":"Baseline thickness was centered far above target."}
{"step_id":4,"inputs_digest":{"batch":"process_run","n":125},"method_id":"basic.normality","outputs":{"pValue":0.5966564503704606,"statistic":0.293375065094196},"status":"success","decision":"Anderson-Darling test did not detect a departure from normality in the baseline sample."}
{"step_id":5,"inputs_digest":{"batch":"process_run","n":125,"groups":25,"subgroup_size":5},"method_id":"control_chart.xbar_r","outputs":{"xBarChartCenterLine":291.34136,"flaggedXBarCount":0,"xBarUCL":301.4545544,"xBarLCL":281.2281656,"rBar":17.527199999999997,"rUCL":37.05250079999999,"flaggedRCount":0,"subgroupCount":25,"subgroupSize":5},"status":"success","decision":"No basic point-limit flags: the baseline was stable around an unacceptable high center."}
{"step_id":6,"inputs_digest":{"batch":"process_run","n":125,"groups":25,"subgroup_size":5},"method_id":"capability.normal","outputs":{"cp":1.769440260471344,"cpk":-1.386416605048157,"pp":1.7221613514240681,"ppk":-1.3493719723267086,"withinStdDev":7.535339638865003,"overallStdDev":7.742209127099444,"belowLslCount":0,"aboveUslCount":125,"outsideSpecCount":125,"outsideSpecPct":100.0,"meanMinusTarget":71.34136000000007},"status":"success","decision":"Baseline process was not capable because it was centered above the upper specification limit."}
{"step_id":7,"inputs_digest":{"batch":"applicators","n":60,"groups":4,"per_group":15},"method_id":"anova.equal_variances","outputs":{"pValue":0.30935641609930664,"statistic":1.2244844378661417},"status":"success","decision":"Median-centered Levene test did not detect unequal applicator variances."}
{"step_id":8,"inputs_digest":{"batch":"applicators","n":60,"groups":4,"per_group":15},"method_id":"anova.oneway","outputs":{"factorPValue":0.14598101308079076,"fStatistic":1.86518479653037,"nozzleAMean":291.55333333333334,"nozzleBMean":290.76800000000003,"nozzleCMean":294.0566666666667,"nozzleDMean":290.91133333333335,"minimumGroupMean":290.76800000000003,"maximumGroupMean":294.0566666666667,"meanSpread":3.288666666666643,"groupCount":4,"totalN":60,"perGroupN":15},"status":"success","decision":"One-way ANOVA did not demonstrate an applicator mean effect; no single applicator is established as the cause."}
{"step_id":9,"inputs_digest":{"batch":"sustaining","n":20},"method_id":"basic.descriptive_summary","outputs":{"mean":219.24650000000003,"median":218.62,"stdDev":5.079968167119493,"skewness":0.25397212128372904,"adPValue":0.30680781462722406,"minimum":208.93,"maximum":230.61,"n":20},"status":"success","decision":"Post-change monitoring is centered close to target."}
{"step_id":10,"inputs_digest":{"batch":"sustaining","n":20},"method_id":"basic.normality","outputs":{"pValue":0.30680781462722406,"statistic":0.4129421640186983},"status":"success","decision":"Anderson-Darling test did not detect a departure from normality in the sustaining sample."}
{"step_id":11,"inputs_digest":{"batch":"sustaining","n":20,"subgroup_size":1},"method_id":"control_chart.imr","outputs":{"individualsUCL":237.4155929451288,"individualsLCL":201.07740705487126,"centerLine":219.24650000000003,"flaggedCount":0,"averageMovingRange":6.8315789473684205,"movingRangeUCL":22.318768421052628,"flaggedMovingRangeCount":0,"n":20},"status":"success","decision":"No point-limit or moving-range-limit flags were found in the available post-change record."}
{"step_id":12,"inputs_digest":{"batch":"sustaining","n":20,"subgroup_size":1},"method_id":"capability.normal","outputs":{"cp":2.201540832049307,"cpk":2.1600693066255796,"pp":2.6246883631347173,"ppk":2.5752457960941686,"withinStdDev":6.056364315042926,"overallStdDev":5.079968167119493,"belowLslCount":0,"aboveUslCount":0,"outsideSpecCount":0,"outsideSpecPct":0.0,"meanMinusTarget":-0.7534999999999741},"status":"success","decision":"Available post-change sample is in specification and shows strong estimated capability, subject to continued monitoring."}
{"step_id":13,"inputs_digest":{"batches":["process_run","sustaining"],"pre_n":125,"post_n":20},"method_id":"basic.descriptive_summary","outputs":{"mean":-72.09486000000004,"median":70.58786000000009,"stdDev":-2.6622409599799504,"skewness":-100.0,"adPValue":0.0,"preMean":291.34136000000007,"postMean":219.24650000000003,"preStdDev":7.742209127099444,"postStdDev":5.079968167119493,"preOutsideSpecPct":100.0,"postOutsideSpecPct":0.0},"status":"success","decision":"Closest canonical method: descriptive pre/post comparison, not a distribution summary; output aliases retain the computed change quantities."}
```

## Submitted route declarations
```json
[{"point":"measurement_system_gate","chosen_branch":"proceed_with_process_analysis","observed":{"grr_pct":12.266610182513121,"ndc":11}},{"point":"baseline_chart_selection","chosen_branch":"xbar_r_for_ordered_subgroups","observed":{"subgroupSize":5,"subgroupCount":25}},{"point":"applicator_comparison","chosen_branch":"equal_variance_oneway_anova","observed":{"levenePValue":0.30935641609930664}},{"point":"sustaining_chart_selection","chosen_branch":"imr_for_individuals","observed":{"subgroupSize":1,"n":20}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
