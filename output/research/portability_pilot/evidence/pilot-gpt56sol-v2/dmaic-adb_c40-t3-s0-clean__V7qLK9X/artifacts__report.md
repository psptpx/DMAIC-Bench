# Compound-response targeted-panel study: decision report

## Executive decision

The sequencing libraries can carry a conclusion. QC found **0 failed libraries**; the usable counts were **6 control** and **6 treated**, so the minimum retained arm size was **6**.

The intended comparison is estimable. There was **1 preparation batch**, it contained both study arms, and the treatment design had rank **2** for **2 columns**. Treatment and preparation batch therefore were not confounded. With only one batch level, the fitted model was the simple treatment model rather than a model with a non-estimable batch coefficient.

The primary panel analysis called **40 genes**: **24 up-regulated** and **16 down-regulated**. Independent qPCR confirmed **10 of 10 nominated candidates**, a concordance of **1.0**. Validation therefore passed and the nominated candidate list may be issued.

## Analysis and findings

### Library quality and design

Usability was computed from both facility QC criteria for every library. Across **12 libraries**, **0 failed**. The balanced usable design retained **6** libraries in each arm. The full-rank treatment design means the compound comparison can be made without attributing an arm effect to preparation batch.

### Differential expression

The count matrix contained **400 genes** and **12 usable libraries**. The primary analysis used median-ratio normalization, a negative-binomial count GLM with a data-derived common dispersion, a treatment coefficient, and multiplicity adjustment. The formal calls apply the brief's joint adjusted-significance and effect-size rule.

An initial normalization attempt failed because individual zero counts made its geometric means undefined; it produced no usable result and was replaced by the standard all-positive-gene reference calculation. The corrected normalization used **399 reference genes** while retaining all genes in testing.

**Up-regulated calls:** G0006, G0007, G0010, G0037, G0039, G0061, G0101, G0107, G0110, G0118, G0131, G0153, G0185, G0194, G0212, G0260, G0277, G0279, G0287, G0293, G0310, G0331, G0374, G0383.

**Down-regulated calls:** G0052, G0114, G0115, G0124, G0149, G0154, G0155, G0187, G0247, G0276, G0280, G0299, G0311, G0314, G0372, G0394.

A sensitivity analysis based on normalized log counts called **38 genes** under the same joint rule. This supports most primary findings but shows that a small subset is model-sensitive; the negative-binomial result remains the predefined primary count-data analysis.

### Independent validation

The qPCR analysis compared independent arm measurements candidate by candidate using two-sided Welch tests and required both statistical significance and the panel-called direction. **10 of 10 candidates** met both requirements, giving **1.0 concordance**. The validated nominees are: G0299, G0277, G0314, G0311, G0276, G0187, G0124, G0154, G0247, G0115.

The validation criterion is met, so the facility can issue these nominated candidates. The remaining panel calls are panel discoveries, not independently qPCR-confirmed candidates, and should be labeled accordingly.

### Gene-set context

Over-representation analysis tested **12 annotated sets** against the **400-gene panel background** and found **1 significant set** after multiplicity adjustment. Significant sets: SET03.

## What changed and what it achieved

The only analytical correction was to the failed first normalization attempt: size factors were re-estimated from genes positive in every library, after which all panel genes remained eligible for modeling. This converted an undefined normalization into a complete primary analysis while preserving transparent documentation of the failure.

## Recommended next actions and control plan

- Issue the independently validated nominee list, with panel direction and qPCR confirmation status attached.
- Release the broader panel-call table separately and mark genes outside the qPCR nominees as discovery findings requiring orthogonal follow-up.
- For future runs, retain the same QC gate, arm-by-batch identifiability check, count-model workflow, joint call rule, and validation gate as a locked analysis template.
- Archive the sample-level QC decisions, design-rank check, normalization factors, full gene-level model output, qPCR tests, and enrichment output so the conclusion can be regenerated.
- Prioritize repeat or expanded validation for model-sensitive panel-only calls before treating them as operational candidates.
