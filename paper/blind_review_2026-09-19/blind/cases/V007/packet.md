# Blind item V007

Focal assessment: Whether readings can support substantive analysis after the measurement system study.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the process team on a honing line that finishes cylinder bores. Assembly has returned units for bore finish, and the accepted band for roughness is 0.40 to 1.60 um Ra with 1.00 as the target. The line records a roughness reading for every bore in the order it is finished, and the archive holds the study in which the same bores were measured several times over by several operators on the roughness tester.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the recorded readings can carry a conclusion at all, how the line has behaved across the run, where bore finish sits against its accepted band today, and what should change next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
{}
```

## Submitted report (complete, identifiers removed)
# Bore Finish (Roughness) — Project Report

**Task:** [TASK] · Honing line, cylinder bore finish
**Requirement:** 0.40 to 1.60 um Ra, target 1.00 um, tolerance width 1.20 um
**Data used:** operator repeat-reading study (90 readings) and the per-bore production record (50 bores in finishing order)

---

## Headline

The honing process is stable and every bore in the run measured inside the accepted band. But the readings the line records cannot support a precise conclusion about bore finish, because **89.72% of the variation in the production record is measurement noise, not bore-to-bore variation**. The number to act on is the roughness tester, not the honing spindle.

Assembly's returns are not explained by anything visible in this run: 0 of 50 bores fell outside 0.40–1.60 um Ra.

---

## 1. Can the recorded readings carry a conclusion? No.

Crossed Gage R&R (ANOVA method) on 3 operators × 10 bores × 3 repeats:

| Measure | Result | Bar | Verdict |
|---|---|---|---|
| % of tolerance consumed | **46.67%** | under 30% | fails |
| % study variation | **28.27%** | under 30% | marginal |
| Distinct categories (ndc) | **4.78** | at least 5 | fails |
| % contribution (variance) | 7.99% | under 9% | passes |

The gage alone eats **46.67% of the 1.20 um band**. Gage standard deviation is **0.0934 um**; the entire spread of the 50-bore production run is **0.0985 um**. The tester is nearly as wide as the process it is supposed to judge.

Splitting the gage: repeatability **37.84%** of tolerance, reproducibility **27.32%** — repeatability (the tester repeating itself on one bore) is the larger share, but operator differences are real and significant (p = 0.0019).

The part × operator interaction was not significant (p = 0.155); it was retained under the standard alpha = 0.25 screening rule, which is the conservative choice.

### Where the operator difference sits

An unblocked one-way ANOVA on operator finds nothing (F = 0.737, p = 0.482) because bore-to-bore spread swamps it. Comparing operators on **the same ten bores** is the valid test, and it is decisive:

- operator1 vs operator2: **p = 0.0038**
- operator1 vs operator3: **p = 0.0055**
- operator2 vs operator3: p = 0.911 (they agree)

Operator means: 1.0991, 1.1835, 1.1862 um — a spread of **0.0871 um**. Operator1 reads low by roughly that amount; the other two are interchangeable. Scatter is equal across all three (Levene p = 0.825, Bartlett p = 0.915), so this is a **fixed offset in method, not an erratic operator**.

---

## 2. How has the line behaved across the run?

Stable, with no signal worth chasing.

- **I-MR chart** (50 bores, finishing order): centre 1.0334, limits **0.7414 to 1.3253**. **0 points beyond limits**, **0 moving ranges** beyond 0.3586.
- Nelson run rules: tests 2, 3 and 6 all clear. Only test 5 (2 of 3 beyond 2 sigma) fires, on **3 points** — bores 37–39. Largest deviation in the whole run is 2.37 sigma.
- **Runs test** about the median: 24 runs against 26.0 expected, **p = 0.568**. No clustering, no oscillation, no mixing.
- **No drift**: correlation of roughness against finishing order r = 0.123, **p = 0.395**. Lag-1 autocorrelation 0.069. No tool-wear ramp across the run.
- **Distribution**: normal (Anderson-Darling **p = 0.527**, Shapiro-Wilk p = 0.478), mild right skew 0.303. Normal-theory limits and indices are appropriate.

The three test-5 points sit at 1.242, 1.049 and 1.264 um — all comfortably inside spec, and all within a single gage standard deviation of ordinary variation. Given that gage sigma (0.0934) is three times the residual process sigma (0.0316), **the most likely explanation for those flags is the tester, not the honing process.** They do not warrant a hunt for a special cause on the line.

---

## 3. Where does bore finish sit against the band today?

| Index | Value |
|---|---|
| Cp | 2.055 |
| Cpk | 1.941 |
| Pp | 2.029 |
| Ppk | 1.917 |
| Cpm (vs target) | 1.922 |
| Observed out of spec | **0 of 50 (0.0%)** |
| Expected ppm out of spec | 0.0045 |

On paper this is excellent — well past the usual Cpk 1.33 gate. **Read it with care.** These indices describe the spread of *readings*, and most of that spread is the tester. Strip out the measured gage variance and the residual bore-to-bore standard deviation is **0.0316 um** against an observed 0.0985 um.

The honing process is therefore *better* than the record makes it look, not worse. A gage-corrected Ppk works out to 5.98, but I am quoting that as an **upper bound and not a claim**: it comes from subtracting one study estimate from another, and no independent data in this project confirms it.

**Centring:** mean is 1.0334 um against a 1.00 target — an offset of 0.0334 um, statistically detectable (t = 2.394, **p = 0.021**) but worth 2.8% of the band and *smaller than one gage standard deviation*. Adjusting the line to close it would be tampering with noise. Recommendation: leave the mean alone.

---

## 4. What should change next

The measurement system is the constraint. Two actions, in order:

**a) Standardise the measuring method and re-train operator1.** The offset is 0.0871 um and specific to one operator, with equal scatter across all three — that is the signature of a method difference (fixture, cutoff, traverse placement), not operator carelessness. Fix the method, write it down, make all three work to it.

**b) Record each bore as the average of 3 traces, not a single trace.** Repeatability is the bigger half of the gage problem and averaging is the direct lever on it.

Recomputing %tolerance from the measured variance components projects:

| Change | Projected % of tolerance |
|---|---|
| Average 2 traces | 38.24% |
| Average 3 traces | 34.98% |
| Remove operator offset only | 37.84% |
| **Both together** | **21.85%** |

Either action alone leaves the gage failing the 30% bar. **Both together clear it.** These are projections, arithmetic on the variance components measured here — they are not results, and a fresh Gage R&R must confirm them before anyone trusts a capability number off this line.

**Do not touch the honing parameters yet.** Until the gage is fixed there is no measurement resolution to detect whether a process change helped. Chasing the 0.033 um centring offset or the bores 37–39 flags now would be reacting to tester noise.

---

## 5. What this report cannot tell you — gaps, stated plainly

The project asks what was changed, what the change achieved, and how it will be held. **I cannot answer those three, because the data does not exist.**

- **No after-change data.** I requested after-change trial readings explicitly. The steward refused: no such batch exists in this project. **No improvement effect is claimed and none was measured.** The changes in section 4 are recommendations that have not been trialled.
- **No control-phase data.** No ongoing monitoring readings and no control plan exist to request. **How the gain will be held cannot be reported** — only proposed: re-run the Gage R&R after the method fix, then keep the I-MR chart on bore roughness using limits re-established on post-fix readings (the current limits, 0.7414 to 1.3253, are inflated by gage noise and should not be carried forward).
- **No designed experiment.** No factor study on stone grit, pressure, speed or dwell exists. No statement about which honing variables drive roughness can be made from this data.
- **No process facts.** Two questions to the process owner — whether each production reading is a single trace or an average, and the operator method and tester calibration state — were both refused; this project records no process facts. So the *mechanism* behind operator1's offset is inferred from the variance components, not confirmed on the shop floor. Verify it before re-training.
- **No improvement target.** The charter released the band and target but no numeric improvement target, so progress against one is not reported.

**One honest caveat on the returns.** Assembly returned units, yet 0 of 50 bores in this record are out of spec. That mismatch is unresolved and this data cannot resolve it. With a gage consuming 46.67% of tolerance, a bore reading 1.55 could truly be past 1.60 and be passed — the nearest reading to a limit in this run sits 3.60 gage sigma below the upper limit, so *this* run is likely clean, but the screening on the line has not been reliable. Fixing the gage is also the fix for return risk.

---

## Summary for the quality manager

**Where things stand:** process stable and in control, every bore in spec, apparent Cpk 1.94 — but the number is not trustworthy.
**What is causing it:** the roughness tester, consuming 46.67% of the tolerance band and 89.72% of the recorded variance, with one operator reading 0.0871 um low.
**What was changed:** nothing yet. No improvement was run and no after-change data exists.
**What the change achieved:** cannot be reported — see above.
**How it will be held:** proposed only — re-qualify the gage, then re-baseline the control chart on post-fix readings.

The first spend should go to the measurement system. Everything else on this line is currently being judged through a tester that cannot see the process.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"method_id":"meta.data_profiling","inputs_digest":{"batch":"define","fields":4,"lsl":0.4,"usl":1.6},"outputs":{"lsl":0.4,"usl":1.6,"tolerance":1.2000000000000002,"target":1.0},"status":"success","decision":"Charter released: accepted band 0.40-1.60 um Ra, tolerance width 1.20 um, target 1.00 um. No improvement-target field was supplied in the batch.","step_id":1}
{"method_id":"msa.gage_rr_crossed","inputs_digest":{"batch":"msa","n":90.0,"operators":3.0,"parts":10.0,"replicates":3.0,"tolerance":1.2000000000000002},"outputs":{"percentStudyVariation":28.26745132926674,"percentTolerance":46.6735403667899,"ndc":4.784635113144765,"percentStudyRepeatability":22.91859209625827,"percentStudyReproducibility":16.546508422558276,"percentToleranceRepeatability":37.84182100093317,"percentToleranceReproducibility":27.32061407991592,"percentContributionGRR":7.990488046524641,"varGRR":0.008713677481481469,"varRepeatability":0.005728013666666668,"varReproducibility":0.002985663814814801,"varPart":0.10033695160082308,"varTotal":0.10905062908230455,"sdGRR":0.09334708073357982,"interactionPValue":0.15533696449120504,"operatorPValue":0.0019118228614868338,"partPValue":6.061817714453355e-14},"status":"success","decision":"Crossed ANOVA Gage R&R, full model (part*operator retained, F=1.42, p=0.155 > 0.05 but kept under the alpha=0.25 screening rule). %tolerance 46.67 exceeds 30, %study variation 28.27 is marginal, ndc 4.78 is below 5: measurement system NOT acceptable for judging conformance to this band. Operator main effect significant (p=0.0019).","step_id":2}
{"method_id":"anova.oneway","inputs_digest":{"batch":"msa","groups":3,"nPerGroup":30,"factor":"operator"},"outputs":{"fStatistic":0.7367772546876292,"factorPValue":0.4816164263797055,"meanOperator1":1.0990733333333333,"meanOperator2":1.18345,"meanOperator3":1.1862099999999998,"operatorSpread":0.08713666666666642},"status":"success","decision":"One-way ANOVA on raw readings finds no operator effect (p=0.482) because bore-to-bore spread dominates the unblocked comparison; the blocked paired test below is the valid comparison.","step_id":3}
{"method_id":"anova.equal_variances","inputs_digest":{"batch":"msa","groups":3,"nPerGroup":30,"test":"levene_median"},"outputs":{"pValue":0.8253166671688879,"statistic":0.192412423021047,"bartlettPValue":0.9153089664005625,"bartlettStatistic":0.17698720501271023,"sdOperator1":0.30167857859252983,"sdOperator2":0.32436449139180146,"sdOperator3":0.3216487764842159},"status":"success","decision":"Levene p=0.825 and Bartlett p=0.915: operators scatter equally. The reproducibility problem is a fixed offset, not one operator being erratic.","step_id":4}
{"method_id":"basic.paired_t","inputs_digest":{"batch":"msa","pairs":10.0,"comparison":"operator part-means, same 10 bores"},"outputs":{"tStatistic":-3.8736901404644035,"pValue":0.0037674921660642534,"tStatistic_op1_vs_op3":-3.628831937682862,"pValue_op1_vs_op3":0.00549560984246447,"tStatistic_op2_vs_op3":-0.11492514961522364,"pValue_op2_vs_op3":0.9110276337563677},"status":"success","decision":"Blocking on bore: operator1 reads low vs operator2 (p=0.0038) and vs operator3 (p=0.0055); operators 2 and 3 agree (p=0.911). The bias sits with operator1 method, spread 0.0871 um.","step_id":5}
{"method_id":"basic.descriptive_summary","inputs_digest":{"batch":"process_run","n":50.0},"outputs":{"mean":1.03336,"median":1.0245,"stdDev":0.09854880899890187,"skewness":0.3031803629719626,"adPValue":0.5265815646159338,"minimum":0.825,"maximum":1.264,"q1":0.9604999999999999,"q3":1.111,"kurtosis":-0.007703504605722333},"status":"success","decision":"50 bores in finishing order: mean 1.0334 um Ra, sd 0.0985, range 0.825-1.264, mild right skew 0.303, all readings inside the 0.40-1.60 band.","step_id":6}
{"method_id":"basic.normality","inputs_digest":{"batch":"process_run","n":50.0,"test":"anderson_darling"},"outputs":{"pValue":0.5265815646159338,"statistic":0.3180385021966785,"shapiroPValue":0.47848226923374476,"shapiroStatistic":0.9781917947015524},"status":"success","decision":"Anderson-Darling p=0.527, Shapiro-Wilk p=0.478: normality not rejected, so normal-theory control limits and normal capability indices are the right tools.","step_id":7}
{"method_id":"control_chart.imr","inputs_digest":{"batch":"process_run","n":50.0,"subgroupSize":1,"sigmaFrom":"MRbar/1.128"},"outputs":{"centerLine":1.03336,"individualsUCL":1.3253161441597916,"individualsLCL":0.7414038558402084,"flaggedCount":0.0,"beyondLimitsCount":0.0,"mrBar":0.10977551020408165,"mrUCL":0.35863659183673474,"mrBeyondCount":0.0,"sigmaWithin":0.09731871471993055,"test5Count":3.0,"test2Count":0.0,"test3Count":0.0,"test6Count":0.0,"maxAbsZ":2.369944986056887,"flaggedCountAllNelsonRules":3.0},"status":"success","decision":"I-MR: centre 1.0334, limits 0.7414-1.3253. flaggedCount is the out-of-control count against the control limits = 0, and 0 moving ranges exceed 0.3586, which is what the in-control conclusion rests on. Supplementary Nelson rules: tests 2, 3 and 6 clear; only test 5 (2 of 3 beyond 2 sigma) fires, on 3 points (bores 37-39), giving an all-rules union of 3. Largest deviation in the run is 2.37 sigma. The run is in control.","step_id":8}
{"method_id":"nonparametric.runs_test","inputs_digest":{"batch":"process_run","n":50.0,"about":"median"},"outputs":{"pValue":0.567628499263336,"runsObserved":24.0,"runsExpected":26.0,"zStatistic":-0.5715476066494082},"status":"success","decision":"24 runs against 26.0 expected, p=0.568: no clustering, mixing or oscillation. Order of finishing carries no pattern.","step_id":9}
{"method_id":"basic.correlation","inputs_digest":{"batch":"process_run","n":50.0,"pair":"finishing order vs roughness"},"outputs":{"correlationCoefficient":0.12305272969126574,"pValue":0.3945756809602718,"lag1Autocorrelation":0.06855268950503973},"status":"success","decision":"r=0.123, p=0.395 against finishing order and lag-1 autocorrelation 0.069: no drift or wear trend across the run.","step_id":10}
{"method_id":"basic.one_sample_t","inputs_digest":{"batch":"process_run","n":50.0,"target":1.0},"outputs":{"pValue":0.020555635435916056,"tStatistic":2.393644576734166,"mean":1.03336,"meanMinusTarget":0.033360000000000056},"status":"success","decision":"Mean 1.0334 sits 0.0334 um above the 1.00 target, t=2.394, p=0.021: statistically detectable but 2.8% of a 1.20 wide band, and smaller than one gage sigma. Not worth chasing.","step_id":11}
{"method_id":"capability.normal","inputs_digest":{"batch":"process_run","n":50.0,"lsl":0.4,"usl":1.6},"outputs":{"cp":2.055103179029559,"cpk":1.9408394422755155,"pp":2.029451213380251,"ppk":1.916613725916309,"cpu":1.9408394422755155,"cpl":2.1693669157836024,"cpm":1.9222988698381795,"ppmExpTotal":0.004531496786525361,"observedOutOfSpec":0.0,"observedOutOfSpecPct":0.0},"status":"success","decision":"As recorded: Cp 2.055, Cpk 1.941, Pp 2.029, Ppk 1.917, zero of 50 bores out of spec. These indices are inflated in the sense that they describe reading spread, most of which is the tester - see the variance partition below.","step_id":12}
{"method_id":"anova.sov","inputs_digest":{"batch":"process_run + msa","n":50.0,"components":"gage vs true process"},"outputs":{"totalVariance":0.00971186775510204,"varGage":0.008713677481481469,"varTrueProcess":0.0009981902736205719,"gageShareOfObservedVariancePct":89.72195360571934,"sdObserved":0.09854880899890187,"sdGage":0.09334708073357982,"sdTrueProcess":0.03159414935744547,"ppkGageCorrected":5.978322057766958,"ppGageCorrected":6.330285956974755,"gageSpreadAsPctOfBand":46.67354036678991},"status":"success","decision":"Decisive result: gage variance 0.008714 of observed 0.009712 = 89.72% of the recorded scatter is measurement noise. Residual bore-to-bore sd is 0.0316 vs gage sd 0.0934. Gage-corrected Ppk 5.98 is an upper bound, not a claim: it rests on subtracting one study estimate from another and is quoted only to show the honing process is far tighter than the record suggests.","step_id":13}
{"method_id":"msa.gage_rr_crossed","inputs_digest":{"batch":"msa","projection":"arithmetic on measured variance components"},"outputs":{"projectedPctTolBothFixes":21.847985541514397,"projectedPctTolAvg2Traces":38.24156981658877,"projectedPctTolAvg3Traces":34.9821443871859,"projectedPctTolNoOperatorBiasSingleTrace":37.841821000933166,"sdRepeatability":0.07568364200186635,"sdReproducibility":0.05464122815983185},"status":"success","decision":"PROJECTION, not a measured result - output keys deliberately not canonical so these are not read as this project measured %tolerance (the measured value is 46.67 in the Gage R&R step). Recomputed from the same measured variance components: averaging 3 traces alone gives 34.98, removing the operator offset alone gives 37.84, both together give 21.85, which clears the 30% bar. Requires confirmation by a fresh study - no such data exists in this project.","step_id":14}
{"method_id":"meta.data_profiling","inputs_digest":{"batch":"improvement","requested":true},"outputs":{"batchAvailable":false},"status":"refused","decision":"Steward refused: no after-change trial readings batch exists in this project. Requested explicitly and confirmed against the steward topic list. No improvement effect, no held gain and no factor study can be reported.","step_id":15}
{"method_id":"meta.data_profiling","inputs_digest":{"batch":"control","requested":true},"outputs":{"batchAvailable":false},"status":"refused","decision":"Steward refused: no ongoing monitoring / control plan batch exists in this project. Requested explicitly and confirmed against the steward topic list. No improvement effect, no held gain and no factor study can be reported.","step_id":16}
{"method_id":"meta.data_profiling","inputs_digest":{"batch":"doe","requested":true},"outputs":{"batchAvailable":false},"status":"refused","decision":"Steward refused: no designed experiment on honing factors batch exists in this project. Requested explicitly and confirmed against the steward topic list. No improvement effect, no held gain and no factor study can be reported.","step_id":17}
{"method_id":"meta.data_profiling","inputs_digest":{"provisionCalls":2},"outputs":{"processFactsAvailable":false,"turnsSpent":2},"status":"refused","decision":"Two provision calls (production reading protocol; operator method and tester calibration state) both refused - this project records no process facts. Root-cause attribution below the level of the variance components is therefore unverified.","step_id":18}
```

## Submitted route declarations
```json
[{"point":"measurement_system_before_process_judgement","chosen_branch":"run crossed Gage R&R first and gate the capability conclusion on it","observed":{"percentTolerance":46.6735403667899,"percentStudyVariation":28.26745132926674,"ndc":4.784635113144765}},{"point":"gage_rr_model_choice","chosen_branch":"full model, part*operator interaction retained","observed":{"interactionPValue":0.15533696449120504,"alphaRule":0.25}},{"point":"normality_route","chosen_branch":"normal-theory tools (I-MR limits, normal capability)","observed":{"adPValue":0.5265815646159338,"shapiroPValue":0.47848226923374476}},{"point":"stability_before_capability","chosen_branch":"process judged in control, so capability indices are reportable","observed":{"beyondLimitsCount":0,"mrBeyondCount":0,"flaggedCountAllNelsonRules":3,"runsPValue":0.567628499263336}},{"point":"centring_action","chosen_branch":"do not adjust the mean; the 0.033 offset is inside gage noise","observed":{"tPValue":0.020555635435916056,"meanMinusTarget":0.033360000000000056,"sdGage":0.09334708073357982}},{"point":"improvement_verification","chosen_branch":"report the gap - no after-change or control data exists, so no achieved gain is claimed","observed":{"batchesAvailable":3,"improvementBatchAvailable":0}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
