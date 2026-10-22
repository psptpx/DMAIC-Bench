# Candidate-region association study report

## Executive conclusion

The plate can support a conclusion. Sample QC failed **3** of **240** participants, a failure fraction of **0.0125**, below the protocol re-genotyping trigger of **0.1**. After protocol exclusions, **237** participants and **139** variants remained. Genotype PCA showed strong but overlapping ancestry structure, so affected and unaffected participants can be compared only with ancestry adjustment. The PC1-adjusted analysis found **1** associated variant: **rs020008**.

## What was measured and changed

Participant call rate was calculated across **150** panel variants. The retention threshold was **0.95**. The excluded participants were **P031, P153, P236**; each had observed call rate **0.9466666666666667**. This left **119** affected and **118** unaffected participants.

The retained participants are:

P001, P002, P003, P004, P005, P006, P007, P008, P009, P010, P011, P012, P013, P014, P015, P016, P017, P018, P019, P020, P021, P022, P023, P024, P025, P026, P027, P028, P029, P030, P032, P033, P034, P035, P036, P037, P038, P039, P040, P041, P042, P043, P044, P045, P046, P047, P048, P049, P050, P051, P052, P053, P054, P055, P056, P057, P058, P059, P060, P061, P062, P063, P064, P065, P066, P067, P068, P069, P070, P071, P072, P073, P074, P075, P076, P077, P078, P079, P080, P081, P082, P083, P084, P085, P086, P087, P088, P089, P090, P091, P092, P093, P094, P095, P096, P097, P098, P099, P100, P101, P102, P103, P104, P105, P106, P107, P108, P109, P110, P111, P112, P113, P114, P115, P116, P117, P118, P119, P120, P121, P122, P123, P124, P125, P126, P127, P128, P129, P130, P131, P132, P133, P134, P135, P136, P137, P138, P139, P140, P141, P142, P143, P144, P145, P146, P147, P148, P149, P150, P151, P152, P154, P155, P156, P157, P158, P159, P160, P161, P162, P163, P164, P165, P166, P167, P168, P169, P170, P171, P172, P173, P174, P175, P176, P177, P178, P179, P180, P181, P182, P183, P184, P185, P186, P187, P188, P189, P190, P191, P192, P193, P194, P195, P196, P197, P198, P199, P200, P201, P202, P203, P204, P205, P206, P207, P208, P209, P210, P211, P212, P213, P214, P215, P216, P217, P218, P219, P220, P221, P222, P223, P224, P225, P226, P227, P228, P229, P230, P231, P232, P233, P234, P235, P237, P238, P239, P240

Variant QC was then rerun on the retained cohort. A variant had to meet call rate **0.95**, minor-allele frequency **0.01**, and unaffected-participant Hardy–Weinberg p-value **1e-06**. The corrected exact test excluded **11** variants and retained **139**. Failures by criterion were:

- **call rate:** rs020016, rs020023, rs020042, rs020107, rs020115
- **minor-allele frequency:** rs020022, rs020048, rs020096, rs020102
- **control-only Hardy–Weinberg equilibrium:** rs020074, rs020143

The retained variants are:

rs020001, rs020002, rs020003, rs020004, rs020005, rs020006, rs020007, rs020008, rs020009, rs020010, rs020011, rs020012, rs020013, rs020014, rs020015, rs020017, rs020018, rs020019, rs020020, rs020021, rs020024, rs020025, rs020026, rs020027, rs020028, rs020029, rs020030, rs020031, rs020032, rs020033, rs020034, rs020035, rs020036, rs020037, rs020038, rs020039, rs020040, rs020041, rs020043, rs020044, rs020045, rs020046, rs020047, rs020049, rs020050, rs020051, rs020052, rs020053, rs020054, rs020055, rs020056, rs020057, rs020058, rs020059, rs020060, rs020061, rs020062, rs020063, rs020064, rs020065, rs020066, rs020067, rs020068, rs020069, rs020070, rs020071, rs020072, rs020073, rs020075, rs020076, rs020077, rs020078, rs020079, rs020080, rs020081, rs020082, rs020083, rs020084, rs020085, rs020086, rs020087, rs020088, rs020089, rs020090, rs020091, rs020092, rs020093, rs020094, rs020095, rs020097, rs020098, rs020099, rs020100, rs020101, rs020103, rs020104, rs020105, rs020106, rs020108, rs020109, rs020110, rs020111, rs020112, rs020113, rs020114, rs020116, rs020117, rs020118, rs020119, rs020120, rs020121, rs020122, rs020123, rs020124, rs020125, rs020126, rs020127, rs020128, rs020129, rs020130, rs020131, rs020132, rs020133, rs020134, rs020135, rs020136, rs020137, rs020138, rs020139, rs020140, rs020141, rs020142, rs020144, rs020145, rs020146, rs020147, rs020148, rs020149, rs020150

An earlier HWE implementation was discarded because it produced numerical warnings and invalid probabilities; none of those preliminary retention results entered the analysis above.

## Cohort comparability

PCA used mean-imputed, allele-frequency-standardized dosages for the retained cohort and variants. PC1 explained **0.09352354350804105** of genotype variance and was associated with affection status at p = **1.0163852371988689e-13**. Structure was not complete separation: unsupervised clusters contained **89** affected and **30** unaffected participants in one cluster, and **30** affected and **88** unaffected participants in the other. Thus the groups overlap and can be compared, but PC1 must be included as a covariate. No independent ancestry-label batch was available; this decision is based on genotype-derived structure.

As a diagnostic, the unadjusted tests had genomic inflation **2.524244878694837**. After PC1 adjustment it was **0.9841026021725029**, showing that the specified change controlled the ancestry-driven inflation.

## Association result

The familywise alpha was **0.05** across **139** retained variants, giving a Bonferroni threshold of **0.00035971223021582735**. Additive logistic likelihood-ratio tests adjusted for PC1 tested **139** variants.

**rs020008** passed the threshold with adjusted p = **4.054916166609094e-05**, likelihood-ratio statistic **16.845509291815546**, and per-allele odds ratio **2.3857989016664805** among **230** called retained participants. No other retained variant met the corrected threshold.

## Recommended next actions and control plan

* Treat rs020008 as a panel-level association requiring confirmation, not yet as a causal result. Validate the genotype cluster/calls for the variant and replicate the PC1-adjusted association in an independent cohort.
* Preserve the participant and variant exclusion lists above with the analysis dataset. Do not restore failed records without new genotyping and a complete QC rerun.
* For future releases, rerun sample call rate first and re-genotype the plate whenever the failure fraction exceeds the protocol trigger. Then rerun variant QC, genotype PCA, the overlap check, and association with any leading ancestry axes supported by the cohort.
* Continue monitoring genomic inflation after adjustment; the observed adjusted value **0.9841026021725029** is the benchmark from this run.
