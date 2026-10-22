# Metabolic-trait candidate-panel study: status report

## Executive conclusion

The discovery plate can proceed past the re-genotyping gate: the computed participant failure fraction was **0.0125**, below the protocol maximum of **0.1**. After participant QC, **237** participants were retained. Variant QC retained **139** of **150** variants.

The cohort is not directly comparable by affection status without adjustment. The leading-axis comparison was separated (PC1 p=1.25789e-14; statistic=59.4446), so the protocol-required next analysis is association testing with leading ancestry axes as covariates.

That adjusted discovery analysis was not released. The **27** variants from the computed unadjusted trend scan at Bonferroni threshold **0.000359712** are therefore preliminary and must not be reported as associations. The unadjusted inflation estimate was lambdaGC=2.64507, reinforcing that the unadjusted scan is not a valid final result.

## What was retained and why

- Participant rule: call rate >= **0.95**; the observed minimum was **0.933333**. **3** participants failed, so the plate did not trigger re-genotyping.
- Variant rule: call rate >= **0.95**, MAF >= **0.01**, and unaffected-control HWE p >= **1e-06**. **11** variants failed and **139** were retained.
- The retained participant and variant identifiers are recorded in `/workspace/discovery_results.json`; no identifiers were invented.

## Replication and reporting decision

The released replication batch contains **120** participants and **150** panel variants, but the steward supplied **0** nominated discovery candidates. Consequently, the computed replication result is **0** candidates and **0** replicated hits. There is no candidate-level replication test to evaluate. Under the protocol, no discovery association can be reported.

## Cause, change, and next action

The immediate cause of the stoppage is not the plate QC: it passed. The cause is ancestry structure combined with the absence of an adjusted discovery result and the resulting absence of nominated replication hits. The change required is to run the discovery association model on the **237** retained participants and **139** retained variants with the leading ancestry axes as covariates, apply the prespecified Bonferroni rule, nominate qualifying hits, and then test those hits in the independent replication cohort for p < **0.05** and the same direction.

Until those steps are completed, investigators should report the study as QC-passed but analytically incomplete, not as a positive association study. Hold the result by retaining the raw steward batches, the executable analysis, `/workspace/trace.json`, and this report; rerun the recorded computations after the adjusted discovery and nomination batches are released.
