# Study disposition

## Executive conclusion

The sequencing libraries pass the facility's technical usability rules, but this study cannot support the biological comparison it set out to make. All **12** libraries were usable and each arm retained **6** usable replicates. However, the **2** preparation batches separate the arms completely: all **6** controls occur in one batch and all **6** treated libraries occur in the other. Treatment and preparation batch are therefore perfectly confounded.

No compound-response genes can be called from this design. The gene-count batch was locked at the design-identifiability gate, so differential expression was not computed. Consequently, no candidate list exists to validate, qPCR concordance could not be computed, and no list should be issued.

## What was assessed

### Prespecified rules

The released brief describes a **400**-gene panel and **6** planned biological replicates per arm. A library must have at least **5000000** assigned reads and mapping rate at least **0.70**. Each arm must retain at least **3** usable replicates. Gene calling would require adjusted p below **0.05** together with absolute log-fold change at least **1.0**. Independent qPCR would then need p below **0.05** in the panel-called direction for at least **0.75** of nominees.

### Library quality

Applying both library rules produced **0** failed samples and **12** usable samples. The control arm retained **6** and the treated arm retained **6**, so the observed minimum per-arm replication was **6**. Technical library quality and replicate count are not the cause of the stop.

### Design identifiability

The usable sample sheet contains **2** conditions and **2** batches. The condition-by-batch table has **6** controls and **0** treated libraries in the first batch, versus **0** controls and **6** treated libraries in the second. An intercept-plus-batch model had rank **2**. Adding treatment left the rank at **2**, although the full design had **3** columns. Thus the treatment column contributes no independent information: any observed arm difference is equally a batch difference.

## Downstream status

The steward refused release of gene-level counts because the design failed the identifiability gate. Therefore the number of significant genes and their identities could not be computed. The qPCR batch remained unavailable behind that blocked analysis, so neither directional confirmations nor validation concordance could be computed. The annotation batch was also unavailable downstream, so enrichment could not be computed. These are missing results, not negative findings.

## What changed and what it achieved

No data transformation or model adjustment was made because none can separate two perfectly aliased factors. The analysis was stopped at the prespecified design gate rather than producing a misleading compound effect. This protects the facility from issuing a candidate list that may reflect preparation batch.

## Required next action and control plan

Repeat library preparation or generate a new experiment in which both control and treated samples occur within every preparation batch. Randomize arm assignment across batches and retain the arm-by-batch allocation with the sample sheet before sequencing. After QC, verify full-rank treatment-plus-batch identifiability before releasing counts for gene calling. If the redesigned study passes that gate, fit a batch-adjusted model, apply the prespecified dual calling thresholds, then calculate directional qPCR confirmation and issue candidates only if the prespecified concordance rule passes. Preserve these checks as mandatory release gates for future studies.
