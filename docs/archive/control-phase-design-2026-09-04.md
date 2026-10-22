# Making the CONTROL phase automatically gradeable

**Status:** design specification. Nothing in the benchmark is modified by this document.
**Date:** 2026-09-04
**Scope:** the CONTROL phase only. DEFINE is being designed separately; this document
consumes a Define artefact (`project_target`) but does not specify how Define produces it,
and defines a fallback so Control is not blocked on Define landing.

---

## 0. Measured status quo (re-measured against the package, not quoted)

Counted directly over `registry.discover()` (23 cases, generator seed 1):

| phase | stages | truths | decision points |
|---|---|---|---|
| define  | 1  | 0  | 0 |
| measure | 48 | 27 | 26 |
| analyze | 61 | 43 | 7 |
| improve | 25 | 10 | 6 |
| **control** | **5** | **3** | **0** |

(The review's "24 stages / 18 truths / 372 tasks" counts the same thing after tier × seed ×
variant expansion in `tasks/builder.py`. Both numbers are consistent; the case-level numbers
are the ones an author edits.)

> **Public-release note.** This census — and every per-case reference in this document — is
> over the **full development corpus**: 23 cases at the time of counting, 24 once `adb_c24`
> was added. This repository publishes 15 of them and holds out the nine expert-derived
> cases (`adb_c03 c05 c07 c08 c10 c15 c16 c19 c20`). Re-running the census here is
> possible and will give smaller numbers. See [`HELD_OUT.md`](../HELD_OUT.md).

The five control stages are: `adb_c12/P_BinomialCap` (capability.binomial),
`adb_c17/AC_C` (control_chart.c), `adb_c05/C_PChart` (control_chart.p),
`adb_c08/C_AppearancePPM` (control_chart.imr), `adb_c20/C_DailyPChart` (control_chart.p).
Of these, `adb_c12` and `adb_c17` are in the public split; `adb_c05`, `adb_c08` and
`adb_c20` are held out, so only two of the five are inspectable from this repository.

Two further facts found while reading the machinery, both of which this design must fix:

1. **No control chart has a reference implementation.** `truth.verifiers.REFERENCE_IMPLS`
   contains 26 entries and not one of the 11 `control_chart.*` methods. `validation.py`
   `_check_truth_verification` does `fn = REFERENCE_IMPLS.get(t.method_id); if fn is None:
   continue` — so every control-chart truth in the corpus passes V7 **vacuously**. The
   `adb_c17` generator says so in its own docstring ("None of these four methods has a
   reference implementation… every truth is self-derived in this generator"). A self-derived
   truth is exactly what V7 exists to forbid; today it is admitted by silence.
2. **`capability.normal.cpk` is also vacuously verified.** `verifiers.capability_normal`
   returns only `{"pp", "ppk"}` — both computed from the *overall* standard deviation
   (`np.std(ddof=1)`). `_suffix_lookup(ref, "cpk")` returns `None`, so the check is skipped.
   `adb_c03` (a held-out case) carries a hard-ish `capability.normal.cpk = 1.46` truth that no
   independent implementation in the development tree has ever reproduced. Control-phase capability confirmation
   makes this the load-bearing number, so the verifier must learn within-subgroup sigma.

**Design premise.** Control is not a numbers-only phase. Choosing the sustaining mechanism is
a data-conditioned routing decision with a handbook-normative answer — the exact object this
benchmark claims to measure. It should be the *densest* decision-point phase, not the emptiest.

**Target after this design:** control stages 5 → ~30, control truths 3 → ~90,
control decision points 0 → ~34 (≥ 1 chart-selection point per case with a control phase,
plus a closure gate, plus a small-shift gate where the data support it).

---

## 1. Control chart selection as a decision point (the headline)

### 1.1 The decision tree

The tree is evaluated on the **improved process's monitoring data** — the data the control
plan will actually be run against, not the baseline. Every branch condition is a fact about
that payload, and every one of them is recomputable by `truth/verifiers.py`.

```
                      ┌────────────────────────────────────────────┐
                      │ What is one plotted observation?           │
                      └────────────────────────────────────────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
  MEASUREMENT on a                DEFECTIVE UNITS                  DEFECTS
  continuous scale             (each unit pass/fail;          (occurrences; a unit
  (y_type=continuous)           binomial support)              can carry several;
        │                       (attribute_proportion)          Poisson support)
        │                               │                    (attribute_count_rate)
        │                               │                               │
        ▼                               ▼                               ▼
 ┌──────────────┐              ┌──────────────────┐          ┌──────────────────┐
 │ subgroup n?  │              │ overdispersed?   │          │ overdispersed?   │
 └──────────────┘              │ (D1 below)       │          │ (D1 below)       │
   │      │      │             └──────────────────┘          └──────────────────┘
 n=1   2≤n≤8   n≥9               │            │                │            │
   │      │      │              YES          NO               YES          NO
   ▼      ▼      ▼               │            │                │            │
 I-MR  Xbar-R  Xbar-S            ▼            ▼                ▼            ▼
   │                          laney_p    ┌─────────┐        laney_u   ┌──────────┐
   │                                     │ n const?│                  │ area/    │
   │                                     └─────────┘                  │ exposure │
   │                                       │     │                    │ const?   │
   │                                      YES   NO                    └──────────┘
   │                                       │     │                      │      │
   │                                       ▼     ▼                     YES    NO
   │                                      np     p                      │      │
   │                                                                    ▼      ▼
   │                                                                    c      u
   │
   └── OVERLAY (does not replace the Shewhart chart):
       if the control plan declares a shift-to-detect δ ≤ 1.5σ  ⇒ add EWMA or CUSUM
       (D2 below). Shewhart alone is the wrong answer; either memory chart is right.
```

### 1.2 Branch conditions, stated exactly

Each row is a *machine-checkable* predicate over the stage payload. `k` = number of
subgroups/periods, `n_i` = subgroup size of period *i*.

| # | Branch | Condition (evaluated on the monitoring payload) | Basis |
|---|---|---|---|
| B1 | `imr` | `y_type=continuous` and every `n_i == 1` (one measurement per rational subgroup) | Montgomery ISQC 6e §6.4; AIAG SPC-2 Ch. II Sec. C |
| B2 | `xbar_r` | continuous, all `n_i` equal, `2 ≤ n ≤ 8` | AIAG SPC-2 Ch. II Sec. C |
| B3 | `xbar_s` | continuous, `n ≥ 9`, **or** `n_i` not constant | AIAG SPC-2 Ch. II Sec. C |
| B4 | `np` | defectives, all `n_i` equal, not overdispersed | Montgomery ISQC 6e §7.2.2 |
| B5 | `p` | defectives, `n_i` varies, not overdispersed | Montgomery ISQC 6e §7.2.1 |
| B6 | `laney_p` | defectives, **overdispersion test D1 rejects** | Laney (2002) *Quality Engineering* 14(4) 531–537 |
| B7 | `c` | defects, inspection opportunity (`area_i`) constant, not overdispersed | Montgomery ISQC 6e §7.3.1 |
| B8 | `u` | defects, `area_i` varies, not overdispersed | Montgomery ISQC 6e §7.3.2 |
| B9 | `laney_u` | defects, **overdispersion test D1 rejects** | Laney (2002) |
| B10 | `memory_chart` (EWMA **or** CUSUM), *in addition to* the Shewhart chart | continuous and the control plan declares `shiftToDetectSigma δ ≤ 1.5` | Montgomery ISQC 6e §9.1.1 / §9.2 |

#### The n = 9…12 convention conflict — named and neutralised

AIAG SPC-2 (2nd ed., Ch. II Sec. C) switches from R to s at **n ≥ 9**. Montgomery ISQC 6e
§6.3.1 says the range loses efficiency "for n > 10, say n ≥ 12". Both are defensible and a
benchmark must not silently pick one and grade agents against it.

> **We adopt AIAG SPC-2: R for 2 ≤ n ≤ 8, s for n ≥ 9.**
> **And we forbid generators from ever landing in the contested band.** Generator invariant
> (asserted, redraw-guarded, in the case's `_assert_invariants`):
> `n == 1` or `2 ≤ n ≤ 5` or `n ≥ 15`. The band {6,7,8} is allowed but discouraged;
> **{9,10,11,12} is an onboarding ERROR.** No task is ever decided by the disputed edge, so
> an agent holding the Montgomery convention is never punished for it.

This is the general pattern used throughout this spec: *name the convention, then design the
data so the convention's disputed region is unreachable.*

#### D1 — the overdispersion test (decides Laney p′ / u′)

Two statistics, both required, both recomputable:

1. **Pearson dispersion test** (the formal, citable decision).
   Binomial: `X² = Σ (x_i − n_i p̄)² / (n_i p̄ (1 − p̄))`, `p̄ = Σx_i / Σn_i`.
   Poisson: `X² = Σ (c_i − ā·area_i)² / (ā·area_i)`, `ā = Σc_i / Σarea_i`.
   Under H0 (no extra-binomial / extra-Poisson variation) `X² ~ χ²_{k−1}`.
   `φ̂ = X²/(k−1)`; reject at `p < 0.05`.
   Basis: McCullagh & Nelder, *Generalized Linear Models* 2e §4.5.2 (Pearson X² as the
   dispersion estimator); Montgomery ISQC 6e §7.3.3 discusses the same statistic for counts.
2. **Laney σ_Z** (the magnitude, and the thing Minitab prints).
   `z_i = (p̂_i − p̄)/√(p̄(1−p̄)/n_i)`; `σ_Z = MR̄(z)/1.128`. Already implemented in the
   `adb_c17` generator with this exact convention.

> **Decision rule (the one we adopt):** route to Laney iff `p(X²) < 0.05` **and** `σ_Z ≥ 1.2`.
> Rationale for the conjunction: with k = 30 and n_i ≈ 3000, the χ² test rejects on
> practically irrelevant dispersion; σ_Z is the effect size that says the limits are actually
> wrong. Requiring both is stricter than either alone and cannot flag a chart that a
> practitioner would leave as-is.
>
> **Generator determinacy band (onboarding ERROR if violated):** a case must generate either
> *clearly overdispersed* (`p(X²) < 0.001` **and** `σ_Z > 1.8`) or *clearly not*
> (`p(X²) > 0.20` **and** `σ_Z < 1.15`). The interval between is unreachable.
> `adb_c17` already redraw-guards on `σ_Z > 1.8`; this generalises that guard and adds the
> dispersion-test half.

Worked check on `adb_c17`-shaped data (30 days, `n_i ∈ [1800,3200]`, real day effect):
`p̄ = 0.060237`, `X² = 325.05` on 29 df, `φ̂ = 11.21`, `p = 8.6e-52`, `σ_Z = 3.573`.
Determinate by a wide margin.

#### D2 — the small-shift gate (decides EWMA/CUSUM)

The trigger must live in the *data or the declared plan*, never only in prose. Both halves
are required:

1. **Declared requirement.** The stage payload carries
   `"shiftToDetectSigma": <float>` — a legitimate control-plan parameter set in Improve /
   Define ("we must catch a drift of 1σ within 10 subgroups"). Route to a memory chart when
   `shiftToDetectSigma ≤ 1.5`.
2. **Data invariant proving the requirement is real** (asserted by the generator, and
   re-checkable by the verifier): on the monitoring window the Shewhart chart's Test-1 count
   is **0** while CUSUM(k=0.5, h=4) and EWMA(λ=0.2, L=3) both signal. If the Shewhart chart
   would have caught it anyway, the decision point is not discriminating and must not be
   authored.

Basis: Montgomery ISQC 6e §9.1.1 — "the Shewhart control chart is relatively insensitive to
small process shifts, say on the order of about 1.5σ or less"; §9.1.3 (CUSUM design) and
§9.2.3 (EWMA design).

> **EWMA and CUSUM are not distinguishable on ARL grounds and must not be forced apart.**
> Author the point as `correct_branch: ewma`, `acceptable_branches: [cusum]`, with
> `branch_evidence` for both. The wrong branch is *Shewhart only*.

### 1.3 How the point is authored (exact `case.yaml` shape)

```yaml
decision_points:
  - point_id: control_chart_route
    phase: control
    rule: >-
      The sustaining chart is fixed by the monitoring data's own shape: one measurement per
      rational subgroup, or a subgroup of 15 parts, or pass/fail units, or defect counts —
      each admits exactly one Shewhart chart family.
    source: "AIAG SPC-2 2e Ch. II Sec. C (control chart selection); Montgomery ISQC 6e Ch. 6-7"
    correct_branch: xbar_s
    acceptable_branches: []
    branch_evidence:
      xbar_s: [control_chart.xbar_s]
      xbar_r: [control_chart.xbar_r]     # wrong branch — see the authoring rule below
      imr:    [control_chart.imr]
```

> **Authoring rule (learned the hard way in `adb_c17`, keep it).** `pq._judge_point` marks a
> point *incorrect* if **any** walked branch is outside the acceptable set — even when the
> correct branch was also walked. So a wrong branch may only carry `branch_evidence` when its
> method is **not required by any other stage of the same case**. In the worked case below,
> `control_chart.imr` appears only in the small-shift stage, so listing it under the wrong
> branch of the *subgroup* routing point would misfire; the example therefore lists only the
> branches that are genuinely mutually exclusive within that case. When in doubt, list the
> correct branch only and let a wrong choice score `unknown` (which stays in the PQ
> denominator anyway — silence about a mandatory checkpoint is not process quality).

Emitting an explicit `route_decisions` entry always beats evidence inference:

```json
{"point": "control_chart_route", "chosen_branch": "xbar_s",
 "observed": {"subgroupSize": 15, "constantSubgroupSize": true, "dataType": "continuous"}}
```

---

## 2. Recomputed control limits on the improved process

### 2.1 Phase I / Phase II split — mandatory

Every control stage payload is split into two windows, and the split is what makes the
flagged-point truth non-circular:

* `baselineWindow` — the improved-process data the limits are **estimated from** (Phase I).
* `monitoringWindow` — later data the limits are **applied to** (Phase II). Never used for
  estimation.

Basis: Montgomery ISQC 6e §4.5 / §6.2.3 (Phase I vs Phase II use of control charts).
Without this split, "flagged points" is estimated and tested on the same data and the
expected count is a property of the estimator, not of the process.

### 2.2 Constants

Sigma is always the **within-subgroup (short-term)** estimate. Never the overall SD.

| Chart | Center line | Limits | σ̂ (within) |
|---|---|---|---|
| I (individuals) | `x̄` | `x̄ ± 3·σ̂`, `σ̂ = MR̄/d2(2)` (= MR̄/1.128, equivalently `x̄ ± 2.660·MR̄`) | `MR̄/1.128` |
| MR | `MR̄` | `UCL = D4(2)·MR̄ = 3.267·MR̄`, `LCL = D3(2)·MR̄ = 0` | — |
| Xbar-R | `x̄̄` | `x̄̄ ± A2(n)·R̄` | `R̄/d2(n)` |
| R | `R̄` | `D4(n)·R̄`, `D3(n)·R̄` | — |
| Xbar-S | `x̄̄` | `x̄̄ ± A3(n)·s̄` | `s̄/c4(n)` |
| S | `s̄` | `B4(n)·s̄`, `B3(n)·s̄` | — |
| p | `p̄ = Σx_i/Σn_i` | `p̄ ± 3√(p̄(1−p̄)/n_i)` — **per-point limits when n_i varies** | — |
| np | `n·p̄` | `n p̄ ± 3√(n p̄(1−p̄))` | — |
| c | `c̄` | `c̄ ± 3√c̄` | — |
| u | `ū = Σc_i/Σarea_i` | `ū ± 3√(ū/area_i)` — per-point | — |
| Laney p′ | `p̄` | `p̄ ± 3·σ_Z·√(p̄(1−p̄)/n_i)` | `σ_Z = MR̄(z)/1.128` |
| Laney u′ | `ū` | `ū ± 3·σ_Z·√(ū/area_i)` | same, with `z_i=(u_i−ū)/√(ū/area_i)` |

Frozen constant table (AIAG SPC-2 2e Appendix E; identical to ASTM E2587-16 Table 3):

| n | d2 | A2 | D3 | D4 | c4 | A3 | B3 | B4 |
|---|---|---|---|---|---|---|---|---|
| 2 | 1.128 | 1.880 | 0 | 3.267 | 0.7979 | 2.659 | 0 | 3.267 |
| 3 | 1.693 | 1.023 | 0 | 2.574 | 0.8862 | 1.954 | 0 | 2.568 |
| 4 | 2.059 | 0.729 | 0 | 2.282 | 0.9213 | 1.628 | 0 | 2.266 |
| 5 | 2.326 | 0.577 | 0 | 2.114 | 0.9400 | 1.427 | 0 | 2.089 |
| 6 | 2.534 | 0.483 | 0 | 2.004 | 0.9515 | 1.287 | 0.030 | 1.970 |
| 7 | 2.704 | 0.419 | 0.076 | 1.924 | 0.9594 | 1.182 | 0.118 | 1.882 |
| 8 | 2.847 | 0.373 | 0.136 | 1.864 | 0.9650 | 1.099 | 0.185 | 1.815 |
| 15 | 3.472 | 0.223 | 0.347 | 1.653 | 0.98232 | 0.78854 | 0.42820 | 1.57180 |
| 25 | 3.931 | 0.153 | 0.459 | 1.541 | 0.98964 | 0.60627 | 0.56517 | 1.43483 |

**Independence of the table is a real problem and it is solved as follows.** A table copied
from the same handbook into both generator and verifier is not an independent
re-implementation. So:

* `c4`, `A3`, `B3`, `B4` are **computed in closed form** by the verifier and never tabled:
  `c4(n) = √(2/(n−1))·Γ(n/2)/Γ((n−1)/2)`;
  `A3 = 3/(c4√n)`; `B3 = max(0, 1 − 3√(1−c4²)/c4)`; `B4 = 1 + 3√(1−c4²)/c4`.
  (Checked: `c4(15) = 0.9823164`, `A3(15) = 0.7885406`, `B3(15) = 0.4281999`,
  `B4(15) = 1.5718001` — matching the table above to 5 dp.)
* `d2` is **computed by numerical integration** in the verifier:
  `d2(n) = ∫_{−∞}^{∞} [1 − (1−Φ(x))ⁿ − Φ(x)ⁿ] dx` (Tippett 1925), via
  `scipy.integrate.quad` over [−8, 8]. Cross-checked against the table:
  n=2…10 → 1.1284/1.6926/2.0588/2.3259/2.5344/2.7044/2.8472/2.9700/3.0775 vs
  1.128/1.693/2.059/2.326/2.534/2.704/2.847/2.970/3.078. Max deviation 5e-4, i.e. table
  rounding.
* `A2 = 3/(d2√n)` follows from the integrated `d2` — also closed form, not tabled.
* `D3`/`D4 = 1 ∓ 3·d3/d2` require `d3` (the SD of the relative range), which has no
  one-dimensional closed form. These **stay tabled**, and the verifier declares so in its
  docstring. (They can still be *sanity*-checked independently: 4e6-replicate Monte Carlo of
  the relative range gives d3(2)=0.8527, d3(5)=0.8644, d3(15)=0.7561, d3(25)=0.7089, hence
  D4 = 3.2669 / 2.1149 / 1.6534 / 1.5411 against the tabled 3.267 / 2.114 / 1.653 / 1.541 —
  agreement to Monte Carlo error, which is a *check*, not an independent implementation.)

Consequence, stated plainly: **R-chart and MR-chart limit truths are `soft`**; Xbar-R's
*center line* and σ̂ are hard, its R-chart limits are soft. Xbar-S limits are hard end to end
because every constant on that path is closed form. This is a reason to prefer Xbar-S cases
when authoring — an additional, principled argument for the n ≥ 15 invariant.

### 2.3 Edge cases that must be specified, not discovered

| Situation | Rule | Basis |
|---|---|---|
| Negative LCL on p / np / c / u / Laney | `LCL = max(0, computed)` | AIAG SPC-2 Ch. II ("a negative limit is reported as zero") |
| `UCL > 1` on a p chart | clipped to 1.0 | same |
| MR chart LCL | always 0 (`D3(2)=0`) | table |
| S chart LCL for n ≤ 5 | 0 (`B3 = 0`) | closed form gives exactly 0 |
| k < 2 subgroups | `NotVerifiable` — no MR̄/R̄/s̄ exists | — |
| a subgroup with `n_i = 0` or `area_i = 0` | `NotVerifiable`; generators must not emit them | — |
| all values identical (σ̂ = 0) | `NotVerifiable`; degenerate limits | — |
| `p̄ = 0` or `p̄ = 1` | `NotVerifiable` for Laney (z undefined) | — |
| a defect count exceeding the unit count on a *defectives* chart | onboarding ERROR (payload mislabels defects as defectives) | — |

---

## 3. Improvement verification (before → after)

### 3.1 The conventions, named

| Y type | Method | Convention — **this is the pick** | Basis |
|---|---|---|---|
| continuous, unpaired | `basic.two_sample_t` | **Welch** (`equal_var=False`), **two-sided**, α=0.05 | Welch (1947); Montgomery & Runger 7e §10.2.2. Also: this is already what `verifiers.two_sample_t` does — the benchmark must not carry two t-test conventions. |
| continuous, matched units | `basic.paired_t` | two-sided; **only** when the payload declares `"pairing": "matched"` | Montgomery & Runger 7e §10.4 |
| continuous, non-normal (AD p < 0.05 on either arm) | `nonparametric.mann_whitney` as a declared `alternative` | two-sided, normal approximation with continuity correction (scipy default for large n) | Montgomery ISQC 6e §15.x; Hollander & Wolfe 3e |
| defectives | `basic.two_proportions` | **pooled** SE, **two-sided** | Fleiss, Levin & Paik 3e §2.3 — under H0: p1=p2 the null-consistent SE is the pooled one. Also already what `verifiers.two_proportions` does. |
| defect rates | `basic.two_poisson_rates` (**new**) | **conditional binomial exact test**, two-sided | Przyborowski & Wilenski (1940); Ng, Gu & Tang (2007) survey — the conditional test is the standard "C-test" |

**Competing conventions we explicitly reject, and why:**

* *Two-proportion, unpooled SE.* Minitab's default for the 2-proportion test is
  "estimate the proportions separately". We use pooled anyway, because
  `verifiers.two_proportions` already computes pooled and a benchmark with two conflicting
  two-proportion truths is worse than a benchmark with a stated non-Minitab convention.
  Tolerance guidance below absorbs the difference for reported p-values near α.
* *Student's pooled t.* Rejected: Welch is already in the verifier and is the safer default
  under unequal post-improvement variance (which is the *point* of many improvements).
* *One-sided "we improved" alternative.* Rejected as a default. The benchmark has already
  shipped one truth (`adb_c03` `basic.one_sample_t`, declared p = 0.0351 one-sided vs 0.0703
  two-sided) that its own verifier could not reproduce. Therefore:

> **Tail convention (hard rule).** Improvement verification is **two-sided** unless the
> payload declares otherwise via the key `alternativeHypothesis` (`LESS_THAN` / `GREATER_THAN`
> / `NOT_EQUAL`), which `verifiers._alternative()` already reads and which already **raises**
> on an unrecognised spelling rather than assuming. A one-sided truth without that key in the
> payload is an onboarding ERROR. The truth's `derivation` string must name the tail
> verbatim, e.g. `"scipy.stats.ttest_ind(equal_var=False, alternative='two-sided')"`.

### 3.2 Where the "before" data comes from

Two admissible shapes, and only these:

* **Shape A (self-contained, preferred).** The control stage payload carries both arms:
  `{"before": [...], "after": [...]}` for continuous, or
  `{"events1", "trials1", "events2", "trials2"}` for defectives. Works in T1 single-stage
  probes and T2 control slices, where earlier phases were never run.
* **Shape B (cross-stage).** The payload references the Measure baseline stage by id
  (`"beforeFromStage": "M_Baseline"`). Only admissible in T3 full-journey tasks. The
  onboarding validator must reject Shape B in any case whose control stage can be sliced
  into a T2 task — otherwise the T2 control slice is unsolvable and NF scores a
  `not_computed` the agent could never have avoided.

---

## 4. Capability confirmation and the Define coupling

### 4.1 The numbers

| Field | Formula | Sigma | Class |
|---|---|---|---|
| `cp` | `(USL−LSL)/(6·σ̂_within)` | within | hard |
| `cpk` | `min((USL−μ)/(3σ̂_within), (μ−LSL)/(3σ̂_within))` | within | hard |
| `pp` | `(USL−LSL)/(6·s_overall)` | overall (`ddof=1`) | hard |
| `ppk` | `min((USL−μ)/(3s), (μ−LSL)/(3s))` | overall | hard |
| `cpkMargin` | `cpk − target_cpk` | — | **hard, this is the goal verdict** |

`σ̂_within` comes from the subgroup structure of the *same* stage: `s̄/c4(n)` when subgrouped
(n ≥ 9), `R̄/d2(n)` when 2 ≤ n ≤ 8, `MR̄/d2(2)` for individuals. Basis: AIAG SPC-2 2e Ch. IV
(within vs overall variation); ISO 22514-2:2017 §4 for the same distinction under the
C/P index naming.

One-sided specs: when only one of LSL/USL is present, `cp`/`pp` are undefined and must be
**absent from the truths**, not reported as `None` (NF's `flatten` drops non-numerics anyway,
but an absent truth is the honest encoding). `cpk` becomes the single available Z/3.

**Boolean goal verdicts must never be a truth.** `nf.flatten` keeps
`isinstance(v,(int,float)) and not isinstance(v,bool)` — a reported `goalMet: true` is
**silently dropped**, so a `goalMet` truth would score `failed`/`not_computed` for an agent
that answered correctly. Encode the verdict as the signed real `cpkMargin` (or
`defectRateMargin = target_rate − observed_rate` for attribute projects). The sign is the
verdict, and the number is gradeable.

### 4.2 The cross-phase dependency (Control's pass criterion comes from Define)

Add one optional top-level block to `case.yaml`:

```yaml
project_target:
  metric: cpk                  # cpk | ppk | defect_rate | dpu | dpmo
  direction: at_least          # at_least | at_most
  value: 1.33
  source: charter              # charter | customer_spec | contractual
```

Contract with the Define designer — deliberately minimal so the two designs do not collide:

* Control **consumes** `project_target`; it does not define how Define is graded on setting it.
* The task builder copies the resolved target into every control stage's payload as
  `"targetCpk": 1.33` (or `targetDefectRate`, …), so a T2 control slice is self-contained.
* **Fallback if Define ships nothing:** the target is declared in `project_target` directly by
  the case author, and Control is unaffected. Control never blocks on Define.
* In T3, the target additionally appears in the Define stage's payload. An agent that reads
  it there and carries it to Control gets the coupling for free; an agent that ignores it
  still sees it in the control payload — the coupling is *rewarded*, never *required*, which
  is what keeps the T2 slice fair.

### 4.3 The closure gate

```yaml
  - point_id: control_closure_gate
    phase: control
    rule: >-
      Close the project only when the improvement is statistically established AND the
      confirmed capability meets the chartered target; otherwise the correct action is to
      return to Improve, not to write a control plan.
    source: "Montgomery ISQC 6e §1.4 (DMAIC control phase); AIAG SPC-2 2e Ch. IV"
    correct_branch: close_project
    acceptable_branches: []
    branch_evidence:
      close_project: [capability.normal]
```

Honest limitation, stated rather than papered over: `branch_evidence` is method-based, so it
cannot by itself distinguish "computed Cpk and correctly concluded close" from "computed Cpk
and wrongly concluded extend". The gate is therefore **explicit-first**: an agent that emits
`{"point": "control_closure_gate", "chosen_branch": "close_project",
 "observed": {"cpk": 1.665, "target": 1.33, "improvementP": 3.0e-37}}` is judged on its actual
conclusion; an agent that stays silent scores `unknown`, which `pq.py` already keeps in the
denominator. That is the correct incentive and needs **no code change**.

*Optional, clearly-flagged enhancement (not required by this design):* add
`observed_predicate` to `DecisionPoint` — a tiny safe expression (`"cpkMargin > 0"`) evaluated
against the trace's merged numeric outputs, used only when neither an explicit decision nor
branch evidence discriminates. It would let the closure gate be inferred. Ship the gate
without it first; the `unknown` verdict is not a bug.

**Generator determinacy:** `|cpkMargin| ≥ 0.10` and the improvement p-value must be on one
clear side (`p < 0.01` or `p > 0.20`). No case may sit on the fence.

---

## 5. Response plan / out-of-control detection

### 5.1 Which rule set — and why the choice is not cosmetic

Measured on the worked example's 20-subgroup monitoring window (§9), against the same frozen
limits:

* **Test 1 alone (points beyond 3σ): 1 flagged point** — subgroup 12.
* **Western Electric (4 rules): 9 flagged points** — subgroups 11–19.
* **Nelson tests 1–8: 11 flagged points** — subgroups 9–19.

A truth of "flaggedCount = 9" without a named rule set is a truth nobody can reproduce. So:

> **Adopted rule set: Nelson (1984) Tests 1–8**, *Journal of Quality Technology* 16(4),
> 237–239, with the parameters below. It is a single primary source that fully specifies all
> eight tests, and it is the numbering Minitab's "Tests for special causes" uses.
> Western Electric Handbook (1956, pp. 25–28) rules are the competing convention; they are
> Nelson's 1, 5, 6 plus an 8-points-one-side rule (Nelson's Test 2 uses **9** points). We do
> not use them, and we say so in every derivation string.

| Test | Rule | Parameters |
|---|---|---|
| 1 | 1 point beyond 3σ from CL | k=3 |
| 2 | 9 consecutive points on the same side of CL | k=9 (**not** WE's 8) |
| 3 | 6 consecutive points all increasing or all decreasing | k=6 |
| 4 | 14 consecutive points alternating up/down | k=14 (13 sign alternations) |
| 5 | 2 of 3 consecutive points beyond 2σ, same side | k=2 of 3 |
| 6 | 4 of 5 consecutive points beyond 1σ, same side | k=4 of 5 |
| 7 | 15 consecutive points within 1σ of CL (either side) | k=15 |
| 8 | 8 consecutive points beyond 1σ of CL (either side) | k=8 |

Counting convention (must be stated, because it changes the number): a "flagged point" is a
**point index**, and every point in a triggering window is flagged, deduplicated across
tests — i.e. the reported count is `|⋃_tests flagged_indices|`. The alternative convention
(count only the last point of each triggering window) gives different numbers; we do not use
it. Zones are computed from the **Phase I** σ̂ and CL, applied to the **Phase II** window.

### 5.2 The two-truth structure that makes this safe

| Truth field | Definition | Class | tol |
|---|---|---|---|
| `flaggedCountTest1` | points beyond 3σ only | **hard** | 0 |
| `flaggedCountNelson` | `|⋃ Tests 1–8|` | **soft** | 1 |
| `firstSignalIndex` | 1-based index of the earliest flagged point (0 if none) | hard | 0 |

Rationale: Test 1 is convention-free — no handbook disputes "beyond 3σ". Making it the hard
truth means an agent that runs only Test 1 (Minitab's out-of-the-box default in several
versions) is not punished, while an agent that runs the full Nelson set gets soft credit for
matching. `firstSignalIndex` is the number a response plan actually turns on ("when do we
react") and it is stable across EWMA/CUSUM parameterisations far more than the count is:
on the worked small-shift stage, CUSUM flags 21 points and EWMA flags 5, but **both first
signal at point 20**.

### 5.3 The response plan itself

An OOC *reaction* ("stop the line, quarantine, escalate to the process owner") is a document,
not a number. See §6. The gradeable residue is exactly: which chart, what limits, how many
signals, and when the first one fires.

---

## 6. What is NOT automatically gradeable — say so and exclude it

| Control-phase deliverable | Verdict |
|---|---|
| Control plan document (AIAG APQP control plan: characteristics, methods, reaction plan, owners) | **Not gradeable. Exclude.** |
| Standard work / SOP updates, work-instruction revisions | **Not gradeable. Exclude.** |
| Operator training and certification records | **Not gradeable. Exclude.** |
| Handover to the process owner, sign-off, project closure paperwork | **Not gradeable. Exclude.** |
| Mistake-proofing (poka-yoke) design | **Not gradeable. Exclude.** |
| Financial benefit validation / hard-savings sign-off by finance | **Not gradeable. Exclude.** |
| Audit schedule, monitoring frequency, sampling plan *rationale* | **Not gradeable** as prose. The *sampling plan numbers* (n, frequency) are gradeable only if a formal criterion (ARL, OC curve, `power.*`) is specified — treat as an Improve-style power question, not a Control artefact. |

**Do not invent a numeric proxy.** The tempting ones — "does the report contain ≥ 5 control
plan rows", "does it mention an owner", "reaction-plan keyword count" — are all
length/keyword proxies. The bench has already been burned by exactly this class of metric:
the fabrication rate is non-monotone under padding, and a report containing *zero numbers*
scores TGS 1.000. A keyword-counting Control axis would be gamed the same way and would
carry the same reviewer risk.

**Recommendation:**

1. **Exclude these from the scored corpus.** No stage, no truth, no decision point.
2. If the organisational half must be represented at all, add a **separately labelled,
   separately reported, non-TGS axis** — call it `CP` (Control-Plan Completeness) — that is
   (a) rubric-scored by a human or a clearly-declared LLM judge, (b) reported as its own
   column with its own inter-rater agreement, and (c) **multiplied into nothing**. It must
   not enter `tgs.compute`, must not enter `AGGREGATE_METRICS` as a competence axis, and the
   paper must state it is not part of the headline score. A benchmark that says "we measure
   the parts of Control that are objectively checkable, and we say which parts are not" is
   strictly more credible than one that fakes coverage.
3. State the exclusion in the paper's Limitations section in one sentence: *"DMAIC-Bench
   grades the analytical content of the Control phase — chart selection, limit computation,
   improvement confirmation, capability confirmation against the chartered target, and
   out-of-control detection. It does not grade control-plan documentation, training or
   handover, which have no objective automatic criterion."*

---

## 7. Taxonomy additions (`taxonomy.yaml`, exact schema)

### 7.1 Enriched `canonical_outputs` for the 11 existing control-chart methods

Today most control-chart entries expose one or two fields, several of them `soft`, so an
agent that computes a whole chart correctly earns almost nothing. Replacement entries below.

> Historical design note: this proposal originally assumed bilingual method aliases.
> The current release uses canonical English aliases and does not maintain a Chinese
> arm. Preserve the English method-recognition behavior when applying these entries;
> a future Chinese extension needs its own version and validation.

```yaml
  # ---- control charts -------------------------------------------------------------
  - method_id: control_chart.imr
    spec_keys: [solver.controlchart.imr.v1]
    aliases: [i-mr chart, individuals and moving range chart, imr]
    family: control_chart
    applicability: {data_type: continuous, prerequisites: []}
    canonical_outputs:
      - {name: centerLine, tol_class: exact}
      - {name: individualsUCL, tol_class: tight}
      - {name: individualsLCL, tol_class: tight}
      - {name: sigmaWithin, tol_class: tight}
      - {name: movingRangeBar, tol_class: exact}
      - {name: movingRangeUCL, tol_class: tight}
      - {name: flaggedCountTest1, tol_class: exact}
      - {name: firstSignalIndex, tol_class: exact}
      - {name: flaggedCountNelson, tol_class: soft}

  - method_id: control_chart.xbar_r
    spec_keys: [solver.controlchart.xbar-r.v1]
    aliases: [xbar-r chart, x-bar and range chart]
    family: control_chart
    applicability: {data_type: continuous, prerequisites: []}
    canonical_outputs:
      - {name: xBarChartCenterLine, tol_class: exact}
      - {name: rBar, tol_class: exact}
      - {name: sigmaWithin, tol_class: tight}
      - {name: xBarUCL, tol_class: tight}
      - {name: xBarLCL, tol_class: tight}
      - {name: rUCL, tol_class: soft}          # D4 is tabled, not closed form
      - {name: rLCL, tol_class: soft}
      - {name: flaggedXBarCountTest1, tol_class: exact}
      - {name: firstSignalIndex, tol_class: exact}

  - method_id: control_chart.xbar_s
    spec_keys: [solver.controlchart.xbar-s.v1]
    aliases: [xbar-s chart, x-bar and s chart]
    family: control_chart
    applicability: {data_type: continuous, prerequisites: []}
    canonical_outputs:
      - {name: xBarChartCenterLine, tol_class: exact}
      - {name: sBar, tol_class: exact}
      - {name: sigmaWithin, tol_class: tight}
      - {name: xBarUCL, tol_class: tight}
      - {name: xBarLCL, tol_class: tight}
      - {name: sUCL, tol_class: tight}         # B4 closed form -> hard
      - {name: sLCL, tol_class: tight}
      - {name: flaggedXBarCountTest1, tol_class: exact}
      - {name: firstSignalIndex, tol_class: exact}

  - method_id: control_chart.ewma
    spec_keys: [solver.controlchart.ewma.v1]
    aliases: [ewma chart, exponentially weighted moving average]
    family: control_chart
    applicability: {data_type: continuous, prerequisites: []}
    canonical_outputs:
      - {name: lambda, tol_class: exact}
      - {name: sigmaWithin, tol_class: tight}
      - {name: firstSignalIndex, tol_class: exact}
      - {name: lastEwmaValue, tol_class: tight}
      - {name: flaggedCount, tol_class: soft}

  - method_id: control_chart.cusum
    spec_keys: [solver.controlchart.cusum.v1]
    aliases: [cusum chart, cumulative sum chart]
    family: control_chart
    applicability: {data_type: continuous, prerequisites: []}
    canonical_outputs:
      - {name: k, tol_class: exact}
      - {name: h, tol_class: exact}
      - {name: sigmaWithin, tol_class: tight}
      - {name: firstSignalIndex, tol_class: exact}
      - {name: maxCPlus, tol_class: tight}
      - {name: maxCMinus, tol_class: tight}
      - {name: flaggedCount, tol_class: soft}

  - method_id: control_chart.p
    spec_keys: [solver.controlchart.p-chart.v1]
    aliases: [p chart, proportion nonconforming chart]
    family: control_chart
    applicability: {data_type: attribute_proportion, prerequisites: []}
    canonical_outputs:
      - {name: centerLine, tol_class: exact}
      - {name: dispersionRatio, tol_class: tight}    # phi-hat = X^2/(k-1)
      - {name: outOfControlCountTest1, tol_class: exact}
      - {name: firstSignalIndex, tol_class: exact}
      - {name: uclAtMinN, tol_class: tight}
      - {name: uclAtMaxN, tol_class: tight}

  - method_id: control_chart.np
    spec_keys: [solver.controlchart.np-chart.v1]
    aliases: [np chart, number nonconforming chart]
    family: control_chart
    applicability: {data_type: attribute_proportion, prerequisites: []}
    canonical_outputs:
      - {name: centerLine, tol_class: exact}
      - {name: ucl, tol_class: tight}
      - {name: lcl, tol_class: tight}
      - {name: outOfControlCountTest1, tol_class: exact}

  - method_id: control_chart.laney_p
    spec_keys: [solver.controlchart.laney-p-chart.v1]
    aliases: [laney p chart, laney p prime, p′ chart]
    family: control_chart
    applicability: {data_type: attribute_proportion, prerequisites: []}
    canonical_outputs:
      - {name: centerLine, tol_class: exact}
      - {name: sigmaZ, tol_class: tight}             # was soft; it is closed form
      - {name: dispersionRatio, tol_class: tight}
      - {name: outOfControlCountTest1, tol_class: exact}

  - method_id: control_chart.c
    spec_keys: [solver.controlchart.c-chart.v1]
    aliases: [c chart, count of defects chart]
    family: control_chart
    applicability: {data_type: attribute_count_rate, prerequisites: []}
    canonical_outputs:
      - {name: centerLine, tol_class: exact}
      - {name: ucl, tol_class: tight}
      - {name: lcl, tol_class: tight}
      - {name: dispersionRatio, tol_class: tight}
      - {name: outOfControlCountTest1, tol_class: exact}

  - method_id: control_chart.u
    spec_keys: [solver.controlchart.u-chart.v1]
    aliases: [u chart, defects per unit chart]
    family: control_chart
    applicability: {data_type: attribute_count_rate, prerequisites: []}
    canonical_outputs:
      - {name: processMean, tol_class: exact}
      - {name: dispersionRatio, tol_class: tight}
      - {name: outOfControlCountTest1, tol_class: exact}
      - {name: uclAtMinArea, tol_class: tight}
      - {name: uclAtMaxArea, tol_class: tight}

  - method_id: control_chart.laney_u
    spec_keys: [solver.controlchart.laney-u-chart.v1]
    aliases: [laney u chart, laney u prime, u′ chart]
    family: control_chart
    applicability: {data_type: attribute_count_rate, prerequisites: []}
    canonical_outputs:
      - {name: processMean, tol_class: exact}
      - {name: sigmaZ, tol_class: tight}
      - {name: dispersionRatio, tol_class: tight}
      - {name: outOfControlCountTest1, tol_class: exact}
```

Note on `nf._field_matches`: `flaggedCountTest1` vs `flaggedXBarCountTest1` are different
segments and will not cross-match — deliberate, since an Xbar-chart flag count and an
R-chart flag count are different quantities. Add no synonym entries for them.

### 7.2 New methods

```yaml
  - method_id: basic.two_poisson_rates
    spec_keys: []          # fill in if/when the private contestant's engine gains a spec
    aliases: [two-sample poisson rate test, comparison of two rates, poisson rate ratio test]
    family: basic_test
    applicability: {data_type: attribute_count_rate, prerequisites: []}
    canonical_outputs:
      - {name: pValue, tol_class: tight}
      - {name: rateRatio, tol_class: tight}
      - {name: rate1, tol_class: exact}
      - {name: rate2, tol_class: exact}
```

`spec_keys: []` is legal (`taxonomy.load` does `e.get("spec_keys", [])`) and keeps the
taxonomy system-agnostic — the benchmark's vocabulary must not be capped by one contestant's
tool inventory. Until a system-agnostic tool exists, author it with
`alternatives: [basic.one_proportion]` (the conditional test *is* an exact one-proportion
test of `x1 | x1+x2` against `π0 = T1/(T1+T2)`), so MS recall is not unfairly zeroed.

```yaml
  - method_id: capability.confirmation
    # NOT PROPOSED — deliberately. Post-improvement capability is capability.normal /
    # capability.binomial / capability.poisson run on improved data. Adding a
    # phase-specific twin would split the taxonomy on phase rather than on statistics,
    # break MS precision for agents that (correctly) reuse the same method, and give the
    # MS-Misuse judge two data_type rows for one computation.
```

### 7.3 What is deliberately *not* added

No `control.plan_audit`, `control.training_record`, `control.handover` or similar. See §6.
Adding a method_id for a non-computable artefact would make it addressable by
`branch_evidence` and would smuggle the ungradeable back in through the PQ door.

---

## 8. Reference implementations for `truth/verifiers.py`

All follow the existing house style: take the **same payload dict the generator emits**,
raise `NotVerifiable` on an unrecognised shape, return a flat dict of canonical field names,
never import the contestant's code.

### 8.1 Shared helpers

```python
def _d2(n):                      # Tippett (1925) integral, quad over [-8, 8]
def _c4(n):                      # sqrt(2/(n-1)) * Gamma(n/2)/Gamma((n-1)/2)
def _a3(n): return 3.0 / (_c4(n) * sqrt(n))
def _b3(n) / _b4(n):             # closed form from c4
def _a2(n): return 3.0 / (_d2(n) * sqrt(n))
_D3D4_TABLE = {...}              # ASTM E2587-16 Table 3 — the ONLY tabled constants,
                                 # because d3 has no 1-D closed form. Documented in the
                                 # docstring; consumers of D3/D4 emit soft truths.
def _subgroups(payload):         # -> np.ndarray (k, n) or ragged list; NotVerifiable on k<2
def _windows(payload):           # -> (baselineWindow, monitoringWindow); monitoring may be []
def nelson_flags(values, cl, sigma, tests=(1,...,8)) -> dict
    # returns {"flaggedCountTest1": int, "flaggedCountNelson": int,
    #          "firstSignalIndex": int (1-based, 0 = none),
    #          "byTest": {test_no: [1-based indices]}}
def _dispersion(counts, exposures, kind) -> (X2, df, phi_hat, p_value)
def _laney_sigma_z(values, cl, se_i) -> float   # MR-bar of z / 1.128
```

**Helper edge cases.** `_d2`: `n < 2` → `NotVerifiable`. `_c4`: `n < 2` → `NotVerifiable`;
`n > 342` overflows `gamma` → use `scipy.special.gammaln` differences (specify this now, do
not discover it). `nelson_flags`: `sigma <= 0` → `NotVerifiable`; windows shorter than a
test's k simply do not fire that test (never an error). `_dispersion`: any `exposure == 0` or
`p̄ ∈ {0,1}` → `NotVerifiable`.

### 8.2 Chart verifiers

| Function | Payload keys read | Returns | Notes / edge cases |
|---|---|---|---|
| `control_chart_imr` | `values`/`data`/`measurements`, opt. `monitoringWindow`, opt. `target` | centerLine, movingRangeBar, sigmaWithin, individualsUCL/LCL, movingRangeUCL, flaggedCountTest1, firstSignalIndex, flaggedCountNelson | `MR̄` uses n−1 differences. σ̂ = MR̄/1.128. If `target` present, CL = target (Phase II). `k<2` → NotVerifiable |
| `control_chart_xbar_r` | `subgroups` (list of lists) or `values`+`subgroupSize` | xBarChartCenterLine, rBar, sigmaWithin, xBarUCL/LCL, rUCL/LCL, flaggedXBarCountTest1, firstSignalIndex | ragged subgroups → NotVerifiable (R chart needs constant n). `n>8` → NotVerifiable *by design*: refuse to verify a chart the selection rule says is wrong |
| `control_chart_xbar_s` | same | xBarChartCenterLine, sBar, sigmaWithin, xBarUCL/LCL, sUCL/LCL, flaggedXBarCountTest1, firstSignalIndex | ragged n allowed only if the payload declares `pooled: true`; otherwise NotVerifiable. `s_i` uses `ddof=1` |
| `control_chart_p` | `defectCounts`, `sampleSizes` | centerLine, dispersionRatio, uclAtMinN, uclAtMaxN, outOfControlCountTest1, firstSignalIndex | per-point limits; LCL floored at 0, UCL capped at 1 |
| `control_chart_np` | `defectCounts`, `sampleSize` (scalar) | centerLine, ucl, lcl, outOfControlCountTest1 | list-valued `sampleSizes` → NotVerifiable |
| `control_chart_c` | `defectCounts` (opt. `inspectionUnits` all equal) | centerLine, ucl, lcl, dispersionRatio, outOfControlCountTest1 | unequal exposures → NotVerifiable (that is a u chart) |
| `control_chart_u` | `defectCounts`, `inspectionUnits` | processMean, dispersionRatio, uclAtMin/MaxArea, outOfControlCountTest1 | per-point limits; zero area → NotVerifiable |
| `control_chart_laney_p` | `defectCounts`, `sampleSizes` | centerLine, sigmaZ, dispersionRatio, outOfControlCountTest1 | reuses `_laney_sigma_z`; `p̄∈{0,1}` → NotVerifiable |
| `control_chart_laney_u` | `defectCounts`, `inspectionUnits` | processMean, sigmaZ, dispersionRatio, outOfControlCountTest1 | as above |
| `control_chart_ewma` | `values`, opt. `lambda` (default **0.2**), `L` (default **3**), `target`, `sigma` | lambda, sigmaWithin, lastEwmaValue, firstSignalIndex, flaggedCount | **time-varying limits** `μ0 ± Lσ√(λ/(2−λ)·(1−(1−λ)^{2i}))` (Montgomery ISQC 6e Eq. 9.26), *not* the asymptotic form. `z_0 = μ0`. μ0 = `target` if present else baseline mean; σ = `MR̄/1.128` on the baseline window |
| `control_chart_cusum` | `values`, opt. `k` (default **0.5**), `h` (default **4**), `target`, `sigma` | k, h, sigmaWithin, maxCPlus, maxCMinus, firstSignalIndex, flaggedCount | **standardized** tabular CUSUM (Montgomery ISQC 6e §9.1.3): `C⁺_i = max(0, z_i − k + C⁺_{i−1})`, `C⁻_i = max(0, −z_i − k + C⁻_{i−1})`, `C⁺_0 = C⁻_0 = 0`. Signal when either > h. `h=5` is the competing convention — we use 4 and say so |

**Defaults are conventions and therefore must be echoed into the truth's `derivation`
string**, e.g. `"standardized tabular CUSUM, k=0.5, h=4, sigma=MR-bar/1.128 on the baseline
window (Montgomery ISQC 6e §9.1.3), seed=1"`. A default that only lives in the verifier's
signature is exactly the "unstated convention" failure this benchmark already survived once.

### 8.3 Extension of `capability_normal` (fixes the vacuous V7 on `cpk`)

```python
def capability_normal(payload):
    """Adds within-subgroup Cp/Cpk when the payload carries subgroup structure.

    Backwards compatible: Pp/Ppk keep their exact current definition (overall sd, ddof=1),
    so no existing truth changes value. Cp/Cpk are ADDED, which turns adb_c03's currently
    unverifiable `cpk` truth into a verified one (and may reveal it to be wrong — that is
    the point, and the finding should be handled before this ships).
    """
```

Within-sigma source, in priority order: (1) `subgroups` present → `s̄/c4(n)` if n ≥ 9 else
`R̄/d2(n)`; (2) `subgroupSize` + flat `values` → reshape, then as (1); (3) individuals →
`MR̄/d2(2)`. If none apply, emit only pp/ppk exactly as today.
Also add `cpkMargin` when `targetCpk` is in the payload, and `ppkMargin` when `targetPpk` is.

**Migration hazard.** Once `capability_normal` returns `cpk`, `_check_truth_verification`
stops skipping every `capability.normal.cpk` truth in the corpus. Run
`validate_case` over every case in the corpus *before* merging this and triage what turns red; a legacy
truth that the reference implementation cannot reproduce must be re-derived or demoted, not
tolerated with a widened tol.

### 8.4 `two_poisson_rates`

```
Inputs : {"count1", "time1", "count2", "time2"}  (time = exposure/units, may be 1.0)
         optional "alternativeHypothesis" (read via the existing _alternative())
Formula: conditional binomial exact test —
         x1 | (x1+x2) ~ Binomial(x1+x2, pi0), pi0 = time1/(time1+time2)
         p = scipy.stats.binomtest(count1, count1+count2, pi0,
                                   alternative=_alternative(payload)).pvalue
         rateRatio = (count1/time1) / (count2/time2)
Edges  : count1+count2 == 0 -> NotVerifiable; any time <= 0 -> NotVerifiable;
         rate2 == 0 -> rateRatio omitted (inf is not a gradeable truth)
Basis  : Przyborowski & Wilenski (1940) Biometrika 31; the conditional "C-test".
```

### 8.5 Registration

```python
REFERENCE_IMPLS = {
    ...,
    "control_chart.imr": control_chart_imr,
    "control_chart.xbar_r": control_chart_xbar_r,
    "control_chart.xbar_s": control_chart_xbar_s,
    "control_chart.p": control_chart_p,
    "control_chart.np": control_chart_np,
    "control_chart.c": control_chart_c,
    "control_chart.u": control_chart_u,
    "control_chart.laney_p": control_chart_laney_p,
    "control_chart.laney_u": control_chart_laney_u,
    "control_chart.ewma": control_chart_ewma,
    "control_chart.cusum": control_chart_cusum,
    "basic.two_poisson_rates": two_poisson_rates,
}
```

This alone closes the vacuous-V7 hole for all 11 chart methods, retroactively including the
existing `adb_c05` / `adb_c08` / `adb_c17` / `adb_c20` truths (of which only `adb_c17` is in
the public split; the other three are held out). **Expect breakage and treat it
as the deliverable, not the obstacle** — `adb_c17` states in its own docstring that its four
truths were never independently checked.

---

## 9. One worked Control stage set, end to end

Case `adb_c24` (new, `language: en`, `y_type: continuous`, `tier: T3`, `provenance:
SIMULATED`). The same five stages transplant unchanged onto `adb_c06`, whose Xbar-R / Xbar-S /
EWMA / CUSUM stages currently sit in measure and analyze.

Numbers below are **actual computed output**, not illustrative. Reproduce with
`numpy.random.default_rng(1*1_000_003 + 20260904)`, drawing in the order shown in §9.2.
(numpy guarantees `default_rng` stream stability across releases, so V4 determinism holds. If
the corpus's pure-`random.Random` convention is preferred instead, the generator must be
ported *and the truths re-frozen* — do not port the code and keep these numbers.)

### 9.1 Payloads

```jsonc
// stage C_MonitorChart  (Phase I: estimate the limits)
{
  "subgroups": [[...15 values...], ... 25 subgroups ...],
  "subgroupSize": 15,
  "unit": "mm",
  "note": "25 consecutive shifts after the process change; 15 parts measured per shift"
}

// stage C_ResponsePlan  (Phase II: apply them)
{
  "baselineWindow": {"subgroups": [...25 x 15...], "subgroupSize": 15},
  "monitoringWindow": {"subgroups": [...20 x 15...], "subgroupSize": 15},
  "ruleSet": "nelson_1984_tests_1_8",
  "note": "20 further shifts monitored against the frozen limits"
}

// stage C_Verify
{
  "before": [...200 values, pre-improvement...],
  "after":  [...375 values, the 25 x 15 improved subgroups flattened...],
  "alternativeHypothesis": "NOT_EQUAL",
  "note": "pre-change routine inspection vs post-change shifts"
}

// stage C_CapabilityConfirm
{
  "subgroups": [...25 x 15...], "subgroupSize": 15,
  "lsl": 9.00, "usl": 11.00, "targetValue": 10.00,
  "targetCpk": 1.33,                    // <- injected from project_target (Define)
  "note": "customer print tolerance 10.00 +/- 1.00 mm"
}

// stage C_SmallShift   (individuals; drives the EWMA/CUSUM decision point)
{
  "values": [...40 daily individual readings...],
  "target": 10.02,
  "shiftToDetectSigma": 1.0,
  "note": "daily first-off reading; the control plan must catch a 1-sigma drift"
}
```

### 9.2 Truths (with tolerances and classes)

Constants used: `c4(15) = 0.9823164`, `A3(15) = 0.7885406`, `B3(15) = 0.4281999`,
`B4(15) = 1.5718001`, `d2(2) = 1.128`.

| stage | method | field | expected | tol | soft |
|---|---|---|---|---|---|
| C_MonitorChart | control_chart.xbar_s | xBarChartCenterLine | **10.035960** | 1e-4 | no |
| C_MonitorChart | control_chart.xbar_s | sBar | **0.189536** | 1e-4 | no |
| C_MonitorChart | control_chart.xbar_s | sigmaWithin | **0.192949** | 5e-4 | no |
| C_MonitorChart | control_chart.xbar_s | xBarUCL | **10.185418** | 1e-3 | no |
| C_MonitorChart | control_chart.xbar_s | xBarLCL | **9.886503** | 1e-3 | no |
| C_MonitorChart | control_chart.xbar_s | sUCL | **0.297913** | 1e-3 | no |
| C_MonitorChart | control_chart.xbar_s | sLCL | **0.081159** | 1e-3 | no |
| C_ResponsePlan | control_chart.xbar_s | flaggedXBarCountTest1 | **1** | 0 | no |
| C_ResponsePlan | control_chart.xbar_s | firstSignalIndex | **12** | 0 | no |
| C_ResponsePlan | control_chart.xbar_s | flaggedCountNelson | **11** | 1 | **yes** |
| C_Verify | basic.two_sample_t | tStatistic | **14.885452** | 0.02 | no |
| C_Verify | basic.two_sample_t | pValue | **2.99e-37** | 1e-36 | no |
| C_CapabilityConfirm | capability.normal | cp | **1.727576** | 0.01 | no |
| C_CapabilityConfirm | capability.normal | cpk | **1.665452** | 0.01 | no |
| C_CapabilityConfirm | capability.normal | ppk | **1.671448** | 0.02 | **yes** |
| C_CapabilityConfirm | capability.normal | cpkMargin | **0.335452** | 0.01 | no |
| C_SmallShift | control_chart.imr | sigmaWithin | **0.181328** | 5e-4 | no |
| C_SmallShift | control_chart.imr | individualsUCL | **10.563984** | 1e-3 | no |
| C_SmallShift | control_chart.imr | flaggedCountTest1 | **0** | 0 | no |
| C_SmallShift | control_chart.cusum | firstSignalIndex | **20** | 0 | no |
| C_SmallShift | control_chart.ewma | firstSignalIndex | **20** | 0 | no |

Cross-checks that make the design points concrete:

* Phase I is genuinely in control: **0** Xbar flags and **0** s flags over the 25 baseline
  subgroups. A `flaggedCount` truth on Phase I data would be measuring the estimator, which
  is why the split exists.
* The rule-set divergence on the same monitoring window: Test 1 → **1** flagged point;
  Western Electric's four rules → **9** (subgroups 11–19); Nelson 1–8 → **11** (subgroups
  9–19), because Nelson's Test 8 (8 consecutive beyond 1σ) fires on subgroups 9–16 and WE has
  no such rule. Firing detail: Nelson T1 {12}, T5 {12–16}, T6 {11–19}, T8 {9–16}.
* The small-shift stage: 40 individuals, `μ0 = 10.02`, a +0.75σ sustained shift from point 16.
  `MR̄ = 0.204538`, `σ̂ = 0.181328`, limits `[9.476016, 10.563984]`. The I chart flags
  **nothing**; CUSUM(0.5, 4) and EWMA(0.2, 3) both first signal at point **20**. This is what
  makes the memory-chart decision point discriminating rather than stylistic. (Note the
  counts diverge — CUSUM 21 flagged points, EWMA 5 — which is precisely why
  `firstSignalIndex` is the hard truth and `flaggedCount` is soft.)
* `sdOverall = 0.192256` vs `σ̂_within = 0.192949`: nearly equal, as they must be for an
  in-control process. A case where they differ materially is a case that is *not* stable and
  must not reach a capability truth (`capability.normal` already carries the
  `stability_confirmed` prerequisite).

### 9.3 Decision points

```yaml
decision_points:
  - point_id: control_chart_route
    phase: control
    rule: >-
      Fifteen parts are measured per shift and the subgroup size is constant, so the
      dispersion of the sustaining chart must be tracked with the subgroup standard
      deviation, not the subgroup range.
    source: "AIAG SPC-2 2e Ch. II Sec. C (n >= 9 -> Xbar-s); Montgomery ISQC 6e §6.3.1"
    correct_branch: xbar_s
    acceptable_branches: []
    branch_evidence:
      xbar_s: [control_chart.xbar_s]
      xbar_r: [control_chart.xbar_r]     # safe here: xbar_r is required nowhere in adb_c24

  - point_id: control_small_shift_route
    phase: control
    rule: >-
      The control plan requires detecting a one-sigma sustained drift in the daily
      first-off reading; a Shewhart individuals chart alone does not meet that requirement.
    source: "Montgomery ISQC 6e §9.1.1 (Shewhart insensitivity below ~1.5 sigma), §9.1.3, §9.2.3"
    correct_branch: ewma
    acceptable_branches: [cusum]
    branch_evidence:
      ewma:  [control_chart.ewma]
      cusum: [control_chart.cusum]
      # no evidence for a "shewhart_only" branch: control_chart.imr is legitimately required
      # by C_SmallShift itself, so listing it would mark a correct trajectory incorrect.

  - point_id: control_closure_gate
    phase: control
    rule: >-
      Close only when the change is statistically established and the confirmed capability
      clears the chartered target; otherwise return to Improve.
    source: "Montgomery ISQC 6e §1.4; AIAG SPC-2 2e Ch. IV (within vs overall capability)"
    correct_branch: close_project
    acceptable_branches: []
    branch_evidence:
      close_project: [capability.normal]

order_constraints:
  - before: basic.two_sample_t
    after: capability.normal
    source: "Montgomery ISQC 6e §1.4 (confirm the improvement before confirming capability)"
  - before: control_chart.xbar_s
    after: capability.normal
    source: "AIAG SPC-2 2e Ch. IV (capability indices require a demonstrably stable process)"
  - before: control_chart.imr
    after: control_chart.ewma
    source: "Montgomery ISQC 6e §9.2 (the memory chart supplements, not replaces, the Shewhart chart)"
```

### 9.4 What a correct agent trajectory looks like

```
 1  meta.data_profiling         -> continuous; 25 subgroups x 15; constant n; separate
                                   40-point individuals series with a declared
                                   shiftToDetectSigma = 1.0
 2  basic.normality             -> AD p = 0.41 on the improved values (parametric route open)
 3  route_decision              point=control_chart_route  branch=xbar_s
                                observed={subgroupSize:15, constantSubgroupSize:true}
 4  control_chart.xbar_s        -> CL 10.035960, sBar 0.189536, sigmaWithin 0.192949,
                                   xBarUCL 10.185418, xBarLCL 9.886503,
                                   sUCL 0.297913, sLCL 0.081159; Phase I 0 flags
 5  control_chart.xbar_s        -> Phase II on the monitoring window with the frozen limits:
    (2nd step, same method)        flaggedXBarCountTest1 = 1, firstSignalIndex = 12,
                                   flaggedCountNelson = 11 (rule set named in the report)
 6  basic.two_sample_t          -> Welch, two-sided: t = 14.885, p = 3.0e-37
 7  control_chart.imr           -> daily individuals: sigmaWithin 0.181328,
                                   UCL 10.563984, flaggedCountTest1 = 0
 8  route_decision              point=control_small_shift_route  branch=cusum
                                observed={shiftToDetectSigma:1.0, shewhartTest1Flags:0}
 9  control_chart.cusum         -> k 0.5, h 4: firstSignalIndex = 20
10  capability.normal           -> cp 1.727576, cpk 1.665452, ppk 1.671448,
                                   cpkMargin = 1.665452 - 1.33 = +0.335452
11  route_decision              point=control_closure_gate  branch=close_project
                                observed={cpk:1.665452, targetCpk:1.33, improvementP:3.0e-37}
12  report                      states the chart choice and why (n = 15 constant, s not R),
                                the limits, the named rule set (Nelson 1984 Tests 1-8) and
                                its flag count alongside the Test-1 count, the two-sided
                                Welch p-value with the tail named, and the closure verdict
                                as "Cpk 1.67 vs chartered target 1.33, margin +0.34 -> met".
```

Scoring of that trajectory: MS recall 1.0 (all five required methods succeeded); NF 21/21;
PQ 3/3 decision points correct (all explicit) + 3/3 order constraints satisfied = 1.0;
HN fabrication 0 provided every quoted number appears in a step's outputs. TGS = 1.0.

Failure modes the stage set now *catches*, none of which it caught before:

* Running Xbar-R on n = 15 → `control_chart_route` **incorrect** (walked a wrong branch),
  and the R-chart limits are numerically wrong besides.
* Reporting a flagged count with no named rule set → the soft Nelson truth may still pass,
  but the hard `flaggedCountTest1` disambiguates whether the agent actually ran Test 1.
* Declaring the project closed while `cpkMargin < 0` → `control_closure_gate` incorrect.
* Running only the I chart on a plan that demands 1σ detection → `control_small_shift_route`
  scores `unknown` at worst and `incorrect` if the agent explicitly says "Shewhart is
  sufficient".
* Computing Cpk from the overall SD → out of tol against the within-sigma truth, and the
  design deliberately keeps `ppk` as a separate soft truth so the confusion is *visible*
  rather than silently absorbed.

---

## 10. Authoring rules and rollout

### 10.1 Rules that must go into the case-onboarding specification

1. Every control stage declares Phase I (`baselineWindow`) and Phase II (`monitoringWindow`)
   whenever it carries a flagged-count truth.
2. Subgroup sizes are `1`, `2..5`, or `>= 15`. `9..12` is an ERROR (§1.2).
3. Overdispersion cases land clearly on one side of the determinacy band (§1.2 D1).
4. `|cpkMargin| >= 0.10`; improvement `p < 0.01` or `p > 0.20` (§4.3).
5. Every convention default (λ, L, k, h, rule set, tail, pooled/unpooled, within/overall
   sigma) is repeated verbatim in the truth's `derivation` string. A default that only exists
   in a function signature is an unstated convention.
6. A wrong branch gets `branch_evidence` only if its method is required nowhere else in the
   same case (§1.3).
7. `y_type` for a control stage is the type of the **improved** Y. A project that converts an
   attribute Y to a continuous one in Improve changes the correct chart family; that is a
   legitimate and interesting case, and the case's `y_type` should then be `mixed` (which
   also disables MS-Misuse, correctly).

### 10.2 Suggested sequencing

| Step | Work | Gate |
|---|---|---|
| 1 | Add the shared helpers + 11 chart verifiers + `two_poisson_rates` to `truth/verifiers.py`, with unit tests against the constant table and against textbook worked examples | new tests green |
| 2 | Extend `capability_normal` with within-sigma Cp/Cpk; run `validate_case` over every case in the corpus | triage every newly-red legacy truth **before** merging |
| 3 | Enrich the 11 taxonomy entries' `canonical_outputs`; add `basic.two_poisson_rates` | `taxonomy.load()` + existing tests green |
| 4 | Author the worked `adb_c24` control stage set; then retrofit control stages onto the cases that already have improvement data (`adb_c05`, `adb_c06`, `adb_c08`, `adb_c17`, `adb_c20`, `adb_c21` — of which `adb_c06`, `adb_c17` and `adb_c21` are public and the rest held out) | V1–V9 clean per case |
| 5 | Add one `control_chart_route` + one `control_closure_gate` per control-carrying case | PQ control-phase point count ≥ 26 |
| 6 | Re-run the full campaign; report the Control-phase sub-scores separately in the paper | — |

### 10.3 Two hazards to keep in view

* **There are two scorers.** The Harbor/benchmark path uses `dmaic_bench/scoring/hn.py`; a
  second, drifted copy of the fabrication logic lives in the originating evaluation harness,
  which is not part of this repository. Any `metric_cue` regex introduced by control-phase
  truths must be validated against the scorer the campaign actually runs, and — in the
  development tree, where both exist — any change to fabrication logic must be made in both.
* **`metric_cue` regexes must cover the English report vocabulary.** Preserve matching
  for `UCL` / "upper control limit", "Nelson" / "Western Electric" / special-cause
  criteria, and `Cpk` / process capability index. This historical proposal originally
  called for bilingual cues during migration. The current release is English-only;
  validate cue behavior against English reports without changing scoring semantics.

---

## Appendix A — sources cited

* AIAG, *Statistical Process Control (SPC)*, 2nd ed., 2005 — Ch. II Sec. C (chart selection,
  subgroup size), Ch. IV (within vs overall variation), Appendix E (constants).
* ASTM E2587-16, *Standard Practice for Use of Control Charts in Statistical Process Control*
  — Table 3 (d2, d3, D3, D4, c4, A2, A3, B3, B4).
* D. C. Montgomery, *Introduction to Statistical Quality Control*, 6th ed. — §1.4 (DMAIC),
  §4.5 / §6.2.3 (Phase I vs Phase II), §6.3.1 (R vs s), §6.4 (individuals), §7.2 (p, np),
  §7.3 (c, u, dispersion), §9.1 (CUSUM, Eq. for the tabular scheme), §9.2 (EWMA, Eq. 9.26).
* D. C. Montgomery & G. C. Runger, *Applied Statistics and Probability for Engineers*, 7th ed.
  — §10.2.2 (Welch), §10.4 (paired).
* L. S. Nelson (1984), "The Shewhart Control Chart — Tests for Special Causes",
  *Journal of Quality Technology* 16(4), 237–239.
* Western Electric Co. (1956), *Statistical Quality Control Handbook*, pp. 25–28.
* D. B. Laney (2002), "Improved Control Charts for Attributes",
  *Quality Engineering* 14(4), 531–537.
* P. McCullagh & J. A. Nelder (1989), *Generalized Linear Models*, 2nd ed., §4.5.2.
* J. L. Fleiss, B. Levin & M. C. Paik (2003), *Statistical Methods for Rates and Proportions*,
  3rd ed., §2.3.
* B. L. Welch (1947), "The generalization of Student's problem…", *Biometrika* 34, 28–35.
* J. Przyborowski & H. Wilenski (1940), "Homogeneity of results in testing samples from
  Poisson series", *Biometrika* 31, 313–323.
* L. H. C. Tippett (1925), "On the extreme individuals and the range of samples taken from a
  normal population", *Biometrika* 17, 364–387 (the d2 integral).
* J. M. Lucas & M. S. Saccucci (1990), "Exponentially weighted moving average control
  schemes: properties and enhancements", *Technometrics* 32(1), 1–29 (λ/L design).
* ISO 22514-2:2017, *Statistical methods in process management — Capability and performance*.
