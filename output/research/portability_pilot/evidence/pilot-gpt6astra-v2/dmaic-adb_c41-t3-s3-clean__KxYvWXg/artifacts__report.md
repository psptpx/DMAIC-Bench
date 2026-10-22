# Study status: discovery plate must be re-genotyped

## Decision for the principal investigator
The current plate cannot support an association conclusion under the released protocol. Of 240 participants, 31 have call rate below 0.95. The failure fraction is 12.9167%, exceeding the allowed 10%. Dropping these participants alone is not an acceptable substitute for the required plate re-genotyping.

The immediate cause of the stop is excessive missing genotype calls. The underlying laboratory cause has not been established; no laboratory troubleshooting records were supplied.

## Retention audit, not approval to proceed
The participant rule provisionally leaves 209 participants: 103 affected and 106 unaffected. The complete passing and failing identifier lists are in `retained.json`.

The initial script mistakenly continued into variant QC and ancestry diagnostics before enforcing the plate stop. Those computations are preserved in `trace.json` for transparency, but do not override the protocol or establish an analysis-ready cohort. On the provisionally passing participants, exact control Hardy–Weinberg testing and call-rate/minor-allele-frequency filtering leave 139 variants and exclude 11: 5 fail call rate, 3 fail minor-allele frequency, and 3 fail Hardy–Weinberg equilibrium. The respective thresholds were 0.95, 0.01, and 0.000001. Complete provisional variant lists are also in `retained.json`; final retention must be recomputed after re-genotyping.

Exploratory PCA used mean-imputed genotypes standardized by allele variance. Leading-axis case/control ranges overlapped; the first-axis Welch comparison gave p = 0.08656. This is neither proof of ancestry equivalence nor permission to compare cases and controls on a failed plate. Leading-axis diagnostics must be repeated on the corrected, quality-controlled cohort.

## Association and replication
No variant association tests or effect estimates were run. There are no nominated discovery associations, and replication was not tested. This means associations are **undetermined**, not absent. Replication cannot rescue a discovery plate that violates the protocol.

## Corrective action and hold
The request for corrected data returned the original discovery batch. The study lead supplied no matching fact about replacement data. This was an unresolved request, not a denial establishing that replacement data cannot exist. No corrected plate was obtained, no laboratory change was implemented here, and no improvement can be claimed.

Quarantine the current plate from inference. Ask the laboratory to investigate DNA quality, handling, assay performance and plate layout, document the cause, and re-genotype as required. Preserve participant and allele identifiers and keep phenotype-blinded QC logs. Release the replacement only after the participant failure gate passes; then recompute variant QC and ancestry diagnostics. If ancestries are separated, redesign recruitment rather than test confounded groups; if structure overlaps, adjust association models for its leading axes. Apply the protocol's retained-panel multiplicity correction, and report discovery hits only after independent, directionally consistent replication. Maintain a signed QC gate and versioned analysis log to prevent this premature downstream processing from recurring.
