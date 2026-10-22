# Sequencing study status report

## Executive conclusion

The library QC result does **not** support carrying the study into gene calling. Of the **12** libraries assessed, **8** passed the facility's usability rules and **4** failed. The usable allocation was **6** control libraries and **2** treated libraries. The minimum usable arm size was therefore **2**, below the required minimum of **3**.

The steward consequently withheld the sample sheet. The study cannot currently establish whether treatment is separable from preparation batch, cannot fit the required batch-aware comparison, and cannot produce a defensible list of responding genes.

## What is causing the stop

The immediate limiting factor is the treated arm's usable-library count. The failed libraries were removed by the stated sequencing QC rules; the resulting treated arm did not retain enough usable biological replicates. Because the sample sheet is locked behind this gate, batch/design identifiability was **not computed**.

There is no released data for the gene-level read-count analysis, qPCR validation, or gene-set annotation. Those steps therefore have no computed result, and the conclusion stops at the replicate/design gate. No gene has been called and no candidate list can be issued.

## What was changed and what it achieved

The available sequencing metrics were evaluated against the facility rules. This produced a reproducible QC result: **8** usable libraries, **4** failed libraries, and a failed minimum-replicate verdict. Declaring that verdict correctly prevented downstream analysis from being presented as conclusive when its required design inputs were unavailable.

## Recommended next action and hold point

Re-sequence the study to restore the treated arm to at least the required usable-replicate count, then rerun library QC. Once that gate passes, obtain the sample sheet and compute whether treatment is estimable separately from preparation batch. Only after that design check should the batch-aware gene-level analysis, independent qPCR validation, and gene-set interpretation proceed.

The current hold should remain in place: no expression candidate list, biological interpretation, or validation claim should be released from this data state.

## Audit trail

The quantitative QC results and the refused design step are recorded in `/workspace/trace.json`. The refused downstream batches are not represented as successful analyses; their absence is the reason the conclusion stops at QC.
