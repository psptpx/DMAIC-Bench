# Bore Roughness (Ra) Project Report — Honing Line

**Scope.** Accepted band for bore finish is 0.40–1.60 um Ra with 1.00 um Ra as the target (tolerance width 1.20). Data released by the steward: the project charter, the roughness-tester repeat-reading study (3 operators x 10 bores x 3 replicates = 90 readings), and the per-bore roughness record of 50 consecutive bores in finishing order. Every figure below comes from computations on these batches (see `/workspace/trace.json`).

## 1. Can the recorded readings carry a conclusion? — Yes, with caution

A crossed gage R&R (ANOVA method, 6-sigma spread) on the operator study gave:

- %StudyVariation = **25.69%**
- %Tolerance = **43.92%**
- Distinct categories (ndc) = **5**
- Part-to-part variation highly significant (p ≈ 1.1e-16); operator effect small but present (p ≈ 5.0e-6); operator-by-part interaction absent (p = 0.679).

Judgement: %StudyVariation under 30% with ndc = 5 puts the tester in the marginal-but-usable zone for monitoring this process. The high %Tolerance (43.92%) reflects that the 10 study bores spanned almost the whole band; for pass/fail decisions near a limit the measurement error is not negligible. Readings can carry the conclusions below; a later gage improvement (operator bias, p ≈ 5.0e-6) would tighten borderline calls.

## 2. How the line behaved across the run — stable, but high-centered

On the 50-bore run in finishing order:

- Mean = **1.109 um Ra** (target 1.00), median = 1.121, stdDev = 0.1955, skewness = 0.170.
- Anderson-Darling normality p = **0.779** — readings are consistent with a normal distribution, so normal-theory limits and capability indices are valid here.
- I-MR control chart: center line 1.109, UCL 1.685, LCL 0.533, **0 points out of control**; mean moving range 0.2165.
- Runs test about the median: p = **0.391** — no trend, drift or clustering over the run.

The process was in statistical control for the whole run. Its behaviour is a steady, common-cause system sitting above target.

## 3. Where bore finish sits against the band today

- Cp = **1.042**, Cpk = **0.853**; Pp = **1.023**, Ppk = **0.837**.
- **1 of 50** bores was out of spec: 1.64 um Ra vs the 1.60 upper limit.

The spread fits the band (Cp > 1), but the process is centered at 1.109 instead of 1.00, which drives Cpk/Ppk below 1 and pushes parts toward the upper limit. The single out-of-spec bore is the visible symptom; with the mean where it is, more near-miss parts will follow.

## 4. What should change next

1. **Recenter the process to the 1.00 target.** The required shift is about 0.11 um Ra of mean. Because the process is stable (0 out-of-control points, runs-test p = 0.391), this is a centering adjustment, not firefighting. Recentering alone would lift Cpk toward Cp (≈1.04) at the current spread.
2. **Verify with a new run** after the adjustment and recompute control limits and capability before declaring the change successful.
3. **Hold the gains** by keeping the I-MR chart in finishing order live, with reaction rules at the control limits (0.533 / 1.685 at the current spread, re-based after the change).
4. **Medium term:** reduce spread (Cpk ≈ 0.85 leaves little margin even after recentering) and improve the measurement system — the operator effect (p ≈ 5.0e-6) and 43.92% %Tolerance argue for an operator-alignment check on the roughness tester.

## 5. Gaps and honesty notes

- **No post-change / improvement data exists.** The steward holds only the three batches above; requests for improvement-action, verification-run and control-plan data were refused as unroutable (such batches do not exist). The conclusion therefore stops at a recommendation: nothing can be reported about what was changed or what a change achieved, because there is no data for it.
- Two questions put to the process owner (`provision`) about which honing settings control centering and whether any change had already been made were refused — no process facts are recorded. The recentering recommendation is statistical, not tied to a named machine setting.
- Provision budget used: 2 of 22 turns.

## Bottom line

The tester can carry the conclusion (marginal gage: %SV 25.69%, ndc 5). The line is stable but runs high: mean 1.109 vs target 1.00, Cpk 0.853, Ppk 0.837, one bore out of spec. Recenter to target, verify with a fresh run, and hold with the I-MR chart; then work on spread and on the gage's operator effect.
