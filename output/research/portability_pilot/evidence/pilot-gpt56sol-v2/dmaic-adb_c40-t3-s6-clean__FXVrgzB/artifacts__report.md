# Study status report

## Executive conclusion

The libraries do not support the compound-versus-vehicle conclusion on the present design. Library QC left **8 usable libraries**, with **4 usable controls** and **4 usable treated libraries**. Replicate quantity therefore passed the facility rule. The decisive problem is design rather than sample count: every usable control is in one preparation batch and every usable treated library is in the other preparation batch. Treatment and preparation batch are therefore perfectly confounded.

No gene can be reported as responding to the compound from this study. This does **not** mean that no genes respond; it means the compound effect cannot be separated from the preparation-batch effect. The gene-count batch was locked at the identifiability gate, so no differential-expression model, adjusted significance result, fold-change call, or candidate count was computed.

Independent qPCR validation also cannot currently support issuing a list. There is no valid panel-derived candidate list to validate, and the qPCR batch remains locked behind the unavailable count analysis. A validation concordance was therefore not computed. The gene-set annotation is downstream of the same blocked route, so enrichment was not assessed.

## Library QC

Applying the brief's stated read-depth and mapping-rate rules produced **4 failed libraries** and **8 usable libraries**. Of the failures, **2** failed read depth and **2** failed mapping rate. The usable set retained **4** libraries in each arm, so the minimum usable replicate count was **4** and the study passed the replicate gate.

This means re-sequencing solely to increase the number of passing libraries is not the immediate analytical issue. The usable libraries are numerous enough under the standing rule, but their allocation across preparation batches is unusable for the intended contrast.

## Design assessment

The usable libraries span **2 preparation batches**, but their arm-by-batch allocation has empty cross-arm cells: the first batch contains all **4 usable controls** and no usable treated libraries, while the second contains all **4 usable treated libraries** and no usable controls. The required intercept, treatment, and batch design has **3 columns** but rank **2**. It is therefore rank deficient, and the treatment coefficient is not separately estimable from batch.

A simple treated-versus-control calculation that omitted batch would attribute the combined treatment-and-batch difference to treatment. That would violate the facility's analysis plan and cannot carry a biological conclusion.

## Candidate and validation status

There is no defensible responding-gene list at this point. The steward refused release of gene-level counts because the declared design was confounded. This was a locked precondition, not evidence that the count data are absent. No significant-gene count can be stated.

Likewise, validation cannot be judged. The qPCR records were not reachable after the count-analysis stop, and no concordance or confirmed-candidate count was computed. The facility should withhold a candidate list rather than reinterpret the unavailable downstream evidence.

## Corrective action and control plan

The facility should prepare replacement or additional libraries so that both treatment arms are represented within each preparation batch. The corrective design must break the present one-arm-per-batch structure; merely adding libraries while preserving that structure will not solve identifiability.

After replacement sequencing, the facility should:

- reapply the same predeclared library-usability rules;
- confirm that each arm still passes the usable-replicate rule;
- rebuild the treatment-plus-batch model matrix and verify full rank before accessing gene calls;
- fit the required batch-adjusted expression model only after that check;
- apply the brief's predeclared adjusted-significance and effect-size rules without modification;
- evaluate independent qPCR in the panel-called direction and issue a list only if the predeclared concordance rule passes; and
- retain the QC table and model-rank check as release controls so this confounding cannot pass silently in a rerun.

No analytical adjustment can recover a separately identifiable treatment effect from the current usable allocation. The required next step is a balanced, crossed preparation design followed by new sequencing and a fresh gated analysis.
