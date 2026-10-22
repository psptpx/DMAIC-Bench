# Final Inspection Reject-Share Project Report

## Data received
All requested batches were received: the project charter, the first inspector agreement study, the disagreement tally by reject category, the per-lot inspected/rejected counts, the second agreement study, and the placement-head counts.

## 1. Can an accept/reject call be relied on?
In the first agreement study, overall agreement with the answer key was **95.83%** (**115** of **120** ratings). Fleiss kappa was **0.831**, the lowest appraiser-versus-standard kappa was **0.899**, and the weakest kappa overall was **0.798**. This showed that the accept/reject criteria still allowed some disagreement and that the criteria needed to be rewritten before calls could be relied on consistently.

After the criteria rewrite, the second study showed overall agreement of **97.5%** (**117** of **120** ratings), Fleiss kappa **0.875**, the lowest appraiser-versus-standard kappa was **0.875**, and the weakest kappa overall was **0.737**. This was an improvement, but the lowest within-appraiser kappa was still **0.737**, so one appraiser's repeatability remains weaker than the others. The criteria rewrite helped, but calibration should continue for that appraiser. Because the weakest kappa remained low, accept/reject calls should not yet be treated as fully reliable; calibration for the weaker appraiser must be completed and re-verified.

## 2. Where are the disagreements concentrated?
The disagreement tally contained **90** items. The largest category was **insufficient solder** with **46** disagreements, or **51.11%** of all disagreements. The top two categories accounted for **66.67%** of disagreements. This points to insufficient-solder calls as the main priority for criteria clarification and training.

## 3. Has the reject share held steady across lots?
The archive contained **25** lots of **400** boards each, with **179** rejected boards in **10000** inspected boards, for an overall reject share of **1.79%**. The p-chart center line was **1.79%** and the upper control limit was **3.78%**. Lot **13** was the single out-of-control point, with **38** rejects, or **9.5%**. There was no linear trend over the lots: correlation coefficient **0.0761**, p-value **0.7176**. The process was broadly stable except for the special-cause lot.

## 4. How does today's level compare with the required reject share?
The required reject share is **2.0%**. The latest inspected lot had **10** rejects in **400** boards, or **2.5%**, above the point-estimate requirement. However, a one-sided exact test gave p-value **0.2821**, and the **95%** confidence interval for that lot was **1.21%** to **4.55%**, so the evidence does not establish that the latest true rate is above the requirement.

The overall binomial capability result was **2.099** process Z against a target Z of **2.054**, consistent with the overall **1.79%** rate being at or better than the required level. The latest lot's process Z was **1.96**, below the target Z, so the latest observation deserves follow-up even though it is not statistically conclusive.

## 5. Do the two placement heads differ?
Head 1 had **56** rejects in **3000** placements (**1.87%**), while head 2 had **49** rejects in **3000** placements (**1.63%**). The difference was not statistically significant: z-statistic **0.689**, p-value **0.491**. Placement head is not an evident driver of the reject share.

## 6. Recommended next steps
1. Investigate the lot **13** special cause and confirm whether it represents a process upset or a recording issue.
2. Focus immediate improvement activity on the **insufficient solder** category, which alone accounts for **51.11%** of disagreements.
3. Continue calibration with the appraiser whose repeatability kappa was **0.737**, and verify that the rewritten criteria are being applied uniformly.
4. Keep the p-chart in place to hold the overall reject share at or below **2.0%** and to detect further special causes.
5. Collect additional recent lots before declaring the latest **2.5%** point a true shift above the required level.
