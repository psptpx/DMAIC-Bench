# Compound study: decision for the principal investigator

## Executive conclusion
The libraries are technically usable, but this study cannot support a compound-specific expression conclusion. Treatment assignment is completely confounded with preparation batch. This is a design limitation, not a sequencing-quality failure. No gene can responsibly be called responsive to the compound from this comparison; this does **not** mean that the compound has no effect.

## Library usability
Applying the facility's assigned-read and mapping-rate rules jointly to each library retained all **12** libraries, with **0** failures. Control and treated arms each retain **6** usable biological replicates; the minimum retained arm size is therefore **6**, passing the facility's replication requirement.

The smallest assigned-read total is **9,365,000** and the lowest mapping rate is **0.876**. Technical quality and retained replication therefore permit proceeding to design assessment, but do not by themselves establish a valid treatment contrast. These results are recorded in the `qc.sample_qc` outputs in `trace.json`.

## Why the intended comparison cannot be made
The sample sheet contains **2** preparation batches. The control-only batch contains **6** controls, and the treated-only batch contains **6** treated libraries. There are **0** batches containing both arms.

I constructed an intercept-plus-batch design and then added treatment. The batch-only matrix has rank **2**; the full matrix still has rank **2** despite having **3** columns. Treatment adds **0** independent dimensions. These computed results, including the batch-by-arm counts, are recorded in `design.identifiability`.

Thus, an observed arm difference would also be a batch difference. The data cannot distinguish compound biology from preparation effects. This does not establish that batch actually caused any expression change; it establishes that the possible causes cannot be separated. Omitting batch would attribute the combined difference to treatment, while including batch would leave a non-identifiable coefficient. Neither approach meets the facility's rules.

## Gene-level analysis and its limit
After the computed confounding verdict was declared, the steward **locked** the gene-level read counts because the design-identifiability prerequisite was not met. The counts were not released. This was not a denial asserting that the records do not exist.

Consequently, normalization, batch-variance estimation, treatment fold changes, gene-level tests, and multiplicity-adjusted significance were not computed. There is no computed significant-gene count or responder list. The conclusion stops at design eligibility. No expression analysis is represented as completed in the trace.

## What changed and what it achieved
No samples were removed, no libraries were re-prepared, and no experiment was changed during this analysis. The analytical decision changed from possible expression testing to withholding compound-specific claims once design confounding was verified. This prevented an uninterpretable batch-associated contrast from being reported as a drug response. No experimental improvement has yet been demonstrated.

## Recommended corrective action and how to hold the improvement
- Review the sample sheet against preparation records. Correct labels only if supported by source documentation, then repeat the eligibility assessment; do not relabel samples merely to satisfy the gate.
- If the sheet is correct, arrange a new preparation design that includes both arms within preparation batches, with balanced allocation and randomized processing order. Use independent biological replication and retain the facility's replication minimum after QC. If suitable source material remains, assess whether balanced re-preparation can rescue the experiment; otherwise repeat the biological experiment.
- Do not simply sequence these same libraries more deeply: extra reads cannot break the treatment–batch aliasing.
- Require a pre-preparation review of the arm-by-batch allocation and design-matrix estimability. Preserve sample identity, randomization, preparation batch, and processing records in an auditable manifest.
- On the corrected experiment, repeat library QC, confirm retained replication and estimability, and only then fit a batch-adjusted expression model and apply the brief's effect-size and adjusted-significance rules.
- Hold release of any responder list until those checks pass. Success must be demonstrated by the corrected manifest and new analysis, not assumed from this recommendation. Validate any resulting candidate response independently before making consequential biological claims.

The supplied scripts and saved steward batches support the computations; `trace.json` records the quantitative results and the stopping decision.
