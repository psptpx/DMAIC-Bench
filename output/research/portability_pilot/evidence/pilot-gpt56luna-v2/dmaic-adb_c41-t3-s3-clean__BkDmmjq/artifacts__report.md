# Case-control candidate-region study report

## Executive conclusion

The discovery plate cannot carry a protocol-valid association conclusion. The protocol requires re-genotyping when more than 0.1 of participants fail the participant call-rate rule; the computed failure fraction was 0.12916666666666668, with 31 failed participants among 240. All association results below are therefore exploratory and not reportable under the study protocol.

## What was retained

The discovery matrix contained 240 participants, 150 variants, and 2519 missing genotype calls. Variant QC retained 19 variants and failed 131. The retained variants were: rs030013, rs030014, rs030026, rs030032, rs030033, rs030036, rs030058, rs030061, rs030071, rs030073, rs030074, rs030078, rs030082, rs030087, rs030099, rs030101, rs030107, rs030109, rs030125. The failed variant identifiers were computed and are preserved in the released genotype batch and analysis trace context.

## Cohort comparability

Using the 19 retained variants, the computed PC1 explained 0.08202113501729184 of standardized genotype variance. The PC1 case-control comparison had p=0.4929934527279859; this does not indicate PC1 separation. However, the available steward route did not provide a separate full ancestry assessment, so comparability on all leading axes was not established. The protocol therefore does not support treating the exploratory association scan as a valid final test.

## Discovery association

The exploratory scan used a Bonferroni threshold of 0.002631578947368421 across 19 retained variants. It produced 0 significant variants. The genomic inflation estimate was 1.4823613388985724. The smallest p-value was 0.07620101460687313 for rs030107, which is not significant at the protocol threshold; consequently no discovery hit was nominated.

## Replication

The independent replication batch contained 120 participants, 60 affected and 60 unaffected, but its candidateVariants list was empty because no discovery hit was nominated. Therefore 0 candidates were replicated out of 0 candidates, and no variant-level replication p-value or direction could be computed. This is not evidence that a variant replicated; it means there was nothing eligible to test.

## What caused the stop, what changed, and next action

The immediate cause is participant-level call quality: 31 failures and a fraction of 0.12916666666666668 exceed the 0.1 plate limit. The analysis was changed from a potential final association report to an explicitly exploratory QC/scan record, with no hit nominated and no replication claim. The investigators should re-genotype the plate, rerun participant and variant QC, reassess ancestry on the required leading axes, and only then repeat association testing and nominate candidates for independent replication. Hold the change with the protocol thresholds, released JSON batches, `/workspace/trace.json`, and this report under audit-controlled versioning.
