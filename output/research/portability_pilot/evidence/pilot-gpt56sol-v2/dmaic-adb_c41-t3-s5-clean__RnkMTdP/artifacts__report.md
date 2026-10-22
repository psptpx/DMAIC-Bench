# Candidate-region association study: final status

## Executive conclusion

The discovery plate **can carry an analysis**. Participant QC failed **3** people, a failed fraction of **0.0125**, so the plate passed the protocol gate and did not require re-genotyping. After the mandated exclusions, **237** participants remained. Variant QC then failed **11** markers and retained **139**.

The retained affected and unaffected participants are not ancestry-separated, but they are not exchangeable without adjustment. The leading ancestry axis differed by affection status (PC1 p-value **4.4356006605713844e-16**) while its score ranges still overlapped (overlap fraction **0.8847887198278855**). The valid route was therefore an additive logistic association scan adjusted for PC1.

All **139** retained variants were tested and **0** models failed. At the computed Bonferroni threshold of **0.00035971223021582735**, **0** variants were significant. The smallest adjusted discovery p-value was **0.005541811296274787**, and genomic inflation was **1.1762264979203456**. Accordingly, no discovery hit was nominated. The replication batch consequently contained **0** candidates and **0** replicated associations. **No variant association should be reported from this study.**

## What the protocol retained

### Participants

Retain every discovery participant except **P127**, **P142**, and **P195**. Those exclusions arise from the participant call-rate rule. The resulting retained cohort contains **237** participants.

### Variants

Retain every panel variant except:

- call-rate failures: **rs050014**, **rs050071**, **rs050082**, **rs050091**, **rs050108**;
- minor-allele-frequency failures: **rs050052**, **rs050092**, **rs050096**, **rs050121**;
- unaffected-participant Hardy–Weinberg failures: **rs050017**, **rs050019**.

These categories account for **5**, **4**, and **2** failures respectively, leaving **139** retained variants. The minimum control Hardy–Weinberg p-value computed during QC was **3.003514136534961e-13**.

## Cohort comparability and analysis route

PCA was run on the participant- and variant-QC-retained genotype matrix after mean imputation and allele standardization. The first attempt failed because the installed environment lacked the requested PCA library; it produced no scientific result. The analysis was rerun successfully using NumPy singular-value decomposition.

The successful assessment found no non-overlapping ancestry axis: the separation indicator was **false**, and the separated-axis result was **0**. PC1 explained a variance fraction of **0.0814350353018884**, showed substantial range overlap between affection groups, and nevertheless differed strongly by affection status. This is overlapping structure, not two disjoint ancestries. A direct unadjusted comparison would violate the protocol; comparison is permitted only after adding PC1 to the association model.

## Discovery and replication

The PC1-adjusted additive logistic scan produced **0** Bonferroni-significant variants. Therefore there is no associated-variant list: none passed the study-wide discovery criterion. The independent replication data were released, but the steward explicitly supplied an empty nominated-candidate set. Testing arbitrary replication-panel variants after seeing the null discovery scan would not be protocol replication, so no such tests were performed.

Replication therefore does not provide support for reporting a finding. This is not missing replication data and not a failed replication of a discovery hit; it is a non-applicable replication stage because discovery produced no candidate.

## Business action and control plan

1. **Do not re-genotype this plate solely for the participant-QC gate.** It passed; preserve the three participant exclusions in the locked analysis set.
2. **Do not report a panel association.** No retained variant crossed the study-wide threshold, and there is no candidate eligible for confirmation.
3. **Preserve the analysis controls.** Keep the eleven variant exclusions, the PC1 covariate, the computed multiple-testing threshold, and the independent replication rule in any rerun.
4. **Reconsider the discovery strategy before further claims.** Investigators should review power and recruitment, consider a larger discovery cohort or a prespecified expanded panel, and repeat the full QC/ancestry/adjusted-testing sequence on any new data. Replication should be reopened only for a variant that first meets the discovery rule and can then be checked for nominal significance and matching direction in the independent cohort.

The operational change made in this run was to remove protocol QC failures and adjust for the observed overlapping ancestry structure. That change produced an analyzable retained cohort and a valid controlled scan; its outcome was a null discovery result rather than a reportable association.
