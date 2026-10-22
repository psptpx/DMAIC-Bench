# Seal-strength project status

## Decision in brief

The recommended setting change should be **held conditionally and monitored**, not released as an unrestricted long-term capability claim. The twenty confirmation seals were convincingly above both requirements and stable on trial limits, but this is still an early twenty-piece run. Against the programme's 55 N margin, overall Ppk is 0.951 and within-process Cpk is 0.882, so longer-run margin still has to be established.

## Baseline: where the line stood

The sixty consecutive baseline assemblies were stable but low and too variable. Their mean was 51.197 N, median 51.420 N, and sample standard deviation 4.359 N. Four seals (6.667%) were below the 45 N LSL. Fifty (83.333%) were below the programme's 55 N level. The one-sample test puts the mean 3.802667 N below 55 N (t = −6.757698, p = 3.474e-9).

The I-MR chart had zero individual and zero moving-range signals. Build-order Pearson correlation was effectively zero (r = 0.006775, p = 0.959), and the median runs test was likewise non-significant (p = 0.434658). Anderson-Darling did not reject normality (p = 0.444). This was therefore common-cause centring/spread, not a demonstrated drift or isolated special cause. Consequently, capability was poor: Cpk = 0.463 (within) and Ppk = 0.474 (overall) against 45 N.

## Which varied settings mattered

The screening experiment was a complete replicated factorial across all three varied settings: 16 runs, two at each of eight corners. The factorial model was significant (p = 0.003695) and explained 88.075% of variation.

* **Bond angle** was significant: high minus low effect +4.628 N (p = 0.0002897).
* **Bead spacing** was also significant: +3.082 N (p = 0.003625).
* **Cure temperature** was not: +0.597 N (p = 0.454).
* The bond-angle × bead-spacing interaction was suggestive but not significant (p = 0.068495).

Residual normality was not rejected (AD p = 0.437450), and Bartlett's test found no evidence of unequal corner variances (p = 0.455696). The justified route was therefore to carry bond angle and bead spacing into the composite design and stop varying cure temperature as a design factor.

## What the composite design supports

The later central composite design had four factorial points, four axial points, and five centre points. Its full quadratic model was significant (p = 0.000485), explained 93.568% of variation, and showed no lack of fit relative to pure error (p = 0.963). Both quadratic terms were highly significant, confirming curvature rather than a “higher is better” corner extrapolation.

The canonical solution was an interior maximum at coded bond angle **+0.481432** and coded bead spacing **+0.468863**. It predicted 48.522 N, with a prediction interval of 46.751 to 49.654 N. Thus the composite analysis identified a direction and robust interior optimum, but its absolute prediction did not support the 55 N requirement. Confirmation was essential.

A material caution remains: composite responses averaged 8.213 N below screening at the four common coded corners (paired t = 7.322, p = 0.00526). The supplied batches do not explain that design-batch scale shift. Composite residual normality was also rejected (AD p = 0.012450), another reason to treat its absolute interval cautiously. I also asked for the mapping from composite coded settings to physical settings; none was available. Therefore, the defensible specification of the change is the coded optimum above—not an invented physical angle or spacing.

## What the change achieved

Twenty seals at the recommended settings averaged **59.873 N** (CI 59.074 to 60.672 N), with median 59.495 N, SD 1.708 N, minimum 57.530 N, and maximum 63.490 N. All twenty were at least 55 N; none was below 45 N. The mean was 4.873 N above 55 N (one-sided t = 12.762, p = 4.549e-11). The exact lower bound for the 55-N pass proportion is 0.861.

Relative to baseline, the mean rose **8.676 N** (Welch t = 12.758, p = 7.250e-21). The 55-N pass fraction rose from 10/60 (16.667%) to 20/20 (100%); the two-proportion comparison was significant (z = 6.667, p = 2.616785e-11). Against the mandatory 45 N LSL, Cpk was 2.692 and Ppk was 2.903. Trial I-MR limits were 54.347 and 65.399 N with zero signals.

The confirmation mean was 11.351 N above the composite model's 48.522 N point prediction. That discrepancy is statistically unmistakable (t = 29.727, p = 1.073e-17). It reinforces that the composite model was useful directionally, but not as an absolute predictor across those batches.

## How to hold the gain

- **Freeze and document the actual process recipe now.** Record the exact physical bond-angle and bead-spacing set-points, the coded mapping, cure condition, material lot, and equipment used for the twenty confirmation seals. The absent coded-to-physical mapping is a documentation gap; it does not invalidate the confirmation data, but it prevents a fully auditable transfer without correction.
- **Start I-MR monitoring at the trial limits**, not occasional capability summaries. The individuals chart centre is 59.873 N with trial limits 54.347–65.399 N; use 45 N as an outer production stop and treat sustained approach toward 55 N as an early warning. Recalculate limits after the planned validation volume.
- **Treat capability as conditional.** Against 45 N, this run supports Cpk 2.692 / Ppk 2.903. Against 55 N, target Ppk is only 0.951 and target Cpk 0.882, with a normal-theory estimate of 2161 ppm below 55 N even though zero of twenty were observed below it.
- **Run the planned longer verification** (for example, the next production sequence) before declaring sustained 55-N margin. Preserve run order and test for drift, not just a capability index.
- **Investigate the unexplained 8.213-N screening/composite shift** and the 11.351-N prediction-to-confirmation gap. Likely candidates cannot be named from these data; material lot, gauge, fixture, operator, cure setup, and design-batch context should be checked from process records.
- **Retain cure temperature in normal process control.** It was not a significant design factor over the tested range, but that supports holding it fixed, not ignoring it.

## Data and conclusion limits

No requested shop-floor batch was reported missing. The only outside process-fact request was unroutable, so there is **no data here mapping composite coded settings to physical settings**; the conclusion stops at coded settings. The composite absolute prediction also cannot be reconciled with either the screening or confirmation batch without the unexplained scale shift. The confirmation performance itself is strong and statistically clear, but twenty early assemblies are not yet proof of sustained margin against the 55 N programme level.
