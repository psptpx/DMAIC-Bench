# Study status report

## Executive conclusion

The library QC supports retaining **8** of **12** libraries: **4** control and **4** treated. Each arm therefore has **4** usable replicates, exceeding the standing minimum of **3**. However, the intended compound-versus-vehicle comparison cannot be made on this design.

All **4** usable controls are in preparation batch L1, while all **4** usable treated libraries are in preparation batch L2. There are **2** preparation batches in the usable data, but each arm occupies only **1** batch. Treatment is consequently perfectly confounded with preparation batch, so a batch-adjusted expression model cannot distinguish compound response from batch effect.

## What was computed

Usability was assessed using the released rules: at least **5000000** assigned reads and mapping rate at least **0.7**. **4** libraries failed QC, leaving **8** usable libraries. The minimum usable arm size is **4**, and both arms meet the required minimum of **3**.

The design check used the usable sample sheet. The observed arm-by-batch structure was control/L1 = **4** and treated/L2 = **4**, with no usable cross-arm support within a batch. The design was therefore found confounded and not identifiable.

## What could not be concluded

The steward refused to release gene-level read counts because the design-identifiable gate requires a non-confounded design. Thus no gene-level differential-expression analysis was computed, no genes can be called, and no effect-size or adjusted-p-value result exists for this study. The conclusion stops at design assessment; a gene list must not be issued.

Because gene counts were not released, the independent qPCR validation batch and gene-set annotation were also not reached. No validation concordance was computed, so the validation requirement for issuing a candidate list cannot be assessed. This is a data/design gate, not evidence that the compound has or lacks a biological effect.

## Recommended change and control plan

Do not issue a candidate list from the current libraries. Re-run the experiment with usable libraries from both arms represented in each preparation batch, while preserving at least **3** usable replicates per arm after QC. Apply the same QC thresholds, include preparation batch in the expression model when there is more than **1** batch, and only proceed to gene calling after treatment is estimable separately from batch. Then perform the planned independent qPCR confirmation before releasing any candidates; the present run cannot establish that validation criterion.

The immediate hold point is the design: the current **8** usable libraries provide replication but not an identifiable treatment contrast. The proposed balanced redesign would remove the confounding that caused the counts gate to refuse release and would permit the downstream expression, annotation, and validation steps to be evaluated honestly.
