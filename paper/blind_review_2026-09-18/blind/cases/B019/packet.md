# Blind item B019

Focal assessment: Stability of the first quality characteristic and subsequent actions.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the process team on a precision-turning cell. Two dimensions on the same part are followed: the outer diameter, accepted between 24.80 and 25.20 mm, and the wall thickness, accepted between 1.20 and 1.60 mm. Both are recorded five consecutive pieces at a time at twenty-five sampling points through one run, both on the same instrument, and the archive holds the study in which that instrument measured the same pieces several times over under several operators. Two further samples are on file: the diameter recorded separately for each of the four turning fixtures, and one window's paired record of coolant delivery pressure and wall thickness.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the recorded readings can carry a conclusion, how each characteristic has behaved across the run, where each sits against the range it is accepted in, which of them decides what this project does next, and what that is. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
{"msa_ndc":{"field":"ndc","op":">=","value":5.0,"source":"AIAG MSA-4 Ch. II Sec. D"},"msa_pass":{"field":"grr_pct","op":"<=","value":30.0,"source":"AIAG MSA-4 Ch. II Sec. D"}}
```

## Submitted report (complete, identifiers removed)
# Turning-cell project assessment

## Management decision

**Prioritize wall-thickness variation and investigate its dispersion signal. Maintain diameter performance rather than making fixture adjustment the main project.** The data support this prioritization, but do not establish a root cause or a successful improvement. Coolant pressure is a promising investigation variable, not yet a proven control lever.

## Can the readings support a conclusion?

The crossed instrument study was analyzed using random-effects ANOVA. The operator-by-part interaction was pooled into error because its computed p-value was 0.3882. Gage repeatability and reproducibility account for **23.88% of study variation**, and **14.72% of tolerance**, with **5 distinct categories**. This is conditional measurement adequacy, not an excellent measurement system. It permits a cautious diagnostic assessment; improve measurement technique and verify calibration, operator consistency and application-specific suitability before certifying gains.

The available repeat readings are at diameter-scale values. Use of the same instrument does not independently prove its performance on the thickness contact geometry or thickness range. That remains an explicit limitation. Neither bias nor long-term instrument drift was established by this study.

## Run behavior and acceptance performance

The ordered data were analyzed as consecutive rational subgroups using X-bar/R charts. Reported signals use the point-outside-control-limits rule, not an exhaustive suite of run-pattern tests. Normality was assessed with Anderson–Darling tests; the p-values were **0.7102 for diameter** and **0.4671 for thickness**. Neither indicates a detectable marginal departure from normality; this does not establish independence or stability.

| Computed result | Outer diameter | Wall thickness |
|---|---:|---:|
| Accepted interval, mm | 24.80–25.20 | 1.20–1.60 |
| Target, mm | 25.00 | 1.40 |
| Observations | 125 | 125 |
| Mean, mm | 25.00150 | 1.391770 |
| Within-subgroup sigma, mm | 0.040612 | 0.095684 |
| Overall sample standard deviation, mm | 0.041378 | 0.092180 |
| X-bar lower limit, mm | 24.94699 | 1.26335 |
| X-bar upper limit, mm | 25.05601 | 1.52019 |
| X-bar signals | 0 | 0 |
| Mean range, mm | 0.094464 | 0.222560 |
| Range upper limit, mm | 0.199697 | 0.470492 |
| Range signals | 0 | 1 |
| Cp | 1.6415 | 0.6967 |
| Cpk | 1.6292 | 0.6681 |
| Pp | 1.6111 | 0.7232 |
| Ppk | 1.5991 | 0.6935 |
| Observed readings outside acceptance | 0 | 6 |

Within-subgroup sigma uses mean range divided by the subgroup-size correction; overall indices use sample standard deviation. The diameter run has no detected chart-limit signals and is centered with substantial acceptance margin. Its results support maintaining the current process, subject to continued monitoring and measurement limitations.

Thickness has no subgroup-mean limit signal, but **subgroup 11 has a range of 0.474100 mm**, exceeding the range limit. Its dispersion is therefore not fully demonstrated stable. Its capability indices must be treated as **descriptive baseline estimates, not certified future capability**. Even the potential index is poor: merely recentering thickness would not solve the spread problem. Do not silently discard the flagged subgroup or recalculate favorable limits without an identified, corrected cause.

## What may be causing the problem?

### Fixture comparison is secondary

The Brown–Forsythe variance test gives p = **0.3486**. The ordinary fixture ANOVA gives F = **3.1641**, p = **0.03142**, indicating evidence of unequal diameter means, rather than evidence that every fixture pair differs. In archive order, fixture means are **24.97698, 24.99745, 25.00966 and 25.00287 mm**. These results warrant checking fixture offsets and setup repeatability during routine maintenance. They do not explain the wall-thickness shortfall; the fixture sample measured diameter. No pairwise significance claims or causal fixture claims are made.

### Pressure is an actionable hypothesis, not established causality

In the paired window, Pearson correlation is **0.7020**, p = **4.1212e-10**. The fitted relationship is:

**Thickness (mm) = 1.189992 + 0.055294 × delivery pressure (bar).**

The regression explains **49.2801%** of observed thickness variation, with adjusted explained variation **48.4056%** and residual standard deviation **0.059288 mm**, using **60 pairs**. Its model p-value is **4.1212e-10**. This supports investigating pressure delivery and regulation. It does not show that changing pressure will remove the observed variation: time, temperature, wear, material, setup or another coupled variable could confound the association. The paired window cannot automatically be equated to the full baseline run.

The process-owner question about independent pressure adjustment returned no matching process fact. Consequently, controllability and coupling remain unknown. Regression assumptions and replicated causal response have not been established; no optimum setting is prescribed.

## Next action and sustainment

- Quality should contain suspect thickness output under the plant's disposition procedure and arrange an application-specific measurement check. Avoid relying solely on borderline measured values for release.
- Process engineering should investigate the flagged sampling point using tool condition, coolant delivery, setup, material and measurement records. Preserve the original baseline and document any assignable cause.
- Establish whether pressure can safely be adjusted independently. Then plan a controlled, randomized and replicated pressure investigation, blocking known nuisance conditions and measuring both characteristics. Seek reduced thickness spread as well as appropriate centering; do not sacrifice diameter.
- After an approved change, collect a new ordered run with the same rational subgroup logic. Demonstrate dispersion and mean stability before claiming capability or improvement. Compare before/after measurement performance, capability and actual nonconformance.
- For sustainment, assign the cell owner to chart review and reaction, quality to acceptance disposition and measurement verification, and engineering to cause correction and change control. Track pressure with the dimensional records. Freeze validated control limits only after the improved baseline is established; on a signal, contain affected production, verify the gage and investigate rather than automatically adjusting the mean.

**What was changed and achieved:** no implemented intervention or verified gain is documented. A request for post-change validation re-served the original thickness baseline, not a new trial. No post-change evidence or control-plan execution data were supplied; the conclusion stops at diagnosis and the proposed investigation. The steward did not explicitly deny a named analytical batch. The missing process fact was an unroutable response, not evidence that pressure is or is not independently controllable.

All numerical findings above are rounded from computed outputs in `trace.json`. The scripts and released JSON records retain the calculation trail.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":23.877330782711752,"percentTolerance":14.719001760327423,"ndc":5.0,"interactionPValue":0.3881626345241282,"repeatVariance":8.451309401708987e-05,"operatorVariance":1.177535612536426e-05,"interactionVariance":0.0,"partVariance":0.0015926065286484402},"status":"success","decision":"Crossed random-effects ANOVA; pool interaction when p >= .05.","inputs_digest":{"batch":"msa","operators":3,"parts":10,"replicates":3}}
{"step_id":2,"method_id":"control_chart.xbar_r","outputs":{"xBarChartCenterLine":25.001499999999997,"flaggedXBarCount":0.0,"rBar":0.09446400000000053,"xbarLCL":24.946994271999998,"xbarUCL":25.056005727999995,"rLCL":0.0,"rUCL":0.19969689600000112,"flaggedRCount":0.0},"status":"success","decision":"diameter; point beyond three-sigma limits rule.","inputs_digest":{"batch":"run_diameter","groups":25,"subgroup_size":5}}
{"step_id":3,"method_id":"basic.normality","outputs":{"pValue":0.7101928709820751,"statistic":0.2587813343726708},"status":"success","decision":"diameter Anderson-Darling normality with estimated mean and variance.","inputs_digest":{}}
{"step_id":4,"method_id":"capability.normal","outputs":{"cp":1.6415424570912225,"cpk":1.629230888663067,"pp":1.6111497676198057,"ppk":1.5990661443626852,"mean":25.001499999999997,"stdDev":0.041378317526094964,"withinSigma":0.04061220980223582,"lsl":24.8,"usl":25.2,"target":25.0,"sampleSize":125.0,"outsideCount":0.0},"status":"success","decision":"diameter; within sigma Rbar/d2, overall sample SD; preliminary single-run capability.","inputs_digest":{}}
{"step_id":5,"method_id":"control_chart.xbar_r","outputs":{"xBarChartCenterLine":1.3917704,"flaggedXBarCount":0.0,"rBar":0.22256000000000004,"xbarLCL":1.26335328,"xbarUCL":1.52018752,"rLCL":0.0,"rUCL":0.47049184000000005,"flaggedRCount":1.0},"status":"success","decision":"thickness; point beyond three-sigma limits rule.","inputs_digest":{"batch":"run_thickness","groups":25,"subgroup_size":5}}
{"step_id":6,"method_id":"basic.normality","outputs":{"pValue":0.46709947065677243,"statistic":0.35017560811203907},"status":"success","decision":"thickness Anderson-Darling normality with estimated mean and variance.","inputs_digest":{}}
{"step_id":7,"method_id":"capability.normal","outputs":{"cp":0.6967409537502998,"cpk":0.6680714569853823,"pp":0.723226262306724,"ppk":0.6934669480653267,"mean":1.3917704,"stdDev":0.09217954344472216,"withinSigma":0.0956835769561479,"lsl":1.2,"usl":1.6,"target":1.4,"sampleSize":125.0,"outsideCount":6.0},"status":"success","decision":"thickness; within sigma Rbar/d2, overall sample SD; preliminary single-run capability.","inputs_digest":{}}
{"step_id":8,"method_id":"anova.equal_variances","outputs":{"pValue":0.3485506170649121,"statistic":1.1205767867463987},"status":"success","decision":"Brown-Forsythe fixture variance test.","inputs_digest":{}}
{"step_id":9,"method_id":"anova.oneway","outputs":{"factorPValue":0.03142159868435731,"fStatistic":3.1640871508843262,"fixtureMean1":24.976979999999994,"fixtureMean2":24.997453333333333,"fixtureMean3":25.00966,"fixtureMean4":25.002866666666666},"status":"success","decision":"Diameter by fixture; ordinary one-way ANOVA.","inputs_digest":{}}
{"step_id":10,"method_id":"basic.correlation","outputs":{"correlationCoefficient":0.7019980688840588,"pValue":4.121164437791441e-10},"status":"success","decision":"Pressure versus thickness observational Pearson association.","inputs_digest":{}}
{"step_id":11,"method_id":"regression.ols","outputs":{"modelPValue":4.1211644377914775e-10,"rSquaredPct":49.280128871694764,"rSquaredAdjPct":48.40564833499985,"intercept":1.1899916469446306,"slope":0.05529391003857327,"residualSD":0.059288210920480894,"sampleSize":60.0},"status":"success","decision":"Observational linear regression; not causal evidence.","inputs_digest":{}}
{"step_id":12,"method_id":"meta.data_profiling","outputs":{"maxRangeSubgroup":11.0,"maxRange":0.47409999999999997},"status":"success","decision":"Locate thickness range signal.","inputs_digest":{}}
```

## Submitted route declarations
```json
[{"point":"measurement","chosen_branch":"conditional_use","observed":{"percentStudyVariation":23.877330782711752,"percentTolerance":14.719001760327423,"ndc":5.0,"interactionPValue":0.3881626345241282,"repeatVariance":8.451309401708987e-05,"operatorVariance":1.177535612536426e-05,"interactionVariance":0.0,"partVariance":0.0015926065286484402}},{"point":"project_priority","chosen_branch":"thickness_variation_and_stability_before_optimization","observed":{"diameterCpk":1.629230888663067,"thicknessCpk":0.6680714569853823,"thicknessRangeSignals":1.0}},{"point":"causal_followup","chosen_branch":"controlled_pressure_investigation_not_fixture_led_project","observed":{"pressureCorrelation":0.7019980688840588}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
