# Candidate-region case-control study: current decision report

## Executive decision

The plate is usable after participant QC: the failed-participant fraction was **0.008333333333333333**, and the computed plate re-genotyping decision was **false**. However, this cohort cannot carry a genetic-association conclusion. Genotype PC **1** separates affected from unaffected participants (p = **3.654069761192594e-129**), the two PC-derived clusters are completely confounded with phenotype (**true**), and the unadjusted scan has genomic inflation **4.746259205035554**. Consequently, no variant is declared associated and there is no valid discovery candidate to replicate.

## What passed quality control

### Participants

The analysis began with **240** participants and **150** panel variants. **2** participants failed participant call-rate QC:

- P039: call rate **0.9466666666666667**
- P197: call rate **0.94**

The minimum observed participant call rate was **0.94**. Both failed participants were removed. The resulting failure fraction was **0.008333333333333333**, so the computed plate re-genotyping flag was **false**.

### Variants

After participant removal, **12** variants failed and **138** were retained. Failed variants and causes were: rs010047 (call_rate), rs010057 (maf), rs010063 (maf), rs010072 (call_rate), rs010088 (call_rate), rs010092 (hwe), rs010101 (call_rate), rs010118 (call_rate), rs010128 (hwe), rs010133 (hwe), rs010141 (maf), rs010149 (maf).

Retained variants were: rs010001, rs010002, rs010003, rs010004, rs010005, rs010006, rs010007, rs010008, rs010009, rs010010, rs010011, rs010012, rs010013, rs010014, rs010015, rs010016, rs010017, rs010018, rs010019, rs010020, rs010021, rs010022, rs010023, rs010024, rs010025, rs010026, rs010027, rs010028, rs010029, rs010030, rs010031, rs010032, rs010033, rs010034, rs010035, rs010036, rs010037, rs010038, rs010039, rs010040, rs010041, rs010042, rs010043, rs010044, rs010045, rs010046, rs010048, rs010049, rs010050, rs010051, rs010052, rs010053, rs010054, rs010055, rs010056, rs010058, rs010059, rs010060, rs010061, rs010062, rs010064, rs010065, rs010066, rs010067, rs010068, rs010069, rs010070, rs010071, rs010073, rs010074, rs010075, rs010076, rs010077, rs010078, rs010079, rs010080, rs010081, rs010082, rs010083, rs010084, rs010085, rs010086, rs010087, rs010089, rs010090, rs010091, rs010093, rs010094, rs010095, rs010096, rs010097, rs010098, rs010099, rs010100, rs010102, rs010103, rs010104, rs010105, rs010106, rs010107, rs010108, rs010109, rs010110, rs010111, rs010112, rs010113, rs010114, rs010115, rs010116, rs010117, rs010119, rs010120, rs010121, rs010122, rs010123, rs010124, rs010125, rs010126, rs010127, rs010129, rs010130, rs010131, rs010132, rs010134, rs010135, rs010136, rs010137, rs010138, rs010139, rs010140, rs010142, rs010143, rs010144, rs010145, rs010146, rs010147, rs010148, rs010150.

## Can affected and unaffected participants be compared?

No. PC **1** had a case-control t statistic of **-55.09290296396201** and p = **3.654069761192594e-129**. Clustering on that axis yielded one cluster with **0** unaffected and **119** affected participants, and the other with **119** unaffected and **0** affected participants. The PC-range-overlap result was **false**. Thus phenotype and genetic background are completely confounded; adding the same PC as a covariate cannot identify a within-background affection effect when there is no within-background case-control contrast.

## Discovery scan

For transparency, an additive trend screen was computed after QC. Its retained-variant Bonferroni threshold was **0.00036231884057971015**, and **38** variants crossed it. These are not reportable associations: genomic inflation was **4.746259205035554**, and the complete phenotype-PC confounding shows that the screen is measuring population structure rather than an identifiable disease effect. Accordingly, none of those screen results was nominated as a discovery hit.

## Replication

The independent replication batch contained **120** participants but supplied **0** nominated candidates and **0** replicated candidates. With no valid discovery candidate or discovery direction, replication cannot support a reportable association and must not be used to select a result post hoc.

## Action and control plan

- Do not report a variant association from this discovery plate.
- Rebuild or augment discovery sampling so affected and unaffected participants overlap within genetic-ancestry strata; matching or stratified recruitment is required before another association scan.
- Re-run the same participant and variant QC pipeline, verify phenotype overlap within ancestry clusters before association testing, and stop again if identifiability fails.
- Pre-nominate only QC-passing, identifiable discovery hits under the retained-variant multiplicity rule; then test exactly those variants in the independent cohort with the prespecified directional rule.
- Preserve the participant exclusions, variant exclusions, PCA diagnostic, inflation diagnostic, and nomination list as the audit controls for the next analysis.
