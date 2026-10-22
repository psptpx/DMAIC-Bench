# Candidate-region case-control study: current status

## Executive conclusion

The discovery plate can support further work after QC, but this cohort **cannot currently support an unadjusted affected-versus-unaffected association conclusion**. Population-structure assessment found separation on PC1 (`p = 4.4356006605713844e-16`), while the unadjusted trend scan had genomic inflation `lambdaGC = 2.633764464461633`. Consequently, the variants crossing the mechanical multiple-testing cutoff are treated as confounded signals, not reportable associations. No valid discovery hit was nominated; the replication batch therefore contains `0` candidates, and `0` variants can be called replicated.

## Protocol applied

The participant retention cutoff was call rate `>= 0.95`; the plate re-genotyping trigger was a participant failure fraction `>= 0.1`. Variant retention required call rate `>= 0.95`, minor-allele frequency `>= 0.01`, and exact Hardy-Weinberg p-value `>= 0.000001` among unaffected retained participants. Discovery used familywise alpha `0.05` over retained variants. Replication would require p-value `< 0.05` and the same effect direction.

## Participant and plate QC

The input contained `240` participants: `120` affected and `120` unaffected. Participant QC failed `3` participants (P127, P142, P195), giving a failure fraction of `0.0125`. Because this does not reach the plate trigger, wholesale plate re-genotyping is not required.

The retained participant set is every input participant except P127, P142, P195: `237` participants, comprising `120` affected and `117` unaffected participants.

## Variant QC

Of `150` panel variants, `139` passed all protocol criteria and `11` failed at least one. The failed variants are: rs050014, rs050017, rs050019, rs050052, rs050071, rs050082, rs050091, rs050092, rs050096, rs050108, rs050121. Thus the retained variant set is every panel variant except those listed.

Criterion-specific failure counts were `5` for call rate, `4` for minor-allele frequency, and `2` for unaffected-participant HWE. These counts can overlap and therefore should not be added to infer unique exclusions.

## Comparability and discovery scan

PCA was computed from the QC-retained genotypes after mean imputation and variant standardization. A Welch comparison of PC1 scores gave statistic `-8.74314141983081` and p-value `4.4356006605713844e-16`, meeting the analysis criterion for separation. Affected and unaffected participants therefore are not safely comparable in an unadjusted scan on this cohort.

For diagnostic purposes, an additive trend scan was nevertheless computed over the `139` retained variants. Its Bonferroni cutoff was `0.00035971223021582735` and `27` variants crossed it, but `lambdaGC = 2.633764464461633` indicates substantial inflation. Because both PCA and inflation identify confounding, **none of these threshold crossings is declared associated and none was nominated for replication**.

## Replication

The independent replication file contains `120` participants, with `60` affected and `60` unaffected. It explicitly contains `0` nominated discovery candidates. With no candidate, no variant-level replication p-value or direction check can be computed. Accordingly, `0` variants are replicated, and replication does not support reporting any association. This is not a negative replication test of a named variant; it is the consequence of having no valid discovery nomination.

## What changed and what it achieved

Applying participant QC removed the low-call participants while preserving a usable plate. Applying variant QC removed all variants that failed the prespecified technical or population-genetic filters. Those changes produced a clean analysis matrix, but they did not resolve the key design problem: affection status remains aligned with genetic structure.

## Recommended next actions and control plan

1. Do not report the unadjusted threshold crossings as trait associations.
2. Investigate recruitment site, ancestry, plate, and batch variables, and reconcile them with PC scores.
3. Rebuild a comparable discovery set through ancestry/site matching or collect additional appropriately matched controls and cases.
4. Prespecify a covariate-adjusted logistic model using justified ancestry components and relevant technical covariates; then rerun QC, separation diagnostics, inflation assessment, and multiplicity correction.
5. Nominate variants only from a discovery analysis that passes the comparability check. Test only those nominations in the independent cohort using the prespecified p-value and same-direction rule.
6. Hold the process by retaining the current call-rate, frequency, HWE, multiplicity, and replication rules in the analysis plan and by recording all exclusions and model covariates before reanalysis.
