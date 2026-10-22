# Changelog

Versioning policy: a reported number must cite the version that produced it.

* **major** — any change to a scoring axis or the reward formula. These
  invalidate comparison with previously reported numbers.
* **minor** — new cases; corrections to truth values, tolerance classes, or gate
  behaviour.
* **patch** — documentation, packaging, and changes that cannot move a score.

Tags are immutable.

## Public distribution licensing - 2026-10-22

- License the current public software distribution under GNU AGPL version 3 only
  (`AGPL-3.0-only`), including the benchmark framework and the `dmaic-harbor`
  integration. Synchronize package metadata, container metadata and documentation.
- Preserve the generated corpus's separate CC BY 4.0 license and the paper's
  separate publication status. No benchmark code, data or scoring behavior changes.
- This licensing update does not revoke rights validly granted with earlier
  distributions.

## [0.2.0] - 2026-09-26

First public release. It contains the material the manuscript
`paper/iclr/dmaic_bench.tex` rests on.

### Corpus
- v2 corpus: 15 cases, 97 tasks, 175 graph nodes across the five DMAIC phases, 66 graded
  forks, 29 statistical methods (`dmaic_bench/v2/cases/`, `docs/DATASHEET.md`). Eight cases
  take their scenario and decision structure from real black-belt closure reports; every batch
  regenerates from a seed and no source material is redistributed (`docs/CASE_SOURCES.md`).
- Held-out designation at the case level: five cases, 32 tasks, drawn on structural criteria
  with a published seed (`docs/HELD_OUT_V2.md`). Every reported campaign ran over all 97 tasks.
- 12 honesty-probe variants in which one batch or one field is withheld.
- English case text is canonical and English is the default build language; no Chinese arm
  ships (`docs/ENGLISH_MIGRATION.md`).
- The v1 corpus (`dmaic_bench/cases/`, `adb_c01` to `adb_c24`) is retired and kept for
  traceability; no reported number is measured on it.

### Harness and scoring
- Harbor 0.22.0 packaging with the stock terminal agent loop: task builder, data steward,
  in-container verifier, offline verifier base image, guarded campaign launcher
  (`harbor/`, `scripts/`).
- Reward = harmonic mean of method recall, method precision, numeric fidelity and route
  conformance, times (1 minus misuse), times the integrity gate (`docs/SCORING.md`).
  The verifier scores a boolean output as a 0/1 indicator instead of dropping it
  (`harbor/src/dmaic_harbor/verify.py`); no DMAIC truth is an indicator, and re-scoring under
  the old and the new scorer gives identical rewards on every DMAIC trial.
- Reference solution at 1.000 and null agent at 0.000 on all 109 tasks (97 clean plus 12
  probes), containerised, against the same build as every contestant.

### Campaigns
- 13 systems from six providers, three complete attempts per task, one build, one scorer;
  every campaign re-scored offline under one tagged scorer version
  (`docs/RESULT_RESTRAINT.md`, `docs/RESULT_PASSK.md`, `paper/iclr/numbers.tex`).
- Instruction controls on 32 paired tasks: permit-stop on all 13 systems
  (`paper/iclr/tab_control.tex`); a replicated control on two systems under five instruction
  conditions (plain, permit-stop, permit-paraphrase, normative, remind), three attempts, 960
  trials (`paper/iclr/tab_ctlrep.tex`, `docs/control_pairs_2026-09-19.json`).
- Two blind expert reviews by three domain experts: 30 trajectory units
  (`paper/blind_review_2026-09-18/`) and 60 fresh units, 40 no-go and 20 go twins
  (`paper/blind_review_2026-09-19/`), with packets, sealed-input hashes and the reviewers'
  records.
- Per-trial run artifacts (traces, reports, steward logs, scorecards) are distributed as an
  archive with the tagged release, not in the tree; `scripts/rescore.py` and
  `scripts/restraint_analysis.py` regenerate every table and macro file from it.

### Life-sciences extension
- Second-domain portability pilot: two cases outside DMAIC, `adb_c40` (bulk RNA-seq under
  library-batch structure) and `adb_c41` (case-control genotype association under cohort
  structure), eight seeds each; fourteen methods with numpy/scipy reference implementations
  (`dmaic_bench/truth/omics.py`); opt-in at discovery (`DMAIC_PILOT_DOMAINS=1`), so the
  97-task corpus and its counts are unchanged. Three systems, three attempts under the
  protocol brief and one under the thresholds-only brief. Design in `docs/PORTABILITY_PILOT.md`,
  every count in `docs/RESULT_PORTABILITY_PILOT.md`, per-trial evidence in
  `output/research/portability_pilot/`.

### Documentation and licensing
- `docs/README.md` indexes the documentation; retired design and result notes are under
  `docs/archive/`.
- Separate software and generated-corpus licensing; see `LICENSE`, `LICENSE-DATA`
  and the current public-distribution licensing entry above.
