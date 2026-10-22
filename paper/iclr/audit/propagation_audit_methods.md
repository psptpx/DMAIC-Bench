# Delivered-report propagation audit: methods and interpretation

This is a completed exploratory, single Codex-assisted annotation pass, not an independently validated expert audit. The analyst could see prior study information, and existing professional-scope rationales were consulted after initial readings. Revisions are retained in `annotation_revision_log.jsonl`. The working protocol was written before the new labels; it is not an external preregistration. No source report, trace, original judgment, scoring rule or manuscript result was changed.

## Unit, coverage and actual work performed

The sampling frame is the 40 STOP-side trajectory–checkpoint units in the frozen 2026-09-19 study-2 manifest, representing 11 agents and 12 cases. There is one sampled checkpoint per trajectory. This is an audit of that stratified sample, not a census of all benchmark trials or all forks within each trajectory.

All 40 complete delivered reports were read. All 556 submitted trace-step identities and statuses were inventoried, and relevant computation records, their outputs and decisions were inspected. The final JSON retains the selected full records and all submitted route decisions; the original complete trace remains linked. This pass does not independently recompute every statistic from raw data or verify that submitted trace order matches actual execution order. Its object is observable report reuse of a recorded result.

The aggregation checks all 280 frozen packet-file hashes against the original manifest, validates every cited report line and trace step, and checks the primary source-field keys. It preserves original sampling weights and judgments. V012 and V049 differ between the frozen scorer labels and currently available rescoring cards; this drift is recorded separately and does not rewrite the frozen study.

## Establishing a candidate computation

Do not use `scorer=incorrect` as the eligibility definition. Locate the focal prerequisite, the corresponding continuation and a successful calculation on that continuation. A refused attempt is not a computed result. A misleading interpretation of the gate diagnostic itself is also not post-fork computation.

“Post-fork” denotes the logical continuation under examination. It is not inferred merely from a later array index. Additional calculations from independent evidence are not automatically invalid because another branch stopped.

The operational distinctions in this sample are:

- After failed measurement adequacy: production charts, capability or substantive comparisons based on the affected measurements.
- After failed stability: pooled capability, selected-regime capability, or further analyses whose results are used to characterize or explain the unstable baseline. A separate later record is not automatically tainted.
- After a null candidate-cause comparison: selected-group comparisons or change/sustainment analyses that might be treated as support for that cause or intervention.
- After failed response-surface adequacy: optimization outputs and candidate settings. Independent confirmation is evaluated on its own evidence; its identity must not simply be assumed to match the computed optimum.
- After an optimum fails the target, or a change test fails: the corresponding confirmation or post-change assessment is a candidate continuation, even if it is ultimately reported as a valid restricted alternative.
- At the terminal confirmation/target checkpoints, diagnostic comparisons are not themselves a completed-control/closure result. This distinction applies to V003, V015, V018 and V042.
- V004, V032, V036, V048 and V049 have no successful blocked continuation; V012 has no pooled-capability computation. V049 still has an over-strong interpretation of its focal null test, already identified by the original review, which is distinct from propagation.

These distinctions should be re-evaluated independently by human reviewers. They explain why the primary denominator is 30, rather than automatically all 32 frozen scorer-incorrect units.

## Trace the result, then judge its use

Use two axes, not a single keyword detector:

1. **Observable reuse.** Identify the source result in the trace, its local report presentation, and another report location that adopts, summarizes or cites that result. Match the value or substantive finding and its evidential role. A repeated business target, the gate diagnostic itself, or a result from a different independently justified sample is not sufficient. Locations may be the opening summary, a later analysis, closing summary, recommendation or proposed control rule. An opening summary can reuse a result even though it occurs earlier on the page; this audit makes no chronological claim from document order.
2. **Professional warrant.** Decide whether the destination preserves the appropriate limitation, uses a valid independent alternative, silently treats a restricted finding as a premise, or makes an explicit unsupported claim/action. A caveat elsewhere in the report is not automatically protective, and any reuse is not automatically contamination.

The machine ledger records the strongest supported report-level disposition:

| Label | Operational meaning |
|---|---|
| NOT_APPLICABLE | No qualifying candidate computation found. |
| NO_REUSE | Candidate result has no substantive report use identified. |
| QUARANTINED | Description or diagnostic reuse preserves the substantive restriction, including a justified alternative. |
| INDIRECT_REUSE | A candidate result operates as a premise in a later synthesis, ranking or recommendation without an explicit forbidden conclusion/action, and the required restriction is not preserved. |
| EXPLICIT_RELIANCE | The result supports an explicit unsupported conclusion or action somewhere in the report. |
| UNCERTAIN | Scope, dependency or professional validity cannot be resolved confidently. |

Cross-section reuse is a separate flag. Explicit reliance can be confined to the local analysis (V001 and V002), and repeated figures can remain quarantined (e.g. V047). V002, V005 and V037 have possible additional links that are not counted as confirmed. Every unit has a report-level judgment; every eligible unit also has a result-specific evidence edge in `result_links.json`. Additional independent analyses appearing in the trace are context, not automatically contaminated sources.

## Metrics and denominators

Let C denote a qualifying candidate computation, R confirmed reuse in a distinct report section, I unsupported indirect use, E explicit reliance, U unresolved professional status, and H the existing expert-majority acted label. H already covers the whole report, not only the immediate analysis paragraph.

- Cross-section reuse: count(C and R) / count(C). Includes restricted descriptions and therefore is not a contamination rate.
- Cross-section reuse without an original acted label: count(C and not H and R) / count(C and not H). This directly tests reuse even where the original review did not identify a forbidden conclusion/action; it still includes valid restricted reuse.
- Reliance anywhere: count(C and (I or E)) / count(C).
- Reliance across sections: count(C and R and (I or E)) / count(C).
- Incremental indirect use: count(C and not H and I) / count(C and not H).
- Incremental reliance of either kind: count(C and not H and (I or E)) / count(C and not H).

Use raw n/N as the primary description of this audit. Do not add overlap across summary/action/analysis locations. Allocate unresolved cases to either side only as a sensitivity calculation; those ranges are not confidence intervals. The current zero incremental count is not evidence that the true risk is zero.

The machine labels should not be converted into population prevalence, model rankings or new significance claims. If independently adjudicated labels are later used to estimate rates in the original sampling population, retain the frozen stratum weights for both numerator and eligible denominator, and account for case-level clustering. This exploratory pass does not generate such estimates.

## Scope limitation

This is delivered-report result lineage. It does not measure hidden reasoning, internal context compaction, harness summaries, memory contamination, real downstream deployment or causal effects on a later agent. Those require the relevant logs and an explicitly extended design. Identical wording or values establishes observable textual reuse, not the causal mechanism that produced an agent's decision.

## Reproduction

Run `python3 output/research/propagation_audit_20260922/summarize.py` from the repository root, or invoke its absolute path from elsewhere. The script is deterministic for fixed inputs, verifies source integrity and rebuilds JSON/CSV labels, the evidence ledger, source hashes, statistics and two differently ordered blank human review sheets. It aggregates annotations; it does not independently validate them.
