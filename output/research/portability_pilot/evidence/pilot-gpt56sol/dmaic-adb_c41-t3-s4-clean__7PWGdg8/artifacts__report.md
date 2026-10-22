# Candidate-region association study report

## Executive conclusion

The plate can support the prespecified analysis. Every released participant was retained: **240** participants, comprising **120** affected and **120** unaffected participants. The participant failure fraction was **0.0**, below the protocol maximum of **0.1**, so re-genotyping is not triggered.

After variant QC, **140** variants were retained and **10** were excluded. The affected and unaffected groups were not separated by the genotype-derived ancestry check (`separated = false`), so they can be compared on this cohort without ancestry-axis covariates. The association analysis found **0** variants meeting the prespecified family-wise criterion. Therefore, this panel provides no protocol-level evidence that a tested variant is associated with affection status in this cohort.

## Participant and plate quality

Participant call rate was calculated across the released panel and compared with the inclusive protocol threshold of **0.95**. The minimum observed participant call rate was **0.9533333333333334** and the maximum was **1.0**. No participant failed, so the retained participant set is the complete released cohort; there are no excluded participant identifiers.

This yields a plate-pass verdict. Nothing was changed at the participant level, because no exclusion or re-genotyping was warranted.

## Variant quality and retained set

A variant was retained only when it met all three prespecified rules: call rate at least **0.95**, minor-allele frequency at least **0.01**, and Hardy–Weinberg p-value among unaffected participants at least **0.000001**.

The excluded variants are: rs040038, rs040054, rs040057, rs040072, rs040104, rs040106, rs040110, rs040112, rs040113, rs040125.

Of the exclusions, **5** failed call rate, **3** failed minor-allele frequency, and **2** failed the unaffected-participant Hardy–Weinberg rule. These reason counts are criterion counts for the observed exclusions. The retained set is every released variant other than the excluded identifiers above, totaling **140** variants.

The filtering change removed protocol-ineligible variants before any association claim was considered.

## Cohort comparability

PCA was run on the participant-retained and variant-retained genotype matrix after mean imputation and allele-frequency standardization. Affected and unaffected PC1 ranges overlapped (`pc1RangesOverlap = true`), and the PC1 comparison gave p = **0.8990497051966733**. PC1 accounted for a variance fraction of **0.02098564776332856**. On this computed check, the groups are not drawn from visibly separated genotype clusters and can be compared. Because no structure associated with affection status was detected, the unadjusted additive trend-test route was used rather than adding ancestry axes as covariates.

A first PCA implementation failed because its optional software dependency was unavailable. It produced no result and was not used. The successful result was recomputed from the same matrix using NumPy singular-value decomposition and is recorded separately in the trace.

## Association analysis

Two-sided additive Cochran–Armitage trend tests were run for **140** retained variants using available genotype calls. The family-wise alpha was **0.05**, giving a computed Bonferroni threshold of **0.00035714285714285714**. The smallest observed p-value was **0.020881951144371365**, which did not pass that threshold. The genomic-inflation factor was **0.8903762915485509**. Accordingly, no variant is declared associated.

This is an absence of statistically significant evidence under the protocol, not proof that every variant has no effect.

## Recommended next actions and control plan

* Do not promote any panel variant as associated from this analysis.
* Preserve the participant and variant inclusion lists, QC metrics, PCA route decision, and complete per-variant test results generated in this run as the audit record.
* If investigators pursue the leading signals, treat them as exploratory and test them in an independent, appropriately powered cohort rather than weakening the prespecified threshold.
* For future batches, rerun the same participant-first gate, the same three-part variant filter, and the ancestry check before association testing. Continue to calculate the multiplicity threshold from the actually retained variant count.
* Investigate assay performance for the call-rate and Hardy–Weinberg exclusions before redesigning or reusing the panel; do not restore excluded variants without new genotype evidence that passes the protocol.
