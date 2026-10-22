# Investigator report

## Decision
The plate passes the protocol's participant-quality gate, but **this cohort cannot support a valid variant–affection association conclusion**. The retained affected and unaffected participants separate completely on the leading genotype principal component. Under the protocol, association testing must stop here; adjusting for ancestry is not a substitute for case-control overlap. No variant has been established as associated, and this is **not** a negative association study.

## Technical quality and retained data
Participant call rates were computed over all 150 supplied variants. Of 240 participants, 1 failed; the failure fraction is 0.00416667, below the protocol's plate re-genotyping trigger. Retain every supplied participant except P198. The retained cohort contains 239 participants: 120 affected and 119 unaffected. The complete participant-level rates and retention decisions are in `participant_qc.csv`.

Variant QC was then computed only in the retained participants. Allele frequency uses observed calls; Hardy–Weinberg equilibrium uses an exact conditional, probability-ordering test in unaffected participants. Applying all protocol cutoffs retained 138 variants and excluded 12: 5 failed call rate, 4 failed minor-allele frequency, and 3 failed control Hardy–Weinberg equilibrium.

Excluded variants: rs010047, rs010057, rs010063, rs010072, rs010088, rs010092, rs010101, rs010118, rs010128, rs010133, rs010141, rs010149.

**Retain every supplied variant except those listed above.** `variant_qc.csv` provides the exhaustive named roster, rates, frequencies, equilibrium probabilities and retention flags. The computed Bonferroni threshold would be 0.00036231884058 if a comparable cohort were available; it was not used to test this noncomparable cohort.

## Cohort comparability
I mean-imputed missing retained genotypes and standardized each variant by its pooled allele-frequency-based variance before singular-value decomposition. The leading component explains a variance fraction of 0.09941361. Its affected score range is -5.854109 to -1.745464; the unaffected range is 0.387946 to 7.173129. These ranges do not overlap. A Welch comparison gives p = 3.3491195e-135. The stopping decision rests on complete separation, not merely statistical significance. Scores are saved in `pca_scores.csv`.

The steward could not route a separate ancestry-score request; it did not deny an existing batch. The comparability assessment was therefore computed directly from supplied calls. This candidate-region panel demonstrates strong phenotype-aligned genetic structure but cannot by itself identify named ancestries or exclude technical batch effects. Independent ancestry markers and recruitment/processing records are needed to establish the source of the separation.

## What changed and what it achieved
Quality filtering removed low-quality participants and variants and produced an auditable technically eligible subset. It did not remove phenotype-aligned structure. No laboratory correction, new recruitment, or adjusted association analysis was performed. Association probabilities, significant-variant counts, and genomic inflation were deliberately not computed after the comparability gate failed.

## Recommended recovery and control
Pause association claims and investigate recruitment ancestry, sample provenance, and genotyping batch alignment with affection status. Obtain independent ancestry information and technical records. Recruit ancestry-matched affected and unaffected participants with genuine overlap, or form adequately represented within-ancestry comparisons; do not extrapolate an adjusted model across separated groups. Re-genotyping alone would not repair an ancestry-confounded sampling design, though confirmed technical artifacts would require laboratory correction.

Before reopening testing, freeze the revised analysis plan, rerun participant and variant QC, and verify ancestry overlap blind to variant-level associations. If structure remains but overlaps, use the leading ancestry axes as prespecified covariates, check calibration, and apply the multiplicity rule to the newly retained panel. Seek independent replication of any eventual findings. Hold the improvement through versioned inclusion lists, reproducible scripts, recruitment balance checks, plate-level QC review, and an explicit comparability sign-off before any association release.

## Audit trail
`trace.json` records the analyses actually run and the decisive branches; the supplied batches and analysis scripts remain alongside the detailed audit tables. There are no association-test entries because those tests were not run.
