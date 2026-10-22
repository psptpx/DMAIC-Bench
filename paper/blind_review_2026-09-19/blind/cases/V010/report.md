# Fillet-Height Process Review

## Bottom line

The baseline was inside the acceptance limits but was centered too low. The designed run showed that chain speed and rail angle, including their interaction, account for almost all experimental variation; air pressure did not. The comparison after the line change showed a statistically significant shift: it raised fillet height and reduced variation, and every observed joint remained inside limits. However, it moved the window mean above target and left the after-window capability constrained toward the upper limit. The next action is a small, closely controlled return toward the DOE corner predicted near target, followed by confirmation and monitoring.

## Baseline: where the line stood

The consecutive record contained 60 joints. The accepted range was 6.80–7.50 mm and the target was 7.15 mm. All 60 joints passed: the count below the lower limit was 0 and above the upper limit was 0. Observed fillet height ranged from 6.936 to 7.186 mm.

The mean, 7.0317 mm, and median, 7.023 mm, sat below target. The one-sample t-test against target gave t = -17.4346 and p = 5.96874e-25, so the low centering was statistically clear, not random noise. Standard deviation was 0.052559 mm. Anderson–Darling normality was rejected (statistic = 0.940414, p = 0.0161038), which makes normal capability and t inferences approximations rather than exact derivations.

Normal-theory capability was nevertheless directionally useful. Cp was 2.24145 and Cpk was 1.48384, indicating that spread was not the constraint; Cpk was limited by distance from the lower limit. Pp was 2.21973 and Ppk was 1.46946. The individuals chart had 0 flags; its center line was 7.0317 mm with control limits of 6.87553 and 7.18787 mm. The median runs test also gave no signal (p = 0.416654). Thus this was a stable-appearing, low-centered process rather than a sequence of uncontrolled spikes.

## Whether varied settings accounted for fillet height

The released design contained 16 runs: two replicates at each corner of three coded factors. The full coded factorial model was significant (p = 2.3531e-05) and explained 96.7834% of variation. Chain speed was significant (coded coefficient +0.142056, p = 2.82767e-06); rail angle was significant (+0.110344, p = 1.87136e-05); and their interaction was positive and significant (+0.0586938, p = 0.0013891). Air pressure was not significant (coefficient -0.0104188, p = 0.420739).

The parsimonious model with chain speed, rail angle, and their interaction remained strong (adjusted R-squared = 94.3817%, p = 2.37078e-08). At the coded corner with chain speed at +1 and rail angle at -1, it predicted 7.1254 mm, with a prediction interval of 7.00994–7.24086 mm. This is the observed design corner closest to the 7.15 mm target and is the direction to test next. Because the steward held no matching process fact, the physical low/high settings behind the coded levels could not be obtained; the team must map +1/-1 to plant setpoints before implementation.

The three variables recorded but not varied in the experiment do not explain the response. Their joint observational model had p = 0.456114 and R-squared = 5.69283%. Marginal correlations for preheat temperature, conveyor width, and solder-pot dwell were respectively 0.154323 (p = 0.294967), 0.114879 (p = 0.43686), and -0.0703937 (p = 0.634476). These are associations, not causal estimates, and none was statistically significant.

## What the line change achieved

Each change window contained 30 joints in supplied order. Before the change, mean fillet height was 7.11773 mm, the median was 7.1085 mm, and standard deviation was 0.129493 mm. After it, the mean was 7.3121 mm, the median was 7.323 mm, and standard deviation was 0.0684268 mm. Every joint in both windows was inside the acceptance limits.

The Welch comparison found a clear increase: mean after minus mean before was 0.194367 mm, with a confidence interval of 0.140477–0.248257 mm, t = 7.26877, and p = 4.60977e-09. The Brown–Forsythe test found lower after-window variance (variance ratio = 0.279227, p = 0.000394892). Mann–Whitney agreed (p = 7.69178e-08). Thus the change was demonstrably associated with both a higher center and less short-term variation.

It over-shot target. The before-window mean was not statistically distinguishable from target (t = -1.36479, p = 0.182814), whereas the after-window mean was above target (t = 12.9753, p = 1.32646e-13). After-window Ppk was 0.915333 versus 0.817888 before, so capability improved but remained below the usual desirable level and was constrained toward the upper limit. The after-window individuals chart had 0 flags, although its moving-range chart had 1 flag; the process therefore needs centering and continued surveillance rather than emergency containment.

## Data gaps and certainty

No project batch was denied. The engineer had no matching process fact for either request, so the physical factor-level mapping and the name of the change made between windows could not be obtained. Consequently, the analysis can establish the coded DOE effects and the measured before/after difference, but cannot identify the exact hardware, setpoint, or recipe change and cannot isolate other events that happened at the same time as the change. The coded coefficients also should not be interpreted as physical units until the low/high mapping is recovered.

## Recommended next actions

Run a small confirmation at the DOE corner using high coded chain speed and low coded rail angle; the prediction there is 7.1254 mm with a prediction interval of 7.00994–7.24086 mm. Hold air pressure at one standardized plant setting because it was not significant. Do not make a production commitment until the coded corner has been translated to documented physical setpoints and confirmed on this line.

After that confirmation, calculate capability from an appropriate prospective sample, set control limits around the confirmed center, and monitor individuals and moving range. Review every moving-range signal and re-center in small steps if the mean remains above target. Keep the acceptance limits and target unchanged, record the exact production settings, and retain the three additional process variables in the log for surveillance rather than using this observational result as evidence to adjust them.
