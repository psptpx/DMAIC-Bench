# Compound expression study: decision for the principal investigator

## Where the study stands
The libraries are usable and the intended treatment contrast is estimable separately from preparation batch. The batch-adjusted analysis identifies **26 candidate responding genes**, not independently validated biological effects. Retain the existing libraries; sequencing QC does not justify resequencing this study.

## Library fitness and design
All 12 libraries passed the facility's assigned-read and mapping requirements; 0 failed. Each arm retains 6 usable biological replicates. The lowest assigned-read count was 9,307,000, and the lowest mapping fraction was 0.863.

The sample sheet contains 2 preparation batches. The first batch contains 5 controls and 1 treated library; the other contains 1 control and 5 treated libraries. The intercept–treatment–batch model has rank 3 for 3 columns: treatment and batch are not completely confounded. Nevertheless, their imbalance limits precision and makes an arm-only comparison inappropriate. Estimability is not proof of random assignment or absence of other confounders.

## Analysis and findings
Counts were matched to sample-sheet labels. Median-ratio library size factors were estimated using genes positive across libraries. Gene-wise ordinary least-squares models of log-transformed normalized counts with a unit pseudocount included treatment and preparation batch. Treatment coefficients are approximate log-fold changes on this transformed scale. Tests used residual degrees of freedom 9; Benjamini–Hochberg adjustment covered all 400 panel genes. Calls require adjusted p < 0.05 and absolute log-fold change on the base-two scale >= 1.

Adding batch after treatment removed a fraction 0.558854 of the aggregate treatment-only residual sum of squares. This is a partial batch association, not the fraction of all biological variation caused by preparation. The preparation imbalance is therefore a material analytical concern, not a reason to pretend the contrast is impossible.

There are 11 increased and 15 decreased candidates. Positive coefficients denote higher expression under compound treatment.

| Gene | Adjusted log-fold change (base two) | BH adjusted p |
|---|---:|---:|
| G0010 | 2.328187 | 0.00348009 |
| G0012 | -2.778255 | 0.00573616 |
| G0017 | -1.493873 | 0.0074802 |
| G0026 | 2.044361 | 0.000239008 |
| G0075 | -2.120177 | 0.00446389 |
| G0078 | 2.113263 | 0.00542583 |
| G0086 | -1.740247 | 0.0074802 |
| G0112 | 2.107373 | 0.0102943 |
| G0133 | -1.561886 | 0.00637517 |
| G0141 | 2.061294 | 0.00573616 |
| G0146 | -1.624495 | 0.00465591 |
| G0163 | 1.934311 | 0.00542583 |
| G0183 | 1.562777 | 0.00196284 |
| G0213 | -2.580055 | 0.000928349 |
| G0228 | -1.639721 | 0.0013284 |
| G0236 | 2.298418 | 0.000664003 |
| G0247 | -3.066504 | 0.000600676 |
| G0291 | -1.530160 | 0.0117582 |
| G0302 | -1.912530 | 0.00125354 |
| G0311 | 1.709912 | 0.020818 |
| G0318 | 2.444797 | 0.000500536 |
| G0342 | -1.999194 | 0.0190084 |
| G0355 | -2.309142 | 0.00104298 |
| G0358 | -2.719620 | 0.000239008 |
| G0372 | -2.223932 | 0.00573616 |
| G0373 | 1.854038 | 0.00500506 |

The complete panel results are in `gene_results.csv`; exact numerical outputs and analysis decisions are in `trace.json`. Genes not listed did not meet both calling criteria in this analysis; that is not evidence of no response.

## What changed, what it achieved, and limits
The analytical approach explicitly conditions on preparation batch rather than pooling arms indiscriminately. It yields an estimable adjusted contrast and the candidate list above. No laboratory intervention was performed, and no before/after improvement was measured. The archive supplied no follow-up validation or monitoring measurements in response to our requests; the request was not routable, rather than a confirmed denial of an existing batch. Conclusions stop at this study's model-based candidates, not validated mechanism or demonstrated process improvement.

The log-expression model assumes approximately homoscedastic independent errors and a common additive batch effect. It is not a negative-binomial count model, and residual assumptions and treatment-by-batch heterogeneity were not formally evaluated. Median-ratio normalization assumes a reasonably stable reference across panel genes. The targeted panel and batch imbalance warrant independent confirmation before consequential biological decisions.

## Facility actions and how to hold the gains
Have the analysis lead review the candidate list with a dispersion-aware count-model sensitivity analysis and validate selected responses in independently prepared biological material using an orthogonal assay. Do not claim validation until measurements exist. Rebalance future preparation runs so both arms are represented comparably within each batch; randomize preparation order and preserve batch identifiers.

Make library QC and post-QC design-rank checks mandatory release gates. Require a batch term whenever preparation spans batches, retain full adjusted panel results and versioned scripts, and have the core lead review arm-by-batch balance before library preparation. Archive subsequent validation and routine QC measurements before assessing whether these procedural changes improve reproducibility. No improvement magnitude or sustained-control claim can yet be computed.
