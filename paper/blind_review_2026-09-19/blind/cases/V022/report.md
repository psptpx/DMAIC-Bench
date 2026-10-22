# Appearance Defect Improvement Project Report

## Measurement reliability
All requested shop-floor batches were released; no data batch was denied. Attribute agreement with the answer key was 93.333%. The appraiser-vs-standard kappa range was 0.7 to 1.0, the between-appraiser Fleiss kappa was 0.736, and the minimum repeat kappa was 0.6. The measurement system can support coarse process comparisons, but it should not be used for lot-by-lot decisions until repeatability is improved.

## Baseline and stability
The lot record contains 25 lots, 125000 inspections, and 334 defects. The overall level was 2672 DPMO with center line 0.002672. The p-chart flagged 0 lots, so the lot-to-lot defective share was stable rather than shifting randomly. The test against the 1500 DPMO charter target gave p = 3.396e-22, so the baseline is significantly above the committed level. The corresponding process Z was 2.786.

## Causes and machine pattern
Reject categories totalled 240, and loose end was the largest category at 142 rejections, or 59.167% of the category total. In the FMEA, loose end had the maximum RPN of 294. The machine tally showed 26 defects in 4000 units for the high-rate machine (6500 DPMO), against 6 in 4000 (1500 DPMO), 6 in 4000 (1500 DPMO), and 4 in 4000 (1000 DPMO) for the other machines. The chi-square test gave statistic 30.843 and p = 9.17e-7. The priority is the machine with the 6500 DPMO rate and the loose-end defect mode.

## Change result
The supplied before/after record had 18 defects in 4000 before the change (4500 DPMO) and 13 defects in 4000 after (3250 DPMO). The proportions test gave z = 0.9 and p = 0.368, so the improvement is not statistically demonstrated. The after-change level is still above the 1500 DPMO charter. The process owner could not supply a matching process fact, so the changed machine and change mechanism are not identifiable from the released data.

## Sustaining
The post-change monitoring record contains 89300 inspections and 110 defects. Its center line was 0.0012318 (1231.8 DPMO), and the p-chart flagged 0 points. Against the 1500 DPMO target, p = 0.985 and the process Z was 3.028. The monitored window is statistically consistent with the committed level.

## Next actions
- Audit and correct loose-end generation on the high-rate machine; loose end has the largest Pareto share and the maximum RPN.
- Improve inspector repeatability before using lot-level judgements for accept/reject decisions; the weakest repeat kappa is 0.6.
- Re-run the changed-machine comparison with more data; the current p = 0.368 does not establish a change effect.
- Continue the post-change p-chart and confirm that 0 points remain outside control limits.
