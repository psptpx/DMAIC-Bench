# Method discipline predicts decision quality

Measured on the 97-task GLM-5.3-Flash campaign (`docs/archive/RESULT_GLM53FLASH_97.md`).

## The question this started as

`method_spam` — "methods were run that no node on the route calls for" — is present in **94 of
97** trials and `ms_precision` is 0.620 against `ms_recall` 0.968. Precision is one of four
axes in the harmonic mean, so if it were penalising legitimate professional behaviour the
pooled mean would be depressed for the wrong reason, and every published number with it. A
black belt who plots the data before deciding is not spamming.

So: is this axis measuring **competence** or **compliance**?

## The answer, and it is not the one I expected

Off-plan method count against `pq` (the fraction of a seed's decision points answered
correctly), over the 97 trials that have graded decision points:

| off-plan methods | n | mean pq | every decision right |
|---|---|---|---|
| 0–1 | 13 | 0.901 | **62%** |
| 2–3 | 30 | 0.614 | 33% |
| 4–5 | 37 | 0.542 | 11% |
| 6+ | 17 | 0.339 | **0%** |

**r = −0.462.** Monotone, and not one trial that ran six or more off-plan methods answered
every decision correctly.

The obvious objection is that a hard task invites flailing, so this is difficulty in disguise.
It is not — the correlation holds inside every tier, where difficulty is held roughly constant:

| tier | n | mean off-plan | r |
|---|---|---|---|
| A-proceed | 46 | 3.2 | −0.380 |
| B-divert | 20 | 5.8 | −0.414 |
| C-stop | 31 | 3.7 | −0.485 |

## Why the axis is not a compliance penalty

`ALWAYS_RELEVANT` already exempts the genuine precondition checks — data profiling, normality,
descriptive summary, equal variances, the runs test. Those are what a careful analyst runs
before committing to a method, and they cost nothing.

What is left, and what is actually being counted, is **substantive hypothesis testing the data
did not ask for**: two-sample t (40 instances), correlation (34), one-proportion (30),
one-sample t (30), one-way ANOVA (27), OLS (25), capability (21). Running a capability index on
a route that never established the process was stable is not exploration; it is the specific
error this benchmark was built to detect. Running every comparison you can think of until one
comes back significant is the thing a Six Sigma curriculum spends a chapter warning against.

So the axis stands, and the finding is stronger than the axis: **a system that cannot decide
what NOT to run also cannot decide where to go.** That is a claim about the model, measured,
and it is independent of whether the arithmetic was right — `ms_recall` is 0.968 throughout.

## What this does not show

Correlation inside a single model's trials. It does not establish direction: an agent that has
already lost the thread may flail, rather than flailing causing the loss. Separating those needs
either the hint protocol (does telling it where to look reduce off-plan work?) or a second model
with a different disposition. Both are cheap; neither has been run.
