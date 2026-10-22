# Datasheet — DMAIC-Bench, 97-task corpus

This document describes the 15-case, 97-task corpus in the current manuscript.
The former 333-task datasheet is preserved in `archive/DATASHEET_legacy_333.md`;
its counts, held-out policy and validation claims must not be applied to this version.

## Purpose and unit

DMAIC-Bench measures whether an agent lets computed diagnostic evidence govern
its next action in an industrial improvement project. A task is one case and
seed, with a business instruction, generated data batches, a data steward,
a reference route and an execution-based evaluator. It is not an extracted QA pair.

## Sources and construction

Case authoring starts from manual extraction of real DMAIC project material:
scenarios, measured characteristics, units, limits and decision evidence.
Released measurements are generated from seeds; source prose, raw measurements,
company names and private source identities are not redistributed.

Eight cases (57 tasks) retain a route from a completed practitioner project.
Seven use standards-encoded routes in project-informed scenarios. The S/P column
in the manuscript describes route construction, not real versus synthetic
scenario provenance. Additional branches can be counterfactual even when a
case retains a source route. See `CASE_SOURCES.md` and `CONSTRUCTION_QC.md`.

A generator creates the data; diagnostic computations on those data determine
the guards and reference route. A fixed case graph can therefore demand
opposite choices under different seeds. Generated data and source extraction
are distinct stages of construction.

## Composition and access

- 15 cases and 97 tasks across all five DMAIC phases.
- 175 graph nodes and 29 statistical methods on reference routes.
- Four industry groups: discrete manufacturing, electronics, process industry and services.
- Five cases / 32 tasks are designated held out at the case level; all reported
  campaigns in the manuscript use the complete 97-task corpus, not a held-out score.
- Actual checkout availability must be checked against the registry; a public
  export and the full research checkout need not contain the same case files.

Per-case counts and route types are in manuscript Table `tab:corpus`.
`construction_qc_coverage.csv` enumerates the current case/seed instances and
sampled expert-review checkpoints; it is not a human acceptance checklist.

## Quality control and human involvement

The source survey records recovery of tables and legacy formats, OCR, duplicate
and illustrative-material checks, source verification of quoted quantities and
formula recomputation. Some records precede the final corpus; they establish
source-analysis practices rather than a 97-instance acceptance record.

Programmatic checks cover graph/guard behavior, generated data, routes, numerical
verification and reference execution. A perfect reference score cannot rule out
an error shared by the reference implementation and scorer.

Three independent human black-belt experts reviewed 30 checkpoints spanning all
15 cases and 26 distinct case/seed instances in study 1. Their feedback informed
corrections. Study 2 independently measured 60 fresh checkpoints across 12 cases
under a frozen protocol; its outcomes were not used to tune scoring rules.
Neither study certifies every value or branch in all 97 tasks. Protocols and
original judgments are retained under `paper/blind_review_2026-09-18/` and
`paper/blind_review_2026-09-19/`.

## Limitations and maintenance

The corpus does not provide a human end-to-end execution baseline. Source-project
practitioners, task authors and blinded reviewers play different roles. Source
routes do not validate synthetic counterfactual branches by themselves.

The review manifests identify the evaluated versions. Later generator, route or
scoring changes require renewed checks; a historical review must not silently
be treated as acceptance of a changed task. Source-page mapping and extraction/
review attribution should be consolidated privately where not already recorded.

Code and generated-data licensing are specified by `LICENSE` and `LICENSE-DATA`.
Those licenses do not grant redistribution rights to confidential source reports.
