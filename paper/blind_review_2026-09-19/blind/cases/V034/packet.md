# Blind item V034

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
# Coating-thickness project status

## Measurement conclusion

The gauge study covered 3 operators, 10 parts and 3 replicates, for 90 readings. Gauge R&R was 25.595558960756396% of study variation and 15.862934151190297% of tolerance, with ndc 5.325263048633628. The steward released the process batch after these computed gate values were declared. The readings can support this project conclusion, but the gauge contribution is not negligible; continue consistent gauge training and periodic MSA.

## What happened across the run

The earlier run contained 125 readings in 25 subgroups. Its mean was 232.2736 um versus the 220.0 um target, with standard deviation 15.442387434506989 um. The X-bar center line was 232.27360000000002 um and 20 subgroup means were flagged; the range chart had zero flags. This is a run-level stability problem, not just random piece-to-piece noise. The normality p-value was 1.4173807372389032e-14, so pooled capability from that unstable run should not be treated as a dependable steady-state capability estimate.

The earlier run had 1 out-of-specification reading (0.8%), with minimum 202.2 um and maximum 261.8 um. Its within-subgroup indices were Cp 1.7509786208973201 and Cpk 1.2137083408611857, while overall indices were Pp 0.8634243500159282 and Ppk 0.5984912224570405. The gap between potential and overall performance is consistent with the detected run shift.

## Change achieved

The sustaining record contained 100 readings in 20 subgroups. Its mean was 219.39270000000005 um, median 219.10500000000002 um, and standard deviation 5.646317805222777 um. The mean change versus the earlier run was -12.88089999999994 um, standard-deviation change was -9.796069629284212 um, and the post/pre variance ratio was 0.13369086994307292. The computed two-sample t statistic was 8.632373210605964 with p-value 5.159111477818606e-15.

All post-change readings were inside the specification: out-of-specification count 0, rate 0.0%, minimum 208.67 um and maximum 234.24 um. The post-change X-bar center line was 219.39270000000002 um with 0 flagged subgroup means; the range chart also had zero flags. Post-change Cp was 2.317454386948129, Cpk 2.2822696357182903, Pp 2.3614209814757787 and Ppk 2.325568707424524. The post-change normality p-value was 0.5410651521150227. On the released sample, the change achieved centering near target, much lower variation, and stable control-chart behavior.

## Applicator finding

The applicator sample had 4 nozzle groups with 15 readings each. The one-way ANOVA statistic was 1.5586494123823231 and its factor p-value was 0.20958647030444327. The evidence does not identify applicator as the specific cause in this sample. Do not adjust nozzles independently on this evidence; first verify common settings and the changed process condition.

## What should change next

Hold the demonstrated post-change setting as the current standard. Add a reaction plan keyed to subgroup X-bar and range signals, with prompt checks of common coating settings, material condition, line speed and application condition when a signal occurs. Keep the same sampling structure and trend the subgroup means rather than relying only on pooled capability. Repeat the gauge study on the current operating range and retain operator technique checks, because the computed gauge R&R remains 25.595558960756396% of study variation.

The evidence supports sustaining the change, not declaring the earlier run acceptable. The post-change result is based on the released sustaining sample; continue collecting the same record to confirm that the zero-flag and zero-defect result holds.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"define","specifications":3},"method_id":"meta.data_profiling","outputs":{"lsl":180.0,"target":220.0,"usl":260.0},"status":"success","decision":"Accepted range and target recorded."}
{"step_id":2,"inputs_digest":{"batch":"msa","operators":3,"parts":10,"replicates":3,"readings":90},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":25.595558960756396,"percentTolerance":15.862934151190297,"ndc":5.325263048633628,"operators":3,"parts":10,"replicates":3,"readings":90},"status":"success","decision":"Gauge study passed the steward gate and process data were released."}
{"step_id":3,"inputs_digest":{"batch":"process_run","readings":125,"groups":25,"subgroupSize":5},"method_id":"basic.descriptive_summary","outputs":{"mean":232.2736,"median":231.12,"stdDev":15.442387434506989,"skewness":0.05305583977016018,"readings":125,"groups":25,"subgroupSize":5,"target":220.0},"status":"success","decision":"Run is centered high relative to target and has substantial overall variation."}
{"step_id":4,"inputs_digest":{"batch":"process_run","readings":125},"method_id":"basic.normality","outputs":{"pValue":1.4173807372389032e-14},"status":"success","decision":"Normality test p-value is very small; interpret pooled capability cautiously."}
{"step_id":5,"inputs_digest":{"batch":"process_run","groups":25,"subgroupSize":5},"method_id":"control_chart.xbar_r","outputs":{"xBarChartCenterLine":232.27360000000002,"flaggedXBarCount":20,"groups":25,"subgroupSize":5,"rChartFlaggedCount":0},"status":"success","decision":"X-bar behavior is not stable across the run; R chart had zero flags but is not separately represented in the canonical output."}
{"step_id":6,"inputs_digest":{"batch":"process_run","readings":125,"specWidth":80.0},"method_id":"capability.normal","outputs":{"cp":1.7509786208973201,"cpk":1.2137083408611857,"pp":0.8634243500159282,"ppk":0.5984912224570405,"readings":125,"specWidth":80.0},"status":"success","decision":"Within-subgroup potential is better than overall performance; stable-process capability cannot be claimed from this run."}
{"step_id":7,"inputs_digest":{"batch":"applicators","groups":4,"readingsPerGroup":15,"readings":60},"method_id":"anova.oneway","outputs":{"factorPValue":0.20958647030444327,"fStatistic":1.5586494123823231,"groups":4,"readingsPerGroup":15,"readings":60},"status":"success","decision":"Nozzle means did not show a detectable difference in this sample."}
{"step_id":8,"inputs_digest":{"batch":"sustaining","readings":100,"groups":20,"subgroupSize":5},"method_id":"basic.descriptive_summary","outputs":{"mean":219.39270000000005,"median":219.10500000000002,"stdDev":5.646317805222777,"skewness":0.21577547161295202,"readings":100,"groups":20,"subgroupSize":5,"target":220.0},"status":"success","decision":"Post-change readings are close to target with much lower variation."}
{"step_id":9,"inputs_digest":{"batch":"sustaining","readings":100},"method_id":"basic.normality","outputs":{"pValue":0.5410651521150227},"status":"success","decision":"No evidence against normality was detected by the computed test."}
{"step_id":10,"inputs_digest":{"batch":"sustaining","groups":20,"subgroupSize":5},"method_id":"control_chart.xbar_r","outputs":{"xBarChartCenterLine":219.39270000000002,"flaggedXBarCount":0,"groups":20,"subgroupSize":5,"rChartFlaggedCount":0},"status":"success","decision":"Post-change X-bar chart has zero flags; R chart also had zero flags."}
{"step_id":11,"inputs_digest":{"batch":"sustaining","readings":100,"specWidth":80.0},"method_id":"capability.normal","outputs":{"cp":2.317454386948129,"cpk":2.2822696357182903,"pp":2.3614209814757787,"ppk":2.325568707424524,"readings":100,"specWidth":80.0},"status":"success","decision":"Post-change potential and overall capability are both strong on this sample."}
{"step_id":12,"inputs_digest":{"batches":"process_run_vs_sustaining","preReadings":125,"postReadings":100},"method_id":"basic.two_sample_t","outputs":{"tStatistic":8.632373210605964,"pValue":5.159111477818606e-15,"meanChange":-12.88089999999994,"stdDevChange":-9.796069629284212,"varianceRatioPostToPre":0.13369086994307292,"preReadings":125,"postReadings":100},"status":"success","decision":"The post-change sample is materially lower in mean and variation than the earlier run."}
{"step_id":13,"inputs_digest":{"batch":"sustaining","readings":100},"method_id":"capability.normal","outputs":{"outOfSpec":0,"outOfSpecPct":0.0,"min":208.67,"max":234.24,"readings":100,"lsl":180.0,"usl":260.0},"status":"success","decision":"No post-change readings were outside the recorded specifications."}
{"step_id":14,"inputs_digest":{"batch":"process_run","readings":125},"method_id":"capability.normal","outputs":{"outOfSpec":1,"outOfSpecPct":0.8,"min":202.2,"max":261.8,"readings":125,"lsl":180.0,"usl":260.0},"status":"success","decision":"The earlier run contained one above-limit reading and no below-limit readings."}
{"step_id":15,"inputs_digest":{"attempt":"sustaining calculation","error":"NumPy ndarray.ptp API removed"},"method_id":"control_chart.xbar_r","outputs":{},"status":"failed","decision":"Initial calculation failed before producing results; corrected with np.ptp and rerun successfully."}
```

## Submitted route declarations
```json
[{"point":"msa_gate","chosen_branch":"declare gauge verdict and release process run","observed":{"percentStudyVariation":25.595558960756396,"ndc":5.325263048633628}},{"point":"process_analysis","chosen_branch":"request applicator and sustaining batches","observed":{"flaggedXBarCount":20}},{"point":"post_change","chosen_branch":"hold the change and strengthen monitoring","observed":{"flaggedXBarCount":0,"outOfSpecPct":0.0}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
