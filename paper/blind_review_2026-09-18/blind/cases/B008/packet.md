# Blind item B008

Focal assessment: Baseline temporal stability and the analyses and conclusions that may follow.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the quality group at a components plant. One critical characteristic has an internally accepted range of 40 to 100, and the line has left a record of sixty consecutive pieces in the order they came off. The customer has asked us to state where this characteristic stands today and to show how we arrived at that figure. Do not assume the shape of this record; look at the data itself first.

## 2. What you are asked to do

From the record the data steward can release, say whether the line has been steady over the run and where the characteristic stands against its accepted range today. Justify in your report why the figure you report is the right one for THIS data. Every number must come from a computation you ran on this task.


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
# Characteristic review — consecutive piece record

## Executive conclusion

The released record contains 60 ordered individual observations. The accepted range is 40 to 100. The line was **not steady over the run**. The median-based runs test returned p = 4.53297617025e-08; the IMR calculation identified 2 flagged individuals. The pooled capability result is inadequate: Cpk = 0.427323045196 and Ppk = 0.427323045196.

Today’s best defensible position is therefore the later-run level, not the pooled mean. The last 30 pieces have mean 94.1136, compared with 71.2168333333 for the first 30 pieces. The later level is close to the upper accepted boundary and produces upper-limit escapes.

## Evidence and method

The observations were analyzed in production order rather than assuming an independent, identically distributed sample. The overall mean is 82.6652166667, median 81.681, and standard deviation 13.5219974117. The normality test p-value is 5.43448095682e-07, so the pooled run should not be represented as one stable normal population. The runs test is appropriate for the ordered sequence and rejects steadiness. The IMR center line is 82.6652166667, with limits 59.9415419461 and 105.388891387; the flagged indices are the computed observations at zero-based positions 11 and 30.

The first 30 observations have mean 71.2168333333 and standard deviation 7.01947130381. The last 30 have mean 94.1136 and standard deviation 7.17989344172. This large level change explains why the pooled distribution is misleading and is the evidence for a process shift rather than a single steady condition.

## Range position and impact

Using the released limits 40 and 100, the record contains 7 observations above the upper limit, 0 below the lower limit, and 7 outside the accepted range. The normal capability indices computed from the pooled run are Cp = 0.739535713216, Cpk = 0.427323045196, Pp = 0.739535713216, and Ppk = 0.427323045196. These values do not support claiming capability.

The most plausible cause visible in this record is a step change in process level between the two equal subsequences; the record alone does not identify the physical assignable cause. The immediate business risk is upward drift/shift toward and beyond the upper boundary.

## Action and control

Quarantine and review product associated with the upper-limit results, investigate what changed at the transition between the first and last subsequences, and verify the measurement system before adjusting the process. Re-center the process below the upper boundary only after the cause is identified and confirmed by fresh ordered data. Hold the improvement with an individuals-and-moving-range chart, review each new result against the accepted limits, and investigate any future shift or limit breach. Capability should be recalculated only after a stable run is demonstrated; the pooled capability above is a baseline showing the present risk, not evidence of control.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"sample_size":60,"batch":"process_run","subsequence":"all_60"},"method_id":"basic.descriptive_summary","outputs":{"mean":82.66521666666667,"median":81.68100000000001,"stdDev":13.521997411740152,"skewness":-0.0023790938480819234,"adPValue":5.434480956817945e-07},"status":"success","decision":null}
{"step_id":2,"inputs_digest":{"sample_size":60,"batch":"process_run"},"method_id":"basic.normality","outputs":{"pValue":5.434480956817945e-07,"statistic":28.850663270142135,"andersonStatistic":1.2827276668885474},"status":"success","decision":"Normality rejected by the omnibus test; Anderson-Darling statistic also exceeded its tabulated critical values."}
{"step_id":3,"inputs_digest":{"sample_size":60,"batch":"process_run","ordering":"production_order","split_rule":"overall median"},"method_id":"nonparametric.runs_test","outputs":{"pValue":4.532976170252393e-08,"runs":10,"median":81.68100000000001},"status":"success","decision":"Reject steadiness: the ordered sequence has too few runs around its median."}
{"step_id":4,"inputs_digest":{"sample_size":60,"batch":"process_run","subgrouping":"individuals with moving ranges"},"method_id":"control_chart.imr","outputs":{"individualsUCL":105.38889138718596,"individualsLCL":59.94154194614737,"centerLine":82.66521666666667,"flaggedCount":2,"movingRangeMean":8.544101694915256,"sigmaWithin":7.5745582401731},"status":"success","decision":"Not stable: two individuals breach the calculated IMR limits."}
{"step_id":5,"inputs_digest":{"sample_size":30,"batch":"process_run","subsequence":"first_30"},"method_id":"basic.descriptive_summary","outputs":{"mean":71.21683333333333,"median":70.8875,"stdDev":7.019471303813235,"skewness":0.47277665691331966,"adPValue":0.43784471922710555},"status":"success","decision":null}
{"step_id":6,"inputs_digest":{"sample_size":30,"batch":"process_run","subsequence":"last_30"},"method_id":"basic.descriptive_summary","outputs":{"mean":94.1136,"median":95.69550000000001,"stdDev":7.179893441722013,"skewness":-0.7017447094254458,"adPValue":0.2536407747255206},"status":"success","decision":null}
{"step_id":7,"inputs_digest":{"sample_size":60,"batch":"process_run","limits_source":"released descriptive fields"},"method_id":"capability.normal","outputs":{"cp":0.7395357132162841,"cpk":0.42732304519554737,"pp":0.7395357132162841,"ppk":0.42732304519554737,"lsl":40.0,"usl":100.0,"aboveUSL":7,"belowLSL":0,"oosTotal":7},"status":"success","decision":"The overall normal capability estimate is inadequate and observed output includes upper-limit violations."}
```

## Submitted route declarations
```json
[{"point":"data_shape","chosen_branch":"ordered individual observations; use IMR and runs test","observed":{"sampleSize":60}},{"point":"distribution","chosen_branch":"report nonnormal overall behavior and avoid treating the pooled run as one stable normal population","observed":{"normalityPValue":5.434480956817945e-07,"runsPValue":4.532976170252393e-08}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
