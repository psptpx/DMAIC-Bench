# Compound-response targeted-panel study

## Executive conclusion

The libraries can carry a conclusion: all **12** libraries passed sequencing QC, with **0** failures and **6** usable replicates in each arm. The minimum retained arm size was **6**, exceeding the required **3**.

The intended comparison is estimable after preparation-batch adjustment. There were **2** batches. The additive design matrix had rank **3** across **3** columns, so treatment was not confounded with batch. Allocation was imbalanced—L1 contained **5** control and **1** treated library, while L2 contained **1** control and **5** treated libraries—but both arms occurred in both batches.

The final batch-adjusted analysis tested **400** genes and called **38** compound-responsive genes using both facility rules: adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**. Of these, **15** increased and **23** decreased under treatment.

## Library and design findings

A library had to have at least **5000000** assigned reads and mapping rate at least **0.70**. The computed QC result was **12** usable libraries and **0** failed libraries. Both control and treated retained **6** usable replicates.

Batch could not be ignored. Its descriptive partial variance fraction on log-normalized expression was **0.31763250525152475**. Accordingly, every gene model included treatment and batch terms rather than using an unadjusted arm comparison.

## Differential-expression analysis

Counts were normalized by median ratios using the **397** genes positive in every library. Each gene was modeled with an intercept, treatment, and batch term. Gene-wise NB2 fits succeeded directly for **397** genes. The remaining **3** estimates lay at the zero-dispersion boundary and were completed with the corresponding Poisson boundary model. The final run produced finite tests for all **400** genes and **0** failed genes. Benjamini–Hochberg adjustment was applied over the full panel; an independent recomputation differed by at most **8.716985466783456e-16**.

There were **51** genes below the adjusted-p threshold and **39** at or beyond the effect-size threshold, but only **38** met both and were called.

### Increased under treatment (**15**)

G0026, G0318, G0236, G0010, G0183, G0141, G0078, G0373, G0163, G0112, G0311, G0283, G0388, G0275, G0081

### Decreased under treatment (**23**)

G0358, G0247, G0355, G0228, G0302, G0012, G0213, G0146, G0086, G0372, G0075, G0342, G0133, G0017, G0291, G0345, G0108, G0295, G0253, G0049, G0340, G0351, G0397

The complete coefficient, standard-error, p-value, adjusted-p-value, dispersion, convergence, and call table is retained in `de_results.csv`.

## What changed during analysis

The initial normalization implementation failed because it attempted geometric means on rows containing individual zero counts. That run produced **0** finite size factors and **400** failed models; it was rejected and contributes no biological conclusion. Restricting size-factor estimation to the **397** genes positive in every library restored valid normalization. Boundary diagnostics then identified **3** zero-dispersion cases, and the explicit Poisson-boundary fallback reduced unresolved model failures to **0**. The resulting final call count was **38**.

The study lead did not supply a prespecified package-level differential-expression procedure when asked. Therefore, this report documents the locally implemented method rather than claiming a DESeq2 or edgeR result.

## Recommended next actions and hold plan

1. Treat the **38** listed genes as the panel findings from this documented batch-adjusted workflow; do not promote the additional adjusted-p-only genes because they did not meet the effect-size rule.
2. Validate the highest-priority findings with an orthogonal expression assay and biological interpretation before making compound-development decisions.
3. For future preparation, balance each arm within each batch. The present overlap makes the contrast estimable, but the **5**-to-**1** allocation in each batch needlessly couples treatment and batch and reduces precision.
4. Lock the QC thresholds, model formula, normalization rule, zero-dispersion fallback, multiple-testing family, software versions, and scripts before the next run. Re-run from the archived JSON inputs and require **0** unresolved model failures before release.
5. Retain `run_qc.py`, `check_design.py`, `run_de.py`, `de_results.csv`, `de_summary.json`, and `trace.json` as the audit package.
