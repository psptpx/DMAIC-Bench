# Investigator report

## Decision
The plate is usable, but **no association is currently reportable**. The discovery scan nominated rs070008; the independent cohort did not replicate it. This is not proof that the variant has no effect, and it is not evidence that the assay plate failed. The protocol's replication requirement, not discovery significance alone, determines reporting.

## Quality and retained cohort
Participant call-rate filtering removed **3** participants (failure fraction **0.0125**), leaving **237**: **118 affected** and **119 unaffected**. This passes the protocol's plate-level failure rule; re-genotyping the entire plate is not triggered. Excluded participants are P016, P077 and P139. All other discovery participants are retained. The complete participant-level decisions are in `sample_qc.csv`.

Variant filtering, recomputed after participant exclusion, retained **139** variants and excluded **11**. There were **5** call-rate failures, **4** minor-allele-frequency failures and **2** control Hardy–Weinberg failures. Control Hardy–Weinberg testing used an exact conditional probability test, not a sparse-cell chi-square approximation.

Excluded for call rate: rs070023, rs070047, rs070114, rs070131, rs070148. Excluded for minor-allele frequency: rs070013, rs070049, rs070069, rs070099. Excluded for Hardy–Weinberg departure: rs070025, rs070133. All other supplied discovery variants are retained. `variant_qc.csv` gives the complete retained list and metrics. These exclusions are analytical changes; no physical assay intervention has been performed.

## Can affected and unaffected participants be compared?
PCA used retained variants, pooled-mean imputation for missing calls, and allele-frequency standardization. The leading axis had affection-status comparison p = **0.899718**, with variance fraction **0.022737**; the next axis had p = **0.164031**. Score ranges overlapped on every examined leading axis. Across **10** inspected axes there was no non-overlapping case/control ancestry separation. The isolated nominal differences on later axes do not establish separate ancestries, particularly when inspecting multiple axes.

These findings support a primary unadjusted additive trend analysis on this panel. They do not prove absence of all ancestry confounding: a candidate-region panel is weaker ancestry evidence than genome-wide ancestry markers. Relatedness, population labels and technical-batch confounding were not established from these files.

## Discovery and independent replication
Observed-call additive trend tests used a Bonferroni threshold of **0.0003597122**. There was **1** significant discovery variant: **rs070008**, p = **0.000005871729**. Genomic inflation was **0.917909**. Additive logistic regression estimated an odds ratio of **2.395108** per coded allele, with confidence bounds **1.621727–3.537305**. The biological identity of the coded allele is not supplied, so this is not a named risk-nucleotide claim.

Independent replication evaluated **1** candidate and replicated **0**. For rs070008, the replication trend p was **0.543816**, and the coded-allele odds ratio was **1.183500**. Direction agreed, but significance did not. The candidate call rate was **0.991667**, with minor-allele frequency **0.306723**; its observed calls included **60 affected** and **59 unaffected** participants. Replication therefore does **not** support reporting the discovery association.

In response, the discovery scan was reconsidered with an exploratory additive logistic model adjusted for **10** leading PCs. It yielded **0** corrected associations; rs070008 had p = **0.0006533933**, and genomic inflation was **1.266132**. This sensitivity analysis cannot rescue failed replication. PCs estimated on the candidate panel can partly absorb genuine local signal; the adjusted scan is not a new confirmatory analysis.

## Interpretation and next actions
The immediate cause of the reporting stop is failed independent confirmation. Sampling variation, discovery effect inflation, residual structure or technical artifacts remain possible explanations; this run does not identify a unique causal explanation. Do not describe the discovery hit as validated, and do not interpret the negative replication as proof of no effect.

Before further claims, audit genotype clusters and missingness at the candidate, verify allele coding across cohorts, check sample identity and relatedness, and obtain ancestry-informative markers and technical-batch metadata. Plan a sufficiently powered independent validation under a frozen analysis plan rather than changing thresholds after seeing results. Any new candidate arising from exploratory adjustment needs independent confirmation.

Hold the result through versioned raw data, the supplied computation scripts, participant and variant manifests, and archived discovery and sensitivity tables. Enforce the same quality, comparability and replication gates on future releases. No steward batch was denied. Broader ancestry, identity and causal explanations were not computed from unavailable metadata and are not asserted here. The retained plate can support this bounded negative reporting decision, not a general claim that the panel contains no true associations.

## Audit trail
`trace.json` contains quantitative outputs in execution order. `analysis.py`, `scan.py`, `replicate.py` and `reconsider.py` document the methods. Report quantities are rounded from trace outputs; participant and variant strings are identifiers. The QC manifests provide the exhaustive membership decisions.
