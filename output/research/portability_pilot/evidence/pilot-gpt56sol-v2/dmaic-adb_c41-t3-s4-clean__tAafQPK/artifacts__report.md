# Candidate-region association study: final status

## Executive conclusion

The discovery plate can support analysis after quality-control exclusions; it does **not** support a positive association conclusion. The adjusted discovery scan produced **0** variants meeting the corrected threshold. Accordingly, the independent replication release contained **0** nominated candidates and **0** replicated findings. No variant should be reported as associated with affection status.

## Plate and participant quality

The discovery matrix was assessed using the protocol-defined participant call-rate rule. **3** participants failed, a failure fraction of **0.0125**, versus the plate stop threshold of **0.1**. Plate re-genotyping was therefore not triggered. The retained cohort contains **237** participants: **119** affected and **118** unaffected.

The excluded participants are P085, P136, and P193. Their exclusion, rather than re-genotyping the whole plate, is the protocol-consistent change that allowed the analysis to proceed.

## Variant quality

After participant filtering, **11** variants failed at least one protocol criterion and **139** were retained. The failure accounting was **5** for call rate, **4** for minor-allele frequency, and **2** for control-only Hardy-Weinberg equilibrium.

The excluded variants were:

- Call rate: rs040024, rs040041, rs040044, rs040059, rs040134
- Minor-allele frequency: rs040066, rs040114, rs040124, rs040130
- Control-only Hardy-Weinberg equilibrium: rs040065, rs040128

## Can affected and unaffected participants be compared?

Yes, but only with ancestry-axis adjustment. The PCA score ranges overlap, so affected and unaffected participants are not separated into non-comparable ancestry cohorts. There was nevertheless evidence of overlapping structure on PC**5**: its case-control comparison gave p = **0.013370319722095542**. In accordance with the protocol, the association model therefore included the leading **5** PCs as covariates.

## Discovery association

The scan tested **139** retained variants with additive logistic models. The Bonferroni threshold was **0.00035971223021582735**, and genomic inflation was **0.8836108651022039**. All models converged; the nonconverged-model count was **0**.

The smallest p-value was **0.012118851514246501** for rs040143, with an estimated per-allele odds ratio of **1.986273688869261**. This p-value does not cross the corrected threshold, so rs040143 is not a discovery association and must not be promoted as a hit.

## Replication and reporting decision

The released replication batch contains the independent cohort but identifies **0** nominated discovery variants. Thus, there was no protocol-qualified candidate on which to evaluate replication p-value and direction. The replication count is **0**, and the study has no reportable association.

## Recommended next actions and control plan

1. Do not report a panel variant as associated with affection status.
2. Preserve the participant exclusions, variant exclusion list, PCA adjustment choice, corrected threshold, scripts, and machine-readable trace as the analysis audit trail.
3. Treat the smallest uncorrected signal as exploratory only; do not selectively replicate or present it as confirmed.
4. If the biological question remains important, pre-specify a better-powered independent study, repeat the same participant and variant QC gates, reassess ancestry before testing, and retain multiplicity correction and same-direction independent replication as release controls.
