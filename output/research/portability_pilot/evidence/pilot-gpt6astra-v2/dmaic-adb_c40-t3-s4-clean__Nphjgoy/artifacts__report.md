# Compound-versus-vehicle expression study

## Decision for the principal investigator

The libraries and design support the intended comparison, but the analysis detected **0 qualifying genes**. Do not issue a compound-responsive candidate list. This is a negative discovery result under the facility's calling rule, not evidence that the compound has no biological effect.

## Library fitness and design

All **12 libraries** pass the combined assigned-read and mapping-rate rules; **0 fail**. There are **6 usable control replicates** and **6 usable treated replicates**. The smallest assigned-read count is **9,325,000**, and the lowest mapping rate is **0.861**. Thus inadequate sequencing quality or loss of replication is not the reason for the negative result.

All usable libraries share **1 preparation batch**, with both arms represented. The intercept-plus-treatment design has rank **2** for **2 columns**: treatment is estimable separately from the constant batch. A batch-adjustment term is not needed here, and between-batch variance cannot be estimated from this design.

## Expression analysis

We tested **400 genes** using median-ratio normalization, a log-transformed normalized-count analysis with a pseudocount, and per-gene Welch comparisons of treated against control. Benjamini–Hochberg adjustment covered the complete tested panel. A call required adjusted p **< 0.05** and absolute log-fold change on the binary logarithm scale **>= 1.0**. **0 genes** met both requirements. The complete effects, raw p-values, adjusted p-values and call flags are in `gene_results.csv`.

This is a transparent approximate analysis of transformed counts, not a fitted negative-binomial RNA-sequencing pipeline. The normalization assumes most panel genes are stable; the targeted panel alone cannot establish absolute transcript abundance or exclude a coordinated global shift. Before treating this result as a definitive negative study, the facility should review count-model sensitivity using a validated dispersion-aware workflow. The present analysis does not establish equivalence or adequate power for every biologically relevant effect.

## Validation and downstream interpretation

The released validation archive explicitly states that no candidates were nominated. It contains **0 candidates**, no qPCR observations, and consequently **0 confirmations**. This is an empty validation set, not a failed biological replication experiment. Concordance cannot be computed because its denominator is empty; neither a passing nor a failing validation fraction can honestly be assigned. Independent validation therefore adds no evidence for issuing a list, and there is no discovered list to validate.

The gene-set annotation request was **locked**, not denied as nonexistent, because the steward requires a computed passing validation concordance. We did not invent a fraction to bypass that rule. No enrichment analysis was performed and no pathway conclusion is supported.

## Actions, changes and control

No libraries were removed, no specimens were re-sequenced and no experimental process was changed. The analytical changes were normalization and explicit design verification; these allowed a technically interpretable comparison but did not produce qualifying discoveries. No improvement in biological response or process performance has been demonstrated.

Release this as a documented negative discovery analysis, with the methodological qualification above. Do not re-sequence solely on the basis of these QC results. If the scientific objective demands a stronger negative conclusion, first review exposure, timing, assay coverage and biologically meaningful effects with the study lead, then plan precision or power using appropriate variance estimates. If a revised experiment is warranted, balance treatment arms within preparation batches and prospectively specify normalization, the count model, multiplicity control and independent validation.

Hold the conclusion through versioned raw releases, retained analysis scripts, full gene-level results, and the machine-readable trace. Apply the same library, identifiability and validation gates to future work; an absent validation denominator must never be converted into a passing gate.
