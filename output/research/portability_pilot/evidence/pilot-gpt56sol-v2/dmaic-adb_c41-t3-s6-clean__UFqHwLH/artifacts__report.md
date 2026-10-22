# Study status report

## Executive conclusion

The discovery plate can proceed through technical QC: **1** participant failed, for a failed fraction of **0.004166666666666667**, and **239** participants remained. It cannot, however, carry an affection-association conclusion. The ancestry analysis found complete case/control separation on axis **2**. Under the protocol, these affected and unaffected participants cannot be compared, so no variant association test was run and no variant can be declared associated from this cohort.

The independent-cohort release contains **0** nominated discovery candidates and **0** recorded discovery directions. Consequently, no candidate-level replication test was possible. The value **0** for replicated candidates means there were no candidates to evaluate; it is not evidence that a tested association failed replication.

## Participant QC and plate disposition

Call rate was computed from all released genotype cells for each participant. **P129** had call rate **0.9466666666666667** and was excluded. Every other released discovery participant was retained. This leaves **120** affected and **119** unaffected participants. Because the computed failed fraction was **0.004166666666666667**, below the protocol's plate limit of **0.1**, re-genotyping the whole plate is not triggered.

## Variant QC

After removing P129, variant call rate, pooled minor-allele frequency, and an exact Hardy-Weinberg test among retained unaffected participants were computed. **137** variants passed all rules and **13** failed at least one. Criterion-specific failure counts were **5** for call rate, **4** for minor-allele frequency, and **4** for control Hardy-Weinberg equilibrium.

Excluded variants: rs060002, rs060010, rs060024, rs060037, rs060043, rs060055, rs060083, rs060093, rs060104, rs060111, rs060114, rs060139, rs060144.

Retained variants: rs060001, rs060003, rs060004, rs060005, rs060006, rs060007, rs060008, rs060009, rs060011, rs060012, rs060013, rs060014, rs060015, rs060016, rs060017, rs060018, rs060019, rs060020, rs060021, rs060022, rs060023, rs060025, rs060026, rs060027, rs060028, rs060029, rs060030, rs060031, rs060032, rs060033, rs060034, rs060035, rs060036, rs060038, rs060039, rs060040, rs060041, rs060042, rs060044, rs060045, rs060046, rs060047, rs060048, rs060049, rs060050, rs060051, rs060052, rs060053, rs060054, rs060056, rs060057, rs060058, rs060059, rs060060, rs060061, rs060062, rs060063, rs060064, rs060065, rs060066, rs060067, rs060068, rs060069, rs060070, rs060071, rs060072, rs060073, rs060074, rs060075, rs060076, rs060077, rs060078, rs060079, rs060080, rs060081, rs060082, rs060084, rs060085, rs060086, rs060087, rs060088, rs060089, rs060090, rs060091, rs060092, rs060094, rs060095, rs060096, rs060097, rs060098, rs060099, rs060100, rs060101, rs060102, rs060103, rs060105, rs060106, rs060107, rs060108, rs060109, rs060110, rs060112, rs060113, rs060115, rs060116, rs060117, rs060118, rs060119, rs060120, rs060121, rs060122, rs060123, rs060124, rs060125, rs060126, rs060127, rs060128, rs060129, rs060130, rs060131, rs060132, rs060133, rs060134, rs060135, rs060136, rs060137, rs060138, rs060140, rs060141, rs060142, rs060143, rs060145, rs060146, rs060147, rs060148, rs060149, rs060150.

## Cohort comparability

PCA used the retained participants and variants after mean imputation and variance standardization. Axis **2** differed by affection status with p-value **1.5825823445808949e-139** and standardized mean difference **7.881556702053639**. More importantly for the protocol's separation rule, affected scores ranged from **1.4900730951609422** to **4.952154918194459**, while unaffected scores ranged from **-5.441281072629988** to **-0.27231576013549713**. Those ranges do not overlap.

This is not the protocol's “overlapping structure” branch in which leading axes can simply be included as covariates. Affection status is confounded with ancestry, so adjustment cannot identify a within-ancestry affection effect in this discovery cohort. Association testing therefore stops at this precondition. No discovery p-values, odds ratios, genomic-inflation estimate, or Bonferroni hits were computed.

## Replication and reporting decision

The replication data were released, but their nominated-candidate list is empty. Because the discovery scan was prohibited, there is no valid discovery association to carry into the independent cohort. Thus replication does not support reporting any association, and it also cannot refute a specific candidate because none was tested.

## Recommended next actions and control plan

- Do not report a panel association from the present discovery comparison.
- Preserve the QC exclusions: remove P129 and the listed failed variants from any legitimate reanalysis of this plate.
- Redesign recruitment or sampling so affected and unaffected participants overlap within ancestry strata. Prefer matched recruitment and verify overlap on ancestry axes before unblinding or testing variants.
- If suitable within-ancestry case/control subsets can be formed, reassess sample and variant QC, repeat the ancestry gate, and only then run ancestry-adjusted association tests.
- Nominate only protocol-significant discovery findings to the independent cohort. For each nomination, prerecord the discovery direction and evaluate the independent result under the protocol's same-direction requirement.
- Hold the study at the ancestry gate in future runs: archive participant/variant QC tables, PCA range diagnostics, the association model specification, and the final nomination list before replication analysis.
