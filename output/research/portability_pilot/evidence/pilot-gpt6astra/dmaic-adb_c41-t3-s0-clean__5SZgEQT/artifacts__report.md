# Candidate-panel study: investigator report

## Decision
The plate is usable after protocol filtering. The retained affected and unaffected participants overlap on the leading genetic ancestry axis, so the cohort supports a within-panel association analysis. There is **1 Bonferroni-significant variant**, also significant in the ancestry-covariate sensitivity analysis. This is an association finding, not evidence of causality or clinical utility.

## Quality and retained data
Of 240 participants, 5 failed the call-rate requirement of 0.95. The observed failure fraction was 0.02083333, below the plate re-genotyping limit of 0.1. No plate re-genotyping was required or performed. Filtering retained 235 participants: 117 affected and 118 unaffected.

Excluded participants: P011, P059, P069, P224, P225. All other supplied participant identifiers are retained; `sample_qc.csv` gives the complete explicit membership and call-rate audit.

Variant QC was applied after participant filtering. Call rate had to reach 0.95, minor-allele frequency 0.01, and control-only Hardy–Weinberg exact-test p-value 1e-06. The HWE test sums conditional genotype probabilities no greater than the observed probability. Allele frequency uses observed calls from the retained cohort.

Excluded 12 variants and retained 138. Failures by rule were 5 for call rate, 4 for frequency and 3 for HWE. Excluded identifiers: rs000031, rs000049, rs000060, rs000078, rs000086, rs000093, rs000114, rs000126, rs000135, rs000138, rs000142, rs000148. Every other supplied variant is retained; `variant_qc.csv` records exact membership and each metric. These failures identify missingness, rare alleles and control genotype disequilibrium, not a demonstrated laboratory root cause.

## Cohort comparability
PCA used retained calls, allele-frequency standardization, and mean imputation solely for PCA. The leading-axis Welch comparison gave p = 0.260362. Affected scores ranged from -3.58153 to 3.94601; unaffected scores ranged from -4.02679 to 4.24263. These overlapping ranges do not support separate-ancestry confounding on the leading axis.

The fourth axis did differ by phenotype (p = 0.00300195). Candidate-panel axes can reflect local association as well as ancestry; therefore an additive logistic sensitivity analysis included the first 5 axes. Independent genome-wide ancestry markers would strengthen this check. The panel alone cannot establish absence of all subtle structure or relatedness.

## Association
Primary tests were additive genotype score/trend tests using observed calls separately per variant. The Bonferroni threshold was 0.0003623188406. Genomic inflation, the median test statistic divided by the null chi-square median, was 0.826762; there is no evidence of global inflation by this diagnostic.

| Variant | Primary p | PC-adjusted sensitivity p |
|---|---:|---:|
| rs000008 | 7.4733891e-07 | 6.4035656e-06 |

The adjusted analysis also yielded 1 significant variant, with genomic inflation 0.802588. No other retained variant met the corrected threshold. Non-significance is not proof of no effect. Complete tests are in `association.csv`.

## Next action and sustained controls
Filtering, rather than changing laboratory data, removed low-quality participants and failing variants and produced the analyzable cohort described above. The sensitivity adjustment preserved the discovery. Validate the lead variant's calls with an independent assay, review raw clusters and missingness by affection status, and replicate in an independent ancestry-matched cohort before biological or clinical claims. Obtain broader ancestry markers and relatedness information for that replication; use balanced case/control laboratory allocation and blinded processing.

Freeze the protocol, raw released batches, scripts, exclusion lists and analysis outputs. On future plates, apply the same participant gate before variant filtering, assess ancestry overlap before testing, and preserve the multiplicity correction. No replication or corrective laboratory intervention was performed here, so durability of the association has not been demonstrated. The steward released the protocol and genotype data; no request was denied and no outside study-lead help was used.

All numerical results above are recorded in `trace.json`; identifiers are audited by computed retention flags and variant-specific test outputs. Reproducible scripts are `analyze.py`, `structure.py`, and `association.py`.
