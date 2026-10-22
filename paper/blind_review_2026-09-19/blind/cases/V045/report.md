# Ticket-breach measurement, capability, and next-step decision

## Executive conclusion

The breach judgement itself is usable: the attribute study found strong agreement with the known answer key and strong repeat agreement. The ticket process, however, is stable but not capable of meeting the internal requirement. Across the supplied periods, its weighted breach share was above the target by a material margin. The most recent period happened to land exactly on target, but it is only one stable-looking period and must not be treated as an improvement.

No operational root cause can be concluded from the released evidence. The team summary shows a numerical difference, but its computed evidence is not strong enough to identify a cause. No process-fact data were provided to explain the difference. Additionally, no intervention or post-change data were supplied, so nothing was changed in this project and no change effect can be claimed.

## Can the breach judgement be relied on?

The measurement study used three reviewers, each making repeat judgements, for 120 total judgements. Exact agreement with the answer key was 96.66666666666667; the minimum reviewer kappa was 0.8989898989898989; and the minimum repeat agreement was 90.0. Appraiser-specific agreement was 95.0, 97.5, and 97.5.

On those computed results, the breach measurement is reliable enough to use for this project. Measurement error is not so large that the process conclusion should be dismissed.

## Has the breach share been steady?

The period series contained 25 periods and 5620 tickets. The ordinary p chart had 0 out-of-control points around a center line of 0.06174377224199288. A Laney p chart, which accounts for the observed dispersion, had 0.8651131315864975 dispersion factor and also found 0 out-of-control points.

The direct equal-share goodness-of-fit test gave chi-square 14.797622478386167 on 24 degrees of freedom and p-value 0.9265407694281627. The time correlation was 0.0862274343491142 with p-value 0.6819311416466498, and the runs test gave 10 runs with p-value 0.15435475680586547. Period rates ranged from 0.03666666666666667 to 0.08333333333333333, with unweighted mean 0.06075, median 0.0625, and sample standard deviation 0.013268069440075546.

Together, these analyses support a steady, common-cause process rather than a sequence with clear trends or isolated special causes.

## How far is today from the requirement?

The target is 0.05. The pooled data contained 347 breaches among 5620 tickets, giving weighted average breach share 0.06174377224199288. At the same volume, target-allowed 281 breaches would correspond to the target; the observed excess was 66, or 1.1743772241992876 percentage points above target. A reduction of 19.020172910662826% in breaches would be needed to move the pooled result to target. The binomial capability assessment gave process Z 4.039512654220945 and one-sided p-value 5.157071390566437e-05, so the observed excess is not explained as ordinary sampling variation around the target.

The latest period is 25, with 10 breaches among 200 tickets: 0.05. Its gap to target is 0.0. That single on-target period is not evidence of a sustained shift.

## What is causing it?

The supplied data do not support an operational cause. Team A had 40 breaches in 600 tickets (0.06666666666666667), while Team B had 26 in 600 (0.043333333333333335), a difference of 0.02333333333333333. The two-proportion test gave 1.7727200782610344 and p-value 0.07627510236570058, which does not establish a team difference strong enough to act on. The process owner supplied no matching operational process fact, so the causal conclusion stops there. It would be unsafe to label team mix, staffing, volume, or any other practice as the cause without those data.

The stability result points instead to a systemic common-cause issue. The next work should collect ticket-level drivers—receipt and due timestamps, category, priority, routing, staffing, queue wait, work time, and commitment type—and relate them to breach status. That is an analysis plan, not an assumed cause.

## What was changed and what did it achieve?

Nothing was changed within the supplied project window. No action log, intervention timestamp, or post-intervention period data was released. Consequently, no improvement, deterioration, or holding effect can be quantified. Treating the latest on-target period as an intervention effect would be unsupported.

## Recommended next actions and control

- Treat the elevated pooled rate as a stable common-cause system and investigate the end-to-end workflow rather than reacting to individual period points that the control charts did not flag.
- Collect the missing ticket-level process facts and rerun the root-cause analysis before selecting a countermeasure. Do not promote the team comparison to a causal finding on the current evidence.
- Pilot a specific process change with pre-defined entry and exit comparisons; until those post-change data exist, claim no benefit.
- Hold the process with the p chart and the internal target, reviewing new periods as they arrive. Investigate genuine control-chart signals and persistent inability to meet the target, not ordinary period-to-period variation.
- Retain the attribute measurement check as part of routine governance so the breach definition remains dependable.

The immediate business position is therefore: measurement is trustworthy, performance is steady but above requirement, and the project must now move from descriptive monitoring to ticket-level causal analysis before claiming or announcing a fix.
