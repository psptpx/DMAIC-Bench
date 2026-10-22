# Human baseline

Most agent benchmarks have no human anchor. Of the eight this one is calibrated against, only
MLE-bench (Kaggle medal thresholds) and PaperBench (eight ML PhDs, best@3 41.4% against o1's
26.6%) carry one, and both authors say plainly that it is the number reviewers ask for first.

This benchmark can offer a narrower but unusually direct anchor, because the routing decision it
scores is one that certified practitioners document in their own project reports.

## What was measured

A private corpus of **155 completed Six Sigma project reports** — black-belt and green-belt work
from electronics, machining, steel, display and process industries — was searched for projects
that ran a measurement-system analysis. **63 did.**

The question asked of each is the one the benchmark's hardest tier asks of a contestant:
*when the gauge study came back, which of the two AIAG MSA-4 acceptance criteria did the analyst
actually apply?* %StudyVariation is the familiar one. The number of distinct categories is the
other, and it is not optional: a gauge that cannot resolve five groups across the part spread
cannot be used to control the process however small its percentage reads.

| | projects | share |
|---|---|---|
| ran a measurement-system analysis | 63 | — |
| **applied the distinct-categories criterion** | **16** | **25%** |
| used the %GR&R screen alone | 47 | 75% |

**Three quarters of real projects stop at the first criterion.** That is the practice the
`gauge-unacceptable(resolution)` seeds reproduce.

## The trap is not a trap

Four tasks place the gauge in the band where the two criteria disagree — %StudyVariation under
the 30% limit, distinct categories at 4. It would be a fair objection that this is a
constructed gotcha, so it is worth recording that the corpus contains the same situation,
reached independently, and resolved correctly. One project's measurement-system conclusion reads
in full:

> %R&R = 29.30% < 30%
> P/T = 32.12 > 30%
> distinct categories = 4 < 5
> therefore this measurement system is not trustworthy. It needs improvement.

At 29.30% the distinct-category count is 4, and that analyst stopped the project at the gauge —
the same terminal branch the benchmark marks correct. **The situation occurs in real work, the
correct answer is the one the benchmark scores, and a practitioner reached it unaided.**

## What this licenses, and what it does not

It supports one claim: **the hardest tier asks something that defeats about three quarters of
documented professional practice and is nonetheless solved by practitioners unaided.** That is
the property a difficulty tier needs — hard, and demonstrably not impossible.

It is **not** a human score on this benchmark's tasks, and must never be reported as one. The
projects analysed are real work on their own data; nobody solved a DMAIC-Bench task. The
comparable quantity is the routing decision, not the reward. A number of the form "humans X% vs
models Y%" would require running practitioners on these tasks under the same harness, which has
not been done.

Three further limits are stated rather than left to be discovered:

- **The corpus is not public.** It is proprietary project documentation and is not redistributed
  with this benchmark. Only the derived counts above are published.
- **Presence in a report is the measurement.** A project that applied the criterion without
  writing it down is counted as not having applied it, so 25% is a floor on practice and the
  claim is stated in that direction.
- **The corpus is Chinese-language and industry-weighted** toward electronics and machining. It
  is evidence about a professional population, not a random sample of one.
