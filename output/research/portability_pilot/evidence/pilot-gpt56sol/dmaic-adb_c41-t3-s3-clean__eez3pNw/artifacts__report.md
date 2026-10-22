# Candidate-region association study status

## Executive conclusion

The current plate **cannot carry an association conclusion**. Participant call-rate QC was run on the complete genotype batch containing **240 participants** and **150 panel variants**. Under the protocol's participant call-rate cutoff of **0.95**, **34** participants failed, for a failure fraction of **0.14166666666666666** (**14.166666666666666%**). This exceeds the allowed maximum failure fraction of **0.1** (**10.0%**). The computed plate-proceed verdict is therefore **false**.

The protocol requires the plate to be re-genotyped before anything else is analyzed when this gate fails. Accordingly, I did not perform variant QC, ancestry assessment, or association testing on this plate.

## Participant QC

The input contained **120 affected** and **120 unaffected** participants. Of the failures, **18** were affected and **16** were unaffected. At the participant-filter level, **206** participants met the call-rate rule: **102 affected** and **104 unaffected**.

Participants failing the rule were:

P002, P003, P009, P013, P016, P023, P030, P040, P044, P063, P066, P068, P088, P094, P095, P108, P112, P118, P129, P130, P139, P141, P150, P153, P157, P160, P169, P182, P192, P203, P211, P212, P220, P238

The participants retained at this QC step are **all participants in the supplied batch except those listed above**. This is a participant-level QC result only; it does not authorize downstream analysis because the plate-level gate failed.

Observed participant call rates ranged from **0.52** to **1.0**.

## Variant status

No variant was declared retained or failed. Although genotype calls were supplied, the protocol says that after this plate-level failure the plate is re-genotyped before anything else is analyzed. Consequently, variant call rate, minor-allele frequency, and unaffected-participant Hardy-Weinberg calculations were not run. The number and identities of retained variants therefore **could not be computed on an admissible cohort**.

Because the retained-variant count is unavailable, the Bonferroni association cutoff also could not be computed.

## Can affected and unaffected participants be compared?

Not on this plate. The required ancestry-structure check was not reached because the participant-QC plate gate failed. Thus it could not be established whether the affected and unaffected groups are ancestry-comparable or whether ancestry covariates would be needed.

## Association results

No variants were tested, and no variant can be reported as associated or non-associated. This is a protocol stop, not evidence of absence of association.

## Required next action and control plan

1. Re-genotype the whole plate rather than proceeding with the current calls.
2. Re-run participant call-rate QC first and apply the same plate-level gate.
3. Only after that gate passes, filter variants using the protocol's call-rate, minor-allele-frequency, and unaffected-participant Hardy-Weinberg rules.
4. On the resulting retained cohort, assess ancestry structure before testing any variant. Stop if groups are separated; if structure overlaps, include its leading axes as covariates.
5. Compute the Bonferroni cutoff from the newly retained variant count and then run the appropriate association tests.
6. Preserve the QC exclusions, ancestry decision, model specification, and multiplicity threshold with the final result so the conclusion remains auditable.

No outside-study facts were requested and no uncomputed downstream result has been substituted for the missing analyses.
