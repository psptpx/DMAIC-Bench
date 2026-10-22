# Discovery panel status report

## Executive decision

This plate cannot support a genetic-association conclusion. Participant quality control failed at the
protocol's first mandatory gate: **31 of 240 participants failed**, a failure fraction of
**0.12916666666666668**, above the permitted **0.10**. The protocol therefore requires
re-genotyping before anything else is analyzed.

The immediate business conclusion is a controlled stop, not a negative association result. There is
currently no valid basis for comparing affected and unaffected participants, nominating a variant, or
claiming replication.

## What was computed

The discovery input contained 240 participants and 150 panel variants, with 120 affected and
120 unaffected participants. For each participant I divided observed genotype calls by
panel variants. The participant rule was call rate at least 0.95.

### Participants failing the individual rule

The following 31 participants failed:

P004, P005, P022, P028, P035, P036, P051, P057, P060, P062, P067, P071, P077, P092, P102, P103,
P120, P123, P126, P128, P130, P136, P139, P146, P153, P156, P162, P211, P217, P229, P240

### Participants passing the individual rule

The following 209 participants met the individual call-rate rule:

P001, P002, P003, P006, P007, P008, P009, P010, P011, P012, P013, P014, P015, P016, P017, P018,
P019, P020, P021, P023, P024, P025, P026, P027, P029, P030, P031, P032, P033, P034, P037, P038,
P039, P040, P041, P042, P043, P044, P045, P046, P047, P048, P049, P050, P052, P053, P054, P055,
P056, P058, P059, P061, P063, P064, P065, P066, P068, P069, P070, P072, P073, P074, P075, P076,
P078, P079, P080, P081, P082, P083, P084, P085, P086, P087, P088, P089, P090, P091, P093, P094,
P095, P096, P097, P098, P099, P100, P101, P104, P105, P106, P107, P108, P109, P110, P111, P112,
P113, P114, P115, P116, P117, P118, P119, P121, P122, P124, P125, P127, P129, P131, P132, P133,
P134, P135, P137, P138, P140, P141, P142, P143, P144, P145, P147, P148, P149, P150, P151, P152,
P154, P155, P157, P158, P159, P160, P161, P163, P164, P165, P166, P167, P168, P169, P170, P171,
P172, P173, P174, P175, P176, P177, P178, P179, P180, P181, P182, P183, P184, P185, P186, P187,
P188, P189, P190, P191, P192, P193, P194, P195, P196, P197, P198, P199, P200, P201, P202, P203,
P204, P205, P206, P207, P208, P209, P210, P212, P213, P214, P215, P216, P218, P219, P220, P221,
P222, P223, P224, P225, P226, P227, P228, P230, P231, P232, P233, P234, P235, P236, P237, P238, P239

These passers are **not an analysis-ready retained cohort** because the plate-level rule supersedes
individual filtering once the failure fraction exceeds its maximum.

## Variant and cohort status

Variant QC tests run: **0**. Consequently, no variant has been analytically retained or rejected under
the call-rate, minor-allele-frequency, and unaffected-participant Hardy-Weinberg rules. Treating all
150 supplied markers as retained would bypass the protocol and is not defensible.

Ancestry tests run: **0**. The required leading-axis check was deliberately not run after the plate
failed. It therefore cannot yet be established whether affected and unaffected participants are
ancestrally comparable or whether covariate adjustment would suffice.

Association tests run: **0**. There are no discovery p-values, effect estimates, corrected threshold
comparisons, or associated variants from this plate. This is not evidence that the panel lacks an
association; the scan was ineligible.

Replication candidates: **0**. Replication data were not requested or analyzed because no valid
discovery association can be nominated. Replication therefore cannot support reporting any variant at
this stage.

## Cause, corrective action, and control plan

The blocking cause is excess participant-level missingness on the discovery plate. The data were not
silently repaired, participants were not selectively removed to evade the plate gate, and downstream
testing was not performed.

The investigators should:

1. Re-genotype the discovery plate and investigate plate processing, DNA quality, and call-clustering
   causes for the listed failures.
2. Recompute participant call rates on the replacement calls and release the plate only if the failure
   fraction is no greater than 0.10.
3. Only after that release, apply variant QC, perform the leading-axis ancestry check, and decide whether
   comparison is prohibited or requires ancestry covariates.
4. Run the eligible association model, apply the protocol's corrected criterion over the retained
   variants, and send only valid discovery nominees to the independent cohort.
5. Report a nominee only after the independent cohort meets the protocol's direction and significance
   requirements.

The hold is maintained by keeping variant QC, ancestry analysis, association testing, and replication
nomination downstream of the participant-QC release gate. The current change achieved a defensible stop
before invalid inference; it did not produce a biological finding.
