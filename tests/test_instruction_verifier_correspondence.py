"""The verifier must test what the instruction asks for, and nothing it never gave anyone.

`build.assert_no_method_leak` guards one direction: the brief must not name the method. Nothing
guarded the other, and the worst defect this benchmark has shipped lived there — Path Quality
compared a declared branch against a decision-graph node key that reaches no instruction, no
batch and no steward reply, so declining correctly and pressing on wrongly produced the same
score. 63 trials at reward 0.000 beside ms_recall 1.000, invisible for a whole campaign because
the oracle is generated from the truth and is the one agent that can name the key.

Two properties are asserted here, and the second is the one that keeps the first honest:

* the shipped corpus has no ERROR-level correspondence finding; and
* every check FIRES when the defect it names is introduced.

A check that has never been observed to fail is not evidence of anything, and four of these five
are cheap to write in a form that can never fail at all.
"""
from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                                     # noqa: E402

from dmaic_bench.core.graph import (DecisionGraph, GraphNode,     # noqa: E402
                                    GuardedEdge)
from dmaic_bench.v2 import correspondence as CO                   # noqa: E402
from dmaic_bench.v2 import registry                               # noqa: E402

CASES = registry.discover()
BASE = CASES["adb_c32"]

#: Nodes that declare a method scoring will never require, because required methods are keyed on
#: the BATCH a node reads. Inert in the built task — `plan.json` and the requirement set are both
#: built from the batch-bearing nodes — but misleading in the case module, and it is the exact
#: shape that made an improvement node's fork unscoreable in adb_c32 before it was given a batch.
#: Some are deliberate: sla_attribute documents why its improvement nodes ship no batch. Pinned,
#: not emptied, so a NEW one has to be argued for.
KNOWN_DEAD_DECLARATIONS = {
    ("adb_c25", "A_root_cause"), ("adb_c25", "C_control"), ("adb_c25", "I_confirm"),
    ("adb_c25", "I_doe"),
    ("adb_c26", "C_control"), ("adb_c26", "I_confirm"), ("adb_c26", "I_improve"),
    ("adb_c27", "C_control"), ("adb_c27", "I_confirm"), ("adb_c27", "I_doe"),
    ("adb_c27", "I_rsm"),
    # adb_c32's C_control is no longer here: giving Control a batch and a data-conditioned
    # chart choice turned the dead declaration into graded work.
    ("adb_c33", "C_control"),
}


@pytest.fixture(scope="module")
def findings():
    return {cid: CO.check_case(case) for cid, case in CASES.items()}


@pytest.mark.parametrize("case_id", sorted(CASES))
def test_no_case_grades_what_it_never_asked_for(case_id, findings):
    bad = CO.errors(findings[case_id])
    assert not bad, "\n".join(f"[{c}] seed {s}: {m}" for c, s, m in bad)


def test_the_dead_declaration_set_does_not_grow(findings):
    seen = set()
    for case_id, per_case in findings.items():
        for check, _seed, message in per_case:
            if check == "C4":
                seen.add((case_id, message.split()[1]))
    new = sorted(seen - KNOWN_DEAD_DECLARATIONS)
    assert not new, (
        f"nodes newly declaring methods nothing will require: {new}. Either give the node a "
        "batch or drop the declaration — a reader of the module takes it for a requirement.")
    gone = sorted(KNOWN_DEAD_DECLARATIONS - seen)
    assert not gone, f"pinned entries that no longer occur; remove them from the set: {gone}"


def test_the_exempt_points_match_the_self_consistency_exemptions():
    """One list of blind spots, not two. They are the same fact seen from two axes."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_sc_branch_inference", _ROOT / "tests" / "test_sc_branch_inference.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    KNOWN_UNOBSERVABLE = module.KNOWN_UNOBSERVABLE
    assert set(CO.EXEMPT_POINTS) == set(KNOWN_UNOBSERVABLE), (
        "correspondence.EXEMPT_POINTS and test_sc_branch_inference.KNOWN_UNOBSERVABLE have "
        "drifted apart; a point the route scorer cannot see is the same point the branch "
        "scorer cannot see")


# --------------------------------------------------------------- each check must be able to fire

def test_c1_fires_when_a_truth_names_a_method_no_route_calls():
    """The verifier grading a computation the project never asks anyone to do."""
    mutant = dataclasses.replace(BASE, truth_fields=BASE.truth_fields + (
        {"field": "ghost.stationary", "method_id": "doe.rsm_canonical",
         "output": "stationary_A", "scale": 1.0, "tol": 0.1},))
    assert "C1" in {c for c, _s, _m in CO.check_case(mutant)}


def test_c2_fires_when_a_guard_reads_a_field_no_trace_can_express():
    """Self-Consistency re-walks the graph on the contestant's numbers; a guard over a field the
    field_map cannot resolve is a fork only the oracle can answer."""
    edges = tuple(list(BASE.graph.edges) + [
        GuardedEdge("A_more_x", "C_control", "ghost.field > 1", guard_fields=("ghost.field",))])
    mutant = dataclasses.replace(BASE, graph=dataclasses.replace(BASE.graph, edges=edges))
    assert "C2" in {c for c, _s, _m in CO.check_case(mutant)}


def test_c3_fires_on_a_fork_no_trace_can_be_scored_wrong_at():
    """The shipped defect, reconstructed: both branches entail work the other also entails, so
    the private `correct_branch` key is the only handle and it reaches nobody."""
    graph = DecisionGraph(
        entry="D",
        nodes=(GraphNode("D", "define"),
               GraphNode("F", "measure", methods=("control_chart.p",), produces=("a.b",)),
               GraphNode("L", "improve"), GraphNode("R", "improve")),
        edges=(GuardedEdge("D", "F"),
               GuardedEdge("F", "L", "a.b == 0", guard_fields=("a.b",)),
               GuardedEdge("F", "R", is_default=True)))
    mutant = dataclasses.replace(
        BASE, graph=graph, seeds=(0,), gate_policy=(), truth_fields=(), batch_facts={},
        generate=lambda seed: ({"blk": {"defectCounts": [1], "subgroupSizes": [10]}},
                               {"a": {"b": 0}}),
        node_data={"D": "blk", "F": "blk"},
        field_map={"a.b": ({"method_id": "control_chart.p",
                            "output": "outOfControlCount", "scale": 1.0},)})
    assert "C3" in {c for c, _s, _m in CO.check_case(mutant)}


def test_c4_fires_when_a_routed_node_loses_its_batch():
    node_data = {k: v for k, v in BASE.node_data.items() if k != "A_machine"}
    assert "C4" in {c for c, _s, _m in CO.check_case(
        dataclasses.replace(BASE, node_data=node_data))}


def test_c5_fires_when_the_brief_never_asks_for_the_report_the_verifier_grades():
    mutant = dataclasses.replace(BASE, goal="Say what should happen next.")
    assert "C5" in {c for c, _s, _m in CO.check_case(mutant)}


def test_c6_fires_when_a_non_guard_field_shares_a_method_with_a_guard_field():
    """`merged_outputs` is last-wins per method, so a second producer under the same method_id
    answers for the guard field too — and a field no guard reads has no business being in the
    routing table at all.

    Measured while extending adb_c32's Control phase: the sustaining chart's out-of-control
    count overwrote the lot record's, and the Self-Consistency re-walk took the in-control
    branch on a seed whose record is out of control.
    """
    field_map = dict(BASE.field_map)
    field_map["sustain.outOfControl"] = ({"method_id": "control_chart.p",
                                          "output": "outOfControlCount", "scale": 1.0},)
    assert "C6" in {c for c, _s, _m in CO.check_case(
        dataclasses.replace(BASE, field_map=field_map))}


def test_c6_does_not_fire_when_every_sharer_is_a_guard_field():
    """Two guard fields from one method are fine — that is what `occurrence` pinning is for,
    and adb_c35 ships exactly that."""
    from dmaic_bench.v2 import registry as _reg
    findings = CO.check_case(_reg.discover()["adb_c35"])
    assert "C6" not in {c for c, _s, _m in findings}
