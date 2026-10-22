# Study status report

## Executive conclusion

The libraries are usable, but the study cannot support the planned compound-versus-vehicle conclusion on its current design. All 12 libraries passed the stated sequencing QC rules. There are 6 usable control replicates and 6 usable treated replicates, so the smaller arm has 6 usable replicates, exceeding the required minimum of 3.

The decisive problem is preparation design: the 2 preparation batches are perfectly confounded with treatment arm. One batch contains only control libraries and the other contains only treated libraries. Consequently, treatment cannot be estimated separately from preparation batch.

## What was computed

The QC analysis retained all libraries: `failedSamples = 0`, `minReplicates = 6`, `usableControl = 6`, and `usableTreated = 6`.

The design analysis returned `confounded = true` and `batchCount = 2`. These results mean the replicate/QC precondition is met, but the design-identifiability precondition is not.

## Gene calls and validation

The steward locked the gene-level read-count batch because the design-identifiability gate requires `confounded = false`. There is therefore no gene-count data available for a valid differential-expression computation, and the conclusion stops there. No responding genes were called, and no candidate list was issued.

Because no valid candidate list could be nominated, qPCR validation concordance could not be computed. Gene-set annotation/enrichment was also not run. These are unavailable downstream results, not negative findings.

## What should happen next

Repeat the experiment or library preparation with treatment and control represented within each preparation batch, while retaining the stated library QC rules and the required replicate minimum. The next analysis should include preparation batch as a model term only after the treatment contrast is estimable independently of batch. Only then should gene-level testing, candidate nomination, independent qPCR confirmation, and gene-set interpretation proceed.

## Control plan

Before releasing another candidate list, verify three gates in order: library usability, sufficient usable replicates in both arms, and treatment/batch identifiability. Hold the list if any gate fails. After an identifiable expression analysis, apply the standing adjusted-significance and fold-change rules, then require the stated independent qPCR concordance rule before issuing candidates.
