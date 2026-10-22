# Candidate-region study: final assessment

## Executive decision
The discovery plate is usable under the protocol, and affected and unaffected participants can be compared on the observed panel structure. However, **no variant meets the corrected discovery threshold**. There is consequently no association eligible for replication or reporting. This is a valid negative panel scan, not proof that the trait has no genetic component or that every panel effect is absent.

## Quality and retained analysis population
Of 240 discovery participants, 3 fail the call-rate rule: P085, P136 and P193. The failure fraction is 0.0125, below the protocol ceiling of 0.1. Retention requires a call rate of at least 0.95. The plate therefore does not require re-genotyping under this rule. The retained population comprises 237 participants: 119 affected and 118 unaffected. All participants other than those named above are retained; `sample_qc.csv` supplies the complete participant-by-participant decision and call rate.

Variant quality was evaluated after participant removal. Retention requires call rate at least 0.95, minor-allele frequency at least 0.01, and an exact Hardy–Weinberg test p-value among retained unaffected participants of at least 0.000001. There are 139 retained variants and 11 exclusions:

- Call-rate exclusions (5): rs040024, rs040041, rs040044, rs040059, rs040134.
- Low-frequency exclusions (4): rs040066, rs040114, rs040124, rs040130.
- Control Hardy–Weinberg exclusions (2): rs040065, rs040128.

All other variants are retained. `variant_qc.csv` is the complete retention manifest, including each quality metric. These filters remove unreliable or unsuitable observations; they do not establish the laboratory cause of missingness or disequilibrium. No physical plate intervention was performed.

## Cohort comparability before association
PCA used retained variants and participants, allele-frequency standardization and mean imputation solely for PCA. The leading 10 axes were inspected for phenotype mean differences and observed range overlap. No inspected axis completely separates affected from unaffected participants. The leading-axis phenotype p-value is 0.595686, and its variance fraction is 0.0210957. The next leading-axis phenotype p-values are 0.664643 and 0.665790. The fourth axis has a nominal p-value of 0.043790, but overlaps substantially and is not compelling evidence of ancestry structure when considered with the other inspected axes and diffuse variance spectrum.

Accordingly, the primary analysis used the unadjusted additive trend test rather than a phenotype-selected covariate model. This panel does not reveal the separate-ancestry situation that would prohibit comparison. It is nevertheless a limited candidate panel, not an ancestry reference panel: overlap and non-significant mean tests do not exclude subtle structure, kinship or laboratory confounding. Broader ancestry markers and relatedness assessment would strengthen future inference.

## Discovery and replication
Complete observed calls were used separately for each retained variant in an additive score (Cochran–Armitage trend) test. Across 139 tests, the Bonferroni threshold is 0.000359712. There are 0 significant variants. The smallest p-value is 0.013392, for rs040143, and does not approach the corrected threshold. Genomic inflation is 1.111377, calculated as the median score statistic divided by its null median; on a small panel this is descriptive, not proof of confounding or its absence. Full results are in `discovery_association.csv`.

The replication batch was obtained. Its nomination list is empty, consistent with the computed 0 discovery candidates. The replicated count is therefore 0 by empty-set accounting: **no replication association test was applicable or run**. Replication sample/variant quality, ancestry and effect estimates were not computed because there were no eligible targets. Do not describe this outcome as unsuccessful replication of a hit. No data request was denied, and there is no missing-data refusal hidden in this conclusion.

## Investigator actions and how to hold the result
Report the protocol-compliant negative discovery result and do not promote nominal signals as confirmed associations. The analysis changes were participant and variant filtering; they achieved a quality-qualified comparison, not a positive finding. No causal explanation for the negative result can be identified from these data alone. Modest effects, limited information and genuinely absent panel associations remain possible; prospective power for specified effects was not computed.

Preserve the released batches, scripts, trace, retention manifests and complete scan as the audit record. Freeze the tested family and correction rule. Investigate the excluded calls and control disequilibrium with the laboratory before future releases, without silently reinstating exclusions. For follow-up, prospectively specify effect sizes, power, ancestry/relatedness checks and a larger or broader study design; do not lower the threshold after inspecting these results. Any future eligible discovery hit must undergo independent, allele-harmonized replication with the protocol's direction and significance requirements before investigators report it as an association.
