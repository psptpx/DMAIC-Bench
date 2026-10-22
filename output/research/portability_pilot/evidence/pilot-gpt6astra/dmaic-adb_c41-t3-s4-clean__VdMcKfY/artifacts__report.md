# Candidate-panel study decision

## Executive conclusion
The plate can support the protocol's association analysis. All 240 participants (120 affected and 120 unaffected) pass participant call-rate QC; 0 fail, for a failure fraction of 0. No re-genotyping trigger is reached. After variant QC, 140 of 150 variants remain and 10 are excluded. The cohort shows no detected ancestry separation on the leading genotype axes, so affected and unaffected participants can be compared under this protocol. This is not proof that subtle ancestry confounding is absent.

## Quality and retained cohort
All participants in the steward's participant manifest are retained; `sample_qc.csv` is the explicit participant retention register. Variant exclusions are rs040038, rs040054, rs040057, rs040072, rs040104, rs040106, rs040110, rs040112, rs040113, rs040125. All other variants in the supplied manifest are retained; `variant_qc.csv` gives the complete manifest, call rates, minor-allele frequencies, exact control Hardy–Weinberg probabilities, and decisions.

The excluded variants comprise 5 call-rate failures, 3 minor-allele-frequency failures and 2 control Hardy–Weinberg failures. These are observed QC defects, not evidence of a particular laboratory cause. Variant QC used retained participants and an exact two-sided Hardy–Weinberg test restricted to unaffected participants. No genotypes were repaired. Filtering is the only change to the analysis panel.

## Comparability
PCA used retained variants, mean imputation for missing calls and allele-frequency standardization. The leading axis explains 0.02098565 of standardized variation; its affected-versus-unaffected Welch comparison gives p = 0.89904971. Leading-axis ranges overlap, and the other leading axes show no phenotype separation. An unadjusted additive trend test was therefore used, rather than claiming a need for ancestry adjustment unsupported by these diagnostics. A candidate-region panel has limited ability to establish ancestry independently; broader ancestry markers and recruitment information would strengthen this conclusion.

## Association results
Variant-specific complete-case Cochran–Armitage tests were compared with the Bonferroni threshold 0.000357142857143. There are 0 significant variants. Genomic inflation lambda is 0.89037629. `association.csv` contains all tested variants, sample counts, statistics and probabilities.


No variant meets the panel-wide association criterion. This does not establish absence of genetic effects; power for small effects has not been quantified. No additional validation or intervention outcome was measured. No requested batch was denied, and no unavailable result has been substituted with an estimate.

## Next steps and control plan
Investigators should inspect genotype clusters and investigate the QC failures before considering rescue of excluded variants. Before expanding the study, plan power against clinically meaningful effects and obtain an independent, ancestry-characterized cohort. Any future positive findings should receive independent assay validation and replication before biological interpretation. Preserve the raw steward batches, scripts, retention registers and all test results as the frozen audit trail. Hold future releases to the same protocol rules, rerun cohort comparability checks after any sample or marker change, and recalculate multiplicity from the retained panel. Filtering achieved a protocol-eligible analysis set; it has not demonstrated a laboratory process improvement or external replication.
