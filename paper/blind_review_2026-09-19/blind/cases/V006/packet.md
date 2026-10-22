# Blind item V006

Focal assessment: Causal judgments and next steps after candidate machine-difference analysis.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team on a high-speed rod-making line. Every unit leaving the line is judged sound or defective on appearance, and the charter commits us to no more than 1500 defective units per million inspected. The archive holds the inspected and defective counts for twenty-five consecutive lots, a study in which several inspectors judged the same retained units against an agreed answer key, and a machine-by-machine tally of defective and sound units over one common window, and one machine's inspected and defective counts either side of a change that was made to it.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether a sound/defective judgement can be relied on at all, whether the defective share has held steady across the lots, how today's level compares with what the charter commits us to, and what should be done next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
# Appearance Defect Reduction — Project Status

## Bottom line

The pass/fail measurement system is adequate to guide this project, provided its known repeatability weakness is controlled. The baseline was stable across lots but clearly above charter, so it required a system change rather than lot-by-lot firefighting. Machine 2 and loose ends were the strongest improvement targets. The monitoring record after the change is stable and meets the charter, although the short change trial by itself did not statistically prove the reduction and the available records do not identify what was physically changed.

## Can the pass/fail judgement be relied on?

The attribute study used 3 appraisers, 20 retained units, 2 repeats per appraiser, and 120 total judgements. The lowest appraiser accuracy was 90.0%; accuracies were 92.5%, 97.5%, and 90.0%. The lowest kappa was 0.7938144330; the individual kappas were 0.8378378378, 0.9459459459, and 0.7938144330. Thus, the judgements can be used for project decisions after accounting for chance agreement.

Repeatability is the weak point. The lowest repeat agreement was 80.0%; the appraisers' repeat agreements were 85.0%, 95.0%, and 80.0%. Future checks should separately report false passes and false fails. Until repeat agreement improves, retain the answer-key units, refresh appraiser calibration, and audit a defined sample from production rather than treating every visual verdict as perfect.

## Baseline: steady, but not capable

The 25-lot baseline contained 334 defectives in 125,000 inspections, or 2,672 DPMO. The charter allows 1,500 DPMO; at that rate the same inspections would correspond to 187.5 defectives. The observed excess is statistically clear (z = 10.7068804639, p = 4.7246199836 × 10^-27). Baseline binomial process Z was 2.7855317876.

The rate nevertheless held steady. Lot DPMO ranged from 1,800 through 3,800. The p chart had 0 out-of-control points; its equivalent limits were 481.8518888440 and 4,862.1481111560 DPMO. A homogeneity test also found no evidence of differing lot shares (chi-square = 14.8420531757, df = 24, p = 0.9252952261). Therefore, the gap was a common-cause process-level capability problem, not a pattern of isolated lots.

## What stands out as the cause

Machine 2 is a clear special cause in the common-window tally. It produced 26 defectives among 4,000 units (6,500 DPMO), while machines 1, 3, and 4 were at 1,500, 1,500, and 1,000 DPMO. Pooling those three machines gives 16 defectives in 12,000 units, or 1,333.3333333333 DPMO. Machine association is significant (chi-square = 30.8428672885, df = 3, p = 9.1733129599 × 10^-7), and machine 2 versus the others is also decisive (z = 5.5306627644, p = 3.1902312547 × 10^-8; excess = 5,166.6666666667 DPMO).

Loose end dominates the charter reject tally: 142 of 240 rejects, or 59.1666666667%. It also has the highest FMEA RPN, 294, compared with 252 for seam split, 210 for stain, 72 for soft spot, and 40 for off-weight. Thus, machine 2 and loose-end prevention are separately well-evidenced priorities. The available data do not cross-tabulate reject category by machine, so they do not prove that loose ends originate on machine 2; seam split remains the secondary risk even though its reject count is lower.

## What was changed, and what it achieved

The available process fact does not describe the physical change; a process-fact query found no matching recorded topic. This is a traceability gap, not evidence that the change was ineffective. The report therefore identifies the machine change only as “the change,” and the operating standard cannot be locked from these records alone.

In the paired trial, defectives fell from 18 in 4,000 before the change to 13 in 4,000 after it. That is an observed movement from 4,500 to 3,250 DPMO: an absolute reduction of 1,250 DPMO and a relative reduction of 27.7777777778%. However, the trial alone does not establish a statistically reliable effect (z = -0.8997715095, p = 0.3682418591), and the immediately post-change machine remained above charter (z = 2.8598837510, p = 0.0021189816).

The longer monitoring record gives stronger evidence of where the line now stands: 110 defectives in 89,300 inspections across 20 periods, or 1,231.8029115342 DPMO. The aggregate is statistically below 1,500 DPMO (one-sided z = -2.0709047497, p = 0.0191838491), and its 95% upper bound is 1,424.8683310274 DPMO. The variable-subgroup p chart has 0 out-of-control points; individual period DPMO ranges from 400 through 1896.5517241379. Its binomial process Z is 3.0277760558.

## What should be done next

1. **Close the change-control gap immediately.** Record the actual machine setting, release, owner, and effective date. The physical change cannot be named or standardized from the released data, and the conclusion stops at “a change was made.”
2. **Hold the gain with a p chart.** Continue the variable-subgroup chart using the post-change center line of 0.0012318029115. Investigate any out-of-control signal; do not react to every ordinary lot-to-lot fluctuation.
3. **Maintain charter governance.** The current record has 1,231.8029115342 DPMO and a 95% upper bound of 1,424.8683310274 DPMO, so it meets the 1,500-DPMO commitment but with limited margin. Review capability at a defined regular interval and after any process release.
4. **Control the remaining priority risks.** Keep loose end (RPN 294) as the primary mechanical/process focus, with seam split (RPN 252) second. Capture reject category and machine together going forward so causes can be localized rather than inferred.
5. **Strengthen visual judgement.** Re-run the attribute study after appraiser retraining and boundary-sample refresh. Set minimum requirements for both accuracy and repeat agreement; the current minimum values are 90.0% accuracy and 80.0% repeat agreement. Track false-pass and false-fail directions separately.
6. **Audit implementation and sustain.** Verify the undocumented change on the floor, preserve the calibration record, and require a defined sample and escalation rule before making future process decisions.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"agreement","units":20,"appraisers":3,"judgements":120,"repeatsPerAppraiser":2},"method_id":"msa.attribute_agreement","outputs":{"kappaMin":0.7938144329896908,"agreementPct":90.0,"repeatAgreementPctMin":80.0,"units":20,"appraisers":3,"judgements":120,"repeatsPerAppraiser":2,"appraiser1AgreementPct":92.5,"appraiser2AgreementPct":97.5,"appraiser3AgreementPct":90.0,"appraiser1Kappa":0.8378378378378379,"appraiser2Kappa":0.9459459459459459,"appraiser3Kappa":0.7938144329896908,"appraiser1RepeatPct":85.0,"appraiser2RepeatPct":95.0,"appraiser3RepeatPct":80.0},"status":"success","decision":"Attribute system is usable with controls: high chance-adjusted agreement but repeat agreement leaves no headroom for drift."}
{"step_id":2,"inputs_digest":{"batch":"lots","lots":25,"inspected":125000,"defectives":334,"nullDPMO":1500},"method_id":"basic.one_proportion","outputs":{"pValue":4.724619983557232e-27,"zStatistic":10.706880463852865,"avgP":0.002672,"avgDPMO":2672.0,"lots":25,"targetDefectsEquivalent":187.5,"targetDPMO":1500,"defectiveTotal":334,"inspectedTotal":125000},"status":"success","decision":"Baseline defective share is significantly above charter."}
{"step_id":3,"inputs_digest":{"batch":"lots","lots":25,"defectives":334,"inspected":125000},"method_id":"capability.binomial","outputs":{"processZ":2.785531787565683,"avgP":0.002672,"avgDPMO":2672.0,"defectiveTotal":334,"inspectedTotal":125000},"status":"success","decision":"Baseline binomial capability is inadequate."}
{"step_id":4,"inputs_digest":{"batch":"lots","lots":25,"subgroupSize":5000},"method_id":"control_chart.p","outputs":{"centerLine":0.002672,"outOfControlCount":0,"upperControlLimit":0.004862148111155955,"lowerControlLimit":0.00048185188884404453,"upperControlLimitDPMO":4862.148111155955,"lowerControlLimitDPMO":481.85188884404454,"lotDefectMin":9,"lotDefectMax":19,"minLotDPMO":1800.0,"maxLotDPMO":3800.0},"status":"success","decision":"Baseline lot-to-lot variation is consistent with common cause."}
{"step_id":5,"inputs_digest":{"batch":"lots","lots":25,"defectives":334,"inspected":125000,"tableRows":25,"columns":2},"method_id":"tables.chisquare_assoc","outputs":{"statistic":14.84205317566622,"pValue":0.9252952261054066,"degreesOfFreedom":24,"defectiveTotal":334,"inspectedTotal":125000},"status":"success","decision":"No evidence that the defective share differs by lot."}
{"step_id":6,"inputs_digest":{"batch":"machines","machines":4,"defectives":42,"inspected":16000},"method_id":"tables.chisquare_assoc","outputs":{"statistic":30.84286728853717,"pValue":9.173312959926518e-07,"degreesOfFreedom":3,"machineCount":4,"machine1DPMO":1500.0,"machine2DPMO":6500.0,"machine3DPMO":1500.0,"machine4DPMO":1000.0,"machine1Defectives":6,"machine2Defectives":26,"machine3Defectives":6,"machine4Defectives":4,"machineInspectedEach":4000,"overallDefectives":42,"overallInspected":16000},"status":"success","decision":"Defective share differs by machine; machine 2 is the outlier."}
{"step_id":7,"inputs_digest":{"batch":"machines","group1":"machine 2","group2":"other machines","group1Defectives":26,"group1Inspected":4000,"group2Defectives":16,"group2Inspected":12000},"method_id":"basic.two_proportions","outputs":{"pValue":3.190231254655291e-08,"zStatistic":5.530662764379728,"machine2P":0.0065,"machine2DPMO":6500.0,"otherP":0.0013333333333333333,"otherDPMO":1333.3333333333333,"machine2Defectives":26,"machine2Inspected":4000,"otherDefectives":16,"otherInspected":12000,"differenceDPMO":5166.666666666667},"status":"success","decision":"Focused contrast confirms machine 2 is materially worse than the other machines."}
{"step_id":8,"inputs_digest":{"batch":"after_change","beforeDefectives":18,"beforeInspected":4000,"afterDefectives":13,"afterInspected":4000},"method_id":"basic.two_proportions","outputs":{"pValue":0.3682418590767994,"zStatistic":-0.899771509542612,"beforeP":0.0045,"beforeDPMO":4500.0,"afterP":0.00325,"afterDPMO":3250.0,"absoluteReductionDPMO":1249.9999999999998,"relativeReductionPct":27.777777777777775,"beforeDefectives":18,"beforeInspected":4000,"afterDefectives":13,"afterInspected":4000,"difference95LowerDPMO":-3972.775729838945,"difference95UpperDPMO":1472.7757298389454},"status":"success","decision":"Observed reduction is not statistically demonstrable in the change trial alone."}
{"step_id":9,"inputs_digest":{"batch":"after_change","defectives":13,"inspected":4000,"nullDPMO":1500},"method_id":"basic.one_proportion","outputs":{"pValue":0.00211898163415606,"zStatistic":2.8598837510064232,"avgP":0.00325,"avgDPMO":3250.0,"defectiveTotal":13,"inspectedTotal":4000},"status":"success","decision":"Immediately after the change, that machine remained significantly above charter."}
{"step_id":10,"inputs_digest":{"batch":"sustaining","periods":20,"defectives":110,"inspected":89300,"nullDPMO":1500},"method_id":"basic.one_proportion","outputs":{"pValue":0.01918384911363467,"zStatistic":-2.0709047496753703,"avgP":0.0012318029115341545,"avgDPMO":1231.8029115341544,"defectiveTotal":110,"inspectedTotal":89300,"upper95DPMO":1424.8683310273984,"confidenceLevelPct":95,"targetDPMO":1500},"status":"success","decision":"Monitoring aggregate is statistically below the charter limit."}
{"step_id":11,"inputs_digest":{"batch":"sustaining","periods":20,"subgroupSizeMin":3200,"subgroupSizeMax":6400},"method_id":"control_chart.p","outputs":{"centerLine":0.0012318029115341545,"outOfControlCount":0,"minSubgroupDPMO":400.0,"maxSubgroupDPMO":1896.5517241379312,"periods":20,"defectiveTotal":110,"inspectedTotal":89300},"status":"success","decision":"Post-change monitoring is stable at the reduced level."}
{"step_id":12,"inputs_digest":{"batch":"sustaining","periods":20,"defectives":110,"inspected":89300},"method_id":"capability.binomial","outputs":{"processZ":3.027776055826837,"avgP":0.0012318029115341545,"avgDPMO":1231.8029115341544,"upper95DPMO":1424.8683310273984,"defectiveTotal":110,"inspectedTotal":89300},"status":"success","decision":"Current binomial capability meets the charter on this record."}
{"step_id":13,"inputs_digest":{"batch":"candidates","categories":5,"rejectTotal":240},"method_id":"quality.pareto","outputs":{"topCategoryPct":59.166666666666664,"topCategoryCount":142,"categoryCount":5,"rejectTotal":240,"looseEndCount":142},"status":"success","decision":"Loose end is the dominant reject category."}
{"step_id":14,"inputs_digest":{"batch":"failure_modes","modes":5},"method_id":"quality.fmea_rpn","outputs":{"maxRpn":294,"modeCount":5,"looseEndRpn":294,"seamSplitRpn":252,"stainRpn":210,"softSpotRpn":72,"offWeightRpn":40},"status":"success","decision":"Loose end has the highest risk priority."}
```

## Submitted route declarations
```json
[{"point":"measurement_gate","chosen_branch":"proceed_using_attribute_data_with_periodic_verification","observed":{"kappaMin":0.7938144329896908,"agreementPct":90.0,"repeatAgreementPctMin":80.0}},{"point":"baseline_variation","chosen_branch":"common_cause_improvement","observed":{"outOfControlCount":0,"homogeneityPValue":0.9252952261054066}},{"point":"machine_priority","chosen_branch":"machine_2","observed":{"machine2DPMO":6500.0,"otherDPMO":1333.3333333333333,"contrastPValue":3.190231254655291e-08}},{"point":"change_evidence","chosen_branch":"retain_change_based_on_monitoring_and_document_the_change","observed":{"trialPValue":0.3682418590767994,"monitoringDPMO":1231.8029115341544,"monitoringUpper95DPMO":1424.8683310273984}},{"point":"process_fact","chosen_branch":"report_missing_process_fact","observed":{}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
