# Candidate-region case-control study report

## Current decision
The discovery plate can proceed without re-genotyping: the computed sample-failure fraction was **0.0125**, below the protocol cutoff of **0.1**. **3** participants failed the participant call-rate rule and should be excluded from downstream analyses. Their IDs are P085, P136, and P193.

Variant QC retained **138** of **150** variants and failed **12**. Failed variants were rs040024, rs040034, rs040041, rs040044, rs040059, rs040065, rs040066, rs040114, rs040124, rs040128, rs040130, and rs040134.

## Cohort comparability
The first principal axis had p=0.8040312257984145, and the leading-axis assessment did not separate affected from unaffected participants. The discovery comparison therefore used the unadjusted dosage model rather than ancestry covariates.

## Discovery association
The Bonferroni-corrected threshold computed over the retained variants was **0.00036231884057971015**. **0** variants met it. The strongest observed discovery result was rs040143 (p=0.01573838744162139; odds ratio=1.798505093170125), so it is not a protocol-declared association.

## Replication
The replication batch contained **120** participants and **150** variants, with **1** participants failing the same participant call-rate rule and **141** variants passing the same variant QC calculation. However, the steward supplied **0** nominated discovery candidates. Consequently, no replication test was applicable: **0** candidates were replicated out of **0** candidates. There is no replication evidence supporting a reportable association.

## What caused the outcome, what changed, and control plan
The limiting factor is lack of a discovery result meeting the corrected threshold, not a failed plate or ancestry separation. The analysis changed the raw calls into a QC-qualified cohort and variant set, removed failed participants and variants, checked ancestry structure, and applied the prespecified multiplicity correction. That change produced a defensible null discovery conclusion and correctly prevented an unsupported replication claim.

Next, investigators should review assay and phenotype quality for the failed records, document the retained participant and variant lists, and treat rs040143 as non-significant rather than as a finding. Any future scan should preregister its QC, ancestry, multiplicity, and independent-replication rules and rerun the complete pipeline after any data correction. Hold the decision by retaining the raw steward batches, the executed analysis scripts, and `trace.json` alongside this report.
