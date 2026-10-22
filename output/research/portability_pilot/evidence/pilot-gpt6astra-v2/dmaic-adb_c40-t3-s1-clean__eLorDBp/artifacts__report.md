# Study disposition: withhold compound-response conclusions

## Executive conclusion
The libraries are technically usable, but the experiment cannot separate a compound effect from a preparation-batch effect. Do not issue a responding-gene list. This is **not evidence that the compound has no effect**: the intended comparison is not identifiable on the available design.

## What was computed
Library usability was evaluated jointly against the assigned-read and mapping-rate cutoffs in the facility brief. All **12** libraries pass; **0** fail. Each arm retains **6** usable biological replicates, satisfying the facility's replication requirement. Thus library quality and retained replication do not force re-sequencing.

Among usable libraries there are **2** preparation batches. The first contains **6** controls and **0** treated samples; the second contains **0** controls and **6** treated samples. I constructed an intercept-plus-batch-plus-treatment model matrix. Its rank is **2** for **3** columns; the batch-only matrix also has rank **2**. Adding treatment therefore supplies no independent information. Treatment and batch are completely aliased.

These results are recorded under `qc.sample_qc` and `design.identifiability` in the accompanying trace. The sample sheet was restricted to libraries passing QC before evaluating the design.

## What can and cannot be concluded
The libraries could support technical descriptions, but not the causal compound-versus-vehicle conclusion requested here. An unblocked comparison would attribute inseparable batch differences to treatment; a batch-adjusted model cannot estimate a distinct treatment coefficient. Computational batch correction cannot restore the missing experimental contrast.

After I declared the computed confounding verdict, the steward **locked** the gene-count release on the identifiability criterion. This was not a denial that the records exist. No differential-expression analysis, batch-variance estimate, responding-gene count, or gene identity was computed. A lack of callable results must not be reported as an absence of responding genes.

The qPCR validation and gene-set annotation remain downstream of that locked stage. Validation concordance and pathway enrichment were not computed. Consequently there is no evaluated independent-validation support for issuing a list. No batch was reported by the steward as nonexistent; the limitation is a failed design precondition, not a guessed replacement for missing evidence.

## Action and control plan
No libraries or experimental assignments were changed during this analysis. The change was to the study's analytical disposition: technical QC passed, but inference was halted before unsupported gene calls. This prevents a batch contrast from being presented as a drug response; it does not repair the experiment.

Verify the preparation records with the facility. If the recorded assignment is correct, prepare a new balanced experiment in which both arms are represented within preparation batches, randomizing preparation order and retaining adequate biological replication. Where suitable biological material remains, consider re-preparing balanced libraries from it; otherwise repeat the biological experiment. Simply obtaining more reads from the same segregated libraries will not resolve the confounding.

Before committing the replacement libraries to sequencing, audit the sample sheet and require an estimable treatment contrast. Apply the existing QC rules, then fit a model including batch, use the facility's multiple-testing and effect-size criteria, and independently validate the nominated candidates before list release. Keep the brief, sample assignments, QC decisions, design-rank check, and validation decision as release-gate records. Escalate any failed gate rather than bypassing it.
