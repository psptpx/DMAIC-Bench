# Candidate-region study: investigator report

## Decision
The plate passes the protocol's participant-quality stop rule and supports a qualified panel-level association conclusion. **rs000008** passes the retained-panel Bonferroni threshold. This is association, not causality or clinical validation. The retained cohort shows no separation on the leading genotype-derived ancestry axis; comparison is reasonable on the available evidence, but this candidate panel cannot rule out subtle ancestry confounding.

## Quality and retained cohort
Of 240 participants, 5 failed call-rate QC (fraction 0.02083333). Retained: 235, comprising 117 affected and 118 unaffected. Whole-plate re-genotyping is not triggered. Excluded participant identifiers: P011, P059, P069, P224, P225. Every other supplied participant is retained; the complete explicit lists are in `participants_qc.json`.

Of 150 variants, 12 failed and 138 were retained. Failures by rule: call rate 5, minor-allele frequency 4, and control Hardy–Weinberg equilibrium 3. Variant QC was computed after participant filtering; Hardy–Weinberg testing used the exact two-sided probability test in unaffected participants. Excluded variant identifiers: rs000031, rs000049, rs000060, rs000078, rs000086, rs000093, rs000114, rs000126, rs000135, rs000138, rs000142, rs000148. Every other supplied variant is retained. `variants_qc.json` records each identifier, decision and QC measurement.

These exclusions are the only implemented change: they remove unreliable calls, very rare variation and departures from control equilibrium. They do not establish the laboratory cause of any failure. No laboratory remediation or new recruitment has occurred.

## Comparability
PCA used mean-imputed retained calls, centered and scaled by allele-frequency variance. The leading component explained 0.02125334 of variance; its affection-group Welch test gave p=0.26036225. Group ranges overlap. This is not the disjoint-ancestry stop branch. A later inspected component had a nominal group difference (p=0.003001952), so an adjusted sensitivity analysis was also performed. That observation does not by itself establish ancestry structure: regional association can contribute to panel PCs.

The steward could not route the request for independent ancestry records, and the study lead supplied no matching ancestry fact. This was not a denied existing batch. Independent ancestry validation was therefore unavailable; the inference is limited to panel-derived structure assessment.

## Association
Additive Cochran–Armitage score tests used nonmissing calls separately for each retained variant. The computed Bonferroni threshold is 0.00036231884058. There were 1 significant variants, with genomic inflation factor 0.82676225. For rs000008, p=7.473389145e-07.

Logistic Wald tests adjusted for 5 leading panel PCs also retained 1 significant variants: rs000008. For rs000008, adjusted p=6.403565567e-06; adjusted inflation factor 0.80258828. This is a sensitivity analysis, not an independently prespecified ancestry model. Same-panel adjustment can absorb regional effects. Full results are in `association_results.json`. No other variant met the corrected criterion; this does not demonstrate absence of effects or adequate power.

## Next actions and control
Validate the implicated variant's calls with an orthogonal assay and replicate the association in an independent, ancestry-matched cohort. Obtain independent ancestry markers and recruitment metadata before treating the result as definitive. Investigate sample failures, missingness and equilibrium failures with the laboratory rather than attributing them to a cause from these data alone.

Freeze the protocol, retained-ID manifests, code and results together. For future plates, enforce the same participant stop rule, variant filters and ancestry prerequisite before association; log exclusions and rerun the entire pipeline after corrected calls. No replication, laboratory improvement or sustained-control outcome has yet been measured.

## Audit
`trace.json` contains computed summaries and variant test outputs; `analyze.py` reproduces the analyses from steward JSON batches. All numerical report results are drawn from trace outputs. QC manifests identify exactly what the analysis changed.
