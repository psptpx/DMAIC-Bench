# Candidate-region study: principal investigator report

## Decision
The plate is usable after protocol QC. The discovery scan identifies 1 association, rs000008. Independent replication confirms 1 of 1 nominated candidates. This supports reporting a replicated panel association, not a causal variant or a clinical predictor.

## Quality and retained analysis set
Discovery contained 240 participants, evenly divided into 120 affected and 120 unaffected, across 150 variants. Participant call rate had to be at least 0.95. There were 3 failures (fraction 0.0125), below the plate re-genotyping trigger of 0.1. The retained cohort comprises 237 participants: 119 affected and 118 unaffected.

Excluded participants: P053, P129, P160. All other supplied participant identifiers are retained. The complete participant-level calls and decisions are in `sample_qc.csv`.

After participant filtering, variants required call rate at least 0.95, minor-allele frequency at least 0.01, and exact conditional Hardy–Weinberg p at least 1e-6 in unaffected participants. There were 6 call-rate failures, 4 frequency failures and 3 Hardy–Weinberg failures; the union removed 13 variants and retained 137.

Excluded variants: rs000003, rs000025, rs000061, rs000079, rs000086, rs000091, rs000107, rs000108, rs000122, rs000130, rs000138, rs000149, rs000150. Every other supplied variant is retained. `variant_qc.csv` is the complete variant-level retention manifest, including each criterion's measured value. These filters—not any laboratory intervention—are the changes made. They removed unreliable or insufficiently informative calls; no cause of the laboratory failures can be established from the supplied calls alone.

## Can the groups be compared?
Allele-frequency-standardized PCA used mean imputation only for structure screening, not for association. The leading component comparison gave p=0.939779. No screened component passed the multiplicity-adjusted screening cutoff of 0.005. Thus the data support proceeding with an unadjusted additive trend scan. Genomic inflation was 1.11594; it is modest, not proof that confounding is absent. A candidate-region panel has limited ancestry resolution. Relatedness, detailed ancestry and processing-batch comparability were not established by these data and remain limitations.

## Discovery and replication
The additive Cochran–Armitage score scan used nonmissing calls at each retained variant. The family-wise alpha was 0.05 and the Bonferroni cutoff was 0.000364963504. For rs000008, discovery p=5.25354032e-11. The additive logistic per-coded-allele odds ratio was 3.78652, with Wald interval 2.47028 to 5.80408. These estimates are not adjusted for unmeasured covariates and may be affected by discovery selection.

Replication retained 118 participants (59 affected, 59 unaffected), with 2 participant call-rate failures. Candidate call rate was 0.991525 and minor-allele frequency was 0.461538. The independent trend-test p was 4.03131836e-05, against the prespecified replication threshold of 0.05. Its odds ratio was 3.09723, in the same increasing-risk coded-allele direction. No pooled significance substitution was used. Direction assumes the common supplied genotype coding; molecular allele labels were not supplied.

## Next actions and control plan
Report the replicated association with its QC manifest, correction procedure and limitations. Do not call the remaining panel variants definitively null: lack of significance is not equivalence. Confirm molecular allele alignment, inspect genotype clusters for the nominated marker, document ancestry and processing metadata, and pursue a larger well-characterized cohort and functional follow-up before causal or clinical claims.

Freeze the supplied batches, scripts, retention manifests and trace with the analysis release. Hold future data to the same prespecified call-rate, frequency, equilibrium and replication rules; monitor failure fractions by processing batch and trigger laboratory review if the plate threshold is breached. No re-genotyping was performed or shown necessary under this protocol. No batch was denied by the steward; unsupported mechanistic and clinical conclusions remain outside this analysis.
