# Brightness line review

## Executive conclusion

The brightness record can be used for directional process decisions, but the measurement system is only marginal rather than strong. Crossed gage R&R was **15.276% of study variation**, **15.373% of tolerance**, and **ndc was 9**. Operator reproducibility variance was **9.414**, compared with repeatability variance of **16.844**, so standardization and operator follow-up remain warranted.

The line did not hold one steady level over the released run. The best least-squares split puts the start of the current regime at production position **26** (source index **25**), after **25** observations in the earlier regime. The current segment is stable under the basic Individuals–Moving Range beyond-limit rule, but it is centered too close to the upper specification. Its mean is **523.740**, while the accepted limits are **350.000** and **550.000**. Current **Cpk is 0.484** and **Ppk is 0.493**; **2** of the current **25** readings were above the upper limit.

No process facts are recorded that identify an intentional change, its cause, or its owner. The upward shift therefore must be treated as an unexplained special cause, not claimed as a verified improvement.

## Measurement reliability

The crossed study used **90** readings from **3** operators, **10** parts, and **3** replicates. Gage standard deviation was **5.124**. Gage R&R consumed **15.276%** of total study variation and **15.373%** of the specification tolerance; **ndc was 9**. The operator effect had p-value **0.001215**, while operator-by-part interaction had p-value **0.160203**.

Conclusion: the system distinguishes multiple part categories, but measurement error is material. Keep using it with caution for this investigation; standardize setup and reading practice, check calibration, retrain operators, and repeat the crossed study before relying on small shifts.

## Behavior over the run

Across all **50** units, mean brightness was **486.826**, standard deviation was **43.052**, and the observed range was **401.600** to **556.900**. The whole-run Anderson–Darling p-value was **0.023433**, so one normal-population interpretation is not supported.

The whole-run I-MR center line was **486.826**, with limits **412.694** and **560.958**; **2** points were beyond those limits, at positions **14** and **23**. The runs test found only **6** runs and p-value **0.00000001094**, showing strong non-random sequence structure. Brightness correlated with production order at **0.751**, with p-value **0.000000000346** and fitted slope **2.217** per unit. These diagnostics establish instability; whole-run capability values are not decision-grade.

The least-squares split starts the later regime at position **26**. Mean brightness rose from **449.912** to **523.740**, a computed increase of **73.828**. The Welch comparison gave t-statistic **-12.006**, p-value **0.000000000000002357**, and an interval for the increase from **61.429** to **86.227**. This is an observed shift, not proof of a known intervention or mechanism.

## Where brightness sits today

The latest regime contains **25** observations. Its Anderson–Darling p-value was **0.431300**, and its basic I-MR chart had center line **523.740**, limits **469.474** and **578.006**, and **0** beyond-limit points. This supports using the segment for a provisional current capability estimate, although the short run and unexplained transition limit confidence.

Current **Cp is 1.843** but **Cpk is 0.484**; **Pp is 1.877** but **Ppk is 0.493**. The large gap between potential spread and one-sided capability shows a centering problem, not primarily excessive within-regime spread. Of the latest **25** readings, **23** were inside specification and **2** were above **550.000**. None were below the lower limit.

The earlier regime had mean **449.912**, **Cpk 1.093**, **Ppk 1.327**, and all **25** readings inside specification. The later regime reduced standard deviation from **25.102** to **17.754**, but the unverified upward shift moved the center dangerously close to the upper boundary and produced the observed high-side failures. It must not be described as a successful change.

## Actions now

- Contain current output and review the **2** high-side units against the accepted upper limit.
- Trace the transition beginning at position **26** through machine settings, material lots, recipes, maintenance, calibration, and operator records. No released fact currently identifies the cause, so the causal conclusion stops here.
- Re-center brightness away from the upper boundary while retaining the lower recent variation. Verify the adjustment with a fresh ordered run before releasing normal production.
- Improve the measurement process by standardizing fixture/setup and operator technique, confirming calibration, and repeating the crossed gage study. Focus first on operator reproducibility because its effect was detected at p-value **0.001215**.
- Hold the gain with an I-MR chart built only after the new center is verified; maintain reaction rules for limit signals and specification breaches. Recalculate capability only from a stable regime rather than combining both levels.

## Evidence limitations

The steward released the charter, measurement study, and ordered production run. A process-owner query returned no matching recorded process fact. Consequently, what changed physically, whether anyone intended the shift, and what any intervention achieved **could not be computed or verified**. There is also no post-corrective-action batch, so sustained improvement cannot yet be demonstrated.
