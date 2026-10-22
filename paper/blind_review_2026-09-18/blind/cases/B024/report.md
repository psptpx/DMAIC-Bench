# Brightness improvement — baseline assessment

## Executive decision
The recorded measurements support conditional process investigation, but neither an unqualified measurement-system approval nor stable long-term capability has been demonstrated. All released production readings meet the accepted range. A moving-range alarm and a strongly skewed distribution mean that observed conformance is not assurance of future conformance. This project remains at baseline assessment, not verified improvement or control closure.

## Can the readings be relied on?
The crossed study contains 90 readings across 10 parts, 3 operators and 3 repeats. Random-effects ANOVA gave an interaction p-value of 0.8084; the nonsignificant interaction was pooled into repeatability. Negative variance components would have been truncated at zero.

Gage R&R is 12.67% of study variation and 13.61% of tolerance, with 11 distinct categories. This is a conditionally usable, rather than excellent, measurement system. Repeatability variance (19.249) dominates operator variance (1.329). Improve fixturing, optical alignment, warm-up and reading procedure before treating marginal units as confidently classified. These are investigation targets, not proven causes. This study assesses precision, not calibration bias, linearity, long-term drift or spatial patchiness.

## How the line behaved
The 50 chronological readings average 429.884 cd/m², with median 420.75, sample standard deviation 39.884 and skewness 1.211. The observed span is 374.2 to 544.2 cd/m².

An individuals chart using successive moving ranges has center 429.884, lower limit 306.659 and upper limit 553.109 cd/m². There are 0 individual beyond-limit signals. The moving-range mean is 46.333 and upper limit is 151.369; there is 1 beyond-limit moving range. The largest jump, 167.6, occurs from unit 20 (376.6) to unit 21 (544.2). Unit positions here are counted from the start of the released run.

Investigate that transition and retain it in the baseline unless a documented assignable cause justifies a separate phase. These are conventional beyond-limit tests, not an exhaustive run-rule analysis. Skewness also makes normal-theory alarm rates approximate. Absence of individual alarms does not establish stability when the moving-range chart signals.

## Brightness against acceptance today
The accepted range is 350–550 cd/m². There are 0 observations below and 0 above it: observed conformance is 100%. Even with no observed failures, the one-sided 95% exact binomial upper bound for the defect fraction is 5.82%, conditional on independent representative sampling. The process signal weakens that assumption.

Anderson–Darling normality gives statistic 1.8276 and p-value 9.69242e-05. A normal capability model is not supported. As a descriptive alternative only, empirical percentile performance gives Pp 1.187 and Ppk 1.058, using lower and upper tail probabilities of 0.00135 from each end and linear sample quantiles 374.359 and 542.897. The lower-side median margin is limiting. These extreme sample quantiles are poorly determined by this small run: the indices are not validated population capability or evidence of predicted yield. Stable predictive capability cannot yet be computed defensibly. The archive is the available baseline; its applicability to present-day unchanged production was not confirmed.

## Causes, changes and next actions
No causal factor records, documented intervention, experiment or post-change confirmation batch were released. Requests for downstream data and process-history clarification were unroutable; this is not a steward finding that a named batch definitively does not exist. There are no recorded process facts available to confirm operating changes. Consequently, no root cause, actual change, achieved improvement or sustained benefit can be claimed from this task.

The quality engineer should review the flagged transition against lot, station, material, recipe, warm-up and maintenance history. The metrology owner should verify calibration against a reference and standardize the reading method, then repeat the crossed study after any measurement change. Manufacturing should collect a longer chronological baseline with those contextual factors and with a measure of within-panel uniformity: a scalar brightness reading alone does not resolve the patchiness complaint.

After confirming the measurement method and separating any justified process phases, investigate candidate factors through a controlled experiment rather than shifting the brightness setpoint on this evidence alone. Verify the chosen change on independent production, reassess distribution and capability, and compare conformance with the baseline.

## Holding a verified improvement
Assign manufacturing responsibility for chronological brightness and moving-range monitoring and quality responsibility for specification disposition. Treat control limits and acceptance limits separately. Use current limits only as provisional investigation thresholds; establish a fresh baseline after verified stabilization rather than continually widening limits. On a signal, check the measurement system, contain suspect production, document the assignable cause and verify restart. Preserve calibration and fixture checks, traceable reaction records, and periodic measurement-study review. Control closure requires post-change records that are not available here.

## Audit trail
The accompanying trace records the computations and route decisions. The local analysis script reproduces results from the steward JSON batches. Rounded figures above are taken directly from trace outputs; recommendations are prospective, not reported interventions.
