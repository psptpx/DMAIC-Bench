# Where the hardest tier lands

Measured on the 40-task corpus, after G3 passed 40/40. **The corpus has since grown to 95
tasks over 15 projects and no model has been run on the 55 new ones** — see the corpus
expansion section of `docs/EXPERIMENT_PLAN.md`. Every number on this page refers to the 40-task
build; the stop tier it reports as 12 tasks is 33 in the current corpus. The number that matters for a
difficulty claim is the **tier**, not a pooled corpus mean, following CORE-Bench — which reports
Easy 60.0% / Medium 57.8% / **Hard 21.5%** and never averages them together.

## C-stop, 12 tasks

| model | gateway | n | mean | pq | sc | zero-rate |
|---|---|---|---|---|---|---|
| gpt-5.6-luna | root | 12 | 0.280 | 0.333 | 0.333 | 67% |
| gpt-6-astra | root | 12 | 0.231 | 0.333 | 0.333 | 75% |
| gpt-5.6-sol | root | 12 | 0.217 | 0.250 | 0.250 | 75% |
| sonnet-5 | anthropic-gateway | 7 | 0.229 | 0.286 | 0.286 | 71% |

**Pooled over the three complete runs: 0.243 — inside the 20–30% band** the calibration targets.
sonnet-5 is reported as a partial run and excluded from the pooled figure; opus-5 and fable-5.1
could not be run at all, because their gateway returned `INSUFFICIENT_BALANCE` part-way through.
That is an operational loss, disclosed here rather than averaged away.

## The pooled corpus mean is not the number

Reported so it cannot be mistaken for a failure to hit the target: **the pooled mean over all 40
tasks cannot reach 20–30% and the arithmetic says so.** Twenty-one A-proceed tasks at roughly
0.749 contribute about 15.7 points that no amount of C-stop dilution removes — reaching a pooled
0.30 while keeping them would need on the order of **97** C-stop tasks. Either the easy tier
shrinks or the headline is per tier. It is per tier, which is also what the literature does.

## The distinct-categories trap

Four of the twelve tasks put %StudyVariation under the 30% screen while the number of distinct
categories lands on 4, so the gauge passes the familiar criterion and is still unusable.

| model | the four trap tasks | mean |
|---|---|---|
| gpt-6-astra | 0.000 · 0.000 · 0.000 · 0.000 | 0.000 |
| gpt-5.6-sol | 0.000 · 0.000 · 0.000 · 0.000 | 0.000 |
| gpt-5.6-luna | 0.000 · 0.000 · 0.000 · 0.000 | 0.000 |

**Twelve trials, twelve zeros.** Every model checked the percentage, saw a number below 30, and
proceeded to an analysis it had no basis for.

This is the one result that needs its guard stated with it. A task no system solves carries
difficulty and no discrimination, and four such tasks are exactly the shape this benchmark was
warned about by SWE-bench's floor. Three things keep them defensible rather than decorative:

- **the oracle scores 1.000 on all four**, and does so through the behaviour-based route, not by
  naming a private key — G3 was re-run on the whole corpus for this;
- **both admissible conventions agree** that the gauge fails, which is a property now pinned by
  test, and which G3 caught being false on an earlier draft;
- **practitioners solve it.** `HUMAN_BASELINE.md` records a real project that met the same
  situation at 29.30% GR&R, computed 4 distinct categories, and stopped. 25% of documented MSA
  projects apply the criterion at all.

So the four tasks are hard, solvable, and currently unsolved by every model measured. They are
reported as a named subset with their own count, never folded silently into a tier mean.

**All three of those guards are static.** They are properties of the task — what the oracle
scores, what the conventions agree on, what a human project once did — and none of them is an
observation of a contestant behaving differently when the obstacle is removed. That is the
difference between "not known to be broken" and "shown to be hard", and this benchmark has
already paid once for treating the first as the second: nine tasks floored at 0.000 beside
`ms_recall` 1.000 were reported as difficulty and were unscoreable.

The missing dynamic evidence is a hint probe, and it has now been run. `hp01`, four tasks, three
rungs, GLM-5.3-Flash, k = 1: **twelve trials, twelve zeros, the gauge decision answered wrongly
in every one — including under the rung that states the criterion and its threshold outright.**

Under that rung the contestant obtained ndc = 4, quoted it correctly (both numeric truths passed,
`ms_recall` 1.000, `nf` 1.000, no gate violation) and then reported Cpk 1.94 on the gauge it had
just measured as unusable. Every axis but one at its maximum, and `pq` at 0.000.

So the four tasks are hard for a reason that is now evidenced rather than argued: it is not that
the criterion is unknown, and not that the environment is broken. It is that a contestant which
can compute, state and quote the criterion does not act on it. Full protocol, the outcome table
this result forced open, and why these four are deliberately ungated: `docs/archive/HINT_PROTOCOL.md`.

One qualification the probe cannot remove: this is one model at k = 1. "No system yet measured
solves these" remains the claim; "no system can" is not.

## Discrimination inside the tier

The tier is not a flat floor. Two tasks separate the models in opposite directions —
`adb_c27-t3-s4` is solved by gpt-6-astra (0.889) and failed by both others, while
`adb_c28-t3-s4` is solved by gpt-5.6-sol and gpt-5.6-luna (1.000) and failed by gpt-6-astra. Four
of the twelve are solved by at least one model and failed by at least one other.

## What this does not support

- **A ranking.** Three models over twelve tasks nested in six cases, at k = 1. The spread
  between them (0.217 to 0.280) is well inside what run-to-run variance could produce, and
  run-to-run variance is not estimable from this data at all — see the k = 1 deviation in
  `EXPERIMENT_PLAN.md`.
- **A pass^k or reliability claim.** Same reason: one attempt per task.
- **A cross-tier pooled figure**, for the arithmetic given above.
