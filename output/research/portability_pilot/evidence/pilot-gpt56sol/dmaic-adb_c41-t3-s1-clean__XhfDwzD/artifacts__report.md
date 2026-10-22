# Candidate-region case-control study: current status

## Executive conclusion

The plate can proceed through technical quality control, but this cohort **cannot support a variant-association conclusion**. Sample QC failed **1** participant, a failure fraction of **0.00416666666667**, which is below the protocol maximum of **0.1**; therefore the plate does not require re-genotyping under the plate rule. After participant filtering, **239** participants remain: **120** affected and **119** unaffected. Variant QC retains **138** variants and excludes **12**.

The required ancestry check then stops the analysis. The leading genotype principal component explains **0.0994136130596** of standardized genotype variance. Affected PC1 scores range from **-5.85410883112** to **-1.74546404828**, while unaffected scores range from **0.387946287522** to **7.17312937944**. These ranges do not overlap. The affection-status logistic likelihood-ratio test for PC1 gives **p = 4.95741040488e-74** with statistic **331.320167287**. The protocol says separately ancestried groups cannot be compared; consequently no per-variant association test was run, and the number of associated variants is **not computable on this cohort**.

## What was computed

### Participant QC and plate disposition

The participant call-rate requirement was **0.95**. Observed participant call rates ranged from **0.946666666667** to **1**. The only excluded participant is **P198**. Every other participant in the supplied participant list is retained. The observed failed-sample fraction is below the plate stop limit, so participant QC permits the workflow to continue.

### Variant QC

QC was calculated after participant filtering. The applied requirements were variant call rate at least **0.95**, minor-allele frequency at least **0.01**, and exact Hardy-Weinberg p-value among unaffected participants at least **1e-06**.

Failures by criterion were: **5** for call rate, **4** for minor-allele frequency, and **3** for control-only Hardy-Weinberg equilibrium. These criterion counts describe checks and need not be added if a variant could fail more than one check.

Excluded variants: rs010047, rs010057, rs010063, rs010072, rs010088, rs010092, rs010101, rs010118, rs010128, rs010133, rs010141, rs010149.

Retained variants: rs010001, rs010002, rs010003, rs010004, rs010005, rs010006, rs010007, rs010008, rs010009, rs010010, rs010011, rs010012, rs010013, rs010014, rs010015, rs010016, rs010017, rs010018, rs010019, rs010020, rs010021, rs010022, rs010023, rs010024, rs010025, rs010026, rs010027, rs010028, rs010029, rs010030, rs010031, rs010032, rs010033, rs010034, rs010035, rs010036, rs010037, rs010038, rs010039, rs010040, rs010041, rs010042, rs010043, rs010044, rs010045, rs010046, rs010048, rs010049, rs010050, rs010051, rs010052, rs010053, rs010054, rs010055, rs010056, rs010058, rs010059, rs010060, rs010061, rs010062, rs010064, rs010065, rs010066, rs010067, rs010068, rs010069, rs010070, rs010071, rs010073, rs010074, rs010075, rs010076, rs010077, rs010078, rs010079, rs010080, rs010081, rs010082, rs010083, rs010084, rs010085, rs010086, rs010087, rs010089, rs010090, rs010091, rs010093, rs010094, rs010095, rs010096, rs010097, rs010098, rs010099, rs010100, rs010102, rs010103, rs010104, rs010105, rs010106, rs010107, rs010108, rs010109, rs010110, rs010111, rs010112, rs010113, rs010114, rs010115, rs010116, rs010117, rs010119, rs010120, rs010121, rs010122, rs010123, rs010124, rs010125, rs010126, rs010127, rs010129, rs010130, rs010131, rs010132, rs010134, rs010135, rs010136, rs010137, rs010138, rs010139, rs010140, rs010142, rs010143, rs010144, rs010145, rs010146, rs010147, rs010148, rs010150.

If the ancestry precondition had been satisfied, the computed Bonferroni threshold over the retained variants would have been **0.00036231884058**, based on familywise alpha **0.05**. It was not used because association testing was prohibited by the ancestry result.

## Business interpretation

Technical filtering changed the analysis set by removing the failed participant and failed variants. That achieved a protocol-compliant QC set, but it did not repair the study-design problem: affection status is perfectly aligned with the leading ancestry axis in the retained cohort. Covariate adjustment is appropriate for overlapping structure, not for groups with no overlap; here it cannot identify a within-ancestry affection contrast.

Accordingly:

- The plate itself passes the sample-failure rule; re-genotyping is not the indicated remedy.
- The listed participant and variant exclusions should be frozen as the QC record for this plate.
- No variant should be called associated or non-associated from these participants.
- The investigators should recruit or select affected and unaffected participants with overlapping ancestry, preferably matched within ancestry strata, and repeat the complete QC and ancestry check before testing variants.
- In a redesigned cohort with overlap, pre-specify leading ancestry axes as covariates where residual overlapping structure remains, then apply the recomputed Bonferroni threshold over that cohort's retained variants.
- Preserve the participant-call-rate, variant-call-rate, frequency, control-only equilibrium, and ancestry diagnostics as release gates so future analyses cannot bypass the same stop condition.

## Reproducibility

The machine-readable audit trail is in `trace.json`. Detailed computed tables are in `sample_qc.csv`, `variant_qc.csv`, and `pca_scores.csv`; the analysis code is in `analyze.py`.
