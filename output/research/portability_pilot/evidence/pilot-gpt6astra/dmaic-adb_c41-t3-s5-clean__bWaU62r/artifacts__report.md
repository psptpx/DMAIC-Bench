# Study disposition

## Executive conclusion
The plate can support a qualified, ancestry-adjusted case–control analysis; it does not require wholesale re-genotyping under the protocol. No variant meets the retained-panel association threshold. This is absence of demonstrated association, not evidence that the panel has no biological effects.

## Quality and retained material
From 240 participants and 150 variants, 2 participants failed the call-rate rule (failure fraction 0.00833333). Retain 238 participants: 118 affected and 120 unaffected. Exclude **P011 and P120**; every other supplied participant is retained. The failure fraction is below the protocol's plate-rework limit.

Variant QC was calculated after participant filtering. Call rate used observed calls; minor-allele frequency used the retained cohort; Hardy–Weinberg equilibrium used a two-sided exact test in unaffected participants only. There were 12 failed variants, leaving 138. Failures comprised 5 call-rate failures, 4 minor-allele-frequency failures and 3 equilibrium failures.

Exclude **rs050014, rs050017, rs050019, rs050040, rs050052, rs050071, rs050082, rs050091, rs050092, rs050096, rs050108 and rs050121**. Every other supplied variant is retained. `sample_qc.tsv` and `variant_qc.tsv` provide the complete identity-level decisions and measurements.

## Can the groups be compared?
Genotype-based ancestry assessment preceded association testing. Missing calls were mean-imputed for PCA only, and dosages were centered and scaled by allele-frequency variance. The leading axis accounts for a variance fraction of 0.0902253. A Welch comparison of affected versus unaffected scores gives p = 3.40801e-15, indicating strong group imbalance in genetic structure.

However, the groups are not separately confined on this axis: unaffected scores span −5.10707 to 5.36721 and affected scores span −4.87178 to 5.96628. Thus the observed structure overlaps rather than creating complete ancestry separation. The appropriate route is adjustment, not an unadjusted comparison or a declaration that the groups are wholly incomparable.

These are inferred genetic axes, not validated ancestry labels. A candidate-region panel is a limited basis for establishing ancestry and may reflect local linkage or trait-related variation. The overlapping ranges support the chosen route but do not establish that all possible confounding is removed. No external ancestry batch was obtained: that request was unroutable, not a denial of the available genotype evidence.

## Association result
Additive logistic regression compared each variant model against a covariate-only model using likelihood-ratio tests. Both models included the leading 5 genotype principal components; this was an analyst-selected adjustment, not a protocol-specified dimension. Missing calls were omitted separately for each association test rather than imputed.

The Bonferroni threshold over retained variants is **0.000362319**. There are **0 significant variants**; the smallest adjusted-model p-value is **0.00443013**. Genomic-control lambda from the median likelihood-ratio statistic is **1.13720**. This is a calibration diagnostic, not proof that adjustment eliminated confounding; no genomic-control rescaling was applied. Full results are in `association.tsv`.

## What changed, what it achieved, and next actions
The analytical changes were removal of low-quality participants and variants, followed by ancestry-covariate adjustment. Filtering produced the retained cohort and panel above. Adjustment allowed a conditional comparison despite ancestry imbalance, and that comparison did not establish any panel-wide association. No wet-lab intervention or prospective validation was performed; improvement relative to an unadjusted test was not quantified because an unadjusted association analysis was not run.

Investigators should not advance any variant as a confirmed association from this run. Obtain independent genome-wide ancestry markers or validated ancestry metadata, inspect group overlap jointly across the leading axes, and assess relatedness and technical covariates. Reassess robustness to ancestry-axis choice and local linkage before treating this as a definitive negative study. Plan independent replication and prospective power assessment for scientifically meaningful effects; neither replication nor power was established here.

Hold the result through a frozen protocol, retained-ID manifests, archived steward batches, executable `analyze.py`, and the numerical audit trail in `trace.json`. Apply the same pretest QC and ancestry gates to subsequent batches. Investigate excluded calls with the laboratory, but do not replace the entire plate solely on the observed failure fraction. Any future laboratory changes must be followed by fresh QC rather than assumed to have worked.
