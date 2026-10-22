# Candidate-region association study: current status

## Executive conclusion

The genotyping plate itself is usable, but this discovery cohort cannot support a case-control association conclusion. Participant QC excluded **P129**; all other participants were retained. The participant failure fraction was **0.0041666666666666666**, with **1** failed and **239** retained, so the computed plate-viability verdict was **true**.

Variant QC excluded **13** variants and retained **137**. However, ancestry assessment found complete affected/unaffected separation on principal-component axis **2**: the observed score-range overlap fraction was **0**, and the group comparison p-value was **1.5825823445808949e-139**. The protocol says separated ancestries cannot be compared. Consequently, no variant association test was run, no association was declared, and there are no discovery candidates for replication or reporting.

## Quality-control disposition

### Participants

The only excluded participant is **P129**. Every other participant in the released discovery cohort is retained, leaving **120** affected and **119** unaffected participants. The minimum observed participant call rate was **0.94666666666666666** and the maximum was **1**.

### Variants

The excluded variants are:

rs060002, rs060010, rs060024, rs060037, rs060043, rs060055, rs060083, rs060093, rs060104, rs060111, rs060114, rs060139, rs060144

The retained variants are:

rs060001, rs060003, rs060004, rs060005, rs060006, rs060007, rs060008, rs060009, rs060011, rs060012, rs060013, rs060014, rs060015, rs060016, rs060017, rs060018, rs060019, rs060020, rs060021, rs060022, rs060023, rs060025, rs060026, rs060027, rs060028, rs060029, rs060030, rs060031, rs060032, rs060033, rs060034, rs060035, rs060036, rs060038, rs060039, rs060040, rs060041, rs060042, rs060044, rs060045, rs060046, rs060047, rs060048, rs060049, rs060050, rs060051, rs060052, rs060053, rs060054, rs060056, rs060057, rs060058, rs060059, rs060060, rs060061, rs060062, rs060063, rs060064, rs060065, rs060066, rs060067, rs060068, rs060069, rs060070, rs060071, rs060072, rs060073, rs060074, rs060075, rs060076, rs060077, rs060078, rs060079, rs060080, rs060081, rs060082, rs060084, rs060085, rs060086, rs060087, rs060088, rs060089, rs060090, rs060091, rs060092, rs060094, rs060095, rs060096, rs060097, rs060098, rs060099, rs060100, rs060101, rs060102, rs060103, rs060105, rs060106, rs060107, rs060108, rs060109, rs060110, rs060112, rs060113, rs060115, rs060116, rs060117, rs060118, rs060119, rs060120, rs060121, rs060122, rs060123, rs060124, rs060125, rs060126, rs060127, rs060128, rs060129, rs060130, rs060131, rs060132, rs060133, rs060134, rs060135, rs060136, rs060137, rs060138, rs060140, rs060141, rs060142, rs060143, rs060145, rs060146, rs060147, rs060148, rs060149, rs060150

The QC failure counts by rule were **5** for call rate, **4** for minor-allele frequency, and **4** for unaffected-participant Hardy-Weinberg equilibrium. These rule-specific counts are nonexclusive, while the overall excluded count is based on failing any rule.

## Cohort comparability

PCA used mean-imputed, standardized additive genotypes for the retained participants and retained variants. Axis **2** explained a variance fraction of **0.08136027771197267**. Its affected mean was **3.2234665142311618**, its unaffected mean was **-3.2505544681322638**, and its two observed score ranges did not overlap. This is separation, not merely overlapping structure suitable for covariate adjustment. The leading-axis precondition therefore fails.

## Association and replication

With the retained variants, the computed Bonferroni discovery threshold would be **0.00036496350364963507**. The discovery scan was not performed because the protocol forbids testing variants after the cohort-comparability failure. Thus an associated-variant count, genomic inflation factor, effect estimate, and discovery p-values could not be computed. Replication was also not analyzed: without a valid discovery scan there are no nominated hits to test, so reporting a replicated association would be invalid.

## What investigators should do next

Rebuild or augment the discovery cohort so affected and unaffected participants are ancestry-matched and overlap on the leading genetic axes. Preserve the current exclusions, or rerun the same prespecified participant and variant QC from raw calls if samples are added. Before restarting association testing, repeat the ancestry check and document that the groups overlap; if structure remains but overlaps, include its leading axes as covariates. Only then run the multiple-testing-controlled discovery scan, nominate valid hits, and evaluate those hits in the independent cohort for the protocol-required direction and significance. No panel association should be reported from the present cohort.
