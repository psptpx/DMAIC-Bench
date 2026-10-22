# Blind item B013

Focal assessment: Stability of the second quality characteristic and subsequent actions.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the process team on a precision-turning cell. Two dimensions on the same part are followed: the outer diameter, accepted between 24.80 and 25.20 mm, and the wall thickness, accepted between 1.20 and 1.60 mm. Both are recorded five consecutive pieces at a time at twenty-five sampling points through one run, both on the same instrument, and the archive holds the study in which that instrument measured the same pieces several times over under several operators. Two further samples are on file: the diameter recorded separately for each of the four turning fixtures, and one window's paired record of coolant delivery pressure and wall thickness.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the recorded readings can carry a conclusion, how each characteristic has behaved across the run, where each sits against the range it is accepted in, which of them decides what this project does next, and what that is. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
# Precision-Turning Cell: Outer Diameter and Wall Thickness - Project Report

## 1. Can the readings carry a conclusion?

Yes, for the instrument itself. A crossed Gage R&R study (3 operators x 10 parts x 3 replicates,
90 readings) on the measuring instrument gave:

- percent Study Variation (Gage R&R) = 17.68%
- percent Tolerance = 9.80%
- Number of Distinct Categories (NDC) = 7.85

Against the AIAG guideline (under 10% excellent, 10-30% acceptable, over 30% unacceptable) and
the NDC>=5 rule of thumb, this measurement system is acceptable - the readings that follow
are trustworthy enough to base a decision on. It is not an excellent system, so part of the
variation seen in the run data has some measurement noise mixed in, but not enough to
invalidate the conclusions below.

## 2. Outer diameter (accept 24.80-25.20 mm)

125 readings, 25 subgroups of 5, in sampling order.

- X-bar chart centerline = 25.0007 mm, 0 subgroups flagged on the X-bar chart, 0 on the
  Range chart. The run is in statistical control.
- Normality: Shapiro-Wilk p = 0.518, Anderson-Darling statistic = 0.39 (well inside the normal
  range), skewness = 0.07. Diameter is normally distributed.
- Capability (normal method): Cp = 1.63, Cpk = 1.62, Pp = 1.61, Ppk = 1.61.

Outer diameter is stable, normally distributed, and highly capable, sitting comfortably inside
its 24.80-25.20 mm window. This characteristic is not a source of concern.

A secondary sample split diameter by the four turning fixtures (15 pieces each, N=60). A
one-way ANOVA found a statistically significant difference in mean diameter across fixtures
(F = 4.08, p = 0.011): fixture 4 runs highest (mean 25.021 mm) and fixture 2 lowest
(mean 24.982 mm). This is real fixture-to-fixture variation, but the overall diameter
distribution above already folds in all four fixtures and is still comfortably capable, so this
finding is noted for fixture maintenance and alignment follow-up but does not change the diameter
verdict.

## 3. Wall thickness (accept 1.20-1.60 mm)

125 readings, 25 subgroups of 5, in sampling order.

- X-bar chart centerline = 1.4002 mm, 0 subgroups flagged on the X-bar chart, but 4
  subgroups flagged out-of-control on the Range chart (subgroup indices 20, 21, 22 and 24,
  covering sampling points roughly 100-124, i.e. the last fifth of the run). The mean has not
  shifted, but the piece-to-piece spread within those subgroups blew out.
- Normality: Shapiro-Wilk p < 0.0001, Anderson-Darling statistic = 3.75, skewness = -0.86. Wall
  thickness is not normally distributed - the distribution is left-skewed, driven by the
  same late-run subgroups that flagged on the Range chart.
- Because the data fails normality, the normal-theory capability numbers (Cp=1.42, Cpk=1.41,
  Pp=1.29, Ppk=1.29) are computed for reference only and are not used as the reported
  capability - they overstate how capable the process really is by assuming a bell curve that
  the data does not follow.
- Capability (non-normal, percentile method, appropriate given the failed normality test):
  Pp = 1.04, Ppk = 0.89.

A Ppk of 0.89 sits below the conventional 1.00 capable floor. Wall thickness is the
characteristic that decides what this project does next, because it is the one that is not
reliably capable, while outer diameter comfortably is.

### What is causing it

A paired sample of coolant delivery pressure and wall thickness (n=60) was tested for a
relationship: Pearson correlation coefficient = -0.0046, p = 0.972. There is no linear
relationship between coolant pressure and wall thickness - coolant delivery pressure is ruled
out as the driver of the late-run spread blow-out.

No other process-fact record exists for what happened in the plant around sampling points
100-124. A direct question to the process owner about that window returned no recorded process
fact (routing refusal: unroutable, with no process topics on file). This is a genuine gap
in the record, not filled in with a guess: the mechanical or process root cause of the
Range-chart excursions is unknown from the data available in this exercise.

## 4. What was changed and what it achieved

No process change has been made yet in this record. The analysis to this point has:

- Confirmed the gage is fit to trust the readings (percent GRR 17.68%, NDC 7.85 - acceptable).
- Cleared outer diameter as capable and stable (Cpk 1.62).
- Identified wall thickness as the at-risk characteristic (Ppk 0.89, non-normal, driven by 4
  out-of-control Range-chart points late in the run).
- Ruled out coolant delivery pressure as the cause (r = -0.005, p = 0.97).
- Flagged, but not resolved, a real difference in diameter mean by turning fixture (p = 0.011)
  as a separate, secondary lead worth chasing on its own track.

## 5. How this will be held

- Outer diameter: continue routine X-bar/R monitoring; no action required now, but track the
  fixture-to-fixture diameter difference (fixture 2 vs fixture 4) since it is statistically real
  even though overall capability is unaffected.
- Wall thickness: treat as the open item. The Range-chart excursions in the last fifth of
  the sampled run, and the resulting Ppk of 0.89, mean the process cannot yet be called capable
  for wall thickness. Coolant pressure has been eliminated as a cause. The next step is to get a
  process fact (tooling wear timing, coolant chemistry change, operator changeover, or similar)
  for what happened around sampling points 100-124 - that fact was asked for and is not
  available in this system, so it needs to come from the shop floor directly, not from further
  data analysis of what is already on hand.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"msa","numOperators":3,"numParts":10,"numReplicates":3,"sampleSize":90},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":17.676789695918146,"percentTolerance":9.798151645361875,"ndc":7.8509511044268905},"status":"success","decision":"Measurement system judged acceptable (AIAG: percentGRR 10-30 = acceptable, NDC>=5 adequate resolution). Declared grr_pct and ndc to steward, which unlocked the outer diameter batch."}
{"step_id":2,"inputs_digest":{"batch":"run_diameter","n":125,"subgroupSize":5,"numSubgroups":25},"method_id":"control_chart.xbar_r","outputs":{"xBarChartCenterLine":25.000736000000003,"flaggedXBarCount":0,"flagged_r_count":0,"r_bar":0.09528800000000018,"sigma_within":0.04096646603611358},"status":"success","decision":"Outer diameter run is in statistical control on both X-bar and R charts; no special cause detected."}
{"step_id":3,"inputs_digest":{"batch":"run_diameter","n":125},"method_id":"basic.normality","outputs":{"pValue":0.5176888478958882,"statistic":0.39079168554886223,"skewness":0.07252491534100985},"status":"success","decision":"Shapiro-Wilk p=0.518, Anderson-Darling stat=0.39 (well below common critical value); diameter data consistent with normal distribution."}
{"step_id":4,"inputs_digest":{"batch":"run_diameter","n":125,"lsl":24.8,"usl":25.2},"method_id":"capability.normal","outputs":{"cp":1.6273472700304952,"cpk":1.621358632076784,"pp":1.6126789138774331,"ppk":1.6067442554743654},"status":"success","decision":"Outer diameter is highly capable and well centered (mean 25.0007 vs target 25.0); normal-theory capability is appropriate given the normality result in step 3."}
{"step_id":5,"inputs_digest":{"batch":"run_thickness","n":125,"subgroupSize":5,"numSubgroups":25},"method_id":"control_chart.xbar_r","outputs":{"xBarChartCenterLine":1.4002144,"flaggedXBarCount":0,"flagged_r_count":4,"r_bar":0.10948400000000001,"sigma_within":0.047069647463456585},"status":"success","decision":"Wall thickness R chart flags 4 out-of-control subgroups (indices 20,21,22,24; sampling points about 100 to 124), a cluster of excess within-subgroup spread near the end of the run. X-bar chart shows no shift."}
{"step_id":6,"inputs_digest":{"batch":"run_thickness","n":125},"method_id":"basic.normality","outputs":{"pValue":1.785017820134272e-08,"statistic":3.748874196248835,"skewness":-0.8599360027421524},"status":"success","decision":"Shapiro-Wilk p under 0.0001, Anderson-Darling stat=3.75 (far above critical values); wall thickness data is not normal, left-skewed, driven by the out-of-control subgroups from step 5."}
{"step_id":7,"inputs_digest":{"batch":"run_thickness","n":125,"lsl":1.2,"usl":1.6},"method_id":"capability.normal","outputs":{"cp":1.4163408960822286,"cpk":1.414822578641628,"pp":1.2878534744100454,"ppk":1.2864728954854774},"status":"success","decision":"Computed for reference only; rejected as the basis for a conclusion because step 6 shows the data fails normality, so normal-theory Cp Cpk Pp Ppk overstate capability here. See step 8 for the accepted figure."}
{"step_id":8,"inputs_digest":{"batch":"run_thickness","n":125,"lsl":1.2,"usl":1.6,"method":"percentile 0.135/50/99.865"},"method_id":"capability.nonnormal","outputs":{"pp":1.0411159597038153,"ppk":0.8944634207953956},"status":"success","decision":"Percentile-based non-normal capability is the accepted figure: Ppk=0.89, below the conventional 1.0 capable floor. Wall thickness is the characteristic driving process risk."}
{"step_id":9,"inputs_digest":{"batch":"fixtures","N":60,"groups":4,"perGroup":15},"method_id":"anova.oneway","outputs":{"fStatistic":4.077211854909738,"factorPValue":0.010893452040248355},"status":"success","decision":"Significant difference in mean outer diameter across the four turning fixtures (p=0.011); fixture 4 runs highest (mean 25.0209 mm) and fixture 2 lowest (mean 24.9825 mm). This is a secondary finding on diameter, which remains capable overall, not on wall thickness."}
{"step_id":10,"inputs_digest":{"batch":"setting","n":60,"x":"coolant delivery pressure bar","y":"wall thickness mm"},"method_id":"basic.correlation","outputs":{"correlationCoefficient":-0.0046019363382516915,"pValue":0.9721620684749913},"status":"success","decision":"No linear relationship between coolant delivery pressure and wall thickness (r=-0.005, p=0.97). Coolant pressure is ruled out as a driver of the wall thickness variability seen in step 5."}
{"step_id":11,"inputs_digest":{"question":"root cause of wall thickness range-chart excursions near sampling points 100 to 125"},"method_id":"meta.data_profiling","outputs":{},"status":"refused","decision":"Process owner had no recorded process fact for this question (provision refused as unroutable, no topics on file). Root cause of the special-cause variation in wall thickness is not established from available data; this is a genuine gap, not filled in."}
```

## Submitted route declarations
```json
[{"point":"measurement_system_acceptability","chosen_branch":"acceptable, proceed with analysis","observed":{"percentStudyVariation":17.676789695918146,"ndc":7.8509511044268905}},{"point":"wall_thickness_capability_method","chosen_branch":"nonnormal percentile capability","observed":{"shapiroP":1.785017820134272e-08,"skewness":-0.8599360027421524}},{"point":"decisive_characteristic","chosen_branch":"wall thickness","observed":{"ppk_thickness_nonnormal":0.8944634207953956,"cpk_diameter":1.621358632076784}},{"point":"wall_thickness_root_cause_hypothesis","chosen_branch":"coolant delivery pressure ruled out; root cause unresolved","observed":{"correlationCoefficient":-0.0046019363382516915,"pValue":0.9721620684749913}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
