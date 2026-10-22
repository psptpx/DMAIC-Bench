# Case-surface hardness and the heat-treat recipe

**Project:** [TASK] — gear-shaft heat-treatment line
**Characteristic:** case-surface hardness (HRC) **Candidate cause:** heat-treat recipe (three in use)
**Question put to us:** does the recipe account for case-surface hardness?

## Headline

The recipe accounts for case-surface hardness, and the evidence is strong: recipe explains
**71.4%** of the hardness variation in the sampled readings (one-way ANOVA F = **52.43**,
p = **3.8e-12**). The three recipes sit on three distinct hardness levels — recipe A
**57.96 HRC**, recipe B **59.74 HRC**, recipe C **61.33 HRC** — and every pairwise gap is
real, not noise.

Two things this project cannot yet claim, and the report says so rather than filling the gap:
there is **no specification for hardness**, so no capability index was computed; and the
"improvement" sample turned out to be the same readings we had already analysed, so **no
independent confirmation that a change was made and held exists**.

## 1. Can the readings carry a conclusion? Yes — the tester is fit for this decision

Before trusting any hardness number we checked the hardness tester itself, using the archived
study: 3 operators, 10 shafts, 3 repeats each, 90 readings. Crossed Gage R&R by the ANOVA
method (the operator x shaft interaction, p = **0.152**, was retained under the usual pooling
rule):

| measure | result | verdict |
|---|---|---|
| Total gage R&R, % of study variation | **12.70%** | acceptable (under 30%) |
| Total gage R&R, % of the 6.0 HRC gage-study tolerance | **21.61%** | acceptable |
| % contribution to variance | **1.61%** | acceptable |
| Number of distinct categories | **11** | acceptable (5 or more) |
| Shaft-to-shaft signal, % of study variation | **99.19%** | the readings are dominated by real part differences |

Repeatability (**10.98%**) is the larger of the two error terms; reproducibility between
operators is **6.39%**. The operator effect is statistically detectable (p = **0.017**) but so
small in magnitude that it does not threaten a decision about recipe. Gage R&R standard
deviation is **0.216 HRC** against recipe differences of **1.58 to 3.37 HRC** — the measurement
system resolves the effect we care about with room to spare.

**This was the gate on the rest of the project, and it passed.** Everything below rests on it.

## 2. How has the baseline behaved? It is not one process — it is two

Sixty consecutive shafts were recorded in run order and handed to us as "one population". They
are not.

- Individuals chart (sigma from the mean moving range **1.457**, within-sigma **1.291**):
  centre line **60.63 HRC**, limits **56.76** to **64.51 HRC**. **2** points fall outside the
  limits and **49** of the 60 points are flagged once run rules are applied.
- Runs test about the median: **10** runs observed where **31** were expected, z = **-5.47**,
  p = **4.5e-08**. The order in which shafts were run is carrying a signal.
- The first 30 shafts average **58.66 HRC**; the last 30 average **62.61 HRC**. That is a
  sustained step of **3.94 HRC** partway through the run, not drift and not scatter.
- The distribution fails normality (Anderson-Darling p = **0.024**) with essentially zero skew
  (**-0.05**) but kurtosis of **-1.21**. A flat, short-tailed shape like that is the signature
  of two levels mixed together, not of a skewed single population. Overall spread
  (SD **2.30 HRC**) is inflated by the step; within a single recipe the spread is only about
  **0.90 HRC** (pooled SD, section 4).

**What this means for the plant:** the baseline record is unstable, so its average and its
spread describe a mixture, not a process. Any capability number calculated from these 60
shafts would be meaningless, and the "one population" label on this record should be corrected.

The step of **3.94 HRC** is close in size to the total spread between recipes, **3.37 HRC**
(recipe A to recipe C). That is consistent with the run-order record spanning more than one
recipe — the same cause showing up in time order. We asked the process owner whether a known
process event, such as a recipe change, occurred around the thirtieth shaft. **No process facts
are recorded for this project**, so the question came back unanswered. We are therefore
reporting the step as an unexplained special cause with a plausible link to recipe, not as a
confirmed recipe change.

## 3. What kind of comparison do these readings admit? A parametric one

The separate per-recipe sample is 15 readings per recipe, 45 in total, and it is well behaved —
unlike the run-order record:

- Anderson-Darling on the one-way model residuals: p = **0.067**. Each group individually also
  passes: recipe A **0.080**, recipe B **0.201**, recipe C **0.413**.
- Equal variances by Levene centred at the median (the centering this batch specifies):
  p = **0.976**. Group standard deviations are **0.909**, **0.928** and **0.866 HRC** —
  practically identical.

Both assumptions hold, so the correct comparison is a **pooled-variance one-way ANOVA**, and we
are entitled to use it rather than fall back to a rank test. We ran the rank test anyway as a
cross-check.

## 4. What does the comparison say about the recipe? It is the cause

One-way ANOVA across the three recipes:

| term | value |
|---|---|
| F statistic | **52.43** |
| p value | **3.8e-12** |
| R-squared | **71.4%** |
| Pooled within-recipe SD | **0.901 HRC** |
| Total variance | **2.711 HRC²** (between recipes **85.18**, within **34.12**, total **119.29** sum of squares) |

Kruskal-Wallis, which assumes nothing about shape, agrees: p = **6.7e-08**. The conclusion does
not hinge on the normality assumption.

All three recipes separate cleanly (Tukey, family-wise controlled):

| comparison | difference (HRC) | p |
|---|---|---|
| A vs B | **1.784** | **7.9e-06** |
| B vs C | **1.584** | **5.7e-05** |
| A vs C | **3.368** | **1.7e-12** |

**Recipe C is the highest-hardness recipe, recipe A the lowest, and the ladder is ordered
A < B < C.** Recipe is not one contributor among many here: it accounts for **71.4%** of the
variation, leaving **28.6%** to everything else on the line. That is the answer to the question
the charter asked.

### The two leading recipes, head to head

Recipe C against recipe B, two-sample t (Welch, 27.9 df — variances were equal, Levene
p = **0.933**, so the pooled and Welch results coincide):

- Recipe C **61.33 HRC** vs recipe B **59.74 HRC**
- Difference **1.584 HRC**, 95% confidence interval **0.913 to 2.255 HRC**
- t = **4.834**, p = **4.4e-05**, Cohen's d = **1.77**
- Mann-Whitney confirms distribution-free: p = **2.6e-04**

The gain from moving B to C is real and its size is bounded: at worst about **0.9 HRC**, at
best about **2.3 HRC**.

## 5. Where the evidence stops — read this before acting

**No capability index. No specification exists.** We could not compute Cp, Cpk, Pp or Ppk and
have reported none. The charter batch carries only the candidate, the goal and the unit (HRC).
Our request for specification limits was refused — the data does not exist — and the process
owner holds no process facts (both questions we spent came back with nothing recorded). The
6.0 HRC figure used in section 1 is the **gage study's** tolerance for judging the tester; it
is not a product spec window and we did not reuse it as one. **Consequence: we can say which
recipe gives the highest hardness, but not whether any recipe meets the customer's
requirement.** That conclusion stops here until engineering supplies the limits.

**No verification that a change was made.** The batch presented as the improvement-phase
sample — the two recipes with the highest averages, side by side — is **element-wise identical**
to the recipe C and recipe B columns of the analysis sample we had already used. We checked this
directly rather than assuming it. It is a re-cut of the same 30 readings, so it quantifies the
gap between the leading two recipes; it does **not** independently confirm that recipe C was
implemented on the line or that hardness improved afterwards. There is no post-change data in
this project.

**No control data.** No control plan or post-change monitoring data was released either. The
hold step below is a recommendation, not something we can report as achieved.

**No explanation for the baseline step.** As noted in section 2, no process event log exists.

## 6. Where this leaves the business, and what to do next

**Where things stand.** The hardness tester is trustworthy for this decision (**12.70%** study
variation, **11** distinct categories). The baseline record is out of control — a **3.94 HRC**
step splits it in two — so the line has not been running as one process. Recipe is the cause of
the hardness differences, at **71.4%** of the variation, with recipe C the strongest at
**61.33 HRC**.

**What is causing it.** The heat-treat recipe. Three recipes in simultaneous use put the same
part on three different hardness levels spanning **3.37 HRC**, and the mixed baseline is what a
plant looks like when it lets that happen unmanaged.

**What was changed, and what the change achieved.** Nothing yet, and this is the honest
position: no implementation and no post-change data exist in this project. What we have is the
evidence to justify a change and a bounded estimate of its size — standardising on recipe C
should lift hardness by **1.584 HRC** over recipe B (95% CI **0.913 to 2.255**) and by
**3.368 HRC** over recipe A.

**Recommended next steps, in order:**

1. **Get the specification.** Until engineering supplies the hardness limits, "higher" cannot
   be converted into "conforming". This is the single biggest gap and it blocks any capability
   claim.
2. **Standardise on one recipe and stop running three.** On hardness alone recipe C is the
   choice. Confirm with metallurgy that higher case hardness is desirable here and not a
   trade-off against core toughness or distortion before locking it in — our data speaks only
   to hardness.
3. **Run a confirmation batch after the change and chart it.** This is the step the current
   data cannot substitute for. Judge it against the within-recipe spread of **0.901 HRC**,
   which is the right yardstick, not the inflated baseline SD of **2.30 HRC**.
4. **How it will be held.** Put recipe selection under change control and run an individuals
   chart on case hardness. Once a single recipe is in force, limits recomputed on
   within-recipe variation will be roughly three sigma of **0.901 HRC** wide — far tighter than
   the **56.76 to 64.51 HRC** limits the mixed baseline produced. The run rules that flagged
   **49** of 60 baseline points are exactly what will catch an unauthorised recipe change next
   time.
5. **Keep an eye on repeatability.** At **10.98%** of study variation it is the larger part of
   gage error. It is not a problem today, but it is where the tester will degrade first.

Every figure in this report comes from a computation recorded in `trace.json`.
