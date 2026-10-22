# Candidate-region association study: final assessment

## Executive conclusion
The plate can support the protocol's association analysis. There is no detected ancestry separation between affected and unaffected participants on this panel. **No variant is declared associated.** This is a negative panel result, not proof that the metabolic trait lacks a genetic basis or that smaller effects are absent.

## Quality and retention
All 240 participants pass the call-rate requirement of 0.95; 0 fail (failure fraction 0.0). This does not exceed the re-genotyping trigger of 0.1. No plate replacement was required. All participant identifiers in `participant_qc.csv` are retained, with their measured call rates. The retained cohort comprises 120 affected and 120 unaffected participants.

Of 150 variants, 10 are removed and 140 retained. Variant QC was calculated after participant QC, using observed calls: call rate at least 0.95, pooled minor-allele frequency at least 0.01, and exact conditional Hardy–Weinberg probability in unaffected participants at least 1e-06. Failures comprise 5 for call rate, 3 for frequency and 2 for Hardy–Weinberg equilibrium. These are exclusion reasons, not established biological or laboratory causes.

Excluded variants: rs040038, rs040054, rs040057, rs040072, rs040104, rs040106, rs040110, rs040112, rs040113, rs040125.

Retained variants: rs040001, rs040002, rs040003, rs040004, rs040005, rs040006, rs040007, rs040008, rs040009, rs040010, rs040011, rs040012, rs040013, rs040014, rs040015, rs040016, rs040017, rs040018, rs040019, rs040020, rs040021, rs040022, rs040023, rs040024, rs040025, rs040026, rs040027, rs040028, rs040029, rs040030, rs040031, rs040032, rs040033, rs040034, rs040035, rs040036, rs040037, rs040039, rs040040, rs040041, rs040042, rs040043, rs040044, rs040045, rs040046, rs040047, rs040048, rs040049, rs040050, rs040051, rs040052, rs040053, rs040055, rs040056, rs040058, rs040059, rs040060, rs040061, rs040062, rs040063, rs040064, rs040065, rs040066, rs040067, rs040068, rs040069, rs040070, rs040071, rs040073, rs040074, rs040075, rs040076, rs040077, rs040078, rs040079, rs040080, rs040081, rs040082, rs040083, rs040084, rs040085, rs040086, rs040087, rs040088, rs040089, rs040090, rs040091, rs040092, rs040093, rs040094, rs040095, rs040096, rs040097, rs040098, rs040099, rs040100, rs040101, rs040102, rs040103, rs040105, rs040107, rs040108, rs040109, rs040111, rs040114, rs040115, rs040116, rs040117, rs040118, rs040119, rs040120, rs040121, rs040122, rs040123, rs040124, rs040126, rs040127, rs040128, rs040129, rs040130, rs040131, rs040132, rs040133, rs040134, rs040135, rs040136, rs040137, rs040138, rs040139, rs040140, rs040141, rs040142, rs040143, rs040144, rs040145, rs040146, rs040147, rs040148, rs040149, rs040150.

`variant_qc.csv` provides the individual call rates, frequencies, control equilibrium probabilities and retention decisions.

## Cohort comparability
Before association testing, missing calls were mean-imputed solely for ancestry PCA, with markers centered and scaled by allele-frequency variance. The leading-axis Welch comparison gives p = 0.89905. The leading axis explains a variance fraction of 0.0209856. Its observed ranges overlap: unaffected [-4.52393, 4.1911], affected [-3.50883, 4.92473]. Other inspected leading axes also showed no phenotype imbalance. Thus there is no detected ancestry barrier to comparison, and no ancestry covariates were introduced.

This is a panel-based check, not definitive ancestry certification; a candidate-region panel can miss population structure and linkage can distort its axes. Broad ancestry markers would strengthen a replication study.

## Association results
A two-sided additive Cochran–Armitage trend test was run on called genotypes separately for every retained variant, using conditional finite-sample null variance and chi-square tail probabilities. Missing calls were excluded from association tests, not imputed. The Bonferroni cutoff is 0.000357142857143. Significant variants: 0. Genomic inflation factor is 0.890376, with no evidence of global inflation by this diagnostic.

The smallest probability is 0.020882, at rs040084, well above the corrected cutoff. No nominal finding should be promoted as an association. Full test statistics, probabilities and called sample counts are in `association.csv` and in the trace.

## Actions and sustainment
The completed change was analytical filtering of unsuitable variants; it yielded a quality-screened, comparable cohort and a valid negative panel-level result. No laboratory remediation or recruitment change was implemented, and no improvement in disease prediction has been demonstrated.

Investigators should retain the negative result, avoid causal or clinical claims, and pursue independent replication or a better-powered, broader study if the biological question remains important. Review failed variant assays and equilibrium departures before reuse. Pre-specify power targets, ancestry assessment, covariates and multiplicity handling in the follow-up protocol; power was not calculated here because a target effect and follow-up design were not supplied.

Hold the result by freezing the released data, QC rules, retention manifests, scripts and association table; rerun these same checks on future plates and stop when protocol gates fail. No steward batch was denied, and no missing-data gap was substituted with an invented result. The conclusions remain limited to these participants and tested variants.
