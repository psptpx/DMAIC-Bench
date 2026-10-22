# Candidate-region study: investigator decision

## Executive conclusion
The discovery plate is usable after protocol QC. The cohort can be compared on the ancestry evidence available from this panel. **rs000008 is the sole discovery association and is independently replicated**, so it meets the protocol's reporting requirement. This supports an association with affection status, not a causal or clinical claim.

## Quality and retained analysis set
Of 240 discovery participants, 3 failed the participant call-rate requirement: P053, P129 and P160. The failure fraction was 0.0125, below the protocol's plate-retyping trigger. Retain every other discovery participant: 237 total, comprising 119 affected and 118 unaffected participants. No plate re-genotyping was indicated or performed.

After participant exclusion, 13 variants failed QC and 137 were retained. There were 6 call-rate failures, 4 minor-allele-frequency failures and 3 control Hardy–Weinberg failures. Retain every supplied variant **except**:

rs000003, rs000025, rs000061, rs000079, rs000086, rs000091, rs000107, rs000108, rs000122, rs000130, rs000138, rs000149, rs000150.

`sample_qc.csv` and `variant_qc.csv` give the full membership decisions and metrics. Variant metrics were recomputed in retained participants, with an exact conditional Hardy–Weinberg test restricted to unaffected participants. Missing genotypes were excluded from those calculations.

## Can cases and controls be compared?
PCA used retained variants, allele-frequency scaling and mean imputation for missing calls. The leading axis had phenotype-comparison p = 0.939779 and variance fraction 0.0227669. The next axis had p = 0.329510 and variance fraction 0.0207196. All inspected axes had overlapping case/control ranges. The spectrum was diffuse; no phenotype comparison survived multiplicity correction across inspected axes. Isolated nominal differences on later axes are not persuasive evidence of distinct ancestry groups.

Accordingly, the analysis proceeded with an unadjusted additive trend test rather than stopping for ancestry separation or imposing an ancestry-adjusted primary model. This is a panel-based assessment, not proof that all population confounding is absent: a candidate-region panel has limited ancestry resolution. PCA coordinates and phenotype labels are preserved in `pca.csv`.

## Discovery association
The retained-panel Bonferroni cutoff was 0.0003649635. There was 1 significant variant, rs000008, with additive trend p = 5.771927e-11. The scan's genomic inflation factor was 1.111212. The per-coded-allele logistic odds ratio was 3.786516, with Wald confidence limits 2.470282 to 5.804076. The coded allele was more common with affection; nucleotide-level effect-allele annotation was not provided, so no base identity is asserted.

Tests used complete calls separately for each variant and a Cochran–Armitage score with finite-sample null variance. Effect estimates came from additive logistic regression. All discovery test results are in `association.csv`. Non-significant variants are not established to be biologically null.

## Independent replication
Replication participant QC excluded 2 participants (failure fraction 0.0166667), retaining 118 participants, with 59 affected and 59 unaffected. The candidate passed QC: call rate 0.9915254, minor-allele frequency 0.4615385, and control Hardy–Weinberg p = 1.0. There were 117 called participants for its test.

rs000008 had replication trend p = 4.349318e-05 and per-coded-allele odds ratio 3.097233. The direction matched discovery and the nominal protocol criterion was met: **1 of 1 candidates replicated**. Reporting the association is therefore supported; the protocol's nonreplication stop rule is not triggered.

## What changed, what it achieved, and how to hold it
The implemented change was analytical exclusion of low-quality participants and variants, not a laboratory intervention. It produced a protocol-eligible discovery set and preserved a strong association that also appeared in independently collected data. The measured QC causes were missing calls, low allele frequency and control genotype disequilibrium; their laboratory root causes cannot be established from genotype arrays alone.

Report rs000008 as a replicated panel association, with the stated coding caveat. Before publication, reconcile allele/strand annotation and assay manifests across cohorts, inspect genotype clusters and batch allocation, and use broader ancestry markers for a sensitivity assessment. Replication ancestry structure and technical batch confounding were not separately modeled here. Investigate failed assays and participants before reuse; do not silently restore them to this analysis.

Archive the released JSON, scripts, QC membership tables, scan results and trace together. Freeze the quality, ancestry, multiplicity and replication gates before subsequent cohorts are analyzed. Reassess if allele harmonization, broader ancestry checks or independent validation contradict the present result. No additional steward batch was denied; the limitations above are unperformed checks, not fabricated measurements or evidence of their absence.

## Audit
All numerical findings above are recorded in `trace.json`; identifier strings label supplied records. The runnable analysis is preserved in `analyze.py`, `scan.py` and `replicate.py`. No external human intervention was needed.
