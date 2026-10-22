# Project status report

## 1. Can the sound/defective judgement be relied on?

The inspector study against the answer key gives an overall agreement of `93.33%` and an overall appraiser-vs-standard kappa of `0.855` (step 1). The minimum appraiser-vs-standard kappa is `0.681`, and the minimum within-appraiser kappa is `0.659`. That is moderate but below the common desirable kappa threshold of 0.75, so the judgement can be used for this investigation, but the inspection process should be improved before it is considered reliable enough for long-term routine decision-making.

## 2. Has the defective share held steady across the lots?

The 25-lot record contains `25` lots of `5000` inspected units each, with a total of `322` defective units and `125000` inspected units (step 2). The p-chart center line is `0.002576` (`2576` DPMO), with control limits `0.000425` and `0.004727`. The number of out-of-control lots is `0`. The defective share is therefore stable across the lots at an average above the charter target.

## 3. How does the 25-lot period compare with the charter?

The charter target is 1500 DPMO. The 25-lot average is `2576` DPMO, and a one-proportion test against 1500 DPMO gives `z = 9.830` and `p = 0.000000` (step 3). The lot record is significantly worse than the committed maximum level.

## 4. What is causing the defects?

The reject-category tally shows that `loose end` is the largest category, accounting for `30.42%` of the recorded reject count (step 4). The risk-rated failure-mode table gives the highest RPN to `seam split`, with `maxRpn = 360` (step 5). So the biggest observed category is loose end, while the highest-risk failure mode by RPN is seam split.

## 5. Are machine differences driving the defect share?

The machine-by-machine defective/sound tally yields a chi-square statistic of `2.578` with `p = 0.461` (step 6). There is no statistically significant association between machine identity and defect outcome in this window; the machine differences alone do not explain the charter miss.

## 6. What did the change achieve?

On the one machine with before/after data, the defect share moved from `1500` DPMO before the change to `2750` DPMO after the change, with `z = 1.214` and `p = 0.225` (step 7). The difference is not statistically significant and is numerically worse after the change, so this single before/after snapshot does not demonstrate an improvement from that change.

## 7. Where does the process stand today?

The sustaining record kept since the change has `100000` inspected and `104` defective units, for `1040` DPMO (step 8). Against the 1500 DPMO charter target, the test yields `z = -3.759` and `p = 0.000171`. The current sustaining record is therefore below the committed level, and the difference is statistically significant.

## 8. What should be done next?

Although current sustaining data are below the 1500 DPMO target, the historical 25-lot period was stable but above target, the measurement system is only moderately reliable, and the immediate before/after change snapshot did not show a significant improvement. The next steps should be:

1. Improve the inspection method, focusing on within-appraiser and appraiser-vs-standard agreement, then rerun the measurement system study before relying on counts for routine disposition.
2. Investigate `loose end`, the top reject category, and `seam split`, the highest-RPN failure mode, through process and defect-data investigations.
3. Use the sustaining record as a provisional control metric but validate with the improved measurement system.
4. Continue sampling after the change to confirm the current below-target level is sustainable rather than a short-run fluctuation.
