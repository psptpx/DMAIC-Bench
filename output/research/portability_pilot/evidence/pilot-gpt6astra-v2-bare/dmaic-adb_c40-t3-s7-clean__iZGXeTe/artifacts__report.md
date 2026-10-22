# Compound-expression study: hold release

## Decision for the principal investigator
The libraries are technically adequate and the intended within-batch comparison is identifiable. The panel provides a **provisional discovery signal**, but independent qPCR does not support issuing a validated compound-responsive gene list. Withhold biological and pathway claims pending investigation and repeat validation. Failure to validate is not proof that the compound has no effect.

## Library and design assessment
Computed from the complete steward archives: 12 libraries were assessed, 0 failed the facility's joint read-depth and mapping criteria, and the minimum usable replication was 6 per arm versus a required 3. The lowest assigned-read count was 9,235,000, and the lowest mapping rate was 0.865. All libraries were retained.

There is 1 preparation batch shared by both arms. The intercept-plus-treatment design has rank 2; treatment is not confounded with batch. A treatment-only comparison is appropriate. A separate batch variance contribution cannot be estimated from this constant batch factor; no batch correction was applied. This establishes estimability, not randomization or immunity to unrecorded confounders.

## Expression analysis
The analysis used panel-total library normalization, a count-scale pseudocount before log transformation, and independent two-sided Welch tests on log expression. Benjamini–Hochberg adjustment covered all 400 panel genes. Calls required adjusted p < 0.05 and absolute log fold change >= 1.0. The resulting 40 provisional calls comprise 17 increases and 23 decreases.

This is a log-normal approximation, not a fitted count-dispersion model. Panel-total normalization assumes that broad panel composition changes do not dominate the signal. The full results are in `gene_results.csv`; estimates below are treated minus control on the binary-log scale. These are **discovery candidates, not validated findings**.

| Gene | Log fold change | Adjusted p |
|---|---:|---:|
| G0002 | -1.781182 | 0.00115025 |
| G0005 | -2.073668 | 0.00113662 |
| G0019 | -2.174951 | 0.0262258 |
| G0038 | 2.441260 | 0.000388478 |
| G0045 | 1.329376 | 0.000347237 |
| G0055 | 2.059981 | 0.000191555 |
| G0060 | -1.664059 | 0.00114248 |
| G0062 | 2.108348 | 0.000347237 |
| G0100 | -1.685910 | 0.000581388 |
| G0108 | -2.720102 | 7.04023e-05 |
| G0112 | -2.375577 | 0.000700488 |
| G0125 | -2.719480 | 0.000347237 |
| G0153 | 2.673777 | 0.000172615 |
| G0156 | -1.960580 | 0.000128549 |
| G0165 | 1.846496 | 0.00074839 |
| G0169 | 1.732749 | 0.00125603 |
| G0173 | 1.902838 | 0.0031367 |
| G0210 | -1.704053 | 0.00925963 |
| G0214 | -2.524406 | 0.000128549 |
| G0215 | -2.477280 | 0.000128549 |
| G0237 | -1.698890 | 0.00437864 |
| G0239 | 1.633534 | 0.00113662 |
| G0241 | -2.809162 | 0.00125603 |
| G0244 | 2.155824 | 0.000186186 |
| G0247 | -1.788999 | 0.00223096 |
| G0263 | 1.407255 | 0.00827065 |
| G0265 | -1.714368 | 0.000128549 |
| G0267 | -2.108335 | 0.00185119 |
| G0271 | 1.281461 | 0.000866369 |
| G0284 | 2.809917 | 0.000128549 |
| G0314 | -2.232945 | 0.00054624 |
| G0327 | 2.162717 | 0.000128549 |
| G0333 | -2.286643 | 0.000866369 |
| G0339 | -2.250740 | 5.11335e-05 |
| G0341 | 1.544917 | 0.000192417 |
| G0366 | -2.533501 | 0.000388478 |
| G0370 | 2.125724 | 0.000186186 |
| G0372 | -2.084905 | 0.000128549 |
| G0379 | -1.700747 | 0.00074839 |
| G0387 | 2.269301 | 0.000186186 |

## Independent validation and stopping point
Independent two-sided Welch tests used the supplied qPCR log-relative-expression replicates. A candidate had to show p < 0.05 in its nominated direction. Of 10 nominated candidates, 0 confirmed: concordance 0.0, below the required 0.75. Nominated directions were consistent with the panel calls. The validation result does not authorize extrapolating confirmation to the other discovery candidates.

| Candidate | qPCR treated-minus-control effect | p value | Confirmed |
|---|---:|---:|---|
| G0125 | -0.131250 | 0.423329 | No |
| G0241 | 0.260500 | 0.463912 | No |
| G0284 | 0.201500 | 0.552641 | No |
| G0108 | -0.338750 | 0.324079 | No |
| G0153 | -0.011000 | 0.95422 | No |
| G0366 | -0.308000 | 0.0648973 | No |
| G0214 | -0.106500 | 0.717203 | No |
| G0215 | 0.265750 | 0.057324 | No |
| G0038 | -0.240750 | 0.439072 | No |
| G0112 | -0.178750 | 0.297004 | No |

Gene-set annotation was requested but **locked**, not denied as nonexistent, because validation failed. No annotation data were released and enrichment could not be computed. Interpretation stops before pathway claims; no significant-set count is asserted.

## Cause, action, and sustainment
The immediate release blocker is lack of independent validation, not inadequate library metrics or preparation-batch confounding. The underlying biological or technical cause remains unknown. Possible explanations to investigate—not established causes—include sample identity or exposure mismatch, assay targeting differences, reference-gene instability, normalization sensitivity, and discovery overestimation.

No laboratory process change or repeat experiment was performed in this task. The analytical change was to move from provisional discovery calls to a release hold after applying the independent validation gate; it prevented unsupported issuance, but has not demonstrated an improvement in assay performance.

The facility should audit sample identity, compound exposure and timing, qPCR primer specificity and efficiency, reference-gene stability, and panel-to-assay target mapping. Reanalyse counts with a dispersion-aware model and assess normalization sensitivity without selecting methods for favorable validation results. Repeat independent biological validation after any documented correction, with prospectively specified candidates and unchanged acceptance rules. If needed, repeat the experiment with randomized arm allocation across preparation batches and balanced processing.

Hold the current candidate list as exploratory. The sequencing lead should retain library-QC and design checks; the validation lead should document assay qualification and concordance; the study lead should authorize release only after the existing gates are met. Archive the raw released batches, analysis scripts, full result tables, declarations, and this trace. No achieved corrective-action benefit or validated response list can currently be claimed.

## Audit trail
`trace.json` records computed scalar results and routing decisions; all displayed results derive from its outputs, with rounding for readability. Reproducible computations are in `analyze.py`, `design.py`, `expression.py`, and `validate.py`. The steward could not supply an additional prespecified testing convention, so the analytical choices above were made explicitly rather than attributed to the study lead.
