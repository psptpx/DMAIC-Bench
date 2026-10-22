# Candidate-region association study report

## Executive conclusion

The plate can support an analysis: participant QC failed **0** participants, a failure fraction of **0.0**, and therefore did not trigger re-genotyping. Every participant supplied by the steward was retained; there are no excluded participant identifiers. The retained cohort contains **120** affected and **120** unaffected participants.

Variant QC retained **140** variants and excluded **10**. The affected and unaffected groups are comparable on the ancestry check: they were not separated, and the PC1 association with affection status had p-value **0.9020282133392976**. Consequently, the protocol route used an unadjusted additive trend test rather than ancestry-axis covariates.

Across **140** tested variants, **0** met the Bonferroni threshold of **0.00035714285714285714**. Thus, this panel provides no protocol-level association finding in this cohort. The genomic inflation factor was **0.8920987391435681**.

## Quality-control disposition

### Participants

Participant call rate was evaluated against **0.95**. The plate-level stop rule was a failed-participant fraction greater than **0.1**. The observed failed fraction was **0.0**, so all **240** supplied participant identifiers were retained and none were removed. This means the complete participant list in the steward's genotype batch is the retained set.

### Variants

A variant had to meet call rate **0.95**, minor-allele frequency **0.01**, and unaffected-participant exact HWE p-value **1e-06**. Failures comprised **5** by call rate, **3** by minor-allele frequency, and **2** by HWE.

Excluded variant identifiers: rs040038, rs040054, rs040057, rs040072, rs040104, rs040106, rs040110, rs040112, rs040113, rs040125.

Retained variant identifiers: rs040001, rs040002, rs040003, rs040004, rs040005, rs040006, rs040007, rs040008, rs040009, rs040010, rs040011, rs040012, rs040013, rs040014, rs040015, rs040016, rs040017, rs040018, rs040019, rs040020, rs040021, rs040022, rs040023, rs040024, rs040025, rs040026, rs040027, rs040028, rs040029, rs040030, rs040031, rs040032, rs040033, rs040034, rs040035, rs040036, rs040037, rs040039, rs040040, rs040041, rs040042, rs040043, rs040044, rs040045, rs040046, rs040047, rs040048, rs040049, rs040050, rs040051, rs040052, rs040053, rs040055, rs040056, rs040058, rs040059, rs040060, rs040061, rs040062, rs040063, rs040064, rs040065, rs040066, rs040067, rs040068, rs040069, rs040070, rs040071, rs040073, rs040074, rs040075, rs040076, rs040077, rs040078, rs040079, rs040080, rs040081, rs040082, rs040083, rs040084, rs040085, rs040086, rs040087, rs040088, rs040089, rs040090, rs040091, rs040092, rs040093, rs040094, rs040095, rs040096, rs040097, rs040098, rs040099, rs040100, rs040101, rs040102, rs040103, rs040105, rs040107, rs040108, rs040109, rs040111, rs040114, rs040115, rs040116, rs040117, rs040118, rs040119, rs040120, rs040121, rs040122, rs040123, rs040124, rs040126, rs040127, rs040128, rs040129, rs040130, rs040131, rs040132, rs040133, rs040134, rs040135, rs040136, rs040137, rs040138, rs040139, rs040140, rs040141, rs040142, rs040143, rs040144, rs040145, rs040146, rs040147, rs040148, rs040149, rs040150.

The same retained set is preserved in `variant_qc.json` under `retained_variants`.

## Cohort comparability

PCA used mean-imputed, variance-standardized genotypes after participant and variant QC. The first component explained a fraction **0.020937526414815125** of genotype variance. The affected PC1 range was **-3.8928531283317525** to **4.786812317511982**, while the unaffected range was **-4.56280316450207** to **3.8246537989541904**; these ranges overlap. Logistic testing of affection status against PC1 gave p-value **0.9020282133392976**. There is therefore no evidence here that the groups come from separate ancestries or that leading-axis adjustment is required by the protocol.

## Association analysis

Each retained variant was tested under an additive genotype model by logistic regression using nonmissing calls. Familywise alpha was **0.05**, divided over **140** retained variants to give the stated Bonferroni threshold. No variant crossed it, so no named variant can be declared associated.

## What changed and what it achieved

QC changed the tested panel from **150** supplied variants to **140** protocol-eligible variants while leaving the participant cohort unchanged. This removed low-call-rate, low-frequency, and HWE-failing variants before testing. The ancestry check then established that case-control comparison was permissible. The resulting multiplicity-controlled analysis produced no declared association.

## Recommended next actions and control plan

Do not present any variant from this run as associated. Preserve the genotype batch, protocol, `sample_qc.json`, `variant_qc.json`, `stratification.json`, `association.json`, and `trace.json` as the audit package. For a future cohort or re-run, lock the same QC thresholds, recompute HWE only among unaffected participants, repeat PCA before association testing, and calculate the Bonferroni cutoff from the variants that actually survive QC. Seek an independently collected, adequately powered cohort if investigators want to distinguish absence of evidence from a small effect; any follow-up must be treated as a new analysis rather than relabeling nominal signals from this panel.

## Computational note

An initial custom HWE implementation generated numerical warnings and its provisional output was discarded. Variant QC was rerun with a corrected exact-test recurrence; all final HWE p-values were checked as finite. The discarded attempt is recorded as failed in the trace and did not feed any downstream result.
