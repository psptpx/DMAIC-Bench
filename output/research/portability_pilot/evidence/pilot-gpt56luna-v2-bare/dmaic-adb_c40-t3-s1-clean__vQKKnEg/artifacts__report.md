# Sequencing-panel study status

## Executive conclusion

The libraries are technically usable: the QC computation found `failedSamples = 0`, with `usableControl = 6` and `usableTreated = 6`. The minimum usable replicate count is `minReplicates = 6`, above the required minimum of `requiredMinReplicates = 3`. The usability rules applied were `minAssignedReads = 5000000` and `minMappingRate = 0.7`.

The comparison cannot support a compound-specific conclusion on this design. The design computation found `confounded = true` across `batchCount = 2` preparation batches: all control libraries were in one batch and all treated libraries were in the other. Consequently, treatment and preparation batch are inseparable.

## Gene and validation status

The steward refused release of the gene-level counts because the design-identifiable gate was not satisfied. There is no gene-count data for this task, so no differential-expression result, responding-gene list, or gene-level significance call can be computed; the conclusion stops there.

Because no nominated gene list could be computed, qPCR validation cannot be scored. The panel gene-set annotation also cannot be used to support an enrichment conclusion. No validation or enrichment number is being reported.

## What is causing the stop

The cause is design confounding, not library usability. The treatment comparison was assigned by preparation batch rather than represented within batches, so any observed expression difference could be caused by treatment, batch, or both. The steward therefore withheld counts rather than release an uninterpretable comparison.

## Recommended next action and control

Repeat the experiment with control and treated libraries distributed across every preparation batch, with the assignment recorded before processing. Retain the same usability rules and require the minimum replicate check before analysis. After a balanced sample sheet is available, request counts, run a batch-aware differential-expression analysis, nominate candidates, and then request qPCR validation. Hold release of a response-gene list until the design is identifiable and the validation criterion has been computed.

This report deliberately does not claim a compound response or validation support because those computations were not possible from the released data.
