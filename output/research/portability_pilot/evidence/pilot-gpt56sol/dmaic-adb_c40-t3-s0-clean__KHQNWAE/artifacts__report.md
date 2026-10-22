# Compound-response study: decision report

## Executive conclusion

The libraries can support a conclusion and the intended treated-versus-control comparison is estimable. All **12** libraries passed the facility's usability rules, leaving **6** usable control and **6** usable treated replicates; the smaller arm therefore has **6**, above the required **3**. The sample sheet contains **1** preparation batch, and that batch contains both arms. The treatment design has rank **2** for **2** model columns, so treatment is not confounded with preparation batch.

The count analysis tested all **400** panel genes and called **40** compound-responsive genes under the joint facility rule of adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**. Of these, **24** increased and **16** decreased in treated cells.

## What was done and what it showed

### Library quality

A library was retained only when assigned reads were at least **5000000** and mapping rate was at least **0.7**. There were **0** failed libraries and **12** usable libraries. Consequently, no library was removed and re-sequencing is not required by the replicate rule.

### Design check

There are **2** experimental conditions in **1** preparation batch. Because both conditions occur within that batch, the intended contrast is estimable and treatment is not aliased with batch. The standing rule requires a batch term only when libraries come from more than **1** batch, so the analysis used the simple treatment model.

### Differential expression

Counts were normalized by median-ratio size factors and analyzed gene by gene with a negative-binomial treatment model and Wald tests. P-values were adjusted together by the Benjamini–Hochberg procedure. The normalization calculation used **399** genes with positive counts in every library. Numerical boundary behavior required **4** fixed-dispersion negative-binomial GLM fallback fits; after fallback, **400** genes had finite tests and **0** remained failed.

Called genes, ordered by adjusted p-value, are:

G0124, G0287, G0115, G0279, G0314, G0277, G0247, G0131, G0194, G0061, G0101, G0331, G0110, G0310, G0299, G0107, G0260, G0154, G0052, G0037, G0006, G0276, G0187, G0153, G0010, G0212, G0293, G0118, G0155, G0114, G0280, G0039, G0311, G0374, G0372, G0007, G0383, G0394, G0149, and G0185.

## Business interpretation and next action

The study has cleared both stopping gates: sequencing quality/replication and design identifiability. The available evidence supports a compound-associated expression response in the listed panel genes. No remedial re-sequencing or design reconstruction is indicated for this data set.

The facility should release the complete gene-level result table alongside this report, retain the raw counts, sample sheet, QC results, normalization/model script, and software environment, and have the study team prioritize the called genes for biological interpretation and orthogonal validation. These findings establish association under this cell-line experiment; downstream validation should determine biological mechanism and reproducibility rather than treating panel response alone as causal proof.

## Hold plan

For any repeat, continue enforcing both library thresholds before analysis, retain at least **3** usable replicates in each arm, and ensure every preparation batch contains both arms whenever more than **1** batch is used. Re-run the same normalization, negative-binomial model, multiple-testing correction, and joint calling rule; archive the full table, including non-called genes and numerical fallback flags.
