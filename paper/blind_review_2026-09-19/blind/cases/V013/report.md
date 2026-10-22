# Chip-Capacitor Line - Defect-Share Project Status Report

**Task:** [TASK] | **Committed defect share:** <= 0.25% of units inspected

## Headline

The line is **stable but not yet at the committed level**. The baseline held steady at
**0.546%** - more than twice the commitment. The change made on the line produced a real,
statistically proven improvement (down to **0.3375%** in the trial, **0.34375%** across the
lots run since), but the level reached is **still significantly above 0.25%**. The project is
not done: another improvement cycle is needed.

## 1. Did the defect share hold steady across the baseline? Yes.

- 25 baseline lots, 4,000 units each (100,000 units, 546 defectives): p-chart center line
  **0.5460%**, with **0 of 25** lots outside the 3-sigma limits (trace step 1).
- Overdispersion check (Laney p'): **sigmaZ = 0.9569** (trace step 2), so the plain p-chart is
  appropriate and the "stable" verdict stands. Declared to the steward: `stable = true`.

## 2. How does the baseline compare with the commitment? Well above it.

- Exact one-proportion test of the baseline total (546 / 100,000) against 0.25%:
  **p = 4.2e-59** (trace step 3). The baseline defect share is significantly **above** the
  committed share, not just noisy around it.
- Binomial capability at baseline: **avgP = 0.00546, processZ = 2.5452** (trace step 4).

## 3. Does anything on file account for it? Yes - the two line settings.

- OLS regression of per-lot defect share on paste_thickness, reflow_peak and their
  interaction (40 lots): model **p = 1.2e-06**, **R-sq = 56.4%**, **adj R-sq = 52.8%**
  (trace step 5). All three terms are significant: paste_thickness **p = 1.6e-05**,
  reflow_peak **p = 3.6e-05**, interaction **p = 1.2e-05**.
- Declared to the steward: `any_factor_significant = true`. The lot-to-lot level is driven by
  the settings, which is also the lever for further improvement.

## 4. Can the change be shown to have done anything? Yes.

- Before/after totals (40,000 units each side): **237/40,000 = 0.5925%** before vs
  **135/40,000 = 0.3375%** after. Two-proportions z-test: **z = 5.30, p = 1.15e-07** - a
  **43.0%** relative reduction (trace step 6).
- The trial was run at alpha = 0.05 with 40,000 units per group; computed power for the
  design effect (0.0059 vs 0.0025) is **1.0** (trace step 7), so the significant result is
  trustworthy.
- **What was physically changed is not on file.** The process owner holds no process fact
  describing it (provision request refused as unroutable; 1 of 26 provision turns spent).
  We can quantify the effect but cannot name the intervention from the data held here.

## 5. Is the level reached since the change enough? No.

- 20 lots run since the change (80,000 units, 275 defectives): p-chart center line
  **0.34375%**, **0 of 20** lots out of control - the new level is stable (trace step 8).
- Exact one-proportion test against the committed 0.25%: **p = 2.85e-07** (trace step 9).
  The current level is still significantly above target - **37.5%** over it, a gap of
  **0.0009375** share points.
- Post-change binomial capability: **avgP = 0.0034375, processZ = 2.7028**, improved from
  2.5452 but still short (trace step 10).

## 6. What should happen next

1. **Keep the change in place and hold it** with the p-chart now running at CL = 0.34375%;
   the process is stable at this level.
2. **Run one more improvement cycle on the two settings.** The regression shows paste
   thickness, reflow peak and their interaction drive the defect share (adj R-sq = 52.8%),
   so a designed experiment over those two factors is the direct route to closing the
   remaining 0.0009375 share points (0.09375 percentage points).
3. **Record the change that was made** in the process documentation - its identity could not
   be recovered from the data held in this environment.
4. **Re-verify against 0.25%** after the next change with the same two-proportions /
   one-proportion tests used here.

*Every figure above comes from a computation run on this task; the corresponding entries are
in /workspace/trace.json. Where data did not exist (the identity of the change), that is
stated plainly rather than guessed.*
