# Compound-response study report

## Executive conclusion

The libraries can support a conclusion: all **12** libraries passed the sequencing rules, with **6** usable control and **6** usable treated libraries. The minimum retained per arm was **6**, above the required **3**.

The intended treatment comparison is estimable, but only after accounting for preparation batch. The design contains **2** batches and the treatment-plus-batch design matrix had rank **3** for **3** columns, so it was not confounded.

The batch-adjusted analysis called **38** compound-responsive genes: **15** higher and **23** lower in treated cells.

## What was checked

A library was required to have at least **5000000** assigned reads and mapping rate at least **0.7**. The computation found **0** failed libraries. Thus no library was removed and no re-sequencing gate was triggered.

Allocation was imbalanced but crossed: batch L1 contained **5** controls and **1** treated library; batch L2 contained **1** control and **5** treated libraries. Because both arms occur in each batch, treatment is separable from batch. The imbalance still makes unadjusted arm means unsafe, which is why batch was retained in the model.

## Differential-expression result

Counts for **400** genes were normalized by median-ratio size factors, using **397** genes positive in every library. Per-gene negative-binomial log-link models included treatment and preparation batch. Treatment Wald p-values were adjusted across all **400** genes by the Benjamini–Hochberg procedure. Calls required adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**. There were **0** unresolved fits; **3** fits required a model-based covariance fallback after their initial discrete-model covariance was unavailable.

Called genes:

G0026, G0318, G0358, G0247, G0236, G0355, G0228, G0010, G0302, G0183, G0012, G0213, G0141, G0078, G0373, G0163, G0146, G0086, G0372, G0112, G0075, G0342, G0133, G0017, G0291, G0345, G0311, G0283, G0388, G0108, G0295, G0253, G0275, G0081, G0049, G0340, G0351, G0397

Direction counts refer to the treated-versus-control coefficient. Full gene-level estimates and adjusted p-values are retained in `de_results.csv`.

## Interpretation and next action

The study clears both facility preconditions and supports a compound-response conclusion for the called genes. The main design weakness is strong arm imbalance within each preparation batch, not perfect confounding. The facility should preserve the batch-adjusted result as the primary analysis, avoid reporting an unadjusted arm comparison, and validate the called targets with an independent assay or replication study. Future preparation should balance both arms within every batch so treatment information does not depend heavily on the small cross-batch overlap.

For hold/control, archive the sample sheet, QC decisions, model specification, complete gene table, and this trace; pre-specify the same QC and calling rules for any replication; and review batch balance before library preparation begins.
