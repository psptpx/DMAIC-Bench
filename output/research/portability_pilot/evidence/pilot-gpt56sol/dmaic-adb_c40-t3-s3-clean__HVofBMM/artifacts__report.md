# Compound-response study: current disposition

## Executive conclusion

The libraries cannot currently support the planned biological conclusion. Of **12** sequenced libraries, **4** failed the standing usability rules, leaving **8** usable libraries. The imbalance is decisive: **6** usable controls remain but only **2** usable treated libraries remain. Thus the minimum arm replication is **2**, below the required **3**, and the replication gate fails.

The analysis therefore stops at library QC. The preparation-batch sample sheet was locked by that failed gate, so treatment-versus-batch identifiability could not be computed. The read-count matrix was then also locked. Consequently, the intended comparison cannot yet be shown estimable on this design, differential expression could not be run, and no responding genes can be reported.

## What is causing the stop

Library usability was computed using the facility's inclusive cutoffs of at least **5000000** assigned reads and mapping rate at least **0.7**. Among the failed libraries, **2** failed assigned-read depth and **2** failed mapping rate; **0** failed both criteria. All failures were in the treated arm, which reduced that arm to **2** usable replicates while control retained **6**.

This is a replication failure, not evidence that the compound has no effect. Absence of gene calls here means that gene-level testing was unavailable, not that a valid test found no response.

## Design and gene analysis status

The sample sheet containing preparation batch was not released because minimum arm replication was **2** rather than **3**. Accordingly, whether treatment and batch are confounded is unknown; batch count is also unknown. It would be inappropriate to guess either result.

The count matrix was not released because sample-sheet analysis is a prerequisite. No batch-adjusted model, fold changes, adjusted p-values, or significant-gene count could therefore be computed. The conclusion stops before gene calling.

## Required next action and control plan

Re-sequence or replace the **4** failed treated libraries, then rerun the same library QC. Do not unlock biological interpretation until each arm retains at least **3** usable libraries. Once that gate passes, release and inspect the sample sheet and verify that treatment is estimable separately from preparation batch. If more than one preparation batch is present, include batch in the expression model as required by the brief. Only after that design check should the count matrix be analyzed under the pre-specified gene-calling rules.

To hold the correction, retain the QC gate in the release workflow: record library-level pass/fail status, arm-level usable counts, and the minimum arm count before releasing design or expression data. This prevents a future under-replicated analysis from being interpreted as a compound result.
