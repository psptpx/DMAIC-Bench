# Discovery panel decision report

## Executive decision

The genotyping plate passes participant-level quality control, but this cohort cannot support the intended case-control association conclusion. The retained affected and unaffected groups are completely separated on ancestry axis PC1. The protocol expressly forbids comparing groups drawn from separate ancestries. I therefore stopped before variant association testing and did not open or test the independent replication cohort.

Consequently, there are no valid discovery associations, no nominated candidates, and nothing eligible for replication or reporting. This is a cohort-design limitation, not evidence that the retained variants lack association.

## Participant quality and plate disposition

The discovery input contained 240 participants and 150 assayed variants. Applying the participant call-rate threshold of 0.95 failed 2 participants: **P039** and **P197**. The failure fraction was 0.008333333333333333, below the plate stop limit of 0.1; the minimum observed participant call rate was 0.94. The plate therefore does not require wholesale re-genotyping under this rule.

The retained participant set is all input participants except P039 and P197: 238 participants, comprising 119 affected and 119 unaffected participants.

## Variant quality

Variant QC was applied after participant exclusion. The rules were call rate at least 0.95, minor-allele frequency at least 0.01, and unaffected-participant Hardy-Weinberg p-value at least 1e-06. Of 150 assayed variants, 12 failed and 138 were retained. Failures by criterion were 5 for call rate, 4 for minor-allele frequency, and 3 for Hardy-Weinberg equilibrium.

The excluded variants are: **rs010047, rs010057, rs010063, rs010072, rs010088, rs010092, rs010101, rs010118, rs010128, rs010133, rs010141, rs010149**.

The retained variant set is every assayed variant except those listed above. Had the ancestry gate passed, the computed Bonferroni association threshold over the retained set would have been 0.00036231884057971015; it was not used to test variants because the mandatory ancestry gate failed.

## Cohort comparability

PCA was computed from the retained, mean-imputed and standardized genotype matrix. PC1 accounted for 0.08458419269851693 of matrix variance. Affected scores ranged from -5.479999991945816 to -1.3056486675438899; unaffected scores ranged from 0.3542467392779523 to 6.467762697901457. Their range-overlap fraction was 0.0. The between-group test on that axis gave p=4.1188787428926535e-128 with statistic -54.39945230423162.

This is separation, not merely overlapping structure that can safely be handled by adding ancestry axes as covariates. A covariate-adjusted model would have no support for distinguishing affection from ancestry. The affected and unaffected participants must not be compared in this cohort.

## Association and replication status

No discovery association analysis was run. Reporting a variant p-value or effect estimate would violate the protocol and would confound ancestry with affection status. There are therefore no associated variants under this study design.

Replication was not analyzed because no protocol-valid discovery hit exists to nominate. Thus replication neither supports nor refutes a reportable association; the conclusion stops at the failed ancestry precondition.

## Required next action and control plan

Investigators should rebuild the discovery comparison with ancestry-matched affected and unaffected participants, or recruit enough participants within overlapping ancestry strata to support a prespecified stratified analysis. Re-genotyping the whole current plate is not the remedy because the plate passed its participant-failure rule.

For the replacement cohort, hold the sequence fixed: participant QC, variant QC, ancestry assessment before outcome association, then ancestry-adjusted testing only where groups overlap. Use the retained-variant Bonferroni denominator from that rerun, nominate only valid discovery hits, and expose the independent replication cohort only after nomination. Report a hit only when the independent result passes the protocol rule and has the same effect direction.
