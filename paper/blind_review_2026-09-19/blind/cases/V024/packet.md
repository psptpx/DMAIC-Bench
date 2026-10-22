# Blind item V024

Focal assessment: Whether readings can support substantive analysis after the measurement system study.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the process team on a honing line that finishes cylinder bores. Assembly has returned units for bore finish, and the accepted band for roughness is 0.40 to 1.60 um Ra with 1.00 as the target. The line records a roughness reading for every bore in the order it is finished, and the archive holds the study in which the same bores were measured several times over by several operators on the roughness tester.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the recorded readings can carry a conclusion at all, how the line has behaved across the run, where voiding sits against its acceptance limit today, and what should change next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
{}
```

## Submitted report (complete, identifiers removed)
# Quality-manager project assessment

## Executive conclusion and scope
The released archive concerns **X-ray joint void area**, not bore roughness. Its acceptance ceiling is **25 percent void area**, with a physical lower bound of **0**. The owner could not resolve the mismatch. Consequently, this report supports only a conditional voiding assessment: it cannot certify bore finish or the roughness tester. Reconcile the project identity and obtain the actual honing records before dispositioning bores.

Current void readings are below the ceiling and show no detected basic control-chart signals. The measurement system is usable cautiously for process investigation, but is not excellent. No implemented improvement or sustained post-change benefit has been demonstrated.

## Can the readings support a conclusion?
The crossed study contains **108** measurements. Full random-effects crossed ANOVA, retaining the interaction and truncating negative variance components, gives gage R&R **20.11% of study variation**, **18.41% of tolerance**, and **6** distinct categories. Interaction evidence is weak (p = **0.5753**). Repeatability variance is **0.3974** and operator variance **0.1911** in squared percentage-point units.

These results support conditional process comparisons, not an unqualified measurement-system approval. Standardize operator positioning and image interpretation, check calibration and bias against reference joints, and repeat the study after training. R&R alone does not establish accuracy or long-term measurement stability.

## Behavior across the recorded run
The **50** ordered observations average **8.3648 percent**, with median **7.69**, sample standard deviation **2.7749**, and range **4.17–15.28 percent**. An individuals/moving-range chart uses successive observations rather than artificial subgroups. Its individual limits are **-0.4834** and **17.2130**, around **8.3648**. The negative calculated lower limit is not a physically attainable void fraction. The moving-range upper limit is **10.8691**. There are **0** individual-limit and **0** moving-range-limit signals. The median runs-test p-value is **0.3913**.

This is a provisional baseline with no detected instability under these tests, not proof that all shifts or autocorrelation are absent. There are no timestamps, strata, or process settings linking this sequence to particular operating conditions.

## Where voiding sits today
There are **0** observed ceiling exceedances among **50** joints. Under independent sampling, the one-sided exact upper confidence bound on the exceedance fraction is **0.058155**. Absence of observed failures is not a guarantee of negligible future risk.

Raw normality is questionable (Anderson–Darling p = **0.02857**; skewness **0.71546**). Normal capability calculations were retained in the trace only as reference calculations and should not be used to sign off this process.

A positive lognormal model is more defensible as an exploratory description: log-scale normality p = **0.57685**. With fixed zero location, percentile capability gives Pp **1.4011** and Ppk **1.3199**; the upper-only index relevant to the acceptance ceiling is **1.3199**. Its extrapolated fraction above the ceiling is **0.000184**. These are fitted-model estimates, not validated field failure rates. The small baseline cannot establish the remote tail; collect a larger representative run before using this projection for acceptance commitments.

## Causes, changes, and next actions
The archive supplies no linked causal factors. The repeated study identifies operator and repeatability contributions to measurement error, not the manufacturing cause of voids. Requests for causal records returned the existing run; improvement-trial and control-plan requests were unroutable. No request was explicitly denied, but no trial, implemented change, or post-change data were supplied. The causal and improvement conclusions stop here: neither a root cause nor an achieved improvement can be claimed.

First resolve scope with the data owner. For the voiding project, preserve ordered readings and add lot, equipment, recipe, operator, material, and maintenance context. Investigate credible mechanisms with the process team and test proposed changes in a designed trial before changing the standard recipe. Compare representative baseline and post-change distributions using the same validated measurement method; do not confuse a measurement change with a process improvement.

## Proposed sustainment, not an existing control plan
Assign quality ownership for measurement checks and production ownership for response to chart signals. Continue ordered individual and moving-range monitoring using the provisional baseline; investigate unusual patterns and contain affected product when acceptance is uncertain. Keep specification decisions separate from control limits. Record causes, corrective actions, and subsequent verification. Recalculate limits only after a documented, validated process change, and audit calibration, operator agreement, and acceptance performance. Obtain actual control-plan and post-change records before closing the project.

## Audit trail
The companion trace records every quantitative analysis run, including the rejected normal-reference capability calculation. Scripts and released JSON batches remain in the workspace for reproduction. All numerical results above are rounded from trace outputs.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":20.108053146463117,"percentTolerance":18.410360402400133,"ndc":6,"repeatabilityVariance":0.39736585898148147,"operatorVariance":0.19107401974466928,"interactionVariance":0,"partVariance":13.964879106097085,"interactionPValue":0.5752918525715551,"n":108},"status":"success","decision":"Full crossed random-effects ANOVA; negative variance components truncated at zero.","inputs_digest":{"batch":"msa","operators":3,"parts":12,"replicates":3}}
{"step_id":2,"method_id":"meta.data_profiling","outputs":{"lsl":0.0,"usl":25.0},"status":"success","decision":"Released charter is percent void area, not roughness.","inputs_digest":{}}
{"step_id":3,"method_id":"basic.descriptive_summary","outputs":{"mean":8.3648,"median":7.6899999999999995,"stdDev":2.7749030062107667,"skewness":0.715459086593583,"adPValue":0.028572851060577234,"n":50,"min":4.17,"max":15.28},"status":"success","decision":"Summary of ordered void area percentages.","inputs_digest":{"batch":"process_run","n":50}}
{"step_id":4,"method_id":"basic.normality","outputs":{"statistic":0.8383933741037524,"pValue":0.028572851060577234},"status":"success","decision":"Anderson-Darling normality test with fitted mean and variance.","inputs_digest":{}}
{"step_id":5,"method_id":"control_chart.imr","outputs":{"centerLine":8.3648,"individualsLCL":-0.48344142422926595,"individualsUCL":17.213041424229267,"flaggedCount":0,"movingRangeMean":3.326938775510204,"movingRangeUCL":10.869108979591836,"flaggedMovingRanges":0,"withinSigma":2.949413808076422},"status":"success","decision":"Individual values with adjacent moving ranges; flags count beyond three-sigma limits only.","inputs_digest":{}}
{"step_id":6,"method_id":"nonparametric.runs_test","outputs":{"pValue":0.3912672792826394,"zStatistic":0.8573214099741123},"status":"success","decision":"Median runs test for sequence randomness.","inputs_digest":{}}
{"step_id":7,"method_id":"capability.normal","outputs":{"cp":1.4127100969206232,"cpk":0.9453629934977303,"pp":1.5015539848927568,"ppk":1.0048159018264746,"upperPpk":1.9982920679590388,"upperCpk":1.8800572003435159},"status":"success","decision":"Normal reference indices, not validated if normality is rejected. Lower boundary is physical zero; upper-only indices are operationally relevant.","inputs_digest":{}}
{"step_id":8,"method_id":"capability.binomial","outputs":{"avgP":0.0,"exceedances":0,"n":50,"upper95DefectFraction":0.05815507911697225},"status":"success","decision":"Observed upper-limit exceedance fraction and one-sided exact binomial upper confidence bound; independent observations assumed. Continuous void area is not binomial data; only acceptance indicators are used.","inputs_digest":{}}
{"step_id":9,"method_id":"basic.normality","outputs":{"statistic":0.29729841646859967,"pValue":0.576848713747224},"status":"success","decision":"Anderson-Darling test on log void fraction; check for lognormal model.","inputs_digest":{}}
{"step_id":10,"method_id":"capability.nonnormal","outputs":{"pp":1.4010695744994526,"ppk":1.3199241083134954,"upperPpk":1.3199241083134954,"logMean":2.071906132722402,"logSigma":0.3220576795570461,"lowerQuantile":3.0214610437747003,"median":7.939943288461594,"upperQuantile":20.864971783726013,"predictedUpperDefectFraction":0.00018445554325994748},"status":"success","decision":"Lognormal MLE with fixed zero location. Percentile-based indices, exploratory tail extrapolation; zero is physical lower bound.","inputs_digest":{"batch":"process_run","n":50}}
```

## Submitted route declarations
```json
[{"point":"scope","chosen_branch":"Analyze released void-area data only; roughness unresolved"},{"point":"measurement","chosen_branch":"Conditional usability; improve operator consistency","observed":{"percentStudyVariation":20.108053146463117,"percentTolerance":18.410360402400133,"ndc":6,"repeatabilityVariance":0.39736585898148147,"operatorVariance":0.19107401974466928,"interactionVariance":0,"partVariance":13.964879106097085,"interactionPValue":0.5752918525715551,"n":108}},{"point":"stability","chosen_branch":"No detected basic chart signals; provisional stable baseline"},{"point":"distribution","chosen_branch":"Lognormal rather than normal capability","observed":{"rawNormalityP":0.028572851060577234,"logNormalityP":0.576848713747224}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
