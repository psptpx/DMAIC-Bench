# Sequencing study status report

## Executive conclusion

The libraries can support an analysis: all 12 libraries passed the facility's sequencing QC, and the minimum usable replicate count was 6. The treatment comparison is estimable because the usable control and treated libraries share the observed preparation batch; the design was not confounded.

The expression analysis tested 400 panel genes and produced 39 genes meeting the planned adjusted-p-value and absolute-log2-fold-change criteria. This is a sequencing result, not an issuable candidate list. Independent qPCR validation tested 10 of those nominated genes, confirmed 0, and yielded concordance 0.0. The required validation concordance is 0.75, so the candidate list must be withheld and the panel result reconsidered.

## What was computed

- QC: `failedSamples = 0`; `usableSamples = 12`; `minReplicates = 6`.
- Design: `confounded = false`; `batchCount = 1`.
- Differential expression: `nGenesTested = 400`; `nSignificant = 39`, using `log2fcThreshold = 1.0` and `padjThreshold = 0.05`.
- Validation: `nCandidatesTested = 10`; `nConfirmed = 0`; `concordance = 0.0`, against `minConcordance = 0.75` and `alpha = 0.05`.
- `nCandidatesUntested = 29`; those genes have no qPCR result in the released validation batch.

The differential-expression calculation used library-size-normalized log2 counts, Welch two-sample tests, and Benjamini-Hochberg adjustment. Validation confirmation required qPCR p < 0.05 and agreement with the sequencing direction.

## Interpretation for the study

The sequencing libraries are not the limiting factor, and the treatment-versus-control comparison can be made on this design. The limiting factor is independent validation: none of the 10 tested nominations met the confirmation rule. The steward therefore did not release the panel gene-set annotation; it was locked because validation concordance 0.0 did not reach 0.75. Enrichment and annotation-based interpretation cannot be computed from the available data.

No gene should be issued as a validated compound-responsive candidate from this run. The 29 nominated genes without qPCR data also cannot be treated as validated; they remain untested rather than confirmed or disproved.

## Recommended next action and control

Withhold the candidate list, review the sequencing calls and qPCR assay performance, and repeat independent validation for the nominated genes—at minimum addressing the 29 currently untested genes and reassessing the 10 tested genes. Reconsider the panel result only after the facility's confirmation rule is met. Hold the release gate on both the candidate list and downstream gene-set interpretation until the computed concordance reaches the required threshold and the steward releases the annotation.

## Traceability

All quantitative results in this report are recorded in `/workspace/trace.json`. The gene-set annotation step was refused by the steward's validation gate, so no enrichment number is reported.
