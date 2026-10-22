# Candidate-region association study: decision report

## Executive conclusion

The discovery plate can support analysis: **3** of **240** participants failed participant QC, a failure fraction of **0.0125**, which is below the protocol's **0.1** re-genotyping trigger. After removing those participants, **237** remained. Variant QC retained **139** of **150** panel variants and excluded **11**.

Affected and unaffected participants are comparable in this retained cohort. The leading-axis ancestry assessment did not separate them: PC1 had **p = 0.5935784745490553**, and the joint leading-axes test had **p = 0.5434782088515374**. The discovery scan therefore proceeded without post-hoc ancestry covariates.

No association met the computed Bonferroni threshold of **0.00035971223021582735**. The scan produced **0** significant variants among **139** tested; its smallest p-value was **0.013391980515363656**, and genomic inflation was **1.1113772313100228**. Consequently, the independent cohort had **0** nominated candidates and **0** replicated findings. **No panel association should be reported.**

## What was retained and removed

### Participants

The participant call-rate rule was applied across **150** calls per participant. The removed participants were **P085**, **P136**, and **P193**. Every other discovery participant was retained, yielding **237** retained participants.

### Variants

The protocol filters produced **5** call-rate failures, **4** minor-allele-frequency failures, and **2** control Hardy–Weinberg failures. These were:

- Call rate: **rs040024, rs040041, rs040044, rs040059, rs040134**
- Minor-allele frequency: **rs040066, rs040114, rs040124, rs040130**
- Control Hardy–Weinberg equilibrium: **rs040065, rs040128**

All other panel variants were retained, for **139** tested variants.

## Cohort comparability

PCA was run on the retained, mean-imputed, allele-frequency-standardized genotype matrix. In addition to the nonsignificant leading-axis tests, nearest-neighbor agreement on the first two axes was **0.4810126582278481**; **0.957983193277311** of affected participants lay inside the unaffected convex hull and **0.9322033898305084** of unaffected participants lay inside the affected convex hull. These diagnostics support overlap rather than separate ancestry groups.

The first PCA implementation failed because its requested software library was unavailable. It produced no quantitative result and was replaced by a successful NumPy/SciPy implementation; both attempts are recorded in the trace.

## Discovery and replication

An additive dosage trend scan was run on each retained variant using available genotypes. The smallest-p variant was **rs040143**, with **p = 0.013391980515363656** and a per-allele odds ratio of **1.8177001406935613**. It did not cross the Bonferroni threshold and is not a discovery association.

Because discovery produced **0** qualifying hits, the replication batch correctly contained an empty candidate list. A same-direction replication test was therefore not applicable. The protocol requires successful independent replication before reporting an association, so the conclusion stops with no reportable association.

## Explicit retained sets

### Retained participants

P001, P002, P003, P004, P005, P006, P007, P008, P009, P010, P011, P012, P013, P014, P015, P016, P017, P018, P019, P020, P021, P022, P023, P024, P025, P026, P027, P028, P029, P030, P031, P032, P033, P034, P035, P036, P037, P038, P039, P040, P041, P042, P043, P044, P045, P046, P047, P048, P049, P050, P051, P052, P053, P054, P055, P056, P057, P058, P059, P060, P061, P062, P063, P064, P065, P066, P067, P068, P069, P070, P071, P072, P073, P074, P075, P076, P077, P078, P079, P080, P081, P082, P083, P084, P086, P087, P088, P089, P090, P091, P092, P093, P094, P095, P096, P097, P098, P099, P100, P101, P102, P103, P104, P105, P106, P107, P108, P109, P110, P111, P112, P113, P114, P115, P116, P117, P118, P119, P120, P121, P122, P123, P124, P125, P126, P127, P128, P129, P130, P131, P132, P133, P134, P135, P137, P138, P139, P140, P141, P142, P143, P144, P145, P146, P147, P148, P149, P150, P151, P152, P153, P154, P155, P156, P157, P158, P159, P160, P161, P162, P163, P164, P165, P166, P167, P168, P169, P170, P171, P172, P173, P174, P175, P176, P177, P178, P179, P180, P181, P182, P183, P184, P185, P186, P187, P188, P189, P190, P191, P192, P194, P195, P196, P197, P198, P199, P200, P201, P202, P203, P204, P205, P206, P207, P208, P209, P210, P211, P212, P213, P214, P215, P216, P217, P218, P219, P220, P221, P222, P223, P224, P225, P226, P227, P228, P229, P230, P231, P232, P233, P234, P235, P236, P237, P238, P239, P240

### Retained variants

rs040001, rs040002, rs040003, rs040004, rs040005, rs040006, rs040007, rs040008, rs040009, rs040010, rs040011, rs040012, rs040013, rs040014, rs040015, rs040016, rs040017, rs040018, rs040019, rs040020, rs040021, rs040022, rs040023, rs040025, rs040026, rs040027, rs040028, rs040029, rs040030, rs040031, rs040032, rs040033, rs040034, rs040035, rs040036, rs040037, rs040038, rs040039, rs040040, rs040042, rs040043, rs040045, rs040046, rs040047, rs040048, rs040049, rs040050, rs040051, rs040052, rs040053, rs040054, rs040055, rs040056, rs040057, rs040058, rs040060, rs040061, rs040062, rs040063, rs040064, rs040067, rs040068, rs040069, rs040070, rs040071, rs040072, rs040073, rs040074, rs040075, rs040076, rs040077, rs040078, rs040079, rs040080, rs040081, rs040082, rs040083, rs040084, rs040085, rs040086, rs040087, rs040088, rs040089, rs040090, rs040091, rs040092, rs040093, rs040094, rs040095, rs040096, rs040097, rs040098, rs040099, rs040100, rs040101, rs040102, rs040103, rs040104, rs040105, rs040106, rs040107, rs040108, rs040109, rs040110, rs040111, rs040112, rs040113, rs040115, rs040116, rs040117, rs040118, rs040119, rs040120, rs040121, rs040122, rs040123, rs040125, rs040126, rs040127, rs040129, rs040131, rs040132, rs040133, rs040135, rs040136, rs040137, rs040138, rs040139, rs040140, rs040141, rs040142, rs040143, rs040144, rs040145, rs040146, rs040147, rs040148, rs040149, rs040150

## Actions and control plan

- Do not re-genotype this plate solely under the participant-failure rule; it passed that gate.
- Preserve the participant and variant exclusion lists above and the analysis trace as the audit record.
- Do not promote the smallest-p variant or any other panel variant as a hit.
- If investigators want another discovery attempt, pre-specify the rationale, sample expansion, ancestry model, and multiplicity plan before looking at new outcomes; then require independent same-direction replication before reporting.
- For future data releases, rerun participant QC, variant QC, ancestry assessment, multiplicity correction, and replication in that order. Any plate crossing its failure gate must stop before association testing.
