# Blind item V023

Focal assessment: Baseline defect-rate chart stability, business performance, and next steps.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team in a shared-services centre. The response commitment written into the customer contract is missed too often; internally we require that no more than 5% of tickets breach it. Twenty-five consecutive periods of ticket volume and breach counts have been exported. The archive also holds a study in which several reviewers each judged the same tickets against a known answer key, and a summary of two teams' intake and breaches over one common window.

## 2. What you are asked to do

Work through the batches the data steward can release and say where this project stands: whether a breach judgement can be relied on at all, whether the breach share has been steady across the periods, how far today's level sits from the internal requirement, and what should be done about it next. Every number in your report must come from a computation you ran on this task; where nothing was computed, draw no conclusion.


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
# Response-Time Breach Project - Status Report

## Bottom line

The breach rate is currently running at 3.52%, below the internal 5% requirement, and it has been stable across the 25 periods examined - no period fell outside the statistical control limits of a p-chart (UCL = 7.43%, LCL = 0%, center line = 3.52%). There is no statistical evidence that this is drifting or that either of the two compared teams is a special cause of breaches.

However, the study that judges whether a ticket breached or not - the measurement system itself - has a known reliability gap that limits how much confidence we can place in every number below.

## 1. Can a breach judgement be relied on?

Three reviewers each classified the same 20 tickets, twice, against a known correct answer (the attribute agreement study).

- Minimum Cohen's kappa (any single appraiser vs. the answer key, pooling both trials): 0.833. This clears the commonly used 0.7 acceptable floor.
- Overall agreement - all three appraisers, both trials, matching the answer key on the same ticket - was only 80% (16 of 20 tickets), below the usual 90% comfort threshold quality teams look for before trusting a pass/fail call unreservedly.

Conclusion: the measurement system is usable, but not fully reliable. Roughly one ticket in five had at least one reviewer or one trial disagree with the correct call. Any breach count derived from this classification process - including the 25-period series below - carries that same margin of uncertainty. We did not re-derive the per-period breach counts from raw ticket-level judgements (that data was not requested), so this is a caveat on the whole report rather than a correction we can apply.

## 2. Has the breach share been steady?

Twenty-five periods, 200 tickets each (5,000 tickets total, 176 breaches):

- Center line (p-bar): 3.52%
- 3-sigma control limits: LCL = 0%, UCL = 7.43%
- Periods outside these limits: 0 of 25

No period signals a special-cause spike or drop. The process is behaving as a stable system around 3.52%.

## 3. How far is today's level from the 5% requirement?

- Average breach rate: 3.52%, versus the 5% requirement - 1.48 percentage points of margin.
- Capability check (binomial): process Z = 1.14 sigma above the target threshold, meaning the average sits comfortably on the good side of the line.
- Statistical test of whether 3.52% is actually different from 5% (one-proportion test): z = -0.96, p = 0.337. This is not statistically significant - with the volume observed (5,000 tickets), we cannot rule out that the true underlying rate is at or near 5%. The point estimate is favorable, but the sample does not yet let us assert with confidence that we are durably below the requirement.

## 4. Is one team driving the breaches?

Team 1: 22 breaches / 600 tickets (3.67%). Team 2: 16 breaches / 600 tickets (2.67%).

Two-proportions test: z = 0.989, p = 0.323. The difference between teams is not statistically significant. This comparison gives no evidence of a team-specific root cause; whatever is driving the roughly 3.5% baseline breach rate appears to be common to both teams, not isolated to one.

## What this means and what to do next

- Where things stand: the breach rate (3.52%) is below the 5% contractual requirement and stable, but the margin is not statistically proven to be real at current sample sizes, and the measurement system that classifies breaches has a reliability gap (80% overall agreement).
- What's causing it: no root cause was isolated. The team-to-team comparison ruled out one candidate (which team handled the ticket) as a significant driver. No other candidate causes were investigated in this round because no further process-level data was requested.
- What was changed: nothing has been changed yet in this project cycle. This is a measure/analyze-stage status check, not a post-improvement report.
- What should happen next:
  1. Tighten the breach-classification criteria or add reviewer calibration and training before trusting the breach count for control decisions - the 80% overall agreement is the binding constraint on confidence in every other number here.
  2. Keep collecting periods on the p-chart; current data supports stable, but 25 periods at 200 tickets is not enough volume to statistically confirm the average is below 5% (p = 0.337 on that test). Continue monitoring rather than declaring victory.
  3. Since the team comparison ruled out team identity as a driver, look at other candidate causes (ticket category, time of day, complexity) if this project continues - none of that data was made available in this batch and is not covered by this report.

## Data gaps

No batch requested in this project was refused as unavailable (denied). The charter and target, reviewer judgement study, 25-period ticket volume and breach series, and two-team comparison were all obtained and used above. Any conclusion beyond what is stated here (for example root causes other than team identity, or day-to-day drivers) is out of scope because that data was not part of this release and was not fabricated.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"agreement","n_appraisers":3,"n_parts":20,"n_trials":2},"method_id":"msa.attribute_agreement","outputs":{"kappaMin":0.8333333333333334,"agreementPct":0.8},"status":"success","decision":"kappaMin above 0.7 floor but overall agreement only 80pct; judgement usable but not fully reliable"}
{"step_id":2,"inputs_digest":{"batch":"subgroups","n_periods":25,"subgroup_size":200},"method_id":"control_chart.p","outputs":{"centerLine":0.0352,"outOfControlCount":0},"status":"success","decision":"no periods outside 3-sigma limits; breach share stable across 25 periods"}
{"step_id":3,"inputs_digest":{"batch":"subgroups","n_periods":25,"subgroup_size":200},"method_id":"capability.binomial","outputs":{"processZ":1.1357604308874591,"avgP":0.0352},"status":"success","decision":"average breach rate 3.52pct below 5pct requirement, 1.14 sigma margin"}
{"step_id":4,"inputs_digest":{"batch":"subgroups","n_periods":25,"total_n":5000,"total_events":176},"method_id":"basic.one_proportion","outputs":{"pValue":0.33687868440515745},"status":"success","decision":"difference between 3.52pct observed and 5pct target not statistically significant at this sample size"}
{"step_id":5,"inputs_digest":{"batch":"root_cause","n1":600,"n2":600,"x1":22,"x2":16},"method_id":"basic.two_proportions","outputs":{"zStatistic":0.9891155080061562,"pValue":0.3226066309190325},"status":"success","decision":"no statistically significant difference between the two teams breach rates"}
```

## Submitted route declarations
```json
[{"point":"measurement_system_reliability","chosen_branch":"usable_with_caution","observed":{"kappaMin":0.8333333333333334,"agreementPct":0.8}},{"point":"process_stability","chosen_branch":"stable","observed":{"outOfControlCount":0,"centerLine":0.0352}},{"point":"team_comparison","chosen_branch":"no_significant_difference","observed":{"pValue":0.3226066309190325}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
