# Candidate-region association study report

## Executive conclusion

The plate can support an association conclusion. Sample QC failed **3** of **240** participants, a failure fraction of **0.0125**, which does not exceed the protocol's plate stop threshold of **0.1**. After participant QC, **237** participants remained. Variant QC retained **139** of **150** variants and failed **11**.

The retained cohort contains ancestry structure related to affection status: the PC1 comparison gave **p = 1.800877623368265e-14**. The affected and unaffected PC1 ranges nevertheless overlap, so they are not separate ancestry cohorts and can be compared only with ancestry adjustment. A PC1-adjusted additive logistic regression identified **1** Bonferroni-significant variant: **rs020008**, with **p = 7.55531482395406e-05** and an estimated per-allele odds ratio of **2.385798901666481**. The computed Bonferroni threshold was **0.00035971223021582735**. Thus, this plate supports rs020008 as the study's association finding, subject to independent confirmation.

## Participant quality control and plate disposition

The input contained **120** affected and **120** unaffected participants. The participant call-rate threshold was **0.95**. The following participants failed and were removed:

- **P031** — call rate **0.9466666666666667**
- **P153** — call rate **0.9466666666666667**
- **P236** — call rate **0.9466666666666667**

All other participants were retained. The resulting analysis cohort contains **119** affected and **118** unaffected participants. Because the observed participant failure fraction was below the plate stop threshold, re-genotyping the whole plate is not required before analysis.

## Variant quality control

The protocol filters were applied after participant QC: variant call rate at least **0.95**, minor-allele frequency at least **0.01**, and unaffected-participant Hardy-Weinberg p-value at least **0.000001**.

The **11** excluded variants were:

- Call-rate failures (**5**): **rs020016, rs020023, rs020042, rs020107, rs020115**
- Minor-allele-frequency failures (**4**): **rs020022, rs020048, rs020096, rs020102**
- Unaffected-participant HWE failures (**2**): **rs020074, rs020143**

Every panel variant not listed above was retained, for **139** retained variants in total.

## Cohort comparability

PCA was computed from the QC-retained genotype matrix. PC1 explained **0.09352354350804105** of genotype variance. Its association with affection status was strong, while the affected and unaffected PC1 intervals overlapped. Therefore, an unadjusted comparison would not meet the protocol, but a comparison including the leading ancestry axis as a covariate does. The association model consequently included **1** ancestry covariate.

## Association analysis

All **139** retained variants were tested using additive genotype dosage in logistic regression with PC1 adjustment. For rs020008, **230** participants had complete genotype data in the variant-specific model. Its genotype coefficient was **0.8695340375028231**, standard error **0.21968555244786325**, and Wald statistic **3.9580847616694537**. Its p-value was below the retained-variant Bonferroni threshold, and no other variant passed that threshold. Genomic-control lambda was **0.976823439086659**, providing no indication of residual test-statistic inflation in this analysis.

## What changed and what it achieved

Quality control removed the participants and variants that did not satisfy the prereleased rules. Ancestry assessment then changed the planned comparison from an unadjusted test to a PC1-adjusted test. These controls left a protocol-compliant cohort and reduced the panel to the variants eligible for inference. The resulting multiplicity-controlled analysis isolated rs020008 as the sole association signal.

## Recommended next actions and hold plan

- Independently verify the rs020008 genotype calls, especially missing calls, using an orthogonal assay before treating the signal as confirmed.
- Replicate the rs020008 association in an independent cohort with ancestry measured and adjusted in the same manner.
- Preserve the participant exclusion list, variant exclusion list, PCA inputs, and fitted-model outputs as the locked analysis record.
- For future batches, rerun the same participant, variant, ancestry, and Bonferroni gates without changing thresholds after seeing outcomes.
- Do not reinterpret excluded variants as negative association results: they were not eligible for testing under the protocol.
