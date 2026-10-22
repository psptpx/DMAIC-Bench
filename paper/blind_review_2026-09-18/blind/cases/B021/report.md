# Seal-strength programme report

## Executive conclusion

The baseline was stable but not capable. Bead spacing and bond angle accounted for much of the seal-strength variation; cure temperature did not. The composite design found an interior maximum, and seals made at the recommended settings improved materially. The confirmation evidence supports an average above the 55 N programme level and all confirmations above the 45 N LSL, but it does not yet prove comfortable 55 N margin for every future seal. Retain the optimised settings, obtain their missing engineering-unit decoding, and run routine I-MR control with capability review.

## Baseline: stable, common-cause underperformance

The ordered baseline contained 60 consecutive assemblies. Mean strength was 52.094833333333334 N, standard deviation was 4.669088936524463 N, minimum was 42.88 N, and maximum was 62.92 N. Normality was plausible (Anderson-Darling p = 0.36524649441978).

Against the 45 N LSL, 3 of 60 seals failed, an observed rate of 0.05000000000000000 or 50000.0 ppm. Cpk was 0.5870748953681952 and Ppk was 0.5065109010763119. The mean was above 45 N (t = 11.77024970724641, p = 2.0234447467079495e-17), but that did not make the process capable.

Only 19 assemblies exceeded the 55 N programme level. The baseline mean was below 55 N by a mean difference of -2.9051666666666662 N (t = -4.819639236228526, p = 5.230000328573192e-06).

The I chart had no flags; its limits were 40.009776742923904 to 64.17988992374276 N around 52.094833333333334 N. The moving-range chart also had no flags. Build-order correlation was not significant (r = -0.16833660057447283, p = 0.19854861618027705). Thus, the shortfall was chronic common-cause performance rather than a visible drift or special cause.

## What settings account for the strength difference

The screening experiment had 16 runs, 3 factors, 8 corners, and 2 replicates per corner. Its saturated coded full-factorial model was significant (F = 16.716112044324973, p = 0.0003450875084604319) and explained 93.60065448974846 percent of the observed variation (adjusted R-squared 88.00122716827839).

Bead spacing and bond angle were the important factors. The coded bead-spacing coefficient was 1.8286875000000007 N (p = 0.00031595270060478386); bond angle was 2.4850625 N (p = 3.7126308417584755e-05). Their interaction was also significant at 0.8846875000000102 N (p = 0.01950483494675). Cure temperature explained essentially nothing over the tested range (coefficient -0.05793750000000007 N, p = 0.8534673068258805), so it was not carried into the composite design as a setting to optimise.

The full 2^3 model was saturated: replicate pure error had 8 degrees of freedom, but lack of fit had 0 degrees of freedom. A screening lack-of-fit p-value therefore could not be computed and was not invented.

## What the composite design supports

The later design had 13 runs, 2 factors, 4 factorial points, 4 axial points, and 5 centre points. The full quadratic model was significant (p = 3.4224870950181055e-08), explained 99.58951944089024 percent of variation, and showed no detectable lack of fit (p = 0.5749941911405526; pure-error degrees of freedom = 4).

Canonical analysis found an interior maximum at coded bead spacing +0.7447278722018995 and coded bond angle +0.760465778391156. Both canonical eigenvalues were negative (-2.2258314214714137 and -1.406663585100884), confirming a maximum rather than a saddle or minimum. The fitted mean at that point was 59.72149535420359 N, with a 95 percent prediction interval of 58.954156544674305 to 60.488834163732875 N.

The process owner supplied no matching fact for converting coded settings to engineering units. That conversion is missing, so this report must stop at coded setpoints rather than invent centre values and increments for bead spacing or bond angle.

## What the change achieved

The confirmation run contained 20 seals. Its mean was 58.60699999999999 N, median 58.68 N, standard deviation 1.9345504033645384 N, minimum 54.62 N, and maximum 61.71 N. Normality was plausible (Anderson-Darling p = 0.8687109326852228).

The confirmation mean was above 55 N by 3.606999999999992 N (t = 8.338368626440896, p = 4.5046555198870935e-08). Its one-sided 95 percent lower confidence bound for the mean was 57.8590141132427 N. 19 of 20 seals were strictly above 55 N; the remaining seal was 54.62 N.

No seal was below the 45 N LSL. Cpk was 1.9423819445199073 and Ppk was 2.344558538654928. The exact 95 percent interval for the underlying below-45 fraction was 0.0 to 0.16843347098308536; zero failures in 20 runs is encouraging but does not prove a failure rate below the baseline 0.05000000000000000 (one-sided exact test p = 0.35848592240854227). A normal-model estimate gave 1.0058125011551945e-06 ppm below 45 N, whereas the observed estimate was 0.0 ppm; the exact bound is the safer business interpretation.

The confirmation I chart had no flags; limits were 51.601683646854426 to 65.61231635314556 N around 58.60699999999999 N. The moving-range chart also had no flags. Run-order correlation was not significant (r = 0.1811416453573467, p = 0.44469752635589777).

Relative to baseline, mean strength increased by 6.512166666666658 N (Welch t = 8.777301128712697, p = 2.1328724262487247e-13). Variation also fell significantly (Levene statistic = 14.68143595055583, p = 0.0002560745937069128). The confirmation mean was -1.1144953542035978 N relative to the RSM point prediction (two-sided t = -2.5763995275313096, p = 0.018492204349091212), although it remained inside the model's 95 percent prediction interval.

## Where this leaves the programme

- **45 N product requirement:** the changed settings are strongly supported. Every confirmation seal exceeded 45 N, the I and moving-range charts were stable, and Cpk/Ppk were above the baseline values.
- **55 N programme margin:** the evidence supports an average above 55 N, but not yet a demonstrated high-margin capability at 55 N. The confirmation minimum was 54.62 N, and the within- and overall-variable 55 N margin indices were only 0.5148946625915555 and 0.621505302339113 respectively.
- **Cause and improvement:** bead spacing and bond angle, including their interaction, explain the design response; the confirmation run independently showed a large mean increase and lower variation. This is strong empirical support that those settings matter, not proof that no other process variable can ever matter.
- **Implementation gap:** engineering-unit centres and increments are unavailable. A physical setting sheet cannot responsibly be issued from coded values alone, so implementation stops at that conversion.

## Recommended next actions

- Obtain and document the engineering-unit decoding for coded bead spacing and bond angle, then issue the exact setpoints and permitted setting ranges.
- Keep the optimised bead-spacing and bond-angle settings under change control. Do not change cure temperature on this evidence: it was not significant over the tested range, but that does not prove it is irrelevant outside that range.
- Run routine I-MR control for seal strength. Investigate any I or moving-range signal, drift, or adjustment; do not reset the chart without an assigned cause.
- Track both the 45 N nonconformance rate and performance against 55 N. Use exact count evidence as well as normal capability estimates, because the confirmation sample had zero LSL failures but its upper confidence bound for the underlying failure fraction was still high.
- Extend capability review on routine production data before relaxing inspection or claiming long-term margin. Recalculate limits and indices only from an in-control, current process period.
- Add measurement-system evidence before using the chart for acceptance decisions. No measurement-system analysis batch was among the released data, so gauge adequacy cannot be concluded here.

## Data and computation limitations

No screening lack-of-fit p-value was computed because the saturated design had no lack-of-fit degrees of freedom. The composite design did provide a valid lack-of-fit test. Engineering-unit decoding was requested but no matching process fact was available; coded values are therefore the furthest implementable setting statement. The confirmation prediction difference is small enough to retain the model for direction, but the observed mean should supersede the fitted point prediction for production planning.
