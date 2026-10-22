# Case-Surface Hardness on the Gear-Shaft Heat-Treat Line

**Task:** [TASK]
**Characteristic:** case-surface hardness, HRC
**Candidate cause under test:** heat-treat recipe (three recipes in use)
**Question put to us:** does the recipe account for case-surface hardness?

## Bottom line

The recipe does not account for case-surface hardness. The three recipes are
statistically indistinguishable (one-way ANOVA F = 0.0987, p = 0.9062), and recipe
accounts for 0.47% of the variation in the readings. Nothing about the recipe should be
changed on the strength of this study, because there is nothing here to change: switching
recipes would move the average hardness by a few hundredths of a point while the
shaft-to-shaft scatter within any one recipe is about 0.994 HRC.

The readings themselves are trustworthy, so this is a real negative result and not a
measurement artefact. The cause of hardness variation lies somewhere we have not yet
measured.

## 1. Can the readings carry a conclusion? Yes

Before testing the recipe we checked the hardness tester, using the archive study in which
3 operators measured the same 10 shafts 3 times each (90 readings), against a tolerance
width of 6.0 HRC.

Crossed gage R&R, ANOVA method:

| Measure | Result | Rule of thumb | Verdict |
|---|---|---|---|
| Total gage R&R, % study variation | 17.45% | under 30% | acceptable |
| Total gage R&R, % of tolerance | 27.50% | under 30% | acceptable |
| Number of distinct categories | 7.96 | 5 or more | acceptable |
| Part-to-part, % study variation | 98.47% | dominant | as it should be |

The part x operator interaction was not significant (p = 0.3942), so it was pooled into
repeatability in the standard way. Repeatability contributes 12.66% and reproducibility
12.00% of study variation, so the equipment and the operators contribute about equally to
measurement error. One caveat worth logging: the operator term is statistically detectable
(p = 0.0000000007), meaning the three operators do sit at slightly different levels
even though the total is inside the acceptance limits. This is small enough not to change
any conclusion below, and large enough to be worth a short refresher on fixture seating
and indent placement.

**Consequence:** the hardness readings can carry a conclusion, and the analysis proceeds.

## 2. How has the baseline behaved? Stable

Sixty consecutive shafts, recorded in the order run, one population:

- Average 58.946 HRC, median 58.890, standard deviation 1.094, range 57.060 to 61.630
- Mild right skew (0.410); normality is not rejected (Anderson-Darling p = 0.3059)

Individuals and moving-range chart (subgroup of 1, since shafts are measured one at a
time):

- Centre line 58.946, upper limit 61.913, lower limit 55.979
- **No individual reading falls outside the limits**, and no runs-rule pattern appears
- Runs test about the median p = 0.1182, so the run order shows no drift, trend or cycling
- **2 moving ranges exceed the moving-range upper limit of 3.645** (centre line 1.116)

Read this carefully, because the two chart halves say different things. The average is
stable: the process is not drifting or shifting. What the two moving-range signals flag is
an occasional large jump from one shaft to the very next one. That is exactly the
signature of a population that is being fed by more than one condition in an unplanned
sequence, which is precisely what this baseline is: 60 shafts from a line that runs three
recipes.

The short-term spread implied by the moving ranges (0.989) and the overall standard
deviation (1.094) are close, which tells us the variation is mostly common-cause,
shaft-to-shaft noise rather than a handful of special events.

## 3. What kind of comparison do these readings admit? A parametric one

The separate per-recipe sample gives 15 shafts under each of the three recipes (45 total).
We checked the two assumptions before choosing a test rather than after:

- Residuals are normal: Anderson-Darling p = 0.3978
- Variances are equal: Levene test, median-centred as the data steward specified,
  p = 0.8313

Both hold comfortably, so a one-way ANOVA is the admissible comparison, not a
distribution-free substitute. We ran Kruskal-Wallis anyway as a cross-check.

## 4. What does the comparison say about the recipe? Nothing to see

| Test | Statistic | p-value | Reading |
|---|---|---|---|
| One-way ANOVA | F = 0.0987 | 0.9062 | no recipe effect |
| Kruskal-Wallis | - | 0.9140 | agrees, distribution-free |

Recipe explains **0.47%** of the total variation. Total variance in the per-recipe sample
is 0.948 HRC-squared, and effectively all of it sits within recipes rather than between
them: pooled within-recipe standard deviation is 0.994 HRC. In plain terms, the gap
between the recipes is invisible against the scatter inside any one of them.

## 5. The two leading recipes, side by side, and why it settles nothing

The final batch presented the two recipes with the highest averages head to head. Two
facts about it need to be on the record.

First, we verified that these are **the identical 30 observations already supplied in the
per-recipe batch**, re-sliced. No new shafts were run and no new measurements were taken.

Second, the two recipes were selected *because* they ranked highest in that same data.
Testing the winners of a comparison on the data that made them winners is a post-hoc
comparison; it cannot confirm anything, and a small p-value here would have been an
artefact of the selection rather than evidence.

Computed anyway, for completeness:

- Difference between the two leading recipes: **+0.054 HRC**
- 95% confidence interval: **-0.661 to +0.769 HRC** - it straddles zero
- Two-sample t-test p = 0.8780; Mann-Whitney p = 0.7244
- Standardised effect size 0.057, i.e. negligible

Even taken at face value the result is null, and the interval tells us the honest
precision: the true gap could be two-thirds of a point in either direction. With 15 shafts
per arm this test could only have resolved a difference of about **1.01 HRC** at 80%
power, so it was never capable of separating recipes that sit 0.054 HRC apart. Do not read
a recipe ranking into these averages.

## 6. What we could not compute, and what that costs

**There is no capability study in this report, because there are no specification limits
for hardness.** The charter records the unit (HRC) and the goal, but no lower or upper
limit and no target. We asked the process owner twice; the process-fact register is empty
and both requests were refused. The 6.0 HRC figure attached to the measurement study is a
tolerance width used to express gage error as a percentage; it is not a two-sided
engineering specification and we will not treat it as one.

So Cp, Cpk, Pp and Ppk are all unavailable, and the conclusion stops there. We can state
that the process is stable and where it is centred; **we cannot state whether it is
capable, what the scrap or rework rate should be, or whether 58.946 HRC is even the right
place to be centred.** Anyone who quotes a capability figure for this line is quoting a
number that does not exist. Closing this gap is the single cheapest thing the plant can do
for this project.

## 7. Where the project stands and what happens next

**Where things stand.** Hardness averages 58.946 HRC with a standard deviation of 1.094
and the process is in statistical control on the average. The measurement system is fit
for the job (17.45% of study variation).

**What is causing it.** Not the recipe. That is the finding, and it is a useful one: it
clears the candidate that was on the table and stops the team from spending money
re-qualifying recipes. The variation is common-cause and lives inside each recipe, with
the occasional adjacent-shaft jump the moving-range chart caught twice.

**What was changed.** Nothing, deliberately. No process change is justified by a factor
that explains 0.47% of the variation, and no recipe should be retired or standardised on
the basis of a 0.054 HRC gap. Acting on this ranking would be acting on noise.

**What the change achieved.** Not applicable, since nothing was changed. There is no
before-and-after to report, and we are not going to manufacture one.

**What should happen next**, in priority order:

1. **Get the specification.** Have engineering issue the hardness limits and target. Until
   that exists, capability cannot be assessed and the project has no way to say whether
   the current average is acceptable.
2. **Look for the real cause with a designed study.** The candidate list should now cover
   the things that change shaft to shaft and were never recorded here: furnace or quench
   position, incoming bar lot and its chemistry, fixture location in the load, quench bath
   temperature and agitation, and shift. Note that the process-fact register was empty, so
   this list is our engineering judgement and not something we were able to confirm with
   the process owner.
3. **Size the next study properly.** The comparison we were handed could only resolve about
   1.01 HRC. If differences of a few tenths of an HRC matter commercially, future sampling
   plans need to be built around that resolution before data is collected, not after.
4. **Chase the two moving-range signals** at their shafts in the run record and find what
   was different about those adjacent pairs; they are the clearest lead in the baseline.
5. **Tighten operator technique.** The operator effect in the gage study was detectable
   even though the system passed. A short standardisation of fixture seating and indent
   placement will shrink measurement error and make the next study more sensitive.

**How it will be held.** Keep the individuals and moving-range chart running on hardness
with the limits established here (centre 58.946, 61.913 and 55.979), so any real shift is
caught against a known-stable baseline, and re-run the gage study on the usual annual
cycle or whenever the tester is serviced. Once specification limits arrive, add a
capability review to the same cadence.

---

*Every figure in this report comes from a computation run on this data and recorded in
`/workspace/trace.json`. Where a number could not be computed, the gap is stated rather
than filled.*
