# Gear-Shaft Heat-Treatment Line: Case-Surface Hardness vs. Recipe

**Task:** [TASK]  |  **Unit:** HRC  |  **Candidate cause under test:** the three heat-treat recipes in use

## Where the project stands

The recorded hardness readings can carry a conclusion, the baseline is stable, and the
comparison they admit says the heat-treat recipe is **not** a detectable cause of
case-surface hardness. No recipe change is justified by this data; the project should
redirect toward other candidate causes while holding the current process on the
control plan established here.

## 1. Can the readings carry a conclusion? Yes.

A crossed gage R&R study on the hardness tester (3 operators x 10 shafts x 3
replicates, tolerance 6.0 HRC) gave:

- **%GRR (study variation) = 16.85%** and **%GRR vs tolerance = 23.53%** — below the
  customary 30% ceiling for an acceptable gauge.
- **ndc = 8** distinct categories — above the minimum of 5.

The measurement system is adequate for the comparisons below. Both verdicts were
declared to the data steward (grr_pct = 16.849, ndc = 8), which released the
production data.

## 2. How has the baseline behaved? Stable, but not normal.

Sixty consecutive shafts in run order (one population):

- Mean **58.182 HRC**, median 57.945, std dev **0.741 HRC**, skewness 0.781.
- Individuals chart: center line 58.182, UCL 60.423, LCL 55.941, with **0 points out
  of control** (and 0 moving-range flags); a median-based **runs test p = 0.6025**
  shows no non-random pattern in run order.
- Normality fails: **Anderson-Darling p = 0.0004** (Shapiro-Wilk p = 0.0018). The
  distribution is mildly right-skewed, so every parametric comparison below was
  double-checked with a rank-based test.

The line is in statistical control at about 58.2 HRC. Any recipe effect would have
to be read against this stable background.

## 3. What comparison do the readings admit?

Fifteen shafts per recipe (A, B, C) were sampled separately. A median-centred
**Levene test p = 0.7807** says the three recipes' variances are indistinguishable,
so a one-way comparison of means is admissible; because the parent population is
non-normal, a Kruskal-Wallis test was run alongside.

## 4. What the comparison says: recipe is not the cause.

| recipe | mean (HRC) | std dev | median |
|---|---|---|---|
| A | 59.102 | 0.735 | 58.82 |
| B | 59.311 | 0.683 | 59.10 |
| C | 59.327 | 0.552 | 59.41 |

- **One-way ANOVA: F = 0.5404, p = 0.5865** — no recipe effect on hardness.
- **Kruskal-Wallis: p = 0.3678** — the non-parametric check agrees.
- Head-to-head of the two highest-averaging recipes (C vs B): mean difference
  **0.0153 HRC**, 95% CI [-0.449, 0.480], **two-sample t p = 0.9466**,
  Mann-Whitney p = 0.7874. Even the best two recipes are statistically
  indistinguishable.

Group means (59.1–59.3 HRC) sit slightly above the run-order baseline mean (58.2
HRC); with both comparisons far from significance, that gap is consistent with
sampling and the baseline's skew, not with a recipe effect.

## 5. What should happen next

1. **Close out recipe as the candidate cause.** Nothing in 45 per-recipe shafts or
   the 30-shaft head-to-head supports it; changing or tuning recipes is not expected
   to move hardness.
2. **Re-point the cause investigation** at factors not yet tested (e.g., material
   lot, prior machining, quench severity, furnace zone/atmosphere) and plan a
   designed experiment around them if they can be manipulated.
3. **Hold the gains:** keep the line on the individuals chart established here
   (CL 58.182, UCL 60.423, LCL 55.941 HRC) so any future shift is flagged against
   this stable baseline, and re-verify the tester with periodic gage studies
   (%GRR 16.85%, ndc 8 at this study).

## Data provenance

All figures above were computed in this run from steward batches: `define`, `msa`
(gage study), `baseline` (60 shafts in run order), `recipes` (15 shafts per recipe),
and `leading_two` (recipes C and B). No batch was denied or missing. No provision
turns were spent (0 of 26). Every number is traceable to a `steps[]` output in
`/workspace/trace.json`.
