# Compound expression study: decision for the principal investigator

## Executive decision
**Withhold the candidate list and reconsider the panel findings.** Technical quality and the recorded design permit an expression comparison, but independent validation does not support release. This is not evidence that the compound has no biological effect; it is failure to substantiate the proposed response list.

## Library quality and design
All 12 libraries meet the facility's assigned-read and mapping-rate requirements; 0 fail. Usable replication is 6 controls and 6 treated libraries, satisfying the replication gate. QC alone does not justify a biological conclusion.

The usable sample sheet contains 1 preparation batch. Both arms occur within it. The intercept-plus-treatment matrix has rank 2 for 2 columns: treatment is not confounded with recorded preparation batch. A separate batch effect cannot be estimated here and a redundant batch term was not fitted. No resequencing or batch correction was necessary on the recorded QC/design criteria. Unrecorded confounders cannot be excluded by this check.

## Panel analysis: provisional, not validated
I normalized counts by each library's panel count total, applied a half-count pseudocount and log transformation, and compared independent arms with two-sided Welch tests. Benjamini–Hochberg adjustment covered all 400 genes. Calls required adjusted p < 0.05 and absolute log fold change >= 1.0. This log-expression analysis assumes panel-total scaling is appropriate and is not a negative-binomial count-model analysis; a count-model sensitivity analysis is recommended before renewed nomination.

The analysis yields 40 provisional calls: 17 increased and 23 decreased. They are listed below solely as audit results, not as an issued candidate list. Fold changes are treated minus control on the log scale.

| Gene | Log fold change | Adjusted p |
|---|---:|---:|
| G0002 | -1.795311 | 0.0011652 |
| G0005 | -2.095742 | 0.00107552 |
| G0019 | -2.703681 | 0.0450799 |
| G0038 | 2.454162 | 0.000426347 |
| G0045 | 1.338657 | 0.000364165 |
| G0055 | 2.061432 | 0.000190898 |
| G0060 | -1.718181 | 0.00124418 |
| G0062 | 2.111020 | 0.000345106 |
| G0100 | -1.706200 | 0.000663091 |
| G0108 | -2.725826 | 7.38877e-05 |
| G0112 | -2.387444 | 0.000740906 |
| G0125 | -2.814592 | 0.000412623 |
| G0153 | 2.703595 | 0.000155479 |
| G0156 | -1.971860 | 0.000136933 |
| G0165 | 1.847941 | 0.000742896 |
| G0169 | 1.737505 | 0.00127226 |
| G0173 | 1.919196 | 0.00328377 |
| G0210 | -1.773541 | 0.0106613 |
| G0214 | -2.559490 | 0.000136933 |
| G0215 | -2.504124 | 0.000136933 |
| G0237 | -1.702266 | 0.00443583 |
| G0239 | 1.636083 | 0.00113932 |
| G0241 | -2.837827 | 0.00144788 |
| G0244 | 2.160492 | 0.000186235 |
| G0247 | -1.817264 | 0.00240761 |
| G0263 | 1.414873 | 0.00829602 |
| G0265 | -1.719263 | 0.000136933 |
| G0267 | -2.119284 | 0.00189649 |
| G0271 | 1.284258 | 0.000869525 |
| G0284 | 2.812078 | 0.000136933 |
| G0314 | -2.240319 | 0.000560395 |
| G0327 | 2.163959 | 0.000136933 |
| G0333 | -2.288880 | 0.000869525 |
| G0339 | -2.276172 | 5.12958e-05 |
| G0341 | 1.549000 | 0.000193013 |
| G0366 | -2.597640 | 0.00055207 |
| G0370 | 2.129133 | 0.000186235 |
| G0372 | -2.099593 | 0.000136933 |
| G0379 | -1.709645 | 0.000742896 |
| G0387 | 2.273670 | 0.000186235 |

## Independent validation and stopping point
The archive nominated 10 leading candidates for independent qPCR, rather than testing every panel call. I used two-sided Welch tests on the supplied log relative expression, requiring p < 0.05 and the panel's expected direction. All nominated genes are among the provisional panel calls.

Confirmed: 0 of 10; concordance 0.00, below the required 0.75. Consequently, no candidate list is authorized. Lack of confirmation is not proof of equivalence or of absent compound response.

| Candidate | qPCR treated-minus-control | p value | Confirmed |
|---|---:|---:|---|
| G0125 | -0.13125 | 0.423329 | No |
| G0241 | 0.26050 | 0.463912 | No |
| G0284 | 0.20150 | 0.552641 | No |
| G0108 | -0.33875 | 0.324079 | No |
| G0153 | -0.01100 | 0.954220 | No |
| G0366 | -0.30800 | 0.064897 | No |
| G0214 | -0.10650 | 0.717203 | No |
| G0215 | 0.26575 | 0.057324 | No |
| G0038 | -0.24075 | 0.439072 | No |
| G0112 | -0.17875 | 0.297004 | No |

Gene-set annotation was requested but **locked by the failed validation gate**. It was not denied as nonexistent. No annotation data were released and no enrichment was computed; pathway interpretation stops here. No batch variance fraction was computed because recorded batch has no variation.

## What changed, what it achieved, and next steps
The analytical disposition changed from provisional panel nomination to a release hold after independent validation. No experimental intervention has been performed, and no corrective improvement in biological concordance has been demonstrated. The achieved safeguard is prevention of an unsupported list and downstream pathway claims.

The proximate reason for withholding is panel–qPCR nonconfirmation, not poor sequencing metrics or recorded batch confounding. Its underlying cause is unresolved. The facility should audit sample identity and arm labels, exposure and harvest records, qPCR reference-gene stability, primer specificity, assay efficiency and plate controls; reconcile the normalization and biological material used by the platforms. These are hypotheses to investigate, not established defects. Reanalyse archived counts with a prespecified count-based model and suitable normalization, without tuning thresholds to rescue the list. Plan an independently replicated, adequately powered validation after the audit, with randomization and arm balance across any future preparation batches.

Hold release under a documented quality gate: archive counts, scripts, full results and candidate nominations; require independent review of QC, design estimability, multiplicity control and validation concordance before unlocking annotation or issuing any list. A failed gate should trigger documented investigation rather than selection of a favorable subset. Full computed panel and validation results are retained in the accompanying CSV files; analysis steps and scalar audit results are in trace.json.
