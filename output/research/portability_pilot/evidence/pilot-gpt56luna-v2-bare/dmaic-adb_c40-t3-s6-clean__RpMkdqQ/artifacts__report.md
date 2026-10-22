# Study status report

## Executive conclusion

The libraries pass the replicate sufficiency requirement: QC leaves **4 usable libraries in each arm**, compared with the required minimum of **3**. The study nevertheless cannot support the planned compound-versus-vehicle expression conclusion because the usable design is confounded: the control libraries are all in preparation batch L1 and the treated libraries are all in preparation batch L2, with **2 batches** represented.

The steward therefore refused to release the gene-level count batch at the design-identifiability gate. No differential-expression result, responding-gene list, qPCR validation score, or gene-set result was computed. The conclusion stops at design assessment; no gene should be nominated from this archive.

## What was checked

A library was evaluated against the released criteria of at least **5,000,000 assigned reads** and mapping rate at least **0.70**. **4 libraries failed** QC. The remaining usable libraries were sufficient for the replicate gate, but this did not repair the batch allocation.

The identifiability analysis used the usable libraries in the sample sheet. Batch and arm were perfectly aligned, producing `confounded=true` for **2** preparation batches. The steward's counts gate requires an identifiable design, so the counts request was refused rather than analysed with an unsupported model.

## Cause and impact

The immediate cause is preparation-batch/arm confounding, not a shortage of usable replicates. Because batch and treatment arm cannot be separated in the usable data, any apparent arm difference could equally be a batch effect. Therefore the archive cannot establish which genes respond to the compound.

There is no data for the gene-level counts step: the steward refused its release under the identifiability gate. The downstream qPCR and gene-set batches consequently cannot be reached. Their results are unavailable, not negative, and no validation concordance can be reported.

## Recommended change and how to hold it

Re-prepare or repeat the experiment with both arms represented within each preparation batch, while retaining the released library-QC criteria and the minimum of **3** usable replicates per arm. Before sequencing or expression modelling, verify from the sample sheet that arm is not perfectly aligned with batch. Then rerun QC, confirm identifiability, perform the planned expression analysis, and only nominate genes meeting the released fold-change and adjusted-p-value rules. Validation should be assessed only after a candidate list exists.

The one request for an outside process fact was unroutable and supplied no study fact; this report therefore makes no claim that such a redesign has already been performed.
