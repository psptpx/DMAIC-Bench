# Candidate-region case-control study report

## Executive conclusion

The discovery plate can carry a conclusion after protocol QC. Exactly **3** of **240** participants failed, a failure fraction of **0.0125**, which is below the plate re-genotyping limit of **0.1**. After the specified exclusions, **237** participants and **139** variants remained.

Affected and unaffected participants were considered comparable for this scan: the PC1 case-control test gave **p = 0.5198453416432482**, above the comparison level of **0.05**, and the computed separation indicator was **0**. The discovery scan found **0** associations at the study-wide threshold. Consequently, there were **0** variants nominated for replication and **0** replicated associations. The study therefore does not support reporting a variant association from this panel.

## Participant QC and plate disposition

Participant call rate was required to be at least **0.95**. The lowest observed participant call rate was **0.94**. The failed participants were P085, P136, P193; these were removed. The retained group contained **119** affected and **118** unaffected participants. Every participant in the released discovery panel other than those named above was retained.

The computed plate-pass indicator was **1**. Thus wholesale plate re-genotyping is not triggered; downstream results use only the retained participants.

## Variant QC

Variants were required to have call rate at least **0.95**, minor-allele frequency at least **0.01**, and unaffected-participant exact HWE p-value at least **0.000001**. Of **150** panel variants, **5** failed call rate, **4** failed frequency, and **2** failed HWE. The union comprised **11** excluded variants:

rs040024, rs040041, rs040044, rs040059, rs040065, rs040066, rs040114, rs040124, rs040128, rs040130, rs040134.

The retained set is all released panel variants except that exact exclusion list, totaling **139** variants.

## Comparability and discovery association

PCA was computed from the retained, mean-imputed, standardized genotypes. The PC1 test statistic was **0.6445593585290945** and its p-value was **0.5198453416432482**. No detectable PC1 separation was found, so the retained affected and unaffected groups were compared using an additive genotype trend scan.

The familywise level was **0.05** over **139** retained variants, giving a Bonferroni declaration threshold of **0.00035971223021582735**. The smallest observed p-value was **0.013391980515363656**, so **0** variants crossed the declaration threshold. The genomic inflation estimate was **1.1113772313100228**. No discovery variant was nominated.

## Replication status

The independent replication file contains **120** participants: **60** affected and **60** unaffected. Its protocol level is **0.05**, with matching discovery direction also required. However, the steward supplied **0** candidate variants and **0** discovery directions because the discovery scan produced no hits. Therefore the variant-level replication-test indicator is **0**: there was nothing eligible to test. The replication cohort does not rescue or confirm an association; it yields **0** replicated findings.

## Actions and control plan

* Preserve the participant and variant exclusion lists with the analysis dataset so the reported retained set remains reproducible.
* Do not report any panel variant as associated or replicated from this study.
* Investigate the modest genomic inflation estimate before any future expanded scan, including additional ancestry or technical covariates if supported by newly collected metadata.
* If the investigators seek another discovery attempt, pre-specify a larger or independent study and repeat the same participant QC, variant QC, structure assessment, multiplicity correction, and directional independent replication rule. Do not selectively test the lowest discovery p-value as though it were a nominated hit.
* Hold any future claim to the same auditable sequence: plate disposition, exclusions, comparability assessment, corrected discovery declaration, and only then independent directional replication.
