# Compound-versus-vehicle study: decision report

## Executive conclusion
The libraries are usable and the intended treatment comparison is identifiable. The analysis calls **0 responding genes** among **400 tested genes**. This is a negative detection result for this panel under the facility's calling rule, not evidence of biological equivalence or absence of effects outside the panel.

## Library quality and design
All **12 libraries** passed the facility's assigned-read and mapping-rate rules; **0 failed**. Each arm retained **6 usable biological replicates**, satisfying the replication gate. The lowest assigned-read count was **9,325,000**, and the lowest mapping rate was **0.861**. No library was excluded and no resequencing is indicated by these checks.

The sample sheet contains **1 preparation batch**, shared by both arms. The treatment design matrix has rank **2** for **2 columns** and is not confounded. A separate batch effect cannot be estimated from a shared batch, nor is a batch term needed here. Batch cannot explain away the contrast through treatment–batch aliasing in this design.

## Expression analysis and findings
Sample identities and arm labels were checked against the sample sheet. Counts were normalized by median ratios to gene geometric means, then log-transformed with a pseudocount. Per-gene treatment-only linear comparisons used pooled residual variance, followed by Benjamini–Hochberg adjustment over the full panel. The facility's adjusted-significance and absolute-effect criteria were applied jointly. Complete gene estimates, raw and adjusted probabilities, and calls are in `gene_results.csv`; the numerical results are also recorded in `trace.json`.

Normalization size factors ranged from **0.8198063825762534** to **1.2689197971307398**. The minimum adjusted probability was **0.8777304743536848** and the maximum absolute log-fold change on the base-two scale was **0.8692842996479331**. Thus there are **0 upregulated** and **0 downregulated** calls. No gene can be singled out as a confirmed compound responder from this analysis.

This is an approximate log-expression analysis, not a negative-binomial count model. It assumes most panel genes provide a stable normalization reference and uses unmoderated gene-specific residual variance. Low-count behavior, normalization assumptions, and modest biological replication limit sensitivity. No equivalence or prospective power calculation was performed. The data do not establish why a response was not detected: lack of compound activity, exposure conditions, modest effects, or panel coverage remain possible explanations rather than findings.

## Action and sustainment
No experimental or preparation change was made. The analytical change was normalization for relative library scale, followed by multiplicity-controlled inference; it produced a defensible negative detection result rather than an unadjusted candidate list. There is no before/after intervention evidence and no claim of an achieved process improvement.

Do not resequence solely to rescue significance when the supplied sequencing metrics pass. Before a new experiment, review compound exposure and target engagement with the study lead, assess whether this panel covers the intended mechanism, and consider an orthogonal biological assay. A validated count-model sensitivity analysis is advisable before treating this result as a definitive development decision. Any follow-up should prospectively define biologically relevant effects and replication needs, rather than select favorable genes post hoc.

Hold the workflow by retaining the brief, raw batches, sample-sheet linkage, executable `analyze.py`, and all results. Continue the library QC and replication gates before expression testing. Balance treatment arms within future preparation batches and include batch in the model when batches vary. No requested batch was denied; the conclusion is limited by the observed study and analysis assumptions, not an undisclosed missing data stage.
