# Compound expression study — PI report

## Decision
The libraries are usable and the intended compound-versus-vehicle contrast is estimable. Under the explicitly described analysis, **39 genes meet the facility's calling criteria**, with 23 higher and 16 lower in treated cells. These are panel-specific expression findings, not proof of a mechanism or an absolute change in total cellular RNA.

## Library quality and design
All 12 libraries pass the supplied library rules; 0 fail. The retained arms each contain 6 biological replicates. The lowest assigned-read count is 11,363,000 and the lowest mapping rate is 0.866. No library was excluded and QC does not justify re-sequencing.

The retained sample sheet contains 1 shared preparation batch. Treatment is not confounded with batch: the intercept-and-treatment design has rank 2 for 2 columns. A separate batch coefficient is neither identifiable nor necessary for a constant batch. Between-batch variation cannot be estimated from this study; this limits generalization across future preparation runs, not the within-run treatment contrast.

## Analysis and findings
Counts were aligned to the sample sheet. Median-ratio size factors were computed using genes positive in every library and centered geometrically. Normalized counts were log-transformed with a unit pseudocount. Each gene was compared using a two-sided Welch test of treated versus control log expression. Benjamini–Hochberg adjustment covered all 400 panel genes. Calls required adjusted p < 0.05 and absolute log-fold change >= 1.0. Log-fold changes below are on the base-two scale, calculated as differences in mean transformed expression; they are not raw-count ratios.

This is a transparent log-scale expression analysis, not a fitted negative-binomial count model. It assumes reasonably behaved transformed biological-replicate measurements and that most panel genes provide a stable normalization reference. A targeted panel may violate the latter assumption if regulation is pervasive. The calls should therefore be validated with independent reference measurements and an independent experiment before mechanistic or clinical use. Genes not called are not established as unchanged.

### Called genes
Positive values denote higher expression with compound. Full precision statistics for every tested gene are in `gene_results.csv` and `trace.json`.

| Gene | Log-fold change | BH adjusted p |
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

## Business implications and next actions
The immediate obstacle was uncertainty about library usability and design, not a demonstrated sequencing failure. The QC and rank checks resolve those prerequisites. The analytical change was to normalize library composition before comparing arms and control panel-wide multiplicity; no experimental process, sample, or treatment was changed. No before/after process improvement has been measured.

Proceed with the called-gene shortlist for independent biological validation, preferably with an orthogonal expression assay and stable reference controls. Do not re-sequence these libraries solely to cure a problem absent from their QC. For future replication, randomize both arms within each preparation batch, balance processing order, retain biological replication, and include batch in the analysis when it varies. Archive the sample manifest, raw counts, scripts, normalization factors, and complete results together. The core should enforce library acceptance and design-rank checks before releasing gene calls, and the PI should approve validation targets before follow-up work begins.

All released batches were analyzed; no batch was denied. No independent validation or post-change follow-up was supplied or computed, so demonstrated reproducibility and sustained process improvement remain unestablished. The present conclusion stops at this experiment's normalized panel expression comparison.

## Audit trail
`trace.json` records the computed QC, design and expression results in execution order. `analyze.py`, `design.py`, and `expression.py` preserve the computations. An initial expression-script syntax error was corrected before any expression computation ran. Reported numerical results are drawn from trace outputs; table entries are rounded displays of those values.
