# Candidate-region association study: current disposition

## Executive conclusion

The plate can support analysis. Participant QC failed **5** participants, a failed fraction of **0.020833333333333332**, which is below the protocol re-genotyping limit of **0.1**. After participant exclusion, **235** participants remained. Variant QC retained **138** variants and excluded **12**.

The retained affected and unaffected groups can be compared: genotype PCA showed overlapping score ranges on all **10** leading axes examined, rather than separate ancestries, and PC1 was not associated with affection status (**p = 0.30536457876275325**). No ancestry covariate requirement was established, so the prespecified additive trend analysis is the primary result; a PC-adjusted model was also computed as a sensitivity analysis.

The protocol-final trend analysis tested **138** variants with a Bonferroni threshold of **0.00036231884057971015**. It identified **1** associated variant: **rs000008**, with **p = 1.9479303715141013e-06** and per-allele odds ratio **2.667354602530193**. Thus this panel provides evidence that rs000008 is associated with affection status in the analyzed cohort; it does not by itself establish causality or external replication.

## Participant quality control

Call rate was computed across **150** panel variants for each of **240** participants. The retention cutoff was **0.95**. The excluded participants were:

P011, P059, P069, P224, P225

The retained participants were all submitted participants except those listed above (**235** retained):

P001, P002, P003, P004, P005, P006, P007, P008, P009, P010, P012, P013, P014, P015, P016, P017, P018
P019, P020, P021, P022, P023, P024, P025, P026, P027, P028, P029, P030, P031, P032, P033, P034, P035
P036, P037, P038, P039, P040, P041, P042, P043, P044, P045, P046, P047, P048, P049, P050, P051, P052
P053, P054, P055, P056, P057, P058, P060, P061, P062, P063, P064, P065, P066, P067, P068, P070, P071
P072, P073, P074, P075, P076, P077, P078, P079, P080, P081, P082, P083, P084, P085, P086, P087, P088
P089, P090, P091, P092, P093, P094, P095, P096, P097, P098, P099, P100, P101, P102, P103, P104, P105
P106, P107, P108, P109, P110, P111, P112, P113, P114, P115, P116, P117, P118, P119, P120, P121, P122
P123, P124, P125, P126, P127, P128, P129, P130, P131, P132, P133, P134, P135, P136, P137, P138, P139
P140, P141, P142, P143, P144, P145, P146, P147, P148, P149, P150, P151, P152, P153, P154, P155, P156
P157, P158, P159, P160, P161, P162, P163, P164, P165, P166, P167, P168, P169, P170, P171, P172, P173
P174, P175, P176, P177, P178, P179, P180, P181, P182, P183, P184, P185, P186, P187, P188, P189, P190
P191, P192, P193, P194, P195, P196, P197, P198, P199, P200, P201, P202, P203, P204, P205, P206, P207
P208, P209, P210, P211, P212, P213, P214, P215, P216, P217, P218, P219, P220, P221, P222, P223, P226
P227, P228, P229, P230, P231, P232, P233, P234, P235, P236, P237, P238, P239, P240

After exclusion, the analysis cohort contained **117** affected and **118** unaffected participants. Because the failed fraction did not exceed **0.1**, the protocol does not require plate re-genotyping before analysis.

## Variant quality control

Variant QC was applied after participant QC. A variant had to meet call rate **0.95**, minor-allele frequency **0.01**, and exact Hardy-Weinberg p-value among unaffected participants **1e-06**. The HWE calculation used **118** retained unaffected participants before variant-specific missing calls.

Excluded variants (**12**):

rs000031, rs000049, rs000060, rs000078, rs000086, rs000093, rs000114, rs000126, rs000135, rs000138
rs000142, rs000148

Retained variants (**138**):

rs000001, rs000002, rs000003, rs000004, rs000005, rs000006, rs000007, rs000008, rs000009, rs000010
rs000011, rs000012, rs000013, rs000014, rs000015, rs000016, rs000017, rs000018, rs000019, rs000020
rs000021, rs000022, rs000023, rs000024, rs000025, rs000026, rs000027, rs000028, rs000029, rs000030
rs000032, rs000033, rs000034, rs000035, rs000036, rs000037, rs000038, rs000039, rs000040, rs000041
rs000042, rs000043, rs000044, rs000045, rs000046, rs000047, rs000048, rs000050, rs000051, rs000052
rs000053, rs000054, rs000055, rs000056, rs000057, rs000058, rs000059, rs000061, rs000062, rs000063
rs000064, rs000065, rs000066, rs000067, rs000068, rs000069, rs000070, rs000071, rs000072, rs000073
rs000074, rs000075, rs000076, rs000077, rs000079, rs000080, rs000081, rs000082, rs000083, rs000084
rs000085, rs000087, rs000088, rs000089, rs000090, rs000091, rs000092, rs000094, rs000095, rs000096
rs000097, rs000098, rs000099, rs000100, rs000101, rs000102, rs000103, rs000104, rs000105, rs000106
rs000107, rs000108, rs000109, rs000110, rs000111, rs000112, rs000113, rs000115, rs000116, rs000117
rs000118, rs000119, rs000120, rs000121, rs000122, rs000123, rs000124, rs000125, rs000127, rs000128
rs000129, rs000130, rs000131, rs000132, rs000133, rs000134, rs000136, rs000137, rs000139, rs000140
rs000141, rs000143, rs000144, rs000145, rs000146, rs000147, rs000149, rs000150

## Cohort comparability and association

The first PCA implementation failed because its software dependency was unavailable; no conclusion was taken from that failure. PCA was then successfully recomputed by NumPy singular-value decomposition on the QC-retained, mean-imputed and allele-frequency-standardized genotype matrix. PC1 had logistic **p = 0.30536457876275325**, and case and control ranges overlapped on every examined axis. The exploratory PC4 result was not used by itself to declare ancestry structure because multiple axes were inspected and the candidate panel contains the tested loci. This supports comparison of the groups and does not establish a requirement for ancestry-axis adjustment.

All **138** primary trend models completed, with **0** model failures. The genomic inflation factor was **0.8252275757628631**. The rs000008 model used **231** participants with nonmissing genotype; its coefficient was **0.9810871956904753**, standard error **0.2061647838285499**, Wald statistic **22.645726059545687**, **p = 1.9479303715141013e-06**, and per-allele odds ratio **2.667354602530193**. No other retained variant crossed the Bonferroni threshold. In the PC-adjusted sensitivity analysis, rs000008 remained significant (**p = 9.729143504599411e-06**) and was again the only variant crossing the same threshold.

## What changed, what it achieved, and next actions

The analysis removed participants below the call-rate rule, removed variants failing call rate, frequency, or control-HWE rules, and checked the cohort for ancestry separation before association testing. These changes converted the submitted plate into a protocol-eligible analysis set and left one association after multiplicity correction.

Investigators should next:

- technically review rs000008 cluster/call quality and confirm its genotype coding and missingness;
- replicate rs000008 in an independent, ancestry-compatible cohort using the same prespecified QC and primary trend model, with ancestry adjustment if structure is established;
- perform conditional or fine-mapping work only after technical confirmation and replication;
- preserve the participant/variant exclusion lists, PCA procedure, covariate specification, and Bonferroni rule as the locked audit trail; and
- on any refreshed plate, rerun participant QC first and stop for re-genotyping if the failed fraction exceeds the protocol limit.

The separately requested study-lead ancestry fact was unavailable, so no external ancestry label was invented. The comparability decision and PC-adjusted sensitivity analysis are based only on the PCA computed from the released genotype data.
