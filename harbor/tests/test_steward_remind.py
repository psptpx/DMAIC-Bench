"""The *remind* instruction control: published preconditions, evaluated on declarations only."""
import json
import pytest

from dmaic_harbor import steward_service as svc


def _cfg(pres):
    return {"task_id": "t", "max_turns": 5,
            "stages": [{"stage_id": "run", "phase": "measure", "label": "Process run",
                        "topics": ["process run"]}],
            "preconditions": pres}


def test_predicate_evaluator_covers_the_guard_dsl():
    h = svc._guard_holds
    assert h("imr.outOfControl == 0", {"imr.outOfControl": 0.0}) is True
    assert h("imr.outOfControl == 0", {"imr.outOfControl": 3.0}) is False
    assert h("(msa.pctSV <= 0.30 and msa.ndc >= 5)", {"msa.pctSV": 0.12, "msa.ndc": 7.0}) is True
    assert h("(msa.pctSV <= 0.30 and msa.ndc >= 5)", {"msa.pctSV": 0.12, "msa.ndc": 3.0}) is False
    assert h("not (pchart.outOfControl > 0)", {"pchart.outOfControl": 0.0}) is True
    assert h("screen.modelPValue < 0.05", {}) is None            # undeclared field
    assert h("screen.modelPValue <", {"screen.modelPValue": 0.01}) is None   # does not parse
    assert h("stable == true", {"stable": True}) is True
    assert h("import os", {"import": 1}) is None


def test_config_accepts_preconditions_and_declare_keys_include_their_fields(tmp_path):
    cfg = svc.parse_config(_cfg([{"when": "(imr.outOfControl == 0)", "fields": ["imr.outOfControl"],
                                  "types": {"imr.outOfControl": "number"}}]))
    assert cfg.preconditions[0]["when"] == "(imr.outOfControl == 0)"
    assert svc.declare_keys(cfg) == {"imr.outOfControl": "number"}


def test_config_rejects_a_predicate_that_does_not_parse():
    with pytest.raises(svc.ConfigError):
        svc.parse_config(_cfg([{"when": "imr.outOfControl ==", "fields": ["imr.outOfControl"]}]))


def test_declare_reports_whether_the_precondition_holds_without_locking(tmp_path):
    cfg = svc.parse_config(_cfg([{"when": "(msa.pctSV <= 0.30 and msa.ndc >= 5)",
                                  "fields": ["msa.ndc", "msa.pctSV"],
                                  "types": {"msa.ndc": "number", "msa.pctSV": "number"}}]))
    st = svc.Steward(cfg, {"run": {"x": [1, 2, 3]}}, audit_path=tmp_path / "audit.jsonl")
    r = st.declare("msa.pctSV", 0.45)
    assert r["ok"] and "not yet decidable" in r["message"]
    r = st.declare("msa.ndc", 7)
    assert "DOES NOT HOLD" in r["message"] and "not licensed" in r["message"]
    # nothing is locked by a precondition: the run is still requestable
    assert st.request("process run")["outcome"] == "data"
    r = st.declare("msa.pctSV", 0.12)
    assert "HOLDS" in r["message"] and "DOES NOT" not in r["message"]
    status = st.status()["message"]
    assert "handbook preconditions" in status and "HOLDS" in status
    last = json.loads((tmp_path / "audit.jsonl").read_text().splitlines()[-2])
    assert last["preconditions"] == {"(msa.pctSV <= 0.30 and msa.ndc >= 5)": True}


def test_plain_config_has_no_preconditions_and_status_says_nothing_about_them(tmp_path):
    cfg = svc.parse_config(_cfg([]))
    st = svc.Steward(cfg, {"run": {}}, audit_path=tmp_path / "a.jsonl")
    assert cfg.preconditions == () and "handbook preconditions" not in st.status()["message"]
