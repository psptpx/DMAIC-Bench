# Sequencing study status report

## Executive conclusion

The study can carry a treatment-versus-control conclusion on its current library design, but the complete nominated list must be withheld. The library QC passed: **0** libraries failed, and each arm retained **6** usable replicates. These results are recorded in the `qc.sample_qc` step of `trace.json`.

The comparison is estimable because the usable libraries span **2** preparation batches with both arms represented. The model therefore included preparation batch. This design decision and the observed non-confounded status are recorded in `design.identifiability`.

## Expression result

The batch-adjusted analysis covered **400** genes and **12** libraries. Using adjusted p < **0.05** and absolute log2 fold change >= **1.0**, it nominated **31** genes:

G0010, G0012, G0017, G0026, G0075, G0078, G0086, G0108, G0112, G0117, G0133, G0136, G0141, G0146, G0163, G0183, G0213, G0228, G0236, G0247, G0291, G0295, G0302, G0318, G0342, G0345, G0351, G0355, G0358, G0372, G0373

The full effect estimates and adjusted p-values are in the outputs of `expression.de_blocked` in `trace.json`.

## Independent validation

The released qPCR data cover **10** of the **31** nominees. **10** of those **10** validated genes confirmed the panel direction at p < **0.05**, giving observed concordance **1.0**, above the required minimum concordance of **0.75**. However, **21** nominees have no qPCR record in the released batch. Therefore the complete **31**-gene list has not been validated and must not be issued as a validated candidate list.

The validated records support the direction of the tested down-regulated candidates, but they do not establish validation for the missing nominees. The conclusion stops at the validated subset until the missing qPCR results are available.

## Gene-set context

The panel annotation contains **12** gene sets over a universe of **400** genes. Enrichment analysis found **1** significant set after BH adjustment. SET03 contained **14** nominated genes and had adjusted p **9.55232041519293e-09**. This supports a structured signal in the panel result, but it does not remove the validation requirement.

## What caused the hold and what changed

The hold is caused by incomplete independent validation, not by failed library QC or an unidentifiable design. The analysis was changed from an unblocked comparison to a batch-adjusted comparison because preparation batch is present and imbalanced across arms, while remaining estimable. The change produced the **31**-gene threshold-qualified nomination; it does not authorize release without validation.

## Recommended next action and control

Obtain independent qPCR results for the **21** nominees without released validation records, apply the same p < **0.05** and direction-matching rule, recompute concordance, and issue a list only if the required concordance of **0.75** is met. Preserve the current usable-library rules, keep preparation batch in the expression model, and retain the trace as the audit record for the decision.
