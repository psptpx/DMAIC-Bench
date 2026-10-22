# Chip-capacitor defect-share project report

## Where the project stands

The baseline covered 25 lots and 100000 inspected units. It contained 546 defects, for an aggregate defect share of 0.00546 (0.546%). The commitment is 0.0025 (0.25%), so baseline performance was above the commitment. A one-proportion test gave z=18.74412857109458 and p=2.161843095041093e-78.

The baseline was steady in the limited statistical sense assessed here: the p-chart had 0 out-of-control lots, and the runs test p-value was 0.4038037971630485. The baseline center line was 0.00546. Stability therefore means the line was consistently producing a level that was consistently worse than the commitment; it does not mean the commitment was met.

## What accounts for the level

The 40-observation settings model was statistically significant (model p-value 1.20039199680057e-06), with R-squared 56.426363457132034% and adjusted R-squared 52.795227078559705%. Thus the recorded settings explain a material share of the observed variation and provide evidence that at least one modeled setting term or interaction is associated with defect share. This is evidence of association, not proof of causation or an optimized setting.

## What the change achieved

The before window had 237 defects in 40000 inspected units, a share of 0.005925. The after window had 135 defects in 40000 units, a share of 0.003375. The reduction was 0.00255 share points, or 43.0379746835443% relative to the before share. The two-proportion test gave z=5.300792345784441 and p=1.1530117357517475e-07, so the observed improvement is statistically significant.

The supplied planning trial used alpha=0.05, 40000 units per group, and planning shares p1=0.0059 and p2=0.0025. The computed prospective power for those assumptions was 0.9999999914471074.

## Is the reached level enough?

The 20 post-change lots covered 80000 inspected units and 275 defects. Their aggregate share was 0.0034375. The post-change one-proportion test against the commitment gave z=5.309942440535915 and p=1.0965986220000534e-07. Therefore the change improved the process, but the level reached since the change is not yet enough to demonstrate attainment of the 0.0025 commitment.

The post-change lot-share mean was 0.0034375, median was 0.00325, and sample standard deviation was 0.0009627093073853165. The post-change p-chart had center line 0.0034375 and 0 out-of-control lots; the post-change runs test p-value was 0.3236781609070164. The evidence supports a stable new level, but that stable level remains above target.

## Recommended next action

Hold the changed process under routine lot-level p-chart monitoring, preserve the settings used after the change, and investigate the significant settings terms with controlled confirmation work. Do not close the improvement project as meeting target: continue adjustment/DOE work until the post-change aggregate share is at or below 0.0025 with sufficient ongoing evidence. Recheck the commitment using fresh inspected and defective counts, and escalate immediately if the control chart signals a special cause.
