# Compound-response panel study report

## Executive conclusion

The libraries and design are adequate to make the planned treated-versus-control comparison, but the panel provides no gene-level response call under the facility's prespecified criteria. All 12 libraries were usable, with 6 usable control libraries and 6 usable treated libraries. The experiment used 1 preparation batch, and that batch contained both arms, so treatment was not confounded with preparation batch.

The final count analysis tested 400 genes and called 0. A call required adjusted p below 0.05 and absolute log2 fold change of at least 1.0. The smallest adjusted p value was 0.47268554775922333, while the largest absolute estimated log2 fold change was 0.8835428113065121. Thus neither the multiplicity-controlled evidence nor the required effect magnitude supports a candidate list.

The facility should not issue a candidate list from this study.

## Library readiness

A library was required to have at least 5000000 assigned reads and mapping rate at least 0.70. Applying both rules produced 0 failed libraries and 12 usable libraries. Each arm retained 6 usable replicates, exceeding the required minimum of 3. Re-sequencing is therefore not indicated by the stated library QC rule.

## Design assessment

There was 1 preparation batch. It included both study arms, and the treatment design was full rank: rank 2 for 2 design columns. Treatment is therefore estimable separately from preparation batch. Because there was only 1 batch, no separate batch coefficient could or needed to be fitted.

## Gene-level analysis

The final analysis used a negative-binomial generalized linear model with median-ratio library normalization, within-arm residual moment dispersion stabilized toward the panel median, Wald tests, and Benjamini-Hochberg adjustment. It included 6 control and 6 treated libraries, tested all 400 genes, and had 0 model failures.

No gene met both the adjusted-p and fold-change rules: 0 genes were called, including 0 upward and 0 downward calls. A preliminary implementation also returned 0 calls, but its dispersion estimate pooled variation across arms. The analysis was corrected to estimate residual variation within arms so a treatment shift would not inflate dispersion. The correction changed the smallest adjusted p value from 0.8400319910514268 to 0.47268554775922333, but it did not change the business conclusion.

## Independent validation

The steward released a validation batch containing 0 nominated candidates and 0 qPCR results, with 0 confirmed candidates. Consequently, validation concordance is undefined: there is no denominator on which to calculate the required proportion. It would be incorrect to report either success or failure against the required concordance of 0.75, and no numeric concordance was declared.

This does not create a validation-supported list. Rather, there is no panel candidate list to validate or issue.

## Annotation limitation

The panel gene-set annotation remained locked because its release requires a numeric validation concordance. Since concordance cannot be computed from an empty candidate set, no annotation or enrichment analysis was available. This does not alter the gene-level conclusion, but pathway interpretation cannot be supplied.

## Recommended next actions and control

- Close the current analysis as an adequately sequenced, estimable study with no genes meeting the prespecified response criteria.
- Do not relax the adjusted-p, fold-change, or validation rules after seeing the result.
- Do not re-sequence solely for library QC: 0 libraries failed and both arms retained 6 usable replicates.
- If the scientific program requires another attempt to identify candidates, plan a new study based on the observed variability and desired detectable effect, then pre-register its sample size and analysis before collecting data.
- Retain the sample-level QC decision, design-rank check, normalization, dispersion procedure, multiple-testing correction, and validation gate as the controlled workflow for any follow-up study.
