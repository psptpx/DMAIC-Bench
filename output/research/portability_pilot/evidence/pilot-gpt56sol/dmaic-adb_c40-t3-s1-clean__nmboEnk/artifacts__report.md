# Compound-response study: decision report

## Executive conclusion

The sequencing libraries pass the facility's usability and replication rules, but they **cannot support the intended compound-versus-control conclusion**. The preparation design completely aliases study arm with preparation batch. Consequently, the observed arm difference cannot be attributed specifically to compound exposure rather than batch.

The gene-count batch remained locked at the design-identifiability gate. Differential expression was therefore not run. No adjusted significance values, fold changes, significant-gene count, or responding-gene list could be computed. This is **not** evidence that no genes respond; the number and identities of responding genes are unknown.

## What was checked

### Library usability

The per-library metrics were tested against both prespecified facility QC rules.

| QC result | Computed value |
|---|---:|
| Libraries assessed | 12 |
| Libraries failing either rule | 0 |
| Usable control libraries | 6 |
| Usable treated libraries | 6 |
| Minimum usable replication across arms | 6 |

Thus the libraries themselves are adequate and the replication prerequisite is met. Library QC is not the cause of the study failure.

### Design identifiability

The usable sample sheet was evaluated with an intercept, treatment indicator, and preparation-batch indicator. The resulting matrix had 3 columns but rank 2, establishing rank deficiency. There were 2 preparation batches, distributed as follows:

| Study arm | L1 | L2 |
|---|---:|---:|
| Control | 6 | 0 |
| Treated | 0 | 6 |

Every control library was prepared in L1 and every treated library in L2. The treatment indicator is therefore identical to the batch indicator. Adding batch to the model, as required by the facility rules, leaves no independently estimable treatment contrast.

## Where the conclusion stops

The steward refused release of gene-level counts because the computed design-confounded verdict did not satisfy the design-identifiability gate. A valid batch-adjusted gene analysis was therefore impossible. No gene should be called from this experiment, and an unadjusted arm comparison would violate the prespecified analysis plan and conflate compound response with preparation effects.

## Root cause and next action

The root cause is allocation at library preparation, not sequencing quality: arm and batch were not crossed.

The facility should repeat library preparation under a randomized, balanced allocation in which both control and treated samples occur within each preparation batch. Batch identifiers must be retained, and the replacement analysis must include batch in its model. Before counts are analyzed, the facility should re-run the same library QC and explicitly verify that the batch-adjusted design matrix is full rank.

No corrective change has yet been applied, so no recovery in inferential capability can be claimed. The hold point should remain in force: gene-level analysis and gene calls may proceed only after usable replication passes and treatment is demonstrably estimable separately from preparation batch.
