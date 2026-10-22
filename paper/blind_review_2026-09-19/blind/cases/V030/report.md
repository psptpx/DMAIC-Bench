# Seal Strength Project - Status Report

**Product:** assembled optical module, housing seal
**Requirement:** seal strength must hold above **45 N** (lower spec limit); the programme margin commits to **55 N**
**Data:** all figures below were computed in this engagement from the batches released by the data steward; nothing is quoted from memory or prior experience.

---

## 1. Where the line stands (baseline, 60 consecutive assemblies)

Across the 60 baseline assemblies, seal strength averaged **59.13 N** with standard deviation **7.95 N** - but that average hides the real story. The process is **not stable**:

- A runs test on the build sequence gives p = **4.5e-08**: the run order is decisively non-random.
- The first 30 assemblies average **52.34 N**; the last 30 average **65.92 N** (Welch two-sample t = -12.88, p = **1.2e-18**). There was a step change mid-run.
- The pooled sample fails normality (Shapiro-Wilk p = **0.0053**; Anderson-Darling p = **0.0057**), consistent with a mixture of two states rather than one capable process.
- An individuals (I-MR) chart puts the centre line at **59.13 N** with limits [45.52, 72.74]; **1** point flags out of control. The limits are inflated by the shift itself.

**Against the product requirement:** pooled Ppk vs the 45 N spec is only **0.59**. **35%** of baseline assemblies (21 of 60) fell below the required 55 N, although none fell below the 45 N hard limit. As run, the baseline cannot hold the committed margin.

I asked the process owner whether any tooling, operator, or material-lot change was recorded at the shift point; the steward holds **no process facts** for this line (request refused as unroutable), so the cause of the mid-run shift is **unknown from available data**. This matters: the late-run state actually produced the strongest seals seen (65.92 N average), and understanding what changed there is a live opportunity (see Section 5).

## 2. Do the varied settings account for seal strength? (screening)

A full 2^3 factorial (bond_angle, bead_spacing, cure_temperature, each low/high, every combination run twice; 16 runs) says yes:

- Model F = **27.36**, p = **5.6e-05**, R^2 = **95.99%**.
- **bond_angle**: effect **+4.85 N** (p < 1e-04) - the dominant lever.
- **bead_spacing**: effect **+2.68 N** (p = 0.0003).
- **bond_angle x bead_spacing interaction**: **+2.37 N** (p = 0.0006).
- **cure_temperature**: no detectable effect (p = **0.875**) - dropped from further work.

A reduced model on the two real factors plus their interaction keeps R^2 = **95.65%** (p = 1.9e-08). The settings that were varied genuinely drive seal strength; I declared `any_factor_significant = true` to the steward on this basis.

## 3. What the design work supports (composite design / RSM)

A central composite design over bond_angle and bead_spacing (4 factorial + 4 axial + 5 centre runs = 13 runs) supports a full quadratic surface:

- R^2 = **98.98%**, adjusted R^2 = **98.25%**; lack-of-fit p = **0.837** - the surface fits, no evidence of model inadequacy.
- Canonical analysis: stationary point at coded **bond_angle = 0.664, bead_spacing = 0.616**; both eigenvalues negative (-2.25, -1.63), so it is a **true maximum**.
- Predicted strength at the optimum: **59.58 N**, with a 95% prediction interval of **[58.38, 60.77] N** - the entire interval clears the 55 N requirement. Composite desirability = **1.0**.

## 4. Did the change hold up? (confirmation at recommended settings)

Twenty seals were built at the recommended settings:

- Mean **59.38 N**, SD **1.97 N**, range **56.55 - 63.77 N**; **every seal above 55 N**.
- Data are consistent with normality (Shapiro-Wilk p = **0.41**), so capability indices are meaningful.
- One-sample t vs the required 55 N: t = **9.94**, one-sided p = **2.9e-09** - the process is significantly above the requirement, not marginally.
- Ppk vs the 45 N spec: **2.43** (baseline was 0.59). Expected fraction below the 55 N requirement: about **1.3%** (was 35%).
- The 95% confidence interval for the confirmation mean, **[58.45, 60.30] N**, contains the RSM prediction of 59.58 N - the model predicted reality.
- Against the pre-shift baseline state, the gain is **+7.03 N** of mean strength (p = 2.4e-10).

## 5. Where the project stands and what happens next

**The goal is met at the recommended settings.** Seal strength moved from an unstable baseline averaging 52-66 N in two distinct states, with 35% of product below the required 55 N, to a verified process centred at 59.4 N with all 20 confirmation seals in spec and Ppk 2.43 against the hard limit. Bond angle and bead spacing are the levers; cure temperature does not matter over the range screened.

**Open items - stated honestly:**

1. **The baseline shift is unexplained.** The last 30 baseline assemblies averaged 65.92 N - 6.54 N *above* the optimised confirmation mean (p = 1.7e-09) - with no recorded process fact to explain it. Either something good happened that we have not captured (a setting drifted toward a better region our design did not explore), or the measurement/build conditions changed. This must be investigated before locking the process: it could hold several more newtons of margin.
2. **No process facts are on record** for this line (the steward refused the provision request as unroutable - no topics recorded). Conclusions about *why* the shift happened stop here; I will not guess.
3. **Control going forward:** the baseline shows this process can shift without warning. Run an individuals chart on seal strength in build order, with control limits computed from the confirmation state (mean 59.38 N, SD 1.97 N), and reaction rules on any point below 55 N. Note that with SD ~2 N and a 4.4 N cushion to 55 N, common-cause points below 55 N are expected roughly 1.3% of the time; any cluster of them signals a special cause.
4. The ~1.3% expected fraction below 55 N, while vastly better than the baseline 35%, is not zero; if the programme requires every seal above 55 N, the shift investigation (item 1) is the cheapest source of further margin, since the late-baseline state demonstrably achieved it.

## Traceability

Every number above appears in `trace.json` under the corresponding step: baseline descriptive/normality/I-MR/runs/capability/shift test (steps 1-6), screening factorial and reduced model (7-8), RSM fit, canonical, optimizer and prediction (9-12), confirmation descriptive, normality, t-test and capability (13-16), and the before/after comparisons (17-18). One `provision` call was made and refused (unroutable); no billed autonomy turns were consumed (0/28).
