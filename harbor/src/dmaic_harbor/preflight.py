"""Campaign preflight: refuse to start a sweep that the host cannot finish.

WHY THIS EXISTS
---------------
Three campaigns in a row lost trials to the host, not to the models. The largest single
loss was an undeclared environment variable: with no container-runtime socket exported,
and with the default BuildKit builder selected, **every** trial dies in environment build
before a model is asked a single question. Nothing warned. The run simply produced a
column of failures that look, in a results table, exactly like a model that cannot do the
task.

A preflight is cheap in a way the failure is not. It runs in seconds, once, before the
first trial; the failure it prevents costs hours of wall clock and the whole budget of
whatever ran before someone noticed.

WHAT IT CHECKS
--------------
1. ``container-runtime``  -- a reachable container runtime (the socket, and a live daemon
   behind it).
2. ``buildx-builder``     -- a build backend that exists and is selected. The default
   builder points at the daemon socket and does not inherit this host's proxy settings,
   so it fails base-image pulls even when the runtime itself is healthy.
3. ``base-images``        -- the pinned base image is present locally or pullable now.
4. ``disk-space``         -- enough free space for the job directory. A sweep writes one
   trial directory per (task x attempt), each holding a trajectory and a verifier log.
5. ``credentials``        -- the credential file exists, is a regular file, is mode 600 or
   400, and its directory is not writable by anyone else.

DESIGN RULES THIS MODULE FOLLOWS
--------------------------------
* **No credential value is ever read into a message.** The credential check reports
  variable NAMES and whether they are empty. It never opens a value, never logs one, and
  never puts one in a process argument.
* **Every failure carries its fix.** A check that says "not configured" and stops has
  moved the operator no closer to a running campaign than the original failure did.
* **Subprocess calls go through an injectable runner** so the whole matrix -- including
  every failure branch -- is exercised in tests without a container runtime, a network,
  or a credential.
* Nothing here is host-specific. Paths are derived from the environment or from
  :mod:`dmaic_harbor.spec`.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:  # pragma: no cover - exercised implicitly by every import in the suite
    from . import spec
except ImportError:  # pragma: no cover - direct-script execution
    import spec  # type: ignore[no-redef]


# --------------------------------------------------------------------------- defaults

#: Free space required, in gibibytes, on the filesystem that will hold the job directory.
#: A single trial directory holds a trajectory, the collected artifacts and a verifier
#: log; a few thousand of them is the scale this default is sized for. Override with
#: ``--min-free-gb``.
DEFAULT_MIN_FREE_GB = 20.0

#: Seconds any single probe subprocess may take. A hung runtime socket is a failure, and
#: it must be reported as one rather than hanging the preflight for as long as it hangs
#: the campaign.
DEFAULT_TIMEOUT_S = 60

#: Where the credential file lives, in resolution order. Matches ``scripts/campaign-env.sh``
#: exactly -- one source of truth, so the preflight cannot pass a file the launcher then
#: refuses to source (or the reverse).
ENV_FILE_VAR = "DMAIC_ENV_FILE"
DEFAULT_ENV_FILE_REL = ".config/dmaic/campaign.env"

#: Other directories under ``~/.config`` that a campaign credential file has plausibly been
#: put in. Probed ONLY to turn "not found" into "found, but not where the loader reads",
#: which is a different operator action. Never sourced, never opened.
NEAR_MISS_DIRS = (".config/autodmaic", ".config/dmaic-bench", ".config/harbor")

#: Environment variables that select the container tooling. Undeclared until now; that is
#: the defect this module was written for.
DOCKER_HOST_VAR = "DOCKER_HOST"
BUILDX_BUILDER_VAR = "BUILDX_BUILDER"

#: Override the container CLI (``docker`` / ``podman`` / a wrapper). Both are probed in
#: this order when unset.
CONTAINER_CLI_VAR = "DMAIC_CONTAINER_CLI"
_CLI_CANDIDATES = ("docker", "podman")

OK, WARN, FAIL, SKIP = "ok", "warn", "fail", "skip"

_STATUS_ORDER = {OK: 0, SKIP: 1, WARN: 2, FAIL: 3}


# --------------------------------------------------------------------------- result model

@dataclass
class Check:
    """One preflight verdict.

    ``fix`` is not decoration. A preflight whose output an operator cannot act on has
    replaced a confusing failure with an early confusing failure.
    """

    name: str
    status: str
    summary: str
    detail: list[str] = field(default_factory=list)
    fix: list[str] = field(default_factory=list)

    @property
    def failed(self) -> bool:
        return self.status == FAIL

    def to_dict(self) -> dict:
        return {"name": self.name, "status": self.status, "summary": self.summary,
                "detail": list(self.detail), "fix": list(self.fix)}


@dataclass
class Report:
    checks: list[Check] = field(default_factory=list)

    @property
    def status(self) -> str:
        return max((c.status for c in self.checks), key=lambda s: _STATUS_ORDER[s],
                   default=OK)

    @property
    def ok(self) -> bool:
        return not any(c.failed for c in self.checks)

    def to_dict(self) -> dict:
        return {"status": self.status, "ok": self.ok,
                "checks": [c.to_dict() for c in self.checks]}

    def render(self, color: bool = False) -> str:
        badge = {OK: "PASS", WARN: "WARN", FAIL: "FAIL", SKIP: "SKIP"}
        tint = {OK: "\033[32m", WARN: "\033[33m", FAIL: "\033[31m", SKIP: "\033[2m"}
        lines = ["", "DMAIC-Bench campaign preflight", "=" * 62]
        for c in self.checks:
            head = f"{badge[c.status]:4}  {c.name:<18}  {c.summary}"
            if color:
                head = f"{tint[c.status]}{head}\033[0m"
            lines.append(head)
            for d in c.detail:
                lines.append(f"        {d}")
            for i, f in enumerate(c.fix):
                lines.append(f"        fix: {f}" if i == 0 else f"             {f}")
        lines.append("=" * 62)
        failed = [c.name for c in self.checks if c.failed]
        if failed:
            lines.append(f"PREFLIGHT FAILED: {', '.join(failed)}")
            lines.append("Nothing was launched. Fix the above and re-run; every trial of a")
            lines.append("campaign started in this state would fail before a model is asked")
            lines.append("anything, and would be recorded as a result.")
        else:
            warned = [c.name for c in self.checks if c.status == WARN]
            lines.append("PREFLIGHT PASSED" + (f" (with warnings: {', '.join(warned)})"
                                               if warned else ""))
        lines.append("")
        return "\n".join(lines)


# --------------------------------------------------------------------------- runner

class Runner:
    """Runs probe subprocesses. Injectable so tests exercise every branch offline."""

    def __init__(self, timeout: int = DEFAULT_TIMEOUT_S, env: dict | None = None):
        self.timeout = timeout
        self.env = env

    def which(self, name: str) -> str | None:
        return shutil.which(name)

    def run(self, argv: list[str], timeout: int | None = None) -> tuple[int, str, str]:
        """``(returncode, stdout, stderr)``. A timeout or a missing binary is a return
        code, never an exception -- a preflight that crashes is a preflight that gets
        commented out."""
        try:
            p = subprocess.run(argv, capture_output=True, text=True,
                               timeout=timeout or self.timeout, env=self.env)
            return p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired:
            return 124, "", f"timed out after {timeout or self.timeout}s: {' '.join(argv)}"
        except FileNotFoundError:
            return 127, "", f"no such executable: {argv[0]}"
        except OSError as exc:  # pragma: no cover - defensive
            return 126, "", f"{type(exc).__name__}: {exc}"


def _first_line(text: str, limit: int = 200) -> str:
    for line in (text or "").splitlines():
        line = line.strip()
        if line:
            return line[:limit]
    return ""


def container_cli(runner: Runner, env: dict) -> str | None:
    override = env.get(CONTAINER_CLI_VAR, "").strip()
    if override:
        return override if runner.which(override) or "/" in override else None
    for name in _CLI_CANDIDATES:
        if runner.which(name):
            return name
    return None


# --------------------------------------------------------------------------- 1. runtime

def check_container_runtime(runner: Runner, env: dict) -> Check:
    name = "container-runtime"
    cli = container_cli(runner, env)
    if cli is None:
        return Check(name, FAIL, "no container CLI on PATH",
                     detail=[f"looked for: {', '.join(_CLI_CANDIDATES)}"],
                     fix=["install a container runtime, or point the preflight at yours:",
                          f"export {CONTAINER_CLI_VAR}=<your-docker-compatible-cli>"])

    host = env.get(DOCKER_HOST_VAR, "").strip()
    detail = [f"cli: {cli}"]

    if not host:
        # This is failure #1 of the last three campaigns, and it is silent: the runtime is
        # installed and healthy, the socket exists, and nothing connects them.
        return Check(
            name, FAIL,
            f"{DOCKER_HOST_VAR} is not set",
            detail=detail + [
                "The runtime client falls back to the default daemon socket. On a host whose",
                "engine is a rootless VM (no daemon at the default path) that socket does not",
                "exist, so EVERY trial fails in environment build, before the model is asked",
                "anything -- and is then recorded as a trial result.",
            ],
            fix=[f'export {DOCKER_HOST_VAR}="unix://$(podman machine inspect '
                 "--format '{{.ConnectionInfo.PodmanSocket.Path}}')\"",
                 "(start the VM first if it is not running: podman machine start)",
                 "For a real Docker daemon, export the path your daemon listens on."],
        )

    detail.append(f"{DOCKER_HOST_VAR}={host}")
    if host.startswith("unix://"):
        sock = host[len("unix://"):]
        if not Path(sock).exists():
            return Check(name, FAIL, f"{DOCKER_HOST_VAR} points at a socket that does not exist",
                         detail=detail + [f"missing: {sock}"],
                         fix=["start the runtime, then re-derive the path:",
                              "podman machine start",
                              f'export {DOCKER_HOST_VAR}="unix://$(podman machine inspect '
                              "--format '{{.ConnectionInfo.PodmanSocket.Path}}')\""])

    rc, out, err = runner.run([cli, "info", "--format", "{{.ServerVersion}}"])
    if rc != 0:
        return Check(name, FAIL, "the container runtime did not answer",
                     detail=detail + [f"`{cli} info` exited {rc}",
                                      _first_line(err) or _first_line(out)],
                     fix=["start the runtime and confirm it answers:",
                          "podman machine start",
                          f"{cli} info"])
    version = _first_line(out) or "unknown"
    return Check(name, OK, f"reachable (server {version})", detail=detail)


# --------------------------------------------------------------------------- 2. builder

def check_buildx_builder(runner: Runner, env: dict) -> Check:
    name = "buildx-builder"
    cli = container_cli(runner, env)
    if cli is None:
        return Check(name, SKIP, "no container CLI on PATH (see container-runtime)")

    builder = env.get(BUILDX_BUILDER_VAR, "").strip()
    if not builder:
        # Failure #2, and the one that reads as a network outage. The default builder's
        # endpoint is the daemon socket, and it does not inherit this shell's proxy
        # variables, so it fails to resolve base-image metadata even when `pull` works.
        return Check(
            name, FAIL,
            f"{BUILDX_BUILDER_VAR} is not set",
            detail=[
                "BuildKit then selects the `default` builder, whose endpoint is the daemon",
                "socket and which does NOT inherit this shell's proxy environment. Base-image",
                "pulls fail with `403 Forbidden` or",
                "`failed to resolve source metadata for ...: EOF` -- which reads as a network",
                "outage and is not one.",
            ],
            fix=[f"{cli} buildx create --name proxied --driver docker-container \\",
                 '    --driver-opt env.HTTP_PROXY="$HTTP_PROXY" \\',
                 '    --driver-opt env.HTTPS_PROXY="$HTTPS_PROXY" \\',
                 '    --driver-opt env.NO_PROXY="$NO_PROXY" --use',
                 f"export {BUILDX_BUILDER_VAR}=proxied",
                 "(a host with no proxy still needs a named docker-container builder here:",
                 " the `default` builder's endpoint is the absent daemon socket.)"],
        )

    rc, out, err = runner.run([cli, "buildx", "inspect", builder])
    if rc != 0:
        text = _first_line(err) or _first_line(out)
        return Check(name, FAIL, f"builder {builder!r} does not exist",
                     detail=[f"`{cli} buildx inspect {builder}` exited {rc}", text],
                     fix=[f"{cli} buildx ls        # what does exist",
                          f"{cli} buildx create --name {builder} --driver docker-container \\",
                          '    --driver-opt env.HTTPS_PROXY="$HTTPS_PROXY" --use'])

    running = "running" in out.lower()
    detail = [f"{BUILDX_BUILDER_VAR}={builder}"]
    for line in out.splitlines():
        if line.split(":", 1)[0].strip() in ("Driver", "Status", "Endpoint"):
            detail.append(line.strip())
    if not running:
        return Check(name, WARN, f"builder {builder!r} exists but is not running",
                     detail=detail,
                     fix=[f"{cli} buildx inspect --bootstrap {builder}"])
    return Check(name, OK, f"builder {builder!r} is running", detail=detail)


# --------------------------------------------------------------------------- 3. images

def base_images() -> list[str]:
    """The images a build must resolve. Derived from the spec, never retyped."""
    return [spec.PYTHON_BASE_IMAGE]


def check_base_images(runner: Runner, env: dict, pull: bool = True) -> Check:
    name = "base-images"
    cli = container_cli(runner, env)
    if cli is None:
        return Check(name, SKIP, "no container CLI on PATH (see container-runtime)")

    images = base_images()
    present, pulled, missing = [], [], []
    for image in images:
        rc, _, _ = runner.run([cli, "image", "inspect", image])
        if rc == 0:
            present.append(image)
            continue
        if not pull:
            missing.append((image, "absent locally; --no-pull, so not fetched"))
            continue
        rc, out, err = runner.run([cli, "pull", image], timeout=max(runner.timeout, 300))
        if rc == 0:
            pulled.append(image)
        else:
            missing.append((image, _first_line(err) or _first_line(out) or f"exit {rc}"))

    detail = [f"present: {i}" for i in present] + [f"pulled: {i}" for i in pulled]
    if missing:
        return Check(
            name, FAIL, f"{len(missing)} of {len(images)} base image(s) unavailable",
            detail=detail + [f"unavailable: {i} -- {why}" for i, why in missing],
            fix=["check registry reachability THROUGH the builder, not just this shell:",
                 f"{cli} pull {missing[0][0]}",
                 "a `403 Forbidden` or an `EOF` resolving source metadata here is almost",
                 f"always the {BUILDX_BUILDER_VAR} defect above, not the registry."],
        )
    if not pull and not present:
        return Check(name, WARN, "base images not verified (--no-pull)", detail=detail)
    return Check(name, OK, f"{len(images)} base image(s) available", detail=detail)


# --------------------------------------------------------------------------- 4. disk

def check_disk_space(path: Path, min_free_gb: float = DEFAULT_MIN_FREE_GB) -> Check:
    name = "disk-space"
    probe = path
    while not probe.exists() and probe != probe.parent:
        probe = probe.parent
    try:
        usage = shutil.disk_usage(probe)
    except OSError as exc:
        return Check(name, WARN, "could not measure free space",
                     detail=[f"{type(exc).__name__}: {exc}", f"path: {probe}"])
    free_gb = usage.free / (1024 ** 3)
    detail = [f"job directory: {path}",
              f"free: {free_gb:.1f} GiB of {usage.total / (1024 ** 3):.1f} GiB"]
    if free_gb < min_free_gb:
        return Check(
            name, FAIL, f"only {free_gb:.1f} GiB free, {min_free_gb:.0f} GiB required",
            detail=detail + [
                "A sweep writes one directory per (task x attempt): trajectory, collected",
                "artifacts and verifier log. Running out mid-campaign loses the trials that",
                "were in flight AND corrupts the ones being written.",
            ],
            fix=["free space, or point the job directory at a larger filesystem:",
                 "  jobs_dir: <path-on-a-larger-filesystem>   # in the job config",
                 "image layers live in the runtime's own storage, which may be a separate",
                 "filesystem (or inside a VM) -- check that too."],
        )
    return Check(name, OK, f"{free_gb:.1f} GiB free", detail=detail)


# --------------------------------------------------------------------------- 5. credentials

def resolve_env_file(env: dict) -> Path:
    override = env.get(ENV_FILE_VAR, "").strip()
    if override:
        return Path(override).expanduser()
    return Path(env.get("HOME", "~")).expanduser() / DEFAULT_ENV_FILE_REL


def scan_env_file(path: Path) -> tuple[list[str], list[str]]:
    """``(declared names, names whose value is empty)``. NO VALUE IS EVER RETURNED.

    The file is opened, but the right-hand side of each assignment is reduced to a single
    bit -- "empty or not" -- on the same line it is parsed, and the text itself is never
    stored, returned, logged or interpolated into a message. Emptiness is the only
    property of a credential this module is permitted to compute, and it is the one that
    separates "you have not filled this in" from "your key is wrong" (which is the
    liveness probe's question, not this one's).
    """
    names: list[str] = []
    empty: list[str] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return names, empty
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        head, sep, tail = line.partition("=")
        if not sep:
            continue
        key = head.strip()
        if not key or not all(ch.isalnum() or ch == "_" for ch in key):
            continue
        names.append(key)
        if tail.strip().strip("'\"") == "":
            empty.append(key)
    return names, empty


def check_credentials(env: dict) -> Check:
    name = "credentials"
    path = resolve_env_file(env)

    if not path.exists():
        near = []
        home = Path(env.get("HOME", "~")).expanduser()
        for rel in NEAR_MISS_DIRS:
            candidate = home / rel / "campaign.env"
            if candidate.exists():
                near.append(str(candidate))
        detail = [f"expected at: {path}"]
        if near:
            detail += ["found a credential file the loader does NOT read:"] + \
                      [f"  {n}" for n in near] + \
                      ["move it, or point the loader at it with "
                       f"{ENV_FILE_VAR}."]
        return Check(name, FAIL, "no credential file", detail=detail,
                     fix=["mkdir -p \"$(dirname \"" + str(path) + "\")\" && chmod 700 "
                          "\"$(dirname \"" + str(path) + "\")\"",
                          "cp .env.example " + str(path),
                          "chmod 600 " + str(path),
                          "$EDITOR " + str(path),
                          f"(or point {ENV_FILE_VAR} at wherever yours already lives)"])

    if path.is_dir():
        return Check(name, FAIL, "credential path is a directory", detail=[str(path)],
                     fix=[f"{ENV_FILE_VAR} must name a FILE, not a directory"])

    st = path.stat()
    mode = stat.S_IMODE(st.st_mode)
    detail = [f"file: {path}", f"mode: {mode:04o}"]

    if mode not in (0o600, 0o400):
        return Check(
            name, FAIL, f"credential file is mode {mode:04o}, must be 600 or 400",
            detail=detail + ["Every value in it is a bearer credential: anything that can",
                             "read it can spend money as you."],
            fix=[f"chmod 600 {path}"])

    parent_mode = stat.S_IMODE(path.parent.stat().st_mode)
    if parent_mode & 0o022:
        return Check(name, FAIL,
                     f"credential directory is mode {parent_mode:04o} (writable by others)",
                     detail=detail + [f"directory: {path.parent}",
                                      "A file mode of 600 protects the contents; it does not"
                                      " stop someone who can write the directory from"
                                      " replacing the file."],
                     fix=[f"chmod 700 {path.parent}"])

    if st.st_size == 0:
        return Check(name, FAIL, "credential file is empty", detail=detail,
                     fix=[f"cp .env.example {path} && $EDITOR {path}"])

    names, empty = scan_env_file(path)
    detail.append(f"declares {len(names)} variable(s)")
    if not names:
        return Check(name, FAIL, "credential file declares no variables", detail=detail,
                     fix=["the file must contain shell assignments, e.g.",
                          '  export SOME_API_KEY="..."',
                          f"see .env.example for the names this campaign expects"])
    if empty:
        # A WARN, not a FAIL: a campaign may deliberately configure a subset of providers.
        # The liveness probe is what turns "declared" into "usable"; see `probe.py`.
        return Check(name, WARN, f"{len(empty)} declared variable(s) are empty",
                     detail=detail + [f"empty: {', '.join(sorted(empty))}"],
                     fix=[f"fill them in, or delete the lines: $EDITOR {path}",
                          "then run the provider liveness probe:",
                          "  python3 -m dmaic_harbor.probe"])
    return Check(name, OK, f"present, mode {mode:04o}, {len(names)} variable(s)",
                 detail=detail)


# --------------------------------------------------------------------------- orchestration

def run_preflight(jobs_dir: Path | str = ".", *, env: dict | None = None,
                  runner: Runner | None = None, pull: bool = True,
                  min_free_gb: float = DEFAULT_MIN_FREE_GB,
                  skip: tuple[str, ...] = ()) -> Report:
    env = dict(os.environ if env is None else env)
    runner = runner or Runner()
    jobs_dir = Path(jobs_dir)

    planned = [
        ("container-runtime", lambda: check_container_runtime(runner, env)),
        ("buildx-builder", lambda: check_buildx_builder(runner, env)),
        ("base-images", lambda: check_base_images(runner, env, pull=pull)),
        ("disk-space", lambda: check_disk_space(jobs_dir, min_free_gb)),
        ("credentials", lambda: check_credentials(env)),
    ]
    report = Report()
    for name, fn in planned:
        if name in skip:
            report.checks.append(Check(name, SKIP, "skipped by request"))
            continue
        report.checks.append(fn())
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="dmaic-harbor-preflight",
        description="Refuse to start a campaign the host cannot finish. "
                    "Exit 0 = safe to launch; exit 1 = at least one hard failure.")
    ap.add_argument("--jobs-dir", default=".",
                    help="where the campaign will write trial directories (disk check)")
    ap.add_argument("--min-free-gb", type=float, default=DEFAULT_MIN_FREE_GB)
    ap.add_argument("--no-pull", action="store_true",
                    help="do not fetch a missing base image; report it instead")
    ap.add_argument("--skip", action="append", default=[], metavar="CHECK",
                    help="skip a named check (repeatable)")
    ap.add_argument("--json", action="store_true", help="machine-readable report on stdout")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_S)
    a = ap.parse_args(argv)

    report = run_preflight(a.jobs_dir, runner=Runner(timeout=a.timeout),
                           pull=not a.no_pull, min_free_gb=a.min_free_gb,
                           skip=tuple(a.skip))
    if a.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(report.render(color=sys.stdout.isatty()))
    return 0 if report.ok else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
