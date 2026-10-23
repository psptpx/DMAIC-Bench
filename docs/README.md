# Documentation index

[English README](../README.md) | [Chinese README](../README.zh-CN.md)

[Publication status](PUBLICATION.md) records the arXiv paper link when available;
[Reproducing results](REPRODUCING_RESULTS.md) lists the required inputs.
Historical `paper/iclr/*.tex` references below denote paper tables or local
analysis outputs, which are distributed separately from the public code tree.

One line per file. The measured corpus is v2 (`adb_c25` to `adb_c39`, 15 cases, 97 tasks); every result file below is on that corpus unless its line says otherwise.

## Benchmark design

| file | what it is |
|---|---|
| [`DATASHEET.md`](DATASHEET.md) | datasheet for the 15-case, 97-task corpus: composition, access, provenance, held-out designation |
| [`SCORING.md`](SCORING.md) | the reward formula as implemented, what each axis measures, and what it cannot mean |
| [`EXPERIMENT_PLAN.md`](EXPERIMENT_PLAN.md) | the pre-registered plan, written before any score was seen, with its deviations register |
| [`HELD_OUT_V2.md`](HELD_OUT_V2.md) | the v2 held-out split: five cases, 32 tasks, structural selection rule and seed |
| [`HELD_OUT.md`](HELD_OUT.md) | the retired v1 split (nine cases withheld for licensing); kept because tests and case files cite it |
| [`CASE_ONBOARDING.md`](CASE_ONBOARDING.md) | how a case enters the benchmark and the validation gates it passes |
| [`FAILURE_MODES.md`](FAILURE_MODES.md) | the failure-mode taxonomy applied to zero-reward trials |
| [`PORTABILITY_PILOT.md`](PORTABILITY_PILOT.md) | design of the life-sciences extension (bulk RNA-seq and case-control GWAS) on the unchanged task contract |
| [`ENGLISH_MIGRATION.md`](ENGLISH_MIGRATION.md) | the 0.2.0 contract making English case text canonical |
| [`control_pairs_2026-09-19.json`](control_pairs_2026-09-19.json) | the 32 paired tasks used by the instruction controls (`paper/iclr/tab_control.tex`, `tab_ctlrep.tex`) |

## Results

| file | what it is |
|---|---|
| [`RESULT_RESTRAINT.md`](RESULT_RESTRAINT.md), [`result_restraint.json`](result_restraint.json) | the 13-system restraint-gap analysis; written by `scripts/restraint_analysis.py`, which also writes `paper/iclr/numbers.tex` |
| [`RESULT_PASSK.md`](RESULT_PASSK.md) | pass^3 and pass@3 by tier under three attempts per task |
| [`STEWARD_REFUSALS.md`](STEWARD_REFUSALS.md) | what contestants asked the data steward for and why it refused, from the steward audit logs |
| [`RESULT_PORTABILITY_PILOT.md`](RESULT_PORTABILITY_PILOT.md) | every count of the life-sciences extension; written by `scripts/pilot_portability_analysis.py` |

## Provenance and QC

| file | what it is |
|---|---|
| [`CASE_SOURCES.md`](CASE_SOURCES.md) | where each case's scenario came from and the licence rule for literature sources |
| [`CONSTRUCTION_QC.md`](CONSTRUCTION_QC.md) | coverage of source extraction, executable verification and expert review over the 97 tasks |
| [`construction_qc_coverage.csv`](construction_qc_coverage.csv), [`construction_qc_summary.json`](construction_qc_summary.json) | the inventory behind `CONSTRUCTION_QC.md`, produced by `scripts/construction_qc_inventory.py` |
| [`LIMITATIONS.md`](LIMITATIONS.md) | what the corpus and the campaigns cannot support |

## Archive

Design notes and result notes for retired corpora or single early campaigns. Nothing in the paper or the README rests on them; they are kept for traceability of decisions that the current corpus inherited.

| file | what it is |
|---|---|
| [`archive/dmaic-bench-v2-longhorizon-design.md`](archive/dmaic-bench-v2-longhorizon-design.md) | 2026-07 design specification for the v2 decision-graph task model |
| [`archive/dmaic-bench-v3-fair-heterogeneous-design.md`](archive/dmaic-bench-v3-fair-heterogeneous-design.md) | 2026-07 design specification for a heterogeneous-agent leaderboard; not what the paper measures |
| [`archive/define-phase-design-2026-09-04.md`](archive/define-phase-design-2026-09-04.md) | design specification for grading the Define phase (v1 corpus) |
| [`archive/control-phase-design-2026-09-04.md`](archive/control-phase-design-2026-09-04.md) | design specification for grading the Control phase (v1 corpus); its section 4.1 is the control-limit house rule |
| [`archive/difficulty-effort-axis-2026-09-04.md`](archive/difficulty-effort-axis-2026-09-04.md) | the human-effort difficulty axis proposed for the v1 corpus |
| [`archive/case-phase-ledger-2026-09-04.md`](archive/case-phase-ledger-2026-09-04.md) | survey of the private source-report corpus against the v1 authored cases |
| [`archive/HUMAN_BASELINE.md`](archive/HUMAN_BASELINE.md) | a practitioner anchor from a different corpus of project reports; not a human score on these tasks |
| [`archive/HINT_PROTOCOL.md`](archive/HINT_PROTOCOL.md) | hint probes for telling a hard task from a broken one, from the 95-task era |
| [`archive/METHOD_DISCIPLINE.md`](archive/METHOD_DISCIPLINE.md) | method precision against decision quality, measured on one campaign |
| [`archive/TIER_RESULTS.md`](archive/TIER_RESULTS.md) | tier results on the 40-task corpus |
| [`archive/RESULT_G3_2026-09-12.md`](archive/RESULT_G3_2026-09-12.md) | the oracle and null-agent controls passing on the corpus that ships |
| [`archive/RESULT_GLM53FLASH_97.md`](archive/RESULT_GLM53FLASH_97.md) | the first single-system campaign on the 97-task corpus, one attempt per task |
| [`archive/DATASHEET_legacy_333.md`](archive/DATASHEET_legacy_333.md) | datasheet of the former 333-task build |

Any file in this directory not listed above is an internal working note that the release script removes.
