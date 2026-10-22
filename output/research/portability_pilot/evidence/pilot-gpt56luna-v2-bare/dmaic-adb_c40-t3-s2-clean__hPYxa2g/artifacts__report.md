# Sequencing study status report

## Executive conclusion

The study is technically usable and can support a compound-versus-vehicle comparison. All 12 libraries passed the facility QC rule, with 6 usable control and 6 usable treated libraries and 0 failed libraries. The minimum usable arm size was 6, so the replicate gate passed.

The comparison is not perfectly confounded with preparation batch: the design contains 2 batches and both arms occur across them. However, batch is important: the computed batch variance fraction is 0.5918669402040435. The primary result therefore uses the batch-adjusted analysis, not the unblocked screen.

## Expression result

The unblocked analysis called 118 genes, but the batch-adjusted analysis called 31 genes under the facility's expression-calling rules. The 31-gene batch-adjusted list is the defensible sequencing result:

G0010, G0012, G0017, G0026, G0075, G0078, G0086, G0108, G0112, G0117, G0133, G0136, G0141, G0146, G0163, G0183, G0213, G0228, G0236, G0247, G0291, G0295, G0302, G0318, G0342, G0345, G0351, G0355, G0358, G0372, G0373.

The unblocked count is retained as a sensitivity result because it is more affected by preparation-batch structure; it is not the issuance list.

## Validation

Independent qPCR tested 10 of the 31 batch-adjusted candidates. All 10 tested candidates were confirmed under the validation rule, and concordance was 1.0, above the facility's validation threshold. The confirmed tested genes are:

G0012, G0075, G0213, G0247, G0295, G0302, G0342, G0355, G0358, G0372.

This supports issuing the validated tested subset, but it does not establish qPCR confirmation for the other 21 candidates because no validation result was obtained for them in this batch.

## Gene-set result

The enrichment computation used a 400-gene universe, 31 primary candidates, and 12 annotated sets. It found 1 significant set after BH adjustment: SET03, with overlap 14, raw p-value 7.960267012660774e-10, and adjusted p-value 9.55232041519293e-09. No biological name beyond the supplied SET03 identifier was provided, so the set should not be given an invented interpretation.

## What caused the change and what to do next

The main change from the initial screen was explicit adjustment for preparation batch. That reduced the called list from 118 genes to 31 and prevented batch-associated signal from being presented as compound response. The qPCR results support the direction and significance of all 10 tested primary candidates.

The facility should issue the 10-gene validated subset as the high-confidence list, retain the remaining 21 batch-adjusted genes as unvalidated candidates, and obtain independent qPCR confirmation for those 21 before treating them as validated. The analysis should be held by retaining the sample sheet, batch-aware model, thresholds, complete candidate-level statistics, validation results, and the trace accompanying this report.
