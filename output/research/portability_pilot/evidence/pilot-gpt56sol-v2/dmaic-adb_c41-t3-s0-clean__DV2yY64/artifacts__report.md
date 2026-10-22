# Candidate-region association study report

## Executive conclusion

The discovery plate can carry an analysis: **3** participants failed call-rate QC, a failure fraction of **0.0125**, and **237** were retained. After variant QC, **137** variants were retained and **13** were excluded. The retained affected and unaffected participants can be compared because no separate-ancestry split was established on the inspected leading axes.

The discovery scan produced **1** Bonferroni-significant candidate, **rs000008**. Its trend-test p-value was **5.253540318605901e-11**, and its discovery per-allele odds ratio was **3.7865156743439763**. Independent replication supports reporting: its p-value was **1.7973641155483908e-05**, its per-allele odds ratio was **3.224088318489**, and same-direction status was **true**.

## Quality and cohort disposition

Participant QC used the protocol call-rate rule. The excluded participants were **P053**, **P129**, and **P160**. The retained set is every supplied participant other than those three, comprising **119** affected and **118** unaffected participants. The observed failure fraction remained below the plate stop rule, so re-genotyping was not triggered.

Variant QC applied all protocol criteria after participant filtering: call rate, pooled minor-allele frequency, and exact Hardy–Weinberg testing among unaffected participants. **6** variants failed call rate, **4** failed minor-allele frequency, and **3** failed control Hardy–Weinberg criteria; these criterion counts yield **13** excluded variants in this data. The excluded variants were **rs000003, rs000025, rs000061, rs000079, rs000086, rs000091, rs000107, rs000108, rs000122, rs000130, rs000138, rs000149, and rs000150**. The retained set is every supplied panel variant other than those listed.

## Ancestry precondition

PCA was computed by singular-value decomposition after mean imputation and allele-frequency scaling on the QC-retained data. The released protocol did not prescribe an axis-count rule, and a request for one was refused as a request for methodological choice; the analysis therefore inspected the leading axes specified in the trace. **10** leading axes were inspected. Affected and unaffected score ranges overlapped on every axis. PC1 had p-value **0.939778863712323**; the smallest axis p-value was **0.02659641854927208**, whose correction across the inspected axes was **0.2659641854927208**. Separate ancestries were therefore not established, and unadjusted trend testing was used.

## Discovery

The additive trend scan tested **137** variants. The computed Bonferroni threshold was **0.00036496350364963507**. Genomic inflation was **1.115940928253286**. Only **rs000008** crossed the threshold, with **234** nonmissing discovery participants and trend chi-square **43.08041958041958**.

## Replication and reporting decision

The independent batch nominated **1** discovery candidate. For **rs000008**, **119** replication participants had genotype calls, comprising **59** affected and **60** unaffected participants. The replication trend chi-square was **18.392794104592795**. The protocol requires p-value below **0.05** and the same effect direction. The candidate replicated status was **true**, so **1** of **1** candidates met both conditions.

## Recommended action and control

The association may be reported with discovery and replication results clearly separated. Preserve the participant and variant exclusion lists, the ancestry check, the retained-variant multiplicity denominator, and the independent replication gate as the locked analysis record. Future analyses should rerun the same scripted QC and ancestry precondition before testing variants.
