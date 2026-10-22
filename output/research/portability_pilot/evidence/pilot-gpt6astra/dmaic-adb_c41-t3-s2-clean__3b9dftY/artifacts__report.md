# Study disposition

## Executive conclusion
The plate is usable under the protocol. After quality filtering, affected and unaffected participants show ancestry-related structure but are not separated into nonoverlapping cohorts. An ancestry-adjusted comparison is therefore appropriate. The adjusted panel analysis declares 1 associated variant; this is a study association, not proof of causality or a clinical prediction tool.

## Plate and retention
Computed participant call rates across 150 variants for 240 participants. At the retention cutoff of 0.95, 3 participants fail (fraction 0.0125). This is below the plate re-genotyping trigger of more than 0.1; mandatory plate re-genotyping is not indicated.

Excluded participants: P031, P153, P236. All other supplied participants are retained: 237 total, including 119 affected and 118 unaffected. The complete participant manifest and computed call rates are in `sample_qc.csv`.

Variant QC was computed after removing failed participants. Requirements were call rate at least 0.95, pooled minor-allele frequency at least 0.01, and exact Hardy–Weinberg probability among retained unaffected participants at least 1e-06. There were 5 call-rate failures, 4 frequency failures, and 2 Hardy–Weinberg failures. The union excludes 11 variants and retains 139.

Excluded variants: rs020016, rs020022, rs020023, rs020042, rs020048, rs020074, rs020096, rs020102, rs020107, rs020115, rs020143. All other supplied variants are retained. `variant_qc.csv` gives every variant's decision and supporting measurements. Low call rate, rare alleles, and control genotype disequilibrium explain exclusions; their laboratory or biological root causes have not been established.

## Comparability before testing
Principal components were computed from retained genotypes, replacing missing calls by variant means and standardizing by allele-frequency variance. The leading component explains a variance fraction of 0.093524. Its case-control Welch-test probability is 1.80088e-14: ancestry structure cannot be ignored. Case scores range from -5.3920 to 4.8647, and control scores from -6.8671 to 5.1923. The substantial overlap supports adjustment rather than declaring the cohort incomparable. A mean difference alone is not complete separation.

The separate ancestry-record request was unroutable, not a denial of a known batch. The structure assessment uses computed panel PCs, not external ancestry assignments. Candidate-panel PCs provide limited ancestry resolution and can incorporate local association signals; independent genome-wide ancestry markers would strengthen this assessment.

## Association analysis
Fit additive logistic models with affection status as outcome, genotype dosage as predictor, and the leading 2 principal components as covariates. Missing genotypes were excluded separately for each variant; PCA imputation was not used as observed genotype data in the association models. Tests were two-sided Wald tests. The panel-wise significance cutoff is 0.05 / 139 = 0.00035971223. Genomic inflation, calculated as median Wald chi-square divided by its null median, is 0.934817; it shows no residual inflation in this diagnostic, but does not prove absence of confounding.

| Variant | Called participants | Dosage odds ratio | Adjusted p-value |
|---|---:|---:|---:|
| rs020008 | 230 | 2.447535 | 6.3625996e-05 |

No other retained variant meets the corrected threshold. Full effect estimates and probabilities are in `association.csv`. Dosage effects refer to the coded allele; nucleotide identity was not supplied. Lack of corrected significance is not proof that other variants have no effect.

## What changed and next steps
The analysis removed protocol-failing records and replaced a potentially confounded crude comparison with ancestry-adjusted testing. This achieved an analyzable cohort and a corrected association result; no laboratory process change, re-genotyping, replication, or clinical benefit has been demonstrated. A before-versus-after association improvement was not measured because unadjusted testing was not used as the primary analysis.

Investigators should validate the associated call technically, replicate the signal in an independent ancestry-balanced cohort, obtain independent ancestry markers, and assess sensitivity to ancestry covariate selection and relatedness. Review missing-call patterns and control disequilibrium with the laboratory before changing assays. Do not infer a causal gene or clinical intervention from this candidate-panel result alone.

Hold the analysis by freezing the raw batches, retention manifests, scripts, covariate procedure and multiplicity rule before replication. Apply the same plate acceptance gate to subsequent batches, require documented QC review and ancestry overlap before testing, and investigate changes in missingness or inflation. `trace.json` records computations; the local scripts reproduce the numerical work. No prospective validation data were analyzed.
