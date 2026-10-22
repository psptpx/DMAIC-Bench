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
