# Candidate-region study: decision for the principal investigator

## Executive conclusion
The discovery plate is usable under the protocol. After quality filtering and ancestry adjustment, **rs020008 is the sole discovery association and is supported by independent replication**. It can be reported as a replicated panel association, not as proof of causation or a clinically validated predictor.

## Quality and retained cohort
The sample call-rate requirement was 0.95. There were 2 failures (fraction 0.00833333), below the plate re-genotyping trigger of 0.1. Excluded participants: P017, P111. All other supplied discovery participants are retained: 238, comprising 118 affected and 120 unaffected participants. No re-genotyping was performed or required by this gate.

Variant filtering was applied after removing failed participants. Requirements were call rate at least 0.95, minor-allele frequency at least 0.01, and control-only exact Hardy–Weinberg p-value at least 1e-06. We removed 11 variants and retained 139. The failed-rule counts were 5 for call rate, 4 for frequency, and 2 for Hardy–Weinberg equilibrium. Excluded variants: rs020001, rs020016, rs020037, rs020045, rs020054, rs020072, rs020084, rs020085, rs020114, rs020117, rs020142. All other supplied variants are retained. The full identity-level decisions and computed metrics are in `sample_qc.csv` and `variant_qc.csv`.

## Can affected and unaffected participants be compared?
Yes, but not without adjustment. PCA used retained variants, allele-frequency standardized dosages, and mean imputation solely for PCA. The leading axis explains fraction 0.101701 of standardized genotype variation and differs by affection status (Welch p = 4.19527e-18). Nevertheless, the group score ranges overlap by 10.671221; the other inspected leading axes also overlap. The next axis has phenotype-comparison p = 0.376887. This is overlapping ancestry structure, not disjoint cohorts. Range overlap is an operational diagnostic, not proof that all ancestry confounding has been eliminated.

We therefore used additive logistic regression with 2 leading PCs as covariates, protecting against the dominant structure while retaining an additional leading axis. Missing genotypes were excluded separately for each association test. The panel is limited for ancestry inference; genome-wide ancestry markers, relatedness information and technical-batch metadata were not supplied, so those potential sources of residual confounding were not assessed.

## Discovery and independent support
The Bonferroni threshold was 0.00035971223. The adjusted scan produced 1 significant variant; genomic inflation, calculated as the median Wald chi-square divided by its null median, was 0.854139. No unadjusted discovery scan was used to select candidates.

| Variant | Discovery dosage odds ratio | Discovery Wald p | Replication dosage odds ratio | Replication Wald p |
|---|---:|---:|---:|---:|
| rs020008 | 2.578933 | 6.7046696e-05 | 2.638422 | 0.0011773988 |

Replication sample QC retained 120 participants with 0 failures; variant QC retained 141 and excluded 9. The discovery hit passed replication variant QC. Replication leading axes overlapped, with phenotype-comparison p-values 0.188036 and 0.705877. The replication model used the same ancestry-adjusted additive approach with independently computed cohort PCs.

Of 1 selected discovery candidate, 1 replicated: the replication p-value is below 0.05 and the dosage effect has the same positive direction. Odds ratios refer to the increment in the supplied coded dosage; a named nucleotide effect allele was not provided. All per-variant discovery estimates are archived in `association.csv` and the trace.

## What changed, what it achieved, and how to hold the result
The analysis excluded low-quality participants and variants, then changed the comparison from a potentially ancestry-confounded raw comparison to an ancestry-adjusted model. The resulting scan has no aggregate inflation signal and its selected association is independently supported. This is an analytical correction, not evidence that a laboratory process intervention occurred; no before/after intervention effect was estimated.

Proceed with reporting the replicated association, including cohort exclusions, exact QC methods, covariate specification, multiplicity correction, and replication criteria. Before manuscript release, verify allele alignment against assay documentation, inspect genotype clusters and missingness by phenotype, and obtain broader ancestry, relatedness and batch information. Seek external validation and functional follow-up before causal or clinical claims. Non-significant variants are not proven to have no effect.

Hold the result with versioned steward batches, reproducible scripts, fixed QC manifests, and an analysis freeze that prevents changing the candidate set after replication. Apply the same plate gate and ancestry checks to future batches; stop if comparability fails, and withhold any future discovery hit that fails independent replication. No requested data batch was denied. The report's quantitative findings are recorded in `trace.json`; unmeasured checks above are recommendations, not completed analyses.
