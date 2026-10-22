"""v3 fair environment: the firewall provisioning simulator + autonomy metering."""
import sys, os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from dmaic_bench.v2 import builder, sonnet_harness
from dmaic_bench.v3.env import make_env

import pytest  # noqa: E402
from dmaic_bench.v2.expert_migration import _legacy_bridge_available  # noqa: E402

# These exercises are pinned to an expert-derived case held out of the public
# release (docs/HELD_OUT.md). Repointing them at a public case is tracked work;
# until then the skip is reported, never silent.
pytestmark = pytest.mark.skipif(
    not _legacy_bridge_available(),
    reason="held-out expert case absent (public release) -- see docs/HELD_OUT.md",
)


def _task():
    return builder.build_project_task(sonnet_harness._get_case("adb_c15"), 0)


def test_provision_returns_data_for_a_stage_request():
    env = make_env(_task())
    r = env.provision("Please provide baseline data")
    assert r["kind"] == "data" and r["data"]


def test_firewall_refuses_method_and_answer_requests():
    env = make_env(_task())
    assert env.provision("Which method should I use for this step?")["kind"] == "refused"
    assert env.provision("What is the correct value for process capability?")["kind"] == "refused"
    assert env.provision("What is the conclusion?")["kind"] == "refused"


def test_simulator_never_holds_the_oracle():
    env = make_env(_task())
    # structural firewall: the simulator's fields are data/facts/persona only — no oracle store
    fields = set(vars(env.simulator))
    assert "oracle" not in fields and "oracle_results" not in fields
    assert set(fields) <= {"task", "facts", "persona"}


def test_autonomy_cost_is_metered_and_budget_capped():
    env = make_env(_task(), max_provision_turns=2)
    env.provision("baseline data"); env.provision("gauge data")
    assert env.autonomy_cost == 2
    assert env.provision("Request again")["kind"] == "budget_exhausted"


def test_facts_are_returned_but_are_not_answers():
    env = make_env(_task(), facts={"specification limits": "LSL=0.85, USL=0.95"})
    r = env.provision("What are the specification limits?")
    assert r["kind"] == "fact" and "0.85" in r["value"]
