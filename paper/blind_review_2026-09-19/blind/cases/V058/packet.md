# Blind item V058

Focal assessment: Baseline defect-rate chart stability, business performance, and next steps.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

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
# Final inspection project status

## Executive conclusion

The original accept/reject call could not be relied on, so the first prerequisite was to repair the measurement system. The rewritten criteria were followed by a large improvement in the attribute study, and the call now appears reliable. The lot record nevertheless did not hold steady: it shows a statistically significant downward trend. The improvement has not yet secured the business requirement. The current supplied placement window rejected **202 of 6,000 boards (3.367%)**, versus the **2.0%** requirement; it contains **82 excess rejects** relative to a 6,000-board allowance of **120**. Head 1 is the dominant immediate focus.

## Could the accept/reject call be relied on?

Originally, no. Three inspectors each judged the same 20 retained boards twice against the answer key (120 calls). Only **73.333%** of calls agreed with the key—**32 mismatches**—and the weakest inspector kappa was **0.285714**. The appraiser agreement rates were **70.0%**, **67.5%**, and **82.5%**. Repeat-trial agreement was only **63.333%**.

Thus, calls made before criteria repair could not safely be treated as truth. The numerical lot record was not interpreted as proof of true defect level until the measurement issue was addressed.

## What had to happen first, and what changed

The disagreement tally's largest category was **insufficient solder**, accounting for **43 of 90 tally entries (47.778%)**. With **16** tombstone entries, those two accounted for **65.556%**. The full tally was **insufficient solder 43, tombstone 16, component offset 13, wrong polarity 11, and solder bridge 7**. The steward did not define the tally's counting unit; it does not reconcile like-for-like with the 120 key-comparison calls and is therefore kept separate rather than presented as a percentage of calls.

The accept/reject criteria were rewritten afterward. In the second study, **99.167%** of 120 calls agreed with the key and the weakest inspector kappa was **0.941860**. There was **1 mismatch**, and repeat agreement rose to **98.333%**. Agreement increased by **25.833 percentage points**, minimum kappa by **0.656146**, and repeatability by **35.0 percentage points**. This supports reliance on the post-rewrite call; it does not by itself prove that every historical lot-level change was caused by the rewrite.

## Did the reject share hold steady across lots?

Across all 25 lots and 10,000 inspected boards there were 311 rejects (**3.11%**). The whole-series p chart had **0** points outside its three-sigma limits, and the above/below-center runs test was not significant (p = **0.154355**). However, “no point outside limits” is not the same as “steady”: lot order had a significant downward trend (p = **0.040377**; slope **-0.000531** per lot; R² **17.026%**).

The strongest data-detected split was after lot 17: the first 17 lots rejected **240/6,800 (3.529%)**, while the last 8 rejected **71/3,200 (2.219%)**; the two-proportion test gave p = **0.000428**, or **0.010276** after considering all 24 candidate splits. This is strong evidence of a level change in the archive, but I did not obtain a process fact tying the criteria rewrite to lot 17, so I will not claim that exact attribution.

## How does today compare with the requirement?

The current placement window is above requirement: **202/6,000 = 3.367%**, with a 95% Wilson interval from **2.939% to 3.854%**; the binomial upper-tail test against 2.0% gives p = **3.217e-12**. At 2%, 6,000 boards allow **120** rejects, so this window has **82 excess rejects**.

By head:

- Head 1: **128/3,000 = 4.267%**, **68 excess rejects**, upper-tail p = **7.684e-15**.
- Head 2: **74/3,000 = 2.467%**, **14 excess rejects**, upper-tail p = **0.042585**.
- Head 1 is **1.800 percentage points** higher than Head 2; the head-to-head two-proportion test gives p = **0.000111**.

The late eight-lot archive segment was **71/3,200 = 2.219%** (95% Wilson interval **1.763% to 2.789%**; upper-tail p = **0.203953**) and had no p-chart point outside limits. Its point estimate is still above 2.0%, but the segment alone does not statistically establish a capability violation. The current placement window is less favorable and is the stronger operational basis for action.

## What should be done next

- **Contain and prioritize Head 1.** Its current 4.267% rate is both materially and statistically worse than Head 2. Apply the plant's containment protocol to Head 1 output while its placement process is investigated.
- **Run a Head 1-specific mechanical/process investigation.** Compare nozzle, pick/place force, feed, solder-paste, and maintenance condition with Head 2. The supplied data identify the head difference, not its physical root cause.
- **Maintain the rewritten criteria and audit them.** Retain boundary boards, answer keys, and blind checks so the 99.167% agreement does not drift.
- **Use a p chart by lot plus trend and run rules.** The archive had no three-sigma flags despite a significant shift, so points outside limits must not be the only escalation trigger.
- **Obtain the missing timing facts.** The criteria-implementation lot and the linkage between the placement window and rewrite could not be retrieved. Until they are supplied, describe the late-lot improvement as occurring after the detected split—not formally as the rewrite's effect.
- **Do not declare the line capable.** Current output remains 1.367 percentage points above the 2.0% requirement. Re-evaluate after Head 1 corrective action with a predefined sample-size and control rule.

No archive batch was denied. The attribution gap is limited to unavailable process-timing facts; it does not undermine the computed MSA improvement, the observed lot shift, or the current head comparison.

**Bottom line:** the call had to be repaired before rejects could be managed; that repair succeeded. The lot record then shifted downward, but today's window is still above requirement, and Head 1 is the clearest next target.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"stage":"define","fieldCount":2},"method_id":"meta.data_profiling","outputs":{"requiredRejectShare":0.02,"releasedBatchCount":6,"deniedBatchCount":0,"unroutableProcessFactCount":2,"targetRejectPct":2.0},"status":"success","decision":"The requirement is 0.02 or lower; no archive batch was denied."}
{"step_id":2,"inputs_digest":{"stage":"study_1","items":20,"inspectors":3,"replications":2,"calls":120},"method_id":"msa.attribute_agreement","outputs":{"attemptCount":2},"status":"failed","decision":"Two preliminary pooling attempts failed from data-shape errors; no result was used."}
{"step_id":3,"inputs_digest":{"stage":"study_1","items":20,"inspectors":3,"replications":2,"calls":120},"method_id":"msa.attribute_agreement","outputs":{"kappaMin":0.2857142857142857,"agreementPct":73.33333333333333,"mismatchCount":32,"withinInspectorAgreementPct":63.33333333333333,"standardFailCount":6,"itemCount":20,"inspectorCount":3,"replicationCount":2,"callCount":120,"standardFailPct":30.0,"appraiser1AgreementPct":70.0,"appraiser2AgreementPct":67.5,"appraiser3AgreementPct":82.5},"status":"success","decision":"Baseline call is not reliable: 32/120 calls disagreed, minimum kappa was 0.2857, and repeat agreement was 63.33%."}
{"step_id":4,"inputs_digest":{"stage":"disagreements","categories":5,"tallyTotal":90},"method_id":"quality.pareto","outputs":{"topCategoryPct":47.77777777777778,"topTwoCumulativePct":65.55555555555556,"insufficientSolderCount":43,"tombstoneCount":16,"tallyTotal":90,"componentOffsetCount":13,"wrongPolarityCount":11,"solderBridgeCount":7},"status":"success","decision":"Insufficient solder is the largest disagreement category; the tally units are not calls against the key."}
{"step_id":5,"inputs_digest":{"stage":"study_2","items":20,"inspectors":3,"replications":2,"calls":120},"method_id":"msa.attribute_agreement","outputs":{"kappaMin":0.9418604651162791,"agreementPct":99.16666666666667,"mismatchCount":1,"withinInspectorAgreementPct":98.33333333333333,"itemCount":20,"inspectorCount":3,"replicationCount":2,"callCount":120},"status":"success","decision":"Post-rewrite call is materially reliable: 1/120 calls disagreed, minimum kappa was 0.9419, and repeat agreement was 98.33%."}
{"step_id":6,"inputs_digest":{"comparison":"study_1_to_study_2","itemsPerStudy":20,"callsPerStudy":120},"method_id":"msa.attribute_agreement","outputs":{"agreementImprovementPctPoints":25.833333333333343,"kappaImprovement":0.6561461794019934,"repeatImprovementPctPoints":35.0},"status":"success","decision":"The rewrite coincided with large descriptive gains in accuracy and repeatability."}
{"step_id":7,"inputs_digest":{"stage":"lots","lots":25,"inspected":10000},"method_id":"control_chart.p","outputs":{"centerLine":0.0311,"outOfControlCount":0,"totalRejected":311,"overallRejectPct":3.11,"lastLotRejectPct":1.25,"lotCount":25,"inspectedCount":10000,"rejectedCount":311,"sigmaLimit":3.0},"status":"success","decision":"The whole-series p chart had no point outside three-sigma limits, but that alone does not establish steadiness."}
{"step_id":8,"inputs_digest":{"stage":"lots","lots":25,"lotRejectRates":25},"method_id":"basic.descriptive_summary","outputs":{"mean":0.0311,"median":0.03,"stdDev":0.009467048114380745,"skewness":-0.02120149167783207,"adPValue":0.5293060244521073},"status":"success","decision":"Lot rates averaged 3.11% with no strong abnormality signal."}
{"step_id":9,"inputs_digest":{"stage":"lots","lots":25},"method_id":"nonparametric.runs_test","outputs":{"pValue":0.15435475680586547,"runsZ":-1.424316902390313,"runsAboveBelow":10},"status":"success","decision":"The above/below-center runs test did not detect clustering at 5% significance."}
{"step_id":10,"inputs_digest":{"stage":"lots","lots":25,"x":"lotOrder","y":"rejectShare"},"method_id":"regression.ols","outputs":{"modelPValue":0.0403770777740765,"rSquaredPct":17.026070164145473,"rSquaredAdjPct":13.41850799736919,"slopePerLot":-0.0005307692307692307},"status":"success","decision":"Reject share trended downward across lot order; the trend explains a modest 17.03% of variation."}
{"step_id":11,"inputs_digest":{"stage":"lots","splitSelection":"maximum absolute z over 24 candidate splits","earlyInspected":6800,"lateInspected":3200},"method_id":"basic.two_proportions","outputs":{"pValue":0.00042815936404371564,"zStatistic":3.5220896261020793,"bonferroniPValue":0.010275824737049175,"earlyRejectPct":3.5294117647058822,"lateRejectPct":2.21875,"afterLot":17,"candidateSplitCount":24,"earlyInspectedCount":6800,"earlyRejectedCount":240,"lateInspectedCount":3200,"lateRejectedCount":71},"status":"success","decision":"The strongest observed split is after lot 17 and remains significant after testing 24 splits; it is not asserted to be the criteria-change lot."}
{"step_id":12,"inputs_digest":{"scope":"all_25_lots","inspected":10000,"rejected":311},"method_id":"capability.binomial","outputs":{"processZ":7.928571428571428,"avgP":0.0311,"upperTailPValue":1.252860457627278e-13,"ciLowerPct":2.7873685933108745,"ciUpperPct":3.4686427738911765,"rejectedCount":311,"inspectedCount":10000,"targetGapPct":1.11,"confidenceLevel":0.95},"status":"success","decision":"All lots combined are statistically above the 0.02 requirement."}
{"step_id":13,"inputs_digest":{"scope":"late_eight_lots","lots":8},"method_id":"control_chart.p","outputs":{"centerLine":0.0221875,"outOfControlCount":0,"ucl":0.04428144337786659,"lcl":9.355662213340887e-05,"lotCount":8,"sigmaLimit":3.0},"status":"success","decision":"The exploratory late segment has no p-chart point outside limits."}
{"step_id":14,"inputs_digest":{"scope":"late_eight_lots","inspected":3200,"rejected":71},"method_id":"capability.binomial","outputs":{"processZ":0.8838834764831838,"avgP":0.0221875,"upperTailPValue":0.20395343727394855,"ciLowerPct":1.762804293976554,"ciUpperPct":2.789276721741904,"rejectedCount":71,"inspectedCount":3200,"rejectPct":2.21875,"targetGapPct":0.21875,"confidenceLevel":0.95},"status":"success","decision":"The observed late-lot rate is 2.22%; its 95% interval includes 2.0%, so this segment alone does not statistically establish a requirement violation."}
{"step_id":15,"inputs_digest":{"scope":"current_placement_window","inspected":6000,"rejected":202},"method_id":"capability.binomial","outputs":{"processZ":7.561538914024003,"avgP":0.033666666666666664,"upperTailPValue":3.216977127203878e-12,"ciLowerPct":2.9392857632235696,"ciUpperPct":3.8537227067370012,"rejectedCount":202,"inspectedCount":6000,"rejectPct":3.3666666666666663,"targetGapPct":1.3666666666666663,"targetMaxRejected":120,"excessRejected":82,"confidenceLevel":0.95},"status":"success","decision":"Today window is demonstrably above requirement at 3.37%."}
{"step_id":16,"inputs_digest":{"scope":"head_1_vs_requirement","inspected":3000,"rejected":128},"method_id":"basic.one_proportion","outputs":{"pValue":7.454556452019344e-19,"processZ":8.867889026274119,"rejectPct":4.266666666666667,"rejectedCount":128,"inspectedCount":3000,"targetGapPct":2.2666666666666666,"targetMaxRejected":60,"excessRejected":68,"confidenceLevel":0.95,"upperTailPValue":7.68370031322142e-15},"status":"success","decision":"Head 1 is above the 2% requirement."}
{"step_id":17,"inputs_digest":{"scope":"head_2_vs_requirement","inspected":3000,"rejected":74},"method_id":"basic.one_proportion","outputs":{"pValue":0.06788915486182899,"processZ":1.8257418583505538,"rejectPct":2.466666666666667,"rejectedCount":74,"inspectedCount":3000,"targetGapPct":0.4666666666666668,"targetMaxRejected":60,"excessRejected":14,"confidenceLevel":0.95,"upperTailPValue":0.04258517365551799},"status":"success","decision":"Head 2 is 2.47%; the two-sided test does not separate it from 2.0% at 5%, though its point estimate remains above target."}
{"step_id":18,"inputs_digest":{"scope":"placement_head_comparison","head1Inspected":3000,"head2Inspected":3000},"method_id":"basic.two_proportions","outputs":{"pValue":0.00011106855772889447,"zStatistic":3.8650453567700054,"head1RejectPct":4.266666666666667,"head2RejectPct":2.466666666666667,"differencePct":1.7999999999999998,"head1RejectedCount":128,"head2RejectedCount":74,"head1InspectedCount":3000,"head2InspectedCount":3000},"status":"success","decision":"Head 1 rejects at a significantly higher rate than Head 2."}
{"step_id":19,"inputs_digest":{"scope":"tally_reconciliation","ratingVectors":6,"pairsCompared":15},"method_id":"msa.attribute_agreement","outputs":{"pairwiseDisagreementCount":126,"stewardTallyTotal":90},"status":"success","decision":"The 90 steward tally could not be reconciled to the 120-call key comparison; its tally unit is therefore not assumed to be one call."}
{"step_id":20,"inputs_digest":{"request":"criteria implementation lot","processFactMatches":0},"method_id":"meta.data_profiling","outputs":{"matchingProcessFactCount":0},"status":"refused","decision":"Do not claim the observed split is the rewrite lot."}
{"step_id":21,"inputs_digest":{"request":"current window timing relative to rewrite","processFactMatches":0},"method_id":"meta.data_profiling","outputs":{"matchingProcessFactCount":0},"status":"refused","decision":"Interpret heads as the supplied current window without an externally confirmed timing linkage."}
```

## Submitted route declarations
```json
[{"point":"measurement_system_gate","chosen_branch":"repair_before_interpreting_lot_calls","observed":{"kappaBefore":0.2857142857142857,"agreementBeforePct":73.33333333333333,"kappaAfter":0.9418604651162791,"agreementAfterPct":99.16666666666667}},{"point":"change_attribution","chosen_branch":"do_not_assign_observed_change_to_rewrite_without_process_fact","observed":{"bestSplitAfterLot":17,"bonferroniPValue":0.010275824737049175,"matchingProcessFacts":0}},{"point":"disagreement_tally_units","chosen_branch":"analyze_as_separate_tally_units","observed":{"tallyTotal":90,"keyComparisonCalls":120}},{"point":"current_action","chosen_branch":"prioritize_head_1_and_hold_control","observed":{"currentRejectPct":3.3666666666666663,"head1RejectPct":4.266666666666667,"head2RejectPct":2.466666666666667}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
