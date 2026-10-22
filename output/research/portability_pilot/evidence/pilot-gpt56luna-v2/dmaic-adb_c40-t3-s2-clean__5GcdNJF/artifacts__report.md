# Sequencing study status report

## Executive conclusion

The study can carry a conclusion. All 12 sequenced libraries passed the facility usability rules, leaving 6 usable replicates in each arm. The treatment comparison is identifiable separately from preparation batch, and the expression analysis therefore included batch as a model term.

The batch-adjusted panel analysis nominated 31 genes using adjusted p < 0.05 and absolute log2 fold change >= 1. The nominated genes are:

G0358, G0213, G0247, G0302, G0355, G0026, G0318, G0228, G0146, G0075, G0236, G0017, G0372, G0086, G0012, G0133, G0291, G0117, G0183, G0342, G0010, G0078, G0141, G0163, G0295, G0373, G0108, G0345, G0112, G0136, G0351

Independent qPCR confirmed 10 of 10 nominated candidates, a concordance of 1.000. This meets the facility validation rule, so the candidate list is supported for issue.

## What was found and what changed

The primary operational risk was whether library QC and the treatment/batch design would support inference. No library failed QC, and the arm-level usable replicate minimum was 6. The sample sheet showed 2 preparation batches with both arms represented across the design, so the comparison was not confounded. The analysis was changed accordingly from an unblocked comparison to a batch-adjusted expression model.

That change produced 31 called genes under the prespecified thresholds. The independent validation result supports the list rather than requiring it to be withheld.

## Supplementary gene-set analysis

The called list contained 31 genes and was evaluated against the 400-gene panel universe and 12 annotated sets using hypergeometric enrichment with BH adjustment. 1 sets met adjusted p < 0.05. This is interpretive support only; it does not change the gene-calling rule.

## Recommendation and control plan

Issue the validated candidate list, preserving the exact treatment direction and adjusted-p results from the blocked analysis. Archive the QC, sample-sheet, count, validation, and annotation inputs with the analysis outputs. For follow-up work, retain the same library usability gates, preserve representation of both arms within each preparation batch, include batch in the model whenever multiple batches are present, and require independent qPCR confirmation before any future list is released.
