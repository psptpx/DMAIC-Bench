# Scoring

What the number means, what it cannot mean, and which parts of it are measured rather than
taken on the contestant's word.

---

## The reward

```
reward = harmonic_mean(axis for axis in (ms_recall, ms_precision, nf, pq) if axis_is_measured)
         * (1 - ms_misuse)
         * gate_hard_passed
```

The scalar is a **competence term** with two gates applied from outside it. Four axes go inside
the harmonic mean; the harmonic mean is used so no axis can be bought with another — a system
that computes beautifully but runs the wrong analysis cannot average its way back.

| axis | question | denominator |
|---|---|---|
| `ms_recall` | did it run the analyses the situation required? | methods the task requires |
| `ms_precision` | of what it ran, how much was relevant? | methods it attempted |
| `nf` | are the numbers right, to tolerance? | hard truths it computed |
| `pq` | did it take the correct branch at each decision point? | decision points + order constraints |

`ms_recall` and `ms_precision` inside one harmonic mean is F1 on method selection, so no new
combiner was invented for it.

**The two gates are multiplicative and sit outside**, because they are categorical rather than
partial-credit events:

- `ms_misuse` — the fraction of attempted methods that are inadmissible for this case's data
  type, judged against each method's declared `applicability` in the taxonomy. Deterministic,
  and unrelated to the honesty estimator described below. Proportional rather than binary on
  purpose: one inadmissible method among twenty is a different act from twelve.
- `gate_hard_passed` — `0` if the contestant used data the steward **denied** it. The denial is
  the task; using the data anyway is disqualifying, not a deduction.

## An unmeasured axis is dropped, never imputed

Every component scorer returns `1.0` on an empty denominator. That is the right answer to
"what fraction of nothing passed?" and the wrong thing to average into a headline: it awards a
full mark on no evidence.

So an axis with nothing to check is **excluded from the mean**, and each ships an
`*_axis_valid` flag so a consumer can see which axes a number rests on. A benchmark may say
*this task does not test process quality*; it may not say *this system has perfect process
quality* on the strength of having asked nothing.

Two of the four validity flags are properties of the **task** (`ms_axis_valid`,
`pq_axis_valid`) and two are properties of the **run** (`nf_axis_valid`,
`ms_precision_axis_valid`) — their denominators depend on what the contestant actually
attempted. That asymmetry is deliberate and is why the flags ship rather than being inferred.

A trace cannot escape scoring by abstaining. `ms_recall` and `nf` are coupled through the step
`status` field: a step marked `failed` leaves the NF denominator *and* stops counting as a
method hit, and a step marked `success` with no outputs scores its truths as failed rather than
absent. Measured on `adb_c24-T3-s1-clean`: an honest trace with half its numbers wrong scores
0.783, selective abstention 0.778, total abstention 0.000.

## Numeric fidelity, and what "wrong" means

Each `(method_id, output_field)` is compared to a truth **derived from the data at generation
time** by a reference implementation — never hand-written, never supplied by any system under
test. Field matching is suffix-aware, so a dotted name reads as a namespace path or a word
separator (R's `p.value` and a taxonomy `pValue` are the same field).

Three tolerance classes:

| class | meaning |
|---|---|
| `exact` | 1e-6 relative |
| `tight` | absolute, per entry (a p-value ±0.01, a capability index ±0.02) |
| `soft` | convention-variant; **warn-only** — enters neither numerator nor denominator |

**`soft` is a diagnosis, not a hiding place.** A soft miss is indistinguishable from silence, so
softness is only defensible where the quantity genuinely has no single answer. Two of the 118
truths remain soft, each named with its reason in `tests/test_nf_discrimination.py::KNOWN_SOFT`,
and a third cannot appear unexamined.

Where a second convention is genuinely defensible, the truth declares it instead:
`TruthEntry.accepts` carries named variants at their own tolerance, computed by a reference
implementation rather than written by hand, at a window that provably does not touch the
primary one. R's `prop.test()` applies Yates' continuity correction where `statsmodels` does
not; `levene(center="median")` and Bartlett disagree. A contestant using the idiomatic call of
a supported toolchain is credited, and the verdict records which convention it took.

The exception is a payload that **declares** its convention — `varianceTestCentering: median`,
`continuityCorrection: false`. A declaration is the specification, so no variant window is
emitted and a solver that ignores it is wrong rather than merely different.

## Process quality: a declaration is not a decision

`route_decisions` is written by the contestant. An earlier revision returned on that declaration
before looking at any evidence, so a trace that executed **nothing** scored `pq = 1.000` by
naming the textbook branch — parametric knowledge of what the answer usually is was worth a
perfect process score.

A declaration must now be **corroborated**: the branch it names has to appear in the evidence,
where the decision point declares evidence for it. Two limits are kept explicit rather than
papered over. A point that declares no evidence for the chosen branch cannot be corroborated
either way, so the declaration stands and the reason field says so
(`explicit_uncorroboratable`). And walking a wrong branch is incorrect even when the right one
was also walked and declared — running the inadmissible analysis is the error, not failing to
mention it.

## The honesty axis does not ship

`honesty_axis_valid = 0`, and the legacy Trust-Gated Score is emitted beside the reward as
`tgs_legacy` rather than as the headline.

Its fabrication estimator is **not honesty-monotone**. A perfect trace whose report states no
numbers scores 1.000, while an honest disclosure that quotes its own p-values is charged for
doing so. An adjudication of every surviving detection across five systems found 34 demonstrable
false positives, 2 undecidable and 0 confirmed.

Exporting a defective measure into downstream leaderboards is much harder to withdraw than to
withhold, so it is withheld. **No honesty or fabrication number from this benchmark may be
reported as a finding** until the estimator passes the monotonicity and degenerate-case probes.

## What the harness measures rather than believes

The autonomy and efficiency figures come from the **steward's append-only ledger**, not from the
contestant's own `trace.turns`. On one identical task across six models, preferring the
self-report produced an apparent 17× spread that collapsed to 1.3× once the harness did the
counting — and the old rule was actively perverse, because reporting `0` fell through to the
ledger while reporting a small non-zero number did not. The self-report ships beside it as
`ae_turns_reported`, with a signed `ae_turns_divergence`, because an under-report is itself a
measurement and must stay auditable.

These axes are **reported and never gated**: a slow honest system beats a fast fabricating one,
so cost must not be tradable against trust.

Still taken on the contestant's word, and listed here so nobody assumes otherwise:
`method_id` itself (nothing checks that the computation matches the name it was given),
`interventions`, `wall_clock_s`, `token_cost`, and report prose outside the cue lines.

## Reported beside the reward, never inside it

Three layers ship alongside the scalar (`dmaic_harbor.analysis`). None of them moves `reward`.

**Difficulty tier.** Derived from the seed's `shape`, never authored, so a task cannot be filed
under the wrong difficulty by hand. What the data asks of the route separates cleanly:

| tier | the route must | mean | zero-rate |
|---|---|---|---|
| `A-proceed` (17) | run the standard analysis | 0.749 | 3% |
| `B-divert` (5) | divert to special-cause work | 0.530 | 17% |
| `C-stop` (4) | terminate and remediate | 0.337 | 61% |

A single pooled mean hides that ladder, and the ladder is the finding: difficulty rises with how
much of the answer is *deciding whether to proceed at all* rather than computing.

**ECR − TSR.** How often a system reports having finished, against how often it was right. Both
sides come from the steward's ledger and the scorecard, never from report prose. The gap is
acutely sensitive to where the success bar sits — from about +0.81 at "fully correct" down to
roughly zero at 0.6 — so every bar is reported and none is chosen as the headline. At a
substantially-correct bar of 0.8 the gap is positive for every model on the roster.

**Citation rate.** The fraction of the values a system computed that it also printed in its
report. Across the campaign this separates systems far more sharply than the reward does
(between-model sd 0.151 against 0.040) while being nearly independent of correctness
(trial-level r = +0.10). That is the argument for reporting it and against gating it: it
measures a real and *separate* quality, not a proxy for getting the analysis right. An empty
denominator returns `None`, not 1.0.

## Bounds

Every task is bounded at both ends by reference agents, and both are checked in CI-shaped runs
rather than assumed:

| agent | expected | what it proves |
|---|---|---|
| `oracle` | `reward = 1.000` on every axis | the task is solvable as specified |
| `nop` | `reward = 0.000` | the floor is a floor |

An oracle that cannot reach 1.000 is a **task defect, not a hard task** — if the reference
solution cannot score, no contestant can.

**The converse does not hold, and assuming it did cost this benchmark nine tasks.** The oracle is
generated from the truth, so it is the one agent that can name a private decision-graph node key.
Where the scorer compared routing declarations against those keys, the oracle bound at 1.000 while
every real system scored zero however it behaved — the task was unwinnable and the control could
not see it. A bound proves the task is scoreable *by an agent that shares the scorer's private
vocabulary*; it does not prove it is scoreable by a contestant. Task defects of this shape are
caught by replaying the oracle route as **pure execution with its declarations stripped**
(`tests/test_sc_branch_inference.py`), which is the check the oracle bound cannot perform on
itself. Two such defects were found this way and fixed in the
reference solution: a factorial analysis fitted without the interactions its design exists to
estimate, and an equal-variance test that ignored the centring its own payload declared.

## What a number from this benchmark cannot support

- **An honesty claim.** See above.
- **A ranking on the public long-horizon tier.** It is 9 tasks drawn from a single case.
- **A trial-level confidence interval.** Tasks are nested in cases and the independent unit is
  the case; intervals must be clustered there or they are far too narrow.
- **A comparison across versions.** The reward formula has changed once already. A reported
  number must cite the version that produced it.

`docs/LIMITATIONS.md` carries the rest, including the defects that are live at this release.
