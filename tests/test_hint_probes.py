"""A hint probe must change the brief and nothing else, and must not contain the answer.

The probe exists to tell a hard task from a broken one. Nine tasks in this corpus were once
reported as difficulty and were unscoreable; the hint approach is the instrument that would have
separated those cases while the campaign was running instead of after it.

For the instrument to mean anything, three things have to hold:

* the hinted instance is a SEPARATE task, and grades exactly what the plain one grades — a probe
  that also moved the truth would be measuring two changes at once;
* no rung hands over a value from the seed's own results or a private graph key; and
* every rung ships a written calibration rationale, because altitude is human judgement and an
  un-argued hint is not evidence of anything.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                          # noqa: E402

from dmaic_bench.core.graph import walk                # noqa: E402
from dmaic_bench.v2 import hints, registry             # noqa: E402
from dmaic_harbor import v2_tasks                      # noqa: E402

CASES = registry.discover()
TARGETS = [(pid, cid, seed)
           for pid, probe in hints.PROBES.items()
           for cid, seed in probe["targets"]]


def test_every_probe_targets_tasks_that_exist_and_still_have_the_shape_it_describes():
    for pid, cid, seed in TARGETS:
        case = CASES[cid]
        assert seed in case.seeds, f"{pid} targets {cid} seed {seed}, which is not shipped"
        _blocks, res = case.generate(seed)
        msa = res.get("msa") or {}
        assert msa.get("pctSV", 1.0) <= 0.30 and msa.get("ndc", 99) < 5, (
            f"{cid} seed {seed} no longer puts the gauge under the headline screen with too "
            f"few distinct categories; the probe's observation is stale")
        assert hints.PROBES[pid]["point"] in walk(case.graph, res), (
            "the probe names a decision point the oracle route does not pass through")


@pytest.mark.parametrize("rung", hints.RUNGS)
def test_no_rung_hands_over_a_value_from_the_seeds_own_results(rung):
    for pid, cid, seed in TARGETS:
        problems = hints.check_hint(hints.hint_text(pid, rung), CASES[cid], seed)
        assert not problems, f"{pid}{rung} on {cid} seed {seed}: {problems}"


def test_the_giveaway_guard_actually_catches_a_giveaway():
    """The guard is mechanical and cannot judge altitude; this is what it CAN do, demonstrated.

    Note what it does not catch: rung L2 is over-specified in substance — it names the quantity
    and its threshold in words — and passes cleanly, because no number from the results appears
    in it. Numeric leakage and conceptual over-specification are different failures and only the
    first is machine-checkable. The second is what the rationale field is for.
    """
    case = CASES["adb_c30"]
    _blocks, res = case.generate(4)
    ndc = res["msa"]["ndc"]
    assert hints.check_hint(f"The study resolves only {ndc} groups.", case, 4)
    assert hints.check_hint("Look again at M_msa before proceeding.", case, 4)
    assert not hints.check_hint("Think about what the standard asks.", case, 4)


@pytest.mark.parametrize("rung", hints.RUNGS)
def test_every_rung_has_a_written_calibration_rationale(rung):
    for pid, probe in hints.PROBES.items():
        assert probe["rationale"].get(rung, "").strip(), (
            f"{pid}{rung} ships no rationale; altitude is human judgement and an un-argued "
            "hint is not evidence")


def test_a_probe_declares_the_mode_it_is_testing_and_the_taxonomy_knows_it():
    from dmaic_harbor import failure_modes as FM
    for pid, probe in hints.PROBES.items():
        assert probe["failure_mode"] in FM.MODES, (
            f"{pid} claims to validate {probe['failure_mode']!r}, which is not a failure mode")
        for field in ("observation", "hypothesis"):
            assert probe[field].strip(), f"{pid} has no {field}"


@pytest.mark.parametrize("rung", hints.RUNGS)
def test_the_hinted_instance_grades_exactly_what_the_plain_one_grades(rung):
    """A probe that also moved the truth would confound the hint with a second change."""
    for _pid, cid, seed in TARGETS:
        case = CASES[cid]
        plain = v2_tasks.build_task(case, seed, language="en")
        hinted = v2_tasks.build_task(case, seed, language="en", hint=("hp01", rung))
        dump = lambda x: json.dumps(x, sort_keys=True, default=str)   # noqa: E731
        assert dump(hinted.stages) == dump(plain.stages)
        assert dump(hinted.truths) == dump(plain.truths)
        assert hinted.task_id != plain.task_id, "a hinted run must not pool with a plain one"
        assert hinted.goal.startswith(plain.goal) and len(hinted.goal) > len(plain.goal)


def test_the_over_specified_control_is_excluded_from_reportable_results():
    assert "L2" not in hints.REPORTABLE_RUNGS
    assert set(hints.REPORTABLE_RUNGS) < set(hints.RUNGS)


def test_an_unknown_probe_or_rung_is_an_error_not_a_silent_no_hint():
    with pytest.raises(KeyError):
        hints.hint_text("hp99", "L1")
    with pytest.raises(KeyError):
        hints.hint_text("hp01", "L9")
