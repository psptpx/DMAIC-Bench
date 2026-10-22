# Compound-expression study: disposition

## Executive decision
The libraries are usable and the arm contrast is identifiable, but this analysis does **not establish a compound-responsive gene list**. None of the 400 panel genes meets the facility's joint statistical and effect-size criteria. This is a failure to detect qualifying effects, not proof that the compound has no biological activity.

## Library quality and study design
All 12 libraries pass both usability criteria; 0 fail. Each arm retains 6 usable biological replicates, exceeding the required 3. The lowest assigned-read count is 9,325,000 and the lowest mapping rate is 0.861, against thresholds of 5,000,000 and 0.70, respectively. There is no QC-driven reason to discard libraries or repeat sequencing.

Both arms share 1 preparation batch. The intercept-and-treatment design has rank 2 for 2 columns: treatment is not confounded with preparation batch. A simple arm comparison is therefore estimable. Between-batch variability cannot be estimated from this design; these data do not establish robustness across preparation batches. Identifiability also does not independently establish random allocation or exclude unrecorded biological confounders.

## Expression analysis and result
I normalized each library by the median ratio to gene-wise geometric means, using genes positive in every library to estimate size factors. I compared log-base-two normalized counts after adding a pseudocount of 1, using two-sided Welch tests on biological replicates. Benjamini–Hochberg correction covered all 400 genes, without outcome-driven filtering. The reported effect is the treated-minus-control mean log expression, an approximation to a log fold change.

The calling rule was adjusted p < 0.05 and absolute log fold change >= 1.0. The qualifying list is empty: 0 total, with 0 increases and 0 decreases. Full gene-wise effects, raw p-values and adjusted p-values are in `gene_results.csv` and the trace. This is a transparent log-scale screening analysis, not a fitted negative-binomial count model; conclusions are conditional on its normalization and variance assumptions. The panel cannot establish genome-wide absence of response, and an equivalence or prospective power analysis was not performed.

## Independent validation and annotation
The released validation record explicitly states that no candidates were nominated: 0 candidates and 0 confirmed candidates. There are no qPCR observations from which to evaluate agreement. Concordance is undefined because the denominator is empty; it is neither a pass nor a failed validation, and it supplies no independent evidence for issuing a list.

The steward locked gene-set annotation behind the validation-concordance gate. I did not declare an invented score to unlock it. Annotation was not released, and enrichment was not computed. This is a locked precondition, not a steward denial that annotation does not exist. Biological pathway interpretation stops here; there is also no qualifying gene list to enrich.

## Business implications and next actions
No experimental process was changed, no library was removed, and no batch correction was imposed. The analytical changes were normalization and panel-wide multiplicity control; they produced no qualifying calls. Neither QC failure nor arm–batch confounding explains the absence of a reportable list. These data cannot distinguish a genuinely weak response from insufficient sensitivity, unsuitable exposure conditions, or effects outside the targeted panel.

Issue a QC-passing, design-estimable **no qualifying response detected** report, not a validated positive list and not a claim of biological equivalence. Before further assay work, review compound exposure, timing and positive-control evidence with the investigator. If smaller effects matter, define that target prospectively and plan power from observed variability. Confirm any future candidates with an independent experiment; use balanced allocation within preparation batches if multiple batches are introduced. Do not resequence solely to fix a QC problem that was not observed.

Retain the released records, executable `analysis.py`, full gene results and `trace.json` under version control. For future studies, hold the same prespecified QC and calling gates, document sample allocation, and require actual independent validation observations before declaring concordance or releasing a validated list. Numerical report statements are drawn from the corresponding QC, design, expression and candidate-accounting outputs in the trace.
