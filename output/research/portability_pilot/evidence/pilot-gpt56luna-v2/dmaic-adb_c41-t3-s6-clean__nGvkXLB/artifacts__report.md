# Candidate-region case-control study report

## Executive conclusion

The discovery plate can proceed past the participant QC stop. The computed participant failure fraction was 0.004166666666666667, and the computed failed-participant count was 1. Variant QC retained 137 variants and failed 13.

A preliminary discovery scan identified 36 variants below the computed Bonferroni threshold of 0.00036496350364963507. The genomic inflation estimate from that scan was 2.7473438941862263. These are discovery findings only, not reportable study associations.

The formal replication handoff contained 0 nominated candidates and 0 replicated candidates. Therefore the study currently has no protocol-valid association to report. The conclusion stops at replication because the steward supplied no nominated discovery hits or discovery directions.

## What was computed

### Discovery QC

- The discovery batch contained 240 participants and 150 panel variants, split into 120 affected and 120 unaffected participants.
- 1 participant failed the protocol call-rate rule; the resulting failure fraction was 0.004166666666666667. This is below the protocol's stated plate re-genotyping trigger, so the plate passed this gate.
- 13 variants failed the combined call-rate, MAF, and control-HWE rules; 137 variants were retained.

### Discovery associations

The unadjusted genotype-by-phenotype scan was run on the retained variants. Its computed significant count was 36, at threshold 0.00036496350364963507, with lambdaGC 2.7473438941862263. The locally nominated discovery list was:

rs060035, rs060009, rs060006, rs060016, rs060042, rs060026, rs060015, rs060074, rs060113, rs060095, rs060060, rs060129, rs060130, rs060103, rs060143, rs060150, rs060120, rs060033, rs060052, rs060141, rs060001, rs060059, rs060086, rs060146, rs060105, rs060112, rs060087, rs060075, rs060030, rs060090, rs060099, rs060088, rs060064, rs060098, rs060048, rs060117

This scan cannot be treated as the final protocol association result because no ancestry variables or leading-axis structure data were released. The protocol requires ancestry comparability to be established before variant testing; that analysis was not computable from the released discovery batch.

### Replication

The independent batch contained 120 participants, with 60 affected and 60 unaffected participants. Its computed failed-participant count was 1, with failure fraction 0.008333333333333333.

For completeness, an exploratory local comparison of the 36 discovery candidates found 0 candidates meeting the replication p-value and same-direction criteria. This exploratory result is not a formal replication result: the steward's replication batch explicitly contained zero nominated candidates and zero discovery directions. The formal replication analysis therefore has 0 candidates and 0 replicated candidates.

## Business interpretation and next actions

**Where things stand:** the plate passed the participant QC stop, and a retained variant set was computed. Strong preliminary discovery signals exist, but no association is reportable.

**What is causing the stop:** two protocol prerequisites are unresolved. First, ancestry structure and case-control comparability were not supplied, so covariate adjustment or a valid comparability decision could not be computed. Second, the replication handoff carried no nominated discovery candidates, so formal replication cannot support reporting.

**What changed:** missing genotypes were handled as missing; participant call rates, variant call rates, MAF, control HWE, discovery associations, and replication comparisons were computed from the steward files. The discovery candidates were recorded locally, but the steward's formal replication payload remained empty.

**What was achieved:** participant and variant QC decisions are quantitative and reproducible, and the preliminary discovery list is preserved. No unsupported association claim was made.

**What should happen next:** obtain the ancestry/leading-axis data and rerun the discovery association with the required covariates if structure overlaps. Then formally nominate the retained discovery candidates, including their discovery directions, to the steward and obtain a replication payload that names those candidates. Reconsider the discovery scan if any nominated candidate fails replication, as required by the protocol.

**How this will be held:** retain `/workspace/trace.json` with the computation steps and route decisions, retain the steward JSON batches and analysis scripts, and do not publish a discovery hit until ancestry comparability and formal same-direction replication are both documented.
