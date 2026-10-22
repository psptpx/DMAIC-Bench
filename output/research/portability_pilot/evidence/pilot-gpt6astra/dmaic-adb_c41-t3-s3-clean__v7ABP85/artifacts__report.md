# Study status: stop and re-genotype

## Executive decision
The current plate cannot support an association conclusion under the released protocol. The sample failure fraction is **0.1416666667**, above the allowed **0.1**. Re-genotyping is required before downstream analysis; excluding poorly called participants alone does not satisfy the protocol.

## Computed evidence
Using the complete steward genotype batch, I calculated each participant's call rate as the fraction of nonmissing calls across the panel.

| Measure | Result |
|---|---:|
| Participants evaluated | 240 |
| Variants per participant | 150 |
| Affected participants | 120 |
| Unaffected participants | 120 |
| Required participant call rate | 0.95 |
| Participants failing | 34 |
| Participants individually passing | 206 |
| Affected participants failing | 18 |
| Unaffected participants failing | 16 |
| Lowest observed call rate | 0.52 |
| Highest observed call rate | 1.0 |

The exact participant-by-participant disposition and call rates are in `participant_qc.csv`: participants marked passing satisfy the individual rule, but are **not an authorized analysis cohort** because the plate-level gate failed. The quantitative results above are recorded in `trace.json` and reproducible with `analyze.py`.

## What remains unresolved
- **Variants retained:** not determined. Variant call-rate, minor-allele-frequency and unaffected-only Hardy–Weinberg filtering were not run because the protocol requires re-genotyping first.
- **Cohort comparability:** not established. Ancestry assessment was not performed; the present result is a technical-quality stop, not evidence of ancestry separation or overlap.
- **Associations:** not tested. No significant-variant count, association probabilities, genomic inflation estimate or corrected testing threshold has been computed. This is not a finding that the panel has no associations.
- **Replacement plate:** requesting replacement calls returned the original batch again. No new post-remediation data were supplied, so improvement cannot be evaluated.

## Cause, action and control
Excessive participant-level missingness is the measured reason for stopping. Its laboratory root cause is unknown: DNA quality, plate handling and calling performance are possibilities to investigate, not established explanations.

Quarantine the current plate from association reporting. Have the laboratory review sample integrity, processing records and calling diagnostics, correct any documented defects, and re-genotype the plate as the protocol requires. No laboratory change has been performed or validated in this analysis; the achieved change is an explicit analysis hold that prevents an unsupported biological conclusion.

On receipt of replacement calls, repeat the same sample gate before variant filtering. After acceptable sample and variant QC, establish ancestry comparability before testing: separate ancestries preclude the comparison; overlapping structure requires leading ancestry axes as covariates. Apply the protocol's Bonferroni correction over the actual retained variants, then independently validate any findings.

Hold the improvement through versioned genotype batches, saved participant and variant exclusion logs, laboratory sign-off on the plate gate, and documented ancestry assessment before any association release. The study remains at the quality-control stop until replacement data demonstrate that it can proceed.
