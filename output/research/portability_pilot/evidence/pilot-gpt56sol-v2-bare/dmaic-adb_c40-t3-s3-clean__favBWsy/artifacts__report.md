# Study disposition

The study cannot currently support a conclusion about compound-responsive genes. Library QC left **8 usable libraries from 12**: **6 controls** and **2 treated samples**. The minimum usable arm therefore contains **2 replicates**, below the facility requirement of **3**.

# What is causing the stop

A library was retained only when it met both facility cutoffs: at least **5,000,000 assigned reads** and a mapping rate of at least **0.7**. Applying those rules produced **4 failures**, all in the treated arm. Of these, **2** failed read depth and **2** failed mapping rate.

This imbalance is decisive: although the control arm retains **6** usable libraries, the treated arm retains only **2**. The libraries therefore cannot carry the planned comparison under the facility's minimum-replication rule.

# Design and biological results

The sample sheet was requested after QC, but the steward locked it because replicate sufficiency failed. Preparation-batch allocation was therefore unavailable, so whether treatment is confounded with preparation batch **could not be computed**. The intended comparison is not presently supportable on QC grounds, and its design identifiability also remains unresolved.

Because the sample sheet could not be released, the downstream count matrix remained locked. Differential expression was not run, so there is **no defensible responsive-gene list**. The qPCR batch and gene-set annotation were downstream of that analysis and also remained unavailable. Validation concordance could not be computed, so validation cannot support issuing a list.

# What changed and what it achieved

The only analytic change made was prospective QC filtering using the facility's standing cutoffs. It reduced the analyzable set from **12** libraries to **8**, but exposed that the treated arm falls below the replication requirement rather than creating an apparently complete but unsupported result. No data were imputed, no failed library was relabeled as usable, and no downstream result was invented.

# Recommended next action and control plan

Recover the treated arm before interpreting expression. The **2 low-depth failures** should be evaluated for additional sequencing if their libraries remain technically sound. The **2 low-mapping failures** require root-cause review and are stronger candidates for library remake or biological replacement. Any recovery plan must produce at least **3 usable treated replicates** while preserving a valid batch structure.

After replacement or recovery, rerun the same two-criterion library QC and do not unlock analysis unless every arm has at least **3 usable replicates**. Then inspect the sample sheet for treatment–batch confounding before fitting a differential-expression model. Only after an identifiable design and a valid gene list should qPCR concordance and gene-set interpretation be evaluated. Preserve the QC table, sample exclusions, batch assessment, model specification, and validation decision with the release so the conclusion remains auditable.
