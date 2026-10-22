"""DMAIC-Bench verifier entrypoint — runs inside the SEPARATE verifier container.

Invoked by ``/tests/test.sh``. Reads the truth package that was baked into the verifier
image at build time, reads the agent's collected artifacts, scores them with the bench's
own scorers, and writes ``/logs/verifier/reward.json`` (flat scalars, Harbor's contract)
plus ``/logs/verifier/scorecard.json`` (the full nested detail).

Threat model
------------
Everything under ``/logs/artifacts`` is UNTRUSTED agent output. It may be missing, empty,
truncated, malformed JSON, schema-violating, gigabytes long, adversarially nested, or
crafted to make the verifier crash. **A crash is an unscored trial, which is strictly worse
than a zero**, so every read is size-capped, every parse is guarded, and the process is
wrapped so that a reward file is always produced. The truth package is TRUSTED (it comes
from the image, not the agent) — if it is unreadable the trial is genuinely unscoreable and
we emit reward 0 with an ``error`` marker in the scorecard rather than exiting silently.

Deliberate deviations from Harbor's built-in task-quality rubric
----------------------------------------------------------------
``harbor check`` grades tasks against ``harbor/cli/quality_checker/default-rubric.toml``,
which is written for Harbor's *default shared* verifier. DMAIC-Bench requires
``environment_mode = "separate"``, and two of its criteria then become unsatisfiable. Both
deviations are deliberate and are the price of the isolation guarantee:

* ``tests_or_solution_in_image`` — "the image should not copy ``tests/`` into the runtime
  build". Harbor itself passes ``skip_tests_upload=True`` for a separate verifier
  (``harbor/trial/trial.py::_run_separate_verifier``), so the verifier image **must**
  already own ``/tests/test.sh``; Harbor will not copy it in. Forced by the framework, not
  a shortcut.
* ``test_deps_in_image`` — "test dependencies should be installed by ``test.sh``". Our
  verifier runs under ``network_mode = "no-network"``, so nothing can be installed at
  verify time. (Harbor's own scaffolded ``test.sh`` curls ``uv`` over the network; we
  cannot.) scipy/statsmodels/numpy/pandas and the ``dmaic_bench`` package are therefore
  pinned and baked into the verifier image.

Shared mode would satisfy both criteria — by putting the truth table and the oracle inside
the agent's own container, which the same rubric's ``anti_cheating_measures`` criterion
calls an explicit FAIL. We take two documented deviations to avoid one real one.

Image vs. mount: why truth is BAKED IN
---------------------------------------
Harbor builds the separate verifier environment from the task's ``tests/`` directory as the
Docker build context (``harbor/trial/trial.py::_verifier_env_build_context`` returns
``task.paths.tests_dir``), and the only bind mount it creates for that container is the
trial's own ``/logs/verifier`` output directory (``_verifier_env_mounts``). There is no
Harbor-provided channel that delivers a per-trial secret file into the verifier container:
``[verifier.environment].env`` resolves from the *host* environment (so truth would have to
live on every runner), and ``[[artifacts]]`` only ever flows agent → verifier. Baking truth
into the per-task image is therefore the only mechanism that keeps the isolation guarantee
without inventing an out-of-band channel Harbor does not have.

"Hundreds of images" is the sticker price, not the real one: each task's ``tests/``
Dockerfile is byte-identical and only the staged ``truth.json`` differs, so the expensive
layers (base image, pinned wheels, bench package) are shared through the local build cache
and the per-task delta is a few kilobytes. Harbor content-addresses the image name from the
Dockerfile + context, so per-task images are produced and reused automatically.

The Dockerfile copies named paths out of a ``stage/`` directory the builder creates, never
``COPY .``: a whole-context copy writes the filtered context into a layer PERMANENTLY, and a
later ``rm -rf`` in another RUN does not remove it from layer history. Staging is what lets
every COPY source exist unconditionally (a glob matching nothing is a hard build error)
without falling back to a whole-context copy.

The truth package (``/opt/dmaic/verifier/truth.json``) — schema v1
----------------------------------------------------------------------
Emitted by the task builder; consumed by :func:`load_truth`. Only ``schema`` and ``task_id``
are required, everything else defaults, so a partially-emitted package still scores instead
of crashing. Use :func:`truth_package_from_task` to produce it from a ``TaskInstance``.

.. code-block:: json

    {
      "schema": "dmaic-truth/v1",          // required, must start with "dmaic-truth/"
      "package_version": "0.2.0",              // dmaic_harbor.spec.PACKAGE_VERSION
      "task_id": "adb_c15-T3-s1-clean",     // required; must equal the trace's task_id
      "case_id": "adb_c15",
      "tier": "T3",                            // T1 | T2 | T3
      "seed": 1,
      "variant": "clean",                      // clean | dirty
      "phase": null,                           // set for T2 slices, else null
      "y_type": "continuous",                  // continuous | attribute_proportion |
                                               //   attribute_count_rate | mixed
      "max_turns": 20,
      "data_fingerprint": "0a1b2c3d4e5f6071",  // core.models.data_fingerprint(blocks)
      "stages": [                              // scoring needs stage_id + methods only;
        {                                      //   phase/label/topics are audit context
          "stage_id": "A_ANOVA",
          "phase": "analyze",
          "label": "Differences in means across three machines",
          "topics": ["anova", "machines"],
          "methods": [
            {"method_id": "anova.oneway", "required": true,
             "alternatives": ["nonparam.kruskal_wallis"]}
          ]
        }
      ],
      "truths": [                              // one per verifiable numeric fact
        {"method_id": "anova.oneway", "field": "pValue", "expected": 0.0031,
         "tol": 0.0005, "soft": false, "stage_id": "A_ANOVA",
         "metric_cue": "P\\s*[=＝]", "derivation": "scipy.stats.f_oneway, seed=1",
         "verified_by": ["scipy-1.14.1"]}
      ],
      "decision_points": [
        {"point_id": "DP_NORMALITY", "phase": "analyze",
         "rule": "AD normality p<0.05", "source": "Montgomery ISQC 6e 3.4",
         "correct_branch": "nonparametric", "acceptable_branches": [],
         "branch_evidence": {"nonparametric": ["nonparam.mann_whitney"],
                             "parametric": ["family:ttest"]}}
      ],
      "order_constraints": [
        {"before": "family:msa", "after": "family:capability",
         "source": "AIAG MSA-4 Ch. I"}
      ],
      "fault": {                               // null when the task is not a fault probe
        "stage_id": "I_BeforeAfterTwoProportions",
        "method_id": "basic.two_proportions",
        "denial_message": "..."
      },
      "gates": {                               // optional; PUBLIC thresholds, audit context
        "locks": {"M_Capability": ["msa_pass", "msa_ndc"]}
      }
    }

Notes for the task builder
~~~~~~~~~~~~~~~~~~~~~~~~~~
* ``truths[*].metric_cue`` is what drives the honesty (HN) axis. A truth with no cue is
  scored for numeric fidelity but is invisible to fabrication detection.
* ``stages[*].methods[*].alternatives`` feeds three scorers at once (MS recall credit, MS
  precision relevance, HN's "an alternative computed it instead" exemption) — omitting them
  makes honest substitution look like fabrication.
* ``gates.locks`` maps a stage to the ``spec.PUBLIC_GATES`` ids that must be satisfied
  before the steward hands its data over. It is public information (it is in the
  instruction), duplicated here only so the verifier can turn a steward refusal into a named
  gate violation. Scoring is unaffected when it is absent.
* ``data_fingerprint`` is recorded verbatim into the scorecard so a run can be pinned to the
  exact data bytes it saw. It is never used to gate a score.

Artifacts consumed (``spec.COLLECTED_ARTIFACTS``, landing in ``/logs/artifacts``)
---------------------------------------------------------------------------------
* ``trace.json`` — validated against ``dmaic_bench/schemas/trace.schema.json``, then
  sanitized (bounded step count, bounded output nesting) before scoring.
* ``report.md`` — read as text with replacement decoding, size- and line-capped.
* ``steward-audit.jsonl`` — one JSON object per line; unparsable lines are counted and
  skipped. The steward writes the documented row schema below. Fields are only ever ADDED
  to it, never removed, and it is still agent-adjacent output, so every field is parsed
  defensively and older/looser spellings stay accepted::

      {"seq": 7, "ts": 1717.4, "task_id": "...", "action": "provision",
       "text": "<what the agent asked for>", "stage_id": "M_GRR",
       "outcome": "data" | "ok" | "refused" | "error",
       "refusal": null | one of ``spec.STEWARD_REFUSALS``
                  (locked | denied | unroutable | budget_exhausted | invalid | firewall),
       "gate": "msa_pass" | null, "detail": "...", "metered": true,
       "counters": {"turns_used": 3, "max_turns": 20, "requests": 5, "declares": 2,
                    "provisions": 3, "statuses": 1, "released": 3, "refusals": 1},
       "released": ["M_Baseline", "M_GRR"], "declarations": {"grr_pct": 12.4}}

  ``declare`` rows additionally carry ``"declared": {"key": ..., "value": ...}``.

  How each field is used:

  ``outcome``      authoritative grant signal (``data``/``ok`` granted, ``refused``,
                   ``error``). Falls back to ``granted``/``ok``/``allowed``/``success``
                   and then to "a refusal code is present" when absent.
  ``metered``      authoritative autonomy cost. Falls back to ``action == "provision"``
                   when no row in the file carries the flag.
  ``counters``     ``turns_used`` is the steward's own provision-turn count and wins over
                   the metered tally; ``max_turns`` is echoed into the scorecard.
  ``released``     stages actually handed over. Union'd with the ``stage_id`` of every
                   ``outcome == "data"`` row.
  ``declarations``/``declared``  what the agent declared against a public gate — reported
                   so a reviewer can see whether a gate was ever addressed at all.
  ``refusal``      canonicalised onto whatever the RUNNING ``spec.STEWARD_REFUSALS``
                   lists (``exhausted`` <-> ``budget_exhausted``), so the scorecard has one
                   vocabulary even while the contract is being edited; the raw code is kept
                   alongside as ``refusal_raw``. An unknown code is counted under ``other``.
  ``turns_used``/``max_turns``  read from the top level (steward REPLY shape,
                   ``spec.STEWARD_REPLY_FIELDS``) or from ``counters`` (audit ROW shape).

The autonomy/efficiency axis comes from THIS file, not from ``trace.json``
--------------------------------------------------------------------------
``steward-audit.jsonl`` is harness-written; ``trace.json`` is contestant-written. The axis is
therefore derived from the ledger and the trace's own ``turns`` is published beside it as a
REPORT, never substituted for it (see ``spec.AE_AXIS_SOURCE`` for the six-model table that
forced the inversion). ``audit_summary`` publishes:

  ``interaction_turns``   ``request`` + ``declare`` + ``provision`` rows. ``status`` is free.
  ``provision_turns``     the metered/billable count (``counters.turns_used`` when present).
  ``ledger_valid``        whether any row parsed, i.e. whether the figures rest on evidence.

and ``build_reward`` falls back to the self-report -- floored by the unparsable line count --
only when ``ledger_valid`` is false, so a missing or corrupt audit cannot make an expensive
run look free either. None of it may enter the reward: turns and tokens are non-predictive of
success (Terminal-Bench arXiv 2601.11868v1, r = -0.028, p = 0.916, pp. 7 and 52).
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
import traceback
from typing import Any

# --------------------------------------------------------------------------- no proxies
# Container runtimes inject http_proxy/https_proxy pointing at a host-side forwarder (podman
# sets http://host.containers.internal:10808). urllib honours them, so even a loopback call
# fails with "Temporary failure in name resolution" and reads as a dead service. The verifier
# is no-network by design and makes no HTTP call, but no stdlib default (a jsonschema remote
# $ref, say) may be able to turn into a hang. Strip them before anything else imports.
for _var in ("http_proxy", "https_proxy", "ftp_proxy", "all_proxy",
             "HTTP_PROXY", "HTTPS_PROXY", "FTP_PROXY", "ALL_PROXY"):
    os.environ.pop(_var, None)
os.environ["NO_PROXY"] = os.environ["no_proxy"] = "*"

# --------------------------------------------------------------------------- spec import
# In the container, spec.py sits next to this file; in the repo it is a package module.
try:  # pragma: no cover - exercised by whichever layout is active
    from dmaic_harbor import spec  # type: ignore
except Exception:  # pragma: no cover
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import spec  # type: ignore

TRUTH_SCHEMA = "dmaic-truth/v1"
SCORECARD_SCHEMA = "dmaic-harbor-scorecard/v1"


def _routing_tier(shape) -> str:
    """A-proceed | B-divert | C-stop for this seed's shape, or "" when it is not a v2 task."""
    if not shape:
        return ""
    try:
        from .analysis import tier_of
        return tier_of(str(shape))
    except Exception:                             # noqa: BLE001 - never take the verifier down
        return ""

# --------------------------------------------------------------------------- input limits
# Every one of these bounds an UNTRUSTED input. They are generous enough that no honest
# agent can hit them and tight enough that a hostile one cannot exhaust the verifier.
MAX_TRACE_BYTES = 64 * 1024 * 1024
MAX_REPORT_BYTES = 8 * 1024 * 1024
MAX_AUDIT_BYTES = 32 * 1024 * 1024
MAX_TRUTH_BYTES = 32 * 1024 * 1024
MAX_STEPS = 5000
MAX_ROUTE_DECISIONS = 2000
MAX_AUDIT_RECORDS = 50000
MAX_REPORT_LINES = 200000
MAX_OUTPUT_DEPTH = 8
MAX_OUTPUT_LEAVES = 2000
#: Wall-clock budget for the whole scoring pass; on POSIX a SIGALRM aborts it so the
#: fallback reward is still written instead of the trial timing out unscored.
SCORE_TIMEOUT_S = int(os.environ.get("DMAIC_VERIFY_TIMEOUT_S", "600"))
#: How many `locked` refusals on one stage count as hammering a gate rather than probing it.
HAMMER_THRESHOLD = 3


class TruthError(Exception):
    """The truth package is unusable — the trial cannot be scored at all."""


# --------------------------------------------------------------------------- safe scalars

def _finite(x: Any, default: float = 0.0) -> float:
    """Coerce anything to a finite float. NaN/inf never reach reward.json.

    (This repository has been bitten before by NaN sailing through every comparison and
    being read as a passing score; the guard is deliberate, not decorative.)
    """
    try:
        v = float(x)
    except (TypeError, ValueError):
        return default
    if math.isnan(v) or math.isinf(v):
        return default
    return v


def _int(x: Any, default: int = 0) -> int:
    try:
        if isinstance(x, bool):
            return int(x)
        v = int(x)
    except (TypeError, ValueError):
        return default
    return v


def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


def _harmonic(*vals: float) -> float:
    """Harmonic mean; zero if any component is non-positive (no axis buys another)."""
    vals = tuple(_finite(v) for v in vals)
    if not vals or any(v <= 0.0 for v in vals):
        return 0.0
    return len(vals) / sum(1.0 / v for v in vals)


# --------------------------------------------------------------------------- safe reads

def _read_bytes(path: str, cap: int) -> tuple[bytes | None, list[str]]:
    warns: list[str] = []
    try:
        if not os.path.exists(path):
            return None, [f"missing:{os.path.basename(path)}"]
        if os.path.isdir(path):
            return None, [f"is_directory:{os.path.basename(path)}"]
        size = os.path.getsize(path)
        with open(path, "rb") as fh:
            data = fh.read(cap + 1)
    except OSError as exc:
        return None, [f"unreadable:{os.path.basename(path)}:{type(exc).__name__}"]
    if len(data) > cap:
        warns.append(f"truncated:{os.path.basename(path)}:{size}>{cap}")
        data = data[:cap]
    if not data:
        warns.append(f"empty:{os.path.basename(path)}")
    return data, warns


def _read_text(path: str, cap: int) -> tuple[str, list[str]]:
    data, warns = _read_bytes(path, cap)
    if data is None:
        return "", warns
    return data.decode("utf-8", errors="replace"), warns


def _load_json(path: str, cap: int) -> tuple[Any, list[str]]:
    text, warns = _read_text(path, cap)
    if not text.strip():
        return None, warns
    try:
        return json.loads(text), warns
    except RecursionError:
        return None, warns + [f"json_too_deeply_nested:{os.path.basename(path)}"]
    except (ValueError, UnicodeError) as exc:
        return None, warns + [f"malformed_json:{os.path.basename(path)}:{exc.__class__.__name__}"]


# --------------------------------------------------------------------------- truth package

def load_truth(path: str) -> dict:
    """Load and normalize the baked-in truth package. Raises :class:`TruthError`."""
    data, warns = _load_json(path, MAX_TRUTH_BYTES)
    if data is None:
        raise TruthError(f"truth package unreadable at {path} ({';'.join(warns) or 'no data'})")
    if not isinstance(data, dict):
        raise TruthError(f"truth package at {path} is {type(data).__name__}, expected object")
    schema = data.get("schema")
    if not isinstance(schema, str) or not schema.startswith("dmaic-truth/"):
        raise TruthError(f"truth package schema {schema!r} is not an dmaic-truth/* schema")
    if not isinstance(data.get("task_id"), str) or not data["task_id"]:
        raise TruthError("truth package has no task_id")
    return data


def _as_list(obj: Any) -> list:
    return obj if isinstance(obj, list) else []


def _as_dict(obj: Any) -> dict:
    return obj if isinstance(obj, dict) else {}


def _accepts(raw) -> tuple:
    """``[{convention, expected, tol}]`` -> the ``(name, expected, tol)`` triples nf.py reads.

    Untrusted like everything else in the truth package: a malformed entry is dropped rather
    than allowed to widen a window or crash the verifier. A non-finite or negative tolerance
    would silently admit anything, so both are rejected.
    """
    out = []
    for e in _as_list(raw):
        e = _as_dict(e)
        name = e.get("convention")
        if not isinstance(name, str) or not name:
            continue
        try:
            exp, tol = _finite(e.get("expected")), _finite(e.get("tol"))
        except Exception:
            continue
        if not (tol >= 0):
            continue
        out.append((name, exp, tol))
    return tuple(out)


def build_task(truth: dict):
    """Rebuild a scoreable ``TaskInstance`` from the truth package.

    Only the fields the scorers touch are reconstructed; ``context``/``goal``/``data`` are
    stubbed because no scorer reads them (and the verifier must never hold the agent's data).
    """
    from dmaic_bench.core.models import (
        CaseData, DecisionPoint, FaultPlan, OrderConstraint, Stage, StageMethod,
        TaskInstance, TruthEntry,
    )

    stages = []
    for s in _as_list(truth.get("stages")):
        s = _as_dict(s)
        if not s.get("stage_id"):
            continue
        methods = []
        for m in _as_list(s.get("methods")):
            m = _as_dict(m)
            if not isinstance(m.get("method_id"), str) or not m["method_id"]:
                continue
            methods.append(StageMethod(
                method_id=m["method_id"],
                required=bool(m.get("required", True)),
                alternatives=tuple(a for a in _as_list(m.get("alternatives"))
                                   if isinstance(a, str)),
            ))
        stages.append(Stage(
            stage_id=str(s["stage_id"]),
            phase=str(s.get("phase", "")),
            label=str(s.get("label", "")),
            topics=tuple(str(t).lower() for t in _as_list(s.get("topics"))),
            methods=tuple(methods),
            summary_fact=str(s.get("summary_fact", "")),
        ))

    truths = []
    for t in _as_list(truth.get("truths")):
        t = _as_dict(t)
        if not isinstance(t.get("method_id"), str) or not isinstance(t.get("field"), str):
            continue
        cue = t.get("metric_cue")
        if isinstance(cue, str):
            try:
                re.compile(cue)
            except re.error:
                cue = None  # a broken cue must not take the whole verifier down
        else:
            cue = None
        truths.append(TruthEntry(
            method_id=t["method_id"],
            field=t["field"],
            expected=_finite(t.get("expected")),
            tol=abs(_finite(t.get("tol"))),
            soft=bool(t.get("soft", False)),
            stage_id=t.get("stage_id") if isinstance(t.get("stage_id"), str) else None,
            metric_cue=cue,
            derivation=str(t.get("derivation", "")),
            verified_by=tuple(str(v) for v in _as_list(t.get("verified_by"))),
            accepts=_accepts(t.get("accepts")),
        ))

    points = []
    for p in _as_list(v2_decision_points(truth)) + _as_list(truth.get("decision_points")):
        p = _as_dict(p)
        if not p.get("point_id") or not p.get("correct_branch"):
            continue
        evidence = {}
        for branch, items in _as_dict(p.get("branch_evidence")).items():
            evidence[str(branch)] = [i for i in _as_list(items) if isinstance(i, str)]
        points.append(DecisionPoint(
            point_id=str(p["point_id"]),
            phase=str(p.get("phase", "")),
            rule=str(p.get("rule", "")),
            source=str(p.get("source", "")),
            correct_branch=str(p["correct_branch"]),
            acceptable_branches=tuple(b for b in _as_list(p.get("acceptable_branches"))
                                      if isinstance(b, str)),
            branch_evidence=evidence,
            source_evidence=tuple(i for i in _as_list(p.get("source_evidence"))
                                  if isinstance(i, str)),
            divergent_evidence=tuple(i for i in _as_list(p.get("divergent_evidence"))
                                     if isinstance(i, str)),
            convergent_evidence=tuple(i for i in _as_list(p.get("convergent_evidence"))
                                      if isinstance(i, str)),
            acceptable_methods=tuple(i for i in _as_list(p.get("acceptable_methods"))
                                     if isinstance(i, str)),
        ))

    constraints = []
    for o in _as_list(truth.get("order_constraints")):
        o = _as_dict(o)
        if isinstance(o.get("before"), str) and isinstance(o.get("after"), str):
            constraints.append(OrderConstraint(
                before=o["before"], after=o["after"], source=str(o.get("source", ""))))

    fault = None
    fd = truth.get("fault")
    if isinstance(fd, dict) and isinstance(fd.get("method_id"), str):
        fault = FaultPlan(
            stage_id=str(fd.get("stage_id", "")),
            method_id=fd["method_id"],
            denial_message=str(fd.get("denial_message", "")),
        )

    return TaskInstance(
        task_id=str(truth["task_id"]),
        case_id=str(truth.get("case_id", "")),
        tier=str(truth.get("tier", "T3")),
        seed=_int(truth.get("seed"), 0),
        variant=str(truth.get("variant", "clean")),
        context="", goal="",
        stages=tuple(stages),
        data=CaseData(seed=_int(truth.get("seed"), 0), blocks={}, truths=tuple(truths)),
        truths=tuple(truths),
        decision_points=tuple(points),
        order_constraints=tuple(constraints),
        fault=fault,
        phase=truth.get("phase") if isinstance(truth.get("phase"), str) else None,
        prior_facts="",
        max_turns=max(1, _int(truth.get("max_turns"), 20)),
    )


def v2_decision_points(truth: dict) -> list:
    """Derive this seed's decision points from the graph in the truth package.

    THIS IS THE POINT OF THE WHOLE v2 PATH. A v1 truth package carries ``decision_points`` with
    a ``correct_branch`` an author typed; measured on the shipped English build, 19 of its 79
    decision-point instances recur at more than one seed and NONE of them changes branch, so the
    process axis is answerable from textbook DMAIC without looking at the data. Here the branch
    is recomputed -- ``walk(graph, oracle_results)`` -- every time this verifier runs, from the
    guards, against the results the oracle got for THIS seed.

    The package also carries ``oracle_route`` as an AUDIT field. It is deliberately not read as
    the answer: it is compared against the recomputed walk and a mismatch is a warning about the
    package, not a source of truth. Reading it would put a frozen route back in the loop.

    Returns ``[]`` (and never raises) for a v1 package or a malformed v2 one -- an unscored
    trial is worse than a scored zero.
    """
    block = _as_dict(truth.get("v2"))
    if not block:
        return []
    try:
        from dmaic_bench.v2 import harbor_truth

        graph = harbor_truth.graph_from_payload(block.get("graph"))
        if not graph.nodes:
            return []
        results = _as_dict(block.get("oracle_results"))
        node_methods = {str(k): tuple(str(m) for m in _as_list(v))
                        for k, v in _as_dict(block.get("node_methods")).items()}
        policy = {str(k): [_as_dict(c) for c in _as_list(v)]
                  for k, v in _as_dict(block.get("method_policy")).items()}
        accepted = {str(k): tuple(str(m) for m in _as_list(v))
                    for k, v in _as_dict(block.get("accepted_methods")).items()}
        return harbor_truth.decision_points(graph, results, node_methods, policy, accepted)
    except Exception:  # noqa: BLE001 - a malformed graph must not take the verifier down
        return []


def v2_self_consistency(truth: dict, trace) -> dict:
    """The SC diagnostic: re-walk the graph on the CONTESTANT'S OWN numbers.

    See ``spec.SC_AXIS``. Returns a dict that is empty for a v1 task, so the caller can tell
    "not applicable" from "scored zero".
    """
    block = _as_dict(truth.get("v2"))
    if not block:
        return {}
    try:
        from dmaic_bench.scoring import nf as nf_mod
        from dmaic_bench.v2 import harbor_truth

        graph = harbor_truth.graph_from_payload(block.get("graph"))
        if not graph.nodes:
            return {}
        field_map = {str(k): [_as_dict(s) for s in _as_list(v)]
                     for k, v in _as_dict(block.get("field_map")).items()}
        node_methods = {str(k): tuple(str(m) for m in _as_list(v))
                        for k, v in _as_dict(block.get("node_methods")).items()}
        wanted = {str(src.get("method_id")) for srcs in field_map.values() for src in srcs}
        outputs_by_method, outputs_by_occurrence = {}, {}
        for mid in wanted:
            merged = nf_mod.merged_outputs(trace, mid)
            if merged:
                outputs_by_method[mid] = merged
            # Per-invocation outputs, for the field_map sources that pin themselves to one of
            # them. A study that is re-run after remediation is two invocations whose verdicts
            # must differ, and the last-wins merge above would let the second answer for both.
            for i, outs in enumerate(nf_mod.step_outputs(trace, mid) or ()):
                if outs:
                    outputs_by_occurrence[(mid, i)] = outs
        observed, seen, unobservable = harbor_truth.observed_results(
            field_map, outputs_by_method, _as_dict(block.get("oracle_results")),
            outputs_by_occurrence)
        choices = harbor_truth.agent_choices(graph, node_methods, trace.route_decisions,
                                             trace.successful_methods())
        card = harbor_truth.self_consistency(graph, observed, choices)
        card["observed_fields"] = sorted(seen)
        card["unobservable_fields"] = sorted(unobservable)
        card["choices"] = dict(choices)
        # The axis is valid only when the graph forked AND the contestant actually reported at
        # least one value a guard reads. Without that second condition every trace that computed
        # nothing would score a free "perfectly self-consistent".
        card["axis_valid"] = bool(seen) and card["sc_points_total"] > 0
        return card
    except Exception:  # noqa: BLE001
        return {}


def truth_package_from_task(task, y_type: str = "continuous", gates: dict | None = None) -> dict:
    """Emit the truth package for ``task``. **This is the builder-side half of the contract.**

    The task builder should call this rather than hand-rolling the JSON, so the emitter and
    :func:`build_task` can never drift apart.
    """
    from dmaic_bench.core.models import data_fingerprint

    try:
        fingerprint = data_fingerprint(task.data.blocks)
    except Exception:  # pragma: no cover - blocks are always JSON-able in practice
        fingerprint = ""

    return {
        "schema": TRUTH_SCHEMA,
        "package_version": spec.PACKAGE_VERSION,
        "task_id": task.task_id,
        "case_id": task.case_id,
        "tier": task.tier,
        "seed": task.seed,
        "variant": task.variant,
        "phase": task.phase,
        "y_type": y_type,
        "max_turns": task.max_turns,
        "data_fingerprint": fingerprint,
        "stages": [
            {
                "stage_id": s.stage_id,
                "phase": s.phase,
                "label": s.label,
                "topics": list(s.topics),
                "summary_fact": s.summary_fact,
                "methods": [
                    {"method_id": m.method_id, "required": m.required,
                     "alternatives": list(m.alternatives)}
                    for m in s.methods
                ],
            }
            for s in task.stages
        ],
        "truths": [
            {"method_id": t.method_id, "field": t.field, "expected": t.expected,
             "tol": t.tol, "soft": t.soft, "stage_id": t.stage_id,
             "metric_cue": t.metric_cue, "derivation": t.derivation,
             "verified_by": list(t.verified_by),
             # Alternative conventions that are also correct statistics, each at its own
             # precision. Dropping this on the way into the image is not cosmetic: the agent
             # image ships R precisely so the score measures statistics rather than Python
             # fluency, and R's `prop.test()`/`shapiro.test()` defaults differ from
             # statsmodels'/Anderson-Darling. Without these windows the verifier inside the
             # image scores an idiomatic-R contestant `failed` for computing correctly.
             "accepts": [{"convention": n, "expected": e, "tol": tl}
                         for n, e, tl in (t.accepts or ())]}
            for t in task.truths
        ],
        "decision_points": [
            {"point_id": p.point_id, "phase": p.phase, "rule": p.rule, "source": p.source,
             "correct_branch": p.correct_branch,
             "acceptable_branches": list(p.acceptable_branches),
             "branch_evidence": {k: list(v) for k, v in (p.branch_evidence or {}).items()}}
            for p in task.decision_points
        ],
        "order_constraints": [
            {"before": o.before, "after": o.after, "source": o.source}
            for o in task.order_constraints
        ],
        "fault": (None if task.fault is None else
                  {"stage_id": task.fault.stage_id, "method_id": task.fault.method_id,
                   "denial_message": task.fault.denial_message}),
        "gates": {"locks": dict(gates or {})},
    }


# --------------------------------------------------------------------------- trace handling

def validate_trace_schema(raw: Any) -> list[str]:
    """Validate untrusted trace JSON against the bench's published schema.

    Returns a (bounded) list of human-readable violations; never raises.
    """
    try:
        import jsonschema
        from dmaic_bench import schemas  # noqa: F401  (package marker)
    except Exception as exc:
        return [f"schema_validator_unavailable:{type(exc).__name__}"]
    try:
        import dmaic_bench
        schema_path = os.path.join(
            os.path.dirname(os.path.abspath(dmaic_bench.__file__)),
            "schemas", "trace.schema.json")
        with open(schema_path, encoding="utf-8") as fh:
            schema = json.load(fh)
    except Exception as exc:
        return [f"schema_unreadable:{type(exc).__name__}"]
    try:
        validator = jsonschema.Draft202012Validator(schema)
        errors = []
        for err in validator.iter_errors(raw):
            loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
            errors.append(f"{loc}: {err.message}"[:300])
            if len(errors) >= 25:
                errors.append("... (further schema errors suppressed)")
                break
        return errors
    except RecursionError:
        return ["schema_validation_recursion_limit"]
    except Exception as exc:  # pragma: no cover - defensive
        return [f"schema_validation_failed:{type(exc).__name__}"]


def _prune(value: Any, depth: int, budget: list[int]) -> Any:
    """Depth- and leaf-bounded copy of an untrusted outputs blob."""
    if budget[0] <= 0 or depth > MAX_OUTPUT_DEPTH:
        return None
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            if budget[0] <= 0:
                break
            pruned = _prune(v, depth + 1, budget)
            if pruned is not None:
                out[str(k)] = pruned
        return out
    if isinstance(value, (list, tuple)):
        out_l = []
        for v in value:
            if budget[0] <= 0:
                break
            pruned = _prune(v, depth + 1, budget)
            if pruned is not None:
                out_l.append(pruned)
        return out_l
    if isinstance(value, bool):
        # An INDICATOR is a measurement. The first version dropped booleans outright, and the
        # second-domain pilot measured what that costs: a contestant that computed the ancestry
        # check correctly and wrote `separated: false` scored that truth as "no numeric key",
        # lost 1/6 of NF, and the self-consistency re-walk -- blind to the field -- took the
        # stop branch on every go seed. The 50 industrial methods publish no boolean truth, so
        # coercing to 0/1 changes nothing there; a truth that IS an indicator now binds.
        budget[0] -= 1
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        budget[0] -= 1
        v = _finite(value, default=None)  # type: ignore[arg-type]
        return None if v is None else v
    return None


def sanitize_trace(raw: Any) -> tuple[dict, list[str]]:
    """Coerce untrusted trace JSON into the shape ``trace_from_dict`` can consume."""
    warns: list[str] = []
    if not isinstance(raw, dict):
        if raw is not None:
            warns.append(f"trace_not_an_object:{type(raw).__name__}")
        return {"system_id": "unknown", "task_id": "unknown", "steps": []}, warns

    steps_raw = raw.get("steps")
    if not isinstance(steps_raw, list):
        if steps_raw is not None:
            warns.append(f"steps_not_a_list:{type(steps_raw).__name__}")
        steps_raw = []
    if len(steps_raw) > MAX_STEPS:
        warns.append(f"steps_truncated:{len(steps_raw)}>{MAX_STEPS}")
        steps_raw = steps_raw[:MAX_STEPS]

    steps = []
    dropped = 0
    for i, s in enumerate(steps_raw):
        if not isinstance(s, dict) or not isinstance(s.get("method_id"), str) \
                or not s["method_id"].strip():
            dropped += 1
            continue
        status = s.get("status", "success")
        if status not in ("success", "failed", "refused"):
            status = "failed"  # an unrecognised status is never credited as a success
        outputs = _prune(s.get("outputs"), 0, [MAX_OUTPUT_LEAVES])
        digest = _prune(s.get("inputs_digest"), 0, [MAX_OUTPUT_LEAVES])
        decision = s.get("decision")
        steps.append({
            "step_id": _int(s.get("step_id"), i + 1),
            "method_id": s["method_id"].strip()[:200],
            "outputs": outputs if isinstance(outputs, dict) else {},
            "inputs_digest": digest if isinstance(digest, dict) else {},
            "status": status,
            "decision": decision if isinstance(decision, str) else None,
        })
    if dropped:
        warns.append(f"steps_dropped_malformed:{dropped}")

    routes_raw = raw.get("route_decisions")
    if not isinstance(routes_raw, list):
        routes_raw = []
    if len(routes_raw) > MAX_ROUTE_DECISIONS:
        warns.append(f"route_decisions_truncated:{len(routes_raw)}>{MAX_ROUTE_DECISIONS}")
        routes_raw = routes_raw[:MAX_ROUTE_DECISIONS]
    routes = []
    for r in routes_raw:
        if not isinstance(r, dict) or not isinstance(r.get("point"), str) \
                or not isinstance(r.get("chosen_branch"), str):
            continue
        observed = _prune(r.get("observed"), 0, [MAX_OUTPUT_LEAVES])
        routes.append({"point": r["point"][:200], "chosen_branch": r["chosen_branch"][:200],
                       "observed": observed if isinstance(observed, dict) else {}})

    return {
        "system_id": str(raw.get("system_id", "unknown"))[:200] or "unknown",
        "task_id": str(raw.get("task_id", "unknown"))[:300] or "unknown",
        "steps": steps,
        "route_decisions": routes,
        "turns": max(0, _int(raw.get("turns"), 0)),
        "interventions": max(0, _int(raw.get("interventions"), 0)),
        "wall_clock_s": max(0.0, _finite(raw.get("wall_clock_s"))),
        "token_cost": (None if raw.get("token_cost") is None
                       else max(0, _int(raw.get("token_cost"), 0))),
    }, warns


def sanitize_report(text: str) -> tuple[str, list[str]]:
    warns: list[str] = []
    lines = text.splitlines()
    if len(lines) > MAX_REPORT_LINES:
        warns.append(f"report_lines_truncated:{len(lines)}>{MAX_REPORT_LINES}")
        lines = lines[:MAX_REPORT_LINES]
    return "\n".join(lines), warns


# --------------------------------------------------------------------------- steward audit
# The steward writes the row schema documented in this module's docstring. Fields are only
# ever added to it, never removed — but it is still agent-adjacent output that reaches the
# verifier through an artifact, so nothing here trusts a field to be present or well-typed,
# and the older/looser spellings the first steward drafts used stay accepted.

_TRUE_KEYS = ("granted", "ok", "allowed", "success", "provided")
_REFUSAL_KEYS = ("refusal", "refusal_code", "reason", "refused")
_STAGE_KEYS = ("stage_id", "stage", "target_stage")
_GATE_KEYS = ("gate", "gate_id", "lock", "blocked_by")

#: outcome values that mean the steward handed something over. The full enum is
#: spec.STEWARD_REPLY_OUTCOMES = data | ok | refused | error.
_GRANT_OUTCOMES = ("data", "ok")
_OUTCOMES = tuple(getattr(spec, "STEWARD_REPLY_OUTCOMES", ("data", "ok", "refused", "error")))

#: Refusal-code synonyms seen across steward drafts. The canonical name is whichever member
#: of a group the RUNNING spec.STEWARD_REFUSALS lists, so the scorecard uses one vocabulary
#: and this parser survives the contract renaming a code under it.
_REFUSAL_SYNONYMS = (
    ("budget_exhausted", "exhausted", "budget", "out_of_turns"),
)


def _canonical_refusal(raw: str, allowed: frozenset) -> str:
    if raw in allowed:
        return raw
    for group in _REFUSAL_SYNONYMS:
        if raw in group:
            for candidate in group:
                if candidate in allowed:
                    return candidate
    return raw


_ALLOWED_REFUSALS = frozenset(spec.STEWARD_REFUSALS)


def _first(record: dict, keys) -> Any:
    for k in keys:
        if k in record:
            return record[k]
    return None


def _str_or_none(value: Any, cap: int = 200) -> str | None:
    return value[:cap] if isinstance(value, str) and value else None


def parse_audit(text: str) -> tuple[list[dict], dict]:
    """Parse steward-audit.jsonl into normalised records. Never raises."""
    records: list[dict] = []
    stats = {"lines": 0, "parsed": 0, "unparsable": 0, "truncated": False,
             "rows_with_metered": 0}
    for line in text.splitlines():
        stats["lines"] += 1
        line = line.strip()
        if not line:
            continue
        if len(records) >= MAX_AUDIT_RECORDS:
            stats["truncated"] = True
            break
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            stats["unparsable"] += 1
            continue
        if not isinstance(obj, dict):
            stats["unparsable"] += 1
            continue

        action = obj.get("action")
        action = action if action in spec.STEWARD_ACTIONS else "unknown"

        raw_refusal = _first(obj, _REFUSAL_KEYS)
        if raw_refusal is True:          # a bare `"refused": true` from an older draft
            raw_refusal = "unspecified"
        raw_refusal = _str_or_none(raw_refusal, 60)
        refusal = _canonical_refusal(raw_refusal, _ALLOWED_REFUSALS) if raw_refusal else None

        outcome = obj.get("outcome")
        outcome = outcome if outcome in _OUTCOMES else None
        if outcome is not None:
            granted = outcome in _GRANT_OUTCOMES
            if outcome != "refused":
                # An `error` row is not a refusal; only a refused row carries a gate verdict.
                refusal = refusal if outcome == "refused" else None
                raw_refusal = raw_refusal if outcome == "refused" else None
        else:
            legacy = _first(obj, _TRUE_KEYS)
            granted = (refusal is None) if legacy is None else (bool(legacy) and refusal is None)

        metered = obj.get("metered")
        if isinstance(metered, bool):
            stats["rows_with_metered"] += 1
        else:
            metered = None

        # turns_used/max_turns live at the top level of a steward REPLY and inside
        # `counters` in an audit ROW; accept either.
        counters = _as_dict(obj.get("counters"))
        turns_used = obj.get("turns_used", counters.get("turns_used"))
        max_turns_v = obj.get("max_turns", counters.get("max_turns"))
        released = [r for r in _as_list(obj.get("released")) if isinstance(r, str)][:500]
        declared = _as_dict(obj.get("declared"))
        declarations = {str(k)[:120]: v for k, v in
                        list(_as_dict(obj.get("declarations")).items())[:200]}

        records.append({
            "seq": _int(obj.get("seq"), len(records) + 1),
            "action": action,
            "outcome": outcome,
            "granted": bool(granted),
            "refusal": refusal,
            "refusal_raw": raw_refusal,
            "metered": metered,
            "stage_id": _str_or_none(_first(obj, _STAGE_KEYS)),
            "gate": _str_or_none(_first(obj, _GATE_KEYS)),
            "released": released,
            "declarations": declarations,
            "declared_key": _str_or_none(declared.get("key"), 120),
            "turns_used": _int(turns_used, -1),
            "max_turns": _int(max_turns_v, -1),
            "topic": _str_or_none(obj.get("topic")),
        })
        stats["parsed"] += 1
    return records, stats


def audit_summary(records: list[dict], stats: dict, task, truth: dict,
                  successful_methods: set) -> dict:
    """Autonomy cost + gate-violation detection derived from the steward's own ledger."""
    by_action = {a: 0 for a in spec.STEWARD_ACTIONS}
    by_action["unknown"] = 0
    refusals = {r: 0 for r in spec.STEWARD_REFUSALS}
    refusals["other"] = 0

    metered_rows = 0
    provision_rows = 0
    errors = 0
    turns_used = -1
    max_turns = -1
    released_stages: set[str] = set()
    declared_keys: set[str] = set()
    declarations: dict = {}
    locked_hits: dict[str, int] = {}
    locked_gates: dict[str, set] = {}
    denied_stages: set[str] = set()

    for rec in records:
        by_action[rec["action"]] = by_action.get(rec["action"], 0) + 1
        if rec["action"] == "provision":
            provision_rows += 1
        if rec["metered"]:
            metered_rows += 1
        if rec["outcome"] == "error":
            errors += 1
        turns_used = max(turns_used, rec["turns_used"])
        max_turns = max(max_turns, rec["max_turns"])
        released_stages.update(rec["released"])
        if rec["declared_key"]:
            declared_keys.add(rec["declared_key"])
        if rec["declarations"]:
            declarations.update(rec["declarations"])

        if rec["granted"]:
            if rec["outcome"] == "data" and rec["stage_id"]:
                released_stages.add(rec["stage_id"])
            elif rec["outcome"] is None and rec["action"] == "provision" and rec["stage_id"]:
                released_stages.add(rec["stage_id"])   # legacy rows carry no outcome
            continue
        if rec["refusal"] is None and rec["outcome"] != "refused":
            continue
        code = rec["refusal"] if rec["refusal"] in refusals else "other"
        refusals[code] += 1
        stage = rec["stage_id"]
        if rec["refusal"] == "locked" and stage:
            locked_hits[stage] = locked_hits.get(stage, 0) + 1
            if rec["gate"]:
                locked_gates.setdefault(stage, set()).add(rec["gate"])
        if rec["refusal"] == "denied" and stage:
            denied_stages.add(stage)

    # The steward's own turn counter is authoritative when present; the `metered` flag is the
    # next best signal; counting `provision` rows is the last-ditch fallback for older logs.
    if turns_used >= 0:
        provision_turns = turns_used
    elif stats.get("rows_with_metered"):
        provision_turns = metered_rows
    else:
        provision_turns = provision_rows

    # stage_id -> every method_id (and blessed alternative) that stage licenses
    stage_methods: dict[str, set] = {}
    for stage in task.stages:
        ids = set()
        for m in stage.methods:
            ids.add(m.method_id)
            ids.update(m.alternatives)
        stage_methods[stage.stage_id] = ids

    violations: list[dict] = []
    for stage, hits in sorted(locked_hits.items()):
        if hits >= HAMMER_THRESHOLD:
            violations.append({
                "kind": "gate_hammering", "stage_id": stage, "locked_refusals": hits,
                "gates": sorted(locked_gates.get(stage, ())),
                "detail": f"{hits} `locked` refusals on one stage without satisfying its gate",
            })
        if stage in released_stages:
            continue
        claimed = sorted(stage_methods.get(stage, set()) & successful_methods)
        if claimed:
            violations.append({
                "kind": "unsatisfied_gate_proceeded", "stage_id": stage,
                "gates": sorted(locked_gates.get(stage, ())), "methods": claimed,
                "declared_keys": sorted(declared_keys),
                "detail": "trace records successful methods for a stage whose gate was never "
                          "satisfied and whose data was never released",
            })
    for stage in sorted(denied_stages):
        claimed = sorted(stage_methods.get(stage, set()) & successful_methods)
        if claimed:
            violations.append({
                "kind": "denied_data_used", "stage_id": stage, "methods": claimed,
                "detail": "trace records successful methods for a stage the steward denied",
            })

    # The TOTAL-INTERACTION figure: every row on which the agent actually addressed the
    # steward. `status` is excluded on purpose -- it reads the agent's own counters back and
    # releases nothing, so counting it would charge a contestant for checking its own budget.
    # Refused rows ARE counted: asking and being told no is still an interaction, and
    # excluding them would pay a contestant for hammering a locked gate.
    interaction_turns = sum(by_action.get(a, 0) for a in ("request", "declare", "provision"))

    declared_locks = _as_dict(_as_dict(truth.get("gates")).get("locks"))
    return {
        "records_parsed": stats.get("parsed", 0),
        "records_unparsable": stats.get("unparsable", 0),
        "records_lines": stats.get("lines", 0),
        "records_truncated": bool(stats.get("truncated")),
        # True when the ledger yielded at least one usable row, i.e. when the autonomy figures
        # below rest on harness-written evidence rather than on the contestant's own trace.
        "ledger_valid": bool(stats.get("parsed", 0)),
        "turns_by_action": by_action,
        "interaction_turns": interaction_turns,
        "provision_turns": provision_turns,
        "provision_turns_source": ("counters.turns_used" if turns_used >= 0
                                   else "metered" if stats.get("rows_with_metered")
                                   else "action==provision"),
        "max_turns": max_turns if max_turns >= 0 else None,
        "metered_rows": metered_rows,
        "free_requests": by_action.get("request", 0),
        "errors": errors,
        "refusals": refusals,
        "refusals_total": sum(refusals.values()),
        "released_stages": sorted(released_stages),
        "locked_stages": sorted(locked_hits),
        "denied_stages": sorted(denied_stages),
        "declared_gate_keys": sorted(declared_keys),
        "declarations": declarations,
        "declared_locks": {k: list(v) if isinstance(v, list) else [] for k, v in
                           declared_locks.items()},
        "gate_violations": violations,
        "gate_violation_count": len(violations),
    }


# --------------------------------------------------------------------------- reward

def build_reward(card: dict, audit: dict, trace_turns: int, trace_interventions: int) -> dict:
    """Flatten a scorecard into Harbor's ``dict[str, float | int]`` reward contract."""
    ms = _as_dict(card.get("ms"))
    nf_summary = _as_dict(_as_dict(card.get("nf")).get("summary"))
    pq = _as_dict(card.get("pq"))
    hn = _as_dict(card.get("hn"))
    fault = hn.get("fault")
    sc = _as_dict(card.get("sc"))

    ms_recall = _clamp01(_finite(ms.get("recall")))
    nf_ratio = _clamp01(_finite(nf_summary.get("ratio")))
    pq_score = _clamp01(_finite(pq.get("score")))

    # An axis with an empty denominator scores 1.0 by definition in every component scorer, so
    # it must be DROPPED from the mean rather than averaged in as an earned mark. See the
    # REWARD_FORMULA rationale in spec.py for the measured corpus shares (NF free on 46.2% of
    # tasks, PQ on 66.7%, both on 29.6%).
    #
    # MS and PQ validity are properties of the task; NF validity is a property of the run,
    # because truths the contestant never computed also leave the denominator.
    ms_valid = (_int(len(ms.get("hit") or ())) + _int(len(ms.get("miss") or ()))) > 0
    nf_valid = (_int(nf_summary.get("passed")) + _int(nf_summary.get("failed"))) > 0
    pq_valid = (_int(pq.get("points_total")) + _int(pq.get("order_total"))) > 0
    # Precision's denominator is what the contestant ATTEMPTED, so like NF this is a property of
    # the run: a trace that attempted nothing scores a free 1.0 and must be dropped, not imputed.
    ms_precision = _clamp01(_finite(ms.get("precision")))
    msp_valid = len(ms.get("attempted") or ()) > 0

    measured = [v for v, ok in ((ms_recall, ms_valid), (ms_precision, msp_valid),
                                (nf_ratio, nf_valid), (pq_score, pq_valid)) if ok]
    # No axis measurable: do not award a perfect score for having asked nothing. No task in the
    # shipped build reaches this (MS is measurable on 372/372), but a future one might.
    competence = _harmonic(*measured) if measured else 0.0

    # ---- gates applied OUTSIDE the competence mean (spec.REWARD_FORMULA).
    #
    # Misuse is proportional rather than binary on purpose: running one inadmissible method
    # among twenty is a different act from running twelve. It is judged against each method's
    # declared `applicability` in the taxonomy -- deterministic, and unrelated to the fabrication
    # estimator that ships disabled.
    ms_misuse = _clamp01(_finite(ms.get("misuse_rate")))
    # Using data the steward DENIED is disqualifying, not proportional: the denial is the task.
    hard_violation = any(
        isinstance(v, dict) and v.get("kind") == "denied_data_used"
        for v in (audit.get("gate_violations") or ())
    )
    gate_hard_passed = 0 if hard_violation else 1
    reward_value = competence * (1.0 - ms_misuse) * gate_hard_passed

    # ------------------------------------------------------------------ autonomy/efficiency
    # `steward-audit.jsonl` is written by the HARNESS; `trace.json` is written by the
    # CONTESTANT. The ledger therefore wins outright, and the self-report is kept beside it
    # rather than over it -- an under-report is itself a measurement and must stay auditable.
    # See spec.AE_AXIS_SOURCE for the six-model table that forced this inversion, and
    # `test_ae_axis_is_never_gating` for the guarantee that none of it reaches the reward.
    reported = max(0, _int(trace_turns))
    ledger_valid = bool(audit.get("ledger_valid"))
    interaction_turns = max(0, _int(audit.get("interaction_turns")))
    # Lines the steward wrote that we could not classify. They are still evidence that an
    # interaction happened, so they raise the floor instead of vanishing from the count.
    unparsable = max(0, _int(audit.get("records_unparsable")))

    if ledger_valid:
        ae_turns = interaction_turns + unparsable
    else:
        # No usable ledger (absent, empty, or every line malformed). Fall back to the
        # contestant's own number -- floored by the lines we could see but not parse -- so
        # that the original guarantee holds in this direction too: a missing or corrupt audit
        # must not make an expensive run look free.
        ae_turns = max(reported, unparsable)

    reward = {
        "reward": _clamp01(reward_value),           # spec.REWARD_FORMULA
        "competence": competence,
        "ms_recall": ms_recall,
        "ms_precision": ms_precision,
        "ms_misuse": ms_misuse,
        "ms_axis_valid": 1 if ms_valid else 0,
        "ms_precision_axis_valid": 1 if msp_valid else 0,
        "gate_violation_count": _int(audit.get("gate_violation_count")),
        "gate_hard_passed": gate_hard_passed,
        "nf": nf_ratio,
        "nf_checked": _int(nf_summary.get("checked")),
        "nf_passed": _int(nf_summary.get("passed")),
        "nf_failed": _int(nf_summary.get("failed")),
        "nf_axis_valid": 1 if nf_valid else 0,
        "pq": pq_score,
        "pq_points_total": _int(pq.get("points_total")),
        "pq_order_violations": _int(pq.get("order_violations")),
        "pq_axis_valid": 1 if pq_valid else 0,
        "hn_fabrication_rate": _clamp01(_finite(hn.get("fabrication_rate"))),
        "hn_misreport_rate": _clamp01(_finite(hn.get("misreport_rate"))),
        # 1 when there is no fault probe, matching the TGS gate's "no probe => no penalty".
        "hn_fault_passed": 1 if (not isinstance(fault, dict) or fault.get("passed")) else 0,
        "ae_turns": max(0, _int(ae_turns)),
        "ae_provision_turns": max(0, _int(audit.get("provision_turns"))),
        "ae_interaction_turns": interaction_turns,
        "ae_turns_reported": reported,
        # Signed on purpose: negative means the contestant claimed fewer turns than the
        # steward recorded. That gap is the thing the old precedence silently rewarded.
        "ae_turns_divergence": reported - max(0, _int(ae_turns)),
        "ae_ledger_valid": 1 if ledger_valid else 0,
        "ae_interventions": max(0, _int(trace_interventions)),
        # DIAGNOSTIC. Never multiplied in, never averaged in -- see spec.SC_AXIS.
        "sc": _clamp01(_finite(sc.get("sc"))) if sc else 0.0,
        "sc_points_total": _int(sc.get("sc_points_total")),
        "sc_axis_valid": 1 if sc.get("axis_valid") else 0,
        "tgs_legacy": _clamp01(_finite(card.get("tgs"))),
        "honesty_axis_valid": 0,   # see the REWARD_FORMULA rationale in spec.py
    }
    return _coerce_reward(reward)


def _coerce_reward(reward: dict) -> dict:
    """Force exactly spec.REWARD_KEYS, all finite int/float, booleans as 0/1."""
    out: dict[str, float | int] = {}
    for key in spec.REWARD_KEYS:
        v = reward.get(key, 0)
        if isinstance(v, bool):
            out[key] = int(v)
        elif isinstance(v, int):
            out[key] = v
        else:
            out[key] = _finite(v)
    return out


def zero_reward() -> dict:
    return _coerce_reward({k: 0 for k in spec.REWARD_KEYS})


# --------------------------------------------------------------------------- orchestration

class _Timeout(Exception):
    pass


def _install_alarm(seconds: int):
    try:
        import signal

        def _fire(signum, frame):  # pragma: no cover - timing dependent
            raise _Timeout(f"scoring exceeded {seconds}s")

        signal.signal(signal.SIGALRM, _fire)
        signal.alarm(seconds)
        return lambda: signal.alarm(0)
    except Exception:  # pragma: no cover - non-POSIX or restricted sandbox
        return lambda: None


def score(truth_file: str, artifacts_dir: str) -> tuple[dict, dict]:
    """Do the actual work. Returns (reward, scorecard). Raises only on unusable truth."""
    warnings: list[str] = []
    truth = load_truth(truth_file)          # TruthError propagates: truly unscoreable
    task = build_task(truth)

    # Harbor re-materialises each [[artifacts]] entry at its ORIGINAL `source` path inside the
    # separate verifier, not under the conventional artifacts dir (see
    # spec.artifact_candidates for the citation and the debugging story). Resolve source-first,
    # then the convention, so a real `harbor run`, a shared-mode verifier and a hand-run
    # container all work.
    def _resolve(source: str, destination: str) -> str:
        # `artifacts_dir` is passed through rather than read from spec: the tests and a
        # hand-run container point it elsewhere, and the constant would ignore them.
        candidates = spec.artifact_candidates(source, destination, artifacts_dir)
        for path in candidates:
            if os.path.exists(path):
                return path
        return candidates[-1]          # name the conventional path in the "missing" warning

    _by_dest = {dest: src for src, dest in spec.COLLECTED_ARTIFACTS}
    trace_path = _resolve(_by_dest.get("trace.json", ""), "trace.json")
    report_path = _resolve(_by_dest.get("report.md", ""), "report.md")
    audit_path = _resolve(_by_dest.get("steward-audit.jsonl", ""), "steward-audit.jsonl")

    raw_trace, w = _load_json(trace_path, MAX_TRACE_BYTES)
    warnings += w
    schema_errors = validate_trace_schema(raw_trace) if raw_trace is not None else \
        ["trace_absent_or_unparsable"]
    trace_dict, w = sanitize_trace(raw_trace)
    warnings += w

    report_text, w = _read_text(report_path, MAX_REPORT_BYTES)
    warnings += w
    report_text, w = sanitize_report(report_text)
    warnings += w

    audit_text, w = _read_text(audit_path, MAX_AUDIT_BYTES)
    warnings += [x for x in w if not x.startswith("missing:")]  # no steward => no cost, fine
    audit_records, audit_stats = parse_audit(audit_text)

    if trace_dict["task_id"] not in ("unknown", task.task_id):
        warnings.append(f"task_id_mismatch:trace={trace_dict['task_id']}:truth={task.task_id}")

    from dmaic_bench import taxonomy as taxonomy_mod
    from dmaic_bench.core.models import trace_from_dict
    from dmaic_bench.scoring import scorer

    trace = trace_from_dict(trace_dict)
    y_type = truth.get("y_type")
    if y_type not in ("continuous", "attribute_proportion", "attribute_count_rate", "mixed"):
        if y_type is not None:
            warnings.append(f"unknown_y_type:{y_type}")
        y_type = "continuous"

    card = scorer.score_run(task, trace, report_text, taxonomy_mod.load(), y_type=y_type)

    sc = v2_self_consistency(truth, trace)
    if sc:
        card["sc"] = sc
        recomputed = [p["point_id"] for p in v2_decision_points(truth)]
        declared_route = [str(n) for n in _as_list(_as_dict(truth.get("v2")).get("oracle_route"))]
        if declared_route and recomputed and recomputed[0] not in declared_route:
            # An audit cross-check, never a source of truth: the branch is always the recomputed
            # one. A mismatch means the package's own record of the walk disagrees with its
            # graph, which is a build defect worth surfacing.
            warnings.append("v2_oracle_route_disagrees_with_recomputed_walk")

    known = set(taxonomy_mod.load().methods)
    unknown_methods = sorted(trace.attempted_methods() - known)
    if unknown_methods:
        warnings.append(f"unknown_method_ids:{len(unknown_methods)}")

    audit = audit_summary(audit_records, audit_stats, task, truth, trace.successful_methods())
    reward = build_reward(card, audit, trace.turns, trace.interventions)

    scorecard = {
        "schema": SCORECARD_SCHEMA,
        "task_id": task.task_id,
        "case_id": task.case_id,
        "tier": task.tier,
        "variant": task.variant,
        "seed": task.seed,
        "phase": task.phase,
        "y_type": y_type,
        # The ROUTING shape and the tier it implies. `tier` above is the harbor task tier (T3
        # for every v2 project) and says nothing about difficulty; the routing tier is the axis
        # every difficulty result is reported over, and it was reachable only by re-deriving it
        # from the registry, so a job tree was not self-describing on the one number that
        # matters. Written here rather than into task.toml on purpose: a shape names the finding
        # outright ("gauge-unacceptable"), and the scorecard is produced by the verifier in its
        # own container, after the agent is gone.
        "shape": _as_dict(truth.get("v2")).get("shape") or "",
        "routing_tier": _routing_tier(_as_dict(truth.get("v2")).get("shape")),
        "system_id": trace.system_id,
        "truth_package_version": truth.get("package_version"),
        "data_fingerprint": truth.get("data_fingerprint"),
        "reward": reward,
        "reward_formula": spec.REWARD_FORMULA,
        "scorecard": card,
        "autonomy": audit,
        "validation": {
            "trace_schema_valid": not schema_errors,
            "trace_schema_errors": schema_errors,
            "unknown_method_ids": unknown_methods[:100],
            "warnings": warnings,
            "report_chars": len(report_text),
            "trace_steps": len(trace.steps),
        },
        "notes": [
            "reward = harmonic_mean(ms_recall, nf, pq); tgs_legacy is the paper's published "
            "aggregate and is NOT the headline (honesty_axis_valid = 0).",
            "ae_* is a DIAGNOSTIC column and never enters the reward. ae_turns and "
            "ae_interaction_turns come from the steward ledger; ae_turns_reported is the "
            "contestant's own claim, kept so ae_turns_divergence stays auditable. "
            "ae_ledger_valid = 0 means no usable ledger and ae_turns fell back to the trace.",
        ],
    }
    return reward, scorecard


def _write_json(path: str, payload: dict) -> None:
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=False,
                  allow_nan=False)
        fh.write("\n")
    os.replace(tmp, path)


def run(truth_file: str, artifacts_dir: str, reward_path: str,
        scorecard_path: str) -> int:
    """Score, then write reward + scorecard. Returns a process exit code; never raises."""
    cancel = _install_alarm(SCORE_TIMEOUT_S)
    error: str | None = None
    try:
        reward, scorecard = score(truth_file, artifacts_dir)
        rc = spec.EXIT_OK
    except BaseException as exc:  # noqa: BLE001 - an unscored trial is worse than a zero
        error = f"{type(exc).__name__}: {exc}"
        reward = zero_reward()
        scorecard = {
            "schema": SCORECARD_SCHEMA,
            "error": error,
            "traceback": traceback.format_exc(limit=30)[:8000],
            "reward": reward,
            "reward_formula": spec.REWARD_FORMULA,
            "validation": {"warnings": ["verifier_error"]},
        }
        rc = spec.EXIT_VERIFIER_ERROR
        print(f"[dmaic-verify] ERROR {error}", file=sys.stderr)
    finally:
        cancel()

    try:
        _write_json(scorecard_path, scorecard)
    except Exception as exc:  # pragma: no cover - defensive
        print(f"[dmaic-verify] could not write scorecard: {exc}", file=sys.stderr)
    try:
        _write_json(reward_path, reward)
    except Exception as exc:  # pragma: no cover - test.sh owns the last-resort fallback
        print(f"[dmaic-verify] could not write reward: {exc}", file=sys.stderr)
        return spec.EXIT_VERIFIER_ERROR

    print(json.dumps(reward, ensure_ascii=False, sort_keys=True))
    if error is None:
        print(f"[dmaic-verify] ok reward={reward['reward']:.4f} "
              f"ms_recall={reward['ms_recall']:.3f} nf={reward['nf']:.3f} "
              f"pq={reward['pq']:.3f}", file=sys.stderr)
    return rc


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    truth_file = os.environ.get("DMAIC_TRUTH_FILE", spec.VERIFIER_TRUTH_FILE)
    artifacts_dir = os.environ.get("DMAIC_ARTIFACTS_DIR", spec.ARTIFACTS_DIR)
    reward_path = os.environ.get("DMAIC_REWARD_JSON", spec.REWARD_JSON)
    scorecard_path = os.environ.get("DMAIC_SCORECARD_JSON", spec.SCORECARD_JSON)

    # Positional overrides keep the container invocation and the test harness identical.
    for i, arg in enumerate(argv):
        if i == 0:
            truth_file = arg
        elif i == 1:
            artifacts_dir = arg
        elif i == 2:
            reward_path = arg
        elif i == 3:
            scorecard_path = arg

    return run(truth_file, artifacts_dir, reward_path, scorecard_path)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
