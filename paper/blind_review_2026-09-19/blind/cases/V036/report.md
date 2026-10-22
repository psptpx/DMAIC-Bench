# Coating thickness project — measurement gate not passed

## Management conclusion
The archived readings do **not support a defensible process acceptance or improvement conclusion**. The immediate priority is the measurement system, not applicator adjustment. The charter specifies acceptance from **180 to 260 µm**, target **220 µm**, giving a computed tolerance width of **80 µm**.

## What was established
A balanced crossed gauge study contains **90 readings**, covering **10 parts**, **3 operators**, and **3 repeats per operator–part combination. I fitted a crossed random-effects variance-components model. The operator–part interaction was not significant (p = **0.5001**) and was pooled into repeatability error; negative variance estimates were constrained to zero.

| Measurement result | Computed value |
|---|---:|
| Gauge R&R, percent of total study variation | 44.34% |
| Gauge R&R, percent of tolerance | 63.70% |
| Distinct categories (truncated discrimination estimate) | 2 |
| Gauge standard deviation | 8.494 µm |
| Pooled repeatability variance | 72.143 µm² |
| Operator variance estimate | 0 µm² |
| Retained interaction variance estimate | 0 µm² |
| Part-to-part variance estimate | 294.801 µm² |

Study variation uses the ratio of gauge standard deviation to combined gauge and part standard deviation; tolerance usage uses the full study spread relative to tolerance. Discrimination is based on the part-to-gauge standard deviation ratio. These calculations are reproducible in `analyze.py` from the released JSON.

Measurement error is large relative both to observed part variation and to tolerance. The computed verdict was declared to the steward, which rejected the measurement acceptance gate. Repeatability dominates the estimated measurement error; the fitted operator component at zero does not prove operators are interchangeable or that calibration bias is absent. This study does not independently establish accuracy, linearity or long-term gauge stability.

## Where the process conclusion stops
The run-order readings were **locked** by the failed measurement gate. Applicator samples and the monitoring record were also **locked** behind the run-order prerequisite. These are access restrictions, not evidence that the records do not exist. No downstream request was denied as genuinely nonexistent.

Consequently, run stability, time trends, process centering, capability, reject rate and applicator differences **could not be computed**. Neither a particular applicator nor a process setting can be identified as the cause. No completed change or sustained improvement can be verified. A request for a replacement measurement study was unroutable, and the process owner had no matching remediation fact. There is no released replacement evidence on which to continue.

## What specifically should change next
- **Quality/metrology owner:** inspect gauge calibration against traceable standards, resolution, probe contact and alignment, fixture repeatability, surface preparation, measurement location and environmental sensitivity. Standardize the measurement method and train operators. Treat these as hypotheses to check, not established physical causes.
- **Production and quality:** protect disposition decisions near the acceptance boundaries with an independently validated measurement method; do not tune applicators on the basis of noisy readings alone. Document any containment and remeasurement decisions.
- **Metrology:** after documented corrective action, repeat a randomized, blinded crossed study using representative parts and operators. Recheck repeatability, reproducibility, discrimination and tolerance usage, and separately check bias and stability. Resume downstream analysis only after the measurement acceptance gate passes.
- **Process engineering:** then obtain chronological rational subgroups, assess spread and mean stability before interpreting capability, and investigate special causes against event records. Evaluate distributional suitability and centering against target. Compare applicators with assumptions checked and avoid treating an observational difference as proof of causation.
- **Control owner:** following a verified process correction, retain timestamped monitoring, calibrated gauge checks, approved control limits, an escalation and containment reaction plan, and a named owner for review. Quantify before/after performance on validated measurements before claiming an achievement.

**Current disposition:** measurement-system remediation required; process diagnosis, improvement benefit and sustainment remain unverified. Recommended actions above are prospective, not changes claimed to have happened.
