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
