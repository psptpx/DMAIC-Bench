# Candidate-region study status

## Executive conclusion

The genotyping plate passes the protocol's participant-level technical gate after exclusion of **P129**, but the retained discovery cohort cannot support a case-control association conclusion. A leading genotype principal component, **PC2**, completely separates affected from unaffected participants. The protocol explicitly prohibits comparing groups drawn from separate ancestries. I therefore stopped before testing any variant.

There are no valid discovery associations from this cohort, no nominated candidates, and hence no replication result that could support reporting an association. This is a design/comparability failure rather than a plate-wide genotyping failure.

## What was computed

### Participant QC and plate disposition

I calculated each participant's nonmissing genotype call rate across **150** panel variants. The protocol retains participants at call rate **0.95** or greater and requires plate re-genotyping only when the failed fraction exceeds **0.1**.

One participant failed: **P129**. The computed failed-participant fraction was **0.004166666666666667**, so the plate passes and does not trigger re-genotyping. After exclusion, **239** participants remain: **120** affected and **119** unaffected. The retained participant set is every discovery participant other than **P129**.

### Variant QC

Among retained participants, I assessed all **150** variants using call rate, minor-allele frequency, and an exact Hardy-Weinberg test in unaffected participants. The thresholds applied were call rate **0.95**, minor-allele frequency **0.01**, and control Hardy-Weinberg p-value **0.000001**.

A total of **137** variants were retained and **13** failed. The failed variants are:

`rs060002`, `rs060010`, `rs060024`, `rs060037`, `rs060043`, `rs060055`, `rs060083`, `rs060093`, `rs060104`, `rs060111`, `rs060114`, `rs060139`, and `rs060144`.

All panel variants other than those listed above are retained. Full participant- and variant-level audit tables are in `discovery_sample_qc.csv` and `discovery_variant_qc.csv`.

### Cohort comparability

I performed PCA on the **239** retained participants and **137** retained variants, using mean imputation and allele-frequency standardization. PC1 did not distinguish affection groups (p-value **0.46719033046**) and accounted for variance fraction **0.126759885485**. PC2 did distinguish them (p-value **1.07733213653e-140**), accounted for variance fraction **0.0861588908144**, and had range-overlap fraction **0** between affected and unaffected participants.

That complete separation on PC2 is not overlapping structure that can safely be handled merely by adding a covariate. Affection status and ancestry are confounded, so their effects are not identifiable in this discovery cohort.

## Association and replication status

No discovery association scan was run because doing so would violate the protocol's ancestry precondition. Accordingly, no Bonferroni threshold was calculated over tested variants, no variant was declared associated, and no effect estimate was produced.

Replication was not analysed because there are no valid discovery candidates to nominate. It therefore cannot currently support reporting any variant. This is not evidence that a candidate failed replication; the conclusion stops earlier because discovery case-control comparison is invalid.

## Recommended next action and control plan

Do not report an association from this discovery cohort and do not attempt to rescue it by covariate adjustment. Assemble or recollect a discovery cohort in which affected and unaffected participants overlap in ancestry, preferably through ancestry-matched recruitment or matching within ancestry strata. Re-run the locked sequence: participant QC, variant QC, and ancestry assessment before any association test. Only if comparability is established should the retained variants be tested and valid discovery hits advanced to the independent cohort.

Preserve the protocol gates in the analysis pipeline so association code cannot execute unless the plate passes and the ancestry review records an overlapping cohort. Retain the generated QC tables and PC scores as the audit trail for the present stop decision.
