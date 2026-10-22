# Candidate-region association study: status report

## Executive conclusion

The discovery plate can support analysis: **3** participants failed the call-rate rule, a failure fraction of **0.0125**, which is below the protocol maximum of **0.1**. After exclusion, **237** participants remained. Variant QC retained **139** of **150** variants and excluded **11**.

The affected and unaffected participants are not exchangeable without adjustment. PC1 differed between groups (p = **4.4356006605714159e-16**) but the observed PC1 ranges overlap, so the protocol's overlapping-structure branch applies. The association models therefore included **1** ancestry covariate, PC1. The adjusted scan tested **139** variants and found **0** associations below the Bonferroni threshold of **0.00035971223021582735**. Consequently, **0** variants were nominated and **0** replicated. No panel association should be reported.

## Quality control and retained data

The participant call-rate threshold was **0.95**. The excluded participants are P127, P142, and P195; all other participants were retained. Re-genotyping is not triggered because the participant failure fraction, **0.0125**, does not exceed **0.1**.

Variant retention required call rate at least **0.95**, minor-allele frequency at least **0.01**, and unaffected-participant HWE p-value at least **0.000001**. Failures comprised **5** call-rate failures, **4** frequency failures, and **2** HWE failures; these criterion counts need not be disjoint. The excluded variants are: rs050014, rs050017, rs050019, rs050052, rs050071, rs050082, rs050091, rs050092, rs050096, rs050108, rs050121.

The retained variants are: rs050001, rs050002, rs050003, rs050004, rs050005, rs050006, rs050007, rs050008, rs050009, rs050010, rs050011, rs050012, rs050013, rs050015, rs050016, rs050018, rs050020, rs050021, rs050022, rs050023, rs050024, rs050025, rs050026, rs050027, rs050028, rs050029, rs050030, rs050031, rs050032, rs050033, rs050034, rs050035, rs050036, rs050037, rs050038, rs050039, rs050040, rs050041, rs050042, rs050043, rs050044, rs050045, rs050046, rs050047, rs050048, rs050049, rs050050, rs050051, rs050053, rs050054, rs050055, rs050056, rs050057, rs050058, rs050059, rs050060, rs050061, rs050062, rs050063, rs050064, rs050065, rs050066, rs050067, rs050068, rs050069, rs050070, rs050072, rs050073, rs050074, rs050075, rs050076, rs050077, rs050078, rs050079, rs050080, rs050081, rs050083, rs050084, rs050085, rs050086, rs050087, rs050088, rs050089, rs050090, rs050093, rs050094, rs050095, rs050097, rs050098, rs050099, rs050100, rs050101, rs050102, rs050103, rs050104, rs050105, rs050106, rs050107, rs050109, rs050110, rs050111, rs050112, rs050113, rs050114, rs050115, rs050116, rs050117, rs050118, rs050119, rs050120, rs050122, rs050123, rs050124, rs050125, rs050126, rs050127, rs050128, rs050129, rs050130, rs050131, rs050132, rs050133, rs050134, rs050135, rs050136, rs050137, rs050138, rs050139, rs050140, rs050141, rs050142, rs050143, rs050144, rs050145, rs050146, rs050147, rs050148, rs050149, rs050150.

## Cohort comparability

On PC1, the affected range was **-5.0085554475801244** to **5.4436831007244431**, while the unaffected range was **-4.3742252657955509** to **6.0877754012465042**. These ranges overlap, so this is not the protocol's separate-ancestry stopping condition. However, the PC1 group test was strongly significant (p = **4.4356006605714159e-16**), requiring adjustment. PC1 explained **0.081435035301888406** of standardized retained-genotype variance.

## Discovery and replication

Additive logistic models adjusted for PC1 converged for all **139** tested variants, with **0** model failures. The familywise alpha was **0.05**, yielding a retained-variant Bonferroni threshold of **0.00035971223021582735**. The smallest observed p-value was **0.0045933080607472605**, so **0** variants passed. Genomic inflation was **1.1818975706719022**, which warrants caution about residual structure but does not change the no-hit decision.

The independent replication batch contains **0** nominated candidates. Thus no replication effect or p-value can be computed; this is not evidence of replication failure, but the logical consequence of having **0** discovery hits. Under the protocol, **0** associations are reportable.

## What investigators should do next

Do not claim association for this panel. Preserve the participant exclusions, variant exclusions, ancestry-adjusted model, scripts, and machine-readable trace as the audit record. Before any redesigned or expanded scan, review the residual inflation, pre-specify ancestry covariates, and obtain additional well-matched samples. Any future discovery signal must again satisfy multiplicity control and then show independent same-direction replication before reporting.

## Analysis integrity note

An initial HWE implementation was numerically unstable, and the preliminary results based on it were discarded. The reported QC and scan use the corrected log-space exact HWE calculation. The failed attempts are recorded as failed steps in the trace and do not contribute to the conclusions above.
