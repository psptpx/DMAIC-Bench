# Compound-expression study: decision report

## Executive decision

The sequencing libraries can carry an analysis: all **12** libraries passed QC, with **0** failures and **6** usable replicates in each arm. The minimum retained count was **6**, above the required **3**.

The intended compound-versus-vehicle comparison is identifiable, but preparation batch must remain in the model. There were **2** batches; the intercept-plus-batch-plus-condition matrix had **3** columns and rank **3**, so treatment was not perfectly confounded with batch. The allocation was nevertheless imbalanced: control had **5** libraries in one batch and **1** in the other, while treated had the reverse **1** and **5** pattern.

The batch-adjusted analysis supports issuing **no response-gene list**. It tested **400** panel genes across **12** libraries; **398** fits passed finite/convergence checks and **2** did not. At adjusted p below **0.05** and absolute log2 fold change at least **1**, the number called was **0**.

Validation cannot support issuance of a list. There were **0** nominated candidates, **0** confirmations, and no qPCR measurements. Concordance is not zero: it is **not computable** because its denominator is zero. Consequently, it cannot be compared honestly with the required **0.75** concordance. Gene-set annotation remained locked behind that validation gate, so enrichment was not run and no pathway conclusion can be made.

## What was done

Library usability was computed using at least **5000000** assigned reads and mapping rate at least **0.7**. The resulting arm minimum was declared to the steward only after calculation.

Design identifiability was checked by constructing the intercept, preparation-batch, and treatment model matrix and calculating its rank. Because the matrix was full rank, the counts were analyzed with preparation batch retained rather than using an unadjusted arm comparison.

Counts were normalized by median ratios. Each gene was fit with an negative-binomial count regression containing batch and condition, using a normalization offset; treatment was tested by a Wald test and p-values were adjusted by the BH procedure. The first execution failed output validation because non-finite diagnostics could not be serialized; that attempt was discarded. The rerun enforced finite and convergence checks and produced the stated result. The **2** failed fits were not silently converted into calls.

## Interpretation and cause

The study is analytically usable and the compound effect is estimable, but treatment and preparation batch are strongly imbalanced. Batch adjustment is therefore essential. After that adjustment and multiplicity control, no gene satisfies the facility's combined statistical and effect-size rule. This is evidence that the present panel experiment does not establish a qualifying response gene; it is not proof that every possible effect is exactly absent.

There is no independent-validation evidence to score because no candidate entered qPCR. The downstream conclusion stops there. A numeric concordance, a validation-pass claim, and enrichment results would all be inventions.

## Recommended next actions and control

- Do not issue a compound-response gene list or pathway claim from this run.
- Preserve the current QC rules, sample-level QC record, full-rank design check, batch term, multiplicity correction, and dual calling rule as release controls.
- If candidate discovery remains important, run a new experiment with treatment distributed evenly across preparation batches and predefine the same analysis before examining results.
- Run qPCR only for candidates produced by that predefined rule. Release a validated list only when concordance has a real denominator and clears the prespecified gate.
- Investigate the **2** non-convergent gene fits before any reanalysis, document any model change, and rerun the entire locked pipeline rather than selecting genes ad hoc.
