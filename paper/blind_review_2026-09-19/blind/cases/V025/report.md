# Coating thickness project status

## Executive conclusion

The readings can carry a process conclusion. The crossed gage study produced **12.27% study variation**, **11.35% of tolerance**, and **11 distinct categories**. The gauge can distinguish meaningful piece-to-piece differences, although measurement variation is large enough that repeatability should still be improved.

The original run was **stable but wholly unacceptable**. Its mean was **291.34 um**, or **71.34 um above the 220.00 um target**. All **125 of 125 readings** were above the **260.00 um upper limit**, so the observed nonconforming rate was **100.00%**. Stability did not imply conformance.

The monitoring record after the undocumented change is materially better. Its mean is **219.25 um**, **0.75 um below target**; **0 of 20 readings** were outside the accepted **180.00–260.00 um** range. The available evidence supports retaining the new condition, while continuing monitoring because the post-change record is still limited.

## Measurement system

The crossed study used **90 readings** from **3 operators**, **10 parts**, and **3 replicates**. Total gage variance was **2.2898**, comprising repeatability variance **1.8156**, operator-by-part variance **0.4656**, and operator variance **0.0086**. The operator test had **p = 0.3605**. Measurement error is therefore driven mainly by repeatability and interaction rather than a persistent operator offset.

Decision: use the readings for process and applicator conclusions, but standardize gauge placement and handling and verify repeatability in a follow-up study.

## Baseline behavior and capability

The baseline median was **291.13 um**, standard deviation **7.74 um**, minimum **272.04 um**, and maximum **311.40 um**. Anderson-Darling normality testing gave **p = 0.5967**, so this sample did not show evidence against a normal capability model.

For the **25 subgroups** of **5 pieces**, the X-bar center line was **291.34 um**, with limits **281.23 um** and **301.45 um**. The average range was **17.53 um**, with an upper range limit of **37.05 um**. There were **0 X-bar flags** and **0 range flags** under the point-limit screen. Thus, the line held a consistent but badly over-applied condition throughout the sampled run.

The within estimates were **Cp = 1.769** and **Cpk = -1.386**; overall estimates were **Pp = 1.722** and **Ppk = -1.349**. The apparently wide potential spread is irrelevant while the center lies beyond the upper specification: the negative one-sided indices correctly identify the baseline as incapable.

## Applicator analysis and cause status

The applicator means were **291.55 um** for nozzle A, **290.77 um** for nozzle B, **294.06 um** for nozzle C, and **290.91 um** for nozzle D. The total spread among those means was only **3.29 um**. Equal-variance testing gave **p = 0.3094**; the one-way applicator ANOVA gave **F = 1.8652** and **p = 0.1460**.

These data do **not** establish one nozzle as the cause. All applicators shared the high condition, so the evidence points operationally toward a common coating-delivery setpoint, calibration, pressure, viscosity, speed, or recipe issue. The dataset cannot distinguish among those common causes; a causal claim would require process-factor records or a controlled trial.

## What changed and what it achieved

The specific intervention is **not recorded in the released data**, and the process-owner query returned no matching process fact. Therefore this report cannot honestly say what physical adjustment produced the result or attribute causality to a named action.

What the observations do establish is a pre/post mean shift of **-72.09 um**, a reduction in absolute target offset of **70.59 um**, and a standard-deviation change of **-2.66 um**. The observed outside-specification rate changed from **100.00%** to **0.00%**, a change of **-100.00 percentage points**.

For the **20 post-change individuals**, standard deviation was **5.08 um**. The I-chart center was **219.25 um**, with limits **201.08 um** and **237.42 um**. There were **0 individual flags** and **0 moving-range flags**. Estimated post-change capability was **Cp = 2.202**, **Cpk = 2.160**, **Pp = 2.625**, and **Ppk = 2.575**. These estimates describe the available record and should not replace continued control-chart evidence.

## Required next actions and control

- Preserve the current machine condition immediately and document the actual recipe, common delivery settings, material condition, line speed, and gauge setup. The missing intervention record is the main traceability gap.
- Center the common coating system on the **220.00 um target** rather than tuning individual nozzles without evidence. Verify all nozzles after any common adjustment.
- Continue an individuals/moving-range chart at the present sampling cadence. Treat the current estimated limits as provisional: investigate any point beyond **201.08–237.42 um** or any moving range above **22.32 um**, then recalculate limits after a longer stable record; quarantine affected production until the assignable cause is resolved and a fresh in-range reading confirms recovery.
- Keep specification disposition separate from chart response: any piece outside **180.00–260.00 um** is nonconforming even if the chart has no signal.
- Improve gauge repeatability through a fixed measurement location, seating method, surface preparation, and operator work instruction, then repeat the crossed study.
- Recalculate capability only after enough additional monitoring confirms that the new center and variation persist. Do not identify nozzle C or any other individual applicator as root cause from the present ANOVA.
