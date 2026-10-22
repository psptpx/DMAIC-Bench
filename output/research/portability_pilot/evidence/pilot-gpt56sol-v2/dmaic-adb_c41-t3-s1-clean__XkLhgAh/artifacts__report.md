# Candidate-region case-control study: current status

## Executive decision

The genotyping plate passes the protocol's participant-level technical gate, but this cohort **cannot carry a case-control association conclusion**. After quality control, affected and unaffected participants are completely separated on the leading ancestry axis. The protocol explicitly prohibits comparing groups drawn from separate ancestries. Accordingly, no variant association test was run, no discovery association can be declared, and there is no valid candidate to take into replication or report.

## What was computed

### Participant quality control

Call rate was computed across the panel for every participant. The result was **2 failed**, a failure fraction of **0.008333333333333333**, and **238 retained**. The retained cohort contains **119 affected** and **119 unaffected** participants. This passes the plate-level technical rule, so wholesale re-genotyping is not triggered.

Excluded participants:

- `P039` — call rate **0.9466666666666667**
- `P197` — call rate **0.94**

Retained participants:

P001, P002, P003, P004, P005, P006, P007, P008, P009, P010, P011, P012, P013, P014, P015, P016, P017, P018, P019, P020, P021, P022, P023, P024, P025, P026, P027, P028, P029, P030, P031, P032, P033, P034, P035, P036, P037, P038, P040, P041, P042, P043, P044, P045, P046, P047, P048, P049, P050, P051, P052, P053, P054, P055, P056, P057, P058, P059, P060, P061, P062, P063, P064, P065, P066, P067, P068, P069, P070, P071, P072, P073, P074, P075, P076, P077, P078, P079, P080, P081, P082, P083, P084, P085, P086, P087, P088, P089, P090, P091, P092, P093, P094, P095, P096, P097, P098, P099, P100, P101, P102, P103, P104, P105, P106, P107, P108, P109, P110, P111, P112, P113, P114, P115, P116, P117, P118, P119, P120, P121, P122, P123, P124, P125, P126, P127, P128, P129, P130, P131, P132, P133, P134, P135, P136, P137, P138, P139, P140, P141, P142, P143, P144, P145, P146, P147, P148, P149, P150, P151, P152, P153, P154, P155, P156, P157, P158, P159, P160, P161, P162, P163, P164, P165, P166, P167, P168, P169, P170, P171, P172, P173, P174, P175, P176, P177, P178, P179, P180, P181, P182, P183, P184, P185, P186, P187, P188, P189, P190, P191, P192, P193, P194, P195, P196, P198, P199, P200, P201, P202, P203, P204, P205, P206, P207, P208, P209, P210, P211, P212, P213, P214, P215, P216, P217, P218, P219, P220, P221, P222, P223, P224, P225, P226, P227, P228, P229, P230, P231, P232, P233, P234, P235, P236, P237, P238, P239, P240

### Variant quality control

Among retained participants, variant call rate and minor-allele frequency were computed, and exact Hardy-Weinberg tests were computed among unaffected participants. **12 variants failed** and **138 variants were retained**. Failure-rule counts were **5 for call rate**, **4 for minor-allele frequency**, and **3 for control-only Hardy-Weinberg equilibrium**. These reason counts are mutually exclusive in this dataset.

Excluded variants and causes:

- `rs010047` — call rate
- `rs010057` — minor-allele frequency
- `rs010063` — minor-allele frequency
- `rs010072` — call rate
- `rs010088` — call rate
- `rs010092` — control-only Hardy-Weinberg equilibrium
- `rs010101` — call rate
- `rs010118` — call rate
- `rs010128` — control-only Hardy-Weinberg equilibrium
- `rs010133` — control-only Hardy-Weinberg equilibrium
- `rs010141` — minor-allele frequency
- `rs010149` — minor-allele frequency

Retained variants:

rs010001, rs010002, rs010003, rs010004, rs010005, rs010006, rs010007, rs010008, rs010009, rs010010, rs010011, rs010012, rs010013, rs010014, rs010015, rs010016, rs010017, rs010018, rs010019, rs010020, rs010021, rs010022, rs010023, rs010024, rs010025, rs010026, rs010027, rs010028, rs010029, rs010030, rs010031, rs010032, rs010033, rs010034, rs010035, rs010036, rs010037, rs010038, rs010039, rs010040, rs010041, rs010042, rs010043, rs010044, rs010045, rs010046, rs010048, rs010049, rs010050, rs010051, rs010052, rs010053, rs010054, rs010055, rs010056, rs010058, rs010059, rs010060, rs010061, rs010062, rs010064, rs010065, rs010066, rs010067, rs010068, rs010069, rs010070, rs010071, rs010073, rs010074, rs010075, rs010076, rs010077, rs010078, rs010079, rs010080, rs010081, rs010082, rs010083, rs010084, rs010085, rs010086, rs010087, rs010089, rs010090, rs010091, rs010093, rs010094, rs010095, rs010096, rs010097, rs010098, rs010099, rs010100, rs010102, rs010103, rs010104, rs010105, rs010106, rs010107, rs010108, rs010109, rs010110, rs010111, rs010112, rs010113, rs010114, rs010115, rs010116, rs010117, rs010119, rs010120, rs010121, rs010122, rs010123, rs010124, rs010125, rs010126, rs010127, rs010129, rs010130, rs010131, rs010132, rs010134, rs010135, rs010136, rs010137, rs010138, rs010139, rs010140, rs010142, rs010143, rs010144, rs010145, rs010146, rs010147, rs010148, rs010150

Had the ancestry precondition passed, the computed Bonferroni discovery threshold over the retained variants would have been **0.00036231884057971015**. It was not used because association testing was stopped first.

### Cohort comparability

PCA was run on the QC-retained, mean-imputed, allele-frequency-standardized genotype matrix. **PC1** explained a variance fraction of **0.09427730354730539**. Its affected-participant range was **-5.899208337332883 to -1.484927464351246**, while its unaffected-participant range was **0.30468856316516874 to 6.737616767616936**. The ranges did not overlap. The absolute standardized case-control difference was **7.14228496850765**, with a Welch-test p-value of **3.654069761192594e-129**.

This is separation, not merely overlapping structure that can safely be handled by adding ancestry covariates. Affection status is confounded with ancestry, so an adjusted model cannot identify a disease effect independently of ancestry in this cohort.

## Discovery and replication status

No discovery association analysis was run because the protocol's mandatory ancestry precondition failed. Therefore:

- there are no valid associated variants from this cohort;
- there are no valid discovery effect estimates or discovery p-values;
- replication support cannot be assessed because there is no protocol-eligible discovery candidate;
- no association should be reported, regardless of what an unadjusted scan might appear to show.

Replication statistics were not computed because there is no protocol-eligible discovery candidate. Replication data were deliberately not used as a substitute discovery scan. Doing so would bypass the prespecified discovery gate and invalidate the study's reporting rule.

## Recommended next action and control plan

- Rebuild the comparison set so affected and unaffected participants overlap in ancestry—for example, recruit ancestry-matched participants or obtain appropriate phenotype representation within each ancestry stratum.
- Repeat participant and variant QC on the rebuilt cohort.
- Re-run the ancestry gate before inspecting any variant association result. Proceed only if the groups overlap; include leading ancestry axes as covariates if residual overlapping structure remains.
- Apply the recalculated Bonferroni threshold to the resulting retained variant set.
- Nominate only protocol-valid discovery hits for the independent same-direction replication test, and report only hits that satisfy that replication rule.

The durable hold is the ancestry precondition: association and replication reporting remain blocked until cohort comparability is established.
