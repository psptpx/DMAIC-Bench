# Candidate-panel study: investigator decision

## Executive conclusion
The plate is analytically usable under the protocol. After quality filtering, affected and unaffected participants overlap on the leading genotype ancestry axes. **rs000008 is the only panel-wide significant association**, and remains significant in an ancestry-axis adjustment sensitivity analysis. This is a candidate association, not proof of causality or clinical utility.

## Quality and retained cohort
Participant call-rate QC excluded 5 participants (failure fraction 0.02083333), below the protocol's plate-rejection limit. There is no protocol requirement to re-genotype this plate. Retained: 235 participants, comprising 117 affected and 118 unaffected.

Excluded participants: P011, P059, P069, P224, P225. All other supplied participants are retained; `sample_qc.csv` gives the complete named inclusion/exclusion manifest and call rates.

Variant QC was computed after participant exclusions. Call rate and minor-allele frequency used the retained cohort; Hardy–Weinberg equilibrium used only retained unaffected participants, with a probability-ordered exact conditional test. The criteria jointly removed 12 variants and retained 138. Failures by criterion were 5 for call rate, 4 for allele frequency, and 3 for equilibrium.

Excluded variants: rs000031, rs000049, rs000060, rs000078, rs000086, rs000093, rs000114, rs000126, rs000135, rs000138, rs000142, rs000148. Every other supplied variant is retained. `variant_qc.csv` contains the full named manifest, criteria measurements and decisions.

## Comparability before testing
Missing genotypes were mean-imputed only for PCA, with allele-frequency standardization followed by singular-value decomposition. The leading axis had a group-comparison Welch p-value of 0.260362; its variance fraction was 0.0212533. The unaffected score range was -4.02679 to 4.24263; the affected range was -3.58153 to 3.94601. Thus the leading axis does not separate affection groups, and the spectrum has no dominant ancestry axis.

A later axis showed a group difference (p = 0.00300195). That is not by itself evidence of distinct ancestries: this candidate panel can encode a genuine association as well as ancestry. We therefore ran a covariate-adjusted sensitivity analysis using the leading genotype axes. These data support comparison rather than an ancestry-separation stop, but cannot establish absence of all confounding. The steward re-served genotype data when ancestry information was requested; no independent ancestry-marker batch was supplied and none is assumed. The small regional panel limits ancestry resolution, and independent ancestry information would strengthen the conclusion.

## Association results
Primary testing used the additive genotype score/trend test on nonmissing calls separately at each retained variant. The Bonferroni threshold was 0.0003623188406. Significant variants: 1. The rs000008 p-value was 7.4733891e-07; genomic inflation factor was 0.826762.

Additive logistic regression adjusted for leading genotype principal components also yielded 1 significant variant: rs000008 (Wald p = 6.4035656e-06). Its genomic inflation factor was 0.802588. Thus adjustment did not remove the finding, and neither analysis shows broad inflation. Panel-derived PCs are not independent ancestry validation and may absorb genuine regional signal. No other retained variant meets the corrected threshold; this does not demonstrate absence of smaller effects. Full results are in `association.csv`.

## Action and control plan
The change made here was analytic filtering, followed by a pre-test structure check and a covariate-adjusted robustness check—not a laboratory intervention. Filtering produced the usable cohort and variant set above; sensitivity adjustment preserved the same candidate finding. No improved laboratory performance or independent replication has been measured.

Prioritize orthogonal assay confirmation of the associated variant and review its genotype clusters, missing calls, sample identity and processing records. Replicate in an independent, ancestry-matched cohort with independent ancestry markers and prespecified covariates. Obtain regional linkage information before interpreting the variant as causal. Do not use the result for clinical decisions yet.

Freeze the protocol, released JSON batches, QC manifests, scripts and full association results. Reapply the same quality gates to new plates, monitor failure patterns and ancestry overlap, and require independent replication before promoting the candidate to a confirmed finding. `trace.json` records computed quantities; the scripts and CSV files permit audit and rerun. No separate validation or laboratory remediation outcome was computed.
