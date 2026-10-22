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
