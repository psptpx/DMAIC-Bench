# Making the DEFINE phase gradeable in DMAIC-Bench

**Status:** design specification. No benchmark code is changed by this document.
**Date:** 2026-09-04
**Scope:** what a Define stage can and cannot contribute to NF / PQ / MS, the taxonomy and
verifier additions required, and one worked stage with real computed truths.

---

## 0. The measured problem this document responds to

Census over the 23 registered cases (`registry.discover()`, seed 1), which expand into the
372 built task instances:

| phase | stages | truths (seed 1) | decision points |
|---|---|---|---|
| define | **1** | **0** | **0** |
| measure | 48 | 27 | 26 |
| analyze | 61 | 43 | 7 |
| improve | 25 | 10 | 6 |
| control | 5 | 3 | 0 |
| (truths with `stage_id = None`) | — | 14 | — |

> **Public-release note.** This census, the 372-task figure and every per-case reference in
> this document are over the **full development corpus** — 23 cases at the time of counting,
> 24 once `adb_c24` was added. This repository publishes 15 of them and holds out the nine
> expert-derived cases (`adb_c03 c05 c07 c08 c10 c15 c16 c19 c20`), so a census re-run here
> returns smaller numbers. See [`HELD_OUT.md`](../HELD_OUT.md). The worked example in §5
> (`adb_c24`) and the Define stage named immediately below (`adb_c09`) are both in the public
> split and can be inspected directly.

The single Define stage in the corpus is `adb_c09/Q_Profile`, whose only method is
`meta.data_profiling` — a taxonomy entry with `canonical_outputs: []`, i.e. a method that
*cannot* carry a truth by construction. So Define currently touches exactly one scoring axis:
it adds one item to the `ms.recall` denominator. It contributes nothing to NF, nothing to PQ,
and (having no `metric_cue`) nothing to HN.

An agent that skips Define forfeits at most one MS-recall item on one case. The benchmark is
named for the full cycle and grades three fifths of it.

**A note on scope.** This document fixes Define. Control (5 stages, 3 truths at seed 1 — the
18 counted by the review are the same truths multiplied across seeds/tiers/variants, and 0
decision points) has a *different* deficiency: it already carries numeric truths, it is missing
decision points. That is a much cheaper fix and is out of scope here; see Appendix C.

---

## 1. What real Define work consists of

Enumerated from ASQ's *Six Sigma Handbook* (Pyzdek & Keller 3e, ch. 5), Juran's *Quality
Handbook* 6e §§ 12–13, and Montgomery *ISQC* 6e § 1.4, in the order a project actually does them:

1. **Project charter** — problem statement, business case, scope, team, timeline, sponsor sign-off.
2. **Voice of the Customer capture** — interviews, complaints, warranty text, surveys; raw and unstructured.
3. **VOC → CTQ translation** — turning "the seal leaks in winter" into a measurable characteristic with a target and a spec.
4. **Problem statement** — what, where, when, how big, stated without cause and without solution.
5. **Scoping** — which product lines / defect categories / process steps are in and out of the project boundary.
6. **Baseline quantification** — the current level of the project Y in defect, yield, rate or capability units, over a stated period.
7. **Goal setting** — the target value of Y and the date, derived from the baseline and a mandate or an entitlement.
8. **COPQ / financial case** — the money the current defect level costs, and the money the target recovers.
9. **Stakeholder and boundary definition** — SIPOC, process boundaries, RACI, risk and constraint register.
10. **Tollgate** — the sponsor's decision that the project is worth chartering.

Items 5–8 are arithmetic over records. Items 1, 2, 4, 9, 10 are writing and negotiation.
Item 3 is a translation whose *output* can sometimes be pinned to a downstream measurable
route and usually cannot.

---

## 2. Honest three-way split

### 2 (a) NUMERICALLY GRADEABLE

Everything in this bucket satisfies four admissibility conditions. These are the test any
future proposal must pass; they are stricter than the current V6/V7 gates and are the reason
this bucket is short.

> **A1 — single-block computable.** V7 calls `REFERENCE_IMPLS[method_id](blocks[stage_id])`
> with exactly one stage payload. A truth that needs two stages' data cannot be verified
> and is not admissible. (Practical consequence: the improvement mandate must live *inside*
> the baseline ledger block, not in a separate "management memo" stage.)
> **A2 — generator-independent.** The verifier recomputes from the payload with scipy/numpy
> and never imports the generator or a contestant's solver.
> **A3 — convention pinned in the payload, not in the verifier.** Wherever practice offers two
> conventions (the 1.5σ shift, the COPQ cost scope, the Pareto vital-few threshold), the
> payload declares which one, the verifier reads the declaration, and the verifier *refuses*
> (`NotVerifiable`) when it is absent. A verifier with a silent default silently produces a
> truth that half the field would compute differently — that is the "wrong convention
> silently produces an unverifiable truth" failure the brief warns about.
> **A4 — seed-invariant conclusion.** The generator asserts, over ≥500 seeds, that the
> branch/threshold consequences do not flip (`_assert_invariants`), with a stated margin.

| # | Quantity | method_id | canonical field | Reference computation |
|---|---|---|---|---|
| 1 | Defects per unit | `define.baseline_defect_metrics` | `dpu` | `D / U` |
| 2 | Defects per opportunity | `define.baseline_defect_metrics` | `dpo` | `D / (U · O)` |
| 3 | Defects per million opportunities | `define.baseline_defect_metrics` | `dpmoLedger` | `1e6 · D / (U · O)` over **all** ledger categories |
| 4 | In-boundary DPMO | `define.baseline_defect_metrics` | `dpmoInScope` | same, restricted to categories whose `ownership` is in the payload's declared `scopeBoundary.include` |
| 5 | Defective-unit rate (PPM) | `define.baseline_defect_metrics` | `ppmDefective` | `1e6 · Dᵤ / U` (defective **units**, not defects) |
| 6 | First-pass yield | `define.baseline_defect_metrics` | `firstPassYield` | `1 − Dᵤ / U` |
| 7 | Long-term Z | `define.baseline_defect_metrics` | `zLongTerm` | `scipy.stats.norm.ppf(1 − dpo_inScope)` |
| 8 | Shifted sigma level | `define.baseline_defect_metrics` | `sigmaLevel` | `zLongTerm + payload["sigmaShift"]` |
| 9 | Rolled throughput yield | `define.rolled_throughput_yield` | `rty` | `Π_i (1 − dᵢ/uᵢ)` over the declared step table |
| 10 | Worst step yield | `define.rolled_throughput_yield` | `minStepYield` | `min_i (1 − dᵢ/uᵢ)` |
| 11 | Vital-few category count | `quality.pareto` (extended) | `vitalFewCount` | smallest `k` with cumulative share ≥ `vitalFewThresholdPct` |
| 12 | Vital-few cumulative share | `quality.pareto` (extended) | `vitalFewCumulativePct` | cumulative share at that `k` |
| 13 | Cost of poor quality | `define.copq` | `copqTotal` | `Σ count·unitCost` over categories listed in `copqScope` |
| 14 | COPQ per unit | `define.copq` | `copqPerUnit` | `copqTotal / U` |
| 15 | Annualized COPQ | `define.copq` | `copqAnnualized` | `copqTotal · periodsPerYear` |
| 16 | Target level | `define.improvement_target` | `targetDpmo` | mandate applied to the declared basis metric |
| 17 | Target sigma | `define.improvement_target` | `targetSigmaLevel` | `norm.ppf(1 − targetDpmo/1e6) + sigmaShift` |
| 18 | Entitlement | `define.improvement_target` | `entitlementDpmo` | baseline recomputed with the vital-few categories driven to zero |

Notes on why each is defensible as *Define* work and not a relabelled Measure item:

* 1–8 are the project **baseline**, computed from a records ledger the organisation already
  has. They require no measurement system study and no sampling plan — which is exactly why
  they belong in Define and why they must not carry `msa_passed` / `stability_confirmed`
  prerequisites (see §3).
* 4 is the one that makes **scoping numerically gradeable**: the ledger declares each
  category's `ownership`, the charter declares the boundary, and an agent that ignores the
  boundary produces a number that differs from the truth by more than any tolerance. This is
  the strongest pattern in this document — *route-by-number*: the routing decision is verified
  by NF rather than by a PQ branch that no trace can evidence. Prefer it wherever it fits.
* 11–12 are scoping, not defect analysis. They reuse `quality.pareto` deliberately (see §3.4).
* 16–18 are goal setting. They are arithmetic, and low-difficulty in isolation; their value is
  **error propagation** — a wrong baseline or a wrong boundary makes the target wrong too, so
  they convert a single Define mistake into a visible multi-truth failure, which is what
  makes a skipped Define phase expensive.

### 2 (b) ROUTING-GRADEABLE as decision points

PQ judges a decision point from an explicit `route_decisions` entry if the system emits one,
otherwise by `branch_evidence` — a map from branch name to method_ids whose *successful
execution* counts as walking that branch. A point with no signal at all is `unknown`, and
`unknown` stays in the denominator.

> **The hard constraint on every Define decision point.** Because evidence is method-based,
> **two branches that run the same methods are indistinguishable to PQ**. A decision point
> whose branches differ only in prose is not evidence-observable; adding it would score
> "does your adapter emit `route_decisions`" rather than "did you decide correctly", which
> systematically penalises every system whose adapter does not emit them. Three of the four
> candidate Define decision points below survive this test; the fourth does not and is
> recommended for deletion rather than for a workaround.

**DP-1 `define_y_selection` — which candidate CTQ becomes the project Y.**

* Rule: the project Y is the output characteristic that (i) the customer complaint names,
  (ii) exists as a measured record covering the declared baseline period, and (iii) is
  measurable without a new measurement system. Where candidates conflict, the customer-named,
  historically-recorded characteristic wins.
* Source: Pyzdek & Keller, *The Six Sigma Handbook* 3e § 5 (CTQ selection); George,
  *Lean Six Sigma Pocket Toolbook* (Y selection).
* Evidence-observable **only if the case is built so the candidates imply different downstream
  method families.** Concretely: candidate A is an attribute pass/fail ledger (⇒
  `capability.binomial`, `control_chart.p`), candidate B is a continuous bench measurement on
  n=12 with no spec limits (⇒ `capability.normal`). Branch evidence:
  ```yaml
  branch_evidence:
    attribute_y: [capability.binomial, control_chart.p, "family:capability"]   # see caveat
    continuous_y: [capability.normal]
  ```
  Caveat: `family:capability` matches both, so it must **not** be used — list method_ids.
* Case-design obligation: a case that cannot make the two candidates route to different
  methods must not carry DP-1.

**DP-2 `define_baseline_adequacy` — is the baseline sufficient to commit to a target.**

* Rule: a numeric target may be committed only when the baseline's uncertainty is smaller than
  the improvement it mandates. Operationally: with a Clopper–Pearson 95% interval on the
  baseline proportion, if the interval half-width ≥ the mandated absolute reduction, the
  correct action is to quantify that uncertainty (or extend the collection window) before
  committing; otherwise commit.
* Source: Montgomery *ISQC* 6e § 4.3 (interval estimation of a proportion) for the interval;
  ASQ Define-tollgate practice for the "baseline before target" requirement.
* Branch evidence:
  ```yaml
  branch_evidence:
    quantify_before_target: [basic.one_proportion, power.two_proportions]
    commit_target:          [define.improvement_target]
  ```
  This is evidence-observable: the "quantify first" branch runs an interval/power method that
  the "commit" branch has no reason to run.
* Case-design obligation: the firing side must be seed-stable. In the worked example
  (n = 48 210, p̂ = 0.02502) the exact CI half-width is 0.00140 against a mandated absolute
  reduction of 0.0125 — a factor of 9, stable under any reseeding. A companion case with
  n = 180, p̂ = 0.0389, half-width 0.0314 fires the other way by a factor of 1.6, which is
  **too narrow**; that case must be built with n ≤ 60 or dropped.

**DP-3 `define_scope_boundary` — scope a defect category in or out.**

* Rule: a defect category whose owning process lies outside the declared project boundary is
  excluded from the project baseline and from the improvement target, *even when it is one of
  the vital few*.
* Source: Juran's *Quality Handbook* 6e § 12 (project nomination and boundaries).
* **Recommendation: do not encode this as a PQ decision point.** Both branches run the same
  methods on the same block, so it is not evidence-observable. Encode it as the numeric pair
  `dpmoLedger` / `dpmoInScope` (§2a #3–4) instead: an agent that scopes wrongly fails a hard
  NF truth. This is strictly stronger than an `unknown`-prone PQ point and costs no new
  machinery.

**DP-4 `define_charter_completeness` — is the charter fit to pass the tollgate.**

* **Not admissible.** There is no method trace that distinguishes a complete charter from an
  incomplete one, and no textbook rule that maps to a deterministic branch. See §2c.

**Order constraints** (partial order over successful steps, PQ's second half):

```yaml
- before: define.baseline_defect_metrics
  after:  define.improvement_target
  source: "Pyzdek & Keller, Six Sigma Handbook 3e ch.5 (a project goal is stated relative to a quantified baseline)"
- before: quality.pareto
  after:  define.improvement_target
  source: "Juran's Quality Handbook 6e §12 (vital-few scoping precedes entitlement-based goal setting)"
```
The first is textbook-tight. The second is only correct for cases whose target is entitlement-
derived (`mandate.type: entitlement`); it must not be attached to relative-reduction cases,
where Pareto is not a prerequisite of the target.

A third candidate — `define.baseline_defect_metrics` before `family:capability` ("baseline
before capability study") — is **not** recommended. DMAIC phase order is a project-management
convention, not a statistical prerequisite, and encoding it would punish a system that
computes capability first and reports a correct baseline anyway. Do not add order constraints
that merely restate the phase names.

### 2 (c) NOT AUTOMATICALLY GRADEABLE

Stated plainly, with no proxy offered:

| Define artefact | Why no automatic score is possible |
|---|---|
| **Project charter narrative** | The graded property is whether a sponsor would sign it. There is no reference implementation of a sponsor. |
| **Problem statement quality** | The textbook criteria ("no cause, no solution, what/where/when/how big") are linguistic properties of free text. A regex for the four slots measures template-filling, not problem framing, and would be gamed by one sentence per slot. |
| **VOC capture fidelity / coverage** | Requires judging whether the customer's actual concern survived transcription. Scoring it needs the ground-truth concern, which only exists if we wrote it — i.e. the "truth" would be an artefact of the generator, violating A2. |
| **VOC → CTQ translation** (general case) | Admissible *only* in the constrained form where the CTQ choice determines a downstream measurable route (that is DP-1, and it is a routing score, not a translation score). The general act of proposing a measurable characteristic has an open answer set. |
| **SIPOC completeness** | Counting boxes measures diligence in filling a template. A SIPOC with five suppliers listed is not better than one with three unless the two extra are real, which requires knowing the real process. |
| **Stakeholder analysis / RACI** | Same, and additionally the correct answer is organisation-specific. |
| **Scope-boundary *rationale*** | The *consequence* of the boundary is numerically gradeable (DP-3 → `dpmoInScope`). The *argument* for drawing it there is not. |
| **Business case narrative** | The COPQ arithmetic is gradeable (§2a #13–15). Whether the project is worth doing given strategy, capacity and risk is a management judgement. |
| **Tollgate decision** | Terminal judgement over all of the above. |

**Recommendation.** Exclude all of the above from TGS and from every aggregate metric.
If the paper wants to report on them at all, report them on a **separate, clearly-labelled
human axis** ("D-Human"), with: a published rubric of at most 5 binary items, two independent
raters, Cohen's κ reported, a stated sample (e.g. 3 systems × 10 tasks — the full grid is not
affordable), and **never** folded into TGS or any harmonic mean. A human axis that is
occasionally reported is honest; a human axis that silently enters the headline number
converts a small annotated sample into a claim about all 372 tasks.

**Do not add an LLM judge for these.** An internal measurement-validity audit of this
benchmark — not published in this repository — has already documented that a text-derived
metric here can be non-monotonic in the property it claims to measure — the fabrication rate moved from 1.0000 to 0.0050 on the
same false statement when surrounding supported numbers were added, a swing larger than the
between-system differences the paper reports. Adding a second, softer text-derived axis to
the same paper is the opposite of the fix that finding calls for. "This part of Define is not
measurable here" is the correct entry in the results table.

---

## 3. Taxonomy additions

New family: **`define`**. Three new methods, plus two new canonical outputs on an existing
method. Written in the exact `taxonomy.yaml` schema, to be inserted after the `meta` block.

```yaml
  # ---- define ----------------------------------------------------------------
  # Project-framing quantities computed from records the organisation already holds.
  # applicability.data_type is deliberately `any`: these run before the Y's data type is
  # settled, and `any` keeps ms.py's misuse judge from flagging them on continuous cases.
  # prerequisites is deliberately empty: a Define baseline precedes MSA and stability by
  # construction, and declaring msa_passed here would make the correct order a violation.
  - method_id: define.baseline_defect_metrics
    spec_keys: []
    aliases: [baseline defect metrics, project baseline, dpmo baseline, process sigma baseline,
              defect ledger baseline, baseline quantification]
    family: define
    applicability: {data_type: any, prerequisites: []}
    canonical_outputs:
      - {name: dpu, tol_class: exact}
      - {name: dpo, tol_class: exact}
      - {name: dpmoLedger, tol_class: exact}
      - {name: dpmoInScope, tol_class: exact}
      - {name: ppmDefective, tol_class: exact}
      - {name: firstPassYield, tol_class: exact}
      - {name: zLongTerm, tol_class: tight}
      - {name: sigmaLevel, tol_class: tight}

  - method_id: define.rolled_throughput_yield
    spec_keys: []
    aliases: [rolled throughput yield, rty, first pass yield chain, process yield rollup]
    family: define
    applicability: {data_type: any, prerequisites: []}
    canonical_outputs:
      - {name: rty, tol_class: exact}
      - {name: minStepYield, tol_class: exact}
      - {name: normalizedYield, tol_class: soft}

  - method_id: define.copq
    spec_keys: []
    aliases: [cost of poor quality, copq, quality cost, failure cost]
    family: define
    applicability: {data_type: any, prerequisites: []}
    canonical_outputs:
      - {name: copqTotal, tol_class: exact}
      - {name: copqPerUnit, tol_class: exact}
      - {name: copqAnnualized, tol_class: exact}

  - method_id: define.improvement_target
    spec_keys: []
    aliases: [improvement target, project goal, target setting, entitlement analysis]
    family: define
    applicability: {data_type: any, prerequisites: []}
    canonical_outputs:
      - {name: targetDpmo, tol_class: exact}
      - {name: targetSigmaLevel, tol_class: tight}
      - {name: entitlementDpmo, tol_class: exact}
      - {name: requiredReductionPct, tol_class: exact}
```

Extension to the existing Pareto entry (append two outputs; do not rename `topCategoryPct`):

```yaml
  - method_id: quality.pareto
    # ... unchanged spec_keys / aliases / family / applicability ...
    canonical_outputs:
      - {name: topCategoryPct, tol_class: exact}
      - {name: vitalFewCount, tol_class: exact}          # NEW
      - {name: vitalFewCumulativePct, tol_class: exact}  # NEW
```

### 3.1 Why `define.*` and not new families per artefact

One family keeps `ms.py`'s `family:` evidence shorthand usable (`family:define` = "did any
project framing happen at all") and keeps the taxonomy's 12→13 family count honest. Four
method_ids rather than one because their **payload shapes differ** (ledger / step table /
cost table / mandate) and a verifier reads exactly one shape.

### 3.2 `spec_keys` is empty on purpose

`spec_keys` maps the private contestant's solver spec onto a method; that engine has no
Define spec today. `Taxonomy.__init__` only rejects *duplicate* non-empty keys, so several
empty lists are legal. When that engine adds Define specs, the keys go here and nothing else
changes.

### 3.3 The scoping quantities reuse `quality.pareto` — and why that forces a new validator gate

Giving scoping its own `define.scope_pareto` would create a naming trap: a system that
correctly computes a Pareto and reports it under the canonical `quality.pareto` would score
0 on a `define.scope_pareto` truth, and `nf.py` explicitly declines to score naming. So the
Define scoping stage requires `quality.pareto` and carries the two **new field names**.

That creates a different hazard, and it must be gated:

> **`nf.merged_outputs` merges every successful step of a `method_id` across the whole trace,
> last-key-wins.** Truths are keyed by `(method_id, field)`; `stage_id` is metadata that NF
> never reads. So if one case runs `quality.pareto` in a Define scoping stage *and* again in a
> Measure stage on different counts, the two output sets collide and NF may resolve a truth
> against the wrong stage's numbers. This hazard already exists in the corpus (`adb_c03` — a
> held-out case — runs `capability.binomial` in three stages against one soft truth) but
> Define makes it routine.

**New gate V10 (proposed):** *no `method_id` may carry truths from more than one `stage_id`
within a case unless the two stages' truth fields are disjoint.* Cheap to implement in
`core/validation.py`, no runtime cost, and it forecloses a silent mis-scoring.

Optionally (a strictly larger change, listed for completeness and **not** recommended for this
submission): make NF stage-aware by having adapters tag steps with `stage_id` and having
`merged_outputs` filter on `truth.stage_id` when present. This is a wire-format change
affecting every adapter and every stored run; V10 gets 95% of the benefit for none of it.

### 3.4 Tolerances: NF compares absolutely, and Define is the first phase with large magnitudes

`nf.check_values` uses `abs(v - expected) <= tol` — **absolute**, always, even for the class
documented as "relative 1e-6". Every existing truth is a p-value, an R², a Cpk or a Z: all
O(1)–O(100). Define introduces DPMO (O(10³)) and COPQ (O(10⁴–10⁶) currency units). A truth of
2195.256862 with `tol_defaults.exact = 1e-6` would fail every agent that writes "2195.3".

**Rule for Define generators:** never inherit `tol_defaults`; set
`tol = max(display_quantum, 1e-3 · |expected|)` per quantity, where `display_quantum` is the
last digit a report would plausibly print (0.1 for DPMO, 1.0 for currency, 0.001 for a yield
fraction, 0.01 for a sigma level). Record the choice in `derivation`.

Two related HN facts, both already in our favour: `hn.extract_numbers` parses
thousands-grouped forms ("60,651") as one number, and emits both readings of a percentage.
Currency symbols do not interfere. `metric_cue` regexes must nonetheless be narrow — `DPMO`
and `COPQ` are good cues, `baseline` is not (it matches prose lines carrying unrelated digits).

---

## 4. Reference implementations for `truth/verifiers.py`

Style follows the file: take one stage payload, return `{canonical_field: float}`, raise
`NotVerifiable` for an unrecognised or under-specified shape, accept new shapes *in addition
to* old ones, and document every convention in the docstring.

### 4.0 The convention decisions, stated up front

**DPMO.** `DPMO = 1e6 · D / (U · O)` where `D` = number of **defects** (a unit may carry
several), `U` = units inspected, `O` = opportunities per unit. The competing usage — DPMO
computed from *defective units* — is a different quantity and gets a different field,
`ppmDefective = 1e6 · Dᵤ / U`. Both are emitted so a system using either convention has a
field to hit, and neither is a synonym of the other. `opportunitiesPerUnit` is **required**;
defaulting it to 1 would silently turn a DPMO into a PPM, which is precisely the
"unverifiable truth" failure mode, so its absence raises `NotVerifiable`.

**Sigma level.** Two things are reported, deliberately separated:
* `zLongTerm = Φ⁻¹(1 − DPO)` — the **unshifted** long-term Z. This is the convention the
  benchmark already uses: `verifiers.capability_binomial` computes
  `processZ = norm.ppf(1 - p)`, and Minitab labels that quantity "process Z". Keeping Define
  consistent with the existing corpus matters more than matching any single textbook.
* `sigmaLevel = zLongTerm + payload["sigmaShift"]` — the **shifted** "process sigma" of the
  Six Sigma literature. The shift is **read from the payload**, never defaulted; a payload
  without `sigmaShift` yields no `sigmaLevel` truth at all. Cases should set `1.5` and cite
  Harry & Schroeder / Bothe. Making the shift data removes the single most common source of
  a silently-wrong Define truth: two competent analysts differing by exactly 1.5.

`DPO` for the Z conversion is the **in-scope** DPO (`dpmoInScope/1e6`), because the project's
sigma level is the sigma level of the project's scope. The payload's `scopeBoundary` decides
this, so it is declared, not assumed.

**COPQ.** `copqTotal = Σ count · unitCost` over exactly the categories named in
`payload["copqScope"]`. Cases should set `["internal_failure", "external_failure"]` (Juran /
Campanella: failure costs; prevention and appraisal are cost of *good* quality). The broader
"COQ = P + A + IF + EF" reading is a *different quantity*; if a case wants it, it declares the
broader scope and the field is still `copqTotal` for that case's declared scope. The verifier
never chooses. Deciding *which* buckets belong in COPQ is a judgement and is therefore
removed from grading by declaration (§2c).

**RTY.** `rty = Π_i (1 − dᵢ/uᵢ)` over the declared step table — the exact product of step
yields. The Poisson approximation `RTY ≈ e^(−DPU)` is a different number and is **not
admissible as a hard truth**; where a case wants it, emit it as `normalizedYield`-adjacent
soft output only, never as the primary `rty`.

**Vital few.** `vitalFewCount` = the smallest `k` such that the cumulative share of the `k`
largest categories ≥ `payload["vitalFewThresholdPct"]`. The threshold is read from the
payload (cases set 80). Ties are broken by `(-count, category_name)` so the ordering is
deterministic when two categories are equal. Generators must additionally assert a **margin**:
the cumulative share at `k` and at `k−1` must each sit ≥ 3 percentage points away from the
threshold across all seeds, or the truth is a coin-flip under reseeding.

### 4.1 `define.baseline_defect_metrics`

```
baseline_defect_metrics(payload) -> dict
```

**Payload keys**

| key | type | required | meaning |
|---|---|---|---|
| `unitsInspected` | int or list[int] | yes | `U`; a list is summed |
| `defectsFound` | int, or omitted when `defectCategories` present | see below | `D`, total defects |
| `defectiveUnits` | int | no | `Dᵤ`; enables `ppmDefective` / `firstPassYield` |
| `opportunitiesPerUnit` | int ≥ 1 | yes | `O` |
| `defectCategories` | list[{name, count, ownership}] | no | per-category ledger |
| `scopeBoundary` | {`include`: list[str]} | required iff `defectCategories` present | ownership labels inside the charter boundary |
| `sigmaShift` | float | no | enables `sigmaLevel` |

**Algorithm**

1. `U = sum(unitsInspected)`; raise `NotVerifiable` if `U <= 0`.
2. `O = int(opportunitiesPerUnit)`; raise if absent or `< 1`.
3. `D` = `sum(c["count"] for c in defectCategories)` when present, else `defectsFound`;
   raise if neither. When both are present they must agree to within 1e-9 — a mismatch is a
   corrupt payload and raises, it is not reconciled.
4. `dpu = D/U`; `dpo = dpu/O`; `dpmoLedger = 1e6·dpo`.
5. If `defectCategories` present: `D_in = Σ count where ownership ∈ scopeBoundary.include`;
   `dpmoInScope = 1e6·D_in/(U·O)`. Absent categories ⇒ no `dpmoInScope` key at all (V7 skips
   fields the reference does not produce — it does **not** treat them as zero).
6. If `defectiveUnits` present: `ppmDefective = 1e6·Dᵤ/U`, `firstPassYield = 1 − Dᵤ/U`.
   Raise if `Dᵤ > U`.
7. `p = dpmoInScope/1e6` if it exists else `dpo`. `zLongTerm = norm.ppf(1 − p)`.
8. If `sigmaShift` present: `sigmaLevel = zLongTerm + sigmaShift`.

**Edge cases (all raise `NotVerifiable` rather than returning a plausible wrong number)**

* `D == 0` ⇒ `p == 0` ⇒ `zLongTerm = +inf`. Raise. A zero-defect baseline is not a Six Sigma
  project baseline, and `float('inf')` would pass any tolerance comparison the way NaN
  already did in a previously-fixed gate bug.
* `p ≥ 1` (more in-scope defects than opportunities) ⇒ `−inf`. Raise.
* `p` extremely small (`< 1e-9`): `norm.ppf` is still finite but the case is degenerate —
  raise, and let the generator pick a realistic ledger.
* `scopeBoundary.include` empty, or matching no category ⇒ `D_in == 0` ⇒ raise.
* `unitsInspected` as a list of unequal length to anything else: it is only summed, so no
  alignment requirement — but a list containing a non-number raises.
* Categories present without `scopeBoundary`: raise. The boundary is the whole point of the
  in-scope field; defaulting to "everything in scope" would silently make `dpmoInScope`
  identical to `dpmoLedger` and destroy the scoping truth.

### 4.2 `define.rolled_throughput_yield`

```
rolled_throughput_yield(payload) -> {"rty", "minStepYield", "normalizedYield"}
```
Payload: `{"steps": [{"name": str, "units": u, "defectiveUnits": d}, ...]}`, ≥ 2 steps.
`yieldᵢ = 1 − dᵢ/uᵢ`; `rty = Π yieldᵢ`; `minStepYield = min yieldᵢ`;
`normalizedYield = rty ** (1/n)` (soft — it is a convention-variant summary).
Raise when: fewer than 2 steps, any `uᵢ ≤ 0`, any `dᵢ > uᵢ`, any `yieldᵢ == 0` (a zero
collapses the product and hides every other step).

### 4.3 `define.copq`

```
copq(payload) -> {"copqTotal", "copqPerUnit", "copqAnnualized"}
```
Payload: `{"costItems": [{"category", "name", "count", "unitCost"}, ...],
`"copqScope": [category, ...]`, `"unitsProduced": U`, `"periodsPerYear": k` (optional),
`"currency": str` (ignored by the verifier)}`.
`copqTotal = Σ count·unitCost over items whose category ∈ copqScope`;
`copqPerUnit = copqTotal / U`; `copqAnnualized = copqTotal · periodsPerYear` (omitted when
`periodsPerYear` is absent — never defaulted to 12 or 4).
Raise when: `copqScope` absent or empty; a scope entry names no item (a typo would silently
drop a whole cost bucket); any negative `count`/`unitCost`; `U ≤ 0` for `copqPerUnit`.
Floating-point note: sum in **declaration order** so the value is reproducible bit-for-bit
across runs, and round only at `TruthEntry` construction.

### 4.4 `define.improvement_target`

```
improvement_target(payload) -> {"targetDpmo", "targetSigmaLevel", "entitlementDpmo",
                                "requiredReductionPct"}
```
Payload adds, to the §4.1 ledger keys (A1: same block):
`"mandate": {"type": "relative_reduction"|"absolute_level"|"entitlement",
             "basis": "dpmoInScope"|"dpmoLedger", "value": v}`.

* `relative_reduction`: `targetDpmo = basis · (1 − v)`, `0 < v < 1`.
* `absolute_level`: `targetDpmo = v`; raise if `v ≥ basis` (a "target" no better than the
  baseline is a payload error).
* `entitlement`: `entitlementDpmo` = the basis recomputed with the vital-few categories
  (per §4.0, threshold from the same payload) driven to zero; `targetDpmo = entitlementDpmo`.
  Requires `defectCategories`.
* `requiredReductionPct = 100 · (basis − targetDpmo)/basis`.
* `targetSigmaLevel = norm.ppf(1 − targetDpmo/1e6) + sigmaShift` (omitted without a shift).
* Raise when `mandate` absent, `basis` names a metric this payload cannot produce (e.g.
  `dpmoInScope` with no categories), `targetDpmo ≤ 0`, or `v` out of range.

### 4.5 `quality.pareto` — extension

Add two outputs and one accepted payload shape; keep every existing shape and
`topCategoryPct` byte-identical.

* New accepted shape: `defectCategories: [{"name": str, "count": n}, ...]` (the Define ledger
  shape) alongside today's `counts` list/dict.
* `vitalFewThresholdPct` read from the payload; **absent ⇒ neither new field is produced**
  (so V7 skips them) rather than defaulting to 80 inside the verifier.
* Sort by `(-count, str(name))`; walk the cumulative share; `vitalFewCount = k`,
  `vitalFewCumulativePct` = cumulative share at `k`.
* Raise on: empty counts, total ≤ 0, any negative count, threshold outside `(0, 100]`.
* `topCategoryPct` semantics are unchanged, and `vitalFewCumulativePct` must **not** be added
  to `nf.FIELD_SYNONYMS` under `topCategoryPct` — `nf.py` already documents that a wrong-scale
  twin matching by name turns "absent" into "failed".

### 4.6 Registration

```python
REFERENCE_IMPLS = {
    ...,
    "define.baseline_defect_metrics": baseline_defect_metrics,
    "define.rolled_throughput_yield": rolled_throughput_yield,
    "define.copq": copq,
    "define.improvement_target": improvement_target,
}
```

---

## 5. Worked Define stage, end to end

A new case `adb_c24` (`industry: electronics`, `y_type: attribute_proportion`, `tier: T3`,
`provenance: SIMULATED`). Only its Define portion is shown. Every number below was computed
with scipy/numpy from the payload as printed — they are the actual truths, not illustrations.

### 5.1 `case.yaml` fragment

```yaml
context: |
  We assemble sealed inline power modules for two OEM customers. Over the past twelve months
  the warranty desk has logged a rising number of returned modules, and the OEM quality team
  has put us on a corrective-action plan. We hold a complete returns ledger for the period,
  with each return classified by the failure seen at teardown and by which plant or supplier
  owns the process that produced it; the firmware timeout class is produced entirely by our
  module supplier under their own change control, and our corrective-action plan covers only
  the processes inside our own plant. Finance keeps a costed breakdown of what the returns
  cost us. The OEM has asked for a halving of the return level within the plan period.

goal: |
  Establish, from the returns ledger and the cost breakdown, how bad the problem inside our
  own plant currently is, which failure classes account for most of it, what the halving
  commitment means as a concrete numeric target, and what the current level costs per year.
  State every figure with the records it came from.

stages:
  - stage_id: D_Charter
    phase: define
    label: Returns ledger and charter mandate
    topics: [returns ledger, charter, mandate, baseline, warranty]
    summary_fact: "In-boundary baseline established at 2195.3 DPMO (sigma level 4.35); OEM target is a 50% reduction."
    methods:
      - method_id: define.baseline_defect_metrics
        required: true
      - method_id: define.improvement_target
        required: true
      - method_id: quality.pareto
        required: true
  - stage_id: D_Cost
    phase: define
    label: Costed returns breakdown
    topics: [cost, finance, copq, money]
    summary_fact: "COPQ over the period is 60,651 currency units (1.258 per unit produced)."
    methods:
      - method_id: define.copq
        required: true
  # ... M_/A_/I_/C_ stages omitted ...
```

Leakage check (V3): the context names no statistical method. "DPMO", "Pareto", "sigma level"
appear **only** in `summary_fact` (which is shown to later-phase T2 slices as an established
fact, exactly as intended) and never in `context`/`goal`, which V3 scans. Note that the
existing `_LEAKAGE_PATTERNS` includes `pareto` — a Define case must therefore describe
scoping as "which failure classes account for most of it", never as "Pareto".

### 5.2 The two payload blocks

```json
{
  "D_Charter": {
    "period": "2025-07-01..2026-06-30",
    "periodsPerYear": 1,
    "unitsInspected": 48210,
    "defectiveUnits": 1206,
    "opportunitiesPerUnit": 12,
    "sigmaShift": 1.5,
    "vitalFewThresholdPct": 80,
    "scopeBoundary": {"include": ["in_scope"]},
    "defectCategories": [
      {"name": "seal_leak",        "count": 660, "ownership": "in_scope"},
      {"name": "connector_fit",    "count": 410, "ownership": "in_scope"},
      {"name": "firmware_timeout", "count": 274, "ownership": "supplier_owned"},
      {"name": "cosmetic_scratch", "count": 120, "ownership": "in_scope"},
      {"name": "label_misprint",   "count":  80, "ownership": "in_scope"}
    ],
    "mandate": {"type": "relative_reduction", "basis": "dpmoInScope", "value": 0.50}
  },
  "D_Cost": {
    "period": "2025-07-01..2026-06-30",
    "periodsPerYear": 1,
    "unitsProduced": 48210,
    "currency": "CU",
    "copqScope": ["internal_failure", "external_failure"],
    "costItems": [
      {"category": "internal_failure", "name": "rework_labour",        "count":   612, "unitCost":    18.50},
      {"category": "internal_failure", "name": "scrap",                "count":   156, "unitCost":    42.00},
      {"category": "external_failure", "name": "warranty_replacement", "count":   388, "unitCost":    96.00},
      {"category": "external_failure", "name": "return_freight",       "count":   388, "unitCost":    14.25},
      {"category": "appraisal",        "name": "final_inspection",     "count": 48210, "unitCost":     0.35},
      {"category": "prevention",       "name": "operator_training",    "count":     1, "unitCost": 12000.00}
    ]
  }
}
```

The two cost buckets outside `copqScope` are present on purpose: they are the trap for a
system that sums the whole cost table. `copqTotal` = 60 651, whole-table `coqTotal` = 89 524.5
— far outside any defensible tolerance, so the mistake is caught, while the *judgement* of
which buckets belong was removed from grading by the payload's own declaration.

### 5.3 Truths, with tolerances and derivations

Computed: `D = 1544`, `D_in = 1270`, `U = 48210`, `O = 12`, `Dᵤ = 1206`.

| method_id | field | expected | tol | soft | metric_cue | how |
|---|---|---|---|---|---|---|
| `define.baseline_defect_metrics` | `dpu` | 0.03202655 | 1e-5 | no | `DPU\|defects per unit` | 1544/48210 |
| `define.baseline_defect_metrics` | `dpmoLedger` | 2668.879209 | 0.5 | no | `DPMO` | 1e6·1544/(48210·12) |
| `define.baseline_defect_metrics` | `dpmoInScope` | 2195.256862 | 0.5 | no | `DPMO` | 1e6·1270/(48210·12) |
| `define.baseline_defect_metrics` | `ppmDefective` | 25015.556938 | 5.0 | no | `PPM\|defective` | 1e6·1206/48210 |
| `define.baseline_defect_metrics` | `firstPassYield` | 0.97498444 | 1e-4 | no | `yield` | 1 − 1206/48210 |
| `define.baseline_defect_metrics` | `zLongTerm` | 2.84865010 | 0.01 | no | `Z\b\|long.term Z` | `norm.ppf(1 − 0.0021952569)` |
| `define.baseline_defect_metrics` | `sigmaLevel` | 4.34865010 | 0.01 | no | `sigma level` | 2.84865 + 1.5 |
| `quality.pareto` | `topCategoryPct` | 42.746114 | 0.05 | no | `seal leak\|largest` | 660/1544 |
| `quality.pareto` | `vitalFewCount` | 3 | 0 | no | `vital few\|account for` | k with cum ≥ 80% |
| `quality.pareto` | `vitalFewCumulativePct` | 87.046632 | 0.05 | no | `cumulative` | (660+410+274)/1544 |
| `define.improvement_target` | `targetDpmo` | 1097.628431 | 0.5 | no | `target` | 2195.2569 · 0.5 |
| `define.improvement_target` | `targetSigmaLevel` | 4.56246017 | 0.01 | no | `target.{0,20}sigma` | `norm.ppf(1 − 1097.63e-6) + 1.5` |
| `define.improvement_target` | `requiredReductionPct` | 50.0 | 1e-6 | no | `reduction` | by construction |
| `define.copq` | `copqTotal` | 60651.0 | 1.0 | no | `COPQ\|cost of poor quality` | 612·18.5 + 156·42 + 388·96 + 388·14.25 |
| `define.copq` | `copqPerUnit` | 1.25805849 | 0.005 | no | `per unit.{0,20}cost` | 60651/48210 |

Tolerances follow §3.4: display quantum, not `tol_defaults`. `vitalFewCount` is an integer, so
`tol = 0` is correct and safe (`abs(v−3) <= 0`).

`derivation` for every entry:
`"derived via truth.verifiers.<fn> (scipy 1.14.1), seed=<s>; conventions: DPMO over defects with O=12 opportunities/unit, sigma shift 1.5 declared in payload, COPQ scope = internal+external failure declared in payload"`,
`verified_by=("scipy",)`.

**Generator invariants** (`_assert_invariants`, asserted over seeds 1..500):

```
dpmoInScope < dpmoLedger                                   # the boundary actually bites
abs(dpmoLedger - dpmoInScope) > 200                        # ... by more than any tolerance
vitalFewCount == 3 and abs(vitalFewCumulativePct - 80) > 3 # threshold margin (§4.0)
abs(cum_at_k_minus_1 - 80) > 3                             # 69.30% here: 10.7pp of margin
copqTotal < coq_whole_table * 0.8                          # the trap stays a trap
0 < targetDpmo < dpmoInScope
ci_halfwidth(defectiveUnits, unitsInspected) * 8 < mandated_absolute_reduction   # DP-2 side
```
The last one holds with a factor of 9 at these numbers (half-width 0.001405 vs mandated
absolute reduction 0.01251), so DP-2 fires on `commit_target` under any reseeding.

### 5.4 The decision point carried by this stage

```yaml
decision_points:
  - point_id: define_baseline_adequacy
    phase: define
    rule: "The 95% interval half-width on the baseline return rate (0.00140) is an order of magnitude smaller than the mandated absolute reduction (0.01251) ⇒ the baseline supports committing to a numeric target directly; no further uncertainty quantification is required before goal setting."
    source: "Montgomery ISQC 6e §4.3 (interval estimate of a proportion); Pyzdek & Keller, Six Sigma Handbook 3e ch.5 (goal stated against a quantified baseline)"
    correct_branch: commit_target
    acceptable_branches: [quantify_before_target]
    branch_evidence:
      commit_target:          [define.improvement_target]
      quantify_before_target: [basic.one_proportion, power.two_proportions]
```

`quantify_before_target` is listed as **acceptable**, not incorrect: with n = 48 210 an agent
that computes the interval anyway has done nothing wrong — it has been conservative. The
point exists to catch the agent that commits to a target on a baseline too thin to support
one, which is the *other* case (n ≤ 60), where `commit_target` becomes the incorrect branch
and `acceptable_branches` is empty. One decision point, two case-side polarities.

Scoping is **not** a decision point here, per DP-3: it is graded by
`dpmoLedger` vs `dpmoInScope`.

Order constraints attached:
```yaml
- before: define.baseline_defect_metrics
  after:  define.improvement_target
  source: "Pyzdek & Keller, Six Sigma Handbook 3e ch.5"
```

### 5.5 What a correct agent trajectory looks like

Steward routing is pure substring matching on lowercase topics, so the agent must ask by topic.

| turn | agent action | steward | agent computation |
|---|---|---|---|
| 1 | "Send me the returns ledger for the baseline period." | `data` → `D_Charter` | — |
| 2 | reads `scopeBoundary` = `["in_scope"]` and the per-category `ownership`; computes both baselines | — | `define.baseline_defect_metrics` → `dpu 0.032027`, `dpmoLedger 2668.88`, `dpmoInScope 2195.26`, `ppmDefective 25015.6`, `firstPassYield 0.974984`, `zLongTerm 2.8487`, `sigmaLevel 4.3487` |
| 3 | ranks the failure classes against the declared 80% threshold | — | `quality.pareto` → `topCategoryPct 42.746`, `vitalFewCount 3`, `vitalFewCumulativePct 87.047` |
| 4 | reads `mandate` and applies it to the declared basis | — | `define.improvement_target` → `targetDpmo 1097.63`, `targetSigmaLevel 4.5625`, `requiredReductionPct 50.0` |
| 5 | "Send me the costed breakdown of the returns." | `data` → `D_Cost` | — |
| 6 | sums **only** the categories in `copqScope` | — | `define.copq` → `copqTotal 60651.0`, `copqPerUnit 1.25806`, `copqAnnualized 60651.0` |
| 7+ | proceeds into Measure with the baseline fixed | — | — |

Trace fragment the adapter emits:

```json
{"step_id": 2, "method_id": "define.baseline_defect_metrics", "status": "success",
 "outputs": {"dpu": 0.0320266, "dpo": 0.00266888, "dpmoLedger": 2668.8792,
             "dpmoInScope": 2195.2569, "ppmDefective": 25015.557,
             "firstPassYield": 0.9749844, "zLongTerm": 2.848650, "sigmaLevel": 4.348650}}
```

and one explicit route decision (optional — `branch_evidence` covers a system that omits it):

```json
{"point": "define_baseline_adequacy", "chosen_branch": "commit_target",
 "observed": {"ci_halfwidth": 0.001405, "mandated_absolute_reduction": 0.012508}}
```

Report prose that satisfies HN (one within-tolerance number on each cue line):

> In-boundary baseline over 2025-07-01..2026-06-30: **2195.3 DPMO** (1 270 in-boundary defects
> across 48 210 units × 12 opportunities), a **sigma level of 4.35**. Including the
> supplier-owned firmware class the ledger reads 2 668.9 DPMO; that class sits outside the
> corrective-action boundary and is excluded from the project baseline and target.
> Three failure classes account for **87.0%** of all returns. The OEM's 50% commitment maps to
> a target of **1097.6 DPMO** (sigma level 4.56). COPQ for the period is **60,651 CU**,
> 1.258 CU per unit produced.

**Scoring outcome for this agent, Define portion:** MS recall 4/4; NF 15/15 passed; PQ 1
decision point correct + 1 order constraint satisfied; HN 0 fabrications, 0 misreports.

**Scoring outcome for an agent that skips Define** (today: no loss at all): MS recall loses 4
required methods; all 15 Define truths become `not_computed` (which correctly stays out of the
NF denominator — the omission is charged once, to MS); the decision point is `unknown` and
stays in the PQ denominator. Since TGS is the harmonic mean of MS recall, NF ratio and PQ,
a skipped Define now costs real headline score for the first time.

**Scoring outcome for an agent that ignores the boundary:** MS recall unaffected; NF fails
`dpmoInScope`, `zLongTerm`, `sigmaLevel`, `targetDpmo`, `targetSigmaLevel` — five hard truths
from one framing error, which is the error-propagation property §2a #16–18 was chosen for.

---

## 6. Adversarial review of this proposal

Things a reviewer will attack, answered rather than hidden.

1. **"This is arithmetic, not statistics."** Correct, and stated: items 1–6 and 13–18 are
   deterministic arithmetic over records. Their discriminative power comes from *framing*
   (which records, which boundary, which convention), not from computational difficulty. If
   the paper claims Define measures statistical skill, that claim is false. It measures
   whether an agent quantifies a baseline against a declared boundary before committing to a
   goal — which is what Define *is*.
2. **"Field-name discipline is now load-bearing."** `dpmoLedger` and `dpmoInScope` are the same
   shape and differ only by scope; a system reporting one number under `dpmo` matches neither
   and is scored `failed`. That is intended (it did not answer the scoping question) but it is
   closer to scoring naming than any existing truth. Mitigation: publish the canonical field
   names (they are already the contract), and never add cross-synonyms between the two.
3. **"Task count and baselines change."** `builder._t2_tasks` emits a phase task for every
   phase that carries methods, so every retrofitted case gains a `T2-define` task, and T1
   cases gain one task per Define stage. The 372-task figure and every stored baseline become
   stale. This is unavoidable and must be budgeted: a Define retrofit means a full re-run.
4. **"How many cases can carry this?"** Only cases whose underlying material contains a
   defect ledger with categories, units and an opportunity count. From the corpus census,
   the attribute/count-rate cases are the natural hosts; the purely continuous cases
   (`capability.normal` baselines) would need a *different* Define baseline — Cpk-based — that
   overlaps Measure's `capability.normal` and would fall foul of V10. Honest recommendation:
   **do not force Define onto every case.** Retrofit the ledger-bearing cases, author 2–3
   Define-native cases, and report Define coverage explicitly in the paper rather than
   implying the whole cycle is graded on every task.
5. **"PQ `unknown` inflation."** Every Define decision point added to a case where the branches
   are not evidence-observable lowers PQ for all systems that do not emit `route_decisions`,
   which is a property of the adapter, not the agent. This is why DP-3 and DP-4 are refused
   above. Hold the line: *no Define decision point without evidence-observable branches.*
6. **"Is `meta.data_profiling` now redundant in Define?"** No — keep it, but stop counting it
   as Define coverage. It is a diagnostic (`ms.ALWAYS_RELEVANT`) with no canonical outputs and
   cannot carry a truth.
7. **"Dirty variants."** `perturb._PROTECTED_NORMALIZED` protects `lsl/usl/target/alpha` from
   nulling and stringification. It must be extended with
   `opportunitiesperunit`, `sigmashift`, `vitalfewthresholdpct`, `copqscope`, `scopeboundary`
   and `mandate` — every one of these is a *declared convention*, and a dirty variant that
   nulls one turns a verifiable truth into an unanswerable question. Without this change,
   dirty Define variants are silently broken.
8. **"Is `ppmDefective` ever confusable with `dpmoLedger`?"** They differ by ~10× here and by
   a factor of `O` in general. Keep `O ≥ 4` in every Define case so no tolerance can bridge them.

---

## 7. Implementation checklist (for the follow-up work, not done here)

1. `taxonomy.yaml`: add family `define` + 4 methods; extend `quality.pareto` outputs. (§3)
2. `truth/verifiers.py`: 4 new verifiers + `pareto` extension + `REFERENCE_IMPLS` entries. (§4)
3. `core/validation.py`: add **V10** (per-case method/stage truth uniqueness). (§3.3)
4. `tasks/perturb.py`: extend `_PROTECTED_NORMALIZED`. (§6.7)
5. Author `adb_c24` (§5) as the reference Define case; run
   `python3 -m dmaic_bench validate adb_c24` and the 500-seed invariant sweep.
6. Retrofit `D_` stages into the ledger-bearing existing cases; V10 will reject any that
   collides with an existing Pareto/binomial stage — resolve by moving, not by weakening V10.
7. Rebuild the harbor dataset; the task count and all baselines change (§6.3).
8. Paper: report Define coverage per case explicitly; report any human axis separately (§2c).

---

## Appendix A — quantities considered and rejected

| Candidate | Why rejected |
|---|---|
| `Z_shift` (long-term vs short-term Z difference) | Requires both a long-term ledger and a short-term subgrouped study in one block (violates A1), and the 1.5 shift is assumed in most cases anyway — the "measurement" would return the assumption. |
| RTY via `e^(−DPU)` | A different quantity from the exact yield product; admitting both under one field name is the convention trap this document exists to avoid. |
| "Charter completeness score" from section-presence regex | Measures template filling (§2c). |
| Takt time / capacity baseline | Real Define work, but no case in the corpus carries the cycle-time records to compute it. Revisit if such a case is authored. |
| Cpk as a Define baseline for continuous cases | Collides with Measure's `capability.normal` under V10 and would need `stability_confirmed`, which Define by definition has not established. |
| VOC→CTQ as a matching task against a closed CTQ list | Converts an open translation into multiple choice; the task is no longer the Define work it claims to measure. |

## Appendix B — worked numbers, reproducible

```python
from scipy import stats
U, O, shift = 48210, 12, 1.5
cats = [("seal_leak",660,"in_scope"), ("connector_fit",410,"in_scope"),
        ("firmware_timeout",274,"supplier_owned"), ("cosmetic_scratch",120,"in_scope"),
        ("label_misprint",80,"in_scope")]
D    = sum(c for _,c,_ in cats)                      # 1544
D_in = sum(c for _,c,o in cats if o == "in_scope")   # 1270
dpu  = D/U                                           # 0.032026550508
dpmo_ledger  = 1e6*D/(U*O)                           # 2668.879209016
dpmo_inscope = 1e6*D_in/(U*O)                        # 2195.256862338
ppm_def = 1e6*1206/U                                 # 25015.556938394
fpy     = 1 - 1206/U                                 # 0.974984443062
z       = stats.norm.ppf(1 - dpmo_inscope/1e6)       # 2.848650100982
sigma   = z + shift                                  # 4.348650100982
target  = dpmo_inscope * 0.5                         # 1097.628431169
tsigma  = stats.norm.ppf(1 - target/1e6) + shift     # 4.562460172805
# pareto over the full ledger, threshold 80
#   k=1 42.746114%  k=2 69.300518%  k=3 87.046632%   -> vitalFewCount 3
copq = 612*18.50 + 156*42.00 + 388*96.00 + 388*14.25 # 60651.0
coq_whole_table = copq + 48210*0.35 + 12000.0        # 89524.5  (the trap)
ci = stats.binomtest(1206, U).proportion_ci(method="exact")   # half-width 0.001404576
```

## Appendix C — the Control gap (out of scope, noted)

Control already carries numeric truths (`control_chart.p`, `control_chart.c`,
`control_chart.imr`, `capability.binomial`) and has **0 decision points**. Unlike Define, this
needs no new taxonomy and no new verifiers: the control-chart family choice *is* an
evidence-observable branch (attribute proportion with varying subgroup size ⇒ `control_chart.p`
or `laney_p` when overdispersed; counts ⇒ `c`/`u`; continuous individuals ⇒ `imr`), with
Montgomery *ISQC* 6e ch. 7 and Laney (2002) as sources, and the overdispersion test is
computable from data the cases already carry. Two or three decision points per control-bearing
case would close that gap at a fraction of this document's cost, and should probably be done
first.
