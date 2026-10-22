# Chip-capacitor defect-share project report

## Executive conclusion

The baseline process was statistically steady but not capable of meeting the commitment. Across **25** baseline lots, there were **599** defects in **100000** inspected, for a pooled share of **0.00599**, versus the committed maximum of **0.0025**. After the line change, the trial and subsequent lots both show a materially lower level. Across the subsequent **20** lots, the pooled share is **0.0018375**, and the available evidence supports that it is below the commitment. The result should now be held with a documented settings plan and a continuing p chart.

## Baseline: steady, but at the wrong level

The baseline p chart had center line **0.00599**, lower limit **0.002329840198160741**, upper limit **0.009650159801839258**, and **0** out-of-control lots. Thus the lot sequence is consistent with a stable common-cause process at the observed level; stability does not imply acceptable performance.

An exact one-sided one-proportion test against the required share of **0.0025** returned **2.73393804200261e-78**. The baseline is therefore demonstrably above the commitment. Its binomial performance summary is average defect share **0.00599** and process Z **2.5127328988583177**.

## What on file accounts for variation

The specified OLS model used **40** per-lot records and included paste thickness, reflow peak, and their interaction. The overall model p-value was **8.381756185366403e-14**, with R-squared **82.72578038855495** and adjusted R-squared **81.28626208760119**. The paste-thickness, reflow-peak, and interaction p-values were respectively **1.0930398582647192e-11**, **8.322450533508334e-11**, and **7.095312426248996e-12**, all below the analysis alpha of **0.05**. These settings strongly account for recorded lot-to-lot variation in an associational model; observational regression alone does not establish causation.

The records do not identify the exact setting values implemented as the line change. A process-owner query found no recorded process fact, so the precise intervention and its documented hold mechanism could not be established and are not guessed here.

## Did the change do anything?

The trial design used **40000** units per group, alpha **0.05**, and planning shares **0.0059** and **0.0025**. Computed two-sided power was **0.9999999914471074**.

In the actual trial, the before window had **235** defects in **40000** inspected, or **0.005875**; the after window had **77** in **40000**, or **0.001925**. The absolute reduction was **0.00395**, the relative reduction was **0.672340425531915**, and the pooled two-proportion z statistic was **8.962482483814625** with p-value **3.1744942874845076e-19**. The confidence interval for the before-minus-after difference was **0.003086626479392266** to **0.004813373520607734**. The trial therefore provides strong evidence that the change reduced defects.

## Is the level reached enough, and is it holding?

The subsequent run contained **147** defects in **80000** inspected, giving **0.0018375**. Its p chart center line was **0.0018375**, lower limit **0**, upper limit **0.0038689472884959383**, with **0** out-of-control lots. On these **20** lots, the new level is statistically stable.

Against the commitment of **0.0025**, the exact one-sided test p-value is **5.060125914974411e-05**, supporting that the current defect share is below the required maximum. The post-change binomial process Z is **2.9047896420453334** at average defect share **0.0018375**.

## Recommended next actions

- Treat the current level as meeting the commitment on the available evidence, while continuing per-lot p-chart monitoring.
- Recover and approve the missing change record: exact paste-thickness and reflow-peak settings, allowed operating ranges, owners, reaction plan, and change-control requirements.
- Lock the approved settings into standard work and verify them at lot release. Because the fitted interaction is significant, manage the two settings jointly rather than one at a time.
- Investigate any future p-chart signal under the reaction plan and continue periodic pooled comparison with the committed share.
- Do not claim the regression proves the settings caused the improvement until the exact intervention is documented and, if needed, confirmed through a controlled experiment.
