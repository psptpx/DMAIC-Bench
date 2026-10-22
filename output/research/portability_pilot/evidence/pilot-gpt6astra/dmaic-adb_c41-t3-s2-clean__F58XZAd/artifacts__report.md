# Investigator report

## Bottom line
The plate is technically usable after QC. The cohort has overlapping ancestry structure, so affected and unaffected participants can be compared only with structure adjustment. The adjusted panel analysis found **1 significant variants**; these are candidate associations, not proof of causality or clinical utility.

## Quality and retained records
Of 240 participants, 3 failed the required call rate of 0.95. The failure fraction was 0.0125, below the plate re-genotyping trigger of 0.1. Retained: 237 participants, including 119 affected and 118 unaffected. Excluded participant identifiers: P031, P153, P236. All other supplied participants are retained; sample_qc.tsv is the complete auditable roster.

Variant QC was computed after participant exclusions. Of 150 variants, 11 failed and 139 remain. Failures by criterion: 5 for call rate, 4 for minor-allele frequency, and 2 for exact Hardy–Weinberg equilibrium in unaffected participants. Requirements were call rate at least 0.95, MAF at least 0.01, and control HWE p at least 1e-06. Excluded variant identifiers: rs020016, rs020022, rs020023, rs020042, rs020048, rs020074, rs020096, rs020102, rs020107, rs020115, rs020143. All other supplied variants are retained; variant_qc.tsv gives the full roster and metrics.

## Comparability
Allele-frequency standardized PCA used retained variants, with missing genotypes mean-imputed for PCA only. The leading axis explains 0.09352354 of genotype variance. Its affected/unaffected Welch-test p-value is 1.8008776e-14. The empirical group ranges overlap (overlap width 10.25671190); ancestry and affection are not completely separated. This supports an adjusted comparison, not a naive trend test. PCA on a candidate panel is an imperfect ancestry proxy and should be checked with genome-wide markers in follow-up. A request for separate ancestry records was unroutable, not a denial of genotype-derived assessment.

## Association
Additive logistic likelihood-ratio tests adjusted for the leading 5 genotype PCs, selected before variant testing. Association fits used observed calls only. Family-wise alpha 0.05 across 139 retained variants yields threshold 0.0003597122302. Genomic inflation lambda is 1.09213503; interpret it cautiously for a small candidate panel. Minimum adjusted p-value: 5.403095e-05.

- **rs020008**: p = 5.403095e-05; per coded-allele odds ratio = 2.62587146; observed participants = 230.

Full results are in association.tsv. Allele coding is dosage from the supplied records; biological risk-allele labels were not supplied. Absence of significance is not evidence of no effect.

## Action and control plan
The analysis changed the usable dataset by excluding protocol failures and changed inference by adjusting for ancestry. No laboratory intervention or replication was performed, so an improvement in laboratory performance cannot be claimed. Investigate low-call samples and failed assays, check sample identity and laboratory logs, and independently replicate candidate signals in ancestry-matched participants. Validate ancestry with broader markers, check relatedness and technical batch effects, and assess sensitivity to the chosen axes before publication. Maintain versioned QC rosters, frozen thresholds and scripts; require the same plate, variant and comparability gates on future releases. Do not use these results for clinical decisions without replication and biological validation.
