# What the contestant asked the steward for, and why it was refused

Measured on the GLM-5.3-Flash campaign (`harbor/jobs/glm53flash-final95` +
`glm53flash-fill`), from the steward audit logs of all 95 tasks. Written to correct an
earlier claim in this repository that these trajectories no longer existed — they do; the
job store is `harbor/jobs/`, which is gitignored and therefore invisible to `git status`.

## The numbers

| | count | share of requests |
|---|---|---|
| requests | 549 | — |
| refused `unroutable` | 91 | 16.6% |
| refused `locked` (a methodology gate) | 21 | 3.8% |

A `request` is **never metered** — 1097 request entries across every job, all
`metered: false`; only `provision` spends the turn budget. So a refusal costs latency and
context, not the task's budget.

## The 91, classified

For every unroutable request, the question asked was: would ANY stage of that task have
matched this text, on its own topics, its `stage_id`, or its label? (`_route` carries all
three, lowercased.)

| | count |
|---|---|
| asked for data the task does not hold | **90** |
| a stage would have matched — a real routing miss | **1** |

And the one is not one. It is `adb_c34-T3-s3-clean` asking for *"Control-phase monitoring
data or control plan for coating thickness"*, which matches the `sustaining` batch — a batch
**added on 2026-09-12**, after that campaign ran. At the time it was refused, it did not
exist. **The genuine routing-miss count is zero.**

## What the 90 were actually asking for

> *"Post-change hardness readings after implementing the selected recipe"*
> *"Improvement intervention implementation and post-change breach results"*
> *"Root cause and process-change data for the bore finish improvement"*
> *"Improvement change and post-change verification data for coating thickness"*

Roughly one per task, across almost every case. The contestant walks Measure and Analyze,
reaches the point where a black belt would implement something and prove it held, and asks
for the batch that would let it — and the corpus has no such batch.

**This is the phase-coverage gap, measured from the other side.** The ratchet in
`tests/test_v2_phase_coverage.py` counts it as authored grading (Improve 17 graded acts;
Control was 0 until `adb_c32` and `adb_c34` were extended). The audit logs show the same gap
as contestant behaviour: the model is not failing to find the data, it is asking for a phase
the benchmark does not carry. Two independent measurements of one thing.

It is also the answer to "is the router the problem". It is not. What looks like 17% of
requests failing to route is 16% of requests asking a question the corpus cannot answer,
and it is the corpus that should change.
