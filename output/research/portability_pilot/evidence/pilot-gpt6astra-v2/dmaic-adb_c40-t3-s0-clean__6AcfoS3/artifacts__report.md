# Compound expression study: decision for the principal investigator

## Executive decision
The libraries and design support a treatment comparison. Issue the panel candidate list with clear validation labels: 39 genes meet the panel calling criteria, and all 10 independently nominated qPCR candidates confirm (concordance 1.0, exceeding the required 0.75). This supports the facility’s release gate, not a claim that every panel candidate has been independently validated or that the compound’s molecular mechanism is established.

## Library quality and design
All 12 libraries are usable; 0 fail QC. There are 6 usable control and 6 usable treated replicates. The lowest assigned-read count is 11,363,000 and the lowest mapping rate is 0.866. No libraries were removed and no resequencing is indicated by these metrics.

Both arms occur in the same preparation batch (batch count 1). The intercept-plus-treatment model has rank 2 for 2 columns; treatment is not confounded with batch. A batch effect cannot be separately quantified across batches here, and no batch correction was applied. This design supports the intended within-batch comparison, but does not establish reproducibility across preparation batches.

## Panel analysis
Counts were normalized by median ratios using genes positive across libraries, then log-transformed with a unit pseudocount. Independent Welch tests compared log expression between arms; Benjamini–Hochberg correction covered all 400 tested genes. Calls required adjusted p < 0.05 and absolute log fold change on the doubling scale >= 1.0. The analysis produced 39 calls. This is a transparent log-expression analysis rather than a fitted negative-binomial count model; a count-model sensitivity analysis is recommended before downstream mechanistic investment.

Positive effects indicate higher expression under compound. The following list is the computed panel result, not blanket qPCR confirmation.

| Gene | Log fold change (doubling scale) | Adjusted p |
|---|---:|---:|
| G0006 | 1.98722 | 0.00251147 |
| G0007 | 1.47597 | 0.00972248 |
| G0010 | 2.09651 | 0.000436418 |
| G0037 | 1.65283 | 0.000302078 |
| G0039 | 2.21941 | 0.00223061 |
| G0052 | -2.14729 | 0.000170796 |
| G0061 | 2.45391 | 0.000123835 |
| G0101 | 2.0833 | 9.91599e-05 |
| G0107 | 1.88145 | 0.000261671 |
| G0110 | 2.03843 | 0.000125665 |
| G0114 | -1.38112 | 0.000515179 |
| G0115 | -2.19541 | 5.78333e-05 |
| G0118 | 2.01639 | 0.0014981 |
| G0124 | -2.38966 | 0.000179702 |
| G0131 | 2.53222 | 7.46102e-05 |
| G0149 | -1.40825 | 0.011652 |
| G0153 | 1.87486 | 0.000349629 |
| G0154 | -2.33179 | 0.000476913 |
| G0155 | -1.79112 | 0.00731897 |
| G0187 | -2.46825 | 0.000170796 |
| G0194 | 1.9919 | 0.000101826 |
| G0212 | 1.45351 | 0.00375683 |
| G0247 | -2.33294 | 7.46102e-05 |
| G0260 | 1.9499 | 0.000701724 |
| G0276 | -2.46308 | 0.000180212 |
| G0277 | 3.00792 | 7.46102e-05 |
| G0279 | 2.14478 | 7.46102e-05 |
| G0280 | -1.65253 | 0.00185564 |
| G0287 | 2.16399 | 7.46102e-05 |
| G0293 | 2.21904 | 0.00111471 |
| G0299 | -2.86946 | 0.000123722 |
| G0310 | 2.20983 | 0.000155149 |
| G0311 | -2.45985 | 0.00526489 |
| G0314 | -2.62213 | 9.91599e-05 |
| G0331 | 2.45534 | 0.000563079 |
| G0372 | -2.14585 | 0.023964 |
| G0374 | 1.93827 | 0.0031103 |
| G0383 | 1.33458 | 0.00745229 |
| G0394 | -1.30254 | 0.005597 |

## Independent validation
Two-sided independent Welch tests were applied to the supplied relative-expression measurements. Confirmation required p < 0.05 and agreement with the nominated panel direction. All nominated genes are also called by this panel analysis. The results support release under the facility rule, with validation restricted to the nominated subset.

| Nominated gene | qPCR treatment-minus-control | p | Confirmed |
|---|---:|---:|---|
| G0299 | -1.9305 | 0.000221657 | Yes |
| G0277 | 2.9565 | 5.5518e-05 | Yes |
| G0314 | -1.5515 | 0.00023871 | Yes |
| G0311 | -2.01875 | 0.000442734 | Yes |
| G0276 | -1.74775 | 4.79963e-05 | Yes |
| G0187 | -1.6 | 0.000395465 | Yes |
| G0124 | -1.63525 | 0.000587964 | Yes |
| G0154 | -2.00375 | 0.000101102 | Yes |
| G0247 | -2.10475 | 7.23749e-05 | Yes |
| G0115 | -2.07725 | 1.91451e-06 | Yes |

## Gene-set interpretation
One-sided hypergeometric overrepresentation against the tested panel, with BH correction across 12 supplied sets, found 1 significant sets. This targeted-panel background avoids treating unmeasured genes as negatives. Anonymous set identifiers do not establish a named biological mechanism.

| Significant set | Candidate overlap | Adjusted p |
|---|---:|---:|
| SET03 | 20 | 5.44133e-15 |

## Action and control plan
The observed treatment-associated expression changes are not explained by an arm-versus-preparation-batch split, and orthogonal validation supports the nominated signals. No laboratory process was changed in this analysis. Normalization addressed sample-scale differences; QC and estimability checks qualified the data, and validation changed the decision from provisional to releasable candidates. These results do not prove a causal molecular pathway.

Release the list with panel-only versus qPCR-confirmed status preserved. Archive the source batches, executable scripts, per-gene results and trace. The core should freeze its normalization, multiplicity and release rules; verify sample identities and assay controls; and retain the same QC, design and validation gates for future studies. Follow-up experiments should randomize both arms across preparation batches and prospectively validate additional candidates. No requested batch was denied; no missing stage has been filled with an invented result.
