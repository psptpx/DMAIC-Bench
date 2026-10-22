# Compound-response panel study: decision report

## Executive decision

The sequencing libraries are adequate to carry an analysis, and the intended treated-versus-control comparison is identifiable. The sequencing screen produced **40 provisional calls** among **400 panel genes**. However, independent qPCR confirmed **0 of 10 nominated candidates**, for concordance **0.0**, below the facility requirement of **0.75**. The validation therefore does **not** support issuing the sequencing-derived list as a compound-response conclusion.

## What was measured and established

### Library fitness

I applied the standing usability rules of at least **5000000** assigned reads and mapping rate at least **0.7** to all **12** libraries. **0** failed. The minimum usable arm size is **6**, against the required minimum of **3**. Thus library QC and replication do not block the comparison.

### Design fitness

The sample sheet contains **1** preparation batch. Because that batch is constant across both arms, it cannot be separated as an additional effect but also is not aligned with only one arm. The nonredundant condition design has rank **2** across **2** columns, so treatment is not confounded and the planned comparison can be made. This conclusion applies to the observed preparation-batch field; it does not eliminate unrecorded technical effects.

## Sequencing result

I normalized counts by median-of-ratios size factors, tested treated against control with gene-wise two-sided Welch tests on log-transformed normalized counts, and applied Benjamini–Hochberg adjustment across all **400** genes. Calls required adjusted p below **0.05** and absolute log2 fold change at least **1.0**.

The **40** provisional sequencing calls are:

G0002, G0005, G0019, G0038, G0045, G0055, G0060, G0062, G0100, G0108, G0112, G0125, G0153, G0156, G0165, G0169, G0173, G0210, G0214, G0215, G0237, G0239, G0241, G0244, G0247, G0263, G0265, G0267, G0271, G0284, G0314, G0327, G0333, G0339, G0341, G0366, G0370, G0372, G0379, G0387.

These are screening calls, not an issuable validated response list. No specialist count-model package was available, and the archive did not specify a count-model implementation; the exact reproducible method used here is recorded in the trace. A future confirmatory reanalysis should predefine and use a dedicated negative-binomial count model.

## Independent validation and release gate

For each of the **10** nominated candidates, I compared the qPCR log2-relative-expression values between arms using a two-sided Welch test. Confirmation required p below **0.05** and an effect in the panel-called direction. The result was **0** confirmed candidates and concordance **0.0**. This misses the required concordance of **0.75**, so the facility should not issue the provisional gene list as evidence of compound response.

Because validation failed that gate, the steward kept the gene-set annotation locked. There is no released annotation available for this route, and enrichment was not computed. The biological interpretation therefore stops at the unvalidated sequencing screen; no pathway claim can be made.

## Business status and next action

**Where the study stands:** acquisition quality and replication are sufficient, and the design supports the intended comparison. The blocking issue is cross-platform reproducibility, not library QC or treatment-batch confounding.

**What changed and what it achieved:** the raw archive was converted into explicit QC, design, sequencing-call, and validation decisions. This narrowed the problem from general data quality to failed independent confirmation. It did not rescue or validate the response list.

**Recommended next steps:**

- Do not release the provisional genes as confirmed compound responders.
- Investigate qPCR assay identity, primer specificity and efficiency, normalization controls, sample correspondence, and plate/run effects before collecting more data.
- Re-run qPCR with a documented analysis plan and adequate biological replication; include positive and negative controls and retain blinded sample identifiers through analysis.
- Re-run sequencing inference with a prespecified dedicated count model and compare sensitivity of the provisional list before renominating candidates.
- Release and test the gene-set annotation only if the repeated validation reaches the standing concordance gate.

**How the decision will be held:** retain the existing library thresholds, minimum-replication gate, dual sequencing call rule, and directional qPCR gate as release controls. Archive scripts, software versions, sample mapping, raw qPCR values, and the candidate-nomination rule so the next review is reproducible and cannot bypass the failed validation gate.
