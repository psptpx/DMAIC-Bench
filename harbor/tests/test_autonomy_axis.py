"""The autonomy/efficiency axis is derived from the STEWARD LEDGER, not from self-report.

`steward-audit.jsonl` is written by the harness; `trace.json` is written by the contestant.
The first release preferred `trace.turns` and consulted the ledger only when the trace was
missing or zero:

    ae_turns = trace_turns if trace_turns > 0 else audit_turns

The stated intent was that a missing trace must not make an expensive run look free. The
measured effect was the opposite. On ONE identical task (`adb_c03-t3-s1-clean`) across the
preserved 692-trial campaign, the models that scored 16-17 got that number *because* they
reported nothing and fell through to the ledger, while the models that reported a small
non-zero number kept it -- so under-reporting was strictly rewarded, and one system appeared
20x cheaper than another for reporting differently rather than behaving differently.

Terminal-Bench (arXiv 2601.11868v1, p. 21) records every cost figure harness-side and takes
nothing from agent self-report. This module pins the same rule here:

  * the ledger wins whenever it is usable, in BOTH directions (a smaller self-report cannot
    discount a run, a larger one cannot inflate it);
  * the self-report survives verbatim as `ae_turns_reported`, with `ae_turns_divergence`
    turning an under-report into a visible measurement instead of a silent discount;
  * two figures are published because they answer different questions -- `ae_provision_turns`
    (metered/billable) and `ae_interaction_turns` (requests + declares + provisions);
  * the original guarantee is preserved: no usable ledger falls back to the self-report,
    floored by the unparsable line count, so a corrupt audit cannot make a run look free;
  * and none of it may ever touch the reward -- Terminal-Bench measured turns/tokens as
    non-predictive of success (r = -0.028, p = 0.916, pp. 7 and 52).
"""
from __future__ import annotations

import glob
import json
import os
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.abspath(os.path.join(_HERE, os.pardir, "src")),
           os.path.abspath(os.path.join(_HERE, os.pardir, os.pardir)),
           _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dmaic_harbor import spec, verify                                     # noqa: E402
# Reuse the container-shaped layout helpers and the session task fixtures; importing the
# fixture functions binds them into this module's namespace so pytest resolves them here.
from test_verify import (DEFAULT_AUDIT, audit_lines, fw, layout,              # noqa: E402,F401
                         perfect_trace, run_verifier, tasks)

AE_KEYS = ("ae_turns", "ae_provision_turns", "ae_interaction_turns", "ae_turns_reported",
           "ae_turns_divergence", "ae_ledger_valid", "ae_interventions")


# --------------------------------------------------------------------------- unit helpers

def _card(**over):
    """A minimally scoreable scorecard; the AE axis does not depend on any of it."""
    card = {
        "ms": {"recall": 1.0, "precision": 1.0, "misuse_rate": 0.0, "hit": ["m"], "miss": []},
        "nf": {"summary": {"checked": 1, "passed": 1, "failed": 0, "ratio": 1.0}},
        "pq": {"score": 1.0, "points_total": 1, "order_total": 0, "order_violations": 0},
        "hn": {"fabrication_rate": 0.0, "misreport_rate": 0.0},
        "tgs": 1.0,
    }
    card.update(over)
    return card


def _ledger(*, request=0, declare=0, provision=0, status=0, provision_turns=0,
            unparsable=0, parsed=None):
    """An `audit_summary`-shaped dict, i.e. exactly what `build_reward` consumes."""
    by_action = {"request": request, "declare": declare, "provision": provision,
                 "status": status}
    if parsed is None:
        parsed = sum(by_action.values())
    return {
        "records_parsed": parsed,
        "records_unparsable": unparsable,
        "records_lines": parsed + unparsable,
        "ledger_valid": bool(parsed),
        "turns_by_action": by_action,
        "interaction_turns": request + declare + provision,
        "provision_turns": provision_turns,
        "free_requests": request,
    }


# --------------------------------------------------------------------------- contract

class TestContract:
    def test_every_ae_key_is_in_the_reward_contract(self):
        for key in AE_KEYS:
            assert key in spec.REWARD_KEYS, f"{key} missing from spec.REWARD_KEYS"

    def test_every_ae_key_is_in_the_test_sh_fallback_block(self):
        """`_coerce_reward` and test.sh's zero-reward heredoc must agree key for key."""
        body = open(os.path.join(_HERE, os.pardir, "templates", "verifier", "test.sh"),
                    encoding="utf-8").read()
        for key in AE_KEYS:
            assert f'"{key}"' in body, f"test.sh fallback reward is missing {key}"

    def test_build_reward_emits_all_ae_keys_as_finite_scalars(self):
        reward = verify.build_reward(_card(), _ledger(request=3), 0, 0)
        for key in AE_KEYS:
            assert key in reward
            assert isinstance(reward[key], (int, float)) and not isinstance(reward[key], bool)

    def test_spec_documents_the_ledger_as_the_source(self):
        # The reason the rule exists belongs next to the rule, not in a commit message.
        assert "steward-audit.jsonl" in spec.AE_AXIS_SOURCE
        assert "trace.turns" in spec.AE_AXIS_SOURCE


# --------------------------------------------------------------------------- precedence

class TestLedgerBeatsSelfReport:
    def test_a_small_self_report_cannot_discount_a_busy_ledger(self):
        """The measured failure: deepseek-v4-flash reported 1 against 20 req + 1 provision."""
        reward = verify.build_reward(_card(), _ledger(request=20, provision=1,
                                                      provision_turns=1), 1, 0)
        assert reward["ae_turns"] == 21
        assert reward["ae_interaction_turns"] == 21
        assert reward["ae_provision_turns"] == 1
        assert reward["ae_turns_reported"] == 1
        assert reward["ae_turns_divergence"] == -20      # under-reported by 20
        assert reward["ae_ledger_valid"] == 1

    def test_a_large_self_report_cannot_inflate_a_quiet_ledger(self):
        """Precedence is inversion, not a floor: the ledger wins in both directions."""
        reward = verify.build_reward(_card(), _ledger(request=2), 99, 0)
        assert reward["ae_turns"] == 2
        assert reward["ae_turns_reported"] == 99
        assert reward["ae_turns_divergence"] == 97

    def test_the_self_report_is_kept_not_overwritten(self):
        """Losing the ability to SEE an under-report would itself be a loss."""
        reward = verify.build_reward(_card(), _ledger(request=17), 0, 0)
        assert reward["ae_turns_reported"] == 0
        assert reward["ae_turns"] == 17
        assert reward["ae_turns_divergence"] == -17

    def test_reporting_zero_and_reporting_one_now_score_the_same(self):
        """The old rule's perverse incentive: `> 0` made claiming 1 better than claiming 0."""
        ledger = _ledger(request=17, provision=1, provision_turns=1)
        zero = verify.build_reward(_card(), ledger, 0, 0)
        one = verify.build_reward(_card(), ledger, 1, 0)
        assert zero["ae_turns"] == one["ae_turns"] == 18
        # ...and the difference between them survives, as a report, where it belongs.
        assert (zero["ae_turns_reported"], one["ae_turns_reported"]) == (0, 1)


class TestTheTwoFiguresAreDistinct:
    def test_metered_and_total_interaction_answer_different_questions(self):
        """Billable provisions vs. how often the steward was touched at all."""
        reward = verify.build_reward(
            _card(), _ledger(request=17, declare=2, provision=4, provision_turns=1), 0, 0)
        assert reward["ae_provision_turns"] == 1     # what the plant was charged
        assert reward["ae_interaction_turns"] == 23  # 17 + 2 + 4
        assert reward["ae_turns"] == 23

    def test_status_polls_are_free(self):
        """`status` reads the agent's own counters back and releases nothing."""
        assert verify.build_reward(_card(), _ledger(request=2, status=9), 0,
                                   0)["ae_interaction_turns"] == 2

    def test_refused_rows_still_count_as_interactions(self, tmp_path, fw):
        """Otherwise hammering a locked gate would be free."""
        truth = verify.truth_package_from_task(fw)
        rows = [{"seq": n, "action": "provision", "outcome": "refused", "stage_id": "I_CCD",
                 "refusal": "locked", "gate": "screening_significant"} for n in range(1, 6)]
        _, reward, card = run_verifier(layout(tmp_path, truth=truth, trace=perfect_trace(fw),
                                              report="", audit=audit_lines(rows)))
        assert reward["ae_interaction_turns"] == 5
        assert card["autonomy"]["turns_by_action"]["provision"] == 5


# --------------------------------------------------------------------------- degenerate

class TestDegenerateLedgers:
    """The original guarantee, in both directions: no audit must not mean no cost."""

    def test_no_audit_file_falls_back_to_the_self_report(self, tmp_path, fw):
        truth = verify.truth_package_from_task(fw)
        _, reward, card = run_verifier(layout(tmp_path, truth=truth, trace=perfect_trace(fw),
                                              report="", audit=None))
        assert reward["ae_ledger_valid"] == 0
        assert reward["ae_turns"] == 12          # perfect_trace claims 12
        assert reward["ae_turns_reported"] == 12
        assert reward["ae_turns_divergence"] == 0
        assert reward["ae_interaction_turns"] == 0
        assert card["autonomy"]["ledger_valid"] is False

    def test_empty_audit_file_falls_back_to_the_self_report(self, tmp_path, fw):
        truth = verify.truth_package_from_task(fw)
        _, reward, _ = run_verifier(layout(tmp_path, truth=truth, trace=perfect_trace(fw),
                                           report="", audit=""))
        assert reward["ae_ledger_valid"] == 0
        assert reward["ae_turns"] == 12

    def test_a_wholly_malformed_audit_is_floored_by_its_line_count(self, tmp_path, fw):
        """The direction the old comment was worried about, made real.

        Every line is garbage, so nothing parses and the ledger is unusable -- but the lines
        themselves are evidence that interactions happened, so a run whose trace claims 0
        cannot be scored free.
        """
        truth = verify.truth_package_from_task(fw)
        trace = perfect_trace(fw)
        trace["turns"] = 0
        audit = "not json\n{oops\n[]\n<html>\n{\"unterminated\":\n"
        _, reward, card = run_verifier(layout(tmp_path, truth=truth, trace=trace, report="",
                                              audit=audit))
        assert card["autonomy"]["records_parsed"] == 0
        assert card["autonomy"]["records_unparsable"] == 5
        assert reward["ae_ledger_valid"] == 0
        assert reward["ae_turns"] == 5, "unparsable ledger lines are still evidence of cost"
        assert reward["ae_turns_reported"] == 0

    def test_a_partly_malformed_audit_adds_the_unreadable_lines_to_the_floor(self, tmp_path,
                                                                             fw):
        truth = verify.truth_package_from_task(fw)
        audit = ("not json at all\n[]\n"
                 "{\"action\": \"provision\", \"granted\": true}\n\n{oops\n")
        _, reward, card = run_verifier(layout(tmp_path, truth=truth, trace=perfect_trace(fw),
                                              report="", audit=audit))
        assert card["autonomy"]["records_parsed"] == 1
        assert card["autonomy"]["records_unparsable"] == 3
        assert reward["ae_ledger_valid"] == 1
        assert reward["ae_interaction_turns"] == 1
        assert reward["ae_turns"] == 4          # 1 readable interaction + 3 unreadable lines

    def test_audit_present_but_trace_absent_is_still_charged(self, tmp_path, fw):
        """The case the old comment named -- and the only one it actually handled."""
        truth = verify.truth_package_from_task(fw)
        _, reward, _ = run_verifier(layout(tmp_path, truth=truth, trace=None, report="",
                                           audit=audit_lines(DEFAULT_AUDIT)))
        assert reward["ae_turns"] == 5
        assert reward["ae_turns_reported"] == 0
        assert reward["ae_ledger_valid"] == 1

    def test_neither_artifact_present_scores_zero_cost_but_says_so(self, tmp_path, fw):
        truth = verify.truth_package_from_task(fw)
        _, reward, _ = run_verifier(layout(tmp_path, truth=truth, trace=None, report="",
                                           audit=None))
        assert reward["ae_turns"] == 0
        assert reward["ae_ledger_valid"] == 0, "0 turns on no evidence must be distinguishable"

    def test_hostile_audit_field_types_cannot_break_the_axis(self):
        """`build_reward` is handed the audit summary; nothing in it may be trusted."""
        for hostile in ({}, {"ledger_valid": "yes", "interaction_turns": "many",
                             "records_unparsable": None, "provision_turns": [1]},
                        {"ledger_valid": True, "interaction_turns": -5,
                         "records_unparsable": -3, "provision_turns": -2}):
            reward = verify.build_reward(_card(), hostile, -7, -1)
            for key in AE_KEYS:
                assert reward[key] >= 0 or key == "ae_turns_divergence"
                assert isinstance(reward[key], int)


# --------------------------------------------------------------------------- non-gating

class TestNonGating:
    """Terminal-Bench: turns/tokens do not predict success (r = -0.028, p = 0.916)."""

    def test_no_ae_key_appears_in_the_reward_formula(self):
        assert "ae_" not in spec.REWARD_FORMULA

    def test_the_headline_is_invariant_under_every_autonomy_figure(self):
        baseline = verify.build_reward(_card(), _ledger(request=1), 1, 0)
        for ledger, turns, interventions in (
                (_ledger(), 0, 0),
                (_ledger(request=500, declare=90, provision=99, provision_turns=99), 0, 40),
                (_ledger(request=1, unparsable=1000), 99999, 7),
                ({}, 0, 0)):
            reward = verify.build_reward(_card(), ledger, turns, interventions)
            assert reward["reward"] == baseline["reward"]
            assert reward["competence"] == baseline["competence"]

    def test_a_cheap_run_and_an_expensive_run_score_identically(self, tmp_path, fw):
        """End to end, through the real verifier, not just through build_reward."""
        truth = verify.truth_package_from_task(fw)
        cheap = [{"seq": 1, "action": "request", "granted": True}]
        expensive = [{"seq": n, "action": "provision", "stage_id": "M_GRR", "granted": True}
                     for n in range(1, 40)]
        rewards = []
        for name, rows in (("cheap", cheap), ("expensive", expensive)):
            _, reward, _ = run_verifier(layout(tmp_path / name, truth=truth,
                                               trace=perfect_trace(fw), report="# Report\n",
                                               audit=audit_lines(rows)))
            rewards.append(reward)
        assert rewards[0]["ae_turns"] != rewards[1]["ae_turns"], "the axis must still measure"
        assert rewards[0]["reward"] == rewards[1]["reward"] == pytest.approx(1.0)

    def test_the_axis_is_reported_in_the_scorecard_for_diagnosis(self, tmp_path, fw):
        truth = verify.truth_package_from_task(fw)
        _, _, card = run_verifier(layout(tmp_path, truth=truth, trace=perfect_trace(fw),
                                         report="", audit=audit_lines(DEFAULT_AUDIT)))
        autonomy = card["autonomy"]
        assert autonomy["interaction_turns"] == 5
        assert autonomy["provision_turns"] == 2
        assert autonomy["ledger_valid"] is True
        assert autonomy["records_lines"] == 6


# --------------------------------------------------------------------------- real campaign

_CAMPAIGN = os.path.abspath(os.path.join(_HERE, os.pardir, "jobs"))

#: One preserved trial per model, all of the SAME task, from the 692-trial campaign. These
#: are the six rows that motivated the inversion. `jobs/` is run output and is gitignored, so
#: the check skips where the campaign was not preserved.
#:
#: The `adb_c03` in these names is NOT a corpus reference and must not be re-pointed at a
#: public case: they are the directory names of preserved RUN ARTIFACTS on disk, and the whole
#: point of the check is that the published table is recomputed from the very artifacts it was
#: published from. Nothing here loads a case, so this block is corpus-agnostic already and
#: works unchanged in a checkout without the held-out cases (docs/HELD_OUT.md) -- it is the
#: presence of `jobs/`, not of `adb_c03`, that decides whether it runs or skips.
_TRIALS = {
    "claude-opus-5":       "dmaic-adb_c03-t3-s1-clean__sn4Xgqt",
    "kimi-k3":             "dmaic-adb_c03-t3-s1-clean__JHQS3a6",
    "gemini-3.1-pro-high": "dmaic-adb_c03-t3-s1-clean__8ZtFuP2",
    "deepseek-v4-flash":   "dmaic-adb_c03-t3-s1-clean__96FSRnE",
    "gpt-5.6-sol":         "dmaic-adb_c03-t3-s1-clean__CjqdBtG",
    "glm-5.3":             "dmaic-adb_c03-t3-s1-clean__g8MVuf9",
}
_EXPECTED = {   # model -> (self-reported trace.turns, ledger-derived interaction turns)
    "claude-opus-5":       (0, 17),
    "kimi-k3":             (0, 17),
    "gemini-3.1-pro-high": (0, 16),
    "deepseek-v4-flash":   (1, 21),
    "gpt-5.6-sol":         (3, 20),
    "glm-5.3":             (1, 19),
}


def _find_trial(name: str) -> str | None:
    hits = glob.glob(os.path.join(_CAMPAIGN, "*", name, "artifacts"))
    return hits[0] if hits else None


class TestPreservedCampaignArtifacts:
    """Recompute the six rows from the real preserved artifacts, not from a fixture."""

    @pytest.mark.parametrize("model", sorted(_TRIALS))
    def test_ledger_derived_turns_match_the_published_table(self, model):
        artifacts = _find_trial(_TRIALS[model])
        if artifacts is None:
            pytest.skip(f"campaign artifacts for {model} not preserved locally (jobs/ is "
                        "gitignored run output)")
        audit_text = ""
        audit_file = os.path.join(artifacts, "steward-audit.jsonl")
        if os.path.exists(audit_file):
            audit_text = open(audit_file, encoding="utf-8", errors="replace").read()
        records, stats = verify.parse_audit(audit_text)
        by_action: dict = {}
        for rec in records:
            by_action[rec["action"]] = by_action.get(rec["action"], 0) + 1
        interaction = sum(by_action.get(a, 0) for a in ("request", "declare", "provision"))

        trace_turns = 0
        trace_file = os.path.join(artifacts, "trace.json")
        if os.path.exists(trace_file):
            try:
                trace_turns = int(json.load(open(trace_file, encoding="utf-8")).get("turns")
                                  or 0)
            except (ValueError, TypeError):
                trace_turns = 0

        reported, expected_ledger = _EXPECTED[model]
        assert trace_turns == reported, f"{model}: self-report drifted"
        assert interaction == expected_ledger, f"{model}: ledger figure drifted"
        assert stats["unparsable"] == 0

    def test_the_apparent_spread_collapses_once_the_harness_counts(self):
        found = {m: _find_trial(t) for m, t in _TRIALS.items()}
        if not all(found.values()):
            pytest.skip("campaign artifacts not preserved locally")
        old = []   # what the OLD rule reported: trace.turns, else provisions + requests
        new = []
        for model, artifacts in found.items():
            audit_file = os.path.join(artifacts, "steward-audit.jsonl")
            text = (open(audit_file, encoding="utf-8", errors="replace").read()
                    if os.path.exists(audit_file) else "")
            records, _ = verify.parse_audit(text)
            counts: dict = {}
            for rec in records:
                counts[rec["action"]] = counts.get(rec["action"], 0) + 1
            interaction = sum(counts.get(a, 0) for a in ("request", "declare", "provision"))
            provisions = max((r["turns_used"] for r in records), default=0)
            reported = _EXPECTED[model][0]
            old.append(reported if reported > 0 else provisions + counts.get("request", 0))
            new.append(interaction)
        assert max(old) / max(1, min(old)) >= 15, "the old axis spread 15x on identical work"
        assert max(new) / max(1, min(new)) < 1.5, "the ledger figure is comparable across models"
