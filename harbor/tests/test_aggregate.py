"""Aggregation: a crash is not a zero, and tokens are not dollars.

Both defects tested here are silent by construction -- they publish a plausible number
rather than an error -- so the tests are written as the counterfactual: build a campaign
containing exactly the failure, aggregate it, and assert that the published figure is not
the one the naive reading produces.
"""
from __future__ import annotations

import json

import pytest

from dmaic_harbor import aggregate, spec

# The campaign-directory builder lives with the supervisor tests, which own the shape of a
# trial directory. Sharing it keeps one definition of "what the framework writes", so a
# drift in that shape breaks both suites at once instead of silently passing one of them.
from test_supervisor import make_trial


def build_campaign(root, spec_rows):
    """``spec_rows`` = list of dicts passed through to :func:`make_trial`."""
    job = root / "jobs" / "main"
    job.mkdir(parents=True, exist_ok=True)
    (job / "config.json").write_text(json.dumps({"job_name": "main"}), encoding="utf-8")
    for i, row in enumerate(spec_rows):
        make_trial(job, f"trial-{i}", **row)
    return root / "jobs"


# ============================================================ a crash is not a zero

def test_a_verifier_crash_is_excluded_not_averaged_in_as_zero(tmp_path):
    """THE defect. The crash fallback writes `reward.json` with every axis at zero and
    marks `scorecard.json` with an error. Reading only `reward.json` -- which is what the
    previous aggregation did -- makes that indistinguishable from a genuine zero."""
    jobs = build_campaign(tmp_path, [
        {"reward": 1.0}, {"reward": 1.0}, {"reward": 1.0},
        {"kind": "verifier_error"},
    ])
    summary = aggregate.summarize(aggregate.collect(jobs))
    row = summary["contestant-a"]

    assert row["n_trials"] == 4
    assert row["n_scored"] == 3
    assert row["n_excluded"] == 1
    assert row["excluded_kinds"] == {"verifier_error": 1}
    # The naive reading is mean(1,1,1,0) = 0.75. The correct one is mean(1,1,1) = 1.0.
    assert row["metrics"]["reward"]["mean"] == pytest.approx(1.0)
    assert row["metrics"]["reward"]["n"] == 3


def test_the_crash_reason_is_carried_through_so_a_recurring_bug_is_visible(tmp_path):
    """One crash is bad luck. The same exception across contestants is a harness bug, and
    an aggregate that reports only a count cannot tell you which you have."""
    jobs = build_campaign(tmp_path, [{"reward": 0.8}] * 10 + [{"kind": "verifier_error"}])
    row = aggregate.summarize(aggregate.collect(jobs))["contestant-a"]
    assert row["verifier_errors"] == ["ValueError: truth package is malformed"]


def test_a_genuine_zero_is_kept_and_lowers_the_mean(tmp_path):
    """The other half of the contract. Excluding real zeros would be the opposite -- and
    equally wrong -- error."""
    jobs = build_campaign(tmp_path, [{"reward": 1.0}, {"reward": 1.0},
                                     {"reward": 0.0}, {"reward": 0.0}])
    row = aggregate.summarize(aggregate.collect(jobs))["contestant-a"]
    assert row["n_excluded"] == 0
    assert row["metrics"]["reward"]["mean"] == pytest.approx(0.5)


def test_every_kind_of_missing_verdict_is_excluded_and_counted_by_kind(tmp_path):
    jobs = build_campaign(tmp_path, [
        {"reward": 0.9}, {"reward": 0.9},
        {"kind": "verifier_error"},
        {"kind": "no_reward"},
        {"kind": "trial_exception"},
    ])
    row = aggregate.summarize(aggregate.collect(jobs))["contestant-a"]
    assert row["n_scored"] == 2 and row["n_excluded"] == 3
    assert row["excluded_kinds"] == {"no_reward": 1, "verifier_error": 1,
                                     "trial_exception": 1}
    assert row["excluded_rate"] == pytest.approx(0.6)
    assert row["exceptions"] == ["TimeoutError"]


def test_exclusions_are_reported_per_model_because_they_are_not_evenly_distributed(tmp_path):
    """The bias argument, made concrete: contestant-b hit infrastructure problems and
    contestant-a did not. Averaging b's crashes in as zeros would penalise b for the
    harness. The exclusions must be visible per row, not folded into a campaign total."""
    job = tmp_path / "jobs" / "main"
    job.mkdir(parents=True)
    (job / "config.json").write_text("{}", encoding="utf-8")
    for i in range(6):
        make_trial(job, f"a{i}", model="contestant-a", reward=0.6)
    for i in range(3):
        make_trial(job, f"b{i}", model="contestant-b", reward=0.6)
    for i in range(3):
        make_trial(job, f"bx{i}", model="contestant-b", kind="verifier_error")

    summary = aggregate.summarize(aggregate.collect(tmp_path / "jobs"))
    assert summary["contestant-a"]["n_excluded"] == 0
    assert summary["contestant-b"]["n_excluded"] == 3
    # Both means are 0.6; without the exclusion b would read 0.30 and look half as good.
    assert summary["contestant-a"]["metrics"]["reward"]["mean"] == pytest.approx(0.6)
    assert summary["contestant-b"]["metrics"]["reward"]["mean"] == pytest.approx(0.6)


def test_the_rendered_table_shows_the_exclusions_and_says_why(tmp_path):
    """An exclusion the reader cannot see is a silent correction, which is its own
    problem: the reader has no way to know the denominator moved."""
    jobs = build_campaign(tmp_path, [{"reward": 1.0}] * 3 + [{"kind": "verifier_error"}])
    md = aggregate.to_md(aggregate.summarize(aggregate.collect(jobs)))
    assert "excluded" in md
    assert "verifier_error:1" in md
    assert "missing observation" in md


def test_campaign_totals_report_the_overall_loss_rate(tmp_path):
    jobs = build_campaign(tmp_path, [{"reward": 0.5}] * 8 + [{"kind": "no_reward"}] * 2)
    totals = aggregate.campaign_totals(aggregate.collect(jobs))
    assert totals == {
        "n_trials": 10, "n_scored": 8, "n_excluded": 2, "excluded_rate": 0.2,
        "excluded_kinds": {"no_reward": 2}, "cost": totals["cost"]}


# ============================================================ cost

def test_tokens_are_reported_even_when_no_price_is_known(tmp_path):
    """9 of 11 contestants had a null `cost_usd`. Token counts were recorded for all of
    them, so tokens are the figure that exists."""
    jobs = build_campaign(tmp_path, [{"reward": 0.5, "tokens": (1000, 100)},
                                     {"reward": 0.5, "tokens": (2000, 200)}])
    cost = aggregate.summarize(aggregate.collect(jobs))["contestant-a"]["cost"]
    assert cost["tokens"]["n_input_tokens"]["sum"] == 3000
    assert cost["tokens"]["n_output_tokens"]["sum"] == 300
    assert cost["usd"]["n_priced"] == 0
    assert "UNPRICED" in cost["usd"]["note"]


def test_no_price_is_ever_invented_for_an_unpriced_model(tmp_path):
    jobs = build_campaign(tmp_path, [{"reward": 0.5}] * 4)
    cost = aggregate.summarize(aggregate.collect(jobs))["contestant-a"]["cost"]
    assert "sum_priced" not in cost["usd"]
    md = aggregate.to_md(aggregate.summarize(aggregate.collect(jobs)))
    assert "unpriced" in md and "$" not in md.split("**excluded**")[0]


def _price(trial, usd):
    result = json.loads((trial / "result.json").read_text())
    result["agent_result"]["cost_usd"] = usd
    (trial / "result.json").write_text(json.dumps(result), encoding="utf-8")


def test_a_partially_priced_model_is_reported_as_a_floor(tmp_path):
    """Summing only the priced subset understates the total by exactly the trials that
    could not be priced. Reporting that number unlabelled is the error; scaling it up to
    'fix' it would be a worse one."""
    jobs = build_campaign(tmp_path, [{"reward": 0.5}] * 4)
    job = tmp_path / "jobs" / "main"
    _price(job / "trial-0", 0.10)
    _price(job / "trial-1", 0.20)

    cost = aggregate.summarize(aggregate.collect(jobs))["contestant-a"]["cost"]
    assert cost["usd"]["sum_priced"] == pytest.approx(0.30)
    assert cost["usd"]["n_priced"] == 2
    assert cost["usd"]["priced_fraction"] == pytest.approx(0.5)
    assert cost["usd"]["is_floor"] is True
    assert "FLOOR" in cost["usd"]["note"]
    assert "(floor)" in aggregate.to_md(aggregate.summarize(aggregate.collect(jobs)))


def test_a_fully_priced_model_is_not_labelled_a_floor(tmp_path):
    jobs = build_campaign(tmp_path, [{"reward": 0.5}] * 2)
    job = tmp_path / "jobs" / "main"
    _price(job / "trial-0", 0.10)
    _price(job / "trial-1", 0.20)
    cost = aggregate.summarize(aggregate.collect(jobs))["contestant-a"]["cost"]
    assert cost["usd"]["is_floor"] is False
    assert "complete" in cost["usd"]["note"]


def test_cost_counts_trials_that_crashed_in_the_verifier(tmp_path):
    """A trial whose verifier crashed still burned the tokens the agent spent getting
    there. Excluding it from the SCORE and from the BUDGET are different decisions, and
    only the first one is right."""
    jobs = build_campaign(tmp_path, [{"reward": 0.5, "tokens": (1000, 100)},
                                     {"kind": "verifier_error", "tokens": (5000, 500)}])
    row = aggregate.summarize(aggregate.collect(jobs))["contestant-a"]
    assert row["n_scored"] == 1
    assert row["cost"]["tokens"]["n_input_tokens"]["sum"] == 6000


# ============================================================ collection

def test_metrics_are_derived_from_the_reward_contract_not_a_retyped_list():
    """A new axis must appear in the aggregate when it is added to the contract, not when
    someone remembers to retype it here."""
    assert aggregate.METRICS == tuple(spec.REWARD_KEYS)


def test_a_control_arm_is_kept_and_labelled_rather_than_dropped(tmp_path):
    """The control row is the one that says whether the pipeline itself is sound. It
    carries no model name, and an aggregate that drops it has discarded its own sanity
    check."""
    job = tmp_path / "jobs" / "main"
    job.mkdir(parents=True)
    trial = make_trial(job, "ctl")
    (trial / "config.json").write_text(json.dumps(
        {"agent": {}, "task": {"path": "/d/task-1"}}), encoding="utf-8")
    result = json.loads((trial / "result.json").read_text())
    result["agent_info"] = {"name": "oracle"}
    (trial / "result.json").write_text(json.dumps(result), encoding="utf-8")

    summary = aggregate.summarize(aggregate.collect(tmp_path / "jobs"))
    assert "<control:oracle>" in summary


def test_the_job_directory_is_not_counted_as_a_trial(tmp_path):
    jobs = build_campaign(tmp_path, [{"reward": 0.5}] * 3)
    assert len(aggregate.collect(jobs)) == 3


def test_bootstrap_is_deterministic_and_brackets_the_mean(tmp_path):
    xs = [0.1, 0.4, 0.6, 0.9, 1.0, 0.3, 0.7]
    lo, hi = aggregate.bootstrap_ci(xs)
    assert (lo, hi) == aggregate.bootstrap_ci(xs)
    assert lo <= sum(xs) / len(xs) <= hi


def test_bootstrap_of_a_single_observation_has_no_interval():
    assert aggregate.bootstrap_ci([0.5]) == (None, None)


def test_an_empty_campaign_exits_two_rather_than_printing_an_empty_table(tmp_path, capsys):
    assert aggregate.main([str(tmp_path)]) == 2
    assert "no trials found" in capsys.readouterr().err


def test_the_cli_writes_json_and_markdown(tmp_path):
    jobs = build_campaign(tmp_path, [{"reward": 0.5}] * 3 + [{"kind": "verifier_error"}])
    out, md = tmp_path / "r.json", tmp_path / "r.md"
    assert aggregate.main([str(jobs), "--out", str(out), "--md", str(md)]) == 0
    payload = json.loads(out.read_text())
    assert payload["campaign"]["n_excluded"] == 1
    assert payload["summary"]["contestant-a"]["n_scored"] == 3
    assert len(payload["trials"]) == 4
    assert "excluded" in md.read_text()
