# Study disposition

## Executive conclusion

The sequencing libraries pass the facility's replicate-count gate after quality control, but they cannot carry the intended compound-versus-vehicle conclusion. Of **12** libraries assessed, **4** failed the joint quality rule and **8** remained. The retained set contains **4** usable controls and **4** usable treated libraries, exceeding the required minimum of **3** per arm.

That numerical sufficiency does not make the contrast identifiable. The usable libraries occupy **2** preparation batches, with every usable control in one batch and every usable treated library in the other. In the required intercept-plus-treatment-plus-batch model, the treatment indicator exactly equals the batch indicator. The model therefore has rank **2** despite having **3** columns. Compound effect and preparation-batch effect cannot be separated.

Accordingly, no genes can be defensibly reported as responding to the compound, and no candidate list should be issued.

## What was computed

Library usability was recomputed from the released per-library metrics using the standing cutoffs of **5000000** assigned reads and mapping rate **0.7**. The result was **4** failed libraries and a minimum retained arm size of **4**.

The design check was then run only on the **8** usable libraries. It found complete treatment–batch confounding across **2** batches. The design matrix rank result, **2** for **3** intended columns, establishes that the planned batch-adjusted treatment contrast is not estimable.

## Where the analysis stops

The steward locked the gene-level count batch after the confounding verdict. Consequently, differential expression was not computed, and there is no computed adjusted significance, fold change, or responding-gene list to report.

The independent qPCR batch is downstream of the count analysis and was not available. Validation concordance and the number of confirmed candidates therefore could not be computed. This is not a validation failure; it is an unavailable validation assessment because no valid candidates could first be nominated. The conclusion stops here rather than substituting an unadjusted arm comparison that would attribute batch differences to treatment.

The gene-set annotation is also downstream of the unavailable validation stage. No enrichment result was computed.

## What caused the stop and what the QC change achieved

Applying the pre-specified QC rules removed libraries for inadequate sequencing performance. This preserved **4** usable replicates in each arm and therefore passed the replication rule. However, the retained controls and treated samples lie in different preparation batches. QC achieved acceptable per-arm replication but did not produce overlap between arm and batch, so it could not rescue causal interpretability.

## Required next action and control plan

Prepare and sequence replacement libraries under a crossed, balanced layout: each preparation batch must contain both control and treated biological replicates. The facility should then repeat the same library QC before examining genes and verify that the treatment-plus-batch design is full rank on the retained set.

Only after that design gate passes should the team fit the required batch-adjusted expression model, nominate genes under the pre-specified significance and effect-size rules, and evaluate independent qPCR in the panel-called direction. Hold issuance of any candidate list until the validation gate is demonstrably met. Archive the post-QC arm-by-batch table and design-rank check as mandatory release controls so this confounding cannot pass unnoticed in the rerun.
