"""v2_tasks.preconditions: the predicates the *remind* control publishes."""
from dmaic_harbor import v2_tasks as V
from dmaic_harbor import build as B


def test_fillet_height_publishes_its_no_go_preconditions_only():
    case = V.discover()["adb_c36"]
    whens = [p["when"] for p in V.preconditions(case)]
    assert "(imr.outOfControl == 0)" in whens          # stability before capability
    assert "(screen.modelPValue < 0.05)" in whens      # a screen that found nothing is a no-go
    assert "(confirm.pValue < 0.05)" in whens          # an unconfirmed improvement is a no-go
    assert not any("normality" in w for w in whens)    # parametric-vs-rank is a choice, not a precondition
    assert not any("cap.ppk" in w for w in whens)      # capability met is a close, not a no-go
    for p in V.preconditions(case):
        assert p["fields"] and all(f in p["when"] for f in p["fields"])
        assert set(p["types"].values()) <= {"number", "bool", "string"}


def test_no_node_key_and_no_branch_leaks_into_a_precondition():
    for case in V.discover().values():
        for p in V.preconditions(case):
            assert set(p) == {"when", "fields", "types"}
            for n in case.graph.nodes:
                assert n.key not in p["when"]


def test_plain_build_publishes_no_preconditions():
    assert B.INSTRUCTION_VARIANT == "plain"
    assert "remind" in B.INSTRUCTION_VARIANTS
