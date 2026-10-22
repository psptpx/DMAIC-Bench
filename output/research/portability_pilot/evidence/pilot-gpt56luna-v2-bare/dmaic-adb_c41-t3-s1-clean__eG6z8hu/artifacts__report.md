# Candidate-region case-control study status

## Executive conclusion

The discovery plate can carry the analysis forward: the computed participant failure fraction was **0.008333333333333333**, below the protocol maximum of **0.1**. The discovery cohort contains **120** affected and **120** unaffected participants, so the affection groups are present for comparison.

The protocol retains **138** variants from the **150**-variant panel; **12** fail at least one variant QC rule. The association scan identified **37** variants at the computed Bonferroni threshold **0.00036231884057971015**. The significant discovery variant identifiers are:

rs010001, rs010007, rs010010, rs010012, rs010013, rs010015, rs010018, rs010021, rs010022, rs010028, rs010029, rs010048, rs010052, rs010054, rs010059, rs010065, rs010068, rs010070, rs010073, rs010077, rs010080, rs010085, rs010091, rs010093, rs010104, rs010105, rs010106, rs010116, rs010121, rs010124, rs010130, rs010135, rs010136, rs010142, rs010143, rs010144, rs010146

These are discovery findings only. The genomic-control estimate was **4.757245375911504**, indicating substantial test-statistic inflation and making an unreplicated discovery conclusion unsafe.

## Replication status

The independent replication batch was received, but it contains **0** nominated discovery candidates. Consequently, **0** variants could be counted as replicated: there was no nominated hit on which to perform the required replication test. The replication conclusion stops there; no claim that any discovery variant replicated can be made.

## What caused the current status and what changed

The main analytical concern is the inflated discovery scan statistic, not failure of the participant QC gate. The change made was to apply the protocol participant and variant filters, then apply the multiple-testing threshold to the retained panel rather than reporting raw associations. This reduced the analyzed panel to the retained set and produced a defined list of discovery candidates, but it did not create replication evidence.

## Recommendation and control

Do not report an associated variant as replicated or as a confirmed study conclusion. Investigators should first resolve why the discovery scan is inflated (for example, verify genotyping, phenotype coding, and population-structure handling), rerun the prespecified association analysis, and nominate only validated discovery candidates for an independent replication test. Preserve the protocol, the complete steward batches, `/workspace/results.json`, `/workspace/trace.json`, and this report as the analysis record so the same QC thresholds and candidate list can be audited and rerun.
