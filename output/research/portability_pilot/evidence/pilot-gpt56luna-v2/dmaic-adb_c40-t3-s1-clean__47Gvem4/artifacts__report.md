# Sequencing study status

## Executive conclusion

The libraries themselves are adequate for analysis: all 12 libraries passed the stated usability rules, and there are 6 usable control replicates and 6 usable treated replicates. However, the intended compound-versus-vehicle comparison cannot be made on this design. The study must not issue a gene candidate list from these data.

## What was checked

A library was retained when assigned reads were at least 5000000 and mapping rate was at least 0.7. The QC computation found 0 failed libraries, 12 usable libraries, and a minimum of 6 usable replicates per arm. The minimum required by the brief is 3 per arm, so library quantity is not the limiting issue.

The sample sheet has 2 preparation batches. Batch L1 contains 6 controls and 0 treated libraries; batch L2 contains 0 controls and 6 treated libraries. Consequently, treatment is perfectly confounded with preparation batch. A model cannot estimate a treatment effect separately from batch on these libraries.

## What could not be concluded

The steward refused to release the gene-level read-count batch because the design-identifiability gate requires a non-confounded design. Therefore there is no released count matrix on which to compute differential expression. No differential-expression result was computed, and the absence of a result is not evidence that no genes respond.

Because gene-level counts were not released, no gene calls, fold changes, adjusted p-values, enrichment result, nominated candidate list, or qPCR concordance can be computed. The conclusion stops at the design gate. The qPCR validation and panel gene-set annotation are consequently also unavailable; validation cannot support or reject a candidate list that cannot validly be nominated.

## Business decision and next action

The change made in this review was to apply the facility's QC and design gates before calling genes. It established that sequencing quality and replicate quantity are sufficient, but that preparation assignment prevents the requested comparison. The achieved outcome is prevention of an uninterpretable treatment claim, not a biological discovery.

The facility should repeat or re-prepare the experiment so that control and treated libraries are represented within each preparation batch, while retaining at least 3 usable replicates per arm after QC. The revised sample sheet should be checked for treatment/batch separability before sequencing or gene calling. Once that gate passes, the facility can request counts, fit the prespecified batch-adjusted analysis, apply the stated call thresholds, and then perform independent qPCR validation before issuing any candidate list.

The current result should be held under the design gate: no compound-responsive genes are reported from this archive, and no validation-supported list is issued.
