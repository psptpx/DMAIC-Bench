# Study status: technically usable plate, invalid case–control comparison

## Principal investigator decision
Do not report an association from this discovery cohort. The plate passes the protocol's participant quality gate, but retained affected and unaffected participants are completely separated on a leading genetic-structure axis. The ancestry-comparability precondition fails. This is not evidence that the panel lacks disease associations; it means that this design cannot distinguish ancestry-linked variation from affection status.

## Quality and retained analysis set
Participant call rate was computed over all supplied variant calls, treating missing calls as uncalled. Of **240** participants, **1** fails the call-rate requirement of **0.95**, a failure fraction of **0.0041666667**, below the plate-stop limit of **0.1**. Retained: **239** participants, comprising **120** affected and **119** unaffected. Re-genotyping the entire plate is therefore not mandated by this gate.

Excluded participant: P129. All other supplied participants are retained for QC purposes. `sample_qc.csv` gives every participant's call rate and inclusion decision; `retained_participants.csv` is the exact retained manifest.

Variant QC was recomputed on the retained participants, using pooled called-allele minor-allele frequency and an exact conditional, probability-ordering Hardy–Weinberg test in unaffected participants only. Requirements were call rate at least **0.95**, minor-allele frequency at least **0.01**, and control Hardy–Weinberg p at least **0.000001**. **13** variants fail and **137** remain. Failures by rule: **5** for call rate, **4** for minor-allele frequency, and **4** for Hardy–Weinberg equilibrium.

Excluded variants: rs060002, rs060010, rs060024, rs060037, rs060043, rs060055, rs060083, rs060093, rs060104, rs060111, rs060114, rs060139, rs060144. All other supplied variants are retained for QC purposes. `variant_qc.csv` contains the full criterion-level audit; `retained_variants.csv` is the exact retained variant manifest. Retention does not mean permission to test association after the ancestry gate fails.

## Cohort comparability: decisive failure
PCA used retained participants and retained variants, with missing dosages replaced by the variant mean and columns standardized by allele-frequency variance. Case/control Welch comparisons and range overlap were inspected on the leading axes; p-values are descriptive diagnostics, not variant association tests.

The first principal component alone looks reassuring: case/control p = **0.46719033**, and explained variance fraction **0.12675989**. That does not establish comparability. The second principal component explains variance fraction **0.08615889** and shows case/control p = **1.0773321e-140**. Its affected score range is **1.6303094** to **5.2697063**, whereas the unaffected range is **-5.5995599** to **-0.34574859**. The ranges do not overlap. Component signs are arbitrary; the separation is not.

This genetic-structure separation is the operational ancestry failure specified by the protocol; specific ancestry labels are not available and are not inferred here. Adding principal components to a logistic model would not create within-ancestry case/control overlap and would require unsupported extrapolation. The saved scores are in `pca.csv`.

## Association and independent confirmation
No variant association test was run, and no association p-values, genomic inflation factor, or odds ratios were estimated. There is no valid discovery candidate set to nominate. Replication analysis was therefore not pursued and support for reporting any variant is **not established**, rather than negative. An initial broad data request was routed to replication and temporarily locked pending discovery analysis; this was not a steward denial or evidence that replication data do not exist. No requested batch was declared nonexistent.

## What changed, what it achieved, and next actions
The only changes made were analytical quality exclusions. These produced an auditable technically retained cohort and panel but did not cure the ancestry imbalance. No laboratory remediation, recruitment change, association rescue, or replication success has been demonstrated.

The study lead should review recruitment sources, ancestry information, and genotype processing for phenotype-linked structure. Recruit or identify affected and unaffected participants within shared ancestry strata, balance processing across affection status, and establish overlap before restarting discovery analysis. Additional ancestry-informative markers or reference-supported ancestry assessment would strengthen diagnosis because this is a candidate-region panel, not a genome-wide ancestry survey. Do not simply remove the axis that reveals the problem.

Hold the analysis at the comparability gate. Preserve the protocol, original batches, scripts, inclusion manifests, and PCA diagnostics. A redesigned cohort must pass participant and variant QC and a documented ancestry-overlap review before any association scan. Only then apply the protocol's retained-panel multiplicity correction and require independent, same-direction replication before reporting. The trace records only computations actually performed; no downstream inferential result has been substituted for the missing valid comparison.
