# Compound-expression study status

## Executive conclusion

The libraries can support an analysis: all 12 libraries passed the stated usability rules, and each arm retained 6 usable replicates. The intended treatment comparison is estimable separately from preparation batch. However, the batch-adjusted expression analysis found 0 genes meeting both calling criteria. There is therefore no compound-responsive gene list to issue.

The independent qPCR batch contained no nominated candidates. The validation proportion is not mathematically computable because there were 0 candidates in its denominator; the steward recorded 0 confirmed candidates and blocked the validation gate, whose required concordance is 0.75. The candidate list must therefore be withheld. Gene-set annotation was not released because its steward gate remained locked after validation did not pass.

## What was computed

### Library readiness

The QC analysis used the per-library metrics and applied the facility rules of at least 5,000,000 assigned reads and a mapping rate of at least 0.70. It found 0 failed libraries among 12 assessed. The usable counts were 6 control and 6 treated libraries, giving a minimum of 6 usable replicates per arm. This exceeds the facility minimum of 3.

### Design adequacy

The sample-sheet analysis found 2 preparation batches. Each batch contained both control and treated libraries: batch L1 had 5 control and 1 treated, while batch L2 had 1 control and 5 treated. The design is therefore not confounded. Because more than 1 batch was present, preparation batch was included as a model term.

### Expression result

The blocked analysis used the 400-gene count panel and all 12 usable libraries, fitting treatment with preparation batch adjustment. A gene required adjusted p < 0.05 and absolute log2 fold change at least 1.0. The resulting number of called genes was 0.

### Validation and annotation

The validation data explicitly reported 0 nominated genes, so there was no candidate-level qPCR result to compare. The number confirmed was 0, but a confirmation fraction cannot be computed for 0 candidates. The facility's required validation concordance is 0.75; the steward gate was recorded as 0 and did not release the gene-set annotation. There is no gene-set annotation data for this run, so no enrichment result can be computed.

## Business decision and next action

The sequencing libraries and experimental design are adequate to carry a conclusion that this analysis produced no genes meeting the prespecified response definition. The immediate business outcome is not a validated candidate list: no list exists to validate, and the validation gate consequently remains unsatisfied.

The facility should withhold a candidate list and avoid claiming either positive or validated gene-level response. Before changing thresholds or interpreting pathway biology, the study lead should review the absence of called genes and decide whether to repeat or extend the experiment under a prespecified plan. Any follow-up should preserve treatment balance across preparation batches, retain the stated QC rules, and define in advance how candidates will be nominated and validated.

## Provenance

All quantitative results in this report are recorded in `/workspace/trace.json`. The gene-set request was not a data denial: it was locked because the declared validation concordance did not meet the required gate. No result has been supplied for that unavailable step.
