# Blind item B020

Focal assessment: Baseline defect-rate chart stability, business performance, and next steps.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team on a chip-capacitor line. Every unit is inspected and the project has committed to holding the defect share at or below 0.25% of units inspected. On file are the inspected and defective counts for twenty-five consecutive baseline lots; a per-lot record of two line settings alongside that lot's defect share; the inspected and defective totals for one window before a change was made to the line and one window after it; the inspected and defective counts for twenty lots run since the change; and the size and risk level the before-and-after trial was run at.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the defect share held steady across the baseline, how it compares with what was committed to, whether anything on file accounts for it, whether the change that was made can be shown to have done anything, whether the level reached since is enough, and what should happen next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


## Original reporting requirements


A Markdown project report written for the plant's quality manager. Requirements:

* every number that appears in the report must be traceable to some `outputs` entry in
  `/workspace/trace.json`;
* for any step the steward `denied`, the report must state plainly that there is no data for it
  and that the conclusion stops there — do not paper over the gap with a guess;
* land the conclusions on the business: where things stand, what is causing it, what was
  changed, what the change achieved, and how it will be held.

## 6. Other constraints

* the environment has no network; every computation happens on this machine.
* the working directory is `/workspace`.
* you are free to decide your own route through the project. Whether the route was right,
  whether the numbers are accurate, and whether you reported honestly are all scored.


## Public data-service thresholds (protocol rules, not independent ground truth)
```json
{"screening_significant":{"field":"any_factor_significant","op":"==","value":true,"source":"Montgomery DAOE 6e 11.2"},"stability_pass":{"field":"stable","op":"==","value":true,"source":"AIAG SPC-2 Ch. I Sec. F; Montgomery ISQC 6e 8.1"}}
```

## Submitted report (complete, identifiers removed)
# Chip-capacitor improvement review

## Management conclusion
The recorded process was already below the committed defective-unit share at baseline. The lots since the change also support meeting that commitment. However, the before/after trial does **not** demonstrate that the intervention improved the process. Maintain monitoring and do not book a proven improvement benefit from this trial.

All shares below are fractions of inspected units, not percentages. Calculations and source batches are recorded in `trace.json`; executable calculations are retained alongside it.

## Baseline: steady and within commitment
The baseline contains 210 defective units among 100000 inspected across 25 lots. The pooled defective share is 0.0021 versus the commitment of 0.0025. A binomial p chart has center 0.0021, lower limit 0, upper limit 0.004271423, and 0 points outside its limits. This supports provisional stability under the point-limit criterion; it does not prove the absence of all special causes or serial dependence. Supplemental run-pattern rules were not tested.

Binomial capability gives process Z = 2.862736, using the normal upper-tail equivalent without a shift adjustment. The exact lower-tail test against the committed share gives p = 0.005218967. The one-sided confidence bound at confidence 0.95 is 0.002354178, below commitment. Thus the baseline average already supports compliance, assuming independent units with a common defect probability. Compliance of the average does not guarantee that every lot will meet the commitment.

## What explains variation on file?
The settings batch has 40 observations. An ordinary least-squares model of lot defect share includes paste thickness, reflow peak, and their interaction, as specified in the supplied model terms. Model p = 1.500086e-19; explained variation is 91.740852%, with adjusted explained variation 91.052590%. Interaction p = 1.462568e-11; paste-term p = 2.631542e-11 and reflow-term p = 9.462678e-10, against significance level 0.05.

These settings jointly account statistically for much of the variation in this batch. The interaction means that a setting's effect depends on the other setting; isolated main-effect coefficients should not be interpreted as universal directions of improvement. The regression is observational and uses unweighted lot shares because this batch has no inspected denominators. Its uncertainty assumes suitable independent, constant-variance errors. It is not proof of root cause, nor a basis for extrapolating an optimum.

The settings records are not linked to the baseline lots by identifiers. The owner could not supply a matching process fact about their relationship. Consequently this fit cannot be asserted to explain the baseline's particular defect level.

## What changed, and what did it achieve?
The physical intervention is not described in the released records. The process-owner question returned no matching recorded fact. We therefore cannot name the change, confirm its implementation fidelity, or attribute an effect to a specific action.

The before window has 79 defective units among 40000 inspected (share 0.001975). The after window has 91 among 40000 (share 0.002275). The after-minus-before difference is 0.000300. A two-sided pooled proportions test, without continuity correction, gives z = -0.921337 and p = 0.356874, not significant at 0.05. The normal-approximation difference interval runs from -0.000338188 to 0.000938188. Both improvement and deterioration remain compatible with the trial; there is no demonstrated benefit and no equivalence conclusion.

For the filed trial design, n = 40000 per group, alpha = 0.05, and alternatives 0.002 versus 0.0025, the two-sided normal-approximation power is 0.320321. This is low sensitivity to the design difference. A nonsignificant finding here cannot establish that the change had no effect. This is prospective design power, not power calculated from the observed difference.

## Is the level since the change enough?
The separate post-change series contains 146 defective units among 80000 inspected across 20 lots. Its pooled share is 0.001825 and binomial process Z is 2.906926. The p chart has center 0.001825, lower limit 0, upper limit 0.003849538, and 0 points outside its limits. There is no point-limit evidence of instability.

Against commitment 0.0025, the exact lower-tail test gives p = 0.00003654350. Its one-sided upper bound at confidence 0.95 is 0.002093405. These results support an adequate sustained average in the observed period, subject to the binomial assumptions. This series must not be combined with the trial windows without knowing whether their units overlap. Its lower point estimate is not itself evidence that the intervention caused improvement.

## Next actions and control
- Keep full inspection and retain lot-level inspected and defective counts, time order, material provenance, and both settings. Confirm that inspection classification is reliable; no measurement-agreement study was supplied or computed.
- Use the post-change chart as provisional ongoing reference. Recalculate sample-size-specific limits when lot size changes. Do not confuse control limits with the business commitment: a stable lot can still exceed the committed share.
- Assign the line quality owner responsibility for reviewing each lot. Investigate signals before changing limits, check measurement and materials, document containment and corrective action, and retain the original reference until a justified process change is verified.
- Obtain the intervention log and dataset linkage before claiming causality. Then use a controlled, preferably randomized and blocked confirmation trial with a pre-agreed meaningful effect, risk level, and adequate power. Account for lot clustering when planning it. No new trial size has been calculated here.
- Preserve both interacting settings in confirmation work and avoid extrapolation beyond observed operating conditions. Do not optimize from association alone.

All shop-floor batches available through the steward were released; none was denied. The missing physical-change and linkage facts stop causal attribution. The project can support current average compliance, but cannot yet close a claim of demonstrated intervention effectiveness.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"control_chart.p","inputs_digest":{"batch":"baseline"},"outputs":{"centerLine":0.0021,"outOfControlCount":0,"lowerLimit":0.0,"upperLimit":0.004271422920575354,"lots":25,"inspected":100000,"defective":210},"status":"success","decision":"Three-sigma point limits; no claim that absence of signals proves stability."}
{"step_id":2,"method_id":"capability.binomial","inputs_digest":{"batch":"baseline"},"outputs":{"avgP":0.0021,"processZ":2.862736263505904,"requiredShare":0.0025},"status":"success","decision":"Unit defective probability; Z without long-term shift."}
{"step_id":3,"method_id":"regression.ols","inputs_digest":{"batch":"settings"},"outputs":{"modelPValue":1.500085955616717e-19,"rSquaredPct":91.74085209479678,"rSquaredAdjPct":91.05258976936318,"n":40,"alpha":0.05,"interceptCoefficient":0.20920658711491874,"interceptPValue":8.640320689883481e-10,"pasteCoefficient":-0.14058444060514141,"pastePValue":2.6315416164508688e-11,"reflowCoefficient":-0.000845338179889292,"reflowPValue":9.46267808847922e-10,"interactionCoefficient":0.0005831658272310514,"interactionPValue":1.4625677522978048e-11},"status":"success","decision":"OLS on lot shares with specified interaction; observational association, not causal attribution. Main effects are at the other predictor equal to zero."}
{"step_id":4,"method_id":"basic.two_proportions","inputs_digest":{"batch":"before_after"},"outputs":{"pValue":0.3568742858820937,"zStatistic":-0.9213374282394291,"beforeShare":0.001975,"afterShare":0.002275,"beforeEvents":79,"afterEvents":91,"beforeN":40000,"afterN":40000,"afterMinusBefore":0.0002999999999999999,"differenceLower":-0.0003381875497713958,"differenceUpper":0.0009381875497713957,"alpha":0.05},"status":"success","decision":"Two-sided pooled score z test, no continuity correction; Wald interval for after minus before. No significant change."}
{"step_id":5,"method_id":"power.two_proportions","inputs_digest":{"batch":"trial_size"},"outputs":{"power":0.3203207855016455,"alpha":0.05,"nPerGroup":40000,"p1":0.002,"p2":0.0025},"status":"success","decision":"Two-sided normal approximation with pooled-null and unpooled-alternative variance; design power, not observed power."}
{"step_id":6,"method_id":"control_chart.p","inputs_digest":{"batch":"after_lots"},"outputs":{"centerLine":0.001825,"outOfControlCount":0,"lowerLimit":0.0,"upperLimit":0.0038495384890759677,"lots":20,"inspected":80000,"defective":146},"status":"success","decision":"Three-sigma point limits; no claim that absence of signals proves stability."}
{"step_id":7,"method_id":"capability.binomial","inputs_digest":{"batch":"after_lots"},"outputs":{"avgP":0.001825,"processZ":2.9069255989362413,"requiredShare":0.0025},"status":"success","decision":"Unit defective probability; Z without long-term shift."}
{"step_id":8,"method_id":"basic.one_proportion","inputs_digest":{"batch":"baseline"},"outputs":{"pValue":0.005218966633675227,"upperBound":0.002354177731888054,"confidence":0.95,"alpha":0.05},"status":"success","decision":"Exact lower-tail test against commitment and one-sided Clopper-Pearson upper confidence bound; assumes independent units with common probability."}
{"step_id":9,"method_id":"basic.one_proportion","inputs_digest":{"batch":"after_lots"},"outputs":{"pValue":3.6543497094608496e-05,"upperBound":0.00209340512012002,"confidence":0.95,"alpha":0.05},"status":"success","decision":"Exact lower-tail test against commitment and one-sided Clopper-Pearson upper confidence bound; assumes independent units with common probability."}
```

## Submitted route declarations
```json
[{"point":"baseline_stability","chosen_branch":"stable","observed":{"outOfControlCount":0}},{"point":"settings_significance","chosen_branch":"any_factor_significant","observed":{"interactionPValue":1.4625677522978048e-11}},{"point":"trial_result","chosen_branch":"no_demonstrated_change_low_power","observed":{"pValue":0.3568742858820937,"power":0.3203207855016455}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
