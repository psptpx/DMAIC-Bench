# Compound-response study: investigator report

## Decision
The libraries are usable and the intended treatment comparison is estimable. The analysis identifies **39 responding genes** among **400 tested**, comprising **23 higher** and **16 lower** in treated cells. These are statistical expression calls under the documented analysis, not proof of mechanism or clinical efficacy.

## Library quality and design
All 12 libraries pass; 0 fail. Each arm retains 6 usable biological replicates, above the required 3. Usability required assigned reads at least 5,000,000 and mapping rate at least 0.7. The observed minima are 11,363,000 assigned reads and mapping rate 0.866.

The sample sheet contains 1 preparation batch shared by both arms. The intercept-and-treatment design has rank 2 for 2 columns. Treatment is therefore not confounded with preparation batch. No batch term is needed for this single-batch comparison. Between-batch variability cannot be estimated from this design, and the findings should not be assumed to generalize across preparation batches without confirmation.

## Analysis and calls
Counts were matched to usable sample identifiers. Library size factors were calculated by the median-ratio method using the 399 genes positive in all libraries, then geometrically centered. Expression was transformed as log base two of normalized counts plus 1. Independent, two-sided Welch tests compared treated and control log expression, with Benjamini–Hochberg adjustment over all 400 genes. Reported log fold change is the treated-minus-control mean log expression, rather than the log ratio of arithmetic mean counts. Calls require adjusted p < 0.05 and absolute log fold change >= 1.

This is a log-scale differential-expression analysis, not a negative-binomial model. Median-ratio normalization assumes most panel genes are not coordinately shifted. Low-count behavior and global expression shifts remain limitations. Noncalled genes are not established to be unaffected. A count-model sensitivity analysis and independent biological validation are recommended before consequential follow-up decisions; neither has been performed here.

| Gene | Log fold change (treated minus control) | BH adjusted p |
|---|---:|---:|
| G0006 | 1.9872 | 0.00251147 |
| G0007 | 1.4760 | 0.00972248 |
| G0010 | 2.0965 | 0.000436418 |
| G0037 | 1.6528 | 0.000302078 |
| G0039 | 2.2194 | 0.00223061 |
| G0052 | -2.1473 | 0.000170796 |
| G0061 | 2.4539 | 0.000123835 |
| G0101 | 2.0833 | 9.91599e-05 |
| G0107 | 1.8814 | 0.000261671 |
| G0110 | 2.0384 | 0.000125665 |
| G0114 | -1.3811 | 0.000515179 |
| G0115 | -2.1954 | 5.78333e-05 |
| G0118 | 2.0164 | 0.0014981 |
| G0124 | -2.3897 | 0.000179702 |
| G0131 | 2.5322 | 7.46102e-05 |
| G0149 | -1.4083 | 0.011652 |
| G0153 | 1.8749 | 0.000349629 |
| G0154 | -2.3318 | 0.000476913 |
| G0155 | -1.7911 | 0.00731897 |
| G0187 | -2.4682 | 0.000170796 |
| G0194 | 1.9919 | 0.000101826 |
| G0212 | 1.4535 | 0.00375683 |
| G0247 | -2.3329 | 7.46102e-05 |
| G0260 | 1.9499 | 0.000701724 |
| G0276 | -2.4631 | 0.000180212 |
| G0277 | 3.0079 | 7.46102e-05 |
| G0279 | 2.1448 | 7.46102e-05 |
| G0280 | -1.6525 | 0.00185564 |
| G0287 | 2.1640 | 7.46102e-05 |
| G0293 | 2.2190 | 0.00111471 |
| G0299 | -2.8695 | 0.000123722 |
| G0310 | 2.2098 | 0.000155149 |
| G0311 | -2.4599 | 0.00526489 |
| G0314 | -2.6221 | 9.91599e-05 |
| G0331 | 2.4553 | 0.000563079 |
| G0372 | -2.1459 | 0.023964 |
| G0374 | 1.9383 | 0.0031103 |
| G0383 | 1.3346 | 0.00745229 |
| G0394 | -1.3025 | 0.005597 |

## Business interpretation and next actions
Sequencing quality is not the limiting factor, and there is no observed preparation-batch aliasing to explain away the treatment contrast. The observed normalized expression differences support a compound-associated response in this experiment; the current records do not establish its molecular mechanism.

No libraries were discarded, no specimens were re-prepared, and no experimental intervention was made. The analytical change was to normalize library composition and account for multiple testing, enabling a reproducible list of candidate responses rather than interpreting raw read differences. No measured improvement from a facility process change is claimed.

Do not re-sequence solely on these QC results. Prioritize the called genes for orthogonal validation, confirm gene identities against the panel annotation, and evaluate a count-model sensitivity analysis before final biological prioritization. If the study is extended, randomize both arms within each preparation batch and retain the batch term whenever multiple batches are present.

Hold the workflow through documented release gates: retain library-level QC, verify usable replication by arm, check design rank before gene testing, lock normalization and calling rules, and archive the sample sheet, count matrix, scripts, and full gene results. `gene_results.csv` provides all tested genes; `trace.json` records the computations and numerical evidence. No requested batch was denied; all available study batches were used. Independent validation, mechanistic attribution, and improvement effectiveness were not computed and are not claimed.
