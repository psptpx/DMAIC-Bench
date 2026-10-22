# Candidate-region association study report

## Executive conclusion

The discovery plate can carry an analysis conclusion: the participant QC failure fraction was 0.0125, so it was below the protocol limit of 0.1. However, the study cannot report an association because the nominated discovery candidate did not replicate under the protocol rule.

## What was retained

The discovery batch contained 240 participants and 150 panel variants. 3 participants failed the call-rate rule, leaving 237 retained participants. 11 variants failed the combined call-rate, MAF, or unaffected-group HWE rules; 139 variants were retained.

## Cohort comparability

The leading-axis p-values were [0.6037562654964042, 0.07587716658106235, 0.2948843207120856, 0.05351640432547867, 0.16891800560817155]. No axis separated affected and unaffected participants at the computed screening criterion, so the cohorts were treated as comparable without ancestry covariates.

## Discovery scan

The Bonferroni threshold was 0.00035971223021582735. One discovery hit was found: rs070008 (variant index 7), with chi-square statistic 20.747062621212326, p-value 3.12487459994016e-05, and positive case-minus-control dosage direction 0.43253373313343335.

## Replication

The independent replication batch contained 120 participants and tested 1 nominated candidate. For rs070008, the replication chi-square statistic was 1.5087099811676088 and the p-value was 0.4703138737947131. The replication direction was 0.07372881355932204, while the discovery direction was 0.43253373313343335; the directions were therefore the same. The candidate did not satisfy the replication reporting rule, so 0 of 1 candidates was replicated and no association is reportable.

## Business action and control

What changed was the application of the protocol gates: participant and variant QC were applied before testing, ancestry comparability was checked, discovery significance was corrected over retained variants, and replication was required before reporting. This achieved a documented discovery result but no reportable finding. Investigators should reconsider the discovery scan rather than report rs070008, review QC and phenotype/genotype generation, and obtain a new independent replication only after that review. The analysis should be held by retaining the released batch files, the executable analysis scripts, and `/workspace/trace.json`, with future conclusions required to pass the same QC, comparability, correction, and replication gates.
