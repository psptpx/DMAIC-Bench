# Compound-expression study: withhold the candidate list

## Executive decision
The libraries are technically usable and the compound-versus-vehicle comparison is estimable. The panel analysis produces **40 provisional gene calls**, but independent qPCR confirms **0 of 10 tested candidates**. Concordance is **0.00**, below the facility requirement of **0.75**. Do not issue a validated compound-response list or claim a confirmed molecular mechanism. This failure does not prove that the compound has no biological effect.

## Library and design readiness
All 12 libraries pass the facility's assigned-read and mapping-rate rules; 0 fail. The control and treated arms retain 6 and 6 usable biological replicates, respectively, satisfying the replication gate. The observed minimum assigned-read count is 9,235,000 and minimum mapping rate is 0.865.

There is 1 shared preparation batch. The intercept-and-treatment design has rank 2 for 2 columns: treatment is not confounded with preparation batch. A separate between-batch variance assessment is not estimable from this design and was not attempted. Additional batch adjustment is unnecessary for the shared batch.

## Panel analysis: provisional, not validated
Counts were normalized by median-of-ratios size factors using genes positive in every library. A treatment-only linear model was fitted to log-transformed normalized counts with a unit pseudocount; treatment coefficients are log-base-two effects. Two-sided residual-variance t tests were corrected by Benjamini–Hochberg across all 400 genes. Calling required adjusted p < 0.05 and absolute log fold change >= 1.0.

This yielded 17 upward and 23 downward calls. This is an explicit log-count linear-model analysis, not a negative-binomial or precision-weighted count analysis. Low-count effects and variance assumptions merit sensitivity analysis before any renewed release decision. The following are **withheld exploratory panel findings**, not an issued candidate list.

| Gene | Treatment log fold change | BH adjusted p |
|---|---:|---:|
| G0002 | -1.6672 | 0.0011001 |
| G0005 | -1.9616 | 0.000615334 |
| G0019 | -1.9859 | 0.00967874 |
| G0038 | 2.5543 | 0.000213262 |
| G0045 | 1.4416 | 0.000122188 |
| G0055 | 2.1721 | 1.26785e-05 |
| G0060 | -1.5450 | 0.000645708 |
| G0062 | 2.2205 | 0.000122188 |
| G0100 | -1.5732 | 0.000513104 |
| G0108 | -2.6078 | 1.26785e-05 |
| G0112 | -2.2626 | 0.000254669 |
| G0125 | -2.5936 | 0.00014729 |
| G0153 | 2.7881 | 8.76904e-05 |
| G0156 | -1.8485 | 0.000116315 |
| G0165 | 1.9586 | 0.000453198 |
| G0169 | 1.8452 | 0.000645708 |
| G0173 | 2.0144 | 0.000553313 |
| G0210 | -1.5806 | 0.00688117 |
| G0214 | -2.4098 | 0.000116315 |
| G0215 | -2.3627 | 0.000109929 |
| G0237 | -1.5868 | 0.00688117 |
| G0239 | 1.7458 | 0.000319639 |
| G0241 | -2.6949 | 0.000490516 |
| G0244 | 2.2683 | 0.000108117 |
| G0247 | -1.6761 | 0.00358974 |
| G0263 | 1.5194 | 0.00558976 |
| G0265 | -1.6021 | 0.000103279 |
| G0267 | -1.9945 | 0.000170191 |
| G0271 | 1.3937 | 0.000319639 |
| G0284 | 2.9221 | 4.46493e-05 |
| G0314 | -2.1200 | 0.000157578 |
| G0327 | 2.2749 | 1.26785e-05 |
| G0333 | -2.1746 | 0.000206718 |
| G0339 | -2.1362 | 1.26785e-05 |
| G0341 | 1.6573 | 0.000133775 |
| G0366 | -2.4153 | 0.000122188 |
| G0370 | 2.2378 | 0.000116315 |
| G0372 | -1.9722 | 0.000103279 |
| G0379 | -1.5880 | 0.000170191 |
| G0387 | 2.3816 | 0.000118987 |

## Independent validation
The archive supplied qPCR for its nominated leading-candidate subset, with 4 independent biological replicates per arm. The denominator is the 10 supplied validation candidates, not the entire panel-call set. Every supplied candidate was also called by this analysis. Two-sided Welch independent-sample t tests compare treated against control on the supplied log-relative-expression measurements. Confirmation requires nominal p < 0.05 and agreement with the panel direction; a directional trend alone is insufficient.

| Gene | qPCR treated minus control | p value | Confirmed |
|---|---:|---:|---|
| G0125 | -0.13125 | 0.423329 | No |
| G0241 | 0.26050 | 0.463912 | No |
| G0284 | 0.20150 | 0.552641 | No |
| G0108 | -0.33875 | 0.324079 | No |
| G0153 | -0.01100 | 0.954220 | No |
| G0366 | -0.30800 | 0.064897 | No |
| G0214 | -0.10650 | 0.717203 | No |
| G0215 | 0.26575 | 0.057324 | No |
| G0038 | -0.24075 | 0.439072 | No |
| G0112 | -0.17875 | 0.297004 | No |

The validation gate fails. The remaining panel calls have not been independently validated in the supplied data. No gene can be presented here as an independently confirmed compound response.

## Where the conclusion stops
The steward **locked** the gene-set annotation request because validation failed. This is not a finding that annotation does not exist. No annotation was released, no enrichment was computed, and no pathway significance can be reported. No requested batch was denied as nonexistent.

## Cause, corrective action, and sustained control
The immediate release blocker is panel–qPCR disagreement, not poor sequencing metrics, inadequate retained replication, or batch confounding. The underlying cause is undetermined: these data do not distinguish sample misidentification, assay-specific normalization or specificity problems, biological differences between validation and sequencing material, or an unstable panel estimate.

The analysis changed the disposition from exploratory panel nominations to a withheld list after independent validation. No laboratory remediation or repeat experiment has been performed, and no improvement in biological reproducibility has been demonstrated.

The facility should audit sample identity and chain of custody; reconcile compound exposure, collection conditions, and validation material with the panel experiment; review qPCR reference-gene stability, primer specificity, efficiency, and raw quality controls; and examine sequencing normalization and low-count sensitivity using a count-aware model. These are proposed investigations, not established causes or completed work. Resolve documented discrepancies before rerunning independent validation on prospectively specified candidates. If new library preparation is needed, randomize both arms within preparation batches and retain biological replication.

Hold release under a signed QC/design/validation checklist, preserve the original candidate denominator and directions, and rerun the same acceptance rule rather than selecting a favorable subset after validation. Only a satisfactory independent validation result should reopen list release and pathway interpretation. Archive source batches, scripts, full expression and validation result tables, and the trace so the decision remains reproducible.
