# Study status: technically usable plate, non-comparable cohort

## Principal-investigator decision
Do not report a variant association from this discovery cohort. The plate passes participant quality control, but affected and unaffected participants occupy disjoint ranges on the second leading genotype principal component. This violates the protocol's ancestry-comparability prerequisite. Adjusting a regression for ancestry would not supply the missing within-ancestry comparison.

## Quality control and retention
Of 240 discovery participants, 1 failed the participant call-rate rule (0.416667%); 239 remain, comprising 120 affected and 119 unaffected participants. The observed failure fraction does not trigger protocol-mandated plate re-genotyping.

Excluded participant: P129. All other released participants are retained. The complete membership and individual call rates are in `sample_qc.csv` and `retained_participants.csv`.

Variant QC was calculated after participant exclusion, using observed-call allele frequencies and a two-sided exact Hardy–Weinberg test in unaffected participants. There are 137 retained and 13 excluded variants: 5 fail call rate, 4 fail minor-allele frequency, and 4 fail control Hardy–Weinberg equilibrium.

Excluded variants: rs060002, rs060010, rs060024, rs060037, rs060043, rs060055, rs060083, rs060093, rs060104, rs060111, rs060114, rs060139, rs060144. All other released variants are retained. `variant_qc.csv` records each criterion and retention decision; `retained_variants.csv` is the explicit retained manifest.

## Comparability precedes association
PCA used the retained genotype matrix, mean-imputed missing calls, and allele-frequency standardization. Leading axes were assessed using case/control score ranges and Welch comparisons. The first component has case/control p = 0.467190; checking it alone would miss the problem. The second component has p = 1.07733e-140 and a positive between-group range gap of 1.97606 score units: the ranges do not overlap. This supports ancestry-linked cohort separation, not merely overlapping structure suitable for covariate adjustment. Genotype PCA is an ancestry proxy; recruitment and ancestry metadata should be audited to establish the operational source of the separation.

## Association and replication
No variant association test was run, no odds ratio was estimated, and no discovery hit was nominated. These quantities are not computable as valid protocol-compliant study conclusions on this non-comparable cohort; this is not a finding of no genetic effects. Replication was not requested or analysed because the discovery analysis must stop first. No replication support can be claimed. There was no steward denial of a requested batch.

## What changed and what happens next
The completed changes are analytical quality filtering and an explicit ancestry-comparability gate. Filtering produced a technically retained dataset, but did not remove the design failure. No recruitment or laboratory intervention has yet been implemented or shown effective.

Audit recruitment sources, ancestry information, sample labels and processing history. Recruit ancestry-overlapping affected and unaffected participants, or redesign the study around adequately represented within-ancestry comparisons. Re-genotyping alone is not a remedy for ancestry-confounded recruitment. Preserve the original data, QC manifests and executable analysis, and require the same QC and leading-axis overlap review for any revised cohort before releasing association results. Only after comparability is established should investigators apply the protocol's multiple-testing correction and require independent, same-direction replication before reporting a discovery association.
