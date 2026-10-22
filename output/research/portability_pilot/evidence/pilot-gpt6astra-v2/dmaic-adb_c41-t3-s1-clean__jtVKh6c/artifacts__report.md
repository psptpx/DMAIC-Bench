# Study status: technically usable plate, noncomparable discovery cohort

## Decision for the principal investigator
Do not report a variant association from this cohort. The plate clears the protocol's participant-quality gate, but affected and unaffected participants are completely separated on the leading genotype ancestry axis. This is the protocol's stop condition, not the overlapping-structure situation in which adding ancestry covariates would permit testing. The result is **non-identifiability of a disease association on this design**, not evidence that the panel has no biological effects.

## Quality review and retained material
Participant call rates were calculated from all supplied discovery calls before filtering. Of 240 participants, 2 failed the call-rate requirement of 0.95; the failure fraction was 0.00833333, below the plate re-genotyping trigger of 0.1. The retained cohort contains 238 participants: 119 affected and 119 unaffected.

Excluded participants: P039, P197. All other supplied participant IDs are retained by technical QC. `sample_qc.csv` gives every identity, call rate and retention decision.

Variant QC was computed after participant filtering, using observed-call frequency and exact probability-ordering Hardy–Weinberg tests in unaffected participants. The requirements were call rate at least 0.95, minor-allele frequency at least 0.01, and control Hardy–Weinberg p at least 1e-06. There were 5 call-rate failures, 4 frequency failures and 3 Hardy–Weinberg failures. Overall 12 variants failed and 138 were retained.

Excluded variants: rs010047, rs010057, rs010063, rs010072, rs010088, rs010092, rs010101, rs010118, rs010128, rs010133, rs010141, rs010149. All other supplied variant IDs are retained by technical QC; `variant_qc.csv` is the complete retention manifest with measured criteria. Technical retention does not authorize an association analysis in a confounded cohort.

## Cohort comparability
PCA used retained genotypes, mean imputation of missing calls, and allele-frequency standardization. Affection groups were compared on leading scores with Welch tests, and score ranges were inspected for overlap. The leading axis accounts for a variance fraction of 0.09427730; its phenotype-comparison p-value is 3.65407e-129. More importantly, its affected range is [-5.899208, -1.484927] while its unaffected range is [0.304689, 6.737617]. There is no overlap. Axis sign is arbitrary and does not affect this conclusion.

This pattern is consistent with ancestry/recruitment confounding and fails the pre-test comparability requirement. The panel alone does not prove a named ancestry or the administrative cause of the split; batch or recruitment records should be audited. A study-lead request for those facts was unroutable, so no confirming metadata or replacement cohort was obtained. The request for replacement records routed back to the existing discovery batch; it was not a release of new participants. No batch was explicitly denied.

## Association and replication
No variant association test, odds-ratio estimate, genomic-inflation statistic or replication test was computed. No discovery candidate can validly be nominated on this noncomparable design, so replication was not pursued. This is not a finding of no significant or no replicated variants. Bonferroni control and independent same-direction replication remain mandatory downstream requirements, but neither can repair the failed discovery precondition.

## Action, change and control
The analysis removed low-quality participants and variants; this achieved a technically retained dataset but did not resolve the ancestry split. No laboratory re-genotyping or recruitment change was performed. Re-genotyping is not mandated by the observed plate failure fraction and would not by itself fix recruitment confounding.

Pause association reporting. Audit sample identity, phenotype coding, recruitment ancestry and laboratory allocation. Recruit or assemble affected and unaffected participants with genuine within-ancestry overlap, with balanced processing. Re-run the frozen QC and ancestry checks on that corrected cohort before opening any association results. If structure overlaps, include its leading axes as covariates; if it remains separated, keep the stop in force. Only then apply the protocol's multiplicity threshold, estimate effects, and seek independent replication with verified allele orientation. Nonreplication must withhold reporting and trigger reconsideration of discovery.

Hold the process through a signed pre-analysis comparability gate, versioned sample and variant manifests, retained protocol, and independent review of replication. `trace.json`, `analyze.py`, the QC tables and `pca.csv` preserve the computations and decisions behind this report.
