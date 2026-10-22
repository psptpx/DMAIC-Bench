# Coating thickness: project assessment

## Management conclusion

The recorded readings support a **qualified process assessment**, not an unconditional measurement-system endorsement or a proven causal improvement claim. The baseline line was reasonably consistent under the chart checks performed, but ran above target. Subsequent monitoring is much better centered and less variable. There is no convincing evidence that applicator identity explains the baseline offset. The intervention itself is not documented in the supplied records, so its mechanism and effectiveness cannot be attributed to a specific action.

## Can the readings carry a conclusion?

The crossed random-effects gauge study gives gauge R&R of **16.61% of study variation**, **11.38% of tolerance**, and **8 distinct categories**. This is usable conditionally for process improvement, but measurement error is not negligible. Operator-by-part interaction was not evident (p = **0.8042**); the nonsignificant interaction was pooled with repeatability. Estimated operator and interaction variance components were **0**, which is a boundary estimate rather than proof of perfect operator agreement.

Retain the gauge for this assessment, while checking calibration, reference standards, positioning, surface preparation and operator technique. R&R does not establish accuracy, bias, linearity or long-term gauge stability; those were not measured here. Do not use this study alone to settle borderline product acceptance disputes.

## Baseline behavior and acceptance

The charter specifies **180–260 um**, with **220 um** as target. The baseline contains **125 readings**, arranged as **25 consecutive subgroups of 5**. The mean was **234.465 um**, overall standard deviation **6.989 um**, and mean offset above target **14.465 um**. There were **0 observed readings outside the accepted range**; that does not guarantee future conformance.

An Xbar–R chart is appropriate to the supplied consecutive-piece grouping, conditional on those pieces sharing comparable operating conditions. The mean-chart limits were **225.223–243.707 um**, with **0 flagged subgroup means**. Average range was **16.018 um**, and the range-chart upper limit was **33.861 um**, with **0 flagged ranges**. These are retrospective point-limit checks, not proof that all special causes or serial patterns are absent. No points were discarded or limits selectively recalculated.

Anderson–Darling normality p = **0.4672** provides no strong evidence against the normal approximation. Within-subgroup sigma was **6.886 um**, estimated from average range. Capability was:

| Index | Baseline |
|---|---:|
| Cp | 1.936 |
| Cpk | 1.236 |
| Pp | 1.908 |
| Ppk | 1.218 |

The spread has substantially more potential than the current centering delivers. The upper acceptance boundary is limiting. These estimates include measurement variation and assume representative sampling; they should not be treated as a contractual capability approval without an agreed criterion.

## What explains the offset?

Applicator mean thicknesses were **232.261 um** for A, **235.699 um** for B, **235.919 um** for C and **234.997 um** for D. Median-centered Levene p = **0.7186** and residual normality p = **0.9554** support using the ordinary independent-group ANOVA as an exploratory comparison. ANOVA gave F = **1.5764**, p = **0.2053**.

The data do not establish an applicator mean effect; nor do they prove the applicators equivalent. All observed applicator means are high of target. Investigate shared setup and operating conditions before replacing or individually compensating applicators. Candidate causes such as common delivery settings, coating properties, line speed and setup calibration remain hypotheses, not measured root causes. Independence and freedom from time/material confounding were not documented.

## What changed and what did it achieve?

The steward supplied a record labeled as readings kept since the change. The process-owner query returned no matching process fact and stated that no process topics were recorded. **The actual change, implementation details and rationale are unavailable.** No released data batch was denied; rather, the owner fact query was unroutable. Therefore this report cannot identify an implemented setting, claim an optimized recipe, or establish causation.

The subsequent **20 individual readings** had mean **222.6895 um**, standard deviation **5.2096 um**, and **0 observed readings outside acceptance**. The mean decreased by **11.7755 um**, leaving an offset of **2.6895 um** above target. This is descriptive evidence of better centering and reduced observed spread, not a controlled experiment.

For the individual observations, trial I–MR limits were **205.856–239.523 um**, with **0 flagged individuals**. Average moving range was **6.3295 um** and its upper limit **20.6784 um**, with **0 flagged moving ranges**. Normality p = **0.8273**. Provisional normal capability was Cp **2.376**, Cpk **2.216**, Pp **2.559**, and Ppk **2.387**. The short record and retrospective limits make these promising preliminary estimates, not proof of durable long-term capability. The sampling structure differs from baseline, so within-process capability estimates use different sigma estimators.

## Specific next actions and how to hold the gain

- **Process engineering:** recover and sign off the change log, actual settings, material conditions, dates and implementation scope. Until then, preserve the current setup rather than attempting to reproduce an unknown intervention.
- **Quality and metrology:** verify gauge references and technique, investigate repeatability contributors, and repeat the gauge study after corrective work. Maintain routine reference checks and a clear escalation route for suspect measurements.
- **Engineering:** prioritize a controlled centering study of common settings. Randomize feasible setting changes, block by material and operating period, and track applicator identity. Confirm the preferred setting in an independent production run before standardizing it. Do not target a particular applicator from the present nonsignificant comparison.
- **Production and quality:** continue time-ordered monitoring with the current trial I–MR limits for individual sampling. If consecutive-piece subgroup sampling resumes, use an appropriate subgroup chart and independently establish its limits; do not mix the chart designs.
- **Shift lead:** on a chart signal, verify the measurement, contain potentially affected output since the last confirmed acceptable check, and investigate setup, material and equipment changes. Document the cause and action before restarting; avoid automatic adjustment to routine common-cause variation.
- **Quality manager:** review an expanded, representative monitoring period spanning shifts, operators and materials. Freeze approved settings and work instructions, assign chart-review responsibility, and recalculate capability only after stability and measurement adequacy are reconfirmed. Keep specification limits separate from statistical control limits.

## Audit basis

All reported numerical results are rounded from `trace.json` outputs. `analyze.py` contains the computations from the steward's complete local JSON batches. The trace distinguishes baseline, applicator and monitoring analyses. Normality nonrejection and absence of point-limit signals are supporting diagnostics, not guarantees. No measured causal model, documented intervention recipe, gauge accuracy assessment or long-term validation was available to close those gaps.
