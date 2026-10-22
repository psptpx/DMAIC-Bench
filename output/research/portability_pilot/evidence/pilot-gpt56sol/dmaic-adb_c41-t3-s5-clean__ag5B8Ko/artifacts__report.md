# Candidate-region association study report

## Executive conclusion

The plate can carry an analysis: **2 of 240** participants failed participant QC, a fail fraction of **0.008333333333333333**, below the re-genotyping boundary of **0.1**. After exclusions, **238** participants remained. Variant QC retained **138 of 150** variants. Genotype PCA found ancestry structure (PC1 case/control p-value **3.4080058932620766e-15**) but the group ranges overlap, so affected and unaffected participants can be compared only with ancestry adjustment. The protocol-compliant PC1-adjusted analysis tested **138** variants and found **0** associations at the Bonferroni threshold **0.00036231884057971015**.

## Quality disposition

The participant call-rate threshold was **0.95**. P011 and P120 each failed and were removed; every other participant was retained. The retained analysis cohort contains **118** affected and **120** unaffected participants. The observed participant call-rate range was **0.9466666666666667** to **1.0**. Because the failure fraction did not exceed **0.1**, re-genotyping is not triggered.

Variant QC applied call rate **0.95**, minor-allele frequency **0.01**, and unaffected-participant HWE p-value **0.000001**. It excluded **12** variants and retained **138**. The excluded variants were:

- call rate: rs050014, rs050071, rs050082, rs050091, rs050108;
- minor-allele frequency: rs050052, rs050092, rs050096, rs050121;
- unaffected-participant HWE: rs050017, rs050019, rs050040.

Thus, the retained variant set is every panel variant except those listed above. The failure categories contain **5**, **4**, and **3** variants, respectively.

## Cohort comparability

PCA used the **238** retained participants and **138** retained variants. PC1 explained **0.0902253366236525** of standardized genotype variance and differed by affection status (Welch statistic **-8.431999923658154**, p-value **3.4080058932620766e-15**), demonstrating structure. Nevertheless, affected and unaffected PC1 score ranges overlap (overlap width **10.238992525458817**), so the protocol's complete-separation stop condition is false. The groups are comparable with PC1 included as an ancestry covariate, not by an unadjusted test.

## Association results and effect of adjustment

The final additive logistic models used genotype dosage plus **1** ancestry covariate. All **138** models converged; **0** models failed. At family-wise alpha **0.05**, the threshold was **0.00036231884057971015**. No variant crossed it. The smallest adjusted p-value was **0.001659485666633129** for rs050022 (odds ratio **2.3835276724837344**, model sample size **233**), which remains above the corrected threshold. Adjusted genomic inflation was **1.144606112920082**.

For diagnosis only, the unadjusted trend analysis had genomic inflation **2.66535720584432** and **22** corrected findings. This reference analysis is not the study conclusion because the protocol requires adjustment when overlapping structure is present.

## What investigators should do next

Do not claim a panel association from this cohort. Preserve the participant and variant exclusion lists, PCA specification, PC1-adjusted model, and Bonferroni rule as the locked analysis record. Treat rs050022 only as a non-significant lead, not a discovery. If additional evidence is sought, use an independently recruited, ancestry-balanced cohort and a prespecified replication analysis; do not relax the present threshold after seeing these results. Continue monitoring ancestry balance and call-rate performance in any new batch, applying the same stop and exclusion rules before testing variants.
