# Study status report

## Executive conclusion

The current discovery plate cannot carry an association conclusion. Participant call-rate QC found **31 failures among 240 participants**, a failure fraction of **0.12916666666666668** (**12.916666666666668%**). This exceeds the protocol maximum of **0.1**. The resulting plate decision is therefore **do not proceed**: re-genotype before any variant-level or inferential analysis.

The steward did not furnish a distinct replacement plate. A request for one re-served the same discovery batch, and a study-lead query did not return a matching process fact. This is not evidence that a replacement can never exist; it means no replacement data were available for this run.

## Participant QC

The participant retention threshold was a call rate of at least **0.95** across **150** input variants. The observed participant call rates ranged from **0.5066666666666667** to **1.0**.

The **31** participants failing the rule were:

P004, P005, P022, P028, P035, P036, P051, P057, P060, P062, P067, P071, P077, P092, P102, P103, P120, P123, P126, P128, P130, P136, P139, P146, P153, P156, P162, P211, P217, P229, P240

The failures comprised **17 affected** and **14 unaffected** participants. Individually, **209** participants met the call-rate rule: **103 affected** and **106 unaffected**. Their identifiers were:

<details>
<summary>Participants passing individual call-rate QC</summary>

P001, P002, P003, P006, P007, P008, P009, P010, P011, P012, P013, P014, P015, P016, P017, P018, P019, P020, P021, P023, P024, P025, P026, P027, P029, P030, P031, P032, P033, P034, P037, P038, P039, P040, P041, P042, P043, P044, P045, P046, P047, P048, P049, P050, P052, P053, P054, P055, P056, P058, P059, P061, P063, P064, P065, P066, P068, P069, P070, P072, P073, P074, P075, P076, P078, P079, P080, P081, P082, P083, P084, P085, P086, P087, P088, P089, P090, P091, P093, P094, P095, P096, P097, P098, P099, P100, P101, P104, P105, P106, P107, P108, P109, P110, P111, P112, P113, P114, P115, P116, P117, P118, P119, P121, P122, P124, P125, P127, P129, P131, P132, P133, P134, P135, P137, P138, P140, P141, P142, P143, P144, P145, P147, P148, P149, P150, P151, P152, P154, P155, P157, P158, P159, P160, P161, P163, P164, P165, P166, P167, P168, P169, P170, P171, P172, P173, P174, P175, P176, P177, P178, P179, P180, P181, P182, P183, P184, P185, P186, P187, P188, P189, P190, P191, P192, P193, P194, P195, P196, P197, P198, P199, P200, P201, P202, P203, P204, P205, P206, P207, P208, P209, P210, P212, P213, P214, P215, P216, P218, P219, P220, P221, P222, P223, P224, P225, P226, P227, P228, P230, P231, P232, P233, P234, P235, P236, P237, P238, P239

</details>

These individual passes do not rescue the plate: because the plate-level failure fraction exceeds its protocol limit, none of these participants should enter the current discovery analysis until re-genotyping is completed.

## Variant retention

The input contained **150** variants, but variant call rate, minor-allele frequency, and control Hardy-Weinberg checks were intentionally not run. The protocol places re-genotyping before any further analysis after this plate-level failure. Consequently, no protocol-valid retained-variant set can be reported from this plate.

## Cohort comparability

Affected and unaffected participants cannot yet be compared for association on this dataset. The required ancestry-structure assessment was not run because participant QC stopped the workflow first. Therefore separation, overlap, and any need for ancestry covariates could not be established.

## Discovery association and replication

No discovery association scan was run, so no associated variants or nominated discovery hits exist from this analysis. The Bonferroni threshold cannot be computed until a valid retained-variant count exists. Replication was not analyzed because there were no protocol-valid discovery candidates. It therefore provides no support for reporting an association at this stage.

## Required next action and control plan

Re-genotype the discovery plate, then rerun participant call-rate QC first. Proceed only if the newly computed failure fraction does not exceed **0.1**. On a passing plate, apply variant QC, assess ancestry structure before testing, use ancestry covariates if overlapping structure is present, run the appropriately adjusted association scan with a retained-variant Bonferroni threshold, and send only valid discovery hits to independent replication. Report a hit only after replication satisfies the protocol's direction and significance requirements.

Preserve the participant-QC output and this stop decision as the audit gate. The current state is a quality hold, not a negative genetic finding.
