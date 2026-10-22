"""Campaign supervisor: launch a job, and RESUME it rather than lose it.

WHY THIS EXISTS
---------------
Three of five jobs in the last campaign took ``SIGTERM`` and nothing restarted them. The
framework has a resume path (``harbor job resume -p <dir>``) and nothing called it, so the
trials those jobs had already paid for were simply abandoned. That is the third-largest
category of the 364 lost trials, and it is the cheapest to fix: the capability already
existed.

THE TWO RULES THAT MAKE THIS SAFE
---------------------------------
1. **Resume, never restart.** ``harbor run`` against a directory that already holds a job
   starts from zero and re-spends every completed trial. This supervisor therefore starts
   a job exactly once -- when the directory does not yet exist -- and every subsequent
   attempt is a resume. The check is on the presence of the job's own ``config.json``, so
   it survives the supervisor being killed too, and re-running the supervisor on a
   finished job is a no-op rather than a second campaign.
2. **Stop when the harness is broken.** If more than
   :data:`DEFAULT_ABORT_ERROR_RATE` of observed trials failed for harness reasons -- no
   verdict produced, a verifier crash, a trial-level exception -- the supervisor aborts
   the campaign instead of resuming into the same wall. On this project's own run history
   that, not model failure, is the realistic mode: a campaign burning budget against a
   broken harness should end, and end loudly.

WHAT COUNTS AS A HARNESS ERROR
------------------------------
Deliberately NOT "a low score". A trial is a harness error when it produced no verdict at
all, or produced one only because the verifier crashed and fell back to zeros:

* no ``verifier/reward.json``                       -- nothing scored it
* ``verifier/scorecard.json`` carries ``error``     -- the verifier crashed; the zeros in
  ``reward.json`` are a fallback, not a measurement
* ``result.json`` carries ``exception_info``        -- the trial itself failed

A model that genuinely scored 0.0 has a clean scorecard and is NOT counted here. Confusing
the two is the same defect this repository's aggregation had, and it would make the abort
threshold fire on a hard task set.
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

try:  # pragma: no cover
    from . import preflight as _preflight
except ImportError:  # pragma: no cover
    import preflight as _preflight  # type: ignore[no-redef]


#: Abort above this fraction of harness-errored trials.
DEFAULT_ABORT_ERROR_RATE = 0.20

#: ...but never on fewer than this many observed trials. Two failures out of three at the
#: start of a sweep is 67% and means nothing; the same rate over fifty trials is a broken
#: harness. Without a floor the abort is a coin flip on the first few trials.
DEFAULT_MIN_TRIALS_FOR_ABORT = 10

#: How many launches (one start + N resumes) before giving up. A job that dies repeatedly
#: is not being rescued by another resume.
DEFAULT_MAX_ATTEMPTS = 5

DEFAULT_BACKOFF_S = 30.0

#: Written into the job directory so a supervisor that is itself killed resumes its own
#: bookkeeping rather than starting a fresh count.
STATE_FILE = "supervisor-state.json"

STARTED, RESUMED = "start", "resume"

# Outcomes
DONE = "done"                 # the job finished cleanly
ABORTED_ERRORS = "aborted_error_rate"
ABORTED_ATTEMPTS = "aborted_max_attempts"
ABORTED_PREFLIGHT = "aborted_preflight"
ABORTED_SIGNAL = "aborted_signal"


# --------------------------------------------------------------------------- trial census

@dataclass
class Census:
    """What the job directory says has actually happened so far."""
    total: int = 0
    scored: int = 0
    harness_errors: int = 0
    kinds: dict = field(default_factory=dict)

    @property
    def error_rate(self) -> float:
        return (self.harness_errors / self.total) if self.total else 0.0

    def to_dict(self) -> dict:
        return {"total": self.total, "scored": self.scored,
                "harness_errors": self.harness_errors,
                "error_rate": round(self.error_rate, 4), "kinds": dict(self.kinds)}


def _is_trial_dir(path: Path) -> bool:
    """A trial directory, not the job directory that contains them.

    Both carry a ``config.json``; only a trial carries a ``trial.log``. Getting this wrong
    counts the job as a trial and shifts every rate by one.
    """
    return (path / "config.json").is_file() and (path / "trial.log").exists()


def classify_trial(trial: Path) -> str:
    """``scored`` | ``no_reward`` | ``verifier_error`` | ``trial_exception``."""
    result = trial / "result.json"
    if result.is_file():
        try:
            if (json.loads(result.read_text(encoding="utf-8")) or {}).get("exception_info"):
                return "trial_exception"
        except (OSError, ValueError):
            pass
    if (trial / "exception.txt").exists():
        return "trial_exception"

    reward = trial / "verifier" / "reward.json"
    if not reward.is_file():
        return "no_reward"

    card = trial / "verifier" / "scorecard.json"
    if card.is_file():
        try:
            data = json.loads(card.read_text(encoding="utf-8")) or {}
        except (OSError, ValueError):
            return "verifier_error"
        if data.get("error"):
            return "verifier_error"
        warnings = ((data.get("validation") or {}).get("warnings") or [])
        if isinstance(warnings, list) and "verifier_error" in warnings:
            return "verifier_error"
    return "scored"


def census(job_dir: Path) -> Census:
    c = Census()
    if not job_dir.is_dir():
        return c
    for cfg in sorted(job_dir.rglob("config.json")):
        trial = cfg.parent
        if not _is_trial_dir(trial):
            continue
        kind = classify_trial(trial)
        c.total += 1
        c.kinds[kind] = c.kinds.get(kind, 0) + 1
        if kind == "scored":
            c.scored += 1
        else:
            c.harness_errors += 1
    return c


# --------------------------------------------------------------------------- state

def load_state(job_dir: Path) -> dict:
    path = job_dir / STATE_FILE
    if not path.is_file():
        return {"attempts": [], "outcome": None}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"attempts": [], "outcome": None}


def save_state(job_dir: Path, state: dict) -> None:
    try:
        job_dir.mkdir(parents=True, exist_ok=True)
        tmp = job_dir / (STATE_FILE + ".tmp")
        tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
        os.replace(tmp, job_dir / STATE_FILE)
    except OSError as exc:  # pragma: no cover - defensive
        print(f"[supervisor] could not persist state: {exc}", file=sys.stderr)


def job_started(job_dir: Path) -> bool:
    """Has this job already been launched? Decides start-vs-resume, and MUST NOT be
    relaxed: the answer determines whether completed trials get re-spent."""
    return (job_dir / "config.json").is_file()


def job_complete(job_dir: Path) -> bool:
    """Harbor writes ``finished_at`` into the job's ``result.json`` when it completes."""
    result = job_dir / "result.json"
    if not result.is_file():
        return False
    try:
        data = json.loads(result.read_text(encoding="utf-8")) or {}
    except (OSError, ValueError):
        return False
    if not data.get("finished_at"):
        return False
    stats = data.get("stats") or {}
    return not (stats.get("n_running_trials") or stats.get("n_pending_trials"))


# --------------------------------------------------------------------------- runner

class JobRunner:
    """Runs the framework CLI. Injectable so the supervisor's whole control flow --
    every kill, every resume, every abort -- is tested without launching a container."""

    def __init__(self, harbor_bin: str = "harbor", env: dict | None = None):
        self.harbor_bin = harbor_bin
        self.env = env

    def start(self, config_path: str, extra: list[str]) -> int:
        return self._run([self.harbor_bin, "run", "-c", config_path, *extra])

    def resume(self, job_dir: str, extra: list[str]) -> int:
        return self._run([self.harbor_bin, "job", "resume", "-p", job_dir, *extra])

    def _run(self, argv: list[str]) -> int:
        print(f"[supervisor] $ {' '.join(argv)}", flush=True)
        try:
            return subprocess.call(argv, env=self.env)
        except FileNotFoundError:
            print(f"[supervisor] no such executable: {argv[0]}", file=sys.stderr)
            return 127


def _describe_exit(rc: int) -> str:
    """A negative return code is death by signal; that is the case this exists for."""
    if rc < 0:
        try:
            name = signal.Signals(-rc).name
        except ValueError:  # pragma: no cover - exotic signal
            name = f"signal {-rc}"
        return f"killed by {name}"
    if rc == 0:
        return "exited cleanly"
    return f"exited {rc}"


# --------------------------------------------------------------------------- supervise

@dataclass
class Outcome:
    outcome: str
    attempts: int
    census: Census
    detail: str = ""

    @property
    def exit_code(self) -> int:
        return 0 if self.outcome == DONE else 1

    def to_dict(self) -> dict:
        return {"outcome": self.outcome, "attempts": self.attempts,
                "census": self.census.to_dict(), "detail": self.detail}


def supervise(config_path: str, job_dir: str | Path, *,
              runner: JobRunner | None = None,
              max_attempts: int = DEFAULT_MAX_ATTEMPTS,
              abort_error_rate: float = DEFAULT_ABORT_ERROR_RATE,
              min_trials_for_abort: int = DEFAULT_MIN_TRIALS_FOR_ABORT,
              backoff_s: float = DEFAULT_BACKOFF_S,
              extra_args: list[str] | None = None,
              sleep=time.sleep,
              on_event=None) -> Outcome:
    """Launch or resume until the job completes, the harness proves broken, or we give up.

    Idempotent by construction: with the job already complete this returns ``done``
    without launching anything, and it never issues ``run`` against a directory that
    already holds a job.
    """
    job_dir = Path(job_dir)
    runner = runner or JobRunner()
    extra = list(extra_args or [])
    state = load_state(job_dir)
    emit = on_event or (lambda kind, payload: None)

    def _finish(outcome: str, detail: str = "") -> Outcome:
        c = census(job_dir)
        state["outcome"] = outcome
        state["detail"] = detail
        state["census"] = c.to_dict()
        save_state(job_dir, state)
        emit(outcome, {"detail": detail, "census": c.to_dict()})
        return Outcome(outcome, len(state.get("attempts", [])), c, detail)

    if job_started(job_dir) and job_complete(job_dir):
        return _finish(DONE, "job was already complete; nothing relaunched")

    while True:
        prior = len(state.get("attempts", []))
        if prior >= max_attempts:
            return _finish(ABORTED_ATTEMPTS,
                           f"{prior} launches without completing; not resuming again")

        mode = RESUMED if job_started(job_dir) else STARTED
        emit("launch", {"mode": mode, "attempt": prior + 1})
        started_at = time.time()
        rc = (runner.resume(str(job_dir), extra) if mode == RESUMED
              else runner.start(config_path, extra))
        c = census(job_dir)
        record = {"mode": mode, "rc": rc, "exit": _describe_exit(rc),
                  "seconds": round(time.time() - started_at, 1),
                  "census": c.to_dict()}
        state.setdefault("attempts", []).append(record)
        save_state(job_dir, state)
        emit("attempt", record)
        print(f"[supervisor] {mode} {_describe_exit(rc)}; "
              f"{c.scored} scored / {c.harness_errors} harness errors "
              f"of {c.total} trials ({c.error_rate:.1%})", flush=True)

        # The abort is checked after EVERY attempt, including a clean one: a job can
        # complete while quietly producing nothing but harness errors, and publishing that
        # as a leaderboard is worse than not finishing.
        if c.total >= min_trials_for_abort and c.error_rate > abort_error_rate:
            return _finish(
                ABORTED_ERRORS,
                f"harness error rate {c.error_rate:.1%} over {c.total} trials exceeds "
                f"the {abort_error_rate:.0%} ceiling ({c.kinds}). This is a broken "
                f"harness, not a hard task set -- a trial that produced no verdict is a "
                f"missing observation, and resuming into it only spends more.")

        if rc == 0 and job_complete(job_dir):
            return _finish(DONE)
        if rc == 0 and not job_complete(job_dir):
            # A clean exit that left the job unfinished is exactly the shape a swallowed
            # cancellation takes. Resume; do not treat rc 0 as proof of completion.
            print("[supervisor] clean exit but job is not complete; resuming", flush=True)

        if len(state["attempts"]) >= max_attempts:
            return _finish(ABORTED_ATTEMPTS,
                           f"{len(state['attempts'])} launches without completing")
        sleep(backoff_s)


# --------------------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="dmaic-harbor-supervise",
        description="Launch a campaign job, resume it when it dies, and abort it when the "
                    "harness -- not the model -- is what is failing.")
    ap.add_argument("-c", "--config", required=True, help="job config passed to `harbor run`")
    ap.add_argument("-p", "--job-dir", required=True,
                    help="the job directory: `<jobs_dir>/<job_name>` from that config")
    ap.add_argument("--max-attempts", type=int, default=DEFAULT_MAX_ATTEMPTS)
    ap.add_argument("--abort-error-rate", type=float, default=DEFAULT_ABORT_ERROR_RATE)
    ap.add_argument("--min-trials-for-abort", type=int, default=DEFAULT_MIN_TRIALS_FOR_ABORT)
    ap.add_argument("--backoff", type=float, default=DEFAULT_BACKOFF_S)
    ap.add_argument("--harbor-bin", default=os.environ.get("HARBOR_BIN", "harbor"))
    ap.add_argument("--skip-preflight", action="store_true",
                    help="do not run the host preflight first (not recommended)")
    ap.add_argument("--no-pull", action="store_true",
                    help="preflight: do not fetch a missing base image")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("rest", nargs=argparse.REMAINDER,
                    help="extra arguments passed through after `--`")
    a = ap.parse_args(argv)

    extra = [x for x in a.rest if x != "--"]

    if not a.skip_preflight:
        report = _preflight.run_preflight(Path(a.job_dir).parent, pull=not a.no_pull)
        print(report.render(color=sys.stdout.isatty()))
        if not report.ok:
            out = Outcome(ABORTED_PREFLIGHT, 0, census(Path(a.job_dir)),
                          "preflight failed; nothing launched")
            if a.json:
                print(json.dumps(out.to_dict(), indent=2))
            return 2

    outcome = supervise(a.config, a.job_dir, runner=JobRunner(harbor_bin=a.harbor_bin),
                        max_attempts=a.max_attempts,
                        abort_error_rate=a.abort_error_rate,
                        min_trials_for_abort=a.min_trials_for_abort,
                        backoff_s=a.backoff, extra_args=extra)
    if a.json:
        print(json.dumps(outcome.to_dict(), indent=2))
    else:
        print(f"\n[supervisor] {outcome.outcome}: {outcome.detail or 'ok'}")
        print(f"[supervisor] {outcome.census.to_dict()}")
    return outcome.exit_code


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
