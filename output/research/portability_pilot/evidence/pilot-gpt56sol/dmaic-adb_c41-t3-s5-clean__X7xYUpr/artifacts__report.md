# Candidate-region association study report

## Executive conclusion

The plate can carry an analysis. Participant QC excluded **P011, P120** and retained **238** participants: **118** affected and **120** unaffected. The failed fraction was **0.008333333333333333**, below the protocol stop threshold of **0.1**, so re-genotyping is not triggered.

Variant QC retained **138** variants and excluded **12**. The retained affected and unaffected groups show strong but overlapping structure. They are therefore comparable only in a structure-adjusted model, not in an unadjusted test.

After adjustment for PC1, **0** variants met the Bonferroni cutoff of **0.00036231884057971015**. The study therefore does **not** support declaring any panel variant associated with affection status.

## Participant disposition

The participant call-rate threshold was **0.95**. The minimum observed participant call rate was **0.9466666666666667**. **2** affected participants and **0** unaffected participants failed. The excluded participant IDs are **P011, P120**. Every participant in the retained list below passed the rule.

**Retained participants:** P001, P002, P003, P004, P005, P006, P007, P008, P009, P010, P012, P013, P014, P015, P016, P017, P018, P019, P020, P021, P022, P023, P024, P025, P026, P027, P028, P029, P030, P031, P032, P033, P034, P035, P036, P037, P038, P039, P040, P041, P042, P043, P044, P045, P046, P047, P048, P049, P050, P051, P052, P053, P054, P055, P056, P057, P058, P059, P060, P061, P062, P063, P064, P065, P066, P067, P068, P069, P070, P071, P072, P073, P074, P075, P076, P077, P078, P079, P080, P081, P082, P083, P084, P085, P086, P087, P088, P089, P090, P091, P092, P093, P094, P095, P096, P097, P098, P099, P100, P101, P102, P103, P104, P105, P106, P107, P108, P109, P110, P111, P112, P113, P114, P115, P116, P117, P118, P119, P121, P122, P123, P124, P125, P126, P127, P128, P129, P130, P131, P132, P133, P134, P135, P136, P137, P138, P139, P140, P141, P142, P143, P144, P145, P146, P147, P148, P149, P150, P151, P152, P153, P154, P155, P156, P157, P158, P159, P160, P161, P162, P163, P164, P165, P166, P167, P168, P169, P170, P171, P172, P173, P174, P175, P176, P177, P178, P179, P180, P181, P182, P183, P184, P185, P186, P187, P188, P189, P190, P191, P192, P193, P194, P195, P196, P197, P198, P199, P200, P201, P202, P203, P204, P205, P206, P207, P208, P209, P210, P211, P212, P213, P214, P215, P216, P217, P218, P219, P220, P221, P222, P223, P224, P225, P226, P227, P228, P229, P230, P231, P232, P233, P234, P235, P236, P237, P238, P239, P240

## Variant disposition

The rules applied to the participant-QC-retained cohort were call rate at least **0.95**, minor-allele frequency at least **0.01**, and unaffected-participant Hardy-Weinberg p-value at least **1e-06**.

* Call-rate failures (**5**): rs050014, rs050071, rs050082, rs050091, rs050108.
* Minor-allele-frequency failures (**4**): rs050052, rs050092, rs050096, rs050121.
* Unaffected-participant Hardy-Weinberg failures (**3**): rs050017, rs050019, rs050040.

**Retained variants:** rs050001, rs050002, rs050003, rs050004, rs050005, rs050006, rs050007, rs050008, rs050009, rs050010, rs050011, rs050012, rs050013, rs050015, rs050016, rs050018, rs050020, rs050021, rs050022, rs050023, rs050024, rs050025, rs050026, rs050027, rs050028, rs050029, rs050030, rs050031, rs050032, rs050033, rs050034, rs050035, rs050036, rs050037, rs050038, rs050039, rs050041, rs050042, rs050043, rs050044, rs050045, rs050046, rs050047, rs050048, rs050049, rs050050, rs050051, rs050053, rs050054, rs050055, rs050056, rs050057, rs050058, rs050059, rs050060, rs050061, rs050062, rs050063, rs050064, rs050065, rs050066, rs050067, rs050068, rs050069, rs050070, rs050072, rs050073, rs050074, rs050075, rs050076, rs050077, rs050078, rs050079, rs050080, rs050081, rs050083, rs050084, rs050085, rs050086, rs050087, rs050088, rs050089, rs050090, rs050093, rs050094, rs050095, rs050097, rs050098, rs050099, rs050100, rs050101, rs050102, rs050103, rs050104, rs050105, rs050106, rs050107, rs050109, rs050110, rs050111, rs050112, rs050113, rs050114, rs050115, rs050116, rs050117, rs050118, rs050119, rs050120, rs050122, rs050123, rs050124, rs050125, rs050126, rs050127, rs050128, rs050129, rs050130, rs050131, rs050132, rs050133, rs050134, rs050135, rs050136, rs050137, rs050138, rs050139, rs050140, rs050141, rs050142, rs050143, rs050144, rs050145, rs050146, rs050147, rs050148, rs050149, rs050150

The familywise alpha was **0.05** across the retained variants, producing the stated Bonferroni cutoff.

## Cohort comparability

PCA was computed from the QC-retained genotype matrix. PC1 explained **0.08041143324224802** of standardized genotype variance and differed by affection status with p-value **4.0403632009987195e-15**. The affected PC1 range was **-4.575433479950249** to **5.618346811390099**; the unaffected range was **-4.804200549932126** to **5.050326164539733**. Those ranges overlap, so the protocol does not stop comparison, but the observed structure requires covariate control. PC1 was therefore included in every association model.

## Association result

Additive logistic regressions tested **138** retained variants, with affection status as outcome and PC1 as a covariate. **0** models failed. The smallest p-value was **0.0018095930621595277** for **rs050022**, with an estimated per-allele odds ratio of **2.363275351744545** using **233** participants with a called genotype. That p-value is above the corrected cutoff and is not a declared association. Genomic inflation was **1.1750327876429354**.

## What changed and what it achieved

QC removed the failed participants and variants before testing. Structure adjustment then addressed the protocol's ancestry precondition. These changes produced an analyzable retained cohort and fully converged adjusted tests, but they did not produce a protocol-significant finding.

## Recommended next actions and control plan

* Do not report rs050022 or any other panel marker as associated; treat the smallest-p result as hypothesis-generating only.
* Review the elevated genomic inflation and repeat sensitivity analyses with independently derived ancestry markers or an external ancestry reference if those data can be obtained. Candidate-region-derived PCs may not fully control population structure.
* Seek independent replication and a larger, ancestry-balanced cohort before revisiting the leading signal.
* Preserve the participant and variant exclusion lists, the PCA specification, and the corrected cutoff as a locked analysis manifest. Apply the same checks before any future rerun, and do not test variants unless ancestry overlap and model adjustment are documented.
* The attempted study-lead provision request was unroutable; no outside ancestry fact was available. All conclusions above come from computations on the released genotype batch.
