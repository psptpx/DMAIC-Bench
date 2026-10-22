# Project status: observed acceptance, unstable process

## Executive conclusion and scope
The released records concern **X-ray joint void fraction**, not cylinder-bore roughness. Their charter specifies an upper acceptance limit of **25% void area**, with a lower physical bound of **0%**. The steward could not clarify this mismatch. These results must not be relabelled as roughness results or used to release honed bores. Obtain the correct honing archive before making that business decision.

For the actual voiding data, all **50** recorded joints are within the released limits, but the process is **not holding steady**. Measurement precision supports conditional diagnostic use, not an unqualified measurement-system endorsement. The project is at baseline investigation, not verified improvement or closure.

## Can the readings support conclusions?
The crossed study contains **108** readings: **12** parts, **3** operators and **3** repeats. A balanced random-effects ANOVA was used. The operator-by-part interaction had p = **0.93741**, so it was pooled into repeatability; negative variance components were constrained to zero.

- Total gage R&R: **18.612%** of study variation and **13.650%** of tolerance.
- Distinct categories: **7**.
- Repeatability variance: **0.28877**; operator variance: **0.03470**; part variance: **9.01420**, in squared percentage-point units.

This is a conditionally useful measurement system, not a negligible contributor. Repeatability dominates the measurement variance. Use it to investigate the substantial run-level movement, but improve fixturing, image acquisition, region selection and analysis standardization before relying on fine distinctions or borderline acceptance decisions. Verify calibration, bias and linearity separately: repeated readings alone do not establish accuracy. Part representativeness and measurement-study randomization are not documented.

## What happened across the run?
An individuals/moving-range chart is appropriate to the supplied single observations in build order. Pooled retrospective estimates give:

| Statistic | Result, percentage-point units unless noted |
|---|---:|
| Individuals center | 11.8282 |
| Individuals lower limit | 7.1338 |
| Individuals upper limit | 16.5226 |
| Individuals outside limits | 5 |
| Mean moving range | 1.7651 |
| Moving-range upper limit | 5.7666 |
| Moving ranges outside limits | 2 |
| Longest same-side sequence | 25 |

These chart limits are screening limits, not specifications or a validated control baseline. Both dispersion excursions and sustained level differences require investigation. A median runs test gives p = **0.000004822**, corroborating nonrandom ordering.

An exploratory equal-half comparison shows the first **25** observations averaging **9.1768%**, versus **14.4796%** for the remaining half: an increase of **5.3028 percentage points**. This split describes the observed pattern; it is not a documented change point or proof of any causal intervention.

The pooled standard deviation is **3.0870**, and the median is **11.235%**. Anderson–Darling normality gives statistic **0.90466**, p = **0.01950**. A normal distribution is questionable, but fitting a nonnormal distribution would not repair the more fundamental lack of stability. No normal or nonnormal predictive capability index is asserted.

## Where voiding sits against acceptance today
In the released run, **0** readings were out of specification, an observed reject rate of **0%**. Values ranged from **6.31%** to **17.70%**, leaving minimum recorded headroom of **7.30 percentage points** below the upper limit. The latest half has a higher average despite remaining below that limit.

Observed conformance does not guarantee future conformance. A nominal one-sided binomial upper confidence bound for the reject percentage is **5.8155%** at **95%** confidence, but it assumes independent observations with constant failure probability. The run's shift undermines that assumption; the bound is illustrative uncertainty, not a validated forecast. There are no dates establishing that this archive describes current production.

## Cause, changes and achieved benefit
No causal process facts were supplied. A request for cause records only re-served the ordered readings. The owner had no recorded facts about the apparent mid-run event. A request for post-improvement validation and control-plan records was unroutable; no such data were released. These were not affirmative steward `denied` responses, but the evidentiary gap is real: **there is no supplied cause, intervention, post-change verification or hold-the-gain dataset**. No change is documented and no improvement benefit can be computed. Conclusions stop at measurement precision, baseline instability and observed acceptance.

Investigate traceability around the level change: equipment and recipe logs, materials, lot or shift boundaries, maintenance, inspection setup, and operator changes. These are candidate explanations, not established causes. Recheck retained joints with controlled measurement conditions to distinguish actual process movement from inspection movement.

## Next actions and holding plan
- Quality manager: resolve the process/data identity mismatch and obtain the roughness archive if honing remains the actual project scope.
- Metrology lead: standardize imaging and analysis, verify reference accuracy and repeat the measurement study after any measurement-system changes.
- Process engineer: join production history to build order, investigate the shift, and confirm suspected drivers with a planned controlled comparison. Do not optimize against an undocumented mixture of operating conditions.
- Production quality: maintain acceptance inspection and traceability while investigating. Escalate excursions and sustained drift; segregate suspect material pending review rather than using control limits as acceptance limits.
- After an identified corrective action, collect a fresh ordered validation run, demonstrate stability and reassess the distribution before capability analysis. Use a bounded or suitably justified nonnormal model only if warranted by stable data.
- Establish control limits from that verified stable phase, document the reaction plan, assign ownership and audit adherence. Do not silently recenter limits to absorb deterioration.

## Audit trail
`trace.json` contains the computed results and routing decisions; `analyze.py` contains the calculations. Complete released batches are retained in `data/`. Report numbers are rounded from trace outputs. No predictive capability, causal effect or improvement outcome has been fabricated.
