# Compound-response study: decision report

## Executive decision
The libraries support the intended comparison. Release the panel-derived candidate list with a clear distinction between panel calls and independently validated candidates. No resequencing or batch rescue was required. These results support compound-associated expression responses in this experiment, not a proven causal molecular mechanism or generalization to other cell lines.

## Library quality and design
All 12 libraries are usable; 0 failed the facility's joint assigned-read and mapping-rate rules. Both control and treated arms retain 6 biological replicates. The design has 1 shared preparation batch, with both arms represented. The treatment model has rank 2 for 2 columns: treatment is estimable. A varying batch effect cannot be estimated in this study and was not inserted into the model. Batch variance was not computed.

## Panel analysis
Median-ratio size factors were computed from genes positive in every library. Log-transformed normalized counts with a unit pseudocount were analyzed by treatment-only ordinary least squares and two-sided t tests. Benjamini–Hochberg adjustment covered all 400 genes; the facility's adjusted-significance and absolute-fold-change rules were applied jointly. This yielded 39 calls: 23 increased and 16 decreased. This is a transparent log-expression approximation, not a negative-binomial count model; low-count and variance assumptions warrant sensitivity review before broader biological interpretation.

The table gives computed treatment-minus-control log-fold changes and adjusted p-values. Full results are in `gene_results.csv`.

| Gene | Log-fold change (base two) | Adjusted p |
|---|---:|---:|
| G0006 | 1.9872 | 0.00029262 |
| G0007 | 1.4759 | 0.0048407 |
| G0010 | 2.0965 | 0.000311264 |
| G0037 | 1.6527 | 0.00024971 |
| G0039 | 2.2193 | 0.00165409 |
| G0052 | -2.1467 | 0.000110656 |
| G0061 | 2.4538 | 8.31475e-05 |
| G0101 | 2.0832 | 6.63892e-05 |
| G0107 | 1.8814 | 9.58215e-05 |
| G0110 | 2.0384 | 8.31475e-05 |
| G0114 | -1.3805 | 0.000253292 |
| G0115 | -2.1952 | 2.05847e-05 |
| G0118 | 2.0162 | 0.000509477 |
| G0124 | -2.3894 | 2.05847e-05 |
| G0131 | 2.5321 | 3.70916e-05 |
| G0149 | -1.4079 | 0.00806635 |
| G0153 | 1.8747 | 0.000263531 |
| G0154 | -2.3309 | 9.58215e-05 |
| G0155 | -1.7906 | 0.00228079 |
| G0187 | -2.4663 | 0.000119679 |
| G0194 | 1.9916 | 6.63892e-05 |
| G0212 | 1.4535 | 0.000605391 |
| G0247 | -2.3326 | 2.44514e-05 |
| G0260 | 1.9499 | 9.58215e-05 |
| G0276 | -2.4610 | 9.58215e-05 |
| G0277 | 3.0078 | 3.70916e-05 |
| G0279 | 2.1448 | 2.05847e-05 |
| G0280 | -1.6525 | 0.000987904 |
| G0287 | 2.1640 | 2.05847e-05 |
| G0293 | 2.2188 | 0.000590037 |
| G0299 | -2.8670 | 6.63892e-05 |
| G0310 | 2.2098 | 9.58215e-05 |
| G0311 | -2.4575 | 0.00202069 |
| G0314 | -2.6218 | 2.97765e-05 |
| G0331 | 2.4549 | 6.63892e-05 |
| G0372 | -2.1405 | 0.00838323 |
| G0374 | 1.9381 | 0.00281345 |
| G0383 | 1.3345 | 0.00679332 |
| G0394 | -1.3021 | 0.00459418 |

## Independent validation
Two-sided Welch tests on the supplied independent qPCR log-expression measurements confirmed 10 of 10 nominated candidates in the expected direction, giving concordance 1.00. This passes the facility's release criterion. The nominated subset confirms the list-level validation gate; it does not individually validate every panel call.

| Nominated gene | qPCR treatment-minus-control | p-value |
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

## Functional interpretation
Using the tested panel as the background, hypergeometric overrepresentation tests with BH adjustment across 12 supplied sets found 1 significant sets.

- SET03: 20 called genes overlap; adjusted p = 5.44133e-15.

Set labels lack biological descriptions, so no named pathway mechanism is asserted. Panel-targeted enrichment is not genome-wide enrichment.

## Action and sustainment
No physical study change was made. Normalization addressed library-scale differences analytically; design review ruled out arm–batch confounding; validation changed the panel calls from provisional to eligible for candidate-list release. The biological source of each response remains to be established.

The facility should archive the released records, scripts, trace and full gene table, issue the candidate list with validation flags, and prioritize the independently confirmed genes for mechanistic follow-up. Review count-model sensitivity and assay specificity rather than treating every panel call as established mechanism. Future studies should randomize both arms within each preparation batch, retain usable replication, and maintain the same QC, estimability, multiplicity and independent-validation release gates. Do not revise thresholds after inspecting outcomes.

All requested batches were available; there was no steward-denied analysis gap. No external human clarification or experimental intervention was needed.
