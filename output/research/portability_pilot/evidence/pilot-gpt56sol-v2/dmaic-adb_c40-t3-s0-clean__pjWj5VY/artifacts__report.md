# Compound-response study report

## Executive conclusion

The sequencing libraries can carry a conclusion. Across 12 libraries, 0 failed the facility QC rules, leaving 6 usable control and 6 usable treated libraries; the minimum retained arm therefore has 6 replicates. The intended comparison is estimable: the usable data contain 1 preparation batch, and adding treatment increases design rank from 1 to 2.

The panel analysis called 40 compound-responsive genes using adjusted p-value below 0.05 and absolute log2 fold change at least 1.0. Of these, 24 increased and 16 decreased. Independent qPCR confirmed 10 of 10 nominated leading candidates in the panel-called direction, for concordance 1.0; this exceeds the required 0.75. The validation gate therefore supports issuing the candidate list, with the important scope qualification that qPCR directly tested the nominated leaders rather than every panel call.

## What was measured and decided

### Library fitness

A library had to have at least 5000000 assigned reads and mapping rate at least 0.7; each arm had to retain at least 3 usable replicates. Applying those rules produced 0 failures among 12 libraries and retained 6 replicates in the smaller arm. Re-sequencing is not required on the stated QC rule.

### Design fitness

All 12 usable libraries are in 1 preparation batch, with both study arms represented. The intercept-only design rank was 1; adding treatment raised it to 2. Treatment is therefore not confounded with batch. Because batch does not vary, the fitted comparison used a simple treatment model rather than an unidentifiable batch coefficient.

### Panel response

The count analysis covered 400 genes and 12 samples, with 6 control and 6 treated samples. Gene-wise negative-binomial regression used median-ratio size-factor offsets, Wald tests, and BH adjustment. Models returned finite inferential results for 397 genes; 3 fits failed and were not called. Applying both release thresholds produced 40 calls.

**Increased (24):** G0006, G0007, G0010, G0037, G0039, G0061, G0101, G0107, G0110, G0118, G0131, G0153, G0185, G0194, G0212, G0260, G0277, G0279, G0287, G0293, G0310, G0331, G0374, G0383

**Decreased (16):** G0052, G0114, G0115, G0124, G0149, G0154, G0155, G0187, G0247, G0276, G0280, G0299, G0311, G0314, G0372, G0394

### Independent validation

The validation used 4 biological replicates per arm for each of 10 nominated leaders. Two-sided Welch tests, together with the required direction check, confirmed 10 candidates at p-value below 0.05. Concordance was 1.0, above the minimum 0.75; the validation release condition passed.

### Gene-set context

Over-representation testing compared the 40 calls with a universe of 400 panel genes across 12 annotated sets. At BH-adjusted alpha 0.05, 1 set was significant. SET03 contained 20 called genes among 30 members (raw p-value 8.83051125328435e-16; adjusted p-value 1.05966135039412e-14). This is supporting biological context, not a substitute for the gene-level and qPCR evidence.

## What changed, what it achieved, and how to hold it

No laboratory rescue or design change was needed. The operational changes were analytical: the standing QC filter was applied before modeling, estimability was checked before calling genes, count-depth normalization and multiplicity control were applied, and release was held behind the independent-validation gate. That sequence retained the full usable study, produced a treatment contrast that the design supports, and prevented release before directional qPCR confirmation.

The facility should now:

- issue the compound-response candidate list, clearly distinguishing the qPCR-tested leaders from the remaining panel-only calls;
- archive the library usability flags, design-rank check, normalized count-model results, adjusted p-values, and qPCR direction checks with the release;
- review the 3 failed gene fits before making any claim about those genes;
- prioritize orthogonal follow-up for panel calls not included in the nominated qPCR subset;
- retain the same QC, estimability, dual-threshold, and validation gates for any repeat study, and pre-balance treatment arms within every preparation batch if additional batches are introduced.
