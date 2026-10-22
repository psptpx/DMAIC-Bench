# Sequencing study status

## Executive conclusion

The libraries can support an analysis: the sequencing QC retained all 12 libraries, with 6 usable control libraries and 6 usable treated libraries. The treatment comparison is identifiable separately from preparation batch, so the study design can answer its stated comparison when batch is included in the model.

The answer from the released data is **no called compound-responsive genes**. The batch-adjusted expression analysis tested 400 genes across 12 samples and returned 0 genes meeting the prespecified calling rule. Consequently, no candidate list can be issued.

## What was found

- Sequencing QC found 0 failed samples and a minimum of 6 usable replicates across the arms.
- The usable libraries span 2 preparation batches, and the treatment effect is not confounded with batch. Batch was therefore retained as a model term.
- The blocked expression analysis produced 0 significant genes under the brief’s adjusted-p-value and absolute-effect-size rule.
- Independent qPCR received 0 nominated candidates and confirmed 0 candidates. The computed concordance fraction is 1, but this is a vacuous fraction because the denominator is 0; it is not validation of a biological hit.
- With 0 nominated genes, gene-set enrichment returned 0 significant sets.

## Business interpretation

The immediate limiting factor is not library usability or design identifiability. Those gates passed. The current result is instead that the batch-adjusted panel analysis supplied no gene satisfying the facility’s calling rule. The validation step consequently cannot rescue or support a candidate list: there was nothing to validate. The appropriate deliverable is a no-hit status, not a list of compound targets.

## What changed and what it achieved

The analysis used the usable libraries, represented preparation batch explicitly, applied the prespecified differential-expression decision rule, and then checked the empty result against the independent validation and annotation batches. This achieved a defensible conclusion that the current data do not nominate a response gene while avoiding an unsupported biological claim.

## Recommended next steps and control

Do not issue a candidate list from this run. Preserve the sample sheet, QC classifications, batch term, thresholds, model specification, and complete trace as the controlled analysis record. If the biological question must be pursued, the facility should first review count depth, dispersion, effect sizes, and the planned power for a repeat experiment; any rerun should preserve representation of both arms in each preparation batch and pre-register the same calling and validation rules. A future list should remain withheld unless genes pass the expression rule and independent qPCR confirms the nominated set.
