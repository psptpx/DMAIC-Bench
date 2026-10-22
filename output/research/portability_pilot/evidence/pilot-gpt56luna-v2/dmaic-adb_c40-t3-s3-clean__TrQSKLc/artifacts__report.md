# Study status report

## Executive conclusion

The library set cannot carry the planned expression conclusion yet. The QC computation found **8 usable libraries** and **4 failed libraries**. The control arm has **6 usable replicates**, but the treated arm has only **2 usable replicates**. The standing rule requires **3 usable replicates per arm** before any gene is called.

The steward therefore locked the sample sheet at the sufficient-replicates gate. The treatment-versus-control design cannot be assessed from the released data, and no gene-level result or validation result can honestly be issued.

## What was computed

Usability was evaluated using the brief's criteria of at least **5000000 assigned reads** and a mapping rate of at least **0.7**. The computation produced **4 failed samples** and a minimum usable replicate count of **2** across the arms.

The failure is concentrated in the treated arm: it has **2 usable replicates**, below the required **3**. The control arm has **6 usable replicates**.

## What was not computed

The sample sheet was not released because the steward rejected the declared minimum replicate count of **2** against the required minimum of **3**. Consequently, there is no released data for preparation-batch assignment or design assessment. The conclusion stops there: batch confounding/identifiability, gene-level differential expression, candidate nomination, qPCR concordance, and gene-set interpretation were not computed.

There is also no qPCR validation result available. It would be inappropriate to claim that any candidate is validated or to issue a candidate list.

## Recommended action and control plan

Resequence or otherwise replace failed treated libraries until the treated arm meets the required usable-replicate gate. Re-run library QC, then release and inspect the sample sheet for batch-aware design before requesting gene counts. Only after those gates pass should the planned differential-expression and independent qPCR validation analyses proceed.

The hold point should be maintained as a release control: no gene call and no candidate list until sufficient usable replicates are demonstrated and the subsequent design, expression, and validation computations are actually available.
