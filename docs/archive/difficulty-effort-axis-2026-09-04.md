# The difficulty axis: observed human effort in DMAIC-Bench

**Date:** 2026-09-04
**Scope:** `dmaic_bench/cases/*/case.yaml`, and the per-case effort ledger that is held
with the held-out corpus.
**Status:** data complete and evidence-backed; see
[Wiring still required](#wiring-still-required).

> **Read this first — what a reader of the public release can and cannot check.**
> This note describes the difficulty axis over the **full 24-case development corpus**.
> Every case that carries an observed-effort figure is one of the nine expert-derived cases
> **held out of the public release** (`adb_c03 c05 c07 c08 c10 c15 c16 c19 c20` — see
> [`HELD_OUT.md`](../HELD_OUT.md)). All 15 published cases record a null `expert_hours`, each
> with its reason stated in `effort_source`, so **none of the figures in the distribution,
> anchor, coverage or lower-confidence sections below is reproducible from this
> repository.** The effort ledger
> is held out with them: it necessarily carries real organisation names, rosters and
> document references, and is not redistributable. What the public release *does* carry is
> the schema — the `expert_hours` / `junior_hours` / `effort_source` fields on every
> `case.yaml`, the conversion rule recorded in `dmaic_bench/cases/_template/case.yaml`, and
> the null-with-a-stated-reason convention described under
> [Coverage](#coverage-reported-honestly).

## Why this exists

DMAIC-Bench saturates. 58% of project-tier trials score exactly 1.000, and every
atomic-tier trial lands on exactly 1.000 or exactly 0.000. (Measured over campaign runs on
the full corpus. Project-tier trials are trials on the nine held-out cases, so this
particular measurement cannot be reproduced from the public release.) A scoring change does
not fix that, and neither does dropping the tasks models happen to solve — you cannot repair
after the fact a distribution you never designed.

Terminal-Bench (arXiv 2601.11868v1) treats difficulty as a **design input measured in human
hours**: expert-hours and junior-hours per task (p. 3, p. 5), enforced by keeping only 89 of 229
submissions on human review, *before any model score exists*. We had no effort axis at all.

We can be better grounded than they are. Terminal-Bench's hours are **estimates by the task
author**, and they publish the consequence: human-versus-empirical difficulty correlates at only
**r = 0.436**. Our project-tier cases are **completed industrial Six Sigma projects executed by
human quality and lean engineers**, and their source decks record real charter dates, real gantt
schedules, real team rosters and real meeting cadence. The duration and team-size inputs below
are **quoted facts**, not recollections.

## What was mined

The source corpus is a private collection of completed Chinese Six Sigma project reports
held by the authors — 95 ledger entries, plus OCR sidecars for the scanned decks. It carries
no redistribution grant, is not published, and is not part of this repository; see
[`HELD_OUT.md`](../HELD_OUT.md). Nine of the benchmark's 24 cases descend from a real project
document, and those nine are exactly the held-out split. Every one of them turned out to carry
an explicit schedule and an explicit roster — a better hit rate than expected, because a Six
Sigma project report is *required* by the methodology to contain a project-plan slide
(`D8`/`D9` in the deck templates these reports use) and a project-team slide (`D7`/`D8`).
The methodology's own reporting template is what makes this axis observable.

Evidence quality found, per case:

| Evidence type | Cases |
|---|---|
| Planned **and actual** per-step dates | adb_c19 (15 steps), adb_c20 (5 phases) |
| Explicit per-phase date ranges | adb_c05, adb_c08, adb_c16 |
| Stated project period + task gantt | adb_c07, adb_c15 |
| Stated duration in days + month-resolution gantt | adb_c03 ("150 days"), adb_c10 ("180 days") |
| Named roster with functional roles | all 9 |
| Meeting cadence stated | adb_c08 (weekly, 1.5 h), adb_c15 (weekly), adb_c19 (2×/month), adb_c20 (per-member table) |
| **Man-days or labour hours stated** | **none — see below** |

## The conversion assumption

**No deck in the corpus states effort.** A search for the Chinese terms for man-day,
person-day, labour input and man-month across all ~100 extracted documents returns no
project-effort statement. What is observed is *duration*, *team size* and *cadence*. Converting
those into practitioner-hours therefore requires one declared assumption, applied uniformly:

```
expert_hours = business_days(start, end) × 8 h/day × Σ role_allocation

role_allocation:  project lead / black belt      0.25 FTE
                  core functional team member    0.10 FTE
                  champion / MBB / coach / finance 0.02 FTE
```

- `business_days` counts Mon–Fri inclusive between the two recorded dates. Chinese public
  holidays are **not** deducted — a known upward bias of roughly 3–5% over a six-month span.
- `expert_hours` is defined as **total practitioner-hours contributed by the recorded team**,
  summed across roles. That is the right analogue of Terminal-Bench's per-task expert-hours,
  because a benchmark contestant executes the entire project alone.
- The allocation fractions encode the standard part-time character of a belt project: the belt
  leading it carries it as about a quarter of the working week, a functional member roughly a
  tenth, a steering role a token fraction.

### The assumption is checked, not merely asserted

`adb_c08` is the only deck that states both a standing-meeting cadence and its duration:

> *(translated from the deck)* One all-hands meeting per week, capped at 1.5 h, Wednesdays
> 09:00–10:30, minuted by the project secretary.

21 people × 1.5 h × 35 business weeks = **1102 h of standing meetings alone**, which is **32%**
of the 3416 h this rule produces for that case. Meetings are a floor, never the whole of a
project, so a rule landing meetings at about a third of total effort is consistent; a rule
producing under 1102 h would have been contradicted by the deck itself. This is one independent
check, not a validation across the set — it is the only one the corpus supports.

## The distribution

Nine cases, sorted by observed effort:

| Rank | Case | Span (recorded) | Cal. days | Bus. days | Team (lead/core/support) | FTE | **Expert-hours** | Conf. |
|---:|---|---|---:|---:|:---:|---:|---:|:---:|
| 1 | adb_c16 | 2025-02-26 → 2025-03-18 | 21 | 15 | 1 / 10 / 0 | 1.25 | **150** | high |
| 2 | adb_c03 | 2024-02-01 → 2024-06-30 | 151 | 107 | 1 / 6 / 3 | 0.91 | **779** | medium |
| 3 | adb_c05 | 2023-03-10 → 2023-08-30 | 174 | 124 | 1 / 6 / 2 | 0.89 | **883** | high |
| 4 | adb_c07 | 2024-06-02 → 2024-11-30 | 182 | 130 | 1 / 5 / 12 | 0.99 | **1030** | medium |
| 5 | adb_c20 | 2024-04-03 → 2024-10-31 | 212 | 152 | 1 / 5 / 5 | 0.85 | **1034** | high |
| 6 | adb_c19 | 2023-03-08 → 2023-10-25 | 232 | 166 | 1 / 5 / 2 | 0.79 | **1049** | high |
| 7 | adb_c10 | 2024-01-01 → 2024-07-07 | 189 | 135 | 1 / 8 / 3 | 1.11 | **1199** | high |
| 8 | adb_c15 | 2023-03-01 → 2023-12-31 | 306 | 218 | 1 / 7 / 3 | 1.01 | **1761** | high |
| 9 | adb_c08 | 2022-04-30 → 2022-12-31 | 246 | 175 | 2 / 19 / 2 | 2.44 | **3416** | high |

**Summary statistics**

| Statistic | Expert-hours |
|---|---:|
| n (cases with a figure) | 9 |
| Median | **1034** |
| Mean | 1256 |
| Std. dev. | 912 |
| Min | 150 (adb_c16) |
| Max | 3416 (adb_c08) |
| Range ratio | **22.8×** |
| Q1 / Q2 / Q3 | 831 / 1034 / 1480 |
| Cases with **no figure** | **14** (all T1, all SIMULATED) |

Underlying observed quantities: calendar span median 189 days (range 21–306); team size median
11 people (range 8–23).

The axis discriminates. It spans 1.36 orders of magnitude, and it does so on two independent
axes at once — duration and headcount — rather than one. Excluding the three-week rapid-response
case (adb_c16), the remaining eight still span 4.4× (779–3416 h), so the spread is not an
artefact of a single outlier.

## Coverage, reported honestly

| Group | Cases | With observed effort |
|---|---:|---:|
| T3 project tier (provenance TRUE / RECONSTRUCTED) | 9 | **9 / 9 (100%)** |
| T1 atomic tier (provenance SIMULATED) | 14 | **0 / 14 (0%)** |
| **Total** | **23** | **9 / 23 (39%)** |

This census was taken over the 23 cases registered at the time; `adb_c24` was added afterwards
as a 15th `SIMULATED` case, also with a null figure, making the corpus 24 with the coverage
unchanged at 9 / 24. Those 15 `SIMULATED` cases are exactly the public split, and the 9
effort-bearing cases are exactly the held-out split ([`HELD_OUT.md`](../HELD_OUT.md)).

The split is not arbitrary and it is not a gap to be closed. The 14 unpopulated cases are
synthetic — authored for the benchmark, with no human project behind them. There is no effort to
observe, so no figure is entered; each of their `case.yaml` files now records that explicitly in
`effort_source` rather than leaving the field blank and ambiguous.

The coincidence worth stating in the paper is that **the tier with 100% effort coverage is
exactly the tier that saturates** (58% of project-tier trials at 1.000). The difficulty target
is now measurable precisely where it is needed.

## junior_hours is null everywhere, deliberately

Terminal-Bench collects expert-hours and junior-hours independently. Our sources record only
the team that actually ran the project, and those teams were led by certified black belts under
MBB coaching. **No deck records a solo execution by an engineer new to the method set**, so
there is no observed junior figure and none is entered.

Two decks are tempting and were rejected on inspection:

- adb_c03 — *"a boundaryless team made up of three parts: 1 MBB + 2 BB + 4 GB"*
- adb_c10 — *"team composition: 1 expert resource + 2 BB + 6 GB, a boundaryless team"*

Both record **belt composition**, and the green-belt count looks like a junior proxy. It is not.
A green belt's share of a black-belt-led team is not the time a junior would need to run the
project alone; recording it as `junior_hours` would be a category error, and multiplying
expert-hours by an invented ratio would convert the observed axis straight back into the
estimated one this work exists to improve on. Left null. If junior-hours are wanted, they must
be collected — not derived.

## The two anchors

### Easiest: adb_c16 — 150 expert-hours

A three-week rapid-response containment, not a chartered belt project. Triggered when a customer
moved from sampled to 100% SI testing and the resulting daily reject rate hit ~15%.

> `D2` problem description — occurrence date 2025-02-26; *"of 100 PCS tested, 18 PCS were
> defective, a defect rate of 18%"*
> `D4` project completion schedule — a **daily** gantt, columns 2/26, 2/27, 2/28, 3/1 … 3/15,
> each DMAIC phase carrying a planned and an actual band
> `D3` project members — a named team lead plus 10 named members across quality, PE,
> production, moulding and SI (11 individuals named in the deck; names withheld here)
> cover date: 2025-03-28

15 business days × 8 h × (0.25 + 10×0.10) = 150 h. Large team, very short clock — the inverse
shape of every other case in the set, which is why it anchors the low end without being a
trivial task.

### Hardest: adb_c08 — 3416 expert-hours

Eight months and a 21-person team — 2.6× the median roster and the longest team-weighted span.

> `D8` project plan: Define start **2022-04-30** | Measure complete **2022-05-15** |
> Analyze complete **2022-05-31** | Improve complete **2022-06-15** |
> Control complete **2022-12-31**
> `D6` team formation: 1 project lead and 1 deputy lead; 6 members from quality management,
> 8 from smart manufacturing and 5 from manufacturing quality; 1 champion; 1 sponsor
> (23 individuals named in the deck; names withheld here)
> `D7` team charter: one all-hands per week capped at 1.5 h; team attendance and
> task-execution records maintained

175 business days × 8 h × (2×0.25 + 19×0.10 + 2×0.02) = 3416 h.

**Caveat that belongs in the paper.** adb_c08's analytical work is concentrated in the first
**33 business days** (Define through Improve, 2022-04-30 → 2022-06-15 — about **644 h** on the
same rule). The remaining six and a half months are Control: standardisation and horizontal
rollout. A benchmark task stopping at the Improve conclusion is closer to 644 h than to 3416 h.
The full-span figure is recorded because DMAIC-Bench T3 tasks require a complete DMAIC
report *including* Control — but adb_c08 is the one case where the choice of endpoint moves the
number by 5×, and it is also the case that sets the top of the range. It should not be quoted as
the hardest case without that sentence attached.

## Lower-confidence figures

Two of the nine are marked `medium`; the rest are `high`.

- **adb_c03** — start date only. The gantt's first column is "February" with no
  day-of-month, so 2024-02-01 is assumed. The deck's own stated total of 150 days
  independently corroborates it (2024-02-01 + 150 d = 2024-06-30). Team size is exact.
- **adb_c07** — team size only. The externally released deck already redacts personal names
  to a single character in the "team lead" / "deputy lead" slots, and the OCR of that org
  chart is partly garbled, so 5 core + 12 support is read off role labels rather than a clean
  roster. Both dates are exact and stated twice (a cover-slide project period of June 2024 –
  December 2024, and the task gantt 2024/6/2 → 2024/11/30).

## A by-product worth keeping: schedule fidelity

Two decks record planned **and** actual dates at step level (adb_c19, 15 steps; adb_c20,
5 phases). That is a free, already-collected measurement of how well a human team holds a DMAIC
schedule, and it is not effort — it is not used above and it is not a junior-hours proxy. It is
noted here because it is the kind of ground truth that is expensive to collect and easy to lose:
adb_c19 ran 232 days against a 235-day plan, finishing 5 days early, while individual steps
drifted from 11 days early to 5 days late.

## Where the data lives

- **The effort ledger** — the authoritative record: per case, the source document and page,
  the quoted evidence in the original Chinese with an English gloss, the dates, the roster
  breakdown, the arithmetic and the confidence level. It is held with the held-out corpus and
  is **not published**, because it necessarily carries real organisation names, rosters and
  document references ([`HELD_OUT.md`](../HELD_OUT.md)).
- **`dmaic_bench/cases/*/case.yaml`** — the native (T1, SIMULATED) cases carry
  `expert_hours`, `junior_hours` and `effort_source`, all null with an explicit stated reason.
  These are the published cases.
- **`dmaic_bench/cases/_template/case.yaml`** — carries the fields plus the conversion rule,
  so the next case authored inherits the axis instead of rediscovering it.

## Wiring still required

Two changes were needed for these figures to reach `CaseMeta` at runtime. Both were in files
owned by other agents, so neither was made in the work this note records:

1. **`dmaic_bench/core/registry.py`**, `meta_from_yaml` — the parser reads its fields
   explicitly and did not pass the three effort keys through. Extra keys in `case.yaml` are
   schema-legal (`case.schema.json` does not set `additionalProperties: false`) and parse
   fine, but they were dropped on the floor. **Since done:** `meta_from_yaml` now reads
   `expert_hours`, `junior_hours` and `effort_source`, and they are fields on `CaseMeta` in
   this release.
2. **The frozen-asset bridge for the effort-bearing cases.** The nine cases that *have*
   observed effort are frozen-asset cases, with no `case.yaml` at all. Adding one would break
   `registry.discover()`, which requires a `generator.py` alongside. The bridge needs to read
   the figures from the effort ledger (or from a `meta.expert_hours` added to each frozen
   asset) and pass them into the `CaseMeta` it constructs. **Not applicable to the public
   release:** all nine are held out, so neither the bridge nor the frozen assets are in this
   repository ([`HELD_OUT.md`](../HELD_OUT.md)).

Note for whoever does (2) in the development tree: the frozen/live meta parity test compares
the live-rebuilt meta against the frozen meta, so the live builder and the frozen builder must
be given the effort figures **together**, or parity will fail.

## Verification

Run in the development tree: `python3 -m pytest tests -q` — 738 passed before this work,
**746 passed, 0 failed** after. The 8 additional tests come from concurrent work by another
agent in `core/`, `scoring/`, `truth/` and `tests/`; no test was added, removed or modified
here. Those are the development tree's counts, not this repository's — the public suite is
smaller, because the held-out cases and the tests that cover them are not here.

One guard fired during the work and was correct to: the packaging-hygiene test that forbids a
romanized company name anywhere in the built distribution rejected a real company name used
as a worked example in the template's comment. The example now names the document by location
only. That guard is also the reason the effort ledger — which necessarily carries real
organisation names, rosters and document references — is kept outside the packaged
distribution, alongside the map from each opaque `adb_cNN` id to its real-world origin.
Neither file is published ([`HELD_OUT.md`](../HELD_OUT.md)).

No truth value, tolerance, stage or method was changed.
