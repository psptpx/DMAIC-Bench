# Compound-response study: decision report

## Executive decision
The libraries and design support an interpretable within-batch compound-versus-vehicle comparison. Release the panel response list with its statistical-method and scope qualifications: 39 genes meet the facility call rule, and the nominated qPCR validation passes. This is not evidence that every listed gene has been independently validated, nor proof of a mechanism.

## Library fitness and design
All 12 libraries are usable; 0 fail QC. Each arm retains 6 usable biological replicates against the required minimum of 3. The lowest assigned-read count is 11,363,000 and the lowest mapping rate is 0.866. The facility usability rules were applied jointly, without exclusions or imputation.

The sample sheet contains 1 preparation batch shared by both arms. Treatment is not confounded with batch; the design matrix has rank 2 and 2 columns. A separate batch variance component cannot be estimated from this design. Adding a batch correction would not identify an additional effect. Causal attribution still relies on biological handling and treatment allocation being comparable, which the sheet alone cannot establish.

## Expression analysis
Median-ratio normalization was followed by log-transformation with a pseudocount, independent two-sided Welch tests, and Benjamini–Hochberg correction over 400 panel genes. Calls require adjusted p < 0.05 and absolute log-fold change on the base-two scale >= 1.0. There are 23 increases and 16 decreases. Effects are differences in mean transformed normalized expression, not raw-count ratios. This is an exploratory log-scale analysis, not a fitted negative-binomial model; the facility should review count-model sensitivity before treating borderline calls as definitive.

Full results, including noncalls, are in `gene_results.csv`. Noncalls are not proof of no response.

### Called genes
| Gene | Direction | Log-fold change (base two) | BH adjusted p |
|---|---|---:|---:|
| G0006 | up | 1.9872 | 0.00251173 |
| G0007 | up | 1.4759 | 0.00972368 |
| G0010 | up | 2.0965 | 0.000436405 |
| G0037 | up | 1.6527 | 0.000302091 |
| G0039 | up | 2.2193 | 0.00222985 |
| G0052 | down | -2.1467 | 0.000170353 |
| G0061 | up | 2.4538 | 0.000123846 |
| G0101 | up | 2.0832 | 9.91648e-05 |
| G0107 | up | 1.8814 | 0.000261721 |
| G0110 | up | 2.0384 | 0.000125673 |
| G0114 | down | -1.3805 | 0.000516081 |
| G0115 | down | -2.1952 | 5.78786e-05 |
| G0118 | up | 2.0162 | 0.00149903 |
| G0124 | down | -2.3894 | 0.000179529 |
| G0131 | up | 2.5321 | 7.46051e-05 |
| G0149 | down | -1.4079 | 0.0116593 |
| G0153 | up | 1.8747 | 0.000349559 |
| G0154 | down | -2.3309 | 0.000478354 |
| G0155 | down | -1.7906 | 0.00730432 |
| G0187 | down | -2.4663 | 0.000170353 |
| G0194 | up | 1.9916 | 0.000101724 |
| G0212 | up | 1.4535 | 0.00375706 |
| G0247 | down | -2.3326 | 7.46051e-05 |
| G0260 | up | 1.9499 | 0.000701775 |
| G0276 | down | -2.4610 | 0.000181026 |
| G0277 | up | 3.0078 | 7.46051e-05 |
| G0279 | up | 2.1448 | 7.46051e-05 |
| G0280 | down | -1.6525 | 0.0018552 |
| G0287 | up | 2.1640 | 7.46051e-05 |
| G0293 | up | 2.2188 | 0.0011138 |
| G0299 | down | -2.8670 | 0.000122656 |
| G0310 | up | 2.2098 | 0.000155153 |
| G0311 | down | -2.4575 | 0.00522944 |
| G0314 | down | -2.6218 | 9.91648e-05 |
| G0331 | up | 2.4549 | 0.000563829 |
| G0372 | down | -2.1405 | 0.0233887 |
| G0374 | up | 1.9381 | 0.00311027 |
| G0383 | up | 1.3345 | 0.00745304 |
| G0394 | down | -1.3021 | 0.00559529 |

## Independent qPCR validation
Using independent two-sided Welch tests on supplied log-relative-expression measurements and the nominated panel direction, 10 of 10 candidates confirm at nominal p < 0.05. Concordance is 1.0, exceeding the required 0.75. All nominated directions also agree with this analysis. The validation therefore supports issuing the list under the facility rule, but selection of leading candidates prevents interpreting this concordance as an unbiased accuracy estimate for the whole list.

| Candidate | qPCR effect | p value |
|---|---:|---:|
| G0299 | -1.9305 | 0.000221657 |
| G0277 | 2.9565 | 5.5518e-05 |
| G0314 | -1.5515 | 0.00023871 |
| G0311 | -2.0188 | 0.000442734 |
| G0276 | -1.7478 | 4.79963e-05 |
| G0187 | -1.6000 | 0.000395465 |
| G0124 | -1.6353 | 0.000587964 |
| G0154 | -2.0037 | 0.000101102 |
| G0247 | -2.1048 | 7.23749e-05 |
| G0115 | -2.0773 | 1.91451e-06 |

## Panel-restricted gene-set interpretation
One-sided hypergeometric tests used the 400 measured genes as the background, with BH correction across 12 annotated sets. There are 1 significant sets at adjusted p < 0.05.

| Set | Called overlap | Set size | BH adjusted p |
|---|---:|---:|---:|
| SET01 | 5 | 30 | 0.372448 |
| SET02 | 2 | 30 | 0.815874 |
| SET03 | 20 | 30 | 5.44133e-15 |
| SET04 | 5 | 30 | 0.372448 |
| SET05 | 4 | 30 | 0.499763 |
| SET06 | 6 | 30 | 0.235104 |
| SET07 | 3 | 30 | 0.694261 |
| SET08 | 2 | 30 | 0.815874 |
| SET09 | 3 | 30 | 0.694261 |
| SET10 | 4 | 30 | 0.499763 |
| SET11 | 6 | 30 | 0.235104 |
| SET12 | 4 | 30 | 0.499763 |

Set identifiers have no biological names in the supplied annotation; do not invent pathway labels or extrapolate enrichment to the whole transcriptome.

## What changed, what it achieved, and how to hold the result
No libraries were replaced, no laboratory process was altered, and no corrective intervention was tested. The analytical change from raw counts was normalization for library scale, followed by multiplicity-controlled screening and an independent validation check. These steps distinguish a technically usable, identifiable and validation-supported response list from unfiltered differences; they do not demonstrate an operational improvement in the facility.

Issue the list as panel-limited, marking the nominated qPCR-confirmed subset separately. Archive the steward releases, scripts, trace and complete gene results with the report. Have the analyst review normalization assumptions and count-model sensitivity, and have the study lead confirm treatment allocation and handling comparability. Prioritize independent follow-up for unvalidated calls and mechanistic work only after biological review. For future runs, balance arms across preparation batches, retain biological replication, lock QC and calling rules before analysis, and continue independent direction-sensitive validation. No released batch was denied; there is no missing-data refusal to substitute with an assumption. Generalization across batches and a demonstrated process-improvement effect remain unmeasured.

Numerical provenance: library fitness, design, expression, validation and enrichment correspond in order to the successful steps in `trace.json`; displayed values are rounded from their outputs.
