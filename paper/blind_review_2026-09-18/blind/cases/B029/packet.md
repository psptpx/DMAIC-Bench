# Blind item B029

Focal assessment: Selection of analysis methods after distribution diagnosis.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the process engineering group at a fine-chemicals plant. Yield on one intermediate has been low and swings from batch to batch; the internally accepted range is 80 to 100 percent. Production has recorded every batch's yield in charge order, and the archive holds the laboratory's study in which the same samples were assayed repeatedly by several analysts. Separately, an earlier run of charges was made deliberately at a high and a low setting, with the resulting yields recorded. Continuing to run charges is expensive, so we need to know whether the setting is worth pursuing at all before we commit to more of them.

## 2. What you are asked to do

Work through the batches the data steward can release and say where this project stands: whether the assay readings can be relied on, how the line has behaved over the run, where yield sits against its accepted range today, and whether the evidence justifies spending more charges on the setting or sends us back to look elsewhere. Every number in your report must come from a computation you ran on this task.


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


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"stage_id":"msa","nParts":10,"nOperators":3,"nReplicates":3,"sampleSize":90,"tolerance":20.0},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":23.08946822558952,"percentTolerance":8.11358627789766,"ndc":5.941670126263153,"varGageRR":0.07314475809876579,"varPart":1.2988591435733854,"sdGageRR":0.270452875929922,"pctSV_repeatability":22.717689263336027,"pctSV_reproducibility":4.126758712962889,"interactionPValue":0.3947109928119996,"operatorPValue":0.1435831761130395,"partPValue":1.1102230246251565e-16},"status":"success","decision":"Assay accepted. Crossed ANOVA with the part-by-operator interaction pooled into error (interaction p=0.395). Gage R&R is 23.09 pct of study variation and 8.11 pct of tolerance with 5.94 distinct categories, so it passes the msa_pass gate of 30 pct; repeatability dominates, operator bias is not significant."}
{"step_id":2,"inputs_digest":{"stage_id":"process_run","sampleSize":30,"nGroups":1},"method_id":"basic.descriptive_summary","outputs":{"mean":86.08750666666666,"median":86.15119999999999,"stdDev":2.860251663021297,"skewness":0.18418193732334195,"adPValue":0.9716358284328265,"adStatistic":0.13879136385014945,"kurtosis":-0.03405081557482026,"min":80.3653,"max":92.6678},"status":"success","decision":"Yield over 30 charges averages 86.09 with sd 2.86, near-symmetric, and Anderson-Darling p=0.972 supports normality, so normal-theory tools apply."}
{"step_id":3,"inputs_digest":{"stage_id":"process_run","sampleSize":30},"method_id":"basic.normality","outputs":{"pValue":0.993237928426975,"statistic":0.9904706832301521},"status":"success","decision":"Shapiro-Wilk p=0.993 confirms normality, so the normal capability model is the right one rather than a non-normal fit."}
{"step_id":4,"inputs_digest":{"stage_id":"process_run","sampleSize":30,"subgroupSize":1},"method_id":"control_chart.imr","outputs":{"centerLine":86.08750666666666,"individualsUCL":95.45399956321839,"individualsLCL":76.72101377011492,"flaggedCount":0,"mrFlaggedCount":0,"mrBar":3.5212379310344835,"mrUCL":11.503884320689657,"sigmaWithin":3.1216648324773795,"test2RunCount":0,"test5Count":0},"status":"success","decision":"Line is in statistical control: no individual outside 76.72 to 95.45, no moving-range violation, no 9-point run and no 2-of-3 beyond 2 sigma. The batch-to-batch swings are common cause, not upsets, so chasing individual bad batches would be wasted effort."}
{"step_id":5,"inputs_digest":{"stage_id":"process_run","sampleSize":30},"method_id":"nonparametric.runs_test","outputs":{"pValue":1.0,"runsObserved":16,"runsExpected":16.0,"runsZ":0.0},"status":"success","decision":"Runs about the median: 16 observed against 16 expected, p=1.0. No clustering or oscillation, confirming the order is random."}
{"step_id":6,"inputs_digest":{"stage_id":"process_run","sampleSize":30,"xVariable":"charge order"},"method_id":"basic.correlation","outputs":{"correlationCoefficient":0.23913992003046136,"pValue":0.20311417762427408},"status":"success","decision":"No drift with charge order (r=0.239, p=0.203). Yield is not decaying over the run, so the low yield is a persistent level problem, not degradation."}
{"step_id":7,"inputs_digest":{"stage_id":"process_run","sampleSize":30,"lsl":80.0,"usl":100.0},"method_id":"capability.normal","outputs":{"cp":1.0678062867780624,"cpk":0.6500277889470022,"pp":1.165398617341356,"ppk":0.7094371852389607,"cpl":0.6500277889470022,"cpu":1.4855847846091228,"ppl":0.7094371852389607,"ppu":1.6213600494437512,"ppmBelowLSL":16655.63031874196,"ppmAboveUSL":0.5749515717953665,"observedOutOfSpec":0},"status":"success","decision":"Not capable, and specifically off-centre low. Cp 1.068 versus Cpk 0.650 (Pp 1.165 versus Ppk 0.709) shows the spread would nearly fit the 20-wide window but the mean sits low, putting about 16656 ppm at risk below 80 against 0.6 ppm above 100. Centring, not variation reduction, is the primary lever."}
{"step_id":8,"inputs_digest":{"stage_id":"process_run","sampleSize":30,"target":90.0},"method_id":"basic.one_sample_t","outputs":{"tStatistic":-7.492210851445262,"pValue":2.9430346525454686e-08,"mean":86.08750666666666,"ciLower":85.01947114302195,"ciUpper":87.15554219031137},"status":"success","decision":"Mean yield is significantly below the 90 midpoint of the accepted range (t=-7.49, p=2.94e-08, 95 pct CI 85.02 to 87.16). This quantifies the centring gap the project has to close."}
{"step_id":9,"inputs_digest":{"stage_id":"screening_doe","sampleSize":12,"nGroups":2},"method_id":"anova.equal_variances","outputs":{"pValue":0.44738339874276234,"statistic":0.6254391789536544,"bartlettPValue":0.6947650620559271},"status":"success","decision":"Levene p=0.447, so the two settings have comparable spread and the pooled two-sample comparison is valid. The setting does not affect variability either."}
{"step_id":10,"inputs_digest":{"stage_id":"screening_doe","sampleSize":12,"nLow":6,"nHigh":6},"method_id":"basic.two_sample_t","outputs":{"tStatistic":-2.059721844071912,"pValue":0.06641813304165052,"lowMean":90.80533333333334,"highMean":88.94885000000001,"effectHighMinusLow":-1.8564833333333406,"effectCiLower":-3.8647654977093895,"effectCiUpper":0.15179883104270853,"pooledSd":1.5611445137569215},"status":"success","decision":"Setting effect is not significant at the 5 pct level (p=0.066) and points the wrong way: high minus low is -1.86, 95 pct CI -3.86 to +0.15. Even the most favourable end of that interval is far short of the 3.91 needed to centre the process."}
{"step_id":11,"inputs_digest":{"stage_id":"screening_doe","sampleSize":12,"nGroups":2},"method_id":"anova.oneway","outputs":{"factorPValue":0.06641813304165023,"fStatistic":4.24245407494701},"status":"success","decision":"One-way ANOVA agrees with the t-test (F=4.24, p=0.066): the setting does not explain a significant share of the yield variation."}
{"step_id":12,"inputs_digest":{"stage_id":"screening_doe","sampleSize":12,"nFactors":1,"nLevels":2},"method_id":"doe.factorial_analysis","outputs":{"modelPValue":0.06641813304165012,"rSquaredPct":29.787381111585546,"rSquaredAdjPct":22.76611922274411,"slope":-0.9282416666666703,"intercept":89.8770916666667,"slopePValue":0.06641813304164912,"residualShapiroP":0.03427972105004414},"status":"success","decision":"Two-level single-factor fit: model p=0.066, R-squared 29.8 pct (adjusted 22.8 pct). The design is one factor at two levels rather than a full factorial, so there are no interaction terms to estimate. Residual Shapiro p=0.034 is a mild normality caveat on only 12 runs, which is why the nonparametric check in step 13 was run as well."}
{"step_id":13,"inputs_digest":{"stage_id":"screening_doe","nLow":6,"nHigh":6},"method_id":"nonparametric.mann_whitney","outputs":{"pValue":0.04112554112554113},"status":"success","decision":"Rank-based test gives p=0.041, marginally significant where the t-test gave 0.066. The two disagree around the 5 pct line, so the honest reading is a weak effect of uncertain significance; either way its sign is negative, so the high setting is the worse of the two."}
{"step_id":14,"inputs_digest":{"stage_id":"screening_doe","nPerGroup":6,"pooledSd":1.5611445137569215},"method_id":"power.two_proportions","outputs":{"power":0.4608415274136006,"powerAtCenteringGap":0.9735580381195968,"mde80":2.803098857426958,"observedEffect":1.8564833333333406,"centeringGap":3.9124933333333445},"status":"success","decision":"Retrospective power for the two-sample comparison of means; the table has no two-sample-t power entry, so the closest power family entry is used and the difference is noted here. Power was only 0.461 against the small observed effect of 1.86, but 0.974 against the 3.91 shift needed to centre the process, and the minimum effect detectable at 80 pct power was 2.80. The trial was therefore well able to see a business-relevant effect and did not, which makes the negative conclusion actionable rather than merely inconclusive."}
```

## Submitted route declarations
```json
[{"point":"msa_pass gate (AIAG MSA-4 Ch. II Sec. D)","chosen_branch":"declare grr_pct=23.089 and proceed to the per-batch yield record","observed":{"percentStudyVariation":23.08946822558952,"percentTolerance":8.11358627789766,"ndc":5.941670126263153,"threshold":30}},{"point":"stability of the run before judging capability","chosen_branch":"in control, so capability indices are meaningful and were computed","observed":{"flaggedCount":0,"mrFlaggedCount":0,"runsPValue":1.0,"trendPValue":0.20311417762427408}},{"point":"capability model choice","chosen_branch":"normal capability, since both normality tests pass","observed":{"adPValue":0.9716358284328265,"shapiroPValue":0.993237928426975}},{"point":"diagnosis: centring versus spread","chosen_branch":"centring is the dominant loss, driven by the lower limit","observed":{"cp":1.0678062867780624,"cpk":0.6500277889470022,"ppmBelowLSL":16655.63031874196,"ppmAboveUSL":0.5749515717953665,"oneSampleTPValue":2.9430346525454686e-08}},{"point":"is the setting worth more charges","chosen_branch":"no - stop spending on this factor and screen other variables","observed":{"effectHighMinusLow":-1.8564833333333406,"effectCiUpper":0.15179883104270853,"modelPValue":0.06641813304165012,"mannWhitneyP":0.04112554112554113,"powerAtCenteringGap":0.9735580381195968,"centeringGap":3.9124933333333445}},{"point":"improve and control evidence","chosen_branch":"no data exists - project reported as stopping at Analyze","observed":{"stagesReleased":4}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
