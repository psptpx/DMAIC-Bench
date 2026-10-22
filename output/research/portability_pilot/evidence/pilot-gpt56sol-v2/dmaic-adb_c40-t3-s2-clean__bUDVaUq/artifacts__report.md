# Compound-response panel study: final report

## Executive decision

The libraries can support a conclusion, and the intended treated-versus-control comparison is estimable when preparation batch is included. The final batch-adjusted count analysis calls **38 genes**. Independent qPCR confirmed **10 of 10** nominated leading candidates, for concordance **1.0**, which exceeds the facility requirement of **0.75**. The validated candidate list may therefore be issued.

One panel gene, **G0009**, did not yield a reliable fitted count model after alternate optimization. It was excluded from calls; no response conclusion is made for that gene.

## Library usability

The QC calculation evaluated **12 libraries**. **0** failed the joint requirement of at least **5000000 assigned reads** and mapping rate at least **0.7**. The control and treated arms each retained **6 usable libraries**, above the required minimum of **3**. Re-sequencing is therefore not required on the observed library metrics.

## Can the intended comparison be made?

Yes, with batch adjustment. There were **2 preparation batches**. The model matrix had **3 columns** and rank **3**, so treatment was not confounded with batch. Allocation was imbalanced: control had **5** libraries in L1 and **1** in L2, while treated had **1** in L1 and **5** in L2. Both arms nevertheless occurred in both batches, making the treatment contrast estimable. Because batch effects could otherwise bias the result, batch was retained in every primary gene model.

## Panel response

Counts were normalized by median-ratio size factors and analyzed gene by gene with a negative-binomial regression containing intercept, preparation batch, and treatment. Treated-minus-control effects were tested with Wald tests, followed by Benjamini-Hochberg correction. Calls required adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**.

Of **400 genes**, **399** had reliable final fits and **1** did not. **38 genes** met both call criteria:

G0026, G0318, G0358, G0247, G0236, G0355, G0228, G0010, G0302, G0183, G0012, G0213, G0141, G0078, G0373, G0163, G0146, G0086, G0372, G0112, G0075, G0342, G0133, G0017, G0291, G0345, G0311, G0283, G0388, G0108, G0295, G0253, G0275, G0081, G0049, G0340, G0351, G0397

The complete effect estimates and adjusted p-values are retained in `de_results_final.csv`. An independently computed log-count, batch-adjusted sensitivity model called **31 genes**; this broadly supports a panel-wide signal but does not replace the count-model calls above.

## Independent validation

The qPCR analysis compared **4 biological replicates per arm** using two-sided Welch tests. Confirmation required p-value below **0.05** and a treated-minus-control effect in the panel-called direction. All **10 nominees** were confirmed, all in the expected down direction:

G0247, G0012, G0213, G0358, G0355, G0372, G0295, G0075, G0342, G0302

Thus **10 of 10** were confirmed and concordance was **1.0**. The validation release rule passes, so the candidate list should not be withheld.

## Gene-set result

One-sided Fisher over-representation tests were run for **12 sets** against the **400-gene** panel universe, with Benjamini-Hochberg correction. **1 set** was significant. SET03 contained **17** response genes among **30** annotated members, with odds ratio **21.732601** and adjusted p-value **5.99587593457e-11**.

## What changed and what it achieved

The analysis did not use an unadjusted arm comparison. It added preparation batch to separate the compound effect from the strongly imbalanced preparation layout. Initial optimization yielded **3** problematic fits; alternate optimization recovered **2**, leaving **1** unresolved fit. This produced a final auditable response list while preserving an explicit no-conclusion status for G0009.

## Recommended next actions and control plan

- Issue the **38-gene panel response list together with the independently supported leading nominees**.
- Treat G0009 as unresolved rather than unchanged. Re-measure or re-sequence it if its status matters to the biological decision.
- Interpret unvalidated members of the broader panel list as sequencing-supported rather than independently confirmed; prioritize additional orthogonal validation before making gene-specific mechanistic claims.
- Preserve the sample sheet, QC gate, batch-adjusted design matrix, full result table, qPCR calculations, and enrichment table as the analysis record.
- In future runs, balance both arms within each preparation batch. Continue applying the same library thresholds, minimum replication gate, batch-adjusted model, dual gene-call thresholds, and validation release rule before issuing a list.
