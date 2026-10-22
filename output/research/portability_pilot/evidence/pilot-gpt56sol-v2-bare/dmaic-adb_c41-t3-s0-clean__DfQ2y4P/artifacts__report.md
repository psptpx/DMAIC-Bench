# Candidate-region association study: final status

## Executive decision

The discovery plate can support a conclusion. Participant QC excluded **3** of **240** participants, a failure fraction of **0.0125**, below the protocol's re-genotyping trigger of **0.1**. The analysis retained **237** participants and **137** variants. There was no evidence that affection groups separated on PC1 (**p = 0.8666902364429903**), so the affected and unaffected participants were compared using an unadjusted additive trend test.

One discovery variant, **rs000008**, passed the Bonferroni threshold and then met the independent-cohort replication rule. The study therefore supports reporting **rs000008** as associated with affection status in these cohorts, while avoiding a causal claim.

## Protocol and analysis route

The prespecified participant call-rate minimum was **0.95**, and plate re-genotyping was triggered only if the failing fraction exceeded **0.1**. Variant retention required call rate at least **0.95**, minor-allele frequency at least **0.01**, and exact Hardy-Weinberg p-value among unaffected participants at least **0.000001**. Discovery used familywise alpha **0.05** over the retained variants. Replication required independent-cohort p-value below **0.05** and the same direction.

An initial PCA implementation failed before producing results because its optional library was unavailable. PCA was then genuinely recomputed by NumPy singular-value decomposition; no result from the failed attempt was used.

## Participant QC and plate disposition

The discovery input contained **240** participants. **3** failed participant call-rate QC: **P053, P129, P160**. Their computed call rates were **0.94**, **0.9466666666666667**, and **0.9466666666666667**, respectively. The failure fraction was **0.0125**, so the plate passed. After exclusion, **237** participants remained: **119** affected and **118** unaffected.

## Variant QC

Of **150** panel variants, **13** failed and **137** were retained.

Excluded variants: rs000003, rs000025, rs000061, rs000079, rs000086, rs000091, rs000107, rs000108, rs000122, rs000130, rs000138, rs000149, rs000150.

Retained variants: rs000001, rs000002, rs000004, rs000005, rs000006, rs000007, rs000008, rs000009, rs000010, rs000011, rs000012, rs000013, rs000014, rs000015, rs000016, rs000017, rs000018, rs000019, rs000020, rs000021, rs000022, rs000023, rs000024, rs000026, rs000027, rs000028, rs000029, rs000030, rs000031, rs000032, rs000033, rs000034, rs000035, rs000036, rs000037, rs000038, rs000039, rs000040, rs000041, rs000042, rs000043, rs000044, rs000045, rs000046, rs000047, rs000048, rs000049, rs000050, rs000051, rs000052, rs000053, rs000054, rs000055, rs000056, rs000057, rs000058, rs000059, rs000060, rs000062, rs000063, rs000064, rs000065, rs000066, rs000067, rs000068, rs000069, rs000070, rs000071, rs000072, rs000073, rs000074, rs000075, rs000076, rs000077, rs000078, rs000080, rs000081, rs000082, rs000083, rs000084, rs000085, rs000087, rs000088, rs000089, rs000090, rs000092, rs000093, rs000094, rs000095, rs000096, rs000097, rs000098, rs000099, rs000100, rs000101, rs000102, rs000103, rs000104, rs000105, rs000106, rs000109, rs000110, rs000111, rs000112, rs000113, rs000114, rs000115, rs000116, rs000117, rs000118, rs000119, rs000120, rs000121, rs000123, rs000124, rs000125, rs000126, rs000127, rs000128, rs000129, rs000131, rs000132, rs000133, rs000134, rs000135, rs000136, rs000137, rs000139, rs000140, rs000141, rs000142, rs000143, rs000144, rs000145, rs000146, rs000147, rs000148.

## Can affected and unaffected participants be compared?

Yes on the measured population-structure check. PCA used the QC-retained discovery matrix with mean imputation and variance standardization. A two-group Welch test on PC1 gave statistic **-0.16804784337181541** and **p = 0.8666902364429903**; at comparison alpha **0.05**, the groups were not separated. This supports the unadjusted scan route. The genomic inflation estimate was **1.115940928253286**; because the protocol supplied no decision cutoff for that estimate, it is reported as a diagnostic rather than used to invent another gate.

## Discovery association

With **137** retained variants, the computed Bonferroni threshold was **0.00036496350364963507**. Exactly **1** variant passed:

- **rs000008**: trend statistic **43.08041958041958**, **p = 5.253540318605901e-11**, positive direction, affected mean dosage **1.205128205128205**, unaffected mean dosage **0.5726495726495726**, and continuity-corrected allelic odds ratio **3.755397108338285**.

No other retained variant met the discovery threshold.

## Independent replication

The replication cohort contained **60** affected and **60** unaffected participants. For the **1** nominated candidate, rs000008 had **119** called samples and call rate **0.9916666666666667**. Its trend statistic was **18.392794104592795**, with **p = 1.7973641155483908e-05**. The direction was positive and matched discovery. Affected and unaffected mean dosages were **1.2203389830508475** and **0.6333333333333333**, and the continuity-corrected allelic odds ratio was **3.3410138248847927**. Thus **1** of **1** candidates replicated under alpha **0.05** and the same-direction rule.

## Business conclusion and next actions

The plate is usable, QC exclusions have been applied, the measured stratification check supports comparing the groups, and rs000008 has both multiplicity-controlled discovery evidence and directionally concordant independent replication. Investigators should report the association with both cohort-specific effect estimates and explicitly describe all QC exclusions and the additive model.

Next, preserve the protocol, source batches, scripts, detailed result JSON, and this trace as the audit package; independently review genotype cluster quality for rs000008; verify allele coding and sample independence; and seek functional follow-up and additional external cohorts. Continue using the same participant and variant QC rules for any rerun, and do not promote the association to causation without further evidence.
