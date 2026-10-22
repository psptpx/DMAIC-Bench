# Investigator report: candidate-region association study

## Decision
The plate is usable after protocol exclusions, but this study does **not establish a reportable variant association**. There are no corrected-significant ancestry-adjusted discovery candidates and therefore no independently confirmed findings. This is not proof that the region has no effects.

## Quality and retained analysis set
Participant QC used call rate at least 0.95. Of 240 participants, 3 failed (0.0125 of the plate), below the re-genotyping trigger of 0.1. Retain 237 participants: 120 affected and 117 unaffected. Exclude P127, P142, P195; every other supplied participant is retained. No plate-wide re-genotyping was indicated or performed.

After participant removal, variants required call rate at least 0.95, minor-allele frequency at least 0.01, and exact control-only Hardy–Weinberg p at least 1e-06. Of 150 variants, 11 failed and 139 remain. Failures comprised 5 call-rate failures, 4 low-frequency failures and 2 Hardy–Weinberg failures. Exclude rs050014, rs050017, rs050019, rs050052, rs050071, rs050082, rs050091, rs050092, rs050096, rs050108, rs050121; all other supplied variants are retained. The complete inclusion flags, call rates, frequencies and HWE results are in `participants_qc.csv` and `variants_qc.csv`.

## Are affected and unaffected participants comparable?
Not without accounting for genetic structure. PCA used allele-frequency-standardized retained calls with mean imputation only for PCA. The leading axis strongly separates phenotype groups (Welch p = 4.31637e-16). We tested 10 leading axes with comparison threshold 0.005; only the leading axis crossed that threshold. This is evidence of phenotype-associated genetic structure, not a definitive diagnosis of ancestry or laboratory confounding. No demographic, ancestry-reference, relatedness or batch covariates were supplied, so those explanations cannot be distinguished here.

## Discovery: what changed and what it achieved
An available-case additive Cochran–Armitage trend scan produced 27 nominal discovery hits after panel correction, but genomic inflation was 2.63376. These are diagnostic, unadjusted findings, not claims for reporting. The panel-wide Bonferroni threshold was 0.00035971223, obtained by dividing 0.05 by the retained variant count.

We changed the analysis, not the biological material: additive logistic models included the leading genetic component as a covariate. Adjusted inflation was 1.18513, and 0 variants met the corrected threshold. The smallest adjusted p was 0.0055800102. Thus the broad unadjusted signal disappears after accounting for the major structure axis. `association.csv` and `adjusted_association.csv` preserve the full scans and adjusted effect estimates. Small-panel inflation estimates are diagnostic rather than proof of calibration; panel-derived components can also absorb genuine regional signal. These results need an ancestry-informed sensitivity analysis before a definitive biological interpretation.

## Independent replication
The steward released replication calls but nominated 0 hits. Our independently computed adjusted discovery set also has 0 candidates. The number confirmed is therefore 0, by empty-set accounting, not by observing replication failures. No candidate-specific replication test or replication effect estimate was warranted or computed. Do not rescue the confounded unadjusted hits by scanning the independent cohort post hoc. The replication cohort remains available for prospectively nominated, valid discovery findings.

## Actions and how to hold the improvement
Do not announce a susceptibility variant or use these results clinically. Preserve the protocol, raw batches, inclusion manifests, scripts, and full scans with this report. Review recruitment ancestry and laboratory allocation; obtain genome-wide ancestry and relatedness markers plus relevant clinical and batch covariates. Confirm case–control overlap within ancestry strata and repeat appropriately adjusted or stratified analyses. The present data support a QC-qualified, structure-sensitive null finding, not causal attribution or a claim of equivalence.

For future runs, freeze QC and multiplicity rules before inspecting outcomes, monitor sample missingness and control HWE, audit group balance across plates, and independently reproduce the analysis before nomination. Require prespecified same-direction replication before reporting a variant. No wet-lab or recruitment intervention was executed here; the demonstrated improvement is removal of misleading unadjusted evidence through statistical adjustment.

## Audit and limits
All displayed quantities are recorded in `trace.json`; record identifiers identify the actual supplied samples and variants. Analyses were local and reproducible using `analyze.py` and `adjusted.py`. No data request was denied; an initial routing lock was resolved by obtaining the earlier batches. Missing external covariates were not invented. A power calculation, causal mechanism, batch-effect estimate, and candidate-specific replication evidence cannot be supplied from the analyses performed.
