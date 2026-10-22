# Sequencing study status report

## Executive conclusion

The study can carry a compound-versus-vehicle conclusion on its current library design. QC passed for all usable libraries: there were **0 failed libraries**, with **6 usable control replicates** and **6 usable treated replicates**. This exceeds the minimum replicate requirement used by the facility.

The comparison is estimable: the sample sheet contains **1 preparation batch**, and that batch contains both arms. The treatment effect is therefore not confounded with preparation batch. Because there is only **1 batch**, no between-batch term was required for this comparison.

## Panel result

The count analysis covered **400 genes** and **12 libraries**. Applying the planned thresholds (adjusted p below **0.05** and absolute log2 fold change at least **1.0**) produced **39 nominated genes**:

G0006, G0007, G0010, G0037, G0039, G0052, G0061, G0101, G0107, G0110, G0114, G0115, G0118, G0124, G0131, G0149, G0153, G0154, G0155, G0187, G0194, G0212, G0247, G0260, G0276, G0277, G0279, G0280, G0282, G0287, G0293, G0299, G0310, G0311, G0314, G0331, G0374, G0383, G0394

These are the genes responding in the sequencing analysis under the stated calling rule. The direction is the treated-minus-control log2 effect computed in the analysis; positive values indicate higher treated expression and negative values indicate lower treated expression.

## Independent validation

The qPCR batch contains measurements for **10 candidates**, with **4 biological replicates per arm**. **10** of the **10** tested candidates were confirmed at p below **0.05** and in the sequencing-called direction. The resulting concordance is **1.0**, above the required minimum concordance of **0.75**.

The validation evidence supports issuing the nominated list for the **10 candidates that were actually tested by qPCR**. The qPCR batch does not contain validation measurements for the remaining **29** sequencing nominations, so those genes are supported by sequencing but not independently validated in this archive. This distinction should be retained in any external communication.

## Gene-set context

The enrichment calculation used the **400-gene** panel universe, **39** sequencing candidates, and **12** annotated sets, with BH adjustment at alpha **0.05**. It found **1 significant set**. The enrichment result is contextual evidence and does not change the gene-calling or validation decision.

## Where the study stands and what to do next

The facility can release the validated candidate list because library QC, design identifiability, sequencing thresholds, and the validation gate all pass. The immediate limitation is validation coverage rather than library quality or study design: only **10** candidates have qPCR results.

Next, retain the complete sequencing and qPCR result tables with the report, label the **10** qPCR-confirmed candidates separately from the unvalidated sequencing nominations, and obtain qPCR follow-up for the remaining **29** nominations if the full panel list is needed for a regulated or high-stakes decision. Preserve the current QC thresholds, design check, adjusted-p-value/effect-size rule, and validation concordance rule as release gates for any follow-up batch.
