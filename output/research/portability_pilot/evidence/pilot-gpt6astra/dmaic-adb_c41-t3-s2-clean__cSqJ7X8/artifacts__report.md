# Study decision for the principal investigator

## Executive conclusion
The plate passes the protocol's participant-quality gate and supports an ancestry-adjusted association analysis. The affected and unaffected groups exhibit ancestry structure, but they overlap rather than being separated. After quality filtering and adjustment, **1 variant is associated at the panel-wide threshold**. This is a candidate association, not proof of causality or clinical utility.

## Quality and retention
Call rates were computed from the full released genotype matrix, treating null calls as missing. Of 240 participants and 150 variants, 3 participants fail the minimum call rate of 0.95. The failure fraction is 0.0125, below the plate re-genotyping trigger of 0.1. Re-genotyping the whole plate is therefore not mandated.

Excluded participants: P031, P153, P236. All other released participants are retained: 237 in total, comprising 119 affected and 118 unaffected. The complete participant roster and individual call rates are in `participant_qc.csv`.

Variant QC was computed after participant exclusion. The requirements were call rate at least 0.95, minor-allele frequency at least 0.01, and control Hardy–Weinberg exact p-value at least 1e-06. The exact test used probability ordering conditional on the control allele count. Call rate and allele frequency used the retained cohort; HWE used only its unaffected participants.

There are 11 excluded variants and 139 retained variants. Failure counts by criterion are 5 for call rate, 4 for allele frequency, and 2 for control HWE. Excluded variants: rs020016, rs020022, rs020023, rs020042, rs020048, rs020074, rs020096, rs020102, rs020107, rs020115, rs020143. **All other released variants are retained.** `variant_qc.csv` provides the complete variant roster, metrics and retention decisions.

## Cohort comparability
PCA used retained variants, mean imputation for missing calls, and allele-frequency standardization. The leading axis explains 0.093524 of standardized genotype variation; its Welch case-control comparison has p = 1.80088e-14. The affected and unaffected score ranges overlap. Thus an unadjusted case-control comparison would ignore ancestry imbalance, but the protocol's absolute stop for separated ancestries is not triggered. We used the leading 2 axes as covariates. Individual scores are saved in `ancestry_pca.csv`.

The ancestry interpretation is inferred from this candidate panel, not independently verified genome-wide ancestry. Overlapping ranges and adjustment are not proof of complete control of confounding. Broader ancestry markers and independent replication would strengthen the conclusion.

## Association results
Each retained variant was tested by additive logistic regression of affection status on genotype dosage, with an intercept and the ancestry covariates. Missing calls were excluded separately for each variant's regression, rather than imputed for association. Significance used the genotype Wald test and Bonferroni threshold 0.00035971223, computed from family-wise alpha 0.05 over the retained panel. Genomic inflation, calculated as the median genotype Wald statistic divided by its null median, is 0.934817; this is descriptive rather than a guarantee of calibration.

| Variant | Called participants | Odds ratio per coded allele | Raw p-value |
|---|---:|---:|---:|
| rs020008 | 230 | 2.447535 | 6.3625996e-05 |

No other retained variant meets the corrected threshold. The complete test results are in `association_results.csv`. The direction refers to the supplied genotype coding; nucleotide allele labels were not supplied. Non-significance does not establish absence of an effect.

## What changed, what it achieved, and next steps
We excluded low-call participants and variants that failed protocol QC, then changed the inferential comparison from an unadjusted contrast to an ancestry-adjusted model because ancestry was imbalanced. These changes produced the retained analysis set and the corrected discovery above. We did not alter laboratory calls, re-genotype the plate, or demonstrate that the association disappears or emerges relative to an unadjusted analysis; no such comparison was run.

Investigators should prioritize the significant variant for independent technical confirmation, obtain allele annotations, and replicate in an ancestry-balanced independent cohort. Confirm ancestry using a broader marker set and assess relatedness and residual confounding before biological interpretation. Do not use this result for clinical decisions without external validation.

Hold the analysis by freezing the protocol, input batches, QC rosters, scripts, ancestry scores and complete results together. Apply the same quality gates to future plates, investigate recurrent call-rate or HWE failures with the laboratory, and recheck ancestry overlap before future association testing. Do not relax thresholds in response to this result.

## Audit and limits
`trace.json` contains computed scalar outputs in analysis order; `analyze.py` and `associate.py` reproduce the calculations from the released batches. No steward denial interrupted the analysis. No independent replication, technical validation or genome-wide ancestry assessment was performed, so those claims remain unestablished. The reported conclusion is limited to this retained cohort and candidate panel.
