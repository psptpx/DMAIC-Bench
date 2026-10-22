# Candidate-region association study: decision report

## Executive conclusion

The discovery plate can carry a conclusion. Participant QC removed **3** participants (0.0125 of the plate), leaving **237** participants: **118** affected and **119** unaffected. Variant QC retained **139** variants and excluded **11**.

Affected and unaffected participants are comparable on this retained cohort: they were not separated on the leading genotype axes. Overlapping structure was detected on PC9, so that axis was included as a covariate rather than ignoring structure.

The adjusted discovery scan found **1** discovery association. **rs070008** passed the computed Bonferroni cutoff but did not meet the independent replication p-value requirement. It is therefore not reportable under the protocol.

## What was done and what changed

### Participant and plate quality

The retained participants are all named discovery participants except P016, P077, P139; those participants failed call-rate QC. The computed failure fraction was **0.0125**, and the plate-pass result was **true**. Removing those participants retained **237** for downstream work. This avoids allowing low-call samples to drive either variant QC or association results.

### Variant quality

Across the retained cohort, **5** variants failed call rate, **4** failed minor-allele frequency, and **2** failed exact Hardy-Weinberg testing among unaffected participants. These categories produced **11** total exclusions and **139** retained variants. The excluded variants were rs070013, rs070023, rs070025, rs070047, rs070049, rs070069, rs070099, rs070114, rs070131, rs070133, rs070148. The retained variants are all named panel variants except those exclusions; the machine-readable complete retained list is preserved in the analysis artifact.

### Cohort comparability

PCA used the QC-retained genotype matrix. The first **10** axes were examined. No axis had disjoint affected/unaffected ranges, so the separation verdict was **false**. PC1 had case-control p = **0.23164020907154623**. PC9 showed overlapping structure with p = **0.029969887133867223** and range-overlap fraction **0.8886841060272633**; it was therefore carried into every discovery model. A first software implementation failed because an optional package was absent; the analysis was rerun successfully with local NumPy/SciPy code, with no substitution of uncomputed results.

### Discovery association

The multiplicity cutoff computed over **139** tested variants was **0.00035971223021582735**. The adjusted scan produced **1** significant variant and genomic inflation factor **0.840369544245204**. For rs070008, the model used **231** called participants, estimated odds ratio **2.279618941071796**, and gave p = **5.094420581075932e-05**. No other retained variant crossed the cutoff.

### Independent replication

The replication analysis tested **1** nominated candidate. For rs070008, **119** participants had called genotypes, comprising **60** affected and **59** unaffected participants. The replication odds ratio was **1.1834997123474893** and p = **0.5443029478701621**. Its direction matched discovery (**true**), but its p-value was not below the replication criterion **0.05**. Thus **0** of **1** candidates replicated, so the reporting gate was not passed.

## Recommendation and control plan

Do not report rs070008 as an association: despite its discovery result and same-direction replication estimate, the independent replication significance condition failed. As required by the protocol, reconsider the discovery scan rather than promoting the hit. Check the nominated assay and analysis implementation, preserve the result as a failed replication, and require a newly justified independent confirmation before any future report. Preserve the participant exclusions, variant exclusions, PCA adjustment, discovery result table, and independent replication result as the analysis lock. Any rerun should use the same scripted sequence: participant QC, plate decision, variant QC, ancestry assessment, adjusted discovery scan, multiplicity correction, and candidate-only replication. The next scientific step is functional follow-up and replication in additional populations; do not broaden the claim beyond the tested phenotype, panel, and cohorts.
