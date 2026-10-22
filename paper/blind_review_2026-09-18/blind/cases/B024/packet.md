# Blind item B024

Focal assessment: Baseline temporal stability and the analyses and conclusions that may follow.

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
# Brightness improvement — baseline assessment

## Executive decision
The recorded measurements support conditional process investigation, but neither an unqualified measurement-system approval nor stable long-term capability has been demonstrated. All released production readings meet the accepted range. A moving-range alarm and a strongly skewed distribution mean that observed conformance is not assurance of future conformance. This project remains at baseline assessment, not verified improvement or control closure.

## Can the readings be relied on?
The crossed study contains 90 readings across 10 parts, 3 operators and 3 repeats. Random-effects ANOVA gave an interaction p-value of 0.8084; the nonsignificant interaction was pooled into repeatability. Negative variance components would have been truncated at zero.

Gage R&R is 12.67% of study variation and 13.61% of tolerance, with 11 distinct categories. This is a conditionally usable, rather than excellent, measurement system. Repeatability variance (19.249) dominates operator variance (1.329). Improve fixturing, optical alignment, warm-up and reading procedure before treating marginal units as confidently classified. These are investigation targets, not proven causes. This study assesses precision, not calibration bias, linearity, long-term drift or spatial patchiness.

## How the line behaved
The 50 chronological readings average 429.884 cd/m², with median 420.75, sample standard deviation 39.884 and skewness 1.211. The observed span is 374.2 to 544.2 cd/m².

An individuals chart using successive moving ranges has center 429.884, lower limit 306.659 and upper limit 553.109 cd/m². There are 0 individual beyond-limit signals. The moving-range mean is 46.333 and upper limit is 151.369; there is 1 beyond-limit moving range. The largest jump, 167.6, occurs from unit 20 (376.6) to unit 21 (544.2). Unit positions here are counted from the start of the released run.

Investigate that transition and retain it in the baseline unless a documented assignable cause justifies a separate phase. These are conventional beyond-limit tests, not an exhaustive run-rule analysis. Skewness also makes normal-theory alarm rates approximate. Absence of individual alarms does not establish stability when the moving-range chart signals.

## Brightness against acceptance today
The accepted range is 350–550 cd/m². There are 0 observations below and 0 above it: observed conformance is 100%. Even with no observed failures, the one-sided 95% exact binomial upper bound for the defect fraction is 5.82%, conditional on independent representative sampling. The process signal weakens that assumption.

Anderson–Darling normality gives statistic 1.8276 and p-value 9.69242e-05. A normal capability model is not supported. As a descriptive alternative only, empirical percentile performance gives Pp 1.187 and Ppk 1.058, using lower and upper tail probabilities of 0.00135 from each end and linear sample quantiles 374.359 and 542.897. The lower-side median margin is limiting. These extreme sample quantiles are poorly determined by this small run: the indices are not validated population capability or evidence of predicted yield. Stable predictive capability cannot yet be computed defensibly. The archive is the available baseline; its applicability to present-day unchanged production was not confirmed.

## Causes, changes and next actions
No causal factor records, documented intervention, experiment or post-change confirmation batch were released. Requests for downstream data and process-history clarification were unroutable; this is not a steward finding that a named batch definitively does not exist. There are no recorded process facts available to confirm operating changes. Consequently, no root cause, actual change, achieved improvement or sustained benefit can be claimed from this task.

The quality engineer should review the flagged transition against lot, station, material, recipe, warm-up and maintenance history. The metrology owner should verify calibration against a reference and standardize the reading method, then repeat the crossed study after any measurement change. Manufacturing should collect a longer chronological baseline with those contextual factors and with a measure of within-panel uniformity: a scalar brightness reading alone does not resolve the patchiness complaint.

After confirming the measurement method and separating any justified process phases, investigate candidate factors through a controlled experiment rather than shifting the brightness setpoint on this evidence alone. Verify the chosen change on independent production, reassess distribution and capability, and compare conformance with the baseline.

## Holding a verified improvement
Assign manufacturing responsibility for chronological brightness and moving-range monitoring and quality responsibility for specification disposition. Treat control limits and acceptance limits separately. Use current limits only as provisional investigation thresholds; establish a fresh baseline after verified stabilization rather than continually widening limits. On a signal, check the measurement system, contain suspect production, document the assignable cause and verify restart. Preserve calibration and fixture checks, traceable reaction records, and periodic measurement-study review. Control closure requires post-change records that are not available here.

## Audit trail
The accompanying trace records the computations and route decisions. The local analysis script reproduces results from the steward JSON batches. Rounded figures above are taken directly from trace outputs; recommendations are prospective, not reported interventions.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":12.672291552221276,"percentTolerance":13.609116407734396,"ndc":11,"interactionPValue":0.8083824385781958,"repeatabilityVariance":19.24939189057832,"operatorVariance":1.329280264895631,"interactionVariance":0.0,"partVariance":1260.8871745063886,"n":90,"operators":3,"parts":10,"replicates":3,"lsl":350.0,"usl":550.0},"status":"success","decision":"ANOVA random effects; pool interaction if p >= 0.05.","inputs_digest":{"batch":"msa"}}
{"step_id":2,"method_id":"basic.descriptive_summary","outputs":{"mean":429.88399999999996,"median":420.75,"stdDev":39.88408899676713,"skewness":1.2107798032721664,"adPValue":9.692419169884592e-05,"n":50,"minimum":374.2,"maximum":544.2,"belowLSL":0,"aboveUSL":0},"status":"success","decision":"All released readings; specification counts empirical.","inputs_digest":{"batch":"process_run"}}
{"step_id":3,"method_id":"control_chart.imr","outputs":{"individualsUCL":553.1091411202779,"individualsLCL":306.65885887972206,"centerLine":429.88399999999996,"flaggedCount":0,"movingRangeMean":46.33265306122449,"movingRangeUCL":151.3687775510204,"movingRangeFlaggedCount":1,"withinSigma":41.075047040092635},"status":"success","decision":"Individual and successive moving-range charts; beyond-limit rule.","inputs_digest":{"batch":"process_run","n":50}}
{"step_id":4,"method_id":"basic.normality","outputs":{"pValue":9.692419169884592e-05,"statistic":1.8275535190596344},"status":"success","decision":"Anderson-Darling normality with estimated normal parameters.","inputs_digest":{"batch":"process_run"}}
{"step_id":5,"method_id":"capability.nonnormal","outputs":{"pp":1.186675403366545,"ppk":1.0581525867491708,"lowerQuantile":374.35876,"upperQuantile":542.896845,"median":420.75,"tailProbability":0.00135},"status":"success","decision":"Empirical percentile snapshot using linear quantiles, NOT fitted population capability. Extreme tails poorly estimated and run unstable; no predictive claim.","inputs_digest":{"batch":"process_run","n":50}}
{"step_id":6,"method_id":"meta.data_profiling","outputs":{"defectCount":0,"observedConformancePct":100.0,"oneSided95DefectUpperPct":5.815507911697225,"confidencePct":95,"maxMovingRange":167.60000000000002,"eventFromUnit":20,"eventToUnit":21,"eventFromBrightness":376.6,"eventToBrightness":544.2},"status":"success","decision":"Exact binomial upper bound assumes independent representative units; event units are one-based.","inputs_digest":{"batch":"process_run"}}
```

## Submitted route declarations
```json
[{"point":"measurement_adequacy","chosen_branch":"conditional use, improve gage","observed":{"grr_pct":12.672291552221276,"ndc":11}},{"point":"stability","chosen_branch":"investigate moving-range signal before predictive capability","observed":{"movingRangeFlaggedCount":1}},{"point":"distribution","chosen_branch":"nonnormal empirical snapshot only","observed":{"normalityPValue":9.692419169884592e-05}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
