# Metabolic-trait candidate-panel study report

## Executive conclusion

The discovery plate can carry a conclusion. The discovery sample-failure fraction was **0.0125**, below the protocol limit of **0.1**, so the plate was not stopped. After participant and variant QC, **237** discovery participants and **138** variants were retained. The affected and unaffected groups each contained **120** participants before QC, so the planned case-control comparison was represented in the released cohort; QC was applied before association testing.

One retained variant, **rs000008**, crossed the Bonferroni threshold of **0.00036231884057971015**. Its discovery p-value was **5.653541578182578e-11**, with odds ratio **0.6082673362951516**. The discovery scan therefore nominated **1** hit.

The independent replication tested **1** nominated candidate. The candidate call rate was **0.9916666666666667**. Replication p-value was **9.684803104789346e-05**, below the replication threshold of **0.05**, and the replication odds ratio was **0.296070460704607**, in the same below-1 direction as discovery. Thus **1** of **1** nominated candidates replicated and rs000008 is supportable for reporting under the supplied protocol.

## What was retained and why

The discovery batch contained **240** participants and **150** panel variants. **3** participants failed the participant call-rate threshold of **0.95**; **237** were retained. Variant QC retained **138** variants. The excluded-criterion counts were **5** for call rate, **4** for MAF, and **4** for control HWE; these criterion counts can overlap and are not summed as a unique-exclusion count.

The protocol thresholds were participant call rate **0.95**, variant call rate **0.95**, MAF **0.01**, and unaffected-control HWE p-value **1e-06**. The plate failure limit was **0.1**. The replication cohort contained **120** participants, with **60** affected and **60** unaffected; **2** failed its sample call-rate check, a fraction of **0.016666666666666666**.

## Association and replication

The discovery association analysis used the retained samples and variants and produced **1** Bonferroni-significant result. The genomic inflation estimate was **1.563144496896257**, so the scan should be interpreted with the observed QC context and not as evidence that every panel marker is reliable.

Replication confirmed the nominated result statistically and directionally. The replication cohort had **60** affected and **60** unaffected participants, and rs000008 had call rate **0.9916666666666667**. The result meets the protocol rule of p below **0.05** with matching direction.

## Business interpretation and next actions

The change made was to apply the steward's numeric QC rules before association testing, use the retained-variant Bonferroni threshold, and require an independent same-direction replication. The change achieved a defensible reportable result: one discovery hit survived correction and was supported in the independent cohort.

Investigators should report rs000008 as the replicated candidate-panel association, including its discovery and replication effect estimates and p-values. They should not generalize the result to variants removed by QC or to untested claims beyond this candidate panel. Before publication, archive the exact genotype/QC manifests and analysis code represented by this trace, preserve the protocol thresholds as the analysis contract, and rerun the locked workflow if additional samples or variants are added.
