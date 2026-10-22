# Candidate-region case-control study report

## Executive conclusion

The plate can carry an analysis: **2** participants failed sample QC, a failure fraction of **0.0083333333**, below the plate stop limit of **0.1**. After exclusions, **238** participants remained: **118** affected and **120** unaffected.

The cohort has ancestry structure associated with affection status, but the observed ancestry-score ranges overlap. Affected and unaffected participants therefore are not completely separated and can be compared only with ancestry adjustment. In the primary adjusted analysis, **0** variants met the corrected significance criterion. This run provides no panel-wide significant association claim.

## Participant QC and plate disposition

Participant call rate was computed across **150** panel variants and compared with the retention threshold of **0.95**. **P011** and **P120** failed; each had call rate **0.9466666667**. Every other participant was retained. Because the plate-level failure fraction was **0.0083333333**, below **0.1**, the protocol does not trigger plate re-genotyping.

## Variant QC

Variant QC used **238** retained participants, including **120** unaffected participants. Of **150** panel variants, **138** passed all protocol criteria and **12** failed. Failure counts were **5** for call rate, **4** for minor-allele frequency, and **3** for exact Hardy-Weinberg testing among unaffected participants.

The excluded variants were: rs050014, rs050017, rs050019, rs050040, rs050052, rs050071, rs050082, rs050091, rs050092, rs050096, rs050108, rs050121.

The retained variant set is every panel variant other than those listed above. Applied thresholds were call rate **0.95**, minor-allele frequency **0.01**, and unaffected-participant Hardy-Weinberg p-value **0.000001**.

## Cohort comparability

PCA used mean-imputed, standardized dosages for the **138** retained variants. The initial software-dependent attempt failed without producing a result; PCA was then successfully recomputed by singular-value decomposition.

PC1 explained **0.0804114332** of genotype variance. Its affected-versus-unaffected Welch statistic was **-8.4059792021**, with p-value **4.040363200998719e-15**. The observed PC1 ranges overlapped by **9.6257596445**, so complete separation was false. This supports an adjusted comparison, not an unadjusted test. The study lead declined to prescribe a method; because PC1 was the dominant phenotype-associated ancestry axis, the primary model adjusted for **1** axis. A model with **5** axes was retained as a sensitivity analysis.

## Association analysis

Each retained variant was tested additively by logistic regression. Bonferroni correction over **138** retained variants at family-wise alpha **0.05** gave a threshold of **0.000362318841**. In the primary PC1-adjusted model, **0** variants passed and the genomic inflation factor was **1.2102866267**. In the **5**-axis sensitivity model, **0** variants passed and the genomic inflation factor was **1.1974436660**. The association conclusion is unchanged. Because residual inflation remains in both models, the result should be described as no detected association, not proof of no genetic effect.

## Actions and control plan

1. Keep **P011** and **P120** excluded unless their genotypes are regenerated and they independently pass the same participant call-rate rule.
2. Freeze the **138**-variant QC set and participant exclusions as the reproducible analysis cohort; preserve the scripts and JSON result files.
3. Review ancestry modeling and relatedness with validated ancestry information before treating the null panel result as definitive, because the primary genomic inflation factor is **1.2102866267**.
4. If genotype regeneration or cohort composition changes, rerun participant QC, variant QC, PCA, and multiplicity correction from the beginning; do not reuse the current threshold automatically.
5. No variant should advance as associated from this analysis. Check any future signal in an independent cohort under a predeclared ancestry-adjusted model.
