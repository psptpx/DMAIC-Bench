# Candidate-region case-control study report

## Executive conclusion

The plate can carry an analysis: the participant failure fraction was **0.0**, which did not exceed the protocol maximum of **0.1**. All **240** participants were retained and **0** were excluded.

After protocol variant QC, **140** variants were retained and **10** were excluded. A genotype-based ancestry check found that affected and unaffected participants were **not separated**; PC1 was not associated with affection status (p = **0.8985276605213535**). The groups are therefore comparable on this cohort, and the protocol did not require ancestry-axis covariates for the association tests.

Testing the retained variants with an additive trend test found **0** associations at the Bonferroni threshold of **0.0003571428571428571**. The present panel therefore supplies no protocol-significant evidence that a retained variant is associated with affection status.

## Protocol and quality disposition

### Participants and plate

Participant call rate had to be at least **0.95**. The lowest observed participant call rate was **0.9533333333333334**, and the highest was **1.0**. Consequently, every participant identifier in the steward's participant list—P001 through P240—is retained; the excluded-participant list is empty. Because the participant failure fraction was **0.0**, re-genotyping is not triggered by the plate rule.

### Variants

Variant retention required call rate at least **0.95**, minor-allele frequency at least **0.01**, and exact Hardy–Weinberg p-value among unaffected participants at least **0.000001**. Of the excluded variants, **5** failed call rate, **3** failed minor-allele frequency, and **2** failed unaffected-participant HWE. These failure categories did not overlap in this dataset.

Excluded variants: **rs040038, rs040054, rs040057, rs040072, rs040104, rs040106, rs040110, rs040112, rs040113, rs040125**.

Every other variant in the steward's rs040001-through-rs040150 panel is retained. Thus the retained set is the original ordered panel after removing exactly the excluded variants listed above.

## Cohort comparability

PCA used the retained genotype matrix with missing calls mean-imputed and variants standardized by diploid-binomial variance. The assessment included **120** affected and **120** unaffected participants. PC1 explained **0.02098564776332856** of standardized genotype variance. Its affected range was **-3.508826971760219** to **4.924733760106628**, while its unaffected range was **-4.523926025774327** to **4.191099686615217**. The ranges overlap, and the PC1 logistic test gave p = **0.8985276605213535**. This satisfies the protocol precondition to compare the groups; no detected structure required PC adjustment.

## Association analysis

The analysis tested **140** retained variants using complete called genotypes at each variant and an additive allele-dosage trend score test. Bonferroni correction applied familywise alpha **0.05** over the retained tests, giving the threshold **0.0003571428571428571**. The smallest observed p-value was **0.02061286706994735** at **rs040084**, based on **237** called participants; it did not cross the threshold. Genomic inflation lambda was **0.8941492183950938**. No variant is declared associated.

## What changed and what it achieved

The analysis removed the **10** protocol-failing variants before cohort assessment and association testing, while retaining every participant. This prevented low-call-rate, uninformative low-frequency, and control-HWE-failing variants from entering inference. The ancestry check then established that the retained affected and unaffected participants could be compared. Multiplicity correction controlled the panel-level decision, and no tested signal survived it.

## Recommended next actions and control plan

1. Do not present any panel variant as associated on this dataset.
2. Preserve the participant call-rate table, per-variant QC table, PCA scores, and complete association table generated in this run as the auditable analysis record.
3. Keep the same pre-specified sequence for any rerun: participant QC and plate decision, variant QC using unaffected participants for HWE, ancestry assessment, then multiplicity-corrected association testing.
4. If investigators need greater sensitivity, pre-plan an independently powered expansion or replication cohort rather than relaxing the current QC or significance rules after seeing these results.
5. Re-evaluate ancestry structure and recompute the Bonferroni denominator whenever participants or variants change; do not carry this run's threshold into a changed analysis set.
