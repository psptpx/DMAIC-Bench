# Candidate-region study: investigator decision

## Executive conclusion
The plate is technically usable and the retained cohort can be compared under the protocol. There is no detected ancestry separation in the panel-derived axes. Additive trend testing identifies **0 associated variants** after correction over the retained panel. These are study associations, not evidence of causality or clinical utility.

## Quality and retention
Computed from the steward's complete calls and affection records, the matrix contains 240 participants and 150 variants. All 240 participants pass the protocol call-rate rule: 0 fail, for a failure fraction of 0.0. The lowest participant call rate is 0.953333. The retained groups contain 120 affected and 120 unaffected participants. Plate re-genotyping is not triggered.

Variant filtering retains 140 and removes 10: 5 fail call rate, 3 fail minor-allele frequency, and 2 fail the exact conditional Hardy–Weinberg test in unaffected participants. Variant missingness and allele frequencies were calculated after participant filtering; missing calls are excluded from their denominators. The exact test sums genotype configurations no more probable than the observed configuration, conditional on allele count.

All participant identifiers in `participants_qc.csv` are retained. The full retained/excluded variant manifest, with call rates, minor-allele frequencies and control equilibrium probabilities, is `variants_qc.csv`. Excluded variants: rs040038, rs040054, rs040057, rs040072, rs040104, rs040106, rs040110, rs040112, rs040113, rs040125. Every other supplied variant is retained.

## Cohort comparability
PCA used retained variants, replacing missing calls by the variant mean for this diagnostic only and scaling centered dosages by allele-frequency variance. The leading-axis affected-versus-unaffected Welch test gives p = 0.89905; its explained variance fraction is 0.0209856. Affected scores range from -3.50883 to 4.92473, versus -4.52393 to 4.1911 in unaffected participants. The other inspected leading axes also overlap and show no group mean evidence of stratification. Thus there is no observed separate-ancestry or overlapping-structure signal requiring ancestry adjustment here. This is a panel-based diagnostic, not proof of ancestry equivalence; subtle structure, relatedness and technical batch effects remain limitations. The study lead supplied no independent ancestry facts in response to the clarification request (unroutable, not a denial of a named batch).

## Association results
Tests use observed calls per variant and an additive Cochran–Armitage score chi-square statistic. The corrected per-variant significance threshold is 0.0003571428571. Genomic inflation, calculated as the median test statistic divided by the null median, is 0.894149; on a candidate panel this is descriptive, not a calibration guarantee. No genomic-control rescaling was used.

No variant meets the corrected threshold; there is no associated-variant list to report.

Allele frequencies refer to the supplied dosage-counted allele; biological allele names and functional annotations were not supplied. Complete test results, including nonsignificant variants and observed sample counts, are in `association_results.csv`. Nonsignificance does not establish absence of an effect.

## Actions and control plan
The implemented change was analytical removal of poor-quality variants, not an experimental intervention. It left a quality-qualified panel and an overlapping cohort suitable for the specified comparison; no participant removal or plate repair was necessary. The QC failure categories explain the exclusions, but their laboratory root causes have not been established.

Investigators should not declare a panel association from this cohort. Before further recruitment, plan power around scientifically meaningful effect sizes and allele frequencies, and consider an independent, larger ancestry-matched study. Confirm questionable calls with an independent assay, review missingness by affection and laboratory batch, and obtain broader ancestry and relatedness data before extending the analysis. No replication or intervention benefit has been measured here. Preserve original calls, QC manifests, code and this trace; apply the same protocol gates to future releases, freeze the retained-panel testing denominator before association, and review any changed samples or calls through the complete QC and ancestry workflow. Do not use these exploratory candidate-panel findings for clinical decisions.
