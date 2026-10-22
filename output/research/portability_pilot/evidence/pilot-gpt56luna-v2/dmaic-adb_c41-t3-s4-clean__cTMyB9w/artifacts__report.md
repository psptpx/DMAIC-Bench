# Candidate-region case-control study report

## Executive conclusion

The discovery plate can carry the analysis forward under the protocol: the computed participant failure fraction was **0.0125**, below the permitted maximum of **0.1**, so the plate was retained rather than re-genotyped. The scan produced **0** Bonferroni-significant variants, so there is currently no discovery association to report.

The independent cohort was available, but the nominated discovery candidate set was empty (**0** candidates). Therefore no replication p-value or same-direction replication assessment could be computed. The conclusion stops at: no protocol-level discovery hit was found, and replication of a hit was not applicable.

## What was retained

- Discovery participants analyzed: **240**.
- Participants failing the call-rate rule: **3**, fraction **0.0125**.
- Discovery panel variants: **150**.
- Variants retained after call rate, control MAF, and control HWE filtering: **138**; variants excluded: **12**.

## Cohort comparability and association analysis

The leading-axis check did not show affected/unaffected separation: PC1 had p-value **0.48379006582465833**, and the separation verdict was false. Structure was nevertheless detected on a later leading axis, whose p-value was **0.03680249497138648**. Consistent with the protocol, the association model included **5** leading-axis covariates rather than comparing separated ancestries.

The Bonferroni threshold over the **138** retained variants was **0.00036231884057971015** (family-wise alpha **0.05**). The adjusted scan found **0** significant variants. The genomic-control lambda was **0.8391361726486453**. Thus, nominal signals are not sufficient for a protocol declaration, and no variant was nominated.

## Replication status

The replication cohort contained **120** participants, including **60** affected and **60** unaffected participants. Its participant QC found **1** failure, a fraction of **0.008333333333333333**. There is no replication association result because there were **0** nominated candidates; consequently, the number replicated is **0** by the empty candidate-set computation, not evidence of successful replication.

## What caused the current status and what changed

The limiting result is the adjusted discovery scan: none of the **138** retained variants crossed the corrected threshold. The analysis was changed from an unadjusted comparison to a structure-adjusted scan because the leading-axis assessment found overlapping structure. That change provided the protocol-required adjustment, but it did not create a qualifying hit.

## Recommended next action and control

Do not report a variant association from this study. Preserve the retained-participant and retained-variant lists, the QC thresholds, the PCA covariate definition, and the exact adjusted model as the analysis lock. If investigators pursue additional work, it should be a prespecified reconsideration of the discovery scan or a new study, with any future candidate requiring an independent replication test under the stated replication rule before reporting.
