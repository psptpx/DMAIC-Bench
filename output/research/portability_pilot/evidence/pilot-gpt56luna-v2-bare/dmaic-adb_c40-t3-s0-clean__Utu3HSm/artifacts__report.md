# Sequencing panel study status

## Executive conclusion

All **12** sequencing libraries passed usability QC, with **0** failed libraries and **6** usable replicates in each arm; the required minimum was **3**. The treatment comparison is identifiable because both arms are represented within the same preparation batch. Only **1** preparation batch was observed, so a separate batch effect cannot be estimated.

The unblocked treated-versus-control analysis covered **400** panel genes using **6** control and **6** treated libraries. **40** genes met adjusted p < **0.05** and absolute log2 fold change >= **1.0**:

G0006, G0007, G0010, G0037, G0039, G0052, G0061, G0101, G0107, G0110, G0114, G0115, G0118, G0124, G0131, G0149, G0153, G0154, G0155, G0187, G0194, G0212, G0247, G0260, G0276, G0277, G0279, G0280, G0282, G0287, G0293, G0299, G0310, G0311, G0314, G0331, G0372, G0374, G0383, G0394

qPCR validation covered **10** of these **40** calls, with **4** qPCR replicates per arm. All **10** were confirmed at p < **0.05** and directionally concordant, giving concordance **1.0**, above the facility threshold of **0.75**. The validated genes were:

G0299, G0277, G0314, G0311, G0276, G0187, G0124, G0154, G0247, G0115

The remaining **30** sequencing calls were not independently validated in the released batch.

## Findings and cause

Library quality is not limiting: **0** of **12** libraries failed and the minimum usable arm size was **6**, above the required **3**. The design limitation is preparation-batch coverage: only **1** batch was observed. Because both arms occur in that batch, the compound comparison can be made, but batch-to-batch reproducibility and batch adjustment cannot be assessed.

## Gene-set result

Over-representation testing used the **400**-gene panel universe, the **40** called genes, and **12** annotated sets with BH adjustment at alpha **0.05**. **1** set passed: SET03.

## Recommendation and control plan

Issue the **10** validated genes as supported by this experiment. Label the other **30** sequencing-only calls as requiring validation before treating them as confirmed. Do not claim that this experiment estimates a batch effect. For the next study, distribute both arms across multiple preparation batches with balanced allocation, then repeat QC, differential analysis, validation, and enrichment using the same rules. Retain the raw steward batches, derived result tables, and this trace for reproducibility.

## Data boundary

No unavailable study fact was inferred. In particular, batch reproducibility was not computed because only **1** batch was observed.
