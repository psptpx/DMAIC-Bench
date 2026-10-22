# Appearance Defect Reduction — Project Status

## Bottom line

The pass/fail measurement system is adequate to guide this project, provided its known repeatability weakness is controlled. The baseline was stable across lots but clearly above charter, so it required a system change rather than lot-by-lot firefighting. Machine 2 and loose ends were the strongest improvement targets. The monitoring record after the change is stable and meets the charter, although the short change trial by itself did not statistically prove the reduction and the available records do not identify what was physically changed.

## Can the pass/fail judgement be relied on?

The attribute study used 3 appraisers, 20 retained units, 2 repeats per appraiser, and 120 total judgements. The lowest appraiser accuracy was 90.0%; accuracies were 92.5%, 97.5%, and 90.0%. The lowest kappa was 0.7938144330; the individual kappas were 0.8378378378, 0.9459459459, and 0.7938144330. Thus, the judgements can be used for project decisions after accounting for chance agreement.

Repeatability is the weak point. The lowest repeat agreement was 80.0%; the appraisers' repeat agreements were 85.0%, 95.0%, and 80.0%. Future checks should separately report false passes and false fails. Until repeat agreement improves, retain the answer-key units, refresh appraiser calibration, and audit a defined sample from production rather than treating every visual verdict as perfect.

## Baseline: steady, but not capable

The 25-lot baseline contained 334 defectives in 125,000 inspections, or 2,672 DPMO. The charter allows 1,500 DPMO; at that rate the same inspections would correspond to 187.5 defectives. The observed excess is statistically clear (z = 10.7068804639, p = 4.7246199836 × 10^-27). Baseline binomial process Z was 2.7855317876.

The rate nevertheless held steady. Lot DPMO ranged from 1,800 through 3,800. The p chart had 0 out-of-control points; its equivalent limits were 481.8518888440 and 4,862.1481111560 DPMO. A homogeneity test also found no evidence of differing lot shares (chi-square = 14.8420531757, df = 24, p = 0.9252952261). Therefore, the gap was a common-cause process-level capability problem, not a pattern of isolated lots.

## What stands out as the cause

Machine 2 is a clear special cause in the common-window tally. It produced 26 defectives among 4,000 units (6,500 DPMO), while machines 1, 3, and 4 were at 1,500, 1,500, and 1,000 DPMO. Pooling those three machines gives 16 defectives in 12,000 units, or 1,333.3333333333 DPMO. Machine association is significant (chi-square = 30.8428672885, df = 3, p = 9.1733129599 × 10^-7), and machine 2 versus the others is also decisive (z = 5.5306627644, p = 3.1902312547 × 10^-8; excess = 5,166.6666666667 DPMO).

Loose end dominates the charter reject tally: 142 of 240 rejects, or 59.1666666667%. It also has the highest FMEA RPN, 294, compared with 252 for seam split, 210 for stain, 72 for soft spot, and 40 for off-weight. Thus, machine 2 and loose-end prevention are separately well-evidenced priorities. The available data do not cross-tabulate reject category by machine, so they do not prove that loose ends originate on machine 2; seam split remains the secondary risk even though its reject count is lower.

## What was changed, and what it achieved

The available process fact does not describe the physical change; a process-fact query found no matching recorded topic. This is a traceability gap, not evidence that the change was ineffective. The report therefore identifies the machine change only as “the change,” and the operating standard cannot be locked from these records alone.

In the paired trial, defectives fell from 18 in 4,000 before the change to 13 in 4,000 after it. That is an observed movement from 4,500 to 3,250 DPMO: an absolute reduction of 1,250 DPMO and a relative reduction of 27.7777777778%. However, the trial alone does not establish a statistically reliable effect (z = -0.8997715095, p = 0.3682418591), and the immediately post-change machine remained above charter (z = 2.8598837510, p = 0.0021189816).

The longer monitoring record gives stronger evidence of where the line now stands: 110 defectives in 89,300 inspections across 20 periods, or 1,231.8029115342 DPMO. The aggregate is statistically below 1,500 DPMO (one-sided z = -2.0709047497, p = 0.0191838491), and its 95% upper bound is 1,424.8683310274 DPMO. The variable-subgroup p chart has 0 out-of-control points; individual period DPMO ranges from 400 through 1896.5517241379. Its binomial process Z is 3.0277760558.

## What should be done next

1. **Close the change-control gap immediately.** Record the actual machine setting, release, owner, and effective date. The physical change cannot be named or standardized from the released data, and the conclusion stops at “a change was made.”
2. **Hold the gain with a p chart.** Continue the variable-subgroup chart using the post-change center line of 0.0012318029115. Investigate any out-of-control signal; do not react to every ordinary lot-to-lot fluctuation.
3. **Maintain charter governance.** The current record has 1,231.8029115342 DPMO and a 95% upper bound of 1,424.8683310274 DPMO, so it meets the 1,500-DPMO commitment but with limited margin. Review capability at a defined regular interval and after any process release.
4. **Control the remaining priority risks.** Keep loose end (RPN 294) as the primary mechanical/process focus, with seam split (RPN 252) second. Capture reject category and machine together going forward so causes can be localized rather than inferred.
5. **Strengthen visual judgement.** Re-run the attribute study after appraiser retraining and boundary-sample refresh. Set minimum requirements for both accuracy and repeat agreement; the current minimum values are 90.0% accuracy and 80.0% repeat agreement. Track false-pass and false-fail directions separately.
6. **Audit implementation and sustain.** Verify the undocumented change on the floor, preserve the calibration record, and require a defined sample and escalation rule before making future process decisions.
