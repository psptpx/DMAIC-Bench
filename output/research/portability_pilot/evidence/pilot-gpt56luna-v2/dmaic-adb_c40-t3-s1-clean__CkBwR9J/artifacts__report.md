# Study status report

## Executive conclusion

The libraries pass sequencing QC: **0** failed, and **12** are usable. The usable replicate count is **6** in each arm, with a minimum of **6**. The library-quality prerequisite is therefore met.

The study cannot support the planned compound-versus-vehicle expression conclusion on the current design. There are **2** preparation batches, but the control libraries are all in one batch and the treated libraries are all in the other. Treatment is consequently perfectly confounded with preparation batch, so a treatment effect cannot be estimated separately from batch.

## What was found

The QC computation retained **12** of **12** libraries: **6** control and **6** treated. The design computation found `confounded = true` across **2** batches. This is the cause of the current stop, not a library-quality or replication shortfall.

## Gene calls and validation

The steward locked the gene-level count batch because the design-identifiability gate was not satisfied. Therefore no differential-expression analysis was run, no gene can be called as responding to the compound, and no candidate list can be issued. The qPCR validation batch was not reached, so validation concordance cannot be computed. The absence of a gene list is a design limitation rather than evidence that no genes respond.

## What changed and what it achieved

No experimental data were changed. The analysis applied the standing QC rules and then tested whether treatment was separable from preparation batch. That test achieved a clear release decision: retain the usable libraries for documentation, but stop inference before gene calling because the design is non-identifiable.

## Recommended next action and control

Repeat the library preparation and/or sequencing with treatment assignments represented in each relevant preparation batch, so treatment is estimable separately from batch. Preserve the QC checks, sample-sheet audit, and design-identifiability check as release gates before any gene-level model is run. After a balanced, identifiable design is available, rerun the planned batch-adjusted expression analysis, then seek independent qPCR validation before issuing any candidate list.

## Data limitation

There is no released gene-count dataset for this route: the steward refused release by locking it behind the unmet identifiability gate. Consequently, gene-level significance, fold changes, validation concordance, and gene-set enrichment are not computable from the data currently released.
