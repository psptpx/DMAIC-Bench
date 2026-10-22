# Appearance defects on the rod line - project report

Charter commitment: no more than 1500 defective units per million inspected.

## Headline

The line is stable and, on the numbers as they are currently inspected, it is
inside the charter: 1016 DPMO against a commitment of 1500.

That result cannot be relied on, because the sound/defective judgement that produced
it does not pass a measurement check. Fixing the inspection is the first job on this
project; until it is fixed, every rate below is provisional.

## 1. Can a sound/defective judgement be relied on? No.

Three inspectors judged 20 retained units twice each against an agreed answer key.

| | repeat own call | matches the key |
|---|---|---|
| inspector 1 | 85% | 70% |
| inspector 2 | 70% | 55% |
| inspector 3 | 55% | 50% |

- all three inspectors agree with each other on **30%** of units
- all three agree *and* match the key on **30%** of units
- Cohen kappa against the key: 0.541, 0.348, 0.415 - worst **0.348**

The usual acceptability floor for kappa is 0.75, with 0.90 wanted for a judgement used
to accept or reject product. The worst inspector sits at 0.348 and the best at 0.541, so
none of them clears it. One inspector repeats their own call on only 55% of units,
which means the same unit shipped or scrapped depends on who looks at it and when.

This is corroborated by the risk ratings: the highest-risk failure mode is "stain"
at RPN 504, and what drives it is a detection rating of 8 - the plant already suspects
this defect is not reliably caught.

**Consequence for the rest of this report:** with a gauge this noisy, the measured
defective rate is a blend of real defects and inspection error, and it can sit either
side of the truth. Escapes and false scrap are both in play. Do not treat the pass
against the charter as banked.

## 2. Has the defective share held steady? Yes.

Twenty-five consecutive lots, 5,000 units each, 125000 inspected in total, 127 judged
defective. A p chart puts the centre line at 1016 DPMO with an upper limit of about
11.8 defectives in a lot of 5,000. **0 lots of 25 fall outside the limits.**

Lots range from 400 to 2200 DPMO, and all of that is common-cause variation. There is
no upset to hunt down and no point chasing individual bad lots - the variation is the
process behaving normally. To move the level you have to change the process itself.

## 3. How does today compare with the commitment?

- observed: **1016 DPMO** (process Z = 3.09)
- committed: 1500 DPMO
- exact binomial test against the commitment: p = 3.34e-06
- 95% confidence interval: **847 to 1209 DPMO**

The whole interval sits below 1500, so this is a real margin and not a lucky sample -
subject to section 1. Note the margin is not large: the worst single lot in the record
ran 2200 DPMO, above the commitment on its own.

## 4. What is causing the defectives?

Two things were checked.

**Reject categories.** 240 rejects across 5 categories; the largest, "loose end", is only
**26.7%** of the total. There is no dominant defect to attack - the classic Pareto
80/20 shape is absent here, so a single-category project would leave most of the
problem untouched.

**Machines.** Over one common window, 4,000 units per machine:

| machine | defective rate |
|---|---|
| machine 1 | 1250 DPMO |
| machine 2 | 0 DPMO |
| machine 3 | 750 DPMO |
| machine 4 | 2000 DPMO |

Chi-square = 8.51 on 3 degrees of freedom, p = 0.0366: the machines are **not** all
running the same defective rate. machine 4 is the worst at 2000 DPMO, machine 2 produced none.

Read this cautiously. The smallest expected count in the table is 4.0, below the 5
that the chi-square approximation wants, and the whole result rests on 16 defective
units. It is a credible lead, not a proven cause - and if inspection is unreliable,
part of the machine-to-machine spread may be which inspector covered which machine.

## 5. What was changed, and what did it achieve?

One machine was changed, and its counts either side are on record:

- before: 6 defective in 4000 inspected (1500 DPMO)
- after: 9 defective in 4000 inspected (2250 DPMO)

The rate went **up**, not down, and the difference is not statistically significant
(z = 0.78, p = 0.438; Fisher exact p = 0.607).

**No improvement has been demonstrated. The change cannot be credited with any gain.**

The trial also could not have proved success even if the change had worked. At 4,000
units a side, power against the observed effect is 0.122, and even a genuine **halving**
of the before-rate would have been detected only 17% of the time. So the null result
is uninformative rather than evidence that the change did nothing - the trial was too
small to settle the question either way. At rates near 1,000 DPMO a fair test needs
tens of thousands of units per side, or a measured variable instead of a pass/fail call.

**What the change physically was, I cannot report.** I asked the process owner and no
process facts are recorded for this project, so the record shows a change with no
description of what was done to which machine. That is a gap in the project record,
not something I will fill with a guess - and it means the change is not reproducible
even if it had worked.

## 6. How is it being held?

The monitoring record since the change covers 20 subgroups of 5,000, 100000 units, 107
defective:

- centre line **1070 DPMO**, process Z = 3.07
- **0 of 20 subgroups outside the control limits** - in control
- worst subgroup 2400 DPMO
- still below the commitment: p = 2.71e-04, 95% CI 877 to 1293 DPMO

Against the baseline: 1016 DPMO before, 1070 DPMO since (z = 0.39, p = 0.693).
**No significant difference - the line is exactly where it started.** The monitoring
record shows a process being held, not improved.

## 7. Where this project stands, and what to do next

Position: stable, inside the charter as inspected, with no demonstrated improvement
and an inspection system that is not fit to certify any of it.

1. **Fix the appearance judgement first.** Written standard with boundary samples for
   each reject category, retrain and requalify all three inspectors, then repeat this
   study and require kappa at or above 0.90 before trusting any rate. Everything else
   on this project is waiting on this; the current worst kappa is 0.348.
2. **Do not roll out the machine change.** It showed 1500 DPMO going to 2250 DPMO with
   power of 0.122. Get the change documented, then retest properly once inspection is
   trustworthy, sized to the effect you actually need to see.
3. **Keep machine 4 as the lead** (2000 DPMO against 0 on machine 2), but confirm it on a bigger
   window after the gauge is fixed, and make sure inspector is not confounded with
   machine when you do.
4. **Hold with the p chart** at a centre line of 1070 DPMO and react to points outside
   the limits rather than to ordinary lot-to-lot movement. Recompute the limits once
   inspection has been requalified, because today's centre line partly reflects
   measurement error.
5. **Do not run a single-category improvement** on the current tally: the biggest
   category is 26.7% of rejects, so the gain available is limited. Revisit the split
   after requalification, since some of the current categorisation is unreliable too.

## Data I could not obtain

All seven data batches held by the steward were released and analysed; none was denied.
The process owner holds no process facts for this project, so two questions went
unanswered: what the change to the machine actually was, and whether inspectors work to
a written standard with boundary samples. Both are stated as gaps above rather than
assumed. Every number in this report is computed on this run and traceable to
`/workspace/trace.json`.
