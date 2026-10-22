# Compound-response study: decision report

## Executive decision

The sequencing libraries pass the facility's quality and replication gate, but the study cannot support the intended compound-versus-vehicle conclusion. Treatment arm is perfectly confounded with preparation batch, so a treatment effect cannot be separated from a batch effect. Gene-level counts were consequently locked by the steward's design-identifiability gate. No differential-expression result, responding-gene list, or validation concordance could be computed. The candidate list must be withheld.

## What was assessed

### Library usability

The released metrics contained **12 libraries**. Applying the prespecified cutoffs of **5,000,000 assigned reads** and **0.70 mapping rate** produced **0 failed libraries** and **12 usable libraries**. The control arm retained **6 usable replicates** and the treated arm retained **6 usable replicates**; the observed minimum was therefore **6**, above the required minimum of **3**. Library quality and retained replication are not the cause of the stop.

### Design identifiability

The usable sample sheet contains **2 preparation batches**. All **6 control libraries** are in the first batch and **0** are in the second; **0 treated libraries** are in the first batch and all **6** are in the second. In the model containing an intercept, treatment, and batch, the **3-column** design has rank **2**, a deficiency of **1**. The treatment indicator is exactly equal to the second-batch indicator. Thus treatment and preparation batch are perfectly aliased, and the planned batch-adjusted contrast is not estimable.

## Expression and validation status

The panel covers **400 genes**, with prespecified calling criteria of adjusted p below **0.05** and absolute log fold change of at least **1.0**. Those criteria could not be applied: the steward refused release of gene-level counts because the design failed identifiability. Consequently, the number and identities of responding genes are not computable from the released data; none should be claimed.

Independent qPCR validation is downstream of the blocked count analysis and was not released. Its planned confirmation rule uses p below **0.05** in the panel-called direction and requires concordance of at least **0.75**. Actual concordance and the number confirmed could not be computed. This is not a failed validation result; it is an unavailable validation assessment because there is no defensible nominated list. Issuance must stop here.

## Cause, corrective action, and hold plan

The problem is allocation, not sequencing quality: arm and preparation batch were not crossed. Re-sequence or prepare a replacement experiment in which both control and treated libraries occur within each preparation batch, while preserving biological replication. Randomize arm across batches and retain the batch term in the analysis. Before releasing counts for inference, repeat both gates: apply library QC and verify full rank of the treatment-plus-batch model on usable libraries. Only after identifiability is demonstrated should the facility run differential expression, nominate genes under the prespecified thresholds, calculate directional qPCR concordance, and issue a list only if the validation gate passes.

For ongoing control, archive the randomization sheet before preparation, review an arm-by-batch table before sequencing, and make model-rank verification a mandatory release checkpoint. Keep the present candidate list on hold; the current design cannot establish compound response.
