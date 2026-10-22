# Canonical Harbor task, for comparison

Generated verbatim by Harbor 0.22.0 itself:

```
harbor task init dmaic/reference --description "layout reference"
```

Keep it here as the ground truth our generated tasks are diffed against — it is what the
framework produces, not what the docs describe.

## What it tells us

- `schema_version = "1.4"`; `[task]`, `[metadata]`, `[verifier]`, `[verifier.env]`,
  `[agent]`, `[environment]`, `[environment.env]`, `[solution.env]`, and a top-level
  `artifacts = []` are all present in a default task.
- Default `[environment].network_mode = "public"`. **Ours must set `no-network`.**
- The default `tests/test.sh` writes `reward.txt` and pulls `uv` over the network at verify
  time. **Ours cannot**: our verifier runs `no-network`, so every dependency must already be
  in the verifier image, and we emit `reward.json` (flat scalars) rather than `reward.txt`.
- The default task uses the SHARED verifier (no `[verifier].environment_mode`), which would
  run the test script in the agent's own container. **Ours must be `separate`** — otherwise
  the truth table and the oracle would be reachable from the agent's container, which
  destroys the benchmark.

## Harbor CLI worth knowing

| command | use |
|---|---|
| `harbor task init <org>/<name>` | scaffold a task |
| `harbor check` | check task quality against a rubric |
| `harbor task start-env -p <dir>` | boot a task's environment for manual poking |
| `harbor add` / `harbor remove` / `harbor sync` | manage `dataset.toml` and task digests |
| `harbor run -c job.yaml` | run a job (alias of `harbor job start`) |
| `harbor exec` | compile paths into tasks and run a job |
| `harbor publish` | publish to the Harbor registry |

## Harbor's own task-quality rubric — our acceptance checklist

`harbor check <path>` grades a task against `harbor/cli/quality_checker/default-rubric.toml`
using an LLM reviewer (defaults: `--agent claude-code --model claude-sonnet-4-6`, so it costs
API budget — run it once before publishing, not in CI).

The eleven criteria, and where we stand:

| criterion | what it wants | us |
|---|---|---|
| `behavior_in_task_description` | everything the tests check is described in `instruction.md` | must hold — the trace/report contract is stated normatively |
| `behavior_in_tests` | everything the instruction describes is tested | must hold |
| `informative_test_structure` | test script has clear sections naming what each checks | verifier `test.sh` |
| `anti_cheating_measures` | no shortcuts; **"copying ground-truth files into image" is an explicit FAIL** | **this is exactly why the verifier is `separate`** |
| `structured_data_schema` | exact schema documented, not just exemplified | `trace.json` schema stated in `instruction.md` |
| `pinned_dependencies` | every Python dep pinned (apt need not be) | both images |
| `typos` | filenames, paths, variable names | check path constants against `spec.py` |
| `tests_or_solution_in_image` | image must not copy `tests/` or `solution/` | ⚠ **deliberate deviation, see below** |
| `test_deps_in_image` | test-only deps installed by `test.sh`, not baked in | ⚠ **deliberate deviation, see below** |
| `hardcoded_solution` | `solve.sh` must *derive* the answer, not `echo` it | oracle re-runs the analyses; no truth file ships in `solution/` |
| `file_reference_mentioned` | files the agent must produce are named in `instruction.md` | `/workspace/trace.json`, `/workspace/report.md` |

### The two deliberate deviations

The rubric is written for Harbor's *default shared* verifier. We require
`environment_mode = "separate"`, and two criteria then become unsatisfiable:

- `tests_or_solution_in_image` — Harbor itself passes `skip_tests_upload=True` for a separate
  verifier (`harbor/trial/trial.py::_run_separate_verifier`), so our verifier image **must**
  own `/tests/test.sh`. Forced by the framework.
- `test_deps_in_image` — our verifier runs `no-network`, so nothing can be installed at verify
  time. (Harbor's own scaffolded `test.sh` curls `uv` from the network; we cannot.)

Both are the price of the isolation guarantee. Shared mode would put the truth table and the
oracle inside the agent's own container — which `anti_cheating_measures` itself calls a FAIL.
We take two documented deviations to avoid one real one.
