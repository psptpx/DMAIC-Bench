# Candidate-region study: investigator decision

## Executive conclusion
The discovery plate is usable after protocol QC. No variant meets the pre-specified association criterion, so there is no candidate to report as replicated. This is a negative result for this panel and analysis, not proof that the trait has no genetic contribution or that smaller effects are absent.

## Quality and retained analysis set
Participant call rate was calculated across the original 150-variant panel. The required minimum was 0.95. Of 240 participants, 3 failed (fraction 0.0125), below the plate re-genotyping threshold of 0.1. Whole-plate re-genotyping is therefore not indicated by this protocol.

Excluded participants: P085, P136, P193. All other participants in the released discovery batch are retained; `participant_qc.csv` gives the complete named manifest and call rates. The retained groups contain 119 affected and 118 unaffected participants.

Variant QC was then recomputed using retained participants. Requirements were call rate at least 0.95, minor-allele frequency at least 0.01, and exact Hardy–Weinberg p-value in unaffected participants at least 0.000001. There were 5 call-rate failures, 4 frequency failures and 2 Hardy–Weinberg failures; 11 variants failed overall and 139 were retained.

Excluded variants: rs040024, rs040041, rs040044, rs040059, rs040065, rs040066, rs040114, rs040124, rs040128, rs040130, rs040134. All other variants in the released panel are retained. `variant_qc.csv` supplies the complete named manifest, computed QC values and retention flags. Hardy–Weinberg testing used the conditional exact distribution, rather than an approximation for rare alleles. These exclusions improve technical eligibility; they do not constitute evidence that an excluded variant is biologically irrelevant.

## Can the groups be compared?
Allele-standardized PCA used mean-imputed genotypes only for the structure screen. Welch tests of the leading 10 axes used a screening cutoff of 0.005. No axis passed that cutoff. The leading-axis p-value was 0.595686; the smallest axis p-value was 0.0437902. Thus the panel does not show compelling case/control separation, and an unadjusted trend scan is defensible.

This is a limited candidate-panel ancestry screen, not a demonstration of exchangeability. Genome-wide ancestry markers, recruitment covariates, relatedness and laboratory allocation were not assessed; those checks would be needed for stronger confounding claims. The PCA screening rule is an analyst diagnostic, not an additional protocol association threshold.

## Discovery and replication
Complete-case additive dosage score tests were run independently for each retained variant; missing calls were not imputed for association. The Bonferroni cutoff was 0.000359712, calculated from the protocol alpha of 0.05 and the retained panel. The smallest p-value was 0.013392, and 0 variants were significant. Genomic inflation was 1.111377, calculated as the median score statistic divided by its null median. This modest diagnostic value does not overturn the null scan or establish absence of confounding. Full results are in `discovery_scan.csv`.

The released independent replication cohort contains 60 affected and 60 unaffected participants. Both the computed discovery-hit set and the steward nomination list contain 0 candidates. Consequently the replication disposition is 0 replicated out of 0 candidates: no confirmatory replication tests, directional comparisons or hit effect estimates were applicable. The protocol requires replication p below 0.05 with the same effect direction, but no variant reached that stage. Replication data were available, not denied. The untouched replication cohort must not be mined for nominal hits and described as confirmation.

## Actions and control plan
Report the absence of panel-wide significant associations with the QC-qualified cohort. Do not nominate a nominal discovery result for clinical use or imply a causal association. Archive the protocol, released batches, analysis scripts, trace and retention manifests with this report.

The actual change was analytical filtering of low-quality participants and variants, not a laboratory intervention. It produced an eligible comparison set but did not reveal an association. Investigate the excluded calls with the laboratory before considering targeted re-calling; do not silently restore them or relax thresholds after inspecting results.

Before a larger study, agree on a scientifically meaningful effect size, allele-frequency range and recruitment design, then perform prospective power planning. Power and the minimum detectable effect were not computed here. Improve ancestry and relatedness assessment and audit laboratory allocation. Freeze QC and multiplicity rules in advance, keep future replication independent, and have a second analyst reproduce the archived scripts and monitor exclusion rates across future plates. There is no basis here for claiming a successful biological intervention or a replicated risk marker.
