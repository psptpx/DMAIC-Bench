"""The acceptance gate for the contestant-isolation policy.

DMAIC-Bench publishes two images and a dataset. One private contestant must never
appear in any of them: it depends on proprietary software and infrastructure that
cannot be redistributed, so a reader could not run it. Its adapter lives under
``harbor/private/``, which is operator-only and not part of this repository.

Policy alone does not hold. This module is what holds it, and it is written to fail
LOUDLY the moment a leak becomes *possible* -- not merely when one occurs.

Design notes
------------
* The forbidden strings come from ``policy.PUBLIC_IMAGE_FORBIDDEN``. The test never
  hardcodes its own copy, so widening the policy widens the test.
* The whitelist is not a list of forgiven files. A public file may name the policy
  only if it is the policy declaration itself (``policy.py``) or if the simulated
  ``.dockerignore`` filter proves it never reaches an image. Adding a file to the
  whitelist without also excluding it from the build context therefore still fails.
* The ``.dockerignore`` filter is simulated here rather than trusted: Docker's
  matcher is Go ``filepath.Match`` plus ``**`` and ``!``, and "I wrote the pattern"
  is not evidence that the pattern matches.
"""
from __future__ import annotations

import glob
import os
import re
import shutil
import sys
import tomllib
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- paths
HARBOR_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = HARBOR_ROOT / "src"
PRIVATE_DIR = HARBOR_ROOT / "private"
TEMPLATES_DIR = HARBOR_ROOT / "templates"
DATASETS_DIR = HARBOR_ROOT / "datasets"
DATASET_DIR = DATASETS_DIR / "dmaic-bench"
DATASET_MANIFEST = DATASET_DIR / "dataset.toml"
JOB_EXAMPLE = HARBOR_ROOT / "job.example.yaml"
DOCKERIGNORE = HARBOR_ROOT / ".dockerignore"
PYPROJECT = HARBOR_ROOT / "pyproject.toml"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from dmaic_harbor import policy, spec  # noqa: E402


# --------------------------------------------------------------------------- harbor
def _harbor_site_packages() -> str | None:
    """Locate Harbor's site-packages when it is not on the default import path.

    Harbor 0.22.0 is installed as a uv tool, so ``python3 -m pytest`` does not see
    it. Rather than skip the model-validation tests (which are acceptance criteria),
    find the interpreter-independent install and put it on the path.
    """
    candidates = sorted(
        glob.glob(
            os.path.expanduser("~/.local/share/uv/tools/harbor/lib/python3.*/site-packages")
        )
    )
    executable = shutil.which("harbor")
    if executable:
        # .../uv/tools/harbor/bin/harbor -> .../uv/tools/harbor/lib/python3.X/site-packages
        tool_root = Path(executable).resolve().parent.parent
        candidates += sorted(glob.glob(str(tool_root / "lib" / "python3.*" / "site-packages")))
    for candidate in candidates:
        if Path(candidate, "harbor").is_dir():
            return candidate
    return None


def _import_harbor_models():
    """Import Harbor's real models, defeating two ways the import can go wrong.

    1. Harbor 0.22.0 is installed as a uv tool, so ``python3 -m pytest`` does not see
       it on the default path.
    2. This repository has a top-level directory literally named ``harbor``. Whenever
       pytest puts the repository root on ``sys.path`` (it does, as soon as the whole
       test directory is collected), ``import harbor`` resolves to that directory as an
       implicit namespace package and every submodule import fails. Skipping on that
       would silently drop two acceptance criteria, so shadowing is repaired rather
       than tolerated.
    """

    def _try_import():
        from harbor.models.dataset.manifest import DatasetManifest
        from harbor.models.job.config import JobConfig

        return DatasetManifest, JobConfig

    shadow = sys.modules.get("harbor")
    if shadow is not None and not getattr(shadow, "__file__", None):
        # A namespace package -- i.e. our own top-level harbor/ directory. Evict it.
        for name in [n for n in sys.modules if n == "harbor" or n.startswith("harbor.")]:
            del sys.modules[name]

    try:
        return _try_import()
    except (ModuleNotFoundError, ImportError):
        pass

    found = _harbor_site_packages()
    if found is None:
        pytest.skip(
            "Harbor 0.22.0 is not importable and no uv tool install was found; "
            "cannot validate against its real pydantic models. "
            "Install with: uv tool install harbor"
        )
    # Prepend, so the real package wins over the shadowing directory.
    if found in sys.path:
        sys.path.remove(found)
    sys.path.insert(0, found)
    for name in [n for n in sys.modules if n == "harbor" or n.startswith("harbor.")]:
        del sys.modules[name]
    return _try_import()


# --------------------------------------------------------------------------- dockerignore
_SKIP_DIR_NAMES = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"}


def _pattern_to_regex(pattern: str) -> re.Pattern[str]:
    """Translate one .dockerignore pattern into an anchored regex.

    Docker matches with Go's ``filepath.Match`` extended by ``**``:
    ``**`` spans separators, ``*`` and ``?`` do not, and every pattern is anchored
    at the build-context root.
    """
    out: list[str] = ["^"]
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char == "*":
            if pattern[i : i + 2] == "**":
                # '**/' may also match zero path segments ('**/x' matches 'x').
                if pattern[i : i + 3] == "**/":
                    out.append("(?:.*/)?")
                    i += 3
                    continue
                out.append(".*")
                i += 2
                continue
            out.append("[^/]*")
            i += 1
        elif char == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(char))
            i += 1
    out.append("$")
    return re.compile("".join(out))


def _parse_dockerignore(text: str) -> list[tuple[re.Pattern[str], bool]]:
    """Return (regex, is_exception) in file order; the LAST match wins, as in Docker."""
    rules: list[tuple[re.Pattern[str], bool]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        exception = line.startswith("!")
        if exception:
            line = line[1:].strip()
        line = line.rstrip("/")
        if not line:
            continue
        rules.append((_pattern_to_regex(line), exception))
    return rules


def _is_excluded(rel_posix: str, rules: list[tuple[re.Pattern[str], bool]]) -> bool:
    """True when Docker would drop this path from the build context.

    A path is excluded if it matches, or if any ancestor directory matches -- Docker
    prunes whole subtrees. Later rules override earlier ones so ``!`` can re-include.
    """
    parts = rel_posix.split("/")
    subjects = ["/".join(parts[: n + 1]) for n in range(len(parts))]
    verdict = False
    for regex, exception in rules:
        if any(regex.match(subject) for subject in subjects):
            verdict = not exception
    return verdict


def _iter_repo_files() -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(HARBOR_ROOT):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIR_NAMES]
        for filename in filenames:
            if filename == ".DS_Store":
                continue
            files.append(Path(dirpath) / filename)
    return sorted(files)


def _rel(path: Path) -> str:
    return path.relative_to(HARBOR_ROOT).as_posix()


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def _forbidden_hits(path: Path) -> list[str]:
    """Forbidden tokens present in a file, scanned as BYTES.

    Deliberately not text-based. An earlier text-only version of this scan returned
    ``None`` for anything that failed to decode as UTF-8 and skipped the file -- so a
    binary blob, a DLP-wrapped source file, or a stray archive could carry the whole
    excluded stack straight past the gate. A byte scan cannot be dodged that way, and
    it costs nothing.
    """
    try:
        data = path.read_bytes()
    except OSError:
        return []
    if _is_dockerfile(path):
        # See _strip_dockerfile_comments: comment lines are the one carve-out.
        data = _strip_dockerfile_comments(
            data.decode("utf-8", "replace")
        ).encode("utf-8", "replace")
    return sorted(
        {token for token in policy.PUBLIC_IMAGE_FORBIDDEN if token.encode() in data}
    )


DOCKERIGNORE_RULES = _parse_dockerignore(DOCKERIGNORE.read_text(encoding="utf-8"))

#: The ONLY file allowed to name the policy: the declaration, whose whole job is to state
#: it. A policy that cannot be written down cannot be audited.
#:
#: This used to be ``spec.py``, and that was the leak. ``spec.py`` is the shared runtime
#: contract and build.py stages it into BOTH images as ``spec.py.txt``, so the declaration
#: travelled into every generated task directory. The policy now lives in a build-time-only
#: module that appears in no staging list (``build.py``: AGENT_MODULES / VERIFIER_MODULES)
#: and in no COPY operand of either Dockerfile, so the permission below costs nothing.
POLICY_DECLARATION = "src/dmaic_harbor/policy.py"


def _is_dockerfile(path: Path) -> bool:
    return path.name == "Dockerfile" or path.name.startswith("Dockerfile.")


def _strip_dockerfile_comments(text: str) -> str:
    """Drop ``#`` comment lines from a Dockerfile.

    NARROW, MECHANICAL CARVE-OUT -- read this before widening it.

    Docker never adds the Dockerfile itself to the image filesystem; only the
    operands of COPY/ADD land there. A ``#`` comment in a Dockerfile is therefore
    in the same category as ``spec.py``'s declaration: a written statement of the
    policy that cannot itself ship. Restating the rule at the top of the image
    that must obey it is worth more than the zero risk it carries.

    What this carve-out does NOT cover, and what still fails hard: a forbidden
    string anywhere in a real instruction -- COPY, ADD, RUN, ENV, ARG, LABEL. Those
    do reach the image or its metadata.
    """
    kept: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        kept.append(line)
    return "\n".join(kept)


# =============================================================================
# 1. No forbidden string in any public file that can reach an image
# =============================================================================

def _subject_present(subject: str) -> bool:
    """True when operator-only material this test needs is actually in the tree."""
    if subject == "harbor/private/":
        return (HARBOR_ROOT / "private").is_dir()
    if subject.startswith("a built"):
        return bool(list((HARBOR_ROOT / "datasets").glob("*/dataset.toml"))) if (HARBOR_ROOT / "datasets").is_dir() else False
    return True


def test_forbidden_strings_confined_to_private_and_the_declaration():
    """Every public mention of the excluded stack must be provably unshippable.

    A file outside ``private/`` may contain a forbidden string only if it is the
    policy declaration, or if the simulated build-context filter proves the file
    never enters an image. Whitelisting a file is therefore not enough on its own --
    the exclusion has to be real.
    """
    offenders: list[str] = []
    for path in _iter_repo_files():
        rel = _rel(path)
        if rel.startswith(f"{policy.PRIVATE_DIR_NAME}/"):
            continue
        if rel == POLICY_DECLARATION:
            continue
        hits = _forbidden_hits(path)
        if not hits:
            continue
        if _is_excluded(rel, DOCKERIGNORE_RULES):
            continue
        offenders.append(f"{rel}: {hits}")

    assert not offenders, (
        "Public file(s) name the private contestant AND would be sent to the Docker "
        "build context. Either remove the mention or exclude the file in "
        ".dockerignore:\n  " + "\n  ".join(offenders)
    )


def test_declaration_and_private_readme_are_the_only_narrative_exceptions():
    """Pin the exception set so it cannot grow silently.

    ``policy.py`` and ``private/README.md`` are the two files the policy explicitly
    permits to describe itself. Any *other* file that names the stack must earn it by
    being excluded from the build context (asserted above) -- this test just makes
    the size and shape of the exception set visible in one place, so a reviewer sees
    it change.
    """
    permitted_in_context = {POLICY_DECLARATION}
    shipping_mentions = set()
    for path in _iter_repo_files():
        rel = _rel(path)
        if not _forbidden_hits(path):
            continue
        if _is_excluded(rel, DOCKERIGNORE_RULES):
            continue
        shipping_mentions.add(rel)

    assert shipping_mentions == permitted_in_context, (
        "The set of shippable files naming the private contestant changed.\n"
        f"  expected: {sorted(permitted_in_context)}\n"
        f"  actual:   {sorted(shipping_mentions)}"
    )


# =============================================================================
# 2. .dockerignore actually removes private/ from the build context
# =============================================================================
def test_private_dir_exists_and_has_content_to_exclude():
    # harbor/private/ is operator-only material: it is not part of the public
    # release (docs/HELD_OUT.md), so this has no subject in a public checkout.
    # It runs, and must pass, in an operator tree where the subject exists.
    if not _subject_present("harbor/private/"):
        pytest.skip("harbor/private/ absent (public release) -- operator-only")
    """A vacuous exclusion test is worse than none. Prove there is something to hide."""
    assert PRIVATE_DIR.is_dir(), "private/ is missing; this test would pass vacuously"
    contents = [p for p in PRIVATE_DIR.rglob("*") if p.is_file()]
    assert contents, "private/ is empty; this test would pass vacuously"


def test_dockerignore_removes_every_private_path_from_the_build_context():
    """Simulate the Docker build-context filter and assert private/** is absent."""
    surviving = [
        _rel(path)
        for path in _iter_repo_files()
        if _rel(path).startswith(f"{policy.PRIVATE_DIR_NAME}/")
        and not _is_excluded(_rel(path), DOCKERIGNORE_RULES)
    ]
    assert not surviving, (
        "These files under private/ would be sent to the Docker build context:\n  "
        + "\n  ".join(surviving)
    )


def test_dockerignore_filter_is_not_trivially_excluding_everything():
    """Guard the guard: a filter that drops the whole context would pass every check."""
    must_survive = ["pyproject.toml", "src/dmaic_harbor/spec.py"]
    for rel in must_survive:
        assert (HARBOR_ROOT / rel).exists(), f"missing fixture file {rel}"
        assert not _is_excluded(rel, DOCKERIGNORE_RULES), (
            f"{rel} must stay in the build context; the .dockerignore rules are "
            "over-broad and every exclusion assertion in this module is now vacuous"
        )


def test_dockerignore_pattern_matcher_behaves_like_docker():
    """Unit-test the simulator itself against known Docker semantics."""
    rules = _parse_dockerignore(
        "\n".join(["private", "**/*.key", "build/**", "docs", "!docs/keep.md"])
    )
    assert _is_excluded("private/operator_agent.py", rules)
    assert _is_excluded("private/nested/deep/file.txt", rules)
    assert _is_excluded("a/b/secret.key", rules)
    assert _is_excluded("secret.key", rules)
    assert _is_excluded("build/x/y.txt", rules)
    assert _is_excluded("docs/index.md", rules)
    assert not _is_excluded("docs/keep.md", rules)
    assert not _is_excluded("src/dmaic_harbor/spec.py", rules)
    assert not _is_excluded("privateer/notes.md", rules), "must not match by prefix"


# =============================================================================
# 3. No Dockerfile can copy its way out
# =============================================================================
_COPY_RE = re.compile(r"^\s*(COPY|ADD)\s+(.*)$", re.IGNORECASE)


def _dockerfiles() -> list[Path]:
    if not TEMPLATES_DIR.is_dir():
        return []
    return sorted(
        p
        for p in TEMPLATES_DIR.rglob("*")
        if p.is_file() and (p.name == "Dockerfile" or p.name.startswith("Dockerfile."))
    )


def _copy_sources(instruction_body: str) -> list[str]:
    """Extract the source operands of one COPY/ADD, both shell and JSON forms."""
    body = instruction_body.strip()
    tokens = [t for t in body.split() if not t.startswith("--")]
    if not tokens:
        return []
    if body.lstrip().startswith("["):
        inner = body[body.index("[") + 1 : body.rindex("]")] if "]" in body else ""
        items = [item.strip().strip('"').strip("'") for item in inner.split(",")]
        items = [item for item in items if item]
        return items[:-1]
    return tokens[:-1]


def _copy_instructions() -> list[tuple[Path, int, str, str]]:
    """(dockerfile, lineno, verb, source) for every COPY/ADD operand in templates/."""
    found: list[tuple[Path, int, str, str]] = []
    for dockerfile in _dockerfiles():
        text = _read_text(dockerfile) or ""
        # Join line continuations so a wrapped COPY is still one instruction.
        text = re.sub(r"\\\s*\n", " ", text)
        for lineno, line in enumerate(text.splitlines(), start=1):
            match = _COPY_RE.match(line)
            if not match:
                continue
            for source in _copy_sources(match.group(2)):
                if source.startswith("--"):
                    continue
                found.append((dockerfile, lineno, match.group(1), source.replace("\\", "/").strip()))
    return found


def test_no_dockerfile_copies_from_private_or_outside_the_context():
    """Hard rule, no exceptions: a COPY/ADD source may not reach excluded material.

    Rejected, with reasons:
      * ``private`` in any path component -- the direct leak.
      * a leading ``/`` or any ``..`` -- escapes the build context.
      * a component naming the excluded stack.
    """
    violations: list[str] = []
    for dockerfile, lineno, verb, source in _copy_instructions():
        parts = Path(source).parts
        reason = None
        if source.startswith("/"):
            reason = "absolute path escapes the build context"
        elif ".." in parts:
            reason = "'..' escapes the build context"
        elif policy.PRIVATE_DIR_NAME in parts:
            reason = "resolves into the excluded directory"
        elif any(token.rstrip("/") in source for token in policy.PUBLIC_IMAGE_FORBIDDEN):
            reason = "names an excluded component"
        if reason:
            violations.append(f"{_rel(dockerfile)}:{lineno} {verb} {source!r} -- {reason}")
    assert not violations, (
        "Dockerfile COPY/ADD source(s) could reach excluded material:\n  "
        + "\n  ".join(violations)
    )


def test_whole_context_copies_are_covered_by_a_proven_context_filter():
    """A whole-context ``COPY .`` is permitted only while the context filter is proven.

    NARROW, EXPLICIT CARVE-OUT -- and it is load-bearing in both directions.

    ``COPY .`` is the one form whose safety is not visible in the Dockerfile: what it
    copies depends entirely on the build context and on ``.dockerignore``. The
    verifier image uses it deliberately (a glob that matches nothing is a hard build
    error, and each of the wheel / source tree / truth file is optional in one build
    mode or another), so banning it outright would be banning a correct Dockerfile.

    What makes it safe is the ONE thing this suite can actually prove: that the
    context filter removes every path under ``private/``. So this test does not wave
    the copy through -- it re-derives that proof and fails with the whole-context
    copies named, the moment the filter stops holding. Deleting the ``private/`` rules
    from ``.dockerignore`` therefore fails here as well as in section 2.

    Residual risk this does NOT cover, and which belongs in review rather than a test:
    a ``COPY .`` puts the entire filtered context into an image layer permanently. A
    later ``rm -rf`` in a separate RUN does not remove it from the layer history. Any
    Dockerfile using this form should copy the specific paths it needs as soon as the
    set of paths is knowable.
    """
    whole_context = [
        f"{_rel(dockerfile)}:{lineno} {verb} {source!r}"
        for dockerfile, lineno, verb, source in _copy_instructions()
        if source in {".", "./", "*"}
    ]
    if not whole_context:
        return

    leaked = [
        _rel(path)
        for path in _iter_repo_files()
        if _rel(path).startswith(f"{policy.PRIVATE_DIR_NAME}/")
        and not _is_excluded(_rel(path), DOCKERIGNORE_RULES)
    ]
    assert not leaked, (
        "A whole-context copy is only safe while .dockerignore removes private/ from "
        "the context, and it no longer does.\n"
        f"  whole-context copies: {whole_context}\n"
        f"  paths that would leak: {leaked}"
    )

    # And the filter must not be a no-op that excludes private/ only by excluding
    # everything -- that would make the permission above meaningless.
    assert not _is_excluded("src/dmaic_harbor/spec.py", DOCKERIGNORE_RULES)


# =============================================================================
# 4. Manifests and task templates reference nothing under private/
# =============================================================================
def _task_tomls() -> list[Path]:
    found: list[Path] = []
    for root in (TEMPLATES_DIR, DATASETS_DIR):
        if root.is_dir():
            found += sorted(root.rglob("task.toml"))
    return found


def test_dataset_manifest_and_task_templates_reference_nothing_private():
    offenders: list[str] = []
    for path in [DATASET_MANIFEST, *_task_tomls()]:
        if not path.exists():
            continue
        text = _read_text(path) or ""
        if policy.PRIVATE_DIR_NAME in text:
            offenders.append(_rel(path))
        for token in policy.PUBLIC_IMAGE_FORBIDDEN:
            if token in text:
                offenders.append(f"{_rel(path)} (contains {token!r})")
    assert not offenders, "manifest/task template references excluded material: " + ", ".join(
        sorted(set(offenders))
    )


def test_every_generated_task_dir_is_clean():
    """Generated task directories are the payload of the agent image. Scan them all."""
    if not DATASET_DIR.is_dir():
        pytest.skip("dataset directory has not been created yet")
    offenders: list[str] = []
    for path in sorted(DATASET_DIR.rglob("*")):
        if not path.is_file() or path.name == ".DS_Store":
            continue
        hits = _forbidden_hits(path)
        if hits:
            offenders.append(f"{_rel(path)}: {hits}")
    assert not offenders, "generated task material names a private contestant:\n  " + "\n  ".join(
        offenders
    )


# =============================================================================
# 5. The published dataset and job config list no private contestant
# =============================================================================
def test_dataset_manifest_validates_and_names_no_contestant(tmp_path):
    # Validate the current release from a fresh build. Operator datasets may be historical
    # experiment artifacts and must retain their original release version.
    DatasetManifest, _ = _import_harbor_models()
    from dmaic_harbor import build
    build.build(tmp_path, limit=1, seeds=(1,), verifier_base=None)
    manifest = DatasetManifest.from_toml_file(tmp_path / "dataset.toml")

    assert manifest.dataset.version == spec.PACKAGE_VERSION, (
        f"dataset version {manifest.dataset.version!r} must track "
        f"spec.PACKAGE_VERSION ({spec.PACKAGE_VERSION!r})"
    )
    assert manifest.dataset.short_name == spec.DATASET_NAME, (
        f"dataset short name {manifest.dataset.short_name!r} must be "
        f"spec.DATASET_NAME ({spec.DATASET_NAME!r})"
    )
    assert manifest.dataset.description.strip(), "dataset needs a real description"

    # A dataset declares TASKS. Contestants belong to a job config, never here.
    blob = " ".join(
        [manifest.dataset.name, manifest.dataset.description, *manifest.dataset.keywords]
        + [task.name for task in manifest.tasks]
        + [file_ref.path for file_ref in manifest.files]
    ).lower()
    for token in policy.PUBLIC_IMAGE_FORBIDDEN:
        assert token.rstrip("/").lower() not in blob, (
            f"dataset manifest names {token!r}; the dataset must not identify a contestant"
        )


def test_job_example_validates_and_lists_no_excluded_contestant():
    _, JobConfig = _import_harbor_models()
    yaml = pytest.importorskip("yaml")
    config = JobConfig.model_validate(yaml.safe_load(JOB_EXAMPLE.read_text()))

    assert config.n_attempts == 3, "the reproducibility example must run at k=3"
    assert config.datasets, "the example must point at the DMAIC dataset"
    assert len(config.agents) >= 2, "the example must run more than one contestant"

    for agent in config.agents:
        identity = " ".join(
            filter(None, [agent.name, agent.import_path, agent.model_name])
        ).lower()
        for token in policy.PUBLIC_IMAGE_FORBIDDEN:
            assert token.rstrip("/").lower() not in identity, (
                f"job.example.yaml lists a private contestant: {identity!r}. "
                "It is not reproducible by a reader and must stay in a local, "
                "uncommitted job config."
            )
        assert not agent.env or not any(
            token.rstrip("/").lower() in key.lower()
            for key in agent.env
            for token in policy.PUBLIC_IMAGE_FORBIDDEN
        ), "job.example.yaml carries excluded-contestant environment wiring"

    # The example must collect exactly the contract's artifacts: they are the only
    # channel to the separate verifier, so a missing one silently zeroes a score.
    sources = {
        (a.source if hasattr(a, "source") else a) for a in config.artifacts
    }
    for source, _destination in spec.COLLECTED_ARTIFACTS:
        assert source in sources, f"job.example.yaml does not collect {source}"


# =============================================================================
# 6. Packaging must not ship the excluded adapter
# =============================================================================
def test_sdist_include_list_is_an_allowlist_without_private():
    data = tomllib.loads(PYPROJECT.read_text())
    build = data["tool"]["hatch"]["build"]

    # An allowlist alone is NOT sufficient, and this is not a belt-and-braces
    # assertion. Hatchling's default file selection picks up README/LICENSE files
    # wherever they live in the tree, and it silently pulled private/README.md into
    # the sdist until an explicit exclude was added. Verified with `python3 -m build`.
    excluded = build.get("exclude", [])
    assert any(
        Path(entry).parts and Path(entry).parts[0] == policy.PRIVATE_DIR_NAME
        for entry in excluded
    ), (
        "[tool.hatch.build] must explicitly exclude the operator-only directory; "
        "the sdist allowlist does not stop hatchling's default file selection"
    )

    sdist = build["targets"]["sdist"]
    include = sdist["include"]
    assert include, "sdist must use an explicit allowlist, not the default everything"
    for entry in include:
        assert policy.PRIVATE_DIR_NAME not in Path(entry).parts, (
            f"sdist include list packages excluded material: {entry!r}"
        )
    wheel = build["targets"]["wheel"]
    for entry in wheel["packages"]:
        assert policy.PRIVATE_DIR_NAME not in Path(entry).parts

    scripts = data["project"]["scripts"]
    assert "dmaic-harbor-build" in scripts
    assert "steward" in scripts
    for target in scripts.values():
        assert target.startswith("dmaic_harbor."), (
            f"console script {target!r} must live in the public package"
        )


def test_public_package_never_imports_from_private():
    """The public side must not depend on the operator-only side, in either direction."""
    offenders: list[str] = []
    for path in sorted(SRC_DIR.rglob("*.py")):
        text = _read_text(path) or ""
        if re.search(rf"\b(import|from)\s+{policy.PRIVATE_DIR_NAME}\b", text):
            offenders.append(_rel(path))
        if "operator_agent" in text:
            offenders.append(f"{_rel(path)} (references the excluded adapter module)")
    assert not offenders, "public package imports excluded material: " + ", ".join(offenders)


def test_copy_rule_classifier_rejects_the_dangerous_forms():
    """Unit-test the COPY classifier itself, without touching a real Dockerfile.

    Section 3 can only fail on Dockerfiles that exist. This keeps the rule honest
    while ``templates/`` is still being written, and pins the parsing of the awkward
    forms (flags, JSON array, multiple sources) that a hand-rolled matcher gets wrong.
    """
    assert _copy_sources("--chown=1000:1000 task/ /opt/x/") == ["task/"]
    assert _copy_sources('["a.py", "b.py", "/dest/"]') == ["a.py", "b.py"]
    assert _copy_sources("--from=builder /out/app /app") == ["/out/app"]
    assert _copy_sources("spec.py steward_cli.py /opt/lib/") == ["spec.py", "steward_cli.py"]

    def classify(source: str) -> str | None:
        parts = Path(source).parts
        if source.startswith("/"):
            return "absolute"
        if ".." in parts:
            return "escape"
        if policy.PRIVATE_DIR_NAME in parts:
            return "private"
        if any(token.rstrip("/") in source for token in policy.PUBLIC_IMAGE_FORBIDDEN):
            return "named"
        return None

    assert classify("private/agent.py") == "private"
    assert classify("../private/x") == "escape"
    assert classify("/etc/passwd") == "absolute"
    # The vendor tokens are supplied by the operator at build time and are deliberately not
    # written into this public file (policy._STRUCTURAL_FORBIDDEN). So prove the MECHANISM
    # rather than a baked-in list: with a token configured, a source naming it is caught.
    import importlib
    os.environ["DMAIC_FORBIDDEN_TOKENS"] = "acme-engine"
    try:
        importlib.reload(policy)
        assert "acme-engine" in policy.PUBLIC_IMAGE_FORBIDDEN
        assert classify("lib/acme-engine_adapter.py") == "named"
    finally:
        del os.environ["DMAIC_FORBIDDEN_TOKENS"]
        importlib.reload(policy)
    assert classify("lib/operator_adapter.py") is None  # nothing configured, nothing flagged
    assert classify("task/blocks.json") is None
    assert classify("dmaic_harbor/spec.py") is None


# =============================================================================
# 7. The excluded adapter carries no credentials and no default endpoint
# =============================================================================
def test_private_adapter_hardcodes_no_endpoint_or_credential():
    # harbor/private/ is operator-only material: it is not part of the public
    # release (docs/HELD_OUT.md), so this has no subject in a public checkout.
    # It runs, and must pass, in an operator tree where the subject exists.
    if not _subject_present("harbor/private/"):
        pytest.skip("harbor/private/ absent (public release) -- operator-only")
    """A file that never ships can still leak if someone copies a line out of it.

    The adapter must take its endpoint and account entirely from the environment: no
    default host, no fallback account, no literal secret. A missing variable has to
    raise, because a silent fallback to ``localhost`` is how an operator's run
    quietly measures nothing.
    """
    adapter = PRIVATE_DIR / "operator_agent.py"
    assert adapter.exists(), "the private adapter is missing"
    source = adapter.read_text(encoding="utf-8")
    body = "\n".join(
        line for line in source.splitlines() if not line.lstrip().startswith("#")
    )
    # Strip the module docstring: it documents the variable names and an example host.
    if body.count('"""') >= 2:
        first = body.index('"""')
        second = body.index('"""', first + 3)
        body = body[:first] + body[second + 3 :]

    for required in (
        "OPERATOR_AGENT_BASE_URL",
        "OPERATOR_AGENT_USERNAME",
        "OPERATOR_AGENT_PASSWORD",
        "OPERATOR_AGENT_AGENT_ID",
    ):
        assert f'_require_env("{required}")' in body, (
            f"{required} must be fetched through _require_env so a missing value raises"
        )

    credential_re = r"""(?:password|passwd|secret|token|api_key)\s*=\s*["'][^"']+["']"""
    for leak in re.findall(credential_re, body, flags=re.IGNORECASE):
        pytest.fail(f"literal credential in the private adapter: {leak!r}")

    for url in re.findall(r"""["']https?://[^"'\s]+["']""", body):
        pytest.fail(f"hardcoded endpoint in the private adapter: {url}")
