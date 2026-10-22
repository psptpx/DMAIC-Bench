# Study decision: report a replicated, ancestry-adjusted association

## Executive conclusion
The plate can support analysis under the protocol. **rs020008 is the sole discovery association and independently replicates.** This supports reporting an association with affection status, not a causal effect or a clinically validated predictor. The principal threat was overlapping ancestry imbalance, not wholesale plate failure. Analysis was changed by excluding poor-quality records and adjusting for the leading ancestry axis; laboratory re-genotyping was not required by the plate rule.

## Quality and retention
Discovery contained 240 participants and 150 variants. Participant call-rate filtering excluded 2 participants (failure fraction 0.00833333), below the protocol's plate-stop boundary. Retained: 238 participants, comprising 118 affected and 120 unaffected.

Excluded participants: P017, P111. All other supplied discovery participants are retained. The complete identity-level manifest and computed call rates are in `participant_qc.csv`.

Variant QC was calculated after participant filtering, with allele frequency from called genotypes and exact conditional Hardy–Weinberg tests in unaffected participants. It excluded 11 variants: 5 for call rate, 4 for minor-allele frequency, and 2 for Hardy–Weinberg departure. Retained: 139.

Excluded variants: rs020001, rs020016, rs020037, rs020045, rs020054, rs020072, rs020084, rs020085, rs020114, rs020117, rs020142. All other supplied discovery variants are retained; `variant_qc.csv` lists each identity, criterion value and decision.

## Can affected and unaffected participants be compared?
PCA used retained variants, mean-imputed missing calls, and allele-frequency standardization. Leading-axis group contrasts used Welch tests; ranges were inspected for disjoint support. The leading ancestry axis differed strongly by affection status (p = 4.19527e-18; variance fraction 0.101701), but the groups overlapped (range overlap 10.671221). No inspected leading axis had disjoint case/control ranges. Thus this is **overlapping structure requiring adjustment**, not a separated-ancestry stop and not permission for a naive scan. Other leading axes showed no persuasive affection association.

This panel-based diagnostic is not proof of genome-wide ancestry balance. Dense ancestry markers and matching would strengthen future studies.

## Discovery result
The additive logistic scan included the leading ancestry axis as a covariate, using called genotypes separately for each variant. The Bonferroni threshold over retained variants was 0.00035971223. It found 1 significant variant. Genomic inflation, calculated as the median squared Wald statistic divided by its null median, was 0.993961; it is descriptive on a small candidate panel, not a substitute for ancestry control.

For **rs020008**, the adjusted coded-allele odds ratio was 2.626314, with Wald interval 1.652831–4.173158, and p = 4.3746074e-05. `association.csv` contains the full scan. Effects refer to the supplied dosage coding; nucleotide allele labels were not supplied and are not inferred.

## Independent replication
Replication retained 120 participants (60 affected and 60 unaffected), with 0 participant failures. Replication QC retained 141 variants and excluded 9; the nominated variant passed. Identity-level replication manifests are also saved.

Replication PCA showed overlapping groups without an affection-associated leading axis; the leading-axis p-value was 0.188036. The replication additive logistic test therefore used no ancestry covariates. For rs020008, 119 called participants gave an odds ratio of 2.729998 and p = 0.00069668495, in the same direction as discovery. The protocol's nominal significance and same-direction requirements were met: 1 of 1 candidates replicated. Reporting this association is supported.

## Actions and controls
Freeze the retained identity manifests, raw steward batches, scripts, and full scan with this report. Do not restore failed variants or participants opportunistically. Keep ancestry assessment ahead of testing and maintain multiplicity correction and independent confirmation as release gates. Before publication, verify physical effect-allele alignment, genotype cluster quality at the hit, and cohort independence with the data steward. Follow with denser ancestry characterization and external confirmation before mechanistic or clinical claims.

No requested study batch was denied, and no missing replication result was substituted. No biological mechanism, intervention effect, or prospective clinical benefit was computed. The achieved change is an analytically controlled and independently supported association, not a demonstrated improvement in patient outcomes.
