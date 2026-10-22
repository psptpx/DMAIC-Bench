# Study decision: valid discovery scan, no reportable association

## Executive conclusion
The plate can support the planned analysis after protocol QC. It does **not** support a positive variant association claim. There are **0 significant discovery variants**, so replication has no discovery candidate to confirm. This is a negative scan at the protocol threshold, not evidence that the trait has no genetic contribution.

## Quality and retained analysis population
Computed from the steward's complete discovery matrix, the starting dataset contains **240 participants and 150 variants**. Participant call-rate filtering excludes **3 participants** (failure fraction **0.0125**), below the protocol's plate re-genotyping trigger. The comparison retains **119 affected and 118 unaffected participants**.

Excluded participants: P085, P136, P193. All other participant identifiers in the released discovery batch are retained. The complete participant decision ledger is `sample_qc.csv`.

After participant filtering, variant call rate, minor-allele frequency and exact, probability-ordered Hardy–Weinberg testing among unaffected participants exclude **11 variants**, retaining **139**. Failure counts are **5** for call rate, **4** for minor-allele frequency and **2** for control Hardy–Weinberg equilibrium.

Excluded variants: rs040024, rs040041, rs040044, rs040059, rs040065, rs040066, rs040114, rs040124, rs040128, rs040130, rs040134. All other variants in the released panel are retained. `variant_qc.csv` lists each identifier, its metrics and its retention decision. These exclusions are analytic changes only; no laboratory re-genotyping was performed. The data do not establish the laboratory causes of the failures.

## Can affected and unaffected participants be compared?
PCA used retained variants, mean imputation for missing calls, and allele-frequency-standardized dosage. Leading axes show overlapping affected and unaffected ranges, not separate ancestry populations. The leading-axis phenotype comparison gives p = **0.595686**; the next axis gives p = **0.664643**. There is no convincing leading-axis ancestry imbalance requiring adjustment. An isolated higher-axis nominal difference is not compelling across the inspected axes. Accordingly, the primary analysis is an unadjusted additive trend scan.

This ancestry check is limited by the candidate-region panel: it is not a genome-wide ancestry or relatedness assessment. It supports proceeding under the released protocol, not a guarantee that all possible confounding is absent.

## Discovery association and replication
Each retained variant was tested using its nonmissing genotypes with an additive Cochran–Armitage score test and asymptotic binomial variance. Bonferroni significance threshold is **0.0003597122302**. The smallest observed p-value is **0.01339198**, and **0 variants** pass. Genomic inflation factor is **1.111377**; this modest value alone is not proof of ancestry confounding. Full test results are in `discovery_association.csv`.

The independent replication batch was obtained. Its nominated list is empty, matching the computed **0 discovery candidates**. The candidate-set reconciliation records **0 replicated associations**; this is an empty set, not an unsuccessful replication experiment. No candidate-specific replication p-value, direction comparison or odds ratio was computed because none was eligible. Replication data were not denied, and no exploratory replication scan was substituted for the prespecified discovery-first rule.

## Recommended action and ongoing controls
Report the QC-passing null discovery result without promoting nominal signals. Preserve the protocol, steward batches, analysis scripts, full QC ledgers, test table and trace as the reproducibility record. Keep excluded calls out of the analysis unless they are re-genotyped and independently pass the same locked QC rules.

If the investigators wish to pursue smaller effects, prospectively plan a larger, ancestry-balanced cohort, genome-wide ancestry markers and an effect-size-based power analysis. Power was not computed here, so the present result cannot quantify which effects have been ruled out. Retain independent replication as a mandatory gate for future discoveries, with allele harmonization and matching direction checked before reporting. Do not loosen correction thresholds or retrospectively redefine candidates to manufacture a positive result.
