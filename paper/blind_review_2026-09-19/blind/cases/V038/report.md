# Appearance Defect Reduction: Project Status Report

## 1. Can we trust the sound/defective call?

We ran an attribute agreement study: 3 appraisers judged 20 retained units, twice each, against a known answer key. Results:

- Overall agreement (all appraisers vs. the answer key, across both trials): **92.5%**
- Worst-case kappa (appraiser repeatability / vs. standard): **0.733**

By common guidelines, a kappa in the 0.7-0.75 range is **marginal** rather than solidly acceptable (0.75+). One appraiser (appraiser 2) drove this: their repeat agreement with themselves was only 90%, and their agreement with the standard was 95% (kappa 0.867), both lower than the other two appraisers, who were near-perfect. This does not invalidate the data below, but it means a slice of the counted defects could be inspector-to-inspector noise rather than real. We recommend refreshing that inspector's calibration before leaning on tight capability numbers.

## 2. Where the process stood at baseline

Across the 25 archived lots (5,000 units inspected per lot, 125,000 units total, 364 defective):

- A p-chart shows the process was **stable** over this period: centerline **0.2912%** (2,912 DPMO), and **no lots** fell outside the 3-sigma control limits.
- Comparing that rate to the charter's 1,500 DPMO ceiling with a one-proportion test: the baseline rate is **statistically significantly above** the requirement (p ≈ 0, essentially certain).

So the baseline problem was not an unstable process throwing occasional bad lots; it was a stable process running at roughly double the committed defect rate.

## 3. Was one machine driving it?

A chi-square test of association across the four machines (defective vs. sound counts) found no significant relationship between machine and defect status (statistic 3.65, p = 0.302). There is a numeric downward trend in defect rate from machine 1 (0.375%) to machine 4 (0.175%), but with the available counts we cannot call any single machine responsible.

## 4. The change and its immediate trial

A change was tried on one machine. In the trial window (4,000 units before, 4,000 after):

- Defective count went from 3 (0.075%) to 6 (0.15%) — numerically worse.
- A two-proportions test found this difference **not statistically significant** (z = 1.00, p = 0.317).

On its own, this trial neither confirms nor rules out an effect of the change; the counts are too small to say anything with confidence. Taken in isolation it would be a caution flag, not a green light.

## 5. What actually happened after the change: the sustained record

The monitoring record kept since the change (20 subgroups, subgroup sizes ranging 3,200-6,400 units, 97,500 units total, 136 defective) tells a different story than the single trial:

- p-chart centerline: **0.1395%** (1,395 DPMO), roughly half the baseline rate.
- The chart is stable: **no out-of-control points**, and a check for overdispersion (sigmaZ = 1.07, close to the expected 1.0) shows no evidence the variation is worse than binomial, so a Laney adjustment was not needed.
- A one-proportion test against the 1,500 DPMO requirement: p = 0.396 — the sustained rate is **statistically indistinguishable from meeting the charter**.

This is the strongest evidence in the data set: over a much larger sample than the single trial, the process is now running at a level consistent with the commitment, whereas the baseline was clearly and significantly above it.

## 6. What's driving the defects, and where the risk sits

From the reject-category tally (240 tallied rejects across 5 categories):

- **Loose end** is the leading category at **34.2%** of all tallied rejects, ahead of off-weight (17.9%), seam split (17.1%), soft spot (15.4%), and stain (15.4%).

From the FMEA on the five candidate failure modes (severity x occurrence x detection):

- **Seam split** carries the highest risk priority number, **RPN = 336** (severity 6, occurrence 7, detection 8), narrowly ahead of loose end (RPN = 280).

Note the mismatch: loose end is the most *frequent* defect, but seam split scores as the highest *risk* once severity and detection difficulty are weighed in. Both deserve attention, for different reasons — loose end because it is the biggest volume driver, seam split because it is the hardest to catch and the most severe when it happens.

## 7. Bottom line and next steps

- **Where things stand:** the process was stable but running at ~2,912 DPMO at baseline, significantly above the 1,500 DPMO charter commitment. Since a change was introduced on the affected machine, the sustained monitoring record shows ~1,395 DPMO, stable and statistically consistent with meeting the requirement.
- **What's causing it:** no single machine among the four sampled shows a statistically distinguishable defect rate, so the baseline gap looks like a systemic process issue rather than one bad machine. Loose end is the dominant defect by volume; seam split is the dominant risk by FMEA scoring.
- **What was changed and what it achieved:** a change was made to one machine. The isolated before/after trial on that machine alone was inconclusive (not statistically significant, and numerically pointed the wrong way on a small sample). But the larger, longer sustained monitoring record after the change shows a real and durable drop to a rate consistent with the charter. We treat the sustained record, not the small trial, as the credible evidence of impact, since it draws on far more data.
- **How it will be held:** continue the p-chart on the monitoring record as the standing control mechanism; it is currently stable with no out-of-control signals. Because the measurement system's worst-case kappa (0.733) is only marginal, we recommend a calibration refresh for the weaker appraiser so that future control-chart signals can be trusted at face value. Prioritize loose end for volume reduction and seam split for risk mitigation (detection improvement in particular, given its detection rating of 8).

## What we could not verify

All data used in this report came from batches released by the data steward and are reflected in `trace.json`. No batch was denied in this run; every requested topic (inspector judgements, per-lot counts, machine tally, before/after change trial, post-change monitoring record, reject categories, and failure modes) was obtained and analysed. The one soft spot in the evidence is the single before/after trial (Section 4), which was too small to be conclusive on its own — we rely on the larger sustained record for the capability conclusion instead.
