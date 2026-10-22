# Compound-expression study: disposition

## Executive decision
The sequencing libraries are usable and the treatment comparison is identifiable after preparation-batch adjustment. However, the batch-adjusted analysis identifies **0 qualifying genes**. Do not issue a compound-responsive candidate list. This is a lack of qualifying evidence, not proof that the compound has no biological effect.

## Library quality and design
All 12 libraries pass the facility's joint thresholds of at least 5,000,000 assigned reads and mapping rate at least 0.7. There are 0 failed libraries, leaving 6 controls and 6 treated replicates; the required minimum is 3 per arm. No library was excluded and QC alone does not require resequencing.

The usable libraries span 2 preparation batches. The first batch contains 5 controls and 1 treated library; the other contains 1 control and 5 treated libraries. The intercept, treatment and batch design has rank 3 for 3 columns. Thus treatment is not completely confounded with batch, but overlap is thin and the allocation is strongly imbalanced. An unadjusted arm comparison would not answer the intended biological question reliably.

## Expression analysis and interpretation
Counts were normalized using gene-wise geometric means and sample median-ratio size factors, then transformed to base-two logarithms with pseudocount 1. Each gene was fitted by ordinary least squares with treatment and preparation batch. Treatment tests were two-sided, with 9 residual degrees of freedom; Benjamini–Hochberg adjustment covered all 400 genes. The calling rule was adjusted p < 0.05 and absolute log-fold change >= 1.0.

There were **0 calls**, so there are no gene names to nominate. Full gene-level estimates and adjusted p-values are saved in `de_results.json`, with numeric results also in `trace.json`. These are log-expression approximations rather than a negative-binomial count-model analysis; small effective within-batch comparisons limit precision.

The incremental batch sum of squares, conditional on treatment, divided by total centered log-expression sum of squares was 0.373379. This documents substantial preparation-associated expression variation, not a causal estimate of a technical mechanism. Batch adjustment was the analytical safeguard applied; no physical processing change or repeat experiment was performed. A causal explanation for the preparation differences cannot be established from these records.

## Independent validation and downstream limits
The validation archive explicitly records no nominated candidates: 0 nominations and 0 confirmations. There are no qPCR measurements to analyze. Concordance has an empty denominator and cannot be computed; it must not be substituted with a passing or failing fraction. The facility requires concordance at least 0.75, based on validation p < 0.05 in the nominated direction. No list has been validated, and no claim of validation failure is made either.

The steward withheld gene-set annotation because the validation-concordance gate was not satisfied. This was a locked prerequisite, not a declaration that annotation does not exist. Enrichment was not computed, and no pathway conclusion is supported. No fabricated concordance was declared to bypass that gate.

## Facility action and sustainment
Retain the libraries and preserve this analysis as a no-candidate result. Do not resequence solely to repair a QC problem that is absent. Before a new biological conclusion is sought, balance and randomize both arms within every preparation batch and expand biological replication where feasible. Review preparation records to investigate batch-associated variation; resequencing the same material alone would not repair allocation imbalance.

For a follow-up, pre-specify the batch-adjusted count-model workflow and calling rule, inspect dispersion and normalization diagnostics, and reserve independent material for directional qPCR confirmation of any future nominations. Hold candidate release until the validation gate is actually evaluable and passed. Preserve sample-to-batch provenance, enforce QC and design-rank checks before testing, and maintain versioned analysis scripts and an auditable release checklist. No improvement in experimental performance has yet been demonstrated; these are recommended controls, not completed interventions.

## Audit trail
`analyze.py`, `design.py`, `expression.py`, and `finish.py` reproduce the computations from the steward-released JSON batches. `trace.json` records the quantitative steps and routing decisions. No outside study-lead clarification was needed.
