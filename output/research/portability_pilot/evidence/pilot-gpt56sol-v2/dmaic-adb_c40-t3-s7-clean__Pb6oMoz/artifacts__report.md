# Compound-response study report

## Executive conclusion

The sequencing libraries and experimental layout can support the intended treated-versus-control comparison. However, the independent validation did not support issuing the candidate list. The facility should therefore **withhold the list and reconsider the panel result**, rather than claim validated compound-responsive genes.

## Where the study stands

### Library usability

All **12** libraries were evaluated against the standing read-depth and mapping rules. **0** failed, leaving **6** usable control libraries and **6** usable treated libraries. The minimum retained replication was **6** per arm, so library QC does not force re-sequencing.

### Can the intended comparison be made?

Yes. The usable design contains **1** preparation batch, both arms occur in it, and the treatment design was full-rank with rank **2** across **2** columns. The computed confounding verdict was `false`. Thus treatment is estimable separately from preparation batch; with only one observed batch, no separate batch coefficient is needed.

### Panel response analysis

The primary reproducible analysis used median-ratio normalization, log-transformed normalized counts, Welch two-sample tests, and Benjamini-Hochberg adjustment, followed by the facility's joint adjusted-significance and effect-size rule. All **400** genes were tested. **40** met both calling criteria: **17** increased and **23** decreased.

Called genes (analytical panel result): G0002, G0005, G0019, G0038, G0045, G0055, G0060, G0062, G0100, G0108, G0112, G0125, G0153, G0156, G0165, G0169, G0173, G0210, G0214, G0215, G0237, G0239, G0241, G0244, G0247, G0263, G0265, G0267, G0271, G0284, G0314, G0327, G0333, G0339, G0341, G0366, G0370, G0372, G0379, G0387.

This is an analytical call set, not an issuable validated candidate list.

### Independent qPCR validation

The qPCR batch covered **10** nominated leading candidates. **0** met the required combination of statistical significance and matching panel direction, giving concordance **0.0**. The validation gate therefore failed. In accordance with the standing rule, the candidate list must be withheld regardless of the sequencing-panel calls.

### Gene-set interpretation

Gene-set annotation was not released because the validation gate failed, so enrichment could not be computed. No pathway or gene-set conclusion is available; the analysis stops at this gate rather than guessing.

## What changed and what it achieved

The initial gene-wise negative-binomial implementation produced **39** calls but had only **398** finite tests. A transparent normalized-log sensitivity analysis was therefore run; its call count was stable at **40** across the tested normalization and variance variants, and that fully testable workflow was used as primary. This resolved the computational instability but did not change the business outcome: validation still failed.

## Recommended next actions and hold plan

1. Keep the candidate list on hold; do not communicate the analytical calls as independently confirmed biomarkers.
2. Review qPCR assay performance, primer specificity, normalization, and the biological material used for validation; repeat validation only after resolving those issues.
3. Reconcile the nomination policy explicitly: qPCR covered the leading subset rather than every analytical call, so future analysis plans should state how nominees are selected before testing begins.
4. Preserve the current QC and design checks as release gates. Any repeat should again require usable replication and an estimable treatment contrast before gene testing.
5. Release gene-set interpretation only after the validation concordance gate passes; until then, no enrichment claim should be made.
