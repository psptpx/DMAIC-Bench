# Study decision for the principal investigator

## Bottom line
The plate is usable under the protocol, but this analysis supports **no reportable variant association**. Quality exclusions were applied before ancestry assessment; the affected and unaffected groups have overlapping ancestry structure, requiring adjustment rather than a naive comparison. The adjusted scan produced **0 significant variants**, so there are **0 replication candidates and 0 confirmed associations**. This is not proof that genetic effects are absent.

## Quality and retention
The discovery data contain **240 participants and 150 variants**. Participant call-rate screening excludes **3 participants**, a failure fraction of **0.0125**, below the protocol's plate-rejection limit. Re-genotyping the whole plate is therefore not triggered. The retained cohort contains **237 participants: 120 affected and 117 unaffected**.

Excluded participants: P127, P142, P195. All other participants in the released discovery batch are retained. `sample_qc.csv` gives the complete participant-level retention manifest and measured call rates.

Variant QC was computed after participant exclusion, using observed-call allele frequencies and an exact, probability-ordered Hardy–Weinberg test among unaffected participants. **11 variants fail and 139 remain**: **5** fail call rate, **4** fail minor-allele frequency, and **2** fail control Hardy–Weinberg equilibrium.

Excluded variants: rs050014, rs050017, rs050019, rs050052, rs050071, rs050082, rs050091, rs050092, rs050096, rs050108, rs050121. All remaining variants in the released panel are retained; `variant_qc.csv` identifies each retained variant and all QC metrics. The protocol's inclusive quality thresholds were used without alteration.

## Comparability before testing
Principal components were computed from retained variants using mean imputation only for PCA and allele-frequency standardization. The leading ancestry axis differs by affection status (Welch test **p = 4.31637e-16**), but the score ranges overlap: affected **−5.28835 to 5.84137**, unaffected **−4.60873 to 6.49177**. Other inspected leading axes did not show compelling affection-status differences. This is overlapping structure, not separate non-comparable ancestry groups. The leading ancestry axis entered the association model as a covariate.

PCA on a candidate-region panel is only a limited ancestry surrogate. It does not establish that all population confounding has been removed; broader ancestry markers and recruitment metadata would strengthen that assessment.

## Association and replication
Each retained variant was tested using an additive logistic likelihood-ratio comparison, with the leading ancestry axis included in both models. Association tests used observed calls rather than imputed genotypes. The computed Bonferroni threshold is **0.000359712**. The adjusted genomic inflation estimate is **1.18479**, which warrants caution about residual structure and the small, selected panel rather than being treated as a guarantee of calibration.

The smallest adjusted p-value is **0.004628** at rs050012, above the corrected threshold. No variant is declared associated. Complete computed effects, uncertainty intervals and p-values are in `association.csv` and the trace; nominal associations must not be promoted to discoveries.

The independent replication batch was released, and its nomination list is empty, consistent with our scan. The replication step therefore counted an empty candidate set; **no candidate-specific replication p-value or direction test was performed**. This is neither evidence of successful replication nor evidence of failed replication. No batch was denied. Replication does not authorize reporting an association when discovery has produced none.

## What changed, what it achieved, and what happens next
The analytical changes were to remove protocol-failing calls at participant and variant levels and to account for observed ancestry structure. These changes yield a quality-filtered, covariate-adjusted analysis with no corrected discovery signal. No wet-lab or recruitment intervention was implemented, and no before/after improvement in biological outcomes is claimed.

Do not report a panel association or a causal genetic conclusion. Investigate excluded sample and variant call failures with the laboratory; retain the original calls and exclusion manifests. Review ancestry and recruitment balance, ideally using independent genome-wide ancestry markers, before extending the analysis. Plan a larger, ancestry-balanced study with prospectively justified power and independently specified replication criteria rather than relaxing correction or mining the replication cohort for new claims.

Hold the result through versioned protocol, archived input batches, reproducible scripts, frozen retention lists and an auditable trace. Any future discovery must meet the original multiplicity rule and independent same-direction replication requirement. Power and residual-confounding sensitivity were not estimated here, so the current negative finding cannot establish clinically meaningful absence of effect.
