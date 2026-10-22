# Study disposition: stop before association testing

## Executive conclusion
The plate passes the protocol's technical sample-quality gate, but **this cohort cannot support a valid affected-versus-unaffected association conclusion**. Retained participants separate completely by affection status along the leading genotype-derived ancestry axis. Under the protocol, this is a design/comparability failure, not a problem that can simply be fixed by adding ancestry covariates.

No variant association tests were run. No associated variant can be declared, and this must not be interpreted as evidence that no variant is associated. Association p-values, effect sizes, and genomic inflation were not computed.

## What was retained
Sample call rates were computed from the released genotype matrix, treating missing calls as missing rather than as reference genotypes. Of 240 participants on a 150-variant panel, 1 failed the minimum call rate of 0.95. The failure fraction was 0.004166666666666667, below the re-genotyping trigger of 0.1. The retained cohort comprises 239 participants: 120 affected and 119 unaffected. **P198 was excluded; all other released participants were retained.** The full participant manifest and call rates are in `participant_qc.csv`.

Variant QC was then recomputed within the retained cohort. Retention required call rate at least 0.95, minor-allele frequency at least 0.01, and control-only Hardy–Weinberg p-value at least 0.000001. Allele frequencies used observed calls; Hardy–Weinberg testing used a two-sided exact conditional test among unaffected participants.

There were 12 excluded variants and 138 retained variants. Failure counts were 5 for call rate, 4 for minor-allele frequency, and 3 for Hardy–Weinberg equilibrium. The excluded variant identifiers are:

`rs010047`, `rs010057`, `rs010063`, `rs010072`, `rs010088`, `rs010092`, `rs010101`, `rs010118`, `rs010128`, `rs010133`, `rs010141`, `rs010149`.

**All other released variants were retained for ancestry assessment**, not cleared for association testing. `variant_qc.csv` supplies the complete retained/excluded manifest and the individual QC measurements. The prospective Bonferroni threshold would be 0.00036231884057971015, calculated from protocol alpha 0.05 and the retained variant count; it was not applied to association results because testing stopped earlier.

## Why comparability fails
PCA used retained variants and retained participants, replacing missing calls with their pooled variant mean and scaling by allele-frequency-based genotype standard deviation. The leading component explained variance fraction 0.09941361305958868. Its Welch affected-versus-unaffected comparison gave p = 3.3491194783865236e-135.

More importantly than that small p-value, the empirical score ranges do not overlap:

| Group | Minimum leading-component score | Maximum leading-component score |
|---|---:|---:|
| Affected | -5.854108831118341 | -1.7454640482762065 |
| Unaffected | 0.38794628752205057 | 7.173129379437073 |

Component sign is arbitrary; separation is not. `ancestry_pcs.csv` preserves participant-level scores. This supports the protocol's separate-ancestry stop branch. The genotype panel does not establish named ancestry categories or prove a particular recruitment mechanism; ancestry-related cohort structure is the operational interpretation requiring investigation. Technical artifacts should also be checked against recruitment and processing records before assigning a definitive biological cause.

## Changes, achieved result, and next action
The changes actually made were computational exclusions under the prespecified quality rules. They produced a technically filtered data set but did **not** restore case-control comparability. No laboratory remediation or replacement recruitment was performed, and no improvement after such an intervention has been measured.

The investigators should pause association claims and audit recruitment ancestry, sample identity, and laboratory processing allocation. Obtain broader ancestry-informative data to validate the observed structure. Recruit or select affected and unaffected participants with genuine ancestry overlap, with balanced processing across affection groups. Simply re-genotyping this plate is not mandated by the sample-failure rule and would not by itself repair a recruitment imbalance. Covariate adjustment is appropriate only after adequate overlap is demonstrated; it is not a substitute for it.

For the replacement or augmented cohort, lock the protocol and analysis pipeline, retain versioned participant and variant manifests, rerun technical QC, and enforce an explicit ancestry-overlap sign-off before association testing. Use structure covariates if residual structure is overlapping, then apply the retained-panel multiplicity correction and seek independent replication of any findings.

## Audit and limits
All displayed quantitative results originate in the sample-QC, variant-QC, and stratification output objects in `trace.json`; identifiers are labels from the released records. `analyze.py` implements the calculations. Only the protocol and genotype/status batches were needed and released; no requested batch was denied. The conclusion stops at the computed ancestry-comparability failure, not at an assumed absence of association. No downstream association or intervention outcome is represented as measured.
