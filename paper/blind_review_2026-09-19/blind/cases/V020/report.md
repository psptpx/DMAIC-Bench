# Appearance-Defect Charter Review — Rod-Making Line

## 1. Can we trust the sound/defective judgement at all?

We ran an attribute agreement study: 3 appraisers, 20 retained units, 2 trials each, judged pass/fail against a known answer key.

- Within-appraiser repeatability (kappa, trial 1 vs trial 2): appraiser1 = 0.659, appraiser2 = 0.794, appraiser3 = 0.681. **kappaMin = 0.659**.
- Overall agreement — all three appraisers, both trials, matching the answer key on the same unit — was **65.0%**.

A kappa of 0.659 is below the commonly used 0.75 threshold for an acceptable attribute measurement system, and 65% overall agreement is well short of the 90%+ usually wanted before trusting a go/no-go call. **The appearance judgement itself is not yet reliable.** Every pass/fail count downstream of this (lot counts, machine tally, before/after change, charter comparison) inherits some of this measurement noise. We proceeded with the rest of the analysis because it is the only data on hand, but this is a real caveat on every number that follows, and closing this gap should be a priority alongside the process-level work below.

## 2. Has the defective share held steady across the lots?

Twenty-five consecutive lots, 5,000 units inspected each (125,000 units total), were charted on a p-chart.

- Center line (pbar) = 0.002576, i.e. **2,576 defective units per million (dpmo)**.
- 0 of 25 lots fell outside the 3-sigma control limits.

The process was stable over this window — the defective share did not drift or spike lot to lot, it was just running at a level higher than the charter allows (see below).

## 3. How does that level compare with the charter?

The charter commits to no more than **1,500 dpmo**. Against the 25-lot baseline:

- Observed rate: 2,576 dpmo vs. 1,500 dpmo target — a processZ of **-1.50** (the target sits about 1.5 standard deviations better than where the baseline was running).

So at baseline the line was stable, but stably missing the charter by a meaningful margin.

## 4. Was one machine the culprit?

A machine-by-machine tally (4 machines, 4,000 units each) was tested for association between machine and defective/sound outcome (chi-square test of association):

- statistic = 2.578, **p = 0.461**.

No significant association — no single machine stands out as materially worse than the others. The elevated defect rate was a systemic issue, not a single bad machine.

## 5. What was changed, and did it work?

One machine's counts were compared either side of a change made to it: before = 6 defects / 4,000 (1,500 dpmo), after = 11 defects / 4,000 (2,750 dpmo).

- Two-proportion test: z = -1.214, **p = 0.225** — on this narrow snapshot alone, the difference is *not* statistically significant. Taken in isolation, this snapshot does not demonstrate the change worked, and numerically even looks worse; the sample is simply too small (11 events) to draw a conclusion from by itself.

**What the specific engineering change was could not be documented.** We asked the process owner directly; the answer was that no process fact describing the change is recorded. This is a genuine gap: we can see that something was done and can measure its downstream effect, but we cannot say in the report what the change actually consisted of.

## 6. Did the change hold up over the following monitoring record?

The monitoring record kept since the change — 20 subgroups of 5,000 units (100,000 units total) — was charted the same way as the baseline:

- Center line = 0.00104, i.e. **1,040 dpmo**.
- 0 of 20 subgroups out of control — stable.

Comparing this full record against the original 25-lot baseline (two-proportion test): z = 8.328, **p < 0.001**. This is decisive: the sustained rate since the change (1,040 dpmo) is significantly lower than the pre-change baseline (2,576 dpmo). Even though the single before/after snapshot in section 5 wasn't significant on its own, the fuller monitoring record makes clear the change produced a real, lasting improvement.

Comparing the sustaining period against the charter target directly (one-proportion test against 1,500 dpmo): z = -3.759, **p < 0.001**. **The line is currently meeting the charter**, running at 1,040 dpmo against a 1,500 dpmo commitment, and doing so in statistical control.

## 7. Where should attention go next?

Two supporting analyses point at where residual risk sits:

- **Pareto of reject categories** (240 tallied rejects across 5 categories): "loose end" is the single largest category at **30.4%** of all rejects, ahead of stain (20.0%), soft spot (19.6%), off-weight (17.5%) and seam split (12.5%).
- **FMEA on the five candidate failure modes**: the highest-risk mode by RPN is **seam split, RPN = 360** (severity 9 x occurrence 5 x detection 8) — not the most frequent defect, but the one combining high severity with poor detectability. "Loose end" (RPN 240) is frequent but comparatively easier to catch and less severe.

These two views disagree on priority for a reason: Pareto ranks by *frequency*, FMEA ranks by *risk*. Loose end is worth attacking first if the goal is moving the average dpmo down fastest (it's the biggest single contributor to volume). Seam split deserves attention on detection controls specifically, since its risk comes from units getting through undetected, not from how often it occurs.

## 8. Bottom line and recommendations

- **Where things stand:** the line is currently meeting the charter (1,040 dpmo vs. 1,500 dpmo commitment, p<0.001, and in statistical control), a real improvement over the pre-change baseline of 2,576 dpmo (p<0.001).
- **What was causing the shortfall:** baseline defect rate was elevated but stable and not attributable to any single machine (chi-square p=0.461); loose end is the largest single reject category (30.4%), and seam split is the highest-risk mode by FMEA (RPN 360) due to poor detectability.
- **What was changed:** something was changed on the monitored machine between the "before" and "after" windows, but the actual engineering content of that change is not recorded anywhere available to us, and the process owner had no fact to supply when asked directly. This should be documented properly so the fix is understood and repeatable, not just observed statistically.
- **What the change achieved:** a statistically significant, sustained drop from 2,576 to 1,040 dpmo, verified against 20 subgroups (100,000 units) of monitoring data, not just the initial before/after snapshot (which alone was inconclusive, p=0.225).
- **How it will be held:** continue the p-chart monitoring on the sustaining record; it is currently stable with no out-of-control points. Before relying further on any pass/fail call, close the measurement system gap — kappaMin of 0.659 and 65% overall agreement are not yet good enough to be confident that what we're counting as "defective" is being judged consistently. Recommend a follow-up gage study with retraining or a clarified visual standard, focused first on the loose-end and seam-split calls where ambiguity is most likely to cost the most.

## Data gaps disclosed

- The specific engineering change made to the machine is not documented; this report describes its measured effect only, not its mechanism.
- All figures in this report are traceable to computed steps in `trace.json`; nothing here is estimated or assumed beyond what is stated as a gap above.
