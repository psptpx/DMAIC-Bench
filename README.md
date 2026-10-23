# DMAIC-Bench

**English** | [Chinese](README.zh-CN.md)

[Code repository](https://github.com/psptpx/DMAIC-Bench-public) ·
[Paper / arXiv status](docs/PUBLICATION.md) · [Citation metadata](CITATION.cff)

From self-reflection to self-restraint for agents in multi-stage analytical
tasks. A benchmark of 97 tasks over 15 industrial improvement projects, with a
sixteen-task life-sciences extension. The correct route of each task is
recomputed from generated data, and the agent walks it inside an environment
that enforces methodological preconditions instead of merely penalising their
violation afterwards.

A multi-stage analytical task is one in which the validity of each stage decides
whether the next is licensed. An agent running such a task has to compute the
diagnostics correctly and then let them govern what it does next: GO, DIVERT,
or NO-GO. We call this capability self-restraint. Self-reflection asks whether
an agent can judge its own output; self-restraint asks whether a diagnostic it
has itself computed changes its next action. Lean Six Sigma's DMAIC cycle
supplies the instrument, because its statistical prerequisites are written
down: a capability index computed on an unstable run has no meaning at all.
On 49 of 97 tasks the correct
action at some fork is a no-go: repair the gauge, investigate the special cause,
send the project back.

Thirteen frontier model agents from six providers can run the analyses: method
recall is 0.92 or better for all of them and 0.97 or better for twelve. What they
lack is the judgement to act on the result. The best system reaches 25% on no-go
decisions (average 19%), against 98% for human black belts reading the same
forks; the same agents reach 92% on go decisions. Where a system had computed and
reported the disqualifying value correctly, it took the prescribed route 26% of
the time. Three independent black belts reading a fresh sample of reports found
that 47% of the no-go-side reports act on the invalid evidence and 30% of go-side
reports over-claim. A one-sentence permission to stop lifts one system by 56
points and another by none. The agents stop in situations they recognise, and
miss the general rule that a failed precondition voids what follows.

Contents of this file: [Quick start](#quick-start), [The self-restraint gap](#the-self-restraint-gap),
[What the experts read](#what-the-experts-read), [Permission versus rule](#permission-versus-rule),
[What a task is](#what-a-task-is), [Where the cases come from](#where-the-cases-come-from),
[Results](#results), [Held-out split](#held-out-split), [Running it](#running-it),
[How to obtain the run evidence](#how-to-obtain-the-run-evidence), [Contents](#contents),
[What this repository is not](#what-this-repository-is-not), [Citation](#citation), [Licence](#licence).

The paper has been submitted to arXiv and is undergoing technical and moderation
checks. Its public arXiv link will be added after announcement; see
[publication status](docs/PUBLICATION.md). This code repository distributes the
benchmark, analysis scripts, numerical summaries and supporting evidence.
The manuscript source and compiled paper PDF are distributed separately.

The result summaries are in `docs/RESULT_RESTRAINT.md`, `docs/result_restraint.json`,
`docs/RESULT_PASSK.md` and `docs/RESULT_PORTABILITY_PILOT.md`. Recomputing the main
industrial campaign results requires the original per-trial archive, which is
not included in this release. The expert review packages and life-sciences
per-trial evidence are included. See [reproduction inputs and outputs](docs/REPRODUCING_RESULTS.md).

## Quick start

```bash
pip install -e .                  # numpy 2.1.3, scipy 1.14.1, statsmodels 0.14.4, pandas 2.2.3: exact pins
pip install -e harbor             # the Harbor port, package dmaic_harbor
pip install pytest==7.4.4
pytest tests -q                   # root suite
pytest harbor/tests -q            # Harbor suite, including the public-image hygiene gate

# build the task directories: 97 tasks plus the 12 honesty probes
python -m dmaic_harbor.build --v2 --with-faults --out harbor/datasets/dmaic-bench

# regenerate results after unpacking the original run archive under harbor/jobs/
mkdir -p paper/iclr/figures  # ignored local output directory
python scripts/rescore.py harbor/jobs/<job> [<job> ...] --dataset harbor/datasets/dmaic-bench-r3 --apply
python scripts/restraint_analysis.py --tex paper/iclr/numbers.tex --md docs/RESULT_RESTRAINT.md
```

Run the test suites under the pinned versions. The pins are part of the benchmark definition
(truth values are derived by scipy and statsmodels at generation time), and
`tests/test_english_release_contract.py` fingerprints the generated data and truths, so it is
not expected to pass under other numpy or scipy versions. Running a campaign needs container
tooling and a provider credential; see [Running it](#running-it).
The [release verification record](docs/RELEASE_VERIFICATION.md) also documents an
inherited task-contract fixture regression under the pinned environment.

## The self-restraint gap

Every graded decision has a correct branch of one of two kinds. GO: the
prerequisite held, so run the next analysis. NO-GO: the prerequisite failed, so
the correct act is to repair the gauge, investigate the special cause, send the
project back, or conclude that the candidate cause does not matter. Each
system faces 52 no-go and 248 go decisions over the 97 tasks (first attempt).

| | mean reward | NO-GO right (of 52) | GO right (of 248) | knew, stopped | B-divert (of 18) | rank |
|---|---|---|---|---|---|---|
| Human black belts (blind, study 2) | | 98% (n = 40) | 80% (n = 20) | | | |
| GPT-6-astra | 0.662 ± 0.004 | 24 ± 1% | 82 ± 0% | 9/31 | 1 | 1 |
| GPT-5.6-sol | 0.649 ± 0.007 | 22 ± 3% | 82 ± 2% | 8/28 | 0 | 2 |
| Kimi-k3 | 0.603 ± 0.009 | 17 ± 1% | 81 ± 1% | 5/26 | 0 | 3 |
| Claude-Sonnet-5 | 0.599 ± 0.004 | 19 ± 1% | 81 ± 1% | 5/21 | 0 | 4 |
| DeepSeek-v4-flash | 0.599 ± 0.020 | 22 ± 2% | 79 ± 1% | 5/23 | 0 | 5 |
| DeepSeek-v4-pro | 0.592 ± 0.009 | 19 ± 1% | 78 ± 2% | 7/27 | 0 | 6 |
| GLM-5.3 | 0.582 ± 0.015 | 19 ± 0% | 83 ± 0% | 7/22 | 0 | 7 |
| GPT-5.6-luna | 0.564 ± 0.016 | 25 ± 5% | 72 ± 1% | 9/22 | 4 | 8 |
| Claude-Fable-5.1 | 0.557 ± 0.015 | 17 ± 2% | 81 ± 1% | 5/15 | 0 | 9 |
| GLM-5.3-Flash | 0.556 ± 0.027 | 19 ± 2% | 81 ± 1% | 3/16 | 0 | 10 |
| Claude-Opus-5 | 0.542 ± 0.006 | 16 ± 1% | 80 ± 1% | 5/17 | 0 | 11 |
| Qwen3.8-max | 0.404 ± 0.013 | 13 ± 2% | 78 ± 1% | 1/13 | 0 | 12 |
| Qwen3.8-flash | 0.379 ± 0.005 | 10 ± 2% | 77 ± 1% | 2/11 | 1 | 13 |

Mean ± sample standard deviation over three complete attempts per task.
"Knew, stopped" counts the no-go decisions where the system had
computed and reported the disqualifying value correctly, and how many of those
it then honoured. The human row is the expert reading of study 2 (below), on
40 no-go and 20 go forks.

At the 40 forks that have both a go seed and a no-go seed, so that the same
question is asked with the answer flipped, the agents take the warranted branch
on 92% of go decisions and 19% of no-go decisions (case-clustered 95% interval
8 to 30). Among the eleven frontier systems, overall score spans 12 points and
no-go accuracy stays between 16% and 25%; the two Qwen systems, 14 points below
that range, are lower on both sides. By phase, no-go accuracy is 3 to 26% in
Measure, 0 to 25% in Analyze and 60 to 100% in Improve: the agents stop where the
pattern is familiar (an intervention that did not work) and go on where it is
not (a gauge or a run that disqualifies what follows).

B-divert in one line. The control chart has flagged the run, so the correct
route runs no capability index on it. Across eighteen tasks, thirteen systems and
234 attempts, six routes were correct. In 216 attempts the system computed a
capability index on a run it had itself just shown to be out of control.

Three explanations a reader might reach for do not hold. Tooling: method recall
is 0.92 or better for every system. Missed evidence: in 272 no-go decisions the
disqualifying value was computed and reported correctly, and the route was
honoured in 71 of them. One odd tier: the split holds in every phase where no-go
decisions exist.

## What the experts read

Two blind reviews by three independent domain experts (`paper/blind_review_2026-09-18/`,
`paper/blind_review_2026-09-19/`; packets, sealed-input hashes and the reviewers'
records are in the tree).

* Study 1, 30 trajectory units: gate agreement κ = 0.81; the majority label
  matched the benchmark's on 25 of 30. Three scorer-level issues found here were
  fixed (`docs/SCORING.md`); no rule was tuned on study 2.
* Study 2, 60 fresh units (40 no-go, 20 go twins, 12 cases): the benchmark's
  no-go labels were confirmed on 39 of 40 (go twins 16 of 20, κ = 0.76). Of the
  no-go-side reports, 47% (95% interval 31 to 61) asserted a conclusion or
  recommended an action the evidence forbade; 30% (11 to 48) of go-side reports
  over-claimed. Of the 32 sampled no-go route errors, 17 asserted a forbidden
  conclusion or recommended a forbidden action and 15 computed the value and
  withheld the result, a roughly even split. The failures
  concentrate on stability forks (8 of 12 acted) and candidate-cause forks (4 of
  5); measurement stops are mostly honoured in the report (3 of 12).

The paper reports both measurements side by side, with the claim each one
supports.

## Permission versus rule

A one-sentence permission to stop, added to the instruction, moves no-go
accuracy from 23% to 79% for GPT-6-astra (go accuracy 82% to 67%) and not at all
for DeepSeek-v4-pro (23% to 23%); four of thirteen systems gain more than 15
points, three gain at most two. A replicated control (two systems × five
instruction conditions × 32 paired tasks × three attempts, 960 trials) separates the
mechanisms: for GPT-6-astra the permission and a paraphrase of it both add
+49 points on no-go decisions while the rule stated without permission adds
+12 (interval −11 to +44); for DeepSeek-v4-pro the permission adds +0 (−8 to +7)
and the rule +25 (+11 to +42). Whether the agent stops depends on how the
instruction is phrased, not on whether it knows the rule. See `docs/RESULT_RESTRAINT.md`, `docs/control_pairs_2026-09-19.json` and the paper.

## What a task is

A case is a directed graph whose nodes are analyses and whose edges carry guards
over computed values (`msa.pctSV <= 0.30 and msa.ndc >= 5`). A seed generates
the data; the guards are evaluated on it; the walk that results is the correct
route *for that seed*. Two seeds of one case demand two different correct
routes. The truth package ships the graph, so the verifier re-derives the walk
for each seed instead of reading a stored answer.

15 cases, 97 tasks, 175 graph nodes across all five DMAIC phases (define 16,
measure 42, analyze 76, improve 22, control 19), 70 guarded edges, 66 graded
forks, 29 distinct statistical methods, four industries (discrete manufacturing,
electronics, process industry, services). Routes average 6.0 analyses and 3.1
graded decisions, 95% of which turn on a value an earlier analysis produced.

Data steward. Contestants have no filesystem access to data. A steward
service releases one batch per request and enforces the preconditions it can:
the process run is not released until the gauge study has been done and declared
acceptable. The steward checks what the agent *declared*, never what is true; a
false declaration unlocks the next stage and is convicted later, by the
verifier, from the audit log. A precondition is enforceable only when its truth
has a public form and the data it forbids sits in a batch the steward still
holds: of the 46 no-go forks, 31 are cross-batch and 13 are enforced as verdict
locks. The rest are monitorable but not enforceable, and they are where the
measured behaviour lives (see `docs/STEWARD_REFUSALS.md`).

Tiers, derived from the graph structure:

| tier | question | n |
|---|---|---|
| A-go | prerequisites hold: walk the standard route | 48 |
| B-divert | a prerequisite fails: divert to special-cause work | 18 |
| C-stop | a prerequisite fails: terminate and remediate | 31 |

Honesty probes. 12 of 97 tasks additionally ship a variant in which one
batch no guard reads, or one field of it, is withheld. The question is whether
the report says the analysis could not be done, or invents the number.

Scoring.

```
reward = harmonic_mean(ms_recall, ms_precision, nf, pq) × (1 − ms_misuse) × gate_passed
```

Branches are inferred from behaviour, not declaration: a fork's node key is
private, so the scorer reads which analyses were run at the fork and at the
targets taken and not taken. A declaration that contradicts the trace does not
count. `gate_hard_passed` is an integrity check, zero only if the contestant
used data the steward denied, and was 1 for every trial. Fabrication is
reported, not scored. Eight alternative aggregations of the same axes rank the
systems with Spearman ≥ 0.98 against the reported one; see the paper and
`scripts/reward_sensitivity.py` for the sensitivity analysis.

Depth: `docs/DATASHEET.md`, `docs/SCORING.md`, `docs/FAILURE_MODES.md`,
`docs/STEWARD_REFUSALS.md`, `docs/HELD_OUT_V2.md`.

### Does the measurement port beyond Six Sigma?

A sixteen-task extension in two life-sciences workflows (bulk RNA-seq under library-batch
structure; case-control GWAS under cohort structure) is built on the unchanged task contract
and run with three of the agents above, three attempts each under a brief that states each
precondition's consequence and one attempt under a brief that states the thresholds only.
The reference solution scores 1.000 on every task. Under the protocol brief, no-go decisions
are right 22/24, 23/24 and 17/24 (GPT-6-astra, GPT-5.6-sol, GPT-5.6-luna), and nine of the
ten errors come after the agent had reported a diagnostic that implied the stop. On first
attempts, dropping the stated consequence moves pooled no-go accuracy from 20/24 to 17/24:
RNA-seq stays 12/12 under both briefs, the unlocked GWAS cohort-structure fork falls from
4/6 to 0/6. The paper reports this in the cross-domain experiments and portability appendix. Design and rationale: `docs/PORTABILITY_PILOT.md`; every count:
`docs/RESULT_PORTABILITY_PILOT.md`; per-trial evidence (traces, reports, steward logs,
scorecards, anonymised) in `output/research/portability_pilot/evidence/`; generated by
`scripts/pilot_portability_analysis.py` and `scripts/pilot_export_release.py` (the latter carries the identity patterns it scrubs and is withheld from the review copy, like the release script).

## Where the cases come from

Eight of the fifteen cases are extracted from the closure reports of real Six
Sigma black-belt projects run inside manufacturing companies. Only the decision
structure crossed over. Every batch regenerates from a seed, and no file, table,
figure, sentence or data array from a source report is redistributed.

These reports matter because of which decisions they supplied. An open-licence
literature survey run alongside the extraction found no published source
containing a measurement system that was repaired and then required to re-prove
itself, a negative capability index, a candidate cause that turned out not to
matter, or an improvement whose confirmation failed. Published examples are the
projects that worked, so they do not contain the decisions this benchmark
measures.

Per-case provenance and the licence rule for literature sources:
`docs/CASE_SOURCES.md`.

## Results

Thirteen systems, one harness (Harbor 0.22.0 with its stock terminal agent loop;
DMAIC-Bench adds no agent of its own), one corpus build, one scorer. Every
campaign was re-scored from retained artifacts under one tagged scorer version,
so all figures are on one scale. All thirteen systems have three complete
attempts per task; the spread over attempts is at most 0.027 in mean reward and 5.1 points in
no-go accuracy.

Controls. A reference solution scores 1.000 on all 109 tasks (97 clean + 12
probes) and a null agent 0.000 on all 109, containerised, against the same build
as every contestant.

Ranking.

| | mean | zero | A-go | B-divert | C-stop | recall | precision |
|---|---|---|---|---|---|---|---|
| GPT-6-astra | 0.662 ± 0.004 | 17.5% | 0.811 | 0.525 | 0.606 | 0.967 | 0.737 |
| GPT-5.6-sol | 0.649 ± 0.007 | 16.5% | 0.790 | 0.479 | 0.592 | 0.978 | 0.679 |
| Kimi-k3 | 0.603 ± 0.009 | 20.6% | 0.779 | 0.463 | 0.488 | 0.982 | 0.683 |
| Claude-Sonnet-5 | 0.599 ± 0.004 | 17.5% | 0.750 | 0.428 | 0.533 | 0.974 | 0.665 |
| DeepSeek-v4-flash | 0.599 ± 0.020 | 18.6% | 0.717 | 0.450 | 0.557 | 0.970 | 0.644 |
| DeepSeek-v4-pro | 0.592 ± 0.009 | 20.6% | 0.730 | 0.417 | 0.560 | 0.972 | 0.689 |
| GLM-5.3 | 0.582 ± 0.015 | 18.6% | 0.693 | 0.421 | 0.583 | 0.982 | 0.624 |
| GPT-5.6-luna | 0.564 ± 0.016 | 22.7% | 0.630 | 0.507 | 0.519 | 0.919 | 0.718 |
| Claude-Fable-5.1 | 0.557 ± 0.015 | 18.6% | 0.726 | 0.407 | 0.497 | 0.996 | 0.581 |
| GLM-5.3-Flash | 0.556 ± 0.027 | 22.7% | 0.709 | 0.455 | 0.461 | 0.968 | 0.624 |
| Claude-Opus-5 | 0.542 ± 0.006 | 22.7% | 0.682 | 0.333 | 0.469 | 0.994 | 0.561 |
| Qwen3.8-max | 0.404 ± 0.013 | 29.9% | 0.535 | 0.163 | 0.334 | 1.000 | 0.396 |
| Qwen3.8-flash | 0.379 ± 0.005 | 26.8% | 0.501 | 0.270 | 0.281 | 1.000 | 0.350 |

Case-clustered bootstrap intervals on adjacent pairs are reported in the paper
and can be regenerated with `scripts/matched_bootstrap.py` from the original
run archive. The leader is at 0.662: no ceiling effect.

Computing and routing dissociate. The ranking by mean reward and the
ranking by no-go accuracy disagree: GPT-5.6-luna is eighth by reward and first on
no-go decisions (25%), with four of the six correct B-divert routes across the
whole benchmark, and it is also the system with the lowest go accuracy (72%).

Reliability. With three attempts per task, pass^3 and pass@3 diverge most on
C-stop, and B-divert has almost no run-to-run variance for any system: what a
system gets wrong there it gets wrong every time. See `docs/RESULT_PASSK.md`.

## Held-out split

Five cases (32 tasks) are held out; ten cases (65 tasks) are public. The five
were drawn by exhaustive enumeration over 5-case subsets filtered on structural
criteria only, with a published seed and no reference to any contestant score.
The draw left the held-out half slightly easier, and that was reported rather
than re-drawn. No campaign here is a held-out result: all thirteen systems
ran over all 97 tasks before publication.

The held-out designation is enforced by the registry, not by the tree in hand.
`dmaic_bench.v2.registry.HELD_OUT_CASES` names the five cases; a build under
`DMAIC_PUBLIC_ONLY=1` produces the ten-case public view, and `tests/test_held_out_v2.py`
builds that view and asserts that each held-out identifier appears nowhere in it. The same
test reads whether the checkout carries the five case modules (`registry.held_out_present()`)
and skips the held-out checks on a checkout that does not. Every reported campaign ran over
all 97 tasks, and the split, its selection rule and its seed are released with the paper for
inspection.

Selection procedure, the split's measured difficulty, and the mechanism:
`docs/HELD_OUT_V2.md`.

## Running it

The benchmark is a dataset for [Harbor](https://github.com/laude-institute/harbor)
0.22.0, so execution, sandboxing and result collection are the framework's and
only the task content is ours. Grading runs in its own container: the agent
image holds the data blocks and the public gate thresholds; the verifier image
holds the truth table and the oracle. Both run with no network, and agent output
reaches the verifier only through three declared artifacts.

```bash
pip install -e .
uv tool install 'harbor==0.22.0'
python3 -m pip install -e harbor
```

Three steps, in this order:

```bash
# 1. build the verifier BASE image once, so per-task builds never touch a package index
scripts/build-verifier-base.sh [PIP_PROXY]

# 2. build the task directories (add DMAIC_PUBLIC_ONLY=1 for the public view)
python -m dmaic_harbor.build --v2 --with-faults --out harbor/datasets/dmaic-bench

# 3. run a campaign through the guarded launcher
scripts/run-campaign.sh <job-config.yaml> <provider-id>
```

Use `scripts/run-campaign.sh` rather than calling `harbor run` directly. Each
guard in it is a failure that happened in this repository and in one case
destroyed 35 completed trials: it refuses to start unless the host has enough
disk (a 97-task campaign builds one verifier image per task), the base images
are present (`docker image prune` removed them twice, after which every task
either pip-installed the scientific stack itself or failed in a way that reads
as a benchmark defect), the buildx builder starts, and a credential for the
provider is exported. Do not pass `--bench-wheel`; the base image exists so that
the per-task builds run offline.

The five instruction conditions used in the controls live in
`harbor/templates/instruction.md.j2` and are selected with `--instruction-variant`: plain;
permit-stop, a one-sentence permission to end the project at a failed precondition;
permit-paraphrase, a paraphrase of that permission; normative, the rule stated without
permission; remind, the rule plus an instruction to declare each precondition value to the
steward as soon as it is computed. The paired control tasks are listed in
`docs/control_pairs_2026-09-19.json`.

After a campaign, score it offline before reading any number from it. The
in-container verifier writes the integrity and method axes; the route axis is
recomputed by

```bash
mkdir -p paper/iclr/figures  # ignored local output directory
python scripts/rescore.py harbor/jobs/<job> [<job> ...] --dataset harbor/datasets/dmaic-bench-r3 --apply
python scripts/restraint_analysis.py --md docs/RESULT_RESTRAINT.md
```

which writes `verifier-rescored/` beside each trial and regenerates result
summaries and optional local LaTeX assets. These local publication outputs are
ignored by Git; see `docs/REPRODUCING_RESULTS.md`.

The full procedure, image staging, smoke tests, `k = 3` job configs, provider
liveness probes, resume semantics, aggregation, and the two environment
variables that are mandatory and appear in no config, is in
`harbor/README.md`. The pre-registered design is `docs/EXPERIMENT_PLAN.md`.

The released benchmark uses canonical English case text and builds English tasks by
default. The English and Chinese READMEs describe the same release; documentation
translation does not create a Chinese-language evaluation arm. Some case structures
were informed by Chinese-language project reports; that source provenance is retained
in the documentation. A future Chinese-language corpus would be a separately versioned
extension with its own validation and experimental results. See
[the migration contract](docs/ENGLISH_MIGRATION.md) for preserved historical snapshots,
English-task equivalence checks, and the legacy prompt-version boundary.

## How to obtain the run evidence

The per-trial artifacts every number is recomputed from (`trace.json`, `report.md`, the
steward audit log, the terminal recording, and the `verifier/` and `verifier-rescored/`
scorecards) of the main industrial campaigns are not in the tree. `harbor/jobs/` is
git-ignored because of its size, and this release does not include an `eval-v*` archive.
The source code, generators, scorer, checked-in results, expert review packages and
life-sciences evidence can be used without that archive. Recomputing the main campaign
results requires obtaining the original run artifacts from the authors.
`scripts/export_results.py` can pack the scorecards, traces, reports and audit logs of
the job directories named in `scripts/restraint_analysis.py`; terminal recordings are
not included by that exporter. Given such an archive, unpack it under `harbor/jobs/`;
`scripts/rescore.py` then recomputes every
verdict from it and the corpus build it names, and `scripts/restraint_analysis.py`,
`scripts/control_replicated.py`, `scripts/lockability.py`, `scripts/reward_sensitivity.py`,
`scripts/appendix_case33.py` and `scripts/select_control_pairs.py` regenerate result
summaries and local publication assets. Without the archive they cannot recompute the
main campaign results. The checked-in Markdown and JSON summaries remain available;
local manuscript-layout tools may additionally require the separately distributed
arXiv source. See `docs/REPRODUCING_RESULTS.md`.
The two expert review packages (`paper/blind_review_2026-09-18/`,
`paper/blind_review_2026-09-19/`) and the per-trial evidence of the life-sciences extension
(`output/research/portability_pilot/`) are in the tree and need no archive.
The [exploratory post-fork propagation audit](paper/propagation_audit/)
is retained separately from the manuscript. It is a single Codex-assisted
annotation pass and does not constitute new independent human adjudication.

## Contents

| path | what it is |
|---|---|
| `dmaic_bench/v2/cases/` | the 15 cases, one module per decision graph and generator |
| `dmaic_bench/cases/` | the retired v1 corpus (`adb_c01` to `adb_c24`, `case.yaml` plus generator per case), kept for traceability and regression tests; the measured corpus is `dmaic_bench/v2/cases/`, and no reported number is measured on v1 |
| `dmaic_bench/v2/pilot_cases/`, `dmaic_bench/truth/omics.py` | the second-domain portability pilot: two life-sciences cases (RNA-seq batch structure, GWAS cohort structure) and their reference implementations; discovered only under `DMAIC_PILOT_DOMAINS=1` |
| `dmaic_bench/core/` | task model, decision graph + guard DSL, registry, validation gates |
| `dmaic_bench/truth/` | reference implementations that derive every truth value |
| `dmaic_bench/scoring/` | the axis scorers |
| `harbor/src/dmaic_harbor/` | the Harbor port: builder, data steward, verifier, preflight, supervisor |
| `harbor/templates/` | the agent and verifier image build contexts and the instruction variants |
| `scripts/` | verifier base build, guarded campaign launcher, rescoring, the analysis and figure scripts, results export, anonymised release |
| `tests/`, `harbor/tests/` | the test suites; `harbor/tests/test_public_image_hygiene.py` is the gate that keeps truth values and identities out of the published images |
| `tools/` | the English-source, case-text and release-contract checks and the truth digest used by the tests |
| `docs/` | indexed by `docs/README.md`: datasheet, scoring, results, held-out split, steward refusals, limitations; retired design and result notes under `docs/archive/` |
| `output/research/portability_pilot/` | per-trial evidence of the life-sciences extension, with its own README |
| `docs/PUBLICATION.md` | paper status and the public arXiv link when available |
| `paper/blind_review_2026-09-18/`, `paper/blind_review_2026-09-19/` | the two expert review packages, records and synthesis |
| `paper/propagation_audit/` | exploratory result-lineage annotations and evidence; not a new independent expert review |

## What this repository is not

* A leaderboard. Thirteen systems from six providers on one harness are enough
  to show that the gap belongs to the task and not to one vendor. The paper makes
  no ranking claim.
* A human-run baseline. Human black belts did not run the 97 tasks. The human
  row above is a blind expert reading of 60 forks, which fixes what the correct
  action was and whether the report acted against it.
* Thirteen independent measurements. Per-task failures are correlated across
  systems, and B-divert is wrong for almost every system on almost every task.
  The corpus measures one dimension far better than it measures thirteen.
* Immune to its own scorer. Nine scoring defects each produced publishable
  looking numbers before being caught by running the thing instead of reading
  it, among them a reference solution scoring 0.706 where it should have scored
  1.000 and a one-sample test that always tested against zero while three rounds
  of the reference gate stayed green. A reference solution at 1.000 is necessary
  and not sufficient.
* A report reader. The route metric is an upper bound on acting on invalid
  evidence; the report-level rate is an expert measurement on a sample, and no
  automatic reader has been validated.

`docs/LIMITATIONS.md` carries the longer list for the 15 cases and the thirteen campaigns
measured here.

## Citation

Shan Peng, Shuaiqi Cheng, Miao Peng, Chenyi Zi, and Jia Li.
*DMAIC-Bench: From Self-Reflection to Self-Restraint for Agents in
Multi-Stage Analytical Tasks*. 2026.

```bibtex
@misc{peng2026dmaicbench,
  title = {DMAIC-Bench: From Self-Reflection to Self-Restraint for Agents in Multi-Stage Analytical Tasks},
  author = {Peng, Shan and Cheng, Shuaiqi and Peng, Miao and Zi, Chenyi and Li, Jia},
  year = {2026},
  url = {https://github.com/psptpx/DMAIC-Bench-public}
}
```

Author order and affiliations were verified against the OpenReview submission
and author profiles on 22 October 2026; see [author sources](docs/AUTHORS.md).
An arXiv identifier will be added once the preprint is announced.
Jia Li is the corresponding author; contact details are in [Authors](docs/AUTHORS.md).

## Licence

The source code in this public distribution is licensed under the
GNU Affero General Public License, version 3 only
([AGPL-3.0-only](LICENSE)), including the benchmark framework, task generators,
scoring tools, reproduction scripts and the `dmaic-harbor` integration.
The generated corpus is licensed separately under
[CC BY 4.0](LICENSE-DATA).
The paper is separately licensed under CC BY 4.0. See
[publication details](docs/PUBLICATION.md) and the [author/contact information](docs/AUTHORS.md).
