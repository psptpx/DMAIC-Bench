# Blind item V019

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
# Final-inspection project status

## Bottom line

The visual accept/reject call is **usable with qualification**. It was not assumed: the first gate was an attribute measurement-system study, and its pooled appraiser-to-standard results were 115 matches among 120 calls (95.8333% agreement) with minimum kappa 0.89899. The system still had error: 3 false accepts and 2 false rejects.

Rewriting the accept/reject criteria did not prove a statistically significant accuracy gain. Accuracy rose to 117/120 (97.5%), but the 1.6667 percentage-point change had p = 0.47202. The observed false rejects fell from 2 to 0; false accepts remained at 3. Thus, the call can support project decisions, but false accepts and inconsistent trials must continue to be managed.

The full 25-lot series was not steady: lot 13 had 38 rejects among 400 (9.5%) and was the single high p-chart signal. The other 24 lots had no 3-sigma outlier and averaged 141/9,600 (1.46875%). Across all 25 lots, the rate was 179/10,000 (1.79%), below the 2.0% requirement on point estimate, but its confidence interval was 1.53925% to 2.06936% and therefore still crossed the requirement.

Today's two-head window was 105 rejects among 6,000 placements (1.75%). This is 0.25 percentage points below the requirement and statistically unchanged from the archive (p = 0.85283), but its confidence interval was 1.43350% to 2.11457%, also crossing 2.0%. The correct business message is favorable current performance, not demonstrated long-term capability with margin.

## What had to be fixed before the call could be trusted

The baseline study compared each inspector's calls with an agreed answer key. It found 5 mismatches among 120 calls, comprising 3 false accepts and 2 false rejects. At the individual-trial level, the weakest result was 18 matches among 20 (90%) with kappa 0.79798. This was sufficient to proceed with analysis, but not evidence that inspection was perfect.

The disagreement tally showed where clarification was needed. Of 90 differing calls, insufficient solder accounted for 46, or 51.1111%. The remaining counts were component offset 14, tombstone 12, solder bridge 9, and wrong polarity 9. The first four categories totaled 81, or 90%, so the rewrite had to cover multiple boundary conditions rather than one isolated defect type.

After the rewrite, accuracy was 117/120, the minimum pooled appraiser kappa was 0.875, and false rejects were 0. However, false accepts remained at 3, and the weakest trial was again 18/20 (90%) with kappa 0.736842. The improvement in total agreement was not statistically significant. The change should therefore be treated as a criteria/clarification intervention with no proven accuracy gain, not as a completed measurement-system fix.

## Whether the reject level held steady

The p-chart center line for all 25 lots was 1.79%, with an upper control limit of 3.77882%. Lot 13 rejected 38/400 (9.5%); the exact probability of 38 or more at the chart center line was 1.66e-16. It is a clear high special cause. Lot 15 had 0 rejects, but the computed lower limit was truncated at zero, so no lower out-of-control claim is made for a point at that boundary.

The runs-around-median check had 11 runs versus an expected 13 and p = 0.40380, providing no evidence of an additional nonrandom pattern. Excluding special-cause lot 13, the remaining 24 lots averaged 1.46875%, had no 3-sigma outlier, and had a confidence interval from 1.23771% to 1.72988%. The retained series is statistically below the 2% requirement (lower-tail p = 0.0000595916). In practical terms: one exceptional lot destabilized the full archive; the rest of the series appears steady and below the requirement.

No process fact explaining lot 13 was released. There is no data on its material, head, operator, settings, corrective action, or closure. The analysis therefore stops at “special statistical cause” and cannot honestly assign a physical cause.

## Today's level and placement heads

Head 1 rejected 56/3,000 (1.8667%) and head 2 rejected 49/3,000 (1.6333%). The difference was 0.2333 percentage points, z = 0.68919 and p = 0.49071, so this window does not identify either head as the problem. Combining them gives 105/6,000 (1.75%). That is 0.25 percentage points below the requirement and unchanged from the archive rate (difference -0.04 percentage points; p = 0.85283), but its confidence interval is 1.43350% to 2.11457% and still crosses 2%.

## Next actions

- Close lot 13's special cause: retrieve lot traceability, material records, placement-head logs, maintenance records, and corrective-action closure evidence. Keep both the all-lot and special-cause-removed views until that investigation is complete.
- Run the p chart routinely at the current lot size and investigate upper-limit signals or sustained shifts; do not manage solely by comparing a single lot with 2%.
- Prioritize false accepts in recurring calibration, using retained boundary examples led by insufficient solder, then the other high-count categories.
- Keep the rewritten criteria and answer key under control. Continue reporting pooled appraiser-to-standard agreement, worst-trial behavior, false accepts, and false rejects—not total agreement alone.
- Collect sequential placement-head subgroups before taking head-specific action; the present head comparison is not significant.
- Declare long-term capability only when the upper confidence bound is below 2% under an agreed stable-period rule. The current all-lot and today windows have not met that evidence standard.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"define","records":1},"method_id":"meta.data_profiling","outputs":{"requiredRejectShare":0.02,"requiredRejectSharePct":2.0},"status":"success","decision":"Required reject share is 0.02."}
{"step_id":2,"inputs_digest":{"batch":"study_1","items":20,"appraisers":3,"trials":2,"ratings":120},"method_id":"msa.attribute_agreement","outputs":{"kappaMin":0.8989898989898989,"agreementPct":95.83333333333333,"agreementCount":115,"mismatchCount":5,"items":20,"appraisers":3,"trials":2,"totalRatings":120,"worstTrialAgreementCount":18,"worstTrialAgreementPct":90.0,"worstTrialKappa":0.797979797979798,"falseAccepts":3,"falseRejects":2,"falseAcceptPct":2.5,"falseRejectPct":1.6666666666666667,"falseAcceptSharePct":2.5,"falseRejectSharePct":1.6666666666666667},"status":"success","decision":"Pooled appraiser-to-standard agreement supports using the calls; residual error remains."}
{"step_id":3,"inputs_digest":{"batch":"disagreements","categories":5,"disagreements":90},"method_id":"quality.pareto","outputs":{"topCategoryPct":51.111111111111114,"total":90,"categoryCount":5,"topCategoryCount":46,"secondCategoryCount":14,"thirdCategoryCount":12,"fourthCategoryCount":9,"fifthCategoryCount":9,"secondCategoryPct":15.555555555555555,"thirdCategoryPct":13.333333333333334,"fourthCategoryPct":10.0,"fifthCategoryPct":10.0,"topFourCount":81,"topFourCumulativePct":90.0,"topFourCategoryCount":4},"status":"success","decision":"Insufficient solder dominates; four categories cover 90%."}
{"step_id":4,"inputs_digest":{"batch":"study_2","items":20,"appraisers":3,"trials":2,"ratings":120},"method_id":"msa.attribute_agreement","outputs":{"kappaMin":0.875,"agreementPct":97.5,"agreementCount":117,"mismatchCount":3,"items":20,"appraisers":3,"trials":2,"totalRatings":120,"worstTrialAgreementCount":18,"worstTrialAgreementPct":90.0,"worstTrialKappa":0.7368421052631579,"falseAccepts":3,"falseRejects":0,"falseAcceptPct":2.5,"falseRejectPct":0.0,"falseAcceptSharePct":2.5,"falseRejectSharePct":0.0},"status":"success","decision":"Post-rewrite calls remain usable; false accepts remain and worst-trial kappa is marginal."}
{"step_id":5,"inputs_digest":{"batches":["study_1","study_2"],"correct":[115,117],"total":[120,120]},"method_id":"basic.two_proportions","outputs":{"pValue":0.4720208091290236,"zStatistic":-0.7191949522280737,"baselineAgreementPct":95.83333333333334,"postAgreementPct":97.5,"absoluteDifferencePct":1.6666666666666607},"status":"success","decision":"The accuracy improvement is not statistically significant."}
{"step_id":6,"inputs_digest":{"batch":"lots","lots":25,"inspections":10000},"method_id":"control_chart.p","outputs":{"lotCount":25,"totalInspected":10000,"totalRejected":179,"centerLine":0.0179,"upperControlLimit":0.03778820693275289,"lowerControlLimit":0.0,"initialOutOfControlCount":2,"computedTailPValue":0.0},"status":"failed","decision":"Numerical underflow invalidated the tail estimate, and equality at a truncated lower limit was incorrectly counted; corrected below."}
{"step_id":7,"inputs_digest":{"batch":"lots","lots":25,"inspections":10000},"method_id":"control_chart.p","outputs":{"centerLine":0.0179,"outOfControlCount":1,"upperControlLimit":0.03778820693275289,"lowerControlLimit":0.0,"sigmaMultiplier":3.0,"signalLot":13,"signalLotInspected":400,"signalLotRejected":38,"signalLotRejectShare":0.095,"signalLotUpperTailPValue":1.6604896986887467e-16,"zeroRejectLot":15,"zeroRejectCount":0,"zeroLotLowerTailPValue":0.0007282565795946638,"signalLotRejectSharePct":9.5},"status":"success","decision":"Only lot 13 is above the upper control limit."}
{"step_id":8,"inputs_digest":{"batch":"lots","lots":25,"inspections":10000,"rejects":179},"method_id":"capability.binomial","outputs":{"processZ":2.099191761058102,"avgP":0.0179,"targetProcessZ":2.0537489106318225,"observedMinusTarget":-0.002100000000000001,"exactLowerTailAtTarget":0.06966966938728753,"exactUpperTailAtTarget":0.9397044687382266,"ci95Lower":0.015392459771213096,"ci95Upper":0.020693613394785426,"confidenceLevel":0.95,"confidenceLevelPct":95.0,"avgPct":1.79,"upperControlLimitPct":3.778820693275289,"observedMinusTargetPct":-0.2100000000000001,"ci95LowerPct":1.5392459771213096,"ci95UpperPct":2.0693613394785424},"status":"success","decision":"The all-lot point estimate is below 2%, but its confidence interval includes 2%."}
{"step_id":9,"inputs_digest":{"batch":"lots","attemptedSummaryCount":3},"method_id":"capability.binomial","outputs":{"confidenceLevelPct":95.0},"status":"failed","decision":"The script failed on an invalid normal-distribution method before producing results; corrected below."}
{"step_id":10,"inputs_digest":{"batch":"lots","excludedLot":13,"lots":24},"method_id":"control_chart.p","outputs":{"lotCount":24,"totalInspected":9600,"totalRejected":141,"centerLine":0.0146875,"outOfControlCount":0,"upperControlLimit":0.032732305076098075,"lowerControlLimit":0.0,"avgPct":1.46875,"observedMinusTargetPct":-0.5312500000000004,"ci95LowerPct":1.2377103001416743,"ci95UpperPct":1.7298783183000406,"exactLowerTailAtTarget":5.9591646053009476e-05},"status":"success","decision":"After excluding lot 13, no remaining lot is outside 3-sigma limits."}
{"step_id":11,"inputs_digest":{"batch":"lots","excludedLot":13,"inspections":9600,"rejects":141},"method_id":"capability.binomial","outputs":{"processZ":2.1784170723087564,"avgP":0.0146875,"targetProcessZ":2.0537489106318225,"observedMinusTarget":-0.005312500000000001,"exactLowerTailAtTarget":5.9591646053009476e-05,"exactUpperTailAtTarget":0.9999572308619642,"ci95Lower":0.012377103001416742,"ci95Upper":0.017298783183000405,"confidenceLevel":0.95,"confidenceLevelPct":95.0},"status":"success","decision":"The 24 lots excluding special cause are statistically below the requirement."}
{"step_id":12,"inputs_digest":{"batch":"heads","heads":2,"placementsPerHead":3000},"method_id":"basic.two_proportions","outputs":{"pValue":0.490705562532215,"zStatistic":0.6891870541365993,"head1Rejects":56,"head1Placements":3000,"head1RejectShare":0.018666666666666668,"head2Rejects":49,"head2Placements":3000,"head2RejectShare":0.01633333333333333,"absoluteDifferencePct":0.23333333333333367,"avgPct":1.75,"observedMinusTargetPct":-0.249999999999999,"ci95LowerPct":1.4334999663436494,"ci95UpperPct":2.1145667115406606,"firstHeadID":1,"secondHeadID":2,"head1RejectSharePct":1.8666666666666667,"head2RejectSharePct":1.6333333333333333},"status":"success","decision":"No statistically significant placement-head difference."}
{"step_id":13,"inputs_digest":{"batch":"heads","heads":2,"placements":6000,"rejects":105},"method_id":"capability.binomial","outputs":{"processZ":2.10835839916911,"avgP":0.0175,"targetProcessZ":2.0537489106318225,"observedMinusTarget":-0.0024999999999999988,"exactLowerTailAtTarget":0.0885381871091673,"exactUpperTailAtTarget":0.9259241808643697,"ci95Lower":0.014334999663436493,"ci95Upper":0.021145667115406604,"confidenceLevel":0.95,"confidenceLevelPct":95.0,"differencePct":-0.03999999999999976,"totalRejected":105,"totalInspected":6000,"observedMinusTargetPct":-0.25,"absoluteMarginBelowTargetPct":0.25},"status":"success","decision":"Today is below 2% on point estimate, but its confidence interval includes 2%."}
{"step_id":14,"inputs_digest":{"batches":["lots","heads"],"archive":[179,10000],"today":[105,6000]},"method_id":"basic.two_proportions","outputs":{"pValue":0.8528296732550668,"zStatistic":-0.18550918940839173,"archiveShare":0.0179,"todayShare":0.0175,"difference":-0.0003999999999999976,"differencePct":-0.03999999999999976},"status":"success","decision":"Today is statistically indistinguishable from the archive rate."}
{"step_id":15,"inputs_digest":{"batch":"lots","lots":25,"nonmedianLots":24},"method_id":"nonparametric.runs_test","outputs":{"pValue":0.4038037971630485,"median":6,"usedLots":24,"aboveMedian":12,"belowMedian":12,"runCount":11,"expectedRuns":13.0,"zStatistic":-0.834847109936722},"status":"success","decision":"No evidence of nonrandom clustering is found by the runs test."}
{"step_id":16,"inputs_digest":{"batches":["study_1","study_2"],"totalRatingsPerStudy":120},"method_id":"msa.attribute_agreement","outputs":{"baselineFalseAccepts":3,"baselineFalseRejects":2,"baselineFalseAcceptPct":2.5,"baselineFalseRejectPct":1.6666666666666667,"postFalseAccepts":3,"postFalseRejects":0,"postFalseAcceptPct":2.5,"postFalseRejectPct":0.0},"status":"success","decision":"The rewrite removed observed false rejects; false accepts remained unchanged."}
{"step_id":17,"inputs_digest":{"batches":["study_1","study_2"],"trialCount":6},"method_id":"msa.attribute_agreement","outputs":{"baselineMinTrialKappa":0.797979797979798,"postMinTrialKappa":0.7368421052631579,"baselineMinTrialAgreementCount":18,"baselineMinTrialAgreementPct":90.0,"postMinTrialAgreementCount":18,"postMinTrialAgreementPct":90.0},"status":"success","decision":"Worst-trial performance warrants continued calibration despite pooled acceptability."}
{"step_id":18,"inputs_digest":{"batches":["study_1","study_2"],"withinPairs":6,"betweenPairs":12},"method_id":"msa.attribute_agreement","outputs":{"baselineMinWithinKappa":0.797979797979798,"postMinWithinKappa":0.7368421052631579,"baselineMinBetweenKappa":0.6938775510204082,"postMinBetweenKappa":0.7368421052631581},"status":"success","decision":"Repeatability and reproducibility remain imperfect after the rewrite."}
```

## Submitted route declarations
```json
[{"point":"measurement_gate","chosen_branch":"obtain and analyze baseline attribute study before lot data","observed":{"baselineAgreementPct":95.83333333333333,"kappaMin":0.8989898989898989}},{"point":"special_cause","chosen_branch":"retain all-lot result and separately report lot-13 exclusion","observed":{"allLotCenterLine":0.0179,"signalLot":13,"excludedCenterLine":0.0146875}},{"point":"placement_heads","chosen_branch":"do not differentiate heads from current window","observed":{"head1RejectShare":0.018666666666666668,"head2RejectShare":0.01633333333333333,"pValue":0.490705562532215}},{"point":"lot_13_process_fact","chosen_branch":"report the process explanation as missing","observed":{"billedTurnsUsed":1,"matchingProcessFacts":0}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
