# Compound-expression study: decision report

## Executive decision

The libraries can carry a conclusion: all **12** libraries passed the sequencing rules, with **6** usable control libraries and **6** usable treated libraries. The smaller arm therefore retains **6** usable replicates against the required minimum of **3**.

The intended comparison can be made. There is **1** preparation batch, and it contains **6** control and **6** treated libraries. Treatment is not confounded with batch. The treatment design has rank **2** across **2** columns and is full rank.

No gene is called as responding to the compound. The analysis found **0** genes satisfying both an adjusted-p threshold of **0.05** and an absolute log2-fold-change threshold of **1.0**.

## What was measured and what changed

Library QC applied the released rules: at least **5000000** assigned reads and mapping rate at least **0.70**. There were **0** failed libraries, so QC filtering changed the analysis set by **0** libraries and retained all **12**. No re-sequencing intervention was required.

The design review found **1** batch containing both study arms, so no batch term with an estimable contrast was needed. This changed the planned analysis to the valid simple treatment contrast rather than a blocked model. The design was not repaired or otherwise altered.

## Gene analysis and result

Counts were normalized by median-ratio size factors. For each gene, I fitted a negative-binomial log-link model with treatment as the predictor and the normalization factor as an offset; a Poisson-limit fit handled a boundary dispersion estimate. I used treatment Wald tests and applied Benjamini–Hochberg adjustment across the panel.

The released panel contained **400** genes. Models converged for all **400** genes. For **1** gene whose negative-binomial dispersion estimate reached its boundary, the Poisson-limit model was used. Among the successfully tested genes, **0** met both calling criteria. Thus there is no facility-qualified responder list to report; this is absence of qualifying evidence, not proof that every biological effect is exactly zero.

## What the facility should do next

Release the result as a technically usable, identifiable study with no genes called at the pre-set criteria. Do not re-sequence merely for library QC, because the retained replicate minimum is met. No gene requires an untestable flag after using the valid Poisson-limit fit for the boundary case.

Hold the conclusion by archiving the released metrics, sample sheet, count matrix, QC flags, normalization table, complete gene-result table, and analysis script together. For future multi-batch work, continue placing both arms within each preparation batch so treatment remains separable from batch. If the PI wants evidence below the current effect or adjusted-p criteria, that requires a prospectively justified follow-up design rather than relaxing thresholds after seeing these results.

## Reproducibility note

The requested pre-specified software method was not available from the study lead, so the report states the locally executed method explicitly. The complete gene results are in `de_results.tsv`, normalization details are in `normalization.tsv`, and the machine-readable analysis record is in `trace.json`.
