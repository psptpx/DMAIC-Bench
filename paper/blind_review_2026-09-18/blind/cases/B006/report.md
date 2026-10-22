# Gear-Shaft Heat-Treatment Line: Case-Surface Hardness Project Report

## Project position

Data were obtained from the local steward and all available batches were requested. No data request was denied, and no outside process-fact (provision) turn was needed. The candidate under study is the heat-treat recipe currently in use; the goal is to establish whether recipe accounts for case-surface hardness (unit HRC).

## Can the recorded hardness readings carry a conclusion?

Yes, with an important baseline caveat. A crossed-gage R&R on the repeat-readings batch gives:

- Study-variation GRR = 11.8953%
- Tolerance GRR = 20.4688%
- Number of distinct categories (NDC) = 11

NDC well above 5 indicates adequate measurement discrimination, and a GRR study-variation fraction of about 11.9% is workable for this kind of comparison. The measurement system is not the limiting source of variation, so the recipe comparisons below are supportable.

## Baseline behavior

The 60 shaft-order baseline readings have:

- Mean = 60.6343 HRC
- Median = 60.9300 HRC
- Standard deviation = 2.2974 HRC
- Anderson-Darling p-value = 0.0236

An individuals-moving-range chart on the shaft-order sequence has center line 60.6343, LCL = 56.7598, UCL = 64.5089, and flags 2 individual points. A runs test for randomness around the median gives p = 4.53298e-08. Therefore the baseline is not one stable random sequence: the shaft-order record contains a patterned level shift (visible later in the run), so the whole baseline cannot be treated as a single stable population. Before/after process evaluation using this baseline as a single comparison would be unsafe.

## What kind of comparison do the recipe readings admit?

The separate recipe sample contains three independent groups with 15 shafts each. Levene's median test for equal variances gives p = 0.9756, so the equal-variance assumption is reasonable. Therefore these data admit both one-way ANOVA and nonparametric confirmation. The one-way ANOVA is strongly significant:

- F = 52.4270
- p = 3.83385e-12

Kruskal-Wallis confirms the same conclusion with p = 6.71554e-08.

Group summaries are:

| Recipe | Mean HRC | Median HRC | StdDev HRC |
|---|---:|---:|---:|
| A | 57.9593 | 58.1500 | 0.9091 |
| B | 59.7433 | 59.9900 | 0.9278 |
| C | 61.3273 | 61.4900 | 0.8659 |

## What the leading-two comparison says

The two recipes with the highest averages are recipe C and recipe B. Their head-to-head sample has equal group sizes (15 each). Levene's median test gives p = 0.9331, so the two-sample comparison with equal variances is appropriate. The two-sample t-test gives t = 4.8340, p = 4.36586e-05. The nonparametric Mann-Whitney test also gives p = 0.000261755. The mean difference is 1.5840 HRC in favor of recipe C.

## Conclusion: where the project stands and what should happen next

1. **Measurement system**: recorded hardness readings can carry a conclusion; the gage resolves enough distinct categories.  
2. **Baseline**: the baseline is unstable, so it should not be used as a single before/after control window.  
3. **Recipe**: recipe C is the current best candidate among the three. It has the highest mean hardness, and the difference versus recipe B is statistically significant.  
4. **Next steps**: standardize recipe C on representative production shafts, implement an ongoing I-MR or xbar-s control chart by shaft order, and hold the gain by monitoring recipe C separately. Further effort should evaluate the practical cost, distortion, and other heat-treatment tradeoffs before permanent rollout.
