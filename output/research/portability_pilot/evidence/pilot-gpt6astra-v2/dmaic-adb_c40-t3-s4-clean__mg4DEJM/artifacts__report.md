# Compound-versus-vehicle study: decision report

## Executive conclusion
The libraries are usable and the intended treatment contrast is estimable. However, **no genes meet the facility's joint significance and effect-size criteria**, so there is no compound-responsive candidate list to issue. This is a negative discovery result, not proof of biological equivalence or absence of smaller effects.

## Library quality and design
All 12 libraries passed the assigned-read and mapping-rate rules; 0 failed. Each arm retained 6 usable biological replicates. The lowest assigned-read count was 9,325,000 and the lowest mapping rate was 0.861. Thus library quality and replication do not require resequencing under the standing rules.

There is 1 preparation batch shared by both arms. The intercept-and-treatment design has rank 2 for 2 columns: treatment is not confounded with preparation batch. A separate batch term would be redundant here. Between-batch variability cannot be estimated from this design, and conclusions should not be generalized to preparation-batch robustness.

## Expression analysis
I used median-of-ratios library normalization, added a unit pseudocount, and tested log-transformed normalized expression with two-sided Welch comparisons. Fold changes are differences in mean base-two log expression, treated minus control. Benjamini–Hochberg correction covered all 400 tested genes. This is a log-scale approximate expression analysis, not a fitted negative-binomial model; full gene-level estimates and adjusted probabilities are saved in `gene_results.csv`.

Calls required adjusted p < 0.05 and absolute log fold change >= 1. The result was 0 called genes: 0 upregulated and 0 downregulated. No enrichment or mechanistic claim follows from this empty discovery set. Normalization assumes most panel genes do not undergo a coordinated shift; absolute global expression changes are not identifiable from relative counts alone.

## Validation and limits of the evidence
The released validation batch explicitly says that no candidates were nominated. Computed inventory counts are 0 candidates and 0 validation records. Consequently, validation concordance cannot be computed: there is no denominator. This is neither a validation failure nor a successful validation, and I did not substitute an artificial concordance to pass the release gate.

The steward kept the panel gene-set annotation **locked** behind the validation-concordance gate. It did not deny the existence of that annotation. No annotation data were released and no enrichment analysis was run. The conclusion stops at the panel's negative discovery result; there is no independent validation or pathway conclusion to report.

## Facility action and control
No experimental preparation, sequencing, or assay change was made during this analysis. The analytical actions were QC retention, explicit design checking, normalization, multiple-testing control, and withholding unsupported candidate claims. They established that the study is analyzable while preventing an empty validation set from being treated as evidence of confirmation. No improvement in assay performance has been demonstrated.

Do not resequence solely because the discovery list is empty. Review exposure, timing, biological response controls, and panel relevance with the investigator. Before any follow-up experiment, define the smallest biologically important effect and plan replication using observed variability; power was not computed here. Consider an independently specified count-model sensitivity analysis before relying on the negative result for a major program decision, without relaxing the calling thresholds post hoc.

Archive the released data, scripts, trace, and gene-level results. Preserve QC, estimability, multiplicity, and validation gates for future studies. If future preparations span batches, balance treatment arms within batches and include batch in the analysis. Any future candidate list must receive genuine independent validation before release.
