# Compound-response panel: decision report

## Decision

The libraries and design can support the intended comparison. All **12** libraries passed QC, leaving **6** control and **6** treated libraries. The batch-adjusted analysis called **39** responding genes: **16** upregulated and **23** downregulated. Independent qPCR confirmed **10** of **10** nominated leading candidates, giving concordance **1.00**, above the required **0.75**. The facility may issue the candidate list.

## Library fitness

Usability required at least **5000000** assigned reads and mapping rate at least **0.70**. There were **0** failures among **12** libraries. Each arm retained **6** usable replicates, above the required **3**, so QC does not trigger re-sequencing.

## Can treatment be separated from batch?

Yes, with adjustment. There were **2** preparation batches. L1 contained **5** control and **1** treated libraries; L2 contained **1** control and **5** treated libraries. The treatment-plus-batch design had rank **3** for **3** columns. It is therefore identifiable, but strongly imbalanced; an unadjusted comparison would not be acceptable.

## Panel result

I fit negative-binomial models to **400** genes with median-ratio library offsets, treatment and batch terms, and a panel-wide dispersion estimate of **0.0319170094148**. Calls required adjusted p-value below **0.05** and absolute log2 fold change at least **1.0** after Benjamini-Hochberg correction.

The **39** panel responders are:

**G0247, G0012, G0318, G0358, G0236, G0010, G0355, G0075, G0141, G0078, G0112, G0163, G0372, G0026, G0373, G0342, G0228, G0086, G0311, G0302, G0283, G0291, G0213, G0183, G0017, G0146, G0133, G0295, G0275, G0345, G0081, G0108, G0388, G0049, G0354, G0340, G0351, G0397, G0253**

An initial gene-wise model run failed at output serialization and was not used. The final result above comes from the complete stabilized rerun.

## Independent qPCR validation

The independently tested nominated leaders were:

**G0247, G0012, G0358, G0355, G0075, G0372, G0342, G0302, G0213, G0295**

For each nominee, I compared **4** biological replicates per arm using a two-sided Welch test. Confirmation required p-value below **0.05** and the panel-called direction. All **10** nominees were confirmed, so concordance was **1.00** against the minimum **0.75**. This clears the release gate. It directly validates the nominated leading subset; it is not a claim that every other panel responder was separately assayed by qPCR.

## Gene-set context

I tested **12** sets against the measured **400**-gene panel background with one-sided Fisher tests and Benjamini-Hochberg correction. **1** set passed adjusted alpha **0.05**: SET03 (overlap **18**, set size **30**, adjusted p **4.63928503609e-12**).

## What to do next and how to hold the result

1. Issue the batch-adjusted responder list, highlighting the qPCR-confirmed nominated leaders.
2. Report the significant gene-set result as secondary panel-relative enrichment, not as genome-wide enrichment.
3. Archive `results/de_final.json`, `results/validation.json`, and `results/enrichment_final.json` with the release.
4. Keep treatment and batch terms in every reanalysis; the allocation imbalance is the study's main design weakness.
5. In follow-up experiments, balance both arms within every preparation batch and retain the same QC, multiplicity, effect-size, and validation gates.
