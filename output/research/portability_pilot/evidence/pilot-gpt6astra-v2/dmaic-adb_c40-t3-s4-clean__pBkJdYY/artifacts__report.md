# Compound-expression study: decision for the principal investigator

## Executive conclusion
The sequencing libraries are technically usable, and the intended treated-versus-control comparison is estimable. However, the analysis found **0 qualifying genes among 400 tested**. No candidates were nominated for independent validation. There is therefore **no responsive-gene list to issue**, and the result should be reported as no qualifying response detected under this analysis—not proof that the compound has no biological effect.

## Library quality and design
All **12 libraries** pass the facility’s joint assigned-read and mapping-rate rules: **0 failed**, leaving **6 usable biological replicates in each arm**. The lowest assigned-read count was **9,325,000**, and the lowest mapping rate was **0.861**. Replication is sufficient under the standing rule, so the QC findings do not justify mandatory re-sequencing.

The usable sample sheet contains **1 preparation batch**, shared by both arms. The intercept-and-treatment design has rank **2** for **2 columns**; treatment is not confounded with batch. A simple treatment comparison is appropriate. A separate batch variance fraction cannot be estimated from a shared single batch, and adding a batch coefficient would not add information.

## Expression analysis
The full released count matrix was analyzed, not the steward’s truncated preview. Counts were normalized using median ratios to gene geometric means, using genes positive in every library. Size factors were scaled to have geometric mean unity. Expression was log-transformed after adding a unit pseudocount; treated and control mean log expression were compared using two-sided Welch tests. Benjamini–Hochberg adjustment covered the complete panel. Calls required both the adjusted-significance and absolute fold-change thresholds in the facility brief.

This yielded **0 upregulated and 0 downregulated qualifying genes**. Gene-level effects, raw probabilities, adjusted probabilities and calls are saved in `gene_results.csv`. This is a transparent log-scale approximation, not a fitted negative-binomial count model; borderline conclusions should be checked with a prespecified count-based model before treating the negative finding as definitive. The effect measure is the difference in mean transformed expression, not the logarithm of an arithmetic-mean count ratio.

## Validation and the stopping point
The released validation record explicitly says that no candidates were nominated. It contains **0 candidates** and no qPCR observations. The empty-set confirmed count is **0**, but **concordance is undefined**, not a successful validation rate and not evidence of validation failure. No candidate list can be independently endorsed from these records.

Panel gene-set annotation was requested but remains **locked** behind the concordance gate. It was not denied as nonexistent. An invented concordance was not declared to bypass that gate. Enrichment was not performed; with no qualifying genes and no released annotation, there is no supported pathway conclusion. The conclusion stops at the negative panel finding and the absence of candidate validation.

## Business implications and next actions
The limiting factor is not library failure or treatment–batch confounding. It is the absence of qualifying panel responses. These data do not identify a technical or biological cause for that absence. No physical intervention, re-sequencing, or experimental redesign was performed; the work applied the facility’s QC and design checks and normalized the released counts. It established that the comparison can be made, but did not produce a list for release.

Report the negative screen with its method limitations. Review exposure conditions, target engagement and biological relevance with the study lead before ordering more sequencing. If the decision requires stronger evidence of absence, estimate precision and plan an adequately powered follow-up for biologically meaningful effects; do not infer equivalence from nonsignificance. If a future analysis nominates candidates, obtain independent directional qPCR evidence and apply the standing concordance gate before release.

Hold this decision through versioned data, the retained scripts, `trace.json`, and `gene_results.csv`. Future runs should retain library QC and arm-replication checks, avoid treatment–batch confounding, prespecify normalization and testing, and prohibit candidate-list release without interpretable independent validation.

## Audit trail
All reported numeric results are in the QC, design, expression and validation outputs of `trace.json`. `analyze.py`, `design.py`, `expression.py`, and `finish.py` retain the calculations and report construction. The validation step is marked failed only because its requested rate is mathematically undefined, not because qPCR contradicted any nominated effect.
