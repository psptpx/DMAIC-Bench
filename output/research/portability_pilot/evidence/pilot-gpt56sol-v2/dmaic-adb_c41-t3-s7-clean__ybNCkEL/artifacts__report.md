# Candidate-region association study: final protocol disposition

## Executive conclusion

The plate can support analysis: participant QC excluded **3** participants, a failure fraction of **0.0125**, below the permitted **0.1**. After all protocol gates, however, **no association is reportable**. The discovery scan nominated **rs070008**, but the independent cohort did not replicate it at the required **0.05** level. The investigators should not present rs070008 as an established association and should reconsider the discovery result and study design before collecting or testing another confirmatory cohort.

## What was done

### Participant and plate QC

The discovery input contained **240** participants and **150** panel variants. At the minimum participant call rate of **0.95**, **3** participants failed: **P016, P077, P139**. They were removed. The retained cohort contains **237** participants: **118** affected and **119** unaffected. Thus the plate passes rather than requiring re-genotyping.

The protocol retains every supplied participant ID other than **P016, P077, P139**.

### Variant QC

Across the retained participants, **139** variants passed and **11** failed. Failures comprised **5** for call rate, **4** for minor-allele frequency, and **2** for exact Hardy–Weinberg equilibrium among unaffected participants.

Excluded variants: rs070013, rs070023, rs070025, rs070047, rs070049, rs070069, rs070099, rs070114, rs070131, rs070133, rs070148.

Retained variants: rs070001, rs070002, rs070003, rs070004, rs070005, rs070006, rs070007, rs070008, rs070009, rs070010, rs070011, rs070012, rs070014, rs070015, rs070016, rs070017, rs070018, rs070019, rs070020, rs070021, rs070022, rs070024, rs070026, rs070027, rs070028, rs070029, rs070030, rs070031, rs070032, rs070033, rs070034, rs070035, rs070036, rs070037, rs070038, rs070039, rs070040, rs070041, rs070042, rs070043, rs070044, rs070045, rs070046, rs070048, rs070050, rs070051, rs070052, rs070053, rs070054, rs070055, rs070056, rs070057, rs070058, rs070059, rs070060, rs070061, rs070062, rs070063, rs070064, rs070065, rs070066, rs070067, rs070068, rs070070, rs070071, rs070072, rs070073, rs070074, rs070075, rs070076, rs070077, rs070078, rs070079, rs070080, rs070081, rs070082, rs070083, rs070084, rs070085, rs070086, rs070087, rs070088, rs070089, rs070090, rs070091, rs070092, rs070093, rs070094, rs070095, rs070096, rs070097, rs070098, rs070100, rs070101, rs070102, rs070103, rs070104, rs070105, rs070106, rs070107, rs070108, rs070109, rs070110, rs070111, rs070112, rs070113, rs070115, rs070116, rs070117, rs070118, rs070119, rs070120, rs070121, rs070122, rs070123, rs070124, rs070125, rs070126, rs070127, rs070128, rs070129, rs070130, rs070132, rs070134, rs070135, rs070136, rs070137, rs070138, rs070139, rs070140, rs070141, rs070142, rs070143, rs070144, rs070145, rs070146, rs070147, rs070149, rs070150.

### Can affected and unaffected participants be compared?

Yes. PCA was computed from the retained genotype matrix after mean imputation and variant standardization. Across the leading **10** axes, there was no axis with non-overlapping affected and unaffected score ranges; `separated` was **false**. The leading-axis comparison had p = **0.23222329891717644**. A two-cluster diagnostic also contained both phenotypes in both clusters and gave p = **0.10449079744457386**, with complete separation **false**. The groups therefore are not drawn from demonstrably separate ancestries and may be compared.

One of the examined axes had a nominal case-control signal. For transparency, a conservative sensitivity scan including all **10** axes was also run; it yielded **0** corrected associations and genomic inflation factor **1.1181624192797353**. Because the prespecified comparability assessment did not establish material phenotype-linked ancestry structure, the additive trend scan without mandatory PC covariates was used as the primary discovery analysis.

### Discovery association

The primary scan tested **139** retained variants, and all **139** models converged. Its Bonferroni threshold was **0.00035971223021582735**, and genomic inflation factor was **0.916467278838885**. Exactly **1** variant crossed the threshold: **rs070008**, p = **1.1326253198110796e-05**, odds ratio per coded allele = **2.395108052343722**, based on **231** complete genotype observations. Its effect direction was positive.

### Independent replication and reporting gate

The replication analysis evaluated **1** candidate. For rs070008, **119** participants had a genotype call and **1** did not. The replication odds ratio was **1.1834997906119342** and its p-value was **0.5443027910807112**. The direction was the same as discovery (**true**), but the p-value did not meet **0.05**. Consequently **0** candidates replicated, and rs070008 fails the protocol's conjunctive replication rule.

## Business disposition and next actions

1. **Do not report a panel association.** The sole discovery nomination did not satisfy the independent replication gate.
2. **Preserve the QC exclusions and audit trail.** Any reanalysis should continue to exclude the listed failed participants and variants unless new genotype data are generated and QC is rerun.
3. **Reconsider the discovery scan rather than promoting the nominal finding.** Review population-covariate sensitivity, genotype calling for rs070008, phenotype definitions, and power; document any revised model before looking at further outcomes.
4. **If pursuing confirmation, use a new adequately powered independent cohort and the same-direction rule fixed in advance.** The current replication data do not support a positive report.
