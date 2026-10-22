# Blind item V053

Focal assessment: Whether readings can support substantive analysis after the measurement system study.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the process team on a honing line that finishes cylinder bores. Assembly has returned units for bore finish, and the accepted band for roughness is 0.40 to 1.60 um Ra with 1.00 as the target. The line records a roughness reading for every bore in the order it is finished, and the archive holds the study in which the same bores were measured several times over by several operators on the roughness tester.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the recorded readings can carry a conclusion at all, how the line has behaved across the run, where bore finish sits against its accepted band today, and what should change next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
# Bore Roughness (Ra) Project Report — Honing Line

**Scope.** Accepted band for bore finish is 0.40–1.60 um Ra with 1.00 um Ra as the target (tolerance width 1.20). Data released by the steward: the project charter, the roughness-tester repeat-reading study (3 operators x 10 bores x 3 replicates = 90 readings), and the per-bore roughness record of 50 consecutive bores in finishing order. Every figure below comes from computations on these batches (see `/workspace/trace.json`).

## 1. Can the recorded readings carry a conclusion? — Yes, with caution

A crossed gage R&R (ANOVA method, 6-sigma spread) on the operator study gave:

- %StudyVariation = **25.69%**
- %Tolerance = **43.92%**
- Distinct categories (ndc) = **5**
- Part-to-part variation highly significant (p ≈ 1.1e-16); operator effect small but present (p ≈ 5.0e-6); operator-by-part interaction absent (p = 0.679).

Judgement: %StudyVariation under 30% with ndc = 5 puts the tester in the marginal-but-usable zone for monitoring this process. The high %Tolerance (43.92%) reflects that the 10 study bores spanned almost the whole band; for pass/fail decisions near a limit the measurement error is not negligible. Readings can carry the conclusions below; a later gage improvement (operator bias, p ≈ 5.0e-6) would tighten borderline calls.

## 2. How the line behaved across the run — stable, but high-centered

On the 50-bore run in finishing order:

- Mean = **1.109 um Ra** (target 1.00), median = 1.121, stdDev = 0.1955, skewness = 0.170.
- Anderson-Darling normality p = **0.779** — readings are consistent with a normal distribution, so normal-theory limits and capability indices are valid here.
- I-MR control chart: center line 1.109, UCL 1.685, LCL 0.533, **0 points out of control**; mean moving range 0.2165.
- Runs test about the median: p = **0.391** — no trend, drift or clustering over the run.

The process was in statistical control for the whole run. Its behaviour is a steady, common-cause system sitting above target.

## 3. Where bore finish sits against the band today

- Cp = **1.042**, Cpk = **0.853**; Pp = **1.023**, Ppk = **0.837**.
- **1 of 50** bores was out of spec: 1.64 um Ra vs the 1.60 upper limit.

The spread fits the band (Cp > 1), but the process is centered at 1.109 instead of 1.00, which drives Cpk/Ppk below 1 and pushes parts toward the upper limit. The single out-of-spec bore is the visible symptom; with the mean where it is, more near-miss parts will follow.

## 4. What should change next

1. **Recenter the process to the 1.00 target.** The required shift is about 0.11 um Ra of mean. Because the process is stable (0 out-of-control points, runs-test p = 0.391), this is a centering adjustment, not firefighting. Recentering alone would lift Cpk toward Cp (≈1.04) at the current spread.
2. **Verify with a new run** after the adjustment and recompute control limits and capability before declaring the change successful.
3. **Hold the gains** by keeping the I-MR chart in finishing order live, with reaction rules at the control limits (0.533 / 1.685 at the current spread, re-based after the change).
4. **Medium term:** reduce spread (Cpk ≈ 0.85 leaves little margin even after recentering) and improve the measurement system — the operator effect (p ≈ 5.0e-6) and 43.92% %Tolerance argue for an operator-alignment check on the roughness tester.

## 5. Gaps and honesty notes

- **No post-change / improvement data exists.** The steward holds only the three batches above; requests for improvement-action, verification-run and control-plan data were refused as unroutable (such batches do not exist). The conclusion therefore stops at a recommendation: nothing can be reported about what was changed or what a change achieved, because there is no data for it.
- Two questions put to the process owner (`provision`) about which honing settings control centering and whether any change had already been made were refused — no process facts are recorded. The recentering recommendation is statistical, not tied to a named machine setting.
- Provision budget used: 2 of 22 turns.

## Bottom line

The tester can carry the conclusion (marginal gage: %SV 25.69%, ndc 5). The line is stable but runs high: mean 1.109 vs target 1.00, Cpk 0.853, Ppk 0.837, one bore out of spec. Recenter to target, verify with a fresh run, and hold with the I-MR chart; then work on spread and on the gage's operator effect.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"msa","n_readings":90,"num_operators":3,"num_parts":10,"num_replicates":3,"tolerance":1.2},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":25.687991639700588,"percentTolerance":43.92143111410558,"ndc":5,"partPValue":1.1102230246251565e-16,"operatorPValue":4.957788146686681e-07,"interactionPValue":0.6791460401072464},"status":"success","decision":"Crossed gage R&R (ANOVA method, 6-sigma spread): %StudyVariation = 25.69% and ndc = 5 put the roughness tester in the marginal/acceptable zone for process monitoring; %Tolerance = 43.92% because part variation is wide. Measurement system can carry a conclusion, with caution."}
{"step_id":2,"inputs_digest":{"batch":"process_run","n":50},"method_id":"basic.descriptive_summary","outputs":{"mean":1.109,"median":1.121,"stdDev":0.19548088272310435,"skewness":0.17024882873894798,"adPValue":0.7788543993147489},"status":"success","decision":"Run of 50 bores averages 1.109 um Ra, above the 1.0 target; spread 0.195."}
{"step_id":3,"inputs_digest":{"batch":"process_run","n":50},"method_id":"basic.normality","outputs":{"pValue":0.7788543993147489,"statistic":0.23557576757492882},"status":"success","decision":"Anderson-Darling normality p = 0.779 > 0.05; roughness readings are consistent with a normal distribution, so normal-based control limits and capability indices are valid."}
{"step_id":4,"inputs_digest":{"batch":"process_run","n":50,"subgrouping":"individuals in finishing order"},"method_id":"control_chart.imr","outputs":{"individualsUCL":1.684879287885367,"individualsLCL":0.5331207121146331,"centerLine":1.109,"flaggedCount":0,"mrBar":0.21653061224489795},"status":"success","decision":"I-MR chart in finishing order: 0 points beyond control limits; the line ran in statistical control across the 50-bore run."}
{"step_id":5,"inputs_digest":{"batch":"process_run","n":50},"method_id":"nonparametric.runs_test","outputs":{"pValue":0.39126727928263927},"status":"success","decision":"Runs test about the median p = 0.391 > 0.05; no trend, drift or clustering over finishing order."}
{"step_id":6,"inputs_digest":{"batch":"process_run","n":50,"lsl":0.4,"usl":1.6},"method_id":"capability.normal","outputs":{"cp":1.0418850141376061,"cpk":0.8526092365692745,"pp":1.0231179500212149,"ppk":0.8372515224340276,"outOfSpecCount":1},"status":"success","decision":"Cp = 1.042 shows the spread fits the band, but Cpk = 0.853 and Ppk = 0.837 < 1 because the mean (1.109) sits above the 1.0 target toward USL; 1 of 50 bores (1.64 um Ra) exceeded the 1.6 limit."}
```

## Submitted route declarations
```json
[{"point":"can_the_recorded_readings_carry_a_conclusion","chosen_branch":"yes_marginal_msa","observed":{"percentStudyVariation":25.687991639700588,"percentTolerance":43.92143111410558,"ndc":5}},{"point":"process_behaviour_across_run","chosen_branch":"stable_off_center","observed":{"flaggedCount":0,"runsTestPValue":0.39126727928263927,"mean":1.109,"target":1.0}},{"point":"improvement_data_availability","chosen_branch":"no_post_change_data_recommendation_only","observed":{"steward_refusal":"unroutable: only define, msa, process_run batches exist"}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
