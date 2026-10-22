# Compound-versus-vehicle targeted-panel study report

## Executive conclusion

The sequencing libraries are usable, and the comparison is identifiable on this design. However, the batch-adjusted analysis nominated no genes. The candidate list must therefore be withheld. Independent qPCR validation cannot establish a candidate-level concordance because there were no nominated candidates and no qPCR records in the released validation batch. The gene-set annotation was not released because the validation gate was not met; no enrichment analysis was performed.

## What was checked

- Library QC evaluated **12** libraries. **0** failed the usability rules, and the smaller usable arm still had **6** replicates. This clears the facility's usable-library and replication prerequisite.
- The libraries came from **2** preparation batches, and both batches contained both study arms. The treatment effect was therefore estimable separately from preparation batch. Batch was included as a model term.
- The count analysis covered **400** genes and **12** libraries, using a batch-adjusted expression model. The calling thresholds were adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**.
- The result was **0** significant genes under those thresholds.

## Validation and release decision

Because the sequencing analysis produced **0** nominated candidates, there was nothing to send forward for candidate-level qPCR confirmation. The validation batch contained **0** qPCR records. Consequently, a candidate-level concordance ratio is undefined rather than a measurable pass. The facility requires concordance of at least **0.75** before issuing a list, so no candidate list is issued.

The steward also withheld the panel gene-set annotation behind that validation gate. Since there is no released annotation and no candidate list, enrichment or pathway claims cannot be computed and are not reported.

## Where the study stands

The technical library prerequisite is satisfied and the treatment-versus-control comparison is statistically estimable. The current stopping point is biological evidence: the batch-adjusted panel analysis produced no calls at the prespecified effect-size and multiplicity thresholds. This is not evidence that a particular gene responds; it is a zero-call result under the stated analysis plan.

## What should happen next

Do not issue a candidate list from this run. First review whether the expected compound effect, count scale, normalization/model choice, and assay sensitivity are adequate for the biological question. If the study lead decides that a stronger or better-powered experiment is warranted, define that follow-up before generating new libraries. Re-sequencing is not required by the library-QC rule here, because the usable-replicate prerequisite passed; it would only be justified by a separately documented technical or power concern.

## Holding the result

The calculation record is stored in `trace.json`. It records the QC result, the design-identifiability result, the batch-adjusted differential-expression result, and the failed/undefined validation step. Any future reanalysis should preserve the same sample sheet, batch term, calling thresholds, and explicit distinction between a zero candidate count and an undefined validation ratio.
