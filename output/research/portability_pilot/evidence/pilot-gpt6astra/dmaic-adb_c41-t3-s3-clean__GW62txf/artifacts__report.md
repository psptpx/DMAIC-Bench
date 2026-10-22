# Study status: plate rejected pending re-genotyping

## Decision for the principal investigator
The current plate cannot support an association conclusion under the released protocol. Participant call-rate QC found **34 failures among 240 participants**, a failure fraction of **0.141667** (approximately **14.1667%**), exceeding the protocol ceiling of **0.1**. Re-genotype the plate before downstream analysis; removing failed participants alone does not satisfy this rule.

## Computation and participant disposition
Using the complete steward genotype batch, I calculated each participant’s call rate as nonmissing calls divided by all panel calls. Participants pass at a call rate of at least **0.95**. The participant-level audit in `participant_qc.csv` identifies every participant, their calculated call rate, and their pass/fail disposition.

**206 participants** meet the individual rule: **102 affected** and **104 unaffected**. These are provisional individual passes, not an approved analysis cohort: the plate-level stop overrides their eligibility for association testing.

## What remains unknown
Variant QC was deliberately not run after the plate failed. Consequently, no retained-variant set or multiple-testing cutoff has been established. Ancestry structure and affected/unaffected comparability have not been assessed. No variant association tests were run: this is not evidence that no variants are associated. Neither significance counts nor inflation estimates can be reported.

A request for replacement re-genotyping data re-served the original genotype batch; it supplied no distinct replacement plate. No improvement has therefore been demonstrated. The conclusion stops at plate quality.

## Cause, action, and sustained control
The demonstrated reason for the stop is excessive participant-level missing genotype calls. The laboratory root cause is not established by these data. Ask the laboratory to investigate DNA quality, processing failures, and calling performance, then re-genotype under the protocol. These are recommended actions, not completed interventions.

The analysis workflow was halted to prevent an unsupported biological claim; no genotype values were imputed or altered. Preserve the original batch and participant QC audit. On replacement data, rerun the plate-level gate before participant and variant filtering. Only after passage should the team apply variant call-rate, minor-allele-frequency, and unaffected-participant Hardy–Weinberg criteria, then assess ancestry comparability. Separate ancestries require redesign rather than a naive comparison; overlapping structure requires appropriate ancestry covariates. Apply the protocol’s Bonferroni rule over retained variants only after these prerequisites are met. Hold release of investigator conclusions until the QC and comparability evidence is reviewed and archived.

## Reproducibility
`analyze.py` contains the computation; `trace.json` records the calculated results and stop decision. The complete source batch is `data/genotypes.json`, and the released protocol is `data/define.json`.
