# Blind item V008

Focal assessment: Whether readings can support substantive analysis after the measurement system study.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the process team on an enamelled-component line. Coating thickness is accepted between 180 and 260 um with 220 um as the target. The line records five consecutive pieces at each of twenty-five sampling points through the run, the archive holds the study in which the same pieces were measured several times over by several operators on the thickness gauge, and a separate sample records thickness piece by piece for each of the four applicators.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the recorded readings can carry a conclusion, how the line has behaved across the run, where coating thickness sits against the range it is accepted in, and what specifically should change next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


## Original reporting requirements


A Markdown project report written for the plant's quality manager. Requirements:

* every number that appears in the report must be traceable to some `outputs` entry in
  `/workspace/trace.json`;
* for any step the steward `denied`, the report must state plainly that there is no data for it
  and that the conclusion stops there — do not paper over the gap with a guess;
* land the conclusions on the business: where things stand, what is causing it, what was
  changed, what the change achieved, and how it will be held.

## 6. Other constraints

* the environment has no network; every computation happens on this machine.
* the working directory is `/workspace`.
* you are free to decide your own route through the project. Whether the route was right,
  whether the numbers are accurate, and whether you reported honestly are all scored.


## Public data-service thresholds (protocol rules, not independent ground truth)
```json
{"msa_ndc":{"field":"ndc","op":">=","value":5.0,"source":"AIAG MSA-4 Ch. II Sec. D"},"msa_pass":{"field":"grr_pct","op":"<=","value":30.0,"source":"AIAG MSA-4 Ch. II Sec. D"}}
```

## Submitted report (complete, identifiers removed)
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


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"meta.data_profiling","outputs":{"lsl":180.0,"target":220.0,"usl":260.0},"status":"success","decision":"Accepted limits from charter","inputs_digest":{}}
{"step_id":2,"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":16.613104067158304,"percentTolerance":11.379541985052946,"ndc":8.0,"interactionPValue":0.8042217346111609,"repeatabilityVariance":2.3021151251481373,"operatorVariance":0.0,"interactionVariance":0.0,"partVariance":81.1092957274335},"status":"success","decision":"Random-effects crossed ANOVA; interaction pooled if p >= .05","inputs_digest":{"batch":"msa","observations":90}}
{"step_id":3,"method_id":"basic.descriptive_summary","outputs":{"mean":234.46504000000004,"median":234.35,"stdDev":6.988630816109187,"skewness":0.1321139279551168,"n":125.0,"subgroups":25.0,"subgroupSize":5.0,"observedOutside":0.0},"status":"success","decision":"Baseline thickness summary","inputs_digest":{"batch":"process_run"}}
{"step_id":4,"method_id":"control_chart.xbar_r","outputs":{"xBarChartCenterLine":234.46504000000004,"flaggedXBarCount":0.0,"xBarLCL":225.22288480000003,"xBarUCL":243.70719520000006,"rBar":16.0176,"rLCL":0.0,"rUCL":33.8612064,"flaggedRCount":0.0,"withinSigma":6.886328460877043},"status":"success","decision":"Three-sigma point rules on consecutive rational subgroups; no points excluded","inputs_digest":{}}
{"step_id":5,"method_id":"basic.normality","outputs":{"pValue":0.4671864052104712,"statistic":0.35014038647291557},"status":"success","decision":"Anderson-Darling normality with estimated normal parameters","inputs_digest":{"batch":"process_run"}}
{"step_id":6,"method_id":"capability.normal","outputs":{"cp":1.9362035094729129,"cpk":1.236021979156259,"pp":1.9078605930362282,"ppk":1.217928598218907,"offsetFromTarget":14.465040000000045},"status":"success","decision":"Normal capability using Rbar/d2 within sigma and sample overall sigma; conditional on representative rational sampling","inputs_digest":{}}
{"step_id":7,"method_id":"anova.equal_variances","outputs":{"pValue":0.718582289950883,"statistic":0.44958270376179693},"status":"success","decision":"Brown-Forsythe median-centered Levene test","inputs_digest":{"batch":"applicators"}}
{"step_id":8,"method_id":"basic.normality","outputs":{"pValue":0.9554027843607665,"statistic":0.15375164699708677},"status":"success","decision":"Normality of applicator within-group residuals","inputs_digest":{}}
{"step_id":9,"method_id":"anova.oneway","outputs":{"factorPValue":0.20526670587984125,"fStatistic":1.5763734430571472,"mean_A":232.26066666666668,"mean_B":235.69866666666667,"mean_C":235.91933333333333,"mean_D":234.99733333333333},"status":"success","decision":"Independent applicator comparison; observational association not causation","inputs_digest":{}}
{"step_id":10,"method_id":"basic.descriptive_summary","outputs":{"mean":222.6895,"median":223.135,"stdDev":5.209583754460317,"skewness":-0.005235934528104451,"n":20.0,"observedOutside":0.0,"meanReduction":11.775540000000035,"offsetFromTarget":2.6895000000000095},"status":"success","decision":"Post-change descriptive comparison only","inputs_digest":{"batch":"sustaining"}}
{"step_id":11,"method_id":"control_chart.imr","outputs":{"centerLine":222.6895,"individualsLCL":205.85579339305713,"individualsUCL":239.5232066069429,"flaggedCount":0.0,"movingRangeMean":6.3294736842105275,"movingRangeUCL":20.67839052631579,"flaggedMRCount":0.0},"status":"success","decision":"Retrospective trial I-MR limits for individual monitoring readings","inputs_digest":{}}
{"step_id":12,"method_id":"basic.normality","outputs":{"pValue":0.8273042005312048,"statistic":0.21371657946368927},"status":"success","decision":"Post-change Anderson-Darling normality","inputs_digest":{}}
{"step_id":13,"method_id":"capability.normal","outputs":{"cp":2.3761849326459332,"cpk":2.2164161982371517,"pp":2.5593855405276216,"ppk":2.387298855246395},"status":"success","decision":"Provisional post-change capability; MRbar/d2; short monitoring record","inputs_digest":{}}
```

## Submitted route declarations
```json
[{"point":"measurement","chosen_branch":"proceed conditionally","observed":{"grr_pct":16.613104067158304,"ndc":8}},{"point":"baseline","chosen_branch":"normal capability conditional on stability and representative sampling","observed":{"flaggedXBarCount":0,"normalityPValue":0.4671864052104712}},{"point":"applicators","chosen_branch":"no demonstrated applicator mean effect; investigate shared centering","observed":{"factorPValue":0.20526670587984125}},{"point":"monitoring","chosen_branch":"individuals moving range; provisional improvement without causal attribution"}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
