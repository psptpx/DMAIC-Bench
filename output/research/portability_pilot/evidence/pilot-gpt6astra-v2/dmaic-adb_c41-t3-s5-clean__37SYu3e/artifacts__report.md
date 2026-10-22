# Study decision

The discovery plate is usable after protocol QC, but **no variant is reportable as associated**. Affected and unaffected participants have substantial, overlapping ancestry structure. Comparison is defensible only after adjustment, not as an unadjusted case-control scan. The adjusted analysis found no discovery association meeting the panel-wide threshold. This is absence of sufficient evidence, not evidence that genetic effects are absent.

## Plate and retention

Participant call-rate filtering excluded **3** participants (failure fraction **0.0125**), below the re-genotyping trigger of **0.1**. The minimum retained call rate was required to be **0.95**. The plate therefore does not require wholesale re-genotyping under this rule. Retained cohort: **237** participants, comprising **120** affected and **117** unaffected.

Excluded participants: P127, P142, P195. All other supplied discovery participants are retained. `sample_qc.csv` gives the exhaustive identifiers, measured call rates and decisions.

Variant QC was applied after participant filtering, with allele frequency computed across retained participants and a two-sided exact Hardy–Weinberg test in unaffected participants. **11** variants failed and **139** were retained: **5** failed call rate, **4** failed minor-allele frequency, and **2** failed control Hardy–Weinberg equilibrium.

Excluded variants: rs050014, rs050017, rs050019, rs050052, rs050071, rs050082, rs050091, rs050092, rs050096, rs050108, rs050121. Every other supplied variant is retained. `variant_qc.csv` is the exhaustive retained/excluded manifest and contains the call-rate, frequency and equilibrium results. Exclusion reasons identify poor completeness, rare alleles and equilibrium departures; they do not establish a laboratory root cause.

## Cohort comparability and association

PCA used retained variants, mean imputation solely for PCA, and allele-frequency variance standardization. Leading-axis scores were compared using Welch tests and checked for group-range overlap before association testing. The leading axis explained **0.0909925** of genotype variance and differed strongly by affection status (p = **4.31637e-16**), but group ranges overlapped. The next axis had p = **0.239306**. No inspected leading axis showed disjoint case/control ranges. This supports overlapping structure rather than an entirely non-comparable cohort; overlap of ranges alone does not prove absence of all confounding.

We fitted additive logistic regression, adjusting for **2** leading genotype PCs, using available calls separately for each variant. The dominant ancestry axis motivated adjustment; the next leading axis was included conservatively. The Bonferroni threshold over retained variants was **0.000359712**. There were **0** significant variants. Genomic inflation was **1.01197**, computed as the median additive Wald statistic relative to its null median. The smallest adjusted p-value was **0.0053186299**, above the threshold. `discovery_association.csv` contains all variant results. No unadjusted scan was used to nominate discoveries, and no before/after inflation reduction is claimed.

## Replication and interpretation

The independent replication batch was released successfully; there was no denied data request. It explicitly nominated no discovery hit, consistent with our computed scan. There are **0** candidates and **0** replicated discoveries. This is an empty-candidate audit, not a failed replication experiment: replication association p-values and directions were not estimated because there is no eligible discovery association. We did not turn the replication cohort into a fresh discovery screen. It cannot rescue subthreshold discovery findings under the protocol.

## Actions and maintenance

The analytical change was to remove failing samples and variants and account for overlapping ancestry structure before testing. This achieved a QC-compliant, ancestry-adjusted scan with near-null median inflation, but yielded no reportable association. No laboratory intervention or new recruitment was performed.

Investigators should report the negative corrected panel result with its limited scope; avoid claiming equivalence or absence of genetic contribution. Review excluded calls and equilibrium departures with the laboratory, preserve the retained-set manifests, and retain the protocol, scripts and complete results as the audit trail. For a future study, recruit ancestry-balanced affected and unaffected participants, add suitable ancestry markers or reference information, assess relatedness and other covariates, and plan sample size prospectively. Candidate-panel PCA is an imperfect ancestry proxy and residual structure remains possible. Apply the same QC and ancestry checks before future scans, lock multiplicity rules in advance, and require an independent same-direction replication before announcing any future hit. Power, relatedness and broader ancestry validation were not computed here.
