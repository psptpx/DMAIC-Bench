# Blind item B004

Focal assessment: Baseline temporal stability and the analyses and conclusions that may follow.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

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
# Wave-soldering fillet-height project report

## Business position

The accepted fillet-height range is 6.80 to 7.50 mm, with 7.15 mm as target. At the 0.05 decision standard, the baseline is centered and stable in the recorded sequence, but it does not have enough margin within the accepted range. The designed run identifies chain speed and rail angle—and their interaction—as significant contributors to fillet height. The later process log does not show that the three uncontrolled logged variables explain fillet height. The labeled after-change window did not demonstrate a credible mean shift, but it did show materially greater short-term and overall spread. The exact physical change cannot be identified from the available data; the process-fact requests returned no matching fact, so causal attribution for the window-to-window difference stops there.

## Baseline behavior

The baseline record contains 60 consecutive joints. Its mean is 7.16048 mm, median is 7.1765 mm, and standard deviation is 0.139507 mm. No joint is below the 6.80 mm lower limit and none is above the 7.50 mm upper limit.

An individuals chart has a center line of 7.16048 mm, upper control limit of 7.57046 mm, and lower control limit of 6.75050 mm. Zero points exceed those limits. The Anderson-Darling normality p-value is 0.535813, the time-order correlation is 0.152514 with p-value 0.244691, and a one-sample test against the 7.15 mm target gives p-value 0.562735. There is therefore no demonstrated normality violation, linear time trend, or offset from target.

The capability problem is spread rather than centering. Baseline Cp is 0.853700, Cpk is 0.828129, Pp is 0.836276, and Ppk is 0.811227. Although production remained inside the accepted range in this sample, the low indices show that ordinary variation leaves little protection and that wider variation can produce nonconforming fillets.

## What accounts for fillet height

The replicated two-level, three-factor designed run has 16 observations. Its full factorial model p-value is 0.0000768869 and it explains 95.6501% of the response variation. In coded units, the chain-speed coefficient is 0.144331 mm, the rail-angle coefficient is 0.092856 mm, and the chain-speed-by-rail-angle coefficient is 0.047994 mm. Chain speed has factorial p-value 0.00000578114 and rail angle 0.000141818; their interaction has p-value 0.00807677. In contrast, air pressure has p-value 0.0652331 and is not significant at 0.05.

These experimental results support chain speed and rail angle, not air pressure, as the settings that account for fillet-height differences in the designed run. They explain the designed contrast; they are not alone a proof that they explain all common-cause variation in the separate 60-joint baseline.

The three variables merely logged through the run do not provide a competing explanation. A joint OLS model using preheat-zone temperature, conveyor-width setting, and solder-pot dwell has 48 observations, p-value 0.893105, and R-squared of only 1.37157%. Their individual correlations have p-values 0.532133, 0.657482, and 0.655030. None is significant at 0.05.

## Before-versus-after change

Each labeled window contains 30 joints. The mean moves from 7.15667 mm before to 7.1957 mm after, while the standard deviation increases from 0.103152 mm to 0.147313 mm. Normality is not rejected in either window.

The variance-equality test is significant, with statistic 5.57004 and p-value 0.0216554. The mean increases by 0.0390333 mm after the change, with confidence interval from −0.0268545 to 0.104921 mm and Welch p-value 0.239919. A Mann-Whitney check similarly gives p-value 0.359308. Therefore the data do not demonstrate a credible mean change; they do demonstrate increased dispersion.

Capability deteriorates in the after window. Before it, Cp is 1.12645, Cpk is 1.10499, Pp is 1.13102, and Ppk is 1.10948. After it, Cp is 0.735054, Cpk is 0.639077, Pp is 0.791962, and Ppk is 0.688554. Again, no observed joint in either 30-piece window lies outside the accepted range. The loss of margin is a leading indicator and should be treated as a process-risk finding, not dismissed because zero defects were observed.

The labels establish sequence, but not mechanism. The process-fact requests returned no matching fact, so the exact setting—or even the physical nature—of what was changed cannot be computed or named. Consequently, the increase in variation cannot be causally assigned to that change from these data.

## Recommended actions

First, stop treating the current condition as acceptable merely because the observed samples contain zero out-of-spec joints. Investigate the after-window spread increase and restore traceable records identifying every line setting. Until that mechanism is documented, report only a temporal association with the after window, not a proven effect.

Second, run a controlled confirmation of the designed-run direction: high chain speed, low rail angle, and air pressure centered at its coded value. The full factorial prediction at those coded settings is 7.16968 mm, with interval 7.02827 to 7.31108 mm for a new observation. Translate the coded settings into their actual engineering units before operation; those units were not part of the released design data and cannot be inferred here. Confirm the result on subsequent production rather than assuming the prediction.

Third, continue an individuals chart and recompute capability on a defined next sample. Release further change only after spread returns to at least the before-window level, the selected settings remain on target, and the chart remains free of control signals. Record actual settings and any intervention in the batch history so the next investigation can distinguish cause from sequence.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"baseline","sampleSize":60},"method_id":"basic.descriptive_summary","outputs":{"mean":7.1604833333333335,"median":7.1765,"stdDev":0.13950742543467862,"skewness":-0.2457671514609367,"adPValue":0.535813052387367,"minimum":6.807,"maximum":7.414,"sampleSize":60.0},"status":"success","decision":"Baseline summary computed from all ordered joints."}
{"step_id":2,"inputs_digest":{"batch":"baseline","sampleSize":60},"method_id":"basic.normality","outputs":{"pValue":0.535813052387367,"statistic":0.31442770376673224,"alpha":0.05},"status":"success","decision":"Normality not rejected."}
{"step_id":3,"inputs_digest":{"batch":"baseline","sampleSize":60,"predictor":"timeOrder"},"method_id":"basic.correlation","outputs":{"correlationCoefficient":0.15251432374816176,"pValue":0.24469145314880297,"alpha":0.05},"status":"success","decision":"No significant linear time-order trend."}
{"step_id":4,"inputs_digest":{"batch":"baseline","sampleSize":60},"method_id":"control_chart.imr","outputs":{"individualsUCL":7.570463499218656,"individualsLCL":6.750503167448011,"centerLine":7.1604833333333335,"flaggedCount":0},"status":"success","decision":"No individual point beyond control limits."}
{"step_id":5,"inputs_digest":{"batch":"baseline","sampleSize":60,"lsl":6.8,"target":7.15,"usl":7.5},"method_id":"capability.normal","outputs":{"cp":0.8536998350742169,"cpk":0.8281294923950885,"pp":0.8362756771057566,"ppk":0.8112272294438739,"lsl":6.8,"target":7.15,"usl":7.5,"belowLSLCount":0.0,"aboveUSLCount":0.0},"status":"success","decision":"Center near target, but spread is inadequate."}
{"step_id":6,"inputs_digest":{"batch":"baseline","sampleSize":60,"hypothesizedMean":7.15},"method_id":"basic.one_sample_t","outputs":{"pValue":0.5627349992385431,"tStatistic":0.5820733238568926,"alpha":0.05},"status":"success","decision":"Mean not distinguishable from target."}
{"step_id":7,"inputs_digest":{"batch":"design","runs":16,"factors":3},"method_id":"doe.factorial_analysis","outputs":{"sampleSize":16.0,"modelPValue":7.688688499771875e-05,"rSquaredPct":95.65009623416219,"rSquaredAdjPct":91.8439304390541,"chainSpeedPValue":5.781140867010384e-06,"railAnglePValue":0.00014181781816854016,"airPressurePValue":0.06523312049063436,"speedAngleInteractionPValue":0.00807677070204324,"factorCount":3.0,"intercept":7.166193750000003,"chainSpeedCoefficient":0.14433124999999944,"railAngleCoefficient":0.09285625000000054,"speedAngleCoefficient":0.04799375000000049,"airPressureCoefficient":0.029281250000000453,"designLevels":2.0},"status":"success","decision":"Chain speed, rail angle, and their interaction are significant; air pressure is not at alpha 0.05."}
{"step_id":8,"inputs_digest":{"batch":"design","runs":16,"factor":"chain_speed"},"method_id":"anova.oneway","outputs":{"sampleSize":16.0,"factorPValue":0.0004076962922869165,"fStatistic":21.21625768001748},"status":"success","decision":"Single-factor factorial model computed."}
{"step_id":9,"inputs_digest":{"batch":"design","runs":16,"factor":"rail_angle"},"method_id":"anova.oneway","outputs":{"sampleSize":16.0,"factorPValue":0.04891530552036835,"fStatistic":4.650755992151346},"status":"success","decision":"Single-factor factorial model computed."}
{"step_id":10,"inputs_digest":{"batch":"design","runs":16,"factor":"air_pressure"},"method_id":"anova.oneway","outputs":{"sampleSize":16.0,"factorPValue":0.5602763356034802,"fStatistic":0.35597269068290505},"status":"success","decision":"Single-factor factorial model computed."}
{"step_id":11,"inputs_digest":{"batch":"logged_variables","sampleSize":48,"predictors":["v1","v2","v3"]},"method_id":"regression.ols","outputs":{"sampleSize":48.0,"modelPValue":0.8931051172421495,"rSquaredPct":1.3715685037973269,"rSquaredAdjPct":-5.353097280034658,"v1PValue":0.6102380201868816,"v2PValue":0.7654909241233165,"v3PValue":0.7317844121532139,"predictorCount":3.0},"status":"success","decision":"The three logged variables jointly do not significantly explain fillet height."}
{"step_id":12,"inputs_digest":{"batch":"logged_variables","sampleSize":48,"predictor":"v1"},"method_id":"basic.correlation","outputs":{"sampleSize":48.0,"correlationCoefficient":0.09241808810960797,"pValue":0.5321333746894727,"alpha":0.05},"status":"success","decision":"No significant individual logged-variable correlation."}
{"step_id":13,"inputs_digest":{"batch":"logged_variables","sampleSize":48,"predictor":"v2"},"method_id":"basic.correlation","outputs":{"sampleSize":48.0,"correlationCoefficient":0.06565978511052907,"pValue":0.6574820774597988,"alpha":0.05},"status":"success","decision":"No significant individual logged-variable correlation."}
{"step_id":14,"inputs_digest":{"batch":"logged_variables","sampleSize":48,"predictor":"v3"},"method_id":"basic.correlation","outputs":{"sampleSize":48.0,"correlationCoefficient":0.06616117462147078,"pValue":0.6550299838488427,"alpha":0.05},"status":"success","decision":"No significant individual logged-variable correlation."}
{"step_id":15,"inputs_digest":{"batch":"after_change","window":"before","sampleSize":30},"method_id":"basic.descriptive_summary","outputs":{"sampleSize":30.0,"mean":7.156666666666669,"median":7.1375,"stdDev":0.10315182427167587,"skewness":0.5821640111938896,"minimum":6.989,"maximum":7.421},"status":"success","decision":"Window summary computed."}
{"step_id":16,"inputs_digest":{"batch":"after_change","window":"before","sampleSize":30},"method_id":"basic.normality","outputs":{"sampleSize":30.0,"pValue":0.34641428443671124,"statistic":0.3974885415070766,"alpha":0.05},"status":"success","decision":"Normality not rejected."}
{"step_id":17,"inputs_digest":{"batch":"after_change","window":"after","sampleSize":30},"method_id":"basic.descriptive_summary","outputs":{"sampleSize":30.0,"mean":7.1957,"median":7.1945,"stdDev":0.14731344719385914,"skewness":0.09694984719214211,"minimum":6.915,"maximum":7.461},"status":"success","decision":"Window summary computed."}
{"step_id":18,"inputs_digest":{"batch":"after_change","window":"after","sampleSize":30},"method_id":"basic.normality","outputs":{"sampleSize":30.0,"pValue":0.4951980309261619,"statistic":0.3320395421803326,"alpha":0.05},"status":"success","decision":"Normality not rejected."}
{"step_id":19,"inputs_digest":{"batch":"after_change","beforeN":30,"afterN":30},"method_id":"anova.equal_variances","outputs":{"sampleSize":60.0,"statistic":5.570044182141309,"pValue":0.02165539705026296,"alpha":0.05},"status":"success","decision":"Window variances were not equal at alpha 0.05."}
{"step_id":20,"inputs_digest":{"batch":"after_change","beforeN":30,"afterN":30,"variances":"unequal"},"method_id":"basic.two_sample_t","outputs":{"sampleSize":60.0,"tStatistic":-1.1888193048157785,"pValue":0.2399191446414538,"afterMinusBeforeMean":0.03903333333333148,"standardError":0.032833697413233165,"welchDF":51.92633193226183,"ci95Lower":-0.026854525644345054,"ci95Upper":0.10492119231100801,"alpha":0.05},"status":"success","decision":"No credible mean change was detected."}
{"step_id":21,"inputs_digest":{"batch":"after_change","beforeN":30,"afterN":30},"method_id":"nonparametric.mann_whitney","outputs":{"sampleSize":60.0,"pValue":0.3593075615878021,"alpha":0.05},"status":"success","decision":"The rank-based sensitivity check also found no credible location shift."}
{"step_id":22,"inputs_digest":{"batch":"design","runs":16,"chainSpeed":1,"railAngle":-1,"airPressure":0},"method_id":"doe.factorial_prediction","outputs":{"sampleSize":16.0,"predictedValue":7.169675000000002,"piLower":7.028269111720463,"piUpper":7.31108088827954,"alpha":0.05,"chainSpeedCoded":1.0,"railAngleCoded":-1.0,"airPressureCoded":0.0},"status":"success","decision":"High chain speed and low rail angle predict nearest target; pressure was centered because its effect was nonsignificant."}
{"step_id":23,"inputs_digest":{"batch":"after_change","window":"before","sampleSize":30,"lsl":6.8,"target":7.15,"usl":7.5},"method_id":"capability.normal","outputs":{"sampleSize":30.0,"cp":1.1264462809917357,"cpk":1.1049901613537907,"pp":1.131018937284096,"ppk":1.1094757194310583,"mean":7.156666666666669,"stdDev":0.10315182427167587,"belowLSLCount":0.0,"aboveUSLCount":0.0},"status":"success","decision":"Capability before the change was marginally acceptable."}
{"step_id":24,"inputs_digest":{"batch":"after_change","window":"after","sampleSize":30,"lsl":6.8,"target":7.15,"usl":7.5},"method_id":"capability.normal","outputs":{"sampleSize":30.0,"cp":0.7350539291217258,"cpk":0.6390768875192596,"pp":0.7919620977515893,"ppk":0.688554475273738,"mean":7.1957,"stdDev":0.14731344719385914,"belowLSLCount":0.0,"aboveUSLCount":0.0},"status":"success","decision":"Capability deteriorated after the change."}
```

## Submitted route declarations
```json
[{"point":"any_factor_significant","chosen_branch":"true","observed":{"chainSpeedPValue":5.781140867010384e-06,"railAnglePValue":0.00014181781816854016,"modelPValue":7.688688499771875e-05}},{"point":"change_identification","chosen_branch":"unknown_no_matching_process_fact","observed":{"meanChangeEvidenceAvailable":false,"exactSettingEvidenceAvailable":false,"provisionAttempts":3}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
