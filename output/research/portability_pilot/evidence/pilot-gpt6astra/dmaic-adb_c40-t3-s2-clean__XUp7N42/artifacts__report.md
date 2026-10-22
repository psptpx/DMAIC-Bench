# Compound expression study: decision for the principal investigator

## Executive conclusion
The libraries support analysis and the intended comparison is estimable separately from preparation batch. The batch-adjusted analysis identifies **26 responding genes** under the stated decision rule, comprising 11 increases and 15 decreases. These are model-based candidates for confirmation, not proof of compound-specific mechanism.

## Library fitness and design
All 12 libraries passed the facility's assigned-read and mapping-rate gates; 0 failed. Each arm retained 6 usable biological replicates against a minimum requirement of 3. The lowest assigned-read count was 9,307,000, and the lowest mapping rate was 0.863. Re-sequencing is not indicated by these QC results.

There are 2 preparation batches. The first listed batch contains 5 control and 1 treated libraries; the other batch contains 1 control and 5 treated libraries. The intercept/treatment/batch design has rank 3 across 3 columns. Thus treatment is not completely confounded, but the allocation is strongly imbalanced and information distinguishing treatment from preparation relies on the cross-arm libraries within batches.

## Analysis and gene calls
Counts were normalized using median ratios to a geometric-mean reference, then log-transformed with a pseudocount. Per-gene ordinary least-squares models included an intercept, treatment and preparation batch. Unmoderated residual-variance t tests used 9 residual degrees of freedom; Benjamini–Hochberg adjustment covered all 400 genes. Calls require adjusted p < 0.05 and absolute log-fold change >= 1.0. Positive effects mean higher expression with compound.

Adding batch to a treatment-only model explained a pooled fraction 0.558854 of its residual transformed-expression sum of squares. This is a conditional descriptive measure, not a causal variance component. It supports avoiding a naive arm comparison; no treatment-only gene calls were made.

| Gene | Estimated log-fold change (base two) | Adjusted p |
|---|---:|---:|
| G0010 | 2.3282 | 0.00348009 |
| G0012 | -2.7783 | 0.00573616 |
| G0017 | -1.4939 | 0.0074802 |
| G0026 | 2.0444 | 0.000239008 |
| G0075 | -2.1202 | 0.00446389 |
| G0078 | 2.1133 | 0.00542583 |
| G0086 | -1.7402 | 0.0074802 |
| G0112 | 2.1074 | 0.0102943 |
| G0133 | -1.5619 | 0.00637517 |
| G0141 | 2.0613 | 0.00573616 |
| G0146 | -1.6245 | 0.00465591 |
| G0163 | 1.9343 | 0.00542583 |
| G0183 | 1.5628 | 0.00196284 |
| G0213 | -2.5801 | 0.000928349 |
| G0228 | -1.6397 | 0.0013284 |
| G0236 | 2.2984 | 0.000664003 |
| G0247 | -3.0665 | 0.000600676 |
| G0291 | -1.5302 | 0.0117582 |
| G0302 | -1.9125 | 0.00125354 |
| G0311 | 1.7099 | 0.020818 |
| G0318 | 2.4448 | 0.000500536 |
| G0342 | -1.9992 | 0.0190084 |
| G0355 | -2.3091 | 0.00104298 |
| G0358 | -2.7196 | 0.000239008 |
| G0372 | -2.2239 | 0.00573616 |
| G0373 | 1.8540 | 0.00500506 |

The complete tested-gene results are in `gene_results.csv`, with unrounded results recorded in `trace.json`. Genes not meeting the joint threshold are not established responders; this does not establish absence of an effect.

## Interpretation limits
The effect estimates approximate expression ratios on normalized, pseudocount-transformed counts. This is a log-linear analysis, not a negative-binomial or moderated count analysis. Its inference assumes suitable transformed residuals, common within-gene residual variance, independent biological replicates, a stable normalization reference and an additive batch effect. Residual diagnostics, alternative count-model sensitivity and treatment-by-batch interaction robustness were not established here. The imbalanced preparation allocation limits precision and makes model misspecification particularly consequential. Gene identities alone do not support pathway or mechanism claims.

All available study batches were supplied; no data request was denied. No independent validation or post-change production results were supplied or analyzed. Consequently this analysis cannot demonstrate replication of the candidates or an achieved operational improvement.

## Facility action and sustained control
The analytical change was to separate treatment from preparation batch in the model rather than attributing all arm differences to compound. This produced the candidate list above; no laboratory intervention was performed and no before/after improvement is claimed.

Do not discard or re-sequence usable libraries solely because of the batch imbalance. Have the facility analyst confirm the calls with a dispersion-aware count model and inspect residuals and influential cross-arm samples before external biological claims. Validate prioritized genes using independent biological material and an orthogonal expression assay.

For subsequent studies, the study lead and preparation team should randomize and balance both arms within every preparation batch, preserving biological independence. Before sequencing, require a signed sample-sheet review for estimability; after sequencing, retain automated library QC and replicate-count gates. Lock the normalization, batch-aware model and multiple-testing rule before examining treatment effects. Archive raw metrics, count tables, allocation records, analysis scripts and review decisions. Monitor future runs against the same gates and withhold gene claims whenever QC or estimability fails. Verify any claimed process improvement with newly collected balanced-run evidence rather than extrapolating from this analysis.
