# Study disposition: technically usable, biologically inconclusive

## Executive conclusion
The libraries pass the facility's sequencing criteria, but this experiment cannot separate a compound effect from preparation batch. Do not issue a compound-response gene list or interpret this as evidence of no response. The limiting issue is the allocation of arms to batches, not sequencing yield.

## Library fitness
Computed from the complete released library-metrics records, all 12 libraries are usable and 0 fail. Control and treated arms each retain 6 replicates, exceeding the required minimum of 3. The lowest assigned-read count is 9,365,000 against a minimum of 5,000,000; the lowest mapping rate is 0.876 against a minimum of 0.70. Each library was assessed against both criteria. The sequencing and replication gates therefore pass, but passing these gates alone does not establish a valid biological contrast.

## Design diagnosis
The usable sample sheet has 2 preparation batches. The first batch contains 6 controls and 0 treated libraries; the second contains 0 controls and 6 treated libraries. An intercept-plus-batch-plus-treatment model has 3 columns but rank 2. The batch-only model also has rank 2: adding treatment supplies no independent information.

Treatment and preparation batch are completely confounded. Any apparent arm difference could be compound response, batch effects, or their combination. Batch adjustment cannot recover a uniquely estimable treatment coefficient, and omitting batch would violate the facility's rules. The design demonstrates aliasing; it does not demonstrate that a batch effect actually occurred or quantify its magnitude.

## Gene conclusions and data boundary
The brief describes a panel of 400 genes and requires adjusted p < 0.05 together with absolute log-fold change on the base-two scale >= 1. These thresholds were read into the computation and retained in the trace; they were not applied to gene estimates.

After the computed confounding verdict was declared, the steward locked the gene-count batch because the identifiability precondition failed. This was a locked release, not a denial that records exist. Gene counts were not obtained, and no expression model, batch-variance estimate, fold change, p-value, adjusted p-value, or significant-gene count was computed. The conclusion stops at design non-identifiability. No genes can be validly called from the present analysis; that is not a computed finding of no significant genes.

## Facility action and control
No laboratory change was implemented in this task. The action taken was to retain all QC-passing libraries, audit the design, and stop the gene-calling workflow before an invalid inference. This achieved an evidence-based hold on the biological conclusion, not a repaired study or an observed improvement in expression results.

The facility should review whether suitable original biological material remains and arrange a crossed, randomized preparation plan with both arms represented within preparation batches. If such material is unavailable, repeat the biological experiment with independent replication and balanced preparation. Merely sequencing these same libraries more deeply cannot remove the aliasing. Any proposed rescue must be reviewed for biological independence and verified for treatment estimability before analysis.

Hold the improvement through a prospective sample-sheet sign-off: verify arm representation across batches, preserve preparation metadata and randomization records, apply the same library QC and retained-replicate gates, and check model rank before releasing counts for gene calling. Once a valid design and usable libraries are available, fit a count-based model including batch and treatment, apply multiplicity correction and the stated effect-size criterion, and independently review the resulting gene list. No rescue outcome or response prediction is claimed here.

## Audit trail
`trace.json` records the executed QC and identifiability computations in order. Released source records are in `data/`; `analyze.py` and `design.py` preserve the calculations. No differential-expression step is listed as executed because it was not run.
