# Compound-versus-vehicle targeted-panel study report

## Executive conclusion

The libraries can support a comparison, but this run does not support a compound-response gene list. All **12** sequenced libraries passed the usability rules: at least **5000000** assigned reads and mapping rate at least **0.70**. The usable set contains **6** control and **6** treated libraries, exceeding the required minimum of **3** usable replicates per arm.

The design is identifiable. There is **1** preparation batch, and it contains both arms, so treatment is not confounded with preparation batch. The comparison can therefore be made on this design. Because there is only **1** batch, there is no between-batch replication in this data set; the analysis result should not be generalized beyond this experiment without further design support.

## Analysis result

The count analysis covered **400** panel genes, using **6** control and **6** treated libraries. A gene was eligible for calling only when adjusted p was below **0.05** and absolute log2 fold change was at least **1.0**. The computation produced **0** significant genes under those rules.

Accordingly, there are no nominated candidates and no compound-responsive genes to report from this sequencing analysis. This is a computed null result, not a claim that the compound has no biological effect.

## Validation and release decision

The independent qPCR batch contained **0** nominated candidates and confirmed **0** genes. A confirmation fraction is not empirically estimable when the candidate set is empty; the recorded concordance value of **0.0** is the routing value used for the steward gate, not evidence from a nonempty validation set. The facility rule requires concordance of at least **0.75** before a candidate list is issued. That gate was not met, and no candidate list should be issued.

The gene-set annotation was not released because the validation-concordance gate was locked. Therefore no annotation-based interpretation was computed, and the conclusion stops at the absence of called genes and the withheld candidate list. No annotation result has been invented.

## What caused the current position

The library and design prerequisites passed: all **12** libraries were usable, both arms retained **6** replicates, and the arms were represented within the same batch. The stopping point is the gene-level result: **0** of **400** genes met both calling thresholds. Since there were **0** candidates, independent qPCR could not provide a confirmation fraction for a candidate list, and the validation gate remained unmet.

## Recommended next action and control

Do not issue a biological candidate list from this run. First review the effect-size and variance assumptions and the study's ability to detect the prespecified minimum absolute log2 fold change of **1.0** at adjusted p below **0.05**. If a stronger answer is required, repeat or extend the experiment with an explicitly planned design that preserves both arms within each preparation batch and adds independent batch replication. Re-run the same QC, batch-aware comparison, thresholded nomination, and independent qPCR confirmation workflow before release. Hold the release decision until the validation requirement of **0.75** concordance is satisfied for a nonempty nominated set.
