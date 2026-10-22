# Metabolic-trait candidate-panel study report

## Executive conclusion

The discovery plate cannot support a conclusion yet. The participant QC analysis found 31 of 240 participants below the required call rate of 0.95, a failure fraction of 0.12916666666666668, above the allowed 0.1. The required action is plate re-genotyping; association findings should not be treated as a study conclusion until that corrective action is completed.

## What was assessed

The released discovery batch contained 240 participants and 150 variants, with 120 affected and 120 unaffected participants. The protocol required participant call rate at least 0.95, and plate re-genotyping at the 0.1 failure threshold. Variant retention required call rate at least 0.95, MAF at least 0.01, and unaffected-control HWE p at least 1e-06.

After applying the participant call-rate filter, 209 participants remained: 103 affected and 106 unaffected. This leaves groups available for a numerical comparison, but the plate-level QC failure prevents using that comparison as a valid final study conclusion.

The variant QC computation retained 19 variants. It tested 19 retained variants for case-control association. The raw leading result was rs030107 with p = 0.03993697606300295; this is only a nominal result. The Bonferroni threshold was 0.002631578947368421, and 0 variants met it. The genomic-control lambda from the tested p-values was 1.8735537539127642.

## Replication

The replication batch reports 0 nominated discovery candidates and supplies no discovery-direction record. Consequently, 0 variants were replicated and replication support for a discovery hit could not be computed. The protocol replication rule is p < 0.05 with the same direction, but there was no nominated candidate to which that rule could be applied. This is not evidence for or against replication.

## Recommendation and control plan

- Re-genotype the discovery plate because the observed participant failure fraction exceeded the protocol limit.
- Re-run participant and variant QC on the corrected calls, then repeat the case-control scan using the protocol's Bonferroni rule.
- Nominate replication candidates only if they meet that corrected discovery rule; then evaluate the independent cohort using p < 0.05 and the same direction.
- Hold the conclusion at “not established” until the corrected plate passes QC and any nominated association satisfies both discovery and replication requirements. Preserve the QC thresholds, retained IDs, association output, and replication nomination list with the next analysis run.

No conclusion of association is reported from this run.
