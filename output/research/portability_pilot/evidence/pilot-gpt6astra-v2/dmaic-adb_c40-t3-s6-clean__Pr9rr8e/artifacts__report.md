# Study disposition: withhold the candidate list

## Executive conclusion
The libraries retain adequate replication after quality filtering, but they cannot support the intended compound-versus-vehicle conclusion. Treatment and preparation batch are completely confounded among usable libraries. This is a design failure after quality filtering, not evidence that the compound has no effect. No responding genes can be identified defensibly, and no candidate list should be issued.

## What was computed
From the released per-library metrics, applying the facility's assigned-read and mapping-rate criteria excluded **4 of 12 libraries**. The retained data contain **4 controls and 4 treated libraries**, giving a minimum of **4 usable replicates per arm** and **8 usable libraries** overall. Replication therefore passes the facility's rule.

The sample sheet shows why replication alone is insufficient: the rejected controls are the controls in the batch otherwise occupied by retained treated libraries; the rejected treated libraries are the treated libraries in the batch otherwise occupied by retained controls. The controls fail assigned-read depth, whereas the treated libraries fail mapping rate.

I constructed an intercept-plus-batch-plus-treatment design matrix. Across the **2 retained batches**, **0 batches** contain usable libraries from both arms. The retained matrix has **3 columns but rank 2**; the intercept-plus-batch matrix also has **rank 2**. Adding treatment supplies no independent contrast. Before filtering, the corresponding matrix had **rank 3**. Thus QC removed the libraries that provided the cross-arm overlap.

## Scope of inference and unavailable analyses
The steward locked the gene-level count batch because the retained design is confounded. Independent qPCR validation and gene-set annotation were also locked by their upstream dependencies. These were **locked requests, not findings that the records do not exist**.

Consequently, differential expression, batch variance attribution, candidate validation concordance, and enrichment were not computed. There is no estimated number of responsive genes and no measured validation success rate. The conclusion stops at design feasibility. An unadjusted arm comparison would mix treatment and preparation effects; including batch cannot solve exact aliasing. Generic batch correction would not recover information that this retained design lacks.

## What changed and what it achieved
The analytical change was exclusion of libraries failing the predefined quality rules. This preserved adequate replicate counts but eliminated treatment–batch overlap. No physical remediation, new sequencing, or validation was performed, and no improvement in biological inference is claimed.

## Recommended next action and control plan
Withhold the list and flag the study as non-identifiable after QC. Investigate low assigned-read yield in the excluded control libraries and poor mapping in the excluded treated libraries. Assess whether existing material can be successfully recovered; additional sequencing alone should not be assumed to fix poor mapping. Reprepare or replace material where necessary.

Restore usable within-batch arm overlap, preferably through a balanced, randomized preparation plan with both arms represented in each batch. Retain the predefined QC criteria rather than reinstating failed libraries merely to make the model fit. After remediation, repeat QC and matrix-rank checks before any gene testing. Only then fit an appropriate count model including batch, apply the facility's multiple-testing and effect-size criteria, and require independent directional qPCR confirmation before release. Maintain a signed sample-disposition record, batch-by-arm table, rank check, and validation gate for future studies.

The computations are preserved in `analyze.py` and `design.py`, with results and routing decisions in `trace.json`.
