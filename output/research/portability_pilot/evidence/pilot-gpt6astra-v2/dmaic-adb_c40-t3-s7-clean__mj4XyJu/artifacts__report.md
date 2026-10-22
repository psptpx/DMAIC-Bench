# Compound-expression study: release decision

## Executive conclusion
**Withhold the candidate list and reconsider the panel findings.** The sequencing libraries are technically usable and the intended treatment contrast is estimable, but independent qPCR does not support release. This is a validation failure, not evidence that the compound has no biological effect.

## Libraries and design
All 12 libraries passed the facility's read-depth and mapping criteria; failed libraries: 0. Control and treated arms each retain 6 usable biological replicates, so replication is sufficient. No libraries were removed or re-sequenced.

There is 1 shared preparation batch. The intercept-plus-treatment design has rank 2 for 2 columns: treatment is not confounded with batch. A separate batch effect cannot be estimated within this single batch and is not needed as an additional model term. Thus the planned comparison can be made on this design; the present obstacle is downstream validation rather than preparation-batch aliasing.

## Panel analysis: provisional evidence only
Counts were normalized by each library's total panel count and transformed to log CPM with a unit pseudocount. Independent, two-sided Welch tests compared treated and control log expression; Benjamini–Hochberg correction covered all 400 genes. Calls required adjusted p < 0.05 and absolute log fold change on the base-two scale >= 1.0. This produced 39 provisional calls.

This is a log-expression approximation, not a fitted negative-binomial count model. Panel-total normalization assumes panel-wide composition is sufficiently stable; large composition changes or low counts can affect inference. The numerical calls therefore describe this analysis, not an independently verified biological list. Full results are saved in `gene_results.csv`.

### Provisional panel calls (not authorized for release)
| Gene | Treated minus control log fold change | Adjusted p |
|---|---:|---:|
| G0002 | -1.805165 | 0.00115184 |
| G0005 | -2.111628 | 0.00103086 |
| G0038 | 2.463324 | 0.000440625 |
| G0045 | 1.345138 | 0.000361457 |
| G0055 | 2.062115 | 0.000190508 |
| G0060 | -1.756971 | 0.0013101 |
| G0062 | 2.112593 | 0.000344296 |
| G0100 | -1.720697 | 0.000733074 |
| G0108 | -2.730111 | 7.62572e-05 |
| G0112 | -2.395912 | 0.000745252 |
| G0125 | -2.883737 | 0.000440625 |
| G0153 | 2.725603 | 0.00014445 |
| G0156 | -1.980041 | 0.00014445 |
| G0165 | 1.848621 | 0.000745761 |
| G0169 | 1.740637 | 0.0013101 |
| G0173 | 1.930730 | 0.00337853 |
| G0210 | -1.823846 | 0.0115758 |
| G0214 | -2.584330 | 0.000135947 |
| G0215 | -2.522977 | 0.000135947 |
| G0237 | -1.704942 | 0.00446048 |
| G0239 | 1.637577 | 0.001145 |
| G0241 | -2.858270 | 0.00160616 |
| G0244 | 2.163553 | 0.000185918 |
| G0247 | -1.837560 | 0.00256441 |
| G0263 | 1.420113 | 0.00832138 |
| G0265 | -1.722952 | 0.000135947 |
| G0267 | -2.126963 | 0.00192201 |
| G0271 | 1.285948 | 0.000871378 |
| G0284 | 2.813274 | 0.000135947 |
| G0314 | -2.245645 | 0.000599262 |
| G0327 | 2.164490 | 0.000135947 |
| G0333 | -2.290793 | 0.000871378 |
| G0339 | -2.294021 | 5.09684e-05 |
| G0341 | 1.551648 | 0.000194149 |
| G0366 | -2.644122 | 0.000670168 |
| G0370 | 2.131222 | 0.000185918 |
| G0372 | -2.110070 | 0.000135947 |
| G0379 | -1.716036 | 0.000745252 |
| G0387 | 2.276487 | 0.000185918 |

## Independent validation
The archive's nominated leading-candidate subset contains 10 genes. Independent two-sided Welch tests were applied to the qPCR log-relative-expression replicates. Confirmation required p < 0.05 and agreement with the nominated panel direction. There were 0 confirmations: concordance 0.0 against the required 0.75. The subset is not a validation experiment for every panel call, and the facility rule prohibits rescuing a list by selecting other unvalidated calls.

| Nominated gene | qPCR effect | p | Confirmed |
|---|---:|---:|---|
| G0125 | -0.131250 | 0.423329 | No |
| G0241 | 0.260500 | 0.463912 | No |
| G0284 | 0.201500 | 0.552641 | No |
| G0108 | -0.338750 | 0.324079 | No |
| G0153 | -0.011000 | 0.954220 | No |
| G0366 | -0.308000 | 0.064897 | No |
| G0214 | -0.106500 | 0.717203 | No |
| G0215 | 0.265750 | 0.057324 | No |
| G0038 | -0.240750 | 0.439072 | No |
| G0112 | -0.178750 | 0.297004 | No |

Gene-set annotation was requested but **locked** because validation did not pass. It was not denied as nonexistent. No enrichment was computed and no pathway claim is justified. The conclusion stops at failed independent validation.

## Business response and sustainment
The analysis changed the disposition from provisional panel candidates to a withheld list. This prevents unsupported candidates from being issued; no physical process change or successful remediation has yet been demonstrated.

The observed cause of withholding is the panel–qPCR discrepancy. Its underlying cause remains unresolved. The facility should audit sample identities, compound exposure records, assay target/isoform agreement, qPCR reference-gene stability, normalization assumptions and raw assay quality. Refit count-aware expression models with robust normalization as a sensitivity check, without treating a different model as permission to bypass validation. Insufficient validation power, assay differences and a nonreproducible panel signal remain possibilities, not established causes.

After resolving assay and provenance concerns, run a prospectively specified independent biological validation with justified power. Randomize and balance arms across any new preparation batches, preserve the QC and identifiability gates, and retain the original nomination and confirmation criteria. Release only after the independent validation gate passes; otherwise continue withholding. Archive raw data, analysis scripts, full result tables and signed release decisions so the gate cannot be silently bypassed. Nothing in this run establishes that corrective work has already improved reproducibility.
