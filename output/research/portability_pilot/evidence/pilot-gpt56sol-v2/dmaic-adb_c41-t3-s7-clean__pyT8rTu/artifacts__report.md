# Candidate-region association study: final status

## Executive conclusion

The discovery plate is technically usable: participant failure was below the protocol stop limit, and affected and unaffected participants remained comparable after quality control and ancestry-axis assessment. The discovery scan produced one Bonferroni-significant candidate, **rs070008**, but the independent cohort did **not** replicate it. Under the study protocol, no variant can therefore be reported as associated. The conclusion is not that the locus has been disproved; it is that this study has not met its pre-specified reporting standard.

## Quality control and plate disposition

The discovery matrix contained **240** participants and **150** panel variants. Participant QC used the required call-rate threshold of **0.95**. **3** participants failed—**P016, P077, and P139**—for a failure fraction of **0.0125**. This is below the plate re-genotyping limit of **0.1**, so the plate can carry the planned analysis. The retained cohort contains **237** participants: **118** affected and **119** unaffected.

Variant QC applied call rate **0.95**, minor-allele frequency **0.01**, and unaffected-participant Hardy–Weinberg p-value **0.000001**. It excluded **11** variants and retained **139**. The excluded variants are **rs070013, rs070023, rs070025, rs070047, rs070049, rs070069, rs070099, rs070114, rs070131, rs070133, and rs070148**; equivalently, every other panel variant was retained. Across the panel, **5** variants failed call rate, **4** failed minor-allele frequency, and **2** failed Hardy–Weinberg equilibrium.

## Cohort comparability

PCA was computed from the retained discovery genotypes after mean imputation and allele-frequency scaling. The affected and unaffected ranges overlapped on all **10** leading axes examined; the separation flag was false, and the leading-axis case-control test had p-value **0.8997177848018328**. No axis met the analysis selection rule for covariate entry. The retained affected and unaffected groups were therefore compared without ancestry-axis covariates.

The study protocol did not provide a more detailed axis-selection rule. A clarification request was made but no matching study fact was available, so the implemented rule was documented rather than represented as protocol language.

## Discovery association scan

An additive logistic association test was run for all **139** retained variants. The Bonferroni significance threshold was **0.00035971223021582735**, and genomic inflation was **0.9164672788396385**. Exactly **1** variant passed: **rs070008**, with discovery p-value **0.000011326253251000435**, odds ratio **2.395108051754563**, and positive log-odds coefficient **0.8734283454003436**.

## Independent replication and reporting decision

The replication batch nominated **1** discovery candidate. For **rs070008**, genotype was available for **119** replication participants, comprising **60** affected and **59** unaffected participants. Its replication effect was in the same positive direction, with odds ratio **1.1834997908318183**, but its p-value was **0.5443027906408363**, above the replication alpha of **0.05**. Consequently, **0** of **1** candidates replicated.

The protocol requires both replication p-value below **0.05** and the same direction. Direction agreed, but significance did not. **rs070008 must not be reported as an association, and there is no reportable panel association from this study.**

## What changed, what it achieved, and next actions

Quality filtering removed the low-call participants and variants that failed call rate, frequency, or control-equilibrium requirements. This allowed a valid discovery comparison on the retained cohort and reduced the tested panel to the variants that met protocol quality. Independent replication then prevented a discovery-only signal from becoming a study claim.

Investigators should now follow the protocol instruction to reconsider the discovery scan rather than promote **rs070008**. Recommended actions are to audit genotype cluster quality and allele coding for the candidate in both cohorts, verify phenotype and sample provenance, document the ancestry-axis rule prospectively, and perform any redesigned or expanded study in a new independent cohort. The present discovery threshold and replication rule should remain locked for this dataset; changing either after seeing the result would not rescue a confirmatory conclusion.
