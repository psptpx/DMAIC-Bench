# Metabolic-trait candidate-panel study report

## Executive conclusion
The discovery plate can carry a conclusion: the computed sample-failure fraction was **0.0125**, below the protocol limit of **0.1**, so re-genotyping was not triggered. The scan was able to compare affected and unaffected participants because the leading-axis structure test gave PC1 p=0.6507520555249791, and the groups were not separated.

The protocol retained **138** of **150** variants; **12** failed QC. Testing used a Bonferroni threshold of **0.00036231884057971015**. Exactly **1** discovery association passed: **rs000008** (discovery p=7.390179111520088e-11, discovery odds ratio=3.699969164353992).

Replication supports reporting rs000008: **1** of **1** candidate replicated, with replication p=9.684803104789346e-05 and the same direction. The replication odds ratio was **3.377574370709382**. Therefore rs000008 is reportable under the supplied protocol.

## What was changed and what it achieved
Participant and variant QC were applied before association testing. The QC retained **138** variants and left a usable discovery comparison. The initial sklearn PCA implementation failed because that package was unavailable; it was replaced with a NumPy eigen-decomposition, which produced the reported PC1 result. No ancestry covariate was added because the groups were not separated on the leading axis.

The discovery hit was then checked in the independent cohort rather than reported from discovery alone. The replication cohort contained **120** participants, with **60** affected and **60** unaffected; **1** candidate call was missing and was excluded from that candidate calculation.

## What investigators should do next
Report rs000008 as a discovery-plus-replication association, including its direction and effect estimate, while describing this as evidence from the supplied cohorts rather than proof of causality. Independently validate the genotype and phenotype records, document the QC exclusions and missing call, and pursue functional or larger-cohort follow-up before clinical or mechanistic claims.

## Holding the result
Preserve the protocol, raw steward batches, analysis scripts, computed result JSON files, and this trace. Re-run the same QC thresholds and corrected testing rule for any amended data; do not add unplanned variants or covariates without a documented protocol change.

## Limits
No additional data beyond the released discovery and replication batches were used. The available replication batch supplied alpha **0.05** but no separate replication QC thresholds; no unprovided QC rule was invented.
