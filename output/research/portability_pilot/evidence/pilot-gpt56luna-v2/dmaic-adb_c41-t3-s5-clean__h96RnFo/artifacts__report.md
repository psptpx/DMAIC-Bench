# Candidate-region case-control study report

## Executive conclusion

The discovery plate can proceed without re-genotyping: the computed sample failure fraction was **0.0125**, below the protocol limit of **0.1**. However, the study cannot carry a final association conclusion yet. The protocol requires ancestry structure to be assessed before testing, and no ancestry or leading-axis data were released. In addition, the replication batch contained **0** nominated candidates, so none of the discovery findings could be replicated. Consequently, **no association is reportable** under the protocol.

## What was retained

The discovery batch contained **240** participants and **150** variants. **3** participants failed the participant call-rate rule; the plate-level trigger was not met. The participant-level QC result should be held for follow-up, but it did not require re-genotyping under the stated rule.

Variant QC retained **139** variants and excluded **11**. Retention used the protocol's call-rate, control MAF, and unaffected-participant HWE rules.

## Discovery scan

After excluding missing calls per variant, the computed Bonferroni threshold was **0.00035971223021582735**. The provisional trend scan produced **27** significant variants, with genomic-control lambda **2.1157548994019657**. Their identifiers were:

rs050003, rs050004, rs050005, rs050007, rs050011, rs050013, rs050016, rs050021, rs050029, rs050037, rs050039, rs050043, rs050046, rs050053, rs050063, rs050064, rs050065, rs050077, rs050090, rs050100, rs050107, rs050110, rs050113, rs050123, rs050139, rs050145, rs050148

These are provisional findings only. The required ancestry-comparability analysis was not computed because the steward released no ancestry or PC batch. Therefore affected and unaffected participants have not been established as comparable for the purpose of a final association claim, and covariate adjustment could not be performed.

## Replication

The released replication batch had **0** nominated discovery candidates and therefore **0** replicated candidates. There was no replication p-value or direction test to compute. This is not evidence that the provisional findings replicated; it is missing nomination/input data. Under the protocol, a discovery association is reported only after independent replication, so none is reportable.

## What caused the current stop

The immediate blockers are missing ancestry information and an empty nominated-hit list in the replication release. The QC gate itself did not block the plate: its measured failure fraction was below the re-genotyping trigger, and variants were filtered according to protocol. The uncorrected preliminary scan was superseded by the corrected scan that excluded missing calls consistently.

## Recommended next actions and hold points

1. Obtain ancestry markers or leading-axis results for the discovery cohort, then test whether the groups are separated or overlapping and, if overlapping, rerun the association model with the required axes as covariates.
2. Nominate the corrected discovery candidates for replication, preserving their discovery directions, and obtain the independent-cohort results.
3. Apply the protocol replication rule to each nominated candidate. Report only candidates with replication evidence meeting the protocol; otherwise reconsider the discovery scan.
4. Preserve the QC filters, missing-call handling, ancestry decision, candidate list, replication results, and this trace as the analysis record.

Until those inputs are supplied, the proper study status is **provisional discovery signal, no reportable association**.
