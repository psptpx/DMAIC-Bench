# Task [TASK]

## 1. Business background

We are the improvement team on a high-speed rod-making line. Every unit leaving the line is judged sound or defective on appearance, and the charter commits us to no more than 1500 defective units per million inspected. The archive holds the inspected and defective counts for twenty-five consecutive lots, a study in which several inspectors judged the same retained units against an agreed answer key, and a machine-by-machine tally of defective and sound units over one common window, and one machine's inspected and defective counts either side of a change that was made to it.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether a sound/defective judgement can be relied on at all, whether the defective share has held steady across the lots, how today's level compares with what the charter commits us to, and what should be done next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.
## 4. Getting data: ask the data steward

This environment has **no network**. Every piece of shop-floor data is held by a "data
steward" service running inside the container — it is not sitting in the filesystem waiting
to be read. You must ask for it one batch at a time, saying what you need right now.

Command line (recommended):

```
steward request "<say in plain language which batch of shop-floor data you need now>"
steward declare <field name> <value>
steward provision "<ask the process owner one question about a process fact>"
steward status
steward --json request "..."          # print the raw JSON reply, for programmatic parsing
```

The equivalent HTTP interface (loopback only, at http://127.0.0.1:8731):

```
GET  http://127.0.0.1:8731/status
POST http://127.0.0.1:8731/request     {"text": "<plain language>"}
POST http://127.0.0.1:8731/declare     {"key": "<field name>", "value": <value>}
POST http://127.0.0.1:8731/provision   {"text": "<plain language>"}
```

* `request` reads records the plant already holds and is **not** charged against your budget;
  the steward routes what you said onto one batch of data.
* `declare` reports a verdict **you computed yourself** back to the steward (for example,
  whether some precondition holds). The steward records what you claimed; it does not look at
  the truth and it will not tell you whether you are right.
* `provision` asks the process owner about a process fact. **Each call costs one turn**; the
  budget is below.
* `status` returns which batches are still available and how many turns you have spent.

### The shape of a steward reply (normative)

Every reply is **one JSON object** (obtain the raw object with `steward --json …` or over
HTTP), with these fields:

| field | type | meaning |
|---|---|---|
| `action` | string | what you did: `request` / `declare` / `provision` / `status` |
| `ok` | boolean | whether the action was satisfied |
| `outcome` | string | `"data"` (data was handed over) / `"ok"` / `"refused"` / `"error"` |
| `refusal` | string or null | why, when `outcome="refused"`; see the table below |
| `gate` | string or null | when a precondition blocked you, the name of the public criterion |
| `stage_id` | string or null | the batch this call landed on |
| `message` | string | the human-readable body: with `outcome="data"`, a preview of the batch |
| `turns_used` | integer | billed turns spent so far |
| `max_turns` | integer | the turn ceiling |
| `seq` | integer | the sequence number of this interaction |

**How to get the complete data**: when `outcome="data"`, the steward also writes the whole
batch as JSON to `/workspace/data/<stage_id>.json`. The preview inside `message` may be
truncated, so **compute from that file** if you want the complete data.

The four values of `refusal` are not interchangeable — treat each one differently:

| `refusal` | meaning | what to do |
|---|---|---|
| `locked` | a precondition has not been satisfied yet | finish that earlier step first, `declare` the verdict you reached, then retry; `message` and `gate` name the field it is waiting on, the threshold, and the handbook it comes from |
| `denied` | that batch has been checked and genuinely does not exist | **do not invent it.** State plainly in the report that this step is missing and what it costs the conclusion |
| `unroutable` | the steward could not tell which batch you meant | ask again in different words |
| `exhausted` | the `provision` turn budget is spent | finish the report from what you already hold, and say which steps you could not get data for |

Some batches are **routed by the verdict you reach**: the steward releases the next batch only
after it has seen you `declare` a particular result. When one blocks you, `message` names the
field it is waiting on.

The `provision` ceiling for this task is **22** turns; `request`, `declare` and
`status` are free.

## 5. Output (normative requirements)

When you finish, two files must exist in the working directory. The schema below is
**normative, not illustrative**: the scoring program reads it field by field.

### 1. `/workspace/trace.json`

A UTF-8 JSON object conforming to `dmaic_bench/schemas/trace.schema.json`:

| field | type | required | meaning |
|---|---|---|---|
| `system_id` | string | yes | identifier of the system that produced this record |
| `task_id` | string | yes | must equal `[TASK]` **verbatim** |
| `steps` | array of object | yes | every quantitative analysis you actually ran, in the order you ran them |
| `route_decisions` | array of object | no | the choices you made at the decisive forks |
| `turns` | integer | no | billed turns you spent |
| `interventions` | integer | no | times you asked for outside human help |
| `wall_clock_s` | number | no | total elapsed seconds |
| `token_cost` | integer or null | no | tokens consumed; null if unknown |

Each element of `steps[]`:

| field | type | required | meaning |
|---|---|---|---|
| `step_id` | integer | no | sequence number, from 1 |
| `inputs_digest` | object | no | the shape of what you actually fed in (sample size, number of groups, which batch it came from) |
| `method_id` | string | yes | the canonical identifier of the analysis this step ran, shaped `<family>.<name>` (lowercase, two dot-separated parts) |
| `outputs` | object | yes | the named scalar results this step produced; keys are suffix-matched, values must be numbers or booleans |
| `status` | string | yes | exactly one of `"success"`, `"failed"`, `"refused"` |
| `decision` | string or null | no | the verdict this step reached |

**`method_id` may only take a value from the table below, and please name the keys of
`outputs` with the canonical field names the same table gives.** This table is the same
complete vocabulary for every task — it does not tell you which entries this task needs, which
is precisely what you are being asked to judge. It fixes only *what one thing is called*, so
that a correct result is not marked wrong for being named differently.

| family | `method_id` | canonical output field names |
|---|---|---|
| anova | `anova.equal_variances` | `pValue`, `statistic` |
| anova | `anova.oneway` | `factorPValue`, `fStatistic` |
| anova | `anova.sov` | `totalVariance` |
| basic_test | `basic.correlation` | `correlationCoefficient`, `pValue` |
| basic_test | `basic.descriptive_summary` | `mean`, `median`, `stdDev`, `skewness`, `adPValue` |
| basic_test | `basic.normality` | `pValue`, `statistic` |
| basic_test | `basic.one_proportion` | `pValue` |
| basic_test | `basic.one_sample_t` | `pValue`, `tStatistic` |
| basic_test | `basic.paired_t` | `pValue`, `tStatistic` |
| basic_test | `basic.two_proportions` | `pValue`, `zStatistic` |
| basic_test | `basic.two_sample_t` | `pValue`, `tStatistic` |
| capability | `capability.binomial` | `processZ`, `avgP` |
| capability | `capability.grouped` | `cpk`, `ppk` |
| capability | `capability.nonnormal` | `ppk`, `pp` |
| capability | `capability.normal` | `cp`, `cpk`, `pp`, `ppk` |
| capability | `capability.poisson` | `dpu` |
| control_chart | `control_chart.c` | `centerLine` |
| control_chart | `control_chart.cusum` | `flaggedCount` |
| control_chart | `control_chart.ewma` | `flaggedCount` |
| control_chart | `control_chart.imr` | `individualsUCL`, `individualsLCL`, `centerLine`, `flaggedCount` |
| control_chart | `control_chart.laney_p` | `sigmaZ` |
| control_chart | `control_chart.laney_u` | `sigmaZ` |
| control_chart | `control_chart.np` | `centerLine` |
| control_chart | `control_chart.p` | `centerLine`, `outOfControlCount` |
| control_chart | `control_chart.u` | `processMean` |
| control_chart | `control_chart.xbar_r` | `xBarChartCenterLine`, `flaggedXBarCount` |
| control_chart | `control_chart.xbar_s` | `xBarChartCenterLine` |
| doe | `doe.create_factorial` | - |
| doe | `doe.factorial_analysis` | `modelPValue`, `rSquaredPct` |
| doe | `doe.factorial_prediction` | `predictedValue`, `piLower`, `piUpper` |
| doe | `doe.rsm_analysis` | `rSquaredPct`, `lackOfFitPValue` |
| doe | `doe.rsm_canonical` | `predictedAtStationary` |
| doe | `doe.rsm_optimizer` | `compositeDesirability`, `predictedResponse` |
| meta | `meta.data_profiling` | - |
| msa | `msa.attribute_agreement` | `kappaMin`, `agreementPct` |
| msa | `msa.gage_rr_crossed` | `percentStudyVariation`, `percentTolerance`, `ndc` |
| nonparametric | `nonparametric.kruskal_wallis` | `pValue` |
| nonparametric | `nonparametric.mann_whitney` | `pValue` |
| nonparametric | `nonparametric.moods_median` | `pValue` |
| nonparametric | `nonparametric.one_sample_wilcoxon` | `pValue` |
| nonparametric | `nonparametric.runs_test` | `pValue` |
| power | `power.two_proportions` | `power` |
| quality_tools | `quality.fmea_rpn` | `maxRpn` |
| quality_tools | `quality.pareto` | `topCategoryPct` |
| regression | `regression.binary_logistic` | `modelPValue` |
| regression | `regression.ols` | `modelPValue`, `rSquaredPct`, `rSquaredAdjPct` |
| regression | `regression.poisson` | `deviance` |
| tables | `tables.chisquare_assoc` | `statistic`, `pValue` |
| tables | `tables.chisquare_gof` | `chiSquare`, `pValue` |

If you believe a step you ran is not in the table, still pick the closest entry and explain
the difference in `decision`; do not invent an identifier. The same goes for output fields:
hang each quantity you computed on a field name the table lists (extra intermediate keys are
fine and do not affect scoring).

Each element of `route_decisions[]`:

| field | type | required | meaning |
|---|---|---|---|
| `point` | string | yes | identifier of the fork |
| `chosen_branch` | string | yes | the branch you took |
| `observed` | object | no | the observed values you based that choice on |

Hard constraints:

* write `status: "success"` only for a step you genuinely computed; write `"refused"` where the
  steward would not release the data and `"failed"` where the computation failed.
* every number in `outputs` must have been computed on this run. Filling one in from
  experience, from memory or from what is "usually the case" is **not allowed**.
* do not put an analysis you never ran into `steps`.

### 2. `/workspace/report.md`

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
