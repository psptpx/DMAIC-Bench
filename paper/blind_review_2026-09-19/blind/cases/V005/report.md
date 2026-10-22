# Seal-strength project status

## Executive conclusion

The baseline line was statistically quiet but not performing the business objective. Its mean was **52.076 N**, versus the product lower specification of **45 N** and the programme requirement of **55 N**. The recommended-setting confirmation improved the observed mean to **59.275 N**, an increase of **7.199 N** with a confidence interval from **5.784 N** to **8.615 N**. All **20** confirmation seals exceeded both thresholds.

The improvement is real in the available sample, but the project should not yet be closed as fully capable against the programme margin. Confirmation overall lower performance was **Ppk 0.720** against **55 N**, despite **Ppk 2.404** against **45 N**. Hold the recommended settings, verify their identity in controlled documentation, and continue sequential monitoring before making a long-term capability claim.

## Baseline behavior and requirement gap

The **60** consecutive baseline assemblies averaged **52.076 N**, with median **51.805 N** and standard deviation **4.298 N**. The observed range was **41.080 N** to **62.920 N**. There were **4** results below **45 N**, or **6.667%**, and **41** below **55 N**, or **68.333%**.

The I-MR centre line was **52.076 N**, with limits **39.400 N** and **64.752 N**; **0** observations crossed them. The runs-test p-value was **0.795**, and the Anderson-Darling p-value was **0.380**. Thus the available sequence gives no signal of a time-order upset or nonnormality. This matters because the weakness is not explained by a few chart signals: the stable baseline itself is centred too low and too widely spread.

The baseline mean was below **55 N** with t statistic **-5.270** and p-value **0.00000202**. Lower capability against **45 N** was only **Cpk 0.558** and **Ppk 0.549**. The line therefore did not reliably meet the product specification and clearly missed the committed margin.

## What accounts for strength

The screening experiment used **16** observations over **3** factors with **2** replicates per treatment combination. The full factorial model had p-value **0.000142** and explained **94.912%** of response variation.

Increasing coded bond angle produced an estimated **4.386 N** effect with p-value **0.0000161**. Increasing coded bead spacing produced **3.081 N** with p-value **0.000200**. Their interaction contributed **2.193 N** with p-value **0.00179**, so the settings should be managed jointly rather than independently. Cure temperature's estimated effect was **0.182 N**, with p-value **0.713**; this experiment does not support it as a driver over the studied range.

## What the response-surface work supports

The quadratic model on **13** design runs explained **98.017%** of observed variation and had model p-value **0.00000832**. Both curvature terms were supported: bond-angle squared had p-value **0.00166**, and bead-spacing squared had p-value **0.00395**. The fitted stationary response was **64.587 N**, but its coded bond angle was **1.817**, outside the circular design radius of **1.414**; it is extrapolative and is not the recommended operating claim.

Within the circular design region, constrained optimization produced a candidate at coded bond angle **1.274** and coded bead spacing **0.614**, with predicted response **63.923 N** and prediction interval **60.719 N** to **67.127 N**. This is model guidance, not proof of production performance. The lack-of-fit p-value was **0.00190**, so the quadratic surface misses structure relative to centre-point repeatability and should not be used for unsupported extrapolation.

The archive says the confirmation seals were made at the recommended settings, but neither the released batch nor the process owner supplied the settings' identity or physical-unit mapping. Consequently, this report cannot state which physical setpoints were changed or prove that the implemented settings equal the computed coded candidate. That documentation gap must be closed before standard work is revised.

## What the change achieved

For the **20** confirmation seals, the mean was **59.275 N**, median **59.040 N**, and standard deviation **1.980 N**. Results ranged from **56.410 N** to **63.240 N**. There were **0** observations below **45 N** and **0** below **55 N**.

The confirmation I-MR limits were **53.352 N** and **65.198 N**, with **0** flagged observations. The runs-test p-value was **0.358**, and the normality p-value was **0.510**. These are encouraging short-run stability results, not evidence covering future shifts, materials, or operators.

Against **55 N**, the one-sided t statistic was **9.657** with p-value **0.00000000460**, supporting a mean above the programme requirement. Compared with baseline, the Welch t statistic was **10.142** with p-value **0.00000000000000223**. The variance test p-value was **0.00105**, supporting the use of the unequal-variance comparison.

## Hold plan and next action

* Freeze the recommended recipe pending verification, and place the actual bond-angle, bead-spacing, and cure-temperature setpoints under revision-controlled standard work. The missing setpoint identity is the immediate documentation action.
* Continue an individuals and moving-range chart using build order. Investigate chart signals and do not recalculate limits after an upset without cause review.
* Keep both requirements visible: **45 N** is the product lower specification; **55 N** is the programme margin. A passing short run against the first does not establish durable capability against the second.
* Extend confirmation across normal sources of variation before closure. Re-estimate capability against **55 N** only after stability is demonstrated on that broader sample.
* Because response-surface lack of fit is significant, augment or refit the design before moving beyond the studied region. Do not pursue the extrapolated stationary point on the present model.

**Disposition:** retain the improved condition under controlled verification. The project has demonstrated a substantial and statistically supported strength increase, but closure awaits documented setpoints and broader evidence of stable capability against the programme margin.
