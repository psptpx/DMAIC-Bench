# Blind item B006

Focal assessment: Baseline temporal stability and the analyses and conclusions that may follow.

At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the improvement team on a gear-shaft heat-treatment line. Case-surface hardness is the characteristic under study and the heat-treat recipe is the candidate cause currently on the table; three recipes are in use. Sixty consecutive shafts from one population have been recorded in the order they were run, a separate sample records hardness for shafts made under each of the three recipes, the archive holds the study in which the same shafts were measured several times over by several operators on the hardness tester, and the two recipes with the highest averages have been pulled out into a sample of their own.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the recorded hardness readings can carry a conclusion, how the baseline has behaved, what kind of comparison these readings admit, what that comparison says about the recipe, and what should happen next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
{"msa_ndc":{"field":"ndc","op":">=","value":5.0,"source":"AIAG MSA-4 Ch. II Sec. D"},"msa_pass":{"field":"grr_pct","op":"<=","value":30.0,"source":"AIAG MSA-4 Ch. II Sec. D"}}
```

## Submitted report (complete, identifiers removed)
# Gear-Shaft Heat-Treatment Line: Case-Surface Hardness Project Report

## Project position

Data were obtained from the local steward and all available batches were requested. No data request was denied, and no outside process-fact (provision) turn was needed. The candidate under study is the heat-treat recipe currently in use; the goal is to establish whether recipe accounts for case-surface hardness (unit HRC).

## Can the recorded hardness readings carry a conclusion?

Yes, with an important baseline caveat. A crossed-gage R&R on the repeat-readings batch gives:

- Study-variation GRR = 11.8953%
- Tolerance GRR = 20.4688%
- Number of distinct categories (NDC) = 11

NDC well above 5 indicates adequate measurement discrimination, and a GRR study-variation fraction of about 11.9% is workable for this kind of comparison. The measurement system is not the limiting source of variation, so the recipe comparisons below are supportable.

## Baseline behavior

The 60 shaft-order baseline readings have:

- Mean = 60.6343 HRC
- Median = 60.9300 HRC
- Standard deviation = 2.2974 HRC
- Anderson-Darling p-value = 0.0236

An individuals-moving-range chart on the shaft-order sequence has center line 60.6343, LCL = 56.7598, UCL = 64.5089, and flags 2 individual points. A runs test for randomness around the median gives p = 4.53298e-08. Therefore the baseline is not one stable random sequence: the shaft-order record contains a patterned level shift (visible later in the run), so the whole baseline cannot be treated as a single stable population. Before/after process evaluation using this baseline as a single comparison would be unsafe.

## What kind of comparison do the recipe readings admit?

The separate recipe sample contains three independent groups with 15 shafts each. Levene's median test for equal variances gives p = 0.9756, so the equal-variance assumption is reasonable. Therefore these data admit both one-way ANOVA and nonparametric confirmation. The one-way ANOVA is strongly significant:

- F = 52.4270
- p = 3.83385e-12

Kruskal-Wallis confirms the same conclusion with p = 6.71554e-08.

Group summaries are:

| Recipe | Mean HRC | Median HRC | StdDev HRC |
|---|---:|---:|---:|
| A | 57.9593 | 58.1500 | 0.9091 |
| B | 59.7433 | 59.9900 | 0.9278 |
| C | 61.3273 | 61.4900 | 0.8659 |

## What the leading-two comparison says

The two recipes with the highest averages are recipe C and recipe B. Their head-to-head sample has equal group sizes (15 each). Levene's median test gives p = 0.9331, so the two-sample comparison with equal variances is appropriate. The two-sample t-test gives t = 4.8340, p = 4.36586e-05. The nonparametric Mann-Whitney test also gives p = 0.000261755. The mean difference is 1.5840 HRC in favor of recipe C.

## Conclusion: where the project stands and what should happen next

1. **Measurement system**: recorded hardness readings can carry a conclusion; the gage resolves enough distinct categories.  
2. **Baseline**: the baseline is unstable, so it should not be used as a single before/after control window.  
3. **Recipe**: recipe C is the current best candidate among the three. It has the highest mean hardness, and the difference versus recipe B is statistically significant.  
4. **Next steps**: standardize recipe C on representative production shafts, implement an ongoing I-MR or xbar-s control chart by shaft order, and hold the gain by monitoring recipe C separately. Further effort should evaluate the practical cost, distortion, and other heat-treatment tradeoffs before permanent rollout.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"inputs_digest":{"batch":"msa","numOperators":3,"numParts":10,"numReplicates":3,"sampleSize":90},"method_id":"msa.gage_rr_crossed","outputs":{"percentStudyVariation":11.89525006200899,"percentTolerance":20.46884241168519,"ndc":11},"status":"success","decision":"Cage gage R&R shows acceptable measurement discrimination; GRR percent study variation=11.9%, tolerance percent=20.5%, ndc=11."}
{"step_id":2,"inputs_digest":{"batch":"baseline","sampleSize":60},"method_id":"basic.descriptive_summary","outputs":{"mean":60.63433333333333,"median":60.93,"stdDev":2.297360583303699,"skewness":-0.05027142686892304,"adPValue":0.023598816664972544},"status":"success","decision":"Baseline hardness distribution is near normal by mean/median but AD p<0.05, and baseline is broad compared with observed shifts."}
{"step_id":3,"inputs_digest":{"batch":"baseline","sampleSize":60,"chart":"imr"},"method_id":"control_chart.imr","outputs":{"centerLine":60.63433333333333,"individualsLCL":56.759750282485875,"individualsUCL":64.5089163841808,"flaggedCount":2},"status":"success","decision":"I-MR chart on shaft-order baseline has two individual points outside control limits; process not stable in baseline period."}
{"step_id":4,"inputs_digest":{"batch":"baseline","sampleSize":60,"median":60.93,"runs":10},"method_id":"nonparametric.runs_test","outputs":{"pValue":4.532976172200165e-08},"status":"success","decision":"Runs test strongly rejects random order; baseline data show a patterned shift rather than random variation."}
{"step_id":5,"inputs_digest":{"batch":"recipes","group":"recipe A","sampleSize":15},"method_id":"basic.descriptive_summary","outputs":{"mean":57.95933333333333,"median":58.15,"stdDev":0.9090691209510234,"skewness":0.25162841503878397,"adPValue":0.07954209122843887},"status":"success","decision":"recipe A group summary computed from the separate recipe sample."}
{"step_id":6,"inputs_digest":{"batch":"recipes","group":"recipe B","sampleSize":15},"method_id":"basic.descriptive_summary","outputs":{"mean":59.74333333333334,"median":59.99,"stdDev":0.9278136101815362,"skewness":0.8169257484520428,"adPValue":0.20118558988872182},"status":"success","decision":"recipe B group summary computed from the separate recipe sample."}
{"step_id":7,"inputs_digest":{"batch":"recipes","group":"recipe C","sampleSize":15},"method_id":"basic.descriptive_summary","outputs":{"mean":61.32733333333332,"median":61.49,"stdDev":0.865872529934538,"skewness":-0.35599272174967544,"adPValue":0.4132405728664873},"status":"success","decision":"recipe C group summary computed from the separate recipe sample."}
{"step_id":8,"inputs_digest":{"batch":"recipes","groups":["recipe A","recipe B","recipe C"],"perGroupSize":[15,15,15]},"method_id":"anova.equal_variances","outputs":{"pValue":0.9755563118740186,"statistic":0.024761981900359043},"status":"success","decision":"Levene median test does not reject equal variances across all three recipe groups."}
{"step_id":9,"inputs_digest":{"batch":"recipes","groups":["recipe A","recipe B","recipe C"],"perGroupSize":[15,15,15]},"method_id":"anova.oneway","outputs":{"factorPValue":3.833851301067109e-12,"fStatistic":52.42698750092324},"status":"success","decision":"One-way ANOVA strongly rejects the null hypothesis that all three recipes have equal case-hardness means."}
{"step_id":10,"inputs_digest":{"batch":"recipes","groups":["recipe A","recipe B","recipe C"],"perGroupSize":[15,15,15]},"method_id":"nonparametric.kruskal_wallis","outputs":{"pValue":6.715535907754879e-08},"status":"success","decision":"Kruskal-Wallis nonparametric test also strongly rejects equal medians across recipes."}
{"step_id":11,"inputs_digest":{"batch":"leading_two","groups":["recipe C","recipe B"],"perGroupSize":[15,15]},"method_id":"anova.equal_variances","outputs":{"pValue":0.9330816690985373,"statistic":0.0071785940756871605},"status":"success","decision":"Levene median test for the leading two recipes supports equal variances before the two-sample t-test."}
{"step_id":12,"inputs_digest":{"batch":"leading_two","groups":["recipe C","recipe B"],"perGroupSize":[15,15]},"method_id":"basic.two_sample_t","outputs":{"pValue":4.3658608057111614e-05,"tStatistic":4.834043506337246,"meanGroup1":61.32733333333332,"meanGroup2":59.74333333333334,"meanDifference":1.5839999999999819},"status":"success","decision":"Two-sample t-test for the leading two recipes shows a significant mean hardness difference."}
{"step_id":13,"inputs_digest":{"batch":"leading_two","groups":["recipe C","recipe B"],"perGroupSize":[15,15]},"method_id":"nonparametric.mann_whitney","outputs":{"pValue":0.0002617547195372892},"status":"success","decision":"Mann-Whitney test confirms the leading-two difference is significant without relying on normality assumptions."}
```

## Submitted route declarations
```json
[{"point":"msa_release_baseline","chosen_branch":"computed crossed gage R&R and declared grr_pct and ndc","observed":{"grr_pct":11.89525006200899,"ndc":11}},{"point":"baseline_release_recipes","chosen_branch":"obtained baseline and analyzed stability","observed":{"baseline_n":60}},{"point":"leading_two_selection","chosen_branch":"chose top two recipes by mean hardness","observed":{"ranked_means":[{"recipe C":61.32733333333332},{"recipe B":59.74333333333334},{"recipe A":57.95933333333333}]}}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
