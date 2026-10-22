# Study disposition: hold for re-genotyping

## Executive conclusion
The current plate cannot support a protocol-compliant association conclusion. Of **240 participants** measured across **150 variants**, **34 participants** fail the minimum call-rate rule of **0.95**. The failure fraction is **0.141667** (approximately **14.1667%**), exceeding the protocol maximum fraction of **0.1**. The protocol therefore requires re-genotyping the plate before downstream analysis. Dropping the failing participants and testing the remainder would not satisfy that requirement.

## What was computed
Participant call rate was calculated as the fraction of nonmissing genotype calls across the full panel, using the complete steward JSON rather than its preview. The inclusive call-rate rule provisionally passes **206 participants**, comprising **102 affected** and **104 unaffected** participants. These are individual-rule passes, not an approved analysis cohort.

`participant_qc.csv` identifies every participant, their computed call rate, and their pass/fail decision. It is the complete participant retention manifest for this QC assessment. `analyze.py` reproduces the computation; `trace.json` contains the quantitative results and the plate-level decision.

## Where the conclusions stop
- **Participants:** Individual eligibility is documented in the manifest, but the plate as a whole is on hold.
- **Variants:** No variant retention set was computed. Variant call-rate, minor-allele-frequency, and control Hardy–Weinberg filtering must await a plate that passes the initial gate.
- **Comparability:** Ancestry structure was not assessed. Neither comparability nor ancestry separation has been established; similar group counts would not establish comparability.
- **Association:** No association tests were run. No variant can be declared associated or unassociated from this analysis, and a retained-panel significance threshold has not been computed. This is a quality failure, not evidence of absence of genetic effects.

A request for replacement measurements returned the original genotype batch, not a distinct post-remediation plate. No improvement or successful re-genotyping has been demonstrated. The steward exposes no declaration gate for this project; the local computed stop decision is recorded in the trace.

## Cause, action, and verification
The demonstrated reason for stopping is excessive participant-level missing calls. The underlying laboratory cause is not established by these data. The laboratory should investigate DNA quality, plate handling, and calling performance without presuming which caused the failure, then re-genotype the plate under the protocol.

The change made here was to place the analysis on hold and produce an auditable participant QC manifest. It prevents unsupported association claims; it does not repair the measurements. No laboratory intervention was performed and no before/after improvement is claimed.

On receipt of a distinctly versioned replacement batch, repeat sample QC and require documented plate acceptance before variant filtering. Then assess ancestry in the retained cohort before testing: stop if affection status and ancestry are separated; use leading ancestry axes as covariates if structure overlaps. Apply the protocol's Bonferroni correction over the retained variants only after those prerequisites pass.

The study lead should own release authorization, with the laboratory owning remediation and the analysis team owning reproducible QC. Preserve original and replacement data, participant and variant manifests, ancestry diagnostics, and analysis specifications. Keep the quality gate enforced on every replacement release and do not relax thresholds to rescue this plate.
