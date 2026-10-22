# Candidate-region association study: final report

## Executive conclusion

The plate can support a conclusion. Participant quality control excluded **P053, P129, P160**. All other enrolled participants are retained, leaving **237** participants: **119** affected and **118** unaffected. The participant failure fraction was **0.0125**, below the protocol's re-genotyping limit of **0.1**.

Variant quality control excluded **rs000003, rs000025, rs000061, rs000079, rs000086, rs000091, rs000107, rs000108, rs000122, rs000130, rs000138, rs000149, rs000150**. All other panel variants are retained, for **137** tested variants. The exclusions comprise **6** call-rate failures, **4** minor-allele-frequency failures, and **3** control Hardy-Weinberg failures; these categories do not overlap in this dataset.

The retained affected and unaffected groups can be compared. Their leading-axis score ranges overlap, PC1 had a case/control p-value of **0.8666902364429908**, and its range-overlap fraction was **0.9351482635508023**. There is no evidence that the groups are drawn from separate ancestries, so the primary association scan was unadjusted. An exploratory adjusted sensitivity scan reached the same nomination but was not made primary.

The primary additive scan tested **137** variants at the Bonferroni threshold **0.00036496350364963507** and found **1** association. That association is **rs000008**, with discovery p-value **9.974888997073252e-10** and per-allele odds ratio **3.7865156483986326**. The scan's genomic inflation factor was **1.1143373639509648**.

Independent replication tested **1** candidate and replicated **1**. For **rs000008**, **119** participants had genotype calls, comprising **59** affected and **60** unaffected participants. Its replication p-value was **5.037312231519292e-05**, its per-allele odds ratio was **3.2240861372085563**, and the direction matched discovery. It therefore passes the protocol's replication rule and may be reported.

## What changed and what it achieved

Quality filtering removed the participants and variants named above before inference. This kept the plate in service rather than triggering re-genotyping, produced a clean retained analysis set, and prevented low-call-rate, rare, or control-disequilibrium variants from entering the multiplicity burden. The ancestry precondition was checked before association testing. Bonferroni control was then applied only over retained variants, and the sole discovery signal survived an independent same-direction replication.

## Recommended next actions and control plan

- Report **rs000008** as the replicated panel association, while describing the odds ratios as estimates rather than causal effects.
- Confirm the **rs000008** calls with an orthogonal genotyping assay and review cluster plots and sample provenance before biological interpretation.
- Investigate the excluded participant call failures and the variant-specific QC failures; retain the present thresholds as release gates for any future batch.
- Preserve the participant exclusions, variant exclusions, ancestry check, primary model specification, multiplicity threshold, and replication-direction rule in a locked analysis record.
- Seek functional follow-up and replication in an additional population; do not generalize beyond ancestries represented by these cohorts without another structure assessment.
