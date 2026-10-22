# Chip-capacitor defect-rate review

## Bottom line

The line is now stable, but it is not at the committed defect share. The baseline was also stable—this was a common-cause process operating far above commitment, not a special-cause outbreak. The later change is strongly associated with a large reduction, and the reduction persisted across the confirmation lots. Nevertheless, the confirmed level remains above commitment, so this is not a project close-out.

No process fact identifying the actual change was available. The measured before-and-after effect is established, but the available evidence does not support a named causal statement such as “changing parameter X caused the gain.”

## Baseline: steady, but not good

The commitment is a defect share of **0.0025** (0.25%). Across **25** consecutive baseline lots, inspection totaled **100,000** units and produced **1,785** defects. The p-chart center line was **0.01785** (1.785%), with 3-sigma limits of **0.011569426827510089** and **0.024130573172489914**. No lot was outside those limits (`outOfControlCount = 0`).

Thus, the baseline held steady, but at **7.14 times** commitment—**0.01535** above the required share. The capability calculation gave `processZ = 97.20350458321009`; here the positive Z indicates adverse performance above the committed maximum. The exact-test routine's p-value underflowed to zero, so the more stable evidence is the Z score and the directly measured excess.

## What the settings record accounts for

A separate record of **40** lots contains paste thickness, reflow peak, and lot defect share. The specified model with both settings and their interaction explained **74.49988903608033%** of lot-to-lot variation (adjusted R-squared **72.37487978908703%**; model p-value **8.844474875407327e-11**). Paste thickness, reflow peak, and their interaction were all significant, with coefficient p-values of **1.3832726192588158e-05**, **6.056350416391993e-05**, and **9.507904201668252e-06**, respectively. Residual normality was not contradicted (Shapiro-Wilk p-value **0.29056822668248805**).

This file therefore accounts statistically for variation in its own defect-share record, but it is observational. It cannot by itself prove causality, and its **40** rows cannot be merged row-for-row with the **25**-lot baseline count series.

## What the change achieved

The trial metadata specified **40000** units per window, alpha **0.05**, planning share **0.018** before, and planning share **0.0025** after; the computed effect size (Cohen h) was **0.1690980192630125** and nominal power was **1.0**.

Observed results were **731** defects among **40000** inspections before (**0.018275**) and **134** among **40000** after (**0.00335**). The absolute reduction was **0.014925**, or **81.66894664842681%**. The Newcombe 95% interval for after-minus-before was **-0.016380877730109874** to **-0.013516114185988718**. The two-proportion test gave z = **-20.409246334850078** and p = **1.3840232699771407e-92**.

So the change can be shown to have coincided with a large, statistically detectable reduction. However, this was a before-and-after comparison, not a randomized comparison, and the identity of the change is absent. The strong observed result supports that something happened; it does not identify which physical action was responsible.

The immediate after window itself was still above commitment: **0.0008500000000000001** above the **0.0025** target, **1.34** times target (exact two-sided p-value **0.0011121688607600864**).

## Level reached since the change

The separate confirmation record had **20** lots and **80000** inspections, with **269** defects. Its center line was **0.0033625** (0.33625%), with p-chart limits of **0.000616560163452684** and **0.006108439836547316**; no lot was outside the limits (`outOfControlCount = 0`). Thus, the new level also held steady under the pointwise control-chart criterion.

It was consistent with the separate immediate after window (z = **0.03528279319945898**, p = **0.9718542438256355**). But it remained **0.0008625** above commitment—**1.345** times the target. The exact 95% share interval was **0.0029732061340359667** to **0.0037884650838915165**, entirely above **0.0025**; the one-sided greater-than-target p-value was **1.936949216991863e-06**. Compared with the allowed count, those **80000** inspections included **69** excess defects. A further reduction of **25.650557620817843%** in the current defect rate is needed to reach **0.0025**. The post-change binomial capability calculation remained adverse, with `processZ = 4.885147045293041`.

## What should happen next

- **Keep the changed configuration in place.** It is strongly associated with a reduction from **0.018275** to **0.00335**, and the **20**-lot record confirms a steady new level.
- **Do not close against the commitment.** The confirmed level is **0.0033625**, not **0.0025**; **69** excess defects occurred in **80000** inspections.
- **Record and verify the actual change and its mechanism.** The process fact needed to identify the change was unavailable. Without that record, the team cannot transfer, standardize, or defend a causal operating recipe.
- **Treat paste thickness and reflow peak as improvement hypotheses, not as a proven recipe.** Their significant association is useful, but the observational surface's in-range minimum predicted **0.00554728662682953** (prediction interval **0.004371384319129843** to **0.006723188934529218**), still above target. A designed, randomized confirmation is required before changing settings.
- **Continue the 3-sigma p-chart by lot and investigate the remaining common-cause gap.** Add a documented reaction plan and only recognize close-out when evidence demonstrates **0.0025 or less**, not merely a stable process.

## Data and computation limits

All requested shop-floor batches were released; none was denied. The process-owner request for the change identity was `unroutable`, so the conclusion stops at “a detectable before-and-after improvement,” not at a named causal change. The settings model is a separate **40**-row observational record and cannot establish causality. The initial post-lot and supplemental computations failed and were rerun successfully; their final reported results come from the corrected computations.
