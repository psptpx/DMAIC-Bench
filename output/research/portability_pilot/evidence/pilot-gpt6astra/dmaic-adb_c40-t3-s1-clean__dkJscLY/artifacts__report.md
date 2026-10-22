# Compound study: library quality passes, causal comparison cannot proceed

## Executive decision
The libraries are technically usable, but this experiment cannot support a compound-versus-vehicle expression conclusion separately from preparation batch. Do not issue a compound-responsive gene list from this design. This is an unidentifiable comparison, not evidence that the compound has no effect.

## What was computed
Using the released per-library metrics and the facility's read-depth and mapping-rate rules, all **12 libraries** passed; **0 failed**. There are **6 usable controls** and **6 usable treated replicates**, so the retained-replication gate passes. The lowest assigned-read count was **9,365,000**, and the lowest mapping rate was **0.876**. These are the computed results in the `qc.sample_qc` trace entry. Re-sequencing for inadequate depth is not indicated by these metrics.

The retained sample sheet contains **2 preparation batches**. The control-only batch contains **6 controls and 0 treated samples**; the treated-only batch contains **0 controls and 6 treated samples**. There are **0 mixed-arm batches**. The batch-only model matrix has rank **2**. Adding treatment leaves rank **2** despite **3 model columns**. These results are recorded in `design.identifiability`.

Thus treatment is perfectly aliased with preparation batch. Batch adjustment cannot identify an independent treatment coefficient, while ignoring batch would label the joint treatment/batch difference as a compound effect. The data do not establish whether batch actually changed expression; they establish that such a change cannot be distinguished from treatment.

## Gene results and data boundary
The steward locked the gene-count release because the computed design verdict failed the identifiability gate. This was a **locked** request, not a claim that the archive lacks counts. No gene-level analysis was run. Fold changes, adjusted significance values, batch variance contributions and the number of responsive genes could not be computed. Conclusions stop at library usability and design non-identifiability; neither responsive genes nor an absence of response can be asserted.

## Facility action and sustained control
No physical experimental change was made in this task. The analytical action was to retain the technically passing libraries but stop gene calling at design review, preventing an unsupported biological conclusion. No rescue outcome has been demonstrated.

The study lead and facility should plan a balanced repeat or a scientifically justified re-preparation from suitable retained biological material. Allocate both arms across preparation batches, randomize handling and sequencing positions, and preserve biological replicate identities. Simply sequencing the existing confounded libraries more deeply will not repair the missing treatment/batch overlap. Re-preparation is a potential remedy only if upstream treatment and handling confounding are also addressed.

Before committing further sequencing, require a signed sample-sheet review verifying treatment estimability and within-batch arm overlap. Repeat library QC and retained-replication checks on the revised study, then verify model rank before releasing counts for inference. Include preparation batch in a multi-batch expression model and apply the facility's predeclared adjusted-significance and effect-size rules. Archive the allocation, QC exclusions, model specification and gene-call audit trail. Only new, identifiable data can demonstrate that the corrective work succeeded.
