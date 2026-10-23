# Paper reference and supporting evidence

The paper reference is recorded in [Publication status](../docs/PUBLICATION.md).
Its public arXiv link will be added after announcement. The manuscript's LaTeX
sources and compiled PDF are distributed separately from this code repository.

The two directories below contain expert-review evidence, rather than the
manuscript source. They are retained for inspection and reproducibility:

- `blind_review_2026-09-18/`: first expert review study.
- `blind_review_2026-09-19/`: second expert review study.

The [exploratory propagation audit](propagation_audit/) retains selected evidence
and result-lineage annotations previously stored with the manuscript. This is a
single Codex-assisted annotation pass, not new independent human adjudication.
The four audit files have been relocated without changing their contents.

The life-sciences per-trial evidence is in
`output/research/portability_pilot/`. The main industrial campaigns' raw job
archive is not included; see [Reproducing results](../docs/REPRODUCING_RESULTS.md).

Some analysis scripts still use the historical `paper/iclr/` path as a local
output target. That directory is Git-ignored and is not part of the public tree.
