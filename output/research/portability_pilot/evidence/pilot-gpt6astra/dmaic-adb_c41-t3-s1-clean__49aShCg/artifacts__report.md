# Investigator report

## Executive conclusion
The plate is technically usable after quality filtering, but **this cohort cannot support a valid variant–affection association conclusion**. Affected and unaffected participants occupy completely separate ranges of the leading genotype structure axis. The protocol requires stopping before variant testing in this situation. This is not a finding of no associated variants: association status remains unestablished.

## Plate and participant quality
Computed call rates from the released genotype matrix. Of 240 participants and 150 variants, 1 participant failed the participant call-rate rule (failure fraction 0.004166666666666667). This is below the protocol's plate-replacement trigger, so re-genotyping the whole plate is not indicated by that rule.

Retained 239 participants: 120 affected and 119 unaffected. Excluded **P198**, with call rate 0.9466666666666667. All other released participant identifiers are retained. The complete per-participant disposition is in `participant_qc.csv`.

## Variant quality
Applied variant filters after participant exclusion. Minor-allele frequency uses the retained cohort; Hardy–Weinberg equilibrium uses only retained unaffected participants and a two-sided exact conditional test. Retained 138 variants and excluded 12: 5 for call rate, 4 for minor-allele frequency, and 3 for control Hardy–Weinberg departure.

Excluded variants by criterion:
- Call rate: rs010047, rs010072, rs010088, rs010101, rs010118.
- Minor-allele frequency: rs010057, rs010063, rs010141, rs010149.
- Control Hardy–Weinberg equilibrium: rs010092, rs010128, rs010133.

All other released variants are retained for cohort assessment, not cleared for association claims. `variant_qc.csv` contains the complete retained/excluded list with the measured metrics. These exclusions do not themselves establish the laboratory or biological cause of the failures.

## Cohort comparability: stop here
Performed PCA on the retained genotype matrix, imputing missing calls to variant means and standardizing by allele-frequency-based genotype standard deviations. The leading axis explains variance fraction 0.09941361305958868. Its affected range is −5.854108831118341 to −1.7454640482762065; its unaffected range is 0.38794628752205057 to 7.173129379437073. There is no overlap. A Welch comparison of this axis gives p = 3.3491194783865236e-135. The range separation, not merely the small p-value, determines the stop decision.

The candidate-panel PCA demonstrates severe genotype structure aligned with affection, consistent with ancestry confounding. It cannot independently identify ancestry populations or exclude a phenotype-aligned technical batch effect. Separate ancestry-marker or recruitment-ancestry metadata requests were unroutable; no external ancestry batch was obtained, and no request was marked denied. The available internal evidence nevertheless fails the protocol's comparability prerequisite. Covariate adjustment is not an adequate substitute for shared ancestry support in this separated cohort.

## Association and next action
No variant association test, genomic inflation estimate, or adjusted association model was run. No variant is declared associated; the number truly associated cannot be computed from a valid comparison here. Bonferroni testing is deferred rather than used to rescue the confounded design.

Quality filtering changed the analytical cohort and removed technically unsuitable variants, but did not restore comparability. No laboratory remediation or recruitment change was implemented, and no post-change improvement can be claimed.

Investigators should audit recruitment ancestry and genotyping batch against affection status, obtain independent ancestry-informative markers or broader genome-wide coverage, and recruit ancestry-matched affected and unaffected participants with genuine overlap. Balance and randomize their laboratory processing. Repeat participant and variant QC and the ancestry-overlap gate on the revised cohort before testing. If residual structure overlaps, use prespecified leading ancestry axes as covariates and apply the protocol's retained-panel multiplicity correction. Validate any eventual signals in an independent matched cohort.

Hold the process through versioned protocol thresholds, immutable raw-data snapshots, complete exclusion manifests, a documented ancestry-overlap sign-off before testing, and renewed QC after each added batch. The supplied scripts, manifests and `trace.json` preserve the computations and the decision to stop.
