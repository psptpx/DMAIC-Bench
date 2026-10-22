# Blind item V021

Focal assessment: The second (repeat) attribute agreement study and subsequent actions.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

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
# Project Report: Final Inspection Accept/Reject Reliability and Reject Share

## Data obtained
All requested plant data batches were released and used: project charter/required level, the first inspector judgement study against the answer key, disagreement tally by reject category, the second inspector study after criteria rewrite, per-lot inspected and rejected counts, and one window of placed and rejected counts for each placement head.

## 1. Can an accept/reject call be relied on?
Before the criteria rewrite, the first retained-board inspector study had an overall agreement of 81.7% with the answer key and a minimum inspector-vs-key kappa of 0.300. This is too weak for reliable final-inspection accept/reject calls.

After the accept/reject criteria were rewritten, the second retained-board study had an overall agreement of 79.2% and a minimum kappa of 0.423. Agreement percentage did not improve significantly (two-proportion test p = 0.6256, z = 0.4880). The lowest kappa improved, but the inspection system still cannot be relied on as demonstrated.

## 2. What had to happen before the call could be trusted?
The initial MSA showed that the accept/reject criterion as written was not producing consistent inspector calls. The criteria were rewritten and a second retained-board study was run. Although the lowest kappa improved, the improvement in agreement rate was not statistically significant. Therefore, the current evidence says the call still cannot be relied on; further revision and retraining are needed.

## 3. Has the reject share held steady across the lots?
The 25-lot record contains 10000 inspected boards and 125 rejected boards, giving an average reject share of 1.25%. A p-chart for constant subgroup size 400 has center line 1.25% and upper control limit 2.92%. One lot falls above the upper control limit (out-of-control count = 1). The Laney-P adjusted sigma_z is 1.047, indicating over-dispersion, and the adjusted chart still flags one lot. The reject share has not held steady across the lots; one high lot needs investigation.

## 4. How does today's level compare with the required level?
The required reject level is 2.0%. In the recent placement-head window, the combined head reject rate was 1.750% (one-proportion test against 2%: p = 0.1666). The point estimate is below 2%, but the result is not statistically significantly below the required level.

Head 1 rejected 56 out of 3000 (1.87%), and Head 2 rejected 49 out of 3000 (1.63%). The difference between heads is not statistically significant (two-proportion p = 0.4907).

## 5. What should be done next?
- Investigate the single out-of-control lot in the p-chart before accepting the current process as stable.
- Focus corrective action on the largest disagreement category, insufficient solder, which accounts for 46.67% of inspector-vs-key disagreement items.
- Rework the accept/reject inspection criteria and training, then rerun an MSA. The current second study still does not demonstrate a reliable accept/reject call.
- Monitor the placement heads with control charts and continue using the 2% required reject share as the business limit.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"study_1","n_appraisers":3,"n_trials_per_appraiser":2,"n_items":20},"method_id":"msa.attribute_agreement","outputs":{"agreementPct":81.66666666666667,"kappaMin":0.30000000000000004},"status":"success","decision":"Initial inspector agreement was too weak to rely on accept/reject calls."}
{"step_id":2,"inputs_digest":{"batch":"study_2","n_appraisers":3,"n_trials_per_appraiser":2,"n_items":20},"method_id":"msa.attribute_agreement","outputs":{"agreementPct":79.16666666666666,"kappaMin":0.423076923076923},"status":"success","decision":"After criteria rewrite, the lowest kappa improved but overall agreement was essentially unchanged."}
{"step_id":3,"inputs_digest":{"batch":"study_1_vs_study_2","x_agree_1":98,"n_total_1":120,"x_agree_2":95,"n_total_2":120},"method_id":"basic.two_proportions","outputs":{"pValue":0.6255661807026858,"zStatistic":0.4879769318876249},"status":"success","decision":"There was no statistically significant change in agreement rate after the criteria rewrite."}
{"step_id":4,"inputs_digest":{"batch":"disagreements","n_categories":5},"method_id":"quality.pareto","outputs":{"topCategoryPct":46.666666666666664},"status":"success","decision":"Insufficient solder is the leading category of inspector disagreement."}
{"step_id":5,"inputs_digest":{"batch":"lots","n_subgroups":25,"subgroup_size":400},"method_id":"control_chart.p","outputs":{"centerLine":0.0125,"outOfControlCount":1,"upperControlLimitP":0.029165364532466733,"lowerControlLimitP":0},"status":"success","decision":"One lot falls above the upper control limit, so the reject share has not held steady across these 25 lots."}
{"step_id":6,"inputs_digest":{"batch":"lots","n_subgroups":25,"subgroup_size":400},"method_id":"control_chart.laney_p","outputs":{"sigmaZ":1.0472892694790117,"upperControlLimitP":0.029953457446808513,"lowerControlLimitP":0,"outOfControlCount":1},"status":"success","decision":"Laney-P sigma_z is greater than 1, indicating over-dispersion; one lot remains outside the adjusted control limits."}
{"step_id":7,"inputs_digest":{"batch":"lots","total_inspected":10000,"total_defects":125},"method_id":"capability.binomial","outputs":{"avgP":0.0125,"processZ":2.2414027276049464,"totalInspected":10000,"totalDefects":125},"status":"success","decision":"Average reject share is below the required 2%, but process variation still breaches the upper control limit."}
{"step_id":8,"inputs_digest":{"batch":"heads","events_combined":105,"trials_combined":6000,"p0":0.02},"method_id":"basic.one_proportion","outputs":{"pValue":0.16660099386519844,"zStatistic":-1.3832083379312197,"requiredRejectShare":0.02},"status":"success","decision":"Today's combined placement-head reject rate is below 2%, but not statistically significantly below the required level."}
{"step_id":9,"inputs_digest":{"batch":"heads","events1":56,"trials1":3000,"events2":49,"trials2":3000},"method_id":"basic.two_proportions","outputs":{"pValue":0.490705562532215,"zStatistic":0.6891870541365993},"status":"success","decision":"There is no statistically significant difference between the two placement heads."}
```

## Submitted route declarations
```json
[{"point":"required_reject_share","chosen_branch":"use 0.02 from project charter","observed":{"required_reject_share":0.02}},{"point":"initial_accept_reject_reliability","chosen_branch":"criteria_rewrite_and_run_second_study","observed":{"study1_kappaMin":0.30000000000000004}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
