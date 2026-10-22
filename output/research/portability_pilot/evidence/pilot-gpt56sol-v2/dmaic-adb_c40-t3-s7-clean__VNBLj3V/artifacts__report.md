# Compound-response panel study: decision report

## Executive decision

The sequencing libraries can support analysis, and the intended treated-versus-control comparison is estimable. The panel analysis called **40 genes**, but independent qPCR confirmed only **0 of 10** nominated candidates, a concordance of **0.0**, below the required **0.75**. Under the facility rule, **do not issue the candidate list**. Reconcile the panel/qPCR discrepancy and repeat validation before release.

## Library readiness

Applying the prespecified usability rules (assigned reads at least **5000000** and mapping rate at least **0.7**) produced **0** failed libraries. **12** libraries remain: **6** control and **6** treated. The minimum retained arm count is **6**, above the required **3**. Re-sequencing is therefore not triggered by library QC.

## Design and comparison

The usable samples occupy **1** preparation batch containing both arms. The nuisance-only design rank was **1** and increased to **2** after adding treatment, so treatment is not confounded with preparation batch and the requested contrast is estimable. With only one observed batch, there is no separate batch effect to estimate.

## Panel result

I analyzed **400** genes across **12** usable libraries using median-ratio normalization, per-gene negative-binomial models, two-sided Wald tests, and Benjamini-Hochberg adjustment. Calls required adjusted p below **0.05** and absolute log2 fold change at least **1.0**. **40** genes met both rules:

G0002, G0005, G0019, G0038, G0045, G0055, G0060, G0062, G0100, G0108, G0112, G0125, G0153, G0156, G0165, G0169, G0173, G0210, G0214, G0215, G0237, G0239, G0241, G0244, G0247, G0263, G0265, G0267, G0271, G0284, G0314, G0327, G0333, G0339, G0341, G0366, G0370, G0372, G0379, G0387

The numerical optimizer reported non-success for **22** non-called genes and for **0** called genes. This limitation should be retained in the audit trail and the panel analysis should be reproduced in the facility's validated count-analysis pipeline before external use.

## Independent validation

For each nominated candidate, I compared the independent qPCR log2 relative-expression values between arms using a two-sided Welch test and checked whether the observed mean difference matched the panel direction. Significance required p below **0.05**. **6** candidates had the expected direction, but only **0** also met the significance rule. The confirmed candidate was none.

Because concordance was **0.0**, below **0.75**, the facility's release criterion fails. The gene-set annotation remained locked at this gate, so enrichment could not be computed; no pathway conclusion is available.

## What should happen next

- Withhold the candidate list; do not describe the panel calls as validated compound responses.
- Audit sample identity, assay direction, normalization, primer performance, and dynamic range for every nominated qPCR assay, prioritizing direction-discordant candidates.
- Reproduce the count analysis in the facility's validated RNA-seq software and investigate optimizer warnings among non-called genes.
- Repeat or redesign independent validation with prespecified assay QC and adequate precision. Recalculate directional concordance before requesting annotation or making pathway claims.
- Hold the result through the existing gates: library QC, arm replication, design identifiability, dual panel thresholds, and directional qPCR concordance. Release only after the validation gate passes.
