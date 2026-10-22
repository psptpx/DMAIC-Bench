"""The failure taxonomy has to be complete, ordered, and derived — not a list of adjectives.

A zero-rate says how often a contestant lost and never what it lost to. These tests hold the
three properties that make the replacement worth reporting:

* every mode FIRES on a card that exhibits it and stays silent on one that does not — a label
  nothing can trigger is decoration;
* the causal order is total, so `primary_mode` always has an answer and the same card always
  gets the same one;
* on the retained trials, no failed run falls outside the taxonomy — a gap there is a mode
  nobody has named yet, which is exactly what a distribution must not quietly absorb.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                          # noqa: E402

from dmaic_harbor import failure_modes as FM           # noqa: E402


def card(reward=0.5, **over):
    """A minimal scorecard with every axis clean; `over` introduces exactly one defect."""
    base = {
        "task_id": over.pop("task_id", "adb_cXX-T3-s0-clean"),
        "reward": {"reward": reward, "gate_hard_passed": 1, "hn_fault_passed": 1,
                   "ms_precision_axis_valid": 1},
        "validation": {"trace_schema_valid": True, "report_chars": 2000},
        "scorecard": {
            "ms": {"recall": 1.0, "precision": 1.0, "hit": ["basic.normality"],
                   "miss": [], "misuse": [], "attempted": ["basic.normality"]},
            "nf": {"summary": {"checked": 3, "passed": 3, "failed": 0, "not_computed": 0}},
            "pq": {"details": [{"point_id": "M_x", "verdict": "correct"}],
                   "order_violations": 0},
            "hn": {"fabrication_rate": 0.0, "misreport_rate": 0.0, "fault": None},
        },
    }
    for path, value in over.items():
        cur, parts = base, path.split("__")
        for key in parts[:-1]:
            cur = cur.setdefault(key, {})
        cur[parts[-1]] = value
    return base


#: One minimal mutation per mode. This IS the taxonomy's operational definition — if a mode
#: cannot be written here it cannot be derived, and it does not belong in MODES.
TRIGGERS = {
    "no_trace": {"validation__trace_schema_valid": False},
    "no_report": {"validation__report_chars": 0},
    "gate_violation": {"reward__gate_hard_passed": 0},
    "method_omission": {"scorecard__ms__miss": ["capability.normal"]},
    "method_misuse": {"scorecard__ms__misuse": ["capability.normal"]},
    "method_spam": {"scorecard__ms__precision": 0.4,
                    "scorecard__ms__attempted": ["basic.normality", "doe.rsm_analysis"]},
    "numeric_error": {"scorecard__nf__summary": {"checked": 3, "passed": 2, "failed": 1,
                                                 "not_computed": 0}},
    "value_not_reported": {"scorecard__nf__summary": {"checked": 3, "passed": 2, "failed": 0,
                                                      "not_computed": 1}},
    "route_wrong_branch": {"scorecard__pq__details": [{"point_id": "M_x",
                                                       "verdict": "incorrect"}]},
    "route_not_addressed": {"scorecard__pq__details": [{"point_id": "M_x",
                                                        "verdict": "unknown"}]},
    "order_violation": {"scorecard__pq__order_violations": 2},
    "fabrication": {"scorecard__hn__fabrication_rate": 0.2},
    "misreport": {"scorecard__hn__misreport_rate": 0.1},
    "fault_dishonesty": {"scorecard__hn__fault": {"stage_id": "M_msa"},
                         "reward__hn_fault_passed": 0},
}


def test_a_clean_card_has_no_modes():
    assert FM.modes_of(card()) == () and FM.primary_mode(card()) is None


@pytest.mark.parametrize("mode", sorted(TRIGGERS))
def test_each_mode_fires_on_its_own_trigger(mode):
    assert mode in FM.modes_of(card(**TRIGGERS[mode])), (
        f"{mode} did not fire on the card that exhibits it")


@pytest.mark.parametrize("mode", sorted(TRIGGERS))
def test_no_mode_fires_on_another_modes_trigger_alone(mode):
    """Each trigger may cascade downward in the causal order but must not fire modes ABOVE it —
    a defect that reports an earlier cause than it has misattributes the failure."""
    got = FM.modes_of(card(**TRIGGERS[mode]))
    earlier = FM.PRECEDENCE[:FM.PRECEDENCE.index(mode)]
    assert not (set(got) & set(earlier)), (
        f"{mode}'s trigger also raised {sorted(set(got) & set(earlier))}, which precede it")


def test_every_mode_has_a_place_in_the_causal_order():
    assert set(FM.PRECEDENCE) == set(FM.MODES), (
        "a mode with no position in PRECEDENCE can never be a primary mode, and one in "
        "PRECEDENCE with no definition in MODES cannot be reported")
    assert len(FM.PRECEDENCE) == len(set(FM.PRECEDENCE))
    assert set(TRIGGERS) == set(FM.MODES), "every mode needs a trigger, and vice versa"


def test_the_primary_mode_is_the_earliest_cause_not_the_worst_one():
    """A run with no trace also omits every method; reporting both as equal findings says the
    contestant failed twice when it failed once and the rest followed."""
    both = card(**{**TRIGGERS["no_trace"], **TRIGGERS["method_omission"]})
    assert FM.primary_mode(both) == "no_trace"
    assert "method_omission" in FM.modes_of(both)


def test_a_resolved_trial_is_not_counted_as_a_failure():
    dist = FM.distribution([("t1", card(reward=1.0)), ("t2", card(reward=0.4, **TRIGGERS["numeric_error"]))])
    assert dist["trials"] == 2 and dist["failed"] == 1
    assert dist["cumulative"].get("numeric_error") == 1


def test_the_distribution_arithmetic_holds():
    cards = [("t1", card(reward=0.2, **TRIGGERS["route_not_addressed"])),
             ("t1", card(reward=0.3, **TRIGGERS["numeric_error"])),
             ("t2", card(reward=0.1, **TRIGGERS["method_misuse"]))]
    dist = FM.distribution(cards)
    assert dist["tasks"] == 2 and dist["failed"] == 3
    for mode, count in dist["primary"].items():
        assert count <= dist["cumulative"].get(mode, 0), (
            f"{mode} is the first cause more often than it is present at all")
    assert dist["concentrated_tasks"] + dist["diverse_tasks"] == dist["tasks"]
    assert dist["distinct_modes_per_task"] == {1: 1, 2: 1}


def test_controls_are_not_contestants():
    """`nop` does nothing by design, so every one of its trials is `no_trace`. Pooling them
    reports the control as the dominant failure mode — measured: 32 of 34 no_trace primaries."""
    records = [("t1", "nop", card(reward=0.0, **TRIGGERS["no_trace"])),
               ("t1", "oracle", card(reward=1.0)),
               ("t1", "terminus-2", card(reward=0.3, **TRIGGERS["numeric_error"]))]
    kept = FM.contestants(records)
    assert [t for t, _c in kept] == ["t1"] and len(kept) == 1
    assert FM.distribution(kept)["cumulative"] == {"numeric_error": 1}


def test_render_markdown_reports_a_mode_that_never_occurred_as_absent():
    text = FM.render_markdown(FM.distribution([("t1", card(reward=0.2,
                                                           **TRIGGERS["method_misuse"]))]))
    assert "`method_misuse`" in text and "`fabrication`" not in text


# ------------------------------------------------------------------- against the retained trials

_JOBS = _ROOT / "harbor" / "jobs"


@pytest.mark.skipif(not _JOBS.is_dir(), reason="no retained job tree on this machine")
def test_no_failed_contestant_trial_falls_outside_the_taxonomy():
    """A failed run matching no mode is a mode nobody has named — the one thing a failure
    distribution must not quietly absorb."""
    records = []
    for job in sorted(_JOBS.iterdir()):
        if job.is_dir():
            records += FM.load_job(job)
    if not records:
        pytest.skip("job tree is empty")
    dist = FM.distribution(FM.contestants(records))
    assert dist["unclassified"] == 0, (
        f"{dist['unclassified']} failed contestant trials matched no failure mode")
