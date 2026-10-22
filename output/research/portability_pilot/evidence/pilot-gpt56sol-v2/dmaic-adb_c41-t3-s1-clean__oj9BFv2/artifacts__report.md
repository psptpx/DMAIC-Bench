# Candidate-region association study: current status

## Executive decision

The genotyping plate passes participant-level quality control, but this cohort cannot support a case-control association conclusion. Genotype PCA shows complete separation of affected and unaffected participants on PC1. The protocol expressly prohibits variant testing when the two groups come from separate ancestry structure. Consequently, no discovery association was tested, there are no valid discovery candidates, and replication cannot support reporting any variant.

## What was analyzed

The discovery batch contained **240 participants**—**120 affected** and **120 unaffected**—and **150 panel variants**. Missing genotype calls were treated as missing, not as a genotype category.

### Participant QC and plate disposition

Participant call rate was computed across the panel and compared with the protocol rule. **2 participants** failed: **P039, P197**. The computed participant failure fraction was **0.0083333333333333**. The plate therefore passes the protocol's re-genotyping gate and **238 participants** are retained: every participant from P001 through P240 except P039 and P197.

This means the plate itself does not need to be repeated merely for participant call-rate failure. It does not, however, cure the later cohort-comparability problem.

### Variant QC

Variant call rate, minor-allele frequency, and an exact Hardy–Weinberg test among retained unaffected participants were computed after participant filtering. **138 variants** were retained and **12 variants** were excluded. The excluded variants are:

rs010047, rs010057, rs010063, rs010072, rs010088, rs010092, rs010101, rs010118, rs010128, rs010133, rs010141, rs010149.

Thus, the retained set is every panel variant from rs010001 through rs010150 except those listed above. The computed Bonferroni discovery threshold over the retained set is **0.0003623188405797101**; it was not applied because the ancestry precondition failed. Among the individual QC checks, **5** variants failed call rate, **4** failed minor-allele frequency, and **3** failed control-only Hardy–Weinberg equilibrium. These criterion counts describe each check separately.

## Required ancestry precondition

PCA was run on the retained cohort and retained variants after mean imputation and variance standardization. PC1 explains a variance fraction of **0.0845841926985169**. Its affected-versus-unaffected Welch statistic is **-54.39945230423162**, with p-value **4.1188787428926535e-128**. Most importantly, the observed case and control PC1 score ranges have an overlap fraction of **0.0**.

This is separation, not merely overlapping structure that can safely be handled by adding principal components as covariates. A covariate adjustment cannot identify a disease effect when affection status and the ancestry axis have no common support. The protocol's precondition therefore fails, and affected and unaffected participants must not be compared in this cohort.

## Association and replication

No variant-level association scan was run because doing so would violate the protocol. Accordingly, no variant is declared associated; this is not evidence that the retained variants are unassociated, but rather that association is not estimable from this confounded cohort.

There are no valid discovery candidates to send to replication. The independent replication stage is therefore not applicable, and no variant meets the protocol's reporting rule. No discovery or replication p-value or odds ratio is claimed.

## Recommended next actions and control plan

- Preserve the participant and variant exclusion lists above as the reproducible QC record; the existing plate passed its technical participant-failure gate.
- Rebuild the comparison set so affected and unaffected participants have overlapping ancestry support—for example, recruit ancestry-matched controls and/or cases, or select a genuinely overlapping subset if one can be justified independently.
- Re-run participant QC, variant QC, and PCA on that redesigned cohort. Association testing may begin only after the PCA precondition demonstrates overlap; if residual overlapping structure remains, include its leading axes as covariates.
- Apply the protocol's multiplicity rule only to variants retained in the redesigned discovery analysis, nominate only valid discovery hits, and then test those in the independent cohort for concordant direction before reporting.
- Hold the study at the ancestry-comparability gate: do not release association claims until that gate and the subsequent replication requirement both pass.
