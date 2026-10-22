# Study status for the principal investigator

## Executive conclusion
The discovery plate is usable after protocol QC, but **no association is currently reportable as replicated**. The discovery candidate rs070008 does not meet the independent replication rule. This is not evidence that the whole panel is biologically irrelevant, nor proof of a technical defect.

## Quality and retained cohort
Participant call-rate filtering excluded 3 participants (failure fraction 0.0125); this does not trigger the protocol's plate re-genotyping rule. The retained cohort contains 237 participants: 118 affected and 119 unaffected.

Retain every supplied discovery participant except P016, P077, P139. The complete identity-level decisions and call rates are in `sample_qc.csv`.

Applying variant call rate, pooled minor-allele frequency and exact two-sided Hardy–Weinberg equilibrium testing in retained unaffected participants excluded 11 variants and retained 139. The failure counts are 5 for call rate, 4 for frequency and 2 for control equilibrium.

Retain every supplied discovery variant except rs070013, rs070023, rs070025, rs070047, rs070049, rs070069, rs070099, rs070114, rs070131, rs070133, rs070148. `variant_qc.csv` gives the complete retained set, metrics and exclusions. Filtering is the only change made to the original discovery calls; missing calls were not fabricated for association testing.

## Comparability and discovery
PCA used standardized retained dosages with mean imputation solely for ancestry assessment. The leading component's affected-versus-unaffected Welch p-value was 0.899718; the next component's was 0.164031. Leading-axis score ranges overlap extensively. Some later axes have nominal differences, but none provides compelling separation after considering the axes examined. These data support comparison within this cohort, not a guarantee that subtle ancestry or other confounding is absent. A small candidate panel is a limited ancestry instrument.

The primary scan used additive Cochran–Armitage trend tests on available calls per variant. Bonferroni significance was 0.00035971223. There was 1 discovery hit, rs070008, with p = 5.87172927e-06. The genomic inflation factor was 0.917909. Its additive logistic odds ratio per coded allele was 2.39511, with Wald interval 1.62173 to 3.5373. The effect is an association estimate, not a causal effect; the released records do not identify the nucleotide represented by the dosage allele.

## Independent replication and reconsideration
Replication participant QC retained 120 participants and excluded 0. There were 119 usable candidate calls. Of 1 candidate tested, 0 replicated: rs070008 had p = 0.543816 and an odds ratio of 1.1835. The direction agrees, but the significance requirement fails. Matching dosage coding across the supplied common panel is assumed; allele labels should be verified before any publication.

The failed replication was not ignored. A post-replication sensitivity scan adjusted for 10 leading PCs in additive logistic models. It yielded 0 significant variants, candidate p = 0.000653393, and inflation factor 1.26613. This exploratory reconsideration cannot rescue a failed independent validation. Adjustment from the same candidate panel can also absorb genuine local signals; it does not establish the cause of nonreplication.

## Action and control plan
Withhold the candidate from confirmed-association reporting. The immediate cause of the reporting stop is failure of independent replication, not excessive participant failure or demonstrated ancestry separation. Sampling variation, discovery effect inflation, phenotype differences and assay or allele-alignment problems remain possible explanations, not established findings.

Before more recruitment, audit allele orientation, raw genotype clusters, phenotype definitions, sample identity and laboratory allocation across cohorts. Obtain broader ancestry markers and relevant covariates if residual structure remains a concern. Plan additional independent validation with a prospectively fixed analysis and power calculation rather than repeatedly retesting this cohort. No prospective power calculation was performed here.

Hold the gain by freezing QC manifests, preserving raw batches and scripts, retaining the corrected discovery threshold, and enforcing the independent replication gate. No re-genotyping or biological intervention was performed and no causal mechanism has been demonstrated. All requested batches were released; there was no denied data step. The reproducible calculations and numerical provenance are in `trace.json`, with full scan tables in `discovery_scan.csv` and `adjusted_sensitivity.csv`.
