# Metabolic-trait candidate-panel study report

## Executive conclusion
The discovery plate can proceed without re-genotyping: the computed participant failure fraction was **0.0125**, below the protocol trigger of **0.1** (the trigger itself is a protocol threshold, not a study result). The retained discovery cohort contains **240** participants and **2** variants after QC. The affected and unaffected groups were not separated on the tested leading axis (PC1 p=0.11642150053597505); the cohort was therefore treated as comparable.

No discovery association passed the Bonferroni scan: **0** significant variants were found among the retained variants, with lambda-GC **0.0**. The two retained variants were rs070049, rs070099; neither is a reportable hit.

The steward supplied **1** replication candidate, **rs070008**. It did not meet the replication decision: replicated candidates were **0** of **1**. Consequently, there is no association to report.

## What was changed and what it achieved
Missing calls were handled as missing for call-rate and allele-count calculations. Participant QC removed no records from the analysis cohort because the plate-level trigger was not met; variant QC retained only variants meeting the protocol call-rate, control-MAF, and control-HWE rules. The ancestry check supported direct case-control comparison. These changes reduced the panel to **2** analyzable variants and prevented unsupported claims from the scan.

## Limitation and next action
The replication release nominated **rs070008**, while the discovery QC/association computation retained a different set of variants and found no significant discovery hit. This candidate mismatch must be resolved by the study lead/data steward before any biological interpretation. Do not report an association. Reconcile the nomination and rerun the prespecified discovery-to-replication workflow; if a future candidate is nominated, require replication p < 0.05 and the same direction before reporting.

## Holding the result
Archive the released batches, the computation script, **trace.json**, and this report together. Any rerun should preserve the same QC thresholds, ancestry gate, multiple-testing correction, and replication rule, and should append a new trace rather than overwrite this record.
