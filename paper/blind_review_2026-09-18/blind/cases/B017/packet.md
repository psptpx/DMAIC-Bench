# Blind item B017

Focal assessment: Baseline temporal stability and the analyses and conclusions that may follow.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

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
# Bore Finish (Ra) - Project Report

**Task:** [TASK] | **Line:** cylinder bore honing | **Characteristic:** surface roughness, um Ra
**Requirement (from charter):** LSL 0.40, USL 1.60 um Ra; target 1.00 stated in the project brief.

---

## 1. Headline

The readings can be trusted, and they show the line is **not stable**. Bore finish stepped up by **0.333 um Ra** at the **26th bore** of the run and has stayed there. All 50 bores are still inside the 0.40-1.60 band (**0.0%** observed out of spec), but the process has moved from sitting near nominal to sitting high, and capability against the upper limit has fallen from **Cpk 1.838** to **Cpk 1.091**.

This is a diagnosis, not a closed project. **No corrective action has been taken, verified, or held** - see section 6.

---

## 2. Can the readings carry a conclusion? Yes.

Crossed Gage R&R (ANOVA method) on the repeat-readings study: 3 operators x 10 bores x 3 replicates = 90 readings.

| Metric | Value | Verdict |
|---|---|---|
| % study variation (gage R&R) | **15.60%** | acceptable (<30%) |
| % contribution | **2.43%** | acceptable (<9%) |
| Number of distinct categories | **8.93** | acceptable (>=5) |
| % tolerance | **33.32%** | **above the 30% guideline - caveat** |
| Repeatability (% study var) | 11.98% | |
| Reproducibility (% study var) | 10.00% | |

The operator x bore interaction was not significant (p = 0.675) and was pooled into repeatability. Bore-to-bore differences dominate (part effect p ~ 1.1e-16), which is what lets the gage discriminate.

**Two honest qualifications.** The operator main effect *is* significant (p = 2.8e-08) - the three operators do not read a given bore identically, though the size of that effect is modest (10.00% of study variation). And at **33.32% of tolerance** the gage is wider than the 30% rule of thumb; it is fit for judging process behaviour, which is what this report does, but it is marginal for accept/reject sorting of individual bores near a limit.

---

## 3. How has the line behaved across the run?

**It has not behaved as one process.** I-MR chart on all 50 bores in finishing order (centre line 1.1124, UCL 1.4137, LCL 0.8110):

* **36 of 50** bores raise special-cause flags, **4** beyond the individuals limits
* 25 Test-2 signals (nine in a row on one side), 13 Test-5, 32 Test-6
* Runs test about the median: only **5** runs against **26** expected, z = -6.00, **p = 2.0e-09**

A process this far out of control has no single capability number. The pooled run also gives a muddled normality answer (Anderson-Darling p = 0.029 rejects, Shapiro-Wilk p = 0.079 does not) - the signature of two levels stacked on top of each other rather than one skewed population.

### The shift, located

Splitting the run at the point of maximum separation puts the change at **bore 26 (index 25)**, exactly mid-run:

| | Bores 1-25 | Bores 26-50 |
|---|---|---|
| Mean Ra | **0.9460** | **1.2787** |
| Std dev | 0.0986 | 0.0887 |
| I-MR special-cause flags | **0** | **0** |
| Anderson-Darling p | 0.108 | 0.514 |

Two-sample t: **t = -12.54, p = 1.1e-16**. Shift = **+0.333 um Ra**.

Three findings make this an actionable picture:

1. **Each half is stable and normal on its own** (zero flags in either segment). This is two settled regimes, not a process out of control in general.
2. **The spread did not change** - Levene p = 0.526. Only the mean moved. That points to a setpoint, consumable, or fixture change rather than to something that added variability.
3. **It is a step, not a drift.** Within the current regime there is no trend at all: OLS on finishing order p = 0.361, R-squared 3.64%, slope -0.0023; correlation r = -0.191. The strong-looking correlation with finishing order over the whole run (r = 0.709, p = 8.2e-09) is the step showing through, and would be misread as gradual wear.

### It was detectable immediately

Both a CUSUM (decision interval 0.396) and an EWMA (lambda = 0.2) referenced to the pre-shift baseline **first signal at index 26 - one bore after the shift**. The line had no such chart running. That is the biggest process-control gap here: 25 bores were finished off-target before anything would have said so.

---

## 4. Where does bore finish sit against the band today?

Capability computed **on the current regime only** (bores 26-50), which is legitimate because that segment is in control and normal:

| | Current (26-50) | Earlier (1-25) |
|---|---|---|
| Mean Ra | 1.2787 | 0.9460 |
| Cp | 2.038 | 2.020 |
| **Cpk** | **1.091** | **1.838** |
| Pp | 2.256 | 2.028 |
| **Ppk** | **1.208** | **1.846** |
| Observed out of spec | 0.0% | 0.0% |

**Read Cp against Cpk.** The line has ample precision - Cp of 2.038 means the spread would fit inside the band twice over. What has been consumed is *centring*. The current mean sits **0.279 um Ra above the 1.00 target** (one-sample t = 15.72, **p = 3.9e-14**). Before the shift it was only 0.054 below target (t = -2.74, p = 0.012), essentially on nominal.

The margin left is thin: the current regime's own upper control limit is **1.5731**, against a USL of **1.60**. Normal process variation now runs right up to the specification. Nothing has failed yet, but no room is left to absorb the next disturbance.

**A caution on the pooled number.** Computed across all 50 bores, Ppk = **0.847** while within-subgroup Cpk = **1.618**. Neither is a valid statement of capability - the gap between them is purely the un-modelled step. They appear here only so that nobody quotes a single whole-run figure for this process. Reported honestly, this project has **no valid single capability number**, only one per regime.

---

## 5. What is causing it

**The statistics locate the shift precisely; the physical cause is not established.** I asked the process owner what changed at bore 26 - tool or stone change, dressing interval, coolant concentration, spindle load, feed pressure, fixture or operator. The reply was that **no process facts are recorded for this project** ("Known process topics: none recorded"). One provision turn of the 22 available was spent confirming that.

So the cause is stated as what the data supports and no further: a **single sustained step in the mean, with variability unchanged, occurring between bore 25 and bore 26, with no subsequent drift**. That signature is characteristic of a discrete change - a new stone or tool, a dressing event, a coolant make-up, or a parameter edit - and is not characteristic of progressive wear, which would appear as a trend. Confirming which one requires the maintenance and tool-change log for that shift, which is not in this dataset. I am not going to name a cause the data does not identify.

---

## 6. What was changed, what it achieved, how it will be held

**Nothing was changed, and there is no data to say otherwise.** I requested readings taken after any corrective action or process improvement. The steward's reply was that no such batch exists; the complete set of data this project can provide is the charter, the repeat-readings study, and the single 50-bore run record.

Therefore:

* **What the change achieved: not computable.** There is no post-action data, so there is no improvement figure. Any number here would be invented.
* **How it will be held: not yet established.** No control plan or verification data exists in this project.

The conclusion stops at diagnosis. That is the honest boundary of this analysis.

---

## 7. Recommendations

1. **Recover the centre.** Bring the mean back toward 1.00 um Ra from its current 1.2787. The pre-shift regime already held 0.9460 with Cpk 1.838, so the capable state is a known, previously achieved condition - this is a recovery, not a development project.
2. **Pull the tool-change and maintenance log for the bore-25/26 boundary.** The shift is located to a single bore. Whatever discrete event sits at that boundary is the prime suspect, and the log will settle in minutes what no further statistics on these 50 readings can.
3. **Put a CUSUM or EWMA chart on the line.** Both signalled at bore 26 in this analysis. A step of 0.333 um Ra ran 25 bores undetected; charting closes that gap to roughly one part.
4. **Re-verify capability only after stability is re-established,** on a fresh in-control run. Do not quote a capability figure spanning the shift.
5. **Address the gage before using it to sort parts.** At 33.32% of tolerance it is marginal for accept/reject decisions near a limit, and the operator effect is real (p = 2.8e-08). Operator technique standardisation and fixturing are the places to look.

---

## 8. Traceability

Every figure above comes from a computation run on this dataset and recorded in `/workspace/trace.json` (22 analysis steps, 6 route decisions). The 0.40/1.60 limits and the 1.00 target are requirement values from the project brief, not computed results. Data gaps are stated as gaps in sections 5 and 6, not estimated.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"msa.gage_rr_crossed","inputs_digest":{"batch":"msa","sampleSize":90,"numGroups":3,"numParts":10,"numReplicates":3,"tolerance":1.2000000000000002},"outputs":{"percentStudyVariation":15.60424773702267,"percentTolerance":33.31868376090741,"ndc":8.925313227424608,"pctContributionGageRR":2.434925474383771,"pctStudyVarRepeatability":11.980249638214563,"pctStudyVarReproducibility":9.998308159105564,"varGageRR":0.0044405387502374225,"varPart":0.1779280305120818,"sdGageRR":0.06663736752181483},"status":"success","decision":"Crossed ANOVA Gage R&R, interaction pooled (p=0.675>0.25). %StudyVar 15.60% <30% and ndc 8.93 >=5, so the measurement system can support conclusions; %Tolerance 33.32% exceeds the 30% guideline, a caveat for spec-based sorting."}
{"step_id":2,"method_id":"anova.oneway","inputs_digest":{"batch":"msa","sampleSize":90,"numGroups":3},"outputs":{"factorPValue":2.8368312920967753e-08,"fStatistic":0.8156215168982714,"partPValue":1.1102230246251565e-16,"interactionPValue":0.6750320379405397},"status":"success","decision":"ANOVA underlying the Gage R&R: operator effect significant, part effect significant, operator x part interaction not significant so it was pooled into repeatability."}
{"step_id":3,"method_id":"basic.descriptive_summary","inputs_digest":{"batch":"process_run","sampleSize":50},"outputs":{"mean":1.11236,"median":1.0825,"stdDev":0.19193927185866017,"skewness":-0.1125434663213487,"adPValue":0.02939576882587034,"minimum":0.741,"maximum":1.502},"status":"success","decision":"Whole-run summary. AD p=0.029 rejects normality for the pooled run; this reflects two superimposed levels, not a skewed single population."}
{"step_id":4,"method_id":"basic.normality","inputs_digest":{"batch":"process_run","sampleSize":50},"outputs":{"pValue":0.07855470700464376,"statistic":0.9587183961824861,"adPValue":0.02939576882587034,"adStatistic":0.8334704684261851},"status":"success","decision":"Pooled-run normality is ambiguous (Shapiro p=0.079, AD p=0.029) - resolved once the run is split at the change point."}
{"step_id":5,"method_id":"control_chart.imr","inputs_digest":{"batch":"process_run","sampleSize":50},"outputs":{"individualsUCL":1.4137060703430309,"individualsLCL":0.8110139296569692,"centerLine":1.11236,"flaggedCount":36,"beyondLimitsCount":4,"sigmaWithin":0.1004486901143436,"test2Count":25,"test5Count":13,"test6Count":32},"status":"success","decision":"Process is NOT in statistical control: 36 of 50 bores raise special-cause flags, 4 beyond the individuals limits. Capability on the pooled run is therefore not interpretable."}
{"step_id":6,"method_id":"nonparametric.runs_test","inputs_digest":{"batch":"process_run","sampleSize":50},"outputs":{"pValue":1.9580439492017376e-09,"zStatistic":-6.001249869818786,"runs":5,"expectedRuns":26.0},"status":"success","decision":"Only 5 runs about the median against 26 expected (p=2.0e-9): the sequence is non-random, consistent with a sustained level shift rather than noise."}
{"step_id":7,"method_id":"basic.two_sample_t","inputs_digest":{"batch":"process_run","nBefore":25,"nAfter":25,"changePointIndex":25},"outputs":{"pValue":1.119436295041613e-16,"tStatistic":-12.541646696259136,"meanBefore":0.94604,"meanAfter":1.27868,"shift":0.33264000000000005,"sdBefore":0.09862068748492882,"sdAfter":0.08865932927034055,"changePointIndex":25},"status":"success","decision":"Change point located at bore 26 (index 25) by maximising the split t-statistic. Level rose 0.333 um Ra, from 0.946 to 1.279 (p=1.1e-16)."}
{"step_id":8,"method_id":"anova.equal_variances","inputs_digest":{"batch":"process_run","numGroups":2,"sampleSize":50},"outputs":{"pValue":0.5262712470395754,"statistic":0.4075079619556113},"status":"success","decision":"Levene p=0.526: spread is unchanged across the shift. Only the mean moved, which points to a setpoint/consumable change rather than added variability."}
{"step_id":9,"method_id":"control_chart.imr","inputs_digest":{"batch":"process_run","segment":"before","sampleSize":25},"outputs":{"individualsUCL":1.2431366312056737,"individualsLCL":0.6489433687943262,"centerLine":0.94604,"flaggedCount":0,"sigmaWithin":0.09903221040189124},"status":"success","decision":"Segment before the change point is itself in control (0 special-cause flags) - two stable regimes, not one chaotic process."}
{"step_id":10,"method_id":"basic.normality","inputs_digest":{"batch":"process_run","segment":"before","sampleSize":25},"outputs":{"pValue":0.11145520329001612,"statistic":0.9346722616164327,"adPValue":0.10790387205279153,"adStatistic":0.5977666600170508},"status":"success","decision":"Segment before the change point is normal (AD p=0.108), so normal-theory capability is valid within the segment."}
{"step_id":11,"method_id":"control_chart.imr","inputs_digest":{"batch":"process_run","segment":"after","sampleSize":25},"outputs":{"individualsUCL":1.5731170567375887,"individualsLCL":0.9842429432624114,"centerLine":1.27868,"flaggedCount":0,"sigmaWithin":0.09814568557919623},"status":"success","decision":"Segment after the change point is itself in control (0 special-cause flags) - two stable regimes, not one chaotic process."}
{"step_id":12,"method_id":"basic.normality","inputs_digest":{"batch":"process_run","segment":"after","sampleSize":25},"outputs":{"pValue":0.7536751847510905,"statistic":0.9742723223380818,"adPValue":0.5136130811772953,"adStatistic":0.3198214087561446},"status":"success","decision":"Segment after the change point is normal (AD p=0.514), so normal-theory capability is valid within the segment."}
{"step_id":13,"method_id":"control_chart.cusum","inputs_digest":{"batch":"process_run","sampleSize":50,"baselineMean":0.94604},"outputs":{"flaggedCount":12,"firstSignalIndex":26,"decisionInterval":0.39612884160756495},"status":"success","decision":"CUSUM against the pre-shift baseline first signals at index 26, one bore after the shift: a CUSUM on the line would have caught this almost immediately."}
{"step_id":14,"method_id":"control_chart.ewma","inputs_digest":{"batch":"process_run","sampleSize":50,"lambda":0.2},"outputs":{"flaggedCount":24,"firstSignalIndex":26},"status":"success","decision":"EWMA (lambda=0.2) also first signals at index 26, corroborating the CUSUM detection point."}
{"step_id":15,"method_id":"capability.normal","inputs_digest":{"batch":"process_run","segment":"after","sampleSize":25,"lsl":0.4,"usl":1.6},"outputs":{"cp":2.037786977794505,"cpk":1.0913028528415507,"pp":2.255825773170005,"ppk":1.2080698957249767,"mean":1.27868,"sdWithin":0.09814568557919623,"sdOverall":0.08865932927034055,"observedOutOfSpecPct":0.0},"status":"success","decision":"Capability of the after-shift regime, computed only because that segment is in control and normal."}
{"step_id":16,"method_id":"capability.normal","inputs_digest":{"batch":"process_run","segment":"before","sampleSize":25,"lsl":0.4,"usl":1.6},"outputs":{"cp":2.0195449459157038,"cpk":1.8379205371130178,"pp":2.0279720725995136,"ppk":1.8455897842037303,"mean":0.94604,"sdWithin":0.09903221040189124,"sdOverall":0.09862068748492882,"observedOutOfSpecPct":0.0},"status":"success","decision":"Capability of the before-shift regime, computed only because that segment is in control and normal."}
{"step_id":17,"method_id":"capability.normal","inputs_digest":{"batch":"process_run","segment":"pooled","sampleSize":50,"lsl":0.4,"usl":1.6},"outputs":{"cp":1.99106628242075,"cpk":1.6182059365994241,"pp":1.0419962421618207,"ppk":0.8468650792129838,"mean":1.11236,"sdWithin":0.1004486901143436,"sdOverall":0.19193927185866017,"observedOutOfSpecPct":0.0},"status":"success","decision":"Pooled capability reported ONLY to show what mixing regimes does: Ppk collapses to 0.847 versus Cpk 1.618 within-subgroup. Not a valid statement of process capability because the run is out of control."}
{"step_id":18,"method_id":"basic.one_sample_t","inputs_digest":{"batch":"process_run","segment":"after","sampleSize":25,"target":1.0},"outputs":{"pValue":3.9145211059776686e-14,"tStatistic":15.716338161675424,"mean":1.27868,"offTarget":0.27868000000000004},"status":"success","decision":"Current regime sits 0.279 um Ra above the 1.00 target (p=3.9e-14): inside the band but significantly off target toward the upper limit."}
{"step_id":19,"method_id":"basic.one_sample_t","inputs_digest":{"batch":"process_run","segment":"before","sampleSize":25,"target":1.0},"outputs":{"pValue":0.011520621958871175,"tStatistic":-2.7357343259367437,"mean":0.94604,"offTarget":-0.05396000000000001},"status":"success","decision":"Pre-shift regime was only 0.054 um Ra below target (p=0.012) - close to nominal, and the better of the two states."}
{"step_id":20,"method_id":"regression.ols","inputs_digest":{"batch":"process_run","segment":"after","sampleSize":25},"outputs":{"modelPValue":0.3610948628364108,"rSquaredPct":3.638035799290435,"rSquaredAdjPct":-0.5516148181317293,"slope":-0.0022976923076923057},"status":"success","decision":"No trend within the current regime (p=0.361): the process is sitting at a new fixed level, not drifting further. A one-off step, so a setpoint correction should recover it."}
{"step_id":21,"method_id":"basic.correlation","inputs_digest":{"batch":"process_run","segment":"after","sampleSize":25},"outputs":{"correlationCoefficient":-0.19073635729169292,"pValue":0.3610948628364107},"status":"success","decision":"Roughness vs finishing order within the current regime: no association (r=-0.191, p=0.361)."}
{"step_id":22,"method_id":"basic.correlation","inputs_digest":{"batch":"process_run","segment":"pooled","sampleSize":50},"outputs":{"correlationCoefficient":0.7091653298668337,"pValue":8.21151743622574e-09},"status":"success","decision":"Apparent strong correlation with finishing order over the whole run (r=0.709) is an artefact of the single step, not a gradual drift."}
```

## Submitted route declarations
```json
[{"point":"measurement_system_trustworthy","chosen_branch":"proceed_with_analysis_gage_acceptable_with_tolerance_caveat","observed":{"percentStudyVariation":15.60424773702267,"percentTolerance":33.31868376090741,"ndc":8.925313227424608,"pctContributionGageRR":2.434925474383771}},{"point":"gage_rr_interaction_pooling","chosen_branch":"pool_interaction_into_repeatability","observed":{"interactionPValue":0.6750320379405397,"alpha":0.25}},{"point":"process_stability","chosen_branch":"not_stable_investigate_shift_before_capability","observed":{"flaggedCount":36,"beyondLimitsCount":4,"runsPValue":1.9580439492017376e-09}},{"point":"capability_basis","chosen_branch":"report_capability_per_regime_not_pooled","observed":{"pooledPpk":0.8468650792129838,"currentCpk":1.0913028528415507,"currentPpk":1.2080698957249767,"segmentFlaggedCount":0}},{"point":"shift_shape","chosen_branch":"step_change_not_drift","observed":{"trendPValue":0.3610948628364108,"segmentShift":0.33264000000000005,"levenePValue":0.5262712470395754}},{"point":"improve_and_control_evidence","chosen_branch":"unavailable_no_post_action_batch_exists","observed":{"provisionTurnsUsed":1,"processFactsAvailable":0}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
