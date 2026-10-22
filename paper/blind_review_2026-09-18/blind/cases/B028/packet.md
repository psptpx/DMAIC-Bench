# Blind item B028

Focal assessment: Baseline temporal stability and the analyses and conclusions that may follow.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team on a gear-shaft heat-treatment line. Case-surface hardness is the characteristic under study and the heat-treat recipe is the candidate cause currently on the table; three recipes are in use. Sixty consecutive shafts from one population have been recorded in the order they were run, a separate sample records hardness for shafts made under each of the three recipes, the archive holds the study in which the same shafts were measured several times over by several operators on the hardness tester, and the two recipes with the highest averages have been pulled out into a sample of their own.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the recorded hardness readings can carry a conclusion, how the baseline has behaved, what kind of comparison these readings admit, what that comparison says about the recipe, and what should happen next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
# Heat-treat hardness project report

## Bottom line

The hardness tester is good enough to support the planned comparison, but the project does not yet support a causal claim that a heat-treat recipe *causes* the difference. Recipe C has the highest observed average, and the C-minus-B comparison is large and statistically strong. However, the 60-shaft baseline changes materially over run order, and no controlled, randomized recipe-change study or process-change fact was provided. The appropriate next step is a randomized, controlled confirmation trial.

## Can these readings carry a conclusion?

The crossed measurement study used 10 parts, 3 operators, and 3 replicates, for 90 hardness readings against a tolerance width of 6 HRC. Total Gage R&R was 12.7004906737% of study variation and 21.6065582208% of tolerance. The tester resolved 11 distinct categories, and part-to-part standard deviation (1.68746159345 HRC) was much larger than Gage R&R standard deviation (0.216065582208 HRC).

These results support use of the readings for this comparison. The tolerance result is not stellar, so the tester should not be assumed adequate for a much tighter requirement without a new study.

## The baseline is not a stable single story

The 60 consecutive baseline shafts averaged 60.6343333333 HRC, with median 60.93 HRC and standard deviation 2.2973605833 HRC. Their values ranged from 56.38 to 64.63 HRC.

The time order matters. Successive hardness values had correlation 0.704271207247 (p=0.000000000485832604). The individuals chart had control limits 56.7603701166 to 64.5082965501 HRC and flagged 2 individual readings; the moving-range chart flagged none. A median runs test found only 10 runs versus 31 expected (p=0.0000000453297617), with 30 readings above and 30 below the median.

Dividing at the observed break is descriptive, not a claim that an identified intervention occurred there. The first 20 shafts averaged 58.366 HRC and the last 40 averaged 61.7685 HRC, a rise of 3.4025 HRC with a two-sample 95% confidence interval of 2.50047982707 to 4.30452017293 HRC (p=0.000000000347915319). Correlation between run order and hardness was 0.843083692523 (p=0.0000000000000000291585482).

Therefore, the overall baseline mean is not a suitable estimate of one stable process level. The observed rise is real in the recorded sequence, but its cause cannot be identified from these hardness values alone.

## What kind of recipe comparison do these data admit?

The recipe batch contains 15 independent shafts for each of 3 recipes, not a randomized experiment and not a paired design. The group summaries are:

- Recipe A: mean 57.9593333333 HRC, median 58.15 HRC, standard deviation 0.909069120951 HRC, n=15.
- Recipe B: mean 59.7433333333 HRC, median 59.99 HRC, standard deviation 0.927813610182 HRC, n=15.
- Recipe C: mean 61.3273333333 HRC, median 61.49 HRC, standard deviation 0.865872529935 HRC, n=15.

Normality checks gave p=0.108693173012 for A, p=0.168295939549 for B, and p=0.376551039114 for C. The median-centered equal-variance check gave p=0.975556311874, so a one-way ANOVA is an appropriate omnibus comparison under these data.

ANOVA strongly rejects equal recipe means: F=52.4269875009 (2 and 42 degrees of freedom), p=0.00000000000383385130107. Recipe accounts for 71.400161283% of the variance in this 45-observation batch, with pooled within-recipe standard deviation 0.901291665704 HRC.

All pairwise differences are material. With multiplicity-controlled p-values, B minus A is 1.784 HRC (95% CI 1.09699531918 to 2.47100468082; adjusted p=0.000132444784585), C minus A is 3.368 HRC (95% CI 2.70399964787 to 4.03200035213; adjusted p=0.000132444784585), and C minus B is 1.584 HRC (95% CI 0.912786158348 to 2.25521384165; adjusted p=0.000132444784585). Thus C is highest, B is second, and A is lowest in this sample.

## Focused comparison of the two leading recipes

Because C and B had the two highest sample means, they were compared directly. Each group has 15 observations. A median-centered variance check gave p=0.933081669099. The pooled two-sample comparison estimated C minus B as 1.584 HRC, with 95% confidence interval 0.912786158348 to 2.25521384165 HRC; t=4.83404350634 with 28 degrees of freedom and p=0.0000436586080571. The estimated standardized effect was Cohen's d=1.76514311492 (Hedges g=1.71743654425).

A Mann–Whitney sensitivity analysis agreed: p=0.000261754719537. These results make the observed C-over-B advantage very unlikely to be a chance difference in this sample. They do not add an independent confirmation, because the leading-two batch contains the same recipe B and C observations already used to identify the leading pair.

## What these data do not establish

A strong observed recipe ordering is not proof that recipe is the cause. The recipe observations were sampled separately under the existing recipes; the available data do not identify how shafts were assigned, blind the measurements, or balance other heat-treat and material conditions. The ordered baseline also shows strong time dependence, so a time-concurrent confounder remains plausible.

A provision question about an intentional process or recipe change at the baseline break was unroutable, and the process owner reported no matching process fact. Consequently, there is no supported basis to say that a documented change occurred, what was changed, or how much improvement that change achieved. No specification limits or target were released either, so capability indices, expected out-of-specification rate, and conformance to the hardness requirement cannot be computed. Those conclusions stop here rather than being estimated from assumptions.

## Recommended next step and process hold

Do not immediately standardize recipe C as a confirmed improvement. Carry recipe C forward as the leading candidate and run a deliberately randomized, contemporaneous confirmation trial against at least recipe B, with predeclared recipe assignment, eligible shaft population, hardness operator(s), test method, alpha, power, and practical difference to detect. Mask measurement order where practical and record material heat, position in the furnace/load, line, and other process conditions so the recipe effect can be separated from time effects.

Until that trial is complete, hold the conclusion at association: recipe C was highest in this sample and beat B by the observed margin. Continue monitoring consecutive production with an individuals and moving-range chart, but investigate the baseline shift before relying on the old baseline limits. After the confirmation run, reassess the measurement study if the tester or operators change, and calculate capability only after an approved specification and a stable process are available.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"stage":"msa","parts":10,"operators":3,"replicates":3,"observations":90},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":12.700490673699216,"percentTolerance":21.606558220784553,"ndc":11,"parts":10.0,"operators":3.0,"replicates":3.0,"observations":90.0,"toleranceWidth":6.0,"gageRRStdDev":0.21606558220784552,"partToPartStdDev":1.6874615934528983},"status":"success","decision":"Acceptable; readings may support the project comparison."}
{"step_id":2,"inputs_digest":{"stage":"msa","parts":10,"operators":3,"replicates":3},"method_id":"anova.sov","outputs":{"totalVariance":2.89421096519341,"gageRRVariance":0.04668433581481525,"partToPartVariance":2.8475266293785944},"status":"success","decision":"Part variation dominates measurement variation."}
{"step_id":3,"inputs_digest":{"stage":"baseline","sampleSize":60},"method_id":"basic.descriptive_summary","outputs":{"mean":60.63433333333333,"median":60.93,"stdDev":2.297360583303699,"skewness":-0.05156972904474212,"adPValue":0.02359881666497351,"sampleSize":60.0,"minimum":56.38,"maximum":64.63},"status":"success","decision":"Overall summary is descriptive only; it mixes nonstationary segments."}
{"step_id":4,"inputs_digest":{"stage":"baseline","comparison":"lag1","sampleSize":60},"method_id":"basic.correlation","outputs":{"correlationCoefficient":0.7042712072465488,"pValue":4.858326036843666e-10},"status":"success","decision":"Strong positive serial correlation."}
{"step_id":5,"inputs_digest":{"stage":"baseline","sampleSize":60,"movingRangeSize":2},"method_id":"control_chart.imr","outputs":{"individualsUCL":64.5082965500661,"individualsLCL":56.76037011660055,"centerLine":60.63433333333333,"flaggedCount":2.0,"sigmaEstimated":1.29132107224426,"movingRangeCenterLine":1.4566101694915252,"movingRangeUCL":4.758745423728813,"movingRangeFlaggedCount":0.0},"status":"success","decision":"Not stable: two individual points signal and the chart masks a large ordered shift."}
{"step_id":6,"inputs_digest":{"stage":"baseline","center":"median","sampleSize":60},"method_id":"nonparametric.runs_test","outputs":{"pValue":4.532976170252393e-08,"runsObserved":10.0,"runsExpected":31.0,"aboveCount":30.0,"belowCount":30.0},"status":"success","decision":"Reject randomness about the median."}
{"step_id":7,"inputs_digest":{"stage":"recipes","recipe":"recipe A","sampleSize":15},"method_id":"basic.descriptive_summary","outputs":{"mean":57.95933333333333,"median":58.15,"stdDev":0.9090691209510234,"skewness":0.28049555095181067,"adPValue":0.07954209122843807,"sampleSize":15.0},"status":"success","decision":"Descriptive group summary."}
{"step_id":8,"inputs_digest":{"stage":"recipes","recipe":"recipe B","sampleSize":15},"method_id":"basic.descriptive_summary","outputs":{"mean":59.74333333333334,"median":59.99,"stdDev":0.9278136101815362,"skewness":0.9106445226524105,"adPValue":0.20118558988872182,"sampleSize":15.0},"status":"success","decision":"Descriptive group summary."}
{"step_id":9,"inputs_digest":{"stage":"recipes","recipe":"recipe C","sampleSize":15},"method_id":"basic.descriptive_summary","outputs":{"mean":61.32733333333332,"median":61.49,"stdDev":0.865872529934538,"skewness":-0.39683266536737954,"adPValue":0.4132405728664873,"sampleSize":15.0},"status":"success","decision":"Descriptive group summary."}
{"step_id":10,"inputs_digest":{"stage":"recipes","recipe":"recipe A","sampleSize":15},"method_id":"basic.normality","outputs":{"pValue":0.10869317301230325,"statistic":0.9037721599439461},"status":"success","decision":"No strong normality rejection at 0.05."}
{"step_id":11,"inputs_digest":{"stage":"recipes","recipe":"recipe B","sampleSize":15},"method_id":"basic.normality","outputs":{"pValue":0.16829593954855082,"statistic":0.9161614276992138},"status":"success","decision":"No strong normality rejection at 0.05."}
{"step_id":12,"inputs_digest":{"stage":"recipes","recipe":"recipe C","sampleSize":15},"method_id":"basic.normality","outputs":{"pValue":0.37655103911405946,"statistic":0.9395343444544608},"status":"success","decision":"No strong normality rejection at 0.05."}
{"step_id":13,"inputs_digest":{"stage":"recipes","groups":3,"groupSize":15,"center":"median"},"method_id":"anova.equal_variances","outputs":{"pValue":0.9755563118740186,"statistic":0.024761981900359043,"alpha":0.05},"status":"success","decision":"Use equal-variance methods."}
{"step_id":14,"inputs_digest":{"stage":"recipes","groups":3,"observationsPerGroup":15,"totalSampleSize":45},"method_id":"anova.oneway","outputs":{"factorPValue":3.833851301067109e-12,"fStatistic":52.42698750092324,"alpha":0.05,"groupCount":3.0,"totalSampleSize":45.0,"dfBetween":2.0,"dfWithin":42.0,"ssBetween":85.1756799999994,"ssWithin":34.11771999999999,"pooledStdDev":0.9012916657035426,"rSquaredPct":71.40016128302103},"status":"success","decision":"Reject equal recipe means; all ordered pairwise differences are material."}
{"step_id":15,"inputs_digest":{"stage":"recipes","groups":3,"observationsPerGroup":15},"method_id":"anova.sov","outputs":{"totalVariance":2.7112136363636363},"status":"success","decision":"Recipe explains most of the observed sample variance."}
{"step_id":16,"inputs_digest":{"stage":"recipes","group1":"recipe A","group2":"recipe B","group1Size":15,"group2Size":15},"method_id":"basic.two_sample_t","outputs":{"tStatistic":5.3192626527934195,"pValue":1.1607145638686094e-05,"difference":1.784000000000006,"lower95":1.09699531918327,"upper95":2.4710046808167423,"confidenceLevel":95.0,"alpha":0.05,"holmAdjustedPValue":0.00013244478458489215},"status":"success","decision":"C is highest; every recipe differs from every other."}
{"step_id":17,"inputs_digest":{"stage":"recipes","group1":"recipe A","group2":"recipe C","group1Size":15,"group2Size":15},"method_id":"basic.two_sample_t","outputs":{"tStatistic":10.39010782364311,"pValue":4.2196883269945285e-11,"difference":3.367999999999988,"lower95":2.7039996478701163,"upper95":4.0320003521298595,"confidenceLevel":95.0,"alpha":0.05,"holmAdjustedPValue":0.00013244478458489215},"status":"success","decision":"C is highest; every recipe differs from every other."}
{"step_id":18,"inputs_digest":{"stage":"recipes","group1":"recipe B","group2":"recipe C","group1Size":15,"group2Size":15},"method_id":"basic.two_sample_t","outputs":{"tStatistic":4.834043506337245,"pValue":4.414826152829738e-05,"difference":1.5839999999999819,"lower95":0.9127861583475468,"upper95":2.255213841652417,"confidenceLevel":95.0,"alpha":0.05,"holmAdjustedPValue":0.00013244478458489215},"status":"success","decision":"C is highest; every recipe differs from every other."}
{"inputs_digest":{"stage":"leading_two","recipe":"recipe C","sampleSize":15},"method_id":"basic.descriptive_summary","outputs":{"mean":61.32733333333332,"median":61.49,"stdDev":0.865872529934538,"shapiroPValue":0.37655103911405946,"shapiroStatistic":0.9395343444544608,"sampleSize":15.0},"status":"success","decision":"Descriptive check for the selected leading pair.","step_id":19}
{"inputs_digest":{"stage":"leading_two","recipe":"recipe B","sampleSize":15},"method_id":"basic.descriptive_summary","outputs":{"mean":59.74333333333334,"median":59.99,"stdDev":0.9278136101815362,"shapiroPValue":0.16829593954855082,"shapiroStatistic":0.9161614276992138,"sampleSize":15.0},"status":"success","decision":"Descriptive check for the selected leading pair.","step_id":20}
{"step_id":21,"inputs_digest":{"stage":"leading_two","groups":2,"groupSize":15,"center":"median"},"method_id":"anova.equal_variances","outputs":{"pValue":0.9330816690985373,"statistic":0.0071785940756871605,"alpha":0.05},"status":"success","decision":"Pooled t is supported for B versus C."}
{"step_id":22,"inputs_digest":{"stage":"leading_two","group1":"recipe C","group2":"recipe B","group1Size":15,"group2Size":15},"method_id":"basic.two_sample_t","outputs":{"df":28.0,"group1Size":15.0,"group2Size":15.0,"tStatistic":4.834043506337246,"pValue":4.3658608057111614e-05,"difference":1.5839999999999819,"lower95":0.9127861583475471,"upper95":2.2552138416524166,"confidenceLevel":95.0,"alpha":0.05,"pooledStdDev":0.89737766111413,"cohenD":1.7651431149215182,"hedgesG":1.7174365442479638},"status":"success","decision":"Recipe C is materially higher than recipe B, but this is not by itself proof of causation."}
{"step_id":23,"inputs_digest":{"stage":"leading_two","group1":"recipe C","group2":"recipe B","group1Size":15,"group2Size":15},"method_id":"nonparametric.mann_whitney","outputs":{"pValue":0.0002617547195372892,"uStatistic":201.0,"alpha":0.05},"status":"success","decision":"Sensitivity analysis agrees with the t test."}
{"step_id":24,"inputs_digest":{"stage":"baseline","comparison":"runOrder","sampleSize":60},"method_id":"basic.correlation","outputs":{"correlationCoefficient":0.8430836925225684,"pValue":2.915854820516087e-17},"status":"success","decision":"Hardness increases strongly with run order."}
{"step_id":25,"inputs_digest":{"stage":"baseline","comparison":"last40MinusFirst20","group1Size":20,"group2Size":40},"method_id":"basic.two_sample_t","outputs":{"tStatistic":7.550655677361809,"pValue":3.4791531902780233e-10,"difference":3.4024999999999963,"lower95":2.500479827073258,"upper95":4.304520172926734,"group1Size":20.0,"group2Size":40.0,"firstSegmentMean":58.366,"lastSegmentMean":61.768499999999996},"status":"success","decision":"The final 40 have a materially higher mean than the first 20."}
```

## Submitted route declarations
```json
[{"point":"measurement_system_gate","chosen_branch":"declare crossed gage R&R and unlock baseline","observed":{"percentStudyVariation":12.700490673699216,"ndc":11}},{"point":"baseline_stability","chosen_branch":"do not treat the 60 observations as one stable baseline","observed":{"lag1Correlation":0.7042712072465488,"runsPValue":4.532976170252393e-08}},{"point":"three_recipe_test","chosen_branch":"pooled one-way ANOVA after equal-variance check","observed":{"equalVariancePValue":0.9755563118740186}},{"point":"leading_pair","chosen_branch":"recipe C versus recipe B by pooled t with Mann-Whitney sensitivity","observed":{"meanC":61.32733333333332,"meanB":59.74333333333334}},{"point":"causal_interpretation","chosen_branch":"report association and require a randomized controlled confirmation","observed":{"unroutableProcessFactRequests":1.0}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
