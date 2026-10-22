# Blind item V022

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
# Appearance Defect Improvement Project Report

## Measurement reliability
All requested shop-floor batches were released; no data batch was denied. Attribute agreement with the answer key was 93.333%. The appraiser-vs-standard kappa range was 0.7 to 1.0, the between-appraiser Fleiss kappa was 0.736, and the minimum repeat kappa was 0.6. The measurement system can support coarse process comparisons, but it should not be used for lot-by-lot decisions until repeatability is improved.

## Baseline and stability
The lot record contains 25 lots, 125000 inspections, and 334 defects. The overall level was 2672 DPMO with center line 0.002672. The p-chart flagged 0 lots, so the lot-to-lot defective share was stable rather than shifting randomly. The test against the 1500 DPMO charter target gave p = 3.396e-22, so the baseline is significantly above the committed level. The corresponding process Z was 2.786.

## Causes and machine pattern
Reject categories totalled 240, and loose end was the largest category at 142 rejections, or 59.167% of the category total. In the FMEA, loose end had the maximum RPN of 294. The machine tally showed 26 defects in 4000 units for the high-rate machine (6500 DPMO), against 6 in 4000 (1500 DPMO), 6 in 4000 (1500 DPMO), and 4 in 4000 (1000 DPMO) for the other machines. The chi-square test gave statistic 30.843 and p = 9.17e-7. The priority is the machine with the 6500 DPMO rate and the loose-end defect mode.

## Change result
The supplied before/after record had 18 defects in 4000 before the change (4500 DPMO) and 13 defects in 4000 after (3250 DPMO). The proportions test gave z = 0.9 and p = 0.368, so the improvement is not statistically demonstrated. The after-change level is still above the 1500 DPMO charter. The process owner could not supply a matching process fact, so the changed machine and change mechanism are not identifiable from the released data.

## Sustaining
The post-change monitoring record contains 89300 inspections and 110 defects. Its center line was 0.0012318 (1231.8 DPMO), and the p-chart flagged 0 points. Against the 1500 DPMO target, p = 0.985 and the process Z was 3.028. The monitored window is statistically consistent with the committed level.

## Next actions
- Audit and correct loose-end generation on the high-rate machine; loose end has the largest Pareto share and the maximum RPN.
- Improve inspector repeatability before using lot-level judgements for accept/reject decisions; the weakest repeat kappa is 0.6.
- Re-run the changed-machine comparison with more data; the current p = 0.368 does not establish a change effect.
- Continue the post-change p-chart and confirm that 0 points remain outside control limits.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"msa.attribute_agreement","outputs":{"kappaMin":0.6,"agreementPct":93.333,"standardKappaMin":0.7,"standardKappaMax":1.0,"fleissKappa":0.736,"appraiserCount":3,"unitsPerAppraiser":20,"judgementsCompared":120,"withinAppraiserKappaMax":0.894},"status":"success","decision":"measurement system usable for coarse process comparisons but not for lot-by-lot decisions without improved repeatability"}
{"step_id":2,"method_id":"quality.pareto","outputs":{"topCategoryPct":59.167,"totalRejectCount":240,"looseEndCount":142,"offWeightCount":21,"seamSplitCount":27,"softSpotCount":29,"stainCount":21},"status":"success","decision":"loose end is the leading reject category"}
{"step_id":3,"method_id":"quality.fmea_rpn","outputs":{"maxRpn":294,"looseEndRpn":294,"seamSplitRpn":252,"stainRpn":210,"softSpotRpn":72,"offWeightRpn":40},"status":"success","decision":"loose end has the maximum risk priority number"}
{"step_id":4,"method_id":"control_chart.p","outputs":{"centerLine":0.002672,"outOfControlCount":0,"lotsCount":25,"totalInspected":125000,"totalDefects":334,"baselineDPMO":2672},"status":"success","decision":"lot defect share stable and above charter"}
{"step_id":5,"method_id":"basic.one_proportion","outputs":{"pValue":3.396e-22,"pObserved":0.002672,"targetP":0.0015,"targetDPMO":1500,"sampleSize":125000,"defectCount":334},"status":"success","decision":"baseline significantly above the committed level"}
{"step_id":6,"method_id":"tables.chisquare_assoc","outputs":{"statistic":30.843,"pValue":9.17e-07,"machine2Defects":26,"machine2Total":4000,"machine2DPMO":6500,"machine1Defects":6,"machine1Total":4000,"machine1DPMO":1500,"machine3Defects":6,"machine3Total":4000,"machine3DPMO":1500,"machine4Defects":4,"machine4Total":4000,"machine4DPMO":1000},"status":"success","decision":"machine-to-machine defect rates differ"}
{"step_id":7,"method_id":"basic.two_proportions","outputs":{"pValue":0.368,"zStatistic":0.9,"beforeDefects":18,"beforeTotal":4000,"beforeDPMO":4500,"afterDefects":13,"afterTotal":4000,"afterDPMO":3250},"status":"success","decision":"before and after change difference not statistically significant"}
{"step_id":8,"method_id":"control_chart.p","outputs":{"centerLine":0.0012318,"outOfControlCount":0,"sustainingTotal":89300,"sustainingDefects":110,"sustainingDPMO":1231.8},"status":"success","decision":"sustaining defect share stable"}
{"step_id":9,"method_id":"basic.one_proportion","outputs":{"pValue":0.985,"pObserved":0.0012318,"targetP":0.0015,"targetDPMO":1500,"sampleSize":89300,"defectCount":110},"status":"success","decision":"sustaining level consistent with charter target"}
{"step_id":10,"method_id":"capability.binomial","outputs":{"processZ":2.786,"avgP":0.002672},"status":"success","decision":"baseline capability below target"}
{"step_id":11,"method_id":"capability.binomial","outputs":{"processZ":3.028,"avgP":0.0012318},"status":"success","decision":"sustaining capability at target"}
```

## Submitted route declarations
```json
[]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
