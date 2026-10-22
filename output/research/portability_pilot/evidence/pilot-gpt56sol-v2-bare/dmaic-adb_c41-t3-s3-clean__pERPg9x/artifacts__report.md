# Discovery-panel study status

## Executive conclusion

The discovery plate cannot carry an association conclusion. Participant call-rate QC found **31** failures among **240** participants, a computed failure fraction of **0.1291666667**. This is above the protocol plate re-genotyping threshold of **0.10**. The required action is therefore to re-genotype the discovery plate and restart QC; proceeding to association or replication on the current calls would bypass the protocol.

## Protocol gate and participant disposition

The participant call-rate minimum is **0.95**. The QC computation used all **150** panel variants for each participant. The failed set contains **17** affected and **14** unaffected participants:

P004, P005, P022, P028, P035, P036, P051, P057, P060, P062, P067, P071, P077, P092, P102, P103, P120, P123, P126, P128, P130, P136, P139, P146, P153, P156, P162, P211, P217, P229, P240

A further **209** participants provisionally meet the individual call-rate rule, comprising **103** affected and **106** unaffected participants:

P001, P002, P003, P006, P007, P008, P009, P010, P011, P012, P013, P014, P015, P016, P017, P018, P019, P020, P021, P023, P024, P025, P026, P027, P029, P030, P031, P032, P033, P034, P037, P038, P039, P040, P041, P042, P043, P044, P045, P046, P047, P048, P049, P050, P052, P053, P054, P055, P056, P058, P059, P061, P063, P064, P065, P066, P068, P069, P070, P072, P073, P074, P075, P076, P078, P079, P080, P081, P082, P083, P084, P085, P086, P087, P088, P089, P090, P091, P093, P094, P095, P096, P097, P098, P099, P100, P101, P104, P105, P106, P107, P108, P109, P110, P111, P112, P113, P114, P115, P116, P117, P118, P119, P121, P122, P124, P125, P127, P129, P131, P132, P133, P134, P135, P137, P138, P140, P141, P142, P143, P144, P145, P147, P148, P149, P150, P151, P152, P154, P155, P157, P158, P159, P160, P161, P163, P164, P165, P166, P167, P168, P169, P170, P171, P172, P173, P174, P175, P176, P177, P178, P179, P180, P181, P182, P183, P184, P185, P186, P187, P188, P189, P190, P191, P192, P193, P194, P195, P196, P197, P198, P199, P200, P201, P202, P203, P204, P205, P206, P207, P208, P209, P210, P212, P213, P214, P215, P216, P218, P219, P220, P221, P222, P223, P224, P225, P226, P227, P228, P230, P231, P232, P233, P234, P235, P236, P237, P238, P239

“Provisionally” is important: because the plate-level gate failed, this participant set cannot advance to inferential analysis. The provisional list is an audit result, not an analysis cohort.

## Variant retention and group comparability

Variant QC was not run after the failed plate gate, so a retained-variant count and retained-variant list could not be computed. There is no defensible post-QC genotype matrix on which to assess whether affected and unaffected participants can be compared. Any ancestry/stratification assessment and any adjustment decision must wait for replacement calls.

## Discovery association and replication

No discovery association scan was run, because the input plate failed its mandatory QC gate. There are therefore no nominated discovery hits. The independent replication cohort was not analyzed: without a valid discovery candidate, replication cannot support reporting a variant and same-direction replication cannot be evaluated.

This is a protocol stop, not evidence that the panel has no association. The current data support neither a positive nor a negative genetic conclusion.

## Corrective action and control plan

Re-genotype the discovery plate, import the replacement calls without substituting or imputing undocumented values, and rerun participant call-rate QC first. Hold all downstream work unless the plate-level participant failure fraction is at or below **0.10**. Once that gate passes, remove individual failures, apply variant call-rate, minor-allele-frequency, and unaffected-participant Hardy–Weinberg filters from the released protocol, assess affected/unaffected comparability, and only then run the corrected discovery scan. Send only valid discovery hits to the independent replication test and require the protocol-specified direction agreement.

Archive the replacement call file, QC script, participant and variant exclusion tables, and final analysis manifest so that the gate and every downstream result can be reproduced.
