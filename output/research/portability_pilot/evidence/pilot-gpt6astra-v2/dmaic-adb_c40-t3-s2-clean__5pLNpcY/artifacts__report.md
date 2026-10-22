# Compound-response study: PI decision

## Executive conclusion
The libraries are usable and the treatment contrast is estimable. The batch-adjusted analysis identifies 26 provisional responding genes. Independent qPCR confirms 10 of 10 supplied nominations: concordance 1.00, exceeding the facility requirement of 0.75. The validation gate passes; issue a clearly labelled panel candidate list, not a claim that every panel hit was independently validated.

## Quality and design
All 12 libraries pass QC; 0 fail. Each arm retains 6 usable biological replicates. There is no QC reason to re-sequence. Across 2 preparation batches, the design matrix has rank 3 for 3 columns. The first batch has 5 controls and 1 treated library; the other has the reciprocal allocation. Treatment and batch are correlated but not perfectly confounded. The sparse within-batch overlap limits precision.

## Analysis and panel candidates
Median-ratio size factors were estimated from the panel. Linear models of normalized log expression included treatment and preparation batch, with residual degrees of freedom 9. Two-sided treatment tests were BH-adjusted across 400 genes. Calls require adjusted p < 0.05 and absolute log fold change >= 1.0. This is an approximate log-expression model rather than a count-likelihood or moderated-variance pipeline. Normalization assumes most panel genes are not globally shifted. Use count-model sensitivity analysis before translational prioritization.
Incremental batch variation conditional on treatment accounts for 0.3178 of total centered normalized log-expression variation. Batch adjustment addresses a material technical component; this fraction is not proof of a particular laboratory mechanism. No laboratory intervention has been performed.

| Gene | Adjusted treatment log fold change | BH adjusted p |
|---|---:|---:|
| G0010 | 2.3309 | 0.0035546 |
| G0012 | -2.7917 | 0.0057017 |
| G0017 | -1.4961 | 0.0074262 |
| G0026 | 2.0498 | 0.00023269 |
| G0075 | -2.1232 | 0.0042935 |
| G0078 | 2.1148 | 0.0053806 |
| G0086 | -1.7496 | 0.0074262 |
| G0112 | 2.1126 | 0.01032 |
| G0133 | -1.5738 | 0.0062828 |
| G0141 | 2.0619 | 0.0057017 |
| G0146 | -1.6353 | 0.0046586 |
| G0163 | 1.9344 | 0.0053806 |
| G0183 | 1.5657 | 0.0018917 |
| G0213 | -2.6828 | 0.00097579 |
| G0228 | -1.6418 | 0.0013313 |
| G0236 | 2.2991 | 0.00066114 |
| G0247 | -3.0789 | 0.00057308 |
| G0291 | -1.5323 | 0.012049 |
| G0302 | -1.9286 | 0.0012605 |
| G0311 | 1.7170 | 0.020543 |
| G0318 | 2.4442 | 0.00050552 |
| G0342 | -2.0121 | 0.019807 |
| G0355 | -2.3144 | 0.0010164 |
| G0358 | -2.7352 | 0.00023269 |
| G0372 | -2.2368 | 0.0057017 |
| G0373 | 1.8551 | 0.0049074 |

## Independent validation
Welch tests compared independent qPCR log-expression replicates between arms; confirmation required nominal p < 0.05 and agreement with the archived expected direction. All supplied nominations show down-regulation. Of these nominations, 9 overlap this analysis’s called genes. G0295 is qPCR-confirmed but does not pass this panel model’s joint calling criteria; do not silently add it to the model-derived list. Validation supports the nominated leading signals, not an estimated confirmation rate for untested hits.

| Nominated gene | qPCR treatment difference | p |
|---|---:|---:|
| G0247 | -2.9718 | 5.4395e-05 |
| G0012 | -2.3625 | 0.0023676 |
| G0213 | -2.5582 | 4.5467e-05 |
| G0358 | -2.3258 | 4.6272e-05 |
| G0355 | -1.7275 | 0.0077008 |
| G0372 | -2.3050 | 6.9439e-06 |
| G0295 | -1.6807 | 0.00081607 |
| G0075 | -2.1645 | 0.0015209 |
| G0342 | -1.7223 | 0.000218 |
| G0302 | -1.9243 | 0.00014595 |

## Functional context
Using the 400-gene measured panel as background, hypergeometric overrepresentation testing with BH across 12 annotated sets finds 1 significant sets. These are exploratory panel-limited associations, not pathway activation or causal mechanism claims.
- SET03: adjusted p 3.4189e-05; overlap 10 called genes.

## Action and control plan
Retain the usable libraries and the batch-adjusted analysis. Release the panel list with explicit validation coverage and methodological limitations; prioritize the overlapping independently confirmed candidates. Reconcile the archived nomination rule with the current analysis before treating the nomination set as identical to the panel-call set. Expand independent validation to untested calls and examine count-model sensitivity and expression residuals before consequential biological claims.
For future work, randomize both arms evenly within preparation batches, preserve sample and batch provenance, and pre-register normalization, inference, multiplicity and validation rules. Hold release to automated QC, full-rank design checks and the validation gate. Archive the raw steward batches, analysis script, gene-level results and trace so the same rules can be rerun. No corrective laboratory change or downstream biological outcome has yet been demonstrated.
All requested batches were supplied; there is no denied-data gap. Quantities in this report are derived from the scalar outputs in trace.json. Detailed gene-level results are in gene_results.csv.
