# Candidate-region study: investigator report

## Decision
The discovery plate is usable after QC. Ancestry structure requires adjustment, not abandonment: affected and unaffected distributions overlap. **Report rs020008 as a replicated panel association**, not as proof of causation. Do not report rs020065 as established: it failed independent replication. Reconsider the discovery scan and its model sensitivity before treating any additional finding as credible.

## Plate and retention
Of 240 discovery participants across 150 variants, 2 failed the participant call-rate rule, a fraction of 0.00833333. This is below the plate stop threshold 0.1; 238 participants remain. Call rate was calculated before variant filtering using a threshold of 0.95.

Excluded participants: P017, P111. All other participants in the released discovery batch are retained; `sample_qc.csv` is the complete identifier-level manifest.

Variant QC on retained participants removed 11 variants and retained 139. Failures comprised 5 call-rate failures, 4 minor-allele-frequency failures and 2 exact conditional Hardy–Weinberg failures in unaffected participants. Excluded variants: rs020001, rs020016, rs020037, rs020045, rs020054, rs020072, rs020084, rs020085, rs020114, rs020117, rs020142.

Retained variants: rs020002, rs020003, rs020004, rs020005, rs020006, rs020007, rs020008, rs020009, rs020010, rs020011, rs020012, rs020013, rs020014, rs020015, rs020017, rs020018, rs020019, rs020020, rs020021, rs020022, rs020023, rs020024, rs020025, rs020026, rs020027, rs020028, rs020029, rs020030, rs020031, rs020032, rs020033, rs020034, rs020035, rs020036, rs020038, rs020039, rs020040, rs020041, rs020042, rs020043, rs020044, rs020046, rs020047, rs020048, rs020049, rs020050, rs020051, rs020052, rs020053, rs020055, rs020056, rs020057, rs020058, rs020059, rs020060, rs020061, rs020062, rs020063, rs020064, rs020065, rs020066, rs020067, rs020068, rs020069, rs020070, rs020071, rs020073, rs020074, rs020075, rs020076, rs020077, rs020078, rs020079, rs020080, rs020081, rs020082, rs020083, rs020086, rs020087, rs020088, rs020089, rs020090, rs020091, rs020092, rs020093, rs020094, rs020095, rs020096, rs020097, rs020098, rs020099, rs020100, rs020101, rs020102, rs020103, rs020104, rs020105, rs020106, rs020107, rs020108, rs020109, rs020110, rs020111, rs020112, rs020113, rs020115, rs020116, rs020118, rs020119, rs020120, rs020121, rs020122, rs020123, rs020124, rs020125, rs020126, rs020127, rs020128, rs020129, rs020130, rs020131, rs020132, rs020133, rs020134, rs020135, rs020136, rs020137, rs020138, rs020139, rs020140, rs020141, rs020143, rs020144, rs020145, rs020146, rs020147, rs020148, rs020149, rs020150.

The protocol thresholds were applied inclusively. `variant_qc.csv` contains each variant's call rate, pooled minor-allele frequency, control HWE probability and retention decision. Filtering removes poor calls and unsuitable markers; it does not itself remove ancestry confounding.

## Cohort comparability and association
PCA used mean-imputed retained dosages centered and scaled by binomial allele variance. The leading axis explained 0.101701 of genotype variance and differed by affection status (Welch p = 4.19527e-18). Its affected range was -5.6954 to 5.7070, versus -4.9643 to 6.5690 in unaffected participants. These overlap substantially; a significant mean difference is not evidence of completely disjoint ancestry. Other inspected leading axes did not show comparable phenotype association. This supports a covariate-adjusted comparison, with caution that a candidate panel is an imperfect ancestry instrument.

Each retained variant was tested by additive logistic regression adjusted for the dominant ancestry axis, using a likelihood-ratio test against the ancestry-only model and excluding missing calls for that variant. The Bonferroni threshold was 0.00035971223. There were 2 discovery hits; genomic inflation, calculated from the median likelihood-ratio statistic, was 0.987025. This diagnostic on a selected panel is not a genome-wide calibration guarantee.

| Variant | Discovery dosage odds ratio | Discovery p | Replication dosage odds ratio | Replication p | Decision |
|---|---:|---:|---:|---:|---|
| rs020008 | 2.626314 | 2.09591e-05 | 2.642171 | 0.000592689 | Replicated |
| rs020065 | 0.404060 | 0.000192765 | 0.745550 | 0.29777 | Not replicated |

## Independent replication and next actions
Replication sample QC retained 120 participants with 0 failures. Variant QC retained 141 markers and excluded 9; both discovery hits passed. Replication used the same additive, ancestry-adjusted likelihood-ratio approach. Its leading-axis phenotype p was 0.188036. The replication criterion was p below 0.05 with concordant dosage direction. Of 2 computed discovery candidates, 1 replicated.

The steward nominated rs020008 only, but full-panel calls allowed independent checking of the additional computed hit. rs020065 had concordant direction but insufficient replication evidence; its small discovery probability cannot override this failure. No unadjusted discovery scan was used to declare associations.

The implemented changes were removal of failing participants and variants and explicit ancestry adjustment. These made the plate analytically usable and the comparison more defensible; they did not establish causality. Reconsider the nonreplicating discovery signal through prespecified ancestry-covariate sensitivity analyses, relatedness checks and technical review, rather than relaxing thresholds or selecting a favorable model. Confirm allele coding with the steward before biological interpretation: effects here are per unit of the supplied dosage, not a named nucleotide allele.

Maintain the frozen QC manifests, scripts, raw released batches and full association tables as the audit trail. Future cohort additions should repeat plate QC and ancestry-overlap review before testing and retain independent confirmation as a reporting gate. Broader ancestry markers and technical/relatedness metadata would strengthen interpretation; these were not provided and those checks were not computed. All required batches were released; no analytical stage ended in a denied-data response. The initial replication request was temporarily locked and was successfully retried after discovery analysis.
