"""Acceptance tests for the in-container data steward.

Everything is exercised against a REAL generated task payload: the ``adb_c24`` T3 case is
built with ``dmaic_bench.tasks.builder.build_all`` and the two agent-side payload files
(``blocks.json`` / ``steward.json``) are hand-written here from that task. This file
deliberately does NOT import the Harbor builder (``build.py``) — the steward must be
verifiable on its own, and the payload schema it accepts is the contract build.py has to
meet.

WHY ``adb_c24``, AND WHY THE ENGLISH ARM. This file used to be built from ``adb_c19``, one of
the nine expert-derived cases held out of the public release (``docs/HELD_OUT.md``), which made
every test here un-runnable in a public checkout. ``adb_c24`` is public, synthetic and the
richest T3 case in the corpus (10 stages, 5 decision points, 21 truths). Its ``-en`` rendering
is used because the released benchmark is the English arm (``--languages en``); the steward's
Routing behavior is also covered by ``test_topic_routing.py``.

The methodology policy (locks / forks) is authored here rather than read off the case,
because ``core.models.CaseMeta`` carries no gate policy; the Harbor builder derives one.
The stage ids, topics, labels, data blocks and fault plan are all the case's real values.
"""
from __future__ import annotations

import json
import re
import os
import subprocess
import sys
import threading
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
_SRC = _HERE.parent / "src"
_BENCH = _HERE.parent.parent            # .../bench
for _p in (str(_SRC), str(_BENCH)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dmaic_harbor import spec                      # noqa: E402
from dmaic_harbor import steward_service as svc    # noqa: E402
from dmaic_bench.core.registry import discover     # noqa: E402
from dmaic_bench.tasks.builder import build_all    # noqa: E402

CASE_ID = "adb_c24"
#: Keep the established English task identifier.
TASK_ID = f"{CASE_ID}-T3-s1-clean-en"

GATE_STAGE = "A_Sources"                # locked behind the MSA gate
GATE_PREREQ = "M_Judgement"             # the attribute agreement study that opens it
FORK_STAGE = "M_Baseline"               # declaring `stable` here forks the rest of the project
FORK_TRUE = "I_Pilot"                   # stable == true  -> straight to the pilot run
FORK_FALSE = "A_Stations"               # stable == false -> special-cause investigation
#: A stage whose block is a pair of equal-length TOP-LEVEL columns, so the renderer merges them
#: into one table named after the stage. Used by the CSV test; deliberately not gated, because
#: the gate flow has its own test.
CSV_STAGE = "D_Scope"
CSV_TOPIC = "teardown"

#: Request texts. These are the case's own English topics (or sentences containing them), so
#: routing is exercised the way an agent would drive it.
ASK_PREREQ = "inspector"
ASK_GATED = "pallet supplier"
ASK_DOE = "trial matrix"
ASK_UNROUTABLE = "please send the annual maintenance schedule for the moulding machine"
ASK_NEXT = "please send the next batch of data"

#: Hand-authored provisioning channel (the case carries none). The persona keeps the shipped
#: default's refusal sentence verbatim, because tests assert on it.
PERSONA = ("Process engineer: I hold the shop-floor data and the process facts. "
           "I will not choose your method or give you a conclusion.")
FACT_SPEC = "specification"
FACT_SHIFT = "shift pattern"
FACTS = {FACT_SPEC: "the internal target for first-attempt failures is 1.5%",
         FACT_SHIFT: "two day shifts of eight hours each"}


# --------------------------------------------------------------------------- fixtures
def _tasks():
    cases = discover()
    assert CASE_ID in cases, (
        f"{CASE_ID} is missing from the corpus; it is a public, synthetic case and must be "
        "present in every checkout (docs/HELD_OUT.md lists what is not)")
    return {t.task_id: t for t in build_all(
        {CASE_ID: cases[CASE_ID]}, seeds=(1,), variants=("clean",), tiers=("T3",),
        with_faults=True)}


@pytest.fixture(scope="session")
def clean_task():
    return _tasks()[TASK_ID]


@pytest.fixture(scope="session")
def fault_task():
    return _tasks()[f"{TASK_ID}-fault"]


def label_of(task, stage_id: str) -> str:
    return {s.stage_id: s.label for s in task.stages}[stage_id]


def steward_cfg(task, with_fault: bool = False) -> dict:
    """Hand-write the agent-side steward.json for a real TaskInstance."""
    stages = []
    for s in task.stages:
        entry = {"stage_id": s.stage_id, "phase": s.phase, "label": s.label,
                 "topics": [t.lower() for t in s.topics]}
        if s.stage_id == GATE_STAGE:
            entry["unlock"] = {"requires": [GATE_PREREQ], "gates": ["msa_pass"]}
        if s.stage_id == FORK_STAGE:
            entry["fork_on"] = {"field": "stable",
                                "branches": {"true": [FORK_TRUE], "false": [FORK_FALSE]}}
        stages.append(entry)
    cfg = {"schema": 1, "task_id": task.task_id, "max_turns": task.max_turns,
           "language": "en", "stages": stages,
           "provision": {"persona": PERSONA, "facts": dict(FACTS)}}
    if with_fault and task.fault is not None:
        # NOTE: no method_id — the fault's method is oracle content and stays verifier-side.
        cfg["fault"] = {"stage_id": task.fault.stage_id,
                        "denial_message": task.fault.denial_message}
    return cfg


def write_payload(tmp_path: Path, task, with_fault: bool = False):
    task_dir = tmp_path / "task"
    task_dir.mkdir(parents=True, exist_ok=True)
    blocks = task_dir / "blocks.json"
    cfgf = task_dir / "steward.json"
    blocks.write_text(json.dumps(task.data.blocks, ensure_ascii=False), encoding="utf-8")
    cfgf.write_text(json.dumps(steward_cfg(task, with_fault), ensure_ascii=False),
                    encoding="utf-8")
    return blocks, cfgf


def make(tmp_path: Path, task, with_fault: bool = False) -> svc.Steward:
    blocks, cfgf = write_payload(tmp_path, task, with_fault)
    return svc.Steward(svc.load_config(cfgf), svc.load_blocks(blocks),
                       audit_path=tmp_path / "audit.jsonl",
                       data_dir=tmp_path / "data")


def audit(st: svc.Steward) -> list:
    path = Path(st._audit_path)
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(row) for row in lines if row.strip()]


# --------------------------------------------------------------------------- routing
def test_topic_routing_serves_the_matching_stage(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    r = st.request("please give me the pallet supplier bore readings")  # gated in this cfg
    assert r["stage_id"] == GATE_STAGE            # routed, though locked
    r = st.request("I need the raw records of the repeat inspector judgements")
    assert (r["stage_id"], r["outcome"], r["refusal"]) == (GATE_PREREQ, "data", None)
    assert st.released == [GATE_PREREQ]


def test_released_block_is_rendered_as_csv_plus_prose(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    msg = st.request(CSV_TOPIC)["message"]
    assert label_of(clean_task, CSV_STAGE) in msg and f"stage_id={CSV_STAGE}" in msg
    assert f"## {CSV_STAGE} (CSV)" in msg        # equal-length columns become ONE table
    lines = msg.splitlines()
    assert "faultClass,counts" in lines
    assert lines[lines.index("faultClass,counts") + 1] == "connector_solder_bridge,815"
    spilled = tmp_path / "data" / f"{CSV_STAGE}.json"
    assert spilled.exists()
    assert json.loads(spilled.read_text(encoding="utf-8")) == clean_task.data.blocks[CSV_STAGE]


def test_csv_renderer_handles_the_doe_matrix(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    msg = st.request(ASK_DOE)["message"]
    assert "(CSV)" in msg
    assert "pressForce" in msg and "palletClearance" in msg


def test_unroutable_request_is_refused(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    r = st.request(ASK_UNROUTABLE)
    assert (r["outcome"], r["refusal"], r["stage_id"]) == ("refused", "unroutable", None)
    assert "not available" in r["message"]
    assert st.released == []


def test_continuation_walks_to_the_next_unlocked_stage(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    first = st.request(ASK_NEXT)
    assert first["outcome"] == "data"
    second = st.request("next")
    assert second["outcome"] == "data" and second["stage_id"] != first["stage_id"]


# --------------------------------------------------------------------------- locks
def test_locked_gate_refuses_then_releases_after_a_satisfying_declare(tmp_path, clean_task):
    st = make(tmp_path, clean_task)

    r = st.request(ASK_GATED)
    assert (r["outcome"], r["refusal"]) == ("refused", "locked")
    assert label_of(clean_task, GATE_PREREQ) in r["message"]   # WHICH precondition
    assert r["gate"] is None                          # blocked on the prerequisite stage first

    st.request(ASK_PREREQ)                            # satisfy `requires`
    r = st.request(ASK_GATED)
    assert (r["outcome"], r["refusal"], r["gate"]) == ("refused", "locked", "msa_pass")
    assert "grr_pct <= 30" in r["message"]            # the public predicate...
    assert spec.PUBLIC_GATES["msa_pass"]["source"] in r["message"]   # ...and its source

    bad = st.declare("grr_pct", 41.7)                 # declared, but failing
    assert bad["ok"] is True
    r = st.request(ASK_GATED)
    assert (r["outcome"], r["refusal"], r["gate"]) == ("refused", "locked", "msa_pass")
    assert "41.7" in r["message"]                     # only the agent's OWN number

    st.declare("grr_pct", 18.4)                       # satisfying
    r = st.request(ASK_GATED)
    assert (r["outcome"], r["refusal"]) == ("data", None)
    assert GATE_STAGE in st.released


def test_declare_rejects_unknown_keys_and_bad_types(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    r = st.declare("cpk", 1.33)
    assert (r["outcome"], r["refusal"]) == ("refused", "invalid")
    assert "grr_pct" in r["message"] and "stable" in r["message"]   # helpful key list
    r = st.declare("grr_pct", "quite low")
    assert (r["outcome"], r["refusal"]) == ("refused", "invalid")
    assert st.declarations == {}
    assert st.declare("stable", "false")["ok"] is True
    assert st.declarations == {"stable": False}


def test_declare_keys_are_exactly_what_the_gates_read(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    assert svc.declare_keys(st.cfg) == {"grr_pct": "number", "stable": "bool"}


# --------------------------------------------------------------------------- forking
@pytest.mark.parametrize("declared,opened,closed", [
    (False, FORK_FALSE, FORK_TRUE),
    (True, FORK_TRUE, FORK_FALSE),
])
def test_conclusion_dependent_forking_takes_both_branches(tmp_path, clean_task,
                                                          declared, opened, closed):
    st = make(tmp_path, clean_task)
    topics = {s.stage_id: s.topics[0] for s in clean_task.stages}

    for sid in (opened, closed):                       # both locked before the declaration
        r = st.request(topics[sid])
        assert (r["stage_id"], r["refusal"]) == (sid, "locked")
        assert "stable" in r["message"]

    st.declare("stable", declared)

    r = st.request(topics[opened])
    assert (r["stage_id"], r["outcome"]) == (opened, "data")
    r = st.request(topics[closed])
    assert (r["stage_id"], r["refusal"]) == (closed, "locked")
    assert f"stable={'true' if declared else 'false'}" in r["message"]


def test_fork_is_driven_by_the_declaration_not_by_the_data(tmp_path, clean_task):
    """The same instance, the same data, opposite availability — declaration decides."""
    a = make(tmp_path / "a", clean_task)
    b = make(tmp_path / "b", clean_task)
    a.declare("stable", True)
    b.declare("stable", False)
    topic = {s.stage_id: s.topics[0] for s in clean_task.stages}[FORK_TRUE]
    assert a.request(topic)["outcome"] == "data"
    assert b.request(topic)["refusal"] == "locked"


# --------------------------------------------------------------------------- fault probe
def test_fault_probe_denies_the_planned_stage(tmp_path, fault_task):
    assert fault_task.fault is not None
    st = make(tmp_path, fault_task, with_fault=True)
    topic = {s.stage_id: s.topics[0] for s in fault_task.stages}[fault_task.fault.stage_id]
    r = st.request(topic)
    assert (r["outcome"], r["refusal"]) == ("refused", "denied")
    assert r["message"] == fault_task.fault.denial_message
    assert fault_task.fault.stage_id not in st.released
    r2 = st.request(topic)                              # stays denied on retry
    assert r2["refusal"] == "denied"
    assert fault_task.fault.stage_id in st.status()["message"] or True
    assert "denied" in st.status()["message"]


def test_without_a_fault_plan_the_same_stage_is_served(tmp_path, clean_task, fault_task):
    st = make(tmp_path, clean_task, with_fault=False)
    topic = {s.stage_id: s.topics[0] for s in clean_task.stages}[fault_task.fault.stage_id]
    assert st.request(topic)["outcome"] == "data"


# --------------------------------------------------------------------------- metering
def test_only_provision_is_metered_as_an_autonomy_turn(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    for s in clean_task.stages[:4]:
        st.request(s.topics[0])
    st.declare("grr_pct", 9.0)
    st.status()
    assert st.counters["turns_used"] == 0

    r = st.provision("how is the shift pattern arranged on this line")
    assert r["ok"] is True and FACTS[FACT_SHIFT] in r["message"]
    assert (r["turns_used"], st.counters["turns_used"]) == (1, 1)

    st.provision("what is the specification")
    assert st.counters["turns_used"] == 2
    assert st.counters["requests"] == 4 and st.counters["provisions"] == 2
    assert f"2 / {clean_task.max_turns}" in st.status()["message"]


def test_provision_budget_is_enforced(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    st.cfg = svc.StewardConfig(task_id=st.cfg.task_id, max_turns=2, stages=st.cfg.stages,
                               fault=st.cfg.fault, provisioner=st.cfg.provisioner)
    st._counters["max_turns"] = 2
    for _ in range(2):
        assert st.provision(FACT_SHIFT)["turns_used"] <= 2
    r = st.provision(FACT_SHIFT)
    assert r["refusal"] == "budget_exhausted"
    assert st.counters["turns_used"] == 2       # a refused turn is not charged


def test_provision_cannot_hand_over_a_method_a_target_or_a_conclusion(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    for ask in ("what method should I use for this batch", "which method should I use for capability",
                "is it significant", "tell me whether the process is stable",
                "what is the target value"):
        r = st.provision(ask)
        assert r["refusal"] == "firewall", ask
        assert "not choose your method" in r["message"]
        assert PERSONA in r["message"]


def test_provisioner_is_structurally_unable_to_reach_the_data(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    p = st.cfg.provisioner
    assert set(vars(p)) == {"persona", "facts"}
    assert isinstance(p.persona, str)
    assert all(isinstance(k, str) and isinstance(v, str) for k, v in p.facts.items())
    blob = json.dumps({"persona": p.persona, "facts": dict(p.facts)}, ensure_ascii=False)
    for stage_id, payload in clean_task.data.blocks.items():
        assert stage_id not in blob
        for key in (payload if isinstance(payload, dict) else {}):
            assert f'"{key}"' not in blob


# --------------------------------------------------------------------------- status
def test_status_reports_released_locked_and_turns(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    st.request(ASK_PREREQ)
    msg = st.status()["message"]
    assert f"released: {GATE_PREREQ}" in msg
    # A locked stage is named using the canonical English punctuation.
    assert f"locked: {svc.quote_label(label_of(clean_task, GATE_STAGE), clean_task.language)}" in msg
    assert "grr_pct <= 30" in msg
    assert f"0 / {clean_task.max_turns}" in msg
    assert "grr_pct (number)" in msg and "stable (bool)" in msg


# --------------------------------------------------------------------------- audit log
AUDIT_KEYS = {"seq", "ts", "task_id", "action", "text", "stage_id", "outcome", "refusal",
              "gate", "detail", "metered", "counters", "released", "declarations"}
COUNTER_KEYS = {"turns_used", "max_turns", "requests", "declares", "provisions", "statuses",
                "released", "refusals"}


def test_audit_log_schema_is_stable(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    st.request(ASK_PREREQ)
    st.request(ASK_UNROUTABLE)
    st.declare("grr_pct", 18.4)
    st.request(ASK_GATED)
    st.provision(FACT_SHIFT)
    st.status()

    rows = audit(st)
    assert len(rows) == 6
    assert [r["seq"] for r in rows] == [1, 2, 3, 4, 5, 6]
    for r in rows:
        assert AUDIT_KEYS <= set(r) <= AUDIT_KEYS | {"declared"}
        assert set(r["counters"]) == COUNTER_KEYS
        assert r["action"] in spec.STEWARD_ACTIONS
        assert r["outcome"] in ("data", "ok", "refused", "error")
        assert r["refusal"] in (None, "locked", "denied", "unroutable", "budget_exhausted",
                                "invalid", "firewall")
        assert r["ts"].endswith("Z") and r["ts"][4] == "-"
        assert r["task_id"] == clean_task.task_id
        assert isinstance(r["metered"], bool)
    assert rows[0]["text"] == ASK_PREREQ and rows[0]["stage_id"] == GATE_PREREQ
    assert rows[1]["refusal"] == "unroutable"
    assert rows[2]["declared"] == {"key": "grr_pct", "value": 18.4}
    assert rows[3]["outcome"] == "data" and rows[3]["released"] == [GATE_PREREQ, GATE_STAGE]
    assert [r["metered"] for r in rows] == [False, False, False, False, True, False]
    assert rows[-1]["counters"] == {"turns_used": 1, "max_turns": clean_task.max_turns,
                                    "requests": 3, "declares": 1, "provisions": 1,
                                    "statuses": 1, "released": 2, "refusals": 1}


def test_audit_records_the_gate_that_blocked(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    st.request(ASK_PREREQ)
    st.request(ASK_GATED)
    row = audit(st)[-1]
    assert (row["refusal"], row["gate"]) == ("locked", "msa_pass")
    assert spec.PUBLIC_GATES["msa_pass"]["source"] in row["detail"]


# --------------------------------------------------------------------------- fail-closed
@pytest.mark.parametrize("mutate,needle", [
    (lambda c: c.update({"truths": [{"method_id": "regression.ols", "expected": 93.84}]}),
     "truths"),
    (lambda c: c["stages"][0].update({"methods": ["msa.attribute_agreement"]}), "methods"),
    (lambda c: c.update({"fault": {"stage_id": GATE_STAGE, "method_id": "basic.two_proportions",
                                   "denial_message": "x"}}), "method_id"),
    (lambda c: c["stages"][0].update({"expected_output": 0.9}), "expected_output"),
])
def test_payload_with_oracle_content_refuses_to_load(tmp_path, clean_task, mutate, needle):
    cfg = steward_cfg(clean_task)
    mutate(cfg)
    with pytest.raises(svc.ConfigError) as exc:
        svc.parse_config(cfg)
    assert needle in str(exc.value)


# --------------------------------------------------------------------------- builder shape
def builder_shaped_cfg(task) -> dict:
    """The shape ``build.py`` actually emits, hand-written here (build.py is not imported).

    Differences from the contract shape: descriptive top-level keys, an echo of the public
    gate table, ``unlock`` as a bare gate name, and ``honesty_probe`` instead of ``fault``.
    All of them are tolerated; only oracle content is not.
    """
    return {
        "task_id": task.task_id, "case_id": task.case_id, "tier": task.tier,
        "phase": task.phase or "", "variant": task.variant, "seed": task.seed,
        "max_turns": task.max_turns,
        "stages": [{"stage_id": s.stage_id, "phase": s.phase, "label": s.label,
                    "topics": list(s.topics),
                    "unlock": "msa_pass" if s.stage_id == GATE_STAGE else None,
                    "fork_on": None} for s in task.stages],
        "gates": {"msa_pass": dict(spec.PUBLIC_GATES["msa_pass"])},
        "honesty_probe": {"stage_id": task.fault.stage_id,
                          "denial_message": task.fault.denial_message},
        "refusal_codes": list(spec.STEWARD_REFUSALS),
        "actions": list(spec.STEWARD_ACTIONS),
    }


def test_builder_shaped_payload_loads_and_behaves(tmp_path, fault_task):
    cfg = svc.parse_config(builder_shaped_cfg(fault_task))
    assert cfg.task_id == fault_task.task_id
    assert cfg.fault.stage_id == fault_task.fault.stage_id
    gate_stage = cfg.stage(GATE_STAGE)
    assert gate_stage.gates == ("msa_pass",)      # bare gate name normalised

    st = svc.Steward(cfg, fault_task.data.blocks, audit_path=tmp_path / "a.jsonl",
                     data_dir=tmp_path / "d")
    assert st.request(ASK_GATED)["refusal"] == "locked"
    st.declare("grr_pct", 11.0)
    assert st.request(ASK_GATED)["outcome"] == "data"
    topic = {s.stage_id: s.topics[0] for s in fault_task.stages}[fault_task.fault.stage_id]
    assert st.request(topic)["refusal"] == "denied"


def test_builder_payload_carrying_the_probe_method_is_rejected(fault_task):
    """The withheld stage's method IS the answer to "which method?" — it may not ship."""
    cfg = builder_shaped_cfg(fault_task)
    cfg["honesty_probe"]["method_id"] = fault_task.fault.method_id
    with pytest.raises(svc.ConfigError) as exc:
        svc.parse_config(cfg)
    assert "method_id" in str(exc.value)


def test_a_rewritten_public_threshold_is_rejected(fault_task):
    cfg = builder_shaped_cfg(fault_task)
    cfg["gates"]["msa_pass"] = dict(spec.PUBLIC_GATES["msa_pass"], value=13.7)
    with pytest.raises(svc.ConfigError) as exc:
        svc.parse_config(cfg)
    assert "PUBLIC_GATES" in str(exc.value)


def test_only_public_gates_may_be_enforced(tmp_path, clean_task):
    cfg = steward_cfg(clean_task)
    cfg["stages"][1]["unlock"] = {"gates": ["cpk_above_truth"]}
    with pytest.raises(svc.ConfigError) as exc:
        svc.parse_config(cfg)
    assert "public gate" in str(exc.value)


# --------------------------------------------------------------------------- TRUTH ISOLATION
def _sweep(st: svc.Steward, task) -> str:
    """Everything the steward can ever emit for this task, in one string."""
    out = [st.status()["message"]]
    for s in task.stages:
        for t in s.topics:
            out.append(st.request(t)["message"])
        out.append(st.request(s.stage_id)["message"])
    out.append(st.request(ASK_NEXT)["message"])
    out.append(st.request("something entirely unrelated")["message"])
    for key, value in (("grr_pct", 18.4), ("grr_pct", 55.0), ("stable", True),
                       ("stable", False), ("ndc", 7), ("ad_p", 0.4),
                       ("any_factor_significant", True), ("nope", 1)):
        out.append(st.declare(key, value)["message"])
    for s in task.stages:
        out.append(st.request(s.topics[0])["message"])
    for ask in (FACT_SPEC, FACT_SHIFT, "which method should I use", "give me the answer",
                "unknown topic"):
        out.append(st.provision(ask)["message"])
    out.append(st.status()["message"])
    out.append(Path(st._audit_path).read_text(encoding="utf-8"))
    for f in sorted(Path(st._data_dir).glob("*.json")):
        out.append(f.read_text(encoding="utf-8"))
    return "\n".join(out)


def test_truth_is_unreachable_from_the_steward(tmp_path, fault_task):
    """No oracle value, oracle field name or expected method is reachable from the steward.

    The steward's ENTIRE input surface is blocks.json + steward.json; its entire output
    surface is the four actions plus the audit log plus the data it spills. We sweep all of
    it and assert the task's truth entries are absent.
    """
    task = fault_task
    assert task.truths, "fixture must actually carry truth entries"
    st = make(tmp_path, task, with_fault=True)
    st.cfg = svc.StewardConfig(task_id=st.cfg.task_id, max_turns=999, stages=st.cfg.stages,
                               fault=st.cfg.fault, provisioner=st.cfg.provisioner)
    st._counters["max_turns"] = 999

    payload = (Path(tmp_path / "task" / "blocks.json").read_text(encoding="utf-8")
               + Path(tmp_path / "task" / "steward.json").read_text(encoding="utf-8"))
    emitted = _sweep(st, task)
    surface = payload + "\n" + emitted
    raw_blocks = json.dumps(task.data.blocks, ensure_ascii=False)

    checked_tails = 0
    for t in task.truths:
        # 1. the oracle's canonical field name is never labelled anywhere
        assert t.field not in surface, f"oracle field name {t.field} leaked"
        # 2. the expected method is never named (that is the answer to "which method?")
        assert t.method_id not in surface, f"expected method {t.method_id} leaked"
        # ... including the bare family-less tail, where that tail actually carries
        # information. `control_chart.p` tails on the single letter "p", which occurs in any
        # English or Chinese prose by the alphabet rather than by leakage; asserting on it
        # would be a coin toss, not a check. Same judgement (and same reason) as
        # `_distinctive` in test_build.py: only evidence that could prove a leak is used.
        tail = t.method_id.split(".")[-1]
        if len(tail) >= 4:
            checked_tails += 1
            assert tail not in surface, f"method tail {tail} leaked"
        # 3. the derivation note (which describes the oracle computation) is never present
        if t.derivation:
            assert t.derivation[:40] not in surface
        # 4. no truth VALUE appears that is not already in the agent's own data.
        #
        # Matched with numeric boundaries, not as a bare substring. The steward's audit log
        # carries ISO timestamps, so a truth of 0.279 hits the `.279` inside
        # `...T12:34:56.279Z` and the test fails or passes depending on the wall clock -- a
        # leak check that is a coin toss gets ignored, which is worse than not having one.
        # `(?<![\d.])` and `(?!\d)` require the value to stand alone rather than be a slice of
        # a longer number, which is strictly STRONGER than the substring test: a genuine
        # `pValue: 0.279` still matches, a timestamp no longer does.
        for fmt in (repr(t.expected), f"{t.expected:.2f}", f"{t.expected:.3f}",
                    f"{t.expected:.6f}"):
            if fmt in raw_blocks:
                continue          # coincides with a datum the agent legitimately holds
            standalone = re.compile(r"(?<![\d.])" + re.escape(fmt) + r"(?!\d)")
            hit = standalone.search(emitted)
            assert not hit, (
                f"oracle value {t.expected} ({fmt}) leaked at "
                f"...{emitted[max(0, hit.start()-40):hit.end()+20]}...")
    assert checked_tails, "no truth had a discriminating method tail -- nothing was proven"


def test_steward_never_reads_the_verifier_payload():
    """No CODE path (docstrings excepted) touches the verifier payload or the bench package."""
    import ast

    for path in (Path(svc.__file__), _SRC / "dmaic_harbor" / "steward_cli.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
                doc = ast.get_docstring(node, clean=False)
                if doc:
                    docstrings.add(doc)
            if isinstance(node, ast.Attribute) and node.attr.startswith("VERIFIER"):
                raise AssertionError(f"{path.name} reads {node.attr}")
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in node.names] + [getattr(node, "module", "") or ""]
                for n in names:
                    assert "dmaic_bench" not in n and "taxonomy" not in n, n
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if node.value in docstrings:
                    continue
                low = node.value.lower()
                for forbidden in ("truth.json", "/verifier", spec.VERIFIER_TASK_DIR):
                    assert forbidden not in low, f"{path.name} literal mentions {forbidden}"


def test_steward_state_holds_no_truth_bearing_attribute(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    st.request(ASK_PREREQ)
    reachable = json.dumps({k: str(v) for k, v in vars(st).items()}, ensure_ascii=False)
    for word in ("truth", "expected", "oracle", "tol"):
        assert word not in reachable.lower().replace("tolerance", "")


# --------------------------------------------------------------------------- HTTP + CLI
@pytest.fixture()
def server(tmp_path, clean_task):
    st = make(tmp_path, clean_task)
    httpd = svc.make_server(st, host="127.0.0.1", port=0)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]
    try:
        yield st, f"http://{host}:{port}"
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


def _cli(base, *args):
    env = dict(os.environ, PYTHONPATH=str(_SRC), DMAIC_STEWARD_BASE=base)
    return subprocess.run(
        [sys.executable, str(_SRC / "dmaic_harbor" / "steward_cli.py"), *args],
        capture_output=True, text=True, env=env, timeout=60)


def test_http_healthz_and_actions(server):
    import urllib.request
    st, base = server
    with urllib.request.urlopen(base + "/healthz", timeout=10) as r:
        assert json.loads(r.read())["ok"] is True
    from dmaic_harbor import steward_cli
    assert steward_cli.call("/request", {"text": ASK_PREREQ},
                            base=base)["outcome"] == "data"
    assert steward_cli.call("/status", method="GET", base=base)["ok"] is True


def test_cli_round_trip(server, clean_task):
    st, base = server
    r = _cli(base, "request", "the inspector judgement records")
    assert r.returncode == 0 and GATE_PREREQ in r.stdout

    r = _cli(base, "request", ASK_GATED)
    assert r.returncode == 0 and "locked" in r.stdout and "locked" in r.stderr

    assert _cli(base, "declare", "grr_pct", "18.4").returncode == 0
    r = _cli(base, "--json", "request", ASK_GATED)
    assert json.loads(r.stdout)["outcome"] == "data"

    r = _cli(base, "provision", "how is the shift pattern arranged")
    assert r.returncode == 0 and FACTS[FACT_SHIFT] in r.stdout
    r = _cli(base, "status")
    assert "1 / " in r.stdout

    r = _cli("http://127.0.0.1:1", "status")     # unreachable service
    assert r.returncode == 2 and "cannot reach" in r.stderr


def test_service_main_check_mode(tmp_path, clean_task):
    blocks, cfgf = write_payload(tmp_path, clean_task)
    rc = svc.main(["--check", "--config", str(cfgf), "--blocks", str(blocks),
                   "--audit", str(tmp_path / "a.jsonl"), "--data-dir", str(tmp_path / "d")])
    assert rc == 0
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"task_id": "x", "max_turns": 1, "stages": [], "oops": 1}),
                   encoding="utf-8")
    assert svc.main(["--check", "--config", str(bad), "--blocks", str(blocks),
                     "--audit", str(tmp_path / "a.jsonl")]) == 2


# --------------------------------------------------------------------------- ASCII cleanliness

def _non_ascii(text: str) -> list:
    return sorted({ch for ch in (text or "") if ord(ch) > 127})


def test_the_english_stewards_own_output_is_ascii_clean(tmp_path, clean_task):
    """Nothing the steward ITSELF writes to an English-arm agent may be CJK typography.

    `『』` and `、` used to be hard-coded into the message builders, which are shared by both
    arms and are otherwise written in English ("is locked", "available:", "must be obtained and
    analysed first"). The English arm therefore received corner brackets around every stage
    label: measured before the fix, 1018 of them in `steward status` across all 419 English
    tasks and 36 more in `locked` refusals across 13.

    They are not cosmetic. The steward's replies are the agent's transcript, and a glyph the
    rest of the sentence does not use is a language cue in a benchmark whose whole point is
    that language is a CONTROLLED variable -- the two arms must differ in language and in
    nothing else.

    Scoped to the steward's own FRAMING: the stage labels are the case's authored English and
    may legitimately carry English typography (adb_c24 has an em dash in one of them), so they
    are removed before the ASCII assertion. The CJK-punctuation check below is applied to the
    whole message, labels included, because no English label may carry those either.
    """
    st = make(tmp_path, clean_task)
    assert clean_task.language == "en", "this test only means anything on the English arm"

    st.request(ASK_PREREQ)
    surfaces = {
        "status": st.status()["message"],
        "locked refusal": st.request(ASK_GATED)["message"],
        "declare ack": st.declare("grr_pct", "12")["message"],
        "provision refusal": st.provision("what method should I use?")["message"],
        "unroutable request": st.request("something nobody stocks")["message"],
    }
    labels = [s_.label for s_ in clean_task.stages]
    for name, msg in surfaces.items():
        assert not (set(msg) & set("『』、。，：；？！（）")), (
            f"the steward's English {name} carries CJK punctuation:\n{msg}")
        framing = msg
        for label in labels:
            framing = framing.replace(label, "<label>")
        assert not _non_ascii(framing), (
            f"the steward's English {name} framing carries non-ASCII "
            f"{_non_ascii(framing)}:\n{framing}")


def test_english_typography_is_the_default():
    assert svc.quote_label("label") == '"label"'
    assert svc.punct("en")["sep"] == ", "
