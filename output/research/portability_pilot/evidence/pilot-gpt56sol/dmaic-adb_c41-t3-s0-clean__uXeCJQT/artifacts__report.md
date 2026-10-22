# Candidate-region association study status

## Executive conclusion

The plate can carry an analysis conclusion. Participant QC excluded **5** participants, a failed fraction of **0.020833333333333332**, which is below the protocol stop boundary of **0.1**. The analysis cohort therefore contains **235** participants: **117** affected and **118** unaffected.

After variant QC, **138** of **150** panel variants were tested. The ancestry check did not show affected/unaffected separation on the leading axis, so the groups can be compared on this cohort without ancestry-axis adjustment. The association analysis found **1** protocol-significant variant: **rs000008**.

## What was retained and removed

Participants retained are all participant IDs in the released genotype batch except: **P011, P059, P069, P224, P225**. Those **5** participants had call rate below **0.95**. The lowest observed participant call rate was **0.94**. Because the failure fraction did not exceed **0.1**, the protocol does not require re-genotyping before analysis.

Variants retained are all panel variant IDs except: **rs000031, rs000049, rs000060, rs000078, rs000086, rs000093, rs000114, rs000126, rs000135, rs000138, rs000142, rs000148**. In total, **12** variants failed QC: **5** for call rate, **4** for minor-allele frequency, and **3** for exact Hardy-Weinberg equilibrium among unaffected participants. The failed sets were:

- Call rate: rs000060, rs000078, rs000086, rs000093, rs000142
- Minor-allele frequency: rs000049, rs000126, rs000138, rs000148
- Unaffected-participant Hardy-Weinberg equilibrium: rs000031, rs000114, rs000135

The retained variants had minimum call rate **0.9702127659574468**, minimum minor-allele frequency **0.09829059829059829**, and minimum unaffected-participant Hardy-Weinberg p-value **0.015987421129153138**.

## Cohort comparability

PCA used mean-imputed, standardized genotypes after participant and variant QC. A logistic likelihood-ratio test of affection status against PC1 gave p = **0.30395785951012233** and statistic **1.0567488951348878**. The affected and unaffected PC1 ranges had an overlap fraction of **0.940285438451622**. PC1 explained **0.021140451630408785** of standardized genotype variance.

These results do not indicate separate ancestries by affection status. The protocol branch taken was therefore an unadjusted additive trend analysis. This conclusion is limited to structure detectable from this candidate-region panel; genome-wide ancestry markers were not released.

## Association result

The additive logistic likelihood-ratio analysis tested **138** retained variants. The computed Bonferroni threshold was **0.00036231884057971015**, based on family-wise alpha **0.05**. **rs000008** had p = **4.63980637645063e-07**, likelihood-ratio statistic **25.408038791885303**, and estimated per-allele odds ratio **2.667354602530193**. It therefore crossed the prespecified threshold. No other retained variant crossed it. Genomic inflation lambda was **0.8271897358417436**.

This is evidence of association, not proof of causality. Effect direction and size should be treated as discovery estimates from the same cohort used for testing.

## Action and control plan

Advance **rs000008** to independent replication and technical genotype confirmation. Preserve the participant and variant exclusion lists above, the exact QC thresholds, the control-only exact-HWE calculation, the PCA implementation, and the Bonferroni denominator with the frozen analysis artifacts. Do not reintroduce excluded records in downstream interpretation. Replication should predefine the same allele coding and additive model, verify population comparability with broader ancestry markers where available, and report both the prespecified significance decision and effect estimate.

## Reproducibility note

All study facts came from the steward's protocol and genotype batches. No provision turn or outside intervention was used. The initial PCA implementation failed because its requested software dependency was unavailable; it produced no quantitative result. The successful rerun used NumPy singular-value decomposition, and that failure is retained in the machine-readable trace.
