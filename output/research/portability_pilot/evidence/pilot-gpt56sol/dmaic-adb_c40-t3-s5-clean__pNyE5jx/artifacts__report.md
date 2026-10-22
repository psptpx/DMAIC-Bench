# Compound-response sequencing study report

## Executive conclusion

The libraries can carry a conclusion: all **12** libraries passed, with **0** failures. The control and treated arms each retain **6** usable libraries, above the required minimum of **3**.

The intended comparison can be made after adjustment for preparation batch. The design contains **2** batches; its model matrix has **3** independent columns out of **3**, so condition is not perfectly confounded with batch.

The batch-adjusted count analysis called **3** genes: **1** higher under compound and **2** lower. Calls required adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**.

## Library readiness

A library had to have at least **5000000** assigned reads and mapping rate at least **0.7**. The observed minima were **9194000** assigned reads and **0.865** mapping rate. Thus **0** libraries failed, and no re-sequencing is required by the replicate rule.

## Design assessment

The usable-library allocation was:

| Arm | L1 | L2 |
|---|---:|---:|
| control | 5 | 1 |
| treated | 1 | 5 |

Although imbalanced, both arms occur in both batches. The fitted design used an intercept, treatment, and batch term. Its full rank establishes that the treatment contrast is estimable separately from batch.

## Compound-responsive genes

A negative-binomial count model with normalization offset, treatment, and batch was fitted gene by gene. Benjamini–Hochberg adjustment was applied to finite Wald tests.

| Gene | log2 fold change | raw p-value | adjusted p-value | Direction |
|---|---:|---:|---:|---|
| G0269 | -1.225721945591161 | 9.212693007378917e-09 | 3.666651816936809e-06 | lower |
| G0241 | 1.0381701034271085 | 0.0004601274390483943 | 0.022517160310255167 | higher |
| G0037 | -1.0088042595053173 | 0.0009804393609548455 | 0.03547407869636623 | lower |

The panel contained **400** genes. Finite tests were obtained for **398**; **2** lacked finite Wald statistics. Models converged for **399**, while **1** did not converge. Therefore the calls above are supported by successful fitted tests, but the untested genes must not be described as evidence of no response.

## What changed and what it achieved

No libraries were removed because all passed the standing QC rules. The analytical change required by the multi-batch design was inclusion of preparation batch in the count model. This preserved the estimable compound contrast while preventing the observed batch imbalance from being treated as compound effect.

## Recommended next actions and control plan

Proceed with biological review and targeted confirmation of the called genes, retaining direction and uncertainty from the batch-adjusted model. Do not reinterpret genes lacking finite tests as null findings. Archive the QC decisions, sample sheet, model matrix, complete gene-level results, and scripts with this report. For follow-up library preparation, distribute each arm across every batch more evenly; rerun the same QC and rank checks before gene calling, and continue to include batch whenever multiple preparation batches are used.
