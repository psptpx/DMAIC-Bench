# Compound-expression study: decision for the principal investigator

## Executive conclusion
The libraries are usable and the treatment contrast is estimable after adjusting for preparation batch. The batch-adjusted panel analysis identified **0 responding genes** under the facility's calling rules. Do not issue a compound-responsive candidate list. This is absence of qualifying evidence in this experiment, not proof that the compound has no biological effect.

## Library quality and design
All **12 libraries** passed the facility's assigned-read and mapping-rate rules; **0 failed**, leaving **6 usable replicates per arm**. The lowest assigned-read count was **9,052,000** and the lowest mapping rate was **0.868**. The replicate-retention requirement is satisfied, so technical QC does not mandate re-sequencing.

There are **2 preparation batches**. The first holds **5 controls and 1 treated library**; the second holds **1 control and 5 treated libraries**. Thus batch and treatment are imbalanced but not completely confounded. The intercept–treatment–batch design has rank **3** for **3 columns**, establishing a separately estimable treatment contrast. The sparse within-batch arm overlap limits precision and makes a batch-ignorant comparison inappropriate.

## Expression analysis and interpretation
I used median-ratio normalization and a pseudocount log transformation, then fitted gene-wise linear models with treatment and preparation batch. Treatment coefficients were tested with residual t tests, followed by Benjamini–Hochberg adjustment across the **400 genes**. Calls required both the facility's adjusted-significance and absolute-fold-change criteria. The models had **9 residual degrees of freedom**. Full gene statistics are in `gene_results.csv`; the executable calculation is in `expression.py`.

The incremental batch sum of squares beyond treatment, divided by total centered log-expression sum of squares, was **0.3727060798353606**. This is a descriptive batch-associated fraction, not a causal variance component. It shows substantial preparation-associated structure and supports including batch rather than attributing that structure to compound exposure.

The blocked analysis produced **0 qualifying genes**. No gene can therefore be nominated as compound-responsive from this analysis. This implementation is an approximate log-expression linear model, not a negative-binomial count model; its normalization assumes a sufficiently stable reference across the targeted panel. A count-aware sensitivity analysis would be appropriate before treating the negative result as definitive. No unadjusted candidate list was computed or released.

## Validation and downstream boundary
The released validation batch explicitly states that no candidates were nominated: it contains **0 candidate genes** and **0 qPCR records**. There are no validation measurements to analyze. Concordance is undefined for this empty cohort; it is neither a validation failure nor successful validation. There is no independently validated list to issue, and the validation conclusion stops here.

The gene-set annotation request was **locked**, not denied: release requires a qualifying computed validation concordance. I did not invent a rate to bypass that gate. Enrichment was not computed, and no pathway conclusion is supported. No requested batch was explicitly denied as nonexistent.

## Facility action and control plan
The analytical safeguard implemented here was explicit adjustment for preparation batch rather than an arm-only comparison. It achieved an interpretable treatment test while respecting the design; it did not produce qualifying candidates. No experimental redesign or re-sequencing was performed, and no before/after laboratory improvement is claimed.

Retain the current libraries and the negative, batch-adjusted result in the study record. Before commissioning additional sequencing, review biological exposure, assay sensitivity and the count-model sensitivity analysis. If greater sensitivity is needed, plan additional independent biological replication with both arms balanced and randomized within every preparation batch; deeper sequencing alone cannot repair the existing imbalance. Use prospective power planning rather than choosing a replication target from this negative result alone.

Hold the decision through documented sample QC, an arm-by-batch design review before library preparation, a prespecified normalization and batch-adjusted analysis, and independent directional qPCR confirmation before any future candidate list is released. Archive the released JSON, analysis scripts, gene results and trace together. Keep candidate release and pathway interpretation paused unless new evidence legitimately satisfies the validation gate.
