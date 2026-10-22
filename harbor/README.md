# DMAIC-Bench on Harbor

DMAIC-Bench packaged as a [Harbor](https://hub.harborframework.com) dataset
(framework version **0.22.0**). Each task hands an agent a real manufacturing-quality
problem and a **data steward** that releases project data one stage at a time, subject
to methodology gates. The agent must walk Define → Measure → Analyze → Improve →
Control, choose its own methods, request the data each method needs, and write a
report. A **separate verifier container** — holding the truth table and the oracle,
which the agent can never reach — scores what it actually did.

What makes this different from a coding benchmark: the measured capability is
*choosing the method*, so the instruction never names one; and the steward can refuse,
so the benchmark can ask whether a system reports a refusal honestly or fills the hole
with a number it did not compute.

---

## Layout

```
harbor/
├── pyproject.toml                     installable package `dmaic-harbor`
├── job.example.yaml                   the reproducibility job (k=3, two contestants)
├── src/dmaic_harbor/
│   ├── spec.py                        THE SHARED CONTRACT — read this first
│   ├── build.py                       bench TaskInstance -> Harbor task directory
│   ├── steward_service.py             the in-container data steward (loopback HTTP)
│   ├── steward_cli.py                 `steward` — the agent's only channel to data
│   ├── verify.py                      runs in the verifier container, writes reward.json
│   │                                  ---- orchestrator-host only; in neither image ----
│   ├── preflight.py                   refuse to start a campaign the host cannot finish
│   ├── probe.py                       per-model reachable / auth-ok / has-balance
│   ├── supervisor.py                  launch, resume on a non-clean exit, abort at 20% errors
│   └── aggregate.py                   model × metric table; excludes unscored trials
├── scripts/
│   ├── launch-campaign.sh             THE campaign entry point — runs every gate in order
│   ├── preflight.sh                   the host preflight, standalone
│   └── e2e.sh                         one task end to end, without the framework runtime
├── templates/
│   ├── environment/Dockerfile         the AGENT image  (data + public thresholds)
│   ├── environment/entrypoint.sh
│   ├── verifier/Dockerfile            the VERIFIER image (truth + oracle)
│   ├── verifier/test.sh               /tests/test.sh, baked into the verifier image
│   ├── instruction.md.j2        # authoritative English task instructions
├── datasets/dmaic-bench/          (not in this repository; `harbor add --scan`
│   └── dataset.toml                   writes the manifest here — see "Publish")
├── reference/                         a stock `harbor task init` scaffold, for diffing
├── tests/                             pytest; the hygiene gate lives here
└── private/                           operator-only, not part of this repository.
                                       See "Private contestants".
```

`spec.py` is authoritative for every path, key and threshold below. It was derived from
Harbor's own pydantic models, not from prose docs; when this README and `spec.py`
disagree, `spec.py` is right and this README is a bug.

---

## The truth-isolation guarantee

This is the reason the port exists, and it is worth understanding before running
anything.

| | **Agent container** | **Verifier container** |
|---|---|---|
| holds | data blocks, public gate thresholds | the truth table, the oracle |
| network | `no-network` | `no-network` |
| sees the other's contents | never | only through 3 collected artifacts |

Harbor's `environment_mode = "separate"` runs verification in its own container. The
agent's output reaches it **only** through `[[artifacts]]` — `trace.json`,
`report.md`, and the steward's `audit.jsonl`, uploaded to `/logs/artifacts`. Nothing
else crosses.

The subtle part is the **steward**, which must enforce prerequisite locks *inside the
agent container* without knowing any truth. It can, because the gate predicates are
public: "%GRR ≤ 30" is in the AIAG MSA manual and in the task instruction itself. The
steward checks **what the agent declared**, never what is true. So a system that
declares a passing gage study it did not perform unlocks the next stage — and is
convicted of it later, by the verifier, from the audit log. Enforcement and grading
stay on opposite sides of the wall.

Two consequences worth stating plainly:

- In separate mode Harbor passes `skip_tests_upload=True`, so **the verifier image
  must already own `/tests/test.sh`**. It is not copied in at run time.
- `reward.json` is parsed as `dict[str, float | int]` — a **flat map of scalars**.
  Anything structured goes to `scorecard.json` beside it, which is collected with the
  rest of `/logs/verifier`.

---

## Install

```bash
uv tool install harbor            # the framework, 0.22.0
python3 -m pip install -e harbor
```

`dmaic-harbor` installs two console scripts:

| script | what it is |
|---|---|
| `dmaic-harbor-build` | generates Harbor task directories from bench cases |
| `steward` | the in-container data-steward CLI (`spec.STEWARD_CLI`) |

The agent image installs `steward` at `/usr/local/bin/steward` itself; the console
script is the equivalent entry point for a host-side or pip-installed steward.

---

## 1. Build the tasks

```bash
dmaic-harbor-build --out harbor/datasets/dmaic-bench
# or: python3 -m dmaic_harbor.build --out harbor/datasets/dmaic-bench
```

One directory per `(case × tier × seed × variant [× fault])` instance, in Harbor's
`TaskPaths` layout, named by `spec.harbor_task_name()`. The generated directories are
**build output**, not source — `.gitignore` keeps them out of git, and they are
reproducible from the builder plus a seed.

Useful flags: `--seeds 1,2,3`, `--variants clean,dirty`, `--tiers T1,T2,T3`,
`--cases adb_c23,adb_c18`, `--limit N`.

The builder enforces three invariants at build time, and aborts rather than emit a
leaky task: no truth in the agent container, **no method name anywhere in the rendered
`instruction.md`** (re-checked against every `method_id` and alias in the taxonomy),
and no answer in `solution/` — `solve.sh` derives every number by asking the steward
for data exactly as an agent would.

## 2. Build the two images

The images are built from **staged contexts**, not from the repository root. The agent
image's context is one task's `environment/` directory plus the steward code; the
verifier image's context is the verifier code, the bench package, and that task's
truth file.

```bash
# --- agent image (data + public thresholds) ---
TASK=harbor/datasets/dmaic-bench/dmaic-<task-id>
CTX=$(mktemp -d)
cp harbor/templates/environment/Dockerfile   "$CTX/"
cp harbor/templates/environment/entrypoint.sh "$CTX/"
mkdir -p "$CTX/dmaic_harbor"
cp harbor/src/dmaic_harbor/{spec.py,steward_service.py,steward_cli.py} \
   "$CTX/dmaic_harbor/"
cp -R "$TASK/environment/task" "$CTX/task"
docker build -t dmaic/agent:0.2.0 "$CTX"

# --- verifier image (truth + oracle) ---
VCTX=$(mktemp -d)
cp harbor/templates/verifier/{Dockerfile,test.sh} "$VCTX/"
cp harbor/src/dmaic_harbor/{verify.py,spec.py} "$VCTX/"
cp -R dmaic_bench "$VCTX/dmaic_bench"
cp "$TASK/truth.json" "$VCTX/truth.json"
docker build -t ghcr.io/dmaic-bench/verifier:0.2.0 "$VCTX"
```

**Read this before changing a build command.** `.dockerignore` lives at
`harbor/.dockerignore`, and Docker only reads a `.dockerignore` at the *context
root*. It therefore protects builds whose context **is** `harbor/` — and a staged
context is protected instead by what you copy into it. The rule is the same either
way: **stage explicitly, never `docker build harbor` with a Dockerfile that
copies the whole context**, and never `cp -R harbor "$CTX"`. The hygiene test
checks the `.dockerignore` half mechanically; the staging half is on you, which is why
the commands above copy named files.

### Build the base image ONCE, and do not use `--bench-wheel`

`scripts/build-verifier-base.sh [PIP_PROXY]` builds
`ghcr.io/dmaic-bench/verifier:0.2.0-base`, which `dmaic-harbor-build` then uses as
`ARG BASE_IMAGE` for every per-task verifier. The 156 per-task builds are `COPY` layers
plus a `pip install` of pins that are already satisfied, so **they need no network**.

Passing `--bench-wheel` instead forces the standalone path, where each of the 156 verifier
images pip-installs the whole scientific stack itself. That was the cause of two consecutive
G3 runs losing all 312 trials, and neither failure was a benchmark defect:

* every buildx builder on this host uses the `docker-container` driver, which keeps its own
  image store and **cannot see the local one**. So even an already-present base image is
  resolved over the registry, and one `registry-1.docker.io` EOF killed all 156 builds.
* the host routes egress through a local proxy the build container does not inherit, so
  `pip install` gets `ECONNREFUSED` while the host reaches PyPI fine.

Hence also the run flag: **`DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0`**, so compose uses
the daemon's own builder, which resolves the local base image.

```bash
scripts/build-verifier-base.sh http://host.containers.internal:10808   # proxy optional
python -m dmaic_harbor.build --v2 --with-faults --out harbor/datasets/dmaic-bench
DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0 harbor run -c <job>.yaml
```

## 3. Run it

```bash
# one task, one attempt, for a smoke test
harbor run -p harbor/datasets/dmaic-bench/dmaic-<task-id> \
           --agent claude-code --model anthropic/claude-sonnet-4-5

# the whole dataset, one attempt
harbor run -p harbor/datasets/dmaic-bench \
           --agent claude-code --model anthropic/claude-sonnet-4-5
```

A directory containing task directories is resolved as a **local dataset**: Harbor
iterates it and keeps every valid task subdirectory. `dataset.toml` and `README.md` are
files, so they are simply skipped.

### At k = 3

```bash
harbor run -c harbor/job.example.yaml
```

`job.example.yaml` is the file the paper's reproducibility statement points at. It is
executable, not illustrative — `tests/test_public_image_hygiene.py` validates it
against Harbor's real `JobConfig` on every test run. It sets `n_attempts: 3` (Harbor
reports pass@k from that), runs two contestants over the same task set, collects
exactly the three contract artifacts, and doubles the timeouts because a DMAIC walk is
long-horizon.

Filter without editing the dataset:

```yaml
datasets:
  - path: harbor/datasets/dmaic-bench
    task_names: ["dmaic-*-t3-*"]
    exclude_task_names: ["*-fault"]
    n_tasks: 10
```

Results land in `harbor/jobs/<job_name>/`; `harbor view` browses the
trajectories.

## 4. Publish the dataset

`dataset.toml` is generated with `tasks = []` on purpose, and is gitignored as build
output: a `[[tasks]]` entry must pin an exact `sha256` content digest, which does not
exist until the task directory does.

**This sequence has been executed end to end against the framework CLI**, on a corpus
built by `dmaic-harbor-build`, up to but not including the network call:

```bash
dmaic-harbor-build --out harbor/datasets/dmaic-bench   # writes tasks + `tasks = []`
cd harbor/datasets/dmaic-bench
harbor add . --scan --to .   # one [[tasks]] entry per task dir, WITH its digest
harbor publish .             # syncs digests itself, then publishes tasks, then dataset
```

Three corrections to what an earlier version of this section claimed. Each was verified,
not reasoned about:

- **`harbor add --scan --to .` does not work.** `packages` is a required positional
  argument, so that command exits 2 with `Missing argument 'packages'.` and leaves the
  manifest untouched. The dot is the argument; `--to` already defaults to `.`.
- **`harbor sync` cannot populate an empty manifest.** It iterates entries that already
  exist and recomputes their digests. Against `tasks = []` it exits 0 and prints
  `Updated 0 digest(s)` — so the two-command sequence above, even with the syntax fixed,
  produced an empty manifest. **The digest comes from `add`, not from `sync`.** `sync`
  earns its keep only when a task directory changes *after* being added; it correctly
  detects that and rewrites the digest.
- **`harbor publish` runs `sync` itself** as its first act, so the separate `sync` step
  buys nothing before a publish.

Two ways this fails silently, both worth knowing before a release:

- **Dropping `--scan` exits 0 and does nothing.** With a `dataset.toml` present, the
  directory resolves as a *dataset* rather than as a directory of tasks, so `add`
  resolves the manifest to itself, prints `No tasks or files to add.`, and succeeds. A
  green exit code is not evidence that the manifest has anything in it — check.
- **`--scan` reads immediate subdirectories only**, requires a `task.toml` in each, and
  warns-and-skips a bad one rather than failing.

One more thing to settle before a first publish: the dataset is named `dmaic/dmaic-bench`
while every task is named `dmaic-bench/dmaic-…`, so the two live under *different*
registry organisations and the publishing account needs both. `--public` also promotes
only task packages owned by the dataset's own organisation, which — given that split —
is not the organisation that owns the tasks. Default visibility is `private`, and
`--public` prompts interactively, so an unattended publish stays private.

Verify before publishing:

```bash
grep -c '^\[\[tasks\]\]' dataset.toml    # must equal the number of task directories
```

`harbor publish` pushes to `hub.harborframework.com` and requires authentication
(`harbor auth login`, or `HARBOR_API_KEY` in the environment); without it it aborts with
`Not authenticated`. Afterwards anyone can run it by name:

```bash
harbor run -d dmaic/dmaic-bench@0.1.0 --agent claude-code
```

Two other resolution paths exist and are worth knowing:

| form | resolves via |
|---|---|
| `-d org/name[@ref]` | the package registry (the Hub) |
| `-d bare-name --registry-path registry.json` | a JSON registry file (`harbor.models.registry:Registry`) listing datasets by local path or git URL |
| `-p <dir>` | a local directory of task directories — no manifest involved |

The populated manifest is **build output and is gitignored** — it would be stale the
moment the corpus regenerated. To pin a released revision, publish it: the Hub holds the
digests, and `-d dmaic/dmaic-bench@0.1.0` is the pin. The working tree stays reproducible
from the builder plus a seed, which is the property that matters here.

---

## 5. Run a campaign

A benchmark run of a few thousand trials is an operations problem before it is a science
problem. The last three campaigns lost trials to the host rather than to the models —
364 of 1 056 in the largest, or 34.5% — so the launch path is gated rather than
optimistic. One command runs every gate in order:

```bash
harbor/scripts/launch-campaign.sh -c harbor/job.example.yaml -p harbor/jobs/dmaic-bench-k3
```

| step | what it refuses to proceed past | standalone |
|---|---|---|
| 1. credentials | a missing credential file, or one not mode 600/400 | `scripts/campaign-env.sh` |
| 2. host preflight | no runtime, no builder, unpullable base image, no disk | `harbor/scripts/preflight.sh` |
| 3. provider liveness | a model that is unreachable, unauthenticated or unfundable | `dmaic-harbor-probe` |
| 4. supervised run | nothing — it launches, and **resumes** rather than restarts | `dmaic-harbor-supervise` |

Add `--dry-run` to run steps 1–3 and stop. Steps 2 and 3 take seconds; the failures they
catch cost hours and the budget of everything that ran before someone noticed.

### The two variables that are mandatory and were never declared

```bash
export DOCKER_HOST="unix://$(podman machine inspect --format '{{.ConnectionInfo.PodmanSocket.Path}}')"
export BUILDX_BUILDER=proxied
```

Without the first, the runtime client falls back to a daemon socket that does not exist
on a VM-backed engine. Without the second, BuildKit selects the `default` builder, whose
endpoint is that same absent socket and which does not inherit this shell's proxy
settings — base-image pulls then fail with `403 Forbidden` or `failed to resolve source
metadata … EOF`, which reads as a network outage and is not one. In both cases **every**
trial dies in environment build, before the model is asked anything, and is then recorded
as a trial result. The preflight fails on either, and prints the export that fixes it.

### Provider liveness

Balance exhaustion was the single largest cause of lost trials. The probe sends one
`max_tokens=1` request per configured model and reports **reachable / auth-ok /
has-balance** separately, because those are three different failures with three different
fixes:

```bash
dmaic-harbor-probe            # exit 0 fundable, 1 not, 3 degraded, 2 no config
dmaic-harbor-probe --dry-run  # print the plan; contact nothing
```

Targets come from a JSON file kept beside the credential file, **outside this repository**
(`$DMAIC_PROVIDERS_FILE`, else `providers.json` next to `$DMAIC_ENV_FILE`). It names
environment *variables*, never values, and no provider, endpoint or model name is
hardcoded in the package:

```json
{"providers": [{"id": "gateway-a", "wire": "openai",
                "base_url_env": "SOME_API_BASE", "api_key_env": "SOME_API_KEY",
                "models": ["model-one", "model-two"]}]}
```

`wire` is `openai` or `anthropic` and selects the request shape only — it names a
protocol, not a vendor. A credential travels in a header, never in a URL, a body or a
process argument, and every provider-supplied string is redacted against the live
credential values before it can reach a message: gateways do echo the offending key back
inside their error text, and error text is exactly what this tool prints.

### Resume, don't restart

Three of five jobs in the last campaign took `SIGTERM` and nothing restarted them, while
`harbor job resume -p <dir>` already existed. The supervisor closes that:

```bash
dmaic-harbor-supervise -c <job-config.yaml> -p <jobs-dir>/<job-name>
```

- It issues `harbor run` **exactly once**, when the job directory does not yet exist.
  Every later attempt is a resume, so completed trials are never re-spent — and that
  holds when the supervisor itself is the thing that was killed.
- A clean exit that left the job unfinished is resumed too. A swallowed cancellation
  exits 0, and treating that as proof of completion is how a half-finished job gets
  published as a finished one.
- Its attempt budget is persisted in the job directory, so restarting the supervisor
  does not reset the count on a crash-looping job.
- **Hard abort at a 20% harness-error rate** (`--abort-error-rate`, floor
  `--min-trials-for-abort`). A campaign burning budget against a broken harness should
  end. A *harness* error is a trial that produced no verdict — no `reward.json`, a
  `scorecard.json` carrying the verifier's crash marker, or a trial-level exception. A
  model that genuinely scored 0.0 is not one, so the abort does not fire on a hard task
  set.

### Aggregate

```bash
dmaic-harbor-aggregate <jobs-dir> --out results.json --md summary.md
```

Two things it will not do. **It will not publish a verifier crash as a score of zero.**
The crash path writes `reward.json` with every axis at zero *and* marks `scorecard.json`
with an `error` key; reading only `reward.json` makes those indistinguishable. Such
trials are excluded from every mean, counted by kind, and shown in the table. A trial
that produced no verdict is a missing observation, and averaging it in would bias exactly
the contestants that hit infrastructure problems most often — which is not a uniform set.

**It will not invent a price.** `cost_usd` was null for 9 of 11 contestants because no
price map covers gateway-served model names, while token counts are recorded for all of
them. So tokens are the primary cost figure; USD appears only where a price was actually
returned, marked `(floor)` where partial and `unpriced` where absent.

---

## Honest note on the reward

**The headline `reward` scalar is the competence term, not the paper's Trust-Gated
Score.** This is a deliberate departure from the published aggregate, and it is not a
simplification.

```
reward = harmonic_mean(ms_recall, nf, pq)
```

— method-selection recall, numeric fidelity, and procedural quality. TGS is still
computed and still emitted, as `tgs_legacy`, alongside a flag `honesty_axis_valid = 0`.

TGS multiplies competence by `(1 - fabrication_rate)`, and on this repository's own
scorer that estimator is **not honesty-monotone**:

- A perfect trace whose report states **no numbers at all** scores TGS **1.000**. There
  is nothing to catch, so nothing is caught.
- An honest disclosure that quotes its own p-values is charged **0.185 of headline
  score** for doing so — the swing from adding supported numbers around an unsupported
  one exceeds every between-system difference in the paper's main table. (Measured on
  the authors' composition experiment, whose result files are not part of this
  repository.)

An estimator that rewards saying less, and penalises showing your work, cannot be the
multiplier on a trustworthiness score. Publishing TGS as a Harbor `reward` would export
that defect to every downstream consumer of this dataset — leaderboards, RL reward
signals, other people's papers — where it would be far harder to withdraw than it is
to not ship. So the scalar is the competence term, and the honesty axis ships marked
invalid until it earns otherwise.

Restore TGS as `reward` only once the estimator passes monotonicity and degenerate-case
probes. (Those probes live in the authors' paper workspace and are not part of this
repository; the property they must establish is stated above.) Until then, read
`tgs_legacy` as *continuity with the published numbers*, not as a measurement.

The full per-axis breakdown — `ms_recall`, `ms_precision`, `ms_misuse`, `nf`, `pq`,
`hn_fabrication_rate`, `hn_misreport_rate`, `ae_turns`, `ae_interventions` — is in
`reward.json` (flat scalars) and `scorecard.json` (structured), per `spec.REWARD_KEYS`.

---

## Private contestants

One contestant in the published comparison is not part of this release. It depends on
proprietary software and infrastructure that cannot be redistributed, so a reader can
neither install it nor reproduce a run of it. It is not in the dataset, not in either
image, and not in `job.example.yaml`.

Its Harbor adapter lives in the operator-only `harbor/private/` directory, which is
excluded from every Docker build context, left out of the wheel and sdist, and guarded
by `tests/test_public_image_hygiene.py`. That directory is not part of this repository,
so the operator instructions that accompany it (endpoint configuration, the local job
config, the `PYTHONPATH` it needs) are not published either. The hygiene suite still
asserts the exclusion policy, and reports the directory as missing rather than passing
vacuously.

A private contestant runs **outside** the task container, on infrastructure the operator
already owns, driven over the network from the orchestrator host, the same way
`claude-code` reaches `api.anthropic.com`. It still fetches every data block *through the
in-container steward*, so locks, refusals and provision metering apply to it exactly as
to any other contestant, and it never sees the truth table. A number measured this way is
reported as operator-hosted and is not presented as reproducible from this release.

---

## Tests

```bash
python3 -m pytest harbor/tests/ -q
```

`tests/test_public_image_hygiene.py` is the acceptance gate for the isolation policy.
It fails when a leak becomes *possible*, not merely when one happens:

- no public file that can reach an image names the private contestant (scanned as **bytes**,
  so a binary or DLP-wrapped file cannot slip past a decode error);
- `.dockerignore` genuinely removes `private/**` — the Docker matcher is **simulated**
  here (`filepath.Match` plus `**` and `!`), because writing a pattern is not evidence
  that it matches;
- no `COPY`/`ADD` in `templates/` can resolve into `private/` or outside its context;
- the manifest, every `task.toml`, and every generated task directory are clean;
- the dataset names no contestant, and `job.example.yaml` lists none;
- the packaging config is an allowlist that cannot pick up `private/`;
- the private adapter hardcodes no endpoint and no credential.

Two carve-outs exist, both narrow, both documented in the test file itself: a `#`
comment in a Dockerfile may state the policy (Docker never puts the Dockerfile into
the image), and a whole-context `COPY .` is permitted **only while the simulated
context filter independently proves `private/**` is excluded** — delete those
`.dockerignore` rules and that test fails too. Everything else is a hard failure.

The suite is mutation-tested: introducing the forbidden string into shipping source,
into an undecodable file, into the manifest, into the job config, or into the sdist
allowlist — or deleting the `private/` rules from `.dockerignore` — each turns it red.

## Running a campaign: the two environment facts that are not in any config

Both were found by a live run, not by a test, and both fail in a way that reads as a model
result rather than a setup problem.

**1. The container runtime and the builder.** `harbor/scripts/preflight.sh` checks these and
prints the fix for each; run it before anything. On a rootless podman host:

```
export DOCKER_HOST="unix://$(podman machine inspect --format '{{.ConnectionInfo.PodmanSocket.Path}}')"
export BUILDX_BUILDER=proxied      # a named docker-container builder; see preflight's message
```

The `docker-container` builder has **its own image store** and cannot see images in the local
daemon. A verifier that layers on a private base image therefore fails with `403 Forbidden` from
the registry even when that image is present locally — the 403 is the builder resolving `FROM`,
not a credential problem. Build with `--bench-wheel` instead, which layers the verifier on the
public python base:

```
python3 -m build --wheel
python3 -m dmaic_harbor.build --v2 --out <dir> \
        --bench-wheel dist/dmaic_bench-0.2.0-py3-none-any.whl
```

**2. The agent's credentials are not the credential file's variables.** `providers.json` tells
the PROBE how to reach each provider (`base_url_env`, `api_key_env`, wire). It tells the agent
nothing: the agent is litellm and reads `ANTHROPIC_API_KEY` / `ANTHROPIC_BASE_URL` or the OpenAI
pair, which is not where the credential file puts them — a GLM model served over the Anthropic
wire lives in `ZAI_KEY` and `ZAI_BASE`. Nothing bridged the two, so the probe could report
`zai/glm-5.3-flash ok` and the campaign then authenticate as whatever happened to be in
`ANTHROPIC_API_KEY`. `scripts/agent-env.sh` closes that gap:

```
source scripts/campaign-env.sh
source scripts/agent-env.sh zai          # exports the ANTHROPIC_* pair from ZAI_*
harbor run -c <job>.yaml
```

The provider id must match the `model_name` prefix in the job config: an `anthropic/…` model
reads the `ANTHROPIC_*` pair whatever provider actually serves it.

## Concurrency is capped by the provider, not by the host

Measured on this corpus with GLM-5.3-Flash over the z.ai gateway: **6 concurrent trials produced
zero rate-limit errors over hours; 14 produced six within two minutes** (`code 1302`). The host
was not the constraint — agent containers sit at ~0% CPU, because a trial is 20–30 model turns
against a growing context and is entirely latency-bound (median trial 50 minutes, max 72).

This matters more than throughput. A rate-limit error surfaces INSIDE the agent's trajectory as
`Unknown Error in LLM interaction`, so it is recorded as the model failing a step. Raising
concurrency past what the provider allows does not just slow a campaign down, it silently
converts an infrastructure limit into a model result — the same class of error the provider
probe exists to prevent, arriving after the probe has passed.

Find the ceiling on a handful of tasks before committing a corpus to it, and treat any
`RateLimitError` in a campaign log as invalidating the trials that saw it.

**A job cannot be resumed after its config changes.** `harbor job resume -p <dir>` reconciles the
persisted trial configs against the planned job config and raises `Existing trial config does not
match planned job config` — so raising concurrency mid-campaign is not a resume, it is a restart.
Finish the remainder as a second job over the outstanding task names; `dmaic_harbor.campaign_report`
takes several job directories and de-duplicates per (task, agent).
