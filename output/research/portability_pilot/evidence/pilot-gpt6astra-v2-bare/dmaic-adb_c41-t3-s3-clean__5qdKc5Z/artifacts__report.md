# Discovery study: hold for re-genotyping

## Executive decision
The current plate cannot support an association conclusion under the study protocol. Of 240 participants, 31 fail the participant call-rate rule. The failure fraction is 0.12916667 (12.916667%), exceeding the plate re-genotyping threshold of 10%. This is a quality-control stop, **not evidence that no variant is associated**.

## What was computed and retained
For each participant, call rate was calculated as nonmissing genotype calls divided by the original panel size. The protocol requires at least 95% calls. Null calls were treated as missing, not as reference genotypes. The complete participant-level results and exact retained/failed membership are in `sample_qc.csv`: `retained=True` means passing this individual rule only.

There are 209 individual-rule passers, comprising 103 affected and 106 unaffected participants. These are provisional QC passers, **not an authorized analysis cohort**: removing failures does not override the plate-level stop. No final variant-retention set has been established.

## Scope of conclusions
Variant call-rate, frequency and control Hardy–Weinberg filtering were not run after the plate failed. Population separation, affected-versus-unaffected comparability, association tests, effect estimates and replication testing were likewise not run. Their values are unknown; none should be reported as null findings or successful validation. Replication cannot rescue an invalid discovery nomination.

A request for replacement calls returned the original discovery data again. The study lead had no matching fact about a replacement plate. Thus no replacement data were obtained and remediation cannot be evaluated. This was not a confirmed steward denial of an existing batch. The conclusion stops at the original plate's QC failure.

## Cause, action and control plan
The demonstrated immediate cause of the stop is excessive participant-level missingness. Its laboratory root cause is not identified from these calls alone. Investigators should quarantine association reporting, have the laboratory review DNA quality, sample handling, plate layout and calling performance, and re-genotype the plate according to the protocol rather than relax thresholds after seeing outcomes.

The change made here was an analytical reporting hold and an auditable participant QC classification, not a laboratory correction. It prevented unsupported downstream inference; no improvement in genotype quality has yet been demonstrated.

On receipt of replacement calls, preserve both versions and rerun participant and plate QC before releasing the hold. Then apply variant QC, evaluate population structure and technical confounding, choose an appropriate association model, correct across retained variants, and test eligible discoveries independently with harmonized alleles and the protocol's direction requirement. The data steward and laboratory should retain the QC manifest and require documented protocol sign-off before investigators report any locus. Keep the replication cohort reserved for that independent validation.

## Audit
`trace.json` records only the sample-QC computation actually completed. `analysis.py` reproduces that calculation and `sample_qc.csv` records its participant-level audit. No synthetic results or unexecuted downstream tests are included.
