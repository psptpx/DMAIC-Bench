# Candidate-region association study: current disposition

## Executive decision

The physical discovery plate passes the protocol's participant-level disposition rule, but this cohort **cannot carry a case-control genetic-association conclusion**. After QC, affected and unaffected participants are completely separated on genetic principal component PC2 (p = 1.582582344580355e-139). This makes affection status confounded with genetic structure and leaves no within-structure contrast from which to identify a trait effect.

Accordingly, there are **no reportable associated variants**, and replication does not support reporting any variant. The replication release contains 0 nominated candidates, so 0 variants could be tested for replication.

## Protocol and data processed

The discovery matrix contained 240 participants (120 affected and 120 unaffected) and 150 panel variants. Participant call rate had to be at least 0.95, and plate re-genotyping was triggered at a participant-failure fraction of 0.1. Variant filters were call rate at least 0.95, MAF at least 0.01, and exact HWE p-value in unaffected participants at least 1e-06. The discovery significance cutoff was the computed Bonferroni threshold 0.0003649635036496351. The replication rule required p below 0.05 and the same direction.

## Quality control and retained records

### Participants and plate

One participant failed participant call-rate QC: **P129**. The failure fraction was 0.004166666666666667, leaving 239 participants: 120 affected and 119 unaffected. Because the observed failure fraction is below the plate threshold, wholesale plate re-genotyping is not required by protocol.

Retained participant IDs are **P001–P128 and P130–P240**; P129 is excluded from all downstream calculations.

### Variants

Variant QC failed 13 variants and retained 137. The excluded variants are:

**rs060002, rs060010, rs060024, rs060037, rs060043, rs060055, rs060083, rs060093, rs060104, rs060111, rs060114, rs060139, rs060144**

The retained set is all panel variants **except** those listed above. This precisely identifies the retained set without obscuring it in a long duplicate list.

## Comparability and association

A PC1-only check was initially negative (p = 0.5031215641305691), but the required broader structure assessment found complete case-control range separation on PC2. PC2 explained 0.08136027771197264 of standardized retained-marker variance and had a group-comparison t statistic of 60.88768020785006, with p = 1.582582344580355e-139. Thus cases and controls cannot be compared as though sampled from the same genetic population.

For transparency, an unadjusted additive trend scan was computed before this problem was fully diagnosed. It produced 36 apparent Bonferroni signals and genomic inflation lambda = 2.296117548164278. These are **not associations to report**: the inflation and PC2 separation show that the scan is tracking cohort structure. A logistic scan adjusted for the leading PCs was attempted, but its Hessian was singular and it produced no adjusted p-values. We do not replace that failed analysis with guesses.

## Replication status

The independent replication file contains 120 participants and the same 150-variant panel, but its nominated discovery-candidate set is empty. Consequently, the computable replication summary is 0 candidates and 0 replicated variants. No per-variant replication p-value or direction concordance can be computed under the protocol. This is not a failed replication of a particular locus; it is the consequence of having no valid discovery nomination.

## What should happen next

1. Do not publish or nominate the unadjusted discovery signals.
2. Audit recruitment site, ancestry, plate allocation, and phenotype coding to identify why affection status is perfectly aligned with PC2.
3. Obtain affected and unaffected participants with overlapping genetic ancestry, or construct adequately sized within-ancestry case-control strata. Simply adding PC covariates cannot recover an effect when the current groups have no overlap.
4. Repeat participant QC, variant QC, multi-axis structure assessment, and the prespecified association scan on the corrected design.
5. Freeze only valid Bonferroni discoveries as replication candidates, then test exactly those candidates in the independent cohort using the prespecified p-value and direction rule.
6. Hold the study by retaining the QC exclusions, PCA diagnostics, model diagnostics, candidate freeze, and replication direction checks in the analysis record before any claim is released.

## Bottom line

The assay plate is usable after its single participant exclusion, and the filtered marker set is defined. The scientific comparison is not usable: complete PC2 separation confounds affection status. The study therefore stops at design remediation, with no associated or replicated variant claim.
