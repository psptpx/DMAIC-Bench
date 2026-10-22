# Blind item B012

Focal assessment: Whether readings can support substantive analysis after the measurement system study.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

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
# Coating Thickness Project Report

## 1. Charter and acceptance range

The process target is **220.0 um**, with an accepted range of **180.0 to 260.0 um**.

## 2. Measurement system (MSA)

The released repeat-readings study contains **3 operators x 10 parts x 3 replicates** (90 measurements).

A crossed gage R&R was computed from those data:

- Percent study variation (`percentStudyVariation`): **44.438146%**
- Percent tolerance (`percentTolerance`): **54.843789%**
- Number of distinct categories (`ndc`): **2**

The steward gate for proceeding to the process-run data is the MSA acceptance criterion. Our computed `grr_pct` is **54.843789%**, and `ndc` is **2**. The measurement system does **not** pass the gate.

### Conclusion on gage capability

The recorded thickness readings from this gauge cannot carry a conclusion about the process. The gage R&R is too high and the number of distinct categories is too low; measurement variation would overwhelm process variation.

## 3. Process behaviour across the run and capability to specification

No process-run data were released. The batch _Thickness readings in sampling order, five to a point_ remains locked because the MSA gate failed (`grr_pct` did not meet the acceptance criterion). Therefore, no computation can be made for:

- how the line behaved across the run;
- where coating thickness sits against 180-260 um;
- applicator-to-applicator differences;
- monitoring record since the change.

There is no data for these steps, and the conclusion stops here rather than relying on guesses.

## 4. What should change next

The next action is not to adjust the process first, but to improve the measurement system. The plant should:

1. Investigate why gage R&R is above the acceptance criterion (`grr_pct = 54.843789%`).
2. Retrain operators and standardise the thickness-gauge method.
3. Inspect and maintain the gauge/fixture and repeatability conditions.
4. Rerun the MSA before collecting or using process-run data, with an acceptable `grr_pct` and an improved number of distinct categories.

Once the measurement system passes, the line, applicator, and monitoring batches should be released and analysed.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"stage_id":"define","records":1},"method_id":"meta.data_profiling","outputs":{"lsl":180.0,"target":220.0,"usl":260.0,"toleranceUm":80.0},"status":"success","decision":"Recorded project charter and accepted coating-thickness range."}
{"step_id":2,"inputs_digest":{"stage_id":"msa","numOperators":3,"numParts":10,"numReplicates":3,"totalReadings":90},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":44.43814624,"percentTolerance":54.84378863,"ndc":2,"numOperators":3,"numParts":10,"numReplicates":3,"totalReadings":90,"grr_pct":54.84378863},"status":"success","decision":"Crossed gage R&R shows percent GRR > 30% and ndc < 5; measurement system is not adequate for process-run conclusions."}
{"step_id":3,"inputs_digest":{"stage_id":"process_run","requested":true},"method_id":"meta.data_profiling","outputs":{},"status":"refused","decision":"Thickness readings in sampling order were locked because grr_pct=54.843789 did not satisfy grr_pct <= 30 [msa_pass], so no process-run analysis could be run."}
```

## Submitted route declarations
```json
[{"point":"gate:msa_pass","chosen_branch":"stop_at_measurement_system_failure","observed":{"grr_pct":54.84378863,"ndc":2,"required_grr_pct_max":30}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
