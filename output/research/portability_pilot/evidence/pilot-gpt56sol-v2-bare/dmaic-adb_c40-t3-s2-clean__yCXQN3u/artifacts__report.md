# Compound-response study: decision report

## Executive decision

The sequencing libraries can carry a conclusion: **0 libraries failed QC**, leaving **6 control** and **6 treated** libraries usable. The smallest arm therefore has **6 usable replicates**.

The intended comparison is estimable after preparation-batch adjustment. The design contains **2 batches** and the treatment-plus-batch model has rank **3 with 3 columns**, so it is not exactly confounded. Allocation is nevertheless imbalanced (control: L1 **5**, L2 **1**; treated: L1 **1**, L2 **5**), making an unadjusted arm comparison inappropriate.

The blocked count analysis called **39 genes** from **400 tested: 16 up and 23 down**. Independent qPCR confirmed **10 of 10 nominated candidates**, for concordance **1.00**, exceeding the required **0.75**. This supports issuing the sequencing list, with the explicit limitation that qPCR directly tested only the nominated subset, not every called gene.

## What was done and what it showed

### Library readiness

Usability was computed per library from the released assigned-read and mapping-rate rules. **12 libraries were usable** and **0 failed**. No sample was removed downstream.

### Design and batch

A model matrix containing intercept, treatment, and preparation batch was tested for rank. It was full rank, so the compound effect can be separated from batch in this dataset. Batch remains consequential: its adjusted variance fraction on normalized log expression was **0.317633**. Accordingly, batch was retained in every gene model.

### Compound-responsive genes

Counts were median-ratio normalized and analyzed using gene-wise negative-binomial models with treatment and batch. Multiple-testing correction and the facility's supplied effect-size rule were both applied.

**Up:** G0318, G0236, G0010, G0141, G0078, G0112, G0163, G0026, G0373, G0311, G0283, G0183, G0275, G0081, G0388, G0354

**Down:** G0247, G0012, G0358, G0355, G0075, G0372, G0342, G0213, G0228, G0302, G0086, G0291, G0017, G0146, G0295, G0133, G0345, G0108, G0049, G0340, G0351, G0397, G0253

The fitted common dispersion was **0.046643**; normalization size factors ranged from **0.789754** to **1.242143**. These are audit details, not additional decision thresholds.

### Independent validation

For each qPCR-nominated candidate, treated and control measurements were compared by a two-sample Welch test and required to agree with the panel direction. **10 of 10** met both requirements. Validation therefore supports release of the response list, while its evidential scope remains the nominated subset.

### Gene-set context

Over-representation was tested across **12 annotated sets** against a universe of **400 panel genes**, using the **39 called genes** and BH adjustment. **1 sets** were significant. The significant sets were: SET03.

## Recommendation and control plan

Issue the batch-adjusted sequencing response list with the qPCR scope caveat above. Do not substitute a simple arm-only analysis: the measured batch contribution and imbalanced allocation show why blocking matters.

For the next experiment, balance each arm within each preparation batch and randomize library preparation order. Retain the same prospective library-QC gate, model-matrix rank check, batch-adjusted count model, multiplicity control, effect-size rule, and directional qPCR concordance gate. Archive per-library QC, the sample sheet, model design, complete gene table, and validation calculations so the released list remains reproducible. If confirmation of every issued gene is required for the intended use, extend qPCR to the untested calls before making gene-specific claims beyond the validated subset.
