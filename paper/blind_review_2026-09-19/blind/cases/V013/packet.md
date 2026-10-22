# Blind item V013

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
# Chip-Capacitor Line - Defect-Share Project Status Report

**Task:** [TASK] | **Committed defect share:** <= 0.25% of units inspected

## Headline

The line is **stable but not yet at the committed level**. The baseline held steady at
**0.546%** - more than twice the commitment. The change made on the line produced a real,
statistically proven improvement (down to **0.3375%** in the trial, **0.34375%** across the
lots run since), but the level reached is **still significantly above 0.25%**. The project is
not done: another improvement cycle is needed.

## 1. Did the defect share hold steady across the baseline? Yes.

- 25 baseline lots, 4,000 units each (100,000 units, 546 defectives): p-chart center line
  **0.5460%**, with **0 of 25** lots outside the 3-sigma limits (trace step 1).
- Overdispersion check (Laney p'): **sigmaZ = 0.9569** (trace step 2), so the plain p-chart is
  appropriate and the "stable" verdict stands. Declared to the steward: `stable = true`.

## 2. How does the baseline compare with the commitment? Well above it.

- Exact one-proportion test of the baseline total (546 / 100,000) against 0.25%:
  **p = 4.2e-59** (trace step 3). The baseline defect share is significantly **above** the
  committed share, not just noisy around it.
- Binomial capability at baseline: **avgP = 0.00546, processZ = 2.5452** (trace step 4).

## 3. Does anything on file account for it? Yes - the two line settings.

- OLS regression of per-lot defect share on paste_thickness, reflow_peak and their
  interaction (40 lots): model **p = 1.2e-06**, **R-sq = 56.4%**, **adj R-sq = 52.8%**
  (trace step 5). All three terms are significant: paste_thickness **p = 1.6e-05**,
  reflow_peak **p = 3.6e-05**, interaction **p = 1.2e-05**.
- Declared to the steward: `any_factor_significant = true`. The lot-to-lot level is driven by
  the settings, which is also the lever for further improvement.

## 4. Can the change be shown to have done anything? Yes.

- Before/after totals (40,000 units each side): **237/40,000 = 0.5925%** before vs
  **135/40,000 = 0.3375%** after. Two-proportions z-test: **z = 5.30, p = 1.15e-07** - a
  **43.0%** relative reduction (trace step 6).
- The trial was run at alpha = 0.05 with 40,000 units per group; computed power for the
  design effect (0.0059 vs 0.0025) is **1.0** (trace step 7), so the significant result is
  trustworthy.
- **What was physically changed is not on file.** The process owner holds no process fact
  describing it (provision request refused as unroutable; 1 of 26 provision turns spent).
  We can quantify the effect but cannot name the intervention from the data held here.

## 5. Is the level reached since the change enough? No.

- 20 lots run since the change (80,000 units, 275 defectives): p-chart center line
  **0.34375%**, **0 of 20** lots out of control - the new level is stable (trace step 8).
- Exact one-proportion test against the committed 0.25%: **p = 2.85e-07** (trace step 9).
  The current level is still significantly above target - **37.5%** over it, a gap of
  **0.0009375** share points.
- Post-change binomial capability: **avgP = 0.0034375, processZ = 2.7028**, improved from
  2.5452 but still short (trace step 10).

## 6. What should happen next

1. **Keep the change in place and hold it** with the p-chart now running at CL = 0.34375%;
   the process is stable at this level.
2. **Run one more improvement cycle on the two settings.** The regression shows paste
   thickness, reflow peak and their interaction drive the defect share (adj R-sq = 52.8%),
   so a designed experiment over those two factors is the direct route to closing the
   remaining 0.0009375 share points (0.09375 percentage points).
3. **Record the change that was made** in the process documentation - its identity could not
   be recovered from the data held in this environment.
4. **Re-verify against 0.25%** after the next change with the same two-proportions /
   one-proportion tests used here.

*Every figure above comes from a computation run on this task; the corresponding entries are
in /workspace/trace.json. Where data did not exist (the identity of the change), that is
stated plainly rather than guessed.*


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"control_chart.p","inputs_digest":{"batch":"baseline","subgroups":25,"subgroup_size":4000,"total_inspected":100000,"total_defects":546},"outputs":{"centerLine":0.00546,"outOfControlCount":0},"status":"success","decision":"Baseline defect share is statistically in control: 0 of 25 lots outside 3-sigma p-chart limits (CL 0.5460%)."}
{"step_id":2,"method_id":"control_chart.laney_p","inputs_digest":{"batch":"baseline","subgroups":25,"total_inspected":100000},"outputs":{"sigmaZ":0.9569},"status":"success","decision":"sigmaZ < 1.1 confirms no meaningful overdispersion; the plain p-chart is the right chart and the stability verdict stands. Declared stable=true."}
{"step_id":3,"method_id":"basic.one_proportion","inputs_digest":{"batch":"baseline","events":546,"trials":100000,"hypothesized_share":0.0025,"alternative":"greater","test":"exact binomial"},"outputs":{"pValue":4.22024e-59},"status":"success","decision":"Baseline defect share 0.546% is significantly ABOVE the committed 0.25% (p = 4.2e-59). Stable but not at the committed level."}
{"step_id":4,"method_id":"capability.binomial","inputs_digest":{"batch":"baseline","events":546,"trials":100000},"outputs":{"avgP":0.00546,"processZ":2.5452},"status":"success","decision":"Baseline binomial capability: avgP = 0.00546, processZ = 2.5452 - short of the level the 0.25% commitment implies."}
{"step_id":5,"method_id":"regression.ols","inputs_digest":{"batch":"settings","n":40,"predictors":["paste_thickness","reflow_peak","paste_thickness*reflow_peak"],"response":"lot_defect_share"},"outputs":{"modelPValue":1.20039e-06,"rSquaredPct":56.426,"rSquaredAdjPct":52.795,"pasteThicknessPValue":1.58787e-05,"reflowPeakPValue":3.64742e-05,"interactionPValue":1.21514e-05},"status":"success","decision":"Line settings account for the defect share: model p = 1.2e-06, adj R2 = 52.8%; paste_thickness, reflow_peak and their interaction are all significant (each p < 4e-05). Declared any_factor_significant=true."}
{"step_id":6,"method_id":"basic.two_proportions","inputs_digest":{"batch":"before_after","before":{"events":237,"trials":40000},"after":{"events":135,"trials":40000}},"outputs":{"pValue":1.15301e-07,"zStatistic":5.3008,"beforeShare":0.005925,"afterShare":0.003375,"relativeReductionPct":43.038},"status":"success","decision":"The change can be shown to have worked: defect share fell from 0.5925% to 0.3375% (z = 5.30, p = 1.15e-07), a 43.0% relative reduction."}
{"step_id":7,"method_id":"power.two_proportions","inputs_digest":{"batch":"trial_size","alpha":0.05,"nPerGroup":40000,"p1":0.0059,"p2":0.0025,"alternative":"two-sided"},"outputs":{"power":1.0},"status":"success","decision":"The trial was run with power = 1.0 (computed > 0.999999, rounds to 1.0) at alpha = 0.05 for the design effect 0.0059 vs 0.0025, so the significant result in step 6 is trustworthy."}
{"step_id":8,"method_id":"control_chart.p","inputs_digest":{"batch":"after_lots","subgroups":20,"subgroup_size":4000,"total_inspected":80000,"total_defects":275},"outputs":{"centerLine":0.0034375,"outOfControlCount":0},"status":"success","decision":"Post-change process is in control at the new level: 0 of 20 lots outside limits (CL 0.34375%)."}
{"step_id":9,"method_id":"basic.one_proportion","inputs_digest":{"batch":"after_lots","events":275,"trials":80000,"hypothesized_share":0.0025,"alternative":"greater","test":"exact binomial"},"outputs":{"pValue":2.84784e-07,"excessVsTargetPct":37.5,"gapSharePoints":0.0009375},"status":"success","decision":"The level reached since the change (0.34375%) is still significantly ABOVE the committed 0.25% (p = 2.85e-07) - about 37.5% over target. The commitment is not yet met."}
{"step_id":10,"method_id":"capability.binomial","inputs_digest":{"batch":"after_lots","events":275,"trials":80000},"outputs":{"avgP":0.0034375,"processZ":2.7028},"status":"success","decision":"Post-change binomial capability: avgP = 0.0034375, processZ = 2.7028 - improved from 2.5452 but still short of the commitment."}
```

## Submitted route declarations
```json
[{"point":"baseline_stability","chosen_branch":"stable","observed":{"outOfControlCount":0,"laneySigmaZ":0.9569,"centerLine":0.00546}},{"point":"any_factor_significant","chosen_branch":"true","observed":{"modelPValue":1.20039e-06,"interactionPValue":1.21514e-05}},{"point":"change_effectiveness","chosen_branch":"effective_but_insufficient","observed":{"zStatistic":5.3008,"pValue":1.15301e-07,"afterShare":0.0034375,"targetShare":0.0025}},{"point":"what_was_changed","chosen_branch":"not_on_file","observed":{"provision_outcome":"refused","refusal":"unroutable"}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
