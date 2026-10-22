# Ticket Breach Rate Improvement Project - Status Report

## 1. Can a breach judgement be relied on?

We ran an attribute agreement study: 3 reviewers each judged the same 20 tickets, twice, against a known answer key.

- Overall agreement (all reviewers and both trials agreeing with each other **and** the answer key, per ticket): **70%**.
- Agreement with the answer key, and the corresponding kappa, per reviewer:
  - Reviewer 1: 90% agreement, kappa 0.76 (weakest)
  - Reviewer 2: 97.5% agreement, kappa 0.94
  - Reviewer 3: 97.5% agreement, kappa 0.93
- **kappaMin = 0.76**

A kappa below 0.90 is generally considered marginal to unacceptable for a pass/fail measurement system, and the overall multi-rater agreement of 70% is well short of what we'd want to trust breach calls on. Reviewer 1 in particular disagrees with the answer key on 1 in 10 tickets and is not even self-consistent on the same ticket across the two trials (80% repeat agreement). **Conclusion: the breach measurement system is not yet reliable enough to be taken at face value.** Any rate we report below should be read with that caveat: some of what we call a "breach" or "non-breach" is reviewer noise, not necessarily a true state of the ticket.

## 2. Has the breach share been steady across the 25 periods?

We ran a p-chart on 25 consecutive periods (200 tickets each, 5,000 tickets total).

- Center line (average breach rate, all 25 periods): **4.56%**
- Upper control limit: 8.99%, lower control limit: 0.13%
- **1 period flagged out of control: period 13**, with a breach rate of 22% (44 of 200), far above the UCL.

That single period is a special cause, not part of the routine process. Recomputing the chart on the other 24 periods:

- Center line: **3.83%**
- Out-of-control count: **0**

So apart from whatever happened in period 13, the process has been stable. That period needs a root-cause look on the shop floor (the data available to us here does not say what happened) before it can be closed out; nothing in this analysis explains it.

## 3. How far from the 5% internal requirement?

Two views, since period 13 skews the average:

- **Including period 13** (all 25 periods, 114 breaches / 5,000 tickets = 4.56%): one-proportion test against the 5% target gives p = 0.163 — not distinguishable from 5% at this scale, i.e. the special cause is large enough to erase the otherwise-favorable signal.
- **Excluding period 13** (24 periods, 92 breaches / 4,800 tickets = 3.83%): one-proportion test against 5% gives p = 0.00014 — the stable process is significantly **below** the 5% requirement.

So the process, when running normally, is comfortably inside the internal requirement (about 1.2 points of headroom, 3.83% vs 5%). The period 13 spike is what puts the reported average at risk of breaching leadership's own ceiling.

## 4. Team comparison

We were given one common window's intake and breaches for two teams: team 1 (30 breaches / 600 tickets = 5.0%) and team 2 (24 breaches / 600 tickets = 4.0%). A two-proportions test gives z = 0.84, p = 0.403 — **no statistically significant difference** between the teams over this window. We cannot point to one team as a systematic driver of the breach rate based on this data alone.

## 5. What this means for the business, and what's next

- **Where things stand**: the underlying ticket-handling process is capable of meeting the 5% requirement and, in its stable state, runs at roughly 3.8%. The 25-period average looks close to the ceiling only because of one anomalous period (period 13, 22% breach rate).
- **What's causing the risk**: an unexplained special-cause spike in period 13. We do not have shop-floor data in this study to say what happened that period (no incident log, no team split for that period) — that gap should be closed with a targeted root-cause review before we conclude anything about it.
- **What was changed / verified**: nothing has yet been changed to address period 13. Team-level performance was checked and found not to differ significantly, so a team-based intervention isn't supported by the data we have.
- **What should be done next**:
  1. Investigate period 13 specifically (shift, backlog, system outage, staffing) since our data collection here stopped at the aggregate count.
  2. Fix the measurement system before trusting the breach/no-breach call on individual tickets: retrain or recalibrate Reviewer 1, and re-run the agreement study to get kappaMin and overall agreement above an acceptable threshold (conventionally kappa ≥ 0.90, agreement ≥ 90%). Until then, small movements in the reported breach rate (e.g. the gap between 3.83% and 5%) should not be over-interpreted.
  3. Once measurement is trustworthy and period 13 is explained, hold the process on a standard p-chart (center line near 3.8%, UCL ~7.9% on the stable data) and treat any point above the UCL as a signal requiring the same kind of investigation, not as evidence the 5% requirement is at risk.

## Data gaps

All batches offered by the data steward for this task (project charter, reviewer agreement study, per-period ticket volumes, team comparison) were obtained and analysed; none were denied. The one substantive gap is explanatory data for period 13 (what happened that period), which was never offered as a batch and was not fabricated for this report.
