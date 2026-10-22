# Void fraction project — status report

**Task:** [TASK]  
**Characteristic:** percent void area per joint  
**Acceptance limits from the charter:** LSL 0.0, USL 25.0 (tolerance 25.0)  
**Charter goal:** void fraction under the acceptance limit and holding steady

## A note on scope before the numbers

The assignment brief describes cylinder-bore roughness in um Ra with a 0.40-1.60 band. Every
batch the data steward actually holds is **percent void area against a 25.0 upper limit** — the
charter, the repeat-reading study and the build-order run all agree on that characteristic and
those limits. No roughness data exists in the archive. This report therefore analyses the void
fraction data that exists; there is no Ra data on which to state anything about a 0.40-1.60 band.

## 1. Can the recorded readings carry a conclusion? Yes.

A crossed gage R&R was run on the repeat-reading study: 3 operators x 12 parts x 3 replicates,
108 readings. The operator-by-part interaction was not significant (p = 0.575) and was pooled
into repeatability.

| Measure | Result | Guideline |
|---|---|---|
| %study variation (total gage R&R) | 19.97% | under 30% acceptable |
| %tolerance | 18.28% | under 30% acceptable |
| Number of distinct categories | 6.92 | 5 or more acceptable |
| Repeatability share of study variation | 16.37% | |
| Reproducibility share of study variation | 11.44% | |

The measurement system resolves part-to-part differences well: part variance is 13.96 of a total
14.54, leaving 0.58 to the gage. Conclusions drawn downstream are supportable.

One caveat worth acting on: the operator main effect is statistically significant (p = 0.00000016)
even though its magnitude is modest. Operators are not reading identically. It does not
invalidate the study, but it is the first thing to tighten if this gage is ever asked to judge
parts nearer the limit.

## 2. How has the line behaved across the run?

Fifty joints in build order. Mean 8.36% void area, median 7.69%, standard deviation 2.77%,
range 4.17% to 15.28%.

Stability was checked four ways and the answer is consistent — the process is stable:

- **I-MR chart:** centre line 8.36, upper individuals limit 17.21. No point beyond the
  individuals limits and none beyond the moving-range limit of 10.87. One Nelson rule-5 signal
  (2 of 3 points beyond 2 sigma) near joint 36; a single pattern flag in 50 points with no
  supporting evidence elsewhere is not a real special cause. The calculated lower limit of
  -0.48 is below the physical floor of zero and is not a usable alarm line.
- **Runs test about the median:** p = 0.391. No trend, drift or non-random patterning across
  build order.
- **EWMA (lambda 0.2):** 0 flags.
- **CUSUM (k = 0.5 sigma, h = 4 sigma):** 0 flags.

EWMA and CUSUM are the sensitive tests for a small sustained shift, and both are silent. The line
has not drifted over this run.

## 3. Where does voiding sit against its acceptance limit today?

The readings are right-skewed (skewness 0.72) and normality is rejected — Anderson-Darling
p = 0.029, Shapiro-Wilk p = 0.019. That is exactly what a bounded fraction should look like, so
the capability statement is built on a fitted lognormal (KS p = 0.709, ahead of Weibull at 0.677):

| Measure | Result |
|---|---|
| Ppk (percentile method, vs USL 25.0) | 1.320 |
| Pp | 1.401 |
| Expected fraction above the 25% limit | 0.018% (184 ppm) |
| Median (50th percentile) | 7.94 |
| 99.865th percentile | 20.86 |
| Joints observed above the limit | 0 of 50 |

The process sits below the limit and the position is not marginal: the signed-rank test against
25.0 gives p < 0.001, and the parametric cross-check agrees (t = -42.39, p < 0.001).

**Capability verdict: capable, but short of a 1.33 Ppk target.** Ppk 1.320 leaves the 99.865th
percentile at 20.86 against a limit of 25.0 — headroom, but not comfortable headroom.

A normal-theory calculation was also run for reference only and should not be quoted as the
verdict: it returns Cp 1.413, Cpk 0.945, Pp 1.502, Ppk 1.005. The Cpk of 0.945 is depressed
entirely by the lower side (Cpu 1.880 vs Cpl 0.945) — it is measuring distance from zero, and
zero void area is a physical floor and the ideal outcome, not a requirement anyone can fail.
Judging this characteristic two-sided understates the process.

**On the defect rate specifically:** zero of 50 joints exceeded the limit, but 50 joints is not
enough to *prove* a low rate. Tested against a 5% nonconformance benchmark the exact
one-proportion p-value is 0.077, and the 95% upper confidence bound on the true rate is 5.8%.
The observed record is clean; the evidence base is thin.

## 4. What was changed, and what did the change achieve? Nothing — and there is no data.

This is the honest limit of the project and the report stops here rather than filling the gap:

- **No improvement data exists.** A request for improvement-trial or post-change data was
  refused; the steward enumerates only three data topics for this project (charter, repeat
  readings, void fraction in build order). No corrective action was trialled, so **no change
  effect can be quantified** — no before/after comparison appears in the trace because none
  could be computed.
- **No control-phase data exists.** There is no post-change monitoring record, so this report
  cannot demonstrate that any gain is being held. What it can say is that the run analysed here
  is already stable on four independent tests.
- **No process facts are available.** Two questions to the process owner — whether zero percent
  void is a natural bound with only the 25% upper limit as a real requirement, and whether any
  setup, material-lot or operator change occurred during the 50 joints — both came back with no
  matching fact recorded. The treatment of the lower limit above is therefore my engineering
  judgement about what void area physically means, not a confirmed customer requirement, and
  the one rule-5 flag near joint 36 could not be checked against a process log.

## 5. Where this leaves the business, and what should change next

**Where things stand.** The gage is fit for the decision, the line is stable, and void fraction is
under the acceptance limit with a Ppk of 1.320 and no observed rejects in 50 joints. There is no
quality emergency here.

**What is causing the residual risk.** Two things, neither of them a special cause. First, common-
cause spread: at a mean of 8.36 with a standard deviation of 2.77 and a right tail, the 99.865th
percentile reaches 20.86 and the fitted rate above the limit is 184 ppm. That is inherent to the
process as it currently runs, not to any event in the run. Second, measurement: a significant
operator effect (reproducibility 11.44% of study variation) is carried in every number above.

**What should change next, in order:**

1. **Close the operator gap in the X-ray reading method.** The gage passes overall, but operators
   differ significantly. Standardise the reading procedure and re-run the study; the target is to
   pull the 11.44% reproducibility share down and hold total gage R&R under 20%.
2. **Confirm the limits with the process owner before any capability number goes to a customer.**
   Whether the 0.0 lower limit is a real requirement changes Ppk from 1.320 to 1.005. That single
   fact is the difference between a capable process and a marginal one, and it is currently
   unconfirmed.
3. **Attack the right tail, not the average.** The mean has ample margin; the risk is in the upper
   percentiles. A variance-reduction trial is warranted — but note that no trial has been run and
   none can be evaluated from the data on hand.
4. **Extend the sample before claiming a defect rate.** Fifty joints cannot demonstrate sub-5%
   nonconformance (p = 0.077, upper bound 5.8%). Continued sampling is needed to make the clean
   record statistically meaningful.

**How it will be held.** No control plan can be evidenced from this data. What the analysis
supports is putting the process on ongoing I-MR monitoring at the established centre line of 8.36
with an upper individuals limit of 17.21, using the upper limit and pattern rules only, since the
calculated lower limit of -0.48 is not physically attainable. Adding EWMA alongside it would give
early warning of the small sustained shift that the individuals chart is poor at catching — both
read zero flags on this run, which is the baseline any future monitoring should be compared to.
