# Compound-expression study status

## Executive conclusion

The libraries can carry a conclusion, and the planned treated-versus-control comparison is estimable. The study retained **6 usable replicates per arm** and had **0 failed libraries** under the stated read and mapping rules. The sample sheet showed **1 preparation batch**, with both arms represented, so the treatment contrast was not confounded with batch.

The computed panel analysis nominated **38 genes** at adjusted p < 0.05 and absolute log2 fold change >= 1. The independent qPCR check tested **10 nominated genes**; **10** were confirmed in the expected direction, giving concordance **1.0**. This exceeds the required validation fraction of **0.75**, so the candidate list can be issued for the validated subset. The ten validated genes are: G0115, G0124, G0154, G0187, G0247, G0276, G0277, G0299, G0311, and G0314.

## What was found and what changed

The initial QC assessment found **0 failed libraries**, **12 usable libraries**, and a minimum arm size of **6**. That achieved the facility requirement of at least **3** usable replicates per arm. Design assessment found no confounding and **1** batch, allowing the comparison to proceed. Differential expression was computed from the complete **400-gene** count matrix for **6** control and **6** treated samples using Welch two-sample tests on log2(count + 1) values with Benjamini-Hochberg adjustment.

The 38-gene panel result was checked against independent qPCR data. All **10** available nominated genes were significant in the expected direction at qPCR p < 0.05, using **4** biological replicates per arm. Because validation concordance was **1.0**, the validation gate was passed rather than withholding the list. The qPCR result supports issuing the ten confirmed candidates; it does not independently validate the remaining nominated genes, so those should be labeled as sequencing-only candidates pending confirmation.

The panel annotation contained **12** gene sets in a **400-gene** universe. Over-representation testing of the 38 candidates found **1** set significant after BH adjustment at 0.05: SET03, with **19** candidate-gene overlaps, raw p **7.68365756990594e-15**, and adjusted p **9.220389083887129e-14**. This supports a SET03-level enrichment signal, but no biological interpretation can be made because the supplied annotation provides set identifiers and genes, not set names or biological descriptions.

## Recommended next actions and control

Issue the ten qPCR-confirmed genes as the supported candidate list, while retaining the other sequencing nominations as unvalidated follow-up targets. Repeat qPCR for the remaining nominations if they are decision-critical. Preserve the sample sheet, count matrix, analysis code, thresholds, and validation results together so that the same usability, design, calling, and confirmation rules are applied to any follow-up sequencing or validation.

The main qualification is design-related: all usable libraries were in **1** preparation batch. The treatment comparison was estimable because both arms occurred in that batch, but this study cannot quantify between-batch variation from this design. A follow-up should distribute both arms across multiple preparation batches and retain batch as a model term.
