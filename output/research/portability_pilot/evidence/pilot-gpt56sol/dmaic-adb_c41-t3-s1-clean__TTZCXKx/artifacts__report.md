# Candidate-region case-control study status

## Executive conclusion

The plate itself can proceed through technical QC: **1** participant failed, the computed participant failure fraction was **0.0041666666666666666**, and re-genotyping was therefore **not** triggered. After participant QC, **239** participants remained: **120** affected and **119** unaffected. Variant QC retained **138** variants and excluded **12**.

The cohort cannot, however, carry a valid case-control association conclusion. In the mandatory structure check, affection status was completely separated on PC1: the PC1 range-overlap fraction was **0.0**, the Welch statistic was **-57.25323470457**, and its p-value was **3.349119478386524e-135**. The protocol says affected and unaffected participants drawn from separate ancestries cannot be compared. Association testing was therefore not run, and no variant can validly be declared associated or non-associated from this cohort.

## What was retained and changed

### Participants

Participant **P198** was excluded; its computed call rate was **0.9466666666666667**. All other participant IDs were retained. This left the **239**-participant cohort described above.

### Variants

The joint variant filters excluded **12** variants. Failures comprised **5** for call rate, **4** for minor-allele frequency, and **3** for exact Hardy-Weinberg testing among retained unaffected participants:

rs010047, rs010057, rs010063, rs010072, rs010088, rs010092, rs010101, rs010118, rs010128, rs010133, rs010141, rs010149

The following **138** variants passed all variant rules:

rs010001, rs010002, rs010003, rs010004, rs010005, rs010006, rs010007, rs010008, rs010009, rs010010, rs010011, rs010012, rs010013, rs010014, rs010015, rs010016, rs010017, rs010018, rs010019, rs010020, rs010021, rs010022, rs010023, rs010024, rs010025, rs010026, rs010027, rs010028, rs010029, rs010030, rs010031, rs010032, rs010033, rs010034, rs010035, rs010036, rs010037, rs010038, rs010039, rs010040, rs010041, rs010042, rs010043, rs010044, rs010045, rs010046, rs010048, rs010049, rs010050, rs010051, rs010052, rs010053, rs010054, rs010055, rs010056, rs010058, rs010059, rs010060, rs010061, rs010062, rs010064, rs010065, rs010066, rs010067, rs010068, rs010069, rs010070, rs010071, rs010073, rs010074, rs010075, rs010076, rs010077, rs010078, rs010079, rs010080, rs010081, rs010082, rs010083, rs010084, rs010085, rs010086, rs010087, rs010089, rs010090, rs010091, rs010093, rs010094, rs010095, rs010096, rs010097, rs010098, rs010099, rs010100, rs010102, rs010103, rs010104, rs010105, rs010106, rs010107, rs010108, rs010109, rs010110, rs010111, rs010112, rs010113, rs010114, rs010115, rs010116, rs010117, rs010119, rs010120, rs010121, rs010122, rs010123, rs010124, rs010125, rs010126, rs010127, rs010129, rs010130, rs010131, rs010132, rs010134, rs010135, rs010136, rs010137, rs010138, rs010139, rs010140, rs010142, rs010143, rs010144, rs010145, rs010146, rs010147, rs010148, rs010150

## Cohort comparability

PCA was computed from the **239** retained participants and **138** QC-retained variants after mean imputation and allele-frequency standardization. PC1 accounted for a variance fraction of **0.09941361305958872**. The complete absence of case/control score-range overlap, together with the PC1 group comparison above, indicates that affection status is confounded with the dominant genetic structure. This is the protocol's non-comparable branch, not the overlapping-structure branch where adding leading axes as covariates would be sufficient.

No ancestry labels, reference-panel assignments, or study-specific separation cutoff were supplied. A request for such a study fact was refused as unroutable. The observed complete PC1 range separation nevertheless directly meets the protocol's substantive prohibition on comparing separate ancestries.

## Association status

For the retained panel, the computed Bonferroni declaration threshold would be **0.0003623188405797101**. No variant-level association test was performed. Consequently, an association count, genomic-inflation estimate, effect estimates, and variant-level p-values could not be computed. The study currently supports technical-QC results only; it supports no genetic association claim.

## Recommended next action and control plan

1. Rebuild or augment recruitment so affected and unaffected participants overlap within ancestry strata; alternatively obtain enough participants in each ancestry to conduct valid within-ancestry case-control analyses.
2. Obtain and lock ancestry metadata or reference-panel assignments and a prespecified separation/axis-selection rule before reopening association testing.
3. Repeat participant QC, variant QC, and the structure assessment on the revised cohort. Association testing may resume only if affected and unaffected participants are comparable; use leading structure axes as covariates only when structure is present but overlapping.
4. Preserve the exclusion lists above and rerun them from raw calls after any re-genotyping or cohort change. Recompute the multiple-testing threshold from the newly retained variant count rather than carrying forward a threshold from this stopped analysis.
