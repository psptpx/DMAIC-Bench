# Study disposition: withhold the compound-response candidate list

## Executive conclusion
The libraries pass the facility's usability and replication rules, but the experiment cannot separate a compound effect from a preparation-batch effect. This is a design limitation, not a sequencing-quality failure. No defensible compound-response gene list can be issued from the released evidence. This does **not** establish that the compound has no effect.

## Library quality
Computed from the released per-library metrics using the brief's joint read-count and mapping-rate criteria:

- All **12** libraries are usable; **0** fail.
- Both control and treated arms retain **6** usable biological replicates, so the minimum retained arm size is **6** and the replication gate passes.
- The lowest assigned-read count is **9,365,000**, and the lowest mapping rate is **0.876**.

These results establish technical eligibility to proceed to design review, not the validity of a biological treatment conclusion.

## Why the intended comparison fails
The usable sample sheet contains **2** preparation batches. The first contains **6** control libraries and **0** treated libraries; the other contains **0** control libraries and **6** treated libraries. There are **0** mixed-arm batches.

I formed an intercept-and-batch design matrix and then added a treatment indicator. The batch-only matrix has rank **2**; the full matrix still has rank **2**, despite having **3** columns. The treatment indicator is therefore completely aliased with batch. There is no separately estimable treatment coefficient under the required batch-adjusted model.

The observed problem is complete confounding; the data do not establish whether any underlying expression differences would be biological, technical, or both. Omitting batch would relabel this combined difference as treatment. Adding batch, applying batch correction, or collecting more sequencing reads from these same libraries cannot resolve the aliasing.

## Where analysis stops
The computed confounding verdict was declared to the steward. The gene-count request was **locked** by the design-identifiability rule. It was not denied as nonexistent. Counts were not released, and differential expression was not run. Effect sizes, adjusted significance values, the number of responding genes, and the fraction of variation attributable to batch were not computed.

The independent qPCR results and panel annotations remain behind downstream gates and were not obtained. Validation concordance and gene-set enrichment were not computed. Consequently, independent validation cannot be claimed to support issuing a list. Even a directionally consistent validation result would need an identifiable underlying experimental contrast before being interpreted as evidence of a compound response.

## Action and control plan
**Immediate disposition:** keep the candidate list on hold. Preserve the usable libraries, metrics, sample sheet, scripts, and computed design evidence. No samples were removed, no laboratory process was changed, and no improvement experiment has been completed. The analytical change was to stop gene calling at the design gate; it prevents an unsupported compound claim rather than rescuing the experiment.

**Corrective action:** the study lead and core facility should plan an identifiable repeat or a justified bridging preparation using suitable retained biological material. Represent both treatment arms within preparation batches, randomize preparation and sequencing positions, and maintain biological replication. Merely resequencing the existing libraries is not a remedy for preparation confounding. Technical repeats must not be counted as new biological replicates.

**Release controls:** approve the batch-by-arm allocation and verify design-matrix estimability before preparation begins. After sequencing, recompute library usability and retained replication, verify sample provenance and the actual design, and fit the prespecified batch-adjusted expression model. Apply the brief's multiplicity and effect-size rules, then independently assess qPCR confirmation against the facility's validation gate. Release candidates only after all gates pass; otherwise keep the list withheld and investigate the failed stage. No achievement of these future controls is claimed here.

## Audit trail
`trace.json` records the computed QC and identifiability results. `analyze.py` and `design.py` reproduce those calculations from the steward's released JSON files. All numerical results above are present in the trace outputs. No outside study-lead clarification was needed to establish the observed design limitation.
