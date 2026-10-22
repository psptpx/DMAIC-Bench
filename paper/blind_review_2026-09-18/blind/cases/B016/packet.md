# Blind item B016

Focal assessment: Baseline temporal stability and the analyses and conclusions that may follow.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the process team on a honing line that finishes cylinder bores. Assembly has returned units for bore finish, and the accepted band for roughness is 0.40 to 1.60 um Ra with 1.00 as the target. The line records a roughness reading for every bore in the order it is finished, and the archive holds the study in which the same bores were measured several times over by several operators on the roughness tester.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the recorded readings can carry a conclusion at all, how the line has behaved across the run, where voiding sits against its acceptance limit today, and what should change next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
# Void-fraction project status

## Executive conclusion

The measurement system is usable for this study. The crossed repeat-reading study used 108 readings from 3 operators, 12 parts, and 3 replicates. Its computed gage R&R results were 19.579787400305115% study variation, 14.39670975513979% tolerance, and ndc 7.061917468066983. On that basis, the process data can be evaluated, with the important qualification that the process itself is not stable.

The released build-order run contained 50 joints. Every one of the 50 readings was within the charter limits of 0.0 to 25.0 percent void area; the observed range was 6.31 to 17.7. This is an acceptance result for the run, not proof of a controlled process.

## What the line did

The overall mean was 11.828199999999999 and the median was 11.235, with standard deviation 3.0870312599648226. The ordered run is not random: the runs-test p-value was 4.822134315143417e-06, based on 10 runs, and the individuals chart flagged 5 points. The chart center line was 11.828199999999999, with limits 7.1330285714285715 and 16.523371428571426.

The sequence also shows a sustained upward shift. The mean of the first 25 readings was 9.176799999999998 and the mean of the second 25 was 14.479599999999998, a difference of 5.302799999999999. The executed normality test returned p-value 0.010893005178885098 and statistic 9.03926884489909, so the combined run should not be treated as a single normal, stable population.

## Capability and voiding limit

The computed overall indices were Cp 1.3497325798748623, Cpk 1.2771925521020675, Pp 1.3497325798748623, and Ppk 1.2771925521020675. Because the runs test and individuals chart show instability, these indices are provisional and should not be used to claim sustained capability. No reading exceeded the 25.0 percent upper limit in the released run, but the upward shift is a warning that future performance could differ from this aggregate result.

## Cause, change, and achieved result

The data support an order-related process shift, not a specific physical cause. The run begins at a lower level and later operates at a higher level; the data supplied contain no lot, machine, tool, recipe, operator, timestamp, or intervention labels that would identify what changed. Therefore the responsible cause cannot be isolated from this batch.

No process improvement or before/after batch was released. Consequently, there is no computed change to report and no computed improvement achieved. The only demonstrated result is that all 50 released readings met the current limit while the sequence was unstable.

## Recommended next action and control

1. Preserve the build-order sequence and add time, lot, machine, recipe, tool condition, operator, and intervention fields to every reading.
2. Investigate the transition associated with the sustained level increase before changing settings; use the chart-flagged observations as review points rather than deleting them.
3. After the assignable cause is addressed, collect a new ordered run and recompute stability and capability separately for the resulting conditions. Do not pool unlike conditions.
4. Hold the process with an individuals/moving-range chart and a documented reaction plan for any signal. Continue periodic verification of the measurement system using the established repeat-reading study design.

The project therefore stands at **Measure/Analyze**: the measurement system is adequate and the current batch meets the voiding limit, but the process is not yet demonstrated to be stable or sustainably capable.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"msa","operators":3,"parts":12,"replicates":3,"observations":108,"tolerance":25.0},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":19.579787400305115,"percentTolerance":14.39670975513979,"ndc":7.061917468066983,"operators":3,"parts":12,"replicates":3,"observations":108,"tolerance":25.0},"status":"success","decision":"Measurement system is adequate for the study; continue to process analysis."}
{"step_id":2,"inputs_digest":{"batch":"process_run","observations":50},"method_id":"basic.descriptive_summary","outputs":{"mean":11.828199999999999,"median":11.235,"stdDev":3.0870312599648226,"skewness":0.16667292489421356,"adPValue":0.010893005178885098,"observations":50},"status":"success","decision":"Overall level and spread were computed; normality evidence is weak."}
{"step_id":3,"inputs_digest":{"batch":"process_run","observations":50},"method_id":"basic.normality","outputs":{"pValue":0.010893005178885098,"statistic":9.03926884489909,"observations":50},"status":"success","decision":"Reject normality at the 0.05 level for the overall ordered run."}
{"step_id":4,"inputs_digest":{"batch":"process_run","observations":50,"lsl":0.0,"usl":25.0},"method_id":"capability.normal","outputs":{"cp":1.3497325798748623,"cpk":1.2771925521020675,"pp":1.3497325798748623,"ppk":1.2771925521020675,"withinCount":50,"outOfSpecCount":0,"withinProportion":1.0,"min":6.31,"max":17.7,"observations":50,"lsl":0.0,"usl":25.0},"status":"success","decision":"All observed readings meet the limits, but capability indices are provisional because stability and normality are not established."}
{"step_id":5,"inputs_digest":{"batch":"process_run","observations":50,"classification":"above_or_below_overall_median"},"method_id":"nonparametric.runs_test","outputs":{"pValue":4.822134315143417e-06,"runs":10,"runsZ":-4.572380853195265,"observations":50},"status":"success","decision":"Reject randomness; the ordered process contains a sustained shift."}
{"step_id":6,"inputs_digest":{"batch":"process_run","observations":50,"chart":"individuals_moving_range"},"method_id":"control_chart.imr","outputs":{"individualsUCL":16.523371428571426,"individualsLCL":7.1330285714285715,"centerLine":11.828199999999999,"flaggedCount":5,"averageMovingRange":1.765102040816326,"observations":50},"status":"success","decision":"The individuals chart flags 5 observations; the run is not statistically stable."}
{"step_id":7,"inputs_digest":{"batch":"process_run","observations_per_half":25},"method_id":"basic.two_sample_t","outputs":{"tStatistic":-1.538806366368109,"pValue":0.13028490115138452,"firstHalfMean":9.176799999999998,"secondHalfMean":14.479599999999998,"halfMeanDifference":5.302799999999999,"observationsPerHalf":25},"status":"success","decision":"The descriptive half-run shift is 5.302799999999999; this comparison is secondary because the split was selected from the ordered data."}
```

## Submitted route declarations
```json
[{"point":"data_topic","chosen_branch":"repeat_readings_operator_study_then_void_fraction","observed":{"roughness_request":"unroutable","available_process_topic":"void fraction/build order"}},{"point":"measurement_gate","chosen_branch":"proceed_after_MSA","observed":{"percentStudyVariation":19.579787400305115,"percentTolerance":14.39670975513979,"ndc":7.061917468066983}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
