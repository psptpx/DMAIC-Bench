# Metabolic-trait candidate-panel study report

## Executive conclusion

The discovery plate can carry a QC-qualified analysis: the participant failure fraction was 0.0125, below the protocol maximum of 0.1, so the plate did not require re-genotyping. The affected and unaffected groups were comparable on the computed leading genotype axes: the separation decision was False and the PC1 comparison p-value was 0.231006994556052.

The discovery scan nominated rs070008. Its association p-value was 3.2746049160304157e-06, below the Bonferroni threshold of 0.00035971223021582735. It is not reportable, however: replication p-value was 0.5374794553122435, above the replication threshold of 0.05. Although the replication direction was the same as discovery, the replication criterion requires both p < 0.05 and matching direction. The reported replicated-hit count is 0 of 1 candidate.

## What was retained

The discovery batch contained 240 participants and 150 panel variants. Participant QC failed 3 participants, leaving 237 retained participants. Variant QC retained 139 variants and failed 11. The implemented filters were participant call rate at least 0.95, variant call rate at least 0.95, minor-allele frequency at least 0.01, and unaffected-participant HWE p-value at least 0.000001.

The retained discovery groups were 120 affected and 120 unaffected participants. No ancestry separation was detected across the examined leading axes, so no ancestry covariate was required by the computed structure result.

## Association and replication

The discovery analysis produced 1 Bonferroni-significant variant. The nominated variant was rs070008, with discovery test statistic 21.648532204861315 and p-value 3.2746049160304157e-06.

The independent replication batch contained 120 participants: 60 affected and 60 unaffected. No replication participants failed the participant call-rate rule; the candidate variant call rate was 0.9916666666666667. The replication test statistic was 0.38023133588027946 and p-value 0.5374794553122435. Because the p-value did not pass 0.05, the discovery result must not be reported as an association.

## Cause, change, and control

The immediate cause of the stop is replication failure, not discovery QC: the plate passed its participant gate, the retained variants passed the stated QC filters, and the cohort comparison was not blocked by detected structure. The change made during analysis was to replace an unavailable scikit-learn PCA implementation with a NumPy SVD implementation; the structure computation then completed successfully. The initial failed software attempt is recorded in the trace and is not treated as a study-data failure.

Investigators should reconsider the discovery scan as required by the protocol, avoid reporting rs070008 as a confirmed association, and perform any further analysis only under the same predeclared QC, structure, multiple-testing, and replication rules. Future releases should preserve the saved batch files, analysis script, trace, and report so that each retained participant, retained variant, nominated hit, and replication decision can be audited.
