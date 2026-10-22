# Candidate-region association study: decision report

## Executive decision

The discovery plate can carry an analysis. Sample QC failed **2** participants, a failure fraction of **0.008333333333333333**, so the plate-stop rule was not triggered. After QC, **238** participants and **139** variants remained. Affected and unaffected participants can be compared only with ancestry adjustment because PC1 shows structure but the group score ranges overlap.

The adjusted discovery scan found **1** association, **rs020008**. The independent cohort confirmed it in the same direction, so **rs020008 may be reported**.

## Quality disposition

The input contained **240** participants and **150** variants. **P017** and **P111** failed participant call-rate QC and were removed, leaving **118** affected and **120** unaffected participants. The minimum observed participant call rate was **0.9466666666666667**.

Variant QC failed **11** variants and retained **139**. The failed variants were:

- call rate: **rs020001, rs020016, rs020084, rs020114, rs020142**
- minor-allele frequency: **rs020037, rs020045, rs020054, rs020072**
- unaffected-participant Hardy-Weinberg equilibrium: **rs020085, rs020117**

The respective failure counts were **5**, **4**, and **2**. Every other supplied panel variant was retained.

## Cohort comparability

PC1 differed between groups with p = **4.195269044230135e-18** and explained **0.10170125571851292** of standardized genotype variance. The score ranges were not separated: **111** affected and **117** unaffected participants lay in their common interval. The additive logistic models therefore included PC1.

The study lead had no separately recorded fact specifying a larger fixed PC count. The analysis used the leading axis on which structure was detected rather than inventing an unavailable rule.

## Discovery association

The scan tested **139** retained variants using two-sided coefficient Wald tests. The Bonferroni threshold was **0.00035971223021582735**, and genomic inflation was **0.9939606416195177**.

- **rs020008:** p = **4.374607422729442e-05**; per-allele odds ratio = **2.626313844354682**; called in **235** retained participants.
- **rs020065:** p = **0.0004180873430676656**; per-allele odds ratio = **0.40406039638668273**; called in **236** retained participants. It did not cross the corrected threshold and is not a discovery association.

## Independent replication

The replication manifest contained **1** candidate. For **rs020008**, **119** participants had calls and **1** call was missing. The replication Wald p-value was **0.0006966849454034404**, the odds ratio was **2.729997712702792**, and the effect direction matched discovery. Thus **1** candidate replicated and the protocol permits reporting rs020008.

## Recommended next actions

- Report **rs020008** as the replicated panel association, with the QC exclusions and PC1 adjustment disclosed.
- Do not report **rs020065** as associated.
- Lock the participant exclusions, variant exclusions, PCA construction, PC1-adjusted logistic model, Wald test, and replication rule in the reproducible analysis record.
- Prespecify an exact ancestry-axis selection rule in the next protocol revision.
