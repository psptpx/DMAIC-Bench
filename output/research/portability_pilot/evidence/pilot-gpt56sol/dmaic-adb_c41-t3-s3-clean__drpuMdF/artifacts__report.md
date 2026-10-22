# Candidate-region study status

## Executive conclusion

The plate cannot support an association conclusion. Participant call-rate QC found **34 failures among 240 participants**, a failure fraction of **0.14166666666666666**. The protocol permits at most **0.1** to fail and requires re-genotyping before any further analysis when that limit is exceeded. The observed plate therefore fails the gate by **10 participants** relative to the maximum count of **24** that would not exceed the rule.

This is a stop decision, not a finding of no association. Variant QC, ancestry structure, case-control comparability, and variant association were not evaluated, so no variant can be called retained or associated from this plate.

## Participant QC

Call rate was computed as the fraction of nonmissing calls across **150 variants** for each participant. The retention cutoff was **0.95**. Observed participant call rates ranged from **0.52** to **1.0**.

The call-rate rule provisionally retains **206 participants**: **102 affected** and **104 unaffected**.

Retained participant IDs: P001, P004, P005, P006, P007, P008, P010, P011, P012, P014, P015, P017, P018, P019, P020, P021, P022, P024, P025, P026, P027, P028, P029, P031, P032, P033, P034, P035, P036, P037, P038, P039, P041, P042, P043, P045, P046, P047, P048, P049, P050, P051, P052, P053, P054, P055, P056, P057, P058, P059, P060, P061, P062, P064, P065, P067, P069, P070, P071, P072, P073, P074, P075, P076, P077, P078, P079, P080, P081, P082, P083, P084, P085, P086, P087, P089, P090, P091, P092, P093, P096, P097, P098, P099, P100, P101, P102, P103, P104, P105, P106, P107, P109, P110, P111, P113, P114, P115, P116, P117, P119, P120, P121, P122, P123, P124, P125, P126, P127, P128, P131, P132, P133, P134, P135, P136, P137, P138, P140, P142, P143, P144, P145, P146, P147, P148, P149, P151, P152, P154, P155, P156, P158, P159, P161, P162, P163, P164, P165, P166, P167, P168, P170, P171, P172, P173, P174, P175, P176, P177, P178, P179, P180, P181, P183, P184, P185, P186, P187, P188, P189, P190, P191, P193, P194, P195, P196, P197, P198, P199, P200, P201, P202, P204, P205, P206, P207, P208, P209, P210, P213, P214, P215, P216, P217, P218, P219, P221, P222, P223, P224, P225, P226, P227, P228, P229, P230, P231, P232, P233, P234, P235, P236, P237, P239, P240.

The **34 failed participants** comprise **18 affected** and **16 unaffected**.

Failed participant IDs: P002, P003, P009, P013, P016, P023, P030, P040, P044, P063, P066, P068, P088, P094, P095, P108, P112, P118, P129, P130, P139, P141, P150, P153, P157, P160, P169, P182, P192, P203, P211, P212, P220, P238.

“Provisionally retained” means only that these participants individually meet the call-rate rule. It does not rescue the plate after the plate-level failure.

## Variants and cohort comparability

No variant was run through call rate, minor-allele frequency, or unaffected-participant Hardy–Weinberg filtering because the protocol stops analysis at the failed plate gate. Consequently, there is no computed retained-variant set and no valid Bonferroni denominator or threshold.

Ancestry structure was not assessed. It therefore could not be established whether affected and unaffected participants are comparable on this cohort, and no ancestry covariates were fitted.

## Association status

No variant association test was run. There is therefore no computed association count, no genomic-inflation result, and no associated-variant list. The study currently has no defensible positive or negative association conclusion.

## Corrective action and control plan

Re-genotype the plate, with particular attention to the listed failed participants and the causes of their missing calls. After replacement calls are delivered, restart the workflow from participant call-rate QC. Proceed to variant QC only if the plate-level gate passes; then establish ancestry comparability before testing variants, adjust for leading ancestry axes if overlapping structure is present, and apply the protocol's Bonferroni rule over the actually retained variants.

To hold the correction, archive the replacement call matrix and rerun the same participant-level calculation before releasing downstream results. Record the participant exclusions, variant exclusions and their reasons, the ancestry decision, the final model, and multiplicity threshold in the next analysis trace.
