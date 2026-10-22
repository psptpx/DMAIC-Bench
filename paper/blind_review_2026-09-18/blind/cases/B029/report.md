# Batch Yield Improvement - Project Status Report

**Task:** [TASK]  
**Product:** intermediate, batch yield  
**Accepted range:** 80.0 to 100.0 percent (tolerance width 20.0)  
**Charter goal:** bring batch yield inside its accepted range and hold it there

---

## 1. Bottom line

The assay can be trusted, the line is stable, and the yield problem is a **centring** problem, not an instability problem. The setting that was trialled **does not earn more charges**: its measured effect points the wrong way and is far too small to close the gap, and the trial was large enough to have seen a useful effect if one existed. Recommendation is to stop spending charges on this factor and screen other variables.

The project has data through Analyze only. There is **no improvement run and no control-phase data** in this project (see section 6), so no claim is made here about a change having been implemented, verified, or held.

---

## 2. Can the assay readings be relied on? Yes

A crossed Gage R&R on the laboratory study (3 analysts, 10 samples, 3 repeats each, 90 readings) gives:

| measure | value | reading |
|---|---|---|
| Gage R&R, percent of study variation | 23.09 | acceptable (under the 30 percent criterion) |
| Gage R&R, percent of tolerance | 8.11 | comfortably capable against the 20-wide window |
| distinct categories (ndc) | 5.94 | can separate good batches from bad |
| repeatability, percent of study variation | 22.72 | dominant measurement term |
| reproducibility, percent of study variation | 4.13 | small |

The analyst-by-sample interaction was not significant (p = 0.395) and was pooled into error. Analyst-to-analyst bias was not significant (p = 0.144), while the samples differed strongly from one another as they should. Practically: the analysts agree with each other, and what residual measurement noise exists is within-analyst repeatability of the assay itself. **The measurement system was declared passing (grr_pct = 23.09) and the yield record was released on that basis.**

Worth noting for later: the assay contributes about 23 percent of the study variation, so if the team ever does drive process spread down, the assay will become the next thing worth tightening.

## 3. How has the line behaved over the run? Stable

Thirty charges in charge order, mean **86.09**, standard deviation **2.86**, median **86.15**, range **80.37** to **92.67**. The distribution is essentially normal (Anderson-Darling p = 0.972, Shapiro-Wilk p = 0.993, skewness 0.184), which justifies the normal capability model used below.

The individuals and moving-range chart shows a process in statistical control:

- centre line **86.09**, limits **76.72** to **95.45** - **0** points outside
- moving-range limit **11.50** with average moving range **3.52** - **0** violations
- no run of nine points on one side of centre, no 2-of-3 beyond two sigma
- runs about the median: **16** observed against **16** expected, p = **1.0**
- no drift with charge order: r = **0.239**, p = **0.203**

This matters commercially. The batch-to-batch swings production has been reporting are **common-cause variation**, not upsets. Investigating individual low batches, or reacting to them one at a time, will consume effort and change nothing. The variation is a property of the current process, and only a change to the process itself will move it.

## 4. Where does yield sit against the accepted range? Inside it, but not safely

| index | value |
|---|---|
| Cp | 1.068 |
| Cpk | 0.650 |
| Pp | 1.165 |
| Ppk | 0.709 |
| Cpl (lower side) | 0.650 |
| Cpu (upper side) | 1.486 |

None of the 30 charges actually fell outside 80 to 100 (**0** observed out of specification). But the gap between Cp **1.068** and Cpk **0.650** is the whole story: the spread would very nearly fit inside the 20-wide window, and the process is sitting **too low within it**. All the risk is on the lower limit - roughly **16656 ppm** expected below 80 against **0.57 ppm** above 100. About one charge in sixty would be expected to miss the floor at the current setting.

The mean is significantly below the 90 midpoint of the accepted range: **86.09** against 90, t = **-7.49**, p = **2.94e-08**, with a 95 percent confidence interval of **85.02 to 87.16**. The centring gap to close is **3.91** percentage points. Because the process is stable, that gap is not going to close on its own.

## 5. Does the evidence justify more charges on the setting? No

Twelve charges were run, six at the low setting and six at the high setting. Spread was comparable at both levels (Levene p = **0.447**), so the setting does not affect variability either.

| | value |
|---|---|
| low setting mean | 90.81 |
| high setting mean | 88.95 |
| effect (high minus low) | **-1.86** |
| 95 percent CI on the effect | **-3.86 to +0.15** |
| two-sample t | -2.06, p = **0.066** |
| one-way ANOVA | F = 4.24, p = **0.066** |
| model fit | p = **0.066**, R-squared **29.8** percent (adjusted **22.8**) |
| Mann-Whitney (rank-based) | p = **0.041** |

Three things sink this factor, and they compound:

1. **The sign is wrong.** The high setting is the *worse* of the two by **1.86** points. If this factor were pursued at all, the move would be toward the low setting, not the high one.
2. **The size is wrong.** The gap that needs closing is **3.91**. The effect estimate is **-1.86**, and even the most favourable end of its confidence interval is **+0.15** - essentially nothing. This factor cannot centre the process even on the most generous reading of its own data.
3. **Significance is marginal and the tests disagree.** The t-test and ANOVA give p = **0.066** (not significant at 5 percent) while the rank-based test gives p = **0.041** (marginally significant). Residual normality on 12 runs is itself borderline (Shapiro p = **0.034**), which is why both families were run. The honest reading is a weak effect of uncertain significance - and the model explains only **29.8** percent of the variation in these runs.

**Why this is a decision and not merely an inconclusive result.** A non-significant trial only justifies walking away if it could have detected something worth having. Power against the small observed effect of **1.86** was only **0.461**, so this trial genuinely cannot resolve effects that size. But power against the **3.91** shift that centring actually requires was **0.974**, and the smallest effect detectable at 80 percent power was **2.80**. An effect large enough to solve the business problem would almost certainly have shown up. It did not. Spending more charges here would be buying precision on a quantity that is too small, and pointed the wrong way, to fix the problem.

## 6. What is missing, and where the conclusion stops

The data steward holds four batches for this project and only four: the charter and yield requirement, the repeat-assay study, the per-batch yield record, and the high/low setting trial. All four were obtained and analysed. Requests for a confirmation run and for control-phase data after a change were refused as not available - **that data does not exist in this project.**

Consequences, stated plainly:

- **No change has been made to the process**, so there is nothing to verify. The report cannot say what a change achieved, because none was implemented.
- **There is no control plan evidence** and no post-change yields, so nothing can be said about how a gain would be held. That work remains to be done once a real lever is found.
- The recommendation in section 5 is a **screening decision about where not to spend**, based on the trial that was run. It is not a validated improvement.

No figure in this report has been supplied from experience or assumption; every number above comes from a computation run on this data and recorded in `trace.json`.

## 7. Recommended next steps

1. **Close out this factor.** Record the setting as screened and rejected: effect **-1.86** (CI **-3.86 to +0.15**) against a required shift of **3.91**, with **0.974** power at that required shift. Do not commit further charges to it.
2. **Keep the target where the problem is.** The objective is a **3.91** point lift in the mean. Spread is close to adequate already (Cp **1.068**); it is centring that is failing (Cpk **0.650**), and the lower limit carries effectively all the risk.
3. **Screen more factors, not more levels of this one.** A multi-factor screening design across candidate variables - charge composition, temperature, hold time, catalyst loading, addition rate - will find a lever of the required size far more cheaply than further charges on a factor whose ceiling is already known to be too low. Design it to detect a shift of about **2.80** or larger, which is what this run size can resolve.
4. **Hold the I-MR chart in place meanwhile.** Limits **76.72** to **95.45** with centre line **86.09** are valid because the run is in control, and they will show immediately whether any future change actually moves the mean rather than just producing a lucky batch.
5. **Revisit the assay only later.** At **23.09** percent of study variation it is acceptable now and is not what is holding yield down. It becomes worth attention once process spread has been reduced.
