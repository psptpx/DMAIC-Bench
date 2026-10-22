# Candidate-region association study: final status

## Executive decision

The plate **can carry a conclusion**. Participant QC failed **2** of **240** participants (failure fraction **0.008333333333**), below the protocol's re-genotyping limit of **0.1**. After required exclusions and variant QC, the retained cohort was not split into nonoverlapping ancestry groups. It did show overlapping structure on PC1, so all discovery tests were adjusted for **1** leading axis rather than comparing affection groups naively.

The final adjusted discovery scan tested **132** retained variants at a Bonferroni cutoff of **0.000378787878788** and nominated **1** association: **rs020008**. The independent cohort tested **1** nominated candidate and replicated **1**. Therefore **rs020008 is reportable under the study protocol**.

## Quality disposition

### Participants and plate

The call-rate rule excluded **P017** and **P111**. Each had call rate **0.946666666667**, below the required **0.95**. The retained discovery cohort has **238** participants: **118** affected and **120** unaffected. Because the observed participant failure fraction is below the stopping limit, re-genotyping the whole plate is not required.

### Variants

Variant QC retained **132** and rejected **18**. Failure accounting was **5** for call rate, **4** for minor-allele frequency, and **9** for exact Hardy-Weinberg testing among unaffected participants. These reason counts describe failed criteria; retention required all criteria.

Rejected variants: rs020001, rs020016, rs020027, rs020037, rs020045, rs020054, rs020072, rs020084, rs020085, rs020092, rs020103, rs020114, rs020117, rs020131, rs020140, rs020142, rs020147, rs020150.

Retained variants: rs020002, rs020003, rs020004, rs020005, rs020006, rs020007, rs020008, rs020009, rs020010, rs020011, rs020012, rs020013, rs020014, rs020015, rs020017, rs020018, rs020019, rs020020, rs020021, rs020022, rs020023, rs020024, rs020025, rs020026, rs020028, rs020029, rs020030, rs020031, rs020032, rs020033, rs020034, rs020035, rs020036, rs020038, rs020039, rs020040, rs020041, rs020042, rs020043, rs020044, rs020046, rs020047, rs020048, rs020049, rs020050, rs020051, rs020052, rs020053, rs020055, rs020056, rs020057, rs020058, rs020059, rs020060, rs020061, rs020062, rs020063, rs020064, rs020065, rs020066, rs020067, rs020068, rs020069, rs020070, rs020071, rs020073, rs020074, rs020075, rs020076, rs020077, rs020078, rs020079, rs020080, rs020081, rs020082, rs020083, rs020086, rs020087, rs020088, rs020089, rs020090, rs020091, rs020093, rs020094, rs020095, rs020096, rs020097, rs020098, rs020099, rs020100, rs020101, rs020102, rs020104, rs020105, rs020106, rs020107, rs020108, rs020109, rs020110, rs020111, rs020112, rs020113, rs020115, rs020116, rs020118, rs020119, rs020120, rs020121, rs020122, rs020123, rs020124, rs020125, rs020126, rs020127, rs020128, rs020129, rs020130, rs020132, rs020133, rs020134, rs020135, rs020136, rs020137, rs020138, rs020139, rs020141, rs020143, rs020144, rs020145, rs020146, rs020148, rs020149.

## Can affected and unaffected participants be compared?

Yes, but only with ancestry adjustment. PC1 explained **0.101777910480** of genotype variance and differed between affection groups (Welch statistic **-9.392820783592**, p = **5.230440889696471e-18**). The empirical PC1 ranges nevertheless overlapped, so the groups were not classified as separate ancestries. Following the protocol, PC1 entered every discovery model as a covariate. The adjusted scan's genomic inflation factor was **1.017335454287**.

## Discovery association

For **rs020008**, the adjusted additive logistic model used **235** called participants. Its coefficient was **0.976219815215** with standard error **0.236356302937**, Wald statistic **4.130288903165**, p = **3.623076440155987e-05**, and odds ratio **2.654403118287** per coded allele. This p-value is below the computed Bonferroni cutoff. No other variant crossed the final Wald-test cutoff.

An exploratory likelihood-ratio implementation was also run, but it was not used for final nomination because its borderline result set differed from the coefficient-test nomination supplied for replication. The final conclusion uses the explicitly documented adjusted Wald analysis above.

## Independent replication and reporting decision

The replication analysis for **rs020008** used **119** called participants. Its coefficient was **1.004300771363** with standard error **0.296176995496**, Wald statistic **3.390880408122**, p = **6.966849453772815e-04**, and odds ratio **2.729997712714**. The effect direction matched discovery and the p-value was below the replication alpha of **0.05**. The protocol's replication gate is therefore satisfied.

## What changed, what it achieved, and how to hold it

- **Participant control:** remove P017 and P111 from discovery analyses; preserve the computed call-rate audit and do not reintroduce them.
- **Variant control:** freeze the retained and rejected variant lists above, together with each stored QC metric and failure reason.
- **Confounding control:** use the frozen PC1-adjusted discovery specification; an unadjusted case-control comparison is not valid for this cohort.
- **Multiplicity control:** keep the cutoff tied to the retained-variant count and do not reinterpret nominal discovery p-values as panel-wide findings.
- **Replication control:** report rs020008 because it passed the independent same-direction rule; do not report unreplicated or non-nominated discovery signals.
- **Next action:** archive the scripts, input batch digests, exclusions, PCA scores, model outputs, and replication result; seek further independent validation and functional follow-up before making causal or clinical claims.
