# Study decision: technically usable plate, non-comparable cohort

## Executive conclusion
The plate passes participant-level quality control, but **this cohort cannot support an association conclusion under the protocol**. Affected and unaffected participants occupy disjoint ranges on the second leading genotype ancestry axis. This is a design/comparability failure, not evidence that the panel lacks associated variants. Neither an unadjusted scan nor ancestry-adjusted regression is justified when the required ancestry overlap is absent.

## Quality control and retained data
The discovery matrix contains 240 participants and 150 variants. Participant call rates were calculated across the original panel before variant filtering. There were 1 failures, a fraction of 0.00416667 (0.4167%). This is below the protocol's plate rejection boundary, so wholesale re-genotyping is not triggered.

Retain all supplied participants except **P129**. This leaves 239 participants: 120 affected and 119 unaffected. The complete identifier-level retention decisions and call rates are in `sample_qc.csv`.

Variant QC was then recomputed on retained participants. Call rate and pooled minor-allele frequency were calculated from observed calls; Hardy–Weinberg equilibrium used a conditional exact two-sided test among unaffected participants. There were 5 call-rate failures, 4 frequency failures, and 4 equilibrium failures. In total 13 variants fail and 137 are retained.

Retain all supplied variants except **rs060002, rs060010, rs060024, rs060037, rs060043, rs060055, rs060083, rs060093, rs060104, rs060111, rs060114, rs060139, rs060144**. `variant_qc.csv` gives every identifier, metric, and final retention decision. QC filtering changed the analytical input, but did not fix its ancestry imbalance.

## Required comparability assessment
PCA used retained variants, genotype-mean imputation for missing calls, centering, and allele-frequency variance scaling. Leading-axis case/control comparisons used Welch tests, alongside inspection of group score ranges; a mean difference alone was not treated as proof of non-overlap.

The first axis has case/control p = 0.46719, with overlapping ranges. Stopping the ancestry check there would be misleading. The second axis has p = 1.07733e-140, explains a variance fraction of 0.0861589, and **completely separates affection groups**:

- Affected score range: 1.63031 to 5.26971.
- Unaffected score range: -5.59956 to -0.345749.

PCA signs are arbitrary; the non-overlap is not. The remaining computed leading-axis diagnostics and individual scores are retained in `trace.json` and `pca.csv`. These genotype-derived axes establish the protocol stop condition; they do not identify named ancestral populations or prove a specific recruitment mechanism.

## Association and replication status
**No variant association test was run.** The prospective Bonferroni threshold calculated from the retained panel is 0.000364963504, but a threshold cannot make a non-comparable cohort valid. Effect estimates, genomic inflation, and discovery hits were not computed. There are no valid nominated discovery candidates, rather than a demonstrated negative scan.

Replication was not requested or analysed because discovery failed the required comparability precondition. Replication support is therefore undetermined, and no association is reportable. This is a deliberate protocol stop, not a steward denial or a claim that replication records do not exist.

## Investigator action and sustained control
Investigate ancestry imbalance in recruitment and possible phenotype-linked laboratory or sampling effects. Obtain broader ancestry markers and recruitment/batch metadata to clarify the source. Recruit affected and unaffected participants within shared ancestry strata, or redesign the cohort with demonstrable common support. Simply adding principal components to regression is not a repair for the observed separation.

No laboratory correction or recruitment intervention has yet been carried out, and no improvement in comparability has been demonstrated. The achieved change is analytical: low-quality records were removed and an invalid comparison was prevented. Preserve the supplied batches, scripts, QC tables, and trace as the audit record. On a revised cohort, repeat participant QC, variant QC, and leading-axis overlap checks before unlocking association testing; then apply the prespecified multiple-testing rule and independent same-direction replication requirement. Hold reporting until both comparability and replication requirements are met.
