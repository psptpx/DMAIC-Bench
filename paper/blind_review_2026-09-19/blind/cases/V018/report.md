# Fillet-Height Project Report - [TASK]

## Reviewed data
- Baseline record: n = 60 consecutive joints.
- Accepted range: lsl = 6.8, target = 7.15, usl = 7.5 mm.
- Logged-variable run: n = 48 records for v1 (preheat zone temperature), v2 (conveyor width setting), and v3 (solder pot dwell).
- Designed run: full factorial with 3 factors, 16 runs, and 2 replicates per corner.
- Before/after windows: n = 30 and n = 30 joints respectively.
- No matching process fact was available when the process owner was asked to describe the physical change between the windows; therefore the specific intervention cannot be named from this run.

## Baseline behavior and acceptance range
- Mean fillet height = 7.16048 mm, median = 7.1765 mm, standard deviation = 0.139507 mm, skewness = -0.245767.
- Minimum = 6.807 mm and maximum = 7.414 mm.
- 0 baseline joints were outside the accepted range.
- Normality checks: Shapiro-Wilk p = 0.502616 (statistic 0.981659), Anderson-Darling p = 0.535813 (statistic 0.314428). There is no evidence of non-normality.
- One-sample t-test against target 7.15 mm: p = 0.562735, t = 0.582073. The baseline mean is not detectably different from target.
- I-MR chart: center line = 7.16048 mm, UCL = 7.57046 mm, LCL = 6.7505 mm, flagged points = 0. No control signals were found.

## Capability against the accepted range
- Baseline capability: Cp = 0.8537, Cpk = 0.828129, Pp = 0.843333, Ppk = 0.818073.
- Although no individuals were outside specification, the baseline process spread is large relative to the 6.8-7.5 mm tolerance.

## Designed run: which varied settings mattered?
- The full factorial model was significant: p = 7.68869e-05, R-squared = 95.6501%, adjusted R-squared = 91.8439%.
- Chain speed was significant: p = 5.78114e-06, high-minus-low effect = 0.288663 mm.
- Rail angle was significant: p = 0.000141818, high-minus-low effect = 0.185713 mm.
- The chain-speed/rail-angle interaction was significant: p = 0.00807677.
- Air pressure was not statistically significant: p = 0.0652331, high-minus-low effect = 0.0585625 mm.
- Conclusion: the varied settings do account for much of the fillet-height variation, primarily through chain speed, rail angle, and their interaction; air pressure is not established as an active effect.

## Logged variables
- Regression of fillet height on v1, v2, and v3 gave model p = 0.893105, R-squared = 1.37157%, adjusted R-squared = -5.3531%.
- Individual p-values were v1 = 0.610238, v2 = 0.765491, and v3 = 0.731784.
- These logged variables do not account for the fillet-height response in this record.

## Before-versus-after change comparison
- Before-change window: mean = 7.15667 mm, standard deviation = 0.103152 mm, Cp = 1.12645, Cpk = 1.10499, Pp = 1.15035, Ppk = 1.12844.
- After-change window: mean = 7.1957 mm, standard deviation = 0.147313 mm, Cp = 0.735054, Cpk = 0.639077, Pp = 0.805501, Ppk = 0.700325.
- Both windows had 0 and 0 values outside specification, respectively.
- Mean difference (after minus before) = 0.0390333 mm. Welch two-sample t-test: t = -1.18882, p = 0.239919. The change cannot be shown to have shifted the mean.
- Levene equal-variance test: statistic = 5.58918, p = 0.0214412. The after-change window has significantly greater variance.
- Therefore the change is not demonstrated to have improved fillet height; the evidence points to a possible degradation in spread and capability that should be investigated.

## Recommended next actions
- Do not credit the process change as an improvement. Investigate and eliminate the increased spread in the after-change window.
- Continue I-MR monitoring and capability checks against the 6.8-7.5 mm accepted range while the issue is investigated.
- Run confirmation trials around chain speed and rail angle, including their interaction, to move the mean to target 7.15 mm without increasing spread.
- Keep logged v1-v3 records for diagnostic context, but do not treat them as response drivers based on this analysis.
- Reassess capability after corrective action and confirm that the process is stable in both location and spread.
