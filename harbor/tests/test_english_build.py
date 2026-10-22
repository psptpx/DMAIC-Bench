"""Build-side consequences of making language a real variable.

Each test fails without the change it guards:

* the leak gate had NAKED substring matching, so ``ols`` fired inside "controls" and any
  English context saying "the line has no process controls" aborted the build;
* the instruction template, the vocabulary heading and the prior-facts sanitiser were all
  hardcoded to one language — the sanitiser silently became a no-op under English generation
  and let the unsanitised stage labels (i.e. the method names) into ``instruction.md``;
* ``_language(task)`` read the CASE's native language, which mislabels half a paired corpus;
* nothing gated an agent-visible stage label, which is how a faithful translation of
  ``appraiser attribute agreement (MSA)`` would have handed the agent the answer.
"""
from __future__ import annotations

import os
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_HARBOR_SRC = os.path.join(_HERE, os.pardir, "src")
_BENCH_ROOT = os.path.join(_HERE, os.pardir, os.pardir)
for p in (_HARBOR_SRC, _BENCH_ROOT):
    if os.path.abspath(p) not in sys.path:
        sys.path.insert(0, os.path.abspath(p))

from dmaic_bench.core import i18n, registry            # noqa: E402
from dmaic_bench.tasks import builder                  # noqa: E402
from dmaic_harbor import build as B                    # noqa: E402


@pytest.fixture(scope="module")
def cases():
    return registry.discover()


@pytest.fixture(scope="module")
def en_tasks(cases):
    out = []
    for case_id, case in sorted(cases.items()):
        if "en" not in i18n.languages_for(case.meta):
            continue
        out.extend(builder.build_tasks(case, seeds=(1,), variants=("clean",),
                                       tiers=("T1", "T2", "T3"), with_faults=True,
                                       languages=("en",)))
    assert out, "no English task built — the arm does not exist"
    return out


# --------------------------------------------------------------------------- the leak gate

def test_the_leak_gate_is_word_aware_in_both_directions():
    """`ols` is a substring of "controls"; under naked containment ordinary English prose
    aborted the build, and that is not a hypothetical — the corpus's own stage ids
    (`G_OLS`, `A_FrameOLS`) registered as `ols` hits."""
    assert B.method_terms_in("the line has no process controls") == []
    assert B.method_terms_in("we drilled the mounting holes") == []
    assert B.method_terms_in("the parts were unloaded from the fixture") == []
    assert "ols" in B.method_terms_in("we ran OLS on the yield data")
    assert "gage r&r" in B.method_terms_in("do a gage-r&r first")
    assert "fmea" in B.method_terms_in("start from the FMEA.")


def test_assert_no_method_leak_still_fails_closed():
    B.assert_no_method_leak("the line has no process controls", "test")
    with pytest.raises(B.MethodLeak):
        B.assert_no_method_leak("do a gage r&r first", "test")
    with pytest.raises(B.MethodLeak):
        B.assert_no_method_leak("please start with a one-way anova", "test")



# --------------------------------------------------------------------------- vocabulary table

@pytest.mark.parametrize("language", ["en"])
def test_vocab_heading_matches_the_table_it_must_strip(language):
    """These two are a hand-mirrored pair. If they drift, the leak gate's strip anchor misses
    and every build aborts on its own vocabulary table."""
    table = B.method_vocabulary(language)
    assert table.startswith(B.vocab_heading(language))
    B.assert_no_method_leak("context.\n\n" + table + "\n\nrest.", "test")


def test_the_english_vocabulary_table_is_english():
    assert not i18n.has_cjk(B.vocab_heading("en"))
    assert B.vocab_heading("en") == B.VOCAB_HEADING


# --------------------------------------------------------------------------- prior facts

class _FakeTask:
    def __init__(self, prior_facts, phase, language):
        self.prior_facts = prior_facts
        self.phase = phase
        self.language = language


def test_english_prior_facts_are_sanitised_not_passed_through():
    """Under English generation the old sanitiser did not recognise the English delimiters, became a
    no-op, and let a list of stage labels — i.e. the methods for the phase being scored —
    reach the instruction."""
    raw = "Completed: y1 baseline record over fifteen days; Completed: teardown log"
    out = B.sanitize_prior_facts(_FakeTask(raw, "measure", "en"))
    assert "Completed:" not in out
    assert "baseline record" not in out
    assert "define" in out and "not asked to redo" in out
    assert not i18n.has_cjk(out)



def test_a_real_summary_fact_survives():
    text = "the baseline pass rate sat near ninety per cent"
    raw = "; ".join([text, "Completed: some label"])
    out = B.sanitize_prior_facts(_FakeTask(raw, "analyze", "en"))
    assert text in out


# --------------------------------------------------------------------------- language wiring

def test_language_is_read_off_the_instance_not_off_the_case(cases):
    """Every default-built instance carries the official English language."""
    paired = [cid for cid, c in cases.items()
              if i18n.languages_for(c.meta) == ("en",)]
    assert paired
    for task in builder.build_tasks(cases[paired[0]], seeds=(1,), variants=("clean",),
                                    tiers=("T3", "T1")):
        assert B._language(task) == task.language


def test_task_toml_and_steward_config_both_carry_the_arm(en_tasks):
    for task in en_tasks[:6]:
        assert 'language = "en"' in B.build_task_toml(task)
        assert B.build_steward_config(task)["language"] == "en"
        assert B.build_oracle_plan(task)["language"] == "en"


def test_the_instruction_template_is_chosen_by_language():
    assert B.instruction_template_path("en").name == "instruction.md.j2"
    for language in ("zh", "fr"):
        with pytest.raises(ValueError, match="English only"):
            B.instruction_template_path(language)


def test_every_english_instruction_renders_leak_free_and_english(en_tasks):
    for task in en_tasks:
        text = B.build_instruction(task)
        body = text.split(B.vocab_heading("en"))[0]
        assert not i18n.has_cjk(body), f"{task.task_id}: instruction body is not English"
        assert f"# Task {task.task_id}" in text
        assert "steward request" in text
        # assert_no_method_leak already ran inside build_instruction; this pins that it did.
        assert B.method_terms_in(body) == [], task.task_id


# --------------------------------------------------------------------------- label gate

def test_the_label_gate_rejects_a_method_named_label():
    stages = [{"stage_id": "M_X", "label": "Attribute agreement analysis on the retained set",
               "topics": ["retained set"]}]
    assert B.steward_label_leaks(stages)
    with pytest.raises(B.LabelLeak):
        B.assert_no_label_leak(stages, "test")


def test_the_label_gate_passes_a_batch_named_label():
    stages = [{"stage_id": "M_X",
               "label": "Repeat bench judgements on a retained set against a known condition",
               "topics": ["retained set", "known condition"]}]
    assert B.steward_label_leaks(stages) == {}
    B.assert_no_label_leak(stages, "test")


def test_official_builds_are_gated():
    assert B.STRICT_AUTHORING_LANGUAGES == ("en",)


def test_building_every_english_steward_config_runs_both_gates(en_tasks):
    for task in en_tasks:
        cfg = B.build_steward_config(task)          # raises on a topic or label defect
        assert cfg["stages"], task.task_id


# --------------------------------------------------------------------------- the oracle

def test_the_oracle_uses_authoritative_english_report_strings():
    """`solve.sh` is the reference solution and the ceiling every contestant is read against.
    Its gap section is what the honesty scorer reads, so it must be written in the arm's own
    language, and its distractor mirror must use the canonical keys."""
    body = open(os.path.join(_HERE, os.pardir, "templates", "solution", "solve.sh"),
                encoding="utf-8").read()
    assert '_STRINGS = {' in body and '"zh": {' not in body and '"en": {' in body
    assert 'def strings(plan):' in body
    assert 'plan.get("language")' in body
    for key in ("recorder", "remark", "shift", "ambient", "row_id"):
        assert f'"{key}"' in body, f"the oracle no longer strips the {key} distractor"
    assert '_ORIGINAL_SUFFIXES = ("_original",)' in body


def test_steward_rejects_unsupported_language_before_serving_data():
    from dmaic_harbor import steward_service as svc
    cfg = {"schema": 1, "task_id": "test", "max_turns": 10, "language": "zh",
           "stages": [{"stage_id": "M", "label": "Measurements", "phase": "measure",
                       "topics": ["measurements"]}]}
    with pytest.raises(svc.ConfigError, match="English only"):
        svc.parse_config(cfg)


@pytest.mark.parametrize("mode", [[], ["--v2"]])
@pytest.mark.parametrize("language", ["zh", "fr", "en,zh", ""])
def test_cli_rejects_unsupported_languages_before_writing(tmp_path, mode, language):
    output = tmp_path / "unsupported"
    with pytest.raises(SystemExit) as exc:
        B.main(["--out", str(output), "--languages", language, *mode])
    assert exc.value.code == 2
    assert not output.exists()
