# Candidate-region case-control study status

## Bottom line
The discovery plate passes the participant-quality gate. The computed sample failure fraction was **0.004166666666666667**, below the protocol limit of **0.1**, so re-genotyping is not triggered. This is a QC conclusion only, not an association conclusion.

After participant QC, **239** of **240** participants remained: **120** affected and **119** unaffected. **1** participant failed the call-rate rule (P129, index **128**). Variant QC retained **137** of **150** variants and failed **13**.

## Cohort comparability and association
The ancestry check found strong separation on the second leading structure axis (PC2 p-value **1.5825823445808038**). The protocol therefore required leading structure axes as covariates rather than a structure-blind comparison. The covariate-adjusted scan used **2** structure covariates and produced **0** Bonferroni-significant associations at threshold **0.00036496350364963507**. No discovery association was nominated.

The unadjusted scan was not used for the conclusion because structure was present. Its computed genomic inflation estimate was **2.7589520149947964**, but it does not override the protocol-required adjusted analysis.

## Replication and reporting
The replication batch contained **0** nominated candidates. Consequently, no replication test could be run and no replication result exists. The protocol requires replication at p < **0.05** in the same direction before reporting. The conclusion therefore stops here: no variant is reportable as associated.

## What to do next
The analysis was changed from a structure-blind scan to a covariate-adjusted scan. That change left no adjusted discovery candidate for replication. Retain the QC exclusions, unaffected-control HWE rule, ancestry assessment, and covariate-adjusted analysis order in the analysis record. Before seeking a publishable association claim, resolve the ancestry structure/design issue and prespecify a valid comparable cohort, then conduct a new discovery scan followed by independent replication.

All reported quantities are recorded in `/workspace/trace.json`.
