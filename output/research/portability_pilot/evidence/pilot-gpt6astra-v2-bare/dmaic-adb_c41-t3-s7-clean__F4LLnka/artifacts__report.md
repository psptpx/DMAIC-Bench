# Study decision: discovery signal, not independently confirmed

## Executive conclusion
The plate is usable after protocol QC; wholesale re-genotyping is not indicated. The discovery scan yields 1 significant variant, **rs070008**, but **0 of 1 candidates replicate**. Do not report a confirmed metabolic-trait association or use this result clinically. It is appropriate to report a discovery-only signal alongside its unsuccessful independent replication. Lack of replication does not establish absence of an effect.

## Plate and retained analysis set
Computed from the released full genotype files, not the steward previews: discovery contains 240 participants and 150 variants. Participant call rate must be at least 0.95. There are 3 failures, a fraction of 0.0125, below the plate threshold of 0.1. Remove P016, P077, P139; retain every other participant in the released discovery roster. This leaves 237 participants: 118 affected and 119 unaffected.

After participant exclusions, variant QC requires call rate at least 0.95, minor-allele frequency at least 0.01, and control-only exact Hardy–Weinberg p at least 1e-06. Exact HWE sums conditional genotype-configuration probabilities no larger than the observed probability. There are 11 excluded variants: rs070013, rs070023, rs070025, rs070047, rs070049, rs070069, rs070099, rs070114, rs070131, rs070133, rs070148. Retain every other variant in the discovery roster, for 139 retained variants. The failure counts are 5 for missingness, 4 for frequency and 2 for HWE. The complete named inclusion/exclusion manifests, with measured QC values, are `sample_qc.csv` and `variant_qc.csv`.

These exclusions are the analytic change actually made; no laboratory repair was performed. They produce a protocol-eligible analysis set, not proof of error-free genotyping. HWE departures flag possible assay or population problems but do not diagnose their cause.

## Can affected and unaffected participants be compared?
PCA used retained genotypes, mean imputation for PCA only, and allele-variance scaling. Affection-group Welch comparisons across 10 leading axes used a corrected screening threshold of 0.005. No axis passes that screen; the leading-axis p-value is 0.899718. This supports proceeding with an unadjusted additive trend scan, rather than claiming a demonstrated ancestry imbalance. PCA on a candidate panel is not a substitute for genome-wide ancestry or relatedness assessment. There are no measured batch, pedigree or clinical covariate adjustments in this analysis, so residual confounding cannot be ruled out.

## Discovery association
The scan used observed genotypes at each retained variant, with an additive Cochran–Armitage score statistic and asymptotic chi-square p-values. Bonferroni significance is 0.00035971223, derived from the protocol alpha of 0.05 and the retained panel size. Genomic inflation is 0.917909, giving no evidence of broad inflation in this panel.

For rs070008, trend p = 5.87172927e-06; the fitted additive logistic odds ratio per encoded allele is 2.39511, with Wald confidence limits 1.62173 to 3.5373. The remaining retained variants do not meet the corrected threshold. `discovery_association.csv` contains the complete scan. Effects refer to the supplied genotype dosage, not a named nucleotide allele; nucleotide harmonization should be verified before external reporting.

## Independent replication
All 120 replication participants pass participant QC (60 affected and 60 unaffected). Applying the same variant thresholds leaves 140 variants and excludes 10; replication QC manifests are saved separately. Only the discovery-selected candidate was tested for confirmation, not a newly selected replication hit.

The candidate passes replication variant QC and has 119 observed calls. Its direction matches discovery, but p = 0.543815626 does not meet the required p < 0.05. Replication odds ratio is 1.1835, with Wald confidence limits 0.686511 to 2.04028. Thus the protocol confirmation criterion fails. A weaker estimated effect, sampling uncertainty and discovery selection could contribute; these data do not distinguish those explanations or establish a technical cause.

## Investigator action and control plan
Freeze the current finding as unconfirmed. Audit raw cluster plots, candidate allele coding and independent sample identity; verify the exclusion manifests before manuscript submission. Investigate the flagged missingness and control HWE failures without selectively restoring variants to improve significance. A further independently recruited, prospectively powered validation study should predefine the candidate, allele orientation, QC rules, ancestry/relatedness handling and replication criterion. No power calculation or causal mechanism was established here.

Preserve the released batches, scripts, QC manifests and complete scan with the trace. Re-run these checks with versioned inputs on any corrected release; record exclusions and review departures before unblinding association results. Hold reporting to the independent-replication gate rather than discovery significance alone. All requested core batches were released; no denied-data gap was substituted with an estimate. No actual laboratory intervention or prospective monitoring outcome is claimed.

## Audit trail
`trace.json` records the computations in execution order and the plate, stratification, discovery and replication decisions. `analyze.py`, `scan.py`, and `finish.py` contain the calculations. Numeric results above are rounded presentations of the corresponding trace outputs; participant and variant strings are identifiers, not numerical results.
