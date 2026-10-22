# Blind item V052

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
# Project Report: Final Inspection Acceptance/Rejection Reliability and Reject Share

## Bottom line
An accept/reject call was **not reliable** in the first study. Agreement was 95.00% overall, overall Cohen's kappa was 0.890, and the weakest appraiser-level kappa was 0.780. The weakest trial-level kappa was 0.659. The accept/reject criteria therefore had to be rewritten before inspection decisions could be relied on. After the rewrite, agreement was 98.33% overall, overall kappa was 0.965, the weakest appraiser-level kappa was 0.947, and the weakest trial-level kappa was 0.894. The rewrite materially improved inspector reliability.

The reject share has held steady across the 25 lots. There were 131 rejects out of 10,000 boards inspected, a rate of 1.31%. The lot median rate was 1.25%, with a standard deviation of 0.556 percentage points. Statistical checks found no shift: the homogeneity chi-square p-value was 0.524, the runs-test p-value was 0.286, and the p-chart had 0 out-of-control lots. The line is therefore not only below its requirement but also stable in the observed window.

The current reject share of 1.31% is below the required 2.00%. The one-proportion test was significant (z = -4.929, p = 0.000000828; exact two-sided p = 0.000000210), and the 95% confidence interval for the reject share was 1.096% to 1.553%. The binomial capability process Z was 2.223. These results indicate the requirement is currently being held with margin.

## Where the mismatches concentrated
Among the 90 mismatches between inspector calls and the answer key, the largest category was insufficient solder: 42 mismatches, or 46.67% of the total. The other categories were solder bridge (16, 17.78%), tombstone (13, 14.44%), component offset (11, 12.22%), and wrong polarity (8, 8.89%). The persistence shown by the before/after agreement studies suggests criteria interpretation was the main reliability issue, and the rewrite addressed it. The mismatch tally shows that insufficient solder should be the first category examined for additional work.

## Placement heads
The two placement heads were not significantly different. Head 1 had 54 rejects in 3,000 placements, a rate of 1.80%; Head 2 had 47 rejects in 3,000 placements, a rate of 1.57%. The two-proportion test gave z = 0.702 and p = 0.482.

## What should be done next
* Hold the rewritten accept/reject criteria in place and continue inspector calibration, because the before/after agreement improvement is the basis for relying on the calls.
* Keep the 25-lot p-chart and homogeneity monitoring in place so that any future shift in reject share is detected.
* Focus improvement work on insufficient solder, the dominant mismatch category, followed by solder bridge and tombstone.
* Continue separate monitoring of both placement heads even though no significant difference is currently observed.

## Data and limitations
The analysis used 3 appraisers, 2 trials, and 20 retained boards in each agreement study, 25 lots, and 3,000 placements per head. All requested shop-floor data batches were released. The process-owner provision channel had no recorded process fact describing the exact wording of the rewritten criteria, so this report cannot specify that wording; it measures the effect of the rewrite through the before/after agreement studies rather than assuming an undocumented mechanism.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"stage_id":"study_1","ratings":120,"appraisers":3,"trials":2,"boards":20},"method_id":"msa.attribute_agreement","outputs":{"kappaMin":0.7802197802,"agreementPct":95.0,"overallKappa":0.8901098901,"overallAgreementPct":95.0,"minAppraiserKappa":0.7802197802,"maxAppraiserKappa":0.9459459459,"minAppraiserAgreementPct":90.0,"maxAppraiserAgreementPct":97.5,"minTrialKappa":0.6590909091,"minTrialAgreementPct":85.0,"appraiserCount":3,"trialCount":2,"boardCount":20,"ratingCount":120},"status":"success","decision":"Before rewrite: overall agreement 95.00 percent and overall kappa 0.890; weakest appraiser kappa 0.780."}
{"step_id":2,"inputs_digest":{"stage_id":"study_2","ratings":120,"appraisers":3,"trials":2,"boards":20},"method_id":"msa.attribute_agreement","outputs":{"kappaMin":0.9473684211,"agreementPct":98.3333333333,"overallKappa":0.965034965,"overallAgreementPct":98.3333333333,"minAppraiserKappa":0.9473684211,"maxAppraiserKappa":1.0,"minAppraiserAgreementPct":97.5,"maxAppraiserAgreementPct":100.0,"minTrialKappa":0.8936170213,"minTrialAgreementPct":95.0,"appraiserCount":3,"trialCount":2,"boardCount":20,"ratingCount":120},"status":"success","decision":"After rewrite: overall agreement 98.33 percent, overall kappa 0.965, weakest appraiser kappa 0.947."}
{"step_id":3,"inputs_digest":{"stage_id":"lots","lots":25,"totalInspected":10000,"totalRejected":131},"method_id":"basic.descriptive_summary","outputs":{"mean":0.0131,"median":0.0125,"stdDev":0.0055565277,"skewness":0.7354284315,"adPValue":0.2716773932,"meanPct":1.31,"medianPct":1.25,"stdDevPct":0.5556527693,"minProportion":0.005,"minPct":0.5,"maxProportion":0.0275,"maxPct":2.75,"lotCount":25,"totalInspected":10000,"totalRejected":131,"meanCount":5.24,"varianceCounts":4.94,"expectedVarianceUnderPbar":5.171356},"status":"success","decision":"Lot reject share averaged 1.31 percent across 25 lots."}
{"step_id":4,"inputs_digest":{"stage_id":"lots","lots":25,"totalInspected":10000,"test":"homogeneity_of_reject_proportions"},"method_id":"tables.chisquare_assoc","outputs":{"statistic":22.9262885789,"pValue":0.5241529976,"degreesOfFreedom":24},"status":"success","decision":"No evidence that reject share differs across lots."}
{"step_id":5,"inputs_digest":{"stage_id":"lots","subgroups":25,"centerLine":0.0131},"method_id":"control_chart.p","outputs":{"centerLine":0.0131,"outOfControlCount":0,"upperControlLimit":0.0301554617,"upperControlLimitPct":3.0155461735,"lowerControlLimit":0.0,"controlChartSubgroups":25},"status":"success","decision":"No out-of-control lots in the p-chart."}
{"step_id":6,"inputs_digest":{"stage_id":"lots","subgroups":25,"cutoff":"mean"},"method_id":"nonparametric.runs_test","outputs":{"pValue":0.2864220228,"runs":16,"nAbove":10,"nBelow":15,"zStatistic":1.0660035818},"status":"success","decision":"No evidence of nonrandom clustering across lot counts."}
{"step_id":7,"inputs_digest":{"stage_id":"lots","totalInspected":10000,"totalRejected":131,"targetProportion":0.02},"method_id":"basic.one_proportion","outputs":{"pValue":8.283305126e-07,"zStatistic":-4.9285714286,"observedProportion":0.0131,"targetProportion":0.02,"totalInspected":10000,"totalRejected":131,"exactPValue":2.095021886e-07,"exactOneSidedPValue":9.80374817e-08,"ci95Low":0.0109641385,"ci95High":0.0155259472},"status":"success","decision":"Overall reject share is significantly below the required 2.00 percent."}
{"step_id":8,"inputs_digest":{"stage_id":"lots","totalInspected":10000,"totalRejected":131,"targetProportion":0.02},"method_id":"capability.binomial","outputs":{"processZ":2.2232343755,"avgP":0.0131,"targetP":0.02,"zAgainstTarget":4.9285714286,"totalInspected":10000,"totalRejected":131},"status":"success","decision":"Observed reject rate corresponds to a binomial process Z of 2.223."}
{"step_id":9,"inputs_digest":{"stage_id":"heads","head1Placed":3000,"head2Placed":3000,"head1Rejected":54,"head2Rejected":47},"method_id":"basic.two_proportions","outputs":{"pValue":0.4823901395,"zStatistic":0.7024635275,"head1Proportion":0.018,"head2Proportion":0.0156666667,"head1Pct":1.8,"head2Pct":1.5666666667,"head1Rejected":54,"head1Placed":3000,"head2Rejected":47,"head2Placed":3000,"difference":0.0023333333,"pooledProportion":0.0168333333},"status":"success","decision":"No statistically significant difference between the two placement heads."}
{"step_id":10,"inputs_digest":{"stage_id":"disagreements","categories":5,"totalCount":90},"method_id":"quality.pareto","outputs":{"topCategoryPct":46.6666666667,"topCategoryCount":42,"totalCount":90,"insufficientSolderPct":46.6666666667,"insufficientSolderCount":42,"solderBridgeCount":16,"solderBridgePct":17.7777777778,"tombstoneCount":13,"tombstonePct":14.4444444444,"componentOffsetCount":11,"componentOffsetPct":12.2222222222,"wrongPolarityCount":8,"wrongPolarityPct":8.8888888889},"status":"success","decision":"Insufficient solder is the largest mismatch category at 46.67 percent of mismatches."}
```

## Submitted route declarations
```json
[{"point":"accept_reject_reliability","chosen_branch":"criteria_rewrite_improved_agreement","observed":{"beforeKappaMin":0.7802197802,"afterKappaMin":0.9473684211,"beforeAgreementPct":95.0,"afterAgreementPct":98.3333333333}},{"point":"reject_share_stability","chosen_branch":"no_evidence_of_shift","observed":{"chiSquarePValue":0.5241529976,"runsPValue":0.2864220228,"pChartOutOfControlCount":0}},{"point":"level_vs_required","chosen_branch":"below_required_level","observed":{"observedProportion":0.0131,"targetProportion":0.02,"oneProportionPValue":8.283305126e-07}},{"point":"placement_head_difference","chosen_branch":"no_significant_difference","observed":{"pValue":0.4823901395,"zStatistic":0.7024635275}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
