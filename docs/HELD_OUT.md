> This file describes the retired v1 split (`adb_c01` to `adb_c24`, nine cases withheld for licensing). The measured v2 corpus and its five held-out cases are described in [`HELD_OUT_V2.md`](HELD_OUT_V2.md).

# The held-out split (v1 corpus)

> **This document is about `adb_c01`–`adb_c24`, the v1 corpus, and the reason those nine are
> withheld is LICENSING.** Every measurement in this repository is on the v2 corpus
> (`adb_c25`–`adb_c39`), which is synthetic and has its own, separately drawn split — see
> `docs/HELD_OUT_V2.md`. Reading this file as a description of what is held out today would be
> wrong in both the identifiers and the reason.

This repository publishes **15 of the benchmark's 24 cases**. Nine are held out.
This document states exactly which, why, and what a third party can and cannot
verify without them.

## What is published

| | cases | provenance | `parametric` |
|---|---|---|---|
| **Public** | 15 | `SIMULATED` | `true` — data and truth regenerate from a seed |
| **Held out** | 9 | `RECONSTRUCTED` (7), `TRUE` (2) | `false` — frozen constant arrays |

Public case identifiers: `adb_c01 c02 c04 c06 c09 c11 c12 c13 c14 c17 c18 c21
c22 c23 c24`.

Held-out case identifiers: `adb_c03 c05 c07 c08 c10 c15 c16 c19 c20`.

The identifiers are opaque by construction — the numbering comes from a
permutation fixed once at random, screened against the former alphabetical
ordering, and applied to **all** cases rather than only the nine, so that the
opaque set is not itself the set of real organisations.

## Why the nine are held out

**Licensing.** The nine derive from Six Sigma project reports produced inside
real companies. The source library carries no copyright statement and no
redistribution grant; the absence of a marking is not a grant. We therefore have
no right to redistribute material derived from those documents, and we do not.

**Consent.** We hold no permission from the report authors or their employers to
republish, and there is no ledger recording one.

**Re-identification.** The nine trace to six or seven organisations in a single
country and sector. A case narrative describes a process in enough detail that
content-level re-identification remains possible in principle. That is the floor
for any public benchmark built on real industrial cases; the honest response is
to publish the synthetic corpus and withhold the rest, not to claim the
anonymisation reaches below that floor.

**They are not, as implemented, "reconstructions."** The onboarding
specification describes `RECONSTRUCTED` as parameters inverted from published
summary statistics and regenerated. No held-out case delivers that: all nine
ship `parametric: false` and frozen constant arrays. Whatever fair-use argument
a genuine reconstruction might support is therefore not available to them as
they stand, and we treat the seven and the two as one class.

## What this costs, stated plainly

The public corpus loses the real-project difficulty axis. `expert_hours` is
recorded only for the nine, so the observed-effort difficulty measure does not
apply to any published case. Any claim in an accompanying paper that rests on
the nine — the human reference line, the effort axis, the industry mix — is a
claim a third party **cannot** reproduce from this repository. Those claims are
marked as such wherever they appear.

The public corpus keeps: the full 49-method taxonomy, all five DMAIC phases, the
decision-graph task model, the data steward, the scoring implementation, the
validation gates, the Harbor packaging, and the reference (oracle) and null
(nop) agents that bound the scale at both ends.

## What the split buys

A held-out set is also the contamination defence this benchmark otherwise lacks.
The published tasks ship their own `truth.json` and a `solution/plan.json`
naming the required methods, so the public corpus is, by design, readable by
anything that crawls this repository. The held-out nine are not, and never
enter it. Future evaluation on the held-out split therefore measures a corpus
that could not have been memorised from this artifact.

We would recommend the split even if the licensing question resolved in our
favour.

## Status

The licensing question is open, not closed. If permission is obtained for any
held-out case, it moves to the public split in a numbered release and is
recorded in CHANGELOG.md. Requests for evaluation on the held-out split, and
takedown requests, go to the contact in docs/DATASHEET.md.
