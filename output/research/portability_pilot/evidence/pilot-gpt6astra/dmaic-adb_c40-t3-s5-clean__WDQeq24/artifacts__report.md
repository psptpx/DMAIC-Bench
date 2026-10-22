# Compound expression study: disposition

## Executive conclusion
The libraries are usable and the intended treatment comparison is estimable separately from preparation batch. However, batch and treatment are substantially imbalanced. The batch-adjusted analysis found **0 responding genes among 400 tested** under the facility's joint significance and effect-size rule. This is a lack of demonstrated response with this analysis, not proof that the compound has no biological effect.

## Library acceptance
All **12 libraries** pass; **0 fail**. Each arm retains **6 usable biological replicates**, exceeding the required **3**. Acceptance required assigned reads at least **5,000,000** and mapping rate at least **0.70**. The observed minima are **9,194,000 assigned reads** and **0.865 mapping rate**. No exclusions or QC-driven resequencing are warranted. These quantities are recorded in the QC step of `trace.json`.

## Design and preparation effects
There are **2 preparation batches**. The first contains **5 control and 1 treated** libraries; the second contains **1 control and 5 treated** libraries. Thus, both arms occur within each batch: the contrast is not completely confounded. The intercept, batch and treatment design has rank **3** for **3 columns**, leaving **9 residual degrees of freedom**. These results are recorded in the design step.

The pooled partial batch variance fraction is **0.551254**, calculated as the reduction in residual sums of squares after adding batch to the treatment-only model, divided by treatment-only residual sums of squares. This is a conditional, fixed-effect partial variance measure, not a random-effects variance component or proof of a specific laboratory mechanism. It supports retaining batch adjustment, as already required by the brief. The imbalanced allocation limits precision and makes an unadjusted arm comparison inappropriate.

## Gene results and interpretation
Counts were normalized by median ratios to per-gene geometric means, with positive-count genes used to estimate normalization factors. Gene-wise linear models were fitted to base-two log normalized counts with pseudocount **1**, including batch and treatment. Treatment coefficients estimate adjusted log fold changes. Residual-variance t tests were corrected across the complete panel using Benjamini–Hochberg adjustment.

The calling rule was adjusted p strictly below **0.05** and absolute log fold change at least **1**. No gene met this rule; the smallest adjusted p was **0.0588805**. Full per-gene estimates and adjusted p-values are in `gene_results.csv`, with their numeric counterparts in the expression step of `trace.json`.

This is an explicitly approximate log-linear analysis rather than a fitted negative-binomial count model. It assumes adequate log-scale variance behavior and a common treatment effect across batches. Median-ratio normalization also assumes a suitable stable reference distribution across the panel. The small within-batch arm overlap makes conclusions particularly sensitive to individual libraries and modeling assumptions. Consequently, the appropriate statement is that no compound-responsive gene is established by this analysis; neither equivalence nor absence of smaller effects has been demonstrated.

## What changed, what it achieved, and what happens next
The analytical change is to account for preparation batch rather than pool the arms indiscriminately. This yields an identifiable, batch-adjusted comparison and prevents preparation differences from automatically being attributed to treatment. An unadjusted gene analysis was not run, so no numerical claim is made about genes removed by adjustment. No laboratory intervention has been performed, and no improvement in experimental outcomes has been measured.

Before using this study for a consequential compound decision, the facility should review library-level influence and log-scale model diagnostics, and confirm the result with a validated count-based or precision-weighted expression workflow including batch. Any promising candidates should receive independent biological and orthogonal assay validation; the present results do not justify a validated responder list.

For the next experiment, randomize and balance both arms within preparation batches, retain adequate biological replication within each batch, and preserve the allocation sheet before library preparation. Merely sequencing the same imbalanced libraries more deeply would not repair the allocation. Hold the process by enforcing the existing read, mapping and usable-replication acceptance checks, checking design rank before gene testing, retaining batch in multibatch analyses, and applying the prespecified multiplicity and effect-size rules. Archive scripts, counts, sample identities, exclusions and gene-level results together for reproducibility.

All available study batches were obtained; none was denied. Independent validation and post-change experimental outcomes were not supplied or computed, so conclusions stop at the current observational, batch-adjusted analysis.
