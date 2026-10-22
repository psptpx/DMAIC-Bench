# Study status for the principal investigator

## Executive conclusion
The plate passes the protocol's participant-quality gate, but the discovery cohort cannot currently carry a disease-specific association conclusion. A strong genetic axis completely separates affected from unaffected participants. This is not evidence that every differentiating variant causes disease. No variant is nominated for reporting, and the released replication batch has no nominated discovery hits. This is an inconclusive, structurally confounded study—not a negative association result.

## Quality and retained material
Participant call rate was calculated across the full panel, with retention at call rate ≥ 0.95. There were 2 failures, a failure fraction of 0.00833333, below the plate re-genotyping threshold of 0.1. After exclusion, 238 participants remain: 119 affected and 119 unaffected. Whole-plate re-genotyping is not triggered.

Excluded participants: P039, P197. Every other discovery participant is retained; `participant_qc.csv` gives the complete identifier-level retention ledger and call rates.

Variant QC was computed after participant filtering: call rate ≥ 0.95, minor-allele frequency ≥ 0.01, and exact two-sided Hardy–Weinberg p ≥ 0.000001 in unaffected participants. There were 12 excluded and 138 retained variants. Failures were attributable to call rate for 5 variants, minor-allele frequency for 4, and control Hardy–Weinberg equilibrium for 3. These checks identify assay/missingness, rarity, and genotype-distribution concerns; they do not establish their laboratory causes.

Excluded variants: rs010047, rs010057, rs010063, rs010072, rs010088, rs010092, rs010101, rs010118, rs010128, rs010133, rs010141, rs010149. All other panel variants are retained. `variant_qc.csv` is the complete identifier-level ledger with measured metrics. Filtering, not alteration of genotype calls, is the change made here.

## Comparability and association decision
PCA used retained variants, replacing missing dosages with variant means and scaling by allele-frequency variance. Welch comparisons of the inspected axes used a corrected threshold of 0.005. The leading axis has group-comparison p = 3.65407e-129. Affected scores range from -5.89921 to -1.48493; unaffected scores range from 0.304689 to 6.73762. The gap is 1.78962, with no overlap.

Thus equal group sizes do not imply comparability. The structure could reflect ancestry, recruitment, or a technical artifact aligned with phenotype; ancestry and recruitment metadata were not supplied and the study-fact query returned no matching facts. We cannot distinguish those causes from these calls alone. Candidate-region PCA also has limited ancestry resolution.

An unadjusted trend scan would conflate this structure with affection status. A PC-adjusted logistic model would encounter complete outcome separation and lack common support; numerical regularization cannot create the missing comparison. Neither scan nor effect estimates were performed, so association counts, genomic inflation, disease odds ratios, and association p-values are not claimed. For a valid future scan of the retained panel, the computed Bonferroni threshold is 0.000362319, using family alpha 0.05.

## Replication
The replication data were released, not denied. The supplied candidate list contains 0 variants; consequently 0 candidates were confirmed, as an empty-set accounting result, not as failed replication tests. The protocol requires replication p < 0.05 and concordant discovery direction. There is no valid discovery estimate to test under that rule, and no replication association tests were run. The independent cohort cannot retrospectively repair the discovery cohort's lack of comparability. Do not promote a new scan of that cohort as independent confirmation.

## Actions and control plan
Preserve the raw batches, code, QC ledgers, and trace. Investigate recruitment ancestry and processing records, verify phenotype and specimen labels, and inspect genotype clusters for excluded variants. Obtain ancestry-informative genome-wide data and relevant technical covariates. Recruit or select ancestry-matched affected and unaffected participants with overlap within processing strata; balance and randomize future laboratory processing.

Re-run the frozen QC protocol and verify genetic overlap before testing variants. Only then perform a prespecified appropriately adjusted association analysis and nominate candidates with allele coding and direction fixed before independent replication. Hold reporting until that chain is complete. QC filtering improved the usable dataset, but no recruitment or laboratory corrective intervention has yet been implemented or shown to restore comparability. Maintain release gates for quality, overlap, multiplicity, and replication to prevent an apparently significant but confounded claim.
