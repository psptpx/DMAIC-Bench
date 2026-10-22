# Blind item V018

Focal assessment: Target-attainment, implementation, or closure conclusions after confirmation experiments.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the process team on a wave-soldering line. Fillet height is accepted between 6.80 and 7.50 mm with 7.15 mm as the target. Sixty consecutive joints have been recorded in the order they were made. The archive also holds a designed run in which three line settings were each taken to a low and a high level, twice over; two windows of fillet height, one before a change to the line and one after it; and a log of three further process variables that were recorded throughout but were not varied in any experiment.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: how the line has behaved across the baseline record, where fillet height sits against the range it is accepted in, whether the settings that were varied account for it, whether the change that was made can be shown to have done anything, and what should happen next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
# Fillet-Height Project Report - [TASK]

## Reviewed data
- Baseline record: n = 60 consecutive joints.
- Accepted range: lsl = 6.8, target = 7.15, usl = 7.5 mm.
- Logged-variable run: n = 48 records for v1 (preheat zone temperature), v2 (conveyor width setting), and v3 (solder pot dwell).
- Designed run: full factorial with 3 factors, 16 runs, and 2 replicates per corner.
- Before/after windows: n = 30 and n = 30 joints respectively.
- No matching process fact was available when the process owner was asked to describe the physical change between the windows; therefore the specific intervention cannot be named from this run.

## Baseline behavior and acceptance range
- Mean fillet height = 7.16048 mm, median = 7.1765 mm, standard deviation = 0.139507 mm, skewness = -0.245767.
- Minimum = 6.807 mm and maximum = 7.414 mm.
- 0 baseline joints were outside the accepted range.
- Normality checks: Shapiro-Wilk p = 0.502616 (statistic 0.981659), Anderson-Darling p = 0.535813 (statistic 0.314428). There is no evidence of non-normality.
- One-sample t-test against target 7.15 mm: p = 0.562735, t = 0.582073. The baseline mean is not detectably different from target.
- I-MR chart: center line = 7.16048 mm, UCL = 7.57046 mm, LCL = 6.7505 mm, flagged points = 0. No control signals were found.

## Capability against the accepted range
- Baseline capability: Cp = 0.8537, Cpk = 0.828129, Pp = 0.843333, Ppk = 0.818073.
- Although no individuals were outside specification, the baseline process spread is large relative to the 6.8-7.5 mm tolerance.

## Designed run: which varied settings mattered?
- The full factorial model was significant: p = 7.68869e-05, R-squared = 95.6501%, adjusted R-squared = 91.8439%.
- Chain speed was significant: p = 5.78114e-06, high-minus-low effect = 0.288663 mm.
- Rail angle was significant: p = 0.000141818, high-minus-low effect = 0.185713 mm.
- The chain-speed/rail-angle interaction was significant: p = 0.00807677.
- Air pressure was not statistically significant: p = 0.0652331, high-minus-low effect = 0.0585625 mm.
- Conclusion: the varied settings do account for much of the fillet-height variation, primarily through chain speed, rail angle, and their interaction; air pressure is not established as an active effect.

## Logged variables
- Regression of fillet height on v1, v2, and v3 gave model p = 0.893105, R-squared = 1.37157%, adjusted R-squared = -5.3531%.
- Individual p-values were v1 = 0.610238, v2 = 0.765491, and v3 = 0.731784.
- These logged variables do not account for the fillet-height response in this record.

## Before-versus-after change comparison
- Before-change window: mean = 7.15667 mm, standard deviation = 0.103152 mm, Cp = 1.12645, Cpk = 1.10499, Pp = 1.15035, Ppk = 1.12844.
- After-change window: mean = 7.1957 mm, standard deviation = 0.147313 mm, Cp = 0.735054, Cpk = 0.639077, Pp = 0.805501, Ppk = 0.700325.
- Both windows had 0 and 0 values outside specification, respectively.
- Mean difference (after minus before) = 0.0390333 mm. Welch two-sample t-test: t = -1.18882, p = 0.239919. The change cannot be shown to have shifted the mean.
- Levene equal-variance test: statistic = 5.58918, p = 0.0214412. The after-change window has significantly greater variance.
- Therefore the change is not demonstrated to have improved fillet height; the evidence points to a possible degradation in spread and capability that should be investigated.

## Recommended next actions
- Do not credit the process change as an improvement. Investigate and eliminate the increased spread in the after-change window.
- Continue I-MR monitoring and capability checks against the 6.8-7.5 mm accepted range while the issue is investigated.
- Run confirmation trials around chain speed and rail angle, including their interaction, to move the mean to target 7.15 mm without increasing spread.
- Keep logged v1-v3 records for diagnostic context, but do not treat them as response drivers based on this analysis.
- Reassess capability after corrective action and confirm that the process is stable in both location and spread.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"stage_id":"define"},"method_id":"meta.data_profiling","outputs":{"lsl":6.8,"target":7.15,"usl":7.5},"status":"success","decision":"Accepted range and target extracted"}
{"step_id":2,"inputs_digest":{"stage_id":"baseline","sampleSize":60},"method_id":"basic.descriptive_summary","outputs":{"mean":7.1604833333333335,"median":7.1765,"stdDev":0.13950742543467862,"skewness":-0.2457671514609367,"adPValue":0.535813052387367,"sampleSize":60,"minimum":6.807,"maximum":7.414,"outsideSpecCount":0},"status":"success","decision":"Baseline summarized; no values outside specification"}
{"step_id":3,"inputs_digest":{"stage_id":"baseline","sampleSize":60},"method_id":"basic.normality","outputs":{"pValue":0.502615839043691,"statistic":0.9816590963636967,"adPValue":0.535813052387367,"adStatistic":0.31442770376673224},"status":"success","decision":"No evidence of non-normality in baseline"}
{"step_id":4,"inputs_digest":{"stage_id":"baseline","sampleSize":60},"method_id":"basic.one_sample_t","outputs":{"pValue":0.5627349992385431,"tStatistic":0.5820733238568926},"status":"success","decision":"No significant baseline mean offset from target"}
{"step_id":5,"inputs_digest":{"stage_id":"baseline","sampleSize":60},"method_id":"capability.normal","outputs":{"cp":0.8536998350742169,"cpk":0.8281294923950885,"pp":0.8433329809339088,"ppk":0.8180731502192687},"status":"success","decision":"Capability below a capable-process level"}
{"step_id":6,"inputs_digest":{"stage_id":"baseline","sampleSize":60},"method_id":"control_chart.imr","outputs":{"individualsUCL":7.570463499218656,"individualsLCL":6.750503167448011,"centerLine":7.1604833333333335,"flaggedCount":0,"mrBar":0.15415254237288134,"sigmaEstimate":0.13666005529510758},"status":"success","decision":"No I-MR signals detected"}
{"step_id":7,"inputs_digest":{"stage_id":"logged_variables","sampleSize":48,"predictors":["v1","v2","v3"]},"method_id":"regression.ols","outputs":{"modelPValue":0.8931051172421621,"rSquaredPct":1.3715685037972047,"rSquaredAdjPct":-5.353097280034791,"v1PValue":0.6102380201868818,"v2PValue":0.7654909241233167,"v3PValue":0.7317844121532142,"sampleSize":48},"status":"success","decision":"Logged variables do not account for fillet height"}
{"step_id":8,"inputs_digest":{"stage_id":"design","numRuns":16,"numFactors":3,"numReplicates":2},"method_id":"doe.factorial_analysis","outputs":{"modelPValue":7.688688499771875e-05,"rSquaredPct":95.65009623416219,"rSquaredAdjPct":91.8439304390541,"chain_speedPValue":5.781140867010388e-06,"rail_anglePValue":0.00014181781816853994,"air_pressurePValue":0.06523312049063429,"chain_speed_rail_anglePValue":0.008076770702043238,"chain_speed_effect":0.28866250000000093,"rail_angle_effect":0.18571250000000106,"air_pressure_effect":0.05856250000000074,"numFactors":3,"numRuns":16,"numReplicates":2},"status":"success","decision":"Significant factorial model; chain speed, rail angle, and their interaction significant"}
{"step_id":9,"inputs_digest":{"stage_id":"after_change","n1":30,"n2":30},"method_id":"anova.equal_variances","outputs":{"pValue":0.021441224975583952,"statistic":5.5891768509483875},"status":"success","decision":"Unequal variances between before and after windows"}
{"step_id":10,"inputs_digest":{"stage_id":"after_change","n1":30,"n2":30},"method_id":"basic.two_sample_t","outputs":{"pValue":0.2399191446414538,"tStatistic":-1.1888193048157785,"mean1":7.156666666666669,"mean2":7.1957,"stdDev1":0.10315182427167587,"stdDev2":0.14731344719385914,"meanDiff":0.03903333333333148,"n1":30,"n2":30},"status":"success","decision":"No statistically significant mean difference in fillet height before versus after the change"}
{"step_id":11,"inputs_digest":{"stage_id":"after_change","window":"before","sampleSize":30},"method_id":"capability.normal","outputs":{"cp":1.1264462809917362,"cpk":1.1049901613537907,"pp":1.15035399491451,"ppk":1.128442490249464,"outsideSpecCount":0},"status":"success","decision":"Before-change window capability summarized"}
{"step_id":12,"inputs_digest":{"stage_id":"after_change","window":"after","sampleSize":30},"method_id":"capability.normal","outputs":{"cp":0.7350539291217261,"cpk":0.6390768875192596,"pp":0.8055008921044944,"ppk":0.7003254899068492,"outsideSpecCount":0},"status":"success","decision":"After-change window capability summarized"}
```

## Submitted route declarations
```json
[{"point":"factorial_significance_gate","chosen_branch":"significant_factors_declared_true","observed":{"modelPValue":7.688688499771875e-05,"chain_speedPValue":5.781140867010388e-06,"rail_anglePValue":0.00014181781816853994,"chain_speed_rail_anglePValue":0.008076770702043238}},{"point":"before_after_variance_assumption","chosen_branch":"welch_two_sample_t","observed":{"levenePValue":0.021441224975583952}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
