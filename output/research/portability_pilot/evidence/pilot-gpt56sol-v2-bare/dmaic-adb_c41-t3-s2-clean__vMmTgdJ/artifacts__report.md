# Candidate-region association study report

## Executive conclusion

The plate can support an analysis. Participant QC failed **2** of **240** participants, a failure fraction of **0.008333333333333333**, below the plate trigger of **0.1**. After participant and variant QC, the analysis retained **238** participants and **139** variants.

Affected and unaffected participants should **not** be compared with an unadjusted scan on this discovery cohort. PC1 separated the groups (**p = 5.623047512871917e-18**), so the definitive discovery scan adjusted for **5** principal components. That stable score scan tested **139** retained variants at a Bonferroni threshold of **0.0003597122302158273** and found **1** association: **rs020008** (**p = 3.337330263864369e-05**, positive direction). Its converged adjusted effect fit estimated an odds ratio of **2.646297913481197** per coded-allele dosage.

Independent replication supports reporting rs020008. The replication test analyzed **119** participants with nonmissing calls and gave **p = 0.0003156987889761041**, odds ratio **2.729997715123794**, in the same positive direction. Thus **1** of **1** nominated candidates met the replication rule.

## Quality control and retained material

The participant call-rate requirement was **0.95**. **P017** and **P111** failed; each had call rate **0.9466666666666667**. They were excluded. All other participant IDs in the discovery batch were retained, comprising **118** affected and **120** unaffected participants.

Variant QC excluded **11** variants and retained all other panel variants. The exclusions and reasons were:

- Call rate: **rs020001, rs020016, rs020084, rs020114, rs020142**.
- Minor-allele frequency: **rs020037, rs020045, rs020054, rs020072**.
- Hardy-Weinberg equilibrium among unaffected participants: **rs020085, rs020117**.

The applied thresholds were call rate **0.95**, minor-allele frequency **0.01**, and unaffected-participant Hardy-Weinberg p-value **1e-06**. The corresponding exclusion counts were **5**, **4**, and **2**.

## Comparability and discovery analysis

PC1 separation was strong, with test statistic **-9.383072793420999** and **p = 5.623047512871917e-18** against the comparison alpha of **0.05**. Therefore, a raw affected-versus-unaffected genotype comparison would be confounded by cohort structure. The analysis changed to an additive logistic framework adjusted for the leading **5** principal components.

A preliminary likelihood-ratio scan identified the same sole hit, but **8** non-hit alternative fits did not meet the strict optimizer convergence check. To avoid basing the panel-wide conclusion on those fits, a stable adjusted score scan was run. Its null fit converged; genomic inflation was **0.7949917264150559**. The score scan confirmed only rs020008 above the multiple-testing threshold. The rs020008 alternative fit itself converged, so its odds-ratio estimate is usable.

## Replication

The independent cohort contained **120** participants, split into **60** affected and **60** unaffected participants. For rs020008, **1** call was missing, leaving **59** affected and **60** unaffected participants in the test. Its replication p-value was below **0.05** and its direction matched discovery, satisfying both protocol conditions.

## Recommendation and control plan

Report rs020008 as the study's replicated candidate-region association, with the explicit qualification that discovery required population-structure adjustment. Do not report the other retained variants as associated, and do not rehabilitate any QC-excluded participant or variant without re-genotyping or a documented protocol amendment.

For the next study phase, validate rs020008 with an orthogonal genotype assay, preserve blinded QC, and pre-specify ancestry or principal-component adjustment before analysis. Retain the participant call-rate, variant call-rate, minor-allele-frequency, unaffected-participant Hardy-Weinberg, Bonferroni, and directional replication checks as release gates. A larger and ancestry-matched cohort should be used to refine the effect estimate and determine whether the signal is causal or tags another regional variant.
