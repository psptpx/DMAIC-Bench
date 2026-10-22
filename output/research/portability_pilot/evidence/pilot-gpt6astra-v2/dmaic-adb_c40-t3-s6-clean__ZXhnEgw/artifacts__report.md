# Compound-expression study: hold conclusions and candidate release

## Executive decision
The libraries retain adequate replication under the facility's rules, but **the intended compound-versus-vehicle comparison cannot be separated from preparation batch after quality filtering**. Do not issue a compound-responsive gene list from this study. This is an unidentifiable comparison, not evidence that the compound has no effect.

## What was computed
Using the steward's complete library metrics and the brief's joint read-depth and mapping criteria, I evaluated all 12 libraries. There were 4 exclusions: 2 for inadequate assigned reads and 2 for inadequate mapping. The retained set contains 4 controls and 4 treated libraries, so the minimum usable replication per arm is 4 and passes the facility's replication requirement.

I then joined the retained library identifiers to the sample sheet and evaluated the model consisting of an intercept, preparation-batch indicator, and treatment indicator. The retained design has 8 libraries across 2 batches:

| Preparation batch | Usable controls | Usable treated |
|---|---:|---:|
| First preparation batch | 4 | 0 |
| Second preparation batch | 0 | 4 |

The nuisance model has rank 2. Adding treatment leaves the rank at 2 despite 3 model columns: the treatment rank gain is 0. Thus batch and treatment are perfectly confounded among usable libraries.

The calculations, scalar outputs and branch decisions are in `trace.json`; `analyze.py` and `design.py` retain the computation code.

## Cause and scope of the conclusion
The original sample sheet contained cross-arm libraries within preparation batches, but those bridging libraries failed QC. The controls in the otherwise treated batch failed depth, and the treated libraries in the otherwise control batch failed mapping. Applying the required exclusions preserved replication but eliminated the overlap needed to distinguish the compound from preparation effects.

A treatment-only model would attribute any batch difference to the compound. A batch-adjusted model cannot recover a separately estimable treatment coefficient here. Batch correction cannot supply information absent from the design, and failed libraries should not be reinstated merely to restore model rank.

## Where the evidence stops
After the computed confounding verdict was declared, the steward **locked** the gene-count batch at the design-identifiability gate. This is not a declaration that the archived counts do not exist. The counts were not released; differential expression, fold changes, adjusted significance, batch expression-variance attribution and pathway enrichment were not computed.

The independent qPCR batch remains downstream of the unavailable count analysis and was not released or evaluated. Validation concordance is therefore unknown, not a failed or successful validation result. There is no defensible nominated compound-specific list to issue. The present conclusion stops at the design audit; no claim about which genes respond is supported.

## What changed and what it achieved
The only implemented change was analytical: excluding unusable libraries and enforcing the design gate before gene testing. This protected the facility from a potentially batch-driven candidate list. No experimental repair, re-sequencing or validation intervention has been performed, and no improvement in biological inference has been demonstrated.

## Recommended next action and how to hold the result
Withhold candidate release and discuss an experimental repair with the investigator and laboratory team. Investigate the depth failures separately from the mapping failures; additional sequencing might help a depth-limited library but is not an assumed cure for mapping problems. Determine whether failed bridge libraries can genuinely be recovered with documented QC. Otherwise prepare new, balanced libraries with both arms represented within preparation batches, randomizing processing order and retaining biological replication rather than substituting technical repeats.

Before reopening inference, rerun the joint library QC, arm-count check and retained-design rank audit. If the repaired design is estimable, fit a batch-adjusted expression model under the facility's prespecified calling rules, then assess independent qPCR direction and significance against the release criterion. Treat validation as a mandatory release gate, not a substitute for an identifiable primary experiment.

Maintain a versioned sample sheet, explicit exclusion reasons, batch-by-arm tables, analysis scripts and a signed release checklist. Recheck balance after exclusions, not just at study planning, and keep candidate release on hold until all gates have documented evidence.
