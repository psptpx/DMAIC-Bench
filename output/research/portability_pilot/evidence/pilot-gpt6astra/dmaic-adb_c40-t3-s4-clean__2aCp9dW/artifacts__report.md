# Compound-versus-vehicle study: decision report

## Executive conclusion
The libraries are usable and the intended treatment comparison is estimable. The analysis calls **0 responding genes among 400 tested**. This is a valid negative finding under the stated calling rules and the analysis described below, not proof that the compound has no biological effect or that the arms are equivalent.

## Library and design readiness
All **12 libraries** passed both facility QC criteria; **0 failed**. Each arm retains **6 usable biological replicates**, exceeding the required **3**. The lowest assigned-read count was **9,325,000**, versus the required **5,000,000**; the lowest mapping rate was **0.861**, versus the required **0.70**. There is no QC-based reason to discard libraries or resequence this study.

The sample sheet contains **1 preparation batch**, shared by both arms. Treatment is not confounded with batch. The intercept-plus-treatment design has rank **2** for **2 columns**, with **10 residual degrees of freedom**. Thus treatment can be compared within batch; a separate batch term is neither needed nor estimable here. Between-batch variation and reproducibility across preparation batches cannot be estimated from this study. This limitation does not prevent the within-batch comparison.

## Expression analysis and findings
Counts were aligned to the sample sheet, checking arm and batch labels. Median-ratio size factors were computed using the **400 genes** positive in every library. Normalized counts were transformed to base-two logarithms after adding a pseudocount of **1**. Gene-wise Welch comparisons of transformed expression were corrected using Benjamini–Hochberg across the full panel. Effect estimates are differences in mean transformed expression, interpreted as approximate log fold changes rather than untransformed arithmetic-mean ratios.

The facility calls genes only at adjusted p **< 0.05** and absolute log fold change **>= 1.0** on the base-two scale. **0 genes** meet both criteria. The minimum adjusted p-value is **0.909966**, and the largest absolute estimated log fold change is **0.869284**. No gene is nominated as a compound responder. All gene-level results are in `gene_results.csv`, with matching scalar results in `trace.json`.

This is an approximate transformed-expression analysis, not a dispersion-shrunk negative-binomial analysis. Median-ratio normalization assumes a sufficiently stable panel reference; a targeted panel cannot independently establish global transcriptional shifts. Low-count effects, sensitivity to modeling choices, and small effects remain limitations. A negative-binomial sensitivity analysis was not computed. No formal equivalence or power conclusion was computed. The supplied data do not establish why a molecular response was absent; inadequate exposure, timing, and genuine lack of effect cannot be distinguished here.

## Operational decision and next actions
**What changed:** no physical experiment, library preparation, or sequencing intervention was made. Analytically, all usable libraries were retained, library-scale normalization was applied, and multiplicity and effect-size gates were enforced. This achieved an estimable, QC-qualified comparison without nominating unsupported targets. There is no measured intervention benefit to claim.

**What to do next:** do not resequence solely to remedy a nonexistent QC failure. Before committing to a biological no-effect conclusion, review compound exposure, assay timing, and positive-control evidence with the study lead. Confirm the negative finding with a validated count-model sensitivity analysis. If follow-up is justified, prioritize independent biological replication and orthogonal expression validation rather than simply adding sequencing depth. No particular gene is supported for responder validation by the current calls.

**How to hold the result:** archive raw batches, scripts, sample identities, normalization factors, and full gene results. Keep QC and replication gates ahead of expression testing. For future preparations, distribute both arms within each batch and include batch in the model when applicable. Prespecify the gene-calling rule and record exclusions before looking at expression results. Require independent verification before making a mechanistic or therapeutic claim.

## Evidence and audit trail
All available steward batches were obtained; none was denied. The conclusion therefore does not stop at a missing requested batch, but it remains limited to this panel, this experiment, and the analysis performed. QC quantities are recorded under `qc.sample_qc`, design quantities under `design.identifiability`, and expression quantities and thresholds under `expression.de_simple` in `trace.json`. Reported decimal summaries are rounded from those outputs. Scripts are preserved as `analyze.py`, `design.py`, and `expression.py`.
