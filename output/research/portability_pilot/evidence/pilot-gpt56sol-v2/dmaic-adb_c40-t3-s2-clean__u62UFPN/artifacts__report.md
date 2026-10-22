# Compound-response panel study: decision report

## Executive decision

The libraries **can carry a conclusion**. All **12** libraries were usable, with **0** failures and **6** retained replicates in each arm; the facility minimum is **3** per arm. The intended treated-versus-control contrast is estimable: the treatment-plus-batch design had rank **3** across **3** columns and was not confounded.

The primary batch-adjusted count analysis identified **38** responding genes at adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**. Of these, **15** increased and **23** decreased. All **400** gene models converged.

Independent qPCR confirmed **10** of **10** nominated leading candidates in the panel-called direction. Concordance was **1.0**, exceeding the required **0.75**, so the facility's validation gate is passed and the candidate list may be issued. The validation result applies directly to the nominated leading subset; it is not independent confirmation of every panel call.

## Library and design assessment

Usability required at least **5000000** assigned reads and mapping rate at least **0.7**. Applying both rules produced **0** failed libraries. The usable allocation remained **6** control and **6** treated libraries.

Preparation batch was strongly imbalanced but not perfectly aliased with treatment. Batch L1 contained **5** control and **1** treated library; batch L2 contained **1** control and **5** treated libraries. Therefore, a simple arm-only comparison would mix compound and preparation effects. The analysis changed the model by adding preparation batch while estimating treatment, as required by the brief.

## Responding genes

Primary modeling used negative-binomial regressions on raw counts, median-ratio size-factor offsets, and treatment plus preparation-batch terms. Benjamini-Hochberg adjustment was applied across **400** genes before enforcing the joint statistical and effect-size rule.

**Up-regulated (**15**):** G0010, G0026, G0078, G0081, G0112, G0141, G0163, G0183, G0236, G0275, G0283, G0311, G0318, G0373, G0388

**Down-regulated (**23**):** G0012, G0017, G0049, G0075, G0086, G0108, G0133, G0146, G0213, G0228, G0247, G0253, G0291, G0295, G0302, G0340, G0342, G0345, G0351, G0355, G0358, G0372, G0397

An exploratory normalized log-expression OLS sensitivity analysis called **26** genes. It was not used for the release decision because the negative-binomial model directly represents integer count mean/variance behavior. The primary model converged for all **400** genes and included all qPCR nominees.

## Independent validation

The qPCR experiment had **4** biological replicates per arm. Each nominee was assessed by a Welch two-sample test on log2 relative expression and counted as confirmed only when p-value was below **0.05** and the mean change had the expected direction. The **10** confirmed nominees were: G0247, G0012, G0213, G0358, G0355, G0372, G0295, G0075, G0342, G0302.

Because **10** of **10** nominees confirmed, the list is supported for issue under the standing rule. This supports the direction and reproducibility of the leading candidates while preserving the distinction between validated nominees and panel-only calls.

## Gene-set context

Over-representation was tested for **12** annotated sets against the **400**-gene panel universe using one-sided Fisher tests and Benjamini-Hochberg adjustment. **0** sets met adjusted p-value below **0.05**. Therefore, no gene-set-level claim should accompany the gene-level release.

## What happens next and how it will be held

1. Issue the batch-adjusted **38**-gene panel response list, clearly flagging the **10** independently confirmed leading candidates.
2. Retain preparation batch in any re-analysis; the observed imbalance makes this a required control rather than an optional sensitivity term.
3. Archive the QC verdict, design-rank check, size-factor/count-model script, full gene table, qPCR test table, and enrichment table with the release package.
4. For future runs, hold the process at the same gates: both library thresholds, at least **3** usable replicates per arm, an identifiable treatment contrast, the joint **0.05**/**1.0** gene rule, and validation concordance of at least **0.75**.
5. If stronger biological interpretation is needed, expand independent validation beyond the **10** leading nominees; do not describe the remaining panel calls as independently validated.
