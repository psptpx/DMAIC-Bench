# Blind item V046

Focal assessment: Baseline defect-rate chart stability, business performance, and next steps.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team on a high-speed rod-making line. Every unit leaving the line is judged sound or defective on appearance, and the charter commits us to no more than 1500 defective units per million inspected. The archive holds the inspected and defective counts for twenty-five consecutive lots, a study in which several inspectors judged the same retained units against an agreed answer key, and a machine-by-machine tally of defective and sound units over one common window, and one machine's inspected and defective counts either side of a change that was made to it.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether a sound/defective judgement can be relied on at all, whether the defective share has held steady across the lots, how today's level compares with what the charter commits us to, and what should be done next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
{}
```

## Submitted report (complete, identifiers removed)
# Appearance-defect project report

## Executive position

The measurement system is usable, but not unquestionable. Across the retained-unit study, agreement with the answer key was **95.83333333333334%** and the minimum appraiser-to-key kappa was **0.6938775510204082**. The overall Fleiss kappa was **0.8391139609443309**. Continue using the system, with calibration and adjudication for difficult classifications rather than treating every judgement as error-free.

The lot archive contains **25** lots, **171** defects, and **125000** inspected units. The aggregate level is **1368 DPMO**, compared with the **1500 DPMO** charter. The one-proportion test returned **p = 0.22785821528181183** and **z = -1.2058943867138037**: the level is numerically under the commitment, but this sample does not establish that it is statistically below the commitment.

## Stability and where to act

The lot p-chart centerline is **0.001368**, with **1** out-of-control lot. The runs-test p-value is **0.39376863464299294**, so there is no computed evidence of a sustained sequence shift; nevertheless, the exceptional lot must be investigated and its records retained.

The common-window machine tally contains **18** defects among **16000** inspections, or **1125 DPMO** overall. Machine rates were **1250 DPMO** for machine 1, **1500 DPMO** for machine 2, **1000 DPMO** for machine 3, and **750 DPMO** for machine 4. Machine 2 is therefore the first equipment comparison to investigate because it is at the charter boundary.

Reject categories total **240**. Loose end contributes **153**, or **63.75%**, making it the dominant observed cause. The FMEA maximum RPN is **392**, belonging to stain; the other computed RPNs were loose end **56**, soft spot **144**, off-weight **96**, and seam split **160**. The immediate improvement work should attack loose-end occurrence while separately reducing the high-risk stain scenario.

## What changed and what it achieved

The change trial compared **4000** inspected units before the change with **4000** after it. Defects fell from **6** (**1500 DPMO**) to **3** (**750 DPMO**): an observed reduction of **750 DPMO**, or **50.0%**. The two-proportion result was **z = 1.0005629750547598** with **p = 0.31703813758955945**. Treat the change as promising and retain it, but do not claim confirmed causal improvement from this trial alone; repeat the comparison with a larger, predefined sample.

## Control plan and next actions

The post-change monitoring record has **20** subgroups, **91** defects, and **93900** inspected units, giving **969.1160809371672 DPMO**. Its variable-size p-chart centerline is **0.0009691160809371672** and has **0** out-of-control signals. The calculated upper-limit range is **2135.9488703872507** to **2619.2668367991055 DPMO**, while the lower-limit range is **0.0** to **0.0 DPMO**.

1. Investigate the single exceptional lot, with special attention to loose-end conditions and machine 2.
2. Standardize the change and verify that operators can recognize the answer-key categories; review disagreements during calibration.
3. Put loose-end prevention first, and assign a separate action to the stain failure mode because its RPN is **392**.
4. Continue the variable-size p-chart. Escalate any future signal, and preserve subgroup size, defect count, machine, category, and change-state fields.
5. Run a larger confirmatory before/after study; the current observed **50.0%** reduction is not statistically confirmed by the computed **0.31703813758955945** p-value.

Overall, the current archive is below the charter numerically, the post-change record is stable, and the main operational opportunity is concentrated in loose end. The evidence supports holding the change while investigating the exceptional lot and strengthening measurement discipline.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"agreement","appraisers":3,"trials_per_appraiser":2,"units":20},"method_id":"msa.attribute_agreement","outputs":{"agreementPct":95.83333333333334,"kappaMin":0.6938775510204082,"fleissKappa":0.8391139609443309,"meanKeyKappa":0.9135185989289333},"status":"success","decision":"Agreement with the answer key is high overall, but the minimum appraiser-key kappa is lower than the pooled agreement; use the measurement system with routine alignment and review."}
{"step_id":2,"inputs_digest":{"batch":"lots","lots":25,"subgroup_size_each":5000},"method_id":"basic.descriptive_summary","outputs":{"mean":1368.0,"median":1000.0,"stdDev":1532.2454111531872,"totalDefects":171,"totalInspected":125000,"targetDpmo":1500.0},"status":"success","decision":"The aggregate defective level is below the charter level."}
{"step_id":3,"inputs_digest":{"batch":"lots","lots":25,"defectives":171,"inspected":125000,"target_rate":0.001},"method_id":"basic.one_proportion","outputs":{"pValue":0.22785821528181183,"zStatistic":-1.2058943867138037,"dpmo":1368.0},"status":"success","decision":"The observed aggregate rate is not significantly different from the charter rate in this test."}
{"step_id":4,"inputs_digest":{"batch":"lots","lots":25,"subgroup_size_each":5000},"method_id":"control_chart.p","outputs":{"centerLine":0.001368,"outOfControlCount":1,"ucl":0.0029361299170668227,"lcl":0.0,"runsPValue":0.39376863464299294,"runs":11},"status":"success","decision":"The lot sequence shows no runs-test evidence of a systematic shift, but one lot signals beyond the three-sigma p-chart limit and requires investigation."}
{"step_id":5,"inputs_digest":{"batch":"machines","machines":4,"common_window":true},"method_id":"capability.binomial","outputs":{"processZ":1.2256644647170392,"avgP":0.001125,"totalDefects":18,"totalInspected":16000,"machine1Dpmo":1250.0,"machine2Dpmo":1500.0,"machine3Dpmo":1000.0,"machine4Dpmo":750.0},"status":"success","decision":"Machine 2 is highest at the charter boundary; machine 4 is lowest in the common window."}
{"step_id":6,"inputs_digest":{"batch":"candidates","categories":5,"total_category_count":240},"method_id":"quality.pareto","outputs":{"topCategoryPct":63.75,"totalCount":240,"topCategoryCount":153},"status":"success","decision":"Loose end is the dominant reject category and should be the first improvement focus."}
{"step_id":7,"inputs_digest":{"batch":"failure_modes","failure_modes":5},"method_id":"quality.fmea_rpn","outputs":{"maxRpn":392,"looseEndRpn":56,"softSpotRpn":144,"offWeightRpn":96,"seamSplitRpn":160,"stainRpn":392},"status":"success","decision":"Stain has the maximum computed RPN and should receive risk-reduction attention alongside the dominant loose-end count."}
{"step_id":8,"inputs_digest":{"batch":"after_change","before_defects":6,"before_inspected":4000,"after_defects":3,"after_inspected":4000},"method_id":"basic.two_proportions","outputs":{"pValue":0.31703813758955945,"zStatistic":1.0005629750547598,"beforeDpmo":1500.0,"afterDpmo":750.0,"absoluteReductionDpmo":750.0,"relativeReductionPct":50.0},"status":"success","decision":"The change trial shows an observed reduction, but the available comparison does not establish statistical significance."}
{"step_id":9,"inputs_digest":{"batch":"sustaining","subgroups":20},"method_id":"control_chart.p","outputs":{},"status":"failed","decision":"Initial computation failed due to a coding syntax error; it was rerun successfully in the next step."}
{"step_id":10,"inputs_digest":{"batch":"sustaining","subgroups":20,"variable_subgroup_sizes":true,"total_defects":91,"total_inspected":93900},"method_id":"control_chart.p","outputs":{"centerLine":0.0009691160809371672,"outOfControlCount":0,"dpmo":969.1160809371672,"uclMinDpmo":2135.9488703872507,"uclMaxDpmo":2619.2668367991055,"lclMinDpmo":0.0,"lclMaxDpmo":0.0},"status":"success","decision":"The post-change monitoring record is stable by the calculated variable-size p-chart and is below the charter level."}
```

## Submitted route declarations
```json
[{"point":"measurement_system","chosen_branch":"proceed_with_caution","observed":{"agreementPct":95.83333333333334,"kappaMin":0.6938775510204082}},{"point":"lot_level","chosen_branch":"investigate_special_cause_and_continue","observed":{"outOfControlCount":1,"runsPValue":0.39376863464299294}},{"point":"change_evidence","chosen_branch":"retain_change_but_confirm","observed":{"relativeReductionPct":50.0,"pValue":0.31703813758955945}},{"point":"sustaining","chosen_branch":"continue_monitoring","observed":{"outOfControlCount":0,"dpmo":969.1160809371672}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
