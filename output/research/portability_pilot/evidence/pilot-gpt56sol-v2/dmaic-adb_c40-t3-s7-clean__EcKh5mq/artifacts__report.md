# Compound-response panel study: decision report

## Executive conclusion

The sequencing libraries and experimental layout can support the planned treated-versus-control comparison. All **12** libraries were usable, **0** failed QC, and each arm retained **6** usable biological replicates. The design used **1** preparation batch containing both study arms, so treatment was not confounded with preparation batch.

The primary count analysis identified **39** genes meeting both the adjusted-p-value threshold of **0.05** and the absolute log2-fold-change threshold of **1.0**. Of these, **17** increased and **22** decreased. However, independent qPCR confirmed **0** of **10** nominated leading candidates, for concordance **0.0**, below the required **0.75**. Under the facility rule, the candidate list must therefore be **withheld**. The sequencing result is a panel finding to reconsider, not a validated list to issue.

## Library readiness

Usability was evaluated from assigned reads and mapping rate using the brief's inclusive cutoffs. The lowest observed assigned-read count was **9235000**, and the lowest observed mapping rate was **0.865**. Consequently, all **12** libraries passed. Control retained **6** usable libraries and treated retained **6**; the minimum retained arm count was **6**, so re-sequencing is not required on the stated QC rule.

## Design and comparison

Among usable libraries there were **2** conditions in **1** preparation batch. That batch contained **6** control and **6** treated libraries. Therefore treatment is estimable. Because batch is constant across every library, no separate batch coefficient was fitted; it would duplicate the intercept rather than remove confounding.

## Panel response

Counts were normalized by median ratios and analyzed using gene-wise negative-binomial regression with a treated indicator. Benjamini–Hochberg adjustment and both prespecified call thresholds were then applied. Finite tests were obtained for **398** genes; **2** low-count genes could not be assigned finite model p-values. The **39** primary response genes were:

G0108, G0327, G0055, G0339, G0284, G0153, G0265, G0387, G0370, G0244, G0267, G0372, G0156, G0366, G0062, G0215, G0045, G0341, G0314, G0038, G0214, G0125, G0112, G0333, G0379, G0241, G0239, G0271, G0173, G0100, G0165, G0169, G0005, G0002, G0060, G0247, G0237, G0210, G0263

A transformed-count sensitivity analysis tested all **400** genes and called **40**. It reproduced all **39** primary calls and additionally called only G0019, one of the count-model failures. G0019 is therefore not included in the primary list and should be treated cautiously. All **10** qPCR nominees were called by both implementations, so this low-count uncertainty does not change the validation decision.

## Independent validation and release decision

For each nominee, independent treated and control qPCR measurements were compared with a two-sided Welch test. Confirmation required a p-value below **0.05** and an effect in the panel-called direction. The result was **0** confirmed candidates and concordance **0.0**. This does not meet the release requirement of **0.75**. The steward consequently kept gene-set annotation locked, so enrichment could not be computed and no enrichment claim is made.

## What changed, what it achieved, and next action

QC filtering was applied before inference but removed **0** libraries; its benefit was to document that sequencing quality and replication are not the cause of the stopped conclusion. Design checking established that the intended comparison is estimable. Normalization and multiplicity correction produced a statistical panel response, and the alternate analysis reproduced all **39** primary calls. Independent validation then failed the mandatory release gate.

Do not issue the candidate list. First audit qPCR assay identity, primer performance, normalization, plate layout, and sample provenance; then repeat independent validation under a documented protocol. Revisit panel normalization and the low-count G0019 result while investigating the panel–qPCR discrepancy. Hold future release with the same automated gates: library usability, retained replication, design estimability, joint effect/significance calling, and validation concordance. Gene-set enrichment should remain deferred until validation passes.
