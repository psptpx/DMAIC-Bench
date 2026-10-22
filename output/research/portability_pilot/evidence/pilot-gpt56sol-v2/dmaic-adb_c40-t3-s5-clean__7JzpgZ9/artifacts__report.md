# Compound-response panel study: decision report

## Executive decision

The libraries can support an analysis, and the intended treated-versus-control contrast is estimable after preparation batch is included in the model. However, the batch-adjusted panel analysis produced **0 qualifying genes**, so there is no compound-response candidate list to issue. Independent qPCR concordance cannot be evaluated: **0 candidates** were nominated, **0 confirmations** were possible, and the released validation batch contains no observations. An empty denominator was not treated as successful validation.

## Measure: library readiness

All **12 libraries** passed the facility's joint QC rule. The failed-library count was **0**. The control and treated arms each retain **6 usable replicates**, so the minimum retained arm size is **6**, above the required minimum of **3**. The applied limits were at least **5000000 assigned reads** and mapping rate at least **0.7**. Re-sequencing is therefore not required on the stated library-QC rule.

## Analyze: whether the planned comparison is possible

There are **2 preparation batches**. Allocation is imbalanced: control has **5** libraries in the first batch and **1** in the second, while treated has **1** in the first and **5** in the second. Nevertheless, both arms occur in both batches. The intercept-plus-treatment-plus-batch matrix had rank **3** across **3 columns**, so treatment is not fully confounded with preparation batch.

The comparison can therefore be made, but only with batch included. A simple unadjusted arm comparison would not respect the facility plan or the observed allocation.

## Analyze: panel response

I analyzed **400 genes** across **12 samples** using median-ratio library normalization and gene-wise negative-binomial regression with treatment and preparation batch terms. Benjamini-Hochberg adjustment was applied across the panel. Calls required adjusted p-value below **0.05** and absolute log2 fold change of at least **1.0**.

The optimizer reported convergence for **399** models, and **398** genes yielded finite p-values for correction. **1 gene** passed the adjusted-p-value component alone, while **1 gene** passed the effect-size component alone. Their intersection was **0**, so no gene satisfies the complete prespecified calling rule. The initial analysis attempt failed during serialization of non-finite model values; it was corrected and rerun, and no output from the failed attempt was used.

## Improve: independent validation and release status

The steward released an empty validation batch because the panel nominated **0 candidates**. It therefore contains **0 qPCR observations**, giving **0 confirmed candidates**. Validation concordance is undefined rather than zero or one; computing a proportion would require division by an empty nominee count. I did not invent a numeric value or declare that the validation threshold of **0.75** had been met.

Accordingly:

- validation does not provide evidence supporting issuance of a candidate list;
- there is no candidate list to issue in any event;
- gene-set enrichment could not be run because its annotation batch remained locked behind a numeric validation-concordance gate.

## What changed and what it achieved

The analysis retained all QC-usable libraries and adjusted explicitly for preparation batch. This changed the analysis from a potentially misleading unadjusted arm comparison into an estimable batch-aware comparison. It achieved a defensible negative panel result under the standing calling rules: no qualifying response was found, rather than a list driven by the arm-batch imbalance.

## Recommended next actions and control plan

1. **Do not issue a compound-response gene list from this run.** Archive the empty call set and the undefined validation status explicitly.
2. **Do not re-sequence solely for library QC.** The observed QC and replication requirements were met.
3. If the biological objective requires another attempt, prepare future treated and control libraries in a balanced way within every preparation batch. Preserve randomized processing order and retain the batch field in the analysis model.
4. Pre-register the same dual calling rule and validation rule before rerunning. Send only genuinely nominated genes to independent qPCR; define prospectively how an empty nominee set is represented so a downstream system does not demand a fabricated concordance.
5. At review, verify library QC, arm-by-batch cross-tabulation, design rank, model convergence, multiplicity correction, effect-size thresholding, and availability of actual qPCR observations before authorizing release.
