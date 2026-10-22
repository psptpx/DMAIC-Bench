# Investigator report: replicated panel association

## Decision
The discovery plate is usable under the protocol. After prespecified quality filtering and an ancestry-structure check, **rs000008 is the sole discovery association and is independently replicated**. Report it as an association with affection status, not as a causal variant, a genome-wide discovery, or a clinically validated predictor.

## Quality and retained cohort
Participant retention required call rate at least 0.95; plate rejection required a failure fraction above 0.1. Discovery excluded 3 participants (failure fraction 0.0125), retaining 237: 119 affected and 118 unaffected. Thus no plate re-genotyping was required. The minimum original call rate was 0.94.

Excluded discovery participants: P053, P129, P160. All other participants in the released discovery batch are retained; `participants_qc.csv` is the complete identity-level manifest.

On those retained participants, variants required call rate at least 0.95, minor-allele frequency at least 0.01, and unaffected-participant exact Hardy–Weinberg p-value at least 1e-6. Of the variants, 13 failed and 137 were retained: 6 failed call rate, 4 failed frequency, and 3 failed Hardy–Weinberg equilibrium. These are screening failures, not demonstrated laboratory root causes.

Excluded discovery variants: rs000003, rs000025, rs000061, rs000079, rs000086, rs000091, rs000107, rs000108, rs000122, rs000130, rs000138, rs000149, rs000150. Every other released discovery variant is retained. `variants_qc.csv` gives every identity, metric and retention verdict. Hardy–Weinberg testing used the conditional exact distribution and summed outcomes no more probable than the observed outcome.

## Can affected and unaffected participants be compared?
Before association testing, we mean-imputed missing calls for PCA only, centered dosages, and scaled by allele-frequency-based genotype standard deviation. We inspected 10 leading axes with Welch phenotype comparisons and range-overlap checks. All showed overlapping phenotype ranges. Discovery leading-axis p-values were 0.939779 and 0.329510; the leading axis explained a variance fraction of 0.022767. Later nominal differences did not survive correction across inspected axes (minimum adjusted p-value 0.265964). There was no evidence of disjoint ancestry or a dominant phenotype-linked ancestry axis, so the scan used unadjusted additive trend tests.

This is a panel-limited check, not proof of identical ancestry. A candidate panel can miss subtle structure and relatedness. Genome-wide ancestry markers and kinship review would strengthen inference; if overlapping structure is subsequently established, rerun association with the leading structure axes as covariates. If ancestry is nonoverlapping, obtain a comparable cohort rather than interpreting adjustment as a cure.

## Discovery and replication
Discovery used complete called genotypes at each retained variant for an additive Cochran–Armitage/score trend test. The Bonferroni threshold was 0.000364964, computed from alpha 0.05 over 137 retained variants. There was 1 significant variant. Genomic inflation lambda was 1.115941; this modest elevation should remain a sensitivity-review item rather than being treated as proof of no confounding.

For **rs000008**, discovery trend p = 5.25354e-11. Logistic regression estimated a per-coded-allele odds ratio of 3.78652, with Wald confidence bounds 2.47026–5.80412. No nucleotide effect allele was supplied, so the effect is described only in the supplied dosage coding. The full scan is in `discovery_associations.csv`.

Replication applied the same quality rules: 2 participants failed (fraction 0.016667), leaving 118, comprising 59 affected and 59 unaffected. Excluded participants: R026, R093. Replication retained 140 variants and excluded 10; 6 failed call rate, 4 failed frequency, and none failed Hardy–Weinberg equilibrium. Excluded variants: rs000003, rs000025, rs000030, rs000061, rs000079, rs000107, rs000108, rs000130, rs000138, rs000150. Complete manifests are in `replication_participants_qc.csv` and `replication_variants_qc.csv`.

Replication PCA also showed overlap, with leading-axis p = 0.804551. The nominated hit passed variant QC. Using 117 called participants, its replication trend p = 4.03132e-05 and coded-allele odds ratio = 3.09723. The direction matched discovery and p was below the protocol replication alpha of 0.05. Thus 1 of 1 discovery candidates replicated. No other variant is reportable under the discovery-plus-replication rule.

## What changed, what it achieved, and how to hold it
The change was analytical filtering, not a laboratory intervention: low-call participants and failing variants were removed before ancestry evaluation and testing. This produced an eligible comparison and a corrected discovery result that passed independent confirmation. No causal reason for the QC failures has been established, and no improvement from re-genotyping is claimed.

Investigators should report the replicated association with its coding and cohort limitations, verify allele harmonization and genotype cluster quality for the hit, and pursue independent biological and broader ancestry-aware validation. Archive the steward batches, scripts, retention manifests, and full scan with the trace. Keep the protocol thresholds fixed for future batches; monitor call-rate and equilibrium failures by plate, require ancestry comparability before testing, and preserve the replication requirement. A future nonreplicating hit must be withheld and the discovery scan reconsidered.

All required batches were released; no step was denied. The record does not establish causality, fine-mapped identity, genome-wide generalizability, or clinical utility. Numerical results are recorded in `trace.json`; the scripts preserve the computations.
