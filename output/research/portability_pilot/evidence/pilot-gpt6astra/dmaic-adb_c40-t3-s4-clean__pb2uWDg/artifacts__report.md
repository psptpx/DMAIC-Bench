# Compound-versus-vehicle expression study

## Executive conclusion
The libraries and design support the intended comparison, but this analysis finds **no genes meeting the facility's response criteria**. This is a valid negative screen under the stated analysis, not proof that the compound has no biological effect. No resequencing is indicated by library QC alone.

## Library usability and design
All **12 libraries** pass the joint assigned-read and mapping-rate requirements; **0 fail**. Each arm retains **6 usable biological replicates**, so the minimum retained arm size is **6**, satisfying the facility's replicate gate. No samples were excluded.

The sample sheet shows **1 shared preparation batch** containing both arms. The treatment design matrix has rank **2** for **2 columns**, so treatment is not confounded with preparation batch. A treatment-only analysis is appropriate here: a constant batch term is redundant with the intercept. Between-batch variation cannot be estimated from this study, and robustness across preparation batches remains untested.

## Expression analysis and findings
The complete **400-gene** panel was analyzed. Counts were normalized using median-ratio size factors derived from genes with positive counts in every library. A small pseudocount was added before logarithmic transformation. Per-gene, two-sided Welch tests compared normalized log expression between arms; Benjamini–Hochberg adjustment covered the full panel. Effect sizes are treated-minus-control mean log expression differences, representing approximate log fold changes rather than ratios of arithmetic mean counts.

The calling rule was adjusted p < **0.05** together with absolute log fold change on the base-two scale ≥ **1.0**. **0 genes** met both requirements: **0 upregulated** and **0 downregulated**. Consequently there is no qualifying responder list. Full gene-level effects, raw p-values, adjusted p-values, and call flags are saved in `gene_results.csv`; the corresponding computed quantities are also recorded in `trace.json`.

This is a log-expression Welch analysis, not a fitted negative-binomial count model. Its inference relies on the adequacy of transformed expression and independent biological replicates. Median-ratio normalization assumes that a broad panel-wide directional change does not dominate the reference. Failure to call genes does not establish equivalence, quantify power, or exclude smaller or variable effects. No power or equivalence analysis was performed. The records establish design estimability, not randomization or freedom from every possible biological confounder.

## What changed, what it achieved, and next actions
No laboratory intervention or design repair was performed. The analytical workflow retained all usable libraries, verified that the intended contrast was estimable, and normalized library scale before applying multiplicity and effect-size criteria. This achieved a defensible screen without manufacturing a responder list; it did not demonstrate an improvement in biological response or facility performance.

Before making a costly compound-development decision, the analysis lead should corroborate the negative screen with a count-based model and inspect normalization and individual-library expression patterns. The principal investigator should review exposure, timing, and expected mechanism and consider independent biological validation of prespecified targets if justified. Additional sequencing is not a remedy for absent treatment effects merely because a screen is negative.

For future work, keep treatment allocation balanced within preparation batches and retain the library-QC and design-estimability gates before gene calling. The facility should archive the sample sheet, released data, analysis scripts, trace, and gene table together; rerun the same documented gates whenever samples or counts change. Broader batch reproducibility requires a deliberately balanced follow-up, not an inferred batch estimate from this shared-batch experiment.

All requested study batches were released; there was no denied data stage. No intervention outcome or follow-up validation data were obtained, so claims of validated efficacy or achieved process improvement stop here.
