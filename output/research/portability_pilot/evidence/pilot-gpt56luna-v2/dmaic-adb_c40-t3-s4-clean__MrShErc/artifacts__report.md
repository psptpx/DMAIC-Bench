# Sequencing study status report

## Executive conclusion

The libraries can support a technically valid comparison: **12** of **12** libraries passed sequencing QC, with **6** usable control replicates and **6** usable treated replicates. The minimum usable replicate count was **6**, above the required minimum of **3**.

The treatment contrast is estimable. All **12** usable libraries were in **1** preparation batch, and that batch contained **6** controls and **6** treated libraries; therefore arm was not confounded with preparation batch.

## Expression result

The analysis covered **400** panel genes using the six-versus-six normalized count comparison, with batch assessed in the design. The calling rule was adjusted p < **0.05** and absolute log2 fold change >= **1.0**. **0** genes met both criteria. Consequently, this run identifies no compound-responsive genes.

## Validation and gene sets

There were **0** nominated candidates and **0** confirmed candidates. The qPCR file contains no candidates to validate, so a candidate-level validation proportion is not biologically estimable; the recorded gate value of **1.0** is vacuous for an empty candidate set, not evidence that any gene was confirmed. The facility rule requires at least **0.75** concordance before issuing a list, and no list was issued.

The panel annotation contained **12** gene sets over a **400**-gene universe. With **0** candidates, the computed number of significant gene sets was **0**.

## What caused the current position and what changed

The limiting result is not library quality or study design: QC passed and the arm contrast is identifiable. The stopping point is that no gene met both prespecified expression thresholds. Because the candidate set is empty, qPCR validation cannot rescue or support a candidate list, and enrichment cannot provide a response interpretation.

No sample was removed and no study conclusion was manufactured. The analysis retained all QC-passing libraries, used the recorded arm and batch information, applied the prespecified calling thresholds, and withheld the candidate list when there was nothing to nominate.

## Recommended next steps and control

Do not issue a compound-response gene list from this run. If the biological question remains important, the study lead should review effect sizes and assay sensitivity and decide whether an independently justified follow-up (for example, additional biological replication or a pre-specified power review) is warranted. Any follow-up should retain the current usability thresholds, preserve treatment representation within preparation batches, repeat the adjusted-p and fold-change gate, and require independent qPCR confirmation before naming candidates.
