# Reproducing results

## Inputs included in this repository

- Benchmark code, seeded generators, the scorer and reference implementations.
- Summary results: `RESULT_RESTRAINT.md`, `result_restraint.json`,
  `RESULT_PASSK.md`, and `RESULT_PORTABILITY_PILOT.md`.
- Expert review packages: `paper/blind_review_2026-09-18/` and
  `paper/blind_review_2026-09-19/`.
- Exploratory result-lineage audit: `paper/propagation_audit/`, a single
  Codex-assisted annotation pass with selected evidence and frozen packet hashes.
  It is not an additional independently validated expert review.
- Life-sciences per-trial evidence: `output/research/portability_pilot/`.

Paths in this list are relative to the repository root except for the summary
files, which are in `docs/`.

## Inputs not bundled

The main industrial campaigns' raw per-trial archive is not included. To
recompute those results, obtain the original run artifacts from the authors and
unpack them under `harbor/jobs/`. Merely cloning this repository does not make
those raw campaigns available. `scripts/export_results.py` exports scorecards,
traces, reports and steward logs from available jobs; it does not export terminal
recordings.

Use the exact scientific dependency versions in `pyproject.toml`, and activate
the same environment for reference-solution subprocesses.

## Numerical summaries and local publication outputs

After restoring the original run archive and the matching corpus build:

```bash
mkdir -p paper/iclr/figures
python scripts/rescore.py harbor/jobs/<job> [<job> ...] --dataset harbor/datasets/dmaic-bench-r3 --apply
python scripts/restraint_analysis.py --md docs/RESULT_RESTRAINT.md --tex paper/iclr/numbers.tex
```

`paper/iclr/` is an ignored local output directory, retained as a generation
target for existing analysis scripts. Its name does not imply that manuscript
sources or compiled paper PDFs are checked in. Scripts such as
`control_replicated.py`, `lockability.py`, `reward_sensitivity.py` and
`appendix_case33.py` also need the original run inputs and may write LaTeX or
figure outputs there.

Manuscript-layout utilities, notably `check_paper_figures.py` and
`fig_task_breakdown.py`, additionally read the full manuscript or its figure
manifest. They require the separately distributed arXiv source project, with
its files extracted into the expected local layout. They are not benchmark
runtime dependencies. The public paper link is in [Publication status](PUBLICATION.md).

## Validation record

[Release verification](RELEASE_VERIFICATION.md) records the tested environment,
source-export parity and the pre-existing contract-fixture regression. A Chinese
README translates the documentation; the validated task instructions, generators,
scoring and recorded experimental inputs remain English.
