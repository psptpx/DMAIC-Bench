"""Steward routing must survive an English corpus, and topics must be validated where written.

Two defects, both silent:

1. `_route` matched a topic by NAKED CASE-INSENSITIVE SUBSTRING CONTAINMENT and returned the
   FIRST hit. The corpus's own Latin topics include ``i`` (from tokenising "I-MR"), ``process``,
   ``line``, ``plan``, ``target`` and ``baseline``; under containment those swallow requests
   meant for other stages, and a misroute returns DATA, not an error, so the agent analyses the
   wrong batch and nothing anywhere records that it happened.
2. Nothing rejected such a topic where it is authored. A topic is a match key, not prose.

English topic edges remain boundary-checked, including mixed alphanumeric keys.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
_SRC = _HERE.parent / "src"
_BENCH = _HERE.parent.parent
for _p in (str(_SRC), str(_BENCH)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dmaic_harbor import steward_service as svc     # noqa: E402
from dmaic_bench.core import registry               # noqa: E402


# --------------------------------------------------------------------------- fixtures
def _cfg(stages, task_id="t-en"):
    return {"schema": 1, "task_id": task_id, "max_turns": 10, "language": "en",
            "stages": [{"stage_id": sid, "phase": ph, "label": lbl, "topics": list(tp)}
                       for sid, ph, lbl, tp in stages]}


def _steward(tmp_path, stages, blocks=None, **kw):
    cfg = svc.parse_config(_cfg(stages), **kw)
    blocks = blocks or {sid: {"values": [1, 2, 3]} for sid, *_ in stages}
    return svc.Steward(cfg, blocks, audit_path=tmp_path / "audit.jsonl")


EN_STAGES = (
    # the hijacker is declared FIRST on purpose: under the old first-hit rule it won everything
    ("M_IMR", "measure", "Appearance PPM run chart", ("i", "mr chart")),
    ("M_Gage", "measure", "Caliper study records", ("caliper records", "appraiser records")),
    ("A_Capability", "analyse", "Capability of the finished line",
     ("process", "process capability")),
    ("A_Furnace", "analyse", "Furnace batch comparison", ("furnace batches",)),
)



# --------------------------------------------------------------------------- 1. the matcher
@pytest.mark.parametrize("topic,text,matches", [
    # the single-letter hijack: "i" is a word in the first, a letter inside words in the rest
    ("i", "i need the data", True),
    ("i", "please provide the caliper records", False),
    ("i", "the machine capability figures", False),
    ("process", "the process data", True),
    ("process", "we reprocessed the batch", False),
    ("line", "the baseline batch", False),
    ("line", "line 3 output", True),
    ("plan", "the sampling plan", True),
    ("plan", "the planned maintenance window", False),
    # elastic separators and prose plurals — the agent writes English, not the key
    ("p chart", "send the p-chart data", True),
    ("nozzle", "the nozzles on line 2", True),
    ("furnace batches", "the furnace batches from last week", True),
    ("r&r", "the r&r study records", True),
    ("y3", "the y3 column", True),
    ("y3", "the xy3 column", False),
    # CJK keeps containment; ASCII edges of a mixed topic stay boundary-checked
])
def test_topic_matching_is_word_aware(topic, text, matches):
    assert bool(svc.topic_match_len(topic, text.lower())) is matches


# --------------------------------------------------------------------------- 2. routing
def test_english_request_reaches_the_stage_it_names(tmp_path):
    st = _steward(tmp_path, EN_STAGES)
    assert st.request("please send the appraiser records")["stage_id"] == "M_Gage"
    assert st.request("the furnace batches from last week")["stage_id"] == "A_Furnace"


def test_single_letter_topic_no_longer_hijacks_english_requests(tmp_path):
    """The measured failure: `"i" in low` was true for essentially every English request."""
    st = _steward(tmp_path, EN_STAGES)
    for text, want in (("I need the appraiser records for the sampled boards", "M_Gage"),
                       ("Give me the furnace batches, including the rework ones", "A_Furnace"),
                       ("the process capability figures for the finished line", "A_Capability")):
        assert st.request(text)["stage_id"] == want, text


def test_the_most_specific_topic_wins_not_the_first_declared(tmp_path):
    """`process` is declared before `process capability` on the SAME stage's sibling key.

    Substring shadowing across stages is what makes first-hit routing a silent misroute; the
    longest match is the deterministic, order-independent resolution.
    """
    stages = (("A_Process", "analyse", "Process baseline", ("process",)),
              ("A_Capability", "analyse", "Capability study", ("process capability",)))
    st = _steward(tmp_path, stages)
    assert st.request("the process capability data")["stage_id"] == "A_Capability"
    assert st.request("the process data")["stage_id"] == "A_Process"



def test_unroutable_english_request_is_refused_not_misrouted(tmp_path):
    st = _steward(tmp_path, EN_STAGES)
    r = st.request("anything you have lying around")
    assert (r["stage_id"], r["refusal"]) == (None, "unroutable")


def test_stage_id_and_label_still_route(tmp_path):
    st = _steward(tmp_path, EN_STAGES)
    assert st.request("give me M_Gage")["stage_id"] == "M_Gage"
    assert st.request("the Furnace batch comparison table")["stage_id"] == "A_Furnace"


# --------------------------------------------------------------------------- 3. the gate
def test_topic_problems_flags_short_and_shadowed_topics():
    probs = svc.topic_problems([
        {"stage_id": "A", "topics": ["i", "process"]},
        {"stage_id": "B", "topics": ["process capability", "x", "shaft diameter"]},
    ])
    joined = "\n".join(probs)
    assert "'i'" in joined and "'x'" in joined            # too short to be a key
    assert "'process'" in joined                          # shadowed by 'process capability'


def test_topic_problems_accepts_a_well_authored_english_case():
    assert svc.topic_problems([
        {"stage_id": "A", "topics": ["appraiser records", "repeat readings"]},
        {"stage_id": "B", "topics": ["furnace batches", "furnace log", "y3"]},
    ]) == []


def test_duplicate_topic_across_stages_is_rejected():
    probs = svc.topic_problems([{"stage_id": "A", "topics": ["furnace batches"]},
                                {"stage_id": "B", "topics": ["Furnace Batches"]}])
    assert probs and "cannot be told apart" in probs[0]


def test_validate_topics_raises_and_parse_config_opts_in(tmp_path):
    bad = (("M_IMR", "measure", "run chart", ("i",)),
           ("M_Gage", "measure", "caliper", ("caliper records",)))
    with pytest.raises(svc.ConfigError) as ei:
        svc.parse_config(_cfg(bad), strict_topics=True)
    assert "unroutable topics" in str(ei.value)

    # default stays permissive: an ALREADY BUILT task must still start, because refusing to
    # boot turns an authoring defect into a dead campaign task.
    cfg = svc.parse_config(_cfg(bad))
    assert [s.stage_id for s in cfg.stages] == ["M_IMR", "M_Gage"]

    path = tmp_path / "steward.json"
    path.write_text(json.dumps(_cfg(bad), ensure_ascii=False), encoding="utf-8")
    assert svc.load_config(path) is not None
    with pytest.raises(svc.ConfigError):
        svc.load_config(path, strict_topics=True)


# --------------------------------------------------------------------------- 4. the corpus
#: The canonical English corpus has no accepted topic defects.
KNOWN_LEGACY_TOPIC_DEFECTS = {}


def test_no_new_case_introduces_an_unroutable_topic():
    """Build-time gate over every authored case. New violations fail here, before a campaign."""
    cases = registry.discover()
    assert cases, "the registry produced no case at all -- this gate would pass vacuously"
    found = {}
    for case_id, case in sorted(cases.items()):
        probs = svc.topic_problems(
            [{"stage_id": s.stage_id, "topics": s.topics} for s in case.meta.stages])
        if probs:
            found[case_id] = probs
    counts = {k: len(v) for k, v in found.items()}
    expected = {k: v for k, v in KNOWN_LEGACY_TOPIC_DEFECTS.items() if k in cases}
    assert counts == expected, (
        "topic-validation findings changed; fix the topic rather than the allow-list:\n"
        + json.dumps(found, ensure_ascii=False, indent=2))
