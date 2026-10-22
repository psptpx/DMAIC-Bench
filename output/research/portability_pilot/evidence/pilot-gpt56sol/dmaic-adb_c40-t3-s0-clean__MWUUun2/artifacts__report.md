# Compound-response study report

## Executive conclusion

The libraries can support a conclusion: **0 libraries failed QC**, and the control and treated arms each retain **6** usable biological replicates, above the required minimum of **3**. The intended treated-versus-control comparison is estimable. There is **1** preparation batch, and it contains **6** control and **6** treated libraries, so treatment is not confounded with preparation batch.

The count analysis tested **400** panel genes and called **40** compound-responsive genes under the facility rule of adjusted p-value below **0.05** and absolute log2 fold change at least **1**. Of these, **24** increased and **16** decreased in treated cells relative to control.

## Library readiness

I applied the release-brief criteria of at least **5000000** assigned reads and mapping rate at least **0.7** to every library. The result was **12** usable libraries and **0** failures. The minimum usable replicate count across arms was **6**, compared with the required **3**. Resequencing is therefore not indicated by the stated library criteria.

## Design assessment

The sample sheet contains **1** preparation batch and **2** conditions. Both conditions occur in that batch, with **6** libraries from each arm. The treatment coefficient is therefore identifiable independently of batch assignment. Because batch does not vary, a separate batch coefficient cannot be fitted and is unnecessary for this dataset.

## Differential-expression analysis

Counts were normalized with median-ratio library size factors. I fitted a per-gene negative-binomial generalized linear model for the treated-versus-control contrast, used Wald tests, and adjusted across all tested genes by the Benjamini-Hochberg procedure. All **400** fits converged, with **0** fit failures. Calls required both stated thresholds.

The first automated result-assembly attempt failed because R retained an unexpected coefficient sub-name. It produced no gene verdict. I removed inherited names and reran the full computation; the successful rerun is the basis of the results below.

### Increased in treated cells

G0287, G0279, G0277, G0131, G0194, G0061, G0101, G0331, G0110, G0310, G0107, G0260, G0037, G0006, G0153, G0212, G0010, G0293, G0118, G0039, G0374, G0007, G0383, G0185

### Decreased in treated cells

G0124, G0115, G0314, G0247, G0299, G0154, G0052, G0276, G0187, G0155, G0114, G0280, G0311, G0372, G0394, G0149

## What this means for the study

The technical library gate and design gate both pass, so the intended compound-versus-vehicle conclusion can be made from this experiment. The analysis provides evidence that the compound is associated with expression changes in the genes listed above. These are statistical calls on the targeted panel, not proof of mechanism or off-panel effects.

## Recommended next actions and control plan

1. Treat the listed genes as the response set for biological interpretation and orthogonal confirmation. Prioritize confirmation using an independent assay and an independent experiment before making mechanistic claims.
2. Archive the released inputs, QC verdict, sample-sheet cross-tabulation, analysis script, complete gene-level results, and this report together. This preserves the exact eligibility and calling rules used here.
3. For future preparation runs, keep both study arms represented within every batch. Reapply the same read-count, mapping-rate, replicate, adjusted-p-value, and fold-change gates before release.
4. For a production or publication workflow, reproduce the count analysis with a validated RNA-sequencing package that uses dispersion sharing/shrinkage. The local environment lacked those standard packages, so the current analysis used independently fitted negative-binomial models. Any disagreement should trigger model review rather than selective reporting.
