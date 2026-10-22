# Blind item V044

Focal assessment: Whether before/after comparisons support improvement conclusions.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team on a chip-capacitor line. Every unit is inspected and the project has committed to holding the defect share at or below 0.25% of units inspected. On file are the inspected and defective counts for twenty-five consecutive baseline lots; a per-lot record of two line settings alongside that lot's defect share; the inspected and defective totals for one window before a change was made to the line and one window after it; the inspected and defective counts for twenty lots run since the change; and the size and risk level the before-and-after trial was run at.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the defect share held steady across the baseline, how it compares with what was committed to, whether anything on file accounts for it, whether the change that was made can be shown to have done anything, whether the level reached since is enough, and what should happen next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
{"screening_significant":{"field":"any_factor_significant","op":"==","value":true,"source":"Montgomery DAOE 6e 11.2"},"stability_pass":{"field":"stable","op":"==","value":true,"source":"AIAG SPC-2 Ch. I Sec. F; Montgomery ISQC 6e 8.1"}}
```

## Submitted report (complete, identifiers removed)
# Chip-capacitor defect-share improvement report

## Executive conclusion

The baseline was statistically stable but chronically unacceptable. Its pooled defect share was **0.005700** against the committed **0.002500**: **2.28 times** the requirement. The line-settings record contains strong statistical associations, but the exact physical setting change implemented between trial windows is not on file. The controlled before/after trial does not demonstrate an effect at its filed risk level. Longer-run post-change data show a favorable point estimate and a stable new level, but do not statistically demonstrate improvement from baseline; that level is still not enough to meet the commitment.

## Baseline: steady, but above the commitment

Across **25 lots**, **570 defects** were found among **100000 inspected**. The p-chart center line was **0.005700**, with equal-lot three-sigma limits of **0.002129** and **0.009271**. The chart flagged **0 lots**, supporting a stable baseline rather than intermittent special causes.

Against the committed share of **0.002500**, the baseline excess was **0.003200**. A one-sided exact binomial test gave **p = 1.5884e-67**. Thus stability did not mean acceptability; the baseline consistently missed the business requirement.

## What the records account for

The filed OLS model used **40 lot records** and included paste thickness, reflow peak, and their interaction. It was significant (**F = 25.670124**, **p = 4.65861e-09**) and explained **68.145%** of observed variation, with adjusted **R-squared = 65.490%**. Term p-values were **7.50498e-07** for paste thickness, **1.22021e-06** for reflow peak, and **4.79242e-07** for their interaction.

This makes the two settings credible explanatory variables on file, including an interaction: their effects should not be interpreted independently. However, these are observational associations and do not alone establish causation. The process-owner query returned no recorded fact matching the exact implemented change. Therefore, this report cannot state which setting was physically changed without inventing it; that documentation gap stops the identification of the intervention itself.

## Did the trial show that the change worked?

The filed design used **6000 inspected per group**, **alpha = 0.05**, and planning shares **0.0059** and **0.0025**. Computed prospective two-sided power was **0.821196**.

Observed shares were **0.006500** before and **0.004833** after, an absolute change of **-0.001667** and a relative reduction of **0.256410**. The pooled two-sided two-proportion test gave **z = 1.216129** and **p = 0.223936**. The observed direction was favorable, but the trial does not statistically demonstrate that the change did anything at the filed risk level. Prospective power for the planned contrast does not override this nonsignificant observed result.

## Is the level reached since the change enough?

Across the subsequent **20 lots**, there were **411 defects** among **80000 inspected**, for **0.005137**. Its p-chart limits were **0.001746** and **0.008529**, and **0 lots** were flagged. The new level therefore appears stable.

Relative to the baseline, the pooled reduction was **0.000563**, or **0.098684** proportionally. The aggregate baseline-versus-post comparison gave **z = 1.610719** and **p = 0.107241**. Thus the post-change point estimate is lower, but this comparison does not statistically demonstrate a sustained reduction from baseline.

Nevertheless, the new average is **2.05 times** the committed share and exceeds it by **0.002637**. The one-sided exact test against the commitment gave **p = 3.3947e-39**. Binomial capability summarizes the new level as **average p = 0.005137** and **process Z = 2.566435**. The result is stable and has a lower point estimate than baseline, but the reduction is not statistically demonstrated and the process is not capable of meeting the commitment.

## Recommended next actions and control plan

- Do not close the project or claim the trial proved effectiveness. Treat the trial result and the later favorable aggregate point estimate as distinct evidence; neither comparison statistically demonstrates improvement.
- Recover and approve the missing change record: identify the actual paste-thickness and reflow-peak settings used, ownership, effective date, and allowed ranges.
- Run a designed, randomized confirmation study of both settings and their interaction. Select sample size from the effect that must be detected, rather than relying on the earlier planned contrast.
- Continue lot-by-lot p-chart monitoring at the demonstrated post-change center line. Escalate any point outside the computed limits and investigate setting drift, inspection changes, and material differences.
- Keep the committed share as the release criterion. Further improvement is required before declaring success, because a stable process can still be stably unacceptable.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"baseline","groups":25,"totalInspected":100000},"method_id":"control_chart.p","outputs":{"centerLine":0.0057,"outOfControlCount":0,"ucl":0.009270979907532385,"lcl":0.0021290200924676157,"totalDefective":570,"totalInspected":100000,"stable":true},"status":"success","decision":"Baseline stable by three-sigma p-chart: no lot outside its control limits."}
{"step_id":2,"inputs_digest":{"batch":"baseline","totalInspected":100000,"requiredShare":0.0025},"method_id":"basic.one_proportion","outputs":{"pValue":1.588400817280976e-67,"avgP":0.0057,"requiredShare":0.0025,"excessShare":0.0032,"ratioToRequirement":2.2800000000000002},"status":"success","decision":"Reject that baseline meets the upper-share commitment; observed share is greater."}
{"step_id":3,"inputs_digest":{"batch":"settings","observations":40,"predictors":3},"method_id":"regression.ols","outputs":{"modelPValue":4.658610154613516e-09,"rSquaredPct":68.1445164732662,"rSquaredAdjPct":65.48989284603837,"fStatistic":25.670123543814185,"pasteThicknessPValue":7.50497899270782e-07,"reflowPeakPValue":1.2202120171998797e-06,"interactionPValue":4.792416137274965e-07,"anyFactorSignificant":true},"status":"success","decision":"The specified settings model is significant; both settings and their interaction are associated with lot defect share, but observational association is not proof of cause."}
{"step_id":4,"inputs_digest":{"batch":"trial_size","nPerGroup":6000,"alpha":0.05},"method_id":"power.two_proportions","outputs":{"power":0.821196457947401,"alpha":0.05,"nPerGroup":6000,"p1":0.0059,"p2":0.0025},"status":"success","decision":"Prospective two-sided power for the filed design assumptions."}
{"step_id":5,"inputs_digest":{"batch":"before_after","groups":2,"trialsPerGroup":6000},"method_id":"basic.two_proportions","outputs":{"pValue":0.22393589211321674,"zStatistic":1.2161287185028007,"beforeShare":0.0065,"afterShare":0.004833333333333334,"absoluteChange":-0.0016666666666666661,"relativeReduction":0.25641025641025633,"beforeDefective":39,"afterDefective":29,"trialsPerGroup":6000},"status":"success","decision":"The observed before/after difference is not statistically significant in a two-sided pooled z-test."}
{"step_id":6,"inputs_digest":{"batch":"after_lots","groups":20,"totalInspected":80000},"method_id":"control_chart.p","outputs":{"centerLine":0.0051375,"outOfControlCount":0,"ucl":0.008528663327080768,"lcl":0.0017463366729192327,"totalDefective":411,"totalInspected":80000,"stable":true},"status":"success","decision":"Post-change level is stable by the three-sigma p-chart."}
{"step_id":7,"inputs_digest":{"batch":"after_lots","totalInspected":80000,"requiredShare":0.0025},"method_id":"basic.one_proportion","outputs":{"pValue":3.394697744792781e-39,"avgP":0.0051375,"requiredShare":0.0025,"excessShare":0.0026374999999999997,"ratioToRequirement":2.0549999999999997},"status":"success","decision":"Post-change defect share remains significantly above the commitment."}
{"step_id":8,"inputs_digest":{"batch":"after_lots","totalInspected":80000},"method_id":"capability.binomial","outputs":{"processZ":2.5664345979906646,"avgP":0.0051375},"status":"success","decision":"One-sided binomial process Z calculated as the standard-normal quantile of yield."}
{"step_id":9,"inputs_digest":{"batches":"baseline,after_lots","groups":2},"method_id":"basic.two_proportions","outputs":{"pValue":0.10724104396572472,"zStatistic":1.6107187184493452,"baselineShare":0.0057,"afterShare":0.0051375,"absoluteReduction":0.0005625000000000005,"relativeReduction":0.09868421052631587},"status":"success","decision":"The pooled post-change level is lower than baseline in the aggregate comparison."}
```

## Submitted route declarations
```json
[{"point":"baseline_stability_gate","chosen_branch":"stable","observed":{"outOfControlCount":0,"centerLine":0.0057}},{"point":"settings_significance_gate","chosen_branch":"any_factor_significant","observed":{"modelPValue":4.658610154613516e-09,"anyFactorSignificant":true}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
