# Sequencing study status

## Executive conclusion

The libraries support an interpretable comparison: all 12 libraries passed the usability rules, with 6 usable control replicates and 6 usable treated replicates. The comparison is identifiable because the 2 preparation batches contain both arms.

The batch-adjusted expression analysis of 400 panel genes nominated 0 genes under the prespecified adjusted-p threshold of 0.05 and absolute log2-fold-change threshold of 1.0. Accordingly, there is currently no compound-responsive gene list to issue.

## What was checked

- Library QC found 0 failed libraries. The minimum usable arm size was 6, above the required minimum of 3. The usability cutoffs were 5,000,000 assigned reads and mapping rate 0.7.
- The sample sheet contained 2 preparation batches and both conditions were represented in each batch. The batch-adjusted model therefore addressed preparation batch rather than treating it as a perfectly confounded factor.
- The expression result was 0 significant genes after applying the prespecified adjusted-p and effect-size criteria.

## Validation and enrichment

No candidates were nominated, so the qPCR batch contained 0 candidates and 0 measurements. Validation concordance is therefore not estimable; the recorded 0 is not evidence that any candidate failed validation. The declared concordance value of 0 is below the facility threshold of 0.75, so the steward locked the gene-set annotation batch. Enrichment was not computed, and no biological interpretation should be inferred from it.

## Business disposition and next actions

The study can make the planned arm comparison on this design, but this analysis does not support issuing a response-gene list. The immediate cause is lack of genes meeting both expression criteria, not library usability or design identifiability. No change to the library set was needed: all libraries were retained.

The facility should review the null expression result with the study lead before extending claims, including checking the prespecified model and effect-size assumptions and deciding whether an independently justified follow-up experiment is warranted. Any future candidate list should be generated under the same declared thresholds and then sent for qPCR validation; enrichment should only be attempted after candidates exist and the validation gate is satisfied.

The analysis should be held by retaining the sample sheet, QC rules, counts, model specification, candidate table, and this trace alongside the report. The locked gene-set step must remain explicitly marked as not computed rather than being replaced by an unvalidated interpretation.
