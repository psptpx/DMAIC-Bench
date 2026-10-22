# Compound-expression study: decision report

## Executive decision

The sequencing libraries can carry a conclusion, and the intended treated-versus-control comparison is estimable. The panel analysis called **38 genes** under the prespecified joint criteria of adjusted p-value below **0.05** and absolute log2 fold change of at least **1.0**. Independent qPCR confirmed **10 of 10** nominated leading candidates in the panel-called direction, for concordance **1.0**, exceeding the required **0.75**. The facility may therefore issue the candidate list, while clearly stating that qPCR directly tested the nominated leading subset rather than every panel call.

## Library quality and design

All **12** libraries passed the assigned-read and mapping-rate rules: **0** failed. Control retained **6** usable libraries and treated retained **6**, so the minimum retained replication was **6**, above the required **3**.

The usable design contains **1** preparation batch and **2** conditions. Its treatment design had rank **2** across **2** columns, so treatment is estimable and is not confounded with preparation batch. Because only **1** batch remains, a separate batch coefficient is neither needed nor estimable; the comparison is the simple treated-versus-control contrast.

## Panel response

After library normalization, negative-binomial gene models completed successfully for all **400** panel genes. The analysis called **38** genes:

G0006, G0007, G0010, G0037, G0039, G0052, G0061, G0101, G0107, G0110, G0114, G0115, G0118, G0124, G0131, G0153, G0154, G0155, G0187, G0194, G0212, G0247, G0260, G0276, G0277, G0279, G0280, G0287, G0293, G0299, G0310, G0311, G0314, G0331, G0372, G0374, G0383, and G0394.

An initial normalization attempt completed **0** gene models because individual zero counts made unrestricted geometric means invalid. That failed result was discarded. The corrected run estimated median-ratio size factors from genes positive in every library; its size factors ranged from **0.7358996855730512** to **1.2415643256753288**. This correction changed the computation from **0** successful models to **400** successful models. The call set comes only from the corrected run.

## Independent validation

The qPCR batch assayed **10** nominated leading candidates with **4** biological observations per arm. Welch two-sample tests at p-value below **0.05**, coupled to agreement with the panel-called direction, confirmed all **10**. Concordance was therefore **1.0**, and the validation gate passed. The directly validated nominees were G0115, G0124, G0154, G0187, G0247, G0276, G0277, G0299, G0311, and G0314.

This supports issuing the nominated candidate list. It does not amount to independent qPCR confirmation of the other panel calls; those remain panel-supported findings.

## Gene-set result

Over-representation was tested across **12** annotated sets in the **400**-gene panel universe using one-sided Fisher tests and BH correction at **0.05**. **1** set was significant: SET03. SET03 contained **20** of the **38** calls among its **30** members, with odds ratio **39.111111111111114**, raw p-value **2.2685638725907814e-16**, and adjusted p-value **2.722276647108938e-15**.

## Recommended next actions and control

1. Release the candidate list with the distinction between independently validated nominees and panel-only calls explicit.
2. Preserve the usable-library mask, normalization rule, model specification, joint call criteria, and qPCR directional rule with the analysis record so reruns use the same gates.
3. For claims centered on panel-only calls, run targeted independent validation before elevating them to validated biomarkers.
4. In the next study, distribute both arms within every preparation batch. The current comparison is valid because both arms share the sole batch, but balanced multi-batch preparation will protect the contrast against future batch effects.
5. Retain the failed normalization step in the audit trail. The corrected positive-reference rule should be part of the maintained workflow to prevent recurrence when individual counts are zero.
