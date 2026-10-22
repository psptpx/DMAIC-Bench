# Study decision for the principal investigator

## Bottom line
The plate can support an ancestry-adjusted panel analysis, but no association is established. There are 0 significant variants after the protocol's multiple-testing correction. This is not evidence that the trait lacks a genetic component or that every panel variant is irrelevant.

## Plate and retained cohort
Computed call rates across the supplied 150 variants for 240 participants. There were 2 failures (fraction 0.00833333), below the protocol's plate-retyping trigger. Exclude P011, P120; retain every other participant listed in `participant_qc.csv`. This leaves 238 participants: 118 affected and 120 unaffected. No re-genotyping was performed or required by this trigger.

On those retained participants, variant call rate, minor-allele frequency, and exact conditional Hardy–Weinberg tests in unaffected participants removed 12 variants and retained 138. The individual rule failure counts were 5 for call rate, 4 for frequency, and 3 for Hardy–Weinberg equilibrium. Exclude rs050014, rs050017, rs050019, rs050040, rs050052, rs050071, rs050082, rs050091, rs050092, rs050096, rs050108, rs050121; retain all other variants in `variant_qc.csv`. That file gives the complete variant-by-variant metrics and decisions. These failures identify protocol exclusions, not proven laboratory mechanisms.

## Comparability must precede association
PCA used retained variants and participants, mean-imputed missing calls, and allele-frequency-standardized genotypes. The leading component explains a variance fraction of 0.090225; its Welch affection-group comparison gives p = 3.40801e-15. Its affected range is -4.87178 to 5.96628, versus -5.10707 to 5.36721 in unaffected participants. The ranges overlap: this is structure with imbalance, not complete ancestry separation. Accordingly, unadjusted testing would not be the appropriate primary comparison.

The analysis changed from a potential crude comparison to additive logistic regression adjusted for 2 leading genotype components. Missing genotypes were omitted per association model, rather than imputed for association. Likelihood-ratio tests compare each genotype model with its ancestry-only null. The ancestry axes are panel-derived proxies, not externally verified ancestry labels; a small candidate panel cannot fully establish population comparability. A separate ancestry-record request was unroutable, not denied. No separately released ancestry reference records were used.

## Association results
The computed Bonferroni threshold is 0.0003623188406. No retained variant meets it. The strongest result, rs050022, has p = 0.001432098, adjusted dosage odds ratio 2.35716, and 233 observed participants. It is not a declared association. Genomic inflation from the median likelihood-ratio statistic is 1.165337; this is a diagnostic, not proof of absence of residual confounding. No genomic-control rescaling was applied. Full results are in `association_adjusted.csv`.

## Next action and sustained control
Do not promote the leading nominal signal to a biological or clinical conclusion. Seek independent replication with ancestry-balanced recruitment and broader ancestry-informative genotyping. Verify sample provenance, relatedness, laboratory batch balance, and genotype coding before confirmatory work. These checks were not supplied or established by the present panel analysis. Confirm that panel-derived ancestry adjustment has not absorbed locus-specific effects, and prespecify covariate selection in replication.

The achieved change is an auditable cleaned cohort and an ancestry-adjusted analysis, not a laboratory intervention or a demonstrated before/after improvement. Preserve raw steward releases, the executable analysis, participant and variant exclusion manifests, ancestry scores, and association results. Apply the same protocol gates to future plates; require independent QC review and ancestry-overlap review before releasing association claims. Reassess residual structure using external ancestry markers rather than interpreting the current null result as conclusive exclusion of genetic effects.

## Audit trail
`trace.json` records computed outputs and branch choices; `analyze.py` reproduces QC, PCA, and adjusted testing. `participant_qc.csv` and `variant_qc.csv` define the exact retained sets, and `ancestry_pcs.csv` preserves participant scores. No data request was denied and no human provisioning was used. No unadjusted association analysis was run.
