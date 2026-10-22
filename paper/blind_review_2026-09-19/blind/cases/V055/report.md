# Voiding Project Status Report

**Task:** [TASK]
**Prepared for:** Plant quality manager
**Scope:** Joint void fraction against the acceptance limit (LSL = 0.0, USL = 25.0 percent void area; goal: void fraction under the acceptance limit and holding steady)

## 1. Can the recorded readings carry a conclusion?

Before trusting the void-fraction readings, we analyzed the repeat X-ray gage study: 3 operators, 12 joints, 3 repeat readings each (108 readings total), a crossed Gage R&R.

- percent Study Variation (GRR): 28.08 percent, in the AIAG marginal band (10-30 percent). Under 30 percent it is not an automatic rejection of the gage, but it is well above the good threshold of 10 percent.
- percent Tolerance (GRR): 19.72 percent, comfortably under the 30 percent AIAG ceiling, i.e. the gage's own error is a small fraction of the 25-point tolerance band.
- Number of Distinct Categories (NDC): 4.82, just short of the AIAG recommendation of 5 or more distinct categories the gage should be able to tell apart.
- The operator main effect (p = 0.167) and the part-by-operator interaction (p = 0.377) are both statistically non-significant; almost all of the measurement error is plain repeatability, not disagreement between operators.

Conclusion on measurement capability: the X-ray gage is marginal, not good. It is precise enough to support a directional, plant-level read on where voiding sits relative to the 25 percent limit (the answer in section 3 below), but it is not precise enough to reliably tell two joints with genuinely close void levels apart (NDC below 5), and it should not be the basis for joint-by-joint accept/reject decisions without improvement to repeatability.

## 2. How has the line behaved across the run?

We ran an I-MR (individuals and moving range) control chart on the 50 void-fraction readings in the order the joints were finished.

- Center line (process mean): 9.69 percent void area
- Individuals control limits: LCL 2.89 / UCL 16.49
- Flagged points: 0 of 50, on both the individuals chart and the moving-range chart

No point exceeded the control limits in either chart. Across this run, the process shows no special-cause signal; it is behaving as a stable, in-control process, not drifting or showing shifts joint to joint.

We also checked whether the readings are close enough to normal to support a standard capability model: Shapiro-Wilk gave p = 0.401, and Anderson-Darling gave an approximate p = 0.477. Neither rejects normality, and skewness is near zero (0.083). The data support a normal-distribution capability analysis.

## 3. Where does voiding sit against its limit today?

With the process confirmed stable and approximately normal, we computed capability against LSL = 0.0 / USL = 25.0 percent void area:

| Index | Value | Basis |
|---|---|---|
| Cp | 1.84 | within-run sigma (moving-range estimate) |
| Cpk | 1.42 | within-run sigma |
| Pp | 1.72 | overall sample sigma |
| Ppk | 1.34 | overall sample sigma |

Both Cpk (1.42) and Ppk (1.34) clear the common 1.33 capability bar. The process mean sits at 9.69 percent, well inside the 0-25 percent band, and both indices are numerically driven by the lower side (Cpl/Ppl) rather than by the upper limit, an artifact of the mean being much closer, in sigma units, to the LSL = 0 floor than to the USL = 25 ceiling. This is not a real defect risk: void fraction cannot physically go below zero, so the binding lower constraint is a mathematical feature of the index, not a sign the line is at risk of underfilling.

Bottom line: voiding today is comfortably inside its acceptance limit and the process is capable and stable at the current sample.

## 4. What should change next

- Improve gage repeatability. Since percent GRR (28.08 percent) and NDC (4.82) are both marginal, and nearly all the error is repeatability rather than operator disagreement, the next step is to look at the X-ray tester's repeatability (fixture, exposure settings, image-analysis threshold) rather than retraining operators, since reproducibility is already fine.
- Re-run the gage study after any repeatability fix to confirm percent GRR drops into the good band (under 10 percent, ideally) and NDC clears 5, before relying on this gage for tighter, joint-level decisions.
- Hold the process on a control chart. The I-MR chart on the current 50 joints is clean; put it into routine use so any future shift or drift is caught before it threatens the limit.

## 5. Data gap: no improvement/before-after data exists

We explicitly asked the data steward for any before/after improvement comparison or control-plan data. The steward's response was outcome = refused, refusal = unroutable, and it enumerated only three data topics that exist for this project: the charter, the repeat-readings/MSA study, and the void-fraction/build-order run already covered above. There is no recorded improvement action and no before/after data for this project. Any statement about what was changed and what it achieved would be invented, so we are not making one. The conclusion of this report stops at: the process, as currently run, is capable and stable, and the gage that measures it is marginal; nothing further can be said about a change because no change was recorded in the data available.

---
All numbers in this report are computed in /workspace/trace.json, steps 1-5.
