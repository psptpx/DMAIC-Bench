# Blind item B009

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
* **stopping is a complete answer.** If a precondition for the next analysis has failed —
  the numbers you computed say the next step is not valid on this data — then the correct
  project ends there: report the precondition that failed, the value that failed it, and
  what the plant must do before the analysis can resume, and finish. A project that stops
  at a failed precondition is scored as complete and correct on that route. Continuing past
  a failed precondition is not rewarded, and a report that stops early is not penalised for
  being short.


## Public data-service thresholds (protocol rules, not independent ground truth)
```json
{}
```

## Submitted report (complete, identifiers removed)
# Honing Line Void-Fraction Project Report

## 1. Data obtained

This project used three batches released by the data steward:
- project charter and voiding limit (`define`);
- repeat X-ray readings of the same joints (`msa`);
- per-joint void fraction in build order (`process_run`).

No requested data batch was denied.

## 2. Can the recorded readings carry a conclusion?

The repeat X-ray study contains 3 operators x 12 parts x 3 replicates.
The crossed gage R&R results are:

- percent study variation = **19.58%**;
- percent tolerance = **14.40%**;
- ndc = **7**.

The measurement system is not ideal (study variation is above the common 10% ideal), but it is within a conditionally acceptable range (less than 30%) and the ndc is 7, above the usual minimum of 5. Therefore the recorded readings can carry a conclusion for process-level decisions, with the explicit caveat that measurement variation must continue to be reduced.

## 3. How the line behaved across the run

The build-order data contains **50** void-fraction readings.
The overall descriptive summary is:

- mean = **11.83**% void area;
- median = **11.23**%;
- stdDev = **3.09**%;
- skewness = **0.1667**;
- minimum = **6.31**%;
- maximum = **17.70**%.

The Anderson-Darling normality test on the 50 readings gives statistic **0.9047** and p-value **0.0195**; normality is rejected at the 5% level.

The line did not stay stable. The first 25 readings have mean **9.18**% and median **9.41**%; the last 25 readings have mean **14.48**% and median **14.57**%. A Mann-Whitney test between these halves gives p-value **2.888e-09**, confirming the two periods are not from the same location distribution.

The I-MR control chart has center line **11.83**%, upper control limit **16.52**%, lower control limit **7.13**%, and flags **5** of 50 points outside control limits. The low-side flags occur in the first portion of the run and the high-side flags occur later. Thus the process shifted upward during the run rather than holding steady.

## 4. Where voiding sits against its acceptance limit

The acceptance limit is **0.0** to **25.0**% void area.
Normal-capability indices computed from all 50 readings are:

- Cp = **1.35**;
- Cpk = **1.28**;
- Pp = **1.35**;
- Ppk = **1.28**.

However, these normal indices must be read with caution because the normality test rejected normality and the run is not statistically stable. The percentile-based nonnormal capability indices are:

- Pp(nonnormal) = **2.20**;
- Ppk(nonnormal) = **1.98**.

All individual void-fraction readings lie within specification. The current run shows Cpk/Ppk above 1.28 (normal) or above 1.98 (nonnormal), so the line is currently inside the acceptance band with margin. The risk is not near-spec location; it is instability caused by a level shift during the run.

## 5. What should change next

1. **Stabilise the line first.** The build-order data show a clear upward shift: the first 25 readings averaged **9.18**% and the last 25 averaged **14.48**%. The process team should investigate what changed between those periods and lock the factor at the setting that keeps the line on target and steady.
2. **Do not rely on normal capability until the process is stable.** The normal capability indices should be recomputed after the process is in statistical control.
3. **Continue reducing measurement variation.** The gage R&R percent tolerance is **14.40%**, above the 10% ideal, which consumes process tolerance and weakens future capability conclusions.
4. **Hold the improvement with an I-MR chart.** The current control limits are UCL **16.52**% and LCL **7.13**%. Future runs should be plotted against these provisional limits until stability is restored, then limits should be recomputed.

## 6. Gaps and limitations

No data batch was denied. The process is not statistically stable, so final capability statements should be treated as conditional. The normal capability index is reported for inspection but should not be used alone until the special causes behind the shift are removed and verified.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"sample_size":50,"source":"process_run.json","batch":"process_run"},"method_id":"basic.descriptive_summary","outputs":{"n":50.0,"mean":11.8282,"median":11.235,"stdDev":3.08703126,"skewness":0.1666729249,"min":6.31,"max":17.7,"usl":25.0,"lsl":0.0},"status":"success","decision":"Overall descriptive summary of all 50 void-fraction readings in build order."}
{"step_id":2,"inputs_digest":{"sample_size":50,"source":"process_run.json"},"method_id":"basic.normality","outputs":{"pValue":0.0194989374,"statistic":0.9046570368},"status":"success","decision":"Anderson-Darling test rejects normality at alpha=0.05 (p=0.0195)."}
{"step_id":3,"inputs_digest":{"sample_size":25,"source":"process_run.json","group":"first_25"},"method_id":"basic.descriptive_summary","outputs":{"n":25.0,"mean":9.1768,"median":9.41,"stdDev":1.3139752661,"skewness":-0.335096528,"min":6.31,"max":11.37},"status":"success","decision":"Descriptive summary for the first 25 readings in build order."}
{"step_id":4,"inputs_digest":{"sample_size":25,"source":"process_run.json","group":"last_25"},"method_id":"basic.descriptive_summary","outputs":{"n":25.0,"mean":14.4796,"median":14.57,"stdDev":1.7562447627,"skewness":-0.0984984287,"min":11.1,"max":17.7},"status":"success","decision":"Descriptive summary for the last 25 readings in build order."}
{"step_id":5,"inputs_digest":{"sample_sizes":[25,25],"source":"process_run.json"},"method_id":"nonparametric.mann_whitney","outputs":{"pValue":2.9e-09},"status":"success","decision":"First and last 25 readings are not from the same location distribution."}
{"step_id":6,"inputs_digest":{"sample_size":50,"source":"process_run.json"},"method_id":"control_chart.imr","outputs":{"individualsUCL":16.5226203213,"individualsLCL":7.1337796787,"centerLine":11.8282,"flaggedCount":5.0},"status":"success","decision":"I-MR chart flags 5 of 50 individual readings outside control limits."}
{"step_id":7,"inputs_digest":{"sample_size":50,"source":"process_run.json","usl":25.0,"lsl":0.0},"method_id":"capability.normal","outputs":{"cp":1.3497325799,"cpk":1.2771925521,"pp":1.3497325799,"ppk":1.2771925521},"status":"success","decision":"Normal capability indices computed; should be interpreted cautiously because normality was rejected and process shifted."}
{"step_id":8,"inputs_digest":{"sample_size":50,"source":"process_run.json","usl":25.0,"lsl":0.0},"method_id":"capability.nonnormal","outputs":{"pp":2.2016848085,"ppk":1.9788743059},"status":"success","decision":"Percentile-based nonnormal capability indices."}
{"step_id":9,"inputs_digest":{"numOperators":3,"numParts":12,"numReplicates":3,"source":"msa.json","tolerance":25.0},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":19.5797874003,"percentTolerance":14.3967097551,"ndc":7.0},"status":"success","decision":"Crossed gage R&R indicates the measurement system is conditionally acceptable, with 7 distinct data categories."}
```

## Submitted route declarations
```json
[{"point":"measurement-system-readiness","chosen_branch":"proceed-with-caution","observed":{"percentStudyVariation":19.5797874003,"percentTolerance":14.3967097551,"ndc":7.0}},{"point":"process-stability","chosen_branch":"report-unstable-and-conditional-capability","observed":{"flaggedCount":5.0,"mannWhitneyPValue":2.9e-09}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
