# Compound expression study: decision for the principal investigator

## Executive conclusion
The sequencing libraries are usable and the compound contrast is identifiable separately from preparation batch. The batch-adjusted screen finds **26 candidate genes**. Independent qPCR confirms **10 of 10 nominated candidates**, concordance **1.00**, exceeding the facility requirement of **0.75**. The validation gate therefore supports issuing the screen as a candidate list, with direct validation labels rather than claiming every listed gene has been independently confirmed.

## Library and design fitness
There were **0 failed libraries** among **12 libraries**; each arm retains **6 usable replicates**, above the required **3**. The minimum observed assigned reads was **9,307,000**, and minimum mapping rate **0.863**. All libraries were retained; no resequencing is indicated by these metrics.

The design spans **2 batches**. The first batch contains **5 controls and 1 treated library**; the other contains **1 control and 5 treated libraries**. The intercept, treatment and batch model has rank **3** for **3** columns: it is not confounded, but the imbalance limits precision. Batch cannot be omitted. Its incremental sum-of-squares fraction, conditional on treatment, is **0.3201** of centered transformed expression variation. This is a descriptive model contribution, not proof of the physical cause of a batch effect.

## Expression analysis and provisional list
Counts were normalized with median-ratio size factors, transformed to binary-log normalized counts with a unit pseudocount, and fitted gene by gene using treatment plus preparation batch. Residual two-sided t tests were adjusted by Benjamini–Hochberg across **400 genes**. Calls require adjusted p below **0.05** and absolute binary-log fold change at least **1.0**. This is approximate log-expression OLS, not a negative-binomial model; inference assumes independent libraries and well-behaved transformed residuals. The model has **9 residual degrees of freedom**. A count-model sensitivity analysis is recommended before publication.

Positive effects indicate greater expression under compound exposure.

| Gene | Binary-log fold change | BH adjusted p | Direct qPCR confirmation |
|---|---:|---:|---|
| G0010 | 2.328 | 0.0034801 | Not assayed in released validation |
| G0012 | -2.778 | 0.0057362 | Yes |
| G0017 | -1.494 | 0.0074802 | Not assayed in released validation |
| G0026 | 2.044 | 0.00023901 | Not assayed in released validation |
| G0075 | -2.120 | 0.0044639 | Yes |
| G0078 | 2.113 | 0.0054258 | Not assayed in released validation |
| G0086 | -1.740 | 0.0074802 | Not assayed in released validation |
| G0112 | 2.107 | 0.010294 | Not assayed in released validation |
| G0133 | -1.562 | 0.0063752 | Not assayed in released validation |
| G0141 | 2.061 | 0.0057362 | Not assayed in released validation |
| G0146 | -1.624 | 0.0046559 | Not assayed in released validation |
| G0163 | 1.934 | 0.0054258 | Not assayed in released validation |
| G0183 | 1.563 | 0.0019628 | Not assayed in released validation |
| G0213 | -2.580 | 0.00092835 | Yes |
| G0228 | -1.640 | 0.0013284 | Not assayed in released validation |
| G0236 | 2.298 | 0.000664 | Not assayed in released validation |
| G0247 | -3.067 | 0.00060068 | Yes |
| G0291 | -1.530 | 0.011758 | Not assayed in released validation |
| G0302 | -1.913 | 0.0012535 | Yes |
| G0311 | 1.710 | 0.020818 | Not assayed in released validation |
| G0318 | 2.445 | 0.00050054 | Not assayed in released validation |
| G0342 | -1.999 | 0.019008 | Yes |
| G0355 | -2.309 | 0.001043 | Yes |
| G0358 | -2.720 | 0.00023901 | Yes |
| G0372 | -2.224 | 0.0057362 | Yes |
| G0373 | 1.854 | 0.0050051 | Not assayed in released validation |

## Validation and scope
Independent, two-sided Welch tests on the released qPCR biological replicates used nominal p below **0.05**, together with agreement with the supplied nomination direction. All supplied nominations point downward and all confirm. The denominator was the entire nominated validation set, not a selected subset that agreed with this screen.

Only **9** of the adjusted calls overlap that set; **17** calls have no direct qPCR measurement here. G0295 confirms by qPCR but is not called by this adjusted screen, so it is not silently added to the panel list. This nomination mismatch should be reconciled with the original selection procedure. Passing the facility's list-level validation gate is not proof that each unassayed candidate is correct.

## Gene-set context
Over-representation used the **400 measured genes** as background, an upper-tail hypergeometric test and BH adjustment over **12 supplied sets** at **0.05**. There are **1 significant sets**.

- SET03: 10 overlapping calls, adjusted p 3.4189e-05.

Set identifiers have no biological descriptions in the released annotation; a mechanistic pathway claim is not justified. Enrichment is conditional on the targeted panel and the provisional call set, not the whole transcriptome.

## Action and control plan
The analytical change was to retain preparation batch in the expression model instead of attributing all between-arm differences to compound exposure. No physical process change or before-and-after improvement experiment was performed, and no improvement effect is claimed. The resulting batch-adjusted screen and independently passing validation support a qualified candidate release, not a definitive mechanistic conclusion.

The facility should reconcile the nomination mismatch, independently assay remaining priority calls, review count-model sensitivity and transformed-model diagnostics, and have the PI approve the clearly labeled candidate list. Future preparations should randomize and balance arms within batches to reduce reliance on sparse cross-arm batch overlap. Preserve raw counts, library metrics, sample-sheet provenance, model specification, multiplicity rules and validation decisions as release controls. Repeat the same eligibility, identifiability and validation gates for future runs; withhold release if any gate fails.

All requested batches were released; no steward denial or missing-data refusal occurred. Full per-gene results are in `gene_results.csv`; quantitative audit entries and routing decisions are in `trace.json`. Analysis scripts and released batches are retained locally for reproducibility.
