# Compound-expression study: decision report

## Executive conclusion

The libraries can carry the planned comparison. No library failed the facility's sequencing-quality rules, and the control and treated arms each retain **6** usable biological replicates. The minimum retained arm size is therefore **6**, above the required minimum of **3**.

The treatment comparison is identifiable on this design. There is **1** preparation batch, it contains **6** control and **6** treated libraries, and adding treatment to the design increased its rank from **1** to **2**. Treatment is therefore not confounded with preparation batch. Because only **1** batch is represented, the facility rule requiring a batch term for multiple batches does not apply.

The final count analysis fit all **400** panel genes and called **0** genes as responding to the compound. Thus this dataset provides no gene-level response meeting the facility's joint criteria; this is not evidence that every biological effect is exactly zero.

## What was measured

Library QC applied the standing inclusive cutoffs of **5000000** assigned reads and mapping rate **0.7**. Across **12** libraries, **0** failed. The resulting arm counts were **6** control and **6** treated.

The sample sheet was joined to the QC result before checking estimability. The usable design contained **12** samples, **2** conditions, and **1** preparation batch. Both conditions occurred within that batch, and the explicit rank calculation showed that treatment contributes an estimable design dimension.

## Expression analysis and gene calls

The count matrix contained **400** genes and **12** samples. Counts were normalized by median-of-ratios size factors. Because the design had **1** batch, a simple treatment model was used. Each gene was fit with a negative-binomial generalized linear model using the normalization factor as an offset. A panel-wide common dispersion was estimated from within-arm variation to stabilize inference at the available replication. Benjamini–Hochberg adjustment was applied across all **400** genes.

A gene required adjusted p-value below **0.05** and absolute log2 fold change at least **1**. All **400** final models fit successfully, **0** failed, and **0** genes met both criteria. There were consequently **0** called increases and **0** called decreases.

An exploratory version that estimated dispersion separately for every gene was not used for the conclusion: it produced only **397** finite gene tests and **4** failed or nonconverged fits. It was replaced by the stabilized analysis above, which achieved **400** valid fits and **0** failed fits. The raw counts and calling thresholds were not changed.

## Business interpretation

Where the study stands: sequencing quality and retained replication are adequate, and the intended compound-versus-vehicle contrast can be made. The limiting result is not library failure or treatment–batch confounding; it is that no tested gene passes the prespecified combination of statistical and effect-size criteria.

What changed during analysis: only the statistical dispersion estimation was stabilized after the exploratory fit showed incomplete diagnostics. What that achieved: complete model fits for the full panel without changing samples, counts, hypotheses, multiple-testing scope, or call thresholds.

## Recommended next actions and control plan

The facility does not need to re-sequence this study for the stated QC or replication rules. Release the result as “no genes called under the prespecified criteria,” together with the important distinction that absence of a call is not proof of no biological effect.

Preserve `qc_results.json`, `design_results.json`, `de_results_common.csv`, and the analysis scripts with the released report. Any rerun should verify the same retained-arm count, the same nonconfounded design verdict, complete fits for all panel genes, adjustment over the full panel, and simultaneous application of both call thresholds.

If the principal investigator needs greater sensitivity or wishes to detect smaller effects, plan a new independently replicated experiment and perform a prospective power analysis rather than relaxing thresholds after seeing these data. Keep both arms represented within every future preparation batch so that treatment remains separable from batch.
