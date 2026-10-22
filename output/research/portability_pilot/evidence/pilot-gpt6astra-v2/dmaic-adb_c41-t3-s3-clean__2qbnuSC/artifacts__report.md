# Study status: stop and re-genotype

## Decision for the principal investigator

**The current discovery plate cannot support an association conclusion under the prespecified protocol.** Sample quality control found **31 failures among 240 participants**, a failure fraction of **0.129167 (12.9167%)**. This exceeds the protocol's permitted plate-failure fraction. The required next action is re-genotyping, not removing the failing participants and continuing the scan.

## What was computed

I calculated each participant's call rate as the number of nonmissing genotype calls divided by the **150** panel variants, treating JSON nulls as missing. I applied the protocol's inclusive participant call-rate cutoff to the original panel before any variant filtering.

**209 participants individually pass** the call-rate rule. This is an individual QC result, not an approved retained analysis cohort: the plate-level stop overrides progression. `participants_qc.csv` identifies every participant, their computed call rate, and whether they individually pass. Participants marked false fail; those marked true pass conditionally on resolving the plate problem.

The quantitative audit is in `trace.json`; the raw released protocol and calls are in `data/`. Only sample QC was completed. The analysis stopped intentionally at its plate gate.

## What remains unestablished

- **Variant retention:** not computed. No variants have been approved for inference. Variant call rate, minor-allele frequency and control Hardy–Weinberg screening must follow successful plate QC.
- **Affected/unaffected comparability:** not assessed. No ancestry-axis analysis was run, so neither comparability nor ancestry confounding can be asserted.
- **Discovery association:** not tested. This is not evidence that the panel lacks associated variants; it is a quality-driven inability to test them under the protocol.
- **Replication:** not evaluated. There are no valid discovery candidates to carry forward. The initial broadly worded request was routed to replication and locked; this was a prerequisite refusal, not a finding that replication data do not exist.
- **Replacement plate:** a request for re-genotyped discovery data returned the same original batch. No distinct replacement dataset was supplied, so no improvement after re-genotyping can be claimed.

## Cause, corrective action and control plan

The demonstrated immediate cause of the stop is excessive participant-level missingness. These calls alone do not establish a laboratory root cause. Investigators should ask the laboratory to review DNA quality, plate position, call-clustering quality, handling and run records before re-genotyping. Preserve the current calls and participant QC manifest as the baseline audit.

The change made here was to halt downstream inference rather than bypass the protocol. It prevented unsupported association reporting; no laboratory correction has yet been implemented or measured.

After re-genotyping, rerun the same participant and plate rules without relaxing thresholds. Only a passing plate should proceed to variant QC and an explicit retained-participant/variant manifest. Check leading ancestry axes before testing: stop if cases and controls occupy separate ancestries; if structure overlaps, include the leading structure axes as covariates. Apply the protocol's retained-panel multiple-testing correction and require independent, same-direction replication before reporting a discovery association. Any replication failure requires reconsideration of the discovery scan.

Hold the improvement through versioned raw releases, reproducible QC scripts, laboratory review of failure patterns, and a documented sign-off at each gate. The present conclusion stops at sample QC until a replacement plate demonstrates compliance.
