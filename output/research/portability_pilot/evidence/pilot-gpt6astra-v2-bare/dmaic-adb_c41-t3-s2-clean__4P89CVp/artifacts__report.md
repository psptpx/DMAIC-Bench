# Investigator report

## Decision
**rs020008 has independent replication support; rs020065 remains an unreplicated discovery finding.** Reporting should remain conditional on allele-harmonization and ancestry/technical review.

The discovery plate is usable after protocol filtering, but affected and unaffected participants are not directly exchangeable on genotype background. Use the ancestry-proxy-adjusted scan rather than unadjusted associations. Replication findings below are evidence for association, not causality or clinical utility.

## Measurement and retention
The discovery matrix contains 240 participants and 150 variants. At the protocol call-rate minimum of 0.95, 2 participants fail (fraction 0.00833333), below the plate re-genotyping trigger of 0.1. Retain 238 participants: 118 affected and 120 unaffected. Exclude P017 and P111; all other supplied participant IDs are retained. Full participant-level results are in `participants_qc.csv`.

After participant removal, require variant call rate at least 0.95, minor-allele frequency at least 0.01, and exact control Hardy–Weinberg p at least 1e-06. There are 5 call-rate failures, 4 frequency failures and 2 HWE failures; 11 variants fail overall and 139 remain. Exclude rs020001, rs020016, rs020037, rs020045, rs020054, rs020072, rs020084, rs020085, rs020114, rs020117 and rs020142. All other supplied variants are retained. `variants_qc.csv` records exact membership and diagnostics. These are computational exclusions, not a physical re-genotyping intervention.

## Comparability and discovery
PCA used mean-imputed, allele-variance-standardized retained genotypes. Screening 10 leading axes at p < 0.005 detects affection separation on the leading axis (p = 4.19527e-18). This suggests population structure, although this candidate-region panel cannot distinguish ancestry from regional signal or unmeasured technical effects. No collection-batch metadata were supplied, so technical confounding is not ruled out.

The additive logistic scan conditions on the leading PC and uses complete calls at each variant. Likelihood-ratio p-values are compared against 0.00035971223, obtained from alpha 0.05 over 139 retained variants. There are 2 significant variants; adjusted genomic inflation is 0.987025. This is compatible with acceptable calibration, not proof of absence of confounding. PCs estimated from the tested panel can absorb true signal; wider ancestry markers are preferable.

| Variant | Adjusted discovery p | Dosage odds ratio | Wald interval |
|---|---:|---:|---:|
| rs020008 | 2.09591e-05 | 2.62631 | 1.65283–4.17316 |
| rs020065 | 0.000192765 | 0.40406 | 0.24425–0.66844 |

## Independent replication
The steward nominated rs020008; rs020065 is an additional candidate arising from our adjusted scan and is explicitly treated as an additional follow-up, not a pre-nominated hit. Replication uses an additive logistic likelihood-ratio test and checks candidate call rate, frequency and control HWE after sample filtering.

Replication retains 120 participants (60 affected, 60 unaffected), with 0 sample exclusions.

- **rs020008**: p = 0.000315699; dosage odds ratio 2.73000, Wald interval 1.52775–4.87835. Protocol replication (QC passed, p < 0.05, same coded direction): **yes**.
- **rs020065**: p = 0.349862; dosage odds ratio 0.77052, Wald interval 0.44510–1.33385. Protocol replication (QC passed, p < 0.05, same coded direction): **no**.

The tests compare the supplied dosage coding. The nominated discovery-direction mapping is consistent with our positive discovery effect. The study lead could not provide allele-harmonization facts; verify reference/effect alleles and strand before formal biological reporting. Replication ancestry and technical-batch comparability have not been comprehensively established; the independent tests are not a substitute for those checks.

## Action and sustained control
Report only supported signals as provisional replicated associations, with the adjusted discovery analysis and independent follow-up clearly distinguished. Do not claim unsupported additional hits or infer that non-significant variants have no effect. Preserve the frozen protocol, source batches, filtering tables, scripts and full association results. Have the data steward verify allele orientation, plate assignments, relatedness and broader ancestry markers; rerun sensitivity analyses with independent ancestry estimates before publication. A matched, larger independent cohort can resolve any unsupported or unstable candidates. For future releases, apply the same participant and variant gates before association testing, audit case/control balance and genotype missingness by batch, and require independent direction-consistent confirmation. No laboratory process change or clinical benefit has yet been demonstrated.
