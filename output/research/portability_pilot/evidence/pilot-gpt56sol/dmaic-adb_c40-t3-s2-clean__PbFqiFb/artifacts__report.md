# Compound-response sequencing study report

## Executive conclusion

The libraries can support an analysis: **0 libraries failed QC**, and the control and treated arms each retained **6 usable libraries**. The intended comparison is estimable after accounting for preparation batch. The batch-adjusted count analysis called **38 genes** as responding to compound, comprising **15 increases** and **23 decreases**.

## Measure: library usability

I applied the standing usability rules directly to assigned reads and mapping rate: at least **5000000 assigned reads** and a mapping rate of at least **0.7**. The minimum retained replication across arms was **6**, exceeding the required **3**. Thus re-sequencing is not required on library-QC grounds.

## Analyze: whether the comparison can be made

There were **2 preparation batches**. The required model matrix had **12 rows** and **3 columns**, with rank **3**; therefore it was full rank and treatment was not confounded with batch. The design is highly unbalanced: batch L1 contained **5 control** and **1 treated** libraries, while batch L2 contained **1 control** and **5 treated** libraries. Because both arms occur in both batches, the treatment coefficient remains estimable, and preparation batch was included in the differential-expression model.

## Analyze: compound-responsive genes

I tested **400 genes** with gene-wise negative-binomial generalized linear models, using median-ratio library-size offsets and terms for treatment and preparation batch. All models completed, with **0 failures**. Wald p-values were adjusted by the Benjamini-Hochberg method. Calls required adjusted p-value below **0.05** and absolute log2 fold change of at least **1.0**.

**Increased with compound (15):** G0026, G0318, G0236, G0183, G0010, G0163, G0373, G0141, G0078, G0112, G0311, G0283, G0275, G0081, G0388.

**Decreased with compound (23):** G0358, G0247, G0355, G0302, G0228, G0213, G0012, G0075, G0146, G0372, G0086, G0017, G0133, G0291, G0342, G0345, G0108, G0295, G0253, G0351, G0340, G0049, G0397.

The statistical and effect-size filters are both consequential: **52 genes** passed the adjusted-p-value filter, **39 genes** passed the fold-change filter, and **38 genes** passed both.

## Improve and control: what to do next

No corrective re-sequencing is indicated by the current library criteria. The facility should release the batch-adjusted result table (`de_results.csv`) with this report and use the listed genes as the response set for biological follow-up rather than substituting an unadjusted arm comparison.

For future preparation, balance each arm within every batch. Although the present overlap made the comparison estimable, its strong imbalance makes the treatment estimate depend heavily on the small cross-arm overlap. Preserve the sample sheet, raw count matrix, QC decisions, size-factor calculation, model formula, and adjustment rule with the release; reruns should continue to enforce the same QC gate and dual gene-call criteria. The requested external choice of analysis method was refused because no such study fact was recorded, so the locally specified negative-binomial workflow and complete gene-level output should be treated as the reproducible analysis specification for this release.
