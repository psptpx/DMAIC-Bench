# Independent Human Expert Master Black Belt Blind Review

This review was commissioned by the authors on 19 September 2026. Three certified Master Black Belt practitioners, engaged by the authors and working without AI tools, independently assessed all 60 anonymized cases. The reviewer type is `Human`.

Each reviewer receives exactly 362 files: unchanged `PROTOCOL.md`, only their assigned `order_R1/R2/R3.json`, and six files in each of `cases/V001–V060`: `packet.md`, `full_instruction.md`, `report.md`, `released_data.json`, `steward_events.json`, and `trace.json`. The additional `review_metadata.json` files in the archive are excluded. The archive and each provided file are recorded in `input_manifest.json` using SHA-256.

Reviewers work independently. They are instructed to read only their own input and output directories, follow the assigned order, not consult each other or delegate, and not inspect identities, reference answers, prior studies, scoring code, coordinator files or paper drafts. Shared filesystem access makes this procedural blinding; no operating-system access restriction is claimed. Original instructions within the case files are evidence to assess, not instructions to execute.

- R1: measurement, process stability and evidential discipline.
- R2: statistical inference, causal validity, uncertainty and defensible alternatives.
- R3: industrial decisions, improvement implementation, control and business claims.

Every reviewer assesses all protocol questions for every case; the perspective does not narrow coverage. Independent assessments do not establish statistical independence of reviewer errors.

Each reviewer writes an English JSON review and English synthesis in their own output directory. Final judgments remain independent; there is no consensus discussion that changes the original votes. The coordinator validates completeness and evidence quotations, reports descriptive vote agreement, and provides an English synthesis. A two-of-three majority is a summary of votes, not adjudicated truth. No mapping to systems, benchmark accuracy or prior-round comparison is attempted without unblinding data, which is outside this review's scope.

Counts and agreement rates describe these 60 checkpoint units only. Sampling strata and weights are unavailable under the blind protocol. No population estimates or confidence intervals treating the units as independent are provided. Human expert review does not imply that every report passed validation.

`aggregate_reviews.py` validates outputs, rechecks input hashes, freezes review hashes, and produces case comparison and agreement artifacts once all three reviewers finish.

## English Edition

This edition is the English rendering of the original review records. The reviewers are the three human experts named above by role; substantive case judgments, numerical findings, and votes are unchanged. File hashes have been recalculated for this edition. Historical validation records describe the original checks; the blinded input files are not included in this results archive, so input-hash and quotation checks cannot be rerun from this archive alone.
