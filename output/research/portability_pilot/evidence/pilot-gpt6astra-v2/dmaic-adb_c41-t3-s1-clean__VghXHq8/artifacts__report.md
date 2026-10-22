# Study status: stop before association testing

## Executive decision
The plate clears the participant-quality gate, but this discovery cohort cannot carry a variant–trait conclusion. Affection status is completely separated on the leading genotype ancestry axis. Under the released protocol, affected and unaffected participants from separate ancestry distributions must not be compared. An adjusted association model would not restore the missing ancestry overlap.

## Quality review and retained records
Computed call rates on the discovery matrix identified 2 failed participants among 240 (failure fraction 0.0083333333). This does not trigger protocol-mandated plate re-genotyping. Exclude P039, P197. All other participants are retained: 238 total, comprising 119 affected and 119 unaffected.

Variant QC was recomputed after participant removal, using observed-call allele frequencies and an exact two-sided Hardy–Weinberg test in unaffected participants. There were 12 exclusions and 138 retained variants. Failure reasons were call rate for 5 variants, minor-allele frequency for 4, and control Hardy–Weinberg equilibrium for 3.

Excluded variants: rs010047, rs010057, rs010063, rs010072, rs010088, rs010092, rs010101, rs010118, rs010128, rs010133, rs010141, rs010149. Every other variant in the released panel is retained. The complete named inclusion/exclusion manifests, call rates, allele frequencies and equilibrium results are in `sample_qc.csv` and `variant_qc.csv`.

## Comparability assessment
PCA used retained variants, mean imputation for missing calls, and allele-frequency standardization. The leading axis explains 0.0942773035 of standardized genotype variance. Its affection-group Welch-test p-value is 3.654069761e-129. More importantly, the observed ranges do not overlap: affected participants range from -5.8992083373 to -1.4849274644, while unaffected participants range from 0.3046885632 to 6.7376167676. The signed overlap is -1.7896160275; a negative value denotes a gap. Other leading axes were also checked and their contrasts and overlap statistics are in the trace.

This is not merely modest population structure that can be addressed by adding ancestry covariates. The discovery comparison has no shared support on its dominant ancestry axis. Genotype PCA alone cannot name the ancestry populations or establish the recruitment cause; those facts have not been established here. A small candidate panel also limits broad ancestry characterization, so independent ancestry markers and recruitment records should confirm the operational diagnosis.

## Association and replication
No variant association tests or effect estimates were run, because the required comparability precondition failed. There are no valid nominated discovery hits; this is not a finding of no genetic association. Independent replication was not requested or analysed, since replication of an invalid discovery comparison would not cure its design problem. Replication support and reportable associations are therefore not established. No data request was denied.

## Actions, achieved change, and control plan
QC removed poor-quality participants and variants and produced explicit audit manifests. That improved analytic quality but did not resolve ancestry–affection confounding. Stop the scan and do not publish variant claims from this cohort. The investigators should review ancestry and recruitment sources, confirm the genotype structure with a suitable independent marker set, and recruit ancestry-matched affected and unaffected participants with shared ancestry support. Balance recruitment and processing within ancestry groups rather than relying on extrapolation from disjoint groups.

Freeze the protocol and inclusion manifests; retain the scripts and trace as the audit record. Before reopening testing, repeat participant QC, variant QC, and leading-axis overlap checks on the redesigned cohort. Use ancestry-adjusted tests only where structure has genuine overlap, apply the protocol's retained-panel multiplicity correction, and require independent same-direction replication before reporting any discovery association. No recruitment or laboratory change has yet been implemented or validated in this task.
