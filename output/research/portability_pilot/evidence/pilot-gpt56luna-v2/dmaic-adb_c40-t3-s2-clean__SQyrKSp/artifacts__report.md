# Compound-expression study status

## Executive conclusion

The study can carry a conclusion. All **12** sequenced libraries were usable under the facility rules, with **6** usable control and **6** usable treated replicates. The treatment contrast is identifiable separately from preparation batch: the usable design contains **2** preparation batches, and both arms occur in both batches. Batch was therefore included in the expression model.

The blocked analysis tested **400** panel genes across **12** samples. **31** genes met the calling rule of adjusted p < **0.05** and absolute log2 fold change >= **1.0**: **10** increased and **21** decreased in treated cells. The responding-gene list is:

G0010, G0012, G0017, G0026, G0075, G0078, G0086, G0108, G0112, G0117, G0133, G0136, G0141, G0146, G0163, G0183, G0213, G0228, G0236, G0247, G0291, G0295, G0302, G0318, G0342, G0345, G0351, G0355, G0358, G0372, G0373

The leading nominated subset comprised **10** genes. Independent qPCR confirmed **10** of **10**, giving concordance **1.0**, above the required minimum of **0.75**. The validated nominated genes were: G0247, G0012, G0213, G0358, G0355, G0372, G0295, G0075, G0342, G0302. The candidate list is therefore supported for issue.

## What caused the result and what changed

There was no sequencing-QC loss: **0** libraries failed the usability criteria. The design was not confounded because preparation batches contained both arms; the change made in analysis was to include batch as a model term rather than comparing arms without adjustment. This produced a batch-adjusted response list of **31** genes.

For context, enrichment was tested across **12** annotated gene sets using a **400**-gene universe and the **31** called candidates. **1** set was significant after BH adjustment: SET03, with an overlap of **14** genes and adjusted p **9.55232041519293e-09**. The other **11** tested sets were not significant after adjustment.

## Decision and next action

Issue the validated candidate list, with the explicit distinction that **31** genes pass the sequencing calling thresholds but **10** leading candidates were independently validated. Preserve the usable-library rules, the batch-aware design check, the batch term in the model, the stated expression thresholds, and the independent qPCR concordance gate as release controls for the next study. If broader biological interpretation is needed, prioritize the significant SET03 enrichment.
