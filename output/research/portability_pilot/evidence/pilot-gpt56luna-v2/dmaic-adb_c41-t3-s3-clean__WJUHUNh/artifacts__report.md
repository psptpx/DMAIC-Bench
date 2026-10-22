# Candidate-region case-control study: status report

## Executive conclusion

The discovery plate cannot support a protocol-valid association conclusion. The participant QC computation found **31** failed participants among **240**, a failure fraction of **0.12916666666666668**, above the protocol maximum of **0.1**. The required action is re-genotyping before interpreting the scan.

## What was retained

The discovery batch contained **150** panel variants. After applying participant QC for the analysis calculation, **139** variants passed the call-rate, MAF, and unaffected-control HWE rules; **11** failed at least one rule. This is an analytical screening result, not a release of the plate from the failed participant-QC gate.

The computed leading-axis comparisons did not show significant affected/unaffected separation: PC1 p=0.09427154429317015, PC2 p=0.7146230735778081, and PC3 p=0.6477903477191944. Thus the available axes did not indicate separated ancestries in this calculation.

## Association and replication

Using the **139** retained variants, the Bonferroni threshold computed from the protocol alpha was **0.00035971223021582735**. The association scan produced **0** variants beyond that threshold. The smallest nominal p-value was **0.000394727763032567** for **rs030133**, which is not below the corrected threshold, so no discovery hit was nominated.

The steward released a replication cohort with **0** nominated candidates and explicitly stated that no discovery hit was nominated. Consequently, the replication computation has **0** replicated hits among **0** candidates; there is no replication result that can support reporting an association. The replication QC calculation itself found **0** failed participants among **120** and **145** variants passing its computed call-rate check, but that does not create a replication test for an absent candidate.

## Business status and next steps

No variant should be reported as associated. The immediate cause is the discovery plate's participant failure fraction above the protocol limit; the scan also has no Bonferroni-significant discovery result and no nominated replication candidate. Re-genotype the discovery plate, rerun participant and variant QC, reassess ancestry before testing, repeat the prespecified association scan, and nominate only variants that cross the corrected threshold. Any future reportable hit must then be tested in the independent cohort in the same direction with replication p below **0.05**. Preserve the rerun outputs and gate decisions in the analysis trace so the QC and reporting rules remain auditable.
