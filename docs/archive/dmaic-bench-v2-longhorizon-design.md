# DMAIC-Bench v2 — The Scientific Method as a Long-Horizon Task

**A benchmark for autonomous agents that must *conduct* a multi-stage improvement project, not compute an answer.**

Design spec · 2026-07-08 · supersedes the T1/T2-centric framing of the original v1 benchmark
draft (an internal note, not published in this repository)
Companions: `dmaic-bench-v3-fair-heterogeneous-design.md` (the v3 redesign, which supersedes
this document wherever the two conflict), `../SCORING.md` (the scoring as implemented)

---

## 0. The thesis in one paragraph

Every long-horizon agent benchmark today grades a **terminal world-state** (τ-bench, WebArena, AppWorld, OSWorld, WorkBench), a **single collapsed answer** (GAIA), a **competition metric on a produced artifact** (MLE-bench, DSBench), or **code that passes hidden tests** (SWE-bench). The two closest scientific ones — ScienceAgentBench and DA-Code — grade **single-shot analysis tasks**. None evaluates an agent that must execute a **multi-stage scientific methodology whose stages are causally and statistically dependent, where the correct next method is a function of what the data revealed at the previous stage, and where the domain's own gating rules are the grading contract.** DMAIC (Define-Measure-Analyze-Improve-Control) is exactly such a methodology. DMAIC-Bench v2 makes **the scientific method itself the task**: the agent walks a data-conditioned decision graph, the environment enforces the methodology's prerequisite gates, and the score measures how faithfully the agent honored the method — computed exactly, gated correctly, and without fabrication.

This is a benchmark-first paper. The production DMAIC engine — a purpose-built,
human-in-the-loop decision-graph system, not redistributable and therefore not part of this
release — is one participant, not the subject.

---

## 1. Why v1 is still a calculation test (the honest self-critique)

The v1 benchmark (T1 atomic / T2 phase / T3 project) has a fatal structural weakness that its own results exposed: **B1-sonnet scored a flat 1.000 on T2**, because for a frontier LLM + code sandbox, the tasks reduce to "run the right scipy call." Three concrete defects:

1. **Decision ground truth is frozen, not conditional.** `DecisionPoint.correct_branch` is fixed at case-authoring time; the parametric generators *deliberately force the data* so the branch is determinate (`adb_c02/generator.py`: "the normality_gate has a determinate correct branch"). The scorer **never evaluates the rule against the observed data** — it string-compares `chosen_branch` to a pre-frozen constant. Two different data draws can never demand two different correct routes. → **A scripted single-path solver aces it. Reviewers call it non-agentic.**

2. **The environment does not gate.** The `DataSteward` hands out any stage the moment its topic is named; it never withholds capability data until MSA passes. All ordering/gating rules live only in *post-hoc scoring* (`pq.py`), never in the environment. → the methodology's *prerequisite structure* — the thing that makes DMAIC hard — is not enforced where it matters.

3. **Data is delivered all-at-once to baselines.** `scaffold.write_scaffold` dumps every stage's data to disk up front. The staged `DataSteward` path exists but the LLM baselines bypass it. → no genuine long-horizon information-gathering.

v2 fixes all three at the level of the **task model and the environment**, not the scorer.

---

## 2. Task formalization: a DMAIC project as a data-conditioned decision graph

A v2 task instance is a tuple `T = (G, D, Θ, Π, B)`:

- **`G` — a decision graph** `(N, E)`. Each node `n ∈ N` is a *stage obligation*: a phase, a set of admissible methods, and the artifact it must produce. Each edge `e ∈ E` carries a **guard** `when(e): Results → bool` evaluated against the *observed computed results so far*. Exactly the production engine's proven runtime model — guarded edges carrying a `when` expression over declared `guardFields`, evaluated by a safe expression evaluator — ported into the benchmark as ground truth.
- **`D` — a parametric data generator** `generate(seed) → (blocks, results⋆)`. Crucially, **the seed controls the data's statistical shape**, and `results⋆` are the *oracle-computed* truth values for that draw. Different seeds ⇒ different shapes ⇒ **different correct paths through `G`**.
- **`Θ` — the oracle**: a trusted solver that, given `blocks`, recomputes every statistic to tolerance. Ground-truth numbers are never hand-frozen; they are generated with the data (contamination-proof, per DA-Code / Spider-2 / SWE-bench execution grading).
- **`Π` — the gating policy**: hard prerequisites (`MSA.pass ⊳ capability`, `screening.significant ⊳ RSM`, `root_cause.confirmed ⊳ improve`) enforced *by the environment at data-release time* (τ-bench policy compliance, made a first-class environment behavior).
- **`B` — budget**: max turns / tool-calls / tokens (MLE-bench, ScienceAgentBench cost accounting).

**The correct trajectory is not a fixed list.** It is `walk(G, results⋆)`: start at Define, and at each guarded branch take the edge whose guard the *oracle results* satisfy. For seed A (normal, stable, capable) the correct walk may be `Define→MSA→Cap(normal)→[Ppk≥1.33]→Control`; for seed B (non-normal, unstable, incapable) the *same graph* yields `Define→MSA→[unstable]→Investigate→Cap(nonnormal)→RootCause→DOE→Confirm→Control`. This single property — **the correct route is a function of the data draw** — is what makes the task genuinely agentic and unscriptable, and it is the property v1 structurally cannot express.

---

## 3. The three core innovations

### 3.1 Conditional decision-graph ground truth (kills the scripted-solver critique)

Ground truth is no longer a flat list of `(method, correct_branch)` constants. It is a graph whose edges are **guard predicates over observed results**:

```
Node  I_capability_route  (phase=analyze)
  ├─ when  normality.pValue >= 0.05      → N_cap_normal      (methods: capability.normal)
  ├─ when  normality.pValue <  0.05      → N_cap_nonnormal   (methods: capability.nonnormal)
  └─ default                             → N_cap_normal
```

The scorer **evaluates each guard against the agent's own observed values and against the oracle's**, and asks: *given what the data actually showed, did the agent walk the edge the methodology mandates?* Two graded quantities fall out:
- **Path correctness** `PC`: fraction of branch points where the agent took the oracle-correct edge *for this draw*.
- **Self-consistency** `SC`: did the agent's route match *its own* observed values (even if its values were wrong)? Separating PC from SC distinguishes "wrong data → wrong-but-consistent route" (a numeric failure) from "right data → wrong route" (a judgment failure) — a diagnostic no single-answer benchmark can produce.

Guards reuse the production engine's safe guard-expression DSL; the graph reuses its exported edge shape `(source, target, when, isDefault, guardFields)`. **We are porting a battle-tested runtime model into a ground-truth schema, not inventing an untested formalism.**

### 3.2 The gating environment (methodology compliance as an environment behavior, not a rubric line)

The v2 steward is a **policy-enforcing environment**, extending τ-bench's policy-compliance-as-metric into policy-compliance-as-*mechanism*:

- **Prerequisite locks.** A stage's data is *withheld* until its precondition is met by the agent's own accepted results. Capability data is not released until the agent has run MSA **and** reported an acceptance decision. Requesting capability early returns `locked: "Complete the measurement system analysis (MSA) and record an acceptance decision before the capability data is released"` — the environment refuses to let the agent skip the gate.
- **Conclusion-dependent forking.** The next data batch depends on *what the agent concluded*. If the agent declares the process **unstable**, the steward releases the *special-cause investigation* dataset; if **stable**, it releases the capability dataset. The environment forks, so the long-horizon dependency is real, not simulated.
- **Fault injection (retained + deepened).** For probe instances the steward denies a mandatory stage's data; passing requires refusal-in-trace + explicit disclosure (v1's trace-grounded fault probe). v2 adds **multiple fault targets per project** and **mid-project faults** (deny data *after* the agent has committed to a plan that needs it).

This makes the gates **load-bearing**: an agent that ignores the methodology cannot even obtain the downstream data, and its trajectory records the violation.

### 3.3 Cascade-aware phase scoring (real projects punish early mistakes)

Phase `N`'s grading **consumes phase `N−1`'s *actual computed output*, not the oracle's.** If the agent mis-estimated the measurement error in MSA, its capability indices are graded against *what its own (wrong) MSA implies*, and the divergence from the oracle cascades — exactly as a real project's later conclusions inherit earlier errors. This is the sequential-state-dependency principle (τ-bench / AppWorld final-state chaining) adapted to a *statistical* pipeline: **the credit for stage N is conditional on the validity the agent carried in from stage N−1.** A benchmark that grades each stage in isolation cannot see cascade failures; DMAIC-Bench v2 makes them first-class.

---

## 4. Metric suite (extends v1's six families)

Scores are reported disaggregated (HELM-style) and combined into a trust-gated aggregate. New/changed axes in **bold**.

| Axis | What it measures | Grounded in |
|---|---|---|
| **PC — Path Correctness** | branch edges walked correctly *for this data draw* | novel; §3.1 |
| **GC — Gate Compliance** | prerequisite gates respected (no capability-before-MSA, no RSM-before-screening) | τ-bench policy |
| **CF — Cascade Fidelity** | phase-N validity given phase-(N−1) actual output | AppWorld/τ-bench chaining; §3.3 |
| NF — Numeric Fidelity | computed statistics vs oracle, to tolerance | SWE-bench / DA-Code / Spider-2 |
| MS — Method Selection | right methods chosen, no misuse (per-stage, admissible-set) | ScienceAgentBench rubric |
| HN — Honesty | no fabrication; fault-probe disclosure (trace-grounded) | WorkBench side-effects + v1 |
| AE — Autonomy/Efficiency | turns, tool-calls, budget, human-intervention count | MLE-bench cost |
| **Rel — Reliability** | **pass^k**: project fully correct on all k independent runs | τ-bench pass^k |

**Trust-Gated Project Score:**
```
TGPS = HM(PC, GC, CF, NF, MS) × (1 − FabricationRate) × FaultGate × GateHardViolationGate
```
Both a fabricated statistic **and** a hard gate violation (trusting capability from a failed MSA) zero the project — the value statement is that *a project built on an unverified measurement system is worthless no matter how elegant the downstream math.* Reported alongside pass^k so a system that is right-but-unreliable is visibly distinguished from right-and-robust.

---

## 5. Contamination, difficulty calibration, and validation

- **Parametric, oracle-computed truth (contamination-proof).** Truth is generated *with* the data from `generate(seed)`; nothing is hand-frozen or web-derivable. Public seeds carry canary GUIDs; the leaderboard uses unpublished seeds; a memorization probe (context-only, no data) flags recall of expert figures.
- **Anti-scripting proof (the reviewer's first attack).** For each project we ship ≥2 seeds whose data shapes force *different* correct routes, and we report a **"single-path baseline"**: a scripted pipeline that always runs the modal route. It must *fail* the off-modal seeds (PC < 1). If a scripted solver can ace the graph, the graph isn't conditional — this is a release gate, not an afterthought.
- **Expert-validated gold (SWE-bench Verified's lesson).** Each project's graph, gates, and admissible-method sets are reviewed by a certified Black Belt; noisy ground truth silently caps the ceiling, so validation is mandatory before a case enters the leaderboard split.
- **Difficulty tiers by graph depth/branching**, not by phase: `L1` (linear, 1 fork), `L2` (2–3 data-conditioned forks), `L3` (full project, ≥4 forks + ≥1 gate + ≥1 fault), anchored to expert-time percentiles (MLE-bench medal analogy).

---

## 6. Positioning (related-work table)

| Benchmark | Multi-stage | Inter-stage *statistical* dependency | Data-conditioned method selection | Methodological gates graded/enforced | Exact numeric grading | Anti-fabrication |
|---|---|---|---|---|---|---|
| SWE-bench (Verified) | within-task | no | no | no | tests | no |
| WebArena / AppWorld / WorkBench | yes | no (world-state) | no | side-effects only | no | side-effect |
| τ-bench | flat | no | no | **policy compliance** | DB match | partial |
| GAIA | reasoning-chain | no | no | no | exact-match | no |
| MLE-bench / DSBench | pipeline | weak | some | no | competition metric | contamination focus |
| ScienceAgentBench / DA-Code | pipeline | weak | some | rubric (not gated) | execution-exact | expert-validated |
| **DMAIC-Bench v2** | **yes** | **yes (MSA→cap→cause→DOE→control)** | **yes (seed-routed graph)** | **yes (env-enforced + graded)** | **yes (oracle tolerance)** | **yes (first-class)** |

The bottom row is the union of properties no prior benchmark holds simultaneously. Each checked cell extends a named predecessor rather than duplicating it. **The one-line novelty:** *the first benchmark to make a domain's scientific method the long-horizon task, with the method's own gating rules as the grading contract and the correct trajectory a function of the data.*

---

## 7. Build plan (what this design compiles to)

1. **`core/graph.py`** — `DecisionGraph`, `GraphNode`, `GuardedEdge(when, target, is_default, guard_fields)`; `walk(graph, results) → path`; guard DSL evaluator (port `JourneyGuardEvaluator` semantics: comparison ops, `in`, and/or, safe field access). *(task #18)*
2. **A data-conditioned case** — `generate(seed)` whose shape parameters (normality, stability, capability) are seed-driven so ≥2 seeds walk ≥2 distinct correct paths; oracle computes `results⋆`. *(task #19)*
3. **Gating environment + scorer** — steward prerequisite locks + conclusion-forking; `PC`, `GC`, `CF` scorers; pass^k harness. *(task #20)*
4. **Tests + forking demo** — two seeds → two correct routes; scorer rewards the data-appropriate route and penalizes the mismatched one; single-path baseline fails off-modal seeds; full suite green. *(task #21)*

Each step is a runnable artifact, not a promise — the PoC (#18–#21) exists to prove the design is real before the full 20-project authoring campaign.

---

## 8. What we deliberately keep from v1

The v1 trace contract, the honesty fault probe (trace-grounded), the parametric truth generators and nine onboarding gates, the CJK-aware field normalization, and the six-family disaggregated reporting all carry forward unchanged. v2 is a **task-model and environment** upgrade — conditional graph truth, gating environment, cascade scoring — layered on the v1 measurement machinery that already works.
