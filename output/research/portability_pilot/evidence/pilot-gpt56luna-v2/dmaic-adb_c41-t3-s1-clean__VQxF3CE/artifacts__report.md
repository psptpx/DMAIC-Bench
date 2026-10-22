# Candidate-region case-control study report

## Executive conclusion

The plate passes participant quality control, but the discovery cohort cannot carry a valid affected-versus-unaffected association conclusion under the study protocol. The leading genotype axis separates the two affection groups, so the protocol's rule for separate ancestries stops the comparison. No discovery association is reportable, and the replication step cannot support a report because the steward supplied no nominated candidates.

## What was computed

- The discovery batch contained 240 participants and 150 panel variants. Two participants failed the participant call-rate rule: P039, P197. The observed sample failure fraction was 0.008333333333333333; the protocol limit was 0.1. The plate therefore passed and does not require re-genotyping under that rule.
- The two failed participants were excluded before variant QC, leaving 238 participants. Variant QC retained 139 variants and failed 11. The failed variant identifiers were: rs010047, rs010057, rs010072, rs010088, rs010092, rs010101, rs010118, rs010128, rs010133, rs010141, rs010149. The retained cohort's minimum participant call rate was 0.9533333333333334, and the Bonferroni threshold over the retained set was 0.00035971223021582735.
- The leading genotype axis differed between affected and unaffected participants with statistic -55.336171713858846 and pValue 4.280198111581079e-133. This is the protocol-defined separate-ancestry situation, not an overlapping structure suitable for adding axes as covariates.
- The exploratory adjusted scan produced 0 threshold-crossing variants at the computed threshold, but that scan is not a valid reportable association analysis because the cohort comparability precondition failed. It must not be treated as evidence of no association.
- The independent replication batch contained 120 participants, but its candidateVariants list was empty. Consequently, 0 candidates were tested and 0 replicated associations were computed. There is no replication data for a nominated discovery hit; the conclusion stops there for replication.

## Business interpretation

What passed was plate usability for participant and variant QC. What prevents a conclusion is cohort design: affection status is aligned with ancestry structure. The failed participants and failed variants were removed as specified, but that QC change did not solve the comparability problem. The empty replication nomination is a consequence of having no defensible discovery hit to send forward, not evidence that replication was negative.

## Recommended next action and control

Do not report a variant association from this release. Rebuild the discovery comparison with ancestry-balanced affected and unaffected sampling, or obtain an independently justified design that provides overlapping ancestries; then rerun the protocol's stratification check before testing variants. Preserve the participant and variant exclusion lists, the QC thresholds, the ancestry diagnostic, and the candidate nomination log as the hold points for the next analysis. Only nominate variants after a valid discovery comparison, and only report them after an independent replication shows the protocol's required same-direction significance.
