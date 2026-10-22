# Metabolic-trait candidate-panel study report

## Executive conclusion

The discovery plate can carry forward: participant QC passed, with **2** failed participants and a failure fraction of **0.008333333333333333**, below the protocol limit. The retained discovery cohort therefore contains **238** participants. The retained variant set contains **34** of **150** panel variants.

The affected and unaffected groups are **not directly comparable without ancestry adjustment**. PC1 showed structure associated with affection status (t = **8.0420120464221**, p = **4.2027663265920956e-14**). The protocol therefore requires the leading structure axes to enter the association model when the ancestry distributions overlap. The scan run here was an unadjusted screening analysis, so its hits are provisional rather than reportable conclusions.

The screening scan produced **10** Bonferroni-significant variants at threshold **0.0014705882352941176**: rs020124, rs020077, rs020030, rs020053, rs020044, rs020139, rs020015, rs020067, rs020105, rs020119. The genomic-control estimate from this scan was **2.0533636430747255**, reinforcing the need to repeat the association analysis with the required structure covariates.

## QC disposition

Participant QC retained every participant except: **P017, P111**. The minimum sample call rate was **0.9466666666666667**. The plate was not re-genotyped because its failed-participant fraction was below the protocol threshold.

Variant QC retained these variants:

rs020015, rs020018, rs020030, rs020031, rs020032, rs020040, rs020041, rs020044, rs020048, rs020053, rs020059, rs020060, rs020062, rs020066, rs020067, rs020068, rs020071, rs020074, rs020077, rs020078, rs020081, rs020090, rs020096, rs020100, rs020105, rs020116, rs020119, rs020124, rs020128, rs020133, rs020134, rs020135, rs020139, rs020148

The computed variant-QC failures were **116**. Of the **150** variants, **5** failed call rate, **4** failed MAF, and **115** failed the unaffected-control HWE criterion; failures may overlap across criteria.

## Replication status

There is no replication data for the **10** nominated discovery hits. The released replication batch contains only **1** candidate, rs020008, which was not among the nominated discovery hits. Consequently, the protocol's requirement for reporting the nominated discovery associations is not met and no nominated discovery association should be reported.

For completeness, the supplied rs020008 batch itself passed sample QC with **0** failed participants and candidate call rate **0.9916666666666667**. rs020008 showed p = **0.0006786817183904285**, odds ratio **2.531324725011956**, and the same direction as its supplied discovery direction. This result cannot be used to validate the ten nominated hits because rs020008 was not one of them.

## What caused the stop, what changed, and what to do next

The immediate stopping cause is not plate quality: it is the ancestry structure and the mismatch between the nominated discovery-hit list and the candidate supplied for replication. No discovery association should be reported until investigators rerun the association scan with the leading structure axes as covariates and the steward supplies replication genotypes for the actual nominated hits. The study lead should also confirm whether rs020008 was intended to replace the nominated list or was released in error.

Hold the current QC outputs, retained-participant list, retained-variant list, PCA definition, covariate-adjusted analysis specification, nominated-hit manifest, and replication candidate manifest under version control. Reuse those locked artifacts for the corrected rerun and require independent verification of candidate IDs, allele coding, p-value threshold, and direction before any report is issued.
