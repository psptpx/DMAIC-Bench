# Compound expression study: decision for the principal investigator

## Executive decision
The libraries are usable and the intended comparison is estimable, provided preparation batch is included. The batch-adjusted analysis identifies **31 responding genes** on the targeted panel: 10 higher and 21 lower in treated cells. These are model-based relative-expression findings, not proof of mechanism or absolute cellular RNA changes.

## Library fitness and design
All 12 libraries passed the facility's read-depth and mapping rules; 0 failed. Each arm retains 6 usable biological replicates. The lowest assigned read count was 9,307,000, and the lowest mapping rate was 0.863. No exclusion or resequencing was necessary on these metrics.

There are 2 preparation batches. The first contains 5 controls and 1 treated library; the second contains 1 control and 5 treated libraries. This is strongly imbalanced, but not completely confounded. The intercept/batch/treatment matrix has rank 3 for 3 columns. Both arms occur within each batch, permitting a treatment contrast separately from batch. The sparse overlap makes inference less robust than a balanced allocation.

## Analysis and results
The full count matrix was normalized to counts per million using each library's panel count sum, then log transformed with a unit pseudocount. Each gene was fitted by ordinary least squares with additive batch and treatment terms. Treatment coefficients are treated-minus-control log fold changes on the base-two scale. Two-sided Student tests used 9 residual degrees of freedom. Benjamini–Hochberg adjustment covered all 400 panel genes, with calls requiring adjusted p < 0.05 and absolute log fold change >= 1.0.

The incremental batch sum of squares after treatment adjustment, divided by total centered log-expression sum of squares across the panel, was 0.297275. This is a descriptive batch-associated fraction, not a random-effects variance estimate or proof of technical causation. The imbalance is why ignoring batch would risk attributing batch-associated differences to treatment. Batch adjustment was used regardless of this descriptive magnitude.

### Called genes
Positive coefficients indicate higher relative expression after treatment; negative coefficients indicate lower relative expression.

| Gene | Adjusted log fold change | BH-adjusted p |
|---|---:|---:|
| G0010 | 1.9946 | 0.0130414 |
| G0012 | -3.1370 | 0.00408562 |
| G0017 | -1.8358 | 0.00113627 |
| G0026 | 1.7154 | 0.000390455 |
| G0075 | -2.4632 | 0.00104535 |
| G0078 | 1.7776 | 0.0161968 |
| G0086 | -2.0926 | 0.00316413 |
| G0108 | -1.9159 | 0.0217568 |
| G0112 | 1.7781 | 0.0314729 |
| G0117 | -1.2509 | 0.00649768 |
| G0133 | -1.9177 | 0.00408562 |
| G0136 | -1.2694 | 0.0324667 |
| G0141 | 1.7241 | 0.0161968 |
| G0146 | -1.9790 | 0.000926962 |
| G0163 | 1.5963 | 0.0161968 |
| G0183 | 1.2295 | 0.00677679 |
| G0213 | -3.0844 | 0.000323849 |
| G0228 | -1.9811 | 0.000550042 |
| G0236 | 1.9613 | 0.00104535 |
| G0247 | -3.4240 | 0.000323849 |
| G0291 | -1.8718 | 0.00408562 |
| G0295 | -2.5769 | 0.0189973 |
| G0302 | -2.2766 | 0.000323849 |
| G0318 | 2.1055 | 0.000390455 |
| G0342 | -2.3567 | 0.00986935 |
| G0345 | -1.8375 | 0.0290334 |
| G0351 | -1.4875 | 0.0449036 |
| G0355 | -2.6555 | 0.000323849 |
| G0358 | -3.0827 | 5.80453e-05 |
| G0372 | -2.5830 | 0.00267104 |
| G0373 | 1.5176 | 0.0189973 |

## What changed, what was achieved, and remaining uncertainty
The analysis explicitly separated the treatment and preparation-batch terms rather than pooling arms without adjustment. No laboratory intervention was made. The achieved output is an estimable, batch-adjusted candidate-gene list; an improvement in laboratory performance has not been demonstrated. Noncalled genes are not established as unchanged.

The model assumes independent biological replicates, additive effects, and adequately behaved log-scale errors. No treatment-by-batch interaction or count-dispersion model was fitted, and residual diagnostics were not performed. Total-count normalization on a targeted panel assumes the panel provides a sufficiently stable relative scale; widespread coordinated expression shifts could violate that assumption. The list should therefore be treated as analysis-model-dependent and confirmed using a count-based or precision-weighted workflow and alternative robust normalization before high-stakes decisions. No gene annotations or functional validation were supplied, so biological pathways and mechanism cannot be concluded here.

All steward-listed data batches were obtained; no requested batch was denied. Follow-up experimental evidence and evidence that a process change works were not supplied or computed, and conclusions do not extend to those outcomes.

## Facility action and control plan
- Retain these libraries; sequencing failure is not the barrier identified here.
- Have the bioinformatics lead independently review normalization, dispersion/variance assumptions, and influential libraries before releasing final biological claims. Preserve batch in every treatment model.
- Confirm prioritized candidates using independent biological material and an orthogonal assay; select both expression directions and include suitable reference controls.
- For future preparations, distribute both arms evenly across batches and randomize preparation order. Record allocation before library preparation and require an estimability check before sequencing.
- Hold the workflow through mandatory library-QC gates, a retained-replicate check, a design-rank check, and versioned analysis with fixed calling rules. Reassess after any sample exclusion.

## Audit trail
`trace.json` contains the sequential computed results, including every gene's coefficient and p-values. `gene_results.csv` is the complete panel result table. The analysis scripts and steward-released JSON batches are retained alongside these files. Numeric table entries are rounded displays of trace outputs; gene labels are archive identifiers.
