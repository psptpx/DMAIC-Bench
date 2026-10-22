# The v2 held-out split

`docs/HELD_OUT.md` describes a split of the **v1** corpus (`adb_c01`–`adb_c24`), held out for
licensing reasons: those cases derive from real company reports nobody granted us the right to
republish. Every measurement in this repository is on the **v2** corpus (`adb_c25`–`adb_c39`),
which is fully synthetic and to which that argument does not apply. Until now v2 had no split
at all, and a benchmark whose every task is public — generator, decision graph, truth fields —
has no contamination defence worth the name.

**Nothing has been published yet.** The remote carries one commit; 74 commits of v2 work and
every case module are local. So this is a design decision taken before release, not a
remediation after one.

## The split

| | cases | tasks |
|---|---|---|
| public | 10 | 65 |
| **held out** | **5** | **32** |

Held out: `adb_c25`, `adb_c26`, `adb_c28`, `adb_c34`, `adb_c39`.

## Whole cases, not seeds

A v2 case IS its decision graph. The data regenerates from a seed, so publishing a generator
and withholding some of its seeds withholds nothing: the routing logic — which is the thing a
contestant would have to have memorised — is in the module either way. The unit of holding out
is therefore the case: its graph, its guards, its truth fields and its generator never enter
the public artifact.

## How the five were chosen, and how they were not

Exhaustive enumeration over 5-case subsets, filtered on **structural criteria only**:

* 28–35 tasks;
* tier proportions within 6 points of the corpus (A 47% / B 21% / C 32%);
* both halves keeping at least three industries;
* the public half keeping every `y_type` in the corpus.

536 subsets qualified. One was drawn from them with `random.Random(20260916)`.

**No contestant score entered the selection.** Choosing among the 536 by how well each matched
measured difficulty would be choosing the split with the test data, which is the one thing a
held-out split exists to prevent. The draw is reproducible from the published seed.

## What the draw gave, measured afterwards

Tier mix **50 / 19 / 31** against the corpus 47 / 21 / 32 — a close structural match, which the
filter guaranteed.

Difficulty did NOT come out even. The held-out half is easier:

| | held out (32) | public (65) |
|---|---|---|
| GLM-5.3-Flash | 0.575 | 0.549 |
| GPT-5.6-sol | 0.685 | 0.622 |

**This is reported rather than corrected.** Re-drawing until the halves matched is precisely
the selection-on-outcome the procedure above avoids, and doing it after seeing the scores would
be worse than not splitting at all. A held-out score should be read as roughly 0.03–0.06
optimistic relative to a public one, and a paper reporting both must say so.

The public half keeps `mixed` as a `y_type` (only `adb_c38` has it) and all three tiers.

## The mechanism, and the test that it works

`dmaic_bench.v2.registry.HELD_OUT_CASES` names them; `discover(include_held_out=False)` and the
`DMAIC_PUBLIC_ONLY` environment variable give the public view without deleting anything, so a
maintainer can build exactly what a third party sees.

A constant naming five cases is worth nothing if a build still emits their truth packages, so
`tests/test_held_out_v2.py` builds under the public view and asserts each held-out identifier
appears **nowhere** — not in a directory name, not in a truth package, not in an instruction,
not in the manifest. It failed on the first run: `solve.sh`, which ships inside every public
task, carried two comments citing `adb_c34` and `adb_c39` by name as the source of a measured
correction. The engineering rationale stayed; the identifiers went.

## What the split does not fix

It is a contamination defence for the FUTURE. Both campaigns reported in this repository were
run over all 97 tasks, on a private tree, before the split existed; their numbers are honest
for what they are but they are not held-out results. The first genuinely held-out figure will
be the first contestant run after publication.
