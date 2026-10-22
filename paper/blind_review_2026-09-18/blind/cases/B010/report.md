# Breach-response improvement: management assessment

## Executive conclusion
The project remains in measurement and investigation, not validated improvement or control. The historical breach share is **4.56%**, below the **5%** internal ceiling by **0.44 percentage points**, but the process is **not steady**. That average is not assurance of future compliance. Reviewer decisions are useful but not uniformly dependable; calibration and adjudication are needed before strong operational conclusions.

## Can breach judgements be trusted?
The answer-key study covers **20 tickets**, **3 reviewers**, and **120 judgements**. Overall individual-judgement accuracy is **95%**. Cohen kappa was computed separately for each reviewer against the key, pooling their repeated trials; repeatability is exact agreement between their trials.

| Reviewer | Accuracy | Repeatability | Kappa against key |
|---|---:|---:|---:|
| First | 90% | 80% | 0.7647 |
| Second | 97.5% | 95% | 0.9355 |
| Third | 97.5% | 95% | 0.9310 |

The minimum kappa is **0.7647**. The weaker reviewer's inconsistencies mean this is not an unqualified measurement-system pass. Overall accuracy must not conceal reviewer-specific risk. These repeated ratings are not independent new tickets, and the study does not establish field-wide error rates. Reconcile disagreements with the answer key, clarify ambiguous breach rules, retrain, and repeat a blinded study on representative tickets. Audit the recorded spike against source timestamps before assigning an operational cause.

## Is the share steady?
A binomial p chart used all **25 periods**, each containing **200 tickets**: **228 breaches in 5,000 tickets**. The weighted center line is **0.0456**, with lower and upper control limits **0.001346** and **0.089854**. The conventional three-sigma point rule flagged **1 period**: period **13**, with **44 breaches**, a proportion of **0.22**.

This is evidence against a stable baseline, not a diagnosis of its cause. Limits describe expected variation, not the contractual or internal requirement. No run-pattern analysis was performed. No observation was removed, and no revised baseline was computed. Investigate the flagged period's timestamps, workflow, staffing, outages, intake mix, and classification decisions; those are investigation hypotheses, not established causes.

## Distance from the requirement
The pooled historical share is **4.56%**, versus the **5%** ceiling. The unshifted normal-equivalent binomial process Z is **1.6891**. This is a descriptive transformation of observed yield, not a validated predictive capability index under instability.

An exact one-sided binomial test of exceedance gives **p = 0.92944**. The nominal exact pooled interval for the breach probability is **[0.039984, 0.051753]**. Failure to establish exceedance is not proof of compliance; furthermore, a constant independent ticket probability is questionable given the chart signal. There is no separately identified current or post-change window, so these calculations describe the export, not a proven new operating level.

## What is causing it?
The common-window team summary has **30 breaches from 600 tickets** for the first team (**5%**) and **24 from 600** for the second (**4%**). A two-sided pooled two-proportion z test without continuity correction gives **z = 0.83551**, **p = 0.40343**. The estimated difference in proportions is **0.0100**, with nominal unpooled Wald interval **[-0.013451, 0.033451]**.

This does not establish a team difference, nor does it establish equivalence. The aggregate comparison cannot explain the flagged period or separate workload mix from process effects. Do not blame a team or transfer its practices as a proven remedy on this evidence.

## What changed, what did it achieve, and how will it be held?
No implemented change or distinct post-change validation dataset was obtained. The improvement request merely re-served the original period counts; those are not evidence of a change. The special-cause investigation and control-plan requests were unroutable, and the owner had no matching recorded process fact. These are access/evidence gaps, not confirmed steward `denied` batches. Consequently the conclusion stops before verified root cause, intervention effectiveness, or sustained control. No improvement benefit is claimed.

Recommended next actions, not completed work:

- Assign the quality lead to reviewer calibration and independent adjudication of questionable classifications.
- Assign the process owner to a documented investigation of the flagged period; retain it in the baseline until an assignable cause and disposition are justified.
- Collect ticket-level timing, workflow and intake attributes linked to periods and teams. Validate an actionable cause before choosing a targeted pilot.
- Predefine pilot success criteria against the internal ceiling, measurement reliability, and stability; preserve comparable denominators and account for intake mix.
- After verified correction, collect prospective follow-up data and establish justified control limits. Use a denominator-adjusted p chart, with named monitoring ownership, an escalation procedure for signals, source-record checks, and documented corrective actions. Reassess capability only after a stable, trustworthy baseline exists.

## Computation provenance
All numerical findings above are recorded in `trace.json`, under attribute agreement, p-chart, descriptive binomial capability, one-proportion testing, and two-proportion testing. Computations are reproducible using `analyze.py` and the steward-released JSON batches. Recommendations and investigation hypotheses have not been presented as computed findings.
