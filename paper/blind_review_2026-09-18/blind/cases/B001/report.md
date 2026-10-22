# Wave-Solder Fillet Height — Project Status Report

**Task:** [TASK]  |  **Spec:** accepted fillet height 6.80–7.50 mm, target 7.15 mm

## 1. Baseline behaviour (60 consecutive joints)

The baseline record is a **stable but off-centre** process:

- Mean = **7.0359 mm**, median = 7.026 mm, std dev = 0.0620 mm (skewness 0.84).
- The mean sits **significantly below the 7.15 mm target** (one-sample t = −14.25, p = 9.3e-21).
- Stability: runs test p = 0.795 (no non-random pattern); I-MR individuals chart centre line 7.0359 mm, limits 6.852–7.220 mm, **0 of 60 points out of control**.
- Capability vs the 6.80–7.50 mm acceptance range: Cp = 1.90, **Cpk = 1.28**, Pp = 1.88, **Ppk = 1.27**. The process is capable but running low in the window; centring alone would lift capability toward Cp ≈ 1.90.
- Caveat: Shapiro–Wilk rejects normality for the baseline (p = 0.0026), so the normal-theory capability figures should be read with modest caution; with zero out-of-control points and all 60 readings inside spec, the practical conclusion stands.

## 2. Do the line settings account for fillet height? (2³ factorial, 2 replicates)

The designed run varied chain speed, rail angle and air pressure, each low/high, twice over (16 runs):

- **Air pressure is the only setting that matters**: effect **+0.084 mm** (high vs low), p = **0.013**.
- Chain speed (effect −0.013 mm, p = 0.651) and rail angle (effect +0.022 mm, p = 0.435) are **not significant**, nor are any interactions (all interaction p-values ≥ 0.14).
- Overall model: F = 1.99, p = 0.178, R² = 63.5% (adj. 31.6%).
- Verdict declared to the steward: `any_factor_significant = true`.

So the settings that were varied **do** account for fillet height, through one lever: air pressure. Raising air pressure raises the fillet.

## 3. Did the change on the line do anything? (before vs after windows, n = 30 each)

- Before: mean **7.0899 mm**, sd 0.1512 mm. After: mean **7.2865 mm**, sd 0.0817 mm.
- Shift of **+0.1967 mm**: Welch two-sample t = −6.27, p = 1.3e-7; Mann–Whitney p = 7.0e-7. The change **did** raise fillet height — by more than twice the air-pressure effect seen in the factorial.
- Levene's test shows the **spread also shrank** after the change (p = 0.0017).
- Capability: before Ppk = **0.64** (Cpk 0.55), with **1 of 30 joints out of spec**; after Ppk = **0.87** (Cpk 0.87), with **0 of 30 out of spec**.
- However, the after-change mean (7.287 mm) is now **above** the 7.15 mm target (one-sample t p = 4.7e-10) and Ppk 0.87 is still below the customary 1.33 goal. The change overshot the target and capability, while much improved, is not yet where it should be.

## 4. The logged (unmanipulated) variables

Regression of fillet height on the three variables logged but never varied (48 records): overall model p = 0.127, R² = 12.0% (adj. 6.0%). Only preheat zone temperature shows even a marginal association (r = 0.304, p = 0.036; model term p = 0.043); conveyor width (p = 0.217) and solder pot dwell (p = 0.750) show none. These variables explain little of the variation and are not the story here, though preheat temperature is worth monitoring.

## 5. What could not be established

- No measurement-system (gage R&R) data exists in this archive, and no residual/cross-shift batch was offered — the steward holds only the five batches released (define, baseline, design, logged variables, after-change). Measurement error is therefore **not quantified** in this report.
- The process owner holds **no recorded process fact** describing what the physical line change was (provision request returned "no process fact matching"). The statistical evidence that *a* change raised and tightened the fillet distribution is strong; linking it to a specific physical alteration relies on the DOE pointer to air pressure.

## 6. Where the project stands and what happens next

1. **The line is stable and currently producing inside spec**, running at ≈ 7.29 mm with Ppk 0.87 — better than before the change (Ppk 0.64) but short of a 1.33 goal.
2. **Re-centre on target.** Air pressure is the proven lever (+0.084 mm per low→high step). The process is running ≈ 0.14 mm above target; a modest air-pressure reduction should bring the mean back to 7.15 mm. With the current after-change spread (sd 0.082 mm), centring would raise Ppk toward ≈ 1.4.
3. **Hold the gains with an individuals control chart** on fillet height (baseline behaviour shows the chart is effective: limits ≈ mean ± 0.184 mm), and monitor preheat zone temperature as a watch item.
4. **Before the next audit**, commission a gage R&R study — none exists — and record what the line change physically was so the improvement can be standardised and replicated.

*Every figure above was computed from the steward-released batches during this run; the full computational record is in `/workspace/trace.json`.*
