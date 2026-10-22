# Blind item B025

Focal assessment: Baseline defect-rate chart stability, business performance, and next steps.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team on an electronic-assembly line. Boards are accepted or rejected by eye at final inspection, and the line is required to hold the reject share at or below 2%. The archive holds the inspected and rejected counts for twenty-five consecutive lots, a study in which several inspectors judged the same retained boards against an agreed answer key, a tally of the items those inspectors called differently from the key broken out by the category the item was rejected under, a second study run on retained boards after the accept/reject criteria were rewritten, and one window's rejected and placed counts for each of the two placement heads.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether an accept/reject call can be relied on, what had to happen before it could be, whether the reject share has held steady across the lots, how today's level compares with what the line is required to hold, and what should be done next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
# Visual-inspection reject project: current position

## Executive conclusion

The inspection calls can now be used with reasonable confidence on evidence from the retained-board studies, but they are not error-free and should continue to be checked. Before that reliance was justified, the accept/reject criteria had to be rewritten and the retained-board study repeated. Agreement with the answer key rose from **95.833333%** (**115** correct calls out of **120**) to **97.5%** (**117** out of **120**), a gain of **1.666667 percentage points**. The minimum appraiser kappa was **0.898990** initially and **0.875000** after rewriting, so the evidence supports an improvement in pooled observed agreement, not an improvement in every agreement statistic.

The reject share has **not held steady** across the archived lots. The p-chart center line was **0.0179**, with limits of **0** and **0.037788**. It flagged **1** lot: lot **13**, whose reject share was **0.095**. Special-cause variation must therefore be addressed before claiming stable capability.

Across the full archive, **179** rejects among **10000** inspections gave a share of **0.0179**, numerically **0.0021** below the required **0.02**. Its exact confidence interval was **0.015392** to **0.020694**, and the exact two-sided test against the requirement gave **p = 0.142918** at significance level **0.05**. Thus the archive does not establish a statistically different long-run level, and its instability further limits that aggregate comparison. The latest lot's share was **0.025**, which is above the required **0.02** even though it remained inside the historical p-chart limit. Today/latest-lot performance is therefore not at the required level.

## Measurement-system findings

In the initial study, the three appraisers' agreement with the key was **95%**, **95%**, and **97.5%**; minimum within-appraiser repeatability was **90%**. The mismatch tally contained **90** calls across **5** reject categories. “Insufficient solder” accounted for **46**, or **51.111111%**, making its visual criterion the priority for clarification. This tally concerns disagreement with the answer key; it does **not** prove that insufficient solder caused most production rejects.

After the criteria rewrite, appraiser agreement with the key was **97.5%**, **100%**, and **95%**, while minimum repeatability remained **90%**. This confirms high retained-board agreement after the intervention, but continued audits are warranted because disagreement remained and the minimum kappa did not improve.

The archive confirms that criteria were rewritten, but no process fact was available describing the exact wording, examples, training, or rollout. Consequently, this report cannot claim which specific edit produced the observed gain.

## Process and placement-head findings

The descriptive binomial calculation from the archive gave average reject share **0.0179** and process Z **2.099192**. It must not be presented as demonstrated stable capability because the control chart found special-cause variation.

For the placement-head window, head 1 had **56** rejects from **3000** placements, a share of **0.018667**; head 2 had **49** from **3000**, a share of **0.016333**. The difference was **0.002333**, with confidence limits **-0.004302** to **0.008969**. The pooled two-proportion test gave **z = 0.689187** and **p = 0.490706** at significance level **0.05**. This window does not support singling out either head as having a different reject share.

No documented assignable cause for the flagged lot was available from the process owner, and no documented reaction plan or existing sustainment control was available. The causal conclusion therefore stops at identifying the statistical signal; a cause must not be guessed.

## Recommended next actions

1. Quarantine and review the records and retained material associated with the flagged lot. Check material, recipe, setup, inspection conditions, rework, and timestamps, then record the verified assignable cause if one is found.
2. Keep the rewritten visual standard at the point of inspection, with explicit boundary examples for insufficient solder. Preserve revision control and record inspector training; these are recommendations, not claims about controls already in place.
3. Repeat blinded retained-board agreement checks periodically and after any standard, product, lighting, or staffing change. Track both agreement with the key and within-appraiser repeatability.
4. Continue the lot-by-lot p chart. Define a reaction plan requiring containment and investigation whenever a point crosses a control limit; do not recalculate limits merely to absorb a special cause.
5. After the flagged lot has been investigated and enough subsequent stable lots are collected, establish a stable baseline and then reassess performance against the required reject share.
6. Do not adjust a placement head based on this window alone. Continue head-tagged collection and re-test if a practical difference emerges or engineering evidence points to a head-specific mechanism.

## Bottom line

Measurement agreement is now high enough to support disciplined monitoring, following the criteria rewrite and repeat study. However, the production process is not demonstrated to be steady, and the latest lot is above the requirement. The immediate priority is special-cause investigation and a documented control plan, followed by stable-data confirmation of sustained performance.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"study_1","appraisers":3,"trials_per_appraiser":2,"retained_boards":20,"calls":120},"method_id":"msa.attribute_agreement","outputs":{"agreementPct":95.83333333333334,"kappaMin":0.8989898989898989,"correctCalls":115,"totalCalls":120,"appraiser1AgreementPct":95.0,"appraiser2AgreementPct":95.0,"appraiser3AgreementPct":97.5,"minimumRepeatabilityPct":90.0},"status":"success","decision":"Initial retained-board calls showed high agreement with the answer key, but discrepancies justified clarifying the criteria before relying on inspection for improvement decisions."}
{"step_id":2,"inputs_digest":{"batch":"disagreements","categories":5,"tallied_disagreements":90},"method_id":"quality.pareto","outputs":{"topCategoryPct":51.111111111111114,"topCategoryCount":46,"totalTallied":90,"categoryCount":5},"status":"success","decision":"Insufficient solder was the leading category among calls that differed from the key, making that criterion the first clarification priority; this is not evidence that it caused most production rejects."}
{"step_id":3,"inputs_digest":{"batch":"study_2","appraisers":3,"trials_per_appraiser":2,"retained_boards":20,"calls":120},"method_id":"msa.attribute_agreement","outputs":{"agreementPct":97.5,"kappaMin":0.8749999999999999,"correctCalls":117,"totalCalls":120,"agreementGainPctPoints":1.6666666666666572,"appraiser1AgreementPct":97.5,"appraiser2AgreementPct":100.0,"appraiser3AgreementPct":95.0,"minimumRepeatabilityPct":90.0},"status":"success","decision":"After criteria were rewritten, pooled agreement with the key increased, supporting use of the calls with continued verification; minimum kappa did not increase."}
{"step_id":4,"inputs_digest":{"batch":"lots","groups":25,"subgroup_size":400},"method_id":"control_chart.p","outputs":{"centerLine":0.0179,"outOfControlCount":1,"lowerControlLimit":0,"upperControlLimit":0.03778820693275289,"flaggedLot":13,"flaggedLotShare":0.095,"latestLotShare":0.025,"requiredRejectShare":0.02,"totalInspected":10000,"totalRejected":179},"status":"success","decision":"The reject share was not steady across lots because one lot exceeded the three-sigma upper control limit."}
{"step_id":5,"inputs_digest":{"batch":"lots","rejected":179,"inspected":10000},"method_id":"basic.one_proportion","outputs":{"pValue":0.14291818833749834,"observedShare":0.0179,"requiredRejectShare":0.02,"difference":-0.002100000000000001,"confidenceIntervalLower":0.015392459771213096,"confidenceIntervalUpper":0.020693613394785426,"significanceLevel":0.05},"status":"success","decision":"The aggregate share was numerically below the requirement, but the two-sided exact test did not establish a difference and instability prevents treating the aggregate as a stable current capability."}
{"step_id":6,"inputs_digest":{"batch":"lots","rejected":179,"inspected":10000},"method_id":"capability.binomial","outputs":{"avgP":0.0179,"processZ":2.099191761058102},"status":"success","decision":"A descriptive binomial process Z was computed from the aggregate reject share, but it is not a demonstration of stable capability because the p chart signaled special-cause variation."}
{"step_id":7,"inputs_digest":{"batch":"heads","head1_placed":3000,"head2_placed":3000},"method_id":"basic.two_proportions","outputs":{"pValue":0.490705562532215,"zStatistic":0.6891870541365993,"head1RejectShare":0.018666666666666668,"head2RejectShare":0.01633333333333333,"shareDifference":0.0023333333333333366,"differenceCILower":-0.004302241555378544,"differenceCIUpper":0.008968908222045217,"head1Rejected":56,"head2Rejected":49,"head1Placed":3000,"head2Placed":3000,"significanceLevel":0.05},"status":"success","decision":"The available window does not provide evidence that the two placement heads have different reject shares."}
```

## Submitted route declarations
```json
[{"point":"measurement_before_process_analysis","chosen_branch":"assess initial inspector agreement before interpreting reject data","observed":{"agreementPct":95.83333333333334,"kappaMin":0.8989898989898989}},{"point":"criteria_response","chosen_branch":"prioritize criterion clarification and evaluate the rewritten criteria","observed":{"topCategoryPct":51.111111111111114}},{"point":"stability_before_capability_claim","chosen_branch":"treat process as unstable and avoid a capability claim","observed":{"outOfControlCount":1}},{"point":"placement_head_followup","chosen_branch":"do not single out a head from this window","observed":{"pValue":0.490705562532215}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
