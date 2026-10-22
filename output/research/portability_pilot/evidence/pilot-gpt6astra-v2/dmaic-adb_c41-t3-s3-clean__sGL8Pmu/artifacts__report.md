# Study status: discovery plate on hold

## Decision for the principal investigator
The current plate cannot support an association conclusion under the released protocol. Re-genotype the plate before proceeding. This is a technical quality stop, not evidence that the panel has no association with the trait.

## What was computed
Using the complete steward discovery file, participant call rate was calculated as the proportion of nonmissing calls across the 150 variants. Of 240 participants, 31 failed the minimum call rate of 95%. The failure fraction is 0.1291666667 (12.916667%), exceeding the protocol plate limit of 10%.

There are 209 individual call-rate passes: 103 affected and 106 unaffected participants. These are **provisional individual passes, not an approved analysis cohort**. The file `sample_qc.csv` names every participant, gives their computed call rate, and flags whether they pass the individual rule. Its `retained` column means only individual call-rate eligibility; the plate-level veto takes precedence.

## What cannot yet be concluded
- **Variant retention:** not computed. The protocol requires re-genotyping before further analysis; no final retained-variant list is established.
- **Cohort comparability:** not evaluated. Neither ancestry overlap nor ancestry separation can be claimed from the completed QC calculation.
- **Discovery associations and effects:** not tested. No discovery hit or absence of hits is established.
- **Replication:** not requested or tested because there are no valid discovery candidates. Replication cannot rescue the failed discovery plate.

The replacement-call request returned the original discovery batch, not a new plate. A follow-up question to the lead was unroutable. No replacement data were obtained; this is not a confirmed steward denial that such data exist. The conclusion stops at sample QC.

## Cause, corrective action, and control
The demonstrated immediate cause of the stop is excessive participant missingness relative to the prespecified acceptance rule. The laboratory root cause is unknown; do not attribute it to ancestry, disease status, DNA quality, or equipment without evidence.

The change made in this analysis was to place an explicit hold on downstream testing rather than remove failed participants and continue. This achieved protocol compliance and prevented unsupported association claims; no laboratory correction or improvement has yet been demonstrated.

The investigators should commission plate re-genotyping and have the laboratory review extraction quality, sample handling, calling performance, and batch records. Preserve the original calls and this QC audit. On receipt of a versioned replacement batch, rerun participant QC and release the plate only if it passes the same protocol gate. Then apply variant call-rate, allele-frequency, and control Hardy–Weinberg filters; assess leading ancestry axes before testing; use ancestry adjustment only where cohort overlap supports comparison. Apply the protocol's retained-panel multiplicity correction and require independent, directionally consistent replication before reporting any association. Reconsider discovery findings that fail replication.

Assign laboratory ownership for remediation and statistical ownership for release approval. Retain the participant and variant disposition tables, analysis scripts, cohort-comparability evidence, and replication decisions with each batch. Do not relax thresholds after seeing results.

## Audit trail
`trace.json` contains the completed sample-QC analysis and the plate-stop decision. `analyze.py` contains the reproducible calculation and a guard that exited before variant QC, ancestry analysis, or association testing. Those unexecuted portions are not recorded as completed analyses.
