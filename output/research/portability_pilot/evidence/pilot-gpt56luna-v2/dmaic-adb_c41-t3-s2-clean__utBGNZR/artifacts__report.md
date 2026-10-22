# Candidate-region case-control study report

## Executive conclusion

The plate passes the participant-level gate, but the discovery cohort cannot carry a case-control association conclusion under the study protocol. The leading ancestry axis separates affected and unaffected participants (axis 1; p=5.861587813431253e-14). The protocol explicitly prohibits comparing groups drawn from separate ancestries. Therefore the discovery association scan is not interpretable, and no variant should be reported as associated.

## What was retained

The discovery batch contained 240 participants and 150 variants. Participant QC found 2 failures, a failure fraction of 0.008333333333333333; this is below the protocol re-genotyping limit of 0.1, so the plate was retained and 238 participants remained. Variant QC retained 34 variants and rejected 116.

## Discovery and ancestry finding

The QC-retained discovery data were used to compute ancestry structure. The first axis separated the phenotype groups, so the required comparison gate failed. An unadjusted exploratory scan produced 10 variants below the Bonferroni cutoff 0.05/34 = 0.0014705882352941176; that result is not a protocol-valid association result and is not reported.

The steward nominated rs020008 for replication. Its exploratory discovery allele-frequency difference was 0.27773821392963965 with p=9.90315797201588e-10; because ancestry separation invalidates the comparison, this is not a reportable discovery claim. The exploratory odds ratio was 3.264150943396227.

## Replication

The independent replication batch contained 120 participants: 60 affected and 60 unaffected. No replication participants failed the computed call-rate rule, and rs020008 had call rate 0.9916666666666667. The candidate showed the same direction as discovery and replication p=0.0006786817183904285; thus 1 of 1 nominated candidates met the computed replication checks. This does not overcome the failed discovery ancestry-comparison gate, so the association is not reported.

## What caused the stop and what to do next

The limiting issue is not plate-level participant QC or replication: it is complete phenotype separation on the leading ancestry axis. The investigators should obtain ancestry-overlapping affected and unaffected participants, or redesign the study so ancestry is not confounded with affection status. A future scan should rerun participant and variant QC, establish ancestry overlap before testing, and use prespecified ancestry covariates only when the groups overlap sufficiently for comparison. The current exploratory hit list should not be treated as evidence of association.

## Control plan

Archive the raw batches, QC decisions, scripts, and this trace. Require the ancestry-comparability gate to pass before any future variant p-values are interpreted, retain the same QC thresholds and Bonferroni rule from the protocol, and require independent same-direction replication before reporting any future discovery hit.
