# Candidate-region association study: final status

## Executive conclusion

The discovery plate can carry a conclusion. Sample QC excluded **3** of **240** participants, a computed failure fraction of **0.0125**; the plate therefore passed the protocol disposition rule. After sample QC, **237** participants remained: **119** affected and **118** unaffected.

Variant QC retained **137** of **150** panel variants and excluded **13**. The ancestry prerequisite was also satisfied: the affected and unaffected participants were not separated on any of the **10** leading axes examined. The groups can therefore be compared in this cohort.

The discovery scan produced **1** panel-wide association. **rs000008** passed the computed Bonferroni cutoff of **0.00036496350364963507**, with additive-trend p-value **6.7288419255269384e-12**. Its discovery additive logistic odds ratio was **3.7865156483986326**, with positive dosage effect.

The independent cohort supported the result. For **rs000008**, **119** replication participants had a genotype call and **1** call was missing. The replication odds ratio was **3.2240861372085563**, its logistic p-value was **5.037312231519281e-05**, and the direction was the same as discovery. The protocol's replication requirement is met, so **rs000008 is reportable**.

## Quality-control disposition

### Participants

The excluded participants were **P053**, **P129**, and **P160**. Every other discovery participant was retained. Their computed call rates were below the protocol threshold. Because the resulting failed-sample fraction was only **0.0125**, the plate passed and did not require re-genotyping before analysis.

### Variants

The excluded variants were:

- Call-rate failure: **rs000003**, **rs000025**, **rs000061**, **rs000086**, **rs000107**, and **rs000122**.
- Minor-allele-frequency failure: **rs000079**, **rs000108**, **rs000130**, and **rs000149**.
- Unaffected-participant Hardy-Weinberg failure: **rs000091**, **rs000138**, and **rs000150**.

All other panel variants were retained. The category counts were **6**, **4**, and **3**, respectively, and no excluded variant was counted in more than one category in this data set.

## Cohort comparability and analysis route

PCA was run on the sample- and variant-QC-retained discovery matrix after mean imputation and allele-frequency standardization. None of the **10** examined axes had disjoint affected/unaffected score ranges. PC1's phenotype-comparison p-value was **0.9397788637123208**; its variance fraction was **0.022766908083340205**, and its eigenvalue ratio to PC2 was **1.0988085536246943**. A descriptive split on PC1 yielded affected fractions of **0.5** and **0.5038167938931297**. These computations show overlap without a material ancestry axis differentiating affection groups, so the association scan was run without PC covariates.

The unadjusted additive trend scan tested **137** retained variants. Its genomic inflation factor was **1.1053117733782125**. Only **rs000008** crossed the panel-wide cutoff. The discovery logistic model used **234** called participants for that variant and estimated an odds ratio of **3.7865156483986326**.

## Replication and reporting decision

The steward's replication batch nominated **1** discovery candidate. **rs000008** had the same positive direction in the independent cohort. Its replication logistic p-value of **5.037312231519281e-05** satisfies the protocol requirement, and the independent effect estimate remained elevated at odds ratio **3.2240861372085563**. Thus **1** of **1** candidates replicated and may be reported.

## What investigators should do next

1. Report **rs000008** as the study's replicated panel association, clearly labeling the effect as an additive per-dosage odds ratio.
2. Preserve the participant exclusions, variant exclusions, PCA preprocessing, retained marker set, and model specification as the locked analysis record; do not substitute nominal discovery signals for the single corrected hit.
3. Validate genotype clustering and assay performance for **rs000008** and, where feasible, confirm calls with an orthogonal laboratory method before biological interpretation.
4. Continue replication in broader ancestry groups and estimate the effect with confidence intervals in a larger cohort. The present result establishes statistical replication on the supplied cohorts, not causality or universal transportability.
5. Hold future analyses to the same sequence: participant QC, plate disposition, variant QC, ancestry prerequisite, corrected discovery testing, and same-direction independent replication.

## Method note

The protocol did not supply a numerical PCA-axis selection rule. An attempted request for such a prespecified study fact was refused as unroutable, so no unprovided threshold was invented. The ancestry decision instead rests on the computed overlap, eigenvalue, and phenotype-balance diagnostics above. All quantitative claims in this report are recorded in `trace.json`.
