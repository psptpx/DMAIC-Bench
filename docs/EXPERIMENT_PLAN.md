# Pre-registered experiment plan

Written **before** the campaign runs and before any model score is seen. Everything below is
fixed in advance; anything that changes afterwards is recorded in the deviations register at
the end, with the reason, rather than quietly revised.

The point of writing it down first is narrow and specific: on this benchmark, run-to-run
variance has been measured at roughly **fourteen times** the between-model variance. With a
spread that wide, a study that decides its analysis after seeing the numbers will find a
ranking whether or not one exists.

---

## 1. Gates — no model spend until all five are green

These are pass/fail conditions on the instrument, evaluated on a cheap pilot. A campaign run
before them has to be re-run, which is the expensive failure.

| | Gate | Threshold |
|---|---|---|
| **G0** | The graph forks | ≥ 80% of decision-point instances observed at more than one seed change their correct branch. **The frozen-branch corpus scores 0%.** |
| **G1** | NF is an axis | `sd(nf) > 0.05` across the pilot, and no task has `nf_checked == 0` |
| **G2** | The tier has headroom | pilot spread ≥ 2 × the minimum detectable difference for the planned design |
| **G3** | The controls bound the scale | `oracle = 1.000` and `nop = 0.000` on every task in the pilot |
| **G4** | The exploits are priced | a method-spam trace and a compute-nothing trace both score materially below an honest run |

G3 and G4 are already met; G1 is met on the current corpus; G0 requires the data-conditioned
layer to be in the build; G2 is measured by the pilot itself.

**An oracle below 1.000 is a task defect, not a hard task.** If the reference solution cannot
score, no contestant can. Two such defects were found this way before any model was called.

## 2. Design

| | |
|---|---|
| Corpus | every publishable case; the nine expert-derived cases are held out (`docs/HELD_OUT.md`) |
| Independent unit | **the case**, not the task and not the trial |
| Instances per case | 4 — two seeds × {clean, dirty} |
| Passes | **k = 3**, the minimum that leaves run-to-run variance estimable |
| Language | English only |
| Agent | one scaffold, held fixed across models |

**Seeds beat passes, roughly two to one.** At an equal 144-trial budget, one instance per case
with fourteen passes gives a minimum detectable difference of 0.209; five instances with three
passes gives 0.127; fourteen instances with one pass gives 0.107. Passes also hit a wall: going
from k = 3 to *infinite* compute improves the detectable difference by about 6%, because the
floor is set by how many independent cases exist, not by how often each is repeated.

**Budget is cut by dropping models, never by dropping cases.** Below k = 2 run-to-run variance
stops being estimable — the exact hole that makes the existing end-to-end data unusable — and
below the full case set the clustering floor rises above the differences the benchmark exists
to detect.

**Minimum reportable configuration:** the full case set × 3 instances × k = 2, for as few as
two contestants. That still supports a paired contrast with an honest interval. It does not
support a ranking, and none will be reported from it.

## 3. Outcomes

**Primary:** mean `reward` per model, with a **wild cluster bootstrap-t** over base cases
(B = 10,000, Rademacher weights). The percentile bootstrap under-covers below roughly thirty
clusters, which is the regime this corpus is in.

**Primary comparison:** paired per-task differences against one **pre-declared reference model**,
not an all-pairs ranking. Every model sees the identical task set, so pairing removes the
between-case variance that otherwise dominates — measured at a 23% reduction in the detectable
difference on the one contrast where it could be checked directly. Pairing is an analysis
choice and costs no compute.

Family-wise error controlled by **Holm** across the contrasts against the reference.

**Secondary, reported disaggregated and never pooled into the headline:**

- each axis (`ms_recall`, `ms_precision`, `nf`, `pq`) with its own standard deviation
- `ms_misuse` and `gate_hard_passed` rates
- the model × case grid, so a single case cannot drive a conclusion invisibly
- tie rates per axis — a near-two-point distribution is itself the finding when it appears
- autonomy and cost from the harness ledger: turns, tokens, wall-clock. **Never gated**: a slow
  honest system beats a fast fabricating one, so cost must not be tradable against trust
- **the variance decomposition itself** — between-model, between-case, within-case run-to-run.
  Terminal-Bench reports 32,155 trials and never states how its intervals were computed; a
  survey of 445 benchmarks found 16.0% using any uncertainty estimate at all. Publishing the
  decomposition costs nothing here because it is already computed

**Full error accounting is part of the result, not an appendix.** Trials that produced no
verdict are reported as missing observations and excluded, never averaged in as zeros. A
previous campaign lost 34.5% of its trials to operational causes; a result that does not say so
is not reproducible.

## 4. Stopping rule

One interim look at k = 2, with O'Brien–Fleming spending (α₁ = 0.0054, α₂ = 0.0492):

- **stop for futility** if the observed spread is below 2 × the detectable difference at k = 2 —
  the tier does not discriminate and more trials will not change that;
- **stop for sufficiency** if every contrast already clears Holm;
- otherwise continue to k = 3 and stop unconditionally.

**Hard abort if the harness error rate exceeds 20%.** On the run history that, not model
failure, is the realistic mode, and a campaign burning budget on a broken harness should end.

## 5. What will not be reported

- **Any honesty or fabrication number.** The estimator is not monotone (`docs/SCORING.md`); the
  axis ships disabled and no number from it is a finding.
- **An ordered ranking while paired intervals overlap.** Overlapping intervals are the result.
- **Trial-level confidence intervals.** The design effect at this clustering is about 4.6, so
  they are roughly 2.15× too narrow.
- **A leaderboard on any tier that fails G2.** A tier whose contestants sit inside the noise
  produces a column of ties; that is reported as a property of the tier, not as a ranking.
- **Pooled cross-tier means** without stated stratum weights.
- **A trial count that includes harness errors.**
- **k = 5 described as "more rigorous"** — it buys about 4% on the detectable difference for 67%
  more compute, and that trade is not made silently.
- **USD as the campaign cost.** Prices resolve for a minority of gateway model names; tokens are
  the primary figure and any dollar amount is marked as a floor.

## Instrument check (single model, full corpus)

Before fanning out to the roster, one model was run across **every** task, because a one-task
connectivity check does not exercise task rendering, steward routing, truth binding or scoring
on the other twenty-five. `glm-5.3-flash`, 26 tasks, k = 1:

| | |
|---|---|
| trials producing a verdict | **26 / 26** — no harness errors, no missing observations |
| distinct reward values | 15 |
| spread / mean | 0.000 – 0.909 / 0.442 |
| axis ranges | `ms_recall` 0.75–1.00 · `ms_precision` 0.17–1.00 · `nf` 0.000–1.000 · `pq` 0.00–1.00 |
| interaction turns | 4 – 11 |

Nine tasks scored exactly 0.000. Each was checked rather than assumed: all nine carry PQ
decision points, every verdict on them is `incorrect` or `unknown`, and the oracle scores 1.000
on all nine — so they are winnable and the zeros are genuine routing failures, not tasks that
cannot be scored.

> **This conclusion was wrong, and the way it was wrong is worth keeping.** The check above
> asked whether the *oracle* could score the task and took yes for proof that a contestant
> could. The oracle is generated from the truth and is therefore the only agent that can name a
> private graph node key, which is what the explicit routing path compares against. Every one of
> those nine tasks was in fact **unscoreable in the correct direction** for any real system: the
> compliant route and the non-compliant one both landed on zero. The full-campaign traces show
> the models had run the gauge study, read the failure and stopped. See the 2026-09-06 entry in
> the deviations register. **An oracle bound is necessary and is not sufficient; a control that
> shares a private vocabulary with the scorer cannot prove the task is winnable without it.**

**One property that shapes the analysis, recorded before the results exist.** On the six
rejection seeds PQ has exactly one decision point, so PQ is binary there, and PQ sits inside a
harmonic mean — one wrong branch zeroes the reward however well the rest of the run went. That
is the correct semantics for a hard prerequisite gate (capability on an out-of-control process
is meaningless, not merely imprecise), but it means those tasks are pass/fail with no gradient
and therefore carry less between-model signal than their count suggests. Per-axis results are
reported disaggregated for exactly this reason.

## 6. Deviations register

Every departure from the above is recorded here with its reason, before the results are
written up.

| date | deviation | reason |
|---|---|---|
| 2026-09-06 | **The campaign ran at k = 1, not the pre-registered k = 3.** | Recorded here rather than discovered at analysis time. Every job config carries `n_attempts: 1`, so run-to-run variance is **not estimable from this campaign** and no pass^k figure may be computed from it — the stopping rule's interim look at k = 2 never became available either. The corpus was run across all eight contestants instead, which buys the between-model contrast and forfeits the within-case one. Any pass^k reporting requires a further campaign at k = 3. |
| 2026-09-06 | **PQ and SC could not credit a correct prerequisite route; the scorer was fixed and every trial re-scored from retained artifacts.** | `point_id` and `correct_branch` are private decision-graph node keys that the task instruction never exposes, so the explicit `route_decisions` path could only ever bind for the oracle; and the correct branch of a prerequisite fork is a terminal remediation node that runs no analysis, so `branch_evidence` held no signature for it either. Declining correctly was therefore indistinguishable from silence while pressing on was incorrect — **both directions scored zero and the point was unpassable by any contestant.** Measured across 7 models x 9 such tasks: reward 0.000 on all 63, beside `ms_recall` 1.000, `nf` 1.000, `gate_hard_passed` 1 and `ms_misuse` 0.000. G3 stayed green throughout because the oracle is the one agent that can name the keys. Branches are now judged on behaviour (`divergent_evidence` / `convergent_evidence`). Re-scored with no model re-run: floored tasks 9/26 -> 1/26, PQ 0.332 -> 0.681, SC 0.288 -> 0.636, mean reward 0.410 -> 0.643. **The model ordering changes, so any ranking taken from the pre-fix numbers is partly an artefact.** |
| 2026-09-05 | **G0 initially measured 67%, below the 80% threshold. The corpus was fixed, not the threshold.** | Six forks were constant across every seed. The first diagnosis — "no seed exercises them" — was wrong: every rejection edge was a self-loop, and the walker is cycle-guarded, so a rejection terminated the walk *on* the fork and recorded nothing. Those forks were unmeasurable whatever the data did. Rejection edges now lead to real nodes, with seeds whose data genuinely takes them. Re-measured: **18/18 = 100%**, and the share of the process-axis denominator that no seed exercises fell from 38% to 0%. |

## Corpus expansion — 95 tasks, 15 projects (2026-09-09)

Eight projects were onboarded from a practitioner corpus of completed black-belt reports
(provenance and what was and was not taken: `docs/CASE_SOURCES.md`). The corpus goes from 40
tasks over 7 projects to **95 tasks over 15**.

**No model has been run on the 55 new tasks.** Everything below TIER_RESULTS and every
per-model number in this file was measured on the 40-task corpus and still refers to it. A
re-measurement is owed and is not reported here as though it had happened.

What has been established on the new tasks:

| | |
|---|---|
| oracle ceiling | **109/109 at reward 1.000 containerised**, 2026-09-12, on 97 clean tasks + 12 honesty probes, with nop 109/109 at 0.000. `docs/archive/RESULT_G3_2026-09-12.md`. The debt this line carried for the whole preceding sequence is paid; it found three defects in doing so. |
| every task builds | 65 task directories built clean through `dmaic_harbor.build --v2`, no method leak, no steward topic collision |
| routes are frozen | all 95 pinned in `tests/data/v2_routes_golden.json` (route, branch decisions, decision points, and a digest of both the generated batches and the oracle results) |
| tier split | **A-proceed 44 · B-divert 18 · C-stop 33** (was 21 · 7 · 12) |

The tier split is the number to be careful about, because the classifier was wrong when the
new cases arrived and would have reported **A 66 · B 16 · C 13**. It keyword-matched the
free-text `shape` label — "gauge-unacceptable" meant stop, anything unrecognised meant proceed
— so eight cases whose authors wrote "tester-unacceptable", "surface-does-NOT-fit" and
"change-cannot-be-shown" put 20 of the 33 stop-tier tasks into the proceed tier, silently, in
the one number the difficulty claim rests on. The tier is now derived from the route: did it
reach a control plan at all, and if so did it get there through the branch a failed stability
check opens. That definition reproduces the hand-classified tier of all 40 pre-existing tasks
exactly, which is why it could be adopted without re-labelling anything, and
`tests/test_tier_classification.py` fails if a shipped shape has no entry or an entry that
disagrees with its route.

Three scoring defects surfaced while authoring, each found by a test rather than by review:

- the cascade precondition "capability is invalid on an out-of-control process" was written as
  the single guard `imr.outOfControl == 0`, so it silently meant "capability presumes an
  INDIVIDUALS chart"; the first subgrouped case's own oracle was charged with a hard violation
  and scored **tgps 0.0 on every seed that reached an index**;
- Self-Consistency resolved a repeated method with a last-wins merge, so a measurement study
  re-run after remediation had its second verdict answer for its first, and the re-walk skipped
  the remediation it had just watched the contestant perform;
- a node that is the target of two different forks makes the earlier fork unreadable — the
  route that ends at that node by the later edge carries the evidence for the branch the
  earlier fork did not take, and the scorer convicted a compliant run.

## Gate results — expanded corpus (40 tasks, 7 projects)

Re-measured after the corpus grew from 26 tasks to 40 and the scoring defects were fixed.
Nothing was run against a model until this table was green.

| gate | threshold | measured | |
|---|---|---|---|
| **G3** controls bound the scale | oracle 1.000 on **every** task | **40/40 at 1.000**, 0 harness errors, 40 attempts for 40 tasks | **pass** |
| **G0** the graph forks | no recurring fork keeps one branch | 0 dormant instances; a skewed seed was added to `adb_c30` rather than the threshold lowered | **pass** |
| tiers are separable | derived from `shape`, not authored | A-proceed 21 · B-divert 7 · **C-stop 12** (was 4) | **pass** |
| corpus language | English only | 0 CJK characters across all 40 truth packages and every agent-visible file | **pass** |

**G3 earned its place twice on this build.** It found the distinct-category trap rejecting under
only one of the two admissible %StudyVariation conventions — the oracle walked the opposite
branch and the ceiling on that task fell to 0.000 — and it found a capability index no single
named convention could match. Both were task defects wearing the costume of hard tasks, and
both were fixed before a model was called. An earlier build of the same tasks also failed G3
outright at 14/14 for two harness reasons — a verifier base image that could not be pulled, and
a stale wheel that left the verifier without `dmaic_bench` at all — neither of which would have
been visible in a model score.

## Gate results — original corpus (26 tasks)

Measured on the data-conditioned corpus (26 tasks, 5 projects), before any campaign spend.

| gate | threshold | measured | |
|---|---|---|---|
| G0 the graph forks | ≥ 80% of recurring forks vary | **100%** (18/18); dormant share of the PQ denominator **0%**, was 38% | **pass** |
| G1 NF is an axis | `sd(nf) > 0.05`, no task with an empty denominator | varies 0.000–1.000 across the pilot | **pass** |
| G2 the tier has headroom | pilot spread ≥ 2 × MDD (≈0.15) | spread **0.800**, one model's mean **0.257** against an oracle ceiling of 1.000 | **pass** |
| G3 controls bound the scale | oracle 1.000, nop 0.000 | 6/6 and 6/6, `sc` moving 1.0 / 0.0 with them | **pass** |
| G4 exploits are priced | spam and compute-nothing score below an honest run | method spam 0.7297 → 0.1710; declare-only PQ 1.000 → 0.375 | **pass** |

The G2 contrast is the one worth keeping in view: on the frozen-branch tier this replaced, the
cheapest model on the roster scored **0.975** and the spread was **0.025** — a column of ties.
Here a real model averages 0.257 with numbers that are *correct* (`ms_recall` 1.00 on 6/6, `nf`
1.000 on 5/6) and routes that are not. The benchmark separates computation from judgement
because the judgement is now a function of the data.
