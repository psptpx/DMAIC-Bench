# Candidate-region case-control study: current disposition

## Executive conclusion

The plate can proceed through technical QC, but this cohort **cannot support a case-control association conclusion**. Participant QC excluded **P198**; the computed plate failure fraction was **0.0041666666666666666**, below the protocol re-genotyping limit of **0.10000000000000001**. Variant QC retained **138** variants and excluded **12**.

The mandatory ancestry check then found affected and unaffected participants separated on the leading genotype axis (`separated = true`). Their observed PC1 ranges do not overlap, and the phenotype comparison on PC1 gave **p = 3.3491194783865236e-135**. The protocol says separately ancestried groups cannot be compared. Therefore I did **not** run variant association tests, and no variant can honestly be called associated or non-associated in this cohort.

## What was computed

### Participant QC and plate disposition

Call rate was computed across **150** panel variants for each of **240** participants. The input comprised **120** affected and **120** unaffected participants. Using the inclusive participant threshold of **0.94999999999999996**:

- **1** participant failed: **P198**, call rate **0.94666666666666666**.
- The failure fraction was **0.0041666666666666666** against a maximum of **0.10000000000000001**.
- The plate therefore passes this gate; **239** participants remain: **120** affected and **119** unaffected.

No plate-wide re-genotyping is required by this rule. P198 must remain excluded from analyses unless new genotype calls cause that participant to pass the same prespecified rule.

### Variant QC

After participant QC, each variant was evaluated using call rate at least **0.95**, MAF at least **0.01**, and exact HWE p-value among unaffected participants at least **1e-6**. Of **150** variants, **138** passed and **12** failed. Failure counts were **5** for call rate, **4** for MAF, and **3** for unaffected-participant HWE; these categories do not overlap in this dataset.

Excluded variants by reason:

- Call rate: rs010047, rs010072, rs010088, rs010101, rs010118
- MAF: rs010057, rs010063, rs010141, rs010149
- Unaffected-participant HWE: rs010092, rs010128, rs010133

Retained variants:

rs010001, rs010002, rs010003, rs010004, rs010005, rs010006, rs010007, rs010008, rs010009, rs010010, rs010011, rs010012, rs010013, rs010014, rs010015, rs010016, rs010017, rs010018, rs010019, rs010020, rs010021, rs010022, rs010023, rs010024, rs010025, rs010026, rs010027, rs010028, rs010029, rs010030, rs010031, rs010032, rs010033, rs010034, rs010035, rs010036, rs010037, rs010038, rs010039, rs010040, rs010041, rs010042, rs010043, rs010044, rs010045, rs010046, rs010048, rs010049, rs010050, rs010051, rs010052, rs010053, rs010054, rs010055, rs010056, rs010058, rs010059, rs010060, rs010061, rs010062, rs010064, rs010065, rs010066, rs010067, rs010068, rs010069, rs010070, rs010071, rs010073, rs010074, rs010075, rs010076, rs010077, rs010078, rs010079, rs010080, rs010081, rs010082, rs010083, rs010084, rs010085, rs010086, rs010087, rs010089, rs010090, rs010091, rs010093, rs010094, rs010095, rs010096, rs010097, rs010098, rs010099, rs010100, rs010102, rs010103, rs010104, rs010105, rs010106, rs010107, rs010108, rs010109, rs010110, rs010111, rs010112, rs010113, rs010114, rs010115, rs010116, rs010117, rs010119, rs010120, rs010121, rs010122, rs010123, rs010124, rs010125, rs010126, rs010127, rs010129, rs010130, rs010131, rs010132, rs010134, rs010135, rs010136, rs010137, rs010138, rs010139, rs010140, rs010142, rs010143, rs010144, rs010145, rs010146, rs010147, rs010148, rs010150

If the ancestry precondition had passed, Bonferroni correction of familywise alpha **0.05** over **138** retained variants would have produced a per-variant threshold of **0.00036231884057971015**. This threshold was computed but was not used to declare associations because testing was stopped first.

### Ancestry precondition

PCA used the **138** QC-retained variants and **239** retained participants, with missing genotypes mean-imputed and variants allele-frequency standardized. PC1 explained a fraction **0.099413613059588721** of standardized genotype variance; PC2 explained **0.019529881006155079**. The affected PC1 range was **[-5.8541088311183413, -1.7454640482762065]**, while the unaffected range was **[0.38794628752205057, 7.1731293794370732]**. These observed ranges do not overlap. A Welch comparison of PC1 by affection status gave t = **-57.253234704569721** and p = **3.3491194783865236e-135**.

This is the protocol's prohibited separated-ancestry branch, not the overlapping-structure branch where leading PCs could simply enter a regression as covariates. Covariate adjustment cannot create case-control support where the ancestry distributions have no observed overlap.

## Where the conclusion stops

No association analysis was run. Consequently:

- there is no valid list of associated variants;
- there are no valid variant-level association p-values or effect estimates to report;
- the retained-variant list is a QC result, not an association result;
- the current data cannot answer whether any panel variant is associated with affection status independently of ancestry.

## Recommended next action and control plan

Recruit or select affected and unaffected participants with overlapping ancestry distributions, preferably using prospective ancestry matching while preserving the phenotype definition. Re-genotyping P198 is optional if retaining that participant matters, but it will not resolve the cohort-wide ancestry separation. Once a comparable cohort is available, rerun the frozen sequence: participant call-rate gate, plate disposition, variant call-rate/MAF/unaffected-HWE filters, ancestry assessment, and only then association testing. If the new cohort has structure but overlap, include the leading ancestry axes as covariates; if it remains separated, stop again. Apply the Bonferroni threshold calculated from the number of variants retained in that new run rather than carrying forward the present threshold.
