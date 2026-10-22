# Study status for the principal investigator

## Decision

The current libraries cannot carry a compound-versus-vehicle conclusion. The QC calculation evaluated **12** libraries and found **4** failures. Filtering leaves **6** usable control libraries and **2** usable treated libraries. The minimum retained arm count is therefore **2**, below the required minimum of **3**. The replicate-sufficiency rule fails, so the facility's prescribed action is to resequence before calling genes.

## What is causing the stop

All QC failures occur in the treated arm. Of the failed libraries, **2** fail assigned-read depth and **2** fail mapping rate. This creates the arm imbalance and leaves too few independent treated replicates. Applying the standing QC rules changed the analyzable set from **12** libraries to **8**; it did not repair the study, because the treated arm still fails the replicate requirement.

## Design and expression conclusions

The steward locked the sample sheet after the failed replicate gate. Preparation-batch assignments are therefore unavailable for analysis, and treatment-versus-batch identifiability could not be computed. It is not possible to say from the released data whether the intended treatment contrast is separable from preparation batch.

Gene-level counts remain locked behind the sample-sheet assessment. Consequently, differential expression was not run, no responding genes can be identified, and no numerical gene-call result is claimed. This is a lack of an admissible analysis, not evidence that the compound has no effect.

## Independent validation and release decision

The qPCR batch remains locked behind gene-level analysis. Validation concordance could not be computed. With no admissible panel candidate set and no accessible validation result, the facility must not issue a candidate list.

## Required next action and control plan

Resequence or replace failed treated libraries, then reapply the same assigned-read and mapping-rate rules. Proceed only after every arm meets the retained-replicate requirement. At that point, obtain the sample sheet and verify that treatment is estimable separately from preparation batch. If it is, fit the batch-adjusted expression model, apply the prespecified gene-call criteria, and then assess independent qPCR concordance before release.

Hold the decision through the same gates on the replacement data: documented library QC, arm-level replicate sufficiency, design identifiability, batch-adjusted expression analysis where required, and independent validation. No change to thresholds or post hoc inclusion of failed libraries should be used to bypass the present stop.
