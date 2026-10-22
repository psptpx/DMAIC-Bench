# Compound-response study: decision report

## Executive decision

The current sequencing libraries cannot support a compound-response conclusion. Among the 12 libraries assessed, 4 failed the facility's joint read-depth and mapping-quality rule. The usable set therefore contains 8 libraries: 6 controls and 2 treated libraries. The minimum arm size is 2, below the required 3, so analysis stops at the replicate gate and the study must be re-sequenced before any gene is called.

No candidate list should be issued from the current data.

## What is causing the stop

The QC failures are confined to the treated arm. Of the 4 failed libraries, 2 failed the assigned-read requirement of 5000000 and 2 failed the mapping-rate requirement of 0.7. This attrition leaves only 2 usable treated replicates while all 6 control replicates remain usable.

The governing rule requires at least 3 usable replicates in every arm. The computed minimum is 2, so that prerequisite is not met.

## What can and cannot be concluded

**Library adequacy:** failed. The libraries cannot carry the requested biological conclusion in their current state.

**Design adequacy:** not computable. After the replicate failure was declared, the steward kept the sample sheet locked. Preparation-batch assignments were therefore unavailable, so whether treatment is estimable separately from preparation batch could not be assessed.

**Compound-responsive genes:** not computable. Gene-level counts remain downstream of the locked sample sheet. No differential-expression model was run, and no genes can honestly be called either responsive or non-responsive.

**Independent validation:** not computable. The validation batch remains downstream of the unavailable gene analysis. There is consequently no computed validation concordance and no basis for issuing a candidate list.

## Corrective action

Re-sequence or replace the 4 failed treated libraries, addressing read yield for the 2 depth failures and mapping quality for the 2 mapping failures. Do not substitute the current under-replicated comparison for the planned analysis.

After replacement data arrive, rerun library QC and hold progression until each arm retains at least 3 usable replicates. Then obtain the sample sheet, test treatment-versus-batch identifiability among usable libraries, and include preparation batch in the expression model if multiple batches remain. Only after those gates pass should gene-level differential expression be computed and nominated candidates sent through independent validation.

## How the decision will be held

The release remains on hold at the replicate gate. The hold is lifted only after repeat QC demonstrates a minimum usable arm size meeting the predefined requirement. Design assessment, gene calling, and validation must then be completed in sequence; until that happens, the facility should report the study as inconclusive rather than issue a candidate list.
