# Project Report: Chip-Capacitor Defect Share

## Bottom line
The line is currently stable and its defect share is below the committed level. The baseline was stable but not capable against the commitment. The settings model identifies paste thickness, reflow peak, and their interaction as strongly associated with lot defect share. The change was followed by a significant reduction, and the post-change lots have remained below target.

## Baseline
Across 25 baseline lots of 4000 units each, there were 599 defects in 100000 inspected units, a defect share of 0.00599 (0.599%). The p chart centerline was 0.00599 and 0 lots were outside the control limits. Against the required share of 0.0025 (0.25%), the one-proportion test gave z = 22.10034078145949, normal-approximation p = 3.136907093091575e-108, and exact binomial p = 3.7306979805640508e-78. The baseline was statistically stable but well above the commitment.

## What accounts for the baseline level
An OLS model on 40 lots from the line-settings batch related lot defect share to paste thickness, reflow peak, and their interaction. The model p-value was 8.381756185366018e-14, with R-squared = 82.72578038855498% and adjusted R-squared = 81.28626208760123%. The paste-thickness p-value was 1.0930398582646995e-11, the reflow-peak p-value was 8.322450533508093e-11, and the interaction p-value was 7.095312426248794e-12. These settings terms are strongly associated with the lot defect share.

## What the change achieved
The before window had 235 defects in 40000 units (0.005875, or 0.5875%). The after window had 77 defects in 40000 units (0.001925, or 0.1925%). The absolute reduction was 0.00395 (0.395 percentage points), with a two-proportion z = 8.962482483814625 and p = 3.174494287484549e-19. The planned comparison used alpha = 0.05, 40000 units per group, p1 = 0.0059, and p2 = 0.0025; its computed power was 0.9999999914471074. The change was followed by a statistically significant improvement.

## Since the change
The 20 post-change lots contained 80000 inspected units and 147 defects, a share of 0.0018375 (0.18375%). The post-change p chart had centerline 0.0018375 and 0 out-of-control lots. Against the required share of 0.0025, the exact one-proportion p-value was 9.717173745815809e-05. The post-change lots were not detectably different from the immediate post-change trial window (z = -0.3310280176820626, p = 0.7406233224472969). Combining all post-change data gives 224 defects in 120000 inspected units, a share of 0.0018666666666666666 (0.18666666666666668%); the test against the required share gave z = -4.393357178922209 and p = 1.1161352409798517e-05. The level reached since the change is below the commitment.

## Recommended next step
Hold the changed line settings and continue to monitor the defect share with the p chart. All requested data batches were released, so no conclusion here is blocked by missing data. The before/after data establish a statistically significant improvement, but they are not a randomized trial, so the evidence supports association rather than definitive causal proof.
