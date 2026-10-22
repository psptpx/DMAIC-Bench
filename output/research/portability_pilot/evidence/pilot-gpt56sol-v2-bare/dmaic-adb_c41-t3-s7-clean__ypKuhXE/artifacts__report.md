# Candidate-region association study: final report

## Executive conclusion

The discovery plate can carry an analytical conclusion. Participant QC failed **3** participants (**0.0125** of the plate), below the protocol's **0.10** re-genotyping trigger. Excluding those participants retained **237** people: **118** affected and **119** unaffected.

Variant QC retained **139** variants and removed **11**. The retained affected and unaffected groups can be compared on this cohort: PC1 did not show detected case-control separation (p = **0.232223**), and the association scan's genomic inflation factor was **0.917909**.

The discovery scan found **1** associated variant. **rs070008** had p = **5.87173e-06**, below the Bonferroni threshold of **0.000359712**, with additive odds ratio **2.39511**. However, the independent replication p-value was **0.543816**, which is not below **0.05**. Although its replication direction was also positive, direction alone is insufficient. Therefore **0** of **1** candidates replicated, and the protocol does **not** support reporting rs070008 as a replicated association.

## What was done

### Participant and plate QC

Participant call rate was computed over all **150** panel variants. The protocol required call rate at least **0.95**. **P016, P077, and P139** failed; all other discovery participants were retained. The minimum observed participant call rate was **0.94**. Since the observed failure fraction was below the plate trigger, wholesale plate re-genotyping is not required for this analysis.

### Variant QC

Variant QC was recomputed after participant exclusions. Retention required call rate at least **0.95**, MAF at least **0.01**, and exact HWE p at least **0.000001** among unaffected participants. The excluded variants were:

rs070013, rs070023, rs070025, rs070047, rs070049, rs070069, rs070099, rs070114, rs070131, rs070133, rs070148

All other panel variants were retained. **5** variants failed call rate, **4** failed MAF, and **2** failed HWE. No excluded variant failed multiple criteria in this dataset.

### Cohort comparability and discovery association

PCA used standardized retained genotypes with mean imputation for sporadic missing calls. A Welch case-control comparison of PC1 gave p = **0.232223**. With no detected separation at alpha **0.05**, the retained groups were compared using an additive allele-dose trend test. rs070008 used **231** nonmissing discovery observations and had trend statistic **20.5296**.

### Independent replication

The steward nominated rs070008 from discovery. Its replication analysis used **119** nonmissing observations: **60** affected and **59** unaffected. The replication trend statistic was **0.368514**, and the additive odds ratio was **1.1835**. The effect direction matched discovery, but its p-value exceeded the replication threshold. It therefore failed the protocol rule requiring both statistical significance and the same direction.

## Business recommendation and control

Do not present rs070008 as a replicated association and do not claim that the panel has produced a reportable association under the prespecified protocol. The defensible conclusion is that the plate passed QC, the cohorts were comparable under the computed PCA check, and rs070008 was a discovery signal that independent replication did not support.

Preserve the participant exclusions, variant exclusions, retained-variant denominator, scripts, and cohort-specific results with the analysis record. Before any renewed claim, verify genotype clustering and call quality for rs070008 and seek additional independent evidence using a prospectively specified analysis. Biological annotation or fine-mapping may be exploratory, but should not be framed as confirmation. Future cohorts should apply the same QC and replication criteria, and any altered model or threshold should be documented as a new analysis rather than replacing this result.
