# Metabolic-trait candidate-panel study report

## Executive conclusion

The discovery plate passes the protocol re-genotyping gate. Discovery participant QC found **2 failed participants** and a sample failure fraction of **0.008333333333333333**; this is below the protocol's maximum allowed fraction of **0.1**. The plate therefore can carry the study forward for analysis, but this QC pass is not an association conclusion.

Variant QC retained **138 variants** and failed **12 variants**. The unadjusted discovery scan produced **37 significant variants** at the computed Bonferroni threshold, but its genomic-control value was **8.698851990266833**. This strong inflation means those unadjusted findings must not be reported as valid associations until population structure is assessed and, if appropriate, adjusted.

No ancestry markers, principal components, or leading ancestry axes were released. Therefore affected and unaffected participants cannot be shown to be comparable on the discovery cohort, and a structure-adjusted association analysis could not be computed. The conclusion stops at this point for a valid discovery association claim.

The replication release contained **0 nominated candidates** and consequently **0 replicated hits**. No candidate-level replication p-values or same-direction checks could be computed. The study currently has **0 reportable associations**.

## What was computed

- Discovery sample QC: **2** failed samples; failure fraction **0.008333333333333333**.
- Discovery variant QC: **12** failed variants; **138** retained variants.
- Unadjusted discovery association scan: **37** significant variants; lambdaGC **8.698851990266833**.
- Replication sample QC: **0** failed samples; failure fraction **0.0**.
- Replication association: **0** nominated candidates and **0** replicated hits; candidate-level replication testing was unavailable because no candidates were supplied.

## What caused the stop

The protocol requires ancestry structure to be assessed before variants are tested, but the released discovery batch contained no ancestry or leading-axis measurements. The inflated unadjusted scan cannot therefore be separated into genuine association and structure-driven signal using the available data. The replication batch also supplied no nominated discovery hits, so it cannot validate any discovery candidate.

## Recommended next actions

1. Obtain ancestry markers or leading principal axes for the discovery cohort and determine whether the affected and unaffected groups overlap or are separated.
2. If the groups overlap, include the leading structure axes as covariates and rerun the association analysis on the **138** retained variants. If the groups are separated, do not compare them on this cohort.
3. Nominate candidates only from that valid, structure-aware discovery analysis and request candidate-specific replication data.
4. Report a hit only after independent replication demonstrates a p-value below the protocol replication threshold and the same effect direction.
5. Preserve the QC script, thresholds, retained-variant manifest, structure assessment, and replication nomination list as the controlled analysis record.

Until these changes are made, the correct business decision is to hold the association report and not claim that the **37** unadjusted discovery findings are real.
