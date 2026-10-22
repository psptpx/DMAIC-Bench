# Compound-response study: decision report

## Executive conclusion

The sequencing libraries can support an analysis: all **12** libraries passed QC, with **0** failures and **6** usable replicates in each arm. The intended compound-versus-vehicle contrast is estimable after adjustment for preparation batch. The complete batch-adjusted analysis tested **400** genes, fit all **400**, and called **0** genes under the prespecified joint criteria. Therefore, there is no response-gene list to issue from this study.

Independent validation cannot support a candidate list: the released qPCR batch contains **0** nominated candidates and **0** confirmations, with no measurements. Concordance is consequently undefined rather than zero. I did not invent or declare a numeric value for it. Gene-set annotation remained locked behind that unavailable declaration, so enrichment could not be computed and no pathway claim is made.

## Library fitness

A usable library required at least **5,000,000** assigned reads and mapping rate at least **0.70**. The facility required at least **3** usable replicates per arm. Applying both rules produced **0** failed libraries; control retained **6**, treated retained **6**, and the minimum arm count was **6**. Re-sequencing is not required on the stated QC and replication rules.

## Design and comparison

There are **2** preparation batches. The usable-sample allocation was imbalanced: batch L1 contained **5** control and **1** treated library, while batch L2 contained **1** control and **5** treated libraries. Nevertheless, both batches contained both arms. The model matrix had **3** columns and rank **3**, and **2** batches had within-batch arm overlap. Thus treatment and batch are not perfectly confounded, and the treatment contrast can be estimated with batch in the model.

## Expression result

The primary complete analysis used median-of-ratios normalization, log-transformed normalized expression, and a linear model containing treatment and preparation batch. P-values for the treatment term were adjusted across **400** genes. Calls required adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**. All **400** fits succeeded and **0** genes met both requirements.

A negative-binomial sensitivity analysis also returned **0** calls. It successfully fit **398** genes and failed on **2**, so it was not used as the complete primary result; its agreement on the call count is only a sensitivity check.

## Validation and release decision

The validation archive states that no candidates were nominated. It contains **0** candidates and **0** qPCR confirmations. Because the denominator is absent, the required confirmation fraction cannot be computed and cannot be compared honestly with the **0.75** release threshold. This does not overturn a positive panel list—there is no positive list to validate. The facility should issue no candidate list and make no validation-supported response claim.

The gene-set annotation was not released because its gate requires a numeric validation concordance. Since that quantity is undefined here, enrichment stops at that gate. No gene-set conclusion is available.

## What changed, what it achieved, and next action

No laboratory intervention or data exclusion was needed: QC retained every library. Analytically, preparation batch was added to the treatment model as required. That change separated the estimable treatment contrast from the strong batch imbalance and yielded a complete result with **0** called genes.

For this study, archive the no-call result and withhold a candidate list. Do not re-sequence merely for QC. If the biological question warrants another experiment, randomize and balance both arms within each preparation batch rather than repeating the current **5**-to-**1** allocation pattern. Continue to hold future releases with the same library-QC, minimum-replication, batch-identifiability, multiplicity-adjusted gene-call, and independent-qPCR gates. Validation concordance should only be calculated when at least one candidate was actually nominated and measured.
