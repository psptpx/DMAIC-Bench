# Candidate-region study status

## Executive conclusion

The plate can carry an analysis: **5 of 240 participants failed sample QC**, giving a failure fraction of **0.020833333333333332**, below the protocol maximum of **0.1**. After all protocol QC, the analysis retained **235 participants** and **138 of 150 variants**.

Affected and unaffected participants **can be compared on this retained cohort**. Their ancestry-PC score ranges overlap; they are not separate ancestry groups. Because a leading axis nevertheless differed by affection status, association testing was adjusted for the first **10** principal components.

The adjusted analysis found **1** associated variant: **rs000008**. Its additive-dosage odds ratio was **2.6498900727615413**, with Wald p-value **1.387897681959808e-05**, below the Bonferroni threshold of **0.00036231884057971015**. This is a panel-level statistical association, not yet proof of causality or external replication.

## Participant QC and plate disposition

The participant call-rate requirement was **0.95**. The excluded participants are:

- **P011**
- **P059**
- **P069**
- **P224**
- **P225**

The retained cohort contains **117 affected** and **118 unaffected** participants. Because the failed-sample fraction did not exceed the re-genotyping trigger, the protocol does not require this plate to be re-genotyped before analysis.

## Variant QC

Variant QC excluded **12** variants and retained **138**. The exclusions were:

- HWE failure among unaffected participants: **rs000031, rs000114, rs000135**
- Low minor-allele frequency: **rs000049, rs000126, rs000138, rs000148**
- Low call rate: **rs000060, rs000078, rs000086, rs000093, rs000142**

Thus, the retained set is every panel variant except those listed above. The failure categories account for **3** HWE failures, **4** frequency failures, and **5** call-rate failures.

## Cohort comparability

PCA used the QC-retained genotype matrix with missing dosages mean-imputed and variants standardized by binomial genotype variance. On PC1, the affected and unaffected ranges overlapped, and the phenotype comparison had p-value **0.260362248140186**; the separate-ancestry condition was therefore false. PC4 showed overlapping structure associated with phenotype, with p-value **0.003001951972322571**. Following the protocol, leading axes were included as covariates rather than treating ancestry as absent.

## Association analysis

An additive logistic model was fitted for each of the **138** retained variants, with the leading ancestry axes as covariates. All models completed; the genomic inflation factor was **0.7990958633797803**. The family-wise significance level was **0.05**.

For **rs000008**, the fitted dosage coefficient was **0.9745181571609529**, its standard error was **0.2242453711591018**, and its Wald statistic was **4.345767103792451**. The model used **231** called participants for this variant and converged. No other retained variant crossed the corrected threshold.

## What changed and what it achieved

QC removed the participants and variants that did not meet the released rules. Ancestry assessment then changed the planned comparison from an unadjusted test to an adjusted one because overlapping structure was observed. This produced a valid within-cohort comparison under the protocol and isolated rs000008 as the sole panel-level signal while avoiding claims from the failed-QC records.

## Recommended next actions and control plan

1. Independently replicate **rs000008** in a comparable cohort and confirm the genotype cluster/call quality manually before interpreting biology.
2. Re-run the analysis with the same frozen participant exclusions, variant exclusions, PCA preprocessing, ancestry covariates, additive model, and multiplicity rule; the scripts and complete result artifacts in `/workspace` provide the audit trail.
3. Preserve blinded QC review before phenotype association in future batches. Monitor participant failure fraction against **0.1**, and stop for re-genotyping if it is exceeded.
4. Treat the observed odds ratio as a study estimate, not a causal effect. Follow replication with fine-mapping or functional work only if the signal persists.

## Reproducibility note

The first PCA run completed its calculations but failed while serializing a NumPy boolean; it produced no accepted result artifact. The serialization issue was corrected and the unchanged PCA was rerun successfully. This failed attempt is retained in the trace rather than hidden.
