# Precision-Turning Cell: Outer Diameter and Wall Thickness - Project Report

## 1. Can the readings carry a conclusion?

Yes, for the instrument itself. A crossed Gage R&R study (3 operators x 10 parts x 3 replicates,
90 readings) on the measuring instrument gave:

- percent Study Variation (Gage R&R) = 17.68%
- percent Tolerance = 9.80%
- Number of Distinct Categories (NDC) = 7.85

Against the AIAG guideline (under 10% excellent, 10-30% acceptable, over 30% unacceptable) and
the NDC>=5 rule of thumb, this measurement system is acceptable - the readings that follow
are trustworthy enough to base a decision on. It is not an excellent system, so part of the
variation seen in the run data has some measurement noise mixed in, but not enough to
invalidate the conclusions below.

## 2. Outer diameter (accept 24.80-25.20 mm)

125 readings, 25 subgroups of 5, in sampling order.

- X-bar chart centerline = 25.0007 mm, 0 subgroups flagged on the X-bar chart, 0 on the
  Range chart. The run is in statistical control.
- Normality: Shapiro-Wilk p = 0.518, Anderson-Darling statistic = 0.39 (well inside the normal
  range), skewness = 0.07. Diameter is normally distributed.
- Capability (normal method): Cp = 1.63, Cpk = 1.62, Pp = 1.61, Ppk = 1.61.

Outer diameter is stable, normally distributed, and highly capable, sitting comfortably inside
its 24.80-25.20 mm window. This characteristic is not a source of concern.

A secondary sample split diameter by the four turning fixtures (15 pieces each, N=60). A
one-way ANOVA found a statistically significant difference in mean diameter across fixtures
(F = 4.08, p = 0.011): fixture 4 runs highest (mean 25.021 mm) and fixture 2 lowest
(mean 24.982 mm). This is real fixture-to-fixture variation, but the overall diameter
distribution above already folds in all four fixtures and is still comfortably capable, so this
finding is noted for fixture maintenance and alignment follow-up but does not change the diameter
verdict.

## 3. Wall thickness (accept 1.20-1.60 mm)

125 readings, 25 subgroups of 5, in sampling order.

- X-bar chart centerline = 1.4002 mm, 0 subgroups flagged on the X-bar chart, but 4
  subgroups flagged out-of-control on the Range chart (subgroup indices 20, 21, 22 and 24,
  covering sampling points roughly 100-124, i.e. the last fifth of the run). The mean has not
  shifted, but the piece-to-piece spread within those subgroups blew out.
- Normality: Shapiro-Wilk p < 0.0001, Anderson-Darling statistic = 3.75, skewness = -0.86. Wall
  thickness is not normally distributed - the distribution is left-skewed, driven by the
  same late-run subgroups that flagged on the Range chart.
- Because the data fails normality, the normal-theory capability numbers (Cp=1.42, Cpk=1.41,
  Pp=1.29, Ppk=1.29) are computed for reference only and are not used as the reported
  capability - they overstate how capable the process really is by assuming a bell curve that
  the data does not follow.
- Capability (non-normal, percentile method, appropriate given the failed normality test):
  Pp = 1.04, Ppk = 0.89.

A Ppk of 0.89 sits below the conventional 1.00 capable floor. Wall thickness is the
characteristic that decides what this project does next, because it is the one that is not
reliably capable, while outer diameter comfortably is.

### What is causing it

A paired sample of coolant delivery pressure and wall thickness (n=60) was tested for a
relationship: Pearson correlation coefficient = -0.0046, p = 0.972. There is no linear
relationship between coolant pressure and wall thickness - coolant delivery pressure is ruled
out as the driver of the late-run spread blow-out.

No other process-fact record exists for what happened in the plant around sampling points
100-124. A direct question to the process owner about that window returned no recorded process
fact (routing refusal: unroutable, with no process topics on file). This is a genuine gap
in the record, not filled in with a guess: the mechanical or process root cause of the
Range-chart excursions is unknown from the data available in this exercise.

## 4. What was changed and what it achieved

No process change has been made yet in this record. The analysis to this point has:

- Confirmed the gage is fit to trust the readings (percent GRR 17.68%, NDC 7.85 - acceptable).
- Cleared outer diameter as capable and stable (Cpk 1.62).
- Identified wall thickness as the at-risk characteristic (Ppk 0.89, non-normal, driven by 4
  out-of-control Range-chart points late in the run).
- Ruled out coolant delivery pressure as the cause (r = -0.005, p = 0.97).
- Flagged, but not resolved, a real difference in diameter mean by turning fixture (p = 0.011)
  as a separate, secondary lead worth chasing on its own track.

## 5. How this will be held

- Outer diameter: continue routine X-bar/R monitoring; no action required now, but track the
  fixture-to-fixture diameter difference (fixture 2 vs fixture 4) since it is statistically real
  even though overall capability is unaffected.
- Wall thickness: treat as the open item. The Range-chart excursions in the last fifth of
  the sampled run, and the resulting Ppk of 0.89, mean the process cannot yet be called capable
  for wall thickness. Coolant pressure has been eliminated as a cause. The next step is to get a
  process fact (tooling wear timing, coolant chemistry change, operator changeover, or similar)
  for what happened around sampling points 100-124 - that fact was asked for and is not
  available in this system, so it needs to come from the shop floor directly, not from further
  data analysis of what is already on hand.
