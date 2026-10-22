# English canonical corpus migration (0.2.0)

English is now the canonical authoring language and the default task-build language.
The current repository does not maintain a bilingual or Chinese-language evaluation arm.
Any future Chinese corpus must be a separately versioned extension with its own validation,
release contract, and experimental results.

This language policy does not change source provenance. Some case structures were informed
by Chinese-language industrial project reports, and some current cases were migrated from
Chinese authoring using their existing English renderings. Those origins remain documented;
they must not be relabeled as originally English projects.

## What changed

Case metadata and generated data labels are authored directly in English. English locale
copies and translation glossaries are no longer the maintained source of truth. Current
prompts, comments, documentation, fixtures, and functional routing/scoring text use English.
Existing English task identifiers, including their `-en` suffixes, are retained even though
English is now the default. The migration does not silently rename historical English tasks.

The package version is 0.2.0 because the language API and defaults changed, and formerly
Chinese prompts in the legacy harness and v2/v3 adapters were translated. Those legacy
prompt bytes are different: results produced under their earlier prompts cannot be pooled
with results under the new prompts as if they were the same experimental condition. Rerun
those paths to evaluate the new prompts, and record the package/prompt version in results.

## Preserved historical records

Original experimental records are not translated or rewritten. In particular, these unused
legacy source snapshots remain byte-for-byte unchanged, including their Chinese text:

- `dmaic_bench/cases/adb_c06/frozen.json`
- `dmaic_bench/cases/adb_c13/frozen.json`
- `dmaic_bench/cases/adb_c21/frozen.json`

Their schema is `dmaic-bench/frozen-legacy-case`; current generators do not load them.
They are retained in Git but excluded from wheel package data, keeping the runtime
distribution free of these unused historical sources. They are explicit historical-provenance exceptions to the English-only current-authoring
policy, not a maintained Chinese task arm. Their SHA-256 hashes are pinned in
`tests/fixtures/historical_source_hashes.json`. Retained run artifacts likewise preserve
their original language and version attribution. English translations of review and design
prose preserve the claims and numbers recorded at the time; they do not retrospectively
revise historical findings or make them current results.

## Equivalence evidence and its limits

Before migration, a baseline captured 450 emitted English tasks covering clean, dirty,
and fault variants across the v1 and v2 task paths. Post-migration comparison found the
same task IDs, instructions, data blocks, steward configuration, and oracle outputs.
The numerical truth digest remains `da2cfe846ee660d5`. A separate comparison of
333 English scaffold directories found identical byte hashes for `TASK.md`, data,
and schema files against the pre-migration baseline.

The release-contract fixture is `tests/fixtures/english_release_contract.json`. It checks
agent-visible content and numerical/structural truths while excluding the translated
`derivation` and `metric_cue` text. Truth metadata differs for 282 tasks in those translated
fields. Fingerprint equality therefore does not by itself prove equivalence of every
possible free-text scoring input; English cue-matching and disclosure behavior also need
regression/replay checks. A separate contract compared 1,332 synthetic scoring fixtures
(333 v1 English tasks × four report scenarios: correct, wrong, missing, and disclosed)
and found exact pre/post equality. This is synthetic scoring regression evidence, not
a replay of historical model reports. It does not establish equivalence for the translated legacy
harness or v2/v3 prompts described above.

Run these checks from the repository root:

```sh
python tools/english_release_contract.py --check
python tools/english_scoring_contract.py
python tools/check_english_sources.py
python tools/truth_digest.py
```

The source check covers Git-visible text and validates the three historical snapshot hashes.
It is a guard for current source authoring, not a claim that every Git history revision,
external source document, ignored run archive, or binary image is English. Release packaging
and any figures must be checked within their own publication scope. Preserve numerical data,
truths, tolerances, IDs, guards, fault behavior, and existing user edits throughout language
maintenance; do not disguise untranslated content with Unicode escapes.

## Distribution validation

The `dmaic_bench-0.2.0` wheel was rebuilt with explicit runtime package data and
scanned: no retired locale/glossary files, historical frozen JSON snapshots, or Han
text remain in the wheel. An extracted-wheel smoke test discovered all 15 public
v1 cases and built 333 English clean/dirty/fault tasks at seeds 1–3. Historical
snapshots remain in Git unchanged. Stale `build/lib` contents must not be reused
when preparing a distribution; use a clean build checkout for release artifacts.

Harbor's version-derived verifier image tags now use `0.2.0`. Build the new base
and task images before running the new package; changing the version does not
publish images or rewrite existing datasets. Existing run artifacts and manifests
remain attached to their original version.

The final migration-focused test run passed 61 tests (3 skipped for unavailable
private inputs). Canonical case validation and the English authoring gate passed
for all 15 public v1 cases. Broader core and Harbor regressions were also run;
transient source/dependency-read failures passed on focused reruns. Optional
installed-Harbor model checks were verified separately on Python 3.12.

## Decision-label terminology

Current paper figures, tables, documentation, and derived analysis outputs use
`NO-GO` for the decision class previously displayed as `STOP`. The underlying
routes, decisions, numerical results, task IDs, and experiment-condition identifiers
(such as `permit-stop`) are unchanged. Ordinary uses of the verb "stop" remain.
Original blinded-review protocols, annotations, transcripts, and audit records retain
their recorded labels. Analysis readers normalize both legacy `STOP` and `NO-GO`
labels to `NO-GO`; those source records must not be rewritten just for presentation.
