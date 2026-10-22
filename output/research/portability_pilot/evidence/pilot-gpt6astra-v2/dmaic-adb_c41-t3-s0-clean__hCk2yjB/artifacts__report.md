# Candidate-panel study: investigator report

## Decision
The discovery plate is usable after protocol QC. The scan identifies 1 significant variant, rs000008. Independent replication supports reporting this association: 1 candidate replicated. This is an association, not proof of causality or clinical utility.

## Quality and cohort comparability
Of 240 discovery participants, 3 failed call-rate QC (failure fraction 0.0125); 237 remain. The failure fraction is below the protocol plate-stop boundary, so re-genotyping the whole plate is not required. Excluded participants: P053, P129, P160. All other discovery participants are retained; the full retained manifest is in `retained.json`.

Variant QC retains 137 and excludes 13. Failures comprise 6 call-rate failures, 4 minor-allele-frequency failures and 3 control Hardy–Weinberg failures. HWE used the exact conditional two-sided test after participant filtering. Excluded variants: rs000003, rs000025, rs000061, rs000079, rs000086, rs000091, rs000107, rs000108, rs000122, rs000130, rs000138, rs000149, rs000150. All other assayed variants are retained and enumerated in the manifest.

Ancestry screening used mean-imputed, allele-variance-standardized genotypes and PCA before testing. Across 10 leading axes, no phenotype comparison survives correction across the axes. The leading-axis Welch p-value is 0.939779; score ranges overlap. Thus this panel provides no robust evidence that cases and controls represent separate ancestries, and an unadjusted additive trend scan is defensible. This small candidate panel cannot exclude subtle ancestry or relatedness; genome-wide ancestry markers would strengthen this assessment.

## Discovery and independent replication
The Bonferroni threshold over retained variants is 0.000364963504. The additive dosage trend test gives rs000008 p = 5.25354032e-11; its per-coded-allele logistic odds ratio is 3.78652, with confidence limits 2.47028 to 5.80408. Genomic inflation is 1.11594; this diagnostic alone is not evidence of confounding. Missing calls are omitted variant by variant in tests, rather than treated as reference alleles.

Replication retains 118 participants after 2 sample failures, and 140 variants after 10 variant failures. The nominated candidate passes replication QC. Its independent trend p-value is 4.03131836e-05, below the replication alpha of 0.05, with odds ratio 3.09723 in the same direction. No other discovery variant clears the corrected threshold; lack of significance is not proof of no effect.

## Actions and control plan
The analytical change was removal of low-quality participants and variants, not a laboratory intervention. It produced an eligible comparison set and a replicated signal. Report the replicated marker with allele coding, uncertainty, QC exclusions, ancestry limitations and independent confirmation clearly stated. Confirm physical allele/strand mapping before external dissemination; the provided matrices use numerical dosage coding. Do not claim a causal variant or deploy a clinical test on this evidence alone.

Archive the released batches, executable scripts, complete scan, retained manifest and trace together. Keep protocol gates fixed for future plates, require ancestry screening before association testing, and preserve independent same-direction replication as a reporting gate. Investigate failed calls through laboratory review rather than silently restoring excluded records. No study batch was denied; the initial replication request was merely premature and was later satisfied. No laboratory remediation or prospective clinical validation was performed.
