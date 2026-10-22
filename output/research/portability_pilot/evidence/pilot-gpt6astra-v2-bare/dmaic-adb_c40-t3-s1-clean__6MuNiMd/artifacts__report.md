# Compound-response study: hold biological conclusions

## Executive decision
The sequencing libraries pass the facility's usability gate, but the experimental design cannot distinguish compound effects from preparation-batch effects. Do not issue a compound-responsive gene list from this study. This is a failure of identifiability, not evidence that the compound has no effect.

## What was computed
Using the complete per-library metrics and the supplied usability rules, **12 libraries were usable and 0 failed**. The minimum usable replication across arms was **6**, exceeding the required **3**. Library quality and replication therefore do not explain the inability to conclude.

The sample-sheet audit found **2 preparation batches**. The first contains **6 controls and 0 treated libraries**; the second contains **0 controls and 6 treated libraries**. An intercept-plus-treatment-plus-batch design matrix has **3 columns but rank 2**. Treatment and batch are completely confounded: there is no within-batch treatment contrast. Excluding otherwise usable libraries cannot create the missing overlap.

The QC and design results are recorded in `trace.json`; the executable computations are in `analyze.py` and `design.py`.

## What cannot be concluded
The steward locked the gene-level counts after the computed confounding verdict. It also locked the validation batch because expression analysis had not been completed. These were access locks, not declarations that the underlying records do not exist. No gene-level differential-expression test, batch-variance estimate, validation-concordance calculation, or enrichment analysis was run. No significant-gene count or confirmed-candidate count is available, and no gene can responsibly be named as compound-responsive on the evidence released.

Independent validation was described in the study background, but its results and experimental design were not released. Validation therefore cannot currently support issuing a list. Even agreement with an unadjusted panel contrast would not by itself separate treatment from preparation effects in this panel design. Gene-set analysis was not pursued because there is no defensible response list to interpret.

An inquiry about corrected sample assignments or crossed replacement libraries returned no matching study fact. No rescue dataset or correction was supplied. This is not proof that rescue material can never be obtained; it means no such remedy was available for this analysis.

## Recommended action and ownership
The facility should hold the biological release and ask the principal investigator and laboratory lead to verify the sample-to-arm and preparation records against source documentation. Correct metadata only if documentary evidence warrants it; do not relabel samples to make the model estimable.

If the records are accurate, repeat or extend preparation with treated and control biological replicates represented within every preparation batch, randomized and balanced across handling and sequencing. Additional sequencing of the same confounded libraries does not solve the design problem. Preserve independent biological replication and pre-specify an identifiable batch-adjusted analysis before collecting replacement data.

After an identifiable dataset is available, repeat the library gate and design-rank audit, normalize counts, assess batch effects, fit the pre-specified expression model, apply the facility's multiplicity and effect-size rules, and evaluate independent validation for significance and directional agreement using its standing concordance criterion. Only then consider issuing a response list and interpreting gene sets.

## What changed and how it will be held
No laboratory intervention or statistical correction was performed, and no improved biological outcome is claimed. The operational change recommended here is a release hold: usable libraries are not sufficient when the intended contrast is not estimable. The analysis documented that distinction and stopped before misleading gene calls.

Maintain a signed sample manifest, enforce arm-by-batch overlap and full model rank before library preparation, and retain QC, model, and validation audit records at release. The laboratory lead owns the balanced preparation plan; the analysis team owns the estimability check and reproducible calculations; the principal investigator approves any redesigned comparison. The current conclusion stops at usable libraries with a non-identifiable compound comparison.
