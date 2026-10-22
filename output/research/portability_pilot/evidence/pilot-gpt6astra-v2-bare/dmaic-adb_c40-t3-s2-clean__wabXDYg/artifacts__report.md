# Compound expression study: decision report

## Executive decision
The libraries can support analysis, and treatment is identifiable separately from preparation batch. Release the batch-adjusted candidate list with the qualifications below. Independent qPCR passes the facility's validation gate; this supports issuing the list, not claiming that every listed gene has been independently validated.

## Library quality and design
All 12 libraries pass the facility's read-depth and mapping criteria; 0 fail. Each arm retains 6 usable replicates against a required minimum of 3.

There are 2 preparation batches. The first contains 5 control and 1 treated libraries; the other contains 1 control and 5 treated libraries. The batch-plus-treatment model has rank 3 for 3 columns: this is imbalance, not complete confounding. The comparison is estimable under an additive batch model, but relies heavily on the minority-arm libraries within each batch. A treatment-by-batch interaction is not reliably resolved by this design.

## Expression analysis and what changed
No libraries or experimental conditions were changed. The analytical protection was to adjust for preparation batch rather than attribute all between-arm differences to compound. Median-ratio normalization was followed by log-transformed gene-wise linear models with batch and treatment, two-sided residual t tests, and panel-wide Benjamini–Hochberg correction. This is an approximate log-linear analysis, not a fitted negative-binomial sequencing model. Low-count uncertainty and unmodeled mean–variance structure remain limitations.

Conditional batch variation accounts for 0.3178 of total centered log-expression variation, measured by the reduction in residual sum of squares when adding batch to treatment. This is an association, not proof of a specific laboratory failure. Adjustment permits a treatment contrast conditional on batch; it does not repair allocation or prove absence of residual confounding.

Across 400 tested genes, 26 meet adjusted p < 0.05 and absolute log fold change >= 1.0. Positive effects indicate increased expression under compound. The complete results are in `gene_results.csv`; the called list is below.

|Gene|Log fold change (base two)|BH adjusted p|
|---|---:|---:|
|G0010|2.3310|0.00355507|
|G0012|-2.7918|0.0057005|
|G0017|-1.4962|0.0074263|
|G0026|2.0499|0.000232769|
|G0075|-2.1232|0.00429345|
|G0078|2.1148|0.00538075|
|G0086|-1.7497|0.0074263|
|G0112|2.1127|0.0103203|
|G0133|-1.5739|0.00628232|
|G0141|2.0619|0.0057005|
|G0146|-1.6354|0.00465891|
|G0163|1.9344|0.00538075|
|G0183|1.5657|0.00189168|
|G0213|-2.6841|0.000976526|
|G0228|-1.6418|0.00133127|
|G0236|2.2992|0.00066113|
|G0247|-3.0790|0.000573086|
|G0291|-1.5323|0.0120487|
|G0302|-1.9288|0.00126071|
|G0311|1.7171|0.0205418|
|G0318|2.4442|0.000505522|
|G0342|-2.0123|0.0198153|
|G0355|-2.3144|0.00101638|
|G0358|-2.7354|0.000232769|
|G0372|-2.2370|0.0057005|
|G0373|1.8552|0.0049074|

## Independent validation
Welch tests on independent qPCR log relative expression confirm 10 of 10 nominated candidates at nominal p < 0.05 in their nominated direction. Concordance is 1.00, exceeding the required 0.75. All confirmed directions are down. Of the panel calls above, 9 have this independent validation. The remaining calls are panel-supported candidates, not independently confirmed findings. G0295 validates by qPCR but does not meet the panel calling rule in this analysis; it has not been silently added to the panel list.

|Nominated gene|qPCR treated minus control|Welch p|
|---|---:|---:|
|G0247|-2.9718|5.43954e-05|
|G0012|-2.3625|0.00236761|
|G0213|-2.5582|4.54674e-05|
|G0358|-2.3258|4.62722e-05|
|G0355|-1.7275|0.00770075|
|G0372|-2.3050|6.94387e-06|
|G0295|-1.6807|0.00081607|
|G0075|-2.1645|0.00152087|
|G0342|-1.7223|0.000218004|
|G0302|-1.9243|0.000145947|

## Gene-set interpretation
Using the 400 tested panel genes as background, 1 sets pass BH correction among 12 tested sets. These are targeted-panel overrepresentation results, not whole-transcriptome pathway activation claims. Set labels lack biological names, so a named mechanism cannot be assigned from the supplied annotation.

|Set|Called-gene overlap|BH adjusted p|
|---|---:|---:|
|SET01|1|0.956777|
|SET02|1|0.956777|
|SET03|10|3.41892e-05|
|SET04|1|0.956777|
|SET05|1|0.956777|
|SET06|2|0.956777|
|SET07|3|0.923471|
|SET08|1|0.956777|
|SET09|2|0.956777|
|SET10|0|1|
|SET11|5|0.143785|
|SET12|5|0.143785|

## Facility action and control plan
Issue the qualified adjusted list and distinguish qPCR-confirmed candidates from unvalidated panel calls. Before using borderline genes for costly downstream decisions, perform a count-model/mean–variance-aware sensitivity analysis and examine residuals and influential libraries. That sensitivity analysis has not been run here, so model robustness is not yet established.

For the next experiment, randomize and balance treatment arms within preparation batches; keep biological replication independent and record preparation and sequencing factors. Validate remaining priority candidates on independent biological material, including increased-expression candidates not represented in the current nominated validation panel. Require prospective QC, design-rank checks, locked normalization and calling rules, and directional validation review before release. Archive the raw steward batches, analysis script, gene results and trace with the release. Monitor future batch-associated variation and investigate preparation practices if it persists.

All requested study batches were supplied; no steward-denied data gaps occurred. No wet-laboratory remediation was performed and no post-change laboratory improvement was measured. The achieved change is an auditable, batch-adjusted inference with independent support for the nominated subset, not a demonstrated improvement to the sequencing process.
