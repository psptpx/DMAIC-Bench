# Candidate-region association study: final status

## Executive conclusion

The plate can carry an analysis. Participant QC excluded **3** of **240** participants, a failure fraction of **0.0125**, below the protocol's re-genotyping threshold of **0.1**. After all QC, **237** participants and **139** variants entered the cohort assessment.

Affected and unaffected participants can be compared: the genotype PCA found **no complete separation** on the **10** assessed leading axes. Because the overlapping structure on PC**5** was associated with affection status at p = **0.012780035217122461**, that axis was included as a covariate in the definitive association scan.

The adjusted scan found **0** associations at the Bonferroni threshold of **0.00035971223021582735**. Accordingly, **0** variants were nominated and **0** replicated. No panel association should be reported.

## Participant QC and plate disposition

The participant call-rate requirement was **0.95**. The failed participants were P085 (call rate **0.9466666666666667**), P136 (**0.94**), and P193 (**0.94**). Thus, all participants except those named were retained: **119** affected and **118** unaffected participants. The failures comprised **1** affected and **2** unaffected participants.

The observed failure fraction of **0.0125** does not exceed **0.1**, so the protocol does not trigger plate re-genotyping.

## Variant QC

Of **150** assayed variants, **11** failed and **139** were retained. The exact exclusions are:

- Call rate below **0.95**: rs040024, rs040041, rs040044, rs040059, rs040134.
- Minor-allele frequency below **0.01**: rs040066, rs040114, rs040124, rs040130.
- Unaffected-participant exact HWE p below **0.000001**: rs040065, rs040128.

All assayed variants not listed above were retained. The failure categories did not overlap: **5** failed call rate, **4** failed frequency, and **2** failed HWE.

## Cohort comparability

PCA used mean-imputed, standardized genotypes from the post-QC matrix. Case and control ranges overlapped on every one of the **10** axes assessed; the PC**5** range-overlap fraction was **0.7758686254811826**. PC**1** had p = **0.5175080156482313**, while PC**5** had the smallest axis p = **0.012780035217122461**. This supports comparison rather than stopping for separate ancestries, while adjusting for PC**5**.

## Discovery association

The definitive additive per-allele logistic likelihood-ratio scan tested **139** retained variants in **237** retained participants, adjusted for PC**5**. All models converged. The Bonferroni threshold was **0.00035971223021582735**, and **0** variants crossed it. The smallest adjusted result was rs040143 at p = **0.009764236067045505**, with per-allele odds ratio **1.8738886627352376**; it is not significant. The adjusted genomic-inflation estimate was **0.8395109657830087**.

As a sensitivity analysis, the unadjusted scan also found **0** significant variants and had genomic-inflation estimate **1.112116290448235**. It does not alter the protocol-facing adjusted conclusion.

## Independent replication and reporting

The released replication cohort contained **0** nominated discovery hits because discovery produced none. Therefore **0** variants could replicate; no variant-level replication test was applicable. The protocol would require p below **0.05** in the same direction, but there is no discovery association to test. This is not missing data or a denied batch—the replication batch was released, and the empty candidate set follows from the discovery result.

## Recommended next action and control

Do not report any panel variant as associated with affection status. Preserve the participant and variant exclusion lists, PCA preprocessing, PC**5** adjustment, and Bonferroni rule with the analysis record. Do not promote nominal results for replication after seeing their p-values. If investigators pursue the trait further, define a new, prospectively powered study or a broader panel and pre-register its ancestry and association model before examining outcomes. The current replication cohort should remain independent for genuinely pre-specified future candidates rather than being mined after this negative scan.
