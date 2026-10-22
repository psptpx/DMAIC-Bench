"""The campaign supervisor: resume rather than lose, and stop when the harness is broken.

The framework CLI is injected, so every control path -- a job killed by SIGTERM, a job
that exits cleanly without finishing, a harness failing at 40%, a supervisor that is
itself killed and restarted -- is exercised here without launching a container or
spending anything. Those are the paths that matter: the last campaign's loss was not a
subtle scheduling bug, it was that nothing called resume at all.
"""
from __future__ import annotations

import json
import signal
from pathlib import Path

import pytest

from dmaic_harbor import supervisor
from dmaic_harbor.supervisor import (ABORTED_ATTEMPTS, ABORTED_ERRORS, DONE, RESUMED,
                                     STARTED)


# --------------------------------------------------------------------------- fixtures

def make_trial(job_dir: Path, name: str, *, kind: str = "scored",
               reward: float = 0.75, tokens: tuple = (1000, 200),
               model: str = "contestant-a", task: str = "task-1") -> Path:
    """One trial directory in the shape the framework writes them.

    ``kind`` selects which of the four real outcomes to reproduce, including the one this
    whole exercise is about: a verifier that crashed and wrote zeros with an error marker.
    """
    trial = job_dir / name
    (trial / "verifier").mkdir(parents=True, exist_ok=True)
    (trial / "trial.log").write_text("log\n", encoding="utf-8")
    (trial / "config.json").write_text(json.dumps(
        {"agent": {"name": "terminus-2", "model_name": model},
         "task": {"path": f"/datasets/dmaic-bench/{task}"}}), encoding="utf-8")

    result = {"started_at": "2026-09-04T10:00:00", "finished_at": "2026-09-04T10:10:00",
              "agent_info": {"name": "terminus-2", "model_name": model},
              "agent_result": {"n_input_tokens": tokens[0], "n_output_tokens": tokens[1]},
              "exception_info": None}

    if kind == "trial_exception":
        result["exception_info"] = {"exception_type": "TimeoutError"}
        (trial / "result.json").write_text(json.dumps(result), encoding="utf-8")
        return trial

    (trial / "result.json").write_text(json.dumps(result), encoding="utf-8")

    if kind == "no_reward":
        return trial

    if kind == "verifier_error":
        # THE case: `reward.json` full of zeros that is a crash fallback, not a score.
        (trial / "verifier" / "reward.json").write_text(
            json.dumps({"reward": 0.0, "competence": 0.0, "ms_recall": 0.0, "nf": 0.0,
                        "pq": 0.0}), encoding="utf-8")
        (trial / "verifier" / "scorecard.json").write_text(json.dumps(
            {"schema": "dmaic-harbor-scorecard/v1",
             "error": "ValueError: truth package is malformed",
             "traceback": "...",
             "validation": {"warnings": ["verifier_error"]}}), encoding="utf-8")
        return trial

    (trial / "verifier" / "reward.json").write_text(
        json.dumps({"reward": reward, "competence": reward, "ms_recall": reward,
                    "nf": 1.0, "pq": 1.0, "hn_fabrication_rate": 0.0, "ae_turns": 9}),
        encoding="utf-8")
    (trial / "verifier" / "scorecard.json").write_text(
        json.dumps({"schema": "dmaic-harbor-scorecard/v1", "task_id": task,
                    "validation": {"warnings": []}}), encoding="utf-8")
    return trial


def mark_job(job_dir: Path, *, started: bool = True, finished: bool = False,
             running: int = 0, pending: int = 0) -> None:
    job_dir.mkdir(parents=True, exist_ok=True)
    if started:
        (job_dir / "config.json").write_text(json.dumps({"job_name": "j"}), encoding="utf-8")
    result = {"started_at": "2026-09-04T10:00:00",
              "stats": {"n_running_trials": running, "n_pending_trials": pending}}
    if finished:
        result["finished_at"] = "2026-09-04T12:00:00"
    (job_dir / "result.json").write_text(json.dumps(result), encoding="utf-8")


class ScriptedRunner(supervisor.JobRunner):
    """A framework CLI whose every invocation is scripted, with a side effect per call.

    ``script`` is a list of ``(return_code, effect)``; ``effect`` receives the job dir, so
    a test can say "this launch produced four trials and was then killed".
    """

    def __init__(self, job_dir: Path, script: list):
        super().__init__(harbor_bin="does-not-exist")
        self.job_dir = job_dir
        self.script = list(script)
        self.calls: list = []

    def _next(self, mode: str) -> int:
        self.calls.append(mode)
        if not self.script:
            return 0
        rc, effect = self.script.pop(0)
        if effect:
            effect(self.job_dir)
        return rc

    def start(self, config_path, extra):
        return self._next(STARTED)

    def resume(self, job_dir, extra):
        return self._next(RESUMED)


def nosleep(_s):
    return None


# ============================================================ start vs resume

def test_a_fresh_job_is_started_once_and_then_only_ever_resumed(tmp_path):
    """`harbor run` against an existing job directory restarts from zero and re-spends
    every completed trial. Exactly one `start` may ever be issued."""
    job = tmp_path / "job"

    def first(d):
        mark_job(d, started=True)
        for i in range(4):
            make_trial(d, f"t{i}")

    def then_finish(d):
        for i in range(4, 8):
            make_trial(d, f"t{i}")
        mark_job(d, started=True, finished=True)

    runner = ScriptedRunner(job, [(-signal.SIGTERM, first), (0, then_finish)])
    out = supervisor.supervise("job.yaml", job, runner=runner, sleep=nosleep)

    assert runner.calls == [STARTED, RESUMED]
    assert out.outcome == DONE
    assert out.census.total == 8 and out.census.harness_errors == 0


def test_a_job_killed_by_sigterm_is_resumed_not_restarted(tmp_path):
    """The literal failure: three of five jobs took SIGTERM and nothing restarted them."""
    job = tmp_path / "job"

    def killed(d):
        mark_job(d, started=True)
        for i in range(3):
            make_trial(d, f"t{i}")

    runner = ScriptedRunner(job, [
        (-signal.SIGTERM, killed),
        (-signal.SIGTERM, lambda d: [make_trial(d, f"u{i}") for i in range(3)]),
        (0, lambda d: mark_job(d, started=True, finished=True)),
    ])
    out = supervisor.supervise("job.yaml", job, runner=runner, sleep=nosleep)
    assert runner.calls == [STARTED, RESUMED, RESUMED]
    assert out.outcome == DONE
    assert supervisor._describe_exit(-signal.SIGTERM) == "killed by SIGTERM"


def test_an_existing_job_directory_is_resumed_even_on_the_first_supervisor_launch(tmp_path):
    """The supervisor itself may be the thing that died. Restarting it must not restart
    the campaign."""
    job = tmp_path / "job"
    mark_job(job, started=True)
    for i in range(5):
        make_trial(job, f"t{i}")
    runner = ScriptedRunner(job, [(0, lambda d: mark_job(d, started=True, finished=True))])
    out = supervisor.supervise("job.yaml", job, runner=runner, sleep=nosleep)
    assert runner.calls == [RESUMED]
    assert out.outcome == DONE


def test_supervising_an_already_complete_job_launches_nothing(tmp_path):
    """Idempotence: re-running the supervisor on a finished campaign is a no-op, not a
    second campaign."""
    job = tmp_path / "job"
    mark_job(job, started=True, finished=True)
    for i in range(6):
        make_trial(job, f"t{i}")
    runner = ScriptedRunner(job, [(0, None)])
    out = supervisor.supervise("job.yaml", job, runner=runner, sleep=nosleep)
    assert runner.calls == []
    assert out.outcome == DONE
    assert "already complete" in out.detail


def test_completed_trials_are_never_recounted_across_resumes(tmp_path):
    """The census is derived from the directory, so a resume that adds nothing adds
    nothing -- there is no running tally to double."""
    job = tmp_path / "job"
    mark_job(job, started=True)
    for i in range(4):
        make_trial(job, f"t{i}")
    before = supervisor.census(job)
    runner = ScriptedRunner(job, [(0, lambda d: mark_job(d, started=True, finished=True))])
    out = supervisor.supervise("job.yaml", job, runner=runner, sleep=nosleep)
    assert (before.total, out.census.total) == (4, 4)


def test_a_clean_exit_that_left_the_job_unfinished_is_resumed(tmp_path):
    """A swallowed cancellation exits 0. Treating rc 0 as proof of completion is how a
    half-finished job gets published as a finished one."""
    job = tmp_path / "job"
    runner = ScriptedRunner(job, [
        (0, lambda d: (mark_job(d, started=True), [make_trial(d, f"t{i}") for i in range(3)])),
        (0, lambda d: mark_job(d, started=True, finished=True)),
    ])
    out = supervisor.supervise("job.yaml", job, runner=runner, sleep=nosleep)
    assert runner.calls == [STARTED, RESUMED]
    assert out.outcome == DONE


def test_a_job_still_running_trials_is_not_treated_as_complete(tmp_path):
    job = tmp_path / "job"
    mark_job(job, started=True, finished=True, running=2)
    assert supervisor.job_complete(job) is False


def test_giving_up_after_max_attempts(tmp_path):
    job = tmp_path / "job"
    runner = ScriptedRunner(job, [(-signal.SIGKILL, lambda d: mark_job(d, started=True))] * 10)
    out = supervisor.supervise("job.yaml", job, runner=runner, max_attempts=3,
                               sleep=nosleep)
    assert out.outcome == ABORTED_ATTEMPTS
    assert len(runner.calls) == 3
    assert out.exit_code == 1


# ============================================================ the hard abort

def test_a_harness_error_rate_above_the_ceiling_aborts_the_campaign(tmp_path):
    """On this project's own history a broken harness, not model failure, is the realistic
    mode. A campaign burning budget against one should end."""
    job = tmp_path / "job"

    def broken(d):
        mark_job(d, started=True)
        for i in range(12):
            make_trial(d, f"ok{i}")
        for i in range(8):                       # 8/20 = 40%
            make_trial(d, f"bad{i}", kind="no_reward")

    runner = ScriptedRunner(job, [(-signal.SIGTERM, broken)] * 5)
    out = supervisor.supervise("job.yaml", job, runner=runner, sleep=nosleep)
    assert out.outcome == ABORTED_ERRORS
    assert len(runner.calls) == 1, "aborting means not resuming into the same wall"
    assert "40.0%" in out.detail and "20%" in out.detail


def test_the_abort_fires_on_a_verifier_crash_rate_too_not_only_on_missing_rewards(tmp_path):
    """A crashing verifier writes a `reward.json`. Counting only missing ones would miss
    the failure mode that is hardest to see."""
    job = tmp_path / "job"

    def crashing(d):
        mark_job(d, started=True)
        for i in range(10):
            make_trial(d, f"ok{i}")
        for i in range(10):
            make_trial(d, f"crash{i}", kind="verifier_error")

    runner = ScriptedRunner(job, [(-signal.SIGTERM, crashing)] * 3)
    out = supervisor.supervise("job.yaml", job, runner=runner, sleep=nosleep)
    assert out.outcome == ABORTED_ERRORS
    assert out.census.kinds["verifier_error"] == 10


def test_a_genuinely_hard_task_set_does_not_trip_the_abort(tmp_path):
    """Every trial scoring 0.0 is a RESULT. Confusing it with a harness failure would make
    the abort fire on exactly the task sets the benchmark is for."""
    job = tmp_path / "job"

    def all_zero(d):
        mark_job(d, started=True, finished=True)
        for i in range(30):
            make_trial(d, f"z{i}", reward=0.0)

    runner = ScriptedRunner(job, [(0, all_zero)])
    out = supervisor.supervise("job.yaml", job, runner=runner, sleep=nosleep)
    assert out.outcome == DONE
    assert out.census.harness_errors == 0 and out.census.error_rate == 0.0


def test_the_abort_will_not_fire_on_a_handful_of_early_trials(tmp_path):
    """Two failures out of three is 67% and means nothing. Without a floor the abort is a
    coin flip on the first few trials of every campaign."""
    job = tmp_path / "job"

    def early(d):
        mark_job(d, started=True, finished=True)
        make_trial(d, "a")
        make_trial(d, "b", kind="no_reward")
        make_trial(d, "c", kind="no_reward")

    runner = ScriptedRunner(job, [(0, early)])
    out = supervisor.supervise("job.yaml", job, runner=runner, sleep=nosleep)
    assert out.census.error_rate > 0.6
    assert out.outcome == DONE, "aborted on 3 trials"


def test_the_abort_also_fires_on_a_job_that_completed_badly(tmp_path):
    """A job can finish while producing nothing but harness errors. Publishing that is
    worse than not finishing."""
    job = tmp_path / "job"

    def finished_but_broken(d):
        mark_job(d, started=True, finished=True)
        for i in range(4):
            make_trial(d, f"ok{i}")
        for i in range(16):
            make_trial(d, f"bad{i}", kind="trial_exception")

    runner = ScriptedRunner(job, [(0, finished_but_broken)])
    out = supervisor.supervise("job.yaml", job, runner=runner, sleep=nosleep)
    assert out.outcome == ABORTED_ERRORS


def test_the_ceiling_is_configurable(tmp_path):
    """The same 5% error rate must abort under a 1% ceiling and pass under a 10% one.

    Each arm gets its OWN job directory: run them against a shared one and the second
    arm short-circuits on `already complete`, which passes without testing the ceiling
    at all.
    """
    def mild(d):
        mark_job(d, started=True, finished=True)
        for i in range(19):
            make_trial(d, f"ok{i}")
        make_trial(d, "bad", kind="no_reward")          # 1/20 = 5%

    strict = tmp_path / "strict"
    assert supervisor.supervise("job.yaml", strict, sleep=nosleep, abort_error_rate=0.01,
                                runner=ScriptedRunner(strict, [(0, mild)])
                                ).outcome == ABORTED_ERRORS

    lenient = tmp_path / "lenient"
    out = supervisor.supervise("job.yaml", lenient, sleep=nosleep, abort_error_rate=0.10,
                               runner=ScriptedRunner(lenient, [(0, mild)]))
    assert out.outcome == DONE
    assert out.census.error_rate == pytest.approx(0.05)


# ============================================================ classification

@pytest.mark.parametrize("kind", ["scored", "no_reward", "verifier_error", "trial_exception"])
def test_classify_trial_round_trips_every_outcome(tmp_path, kind):
    trial = make_trial(tmp_path / "job", "t", kind=kind)
    assert supervisor.classify_trial(trial) == kind


def test_a_zero_score_with_a_clean_scorecard_is_scored_not_an_error(tmp_path):
    trial = make_trial(tmp_path / "job", "t", reward=0.0)
    assert supervisor.classify_trial(trial) == "scored"


def test_a_scorecard_that_will_not_parse_is_treated_as_a_verifier_error(tmp_path):
    """Fail closed. An unreadable verdict is not a verdict, and calling it one publishes
    whatever zeros happen to be beside it."""
    trial = make_trial(tmp_path / "job", "t")
    (trial / "verifier" / "scorecard.json").write_text("{truncated", encoding="utf-8")
    assert supervisor.classify_trial(trial) == "verifier_error"


def test_the_job_directory_itself_is_not_counted_as_a_trial(tmp_path):
    """Both carry a config.json; only a trial carries a trial.log. Getting this wrong
    shifts every rate by one."""
    job = tmp_path / "job"
    mark_job(job, started=True)
    for i in range(4):
        make_trial(job, f"t{i}")
    assert supervisor.census(job).total == 4


def test_census_of_an_absent_directory_is_empty_not_an_error(tmp_path):
    assert supervisor.census(tmp_path / "never-created").total == 0


# ============================================================ state

def test_state_survives_the_supervisor_being_killed(tmp_path):
    """The attempt budget must not reset every time the supervisor is restarted, or a
    crash-looping job is resumed forever."""
    job = tmp_path / "job"
    runner = ScriptedRunner(job, [(-signal.SIGKILL, lambda d: mark_job(d, started=True))] * 2)
    supervisor.supervise("job.yaml", job, runner=runner, max_attempts=2, sleep=nosleep)

    state = supervisor.load_state(job)
    assert len(state["attempts"]) == 2
    assert state["attempts"][0]["mode"] == STARTED
    assert "killed by SIGKILL" in state["attempts"][0]["exit"]

    runner2 = ScriptedRunner(job, [(0, None)])
    out = supervisor.supervise("job.yaml", job, runner=runner2, max_attempts=2,
                               sleep=nosleep)
    assert out.outcome == ABORTED_ATTEMPTS
    assert runner2.calls == [], "the budget carried over; nothing relaunched"


def test_a_corrupt_state_file_does_not_stop_the_supervisor(tmp_path):
    job = tmp_path / "job"
    job.mkdir()
    (job / supervisor.STATE_FILE).write_text("{ truncated", encoding="utf-8")
    assert supervisor.load_state(job) == {"attempts": [], "outcome": None}


def test_events_are_emitted_for_each_launch(tmp_path):
    job = tmp_path / "job"
    events: list = []
    runner = ScriptedRunner(job, [
        (-signal.SIGTERM, lambda d: mark_job(d, started=True)),
        (0, lambda d: mark_job(d, started=True, finished=True)),
    ])
    supervisor.supervise("job.yaml", job, runner=runner, sleep=nosleep,
                         on_event=lambda kind, payload: events.append(kind))
    assert events.count("launch") == 2 and events[-1] == DONE


def test_a_missing_framework_binary_is_a_return_code_not_a_crash(tmp_path):
    rc = supervisor.JobRunner(harbor_bin="definitely-not-a-real-binary-xyz").resume(
        str(tmp_path), [])
    assert rc == 127


# ============================================================ CLI

def test_the_cli_refuses_to_launch_when_the_preflight_fails(tmp_path, monkeypatch, capsys):
    """The preflight must gate the launch. A supervisor that starts a campaign on a host
    that cannot build an image has reproduced the original failure with extra steps."""
    monkeypatch.setenv("HOME", str(tmp_path / "empty"))
    monkeypatch.delenv("DOCKER_HOST", raising=False)
    monkeypatch.delenv("BUILDX_BUILDER", raising=False)
    monkeypatch.delenv("DMAIC_ENV_FILE", raising=False)
    launched: list = []
    monkeypatch.setattr(supervisor, "supervise",
                        lambda *a, **k: launched.append(a) or None)
    rc = supervisor.main(["-c", "job.yaml", "-p", str(tmp_path / "job"), "--no-pull"])
    assert rc == 2
    assert launched == [], "the campaign was launched despite a failed preflight"
    assert "PREFLIGHT FAILED" in capsys.readouterr().out
