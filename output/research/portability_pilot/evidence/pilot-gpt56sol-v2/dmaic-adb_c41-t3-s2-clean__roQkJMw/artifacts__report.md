# Candidate-region association study: final status

## Executive conclusion

The discovery plate can carry a conclusion. Participant QC excluded P017 and P111; the failed-sample fraction was 0.008333333333333333, and the plate therefore passed the protocol gate. After participant and variant QC, 238 participants and 139 variants remained. The retained affected and unaffected groups overlap in genotype-derived ancestry space, so they are comparable only with ancestry adjustment. A PC1-adjusted discovery scan identified rs020008, and the independent cohort replicated its positive direction at the protocol criterion. The association is therefore reportable.

## Quality and retained analysis set

- Participant QC failed 2 participants: P017 and P111. The minimum observed participant call rate was 0.9466666666666667. The retained set contains 118 affected and 120 unaffected participants.
- Variant QC failed 11 variants: rs020001, rs020016, rs020037, rs020045, rs020054, rs020072, rs020084, rs020085, rs020114, rs020117, rs020142. Of these, 5 failed call rate, 4 failed minor-allele frequency, and 2 failed control-only Hardy–Weinberg equilibrium.
- Retained variants (139): rs020002, rs020003, rs020004, rs020005, rs020006, rs020007, rs020008, rs020009, rs020010, rs020011, rs020012, rs020013, rs020014, rs020015, rs020017, rs020018, rs020019, rs020020, rs020021, rs020022, rs020023, rs020024, rs020025, rs020026, rs020027, rs020028, rs020029, rs020030, rs020031, rs020032, rs020033, rs020034, rs020035, rs020036, rs020038, rs020039, rs020040, rs020041, rs020042, rs020043, rs020044, rs020046, rs020047, rs020048, rs020049, rs020050, rs020051, rs020052, rs020053, rs020055, rs020056, rs020057, rs020058, rs020059, rs020060, rs020061, rs020062, rs020063, rs020064, rs020065, rs020066, rs020067, rs020068, rs020069, rs020070, rs020071, rs020073, rs020074, rs020075, rs020076, rs020077, rs020078, rs020079, rs020080, rs020081, rs020082, rs020083, rs020086, rs020087, rs020088, rs020089, rs020090, rs020091, rs020092, rs020093, rs020094, rs020095, rs020096, rs020097, rs020098, rs020099, rs020100, rs020101, rs020102, rs020103, rs020104, rs020105, rs020106, rs020107, rs020108, rs020109, rs020110, rs020111, rs020112, rs020113, rs020115, rs020116, rs020118, rs020119, rs020120, rs020121, rs020122, rs020123, rs020124, rs020125, rs020126, rs020127, rs020128, rs020129, rs020130, rs020131, rs020132, rs020133, rs020134, rs020135, rs020136, rs020137, rs020138, rs020139, rs020140, rs020141, rs020143, rs020144, rs020145, rs020146, rs020147, rs020148, rs020149, rs020150.

## Cohort comparability

PCA was computed on the QC-retained matrix. No examined leading axis completely separated affection groups (`separated = false`). PC1 explained 0.10170125571851286 of genotype variance and was associated with affection status (logistic p = 4.764802508093119e-14); its case and control score ranges overlapped. Thus an unadjusted comparison would be inappropriate, but comparison is permissible with PC1 in the model. The initial software-dependent PCA attempt failed because its package was absent; the completed result used NumPy SVD and is the basis for this decision.

## Discovery association

The additive logistic scan included PC1 and tested 139 QC-retained variants. Its Bonferroni threshold was 0.00035971223021582735, and genomic inflation was 0.993960641619535. Exactly 1 variant passed: rs020008 (nonmissing n = 235, p = 4.37460742272943e-05, odds ratio = 2.626313844354682, positive beta = 0.9655812829642845).

## Independent replication and reporting decision

The replication batch contained the nominated candidate rs020008. Its additive logistic result used 119 nonmissing participants and gave p = 0.0006966849454034408, odds ratio = 2.729997712702792, and beta = 1.0043007713587122. The direction matched discovery (`same_direction = true`), and 1 of 1 candidates replicated at alpha 0.05. The protocol therefore permits rs020008 to be reported; no other discovery variant is reportable.

## Actions and control plan

1. Preserve the participant exclusions, variant exclusions, PCA/SVD loadings, PC1-adjusted model specification, and nominated-hit record as the locked analysis set.
2. Report rs020008 as the replicated panel association, with discovery and replication estimates shown separately rather than pooled post hoc.
3. Do not promote rs020065 or any other non-Bonferroni discovery signal.
4. Before publication, run routine implementation review and biological annotation; retain the independent replication result and same-direction rule in the audit package.
5. For future plates, reapply the same call-rate, frequency, control-equilibrium, ancestry, multiplicity, and independent-replication gates before reporting.
