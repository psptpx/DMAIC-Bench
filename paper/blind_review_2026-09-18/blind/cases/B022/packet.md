# Blind item B022

Focal assessment: Permissible comparisons after diagnosing variance differences between recipe groups.

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
# Hardness / heat-treatment recipe review

## Management conclusion
The readings support a qualified comparison, not a recipe-change authorization. Recipe groups differ in spread, and the robust median comparison detects an overall median difference. Mean-based and rank comparisons are inconclusive, so the result depends on the feature of hardness being compared; it does not justify declaring the highest observed mean the best recipe. Causality is unconfirmed because random assignment, independence and control of other process factors were not documented. No implemented change or achieved improvement is evidenced by the released records.

## Measurement system
Crossed random-effects ANOVA gives gage R&R study variation of 14.35%, tolerance consumption of 19.84%, and 9 distinct categories. This supports conditional use for comparative investigation, not treating measurement error as negligible. The operator-by-part interaction is not supported (p = 0.8681); its negative estimated variance was truncated to zero while retaining the unpooled model. Tolerance consumption uses the study's supplied tolerance width; it does not establish the actual specification endpoints or tester accuracy. Check calibration, bias and ongoing repeatability before a production decision.

## Baseline behavior
The chronological sample contains 60 shafts. Mean hardness is 58.9547 HRC, median 58.825, and sample standard deviation 0.9683 HRC. Anderson–Darling normality p = 0.5709 does not flag a departure from a normal marginal distribution.

The individuals chart center is 58.9547 HRC, with limits 56.0634 to 61.8459; 0 individual points exceed them. However, the moving-range chart has 1 exceedance above its upper limit of 3.5516. The largest jump is 3.78 HRC, from shaft 44 (60.55) to shaft 45 (56.77). Investigate that transition before claiming statistical control. These are point-beyond-limit checks, not an exhaustive set of pattern rules. No capability index was computed: specification endpoints are unavailable and baseline stability is unresolved.

## Recipe comparison
| Recipe | Sample size | Mean HRC | SD HRC | Median HRC | Normality p |
|---|---:|---:|---:|---:|---:|
| recipe A | 15 | 59.0347 | 0.4375 | 59.00 | 0.0311 |
| recipe B | 15 | 59.3040 | 1.2008 | 59.75 | 0.3160 |
| recipe C | 15 | 60.1113 | 2.7221 | 59.90 | 0.5608 |

Median-centered Levene/Brown–Forsythe gives statistic 8.7608, p = 0.0006608. Equal-variance pooled ANOVA is therefore inappropriate. Recipe A also shows a normality concern. Mood's median test provides a robust location comparison (p = 0.0218); it provides evidence that not all recipe medians are equal. This omnibus result does not identify a winning pair. Unequal spread and the small samples warrant confirmation; the different conclusions from median, mean and rank tests should not be collapsed into a single claim that recipes are equivalent or universally different. Welch's unequal-variance mean comparison gives F = 1.3709, p = 0.2755; interpret cautiously given the nonnormal small sample. Kruskal–Wallis sensitivity p = 0.3602 likewise gives no compelling separation, but unequal shapes prevent reading it solely as a median test. Failure to detect a difference is not evidence of equivalence.

The leading sample is the same C and B readings, not a new trial. The exploratory Welch comparison estimates C minus B at 0.8073 HRC, t = 1.0509, p = 0.3063. The nominal confidence interval is -0.7991 to 2.4138 HRC and crosses zero. Selection by observed means makes this unsuitable as independent confirmation. C's higher sample mean accompanies much greater spread; higher hardness alone is not an approved optimization objective.

## What happens next and how it will be held
No process facts were supplied in response to the assignment/confounding or specification questions. The request for implementation and post-change records was unroutable, not a confirmed denial of an existing batch. Thus no data support a claim of implemented change, improved yield, savings or sustained control; the conclusion stops at diagnostic comparison.

Investigate the baseline transition using furnace/load, material-lot, quench, tester and operator logs; verify the recipe A extreme reading without deleting it merely for being unusual. Obtain approved hardness requirements and the economically meaningful difference. Design a randomized, blocked confirmation trial across material lots and furnace loads, preserving shaft identity and run order, and assess both location and dispersion. Do not standardize C based on its observed mean.

After a confirmed beneficial change, document the recipe and operating window, train operators, and validate the measurement system. Quality should own a chronological individuals/moving-range chart and a reaction plan: verify the reading, contain affected material as required by specifications, investigate assignable causes, and record disposition. Establish new limits from demonstrated stable post-change operation rather than recalculating limits to hide signals. Only then assess capability against approved limits and verify sustained performance.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":14.352546404740247,"percentTolerance":19.840941233024598,"ndc":9.0,"repeatVariance":0.03700669966666668,"operatorVariance":0.0023595952345668845,"interactionVariance":0.0,"partVariance":1.8716598210493818,"interactionPValue":0.8681405191953212},"status":"success","decision":"Unpooled crossed random-effects ANOVA; negative components truncated at zero.","inputs_digest":{"batch":"msa"}}
{"step_id":2,"method_id":"basic.descriptive_summary","outputs":{"mean":58.95466666666667,"median":58.825,"stdDev":0.9682930405767555,"skewness":0.05531943247125472,"adPValue":0.5708574747047122,"n":60.0},"status":"success","decision":"Single chronological population.","inputs_digest":{"batch":"baseline"}}
{"step_id":3,"method_id":"basic.normality","outputs":{"statistic":0.300260920381362,"pValue":0.5708574747047122},"status":"success","decision":"Anderson-Darling normality with estimated mean and variance.","inputs_digest":{"batch":"baseline"}}
{"step_id":4,"method_id":"control_chart.imr","outputs":{"centerLine":58.95466666666667,"individualsLCL":56.06339367712466,"individualsUCL":61.84593965620868,"flaggedCount":0.0,"mrMean":1.0871186440677965,"mrUCL":3.551616610169491,"mrFlaggedCount":1.0,"withinSigma":0.9637576631806707},"status":"success","decision":"Individuals and moving ranges; point-beyond-limit rule.","inputs_digest":{"batch":"baseline"}}
{"step_id":5,"method_id":"basic.descriptive_summary","outputs":{"mean":59.03466666666667,"median":59.0,"stdDev":0.43752333271114485,"skewness":1.9245002580118937,"adPValue":0.031077109474092385,"n":15.0},"status":"success","decision":"recipe A distribution and normality.","inputs_digest":{"batch":"recipes"}}
{"step_id":6,"method_id":"basic.descriptive_summary","outputs":{"mean":59.30399999999999,"median":59.75,"stdDev":1.2008259062590458,"skewness":-0.7111504447142736,"adPValue":0.3159599196752811,"n":15.0},"status":"success","decision":"recipe B distribution and normality.","inputs_digest":{"batch":"recipes"}}
{"step_id":7,"method_id":"basic.descriptive_summary","outputs":{"mean":60.11133333333334,"median":59.9,"stdDev":2.722120671899201,"skewness":0.6181318209014262,"adPValue":0.5607890764320697,"n":15.0},"status":"success","decision":"recipe C distribution and normality.","inputs_digest":{"batch":"recipes"}}
{"step_id":8,"method_id":"anova.equal_variances","outputs":{"pValue":0.0006607844289582165,"statistic":8.760828590715361},"status":"success","decision":"Brown-Forsythe median-centered Levene test; reject equal variances.","inputs_digest":{"batch":"recipes"}}
{"step_id":9,"method_id":"anova.oneway","outputs":{"factorPValue":0.2754590424634292,"fStatistic":1.3708906394371467,"dfNumerator":2.0,"dfDenominator":21.22896107840732},"status":"success","decision":"Welch heteroscedastic one-way ANOVA, not pooled ANOVA.","inputs_digest":{"batch":"recipes"}}
{"step_id":10,"method_id":"nonparametric.kruskal_wallis","outputs":{"pValue":0.3602224775091209,"statistic":2.042066890660353},"status":"success","decision":"Sensitivity rank comparison; unequal shapes preclude a pure median interpretation.","inputs_digest":{"batch":"recipes"}}
{"step_id":11,"method_id":"basic.two_sample_t","outputs":{"pValue":0.3062991954330387,"tStatistic":1.0509442539342937,"difference":0.8073333333333537,"ciLower":-0.7991114556866232,"ciUpper":2.413778122353331,"df":19.250015562654568},"status":"success","decision":"Two-sided Welch C minus B; selected on these same data, exploratory not independent confirmation.","inputs_digest":{"batch":"leading_two"}}
{"step_id":12,"method_id":"nonparametric.moods_median","outputs":{"pValue":0.021837847908763242,"statistic":7.648221343873518,"pooledMedian":59.24},"status":"success","decision":"Mood median test rejects equality of recipe medians at the conventional significance level. Unequal spreads and nonnormal recipe A motivate this comparison; omnibus result does not identify a winning pair.","inputs_digest":{"batch":"recipes"}}
{"step_id":13,"method_id":"meta.data_profiling","outputs":{"jumpFromShaft":44.0,"jumpToShaft":45.0,"jumpFromValue":60.55,"jumpToValue":56.77,"largestMovingRange":3.779999999999994},"status":"success","decision":"Locate largest moving range using one-based shaft numbering.","inputs_digest":{"batch":"baseline"}}
```

## Submitted route declarations
```json
[{"point":"measurement","chosen_branch":"proceed_conditionally","observed":{"percentStudyVariation":14.352546404740247,"percentTolerance":19.840941233024598,"ndc":9.0,"repeatVariance":0.03700669966666668,"operatorVariance":0.0023595952345668845,"interactionVariance":0.0,"partVariance":1.8716598210493818,"interactionPValue":0.8681405191953212}},{"point":"recipe_comparison","chosen_branch":"unequal_variances_welch","observed":{"variancePValue":0.0006607844289582165}},{"point":"distribution_assumptions","chosen_branch":"unequal_spread_robust_median_difference_with_inconclusive_mean_sensitivity","observed":{"medianPValue":0.021837847908763242}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
