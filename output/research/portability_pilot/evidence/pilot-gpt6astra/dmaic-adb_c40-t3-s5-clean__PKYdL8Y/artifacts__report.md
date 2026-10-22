# Compound expression study: decision for the principal investigator

## Where the study stands
The libraries are usable, and the intended comparison is estimable after preparation-batch adjustment. However, the analysis performed here calls **0 responding genes**. This is not evidence that the compound has no biological effect: the imbalanced design limits precision and the gene-level analysis is exploratory.

## Library quality
All 12 libraries pass the facility's assigned-read and mapping-rate criteria; 0 fail. The retained arms contain 6 control and 6 treated biological replicates, satisfying the replication gate. The lowest assigned-read count is 9,194,000 and the lowest mapping rate is 0.865. No library exclusion or QC-driven resequencing is warranted by these metrics.

## Design and the source of uncertainty
There are 2 preparation batches. The first contains 5 controls and 1 treated library; the other contains 1 control and 5 treated libraries. Both arms occur within each batch. The intercept–treatment–batch design has rank 3 for 3 columns, so treatment is not perfectly confounded with batch. Nevertheless, the imbalance makes treatment estimates depend heavily on the sparsely represented arm in each batch.

The incremental batch sum of squares after treatment, divided by total centered transformed-expression sum of squares, is 0.377496. This is a descriptive batch-associated fraction, not a causal variance-component estimate. It supports retaining batch in the model; ignoring it could attribute preparation differences to the compound. These data do not establish the physical cause of the batch association.

## Gene analysis and interpretation
Counts were normalized by median ratios over genes positive in every library, then transformed by a base-two logarithm after adding a pseudocount of 1. Each of 400 genes was fitted with an intercept, treatment and preparation batch. Residual t tests used 9 residual degrees of freedom; Benjamini–Hochberg correction covered the entire panel. Calls required adjusted p < 0.05 and absolute log fold change on that scale >= 1.0.

No genes meet both criteria. The complete estimates, unadjusted probabilities, adjusted probabilities and call flags are in `gene_results.tsv`. This is a transparent log-expression linear-model analysis, not a count likelihood or empirical-Bayes model. Normalization assumes a sufficiently stable reference across the panel, and ordinary residual tests assume suitable transformed residual behavior. Those assumptions have not been established by diagnostic testing here. The result should therefore be treated as a batch-adjusted exploratory screen, not definitive evidence of absence or a validated clinical conclusion.

## What changed, what it achieved, and what happens next
The analysis explicitly separates treatment from preparation batch rather than using an unblocked arm comparison. This yields an estimable adjusted contrast and no supported gene calls under the stated implementation. An unblocked comparison was not run, so no numerical claim about removed false positives is made. No wet-lab process or experimental allocation was changed, and no improvement or follow-up outcome has been measured.

Before a final biological decision, the facility should review normalization and residual diagnostics and confirm findings using a validated batch-adjusted count-based or precision-weighted expression pipeline. Avoid selecting a model simply to obtain significant genes. Validate any subsequently supported candidates independently. If stronger sensitivity is needed, collect additional independent biological replicates with arms balanced and randomized within preparation batches; sequencing the same imbalanced allocation more deeply does not correct allocation imbalance.

For ongoing control, preserve the sample sheet and batch identifiers, enforce library-quality and retained-replication gates before analysis, check design rank before committing libraries to sequencing, and retain batch terms whenever multiple batches are present. Archive the scripts, full gene results and decision trace with the study. All currently listed steward batches were obtained; no requested batch was denied. Prospective validation and process-improvement effectiveness remain unmeasured, not inferred.

## Audit trail
`trace.json` records the computed QC, design-rank, batch-association and blocked-expression results. `analyze.py`, `design.py` and `expression.py` reproduce the calculations from the released JSON batches. Numerical values in this report are drawn from the trace outputs.
