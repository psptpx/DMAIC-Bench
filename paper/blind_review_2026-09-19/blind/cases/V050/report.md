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
