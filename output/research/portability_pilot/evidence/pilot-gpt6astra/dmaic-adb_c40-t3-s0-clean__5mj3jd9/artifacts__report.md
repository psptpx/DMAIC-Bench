# Compound-response study: decision report

## Executive conclusion
The libraries can support the planned comparison. All 12 libraries pass facility QC; 0 fail. Both arms retain 6 biological replicates, exceeding the required 3. The preparation design is not confounded with treatment. Under the explicitly described log-scale analysis, 39 of 400 genes meet the facility calling rules: 23 increased and 16 decreased in treated cells.

These are expression-response candidates, not evidence of therapeutic efficacy or a demonstrated molecular mechanism. Confirmation should precede major biological or operational decisions.

## Library fitness and design
Libraries were required to have at least 5,000,000 assigned reads and mapping rate at least 0.7. The observed minima were 11,363,000 assigned reads and 0.866. No exclusion or resequencing is indicated by these rules.

All retained samples share 1 preparation batch. The intercept-and-treatment design has rank 2 for 2 columns. Both arms occur in the shared batch, so the treatment contrast is estimable. There is no varying batch term to fit. Between-batch variability cannot be estimated from this design, and generalization across preparation batches remains untested.

## Expression method and results
Sample identifiers were matched to the retained libraries. Depth normalization used median count ratios to each gene's geometric mean, using genes with positive counts in every retained library to estimate the size factors. Factors ranged from 0.746276 to 1.259071. This assumes that most panel genes do not undergo a coordinated directional shift; without external controls, absolute global expression changes are not identifiable through this normalization.

The analysis transformed normalized counts with log base two after adding a pseudocount of 1. Each gene was compared using a two-sided Welch test on transformed expression. Fold change below means the treated-minus-control mean on that log scale, not the logarithm of the arithmetic mean count ratio. Benjamini–Hochberg adjustment covered all 400 panel genes, with no significance-based prefilter. Calls require adjusted p < 0.05 and absolute log fold change >= 1.0.

This is an approximate log-scale analysis, not a fitted negative-binomial count model. Small-sample distribution assumptions and low-count transformation effects remain limitations. A validated count-model sensitivity analysis was not performed; it should be completed before treating the candidate list as a final production release. Noncalled genes are not established to have no effect.

### Called genes
Positive fold change denotes increased expression with compound. All displayed numerical results are rounded from trace outputs.

| Gene | Log fold change (base two) | BH adjusted p |
|---|---:|---:|
| G0006 | 1.9872 | 0.00251173 |
| G0007 | 1.4759 | 0.00972368 |
| G0010 | 2.0965 | 0.000436405 |
| G0037 | 1.6527 | 0.000302091 |
| G0039 | 2.2193 | 0.00222985 |
| G0052 | -2.1467 | 0.000170353 |
| G0061 | 2.4538 | 0.000123846 |
| G0101 | 2.0832 | 9.91648e-05 |
| G0107 | 1.8814 | 0.000261721 |
| G0110 | 2.0384 | 0.000125673 |
| G0114 | -1.3805 | 0.000516081 |
| G0115 | -2.1952 | 5.78786e-05 |
| G0118 | 2.0162 | 0.00149903 |
| G0124 | -2.3894 | 0.000179529 |
| G0131 | 2.5321 | 7.46051e-05 |
| G0149 | -1.4079 | 0.0116593 |
| G0153 | 1.8747 | 0.000349559 |
| G0154 | -2.3309 | 0.000478354 |
| G0155 | -1.7906 | 0.00730432 |
| G0187 | -2.4663 | 0.000170353 |
| G0194 | 1.9916 | 0.000101724 |
| G0212 | 1.4535 | 0.00375706 |
| G0247 | -2.3326 | 7.46051e-05 |
| G0260 | 1.9499 | 0.000701775 |
| G0276 | -2.4610 | 0.000181026 |
| G0277 | 3.0078 | 7.46051e-05 |
| G0279 | 2.1448 | 7.46051e-05 |
| G0280 | -1.6525 | 0.0018552 |
| G0287 | 2.1640 | 7.46051e-05 |
| G0293 | 2.2188 | 0.0011138 |
| G0299 | -2.8670 | 0.000122656 |
| G0310 | 2.2098 | 0.000155153 |
| G0311 | -2.4575 | 0.00522944 |
| G0314 | -2.6218 | 9.91648e-05 |
| G0331 | 2.4549 | 0.000563829 |
| G0372 | -2.1405 | 0.0233887 |
| G0374 | 1.9381 | 0.00311027 |
| G0383 | 1.3345 | 0.00745304 |
| G0394 | -1.3021 | 0.00559529 |

## What changed, what it achieved, and what happens next
No experimental preparation, library, or sample allocation was changed. The analytical changes were depth normalization and panel-wide multiplicity control; the resulting calls above are conditional on that normalization and testing framework. The observed comparison is not attributable to a between-arm preparation-batch split, because preparation batch is shared. Neither normalization nor shared batch rules out unrecorded biological or handling differences.

The facility should retain these libraries rather than resequence for QC reasons, review the full effect-size and adjusted-p table, and confirm priority candidates using an orthogonal assay and independent biological material. The bioinformatics lead should run a validated count-based differential-expression workflow as sensitivity confirmation, checking low-count behavior and the normalization assumption. The study lead should review allocation and handling records before asserting a causal compound mechanism.

For future work, keep both arms represented within preparation batches and preserve balanced allocation, blinded handling where feasible, and sample-to-library provenance. Hold performance through automated library-QC and replication gates, a pre-analysis design-rank check, locked calling thresholds, and versioned analysis scripts and count tables. Do not select a model or thresholds to maximize the call count.

## Audit and limits
All requested record batches were supplied; no step was denied by the steward. No outside study-fact consultation was needed. No intervention outcome or independent validation data were supplied or computed, so no claim of successful operational improvement or biological confirmation is made. Between-batch variance and validated count-model sensitivity remain uncomputed, rather than inferred from this single-batch study.

`trace.json` contains the QC, identifiability, and expression computations in execution order. `gene_results.csv` includes every tested gene, including noncalls; the scripts and steward-released JSON records preserve reproducibility. Numerical entries in this report map to the corresponding QC, design, or expression outputs in the trace.
