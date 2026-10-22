# Case-control candidate-panel assessment

## Executive conclusion

The plate can carry a conclusion: discovery sample QC passed, the case and control groups were available for comparison, and variant QC produced a defined analysis set. However, the study does **not** support reporting an associated variant under the protocol. No retained variant met the Bonferroni-corrected discovery criterion, and no evaluated nominal candidate replicated.

## What was retained

Discovery sample QC failed for 3 participants, a failure fraction of 0.0125, below the protocol maximum of 0.1. The resulting analysis set contained 237 participants. Variant QC retained 138 of 150 variants; the variant call-rate pass count before the remaining variant filters was 145. The affected and unaffected counts were 120 and 120, respectively, so the planned case-control comparison was possible.

Replication sample QC failed for 1 participant, a failure fraction of 0.008333333333333333, and retained 119 participants. Replication variant QC retained 141 of 150 variants.

## Association and replication

The protocol cutoff was 0.05 divided by the 138 retained discovery variants, giving 0.00036231884057971015. Zero variants met that corrected threshold. Four nominal signals were below 0.05: rs040007 (p=0.0086080795615435), rs040123 (p=0.03805299080101593), rs040131 (p=0.04446690305258849), and rs040143 (p=0.04659919664846377). They are exploratory only because none met the corrected criterion.

The steward batch nominated 0 candidates for replication. For completeness, the four nominal candidates were evaluated against the independent replication calls. Their replication p-values were 0.4624655194532763, 0.7132224629711441, 0.15123975969049577, and 0.7303646767223837, respectively. Zero of 4 met the replication p<0.05 and same-direction rule. rs040131 also showed discordant direction; the other 3 had the same direction, but still failed the replication p-value requirement.

## Business interpretation and next steps

The immediate cause of the non-conclusion is statistical: nominal signals did not survive the protocol correction, and none of the evaluated candidates met independent replication. QC itself did not stop the analysis. The change made was to apply the released protocol thresholds, remove failing participants and variants from the analysis sets, apply the corrected discovery threshold, and then assess replication with both its p-value and direction requirements. This achieved a reproducible, protocol-compliant stopping point rather than an unsupported association claim.

Investigators should not report a panel association from this release. They should preserve the QC exclusions, retained-variant manifest, analysis code, and trace, and seek additional samples or a pre-specified follow-up study before reopening association claims. Any future candidates should be nominated only after meeting the corrected discovery rule and should be tested in an independent cohort using the same replication rule.
