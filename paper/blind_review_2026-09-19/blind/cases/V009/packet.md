# Blind item V009

Focal assessment: Applicability of the response-surface model and the basis for subsequent optimization.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the development team on an assembled optical module. The seal between the two housings must hold at least 45 N, and the product margin the programme committed to needs it above 55 N. Sixty consecutive assemblies have been pulled and tested in the order they were built. The archive also holds a screening run in which three assembly settings were each taken to a low and a high level twice over; a later composite design over two of those settings, with the centre setting run five times; and twenty seals made at the settings that design work recommended.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: how the line has behaved across the baseline, where seal strength sits against what the product requires, whether the settings that were varied account for it, what the design work supports concluding, and what should happen next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
{"screening_significant":{"field":"any_factor_significant","op":"==","value":true,"source":"Montgomery DAOE 6e 11.2"}}
```

## Submitted report (complete, identifiers removed)
# Seal Strength Project Report

## Data obtained
All requested project batches were released by the steward and used for the computations below; none were denied.

## 1. Baseline line behaviour
Sixty consecutive assemblies were measured in build order. The baseline seal strengths had mean 52.09 N, median 51.36 N, and sample standard deviation 4.669 N. Minimum and maximum values were 42.88 N and 62.92 N. Normality was not rejected (Shapiro-Wilk W = 0.9805, p = 0.452). Against the product lower specification limit of 45.0 N, the baseline one-sided capability was Cpk = 0.587 and Ppk = 0.507, both below 1, so the line was not capable. An individuals control chart had centre line 52.09 N, UCL = 64.19 N, LCL = 40.00 N, and 0 out-of-control flags; this suggests the baseline line was stable but consistently too close to the lower limit.

## 2. Seal strength against product requirements
The product requires the seal to hold at least 45.0 N, and the programme margin requires strength above 55.0 N. In baseline, 3 of 60 assemblies were below 45.0 N and 41 of 60 were below 55.0 N. The line therefore did not meet either requirement at the start of this work.

## 3. Screening-run conclusions
The screening run was a 16-run two-level experiment in three assembly settings, with two replicates per corner. The full factorial model was significant (p = 0.000345, R-squared = 93.6%). Bond angle and bead spacing were significant factors (p = 3.71e-05 and p = 0.000316, respectively), and their interaction was also significant (p = 0.0195). Cure temperature was not significant (p = 0.853). This supports concluding that the settings that were varied, particularly bond angle and bead spacing, account for the seal strength.

## 4. Composite-design conclusions
The composite design over bond angle and bead spacing, with the centre run five times, consisted of 13 runs. A full quadratic response-surface model fit well: R-squared = 99.6%, adjusted R-squared = 99.3%, and lack-of-fit p = 0.575. The stationary point was predicted at 59.72 N, and the optimizer returned the same practical point at coded bond_angle = 0.760 and coded bead_spacing = 0.745, with predicted response 59.72 N.

## 5. Confirmation run at the recommended settings
Twenty seals were then made at the settings the design work recommended. The confirmation run had mean 58.607 N, median 58.68 N, and standard deviation 1.935 N. Normality was not rejected (Shapiro-Wilk W = 0.9722, p = 0.801). Minimum and maximum values were 54.62 N and 61.71 N; 0 of 20 were below 45.0 N, and 1 of 20 were below 55.0 N. Against the lower limit of 45.0 N, Cpk = 1.942 and Ppk = 2.345, so the current settings are now capable of holding at least 45 N. Against a strict individual-seal interpretation of the 55.0 N programme margin, Cpk = 0.515 and Ppk = 0.622. One-sample t-tests confirmed the mean is significantly above both 45.0 N (t = 31.456, one-sided p = 3.74e-18) and 55.0 N (t = 8.338, one-sided p = 4.5e-08).

## 6. What should happen next
1. Freeze the recommended coded settings: bond_angle = 0.760 and bead_spacing = 0.745.
2. Monitor the line with an individuals/moving-range chart going forward to hold the gain.
3. If the engineering requirement is that every seal must exceed 55.0 N, the current confirmation run shows one value below that margin and capability against 55 N is still too low (Cpk 0.515, Ppk 0.622); further work should reduce variation or shift the process higher before committing to the programme margin statement.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"baseline","sampleSize":60,"groups":1},"method_id":"basic.descriptive_summary","outputs":{"sampleSize":60,"mean":52.094833333333334,"median":51.355000000000004,"stdDev":4.669088936524463,"skewness":0.2629089001685771,"adPValue":0.15,"min":42.88,"max":62.92,"countBelow45":3,"countBelow55":41},"status":"success","decision":"Baseline descriptive summary computed"}
{"step_id":2,"inputs_digest":{"batch":"baseline","sampleSize":60},"method_id":"basic.normality","outputs":{"pValue":0.45211939336700513,"statistic":0.980547194474672},"status":"success","decision":"Baseline normality not rejected"}
{"step_id":3,"inputs_digest":{"batch":"baseline","sampleSize":60,"lsl":45.0},"method_id":"capability.normal","outputs":{"cpk":0.5869104771848702,"ppk":0.5065109010763119},"status":"success","decision":"Baseline not capable against 45 N"}
{"step_id":4,"inputs_digest":{"batch":"baseline","sampleSize":60},"method_id":"control_chart.imr","outputs":{"individualsUCL":64.18520960451977,"individualsLCL":40.00445706214689,"centerLine":52.094833333333334,"flaggedCount":0},"status":"success","decision":"Baseline stable over time"}
{"step_id":5,"inputs_digest":{"batch":"screening_run","sampleSize":16,"groups":1},"method_id":"doe.factorial_analysis","outputs":{"modelPValue":0.0003450875084604319,"rSquaredPct":93.60065448974846,"bondAnglePValue":3.7126308417585684e-05,"beadSpacingPValue":0.0003159527006047807,"cureTemperaturePValue":0.8534673068258881,"interactionPValue":0.019504834946750368},"status":"success","decision":"Factorial model significant; bond angle and bead spacing matter"}
{"step_id":6,"inputs_digest":{"batch":"composite_design","sampleSize":13,"groups":5},"method_id":"doe.rsm_analysis","outputs":{"rSquaredPct":99.58951944089024,"lackOfFitPValue":0.5749941911405583,"rSquaredAdjPct":99.29631904152613},"status":"success","decision":"Full quadratic response surface is adequate"}
{"step_id":7,"inputs_digest":{"batch":"composite_design","sampleSize":13},"method_id":"doe.rsm_canonical","outputs":{"predictedAtStationary":59.7214953542036,"bondAngleCanonical":0.7604657783911608,"beadSpacingCanonical":0.7447278722019034},"status":"success","decision":"Stationary point identified"}
{"step_id":8,"inputs_digest":{"batch":"composite_design","sampleSize":13},"method_id":"doe.rsm_optimizer","outputs":{"predictedResponse":59.72149535420354,"bondAngleCodedOpt":0.7604657117963047,"beadSpacingCodedOpt":0.7447276688460702},"status":"success","decision":"Recommended coded settings found by optimizer"}
{"step_id":9,"inputs_digest":{"batch":"confirmation_runs","sampleSize":20,"groups":1},"method_id":"basic.descriptive_summary","outputs":{"sampleSize":20,"mean":58.60699999999999,"median":58.68,"stdDev":1.9345504033645384,"skewness":-0.1888186382950675,"adPValue":0.15,"min":54.62,"max":61.71,"countBelow45":0,"countBelow55":1},"status":"success","decision":"Confirmation run descriptive summary computed"}
{"step_id":10,"inputs_digest":{"batch":"confirmation_runs","sampleSize":20},"method_id":"basic.normality","outputs":{"pValue":0.8012679290053409,"statistic":0.9722380469808627},"status":"success","decision":"Confirmation data approximately normal"}
{"step_id":11,"inputs_digest":{"batch":"confirmation_runs","sampleSize":20,"lsl":45.0},"method_id":"capability.normal","outputs":{"cpk":1.941837954454652,"ppk":2.344558538654928},"status":"success","decision":"Confirmation run capable against 45 N"}
{"step_id":12,"inputs_digest":{"batch":"confirmation_runs","sampleSize":20,"target":45.0},"method_id":"basic.one_sample_t","outputs":{"tStatistic":31.455553617959925,"pValue":3.741024404656802e-18},"status":"success","decision":"Mean significantly above 45 N"}
{"step_id":13,"inputs_digest":{"batch":"confirmation_runs","sampleSize":20,"target":55.0},"method_id":"basic.one_sample_t","outputs":{"tStatistic":8.338368626440896,"pValue":4.5046555198870935e-08},"status":"success","decision":"Mean significantly above 55 N"}
{"step_id":14,"inputs_digest":{"batch":"confirmation_runs","sampleSize":20,"lsl":55.0},"method_id":"capability.normal","outputs":{"cpk":0.5147504594486602,"ppk":0.621505302339113},"status":"success","decision":"Confirmation run not yet capable against every-seal-above-55 interpretation"}
```

## Submitted route declarations
```json
[{"point":"baseline_stability","chosen_branch":"continue_to_screening","observed":{"flaggedCount":0,"cpk":0.5869104771848702,"ppk":0.5065109010763119}},{"point":"screening_significance","chosen_branch":"declare_any_factor_significant_true","observed":{"modelPValue":0.0003450875084604319,"rSquaredPct":93.60065448974846,"bondAnglePValue":3.7126308417585684e-05,"beadSpacingPValue":0.0003159527006047807}},{"point":"composite_optimization","chosen_branch":"recommended_settings_from_optimizer","observed":{"bondAngleCodedOpt":0.7604657117963047,"beadSpacingCodedOpt":0.7447276688460702,"predictedResponse":59.72149535420354}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
