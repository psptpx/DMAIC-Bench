# Candidate-region case-control study report

## Executive conclusion

The discovery plate can carry an analysis: participant QC failed **3** participants, a failure fraction of **0.0125**, below the protocol re-genotyping limit of **0.1**. After exclusions, **237** participants and **139** variants remained.

The retained cohort shows ancestry-related structure on PC1 (case/control comparison **p = 4.4356006605713844e-16**), but the PC1 score ranges overlap. Affected and unaffected participants are therefore comparable only with PC1 adjustment, not by an unadjusted scan. The PC1-adjusted additive logistic scan tested **139** variants; **139** models converged and **0** passed the Bonferroni threshold of **0.00035971223021582735**. Accordingly, **0** variants were nominated and **0** replicated. No variant association should be reported.

## Protocol and QC

The participant call-rate cutoff was **0.95**. Excluded participants: P127, P142, P195. All other participants were retained.

Variant rules were call rate at least **0.95**, minor-allele frequency at least **0.01**, and exact Hardy-Weinberg p-value among unaffected participants at least **1e-06**. Of the excluded variants, **5** failed call rate, **4** failed frequency, and **2** failed control HWE. Excluded variants: rs050014, rs050017, rs050019, rs050052, rs050071, rs050082, rs050091, rs050092, rs050096, rs050108, rs050121.

Retained variants: rs050001, rs050002, rs050003, rs050004, rs050005, rs050006, rs050007, rs050008, rs050009, rs050010, rs050011, rs050012, rs050013, rs050015, rs050016, rs050018, rs050020, rs050021, rs050022, rs050023, rs050024, rs050025, rs050026, rs050027, rs050028, rs050029, rs050030, rs050031, rs050032, rs050033, rs050034, rs050035, rs050036, rs050037, rs050038, rs050039, rs050040, rs050041, rs050042, rs050043, rs050044, rs050045, rs050046, rs050047, rs050048, rs050049, rs050050, rs050051, rs050053, rs050054, rs050055, rs050056, rs050057, rs050058, rs050059, rs050060, rs050061, rs050062, rs050063, rs050064, rs050065, rs050066, rs050067, rs050068, rs050069, rs050070, rs050072, rs050073, rs050074, rs050075, rs050076, rs050077, rs050078, rs050079, rs050080, rs050081, rs050083, rs050084, rs050085, rs050086, rs050087, rs050088, rs050089, rs050090, rs050093, rs050094, rs050095, rs050097, rs050098, rs050099, rs050100, rs050101, rs050102, rs050103, rs050104, rs050105, rs050106, rs050107, rs050109, rs050110, rs050111, rs050112, rs050113, rs050114, rs050115, rs050116, rs050117, rs050118, rs050119, rs050120, rs050122, rs050123, rs050124, rs050125, rs050126, rs050127, rs050128, rs050129, rs050130, rs050131, rs050132, rs050133, rs050134, rs050135, rs050136, rs050137, rs050138, rs050139, rs050140, rs050141, rs050142, rs050143, rs050144, rs050145, rs050146, rs050147, rs050148, rs050149, rs050150.

## Cohort comparability

PCA used the participant- and variant-QC-retained matrix after mean imputation and dosage standardization. PC1 explained a variance fraction of **0.08143503530188842** and its affected/unaffected Welch statistic was **-8.74314141983081**. The groups' observed PC1 ranges overlapped, so they were not treated as separate ancestries. Following protocol, PC1 entered every discovery model as a covariate.

## Discovery and replication

The adjusted scan's genomic inflation factor was **1.1762264979203334**. Since no test crossed the corrected threshold, there was no discovery effect to nominate. The independent replication batch was available, but its candidate list was empty; the replication criterion of **p < 0.05** in the same direction therefore could not confirm any candidate. This is a valid null discovery outcome, not a missing-data substitution.

## Recommended next actions and control

Do not report a panel association from this study. Preserve the participant exclusions, variant exclusions, PCA construction, PC1 adjustment, and corrected threshold in the locked analysis record. Before any new claim, pre-specify whether a larger independent discovery cohort or a redesigned, ancestry-balanced sample will be collected; rerun the same QC and structure gates; and send only threshold-passing discovery variants to independent replication. Continue monitoring participant failure fraction against the plate gate and retain the exact control-HWE check in future runs.
