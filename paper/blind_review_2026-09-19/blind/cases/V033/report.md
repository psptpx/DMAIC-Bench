# Void fraction project — status report

**Task:** [TASK] · **Acceptance limit:** 0.0 to 25.0 percent void area (upper limit governs) · **Data:** 3 batches released by the data steward

> **A note on scope before the numbers.** The project brief describes a honing line and a roughness band of 0.40 to 1.60 um Ra. Every batch the plant actually holds is X-ray **percent void area** against an upper acceptance limit of **25.0**, measured per joint in build order. This report analyses the data that exists. No roughness/Ra data was released and none was requested successfully, so nothing here should be read as a statement about Ra or about a 1.60 limit.

---

## 1. Bottom line

| Question | Answer |
|---|---|
| Can the readings carry a conclusion? | **Yes, with a caveat.** Measurement error is 13.65% of tolerance and 18.61% of study variation — conditionally acceptable. |
| How has the line behaved across the run? | **Badly in one specific way.** The process is not stable: it took a sustained step **up by 5.30 percentage points** at joint 25 and has stayed there. |
| Where does voiding sit against its limit today? | **Inside the limit, with margin.** Current level 14.48 against a limit of 25.0; **Ppk 2.00**; **0 of 50** joints have ever exceeded the limit. |
| What should change next? | Find and reverse the joint-25 step change. **This is where the analysis stops for lack of data** (Section 6). |

The headline is that the line is not in trouble on conformance, but it is in trouble on control. It gave away roughly a third of its margin to the limit in a single unexplained step and nobody caught it.

---

## 2. Can we trust the readings? (Measure)

A crossed gage R&R study was released: 3 operators × 12 joints × 3 repeats = **108** readings, tolerance 25.0. Analysed by the ANOVA method.

The operator × joint interaction is not significant (**p = 0.937**), so it was pooled into repeatability — the operators do not disagree differently on different joints.

| Measure | Result | Verdict |
|---|---|---|
| Total gage R&R, % study variation | **18.61%** | under 30% — conditionally acceptable |
| Total gage R&R, % tolerance | **13.65%** | comfortable against the 25.0 limit |
| % contribution to total variance | **3.46%** | measurement noise is a small share |
| Distinct categories (ndc) | **7.44** | above 5 — the gage can rank joints |
| Repeatability, % study variation | **17.59%** | the dominant component |
| Reproducibility, % study variation | **6.10%** | secondary |

Joint-to-joint variation carries **96.54%** of total variance, measurement error **3.46%**. Real differences between joints dominate, which is what makes the rest of this analysis possible.

Two honest qualifications. First, operator bias **is** statistically detectable (**p = 0.0064**) — small in magnitude, but real; the operators are not interchangeable to the last decimal. Second, at 18.61% the system is *conditionally* acceptable, not good: the limiting factor is the tester repeating itself (17.59%), not the people. Every conclusion below inherits that noise floor, which is why the step change had to be confirmed by several independent methods rather than one.

**Decision taken: proceed with the analysis.** The measurement system is good enough to support conclusions about a 5-point shift.

---

## 3. How has the line behaved? (Analyse)

Fifty joints in build order. Mean **11.83**, median **11.24**, standard deviation **3.09**, range **6.31 to 17.70**.

The pooled run fails normality — Anderson-Darling **p = 0.0195**, Shapiro-Wilk **p = 0.0479**. That is the first clue: not skew, but a mixture of two populations.

### The process is not in control

An I-MR chart over the whole run, centre line **11.83**, limits **7.13 to 16.52**:

- **5** points beyond the individuals limits
- **27** points inside runs of 9 or more on one side of the centre line
- a runs test about the median gives **10** runs where **26** were expected, **p = 0.0000048**

The ordering is not random. Something moved and stayed moved.

### The step change, dated three ways

| Method | Signal |
|---|---|
| Maximum-t changepoint scan | break at **joint 25** |
| Tabular CUSUM (k=0.5, h=4) vs. the early baseline | first signal at **joint 25**, then signalled for **25** consecutive joints |
| EWMA (λ=0.2, L=3) | first signal at **joint 26** |

Sizing the step:

| | Joints 1–25 | Joints 26–50 |
|---|---|---|
| Mean void fraction | **9.18** | **14.48** |
| Standard deviation | **1.31** | **1.76** |

- Step size: **+5.30** percentage points
- Welch two-sample t: **t = −12.09, p = 0.0000000000000012**
- Mann-Whitney (distribution-free confirmation): **p = 0.0000000029**
- Levene test on spread: **p = 0.302**

That last number matters for diagnosis. **The spread did not change — only the level did.** A process that loses control of its variability looks noisy; this one shifted cleanly to a new setting and became stable again there. That is the signature of something being *set* differently — a lot, a parameter, a fixture, a tool change — not of the process degrading or wearing.

Each segment is well behaved on its own: the early segment shows **0** control-chart flags, and the current segment shows **0** flags about its own centre line of **14.48** (limits **9.54 to 19.42**). Both segments pass normality (AD **p = 0.709** and **p = 0.678**). The instability is one event, not chronic noise.

### It is holding, not still sliding

Void fraction regressed on build order within the current 25 joints: slope **0.053** per joint, **p = 0.282**, R² **5.0%** (adjusted **0.9%**). No significant residual drift. The line has settled at the worse level rather than continuing to deteriorate — which buys time, but does not fix anything.

---

## 4. Where does voiding sit against the acceptance limit?

**Capability on the pooled run is not a valid statement and is not being reported as one.** Stability is a precondition for capability, and it fails (5 out-of-limit points, runs test p = 0.0000048, AD p = 0.0195). For the record the pooled figures come out at Cp **2.66** / Cpk **2.52** / Pp **1.35** / Ppk **1.28**, and the wide gap between Cpk 2.52 and Ppk 1.28 is nothing but the arithmetic shadow of the uncontrolled step. Quoting Cpk 2.52 to a customer would be misleading.

**The valid statement is capability of the current, stable segment:**

| | Current segment (joints 26–50) | Earlier segment (joints 1–25) |
|---|---|---|
| Mean | **14.48** | **9.18** |
| Standard deviation | **1.76** | **1.31** |
| Cp / Cpk | **2.53** / **2.13** | **3.09** / **2.27** |
| Pp / **Ppk** | **2.37** / **2.00** | **3.17** / **2.33** |
| Joints over the 25.0 limit | **0 of 25** | **0 of 25** |
| Expected ppm above limit | **0.001** | **0.0** |

Supporting tests: the current mean is significantly below the acceptance limit (one-sample t vs. 25.0: **t = −29.95, p = 0.000000000000000000016**), and across the whole run **0 of 50** joints exceeded the limit — observed nonconforming fraction **0.0**, not significantly greater than a 5% reference (**p = 1.0**).

**So: voiding is inside its acceptance limit today, comfortably, and no joint has ever breached it.** Ppk 2.00 clears the usual 1.33 expectation with room to spare.

The warning is in the comparison, not the absolute. The line demonstrated **Ppk 2.33** at a mean of 9.18 before the step and now delivers **Ppk 2.00** at 14.48. It surrendered real margin for no known reason, and it did so without anyone stopping the line. A second step of the same size would put the mean near 19.8 against a limit of 25 — at that point the margin is thin and scrap starts to be a question of luck.

---

## 5. What is causing it?

**Unknown, and not determinable from the data available.** The evidence narrows the cause considerably without identifying it:

- it began at **joint 25** (three independent detection methods agree within one joint)
- it moved the **mean only**, not the spread (Levene **p = 0.302**)
- it was a **step, not a drift** (no significant trend within either segment; current-segment slope **p = 0.282**)
- it is **not measurement artefact** — the shift is 5.30 points against a gage R&R standard deviation of **0.57**, and measurement error accounts for only **3.46%** of total variance

That profile points at a discrete change to an input or a setting at that moment in the build sequence. Identifying which one requires process facts that this project does not contain — see below.

---

## 6. Gaps: what could not be obtained, and what it costs

This section exists because the honest answer to part of the brief is "no data."

**Root cause — no data.** The process owner was asked what changed on the line around joint 25 (material lot, equipment setting, tooling, operator). The answer was that no process fact matching that exists, and that **no process topics are recorded at all** for this project. One provision turn was spent establishing this; further questions would return the same. **Consequence: the step change can be dated, sized and characterised, but not explained.** No cause is asserted in this report because none was obtained, and inventing a plausible one (a lot change, a fixture swap) would be fabrication.

**Improvement — no data, because no improvement happened.** The steward holds exactly three batches: the charter, the gage study, and the 50-joint run. There is **no improve-phase batch and no control-phase batch**. So, plainly:

- **What was changed: nothing.** No countermeasure was implemented within this project.
- **What the change achieved: not applicable.** There is no before/after data because there is no "after."
- **How it will be held: cannot be evidenced.** No control plan, no post-change data, no verification of a hold exists.

Anyone reading a completed DMAIC story into this project would be reading something that is not here. **This project stands at the end of Analyse.** It has established that the measurement system is adequate, that the process is out of control in one specific, dated, quantified way, and that conformance is nevertheless currently safe. It has not improved anything, and it cannot claim to have.

**Also not available:** any roughness/Ra data, and any joint-level covariates (lot, machine, operator, shift) that would let the step be attributed by regression or ANOVA. With only an index and a value per joint, attribution is impossible in principle from this dataset, not merely unattempted.

---

## 7. Recommendations

Ranked by what the numbers actually support.

1. **Reconstruct what changed at joint 25.** This is the whole project. The window is tight and precisely dated. Pull build records, lot certificates, parameter logs, tooling changes and shift handovers spanning joints 24 to 26 and find the discrete event. Until this is answered, nothing can be fixed and nothing can be prevented from recurring.
2. **Start recording joint-level context with every reading.** Lot, machine, tool, operator, shift. Without it, the next step change will be just as undiagnosable as this one. Fifty numbers and an index cannot answer "why."
3. **Put the early segment's performance on the board as the recovery target.** The line has already demonstrated a mean of **9.18** at **Ppk 2.33**. That is not aspirational, it is history — it ran that way for 25 consecutive joints with zero control-chart flags.
4. **Chart void fraction going forward with limits fixed on the demonstrated baseline** (centre line **9.18**, limits **5.14 to 13.22**), not on the current inflated level. Recentring the chart on 14.48 would normalise the loss. CUSUM caught this step at the first joint after it occurred; a chart run live would have flagged it in real time instead of 25 joints later.
5. **Work the tester's repeatability when the shift work is done.** At **17.59%** of study variation it is the larger half of a **18.61%** gage R&R and the reason the system is only conditionally acceptable. Also worth resolving the small but real operator bias (**p = 0.0064**) through a fixturing or procedure review.
6. **Do not report Cpk 2.52.** The only defensible capability statement is the current segment's **Ppk 2.00 / Cpk 2.13**, and it should be quoted with the caveat that it describes a level the process arrived at by an uncontrolled step.

---

## 8. Traceability

Every figure above comes from a computation performed on this run and recorded in `/workspace/trace.json` (**19** analysis steps, **7** route decisions). Source batches: `define` (charter and limits), `msa` (108 repeat readings), `process_run` (50 joints in build order). Billed provision turns: **1** of 22 — the single root-cause question, which returned no data.
