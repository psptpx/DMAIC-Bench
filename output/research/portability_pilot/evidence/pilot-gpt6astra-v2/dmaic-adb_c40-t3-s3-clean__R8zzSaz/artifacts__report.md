# Compound-expression study: hold pending library recovery

## Decision for the principal investigator
The current libraries cannot support a facility-compliant conclusion about the compound. Do not issue a candidate list or interpret the absence of a list as evidence of no biological effect. The immediate limiting factor is insufficient usable treated replication, not an observed absence of expression changes.

## Computed library quality assessment
I applied the facility's joint rule to every library in the released sequencing-metrics batch: assigned reads at least 5,000,000 and mapping rate at least 0.70. A library had to pass both criteria.

| QC result | Computed value |
|---|---:|
| Libraries assessed | 12 |
| Libraries failing QC | 4 |
| Libraries retained | 8 |
| Retained control replicates | 6 |
| Retained treated replicates | 2 |
| Minimum retained across arms | 2 |
| Required usable replicates per arm | 3 |
| Libraries below assigned-read threshold | 2 |
| Libraries below mapping-rate threshold | 2 |

All failed libraries belong to the treated arm. The measured problems are inadequate assigned-read yield and inadequate mapping; the metrics alone do not identify their underlying laboratory causes.

## Where the inference stops
After computing and declaring the minimum retained replication, I requested the sample sheet. The steward **locked** it because the replication requirement was unmet. This is a precondition failure, not a declaration that the sample sheet does not exist.

Consequently, preparation-batch structure among usable libraries could not be assessed. Whether the intended treatment contrast is estimable separately from batch is **unknown**, not established and not demonstrated to be confounded. Gene-level counts, independent qPCR validation and gene-set annotations were not obtained. Differential expression, batch effects, validation concordance and enrichment were not computed. No responsive genes can be nominated from this analysis, and validation cannot currently justify issuing a list.

## Corrective action and control plan
The analytical change made was to exclude unusable libraries and enforce the replication hold. This prevented unsupported gene calling; it did not repair the study. No resequencing or laboratory correction was performed, and no recovery benefit has yet been measured.

The facility should investigate the treated-library failures and re-sequence before resuming gene calling. For low-yield libraries, check library adequacy and sequencing allocation; for low-mapping libraries, investigate read quality, contamination, reference compatibility and preparation problems before assuming additional reads will solve the issue. Reprepare or replace failed biological libraries where necessary, without counting repeated sequencing of the same library as an independent biological replicate.

After recovery, rerun the same QC rules and verify sufficient usable biological replication in each arm. Obtain the sample sheet and check treatment estimability independently of preparation batch. Any additional preparation should avoid arm-specific batches and retain appropriate controls. Only proceed to gene-level analysis once that design check passes, including batch in the model when applicable and applying the prespecified effect-size and multiplicity criteria. Require independent qPCR to meet the facility concordance rule before issuing a candidate list; withhold and reconsider the panel result if validation fails.

Hold these gains through a versioned sample sheet, documented exclusions, batch-balanced preparation planning, and explicit QC, design and validation sign-offs before release. The supplied computation script and trace preserve the current QC decision for audit; downstream conclusions remain pending new usable data.
