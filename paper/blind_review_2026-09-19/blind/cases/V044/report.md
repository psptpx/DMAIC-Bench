# Chip-capacitor defect-share improvement report

## Executive conclusion

The baseline was statistically stable but chronically unacceptable. Its pooled defect share was **0.005700** against the committed **0.002500**: **2.28 times** the requirement. The line-settings record contains strong statistical associations, but the exact physical setting change implemented between trial windows is not on file. The controlled before/after trial does not demonstrate an effect at its filed risk level. Longer-run post-change data show a favorable point estimate and a stable new level, but do not statistically demonstrate improvement from baseline; that level is still not enough to meet the commitment.

## Baseline: steady, but above the commitment

Across **25 lots**, **570 defects** were found among **100000 inspected**. The p-chart center line was **0.005700**, with equal-lot three-sigma limits of **0.002129** and **0.009271**. The chart flagged **0 lots**, supporting a stable baseline rather than intermittent special causes.

Against the committed share of **0.002500**, the baseline excess was **0.003200**. A one-sided exact binomial test gave **p = 1.5884e-67**. Thus stability did not mean acceptability; the baseline consistently missed the business requirement.

## What the records account for

The filed OLS model used **40 lot records** and included paste thickness, reflow peak, and their interaction. It was significant (**F = 25.670124**, **p = 4.65861e-09**) and explained **68.145%** of observed variation, with adjusted **R-squared = 65.490%**. Term p-values were **7.50498e-07** for paste thickness, **1.22021e-06** for reflow peak, and **4.79242e-07** for their interaction.

This makes the two settings credible explanatory variables on file, including an interaction: their effects should not be interpreted independently. However, these are observational associations and do not alone establish causation. The process-owner query returned no recorded fact matching the exact implemented change. Therefore, this report cannot state which setting was physically changed without inventing it; that documentation gap stops the identification of the intervention itself.

## Did the trial show that the change worked?

The filed design used **6000 inspected per group**, **alpha = 0.05**, and planning shares **0.0059** and **0.0025**. Computed prospective two-sided power was **0.821196**.

Observed shares were **0.006500** before and **0.004833** after, an absolute change of **-0.001667** and a relative reduction of **0.256410**. The pooled two-sided two-proportion test gave **z = 1.216129** and **p = 0.223936**. The observed direction was favorable, but the trial does not statistically demonstrate that the change did anything at the filed risk level. Prospective power for the planned contrast does not override this nonsignificant observed result.

## Is the level reached since the change enough?

Across the subsequent **20 lots**, there were **411 defects** among **80000 inspected**, for **0.005137**. Its p-chart limits were **0.001746** and **0.008529**, and **0 lots** were flagged. The new level therefore appears stable.

Relative to the baseline, the pooled reduction was **0.000563**, or **0.098684** proportionally. The aggregate baseline-versus-post comparison gave **z = 1.610719** and **p = 0.107241**. Thus the post-change point estimate is lower, but this comparison does not statistically demonstrate a sustained reduction from baseline.

Nevertheless, the new average is **2.05 times** the committed share and exceeds it by **0.002637**. The one-sided exact test against the commitment gave **p = 3.3947e-39**. Binomial capability summarizes the new level as **average p = 0.005137** and **process Z = 2.566435**. The result is stable and has a lower point estimate than baseline, but the reduction is not statistically demonstrated and the process is not capable of meeting the commitment.

## Recommended next actions and control plan

- Do not close the project or claim the trial proved effectiveness. Treat the trial result and the later favorable aggregate point estimate as distinct evidence; neither comparison statistically demonstrates improvement.
- Recover and approve the missing change record: identify the actual paste-thickness and reflow-peak settings used, ownership, effective date, and allowed ranges.
- Run a designed, randomized confirmation study of both settings and their interaction. Select sample size from the effect that must be detected, rather than relying on the earlier planned contrast.
- Continue lot-by-lot p-chart monitoring at the demonstrated post-change center line. Escalate any point outside the computed limits and investigate setting drift, inspection changes, and material differences.
- Keep the committed share as the release criterion. Further improvement is required before declaring success, because a stable process can still be stably unacceptable.
