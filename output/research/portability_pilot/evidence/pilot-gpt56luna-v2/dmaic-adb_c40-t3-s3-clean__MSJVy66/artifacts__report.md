# Sequencing study status

## Executive conclusion

The libraries cannot yet carry a compound-versus-vehicle expression conclusion. The QC analysis found **8 usable libraries out of 12**. Control retained **6 usable libraries**, but treated retained only **2**, below the required minimum of **3 usable replicates per arm**. The replicate gate therefore failed, and the study must be re-sequenced before gene calling.

## What was computed

A library was counted as usable only when it met both QC rules: at least **5000000 assigned reads** and mapping rate at least **0.7**. The computation found **4 failed libraries**, all in the treated arm; control had **0 failures** and treated had **4 failures**. The usable counts were **6 control** and **2 treated**, giving a minimum usable-replicate count of **2**. The required minimum was **3**, so the gate result was false.

## Design and gene conclusions

The sample sheet was not released: the steward locked it at the `replicates_sufficient` gate because the computed minimum was **2**, not at least **3**. Consequently, preparation-batch identifiability was not computed. There is no released sample-sheet data for that analysis, and the conclusion stops there.

The gene-level read-count batch was not released because the sample sheet was unavailable. Therefore no adjusted-p-value or fold-change analysis was run, and no gene can be called from this run. The panel contains **400 genes**, but no candidate count is available.

The qPCR validation batch and gene-set annotation batch were also not released. Validation concordance and confirmed-candidate counts therefore cannot be computed, so no candidate list can be issued or validated from the current run.

## What should happen next

Re-sequence the failed/insufficient treated arm and re-run library QC. The release gate must first show at least **3 usable replicates in each arm**. Only after that gate passes should the sample sheet be reviewed for treatment-versus-preparation-batch identifiability, followed by batch-aware gene-level analysis and independent qPCR validation.

## Holding the change

The current decision is held by the measured QC gate: **2** minimum usable replicates versus the required **3**. The steward declaration recorded this computed value, and the downstream release remained locked. No design, differential-expression, validation, or enrichment result has been substituted for the unavailable data.
