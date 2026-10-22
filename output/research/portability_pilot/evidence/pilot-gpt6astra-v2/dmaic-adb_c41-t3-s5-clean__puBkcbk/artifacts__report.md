# Study decision for the principal investigator

## Bottom line
The plate can support a protocol-compliant analysis, but **no variant currently supports a reportable association**. Quality filtering leaves 237 participants and 139 variants. The cohorts overlap in ancestry, but ancestry is imbalanced by affection status, so an unadjusted comparison is inappropriate. The adjusted scan yields 0 significant associations. This is a negative panel result, not proof that the trait has no genetic component or that every tested effect is absent.

## Quality and retained cohort
Participant call rates were computed over the supplied discovery panel. Of 240 participants, 3 failed the protocol call-rate rule (failure fraction 0.0125), below the protocol plate-rejection limit. Re-genotyping the whole plate is therefore not triggered. Retained participants comprise 120 affected and 117 unaffected individuals.

Excluded participants: P127, P142, P195. All other supplied discovery participants are retained; `sample_qc.csv` is the complete membership and call-rate ledger.

Variant QC was recomputed after participant removal. Call rate and minor-allele frequency used retained participants; Hardy–Weinberg equilibrium used unaffected participants only, with a conditional, probability-ordered exact test. There are 11 failed variants: 5 call-rate failures, 4 frequency failures, and 2 equilibrium failures. The remaining 139 pass all protocol rules.

Excluded variants: rs050014, rs050017, rs050019, rs050052, rs050071, rs050082, rs050091, rs050092, rs050096, rs050108, rs050121. All other supplied panel variants are retained; `variant_qc.csv` contains every variant's metrics and disposition. These removals are analytical exclusions, not repaired genotype calls.

## Can affected and unaffected participants be compared?
Mean-imputed, allele-frequency-standardized PCA was run on retained calls before any association test. The leading axis differs by affection status (Welch p = 4.31637e-16), yet the group ranges overlap. Its variance fraction is 0.0909925. The next axis shows no clear group difference (p = 0.239306). None of the inspected leading axes has disjoint case/control ranges. These findings support an overlapping-structure route rather than stopping for completely separated ancestries.

The primary scan therefore used additive logistic regression with the leading 2 principal components as covariates. Including the next leading axis is a conservative adjustment beyond the clearly imbalanced first axis. Missing calls were excluded per variant in regression, not imputed as observed genotypes. A candidate-region panel gives limited ancestry resolution: range overlap and PCA do not establish that all confounding has been eliminated. Broader ancestry markers and recruitment information would strengthen this assessment.

## Discovery and replication
The computed Bonferroni threshold is 0.000359712 over retained variants. The adjusted scan has 0 significant variants, with genomic inflation factor 1.01197, computed from the median dosage Wald statistic relative to its null median. The smallest adjusted p-value is 0.00531863 at rs050012, still above the corrected threshold. Full adjusted effects, uncertainty, p-values and sample counts are in `association.csv` and the trace. No unadjusted discovery scan was run, so no numerical before/after reduction in significance is claimed.

Replication records are available, not denied. The independently computed discovery candidate count is 0, matching the empty steward nomination list. Accordingly the replicated count is 0 by empty-set accounting; **no replication association test was performed**. This is neither a replication failure nor a replication success for any variant. The replication reporting gate has no eligible discovery hit to evaluate; do not promote nominal discovery signals into confirmed findings.

## What changed, what it achieved, and what comes next
The analysis excluded low-quality participants and variants and explicitly adjusted for overlapping ancestry structure. The resulting scan has near-null median inflation and no corrected signals. That supports reporting a carefully qualified negative discovery result, not a biological or clinical association claim. No laboratory intervention or new recruitment has been performed, and their potential benefits have not been measured.

Investigators should archive this negative result and its QC ledger, review recruitment and ancestry balance, and obtain broader ancestry information before claiming that confounding is fully addressed. If further discovery is justified, pre-specify a larger, ancestry-balanced study with a prospective power calculation; power and a required future sample size were not computed here. Any future corrected hit must be allele-harmonized and independently replicated under the protocol before reporting.

Hold the process by freezing the supplied protocol, raw steward releases, scripts, exclusion ledgers and adjusted results; automate the plate stop rule, participant and variant filters, ancestry check, multiplicity correction and replication-direction check in future runs. Do not change thresholds or reroute nominal hits after seeing results.

## Audit
All reported numerical results are recorded as scalar outputs in `trace.json`; identifiers are labels rather than measured quantities. Scripts and CSV ledgers preserve the calculation path. The initial broad request was temporarily locked by release order; it was resolved by requesting the protocol and discovery batches explicitly. No required batch was denied. Replication effect estimates and future-study power were not computed, and no such estimates are inferred.
