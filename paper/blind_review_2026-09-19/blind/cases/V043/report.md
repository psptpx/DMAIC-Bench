# Coating Thickness Project Report

**Task:** [TASK]  
**Spec:** LSL = 180 um, USL = 260 um, Target = 220 um

## 1. Can the readings be trusted?

Before looking at the process data, we checked the measurement system itself. A crossed
Gage R&R study (3 operators x 10 parts x 3 replicates) gave:

- %Study Variation = **25.6%**
- %Tolerance = **13.6%**
- Number of Distinct Categories (ndc) = **5.3**

By standard guidelines (%StudyVar under 30%, ndc of 5 or more), the gauge is acceptable.
The readings that follow can be used to draw conclusions about the process, not just the
gauge.

## 2. How has the line behaved across the run?

The 25-point, 5-piece-per-point sampling run (n=125) was charted on an Xbar-R chart.
The centerline sat at **232.3 um**, well above the 220 um target, and **20 of the 25**
subgroup averages fell outside the control limits (211.7 to 227.1 um retrospective
limits were exceeded on the high side almost throughout the back half of the run).

Breaking the run into its two visible halves confirms this is a real, one-time shift
and not noise:

- Subgroups 1-12 (first 60 pieces): mean **218.5 um**, standard deviation 6.9 um.
- Subgroups 13-25 (last 65 pieces): mean **245.0 um**, standard deviation 8.7 um.
- A two-sample t-test between the two halves gives t = -19.0, p < 1e-37 - the
  difference is not explainable by chance.
- Each half individually passes a normality check (p = 0.96 and p = 0.16 respectively),
  so the run is best read as two distinct, internally normal regimes rather than one
  unstable process. Pooling them (as a single capability study would) fails normality
  outright (p < 1e-13), which is a symptom of the mixture, not of the process itself.

Because the run is not one stable process, the capability numbers computed on the
pooled 125 readings (Cp = 1.75, Cpk = 1.21, Pp = 0.86, Ppk = 0.60) should not be quoted
as *the* capability of the line. The large gap between Cpk and Ppk is itself the tell:
potential capability (short-term, Cp/Cpk) looks fine, actual performance (long-term,
Pp/Ppk) does not, because the mean moved out from under the target mid-run.

## 3. Where did the shift come from?

The applicator (nozzle) sample gives four groups of 15 pieces, one per applicator.
A one-way ANOVA across applicators A-D gives F = 1.56, p = 0.21 - **no significant
difference between applicators**. All four run at similarly elevated means (230.5 to
234.0 um). This rules out one bad nozzle as the explanation; whatever caused the shift
affected the line as a whole, not a single piece of equipment.

**We could not go further than this.** We asked the process-owner channel directly what
caused the shift and what corrective action was taken; the steward reported it holds no
process fact matching that question and could not route it. The mechanical or
procedural root cause (e.g., a material lot, a setting drift, a shift change) is
therefore **not established by any data available to this project**, and this report
does not guess at one. The applicator ANOVA narrows the search to a line-wide cause but
does not name it.

## 4. What did the fix (whatever it was) achieve?

A monitoring record kept after some change was made shows 100 readings (20 subgroups of
5). On the Xbar-R chart:

- Centerline **219.4 um** - within 0.6 um of the 220 um target.
- **0 of 20** subgroups flagged out of control on either the Xbar or R chart.
- The data passes a normality check (p = 0.54).
- Capability: Cp = 2.32, **Cpk = 2.28**, Pp = 2.36, **Ppk = 2.33**.
- **0 of 100** pieces fell outside 180-260 um.

Cpk and Ppk are now close together (2.28 vs 2.33), which is what a stable, capable
process looks like: unlike the earlier run, there is no meaningful gap between
short-term potential and long-term actual performance.

## 5. Where this leaves the project

- The measurement system is fit for use (Gage R&R passes).
- The sampled run documented a real, statistically significant upward shift in coating
  thickness partway through, large enough to push the process out of control and drop
  long-term Ppk to 0.60.
- The shift was line-wide, not attributable to any one of the four applicators.
- **The specific mechanical or procedural root cause of the shift is not known from any
  data this project could obtain.** This is a genuine gap, not an oversight: the
  process-owner channel had no record of it.
- Whatever change was made afterward has held: the post-change monitoring record shows
  a process centered on target, in statistical control, with Cpk/Ppk above 2.2 and zero
  parts out of spec in 100 pieces sampled.

## 6. Recommendation

Continue the Xbar-R chart on the post-change data as the ongoing control plan - it is
already showing a stable, capable process (Ppk 2.33) and should continue to be read at
the same subgroup size (5) to catch any recurrence early. Because the root cause of the
original shift was never identified, the team should still document what was changed
(even informally) so that if thickness drifts upward again, the fix is not being
rediscovered from scratch. Without that record, a repeat event carries the same
investigation cost this project just paid.
