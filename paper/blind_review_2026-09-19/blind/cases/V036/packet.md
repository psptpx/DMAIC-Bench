# Blind item V036

Focal assessment: Whether readings can support substantive analysis after the measurement system study.

At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? (2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. (3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?

## Original assignment (business sections)
# Task [TASK]

## 1. Business background

We are the process team on an enamelled-component line. Coating thickness is accepted between 180 and 260 um with 220 um as the target. The line records five consecutive pieces at each of twenty-five sampling points through the run, the archive holds the study in which the same pieces were measured several times over by several operators on the thickness gauge, and a separate sample records thickness piece by piece for each of the four applicators.

## 2. What you are asked to do

Work through the batches the data steward will release and report where this project stands: whether the recorded readings can carry a conclusion, how the line has behaved across the run, where coating thickness sits against the range it is accepted in, and what specifically should change next. Every number in your report must come from a computation you ran on this task; where something could not be computed, say so rather than inventing it.


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
# Coating thickness project — measurement gate not passed

## Management conclusion
The archived readings do **not support a defensible process acceptance or improvement conclusion**. The immediate priority is the measurement system, not applicator adjustment. The charter specifies acceptance from **180 to 260 µm**, target **220 µm**, giving a computed tolerance width of **80 µm**.

## What was established
A balanced crossed gauge study contains **90 readings**, covering **10 parts**, **3 operators**, and **3 repeats per operator–part combination. I fitted a crossed random-effects variance-components model. The operator–part interaction was not significant (p = **0.5001**) and was pooled into repeatability error; negative variance estimates were constrained to zero.

| Measurement result | Computed value |
|---|---:|
| Gauge R&R, percent of total study variation | 44.34% |
| Gauge R&R, percent of tolerance | 63.70% |
| Distinct categories (truncated discrimination estimate) | 2 |
| Gauge standard deviation | 8.494 µm |
| Pooled repeatability variance | 72.143 µm² |
| Operator variance estimate | 0 µm² |
| Retained interaction variance estimate | 0 µm² |
| Part-to-part variance estimate | 294.801 µm² |

Study variation uses the ratio of gauge standard deviation to combined gauge and part standard deviation; tolerance usage uses the full study spread relative to tolerance. Discrimination is based on the part-to-gauge standard deviation ratio. These calculations are reproducible in `analyze.py` from the released JSON.

Measurement error is large relative both to observed part variation and to tolerance. The computed verdict was declared to the steward, which rejected the measurement acceptance gate. Repeatability dominates the estimated measurement error; the fitted operator component at zero does not prove operators are interchangeable or that calibration bias is absent. This study does not independently establish accuracy, linearity or long-term gauge stability.

## Where the process conclusion stops
The run-order readings were **locked** by the failed measurement gate. Applicator samples and the monitoring record were also **locked** behind the run-order prerequisite. These are access restrictions, not evidence that the records do not exist. No downstream request was denied as genuinely nonexistent.

Consequently, run stability, time trends, process centering, capability, reject rate and applicator differences **could not be computed**. Neither a particular applicator nor a process setting can be identified as the cause. No completed change or sustained improvement can be verified. A request for a replacement measurement study was unroutable, and the process owner had no matching remediation fact. There is no released replacement evidence on which to continue.

## What specifically should change next
- **Quality/metrology owner:** inspect gauge calibration against traceable standards, resolution, probe contact and alignment, fixture repeatability, surface preparation, measurement location and environmental sensitivity. Standardize the measurement method and train operators. Treat these as hypotheses to check, not established physical causes.
- **Production and quality:** protect disposition decisions near the acceptance boundaries with an independently validated measurement method; do not tune applicators on the basis of noisy readings alone. Document any containment and remeasurement decisions.
- **Metrology:** after documented corrective action, repeat a randomized, blinded crossed study using representative parts and operators. Recheck repeatability, reproducibility, discrimination and tolerance usage, and separately check bias and stability. Resume downstream analysis only after the measurement acceptance gate passes.
- **Process engineering:** then obtain chronological rational subgroups, assess spread and mean stability before interpreting capability, and investigate special causes against event records. Evaluate distributional suitability and centering against target. Compare applicators with assumptions checked and avoid treating an observational difference as proof of causation.
- **Control owner:** following a verified process correction, retain timestamped monitoring, calibrated gauge checks, approved control limits, an escalation and containment reaction plan, and a named owner for review. Quantify before/after performance on validated measurements before claiming an achievement.

**Current disposition:** measurement-system remediation required; process diagnosis, improvement benefit and sustainment remain unverified. Recommended actions above are prospective, not changes claimed to have happened.


## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)
```jsonl
{"step_id":1,"method_id":"meta.data_profiling","outputs":{"lsl":180.0,"usl":260.0,"target":220.0,"tolerance":80.0},"status":"success","decision":"Specifications read from charter; tolerance computed."}
{"step_id":2,"method_id":"msa.gage_rr_crossed","inputs_digest":{"batch":"msa","shape":[3,10,3]},"outputs":{"percentStudyVariation":44.34026199179066,"percentTolerance":63.70295058178359,"ndc":2,"interactionPValue":0.5001485510264241,"repeatabilityVariance":72.14339400578065,"operatorVariance":0,"interactionVariance":0.0,"partVariance":294.8008335854499,"gageStdDev":8.493726744237811,"numReadings":90,"numParts":10,"numOperators":3,"numReplicates":3},"status":"success","decision":"Crossed random-effects ANOVA; interaction pooled if p >= .05. Measurement system unacceptable."}
{"step_id":3,"method_id":"control_chart.xbar_r","inputs_digest":{"requested_batch":"sampling order","data_received":false},"outputs":{},"status":"refused","decision":"Locked: computed GRR fails measurement gate. No quantitative analysis run."}
{"step_id":4,"method_id":"anova.oneway","inputs_digest":{"requested_batch":"applicator sample","data_received":false},"outputs":{},"status":"refused","decision":"Locked: sampling-order prerequisite unmet. No quantitative analysis run."}
{"step_id":5,"method_id":"meta.data_profiling","inputs_digest":{"requested_batch":"monitoring record","data_received":false},"outputs":{},"status":"refused","decision":"Locked: sampling-order prerequisite unmet. No quantitative analysis run."}
```

## Submitted route declarations
```json
[{"point":"msa_pass","chosen_branch":"stop_and_repair_measurement_system","observed":{"grr_pct":44.34026199179066,"ndc":2}},{"point":"downstream_access","chosen_branch":"locked_no_process_conclusions"}]
```

Released raw batches, service events and the full original instructions are in this item directory. Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.
