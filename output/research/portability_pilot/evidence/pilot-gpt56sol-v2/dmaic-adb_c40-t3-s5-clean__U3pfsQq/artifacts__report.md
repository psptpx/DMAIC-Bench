# Compound-response panel: decision report

## Executive decision

The libraries can support analysis: all **12** passed the facility's usability rules, with **6** usable controls and **6** usable treated libraries. The intended treatment comparison is estimable after adjustment for preparation batch. However, the valid batch-adjusted analysis called **0** genes, and the validation archive contains **0** nominated candidates and **0** qPCR confirmations. The validation fraction is therefore not estimable, not a demonstrated zero rate. **Do not issue a compound-response candidate list from this study.**

## What stands behind that decision

### Library quality and replication

Applying the brief's minimum of **5,000,000** assigned reads and **0.70** mapping rate jointly produced **0** failed libraries. The minimum usable replication in either arm was **6**, above the required **3**. Re-sequencing is therefore not required for library attrition.

### Can treatment be separated from batch?

Yes, but only in a batch-adjusted model. There were **2** preparation batches. The intercept, treatment, and batch design had rank **3** across **3** columns, so it was not perfectly confounded. Allocation was nevertheless strongly imbalanced: the first batch contained **5** controls and **1** treated library, while the second contained **1** control and **5** treated libraries. Batch adjustment is essential.

### Gene-level response

The final analysis tested all **400** panel genes with median-ratio library normalization and negative-binomial generalized linear models containing treatment and preparation batch. All **400** fits succeeded. Benjamini-Hochberg adjustment was applied, followed by the facility criteria of adjusted p below **0.05** and absolute log2 fold change of at least **1.0**. The result was **0** called genes.

As a diagnostic only, an arm-only model that incorrectly omitted batch generated **57** apparent calls among **399** successful fits, with **1** failed fit. This is not the study result; the contrast between it and the valid model shows how the imbalanced batch allocation can create misleading treatment signals.

An earlier gene-wise maximum-likelihood implementation failed during call assignment because some fits had missing adjusted p-values. It contributed no result; the stable generalized-linear-model run above superseded it.

### Independent validation and annotation

The released validation batch explicitly contained **0** nominated candidates and no qPCR measurements, yielding **0** confirmed candidates. With a zero denominator, concordance cannot be computed and therefore cannot demonstrate the required **0.75** confirmation fraction at validation alpha **0.05**. The administrative declaration of **0** was used only to route the steward and must not be interpreted as a measured concordance.

Because the validation gate was not met, the steward kept the gene-set annotation locked. Gene-set enrichment was not computed, and no pathway conclusion is available.

## What changed and what it achieved

The analysis changed from the invalid arm-only comparison to the required treatment-plus-batch model. That change reduced the apparent call count from **57** to **0**, preventing a batch-driven list from being reported. It did not rescue a validated compound-response signature.

## Recommended next action and control plan

1. Withhold the candidate list and make no gene-specific or pathway claim from this run.
2. If the biological question must be pursued, repeat or extend the experiment with both arms deliberately balanced within every preparation batch; preserve the current dual library-QC gate and minimum replication gate.
3. Pre-register the count-model, normalization, multiple-testing procedure, and qPCR nomination set before rerunning. The study lead did not provide a prespecified computational method when asked, so this report documents the method actually used rather than claiming it was prespecified.
4. Release a list only after the batch-adjusted panel analysis passes both call criteria and independent qPCR supplies an estimable confirmation fraction meeting the facility gate. Keep annotation and enrichment downstream of that gate.
