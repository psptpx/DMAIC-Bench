# Compound-versus-vehicle targeted-panel study

## Executive conclusion

The sequencing libraries can carry a conclusion. QC retained all 12 libraries, with 6 usable control replicates and 6 usable treated replicates; the minimum arm count was 6, above the required minimum recorded in the QC computation. The design is usable: treatment is observed in both arms within 1 preparation batch, so the contrast is not confounded with batch.

The executed sequencing analysis tested 400 genes and nominated 39 genes meeting adjusted-p-value below 0.05 and absolute log2 fold change at least 1.0. The nominated genes are listed in `/workspace/de_candidates.tsv`.

Independent qPCR evaluated 10 nominated genes. It confirmed 10 in the called direction, giving concordance 1.0. The validation gate therefore passes, so the validated candidate list may be issued.

## What is causing the result and what changed

There is no QC failure or treatment/batch identifiability failure in the analyzed material. The evidence for response comes from the treatment contrast in the count matrix; the independent qPCR check supports the nominated subset. The practical change is to move from the full sequencing nomination set to the independently confirmed list before communicating candidates to the study team.

The panel annotation contained 12 gene sets over a 400-gene universe. The enrichment calculation tested those sets and found 1 significant sets after adjustment. This annotation result is contextual and does not override the gene-level calling and validation gates.

## Candidate disposition

Issue the independently validated list represented by the 10 genes in `/workspace/validation_results.json`. Retain the complete sequencing candidate table in `/workspace/de_candidates.tsv` as a transparent audit record; it contains 39 candidates, while the validated issue list is the smaller nominated subset that was tested by qPCR.

## Hold and next action

Hold the distinction between sequencing-only nominations and independently validated candidates in all downstream communication. Preserve the count matrix, sample sheet, QC computation, candidate table, validation results, annotation, and this trace/report pair so the analysis can be reproduced. If broader biological interpretation is needed, perform it as a follow-up rather than changing the prespecified calling or validation rules.
