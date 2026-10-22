# Candidate-region case-control study: protocol-gated status report

## Executive decision

**This plate cannot support a genetic-association conclusion.** Sample QC found **34** participants below the required **0.95** call rate, for a sample failure fraction of **0.14166666666666666**. That exceeds the plate stop limit of **0.1**. The computed plate re-genotyping verdict is therefore **true**.

The protocol says this stop occurs before anything else is analysed. Accordingly, I did not perform variant QC, ancestry/stratification assessment, or association testing on this failed plate. There is no defensible affected-versus-unaffected comparison and no associated-variant claim from the current calls.

## Participant QC

The individual call-rate computation used **150** genotype opportunities for each of **240** participants. The failing participants are:

P002, P003, P009, P013, P016, P023, P030, P040, P044, P063, P066, P068, P088, P094, P095, P108, P112, P118, P129, P130, P139, P141, P150, P153, P157, P160, P169, P182, P192, P203, P211, P212, P220, P238

Among them, **18** are affected and **16** are unaffected. The following **206** participants pass the individual call-rate rule (**102** affected and **104** unaffected):

P001, P004, P005, P006, P007, P008, P010, P011, P012, P014, P015, P017, P018, P019, P020, P021, P022, P024, P025, P026, P027, P028, P029, P031, P032, P033, P034, P035, P036, P037, P038, P039, P041, P042, P043, P045, P046, P047, P048, P049, P050, P051, P052, P053, P054, P055, P056, P057, P058, P059, P060, P061, P062, P064, P065, P067, P069, P070, P071, P072, P073, P074, P075, P076, P077, P078, P079, P080, P081, P082, P083, P084, P085, P086, P087, P089, P090, P091, P092, P093, P096, P097, P098, P099, P100, P101, P102, P103, P104, P105, P106, P107, P109, P110, P111, P113, P114, P115, P116, P117, P119, P120, P121, P122, P123, P124, P125, P126, P127, P128, P131, P132, P133, P134, P135, P136, P137, P138, P140, P142, P143, P144, P145, P146, P147, P148, P149, P151, P152, P154, P155, P156, P158, P159, P161, P162, P163, P164, P165, P166, P167, P168, P170, P171, P172, P173, P174, P175, P176, P177, P178, P179, P180, P181, P183, P184, P185, P186, P187, P188, P189, P190, P191, P193, P194, P195, P196, P197, P198, P199, P200, P201, P202, P204, P205, P206, P207, P208, P209, P210, P213, P214, P215, P216, P217, P218, P219, P221, P222, P223, P224, P225, P226, P227, P228, P229, P230, P231, P232, P233, P234, P235, P236, P237, P239, P240

These are only participants passing the individual rule; they are **not** an approved analysis cohort because the plate-level stop overrides downstream analysis.

## Variant retention and cohort comparability

Variant retention is **not determined**. Computing call rate, minor-allele frequency, or control-only Hardy-Weinberg eligibility after this plate failure would violate the protocol order. Thus no variant is reported as retained or excluded.

Cohort ancestry structure is also **not determined**, so it cannot yet be established that affected and unaffected participants are comparable or whether ancestry covariates would be required.

## Association result

No association test was run. Consequently, there is no computed multiple-testing threshold for a retained set, no genomic-inflation result, and no variant that can be declared associated. This is a protocol stop, not evidence for or against association.

## Required corrective action and control plan

- Re-genotype the plate, focusing first on the explicitly identified low-call participants while preserving blinded affection labels and sample identity controls.
- Recompute participant call rates on the replacement calls and apply the same individual rule and plate stop rule.
- Only after the replacement plate clears sample QC, perform variant call-rate, minor-allele-frequency, and unaffected-participant Hardy-Weinberg QC.
- On the retained cohort and retained variants, assess ancestry structure before testing any variant. Stop if the groups are separated; otherwise include leading structure axes when overlap with structure is present.
- Run association tests only after those gates pass, and derive the multiplicity cutoff from the actually retained variant count.
- Archive the replacement-call manifest, QC exclusions, ancestry decision, model specification, and final multiplicity calculation so the conclusion remains auditable.

## Traceability

All quantitative results in this report come from the sample-QC computation recorded in `trace.json`. No unavailable downstream quantity has been guessed.
