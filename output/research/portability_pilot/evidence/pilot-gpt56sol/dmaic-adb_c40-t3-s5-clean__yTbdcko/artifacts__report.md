# Compound-versus-vehicle expression study: decision report

## Executive conclusion

The libraries can carry an analysis: **0** libraries failed sequencing QC, and the control and treated arms each retain **6** usable replicates. This exceeds the required minimum of **3** per arm.

The intended comparison is estimable, but preparation batch must be controlled. There are **2** preparation batches. The model matrix for treatment plus batch had rank **3** across **3** columns, so treatment is not exactly confounded with batch. The allocation is nevertheless imbalanced: control contributes **5** libraries in L1 and **1** in L2, while treated contributes **1** in L1 and **5** in L2.

After batch-adjusted count modeling and multiplicity correction, **3** genes meet both calling criteria:

| Gene | Direction | log2 fold change | adjusted p-value |
|---|---:|---:|---:|
| G0037 | decreased | -1.0088042595053173 | 0.03565234039835802 |
| G0241 | increased | 1.0381701034271085 | 0.02263031186960318 |
| G0269 | decreased | -1.225721945591161 | 0.0000036850772029515667 |

## What was assessed

Library usability was evaluated at the facility thresholds of **5000000** assigned reads and mapping rate **0.7**. All **12** libraries passed, leaving **6** usable control and **6** usable treated libraries.

The sample sheet was then checked for estimability rather than treating batch balance as a visual judgment. The usable-sample design used **12** rows and included treatment and batch. Because its rank equaled its **3** columns, the treatment coefficient can be estimated separately from batch.

For expression, all **400** panel genes across **12** samples were modeled with count-depth offsets and terms for treatment and batch. Two-sided treatment Wald p-values were adjusted together over all **400** genes by Benjamini–Hochberg. Calls required adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**. All **400** genes received a finite final test. The primary negative-binomial fit was singular at the zero-dispersion boundary for **3** genes; those used the Poisson boundary limit under the same design. Final model failures were **0**.

## Interpretation and limitations

The data support compound-associated expression changes for the listed genes conditional on the batch-adjusted model. Because treatment allocation is strongly imbalanced across the **2** batches, the conclusion should not be presented as coming from a balanced experiment; it depends on the within-batch overlap represented by the **1** minority-arm library in each batch. The design is estimable, not ideal.

The facility thresholds were applied exactly. No gene was called from an unadjusted treatment-only analysis. The reported gene list requires both statistical and effect-size criteria, not either criterion alone.

## Recommended next actions and control plan

1. Preserve the raw counts, sample sheet, QC metrics, analysis script, and final result artifact together; reruns should retain treatment and batch in the model.
2. Validate the **3** called genes with an orthogonal assay before making a high-stakes biological claim.
3. For the next experiment, distribute each arm evenly within each preparation batch and randomize preparation order. This removes the current dependence on sparse cross-arm overlap.
4. Continue release gating: stop before gene calling if either arm falls below **3** usable replicates, and stop if treatment becomes exactly confounded with batch.
5. Hold future calls to adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**, with all panel genes included in multiplicity correction.
