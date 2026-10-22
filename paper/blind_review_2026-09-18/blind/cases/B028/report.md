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
