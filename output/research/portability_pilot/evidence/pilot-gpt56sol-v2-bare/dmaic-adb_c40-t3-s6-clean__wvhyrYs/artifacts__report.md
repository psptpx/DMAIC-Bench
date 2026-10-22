# Compound-response study: disposition report

## Executive conclusion

The sequencing libraries pass the facility's replicate-sufficiency requirement, but the study cannot support the comparison it was designed to make. QC retained **8** libraries: **4** control and **4** treated, while the required minimum is **3** usable replicates per arm. However, all **4** retained controls are in preparation batch L1 and all **4** retained treated libraries are in preparation batch L2. The compound arm is therefore inseparable from preparation batch.

No gene-response list should be issued. Gene-level counts were not released past the design-identifiability gate, so differential expression could not be computed. The qPCR validation and gene-set annotation are downstream of that blocked analysis and were likewise unavailable. There is therefore no computed validation concordance, no confirmed-candidate count, and no enrichment result.

## Library quality and sufficiency

The facility rule required at least **5000000** assigned reads and a mapping rate of at least **0.7** for a usable library. Applying both rules to **12** libraries caused **4** failures and retained **8**. The retained counts were **4** in each arm, giving a minimum arm count of **4** against the required **3**. Thus library quantity alone was sufficient to continue to design assessment.

The QC exclusions were asymmetric in cause: the excluded control libraries failed the assigned-read criterion, while the excluded treated libraries failed the mapping-rate criterion. The conclusion above uses only libraries meeting both rules.

## Why the intended comparison fails

The retained analysis set spans **2** preparation batches, but it has no within-batch arm overlap: the control-by-batch counts are **4** and **0**, while the treated-by-batch counts are **0** and **4**. A model containing an intercept, compound arm, and preparation batch has **3** columns but rank **2**. This rank deficiency establishes perfect confounding: the observed arm contrast could be caused by compound, preparation batch, or both, with no information in this design to separate them.

A simple treated-versus-control analysis would estimate the combined arm-and-batch contrast and would not answer the biological question. Calling it a compound effect would be misleading.

## Gene calls and validation

The steward locked the count batch after the confounding verdict. Accordingly, no adjusted significance values, fold changes, or responder count were computed, and there is no defensible candidate list to nominate.

The validation conclusion stops at the same point. Without an eligible panel-derived candidate list, the qPCR batch was not available for concordance scoring. Validation therefore cannot rescue or support release of a gene list.

## Required corrective action

Repeat library preparation and sequencing under a design that represents both control and treated samples within each preparation batch. Randomize samples across batches and preserve arm balance through processing. If the existing biological material permits, reprepare enough material to create within-batch arm overlap; otherwise repeat the experiment with a prospectively blocked allocation.

Before analysis of the replacement data, reapply the same library QC rules and verify both replicate sufficiency and full-rank condition-plus-batch identifiability. Only then run batch-adjusted differential expression, apply the prespecified gene-calling rules, nominate candidates, and score qPCR concordance. Hold release of any biological responder list until all of those gates pass. This prevents a technical batch contrast from being reported as a compound response.
