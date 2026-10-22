"""The campaign preflight, exercised offline.

Every branch here runs with NO container runtime, NO network and NO credential: the
subprocess layer is injected, and the credential checks operate on files this test makes
in a temporary directory. That is deliberate and not merely convenient -- a preflight
whose failure paths are only ever exercised by a real broken host is a preflight whose
failure paths are never exercised, and the failure paths are the entire product.
"""
from __future__ import annotations

import os
import stat
from pathlib import Path

import pytest

from dmaic_harbor import preflight, spec
from dmaic_harbor.preflight import FAIL, OK, SKIP, WARN


# --------------------------------------------------------------------------- fakes

class FakeRunner(preflight.Runner):
    """Answers probe subprocesses from a scripted table.

    Keys are matched as a prefix of the joined argv, so a test states only as much of the
    command as it cares about.
    """

    def __init__(self, table: dict, present: tuple = ("docker",)):
        super().__init__(timeout=1)
        self.table = table
        self.present = present
        self.calls: list = []

    def which(self, name):
        return f"/usr/bin/{name}" if name in self.present else None

    def run(self, argv, timeout=None):
        self.calls.append(list(argv))
        joined = " ".join(argv)
        for prefix, response in self.table.items():
            if joined.startswith(prefix):
                return response
        return (1, "", "unscripted command")


HEALTHY = {
    "/usr/bin/docker info": (0, "27.0.3\n", ""),
    "docker info": (0, "27.0.3\n", ""),
    "docker buildx inspect proxied": (
        0, "Name: proxied\nDriver: docker-container\nStatus: running\n", ""),
    f"docker image inspect {spec.PYTHON_BASE_IMAGE}": (0, "[]", ""),
}


def env(**kw) -> dict:
    base = {"HOME": "/nonexistent-home", "DOCKER_HOST": "unix:///tmp",
            "BUILDX_BUILDER": "proxied"}
    base.update(kw)
    return {k: v for k, v in base.items() if v is not None}


def _named(report, name):
    return next(c for c in report.checks if c.name == name)


# ============================================================ 1. container runtime

def test_missing_docker_host_is_a_hard_failure_with_the_export_in_the_fix():
    """The defect that killed three campaigns: nothing warns, and every trial dies."""
    c = preflight.check_container_runtime(FakeRunner(HEALTHY), env(DOCKER_HOST=None))
    assert c.status == FAIL
    assert "DOCKER_HOST is not set" in c.summary
    # The message must carry the actual command, not an instruction to go find one.
    assert any("export DOCKER_HOST=" in line for line in c.fix)
    assert any("before the model is asked" in line for line in c.detail)


def test_docker_host_pointing_at_an_absent_socket_fails_and_names_the_socket(tmp_path):
    missing = tmp_path / "nope.sock"
    c = preflight.check_container_runtime(
        FakeRunner(HEALTHY), env(DOCKER_HOST=f"unix://{missing}"))
    assert c.status == FAIL
    assert str(missing) in " ".join(c.detail)


def test_unreachable_daemon_is_reported_with_the_runtime_s_own_words(tmp_path):
    sock = tmp_path / "s.sock"
    sock.touch()
    runner = FakeRunner({"docker info": (1, "", "Cannot connect to the Docker daemon")})
    c = preflight.check_container_runtime(runner, env(DOCKER_HOST=f"unix://{sock}"))
    assert c.status == FAIL
    assert "Cannot connect to the Docker daemon" in " ".join(c.detail)


def test_healthy_runtime_passes_and_reports_the_server_version(tmp_path):
    sock = tmp_path / "s.sock"
    sock.touch()
    c = preflight.check_container_runtime(FakeRunner(HEALTHY),
                                          env(DOCKER_HOST=f"unix://{sock}"))
    assert c.status == OK
    assert "27.0.3" in c.summary


def test_no_container_cli_at_all_is_a_failure_not_a_crash():
    c = preflight.check_container_runtime(FakeRunner(HEALTHY, present=()), env())
    assert c.status == FAIL
    assert "no container CLI" in c.summary


def test_a_probe_that_times_out_is_a_verdict_not_an_exception():
    """A hung socket must be reported. A preflight that hangs is one that gets deleted."""
    runner = preflight.Runner(timeout=1)
    rc, _, err = runner.run(["/bin/sh", "-c", "sleep 5"], timeout=1)
    assert rc == 124 and "timed out" in err


def test_a_missing_executable_is_a_verdict_not_an_exception():
    rc, _, err = preflight.Runner(timeout=1).run(["definitely-not-a-real-binary-xyz"])
    assert rc == 127 and "no such executable" in err


# ============================================================ 2. buildx builder

def test_missing_buildx_builder_names_the_symptom_it_actually_produces():
    """This one is nasty because it reads as a network outage. The message must say so."""
    c = preflight.check_buildx_builder(FakeRunner(HEALTHY), env(BUILDX_BUILDER=None))
    assert c.status == FAIL
    blob = " ".join(c.detail + c.fix)
    assert "403" in blob and "EOF" in blob
    assert "buildx create" in blob
    assert "export BUILDX_BUILDER=proxied" in blob


def test_nonexistent_builder_fails_and_suggests_listing_what_does_exist():
    runner = FakeRunner({"docker buildx inspect proxied":
                         (1, "", 'ERROR: no builder "proxied" found')})
    c = preflight.check_buildx_builder(runner, env())
    assert c.status == FAIL
    assert "does not exist" in c.summary
    assert any("buildx ls" in f for f in c.fix)


def test_existing_but_stopped_builder_warns_rather_than_blocks():
    runner = FakeRunner({"docker buildx inspect proxied":
                         (0, "Name: proxied\nStatus: inactive\n", "")})
    c = preflight.check_buildx_builder(runner, env())
    assert c.status == WARN
    assert any("--bootstrap" in f for f in c.fix)


def test_running_builder_passes():
    assert preflight.check_buildx_builder(FakeRunner(HEALTHY), env()).status == OK


# ============================================================ 3. base images

def test_base_image_list_is_derived_from_the_spec_not_retyped():
    assert preflight.base_images() == [spec.PYTHON_BASE_IMAGE]


def test_locally_present_base_image_needs_no_pull():
    runner = FakeRunner(HEALTHY)
    c = preflight.check_base_images(runner, env())
    assert c.status == OK
    assert not any(a[:2] == ["docker", "pull"] for a in runner.calls)


def test_absent_base_image_is_pulled_and_then_passes():
    runner = FakeRunner({
        f"docker image inspect {spec.PYTHON_BASE_IMAGE}": (1, "", "No such image"),
        f"docker pull {spec.PYTHON_BASE_IMAGE}": (0, "Status: Downloaded", ""),
    })
    c = preflight.check_base_images(runner, env())
    assert c.status == OK
    assert any(a[:2] == ["docker", "pull"] for a in runner.calls)


def test_unpullable_base_image_fails_and_points_at_the_builder_not_the_registry():
    """The observed failure mode: the pull error IS the builder defect, wearing a
    network error's clothes. Sending the operator to check their connection wastes the
    hour that the message could have saved."""
    runner = FakeRunner({
        f"docker image inspect {spec.PYTHON_BASE_IMAGE}": (1, "", "No such image"),
        f"docker pull {spec.PYTHON_BASE_IMAGE}":
            (1, "", "failed to resolve source metadata: EOF"),
    })
    c = preflight.check_base_images(runner, env())
    assert c.status == FAIL
    assert "BUILDX_BUILDER" in " ".join(c.fix)


def test_no_pull_reports_absence_without_fetching():
    runner = FakeRunner({f"docker image inspect {spec.PYTHON_BASE_IMAGE}":
                         (1, "", "No such image")})
    c = preflight.check_base_images(runner, env(), pull=False)
    assert c.status == FAIL
    assert not any(a[:2] == ["docker", "pull"] for a in runner.calls)


# ============================================================ 4. disk

def test_disk_check_fails_below_the_threshold_and_explains_the_consequence(tmp_path):
    c = preflight.check_disk_space(tmp_path, min_free_gb=10 ** 9)
    assert c.status == FAIL
    assert "loses the trials" in " ".join(c.detail)


def test_disk_check_passes_above_the_threshold(tmp_path):
    assert preflight.check_disk_space(tmp_path, min_free_gb=0.0001).status == OK


def test_disk_check_walks_up_to_an_existing_parent(tmp_path):
    """The job directory usually does not exist yet -- that is the normal case, not an
    error, and measuring the filesystem still has to work."""
    c = preflight.check_disk_space(tmp_path / "not" / "yet" / "created", min_free_gb=0.0001)
    assert c.status == OK


# ============================================================ 5. credentials

def _write_env_file(path: Path, text: str, mode: int = 0o600) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.parent.chmod(0o700)
    path.write_text(text, encoding="utf-8")
    path.chmod(mode)
    return path


def test_missing_credential_file_gives_the_four_commands_that_create_it(tmp_path):
    c = preflight.check_credentials({"DMAIC_ENV_FILE": str(tmp_path / "campaign.env"),
                                     "HOME": str(tmp_path)})
    assert c.status == FAIL
    fix = " ".join(c.fix)
    assert "chmod 600" in fix and "cp .env.example" in fix


def test_a_credential_file_in_the_wrong_config_dir_is_reported_as_a_near_miss(tmp_path):
    """"No credential file" and "your credential file is somewhere the loader does not
    read" are different problems with different fixes, and the second one looks exactly
    like the first from inside the loader."""
    home = tmp_path / "home"
    stray = home / preflight.NEAR_MISS_DIRS[0] / "campaign.env"
    _write_env_file(stray, "export A=1\n")
    c = preflight.check_credentials({"HOME": str(home)})
    assert c.status == FAIL
    blob = " ".join(c.detail)
    assert "does NOT read" in blob and str(stray) in blob


def test_world_readable_credential_file_is_a_finding_not_a_warning(tmp_path):
    p = _write_env_file(tmp_path / "campaign.env", "export A=1\n", mode=0o644)
    c = preflight.check_credentials({"DMAIC_ENV_FILE": str(p), "HOME": str(tmp_path)})
    assert c.status == FAIL
    assert "0644" in c.summary
    assert f"chmod 600 {p}" in c.fix


def test_mode_400_is_accepted(tmp_path):
    p = _write_env_file(tmp_path / "campaign.env", "export A=1\n", mode=0o400)
    c = preflight.check_credentials({"DMAIC_ENV_FILE": str(p), "HOME": str(tmp_path)})
    assert c.status == OK


def test_group_writable_directory_defeats_a_correct_file_mode(tmp_path):
    """0600 protects the contents. It does nothing about someone who can replace the
    file with their own."""
    p = _write_env_file(tmp_path / "d" / "campaign.env", "export A=1\n")
    p.parent.chmod(0o770)
    c = preflight.check_credentials({"DMAIC_ENV_FILE": str(p), "HOME": str(tmp_path)})
    assert c.status == FAIL
    assert "writable by others" in c.summary


def test_empty_credential_file_fails(tmp_path):
    p = _write_env_file(tmp_path / "campaign.env", "")
    c = preflight.check_credentials({"DMAIC_ENV_FILE": str(p), "HOME": str(tmp_path)})
    assert c.status == FAIL
    assert "empty" in c.summary


def test_declared_but_unfilled_variables_warn_and_name_only_the_variables(tmp_path):
    p = _write_env_file(tmp_path / "campaign.env",
                        'export FILLED_KEY="s3cr3t-value-abcdef"\nexport EMPTY_KEY=""\n')
    c = preflight.check_credentials({"DMAIC_ENV_FILE": str(p), "HOME": str(tmp_path)})
    assert c.status == WARN
    assert "EMPTY_KEY" in " ".join(c.detail)


# --- the property that matters most in this whole file ------------------------------

SECRET = "sk-do-not-print-me-0123456789abcdef"


def test_no_credential_value_reaches_any_field_of_any_check(tmp_path):
    """The credential check opens the file. Nothing it produces may contain a value.

    Asserted over the ENTIRE rendered report and the entire JSON form, not just the
    fields this test happens to think of -- a leak into a field nobody enumerated is
    exactly the leak that ships.
    """
    p = _write_env_file(tmp_path / "campaign.env",
                        f'export A_KEY="{SECRET}"\nexport B_KEY="{SECRET}xyz"\n')
    e = {"DMAIC_ENV_FILE": str(p), "HOME": str(tmp_path)}
    c = preflight.check_credentials(e)
    assert SECRET not in (c.summary + " ".join(c.detail) + " ".join(c.fix))
    assert SECRET not in str(c.to_dict())

    report = preflight.run_preflight(tmp_path, env=e, runner=FakeRunner(HEALTHY))
    assert SECRET not in report.render()
    assert SECRET not in str(report.to_dict())
    # ...and the names ARE reported, so the check is not passing by saying nothing.
    assert "A_KEY" in str(c.to_dict()) or c.status == OK


def test_scan_env_file_returns_names_and_emptiness_and_never_a_value(tmp_path):
    p = _write_env_file(tmp_path / "campaign.env",
                        "# a comment\n"
                        f'export FULL="{SECRET}"\n'
                        "export EMPTY=\n"
                        "BARE_ASSIGN=x\n"
                        "not an assignment\n")
    names, empty = preflight.scan_env_file(p)
    assert names == ["FULL", "EMPTY", "BARE_ASSIGN"]
    assert empty == ["EMPTY"]
    assert SECRET not in str(names) + str(empty)


# ============================================================ orchestration

def test_full_preflight_on_a_healthy_host_passes_and_exits_zero(tmp_path):
    sock = tmp_path / "s.sock"
    sock.touch()
    p = _write_env_file(tmp_path / "campaign.env", 'export A_KEY="filled-in-value"\n')
    report = preflight.run_preflight(
        tmp_path,
        env=env(DOCKER_HOST=f"unix://{sock}", HOME=str(tmp_path),
                DMAIC_ENV_FILE=str(p)),
        runner=FakeRunner(HEALTHY))
    assert report.ok, report.render()
    assert report.status == OK
    assert "PREFLIGHT PASSED" in report.render()


def test_full_preflight_on_the_host_that_lost_the_campaign_fails_loudly(tmp_path):
    """The exact starting state of the campaign that lost 364 trials: no runtime socket
    exported, no builder selected, no credential file."""
    report = preflight.run_preflight(
        tmp_path,
        env={"HOME": str(tmp_path / "empty-home")},
        runner=FakeRunner(HEALTHY))
    assert not report.ok
    text = report.render()
    assert "PREFLIGHT FAILED" in text
    assert "container-runtime" in text and "buildx-builder" in text
    assert "credentials" in text
    assert "Nothing was launched" in text
    for name in ("container-runtime", "buildx-builder", "credentials"):
        assert _named(report, name).fix, f"{name} failed without telling anyone how to fix it"


def test_every_failing_check_carries_a_fix(tmp_path):
    """A structural guarantee, not a spot check: no check may fail mutely."""
    report = preflight.run_preflight(tmp_path, env={"HOME": str(tmp_path / "nope")},
                                     runner=FakeRunner({}, present=("docker",)))
    for c in report.checks:
        if c.status == FAIL:
            assert c.fix, f"check {c.name} failed with no fix"


def test_checks_can_be_skipped_and_a_skip_is_visible(tmp_path):
    report = preflight.run_preflight(tmp_path, env=env(HOME=str(tmp_path)),
                                     runner=FakeRunner(HEALTHY),
                                     skip=("base-images", "credentials"))
    assert _named(report, "base-images").status == SKIP
    assert _named(report, "credentials").status == SKIP


def test_cli_exit_code_is_one_on_failure_and_json_is_machine_readable(tmp_path, capsys,
                                                                     monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "empty"))
    monkeypatch.delenv("DOCKER_HOST", raising=False)
    monkeypatch.delenv("BUILDX_BUILDER", raising=False)
    monkeypatch.delenv("DMAIC_ENV_FILE", raising=False)
    rc = preflight.main(["--jobs-dir", str(tmp_path), "--no-pull", "--json"])
    assert rc == 1
    import json
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False
    assert {c["name"] for c in payload["checks"]} == {
        "container-runtime", "buildx-builder", "base-images", "disk-space", "credentials"}


def test_resolution_order_matches_the_shell_loader(tmp_path):
    """One source of truth. If these drift, the preflight passes a file the launcher then
    refuses to source -- or the reverse, which is worse."""
    loader = (Path(__file__).resolve().parents[2] / "scripts" / "campaign-env.sh").read_text()
    assert preflight.ENV_FILE_VAR in loader
    assert preflight.DEFAULT_ENV_FILE_REL.replace(".config", "$HOME/.config", 1) in loader \
        or "/.config/dmaic/campaign.env" in loader
    assert preflight.resolve_env_file({"HOME": "/h"}) == Path("/h/.config/dmaic/campaign.env")
    assert preflight.resolve_env_file({"HOME": "/h", "DMAIC_ENV_FILE": "/x/y"}) == Path("/x/y")


def test_the_standalone_script_exists_and_is_executable():
    script = Path(__file__).resolve().parents[1] / "scripts" / "preflight.sh"
    assert script.is_file()
    assert os.stat(script).st_mode & stat.S_IXUSR


def test_the_launcher_runs_the_preflight_before_it_launches_anything():
    """The requirement is not "a preflight exists". It is "the thing that launches a
    campaign runs it"."""
    launcher = (Path(__file__).resolve().parents[1] / "scripts" / "launch-campaign.sh")
    text = launcher.read_text()
    assert os.stat(launcher).st_mode & stat.S_IXUSR
    i_pre = text.index("dmaic_harbor.preflight")
    i_run = text.index("dmaic_harbor.supervisor")
    assert i_pre < i_run, "the preflight must gate the launch, not follow it"
    assert "exit 2" in text[i_pre:i_run], "a failing preflight must stop the launch"
