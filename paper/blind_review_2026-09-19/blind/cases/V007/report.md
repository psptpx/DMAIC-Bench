# Bore Finish (Roughness) — Project Report

**Task:** [TASK] · Honing line, cylinder bore finish
**Requirement:** 0.40 to 1.60 um Ra, target 1.00 um, tolerance width 1.20 um
**Data used:** operator repeat-reading study (90 readings) and the per-bore production record (50 bores in finishing order)

---

## Headline

The honing process is stable and every bore in the run measured inside the accepted band. But the readings the line records cannot support a precise conclusion about bore finish, because **89.72% of the variation in the production record is measurement noise, not bore-to-bore variation**. The number to act on is the roughness tester, not the honing spindle.

Assembly's returns are not explained by anything visible in this run: 0 of 50 bores fell outside 0.40–1.60 um Ra.

---

## 1. Can the recorded readings carry a conclusion? No.

Crossed Gage R&R (ANOVA method) on 3 operators × 10 bores × 3 repeats:

| Measure | Result | Bar | Verdict |
|---|---|---|---|
| % of tolerance consumed | **46.67%** | under 30% | fails |
| % study variation | **28.27%** | under 30% | marginal |
| Distinct categories (ndc) | **4.78** | at least 5 | fails |
| % contribution (variance) | 7.99% | under 9% | passes |

The gage alone eats **46.67% of the 1.20 um band**. Gage standard deviation is **0.0934 um**; the entire spread of the 50-bore production run is **0.0985 um**. The tester is nearly as wide as the process it is supposed to judge.

Splitting the gage: repeatability **37.84%** of tolerance, reproducibility **27.32%** — repeatability (the tester repeating itself on one bore) is the larger share, but operator differences are real and significant (p = 0.0019).

The part × operator interaction was not significant (p = 0.155); it was retained under the standard alpha = 0.25 screening rule, which is the conservative choice.

### Where the operator difference sits

An unblocked one-way ANOVA on operator finds nothing (F = 0.737, p = 0.482) because bore-to-bore spread swamps it. Comparing operators on **the same ten bores** is the valid test, and it is decisive:

- operator1 vs operator2: **p = 0.0038**
- operator1 vs operator3: **p = 0.0055**
- operator2 vs operator3: p = 0.911 (they agree)

Operator means: 1.0991, 1.1835, 1.1862 um — a spread of **0.0871 um**. Operator1 reads low by roughly that amount; the other two are interchangeable. Scatter is equal across all three (Levene p = 0.825, Bartlett p = 0.915), so this is a **fixed offset in method, not an erratic operator**.

---

## 2. How has the line behaved across the run?

Stable, with no signal worth chasing.

- **I-MR chart** (50 bores, finishing order): centre 1.0334, limits **0.7414 to 1.3253**. **0 points beyond limits**, **0 moving ranges** beyond 0.3586.
- Nelson run rules: tests 2, 3 and 6 all clear. Only test 5 (2 of 3 beyond 2 sigma) fires, on **3 points** — bores 37–39. Largest deviation in the whole run is 2.37 sigma.
- **Runs test** about the median: 24 runs against 26.0 expected, **p = 0.568**. No clustering, no oscillation, no mixing.
- **No drift**: correlation of roughness against finishing order r = 0.123, **p = 0.395**. Lag-1 autocorrelation 0.069. No tool-wear ramp across the run.
- **Distribution**: normal (Anderson-Darling **p = 0.527**, Shapiro-Wilk p = 0.478), mild right skew 0.303. Normal-theory limits and indices are appropriate.

The three test-5 points sit at 1.242, 1.049 and 1.264 um — all comfortably inside spec, and all within a single gage standard deviation of ordinary variation. Given that gage sigma (0.0934) is three times the residual process sigma (0.0316), **the most likely explanation for those flags is the tester, not the honing process.** They do not warrant a hunt for a special cause on the line.

---

## 3. Where does bore finish sit against the band today?

| Index | Value |
|---|---|
| Cp | 2.055 |
| Cpk | 1.941 |
| Pp | 2.029 |
| Ppk | 1.917 |
| Cpm (vs target) | 1.922 |
| Observed out of spec | **0 of 50 (0.0%)** |
| Expected ppm out of spec | 0.0045 |

On paper this is excellent — well past the usual Cpk 1.33 gate. **Read it with care.** These indices describe the spread of *readings*, and most of that spread is the tester. Strip out the measured gage variance and the residual bore-to-bore standard deviation is **0.0316 um** against an observed 0.0985 um.

The honing process is therefore *better* than the record makes it look, not worse. A gage-corrected Ppk works out to 5.98, but I am quoting that as an **upper bound and not a claim**: it comes from subtracting one study estimate from another, and no independent data in this project confirms it.

**Centring:** mean is 1.0334 um against a 1.00 target — an offset of 0.0334 um, statistically detectable (t = 2.394, **p = 0.021**) but worth 2.8% of the band and *smaller than one gage standard deviation*. Adjusting the line to close it would be tampering with noise. Recommendation: leave the mean alone.

---

## 4. What should change next

The measurement system is the constraint. Two actions, in order:

**a) Standardise the measuring method and re-train operator1.** The offset is 0.0871 um and specific to one operator, with equal scatter across all three — that is the signature of a method difference (fixture, cutoff, traverse placement), not operator carelessness. Fix the method, write it down, make all three work to it.

**b) Record each bore as the average of 3 traces, not a single trace.** Repeatability is the bigger half of the gage problem and averaging is the direct lever on it.

Recomputing %tolerance from the measured variance components projects:

| Change | Projected % of tolerance |
|---|---|
| Average 2 traces | 38.24% |
| Average 3 traces | 34.98% |
| Remove operator offset only | 37.84% |
| **Both together** | **21.85%** |

Either action alone leaves the gage failing the 30% bar. **Both together clear it.** These are projections, arithmetic on the variance components measured here — they are not results, and a fresh Gage R&R must confirm them before anyone trusts a capability number off this line.

**Do not touch the honing parameters yet.** Until the gage is fixed there is no measurement resolution to detect whether a process change helped. Chasing the 0.033 um centring offset or the bores 37–39 flags now would be reacting to tester noise.

---

## 5. What this report cannot tell you — gaps, stated plainly

The project asks what was changed, what the change achieved, and how it will be held. **I cannot answer those three, because the data does not exist.**

- **No after-change data.** I requested after-change trial readings explicitly. The steward refused: no such batch exists in this project. **No improvement effect is claimed and none was measured.** The changes in section 4 are recommendations that have not been trialled.
- **No control-phase data.** No ongoing monitoring readings and no control plan exist to request. **How the gain will be held cannot be reported** — only proposed: re-run the Gage R&R after the method fix, then keep the I-MR chart on bore roughness using limits re-established on post-fix readings (the current limits, 0.7414 to 1.3253, are inflated by gage noise and should not be carried forward).
- **No designed experiment.** No factor study on stone grit, pressure, speed or dwell exists. No statement about which honing variables drive roughness can be made from this data.
- **No process facts.** Two questions to the process owner — whether each production reading is a single trace or an average, and the operator method and tester calibration state — were both refused; this project records no process facts. So the *mechanism* behind operator1's offset is inferred from the variance components, not confirmed on the shop floor. Verify it before re-training.
- **No improvement target.** The charter released the band and target but no numeric improvement target, so progress against one is not reported.

**One honest caveat on the returns.** Assembly returned units, yet 0 of 50 bores in this record are out of spec. That mismatch is unresolved and this data cannot resolve it. With a gage consuming 46.67% of tolerance, a bore reading 1.55 could truly be past 1.60 and be passed — the nearest reading to a limit in this run sits 3.60 gage sigma below the upper limit, so *this* run is likely clean, but the screening on the line has not been reliable. Fixing the gage is also the fix for return risk.

---

## Summary for the quality manager

**Where things stand:** process stable and in control, every bore in spec, apparent Cpk 1.94 — but the number is not trustworthy.
**What is causing it:** the roughness tester, consuming 46.67% of the tolerance band and 89.72% of the recorded variance, with one operator reading 0.0871 um low.
**What was changed:** nothing yet. No improvement was run and no after-change data exists.
**What the change achieved:** cannot be reported — see above.
**How it will be held:** proposed only — re-qualify the gage, then re-baseline the control chart on post-fix readings.

The first spend should go to the measurement system. Everything else on this line is currently being judged through a tester that cannot see the process.
