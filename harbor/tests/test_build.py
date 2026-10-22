"""Acceptance tests for the task materialiser.

Four properties matter more than the rest, and each has a test that would actually catch a
regression rather than restate the implementation:

1. every ``task.toml`` validates against **Harbor's own** ``TaskConfig`` (not a local copy);
2. the layout satisfies Harbor's ``TaskPaths``, and the agent's build context can reach
   neither ``solution/`` nor ``tests/``;
3. no truth value reaches ``environment/`` — the agent container's whole security premise;
4. ``instruction.md`` names no statistical method — choosing one is the measured capability.
"""
from __future__ import annotations

import json
import os
import sys
import tomllib
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
BENCH_ROOT = HERE.parents[1]
for _p in (str(BENCH_ROOT), str(HERE.parent / "src")):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _add_harbor_to_path() -> None:
    """Make the Harbor framework importable, working around a name collision.

    Harbor 0.22.0 is installed as a `uv tool`, in its own virtualenv, and this repository's
    own package directory is also called ``harbor`` — so with ``bench/`` on sys.path the
    plain name resolves to *our* directory as an empty namespace package and the framework
    models are unreachable. Locating the tool venv from the CLI shim on PATH and putting its
    site-packages FIRST lets the real regular package win the lookup. Tests that need the
    framework skip rather than fail if it genuinely is not installed.
    """
    import shutil
    shim = shutil.which("harbor")
    if not shim:
        return
    venv = Path(shim).resolve().parent.parent
    for site in venv.glob("lib/python*/site-packages"):
        if (site / "harbor" / "models" / "task" / "config.py").exists():
            sys.path.insert(0, str(site))
            sys.modules.pop("harbor", None)
            return


_add_harbor_to_path()

from dmaic_harbor import build as B          # noqa: E402
from dmaic_harbor import spec                # noqa: E402
from dmaic_harbor import steward_service     # noqa: E402

harbor_config = pytest.importorskip("harbor.models.task.config",
                                    reason="Harbor 0.22.0 is not importable here")
harbor_paths = pytest.importorskip("harbor.models.task.paths")
harbor_task = pytest.importorskip("harbor.models.task.task")
TaskConfig = harbor_config.TaskConfig
TaskPaths = harbor_paths.TaskPaths
Task = harbor_task.Task


# --------------------------------------------------------------------------- fixtures

#: A slice broad enough to exercise every code path that varies: a T1 single-stage probe, a
#: T2 phase slice, a T3 full journey, a dirty variant, and the official English language.
#:
#: Split in two because nine expert-derived cases are held out of the public release
#: (docs/HELD_OUT.md). The public half is what a public checkout can build and is on its own
#: sufficient for every property asserted below; the held-out half is ADDED when the checkout
#: has it, so a developer tree keeps exactly the coverage it had. Membership is resolved
#: against the registry rather than assumed, so neither half can silently name a case that has
#: gone away.
_PUBLIC_SAMPLE = (
    "adb_c23",   # T1 single-stage probe
    "adb_c02",   # T1, a decision point and an order constraint
    "adb_c24",   # the only public T3 case: 10 stages, 5 decision points, 21 truths
)
#: Coverage no public case supplies: adb_c15 is the ONLY case in the corpus that declares a
#: prerequisite lock, and adb_c07/adb_c20 are further T3 journeys. All three are held out.
_HELD_OUT_SAMPLE = ("adb_c15", "adb_c07", "adb_c20")


def _sample_cases() -> tuple:
    available = set(B._case_index())
    missing = [c for c in _PUBLIC_SAMPLE if c not in available]
    assert not missing, f"public sample case(s) missing from the registry: {missing}"
    return _PUBLIC_SAMPLE + tuple(c for c in _HELD_OUT_SAMPLE if c in available)


SAMPLE_CASES = _sample_cases()


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    """The PUBLIC corpus -- what actually ships.

    A developer tree carries the de-identification map, and the case bridge re-applies internal
    organisation names unless told otherwise, so a default build is refused by the identity
    gate. Every property these tests assert (no method leak, no truth in the agent context, a
    valid task.toml) is a property of the published artifact, so the published mode is the one
    to exercise.
    """
    out = tmp_path_factory.mktemp("hb")
    previous = os.environ.get(B.PUBLIC_IDENTITY_ENV)
    os.environ[B.PUBLIC_IDENTITY_ENV] = "1"
    try:
        dirs = B.build(out=out, seeds=(1,), variants=("clean", "dirty"),
                       tiers=("T1", "T2", "T3"), cases=SAMPLE_CASES, with_faults=True)
    finally:
        if previous is None:
            os.environ.pop(B.PUBLIC_IDENTITY_ENV, None)
        else:
            os.environ[B.PUBLIC_IDENTITY_ENV] = previous
    assert dirs, "the sample slice produced no tasks"
    return dirs


@pytest.fixture(scope="module")
def tasks():
    cases = {k: v for k, v in B._case_index().items() if k in SAMPLE_CASES}
    return {t.task_id: t for t in B.build_all(cases, seeds=(1,),
                                              variants=("clean", "dirty"),
                                              tiers=("T1", "T2", "T3"), with_faults=True)}


def _task_of(task_dir: Path, tasks: dict):
    cfg = tomllib.loads((task_dir / "task.toml").read_text(encoding="utf-8"))
    return tasks[cfg["metadata"]["task_id"]]


# --------------------------------------------------------------------------- 1. task.toml

def test_task_toml_validates_against_harbor(built):
    for d in built:
        cfg = TaskConfig(**tomllib.loads((d / "task.toml").read_text(encoding="utf-8")))
        assert cfg.schema_version == spec.HARBOR_SCHEMA_VERSION


def test_task_toml_carries_the_isolation_settings(built):
    for d in built:
        cfg = TaskConfig(**tomllib.loads((d / "task.toml").read_text(encoding="utf-8")))
        assert cfg.environment.network_mode.value == "no-network"
        assert cfg.environment.workdir == spec.WORKSPACE
        assert cfg.verifier.environment_mode.value == "separate", (
            "a shared verifier would put the truth table in the agent's own container")
        assert cfg.verifier.environment is not None
        assert cfg.verifier.environment.network_mode.value == "no-network"
        # docker_image must stay unset: harbor.environments.definition
        # .should_use_prebuilt_docker_image() short-circuits the build when it is set, and
        # the build of tests/ is the only thing that bakes this task's truth in.
        assert cfg.verifier.environment.docker_image is None


def test_task_toml_declares_every_collected_artifact(built):
    want = {(src, dest) for src, dest in spec.COLLECTED_ARTIFACTS}
    for d in built:
        cfg = TaskConfig(**tomllib.loads((d / "task.toml").read_text(encoding="utf-8")))
        got = {(a.source, a.destination) for a in cfg.artifacts}
        assert got == want


def test_agent_timeout_scales_with_tier_and_turns(built):
    seen = {}
    for d in built:
        cfg = TaskConfig(**tomllib.loads((d / "task.toml").read_text(encoding="utf-8")))
        seen.setdefault(cfg.metadata["tier"], set()).add(cfg.agent.timeout_sec)
    assert max(seen["T1"]) < min(seen["T3"]), "a T1 probe must not get a T3 budget"


# --------------------------------------------------------------------------- 2. layout

def test_layout_matches_harbor_task_paths(built):
    for d in built:
        p = TaskPaths(d)
        assert p.instruction_path.is_file()
        assert p.config_path.is_file()
        assert p.environment_dir.is_dir()
        assert p.solution_dir.is_dir()
        assert p.tests_dir.is_dir()
        assert p.discovered_solve_path is not None

        # There is deliberately NO tests/test.sh. Harbor requires one only for a SHARED
        # verifier: `Task._validate_tests` resolves the effective verifier environment first
        # and returns early when one exists, which is exactly our case
        # (`environment_mode = "separate"` with a `[verifier.environment]` block). In separate
        # mode Harbor passes `skip_tests_upload=True` and the verifier IMAGE owns
        # /tests/test.sh, so a copy on the host would be dead weight that could drift from the
        # one actually executed. The script lives at tests/stage/test.sh, where the verifier
        # Dockerfile COPYs it from.
        assert p.discovered_test_path is None
        assert (d / "tests" / "stage" / "test.sh").is_file()
        # Harbor's own verdict is what counts:
        assert Task.is_valid_dir(d), f"Harbor rejects {d.name}"


def test_agent_build_context_cannot_reach_solution_or_tests(built):
    """environment/ IS the Docker build context, so what is not in it cannot enter the image.

    Harbor's rubric fails a task whose image copies tests/ or solution/
    (``tests_or_solution_in_image``); the structural guarantee is that they are siblings of
    the context, and that nothing inside it references them.
    """
    for d in built:
        names = {p.name for p in (d / "environment").rglob("*") if p.is_file()}
        assert "solve.sh" not in names and "truth.json" not in names
        assert "plan.json" not in names
        # and no build instruction reaches outside the context for them. (Prose may still
        # *mention* /solution — spec.py documents the whole layout — so only COPY/ADD count.)
        dockerfile = (d / "environment" / "Dockerfile").read_text(encoding="utf-8")
        for line in dockerfile.splitlines():
            head = line.strip().upper()
            if head.startswith("COPY") or head.startswith("ADD"):
                assert "solution" not in line and "tests" not in line
                assert "truth" not in line


def test_staged_sources_are_plain_utf8(built):
    """Endpoint DLP encrypts *.py at rest; a wrapped file reaches the container as NULs."""
    for d in built:
        for f in list((d / "environment").rglob("*.py")) + list((d / "tests").rglob("*.py")):
            data = f.read_bytes()
            assert b"\x00" not in data, f"{f} looks like ciphertext, not source"
            compile(data.decode("utf-8"), str(f), "exec")


def test_verifier_context_carries_truth_and_test_script(built):
    for d in built:
        assert (d / "tests" / "Dockerfile").is_file()
        assert (d / "tests" / "stage" / "test.sh").is_file()
        truth = json.loads((d / "tests" / "stage" / "truth.json").read_text(encoding="utf-8"))
        assert truth["schema"] == "dmaic-truth/v1"
        assert truth["task_id"]


# --------------------------------------------------------------------------- 3. no truth

def _numbers(node, out):
    if isinstance(node, bool):
        return
    if isinstance(node, (int, float)):
        out.append(float(node))
    elif isinstance(node, dict):
        for v in node.values():
            _numbers(v, out)
    elif isinstance(node, (list, tuple)):
        for v in node:
            _numbers(v, out)
    elif isinstance(node, str):
        try:
            out.append(float(node))
        except ValueError:
            pass


def _distinctive(value: float) -> bool:
    """Is this truth value one whose appearance in the payload would actually prove a leak?

    Degenerate truths — 0, 1, a small count like 4 — collide with raw data by arithmetic, not
    by leakage (``pValue = 0.0`` next to a data column that happens to contain a zero). Only
    values that carry information are evidence, so the test judges those and says so, rather
    than passing vacuously on a threshold nobody wrote down.
    """
    return abs(value - round(value)) > 1e-9 or abs(value) >= 1000


def test_no_truth_value_reaches_the_agent_container(built, tasks):
    checked = 0
    for d in built:
        task = _task_of(d, tasks)
        payload = []
        for name in ("blocks.json", "steward.json"):
            _numbers(json.loads((d / "environment" / "task" / name).read_text("utf-8")),
                     payload)
        present = set(payload)
        for entry in task.truths:
            if not _distinctive(entry.expected):
                continue
            checked += 1
            assert not any(abs(x - entry.expected) <= 1e-9 for x in present), (
                f"{task.task_id}: truth {entry.method_id}.{entry.field}="
                f"{entry.expected} appears in the agent payload")
    assert checked > 20, "the sample carried too few distinctive truths to prove anything"


def test_no_truth_shaped_key_reaches_the_agent_container(built):
    """Structural companion to the value test: the payload has no truth-carrying section."""
    forbidden = {"truths", "expected", "correct_branch", "acceptable_branches",
                 "branch_evidence", "decision_points", "order_constraints", "derivation"}
    for d in built:
        for name in ("blocks.json", "steward.json"):
            text = (d / "environment" / "task" / name).read_text("utf-8")
            blob = json.loads(text)
            stack = [blob]
            while stack:
                node = stack.pop()
                if isinstance(node, dict):
                    assert not (set(node) & forbidden), f"{d.name}/{name}: {set(node) & forbidden}"
                    stack.extend(node.values())
                elif isinstance(node, list):
                    stack.extend(node)


def test_honesty_probe_hides_the_method(built, tasks):
    """The probe withholds a batch; naming its method in the agent's own image defeats it."""
    seen_probe = False
    for d in built:
        cfg = json.loads((d / "environment" / "task" / "steward.json").read_text("utf-8"))
        fault = cfg.get("fault")
        if not fault:
            continue
        seen_probe = True
        assert "method_id" not in fault
        assert set(fault) == {"stage_id", "denial_message"}
        task = _task_of(d, tasks)
        assert task.fault.method_id not in json.dumps(cfg, ensure_ascii=False)
    assert seen_probe, "with_faults=True produced no honesty probe to check"


def test_solution_ships_no_computed_answer(built, tasks):
    """Harbor's ``hardcoded_solution`` criterion: the oracle derives, it does not recite."""
    for d in built:
        task = _task_of(d, tasks)
        plan = json.loads((d / "solution" / "plan.json").read_text("utf-8"))
        blob = json.dumps(plan, ensure_ascii=False)
        for entry in task.truths:
            if _distinctive(entry.expected):
                assert repr(entry.expected) not in blob
        numbers = []
        _numbers(plan, numbers)
        for entry in task.truths:
            if _distinctive(entry.expected):
                assert not any(abs(x - entry.expected) <= 1e-9 for x in numbers)


# --------------------------------------------------------------------------- 4. no method

def test_instruction_names_no_statistical_method(built):
    """No method name outside the vocabulary block.

    The instruction now carries the full 49-method menu, which is identical on every task and
    therefore discloses nothing about this one -- see
    `test_instruction_supplies_the_full_method_vocabulary` for why withholding it made
    MS-Recall measure naming luck. What must still never appear is a per-stage shortlist.

    This calls the real gate rather than re-implementing the scan: a hand-rolled copy would
    drift from the code that actually runs at build time, and this test exists precisely to
    catch that code failing.
    """
    for d in built:
        text = (d / "instruction.md").read_text("utf-8")
        cfg = tomllib.loads((d / "task.toml").read_text("utf-8"))
        # the task identifier is structural (the trace must echo it) and is scanned
        # separately by B.identifier_leaks
        B.assert_no_method_leak(text, d.name, allow=(cfg["metadata"]["task_id"],))


def test_leak_gate_actually_fires():
    """A gate nobody has seen fail is not a gate."""
    with pytest.raises(B.MethodLeak):
        B.assert_no_method_leak("do a gage r&r first", "unit test")
    B.assert_no_method_leak("first understand the current batch", "unit test")


def test_instruction_states_the_output_contract(built):
    for d in built:
        text = (d / "instruction.md").read_text("utf-8")
        for token in (spec.TRACE_FILE, spec.REPORT_FILE, spec.STEWARD_BASE,
                      "method_id", "route_decisions", "outcome", "refusal", "stage_id",
                      B.AGENT_DATA_DIR, "locked", "denied", "unroutable", "exhausted"):
            assert token in text, f"{d.name}: instruction never mentions {token}"


def test_prior_facts_are_stripped_of_stage_labels(tasks):
    """T2 prior_facts is a list of stage labels, and labels name methods."""
    t2 = [t for t in tasks.values() if t.tier == "T2" and t.prior_facts]
    assert t2, "no T2 task in the sample carried prior facts"
    for task in t2:
        cleaned = B.sanitize_prior_facts(task)
        assert cleaned
        assert "Completed: " not in cleaned


# --------------------------------------------------------------------------- steward config

def test_steward_accepts_every_generated_config(built):
    for d in built:
        steward_service.load_config(d / "environment" / "task" / "steward.json")


def test_locks_and_forks_are_satisfiable(built):
    """A lock whose opener is only offered later is a task nobody can finish."""
    saw_requires = saw_gate = False
    for d in built:
        cfg = json.loads((d / "environment" / "task" / "steward.json").read_text("utf-8"))
        order = [s["stage_id"] for s in cfg["stages"]]
        for stage in cfg["stages"]:
            for req in stage.get("unlock", {}).get("requires", []):
                saw_requires = True
                assert order.index(req) < order.index(stage["stage_id"])
            for gate in stage.get("unlock", {}).get("gates", []):
                saw_gate = True
                assert gate in spec.PUBLIC_GATES
            fork = stage.get("fork_on")
            if fork:
                for targets in fork["branches"].values():
                    for t in targets:
                        assert order.index(t) > order.index(stage["stage_id"])
    # The GATE half of this test only has material in a developer tree: adb_c15 is the only
    # case in the corpus whose stages carry `unlock.gates`, and it is held out of the public
    # release (docs/HELD_OUT.md). The `requires` half is exercised in both, because it is
    # derived from every case's order constraints.
    assert saw_requires, (
        "the sample produced no prerequisite at all -- this test would have passed vacuously")
    if not saw_gate:
        assert not any(c in B._case_index() for c in _HELD_OUT_SAMPLE), (
            "a held-out case is present but contributed no gate; the gate derivation broke")


def test_gate_locks_agree_with_the_verifier_package(built, tasks):
    for d in built:
        task = _task_of(d, tasks)
        truth = json.loads((d / "tests" / "stage" / "truth.json").read_text("utf-8"))
        assert truth["gates"]["locks"] == B.gate_locks(task)


# --------------------------------------------------------------------------- CLI

def test_cli_writes_the_directories_it_prints(tmp_path, capsys, monkeypatch):
    # Exercise the published mode: a developer tree would otherwise be stopped by the identity
    # gate, which is the point of the gate.
    monkeypatch.setenv(B.PUBLIC_IDENTITY_ENV, "1")
    # A public case (docs/HELD_OUT.md) so this runs in a public checkout too; adb_c24 is the
    # only public case that produces T2 slices.
    rc = B.main(["--out", str(tmp_path), "--tiers", "T2", "--seeds", "1",
                 "--variants", "clean", "--cases", "adb_c24", "--limit", "2"])
    assert rc == spec.EXIT_OK
    printed = [Path(p) for p in capsys.readouterr().out.split() if p.strip()]
    assert printed and all(p.is_dir() for p in printed)


# --------------------------------------------------------------- identity gate

def test_build_refuses_an_internal_identity_corpus_by_default(tmp_path, monkeypatch):
    """The de-identification is reversible in a developer tree, so the gate must default shut.

    The case bridge re-applies internal organisation names whenever the developer-only
    identity map is present and DMAIC_BENCH_PUBLIC_IDENTITY is unset. A default build then
    wrote a real company name into 166 of 377 `instruction.md` files -- each of which is copied
    verbatim into the agent image as TASK.md. Measured, not hypothesised. So `--internal` turns
    the guard OFF rather than on: a gate whose safe state is the default is the only kind that
    survives someone in a hurry.
    """
    monkeypatch.delenv(B.PUBLIC_IDENTITY_ENV, raising=False)
    internal, why = B.identity_mode()
    if not internal:
        pytest.skip(f"no identity map in this tree ({why}) -- nothing to gate")

    with pytest.raises(B.IdentityLeak) as exc:
        B.build(out=tmp_path / "refused", seeds=(1,), variants=("clean",), tiers=("T1",),
                limit=1)
    message = str(exc.value)
    assert B.PUBLIC_IDENTITY_ENV in message, "the refusal must say how to build a public corpus"
    assert "--internal" in message
    assert not (tmp_path / "refused").exists(), "it must refuse before writing anything"


def test_public_identity_mode_builds_and_names_no_organisation(tmp_path, monkeypatch):
    monkeypatch.setenv(B.PUBLIC_IDENTITY_ENV, "1")
    internal, _ = B.identity_mode()
    assert not internal

    dirs = B.build(out=tmp_path / "public", seeds=(1,), variants=("clean",), tiers=("T3",),
                   limit=3)
    assert dirs

    # Read the mapping rather than hard-coding names: the list of what must not appear does not
    # belong in a file that ships publicly.
    #
    # That same reasoning is why the map itself is not in the public release, so a public
    # checkout has nothing to compare against. The half of this test that matters there has
    # already run above -- public-identity mode builds -- and the comparison half is skipped
    # with a reason rather than silently passing on an empty set of forbidden names.
    identity_map = B.BENCH_ROOT / "dmaic_bench" / "cases" / B.IDENTITY_MAP
    if not identity_map.exists():
        pytest.skip("identity map absent (public release) -- see docs/HELD_OUT.md; "
                    "the build half of this test ran and passed")
    raw = json.loads(identity_map.read_text(encoding="utf-8"))
    secrets = set()

    def _walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, str) and k in ("title", "internal_title", "former_case_id",
                                                "legacy_source_id", "source"):
                    if len(v.strip()) >= 3:
                        secrets.add(v.strip())
                else:
                    _walk(v)
        elif isinstance(node, list):
            for v in node:
                _walk(v)

    _walk(raw)
    assert secrets, "the identity map yielded nothing to check against"

    offenders = []
    for d in dirs:
        for f in d.rglob("*"):
            if not f.is_file():
                continue
            blob = f.read_bytes()
            for secret in secrets:
                if secret.encode("utf-8") in blob:
                    offenders.append(f"{f.relative_to(d)}: {secret}")
    assert not offenders, offenders[:5]


def test_instruction_supplies_the_full_method_vocabulary(built):
    """The trace contract demands a canonical `method_id`; the instruction must say which ones.

    Measured on a live campaign before this was fixed: a model computed all seven required
    analyses of a T2 task correctly and scored MS-Recall 0.000, because it wrote
    `msa.agreement` for `msa.attribute_agreement` and `pareto.prioritization` for
    `quality.pareto`. Seven for seven semantically, zero for seven by string match. Asking an
    agent to hit a 49-value enum it has never been shown measures naming luck, and every
    contestant fails it identically -- which looks like a capability result and is not one.

    The whole menu is safe to publish: it is the same 49 rows on every task, so it says nothing
    about this one. The per-stage shortlist is the thing that would, and
    `test_instruction_names_no_statistical_method` still guards that.
    """
    expected = set(B.method_terms())
    canonical = {t for t in expected if "." in t and " " not in t}
    assert len(canonical) >= 45, "taxonomy shrank unexpectedly; update this test deliberately"

    for d in built:
        text = (d / "instruction.md").read_text(encoding="utf-8")
        assert B.vocab_heading("en") in text, f"{d.name}: no vocabulary block"
        missing = sorted(m for m in canonical if f"`{m}`" not in text)
        assert not missing, f"{d.name}: vocabulary omits {missing[:5]}"


def test_the_vocabulary_block_does_not_make_the_leak_gate_vacuous():
    """Stripping the block before scanning must not stop the gate catching a real leak."""
    vocab = B.method_vocabulary()

    B.assert_no_method_leak(f"prose\n\n{vocab}\n\nmore prose\n", "clean")  # must not raise

    with pytest.raises(B.MethodLeak):
        B.assert_no_method_leak(f"run anova.oneway first\n\n{vocab}\n\nmore\n", "id leak")

    with pytest.raises(B.MethodLeak):
        B.assert_no_method_leak(f"do a Gage R&R study\n\n{vocab}\n\nmore\n", "alias leak")
