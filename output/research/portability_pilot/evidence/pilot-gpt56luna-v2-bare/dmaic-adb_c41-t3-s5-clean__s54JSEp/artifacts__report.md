# Candidate-region case-control study report

## Executive conclusion

The discovery plate passes the participant QC gate: 3 of 240 participants failed the call-rate rule, a failure fraction of 0.0125, below the protocol maximum of 0.1. The affection groups are suitable for comparison on the measured QC-pass indicator; its chi-square test was 3.037974683544304 with p=0.0813373387733938.

The protocol retains 139 of 150 variants; 11 fail at least one variant rule. The discovery scan found 28 variants below the Bonferroni threshold of 0.00035971223021582735. However, lambdaGC was 2.2856510997816355, so the association signal is materially inflated and should not be treated as clean evidence without follow-up.

No discovery hit was nominated in the released replication batch: the steward supplied zero candidate variants. Consequently, the formal replication result is 0 replicated variants out of 0 candidates. This means the study currently cannot report a replicated association. The exploratory comparison of the discovery hit list found 2 variants with replication p<0.05 and concordant direction, but this is not a protocol replication result because the candidates were not nominated.

## What was computed

- Discovery data contained 240 participants: 120 affected and 120 unaffected.
- Participant QC failed for 3 participants (0.0125); the protocol limit was 0.1.
- Variant QC retained 139 variants and rejected 11.
- Discovery association used the retained variants and the protocol Bonferroni threshold 0.00035971223021582735; 28 passed.
- Replication data contained 120 participants: 60 affected and 60 unaffected, but no candidates were supplied for the formal test.

The discovery hit names were: rs050003, rs050004, rs050005, rs050007, rs050011, rs050013, rs050016, rs050021, rs050029, rs050037, rs050039, rs050043, rs050046, rs050053, rs050063, rs050064, rs050065, rs050067, rs050077, rs050090, rs050100, rs050107, rs050110, rs050113, rs050123, rs050139, rs050145, rs050148.

## Business interpretation and next steps

What is working is the plate-level participant QC and the ability to compare the two affection groups. What is preventing a conclusion is not participant QC; it is the combination of association inflation and the absence of a nominated candidate list in the replication release. The immediate change is to freeze the QC-retained discovery dataset, investigate the source of lambdaGC=2.2856510997816355, and explicitly nominate the discovery hits with their discovery directions before rerunning the independent replication analysis.

Investigators should not claim replication from the exploratory count. After nomination, rerun the prespecified replication rule (p<0.05 and same direction), retain the exact candidate list and directions, and only report variants that meet that rule. Hold the process by versioning the retained-variant list, the nomination manifest, the QC thresholds, and the analysis trace alongside the final report.
