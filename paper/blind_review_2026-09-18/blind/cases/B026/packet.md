# Blind item B026

Focal assessment: Business conclusions and next steps after normal capability analysis.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

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
# Brightness line project status

## Executive conclusion

The recorded readings are usable for this assessment, with a measurement-system caution. Crossed Gage R&R was **13.3364% of study variation** and **14.4480% of tolerance**, with **10 distinct categories**. That is adequate to distinguish these sampled units, but the measurement method should still be improved before using small shifts to make decisions.

The line appears statistically stable during the released run, but stable at an unacceptable level of performance. The Individuals chart had a center line of **411.4340**, limits of **271.4807** and **551.3873**, and **0 flagged observations**. The Moving Range chart also had **0 flags**. The runs-test p-value was **0.7751**, so it did not identify nonrandom ordering.

Capability is poor against the accepted range of **350** to **550** candela per square metre. The short-term indices were **Cp 0.7145** and **Cpk 0.4390**; overall indices were **Pp 0.6856** and **Ppk 0.4212**. The line therefore cannot reliably hold the requirement even though no special-cause chart signal was detected.

## Measurement reliability

The crossed study used **90 readings**. The total Gage R&R result was **13.3364% of study variation**, its tolerance consumption was **14.4480%**, and it resolved **10 distinct categories**. Most observed variation was between units rather than the gage, but the gage result is not excellent. Use the present record for the broad conclusion that the process is underperforming; improve repeatability and operator standardization before relying on fine differences.

## Run behavior and present position

The released ordered record contains **50 readings**. Its mean was **411.4340**, median **416.8500**, and overall standard deviation **48.6166**. The accepted-range midpoint is **450.0000**, placing the run mean **38.5660** below the midpoint.

The Anderson-Darling p-value was **0.4084**, so the data did not provide evidence against the normal model used for capability. The I-MR and runs results likewise found no time-order signal. This does not mean the process is good: it means the large spread and low centering look like common-cause performance in this run rather than an isolated chart excursion.

The latest released reading was **401.6000**, which is inside the accepted range. Across the run, however, only **46 readings**, or **92.0000%**, were in range; **4 readings** were below the lower limit and **0 readings** were above the upper limit. A single acceptable latest unit therefore does not establish current capability.

## Cause, change, and achieved result

No documented process fact matched the request for assignable causes, implemented changes, or post-change evidence. The released data contain brightness outcomes but no process settings or factor labels. Consequently, no physical root cause can be attributed from this evidence.

There is also no identified intervention and no post-change brightness batch. What was changed and what that change achieved therefore **cannot be computed**; the improvement conclusion stops at the baseline. Claiming a cause or benefit would be speculation.

## What should change next

- Contain the customer risk now by reviewing units below the lower requirement and maintaining end-of-line screening while improvement work proceeds.
- First reduce common-cause brightness variation, then move the process center toward the accepted-range midpoint. The low **Cpk 0.4390** versus **Cp 0.7145** shows that both spread and lower-side centering need attention.
- Run a structured cause study with recorded candidate factors such as equipment settings, material lots, environmental conditions, and time. Randomize controlled trials where practical; do not select a cause from brightness outcomes alone.
- Improve the measurement method through fixture, setup, and operator-work standardization, then repeat the crossed study. The current **13.3364%** study-variation result is usable with caution, not a reason to stop measurement improvement.
- After an intervention, collect a new ordered run under the same measurement definition. Recheck stability before recomputing capability; compare against this baseline only after confirming the new run is stable.

## Hold plan

Continue an Individuals-Moving Range chart in production and use a documented reaction plan for chart signals or readings outside the accepted range. Once a verified improvement produces a stable run, calculate fresh limits rather than treating the present wide limits as a performance target. Track both lower-side conformance and capability, and repeat the measurement-system study after measurement-method changes or on the plant's normal audit cycle.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"msa","sampleSize":90,"numOperators":3,"numParts":10,"numReplicates":3},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":13.336418528430315,"percentTolerance":14.447970756038174,"ndc":10,"grandMean":442.3404122222222,"varianceRepeatability":21.49864487399998,"varianceReproducibility":1.695117233481606,"varianceGageRR":23.193762107481586,"variancePartToPart":1280.8518013714402,"varianceTotal":1304.0455634789218},"status":"success","decision":"Crossed random-effects ANOVA Gage R&R is conditionally acceptable for this study, but should be improved."}
{"step_id":2,"inputs_digest":{"batch":"process_run","sampleSize":50},"method_id":"meta.data_profiling","outputs":{"sampleSize":50,"lsl":350.0,"usl":550.0,"acceptedMidpoint":450.0,"meanBelowMidpoint":38.56600000000003,"latestReading":401.6,"belowLslCount":4,"aboveUslCount":0,"conformingCount":46,"conformingPct":92.0},"status":"success","decision":"The latest observation is in range, but the full run contains lower-side nonconformance."}
{"step_id":3,"inputs_digest":{"batch":"process_run","sampleSize":50},"method_id":"basic.descriptive_summary","outputs":{"mean":411.43399999999997,"median":416.85,"stdDev":48.61663698608466,"skewness":-0.15438472485919366,"adPValue":0.40837171385540083,"adStatistic":0.371831493875149},"status":"success","decision":"Anderson-Darling does not provide evidence against a normal model for these observations."}
{"step_id":4,"inputs_digest":{"batch":"process_run","sampleSize":50,"ordered":true},"method_id":"control_chart.imr","outputs":{"individualsUCL":551.3873217542337,"individualsLCL":271.48067824576634,"centerLine":411.43399999999997,"flaggedCount":0,"movingRangeMean":52.62244897959184,"movingRangeUCL":171.91754081632652,"movingRangeFlaggedCount":0,"withinSigma":46.651107251411204},"status":"success","decision":"No observations or moving ranges exceed the classical I-MR limits; the run appears stable at its current high variation."}
{"step_id":5,"inputs_digest":{"batch":"process_run","sampleSize":50,"ordered":true},"method_id":"nonparametric.runs_test","outputs":{"pValue":0.7750513736700824,"statistic":0.2857738033247041,"runsCount":27},"status":"success","decision":"The median runs test does not detect nonrandom ordering."}
{"step_id":6,"inputs_digest":{"batch":"process_run","sampleSize":50,"lsl":350.0,"usl":550.0},"method_id":"capability.normal","outputs":{"cp":0.7145239480318013,"cpk":0.4389606422338566,"pp":0.6856363459050899,"ppk":0.42121383274333274},"status":"success","decision":"The stable process is not capable against the accepted range and is shifted toward the lower limit."}
```

## Submitted route declarations
```json
[{"point":"measurement_system_gate","chosen_branch":"proceed_with_caution","observed":{"grrPct":13.336418528430315,"percentTolerance":14.447970756038174,"ndc":10}},{"point":"stability_before_capability","chosen_branch":"stable_run_normal_capability","observed":{"imrFlaggedCount":0,"runsPValue":0.7750513736700824,"adPValue":0.40837171385540083}},{"point":"causal_and_post_change_evidence","chosen_branch":"stop_without_attribution","observed":{"processFactsAvailable":false,"postChangeDataAvailable":false}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
