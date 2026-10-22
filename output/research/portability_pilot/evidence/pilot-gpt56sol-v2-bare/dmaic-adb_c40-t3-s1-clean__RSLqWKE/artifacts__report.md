# Study status report

## Executive conclusion

The sequencing libraries pass the facility's usability gate, but the experiment cannot support the comparison it set out to make. Treatment arm and preparation batch are completely confounded. Consequently, a treatment effect cannot be separated from a batch effect, the gene-level counts were not released through the design-identifiability gate, and no defensible compound-responsive gene list can be issued.

The qPCR batch was also unavailable because it is downstream of the blocked count analysis. Validation concordance and candidate confirmation therefore could not be computed. The validation does not currently support issuing a list—not because it failed, but because it could not be scored in this routed analysis.

## Library readiness

The QC assessment covered 12 libraries. A library was assessed against the facility requirements of at least 5,000,000 assigned reads and a mapping rate of at least 0.70.

No libraries failed: the failed-library count was 0. There were 6 usable control libraries and 6 usable treated libraries. The minimum usable replicate count across arms was therefore 6, exceeding the required minimum of 3. Library yield, mapping, and replicate count are not the reason the study stops.

## Design assessment

The sample sheet contains 2 preparation batches and 2 conditions. Every control library was prepared in one batch, while every treated library was prepared in the other. Thus batch membership exactly reproduces treatment membership.

The combined condition-and-batch model had 3 columns but rank 2. This rank deficiency means the treatment coefficient and batch coefficient cannot both be estimated. Any observed difference between arms would be equally compatible with compound exposure, preparation batch, or their combination.

## Differential expression and responding genes

No differential-expression analysis was run. After the confounding verdict was declared, the steward locked the gene-level count batch because the design was not identifiable. Therefore:

- the number of responding genes is unknown;
- no genes can be named as compound-responsive;
- applying the prespecified adjusted-significance and fold-change rules was impossible; and
- an unadjusted arm comparison would not repair the problem, because it would merely estimate the inseparable arm/batch contrast.

This is a design failure rather than evidence that the compound has no effect.

## Validation and annotation

The qPCR validation records were locked behind completion of the count analysis. Candidate-level confirmation and overall concordance were not computed, so no claim of validation success or failure is justified.

The panel gene-set annotation was subsequently locked behind validation. No enrichment analysis was run. These are unavailable steps, not negative results.

## Cause, corrective action, and hold plan

The root cause is allocation of the treatment arms to different preparation batches. Good sequencing metrics cannot compensate for that allocation.

The facility should not release a compound-response gene list from the present sequencing run. The next study should place both control and treated biological replicates within each preparation batch, randomize library preparation and sequencing order, and preserve the treatment-to-batch allocation in the sample sheet before laboratory work begins. If rerunning all material is infeasible, additional libraries must create genuine within-batch treatment contrasts; merely adding more control libraries to the control-only batch or more treated libraries to the treated-only batch will leave the aliasing intact.

Before analysis of the rerun, hold the study at a design review that checks both arms are represented within batches. Then repeat library QC, fit a model that includes batch and treatment, apply the prespecified gene-calling rules, and score qPCR concordance only against candidates from that identifiable model. Release the gene list only after those gates pass.
