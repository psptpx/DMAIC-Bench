# Display brightness at end of line - project status

Task: `[TASK]`. Accepted range 350 to 550 cd/m2 (tolerance width 200 cd/m2).
All figures below come from computations run on this task and recorded in `/workspace/trace.json`.

## Headline

The readings can be trusted. The line cannot. Brightness stepped up by **73.83 cd/m2** partway
through the run and now sits at **523.74 cd/m2**, hard against the 550 upper limit, with
**Cpk 0.4839** and **2 of the last 25 units already measured above 550**. The problem is
centring, not scatter. No improvement has yet been made or verified, because the plant holds no
data for those phases.

## 1. Can the recorded readings be relied on? Yes

Crossed gage R&R by ANOVA on the archive study: 3 operators, 10 units, 3 repeat readings each
(90 readings). The part-by-operator interaction was not significant (p = 0.160203), so it was
pooled into repeatability in the usual way.

| Source | sd (cd/m2) | % of study variation |
|---|---|---|
| Repeatability (the gauge itself) | 4.2942 | 12.8011 |
| Reproducibility (operator to operator) | 2.6993 | 8.0466 |
| **Total gage R&R** | **5.0721** | **15.1201** |
| Unit to unit | 33.1597 | - |
| Total | 33.5454 | - |

Total gage R&R is **15.1201 %** of study variation and **15.2163 %** of the 200 cd/m2
tolerance, with **9.2182** distinct categories. That is inside the customary 30 % limit and
above the 5-category minimum, so the end-of-line reading is fit to judge units and to drive
process decisions. Operators do differ detectably (p = 0.0000149671) but the effect is small
next to unit-to-unit spread, and it does not change the verdict. Note this places a floor on
what you can see: any real shift of the order of the 5.0721 cd/m2 gauge sd will be hard to see unit by unit.

This verdict was declared back to the steward as `grr_pct = 15.12`, which released the
production record.

## 2. How has the line behaved over the run? It broke into two levels

50 units in production order. Overall mean **486.826 cd/m2**, sd **43.052**, spanning
**401.6** to **556.9**, skewness **-0.2213**.

The run is not stable, and three independent checks agree:

* **Individuals chart**: centre line 486.826, limits 412.6944 to 560.9576 (within-unit sigma
  24.7105 from a mean moving range of 27.8735). **46 of 50 points are flagged** - not scattered
  specials, but long stretches sitting on one side of the centre line. The moving-range chart
  flags only **1** point, at the step itself, which says the unit-to-unit noise never changed.
* **Runs test about the median**: **6 runs observed against 26.0 expected**, z = -5.7155,
  p = 0.000000010940. The order of the readings is not random.
* **Step localisation**: the split that best separates the run falls at **unit 25**. The first
  25 units average **449.912** (sd 25.1022); the last 25 average **523.74** (sd 17.7544). The
  difference is **73.828 cd/m2**, t = -12.006, p = 0.00000000000000046.

Spread did not change across the step (Levene p = 0.229194). Each half is normal on its own
(Anderson-Darling p = 0.897990 before, p = 0.431300 after), which is why the pooled run fails
normality (p = 0.023433) - it is a mixture of two stable levels, not a heavy-tailed process.
So normal capability is valid per regime, and only per regime.

## 3. Where does brightness sit against its accepted range today?

| Scope | Mean | Cp | Cpk | Pp | Ppk | Units outside 350-550 |
|---|---|---|---|---|---|---|
| Units 0-24 (before the step) | 449.912 | 1.0937 | 1.0927 | 1.3279 | 1.3267 | 0 |
| Units 25-49 (**current**) | 523.74 | 1.8428 | 0.4839 | 1.8775 | 0.493 | 2 above 550 |
| Whole run (mixed, for reference only) | 486.826 | 1.349 | 0.8522 | 0.7743 | 0.4891 | 2 above 550 |

Read the current row. **Cp 1.8428 against Cpk 0.4839** is the whole diagnosis in two numbers:
the line is tight enough to hold this tolerance comfortably, but it is aimed in the wrong place.
At the present centre, **6.956 %** of output is predicted above the 550 limit, and observation
bears that out with 2 overshoots in the last 25 units. The current level is a long way from the
450 cd/m2 mid-range point (t = 20.7667, p = 0.000000000000000076).

The whole-run Ppk of 0.4891 should not be quoted to a customer as this line's capability. It
averages two different processes and forecasts neither.

Worth noting against the original complaint: set makers reported units looking **dim**. Nothing
in these 50 units is anywhere near the 350 lower limit - the closest is 401.6, and predicted
fallout below 350 is negligible in both regimes. Either the dim units come from an earlier
period not in this record, or the complaint needs re-examining. This record cannot settle it.

## 4. What is causing the step - and where this report stops

I can date the change to unit 25 and size it at 73.83 cd/m2. I cannot say what caused it, and I
will not guess.

* **No improvement-trial or factor-study data exists.** I asked the data steward for it and the
  request was refused as unroutable: the only topics this project holds are the charter, the
  repeat readings and the end-of-line brightness record. No factor effects were estimated, so
  no driver of brightness is quantified here.
* **No process facts are available.** Two questions to the process owner - what changed on the
  line around unit 25, and whether the charter carries a numeric centring target or a required
  capability index - both came back with no matching fact recorded. The physical cause of the
  step is therefore unestablished by data on this run.
* **No post-change or control-phase data exists.** So there is nothing to report under "what
  was changed" and "what the change achieved": **no intervention has been made and verified
  within this project's data.** Any claim of improvement, sustained capability or control-chart
  performance after a change would be invention. The conclusion stops at diagnosis.

The abruptness of the step, with spread unchanged, is characteristic of a setpoint, recipe or
calibration change rather than gradual drift or a material spread issue - but that is a
hypothesis for the line engineers to confirm against the change log, not a finding from these
numbers.

## 5. What should be changed next

1. **Re-centre the line.** The gap to the mid-range point is what the numbers support acting on:
   the current mean is 523.74, a gap of 73.74 cd/m2 above the 450 mid-range, and pulling the centre back down converts
   Cpk 0.4839 towards the Cp 1.8428 the spread already allows. Do not attack variation first;
   Levene p = 0.229194 says variation is not what changed.
2. **Find the change at unit 25 in the change log.** Setpoint, recipe, calibration and lot
   records for that point in the run. Until this is named, the same step can recur.
3. **Quarantine and re-check the overshoots.** 2 units in the last 25 read above 550, at up to
   556.9. Gauge R&R of 5.0721 cd/m2 sd means a reading of 556.9 is genuinely over limit, not a
   measurement artefact.
4. **Hold it with an individuals-and-moving-range chart on the end-of-line reading**, with limits
   recomputed from a stable stretch after re-centring - not from this run, whose limits
   (412.6944 to 560.9576) are inflated by the step itself and would let a 73.828 cd/m2 move pass
   almost unremarked. Add a run-length rule; the runs test caught this shift far more sharply
   (p = 0.000000010940) than the 3-sigma rule did.
5. **Then verify.** Collect a post-change run and recompute stability and capability. That step
   cannot be closed out from the data now available.

## Basis and limits

* Measurement study: 90 readings, 3 operators x 10 units x 3 replicates, tolerance 200 cd/m2.
* Production record: 50 units, in order, LSL 350 / USL 550.
* Metered turns used: 2 of 20. Outside human interventions: 0.
* Batches released: 3 (charter, repeat readings, end-of-line record). Improvement, verification
  and control-phase batches: none exist.
