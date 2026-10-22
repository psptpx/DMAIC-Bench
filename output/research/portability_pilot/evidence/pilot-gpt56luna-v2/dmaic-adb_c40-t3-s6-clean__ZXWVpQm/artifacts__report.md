# Compound-versus-vehicle panel study: status report

## Executive conclusion

The libraries pass the replicate-count gate but the study design cannot support the planned compound-versus-vehicle conclusion. QC was computed for 12 libraries: 4 failed and 8 were usable. The usable set contains 4 control replicates and 4 treated replicates, meeting the required minimum of 3 per arm.

The decisive problem is preparation-batch confounding. The usable libraries occupy 2 preparation batches, with all 4 usable controls in L1 and all 4 usable treated libraries in L2. Treatment therefore cannot be separated from batch. The steward locked the gene-level count batch on this basis, so no differential-expression result was computed.

Accordingly, no responding genes can be called, no candidate list can be nominated, and qPCR validation cannot support issuing a list. There is no gene-level count data for this route; the conclusion stops there rather than substituting an unadjusted comparison.

## What was assessed

A library was counted as usable only when assigned reads were at least 5000000 and mapping rate was at least 0.7. The QC computation found 4 failed libraries and a minimum usable replicate count of 4 across the two arms. The minimum required replicate count was 3.

The design computation used the 8 usable libraries and found 2 preparation batches. It found perfect alignment of arm and batch: controls were in L1 and treated libraries were in L2. Because the treatment contrast is not estimable separately from batch, adding batch to the model cannot recover the intended comparison.

The standing gene-call thresholds were adjusted p below 0.05 and absolute log2 fold change at least 1, but they were not applied: the count data were not released after the design gate failed. The independent-validation rule requires confirmation of at least 0.75 of nominated candidates, but there were no nominated candidates to validate.

## Business impact

The QC change achieved a clear result: the usable library set is large enough by arm, so insufficient replicate count is not the blocker. The blocker is allocation of usable libraries across preparation batches. Because the treatment effect and batch effect are inseparable, any apparent expression difference would have an unresolvable design explanation.

No gene list is issued. No validation conclusion is claimed. There is no missing computation to paper over: the steward explicitly refused the gene-count batch under the design-identifiability gate.

## Recommended next action and control

Repeat the experiment or re-sequence only after correcting the design so that each preparation batch contains both arms, while retaining the stated library QC rules. Reassess usable replicates and batch balance before running gene-level analysis. If the redesign passes, include preparation batch in the expression model, apply the stated gene thresholds, and send only nominated candidates to independent qPCR. Hold the candidate list unless the validation concordance reaches the stated minimum of 0.75.

Maintain the sample sheet with arm, batch, and QC metrics together, and make design identifiability a release gate before counts or candidate lists are accepted.

## Traceability

All reported computed quantities are recorded in `/workspace/trace.json`. The QC result is step 1, the batch-confounding result is step 2, and the refused count-based analysis is step 3.
