# Compound-expression study: decision for the principal investigator

## Executive decision
The libraries are usable and the compound contrast is estimable separately from preparation batch. The batch-adjusted analysis identifies **26 panel-responsive candidates**. Independent validation confirms **10 of 10 archived nominees**, a concordance of **1.00**, exceeding the facility release requirement of 0.75. The validation gate therefore supports issuing a candidate list, with explicit labels distinguishing panel calls from independently confirmed candidates. It does not establish that every panel call has been validated.

## Library quality and design
All 12 libraries pass; 0 fail. Each arm retains 6 usable biological replicates. The minimum assigned-read count is 9,307,000, and the minimum mapping rate is 0.863. Resequencing is not indicated by these metrics.

There are 2 preparation batches. The first contains 5 controls and 1 treated library; the second contains 1 control and 5 treated libraries. The model matrix has rank 3 for 3 columns: this is imbalance, not complete confounding. Batch is required in the analysis, and sparse cross-arm representation within batches limits precision and robustness.

## Expression analysis
Counts were normalized by median ratios to gene geometric means with a pseudocount, then log-transformed and fitted gene by gene with treatment and preparation batch. Treatment t tests used residual degrees of freedom 9; Benjamini–Hochberg adjustment covered all 400 panel genes. Calls require adjusted p below 0.05 and absolute log fold change at least 1.0. The reported effects use base-two logs. This is an approximate log-scale linear analysis, not a fitted negative-binomial count model; a production count-model sensitivity check is recommended before external dissemination.

Adding batch conditional on treatment accounts for 0.3203 of total centered log-expression variation. This is an incremental sum-of-squares fraction, not a causal variance estimate. The analytical safeguard was to include batch rather than report an unadjusted arm comparison. No physical study intervention was performed, and no before/after improvement was measured.

### Panel calls
Positive effects indicate higher expression under compound exposure. The table is the computed panel list, not a claim of validation for every row.

| Gene | Log fold change | BH adjusted p |
|---|---:|---:|
| G0010 | 2.327 | 0.00343535 |
| G0012 | -2.780 | 0.00576734 |
| G0017 | -1.495 | 0.00758214 |
| G0026 | 2.043 | 0.000227698 |
| G0075 | -2.122 | 0.00419052 |
| G0078 | 2.112 | 0.00553382 |
| G0086 | -1.742 | 0.00758214 |
| G0112 | 2.106 | 0.010275 |
| G0133 | -1.563 | 0.00649232 |
| G0141 | 2.060 | 0.00576734 |
| G0146 | -1.626 | 0.00468346 |
| G0163 | 1.933 | 0.00553382 |
| G0183 | 1.561 | 0.0018049 |
| G0213 | -2.580 | 0.000959267 |
| G0228 | -1.641 | 0.0012684 |
| G0236 | 2.297 | 0.000681377 |
| G0247 | -3.068 | 0.000548994 |
| G0291 | -1.532 | 0.012282 |
| G0302 | -1.914 | 0.00126454 |
| G0311 | 1.708 | 0.0208407 |
| G0318 | 2.443 | 0.000505069 |
| G0342 | -2.001 | 0.0190568 |
| G0355 | -2.311 | 0.000979585 |
| G0358 | -2.721 | 0.000227698 |
| G0372 | -2.225 | 0.00576734 |
| G0373 | 1.852 | 0.00474271 |

## Independent validation
Two-sided Welch tests were run on independent qPCR log-expression values. Confirmation required nominal significance and agreement with the archived expected direction. All archived nominees confirmed. Of these, 9 also pass the present panel calling rule. The archived nominee G0295 validates by qPCR but is not a panel call under this analysis; it should be described as validation-supported rather than silently inserted into the panel list. The validation subset was supplied by the archive and was not selected anew from this model. The untested remainder needs additional validation if individual confirmation is required.

## Functional interpretation
Using the assayed panel as the background, upper-tail hypergeometric tests with BH adjustment across 12 annotated sets identify 1 significant sets.
- SET03: overlap 10; adjusted p 3.41892e-05.

Enrichment describes this targeted panel, not the whole transcriptome, and is not evidence of a causal pathway mechanism. Annotation labels alone do not support a biological pathway name.

## Facility action and sustainment
Release a clearly qualified panel candidate list with a separate validation-status column and preserve the archived nomination set. Reconcile the nomination/model discrepancy before external communication. Review count-model sensitivity and investigate any candidate whose status changes. Do not remove batch merely because the contrast is mathematically estimable.

For the next experiment, randomize and balance both arms within each preparation batch, retain sample-to-batch provenance, and prospectively specify the analysis and validation nomination rules. Hold future releases at the same library-quality, replication, estimability, adjusted-significance, effect-size and validation gates. Preserve raw batches, scripts, gene-level results and the analysis trace for reproducibility. No data request was denied; the limits here are model approximation, batch imbalance and incomplete per-candidate validation coverage, not a missing released batch.
