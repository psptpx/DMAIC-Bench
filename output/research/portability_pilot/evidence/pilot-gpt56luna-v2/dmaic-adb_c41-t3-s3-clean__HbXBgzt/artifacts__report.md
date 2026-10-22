# Study status report

## Executive conclusion

The discovery plate **cannot carry a valid association conclusion**. The participant QC computation found 31 failed participants, a failure fraction of 0.12916666666666668, exceeding the protocol limit of 0.1. The protocol therefore requires re-genotyping before anything is analysed. The appropriate next action is to re-genotype the discovery plate, rerun participant and variant QC, then rerun ancestry assessment and association testing.

## What was measured

The discovery batch contained 240 participants and 150 panel variants. The protocol requires participant call rate at least 0.95, variant call rate at least 0.95, minor-allele frequency at least 0.01, and unaffected-participant HWE p-value at least 1e-06. It also requires ancestry comparability before testing, Bonferroni correction over retained variants, and replication at p < 0.05 in the same direction.

The failed participant IDs were: P004, P005, P022, P028, P035, P036, P051, P057, P060, P062, P067, P071, P077, P092, P102, P103, P120, P123, P126, P128, P130, P136, P139, P146, P153, P156, P162, P211, P217, P229, P240.

## Variant and participant retention

After applying the stated variant filters to the released discovery calls, 209 participants met the individual call-rate rule, while 131 variants failed at least one variant rule and 19 variants were retained. The retained variant IDs were:

rs030013, rs030014, rs030026, rs030032, rs030033, rs030036, rs030058, rs030061, rs030071, rs030073, rs030074, rs030078, rs030082, rs030087, rs030099, rs030101, rs030107, rs030109, rs030125

Because the plate-level participant failure rule was breached, these are QC results from a failed plate, not a cleared analysis set.

## Cohort comparability and association

The protocol requires an ancestry-structure check before any variant is tested. No ancestry labels, principal components, or separation statistic were released, and the available genotype batch does not contain such fields. Therefore affected and unaffected participants **cannot be declared comparable from this run**; this step is unavailable and the conclusion stops there. No ancestry-adjusted association result can be reported.

A provisional unadjusted scan was computed only as a diagnostic: it produced 0 variants below the Bonferroni threshold of 0.002631578947368421 and lambda-GC 0.35308534416370824. It is not a valid study conclusion because the plate failed participant QC and ancestry comparability was not established.

## Replication

The replication release contained no nominated discovery candidates: the computed candidate count was 0. Thus the number replicated was 0; there is no replication-supported association to report. This is not evidence that a hit failed replication; rather, no candidate was nominated because the discovery analysis did not clear the required gates.

## What changed, what it achieved, and how to hold it

The analysis applied the protocol's participant and variant QC rules to the steward-released calls and stopped the reportable discovery path when the plate-level failure rule was exceeded. This prevented an invalid association claim. No data transformation can rescue this batch: the required change is re-genotyping, followed by the same QC audit. The investigators should preserve the QC script, thresholds, failed-ID list, retained-variant list, ancestry check, and replication nomination log as the release checklist for the replacement plate.

Numbers and decisions above are recorded in `/workspace/trace.json`; unavailable ancestry data are explicitly marked as refused there. No association should be reported from the current discovery plate.
