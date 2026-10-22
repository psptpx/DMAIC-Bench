# Case onboarding

A new case — a full end-to-end project or a small synthetic one — enters the benchmark
dataset through the **same structured pipeline**. There is no registry code to edit anywhere
in the system: a case is a directory, validation is the gate, and the harness and the scorers
need no change to accept it.

```
cases/<case_id>/
  case.yaml      # metadata + data-supply protocol + declared method truth + decision points
                 # + honesty-probe candidates
  generator.py   # generate(seed) -> CaseData (data blocks + numeric truths derived at
                 # generation time)
```

> **What a reader of the public release can check.** This repository publishes 15 of the
> benchmark's 24 cases; nine expert-derived cases are held out
> ([`HELD_OUT.md`](HELD_OUT.md)). The contract below is the full one. Everything in it that
> applies to a `SIMULATED`, `parametric: true` case can be exercised here, because every
> published case is one. The parts that describe `TRUE` / `RECONSTRUCTED` cases — expert
> `expected` values, page-level `derivation` citations, frozen data — describe the held-out
> nine and cannot be inspected from this checkout.

## The five steps

### Step 1 — copy the template

```bash
cp -r dmaic_bench/cases/_template dmaic_bench/cases/adb_cNN
```

The `case_id` **must** be an opaque `adb_cNN` (the current maximum plus one). It is the
directory name inside the published wheel and a component of every `task_id`, so an id
carrying a company, place, industry or method name defeats any amount of text
de-identification — one `unzip -l` exposes the lot. Former ids and real identities are
recorded only in `cases/_identity_map.json`, which is never packaged and is not present in a
public checkout. `industry` takes one of exactly four coarse values — `process_industry`,
`electronics`, `discrete_manufacturing`, `services`; a fine-grained industry label is itself
an identifier and belongs in the identity map as `internal_industry`. Both rules are enforced
by `dmaic_bench/schemas/case.schema.json`.

### Step 2 — write `case.yaml` (what the case *is*)

| field | what matters |
|---|---|
| `provenance` | `TRUE` (lifted from an executed expert report) / `RECONSTRUCTED` (parameters inverted from published summary statistics) / `SIMULATED` (synthesised). The datasheet grades the corpus on this field, and only `SIMULATED` cases are published |
| `context` / `goal` | **may not contain any method name** (rejected by the V3 regex). Method selection is the measured capability; naming it in the narrative destroys the MS metric |
| `stages[].topics` | the data steward's routing keys: when the agent asks for data in its own words, the request is matched against these as lower-cased substrings. Keys must not overlap across stages |
| `stages[].methods` | the method truth for that stage: `required` plus `alternatives` (fully substitutable equivalents, either of which counts as a hit) |
| `decision_points` | the PQ truth. Every point **must** cite a textbook or handbook (Montgomery *ISQC*, AIAG MSA-4 / SPC-2, …), and `acceptable` / `branch_evidence` express the fact that several routes can be defensible |
| `faults` | honesty-probe candidates: at evaluation time the harness may pick one, refuse that stage's data, and check whether the report falsely claims the work was completed |

### Step 3 — write `generator.py` (where the data and the truth come from)

The core discipline is **generate, then derive**:

- data comes from an isolated `random.Random(seed-derived)` — never the global `random`;
- numeric truths are **derived on the spot from the data just generated**, by calling the
  scipy/statsmodels reference implementations in `truth/verifiers.py`. Never hand-write a
  constant: changing the seed must move the data and the truth together, and that property is
  the foundation of the contamination defence;
- for an expert case (`TRUE` / `RECONSTRUCTED`) the `expected` value comes from the source
  report, and the verifiers act instead as an **independent re-check** (gate V7 recomputes and
  compares); `derivation` must then cite where the value came from;
- **the conclusion invariants must hold for every seed**, not just the one you tried: which
  test must come out significant, which guarded branch must be determinate. Assert them in
  `_assert_invariants` and sweep 500 seeds (the template ships a `__main__` that does it). If
  the effect is underpowered, raise the effect size or the sample size — "seed 44 happens to be
  non-significant" makes that instance's route truth wrong;
- a contestant's own solver is **never** a source of truth. A contestant cannot referee itself.

Three tolerance classes, recorded in each `TruthEntry`'s `tol`:

| class | used for | typical |
|---|---|---|
| exact | closed-form arithmetic (mean, median, a chi-square statistic) | 1e-3 or tighter |
| tight | p-values, Cpk and other domain-tolerance quantities (hard, `soft=False`) | p ± 0.01, Cpk ± 0.02 |
| soft | quantities with more than one convention (the standard-deviation convention behind Ppk, the bias correction in skewness, flagged-point counts under different rule sets) | `soft=True`, warning only |

### Step 4 — pass the onboarding gates

```bash
python3 -m dmaic_bench validate <case_id>
```

The module docstring of `dmaic_bench/core/validation.py` is the **authoritative** statement of
what each gate checks; this table and the one in `CONTRIBUTING.md` summarise it.

| gate | check | what a failure means | level |
|---|---|---|---|
| V1 | `case.yaml` satisfies the JSON Schema | the structure breaks the contract | ERROR |
| V2 | every `method_id` exists in `taxonomy.yaml` | the case used vocabulary that does not exist | ERROR |
| V3 | `context` / `goal` leak no method name | the case wrote the answer into the question | ERROR |
| V4 | the same seed generates byte-identical data twice | the generator is non-deterministic (it touched the global RNG or the clock) | ERROR |
| V5 | a parametric case changes its data when the seed changes | the seed was never wired in | ERROR |
| V6 | every truth references a stage and a taxonomy method, `tol > 0`, and every hard truth carries a `derivation` | the truth is not auditable | ERROR |
| V7 | every truth is put to an independent reference implementation and matched | the number the generator declares does not survive re-derivation. A truth that *cannot* be re-derived is a WARNING naming the method and the field — never a silent skip — and the run reports the verified fraction | ERROR on mismatch |
| V8 | every stage has a non-empty, JSON-serialisable data block, with topics distinct enough to route | the data-supply protocol is incomplete | ERROR |
| V9 | fault and decision references resolve to real stages, methods and phases | a probe is configured against nothing | ERROR |
| V10 | one method does not carry truths from two stages of the same case unless the field sets are disjoint | the NF scorer merges a method's outputs across the whole trace, so the contestant must report one step per analysis or one of the two truths is judged failed | WARN |
| V11 | per phase, report whether anything in it is actually graded | a phase with no hard truth and no decision point costs nothing to skip. Reported per case rather than enforced, because a single atomic-tier case legitimately spans one phase; the corpus-level claim is asserted in `tests/test_phase_coverage.py` | WARN |

### Step 5 — add a smoke test and open a PR

Add the `case_id` to the parametrised list in the matching `tests/test_cases_native_*.py`
(validation and the seed-invariant sweep then run automatically) and open a pull request. A
green CI admits the case: the task builder (`tasks/builder.py`) discovers the new case on its
own and derives the T1/T2/T3 instances, the clean/dirty variants and the fault plans, with no
registration code anywhere.

## How the two kinds of case differ at onboarding

| | mini / synthetic case (`SIMULATED`) | expert case (`TRUE` / `RECONSTRUCTED`) |
|---|---|---|
| data | entirely seed-generated | extracted tables frozen as constants, or parameters inverted and regenerated from a seed |
| truth | 100 % derived on the spot | the expert's figures are `expected`; the verifiers re-check them (V7) |
| `parametric` | true | true when inverted, false when purely extracted |
| typical tier | T1 (one atomic task per stage) | T3 (whole case end to end, sliced per phase into T2) |
| de-identification | not needed | organisation name → industry bucket; the legal boundary decides public split or hold-out |
| `derivation` | `"derived via truth.verifiers.xxx, seed=N"` | `"expert report p.42, session output"` |

Every published case is in the left-hand column. The right-hand column describes the nine
held-out cases ([`HELD_OUT.md`](HELD_OUT.md)); none of them is in this repository.

## A second registry source, and why you will not see it here

`registry.discover()` accepts a second source besides case directories: a read-only bridge
over the frozen cases of the originating evaluation harness, registered through the same
`Case` model with `parametric=False`. Neither that harness nor its bridge module is part of
this repository, so in a public checkout `discover()` returns the native case directories
alone — `tests/test_public_corpus.py` asserts the bridge is absent. Where such a case was
later re-authored as a native parametric case, the native directory **shadows** the bridge
version, so evaluation scripts switch across without noticing; several published cases still
carry a `frozen.json` beside their generator as a self-contained data asset from that lineage.
Nothing about the five steps above changes for a re-authoring: it is a new directory that
happens to reuse an existing `case_id`.

## Canonical English case authoring

Author case metadata and generated data labels directly in English. English is the
canonical corpus language and the default build language; no Chinese arm is maintained.
The existing English renderings supplied the migration baseline. Do not reintroduce
translation dictionaries or bilingual case copies as a requirement for new cases.
A future Chinese corpus must be a separately versioned extension with independent
validation; it must not silently alter this release's task set or language labels.

Three hard rules remain:

1. **`topics` are routing keys, not prose.** Match Latin keys on word boundaries,
   longest first, with at least 3 alphanumeric characters (2 for mixed letters and
   digits, such as `y3`). Avoid collisions between stages in the same case.
2. **No statistical method name in `context` / `goal` / `label` / `topic`** (V3).
   Choosing the method is the measured capability. Translating a source description
   into a technical method name can inadvertently give away the answer.
3. **A `label` identifies a batch of data.** It must not tell the contestant what
   analysis to perform. Steward status and routing responses expose these labels.

Use opaque role codes such as `Appraiser A` for personal identifiers; never transliterate
personal or company names. Keep the provenance of source project reports accurate,
including their original language. Numerical data, truths, tolerances, stage and method
IDs, decision rules, order constraints, and fault plans must retain their semantics.

After authoring or translation, validate the English corpus and routing, scan the public
sources and generated agent-visible files for residual Chinese, and verify that the
numerical truth digest is unchanged when only language has changed. Historical run
artifacts must keep their original language/version attribution. The three archived
`frozen.json` source snapshots are byte-preserved exceptions, documented in
[the English migration contract](ENGLISH_MIGRATION.md); current generators do not load them.

## Authoring a v2 project case: when a fork is actually scoreable

A v2 project case is a Python module under `dmaic_bench/v2/cases/` exposing a module-level
`CASE: V2Case`; the registry finds it, and there is no `case.yaml`. Everything above about
determinism, generate-then-derive and method-name leaks still applies. What is specific to v2
is the decision graph, and one property of it is easy to get wrong and impossible to notice by
reading:

> **A fork can only be scored if each of its branches leads to work that no other branch leads
> to, and that has not already happened earlier on the route.**

Path Quality and Self-Consistency both recover the branch a contestant took from what it RAN,
because the fork's own node key is private and never reaches the agent. Where that recovery
fails, walking correctly and walking wrongly are the same trace, and every contestant scores
zero on the point whatever it does. Four ways to break it, all of them caught by
`tests/test_sc_branch_inference.py` and `tests/test_v2_graph_truth.py`, and all of them found
that way rather than by review:

1. **Both branches run nothing.** Two improvement nodes with no batch and no method are one
   node as far as scoring is concerned. Give at least one of them a real computation on a real
   batch — a post-change batch on the branch that acts is usually the honest answer.
2. **Both branches run the same method.** Two special-cause investigations that both test the
   run for a non-random pattern cannot be told apart. Make them do the different work they
   would really do.
3. **The winning branch's work already happened.** `capability.normal` at a baseline node puts
   `capability.normal` inside the convergent set of every branch downstream of it, so that
   branch appears to have been taken on every route. If a later node needs a second capability
   verdict, either the earlier node has to ask its question with a different method, or the
   later one does.
4. **One node is the target of two different forks.** The route that reaches it by the second
   edge carries the evidence for the branch the first fork did **not** take. Split it into two
   nodes: "the settings we varied explain nothing" and "the change we made did nothing" are
   different findings that happen to run the same computation.

`node_methods` is built over `case.node_data` only, so a node without a batch contributes no
methods to any of this — which is what makes a terminal remediation node readable as
abstention, and what makes an improvement node invisible unless it is given a batch.

Two more v2-specific rules worth stating:

- **A method that runs twice needs `"occurrence": n` on its `field_map` sources.** The default
  resolution merges every invocation with last-wins, so the second study's verdict answers for
  the first. `adb_c33` (a measurement study re-run after remediation) and `adb_c35` (two charts
  and two capability studies) both depend on the pin.
- **Do not publish a truth whose value a batch already contains.** `adb_c39`'s confirmation
  runs are tested against the level the charter requires rather than against the surface's own
  prediction, precisely so that batch does not hand over the number the optimiser was supposed
  to produce; `opt.predictedResponse` routes the graph and is deliberately absent from
  `truth_fields`.

- **A paired control chart is TWO charts, and a stability guard must read both.** The
  taxonomy's `flaggedCount` on `control_chart.xbar_r` and `control_chart.xbar_s` is the
  LOCATION chart's count; the dispersion chart is `flaggedRangeCount` / `flaggedSCount`. A
  guard that reads only the first passes a run whose within-subgroup spread is out of control
  — and the location limits it then trusts are `x̄̄ ± A2·R̄`, built out of exactly those
  ranges. `adb_c34` and `adb_c35` guard on the conjunction and each ship a seed where the
  means sit inside their limits while the ranges do not. The I-MR pair is the deliberate
  exception: the moving-range chart is largely redundant with the individuals chart and its
  runs rules inflate false alarms (Montgomery ISQC 6e §6.4, after Rigdon et al.), so those
  cases read the individuals chart alone. Thirteen shipped seeds carry an MR-chart flag under
  that convention.
- **A dispersion truth needs its own honesty cue.** `dmaic_bench/v2/cues.py` keys a cue on
  (method, output), so the location chart's vocabulary must not satisfy the dispersion
  chart's truth: a report that only ever says "X-bar" has not told us the ranges were read.

Run both suites before opening the PR — the case tests live in `tests/`, the packaging and
build tests in `harbor/tests/` and need `PYTHONPATH=harbor/src:.`.
