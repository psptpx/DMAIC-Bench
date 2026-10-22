# Blind item V041

Focal assessment: Applicability of the response-surface model and the basis for subsequent optimization.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the development team on an assembled optical module. The seal between the two housings must hold at least 45 N, and the product margin the programme committed to needs it above 55 N. Sixty consecutive assemblies have been pulled and tested in the order they were built. The archive also holds a screening run in which three assembly settings were each taken to a low and a high level twice over; a later composite design over two of those settings, with the centre setting run five times; and twenty seals made at the settings that design work recommended.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: how the line has behaved across the baseline, where seal strength sits against what the product requires, whether the settings that were varied account for it, what the design work supports concluding, and what should happen next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
{"screening_significant":{"field":"any_factor_significant","op":"==","value":true,"source":"Montgomery DAOE 6e 11.2"}}
```

## Submitted report (complete, identifiers removed)
# Seal strength on the optical module: where the project stands

Task: `[TASK]`. Requirement: seal strength must hold at least **45.0 N** (specification
floor), and the programme committed to a product margin above **55.0 N**. Every figure below comes from a
computation run on this task and is traceable to an `outputs` entry in `/workspace/trace.json`.

## 1. Where things stand

Sixty consecutive assemblies were pulled in build order. The line is **stable but not capable**.

- Mean 52.08 N, median 51.81 N, standard deviation 4.30 N, skewness -0.15.
- Stability: the individuals/moving-range chart flagged **0** points, with centre line 52.08 N and limits
  39.40 to 64.75 N. The runs test on build order gives p = 0.795, so there is no drift, no clustering,
  no shift over the sixty builds.
- Normality holds (Shapiro p = 0.676, Anderson-Darling p = 0.380), so normal-theory capability and
  t-tests are legitimate here.
- Capability against the 45 N floor: **Cpk 0.56, Ppk 0.55**, about **49,874 ppm** below specification.
  Four of the sixty assemblies actually fell below 45 N.
- Against the 55 N product margin: 41 of 60 assemblies (fraction 0.683) came in below it. The mean falls
  short by **2.92 N** (one-sample t = -5.27, p = 2.02e-06), and the whole 95% confidence interval,
  50.97 to 53.19 N, sits under 55.

Cp and Pp are not quoted anywhere in this report. The requirement is one-sided (a floor only), so those
two indices are undefined rather than computed; the trace records that reasoning instead of a number.

**Read across:** this is a centring problem in a process that is behaving predictably. Nothing is broken
intermittently, so chasing individual bad seals would have been wasted effort. The mean sits in the wrong
place, and the spread is wide enough that the floor is breached routinely.

## 2. Do the settings that were varied account for it

Yes. The screening run was a full three-factor design at a low and a high level, each corner run twice
(16 runs). Fitted with all interactions: model p = 1.42e-04, R-squared 94.91%.

| term | effect (N) | p |
|---|---|---|
| bond angle | +4.39 | 1.61e-05 |
| bead spacing | +3.08 | 2.00e-04 |
| bond angle x bead spacing | +2.19 | 1.79e-03 |
| cure temperature | +0.18 | 0.713 |

Two settings and their interaction carry the response; **cure temperature is inert** and was dropped. A
reduced two-factor model retains 93.26% of the variation with a residual standard deviation of 0.90 N.
The strongest screening corner already averaged **59.06 N**, above the requirement, which showed there was
real headroom to be had from settings alone. On that basis `any_factor_significant` was declared true.

## 3. What the design work supports concluding

A composite design over the two live settings, with the centre run five times (13 runs), gives a quadratic
surface: R-squared 98.02%, model p = 8.32e-06, with both linear terms and both quadratic terms significant
(bond angle p = 6.44e-07, bead spacing p = 0.0020, bond angle squared p = 0.0017, bead spacing squared
p = 0.0039). The two-factor interaction is not significant here (p = 0.130).

Two qualifications matter and neither should be buried:

1. **Lack of fit is significant**: F = 40.34, p = 0.0019, measured against a very tight pure error of
   0.25 N from the five centre replicates (centre mean 57.93 N). The curvature is real, but a quadratic is
   an approximation of this surface, not a faithful description of it. Predictions from it carry more
   error than the fit statistics alone suggest.
2. **The mathematical optimum lies outside the region actually explored.** Canonical analysis puts the
   stationary point at a true maximum (both eigenvalues negative, -4.65 and -2.74) predicting 64.59 N, but
   at coded radius **2.08** against a design radius of 1.414. Using it would be extrapolation, so it was
   not used.

Constrained to the region the design actually covers, the recommended operating point is bond angle +1.27
and bead spacing +0.61 in coded units, predicting **63.92 N** (95% prediction interval 60.72 to 67.13 N),
8.92 N above the requirement.

## 4. What the change achieved

Twenty seals were made at the recommended settings.

- Mean **59.28 N**, standard deviation **1.98 N**, weakest seal 56.41 N.
- **Zero** seals below the 45 N floor and **zero** below the 55 N requirement; all twenty clear both.
- Stable: I-MR flagged 0 points, with limits 53.35 to 65.20 N, entirely above the floor.
- Normality holds (Shapiro p = 0.321, AD p = 0.510).
- Against the 45 N floor: **Cpk 2.41, Ppk 2.40**.
- Against the 55 N requirement the mean now clears it by **4.27 N** (t = 9.66, p = 9.21e-09), with a
  one-sided 95% lower bound of **58.51 N**.
- Versus baseline: **+7.20 N** (Welch t = 10.14, p = 2.23e-15, Cohen's d = 1.86), corroborated
  distribution-free by Mann-Whitney (p = 1.66e-09). Variation genuinely fell too, standard deviation 4.30
  to 1.98 N (Levene p = 0.0011) — the gain is not a mean shift with the spread left untouched.
- Share of seals meeting the 55 N requirement rose from **0.317** (19 of 60) to **1.000** (20 of 20),
  z = 5.29, p = 1.19e-07.

**The model over-predicted, and that is worth stating.** Observed 59.28 N against a predicted 63.92 N is a
gap of **-4.65 N**, and the observed mean falls **outside** the 95% prediction interval (p = 2.38e-09).
The improvement is real and confirmed; the surface's point prediction is not trustworthy to the newton.
This is exactly what the significant lack of fit warned about, and it is why the confirmation run, not the
model, is the basis for the verdict.

## 5. The honest limit on the 55 N margin

The requirement is met on average and met by every seal in this run, but it is **not met with
capability-grade headroom**. Treating 55 N as the floor rather than 45 N gives **Ppk 0.72** and an
estimated **15,410 ppm** below 55 N. In plain terms: at the current spread, roughly one seal in sixty-five
would be expected under 55 N over a long production run even with the settings held perfectly. Twenty
consecutive passing seals do not contradict that; a sample of twenty is simply too small to see a
one-in-sixty-five event reliably.

## 6. What should happen next

1. **Freeze the recommended settings** — bond angle +1.27, bead spacing +0.61 coded — as the standard
   operating condition, and release cure temperature as a control variable, since it moved the response by
   0.18 N (p = 0.713) and is not worth constraining.
2. **Hold with an I-MR chart on seal strength**, centred at 59.28 N with limits 53.35 to 65.20 N from the
   confirmation run. Recompute the limits once 40 to 60 seals have accumulated at the new settings; twenty
   points is a provisional basis.
3. **Do not close the project on the 55 N margin.** Ppk 0.72 against 55 N means variation reduction is the
   next piece of work, not further mean-shifting. The mean already sits 4.27 N clear.
4. **If more mean is wanted, run a small follow-up design shifted toward the stationary point** rather
   than extrapolating to it. The canonical maximum sits at coded radius 2.08, beyond the explored region,
   and the significant lack of fit plus a -4.65 N prediction miss both say the surface should not be
   trusted outside where it was fitted.

## 7. Data and gaps

All five batches held by the data steward were released and analysed: the charter, the 60-assembly
baseline, the replicated three-factor screening run, the composite design, and the twenty confirmation
seals. **No batch was denied**, so no step of this analysis is missing for want of data.

One limitation is not a data gap but is worth recording: the process owner holds **no recorded process
facts** for this task (one query returned nothing available). So this report says nothing about whether the
recommended bond angle and bead spacing can be held to a stated tolerance in routine production, what the
measurement system contributes to the 1.98 N observed spread, or what the settings cost to maintain. No
gauge study was available either, so the split between product variation and measurement variation is
unknown. Point 2 above — hold the chart and recompute the limits on more data — is the safeguard against
that uncertainty, not a substitute for closing it.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"sampleSize":60,"groups":1,"batch":"baseline"},"method_id":"basic.descriptive_summary","outputs":{"mean":52.07566666666666,"median":51.805,"stdDev":4.2984961369702335,"skewness":-0.14758060977391452,"adPValue":0.38002711705108244,"minimum":41.08,"maximum":62.92,"belowLsl":4,"belowRequired":41,"fracBelowRequired":0.6833333333333333},"status":"success","decision":"Baseline centres at 52.08 N with sd 4.30 N; 4 of 60 below the 45 N floor and 41 of 60 below the 55 N requirement."}
{"step_id":2,"inputs_digest":{"sampleSize":60,"groups":1,"batch":"baseline"},"method_id":"basic.normality","outputs":{"pValue":0.6764205833753795,"statistic":0.9851228579009723,"adPValue":0.38002711705108244},"status":"success","decision":"Normality not rejected (Shapiro p=0.676, Anderson-Darling p=0.380), so normal-theory capability and t-tests are appropriate."}
{"step_id":3,"inputs_digest":{"sampleSize":60,"groups":1,"batch":"baseline"},"method_id":"control_chart.imr","outputs":{"centerLine":52.07566666666666,"individualsUCL":64.74966594542613,"individualsLCL":39.401667387907196,"flaggedCount":0,"sigmaWithin":4.2246664262531555,"mrBar":4.765423728813559},"status":"success","decision":"No point outside the individuals or moving-range limits: the line is stable, so the shortfall is common-cause, not a special-cause excursion."}
{"step_id":4,"inputs_digest":{"sampleSize":60,"groups":1,"batch":"baseline"},"method_id":"nonparametric.runs_test","outputs":{"pValue":0.7945434963754623,"zStatistic":0.2604152298810939,"runs":32,"expectedRuns":31.0},"status":"success","decision":"Build order shows no drift or clustering (p=0.795); the 60 assemblies behave as one homogeneous population."}
{"step_id":5,"inputs_digest":{"sampleSize":60,"groups":1,"batch":"baseline","lsl":45.0},"method_id":"capability.normal","outputs":{"cpk":0.5582820790060223,"ppk":0.5486931895251083,"sigmaWithin":4.2246664262531555,"sigmaOverall":4.2984961369702335,"zLsl":1.6460795685753251,"ppmBelowLsl":49873.68915258372,"capabilityVsRequired55":-0.22677181663465318},"status":"success","decision":"Stable but not capable: Cpk 0.56, Ppk 0.55 against the 45 N floor, about 49874 ppm below spec. cp and pp are not reported because the requirement is one-sided (LSL only), so they are undefined here rather than computed."}
{"step_id":6,"inputs_digest":{"sampleSize":60,"groups":1,"batch":"baseline","testValue":55.0},"method_id":"basic.one_sample_t","outputs":{"pValue":2.024484174071137e-06,"tStatistic":-5.2697008152912845,"mean":52.07566666666666,"ci95Lower":50.965247367906905,"ci95Upper":53.18608596542642,"meanShortfall":-2.924333333333337},"status":"success","decision":"Baseline mean is below the 55 N product margin by 2.92 N (t=-5.27, p=2.02e-06); the whole 95% CI [50.97, 53.19] lies under 55."}
{"step_id":7,"inputs_digest":{"sampleSize":16,"groups":8,"factors":3,"batch":"screening_run"},"method_id":"doe.factorial_analysis","outputs":{"modelPValue":0.0001417792462045015,"rSquaredPct":94.9115904373612,"rSquaredAdjPct":90.45923207005224,"fStatistic":21.31714983552114,"pValue_bond_angle":1.6133893323495207e-05,"pValue_bead_spacing":0.00019993241547936803,"pValue_cure_temperature":0.7132611114928761,"pValue_bond_angle_x_bead_spacing":0.0017912880490681346,"effect_bond_angle":4.38612499999998,"effect_bead_spacing":3.081125000000008,"effect_cure_temperature":0.1821250000000042,"effect_bond_angle_x_bead_spacing":2.1926250000000143,"nSignificantTerms":3,"anyFactorSignificant":true,"reducedModelRSquaredPct":93.26276613213088,"reducedResidStdDev":0.898672133854537,"bestCornerMean":59.056},"status":"success","decision":"Replicated 2^3: bond angle (+4.39 N), bead spacing (+3.08 N) and their interaction (+2.19 N) are significant; cure temperature is inert (+0.18 N, p=0.713). The varied settings do account for the shortfall. Declared any_factor_significant=true."}
{"step_id":8,"inputs_digest":{"sampleSize":13,"groups":9,"factors":2,"centrePoints":5,"batch":"composite_design"},"method_id":"doe.rsm_analysis","outputs":{"rSquaredPct":98.01737641449877,"lackOfFitPValue":0.0018986454618481474,"rSquaredAdjPct":96.60121671056932,"modelPValue":8.319937285038599e-06,"lackOfFitF":40.34160786968319,"pureErrorStdDev":0.2514963916242127,"centreMean":57.931799999999996,"coef_bond_angle":6.319122099301679,"coef_bead_spacing":1.798696267547763,"coef_bond_angle_sq":-1.9929750035951086,"coef_bead_spacing_sq":-1.6998500026113694,"pValue_bond_angle":6.436966385163061e-07,"pValue_bead_spacing":0.001997102846945542,"pValue_bond_angle_sq":0.0016645744226064787,"pValue_bead_spacing_sq":0.003945465890083207,"pValue_bond_angle_x_bead_spacing":0.13044797762324883},"status":"success","decision":"Quadratic surface explains 98.02% of variation (p=8.32e-06) with both linear and both quadratic terms significant, but lack of fit is significant (F=40.34, p=0.0019) against a very tight pure error of 0.25 N: the quadratic form is a working approximation, not an exact description."}
{"step_id":9,"inputs_digest":{"sampleSize":13,"factors":2,"batch":"composite_design"},"method_id":"doe.rsm_canonical","outputs":{"predictedAtStationary":64.58718079009289,"stationary_bond_angle":1.8173160589514012,"stationary_bead_spacing":1.0156909443798057,"eigenvalue1":-4.649179475964806,"eigenvalue2":-2.7364705364481496,"stationaryRadius":2.081889947287751,"isMaximum":true},"status":"success","decision":"Both eigenvalues negative, so the stationary point is a true maximum, but it sits at coded radius 2.08, outside the design region (axial radius 1.414). Using it directly would be extrapolation."}
{"step_id":10,"inputs_digest":{"sampleSize":13,"factors":2,"batch":"composite_design","constraintRadius":1.41421356},"method_id":"doe.rsm_optimizer","outputs":{"predictedResponse":63.92321358321104,"compositeDesirability":0.9629748209329545,"opt_bond_angle":1.2737647237820153,"opt_bead_spacing":0.6144294734226083,"optRadius":1.4142136151804852,"marginOverRequired":8.923213583211037},"status":"success","decision":"Constrained to the explored region, the optimum is bond angle +1.27, bead spacing +0.61 in coded units, predicting 63.92 N, 8.92 N above the requirement. Desirability is a one-sided score built on the 55 N target, not a Minitab multi-response value."}
{"step_id":11,"inputs_digest":{"sampleSize":13,"factors":2,"batch":"composite_design"},"method_id":"doe.factorial_prediction","outputs":{"predictedValue":63.92321358321104,"piLower":60.71938187093668,"piUpper":67.12704529548539,"ciLower":61.93628142820059,"ciUpper":65.91014573822149},"status":"success","decision":"Prediction at the recommended setting: 63.92 N, 95% prediction interval 60.72 to 67.13 N. Entry used for a response-surface prediction; the table has no separate rsm_prediction id."}
{"step_id":12,"inputs_digest":{"sampleSize":20,"groups":1,"batch":"confirmation_runs"},"method_id":"basic.descriptive_summary","outputs":{"mean":59.27499999999999,"median":59.04,"stdDev":1.9797301783190986,"skewness":0.6007215186410805,"adPValue":0.5101447105824561,"minimum":56.41,"maximum":63.24,"belowLsl":0,"belowRequired":0,"fracAboveRequired":1.0},"status":"success","decision":"Twenty confirmation seals average 59.28 N with sd 1.98 N; the weakest is 56.41 N, so none fall below either the 45 N floor or the 55 N requirement."}
{"step_id":13,"inputs_digest":{"sampleSize":20,"groups":1,"batch":"confirmation_runs"},"method_id":"basic.normality","outputs":{"pValue":0.32068275910071753,"statistic":0.9467683759131525,"adPValue":0.5101447105824561},"status":"success","decision":"Confirmation seals are consistent with normality (Shapiro p=0.321, AD p=0.510)."}
{"step_id":14,"inputs_digest":{"sampleSize":20,"groups":1,"batch":"confirmation_runs"},"method_id":"control_chart.imr","outputs":{"centerLine":59.27499999999999,"individualsUCL":65.19745240761478,"individualsLCL":53.35254759238521,"flaggedCount":0,"sigmaWithin":1.974150802538261,"mrBar":2.226842105263158},"status":"success","decision":"Confirmation run is stable with no flagged points; the new limits (53.35 to 65.20 N) sit entirely above the 45 N floor."}
{"step_id":15,"inputs_digest":{"sampleSize":20,"groups":1,"batch":"confirmation_runs","lsl":45.0},"method_id":"capability.normal","outputs":{"cpk":2.4103190735050797,"ppk":2.403526190308126,"sigmaWithin":1.974150802538261,"sigmaOverall":1.9797301783190986,"zLsl":7.210578570924379,"ppmBelowLsl":2.7857318686229193e-07,"ppkVsRequired55":0.7197950587437636,"cpkVsRequired55":0.7218293547624659,"ppmBelowRequired55":15410.148486626098},"status":"success","decision":"Against the 45 N floor capability is now Cpk 2.41 / Ppk 2.40. Against the tougher 55 N product margin Ppk is only 0.72, about 15410 ppm, so the margin is met on average but not with capability-grade headroom. cp and pp are undefined for a one-sided requirement and are not reported."}
{"step_id":16,"inputs_digest":{"sampleSize":20,"groups":1,"batch":"confirmation_runs","testValue":55.0},"method_id":"basic.one_sample_t","outputs":{"pValue":9.205634874451753e-09,"tStatistic":9.657064087317059,"mean":59.27499999999999,"ci95Lower":58.3484577557224,"ci95Upper":60.20154224427758,"lower95OneSidedBound":58.50954554071334,"marginOverRequired":4.2749999999999915},"status":"success","decision":"Confirmation mean exceeds the 55 N requirement by 4.27 N (t=9.66, p=9.21e-09); the one-sided 95% lower bound is 58.51 N."}
{"step_id":17,"inputs_digest":{"sampleSize":80,"groups":2,"batches":"baseline+confirmation_runs"},"method_id":"anova.equal_variances","outputs":{"pValue":0.0010523717921275457,"statistic":11.584918360378822,"sdBaseline":4.2984961369702335,"sdConfirm":1.9797301783190986},"status":"success","decision":"Variation genuinely fell, not just the mean: sd 4.30 to 1.98 N, Levene p=0.0011. Welch is therefore the right two-sample test."}
{"step_id":18,"inputs_digest":{"sampleSize":80,"groups":2,"batches":"baseline+confirmation_runs"},"method_id":"basic.two_sample_t","outputs":{"pValue":2.2252665764921073e-15,"tStatistic":10.141739773219125,"meanDifference":7.199333333333328,"meanBaseline":52.07566666666666,"meanConfirm":59.27499999999999,"cohensD":1.8631529590875198},"status":"success","decision":"Welch test: the change lifted seal strength by 7.20 N (p=2.23e-15, d=1.86)."}
{"step_id":19,"inputs_digest":{"sampleSize":80,"groups":2,"batches":"baseline+confirmation_runs"},"method_id":"nonparametric.mann_whitney","outputs":{"pValue":1.6622939292704701e-09,"statistic":1143.0},"status":"success","decision":"Distribution-free confirmation of the same shift (p=1.66e-09), so the result does not depend on the normal assumption."}
{"step_id":20,"inputs_digest":{"sampleSize":80,"groups":2,"batches":"baseline+confirmation_runs","threshold":55.0},"method_id":"basic.two_proportions","outputs":{"pValue":1.1919101483570671e-07,"zStatistic":5.294732102211408,"propBaselineMeetingReq":0.31666666666666665,"propConfirmMeetingReq":1.0,"countBaseline":19,"countConfirm":20},"status":"success","decision":"Share of seals meeting the 55 N requirement rose from 0.317 to 1.000 (z=5.29, p=1.19e-07)."}
{"step_id":21,"inputs_digest":{"sampleSize":20,"batches":"composite_design vs confirmation_runs"},"method_id":"doe.factorial_prediction","outputs":{"predictedValue":63.92321358321104,"piLower":60.71938187093668,"piUpper":67.12704529548539,"observedMean":59.27499999999999,"gap":-4.648213583211046,"tStatistic":-10.500139523884638,"pValue":2.3842485763481136e-09,"observedInsidePI":false},"status":"success","decision":"Model validation: observed 59.28 N is 4.65 N below the predicted 63.92 N and falls outside the 95% prediction interval (p=2.38e-09). The surface over-predicts, which the significant lack of fit already warned about."}
```

## Submitted route declarations
```json
[{"point":"baseline_stability_vs_capability","chosen_branch":"stable_but_incapable_so_attack_the_settings","observed":{"flaggedCount":0,"runsPValue":0.7945434963754623,"cpk":0.5582820790060223,"ppk":0.5486931895251083,"oneSampleTPValue":2.024484174071137e-06,"meanShortfall":-2.924333333333337}},{"point":"screening_any_factor_significant","chosen_branch":"true_proceed_to_composite_design","observed":{"pValue_bond_angle":1.6133893323495207e-05,"pValue_bead_spacing":0.00019993241547936803,"pValue_cure_temperature":0.7132611114928761,"nSignificantTerms":3}},{"point":"drop_inert_factor","chosen_branch":"drop_cure_temperature_carry_two_factors_forward","observed":{"effect_cure_temperature":0.1821250000000042,"pValue_cure_temperature":0.7132611114928761}},{"point":"stationary_point_inside_design_region","chosen_branch":"no_use_constrained_optimum_on_the_boundary","observed":{"stationaryRadius":2.081889947287751,"designRadius":1.41421356,"predictedAtStationary":64.58718079009289,"constrainedPrediction":63.92321358321104}},{"point":"rsm_lack_of_fit","chosen_branch":"significant_treat_prediction_as_approximate_and_verify_empirically","observed":{"lackOfFitPValue":0.0018986454618481474,"pureErrorStdDev":0.2514963916242127}},{"point":"confirmation_verdict","chosen_branch":"improvement_confirmed_move_to_control","observed":{"mean":59.27499999999999,"lower95OneSidedBound":58.50954554071334,"belowRequired":0,"flaggedCount":0,"ppk":2.403526190308126}},{"point":"margin_headroom_at_55N","chosen_branch":"mean_meets_requirement_but_ppk_below_capability_grade","observed":{"ppkVsRequired55":0.7197950587437636,"ppmBelowRequired55":15410.148486626098}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
