# Fillet-Height Project Report

## Bottom line

The baseline is not a single stable level. It starts near the target, then shifts high; the final observed nonconformance is on the high side. The designed run identifies chain speed, rail angle, and their interaction as influential settings. The operational before/after comparison shows a statistically significant increase in mean fillet height and a significant reduction in spread, but the service provided no record of what was actually changed. Therefore, the conclusion stops at association with the change window and cannot identify the mechanism.

## Acceptance limits and baseline behavior

The accepted interval is 6.8 to 7.5 mm, with target 7.15 mm. Across all 60 baseline joints, the mean was 7.263783 mm, median 7.267 mm, and standard deviation 0.145937 mm. One joint was above the upper limit and none were below the lower limit. The observed nonconforming proportion is 0.016667, with an exact 95% upper confidence bound of 0.089399.

The baseline mean was 0.113783 mm above target (one-sample p = 0.000000111261). Height also increased with production order: the order slope was 0.006274 mm per joint, with R-squared 56.369292% and p = 0.000000000004913. The first half averaged 7.1394 mm and the second half 7.388167 mm, a difference of 0.248767 mm (two-sample p = 0.000000000000000001560). Runs tests about both target and the sample mean supported nonrandom patterning.

An overall individuals chart produced three limit signals, but it mixed the two levels. Separate charts for each half had no within-half signals and centers of 7.1394 and 7.388167 mm. A CUSUM first signaled at index 22 and then identified the sustained higher section. These results support a real level shift rather than isolated instability.

Against the accepted interval, short-term potential was better than overall performance: Cp = 1.533557, Cpk = 1.035005, Pp = 0.799433, and Ppk = 0.539541. The high mean, rather than short-term variation alone, is the principal concern.

## What accounts for the height

The replicated 2-to-the-3rd designed run contains 16 runs. Its full factorial model was significant (p = 0.000239552) and explained 94.176379% of response variation. Chain speed had a coded effect of 0.2399 mm (one-way p = 0.001637); rail angle had a coded effect of 0.161525 mm; and air pressure had a smaller coded effect of 0.037775 mm (one-way p = 0.675644). In the full factorial, the chain-speed coefficient p was 0.000029490 and rail-angle coefficient p was 0.000461398, while air pressure was not significant (p = 0.220210). The chain-speed/rail-angle interaction effect was 0.122425 mm with coefficient p = 0.002580.

Thus, two deliberately varied settings and their interaction account for most variation in the designed response. Air pressure was not established as an important individual factor. The three logged variables were analyzed on 48 rows: their joint regression was not significant (p = 0.090413, R-squared 13.556306%), although preheat temperature had a marginal association (correlation 0.333018, p = 0.020731; regression coefficient p = 0.019762). This is not causal evidence and does not explain away the designed effects.

Among factorial corners, high chain speed, low rail angle, and low air pressure was closest to target, with predicted height 7.1824 mm and 95% prediction interval 7.021960 to 7.342840 mm. This should be treated only as a confirmation candidate, not an adopted setting, until a controlled trial demonstrates that it centers and holds production.

## Before/after change

The before window averaged 7.191667 mm with standard deviation 0.133718 mm; its mean was not distinguishable from target (difference 0.041667 mm, p = 0.098564). The after window averaged 7.284033 mm with standard deviation 0.076011 mm; it was 0.134033 mm above target (p = 0.000000000144409). The after-minus-before mean increase was 0.092367 mm (95% CI 0.035839 to 0.148894 mm; p = 0.001933). A rank test agreed (p = 0.001721).

Spread also changed: SD fell from 0.133718 to 0.076011 mm, the variance ratio was 3.094751, and Levene's p was 0.042181. Neither window had an individual outside its own chart limits, but moving the level upward does not improve target performance.

The after window failed Shapiro-Wilk (W = 0.900046, p = 0.008420). A Johnson SU sensitivity fit was compatible with the data (KS p = 0.385697) and gave Pp = 0.992189 and Ppk = 0.840650. The corresponding normal-theory values were Pp = 1.534863 and Ppk = 0.947084. With only a small after-sample and a rejected normal fit, these should be read as imprecise sensitivity results, not a definitive capability claim.

## Data gap and what happens next

No data batch was denied. However, the process owner question about the identity and direction of the actual line change was unroutable; that step has no data and its conclusion stops there. The significant before/after result does not identify what changed and cannot support a causal claim about a named setting.

Next: preserve the current configuration while running a controlled confirmation of the target-near factorial corner; continue an individuals chart and CUSUM centered at 7.15 mm; retrieve the missing change record; and collect enough after-change data for a distribution-free or model-validated capability review. If confirmation does not lower the level and tighten variation around target, adjust chain speed and rail angle using the designed-model relationship rather than reacting to individual joints.
