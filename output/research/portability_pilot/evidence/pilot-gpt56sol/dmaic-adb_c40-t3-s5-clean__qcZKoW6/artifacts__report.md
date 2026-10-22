# Compound-response study: decision report

## Executive decision

The libraries can support analysis: **0 libraries failed QC**, and the control and treated arms each retain **6 usable replicates**, above the required minimum of **3**.
The intended comparison is estimable after preparation-batch adjustment. The treatment-plus-batch matrix has rank **3** across **3** columns, so treatment is not perfectly confounded with batch.
The adjusted analysis calls **3 genes**: **1 upregulated** and **2 downregulated**.

## Measure: library usability

All **12 libraries** were assessed against both standing QC rules. The control arm retained **6** usable libraries and the treated arm retained **6**. Re-sequencing is therefore not required on the current library-QC evidence.

## Analyze: design and batch

There are **2 preparation batches**. Their control/treated cell counts are **5/1** and **1/5**. This is imbalanced, but each batch contains both arms. The full model rank equals its **3 columns**, establishing an estimable treatment coefficient when batch is included.

## Analyze: responding genes

I fitted batch-adjusted negative-binomial count models with median-ratio library-size offsets, adjusted p-values over all **400 panel genes** using Benjamini–Hochberg, and required adjusted p-value below **0.05** together with absolute log2 fold change of at least **1**.

| Gene | Direction | log2 fold change | p-value | adjusted p-value |
|---|---:|---:|---:|---:|
| G0269 | down | -1.225722 | 8.64877e-09 | 3.45086e-06 |
| G0037 | down | -1.008804 | 0.000446656 | 0.022277 |
| G0241 | up | 1.038170 | 0.000739505 | 0.0265937 |

The dual rule matters: genes meeting only the statistical threshold were not called when their effect size was below the required cutoff.

## Limitation

Finite treatment results were obtained for **399 genes**. **1 gene**, G0283, had a total observed count of **362** but its gene-specific negative-binomial fit did not produce a finite result; it is untestable in this analysis rather than evidence of no response. The called-gene conclusion therefore applies to genes with estimable models.

## Improve and hold

- Proceed with biological validation of the called genes; preserve direction and effect-size expectations from the table.
- Do not re-sequence solely for library QC, because both arms cleared the replication gate.
- Keep preparation batch in any reanalysis of these libraries. The batch-adjusted model is the change that makes the intended contrast interpretable despite imbalance.
- For future preparations, randomize both arms across every batch more evenly, retain the same library QC gates, archive the sample sheet with the count matrix, and rerun the same locked calling rule.
- Treat the gene with the failed model fit as missing inferential evidence; review that target separately or obtain a more suitable assay if it is scientifically important.

## Bottom line

The study can carry a qualified conclusion: library QC and design identifiability both pass, and **3 genes** meet the facility's complete response rule under batch adjustment. Follow-up should validate those responses and improve arm balance across preparation batches in future work.
