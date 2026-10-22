# Compound-expression study: decision report

## Executive decision

The libraries can carry the planned comparison. No library failed the facility usability rules, and the minimum usable replication is **6 per arm**, versus the required **3**. The treated-versus-control contrast is identifiable: **1** preparation batch contains both conditions, so treatment is not confounded with preparation batch.

The prespecified count analysis calls **40 genes** at adjusted p below **0.05** and absolute log2 fold change at least **1.0**. Independent qPCR confirms **10 of 10** nominated candidates in the called direction, for concordance **1.0**, exceeding the required **0.75**. On the facility rule, validation therefore supports issuing the panel-derived list. This support applies directly to the nominated subset; it is not direct qPCR evidence for every other called gene.

## Library readiness and design

QC evaluated **12** libraries against at least **5000000** assigned reads and mapping rate at least **0.7**. Failed libraries: **0**. Usable control libraries: **6**; usable treated libraries: **6**. Thus the study clears the minimum-replication gate.

The sheet contains **1** preparation batch and **2** conditions. Because both conditions occur in that batch, the intended treatment contrast can be estimated without treatment-batch aliasing. However, the study cannot estimate a separate preparation-batch effect or demonstrate portability across batches.

## Differential expression

I fit per-gene negative-binomial likelihood-ratio models with treatment as the predictor, positive-count median-ratio library normalization, and BH adjustment across **400** tested genes. All repaired fits completed; fit failures: **0**. The result contains **24 up-regulated** and **16 down-regulated** genes.

The first implementation used ordinary geometric means despite zero counts. It produced **400** fit failures and was rejected. Replacing that normalization with the positive-count variant changed the computation from unusable to fully converged. A separate log-normalized Welch sensitivity analysis called **38 genes** under the same joint cutoffs, broadly supporting but not defining the primary list.

**Up-regulated:** G0287, G0279, G0277, G0131, G0194, G0331, G0061, G0101, G0110, G0310, G0107, G0260, G0037, G0006, G0153, G0212, G0010, G0118, G0293, G0039, G0374, G0007, G0383, G0185.

**Down-regulated:** G0115, G0124, G0247, G0314, G0299, G0276, G0154, G0187, G0052, G0114, G0280, G0155, G0372, G0311, G0394, G0149.

## Independent validation

For each nominated candidate I compared independent qPCR values between arms with a two-sided Welch test and required p below **0.05** plus agreement with the panel-called direction. Confirmed candidates: **10**; candidates tested: **10**; concordance: **1.0**. The release criterion was **0.75**, so validation passed.

## Gene-set interpretation

Over-representation testing used the **400**-gene panel as the universe, the **40**-gene call list as the query, and BH correction across **12** annotated sets. **1** set was significant. SET03 contained **20** called genes among **30** annotated members, with adjusted p **1.05966135039412e-14**.

## What the facility should do next

Issue the called list with the method, joint cutoffs, and qPCR scope stated above. Preserve the count matrix, sample sheet, complete per-gene result table, qPCR calculations, and normalization repair in the release package so the decision is auditable.

For follow-up, validate additional called genes rather than implying that nominated-candidate concordance directly confirms the entire list. Repeat the experiment with both arms represented in additional independent preparation batches; this retains identifiability while allowing a batch effect and cross-batch reproducibility to be assessed. Pre-register the same QC, calling, and validation gates, and monitor future runs against them.
