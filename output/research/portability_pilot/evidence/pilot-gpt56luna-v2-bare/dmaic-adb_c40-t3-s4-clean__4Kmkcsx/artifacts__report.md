# Sequencing study status report

## Executive conclusion

The libraries can carry a technically eligible comparison: all **12** libraries passed the facility's usability rules, with **6** usable control replicates and **6** usable treated replicates. The minimum usable replicate count was **6**, above the required **3** per arm.

The comparison is identifiable on this design. There was **1** preparation batch, and both arms were represented in it; the computed confounding verdict was `false`.

The expression analysis covered **400** genes using **6** control and **6** treated libraries. No genes were called: `nSignificant = 0`, with **0** up and **0** down calls. The smallest adjusted p-value was **0.9147096113359283**, whereas the prespecified adjusted-p cutoff was **0.05** and the absolute log2 fold-change cutoff was **1.0**. Therefore there is no compound-responsive gene list to issue from this dataset.

## What was checked and what it achieved

- Library QC applied the recorded minimum of **5,000,000** assigned reads and mapping rate of **0.7**. The analysis found **0** failed samples and retained **12** libraries.
- The sample-sheet assessment found no treatment/batch confounding. Both arms were present in the single batch, so the design itself does not prevent the intended comparison.
- The gene-level analysis tested the complete panel of **400** genes and found no gene meeting both calling thresholds. This means the lack of a list is an analysis result, not a consequence of losing libraries or of a confounded preparation batch.

## Validation and annotation status

The released validation batch explicitly contained **0** nominated candidates and **0** qPCR records. Consequently, validation concordance is undefined; it must not be reported as a successful concordance value. The computed validation assessment therefore produced **0** confirmed candidates only in the literal sense that there were no candidates to confirm, not as evidence of validation support.

The gene-set annotation request was locked because the steward requires validation concordance of at least **0.75**, and the available validation batch had no candidates from which concordance could be computed. There is no gene-set annotation data for this run, so enrichment and pathway conclusions cannot be computed and the conclusion stops there.

## Recommendation and control plan

Do not issue a compound-responsive gene list from this experiment. The immediate cause is not library usability or design identifiability; it is that the prespecified differential-expression criteria yielded **0** candidates. Do not reinterpret unadjusted signals as discoveries, and do not claim qPCR support when no candidate was nominated or measured.

For the next study decision, retain the current QC and design checks, rerun the same prespecified expression workflow on any new data, and require an actual nominated set before interpreting qPCR concordance or gene-set enrichment. If candidates emerge, obtain qPCR results for those candidates before issuing a list; otherwise the validation and annotation gates should remain closed.
