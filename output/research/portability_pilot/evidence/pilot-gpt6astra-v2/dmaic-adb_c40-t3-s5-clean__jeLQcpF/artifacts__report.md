# Compound-expression study: disposition

## Executive conclusion
The sequencing libraries are usable, and the compound-versus-vehicle contrast is estimable separately from preparation batch. However, the batch-adjusted analysis found **0 qualifying genes**. No compound-responsive gene list should be issued. This is absence of sufficient evidence under the stated calling rules, not proof that the compound has no biological effect.

## Library quality and experimental design
All **12** libraries passed the facility's assigned-read and mapping-rate rules; **0** failed. Both arms retain **6** usable biological replicates, so resequencing is not required on library-quality grounds.

There are **2** preparation batches. The first holds **5** controls and **1** treated library; the second holds **1** control and **5** treated libraries. The intercept, batch and treatment model has rank **3** for **3** columns. Thus batch and treatment are not completely confounded, but their strong imbalance reduces precision and makes an unadjusted arm comparison unsuitable for compound attribution.

## Expression analysis
The analysis tested **400** genes using median-ratio count normalization, a pseudocount log transformation, and gene-wise ordinary least-squares models including preparation batch and treatment. Treatment tests used residual degrees of freedom **9** and Benjamini–Hochberg correction across the tested panel. Calling required adjusted p below **0.05** and absolute log fold change on the base-two scale at least **1.0**.

The batch term's unique sum of squares after treatment, divided by total centered transformed-expression sum of squares, was **0.37339764556466926**. This is a descriptive partial variance fraction, not a causal estimate or a principal-component variance fraction. It supports treating preparation batch as an important source of expression variation.

No genes passed both calling thresholds. Full per-gene estimates and adjusted p values are retained in `gene_results.json`. The fitted model is a log-linear approximation, not a dispersion-moderated count model; a production-grade count-model sensitivity analysis would strengthen any final negative interpretation. No unadjusted gene list was produced or used.

## Validation and downstream boundary
The released validation archive contains **0** nominated candidates and **0** qPCR records. Therefore validation concordance cannot be computed: the denominator is empty. It is neither a failed validation experiment nor evidence of successful confirmation. There is no validated candidate list to release.

Panel annotation was requested but **locked**, not denied, because a computed passing validation concordance had not been declared. An undefined concordance was not replaced with an invented value. Gene-set enrichment was not run, and no pathway conclusion is supported. No batch was reported as genuinely nonexistent by a steward denial.

## Facility action and control
Retain the usable libraries and preserve the batch-adjusted analysis as the current result. The analytical change was to explicitly account for preparation batch rather than attribute between-batch expression variation to the compound; the achieved result is an estimable comparison with no qualifying response calls. No laboratory intervention or successful corrective experiment has been demonstrated.

Before interpreting this as a definitive negative study, perform a count-based, dispersion-aware sensitivity analysis and assess precision for biologically relevant effects. If further experimentation is warranted, randomize and balance both arms within each preparation batch, preserving biological independence. Extra sequencing depth alone will not repair allocation imbalance.

Hold release under the facility's QC, estimability and independent-validation gates. If future analysis nominates candidates, obtain independent directional qPCR confirmation before issuing a list or proceeding to enrichment. Archive sample-sheet checks, model specifications, complete gene results and validation denominators alongside each release decision. The executable scripts and `trace.json` preserve the computations supporting this report.
