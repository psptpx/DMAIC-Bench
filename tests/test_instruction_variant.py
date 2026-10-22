"""The permit-stop instruction variant adds exactly one paragraph and nothing else.

It is the scaffold control for the restraint gap (paper/REBUTTAL_PLAN.md P2). The plain
instruction never states that a stopped project is a complete answer, so a shared
"finish the task" pressure from the harness is an alternative explanation the control must
exclude. The variant may change the instruction only; the truth package is built the same way.
"""
import sys
from pathlib import Path

sys.path[:0] = [".", "harbor/src"]
from dmaic_harbor import build as B                                    # noqa: E402

MARK = "stopping is a complete answer"



def test_variants_are_named():
    assert B.INSTRUCTION_VARIANTS == ("plain", "permit-stop", "permit-paraphrase", "normative", "remind")
    assert B.INSTRUCTION_VARIANT == "plain"


def test_template_carries_the_conditional():
    tpl = (B.TEMPLATES_DIR / "instruction.md.j2").read_text(encoding="utf-8")
    assert "{{#if permit_stop}}" in tpl and MARK in tpl
    assert "{{#if permit_paraphrase}}" in tpl and "{{#if normative}}" in tpl


def test_built_datasets_differ_only_in_the_paragraph():
    plain = Path("harbor/datasets/dmaic-bench/dmaic-adb_c31-t3-s1-clean")
    permit = Path("harbor/datasets/dmaic-bench-permit-stop/dmaic-adb_c31-t3-s1-clean")
    if not (plain.exists() and permit.exists()):
        import pytest
        pytest.skip("both datasets must be built locally")
    a = (plain / "instruction.md").read_text(); b = (permit / "instruction.md").read_text()
    assert MARK not in a and MARK in b
    extra = [l for l in b.splitlines() if l not in a.splitlines()]
    assert 5 <= len(extra) <= 9 and all(MARK in l or l.startswith("  ") for l in extra)
    for name in ("tests/truth.json", "tests/test.sh", "environment/Dockerfile"):
        if (plain / name).exists():
            assert (plain / name).read_bytes() == (permit / name).read_bytes(), name
