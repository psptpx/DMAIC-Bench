# Compound-response study: assessment for the principal investigator

## Executive decision
The libraries are technically usable and the intended contrast is estimable after accounting for preparation batch. However, the batch-adjusted analysis detected **0 responding genes** among **400 tested genes** under the facility calling rules. Do not issue a compound-response gene list or a pathway claim from this study. This is absence of detected evidence, not proof that the compound has no biological effect.

## Library quality and design
Applying both assigned-read and mapping-rate requirements jointly yielded **0 failed libraries** out of **12**. Both control and treated arms retained **6 usable biological replicates**, so the minimum usable-replicate requirement is satisfied. No samples were removed.

There are **2 preparation batches**. The first batch contains **5 control and 1 treated** library; the second contains **1 control and 5 treated** libraries. Consequently, batch and treatment are imbalanced but not completely confounded. The intercept-plus-batch-plus-treatment design has rank **3** for **3 columns**, permitting an adjusted treatment estimate. The sparse crossover makes that estimate less precise and sensitive to the additive-model assumption.

## Expression analysis and interpretation
Counts were converted to panel-total counts per million, then log transformed with a pseudocount. The marginal fraction of within-gene log-expression variation associated with batch was **0.676900**. This is a descriptive variance fraction, not a causal estimate of the effect of preparation: some variation is shared with treatment because of allocation imbalance.

For each gene, ordinary least squares modeled log expression as a function of preparation batch and treatment. Treatment coefficients were tested with two-sided residual t tests and Benjamini–Hochberg correction across the panel; calls additionally required the facility effect-size threshold. The models had **9 residual degrees of freedom**. No genes met both calling criteria. Full estimates and adjusted significance measures are saved in `gene_results.csv`; their coefficients and adjusted values are also recorded in the trace.

The analytical change was to block on preparation batch rather than attribute the arm difference directly to compound exposure. This produced an adjusted, estimable comparison without a supported response list. No laboratory remediation or repeat experiment was performed, and no numerical benefit relative to an unadjusted analysis is claimed because that analysis was not run.

These are exploratory log-count linear models, not a dispersion-moderated count-model pipeline. Panel-total normalization assumes panel composition is sufficiently stable and cannot identify a panel-wide absolute expression shift. The batch-heavy allocation and limited crossover constrain sensitivity; failure to call genes is not an equivalence test. A count-aware sensitivity analysis and normalization review would be appropriate before treating this as the definitive negative result.

## Validation and the stopping boundary
The released validation batch explicitly reports no nominated candidates: **0 candidates** and therefore **0 confirmed candidates**. It contains no qPCR observations. Validation concordance is undefined because its denominator is empty; it cannot be scored as either a successful validation or a measured discordance. Independent validation therefore does not support issuing any list, and conclusions stop at the adjusted panel analysis.

The gene-set annotation request was **locked**, not denied as nonexistent, because the validation-concordance gate could not be satisfied. No concordance was invented to bypass the gate. No enrichment analysis was computed, and no pathway conclusion is warranted.

## Facility action and control plan
- Release a qualified technical report: libraries passed QC, the adjusted contrast was identifiable, and no response genes were detected with this method.
- Audit preparation allocation and processing records to understand the strong batch association; do not label batch as a proven causal mechanism from these observational patterns alone.
- For follow-up, randomize and balance both arms within every preparation and sequencing batch, preserve biological independence, and document allocation before library preparation. Where feasible, add reference material and suitable normalization controls.
- Reassess precision and prospective power using the observed variability and biologically relevant effects before choosing follow-up replication. Neither power nor a required future sample size was computed here.
- Predefine normalization, count-aware modeling, multiplicity control and candidate nomination before examining follow-up results. Independently validate any future nominated candidates using the facility direction-and-significance rule.
- Hold the process with sample-sheet design-rank checks, per-library QC gates, documented batch balance, versioned analysis code and an explicit validation release gate. Monitor follow-up batch variation and retain an audit trail; improvement cannot be claimed until follow-up measurements demonstrate it.

## Audit materials
`analysis.py` contains the computations, `trace.json` records their numerical results and routing decisions, and `gene_results.csv` retains the gene-level output. Released steward JSON files and the annotation refusal are retained alongside them. No outside study-fact clarification was needed.
