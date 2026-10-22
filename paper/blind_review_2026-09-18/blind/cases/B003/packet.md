# Blind item B003

Focal assessment: The second (repeat) attribute agreement study and subsequent actions.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team on an electronic-assembly line. Boards are accepted or rejected by eye at final inspection, and the line is required to hold the reject share at or below 2%. The archive holds the inspected and rejected counts for twenty-five consecutive lots, a study in which several inspectors judged the same retained boards against an agreed answer key, a tally of the items those inspectors called differently from the key broken out by the category the item was rejected under, a second study run on retained boards after the accept/reject criteria were rewritten, and one window's rejected and placed counts for each of the two placement heads.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether an accept/reject call can be relied on, what had to happen before it could be, whether the reject share has held steady across the lots, how today's level compares with what the line is required to hold, and what should be done next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
# Quality improvement project status

## Executive assessment
The accept/reject system was not initially dependable. Rewriting the inspection criteria was the necessary measurement-system intervention before interpreting production rejects. The retained-board recheck now supports using the calls, with ongoing audits. The production history is stable under the basic point-limit chart rule, but stability is not compliance: the observed reject share is **3.11%**, above the **2%** requirement. The higher-reject placement head is the next investigation priority, not yet a proven root cause.

## Measurement: what changed and what it achieved
The initial study contained 120 ratings on 20 retained boards. Overall agreement with the key was 73.33%; minimum appraiser Cohen kappa was 0.2857. Appraiser agreement was 70%, 67.5%, and 82.5%; repeatability was 60%, 55%, and 75%. These results do not support relying on the original visual calls.

The separate disagreement tally contained 90 items. Insufficient solder accounted for 47.78%, the largest category, followed by tombstone at 17.78%, component offset at 14.44%, wrong polarity at 12.22%, and solder bridge at 7.78%. This is a Pareto of disagreement with the key, **not** a Pareto proving the causes of production defects. It justified prioritizing clearer accept/reject examples, particularly solder adequacy. This separate tally should not be treated as the count of mismatches in the retained-board rating matrix.

After the criteria were rewritten, agreement rose to 99.17% and minimum kappa to 0.9419. Appraiser agreement was 100%, 100%, and 97.5%, with repeatability of 100%, 100%, and 95%. Kappa was calculated against the key separately for each appraiser, pooling repeat ratings; overall agreement is the fraction of all ratings matching the key. The recheck supports operational use, not a guarantee of perfect field inspection: retained boards and repeated ratings are not independent samples of all future production. Maintain the rewritten standard, boundary examples and inspector calibration. The data demonstrate improved measurement, not a reduction in physical defects.

## Process stability and requirement
Across 25 lots, 311 of 10000 inspected boards were rejected. A binomial p chart has center line 0.0311, lower limit 0.005062 and upper limit 0.057138, with 0 points outside the limits. This is evidence of common-cause behavior under the point-limit rule, not proof that every possible run-pattern test passes. Board independence and consistent classification are assumptions; the archive does not establish the timing of these lots relative to the criteria change.

Binomial capability gives average reject share 3.11%, or 1.555 times the required level. The unshifted yield-equivalent process Z is 1.8649; continuous-data capability indices are inappropriate for these counts. An exact upper-tail binomial test against the required share gives p = 1.253e-13, supporting that the underlying level exceeds the requirement if the sampling assumptions hold. The archive-wide estimate describes the observed window, not a separately measured current-day rate. Do not confuse control limits with the customer requirement.

## Placement-head evidence and next action
The head comparison window contains 128 rejects among 3000 placements for the first head and 74 among 3000 for the other. The rates are 4.2667% and 2.4667%, a difference of 1.8000 percentage points. A pooled, two-sided proportions test gives z = 3.8650, p = 0.000111069. The higher rejection rate merits a focused investigation of the first head.

This observational comparison cannot separate head condition from board mix, component mix, setup, operator, or time. Placement denominators also must not be conflated with inspected-board denominators. Inspect alignment, nozzle condition, feeders and setup records; stratify comparable jobs and confirm the mechanism before choosing a corrective action. Use a controlled matched-job trial where practical and verify both placement and final-board rejection afterward.

## Hold the gains and close the project
Quality should own version-controlled criteria, retained boundary samples, refresher training and periodic blinded agreement checks. Production engineering should own the head investigation and documented corrective trial. Continue lot-level p-chart monitoring with the validated inspection method; investigate signals rather than adjusting a stable process at random. After a verified physical process change, collect a fresh ordered lot series and reassess stability and compliance before resetting limits or claiming closure.

No physical head correction or post-correction production study was supplied, so no achieved production improvement or sustained compliance can be claimed. No batch was denied; the owner supplied no additional process facts in response to the criterion question. Mechanical root cause, comparability of head workloads, measurement-change chronology and present-day performance remain unverified. The project has qualified its inspection method and identified an actionable association, but has not yet demonstrated that the line meets its requirement.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"meta.data_profiling","inputs_digest":{"source":"define"},"outputs":{"requiredRejectShare":0.02},"status":"success","decision":"Business target"}
{"step_id":2,"method_id":"msa.attribute_agreement","inputs_digest":{"source":"study_1"},"outputs":{"appraiser1Kappa":0.2857142857142857,"appraiser1AgreementPct":70.0,"appraiser1RepeatabilityPct":60.0,"appraiser2Kappa":0.3085106382978724,"appraiser2AgreementPct":67.5,"appraiser2RepeatabilityPct":55.00000000000001,"appraiser3Kappa":0.6111111111111109,"appraiser3AgreementPct":82.5,"appraiser3RepeatabilityPct":75.0,"kappaMin":0.2857142857142857,"agreementPct":73.33333333333333,"boards":20,"ratings":120},"status":"success","decision":"Compare ratings to standard; kappa pooled over repeats within each appraiser."}
{"step_id":3,"method_id":"quality.pareto","inputs_digest":{"source":"disagreements"},"outputs":{"topCategoryPct":47.77777777777778,"totalDisagreements":90,"component offsetPct":14.444444444444445,"insufficient solderPct":47.77777777777778,"solder bridgePct":7.777777777777778,"tombstonePct":17.77777777777778,"wrong polarityPct":12.222222222222221},"status":"success","decision":"Prioritize clarification of insufficient solder"}
{"step_id":4,"method_id":"msa.attribute_agreement","inputs_digest":{"source":"study_2"},"outputs":{"appraiser1Kappa":1.0,"appraiser1AgreementPct":100.0,"appraiser1RepeatabilityPct":100.0,"appraiser2Kappa":1.0,"appraiser2AgreementPct":100.0,"appraiser2RepeatabilityPct":100.0,"appraiser3Kappa":0.9418604651162791,"appraiser3AgreementPct":97.5,"appraiser3RepeatabilityPct":95.0,"kappaMin":0.9418604651162791,"agreementPct":99.16666666666667,"boards":20,"ratings":120},"status":"success","decision":"Compare ratings to standard; kappa pooled over repeats within each appraiser."}
{"step_id":5,"method_id":"control_chart.p","inputs_digest":{"source":"lots"},"outputs":{"centerLine":0.0311,"outOfControlCount":0,"lcl":0.005061801617623388,"ucl":0.05713819838237661,"lotCount":25,"inspected":10000,"rejected":311},"status":"success","decision":"No points beyond three-sigma limits; this does not prove independence or exclude all run patterns."}
{"step_id":6,"method_id":"capability.binomial","inputs_digest":{"source":"lots"},"outputs":{"avgP":0.0311,"processZ":1.8648673498199195,"requiredRejectShare":0.02,"rejectPct":3.11,"targetPct":2.0,"ratioToTarget":1.555},"status":"success","decision":"Stable on point-limit rule but reject level exceeds requirement; Z uses no shift."}
{"step_id":7,"method_id":"basic.one_proportion","inputs_digest":{"source":"lots"},"outputs":{"pValue":1.252860457627278e-13},"status":"success","decision":"Exact one-sided binomial test of reject share above requirement; assumes independent boards."}
{"step_id":8,"method_id":"basic.two_proportions","inputs_digest":{"source":"heads"},"outputs":{"pValue":0.00011106855772889447,"zStatistic":3.8650453567700054,"head1Pct":4.266666666666667,"head2Pct":2.466666666666667,"differencePctPoints":1.7999999999999998,"head1Rejected":128,"head2Rejected":74,"head1Placed":3000,"head2Placed":3000},"status":"success","decision":"Two-sided pooled two-proportion z test: head 1 has higher rejection; observational association, not proof of cause."}
```

## Submitted route declarations
```json
[{"point":"measurement_baseline","chosen_branch":"clarify criteria before process inference","observed":{"appraiser1Kappa":0.2857142857142857,"appraiser1AgreementPct":70.0,"appraiser1RepeatabilityPct":60.0,"appraiser2Kappa":0.3085106382978724,"appraiser2AgreementPct":67.5,"appraiser2RepeatabilityPct":55.00000000000001,"appraiser3Kappa":0.6111111111111109,"appraiser3AgreementPct":82.5,"appraiser3RepeatabilityPct":75.0,"kappaMin":0.2857142857142857,"agreementPct":73.33333333333333,"boards":20,"ratings":120}},{"point":"measurement_recheck","chosen_branch":"proceed with qualified measurement system","observed":{"appraiser1Kappa":1.0,"appraiser1AgreementPct":100.0,"appraiser1RepeatabilityPct":100.0,"appraiser2Kappa":1.0,"appraiser2AgreementPct":100.0,"appraiser2RepeatabilityPct":100.0,"appraiser3Kappa":0.9418604651162791,"appraiser3AgreementPct":97.5,"appraiser3RepeatabilityPct":95.0,"kappaMin":0.9418604651162791,"agreementPct":99.16666666666667,"boards":20,"ratings":120}},{"point":"lot_stability","chosen_branch":"stable by point limits; assess binomial capability","observed":{"centerLine":0.0311,"outOfControlCount":0,"lcl":0.005061801617623388,"ucl":0.05713819838237661,"lotCount":25,"inspected":10000,"rejected":311}},{"point":"improvement_focus","chosen_branch":"investigate higher-reject placement head","observed":{"pValue":0.00011106855772889447,"zStatistic":3.8650453567700054,"head1Pct":4.266666666666667,"head2Pct":2.466666666666667,"differencePctPoints":1.7999999999999998,"head1Rejected":128,"head2Rejected":74,"head1Placed":3000,"head2Placed":3000}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
