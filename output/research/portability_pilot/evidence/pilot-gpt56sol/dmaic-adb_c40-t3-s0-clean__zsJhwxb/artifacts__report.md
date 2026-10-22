# Compound-response study report

## Executive conclusion

The libraries can carry a conclusion: all **12** of **12** libraries passed the facility usability rules, leaving **6** control and **6** treated replicates. The planned comparison can be made: the treatment design was not confounded with preparation batch. The analysis called **40** responding genes, comprising **24** higher in treated cells and **16** lower in treated cells.

## Library readiness

A library had to have at least **5,000,000** assigned reads and mapping rate at least **0.70**. Applying both rules produced **0** failures and **12** usable libraries. The minimum retained count across arms was **6**, above the required **3** per arm. Re-sequencing is therefore not required by the standing replication rule.

## Can the intended contrast be estimated?

Yes. There was **1** preparation batch, containing **6** control and **6** treated libraries. The intercept-plus-treatment matrix had rank **2** across **2** columns, so the treated-versus-control coefficient is estimable. Because only **1** batch was observed, a separate batch coefficient was neither needed nor estimable; the required multi-batch adjustment rule was not triggered.

## Differential-expression result

The complete **400**-gene panel was analyzed with median-ratio size-factor normalization followed by per-gene negative-binomial generalized linear models for treated versus control. Size factors ranged from **0.735900** to **1.241564**. Gene-wise moment dispersions were stabilized toward a panel median of **0.076488**. There were **0** model failures. P-values were adjusted across all **400** tests by the Benjamini-Hochberg procedure. A call required adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**.

### Higher in treated cells (24)

G0277, G0131, G0061, G0331, G0287, G0279, G0310, G0293, G0039, G0101, G0010, G0110, G0194, G0006, G0118, G0260, G0107, G0153, G0374, G0037, G0212, G0007, G0383, G0185

### Lower in treated cells (16)

G0314, G0299, G0124, G0247, G0115, G0154, G0276, G0187, G0052, G0311, G0155, G0280, G0372, G0114, G0149, G0394

The full gene-level estimates, p-values, adjusted p-values, dispersions, and call flags are retained in `de_results.csv`.

## What changed and what it achieved

No laboratory rescue or sample exclusion was needed: QC removed **0** libraries. The analytical data were normalized for library-size differences, then the treatment effect was estimated directly because the design check found no confounding. This produced **40** calls with **0** failed fits while preserving all **12** usable libraries.

## Recommendation and control plan

Proceed with biological review and targeted confirmation of the listed genes; do not re-sequence solely for the facility QC rule. Preserve the sample sheet, raw count matrix, `de_results.csv`, analysis scripts, `trace.json`, and this report as the audit package. For follow-up work, randomize both arms within every preparation batch and retain at least **6** usable replicates per arm if the same replication depth is intended. Re-run the same QC gates before modeling, include batch whenever more than **1** batch is present, and continue to enforce the same adjusted-p-value and effect-size thresholds.

## Interpretation limits

All libraries came from a single preparation batch, so this experiment cannot estimate between-batch variability or demonstrate reproducibility across batches. Also, specialist RNA-seq packages were unavailable in the environment; the result uses an explicit negative-binomial GLM workflow with documented normalization and dispersion stabilization rather than a specialist implementation. Independent confirmation is advisable before treating the panel calls as broadly generalizable biomarkers.
