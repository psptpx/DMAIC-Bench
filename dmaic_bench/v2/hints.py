"""Hint probes: telling a hard task from a broken one, causally.

A task no system solves is ambiguous, and the ambiguity is not academic. This benchmark shipped
nine tasks that every model floored at 0.000 beside ms_recall 1.000, reported them as difficulty,
and they were unscoreable — the verifier compared a private node key nobody could produce. It
took an offline re-score to find, after a campaign had been paid for.

The hint approach is the instrument that separates the two cases while the campaign is running.
Take a failed trajectory, form a hypothesis about the root cause, phrase a hint that addresses
that cause, rerun, and read the outcome:

    a calibrated hint lets the agent past the point it failed at
        -> the failure mode is real and causally confirmed: a capability gap
    a calibrated hint changes nothing, or only an over-specified one works
        -> a broken environment, a false negative, or a task solvable only when handed the answer

**Partial success still validates.** The agent may clear the previously-failing step and then
fail later. That confirms the mode; finishing the task is not required.

## Calibration

The value of a hint is entirely in its altitude, and the band is narrow:

* **over-specified** — the hint contains the answer. It proves the agent can transcribe, and it
  destroys the causal signal: you can no longer tell whether it overcame its own limitation.
* **under-specified** — the hint is too generic to change behaviour, so the mode stays
  unconfirmed and you have learned nothing.
* **calibrated** — it names the DIMENSION the agent must attend to, and stops short of naming
  what it will find there.

Rather than ship one hint per probe and argue about where it sits, each probe here ships three
rungs, and the outer two are CONTROLS in the same sense that nop and oracle bound the reward
scale:

    L0  deliberately under-specified   if this alone works, the failure was inattention
    L1  the calibrated hint            the one the finding rests on
    L2  deliberately over-specified    if ONLY this works, suspect a knowledge gap or a defect

A result is only quotable as "mode confirmed" when L1 moves the agent past the failure point and
L0 does not. L2 is never reported as a resolve.
"""
from __future__ import annotations

import re

#: Probe ids are opaque on purpose: the id reaches the agent inside the task identifier, and a
#: descriptive one would be a hint of its own.
PROBES = {
    "hp01": {
        "targets": (("adb_c30", 4), ("adb_c30", 5), ("adb_c31", 3), ("adb_c31", 4)),
        "failure_mode": "route_wrong_branch",
        "point": "M_msa",
        "observation": (
            "Twelve trials across three frontier models, twelve zeros. Each one computed the "
            "percentage of study variation, saw a number below 30, and proceeded to a "
            "capability index it had no basis for. The oracle scores 1.000 on all four through "
            "the behaviour-based route, and both admissible conventions agree the gauge fails, "
            "so the task is not known to be broken -- but 'not known to be broken' is not "
            "evidence, and until this probe runs the four tasks carry difficulty and no "
            "demonstrated discrimination."),
        "hypothesis": (
            "The contestant applies ONE remembered acceptance criterion and stops checking. It "
            "is not that it cannot compute the second quantity; it is that reaching a familiar "
            "threshold ends the enquiry."),
        "rungs": {
            "L0": "Take care over the measurement study before you rely on the readings.",
            "L1": ("A measurement system is not judged acceptable on a single number. Before "
                   "you rely on these readings for anything downstream, satisfy yourself that "
                   "the study has answered every question the standard asks of a gauge, not "
                   "only the first one that comes to mind."),
            "L2": ("Work out how many distinct groups this gauge can tell apart across the "
                   "spread of the parts. If that count is below five the gauge cannot be used "
                   "to control the process, whatever its percentage of study variation says."),
        },
        "rationale": {
            "L0": ("Names no dimension -- 'take care' is an exhortation, and the agent was "
                   "already taking care. Included as the under-specified control: if this moves "
                   "the agent, the failure was inattention rather than a missing criterion, and "
                   "the L1 finding would not mean what it claims."),
            "L1": ("Names the dimension -- criterion COMPLETENESS -- and stops there. It does "
                   "not say which criterion is missing, what quantity answers it, what its "
                   "threshold is, or which way this gauge will come out. An agent that knows "
                   "the standard can act on it; one that does not still has to find it. This "
                   "is the same altitude as 'make sure you explore all the relevant code files "
                   "before writing the patch': the class of thing to attend to, not the place "
                   "the answer is."),
            "L2": ("Hands over the quantity and its threshold, so it proves only transcription. "
                   "Included as the over-specified control: a task that passes ONLY here is a "
                   "task solvable when handed the answer, which is a defect signal, not a "
                   "result."),
        },
    },
}

RUNGS = ("L0", "L1", "L2")

#: A run under L2 is never a resolve. Stated here so an analysis cannot quietly pool it.
REPORTABLE_RUNGS = ("L0", "L1")


def probe_for(case_id: str, seed: int):
    """``(probe_id, probe)`` for a task that has one, else ``(None, None)``."""
    for probe_id, probe in PROBES.items():
        if (case_id, int(seed)) in probe["targets"]:
            return probe_id, probe
    return None, None


def hint_text(probe_id: str, rung: str) -> str:
    rung = rung.upper()
    if probe_id not in PROBES:
        raise KeyError(f"unknown hint probe {probe_id!r}")
    if rung not in RUNGS:
        raise KeyError(f"unknown rung {rung!r}; expected one of {RUNGS}")
    return PROBES[probe_id]["rungs"][rung]


def suffix(probe_id: str, rung: str) -> str:
    """The task-id tail for a hinted instance. Opaque, so it leaks nothing by being read."""
    return f"{probe_id}{rung.lower()}"


# --------------------------------------------------------------------------- the giveaway guard

def _renderings(value) -> set:
    try:
        f = float(value)
    except (TypeError, ValueError):
        return set()
    out = set()
    for scale in (1.0, 100.0):
        g = f * scale
        for places in (0, 1, 2, 3, 4):
            s = "%.*f" % (places, g)
            out.add(s)
            if "." in s:
                out.add(s.rstrip("0").rstrip("."))
    # No length floor. A single digit is exactly the shape of the answer here -- the number of
    # distinct categories is 4 -- and dropping short renderings to reduce noise let the one
    # value the probe exists around through the guard. Matching is word-bounded instead, so "4"
    # does not fire inside "24" or "0.42".
    return out


def _scalars(results, prefix=""):
    for key, value in (results or {}).items():
        if key.startswith("_"):
            continue
        if isinstance(value, dict):
            yield from _scalars(value, f"{prefix}{key}.")
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            yield f"{prefix}{key}", value


def check_hint(text: str, case, seed: int) -> list:
    """``[detail]`` -- ways this hint hands over something it should not.

    Mechanical over-specification checks only. They cannot judge altitude, which is human work
    and is why every rung ships a written rationale; what they can do is stop a hint containing
    an answer, a private graph key, or a value from this seed's own results. The method
    vocabulary is checked separately and more thoroughly by ``build.assert_no_method_leak``,
    which sees the rendered instruction.
    """
    findings = []
    low = text.lower()
    _blocks, results = case.generate(seed)

    for node in case.graph.nodes:
        if node.key.lower() in low:
            findings.append(f"names the private graph node key {node.key!r}")
    for field, value in _scalars(results):
        for rendering in sorted(_renderings(value), key=len, reverse=True):
            if re.search(r"(?<![\d.])" + re.escape(rendering) + r"(?![\d.])", text):
                findings.append(f"contains {rendering!r}, a rendering of this seed's {field}")
                break
    return findings
