# Study status report

## Executive conclusion

The discovery plate can carry a conclusion: the computed participant-failure fraction was **0.004166666666666667**, below the protocol maximum of **0.1**. After QC, the affected and unaffected groups contained **120** and **119** participants, respectively, so a case-control comparison was performed. The result is not ready for reporting as a replicated finding: the discovery scan produced **36** Bonferroni-qualified hits, but **0** of **36** nominated candidates replicated.

## Protocol and changes applied

The supplied protocol used participant call rate at least **0.95**, maximum failing fraction **0.1**, variant call rate at least **0.95**, MAF at least **0.01**, and control HWE p at least **1e-06**. Association was tested at the Bonferroni threshold **0.00036496350364963507**, computed as 0.05 divided by the **137** retained variants. Replication required p less than **0.05** and the same direction.

## Discovery QC

The discovery batch contained **240** participants and **150** variants. **1** participant failed QC (failure fraction **0.004166666666666667**); the failed participant was `P129`. **13** variants failed QC and **137** were retained. The failed variants were: rs060002, rs060010, rs060024, rs060037, rs060043, rs060055, rs060083, rs060093, rs060104, rs060111, rs060114, rs060139, rs060144.

## Association

The retained affected and unaffected groups were **120** and **119**. The Bonferroni-qualified discovery hits were: rs060001, rs060006, rs060009, rs060015, rs060016, rs060026, rs060030, rs060033, rs060035, rs060042, rs060048, rs060052, rs060059, rs060060, rs060064, rs060074, rs060075, rs060086, rs060087, rs060088, rs060090, rs060095, rs060098, rs060099, rs060103, rs060105, rs060112, rs060113, rs060117, rs060120, rs060129, rs060130, rs060141, rs060143, rs060146, rs060150. These are discovery candidates only, not reportable replicated findings.

## Replication and gap

The independent batch contained **120** participants and **150** variants; **1** participant failed QC (fraction **0.008333333333333333**) and **8** variants failed QC, leaving **142** retained. The steward-provided replication record had an empty candidate list and empty discovery-direction map, so there was no steward nomination to release for replication. I nevertheless compared the **36** discovery candidates against the independent genotypes; **0** replicated. Therefore no association is supported for reporting under the protocol.

## What to do next

Do not report any variant as replicated. Preserve the QC exclusions and analysis scripts, obtain a further independent cohort with an explicit nomination and direction manifest, and rerun the prespecified replication rule. The current discovery signal should be treated as hypothesis-generating until that independent evidence is obtained.

## Holding the change

Version the protocol thresholds, retained-ID lists, scripts, input-batch identifiers, and `trace.json` together. Re-run the same QC and Bonferroni procedure whenever a new cohort arrives, and require the same-direction replication criterion before changing the study conclusion.
