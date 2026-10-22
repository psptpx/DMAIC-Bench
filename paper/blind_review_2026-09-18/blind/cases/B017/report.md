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
