# Metabolic-trait candidate-panel study report

## Executive conclusion

The discovery plate can carry an analysis conclusion: participant QC found **3** failed participants and a fail fraction of **0.0125**, below the protocol maximum of **0.1**. Re-genotyping was therefore not triggered.

After removing failed discovery participants, **237** participants remained. Final variant QC retained **137** variants and failed **13**. The affected/unaffected cohort comparison did not show ancestry separation in the leading **5** tested axes; the minimum leading-axis phenotype-separation p-value was **0.10983038816211961**, so no ancestry covariates were required by the protocol.

The discovery scan tested **137** retained variants. The Bonferroni threshold was **0.00036496350364963507** and **1** variant was significant: **rs000008**, with p-value **9.974888997073213e-10**, odds ratio **3.7865156483986326**, and a positive direction.

The independent replication cohort contained **120** participants. Its candidate call rate for rs000008 was **0.9916666666666667**; **2** replication participants failed the sample call-rate rule, a fraction of **0.016666666666666666**. rs000008 replicated with p-value **5.037312231519281e-05**, odds ratio **3.2240861372085563**, and the same positive direction. Thus **1** of **1** nominated candidates replicated and rs000008 is reportable under the protocol.

## What caused the result and what changed

The initial discovery data contained low-call participants and low-quality variants. Applying participant QC removed **3** participants, and applying variant QC to the retained discovery cohort removed **13** variants. The resulting association scan identified one corrected-significance hit, rs000008. A sensitivity scan including **5** PCs also found **1** significant hit, consistent with the primary result.

The decisive improvement was requiring replication before reporting. The independent cohort confirmed rs000008 at p-value **5.037312231519281e-05** with concordant direction, changing the finding from a discovery-only candidate into a protocol-reportable association.

## What investigators should do next

Report rs000008 as the single replicated association, including its discovery and replication effect estimates and directions. Preserve the participant and variant exclusion lists, the QC thresholds, the tested-variant set, and the nominated-hit manifest as the audit trail. Do not promote any other variant: the discovery scan produced **1** corrected hit, and no other nominated candidate was available for replication.

The analysis should be held by rerunning the recorded QC, structure assessment, discovery scan, and replication check from the steward batches before any future report revision. The replication sample had **2** sample QC failures, so any follow-up should retain the same sample-level QC rule rather than silently changing the cohort.
