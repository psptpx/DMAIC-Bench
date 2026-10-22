# Metabolic-trait candidate-panel study report

## Executive conclusion

The discovery plate can carry the study forward. Sample QC passed: 2 of 240 discovery participants failed the call-rate rule, a failure fraction of 0.008333333333333333, below the allowed 0.1. After removing those participants, 238 participants remained: 118 affected and 120 unaffected.

The protocol retained 34 of 150 variants. A total of 116 variants failed at least one rule: 5 failed call rate, 4 failed MAF, and 112 failed control HWE; these categories overlap. The excluded participants were P017 and P111. The retained discovery variants are the 34 IDs recorded in the QC computation; the complete retained and excluded lists are preserved in the working analysis artifacts.

## Comparability and discovery scan

The affected and unaffected groups are not directly comparable without ancestry adjustment. The leading axis explained 0.13078054874892756 of standardized genotype variation and differed between groups with p=5.861587813431253e-14. Under the protocol, the leading ancestry axes must therefore enter the association model as covariates.

An unadjusted scan produced 10 provisional candidates at a Bonferroni threshold of 0.0014705882352941176. This is not a reportable association result: the required covariate-adjusted discovery analysis was not computed. Consequently, there is no valid adjusted discovery hit list and no discovery association can be declared from this run. The provisional unadjusted results should not be used as a conclusion.

## Replication

The independent cohort contained 120 participants: 60 affected and 60 unaffected. No replication participant failed sample QC. The steward supplied one nominated candidate, rs020008. Its call rate was 0.9916666666666667. The replication test produced p=0.0006620796019655648, an odds ratio of 2.5108199789449057, and the same direction as the supplied discovery direction. Thus, the nominated replication candidate replicated at the protocol's p<0.05 threshold.

Replication support alone is insufficient for reporting. rs020008 was not a retained discovery variant in the QC-retained set, and the required adjusted discovery result was not computed. Therefore no association is reportable at this stage. There is no denied data batch in this run; the stopping point is the missing adjusted discovery computation, not missing steward data.

## What changed, what it achieved, and what happens next

The analysis removed the two low-call-rate participants and filtered the panel to the 34 variants meeting call-rate, MAF, and control-HWE requirements. This achieved a passing plate-level sample QC result and a defined discovery analysis set. The ancestry check then changed the analysis route from an unadjusted comparison to a covariate-adjusted association model.

Next, investigators should rerun the discovery association analysis on the 238 retained participants and 34 retained variants with the leading ancestry axes as covariates, apply the Bonferroni rule over the 34 retained variants, and nominate only those adjusted discovery hits for replication. Any nominated hit must replicate with p<0.05 in the same direction before it can be reported. The QC exclusions, retained variant list, ancestry decision, model specification, and replication rule should be locked in the analysis record so that the result is held reproducibly.
