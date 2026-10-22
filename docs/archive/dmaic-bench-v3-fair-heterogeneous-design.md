# DMAIC-Bench v3 — Fair Evaluation of Heterogeneous DMAIC Agents

**A ground-up redesign so that a one-shot LLM+sandbox agent, a tool-planning agent, a purpose-built human-in-the-loop decision-graph engine, and a human expert can all be ranked fairly on one leaderboard — and the result supports a top-conference paper.**

Version 3.0 · 2026-07-09 · supersedes the v2 task-model doc where they conflict
Companions: `dmaic-bench-v2-longhorizon-design.md` (v2 graph task-model, kept), `../SCORING.md` (the scoring as implemented). The v2 method-selection gap analysis that motivates §0 is an internal note and is not published in this repository.

---

## 0. Why a v3 (the honest reckoning)

v2 proved the *mechanism* (conditional decision-graph truth, gating environment, cascade scoring) but live contestant runs exposed **six flaws that make current scores unfit for a fair, paper-grade leaderboard**:

| # | Flaw (evidence) | Consequence |
|---|---|---|
| F1 | **Method selection was fed** — `admissible_methods` in the briefing + hand-holding prompts told the agent *which* method to use (`M_GRR→msa.gage_rr_crossed`). | The hardest, most-decisive DMAIC skill — picking the right method from ~49 candidates under data/context ambiguity — was **untested**. Sonnet's 0.95 only shows "given the method, it computes." |
| F2 | **Toy inflation** — `injection_molding` is a 30-number synthetic task; everyone scores 0.8+. | Discrimination collapses; real difficulty hidden. |
| F3 | **Oracle not grounded** — migrated expert cases used placeholder truths (`msa.pctTol=0.15`), so a *correct* agent value (0.0646) was scored wrong (NF artifact → false 0.71). | Numeric fidelity un-scorable on real cases without hand-grounding. |
| F4 | **Naming/format penalty** — a correct value under a different field name (`F_value`≠`fStatistic`) scored 0. | Penalizes conventions, not competence. |
| F5 | **Protocol bias against the production engine** — the autonomous blind-session protocol assumes turn-paced human provisioning is unavailable; that engine pauses at decision nodes → "does-not-route" (0), even on its home turf. | The bespoke engine is structurally disadvantaged; the board is unfair. |
| F6 | **Non-comparable access** — Sonnet via subagent+scipy, DeepSeek via a bespoke driver, the production engine via HTTP with hand-mapped `computedSpecKeys`. Three different harnesses, one column. | Scores aren't commensurable. |

v3 fixes all six at the level of **task contract, scoring, and harness** — grounded in how the strongest agent benchmarks (SWE-bench, OSWorld, τ/τ²-bench, HAL, MLE-bench) solve each piece.

---

## 1. First principles (each traced to a predecessor)

1. **Contract, not protocol.** A task is `(input data + a fixed policy document + a verifiable OUTPUT contract)`. The contract **never** prescribes turn count, planning, tool use, or interaction style. *(SWE-bench: repo+hidden tests; OSWorld: final-state `success()`.)*
2. **One thin adapter.** Every contestant is wrapped behind `run(task_input) -> Deliverable` (a standardized trace + report schema). Standardize **I/O schema, allowed tool/data surface, budget meter, and the verifier**; leave **internal control flow entirely free**. *(HAL `run(input)->dict`; Inspect's Solver/Scorer/Dataset split.)*
3. **Outcome-graded, form-neutral.** Grade the *artifacts and computed values to tolerance* + the *correct conclusion*, not the trajectory shape. Every rubric checkpoint is a **semantic sub-state achievement** with **name/method/route normalization**, so valid alternatives and naming differences aren't penalized. *(OSWorld checkpoints; τ-bench DB-equality; fixes F3/F4.)*
4. **Isolated, independent verifier.** Ground truth is computed by a trusted solver in a store the agent can never write to; no agent artifact is read by the grader. *(Berkeley RDI 2026 exploit audit; the per-case grounding-script pattern; fixes F3.)*
5. **Two-channel scoring: outcome × method-validity.** Channel 1 = did the computed values / conclusion match truth to tolerance. Channel 2 = was the *method itself* valid & correctly selected (no misuse). An agent that reaches a right-looking number via a statistically invalid method scores high on C1, **flagged on C2**. *(τ-bench dual grader; ToolBench misuse metrics; fixes F1.)*
6. **Method selection is a first-class test, not a given.** The contract exposes the **full method vocabulary (~49)** and the *data*, never a per-node shortlist; the agent must pick. *(GAIA/BrowseComp "don't tell it which resource"; fixes F1.)*
7. **Fair interactivity via a fact-scoped, method-blind simulator.** Any agent that needs provisioning gets a τ²-style dual-control "process engineer" simulator behind an **information firewall** (below). *(τ²-bench dual-control; fixes F5.)*
8. **Multi-axis Pareto, not one scalar.** Report `{outcome, method-validity, autonomy-cost, $/tokens, pass^k}` and an explicit **autonomy-level label**; rank on a frontier. *(HAL cost-as-axis; MLE-bench fixed envelope; τ-bench pass^k; fixes F5/F6.)*

---

## 2. Dataset definition (v3)

### 2.1 A case is a contract, not a script
```
Case = {
  context:        business framing (CTQ, spec limits, goal) — NO method names
  policy_doc:     the DMAIC methodology rules that constitute the grading contract
                  (e.g. "capability requires a stable, MSA-validated process";
                   "choose the capability method by the fitted distribution")
  data_store:     raw data tables, provisioned on request (never the answers)
  method_space:   the full ~49-method vocabulary (SAME for every case) — the menu
  output_contract: the required Deliverable schema (trace + report + declared decisions)
  oracle:         INDEPENDENT ground truth — correct method PER decision, correct values
                  to tolerance, correct conclusions — held in a store disjoint from data_store
}
```
The crucial change from v2: **no `admissible_methods` per node.** The agent sees the *data* and the *policy*, and must select the method. The oracle records *which* method is correct (and which are misuse) for this data.

### 2.2 Three ground-truth layers (so NF is always scorable)
- **Parametric cases** (`generate(seed)`): data + truth co-generated; contamination-proof; support data-conditioned method forks (seed decides normal→normal-cap vs skewed→Box-Cox, constant-n→P-chart vs varying→Laney, crossed vs nested gage layout, …).
- **Reconstructed expert cases** (`adb_c15`, `adb_c16`, `adb_c20`, `adb_c08`…): real multi-stage projects; truth **independently derived by verifiers** (one grounding script per case, generalized to all), never placeholders (fixes F3). *Every case named here is in the held-out split and is absent from this repository, as are its grounding scripts — see `../HELD_OUT.md`.*
- **Held-out private cases**: unpublished seeds + never-published expert cases for the leaderboard split; canary GUIDs; memorization probe. (This is the split described in `../HELD_OUT.md`: the public release carries 15 of the 24 cases, and the nine expert-derived cases are withheld.)

### 2.3 Difficulty tiers by *decision hardness*, not size
- **D1 — determinate:** one clearly-correct method per stage (calibration floor).
- **D2 — method-ambiguous:** data shape forces a non-obvious method choice (skewed data that *looks* usable with normal-cap; unequal variances that *look* poolable) — tests C2 misuse.
- **D3 — full project:** 5-phase DMAIC, ≥4 method-selection decisions, ≥1 gate, ≥1 honesty fault, cascade dependencies, ≥2 valid alternative routes.
Anchor tiers to **expert-time percentiles** (MLE-bench medal analogy).

### 2.4 Robustness & honesty variants
Dirty variants (renamed columns, nulls, unit confusion, distractor tables) and fault-injection (deny a mandatory stage's data) apply to every tier — testing data-prep and anti-fabrication.

---

## 3. Scoring system (v3)

### 3.1 Two channels, computed on the standardized Deliverable
Every contestant, however it ran, emits a **Deliverable** = `{trace: [ {declared_method, inputs_digest, outputs, decision} ], report, route_decisions}`. Scoring reads *only* the Deliverable + the isolated oracle.

**Channel 1 — Outcome fidelity** (did it get the right answers)
- `NF` numeric fidelity: declared outputs vs oracle **to tolerance**, with **semantic field normalization** (synonyms, dotted/nested, unit-aware) so `F_value`≡`fStatistic` (fixes F4).
- `CQ` conclusion quality: the report's stated conclusions match the oracle conclusions (stable/unstable, capable/not, which factor significant), cue-line matched.
- `ART` required artifacts present (the control chart with the right OOC points, the capability index, the DOE optimum).

**Channel 2 — Method validity** (did it do it the right way) — the v3 core
- `MS-sel` method-selection accuracy: for each decision, did the agent pick a method in the oracle's **correct/acceptable** set for *this data*? (picking normal-cap on skewed data = wrong even if the number is close).
- `MISUSE` misuse rate: fraction of decisions using an **invalid** method (pooled-t under unequal variance; capability on an out-of-control process; crossed gage on a nested design). Detected from `declared_method` + `inputs_digest` against the policy.
- `GC` gate compliance: methodological prerequisites respected (MSA before capability, screening before RSM, root-cause before improve).
- `HN` honesty: no fabrication (claimed value with no successful computation) + fault-probe disclosure.

### 3.2 The Trust-Gated Project Score (per case)
```
Competence = HM(NF, CQ, MS-sel, GC)            # harmonic — no axis buys another
TGPS       = Competence × (1 − MISUSE) × (1 − FabRate) × FaultGate
```
Method misuse and fabrication are **multiplicative gates**: a project that reaches the right number via an invalid method, or fabricates, is discounted toward zero — because in the field a right-looking number from a wrong method is a *trap*, not a success. `ART` and route-alternatives feed partial credit inside CQ/GC rather than as separate gates.

### 3.3 The leaderboard is a profile, not a scalar (fixes F5/F6)
Each contestant is reported as:
```
{ TGPS, MS-sel, MISUSE,                 # what it got right / how validly
  autonomy_level ∈ {L4,L3,L2,L1},       # L4 one-shot autonomous … L2 human-provisioned … L1 human
  autonomy_cost = #provisioning turns,  # metered like $ (0 for clean one-shot)
  cost_$ / tokens,                       # HAL cost axis
  pass^k reliability }                   # τ-bench consistency
```
Ranking is on the **Pareto frontier** of (TGPS, cost, autonomy). The production engine can be "high MS-sel / high method-validity **at L2**" while Sonnet is "high TGPS **at L4**" — the tradeoff is *shown*, not silently collapsed. This is the paper's headline framing: *autonomy level is a declared axis, not a hidden confound.*

---

## 4. Fair heterogeneous harness (the part that makes it honest)

### 4.1 One adapter contract
```python
class Agent(Protocol):
    def run(self, task: TaskInput, env: Env) -> Deliverable: ...
```
`TaskInput` = context + policy_doc + method_space (no method shortlist). `Env` exposes exactly two calls, identical for every contestant:
- `env.request(data_key) -> table`  — pull a raw data table on demand (metered).
- `env.provision(natural_language_request) -> response`  — the dual-control simulator (metered as an autonomy turn).

The autonomous LLM agent calls `request` a few times and never needs `provision`; the tool-agent likewise; **the production engine's decision-node pauses are mapped onto `provision`** so its native HITL loop runs to completion. Internal control flow is free; only the Deliverable is scored.

### 4.2 The information firewall (leak-proof simulator) — critical
The provisioning simulator and the grader read **disjoint stores**:
```
simulator context = { raw_data_tables, process_facts, persona }     # what a real engineer HAS
grader   context  = { correct_method_per_decision, oracle_values, conclusions }   # the ANSWERS
```
The simulator may hand over a data column, the spec limits, "yes the fixture is installed" — **never** a method choice, a target value, or a conclusion. A wrong provisioning request returns the datum but **does not advance the score**; only reaching the output contract does. (τ-bench "constrained to observable state," hardened into a structural firewall; the simulator is itself **validated against a scripted/held-out human baseline** per the 2606.20708 decision-fidelity warning.)

### 4.3 Budget & isolation parity
- **Same envelope for all:** identical cap on `provision` turns, tool budget, wall-clock; all reported (MLE-bench fixed-envelope; HAL metering).
- **Verifier isolation:** oracle computed independently; no agent-written file is read by the grader (Berkeley RDI).

### 4.4 How each contestant plugs in (all via the same `run`/`Env`)
| Autonomy | Contestant | Native loop | Uses `provision`? |
|---|---|---|---|
| L4 | LLM + sandbox (Sonnet) one-shot | writes/executes scipy, routes itself | rarely (0–1) |
| L3 | tool-agent (DeepSeek + Python tool + planning) | plan → tool calls → report | occasionally |
| L2 | **the production engine** — a purpose-built human-in-the-loop decision-graph system | journey pauses → `provision` returns the datum/action | yes, metered as autonomy cost |
| L1 | human expert (reference line H) | analyst works the case | n/a |

Every one emits the same Deliverable; every one is scored by the same two-channel rubric against the same isolated oracle. **That is the fairness guarantee.**

---

## 5. What this makes the paper able to claim

- **RQ1 — Does the benchmark measure *conduct* (method selection + validity), not just computation?** Two-channel scoring + no fed methods: show that fed-method scores (v2) collapse the discrimination that method-selection scoring (v3) restores.
- **RQ2 — Are heterogeneous agent architectures fairly comparable?** The `run`/`Env` adapter + firewall simulator + autonomy-axis leaderboard: show the same task, same oracle, same budget across L4/L3/L2, with autonomy declared.
- **RQ3 — Does scaffolding, not model scale, drive DMAIC agency?** Same model A0(no-tools)=0 vs A2(tool)=high (already observed) — now re-run under method-selection scoring.
- **RQ4 — Where do bespoke vs generalist agents win?** The production engine (L2, high method-validity, low autonomy) vs Sonnet (L4, high TGPS) on the Pareto frontier — a genuine architectural finding, not "who's biggest."

Table set: **main Pareto board** (TGPS × autonomy × cost), **method-selection & misuse table** (the v3 novelty), **RB robustness**, **fault-honesty**, **ablations** (feed-methods vs not; with/without gates), **human line H**. Contamination: parametric + private seeds + memorization probe. Verifier isolation + simulator validation are stated as table-stakes.

---

## 6. Build order (v3 on top of v2 machinery)
1. **Un-feed methods:** drop `admissible_methods` from the briefing; expose the full method vocabulary; add `declared_method` to the trace schema.
2. **Two-channel scorer:** `MS-sel` + `MISUSE` (policy-driven, per-decision) + semantic field normalization; wire the new TGPS.
3. **Adapter + Env + firewall simulator:** `run(task,env)`, `env.request/provision`, dual-store simulator, budget meter, autonomy-turn counter.
4. **Production-engine adapter:** map journey pauses → `provision`; capture its Deliverable (declared methods + values) uniformly — retire the hand-mapped `computedSpecKeys`.
5. **Ground all expert oracles** (generalize the per-case grounding scripts — these cases are held out, see `../HELD_OUT.md`); build D2 method-ambiguous cases; add misuse-trap data.
6. **Re-run the full board** under v3; report the Pareto profile; write the paper.

**Bottom line.** v2 asked *"can the agent walk the right route and compute?"*. v3 asks the two questions that actually decide a DMAIC project and that a top venue will demand: *"did it choose the right method under ambiguity (not fed to it), and is every heterogeneous contestant — including the human-in-the-loop bespoke engine — judged by the same isolated, form-neutral, two-channel contract on a Pareto board where autonomy is declared, not hidden?"*
