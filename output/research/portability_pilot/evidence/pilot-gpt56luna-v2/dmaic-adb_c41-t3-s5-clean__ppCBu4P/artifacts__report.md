# Candidate-region case-control study report

## Executive conclusion

The discovery plate can carry a quality-control conclusion: participant QC found **3** failed participants, a failure fraction of **0.0125**, and the plate passed the protocol gate. The discovery scan retained **26** variants and failed **124** variants under the call-rate, MAF, and unaffected-control HWE rules.

The association scan found **6** discovery-significant variants after the computed Bonferroni correction. The observed genomic inflation estimate was **3.786076811817577**, so the scan should not be treated as a clean final result without resolving ancestry structure and rerunning the appropriate covariate-adjusted analysis.

The study cannot currently report an association. The released replication batch nominated **0** candidates, so no replication test, replication p-value, direction check, or replicated-hit count could be computed. This is missing nomination/input data, not evidence of replication failure. The protocol requires replication before reporting.

## What was computed

- Discovery sample QC: **3** samples failed; failure fraction **0.0125**.
- Discovery variant QC: **124** variants failed and **26** were retained.
- Discovery association: **6** variants were significant; lambda GC was **3.786076811817577**.
- Replication sample QC: **1** sample failed; failure fraction **0.008333333333333333**.
- Replication testing: no candidates were supplied, so no replication p-values or same-direction checks could be computed.
- Ancestry structure: no ancestry results or leading-axis coordinates were released, so comparability and covariate adjustment could not be assessed.

The retained discovery variant labels were: rs050001, rs050004, rs050010, rs050012, rs050015, rs050037, rs050044, rs050045, rs050048, rs050050, rs050053, rs050055, rs050061, rs050073, rs050094, rs050099, rs050100, rs050101, rs050102, rs050104, rs050107, rs050114, rs050118, rs050132, rs050139, and rs050144.

The six discovery labels were rs050004, rs050037, rs050053, rs050100, rs050107, and rs050139. They are provisional discovery findings only; they are not reportable under the protocol.

## Cause, change, and achieved state

The immediate cause of the stopped conclusion is incomplete downstream evidence: the replication release explicitly contained no nominated discovery candidates, and the ancestry evidence required before comparing affected and unaffected participants was not available. The change made was to apply the stated participant and variant QC rules and to stop rather than infer replication or ancestry results. That achieved a defensible discovery QC/scan inventory while preventing an unsupported biological claim.

## Next actions and control

The investigators should obtain the ancestry/leading-axis data, nominate the discovery candidates with their discovery directions, rerun the association using the required ancestry covariates if structure overlaps, and then test each nominated candidate in the independent cohort for the required p-value and direction. Until those inputs and analyses exist, no association should be reported. Preserve the released batches, scripts, trace, and report together so the QC filters, candidate nomination, replication decision, and any rerun remain auditable.
