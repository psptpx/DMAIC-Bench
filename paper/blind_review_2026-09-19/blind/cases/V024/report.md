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
