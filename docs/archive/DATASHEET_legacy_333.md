# Datasheet — DMAIC-Bench

Structured after Gebru et al., *Datasheets for Datasets*. Every count in this
document was measured from the released build, not asserted.

---

## Motivation

**Why was this dataset created?** To measure whether an LLM agent can conduct a
multi-stage statistical investigation whose correct next step is a function of
what earlier steps computed. Existing agent benchmarks grade a terminal
world-state, a collapsed answer, or code that passes hidden tests; DMAIC has a
codified admissibility structure, so the *route* can be graded deterministically
instead of by an LLM judge.

**Who funded it?** Withheld during double-blind review.

---

## Composition

**What do instances represent?** One instance is a containerised task: a
business narrative naming no statistical method, a metered data steward holding
that case's data blocks, a turn budget, and a verifier holding the truth table
and the reference solution.

**Recorded released build** (`--languages en --with-faults`, 15 public cases):

These counts describe the build recorded for this datasheet. The current source corpus
uses canonical English and defaults to English; the explicit language flag documents
the historical build invocation. No Chinese arm is maintained. Chinese-language source
provenance remains documented, and any future Chinese extension must be separately
versioned and validated.

| | count |
|---|---:|
| Tasks | **333** |
| Cases | **15** |
| T1 atomic / T2 phase / T3 end-to-end | 294 / 30 / **9** |
| clean / dirty variants | 168 / 165 |
| Truth entries | 687 (456 hard, 231 soft) |
| Decision points | 147 |
| Methods in the taxonomy | 49, in 12 families |
| Tasks where NF is measurable | 213 / 333 (64.0 %) |
| Tasks where PQ is measurable | 111 / 333 (33.3 %) |
| On-disk size | 104 MB |

**The long-horizon tier is thin in the public release.** T3 carries 9 tasks
drawn from a single case, because the other end-to-end cases are the nine
held-out expert projects. A reader should not treat the public T3 slice as a
long-horizon benchmark; it is a worked example of one. See `HELD_OUT.md`.

**Is any instance derived from a real document?** No published instance
reproduces one. Every public case declares `provenance: SIMULATED` and
`parametric: true`: data comes from a seeded generator and truth is derived from
that data at generation time. The nine cases that derive from real project
reports are held out and are not in this repository.

A distinction worth stating plainly, because "SIMULATED" could otherwise be read
as broader than it is. Several public cases were **drafted around real project
work** — the industry, the instrument, the characteristic being measured and the
way the process fails are informed by completed Six Sigma projects. What is
generated is everything a reader could trace: all numbers, all batches, all
truths. **No real measurement, table, figure, sentence, product, organisation or
person from a source project appears in any published case**, the source corpus
is not redistributed, and no identity map is shipped. A case whose scenario was
informed by real work and whose every datum is generated is `SIMULATED`; the
label describes the data, and this paragraph describes the scenario.

**Does the data contain personal information?** No. No published case contains
a personal name, an organisation name, a location, or a date tied to a real
project. De-identification is enforced at build time, not by convention: a build
refuses to emit a corpus unless public-identity mode is set, and the released
package ships no identity map, so the reversing path is unreachable for a third
party.

**Is anything missing from individual instances?** Deliberately, yes. The
instruction never names a method — that is the measured capability, and a build
gate rejects any task whose rendered instruction leaks a method name or alias.

---

## Collection

**How was the data acquired?** Generated. Each case is a generator, not a
dataset: `generate(seed) → blocks`, then shared reference implementations run on
those blocks to produce the truth table. A new seed changes data and truth
together.

**Who was involved?** The authors. No crowdworkers were employed and no human
subjects were involved, so no compensation or IRB statement applies.

**Over what timeframe?** Case authoring and the release build, 2026.

---

## Preprocessing

**Was anything cleaned or labelled?** Truths are *derived*, never hand-written.
Every truth entry carries `derivation` metadata naming how it was produced, and
an onboarding gate independently recomputes it with a separate reference
implementation; a mismatch fails the gate.

**Is the raw data available?** The generator is the raw data. Given a case and a
seed, the entire instance regenerates byte-identically — a gate asserts this.

---

## Uses

**What is it for?** Evaluating agents on method selection, numeric fidelity and
process conformance in a gated, multi-stage statistical workflow.

**What should it *not* be used for?**
- Certifying an agent for regulated or safety-critical deployment.
- Ranking models on the public T3 slice — 9 tasks from 1 case cannot support a
  ranking.
- Any honesty or fabrication claim. That axis ships disabled
  (`honesty_axis_valid = 0`) because its estimator is demonstrably not
  honesty-monotone. See `SCORING.md`.
- Claiming DMAIC is the only defensible improvement methodology. The claim is
  narrower: DMAIC's process is codified enough to grade.

**Is there anything that could cause harm?** A benchmark that appears to
certify statistical competence could be cited to justify removing human review
from a quality decision. It does not support that, and `LIMITATIONS.md` says so
directly.

---

## Distribution

**How is it distributed?** As source in this repository plus a build step; the
task directories are build output, regenerable from the builder and a seed, and
are not committed.

**Licence.** Code MIT (`LICENSE`); corpus CC BY 4.0 (`LICENSE-DATA`).

**Any third-party restrictions?** None on the published corpus. Every shipped
case is self-authored and generates its data from a seed; no third-party data
file is redistributed and no case reproduces a third party's prose. That is
precisely why the nine expert cases are absent.

**One qualification, added when it became true.** `dmaic_bench/v2/cases/_sources/`
holds source records for cases being onboarded from **CC BY 4.0** literature, and
`docs/CASE_SOURCES.md` carries the attribution. Those records quote each article's
own licence notice and a small number of sentences as evidence for the numbers
extracted from them, so that a reviewer can check a value against the sentence it
came from. They are quoted under CC BY with attribution. What a source record
contributes to a case is the **scenario and the decision structure** — the
industry, the characteristic, its limits, and which numbers decided which
judgement. The data of any case built from one is still generated from a seed,
exactly as for every other case here.

No record enters unless the article is CC BY with **no NonCommercial and no
ShareAlike** clause, verified against the article's own `<permissions>` block
rather than an aggregator's metadata: licence fields were observed mislabelling
CC BY-NC as CC BY during the survey that produced these records.

---

## Maintenance

**Who maintains it?** Withheld during double-blind review; contact and takedown
address are published with the camera-ready.

**Will it be updated?** Yes — numbered releases, recorded in `CHANGELOG.md`.
Corrections to truth values, tolerance classes or gate behaviour are breaking
changes and get a minor version; new cases get a minor version; scoring changes
get a major version, because they invalidate previously reported numbers.

**How can someone extend it?** `CONTRIBUTING.md`. A case enters only through the
onboarding gates; there is no manual path.

**Will old versions be supported?** Tags are immutable. A reported number must
cite the version that produced it, because the reward formula has changed once
already and would silently change comparisons.
