# Compound-response targeted-panel study: decision report

## Executive decision

The sequencing libraries and experimental layout can support the planned treated-versus-control comparison, but the panel provides **no qualifying responsive genes**. The definitive analysis called **0** genes, with **0** upregulated and **0** downregulated. Therefore there is no candidate list to issue.

Independent validation cannot rescue or approve a list: the validation batch contains **0** nominated candidates and **0** confirmations. Its concordance is undefined because the denominator is zero. I did not replace that undefined quantity with an invented value, so the validation gate is not passed and the downstream gene-set annotation remained locked.

## What was measured

### Library usability

The QC computation evaluated **12** libraries. **0** failed. The control arm retained **6** usable libraries and the treated arm retained **6**, giving a minimum arm count of **6**. Thus the library set clears the pre-analysis replicate requirement.

### Design

There is **1** preparation batch. Both arms occur in that batch. The treatment design had rank **2** across **2** columns, and the computed confounding verdict was false. The treatment contrast is therefore estimable. Because only **1** batch exists, no separate batch coefficient is applicable.

## Expression result

A preliminary gene-wise dispersion fit was rejected as the decision model because it produced **3** failed fits and **4** nonconvergent fits. To obtain a complete panel result, I used median-of-ratios normalization and negative-binomial generalized linear models with a shared estimated dispersion of **0.061638700202367794**, followed by Benjamini-Hochberg adjustment.

The definitive analysis fit all **400** genes, with **0** failed fits and **0** nonconvergent fits. At adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**, it called **0** genes. The largest absolute fitted log2 fold change was only **0.8832830373496442**, so even the largest estimated response did not reach the required effect-size threshold.

## Validation and downstream interpretation

The qPCR release explicitly contains no nominees. With **0** candidates and **0** confirmations, a confirmation proportion cannot be computed. The facility's required concordance is **0.75**, using qPCR significance below **0.05** in the panel-called direction, but there are no candidate-level measurements to evaluate. This is an undefined validation result, not a failed proportion of zero and not a successful vacuous proportion.

Because no numeric validation concordance can be honestly declared, the gene-set annotation batch remained locked. Enrichment was therefore not computed. This does not alter the gene-level conclusion: there are no called genes to form a candidate set.

## Business conclusion and next action

The study is technically analyzable: library QC did not remove any samples, replication remained adequate, and treatment was not confounded with preparation batch. What prevents a biological candidate list is the panel result itself, not sequencing usability or design identifiability.

The facility should **withhold a compound-responsive candidate list** and record that no panel gene met the pre-specified joint criteria. No re-sequencing is indicated by the observed library QC. If the PI requires another attempt to detect a response, the next step should be a newly planned experiment that revisits exposure conditions and prospective power rather than relaxing thresholds after seeing these data. Any future candidates should be nominated under a pre-specified analysis and independently validated before release.

For control, retain the sample-level QC classifications, design-rank check, full differential-expression table, and empty validation record with this report. Apply the same pre-specified QC, effect-size, multiplicity, and validation gates to any repeat study.
