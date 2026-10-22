# Study status report

## Executive conclusion

The libraries pass the usable-replicate requirement, but the planned compound-versus-vehicle comparison is not identifiable on the usable design. Consequently, no defensible gene response list can be issued from this study.

## What was computed

The sequencing QC computation found 4 failed libraries. It retained 4 control libraries and 4 treated libraries, so the minimum retained replicate count across arms was 4. The QC rules therefore did not stop the study for insufficient usable replicates.

The design computation found 2 preparation batches among 8 usable libraries. All 4 usable control libraries are in batch L1, while all 4 usable treated libraries are in batch L2. Thus treatment is perfectly confounded with preparation batch. A batch term cannot separate the compound effect from the batch effect in this design.

## What could not be concluded

The steward locked the gene-level read-count batch because the design-identifiable gate was not satisfied. There is no gene-level count data available for this run, so differential-expression results were not computed and the number of responding genes is unknown. The conclusion stops there for gene calling.

Because no nominated gene list was produced, independent qPCR validation and gene-set annotation were not released. Validation concordance and enrichment therefore were not computed. No candidate list should be issued.

## Cause, change, and achieved result

The limiting issue is not the number of usable replicates; it is the allocation of usable libraries across preparation batches. QC removed low-read or low-mapping libraries, leaving one arm in each batch. The QC filtering achieved adequate retained replication, but it did not achieve an identifiable treatment comparison.

## Recommended next action and control

Reprepare or re-sequence the study with both arms represented within each preparation batch, while applying the same library usability rules before analysis. Record the batch and arm assignments before release, verify that the treatment contrast is identifiable after QC, and include batch in the expression model when multiple batches remain. Only after that check should gene calls and independent qPCR validation be attempted.
