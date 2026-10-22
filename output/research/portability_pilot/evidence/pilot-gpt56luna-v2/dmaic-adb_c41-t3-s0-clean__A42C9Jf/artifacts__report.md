# Case-control candidate-region study report

## Executive conclusion

The discovery plate can carry an analysis conclusion: the participant failure fraction was 0.0125, below the protocol re-genotyping trigger of 0.1. After QC, the analysis retained 237 participants and 138 variants. The affected and unaffected groups showed ancestry structure, so the fifth leading ancestry axis was included as a covariate rather than comparing the groups without adjustment.

The adjusted discovery scan found 0 variants at the Bonferroni threshold of 0.00036231884057971015. Thus there is no discovery-significant variant from the scan as computed here. The steward nevertheless supplied 1 nominated candidate, rs000008, for the independent replication step. It replicated with p=0.00001087584102880892, odds ratio 3.2240859980419136, and the same positive direction. Under the stated reporting rule, rs000008 is supported for reporting by the supplied replication analysis, although the absence of a Bonferroni-significant adjusted discovery result should be explicitly disclosed and the discovery/nomination provenance reviewed.

## What was retained and excluded

- The batch contained 240 participants and 150 panel variants.
- Three participants failed the participant call-rate rule: P053, P129, and P160 (zero-based indices 52, 128, and 159). The retained participant count was 237.
- The 12 excluded variants were rs000003, rs000025, rs000061, rs000079, rs000086, rs000091, rs000107, rs000108, rs000130, rs000138, rs000149, and rs000150. The retained variant count was 138.
- Variant retention used call rate at least 0.95, MAF at least 0.01, and unaffected-control HWE p at least 0.000001. Among retained variants, the minimum observed MAF was 0.0811965811965812 and the minimum observed HWE p-value was 0.0022224488325383795.

## Cohort comparability

The fifth leading ancestry axis separated the affection groups at p=0.04984163325445762. The groups were therefore not treated as unconditionally comparable. The adjusted association model included that axis as a covariate. The first-axis p-value was 0.7718589642522526; the relevant structure decision was driven by the fifth axis.

## Association and replication

The adjusted scan tested 138 retained variants. Its Bonferroni threshold was 0.00036231884057971015, and 0 variants passed it. The replication batch nominated rs000008. Its replication candidate call rate was 0.9916666666666667, with 1 missing candidate call among the 120-person replication cohort. The replication p-value was 0.00001087584102880892, below the protocol replication alpha of 0.05, and the odds ratio was 3.2240859980419136 in the same positive direction as the discovery direction. Therefore 1 of 1 nominated candidates replicated by the stated rule.

## Cause, change, achieved result, and control

The main data-quality issue was missing genotype calls: 3 participants failed participant QC and 12 variants failed variant QC. The plate-level failure fraction did not trigger re-genotyping. The main design issue was ancestry structure, addressed by adding the fifth leading axis as a covariate. This produced a QC-filtered, structure-adjusted discovery analysis and a concordant replication result for the nominated candidate.

Before publication, investigators should reconcile why rs000008 was nominated despite 0 Bonferroni-significant adjusted discovery variants, rerun the discovery model with an independently validated ancestry/covariate specification, and preserve the exact QC exclusions, model code, candidate nomination rule, and replication output as the analysis lock. The steward rejected all attempted declaration keys as invalid because this project exposed no declaration keys; those failed declarations are not evidence of a biological or QC verdict.
