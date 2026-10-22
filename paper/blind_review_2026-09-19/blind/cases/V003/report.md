# Fillet Height Project Report - Wave-Soldering Line

## Scope and accepted range

Fillet height is accepted between 6.80 mm and 7.50 mm, target 7.15 mm. All numbers below come from computations run against the shop-floor batches released by the data steward (baseline record, designed run, before/after windows, and the logged-variable set).

## 1. Where the baseline stood

Sixty consecutive joints were recorded in production order (batch baseline).

- Mean = 7.1605 mm, median = 7.1765 mm, standard deviation = 0.1395 mm, skewness = -0.240.
- Anderson-Darling normality test: statistic = 0.314, p = 0.464 - no evidence against normality.
- I-MR individuals chart: center line 7.1605, UCL 7.5705, LCL 6.7505, 0 points out of control. The baseline run was statistically stable - no special-cause signals in 60 joints.
- Capability against the 6.80-7.50 mm spec: Cp = 0.854, Cpk = 0.828, Pp = 0.836, Ppk = 0.811.

Bottom line: the line was stable and roughly centered on target, but not capable. A Cpk around 0.83 (well under the conventional 1.33 bar) means the natural process spread is wide relative to the tolerance band, even with no drift or special causes present. This is a spread problem, not a centering or a stability problem.

## 2. Does the designed run explain fillet height?

A 2^3 full factorial (chain_speed, rail_angle, air_pressure), replicated twice, 16 runs, was analyzed by OLS regression with all interactions (batch design).

- Model overall: p = 7.7e-05, R-squared = 95.65%, adjusted R-squared = 91.84%. The three settings, together with their interactions, account for nearly all of the run-to-run variation in this designed experiment.
- chain_speed: p = 5.8e-06 (highly significant main effect).
- rail_angle: p = 1.4e-04 (highly significant main effect).
- chain_speed x rail_angle interaction: p = 0.008 (significant).
- air_pressure: p = 0.065 - not significant at the conventional 0.05 level on its own.

Conclusion: chain_speed and rail_angle drive fillet height, and they interact - the effect of one depends on the level of the other. Air_pressure's main effect is marginal and should not be treated as a lever on its own without further runs.

## 3. Did the change that was made do anything?

The archive holds a before-window and an after-window of fillet height (batch after_change, 30 joints each), bracketing a change to the line. Both windows are consistent with normality (AD p = 0.346 before, p = 0.495 after), so a t-test is appropriate, but a Levene test found the variances differ significantly (p = 0.022), so a Welch (unequal-variance) t-test was used:

- Before: mean = 7.1567 mm, sd = 0.1032 mm (n = 30).
- After: mean = 7.1957 mm, sd = 0.1473 mm (n = 30).
- Welch's t-test: t = -1.189, p = 0.240 - no statistically significant shift in mean.
- Mann-Whitney U (nonparametric check): p = 0.359 - confirms no significant location shift.

However, capability moved in the wrong direction:

- Before-window capability: Cp = 1.126, Cpk = 1.105, Pp = 1.131, Ppk = 1.109.
- After-window capability: Cp = 0.735, Cpk = 0.639, Pp = 0.792, Ppk = 0.689.

The change did not move the mean, but the spread widened (Levene p = 0.022) and capability fell from a Cpk near 1.1 to a Cpk near 0.64. On the numbers alone, whatever was changed made the process less consistent, not more, even though nobody would see it by looking at the average.

What the change actually was, and whether it was based on the DOE findings, could not be established. I asked the process owner directly; the request came back refused (unroutable - no process fact on file matches it). This is a real gap: without knowing what was changed, we cannot say whether the DOE-significant factors (chain_speed, rail_angle) were the ones touched, or something unrelated was adjusted. The report stops there on that specific question rather than guessing.

## 4. The three logged-but-unvaried variables

Preheat zone temperature, conveyor width setting, and solder pot dwell time were recorded throughout the run (batch logged_variables, 48 rows) but never deliberately varied. An OLS regression of fillet height on all three gives model p = 0.893, R-squared = 1.37%, adjusted R-squared = -5.35%. None of the three show a usable relationship with fillet height in this data. That is consistent with them being background noise rather than levers - but because they were never varied, this is an observational, not causal, statement; it does not rule out an effect that only shows up outside the narrow range these variables happened to occupy during the run.

## 5. What this means for the business

- The line is currently running with a fillet-height spread too wide for the tolerance band (baseline Cpk 0.83; after-change Cpk 0.64 - worse, not better).
- The designed experiment identifies chain_speed and rail_angle, and their interaction, as the real levers on fillet height. Air_pressure is not a confirmed lever at this sample size.
- The line change that was actually made cannot be shown to have improved the mean, and the data suggest it made the process more variable, not less. This should be treated as a caution flag, not a win, until the nature of the change is documented.
- The three continuously-logged variables (preheat temp, conveyor width, dwell) do not explain fillet height in the ranges observed and are not a current line of investigation.

## 6. Recommended next steps

1. Identify and document what was actually changed between the before and after windows, and confirm whether it touched chain_speed or rail_angle. Until this is on record, the after-change capability drop cannot be diagnosed.
2. Re-target chain_speed and rail_angle using the DOE model (which explains 95.65% of run-to-run variance) to find a setting combination that both centers the process on 7.15 mm and reduces variance - the interaction means this is not a simple two independent-knob adjustment.
3. Do not roll out the recent line change further until the variance increase is understood; a Cpk of 0.64 is a regression from the already-inadequate baseline of 0.83.
4. Re-run a baseline-style stability check (I-MR chart, capability) after any deliberate re-setting, since none of the analysis above found instability - only inadequate spread and, after the change, added spread.
