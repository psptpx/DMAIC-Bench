# Contributing

## Adding a case

A case enters only through the onboarding gates — there is no manual path, and a
case that fails any ERROR-level gate cannot be built.

1. Copy `dmaic_bench/cases/_template/` and write `case.yaml` + `generator.py`.
2. Truths must be **derived, never hand-written**. `generate(seed)` produces the
   data; a reference implementation in `dmaic_bench/truth/` produces the truth
   from that data. If a method has no reference implementation, add one first.
3. The narrative must name no method. Gate V3 rejects the case otherwise, checking
   every identifier and alias in the 49-method taxonomy.
4. Run the gates: `python3 -m dmaic_bench.cli validate <case_id>`.
5. Both suites must pass: `pytest` in the repository root and in `harbor/`.

## The gates

| gate | checks | level |
|---|---|---|
| V1 | schema | ERROR |
| V2 | every `method_id` exists in the taxonomy | ERROR |
| V3 | context and goal contain no method name | ERROR |
| V4 | same-seed generation is byte-identical twice | ERROR |
| V5 | different seeds yield different data | ERROR |
| V6 | truths reference valid stages and carry `derivation` | ERROR |
| V7 | truths are independently recomputed and matched | ERROR |
| V8 | every stage has a non-empty serialisable data block | ERROR |
| V9 | fault and decision references resolve | ERROR |
| V10 | stage binding is unambiguous | WARN |
| V11 | phase coverage | WARN |

## What will be rejected

- A truth value that a reference implementation cannot reproduce.
- A case whose narrative, stage label, or steward topic names a method.
- Any real organisation name, personal name, or document derived from a source
  we cannot redistribute. See `docs/HELD_OUT.md` — this is not negotiable.
- A credential, endpoint list, or anything resembling one, in any file.

## Style

English is the canonical language for case text and the default for task builds.
Use English throughout the public repository: documentation, comments, fixtures,
instructions, stage labels, data labels, steward messages, CLI help, and error text.
Preserve source provenance accurately; an English release does not imply that
its source project reports were written in English. There is no maintained Chinese
arm. Any future Chinese extension must be separately versioned and validated.

Translation must preserve numerical data, truths, tolerances, method and stage IDs,
guards, and fault behavior. Check routing and scoring after translating functional
strings; do not expose the expected statistical method through a translated label.
Historical experimental records retain their original provenance and must not be
rewritten to imply that an old run used the current English corpus.

The three archived `cases/*/frozen.json` snapshots named in
`docs/ENGLISH_MIGRATION.md` are explicit exceptions: preserve their original bytes,
including Chinese source text. They are not loaded by current generators. The source
check validates their pinned hashes rather than translating them.
