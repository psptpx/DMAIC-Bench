# Blind item V054

Focal assessment: Whether readings can support substantive analysis after the measurement system study.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team at a moulding plant. Complaints from the customer's assembly line about one critical fitting dimension have risen this quarter; the internally accepted range for it is 12 to 28 mm. The line has kept a piece-by-piece record in production order, and the archive also holds the study in which the same pieces were read several times over by several inspectors. Nobody has yet gone through either of them properly.

## 2. What you are asked to do

Work through the batches the data steward can release and say where this project stands: whether the recorded readings can be relied on at all, how the line has behaved over the run, where the dimension sits against its accepted range today, and what should be done about it next. Every number in your report must come from a computation you ran on this task; where the data does not support a judgement, say so instead of making one.


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
# Critical-dimension project report

## Bottom line

The released production record looks good on its face: all 30 recorded readings were within the accepted range of 12 to 28 mm, and its calculated capability indices are high. The project cannot yet rely on those readings for precise decisions, however, because the inspector repeat study failed the measurement-system assessment. The measurement variation consumed 51.4733% of total study variation and 54.1109% of tolerance, with only 2 distinct categories. Fixing and revalidating the measurement system must come first.

## Can the recorded readings be relied on?

No, not at the level needed for final process, capability, or complaint discrimination. The balanced crossed repeat study had substantial measurement variation, dominated by repeatability. Its %Study Variation was 51.4733%, %Tolerance was 54.1109%, and it distinguished only 2 distinct categories. Under the usual measurement-system criteria, this is not an acceptable gauge for characterizing this critical dimension. The production values are recorded observations, not confirmed piece values.

## Released production run

The 30 ordered production observations had mean 19.7531 mm, median 19.858 mm, standard deviation 1.1386 mm, and skewness 0.2402. Their minimum was 17.8348 mm and maximum was 22.1142 mm, so the recorded run remained inside 12 to 28 mm. Anderson-Darling gave a p-value of 0.6665 and Shapiro-Wilk gave a p-value of 0.5893 (statistic 0.9718); neither result contradicts a normal fit to these observations, although a lack of significant departure is not proof of normality.

## Behaviour across the released run

An individuals chart fitted from the 30 ordered readings had a center line of 19.7531 mm, upper control limit 23.2142 mm, and lower control limit 16.2920 mm. None of the 30 points was outside those trial limits. The order-index correlation was 0.0182 with a p-value of 0.9240, giving no evidence of a linear drift within this run. This is a short, self-starting assessment of the released run; it does not establish long-term stability or that the process is currently unchanged.

## Capability against the accepted range

Using a normal model and the 12 to 28 mm limits, the within-subgroup indices were Cp 2.3118 and Cpk 2.2404; the overall indices were Pp 2.3421 and Ppk 2.2698. Those high values describe the released readings only. Because the gauge failed its study and the record has no released timeframe, they should not be used as confirmation that the customer complaint is resolved or that today's production has this capability.

## Evidence boundaries

The steward released only these data topics: the charter/accepted range, the inspector repeat study, and the piece-by-piece production record. No released batch gives a cause, process-change history, intervention, timeframe, complaint linkage, or post-change verification. Requests for a process-change and verification record did not route to any available data. Therefore this analysis cannot say what caused the complaints, whether any change was made, what any change achieved, or whether the released run represents today's process. Those conclusions stop here rather than being guessed.

## Next steps

1. Quarantine precise process and product decisions that depend on this gauge. Investigate the dominant repeatability problem, including instrument condition, calibration, fixture, procedure, environment, and inspector practice. Do not assume an operator effect from these data.
2. Repair or replace the measurement method and repeat a crossed MSA. Release production decisions only after the remediated gauge meets the plant's measurement-system acceptance rule and has enough distinct categories.
3. Use the validated gauge to reconfirm control and capability on a fresh, time-stamped current-production sample. Preserve production order and collect settings, cavities/material lots if applicable, inspectors, and other relevant process context.
4. Obtain and analyse complaint parts or directly linked measurements. Compare their population, timeframe, and measurement conditions with this released run before drawing any cause-and-effect conclusion.
5. If a future process change is made, lock the change under the control plan and verify it with before/after data from the validated gauge. Continue routine individuals monitoring and periodic MSA checks so the dimension is held at 19.7531 mm only if that remains the validated process center.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"source":"data/msa.json","operators":3,"parts":10,"replicates":3,"observations":90},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":51.473329606737806,"percentTolerance":54.110887452284864,"ndc":2,"observations":90,"grandMean":19.19262,"repeatabilityVariance":2.0132255837777775,"operatorVariance":0.06889931639917493,"interactionVariance":0,"partToPartVariance":5.776422083469133},"status":"success","decision":"The gauge is unacceptable for process or tolerance decisions; repeatability is the dominant measurement-error component."}
{"step_id":2,"inputs_digest":{"source":"data/process_run.json","observations":30},"method_id":"basic.descriptive_summary","outputs":{"mean":19.753083333333333,"median":19.85805,"stdDev":1.1385903883624102,"skewness":0.24016832326638138,"adPValue":0.6665468135257078,"observations":30,"lsl":12.0,"usl":28.0,"minimum":17.8348,"maximum":22.1142},"status":"success","decision":"The recorded run is centered near the middle of the accepted range and all recorded observations are inside it."}
{"step_id":3,"inputs_digest":{"source":"data/process_run.json","observations":30},"method_id":"basic.normality","outputs":{"pValue":0.5893289950784444,"statistic":0.9717934944274457,"adPValue":0.6665468135257078},"status":"success","decision":"Neither normality test contradicts a normal distribution for these 30 recorded readings."}
{"step_id":4,"inputs_digest":{"source":"data/process_run.json","observations":30,"movingRanges":29},"method_id":"control_chart.imr","outputs":{"individualsUCL":23.21415609195402,"individualsLCL":16.292010574712645,"centerLine":19.753083333333333,"flaggedCount":0,"mrBar":1.3011551724137929,"sigmaWithin":1.1535063585228662},"status":"success","decision":"The ordered run has no individual-point signal outside the trial control limits."}
{"step_id":5,"inputs_digest":{"source":"data/process_run.json","observations":30},"method_id":"capability.normal","outputs":{"cp":2.311791909046338,"cpk":2.2404394150202513,"pp":2.3420772684565065,"ppk":2.269790029431125},"status":"success","decision":"Nominal capability is high, but it is conditional on gauge remediation and confirmation."}
{"step_id":6,"inputs_digest":{"source":"data/process_run.json","observations":30,"timeOrder":true},"method_id":"basic.correlation","outputs":{"correlationCoefficient":0.018188163129476506,"pValue":0.9240008311515939},"status":"success","decision":"The order-index correlation gives no evidence of linear drift over this short run."}
```

## Submitted route declarations
```json
[{"point":"measurement_system_before_production","chosen_branch":"analyse the repeat study and declare grr_pct before requesting the production record","observed":{"percentStudyVariation":51.473329606737806}},{"point":"cause_and_change_evidence","chosen_branch":"report absence of released evidence rather than infer cause, chronology, or a change effect","observed":{"releasedBatchCount":3.0}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
