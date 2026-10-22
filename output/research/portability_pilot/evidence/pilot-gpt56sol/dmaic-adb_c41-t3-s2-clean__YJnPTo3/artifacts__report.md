# Candidate-region association study report

## Executive conclusion

The plate can carry a conclusion. Participant QC excluded 3 participants and retained 237; the sample-failure fraction was 0.0125, below the protocol stop limit of 0.1. After variant QC, 139 variants were retained and 11 were excluded.

Affected and unaffected participants are comparable on this retained cohort only after ancestry adjustment. Their leading-axis score ranges overlap, so they are not completely separated, but PC1 differs by affection status (p = 2.0003440952185783e-14). The association models therefore included PC1.

The adjusted analysis found 1 protocol-significant variant: **rs020008** (p = 7.306359224212055e-05, odds ratio per coded allele = 2.3902781391350323). This is below the Bonferroni cutoff of 0.00035971223021582735 across 139 retained variants. Genomic inflation was 0.9846129316919627 and there were 0 model failures.

## What was retained and changed

### Participants

The source cohort contained 240 participants: 120 affected and 120 unaffected. The participant call-rate threshold was 0.95. The following participants each had call rate 0.9466666666666667 and were excluded: **P031, P153, P236**. All other participants were retained, leaving 119 affected and 118 unaffected participants.

### Variants

The source panel contained 150 variants. QC required call rate at least 0.95, minor-allele frequency at least 0.01, and exact Hardy-Weinberg p-value among unaffected participants at least 1e-06.

All variants were retained except: **rs020016, rs020022, rs020023, rs020042, rs020048, rs020074, rs020096, rs020102, rs020107, rs020115, rs020143**. In criterion-level counts, 5 failed call rate, 4 failed minor-allele frequency, and 2 failed unaffected-participant Hardy-Weinberg equilibrium.

Failure-reason lists:

- Call rate: rs020016, rs020023, rs020042, rs020107, rs020115
- Minor-allele frequency: rs020022, rs020048, rs020096, rs020102
- Hardy-Weinberg equilibrium: rs020074, rs020143

## Cohort comparability

PCA was computed after participant and variant QC, with missing genotypes mean-imputed and retained variants standardized. PC1 explained 0.08351091648506719 of genotype variance. The affected PC1 range was -5.0087056584208005 to 4.6049931365269385; the unaffected range was -6.402423432271143 to 4.886355215018731. These ranges overlap, so the protocol permits comparison, but the PC1 test statistic of 8.166605766612712 and p-value of 2.0003440952185783e-14 show that unadjusted testing would be inappropriate.

## Association result

An additive logistic regression was fit separately for every retained variant, using affection status as the outcome and genotype dosage plus PC1 as predictors. For rs020008, the analysis used 230 participants; the dosage coefficient was 0.8714097353793603 with standard error 0.2197154856993242, giving an odds ratio of 2.3902781391350323 and p-value 7.306359224212055e-05. It is the only result below the protocol cutoff of 0.00035971223021582735.

## Recommended next actions and control plan

- Treat rs020008 as the panel's association finding, not as a causal claim. Replicate it in an independent, ancestry-compatible cohort and review local linkage disequilibrium and functional evidence.
- Do not return the excluded participants or variants to this analysis unless new genotype data pass the same prespecified QC rules. Re-genotyping the excluded participants is appropriate if their inclusion is operationally important.
- Preserve the participant exclusions, variant exclusions, PCA transformation, PC1 adjustment, and Bonferroni rule in the reproducible pipeline. On any refreshed dataset, rerun participant QC first and stop if the plate-level rule fails.
- Review genotype cluster quality for rs020008 and confirm allele coding before interpretation, because its estimated effect is per coded allele.
