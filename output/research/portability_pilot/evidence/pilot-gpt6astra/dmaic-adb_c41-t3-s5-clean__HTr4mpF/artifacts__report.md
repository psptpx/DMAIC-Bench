# Study conclusion

The plate is usable after protocol QC, but affection groups differ in ancestry composition. Their ancestry distributions overlap, allowing an ancestry-adjusted comparison; a naive case–control comparison would be confounded. Findings remain exploratory panel associations, not proof of causation.

## Quality and retained cohort

Of 240 participants, 2 failed the call-rate requirement of 0.95: a failure fraction of 0.00833333, below the plate re-genotyping trigger of 0.1. The retained cohort contains 238 participants: 118 affected and 120 unaffected. No plate replacement was required.

Excluded participants: P011, P120. All other participants in the released batch are retained; the full membership and call rates are recorded in `sample_qc.csv`.

Of 150 variants, 12 failed and 138 were retained. Failures comprised 5 for call rate, 4 for minor-allele frequency and 3 for unaffected-participant Hardy–Weinberg equilibrium. Required minima were 0.95, 0.01 and 0.000001 respectively. HWE was computed by the conditional exact, probability-ordered two-sided test using called control genotypes. Variant QC was computed after participant removal.

Excluded variants: rs050014, rs050017, rs050019, rs050040, rs050052, rs050071, rs050082, rs050091, rs050092, rs050096, rs050108, rs050121. All remaining variants are retained. `variant_qc.csv` identifies each retained and excluded variant with its computed metrics.

## Cohort comparability

PCA used retained variants, mean-imputed missing calls, and allele-frequency standardized dosages. The leading axis explained 0.09022534 of variance; its affection-group Welch comparison gave p = 3.408006e-15. Affected scores spanned -4.871782 to 5.966279, while unaffected scores spanned -5.107065 to 5.367211. This is structure with overlap, not separate non-comparable ancestry cohorts. The comparison therefore proceeds with the leading ancestry axis included as a covariate. This panel-based assessment is not a substitute for dense ancestry markers; residual structure remains a limitation.

## Association

Tests used additive logistic regression, adjusting for the leading ancestry axis, with a likelihood-ratio comparison against an ancestry-only model. Missing genotypes were excluded separately for each test. The Bonferroni threshold is 0.05 / 138 = 0.0003623188406.

There were 0 significant variants. Genomic inflation (median likelihood-ratio statistic divided by its null median) was 1.15122.


Full test results are in `association.csv`. The odds ratios refer to the encoded counted allele, not a named risk allele. Inflation is descriptive on this small, potentially correlated candidate panel and should not be interpreted as definitive calibration evidence.

## Actions and control plan

The change made was to remove protocol-failing participants and variants and account for the observed ancestry imbalance rather than test raw group differences. This enabled a QC-qualified, ancestry-adjusted analysis; no laboratory intervention or replication has been performed. The biological or operational source of the ancestry imbalance cannot be identified from genotype calls alone.

No variant meets the protocol association threshold. The smallest adjusted p-value was 0.00120247, above the Bonferroni threshold. If investigators pursue suggestive signals, treat them as hypotheses for independent, ancestry-balanced replication, not discoveries; confirm genotypes and allele annotations before biological interpretation. Obtain dense ancestry markers and evaluate additional ancestry axes, relatedness, batch effects and sensitivity to local linkage before making a robust causal claim. Do not treat nonsignificance as proof of no effect.

Freeze the retained membership, QC rules, scripts and result tables as the analysis record. Apply the same pre-test quality and ancestry gates to future releases; re-genotype plates that breach the failure rule, and halt comparisons without ancestry overlap. The investigator should review replication and sensitivity evidence before translating results into clinical or mechanistic conclusions.
