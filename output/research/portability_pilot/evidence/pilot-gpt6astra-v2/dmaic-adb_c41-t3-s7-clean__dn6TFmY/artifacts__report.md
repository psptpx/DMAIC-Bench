# Investigator report

## Bottom line
The plate is usable under the protocol, and the retained cohort is sufficiently comparable for a panel-level association scan. The discovery signal does not meet the independent replication rule and must not be reported as an established association.

## Quality and cohort comparability
Of 240 discovery participants, 3 failed the call-rate rule; the failure fraction was 0.0125, below the plate re-genotyping trigger of 0.1. Retained participants number 237 (118 affected and 119 unaffected). All participants except P016, P077, P139 are retained. The participant call-rate cutoff was 0.95.

Variant QC retained 139 and excluded 11: 5 failed call rate, 4 failed minor-allele frequency, and 2 failed exact control Hardy–Weinberg testing. Cutoffs were 0.95, 0.01, and 1e-06, respectively. All supplied variants except rs070013, rs070023, rs070025, rs070047, rs070049, rs070069, rs070099, rs070114, rs070131, rs070133, rs070148 are retained. Full participant and variant decisions are in `sample_qc.tsv` and `variant_qc.tsv`.

PCA used mean-imputed, allele-standardized retained genotypes. Leading-axis ranges overlapped between affection groups. The first-axis phenotype comparison gave p=0.899718; its variance fraction was 0.0227369. Later nominal differences were not compelling after accounting for the axes examined. We found no clear ancestry separation or strong phenotype-linked structure warranting covariates, so proceeded with unadjusted dosage trend tests. This small candidate panel cannot exclude subtle ancestry confounding as effectively as genome-wide ancestry markers.

## Discovery and replication
Complete-case additive trend testing found 1 significant variant at Bonferroni threshold 0.00035971223. Genomic inflation was 0.917909. The hit was rs070008, p=5.87172927e-06; its additive logistic odds ratio per coded allele was 2.39511, with confidence interval [1.62173, 3.5373]. No other retained variant met the corrected threshold. These are panel-wide rather than genome-wide claims.

Replication sample QC excluded 0 participants and retained 120. The nominated variant passed replication QC: call rate 0.991667, minor-allele frequency 0.306723, and control Hardy–Weinberg p=0.753918. Among 1 discovery candidates, 0 replicated. Replication trend p=0.543815626, versus the required 0.05; the per-coded-allele odds ratio was 1.1835. The direction agreed with discovery.

## Actions and holding the result
QC exclusions, rather than laboratory changes or post-hoc threshold changes, produced the analysis-ready cohort. No re-genotyping was required and no intervention on the biological trait has been tested. Withhold the discovery association. Reconsider the scan, including ancestry sensitivity, assay artifacts, phenotype comparability and allele harmonization; seek further independent evidence without relaxing the reporting rule.

Preserve the original releases, analysis scripts, QC manifests, full association results and trace. Apply the same frozen QC and replication gates to future cohorts, inspect ancestry before testing, and log deviations prospectively. No requested batch was denied. The replication result does not support reporting the discovery association. Failure to replicate is not proof of no biological effect, but the protocol stops the affirmative conclusion here. No clinical utility or causal allele has been established.
