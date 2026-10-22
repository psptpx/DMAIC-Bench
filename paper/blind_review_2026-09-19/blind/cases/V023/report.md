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
