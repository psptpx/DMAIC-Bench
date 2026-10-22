# Blind item V050

Focal assessment: Optimization results and the basis for subsequent confirmation or implementation.

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
# Seal-strength project: decision for the quality manager

## Executive decision
The baseline is consistent with a repeatable but inadequate process. Screening identifies bond angle and bead spacing as useful levers. The recommended-settings batch is substantially stronger and supports a mean above the programme requirement. However, the composite model does **not** predict that achievement. Do not close the project or deploy the model as a validated operating recipe until this discrepancy and the physical setting records are reconciled.

## Baseline behaviour and requirements
The hard lower requirement is 45 N; the programme requires strength above 55 N. Across 60 consecutive seals, mean strength was 51.197 N, median 51.420 N and sample standard deviation 4.359 N. There were 4 observations below the hard limit and 50 below the programme threshold.

An individuals/moving-range analysis gave individual limits 37.816–64.579 N and 0 outside-limit observations. The moving-range upper limit was 16.437 N with 0 exceedances. These pointwise screens show no gross special-cause signal; they are not proof of independence or exhaustive run-pattern testing. Anderson–Darling normality p=0.4440 does not reject a normal approximation.

Conditional lower-only capability is Cpk=0.463, Ppk=0.474 against the hard requirement: inadequate protection of the lower tail. Cp and Pp cannot be computed without an upper specification. For a test that the mean exceeds the programme threshold, t=-6.758, one-sided p=1.00000000; the one-sided 95% upper mean bound is only 52.138 N. The baseline does not support the programme margin.

## What the screening explains
A full replicated factorial fit to 16 trials explains 88.08% of the screening variation (model p=0.00370). High-minus-low effects were:

| Setting | Effect, N | p-value |
|---|---:|---:|
| Bond angle | 4.6277 | 0.000290 |
| Bead spacing | 3.0818 | 0.003625 |
| Cure temperature | 0.5970 | 0.454058 |

The angle–spacing interaction effect was 1.5965 N (p=0.06850); it is suggestive rather than strong evidence. Temperature and its interactions are not demonstrated drivers in this experiment. Angle and spacing justify follow-up, but experimental effects do not identify the cause of baseline variation without records linking baseline settings to strengths. Randomization and measurement-system validation were not supplied.

## What the composite design supports
The full quadratic fitted to 13 trials has R-squared 93.57% and lack-of-fit p=0.96271. Replicated-centre pure error permits this test, but failure to detect lack of fit is not proof of a globally valid model.

The stationary point is at coded angle 0.2407, coded spacing 0.2344. Quadratic-form eigenvalues -1.5980 and -1.2016 identify a local maximum. Predicted strength there is 48.362 N; a conditional 95% individual prediction interval is 46.912–49.813 N. Thus optimizing this fitted surface cannot deliver the programme target within its supported region. There is no defensible basis for extrapolating it to a stronger recipe.

## What the recommended-settings batch achieved
The archive labels this as the recommended-settings batch, but does not disclose the actual recipe. Its 20 seals had mean 59.873 N and standard deviation 1.708 N; 0 were below the hard limit and 0 below the programme threshold. The one-sided target test gives t=12.762, p=4.55e-11, and a 95% lower confidence bound on the mean of 59.213 N. This supports a mean above target, not a guarantee for all future seals.

The mean exceeds baseline by 8.676 N (Welch p=1.45e-20). Against the hard limit, conditional lower-only Cpk=2.692 and Ppk=2.903; against the programme threshold, the overall lower index is 0.951. The batch's normality p=0.2112. A provisional chart in supplied record order has 0 individual-limit and 0 moving-range exceedances, but confirmation chronology and long-term stability are not established.

Crucially, the confirmation mean is 11.511 N above the fitted composite maximum, and 20 confirmation measurements exceed its individual prediction interval. The result is encouraging observed performance, **not validation of that surface**. A changed recipe, coding mismatch, batch shift or omitted process variable could explain this; none is established by the supplied data.

## Missing evidence and next actions
No physical coding map or implementation record was released: the request was unroutable, not a checked denial. The process-owner query also yielded no measurement or sampling facts. Therefore physical setpoints, measurement adequacy, randomization and the reason for the model/confirmation discrepancy cannot be determined. No claim of a specific physical change or verified root cause is justified.

Recover signed setting sheets and coding maps, check response units and sample provenance, and reconcile the design and confirmation batches before further optimization. Validate the destructive pull measurement method with an appropriate nested or reference-based study. Repeat randomized, blocked confirmation at the verified recipe with representative material, operators and time coverage; explicitly assess both the programme lower tail and the hard specification.

For containment, retain pull-test surveillance and segregate suspect production under the plant's approved disposition procedure. Once the recipe and sustained stability are established, lock controlled setpoints, record material and cure history, and create an owned control plan. Use time-ordered strength charts with documented special-cause reaction and capability review; recalculate limits only after an approved stable-process study. The present evidence supports continued improvement work, not unconditional project closure.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"basic.descriptive_summary","inputs_digest":{"batch":"baseline"},"outputs":{"mean":51.19733333333334,"median":51.42,"stdDev":4.358781849214244,"skewness":0.3060216575441991,"n":60.0,"lsl":45.0,"requiredLevel":55.0,"belowLSL":4.0,"belowTarget":50.0},"status":"success","decision":""}
{"step_id":2,"method_id":"control_chart.imr","inputs_digest":{"batch":"baseline"},"outputs":{"centerLine":51.19733333333334,"individualsLCL":37.81606755619666,"individualsUCL":64.57859911047002,"flaggedCount":0.0,"movingRangeMean":5.0313559322033905,"movingRangeUCL":16.437439830508477,"movingRangeFlags":0.0,"withinSigma":4.460421925712226},"status":"success","decision":"Pointwise three-sigma screen; does not establish absence of all special causes."}
{"step_id":3,"method_id":"basic.normality","inputs_digest":{"batch":"baseline"},"outputs":{"statistic":0.35726439281149425,"pValue":0.4440166457189789},"status":"success","decision":"Anderson-Darling normality test"}
{"step_id":4,"method_id":"capability.normal","inputs_digest":{"batch":"baseline"},"outputs":{"cpk":0.46313506035596014,"ppk":0.473934656342156,"targetPpk":-0.29080499997586595},"status":"success","decision":"Lower-only indices; Cp and Pp undefined without USL. Conditional on stability and normality."}
{"step_id":5,"method_id":"basic.one_sample_t","inputs_digest":{"batch":"baseline"},"outputs":{"tStatistic":-6.757697531402264,"pValue":0.9999999965263269,"meanLower95":50.25698201684555,"meanUpper95":52.13768464982113},"status":"success","decision":"One-sided test mean exceeds programme target; not a guarantee for individuals."}
{"step_id":6,"method_id":"doe.factorial_analysis","inputs_digest":{"batch":"screening_run"},"outputs":{"modelPValue":0.0036952811952333745,"rSquaredPct":88.07537815826764,"n":16.0,"errorDF":8.0,"residualSD":1.5174864496923863,"AEffect":4.6277499999999945,"APValue":0.00028971645720400456,"BEffect":3.081750000000001,"BPValue":0.0036251317340484156,"CEffect":0.5969999999999902,"CPValue":0.4540583696688957,"ABEffect":1.5965000000000011,"ABPValue":0.06849524644563439,"ACEffect":0.009750000000002368,"ACPValue":0.9900619904057812,"BCEffect":-0.38525000000000786,"BCPValue":0.6253300432094485,"ABCEffect":0.2224999999999874,"ABCPValue":0.7767955788957847},"status":"success","decision":"Full replicated factorial; A angle, B spacing, C temperature."}
{"step_id":7,"method_id":"doe.rsm_analysis","inputs_digest":{"batch":"composite_design"},"outputs":{"rSquaredPct":93.56781431583127,"lackOfFitPValue":0.9627114149832965,"lackOfFitF":0.08835496385922445,"pureErrorSS":2.0699970680000126,"pureErrorDF":4.0,"lackOfFitDF":3.0,"residualSD":0.5615244499318535,"n":13.0,"intercept":48.20268000026528,"angle":0.7733541208432051,"spacing":0.5676878420430844,"interaction":-0.01754999999999238,"angleSquared":-1.5978150032289886,"spacingSquared":-1.2017650018998314},"status":"success","decision":"Full quadratic with replicated-centre pure-error lack-of-fit test."}
{"step_id":8,"method_id":"doe.rsm_canonical","inputs_digest":{"batch":"composite_design"},"outputs":{"predictedAtStationary":48.36230139645569,"stationaryAngle":0.24071617975852067,"stationarySpacing":0.23443155367212534,"eigenvalueLow":-1.5980093293547264,"eigenvalueHigh":-1.2015706757740936,"piLower":46.911802499808,"piUpper":49.812800293103386},"status":"success","decision":"Negative eigenvalues identify a fitted maximum; prediction interval conditional on quadratic adequacy."}
{"step_id":9,"method_id":"basic.descriptive_summary","inputs_digest":{"batch":"confirmation_runs"},"outputs":{"mean":59.87299999999999,"median":59.495000000000005,"stdDev":1.707648737453437,"skewness":0.7043198881179051,"n":20.0,"lsl":45.0,"requiredLevel":55.0,"belowLSL":0.0,"belowTarget":0.0},"status":"success","decision":""}
{"step_id":10,"method_id":"control_chart.imr","inputs_digest":{"batch":"confirmation_runs"},"outputs":{"centerLine":59.87299999999999,"individualsLCL":54.34808398656214,"individualsUCL":65.39791601343784,"flaggedCount":0.0,"movingRangeMean":2.077368421052632,"movingRangeUCL":6.7867626315789495,"movingRangeFlags":0.0,"withinSigma":1.8416386711459507},"status":"success","decision":"Pointwise three-sigma screen; does not establish absence of all special causes."}
{"step_id":11,"method_id":"basic.normality","inputs_digest":{"batch":"confirmation_runs"},"outputs":{"statistic":0.4773550324320155,"pValue":0.21115690637800058},"status":"success","decision":"Anderson-Darling normality test"}
{"step_id":12,"method_id":"capability.normal","inputs_digest":{"batch":"confirmation_runs"},"outputs":{"cpk":2.691986622751454,"ppk":2.9032122109959664,"targetPpk":0.9512104554685218},"status":"success","decision":"Lower-only indices; Cp and Pp undefined without USL. Conditional on stability and normality."}
{"step_id":13,"method_id":"basic.one_sample_t","inputs_digest":{"batch":"confirmation_runs"},"outputs":{"tStatistic":12.761827436016908,"pValue":4.549448452460978e-11,"meanLower95":59.21274470092243,"meanUpper95":60.53325529907755},"status":"success","decision":"One-sided test mean exceeds programme target; not a guarantee for individuals."}
{"step_id":14,"method_id":"basic.two_sample_t","inputs_digest":{"batch":"confirmation_runs"},"outputs":{"tStatistic":12.757604095833555,"pValue":1.4499350334549586e-20,"meanDifference":8.67566666666665},"status":"success","decision":"Welch comparison of distinct batches; association, not unconfounded causal effect."}
{"step_id":15,"method_id":"meta.data_profiling","inputs_digest":{"batch":"confirmation_runs"},"outputs":{"confirmationMinusRsm":11.510698603544299,"confirmationOutsideRsmPI":20.0,"confidencePct":95.0},"status":"success","decision":"Consistency audit of confirmation against local stationary prediction; settings equivalence is unverified."}
```

## Submitted route declarations
```json
[{"point":"screening_significance","chosen_branch":"significant","observed":{"any_factor_significant":true}},{"point":"release","chosen_branch":"hold_model_based_rollout_pending_reconciliation","observed":{"confirmation_above_target":true,"rsm_max_below_target":true}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
