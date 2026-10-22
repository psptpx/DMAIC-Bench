"""The property the v2 port exists to create: a decision point whose correct branch is a
function of the data, not a string someone typed.

Every test here is written to fail if the GUARDS CEASE FORKING, not merely if the code crashes.
The shipped v1 corpus is the control: of its 79 decision-point instances, 19 recur at more than
one seed and none of them changes branch, so a contestant with textbook DMAIC knowledge answers
the process axis without consulting the data. These assertions pin the opposite.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_PKG_ROOT = str(Path(__file__).resolve().parents[1])
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.graph import branch_decisions, score_path, walk  # noqa: E402
from dmaic_bench.v2 import harbor_truth as HT                          # noqa: E402
from dmaic_bench.v2 import registry                                     # noqa: E402

CASES = registry.discover()
ROUTE_CASES = {cid: c for cid, c in CASES.items()
               if getattr(c, "discriminator", "route") == "route"}


def _node_methods(case, results):
    return {k: tuple(case.methods_at(k, results)) for k in case.node_data}


def _points(case, seed):
    _, results = case.generate(seed)
    return HT.decision_points(case.graph, results, _node_methods(case, results))


# --------------------------------------------------------------------------- the headline

def test_the_correct_branch_moves_with_the_data():
    """Across the whole v2 build: how many recurring decision points change branch?

    The number this replaces is ZERO -- measured on the shipped English v1 build, where every
    one of the 19 decision points that recurs at more than one seed keeps the same
    ``correct_branch``. If this assertion ever reads 0 again, the corpus has stopped being
    data-conditioned and the port has lost its purpose, whatever else still passes.
    """
    seen, branches = {}, {}
    for cid, case in CASES.items():
        for seed in case.seeds:
            for p in _points(case, seed):
                key = (cid, p["point_id"])
                seen[key] = seen.get(key, 0) + 1
                branches.setdefault(key, set()).add(p["correct_branch"])
    recurring = [k for k, n in seen.items() if n > 1]
    varying = [k for k in recurring if len(branches[k]) > 1]
    assert recurring, "no decision point recurs across seeds; the statistic is undefined"
    assert len(varying) >= 12, (
        f"only {len(varying)} of {len(recurring)} recurring decision points change branch "
        f"across seeds; the shipped v1 corpus scores 0 and this port exists to beat it")


#: The pre-registered release gate: at least this share of the RECURRING decision points must
#: take more than one branch across the corpus's seeds. It is a fraction of the forks the corpus
#: actually poses, not a count, so adding a seed cannot dilute it and adding a fork cannot be
#: hidden behind the ones that already vary.
DORMANT_FORK_GATE = 0.80


def _fork_census():
    """``(recurring, varying)`` -- ``{(case_id, point_id): {branch}}`` for the whole v2 corpus."""
    seen, branches = {}, {}
    for cid, case in CASES.items():
        for seed in case.seeds:
            for p in _points(case, seed):
                key = (cid, p["point_id"])
                seen[key] = seen.get(key, 0) + 1
                branches.setdefault(key, set()).add(p["correct_branch"])
    recurring = {k: branches[k] for k, n in seen.items() if n > 1}
    varying = {k: v for k, v in recurring.items() if len(v) > 1}
    return recurring, varying


def test_no_recurring_fork_is_dormant():
    """A fork the data never sends the other way is a fork an agent answers without reading it.

    Six of the eighteen used to be exactly that, and all six were PREREQUISITE gates -- the
    gauge study, the attribute agreement study, the stability check -- so 38% of the process
    axis was collectible by assuming "the measurement system passed and the process is stable",
    on a benchmark whose headline claim is that the correct route is a function of what the data
    revealed. The rule they encode (a %GRR above 30 voids every downstream comparison;
    capability is undefined on an out-of-control process) is the most citable part of the
    methodology, and it was the part nothing tested.

    They were dormant for a STRUCTURAL reason, not a sampling one: the rejection edge was a
    self-loop (or, on the method-trap project, a second edge to the same node), and ``walk`` is
    cycle-guarded, so a rejection terminated the walk ON the fork and ``branch_decisions`` --
    which reads each branch point's successor -- never recorded a decision at all. No seed could
    have woken them. See ``test_a_rejection_branch_is_never_a_self_loop`` for the guard on that.
    """
    recurring, varying = _fork_census()
    dormant = sorted(set(recurring) - set(varying))
    share = len(varying) / len(recurring)
    assert not dormant, (
        f"{len(dormant)} of {len(recurring)} recurring decision points never change branch: "
        f"{dormant}. Add a seed whose data takes the other edge -- do not relax this gate.")
    assert share >= DORMANT_FORK_GATE, f"{share:.0%} of recurring forks vary"


def test_the_dormant_share_of_the_pq_denominator_is_zero():
    """The same statistic weighted the way the score is: how much of the process axis comes
    from forks no seed exercises? It was 24 of 63 instances (38%)."""
    per_point, total = {}, 0
    for cid, case in CASES.items():
        for seed in case.seeds:
            for p in _points(case, seed):
                per_point.setdefault((cid, p["point_id"]), []).append(p["correct_branch"])
                total += 1
    free = sum(len(v) for v in per_point.values() if len(v) > 1 and len(set(v)) == 1)
    assert total > 0
    assert free / total <= 1.0 - DORMANT_FORK_GATE, (
        f"{free}/{total} = {free / total:.0%} of the PQ denominator comes from forks that never "
        f"change branch")
    assert free == 0, f"{free} PQ instances are still free: {sorted(per_point)}"


@pytest.mark.parametrize("case_id", sorted(CASES))
def test_a_rejection_branch_is_never_a_self_loop(case_id):
    """The mechanism that made six forks unmeasurable, forbidden structurally.

    ``walk`` stops when the chosen edge revisits a node, so a branch point whose non-default
    edge fails and whose default edge returns to the same node produces a path that ENDS at the
    fork -- and a fork with no successor on the path is not a decision point, so it can neither
    fork nor be scored. Two edges to the SAME target are the degenerate version of the same bug:
    the guard is decorative because both answers are the same answer.
    """
    graph = CASES[case_id].graph
    for node in graph.nodes:
        out = graph.edges_from(node.key)
        if len(out) < 2:
            continue
        assert all(e.target != node.key for e in out), (
            f"{case_id} {node.key}: a branch of this fork loops back to itself, so the walk "
            f"terminates on it and the decision is never recorded")
        targets = {e.target for e in out}
        assert len(targets) == len(out), (
            f"{case_id} {node.key}: two edges lead to {sorted(targets)}, so the guard cannot "
            f"change where the project goes")


#: Every prerequisite gate in the corpus, and the seed on which the data REJECTS. Named
#: explicitly rather than derived, so deleting the seed that exercises one is a test failure
#: naming the gate rather than a quiet drop in an aggregate.
PREREQUISITE_REJECTIONS = (
    ("adb_c25", "M_msa", "M_msa_fix"),
    ("adb_c26", "M_agree", "M_agree_fix"),
    ("adb_c27", "M_msa", "M_msa_fix"),
    ("adb_c27", "M_stability", "A_special_cause"),
    ("adb_c28", "M_msa", "M_msa_fix"),
    ("adb_c29", "M_stability", "A_special_cause"),
)


@pytest.mark.parametrize("case_id,point,rejects_to", PREREQUISITE_REJECTIONS)
def test_a_seed_exercises_every_prerequisite_rejection(case_id, point, rejects_to):
    case = CASES[case_id]
    took = {p["correct_branch"] for seed in case.seeds for p in _points(case, seed)
            if p["point_id"] == point}
    assert rejects_to in took, (
        f"{case_id} {point}: no seed's data rejects to {rejects_to}, so an agent that assumes "
        f"the prerequisite passed is never wrong here")
    assert len(took) > 1, f"{case_id} {point}: every seed rejects; the acceptance edge is dormant"


@pytest.mark.parametrize("case_id", sorted(ROUTE_CASES))
def test_every_route_case_has_a_fork_that_actually_forks(case_id):
    case = ROUTE_CASES[case_id]
    branches = {}
    for seed in case.seeds:
        for p in _points(case, seed):
            branches.setdefault(p["point_id"], set()).add(p["correct_branch"])
    forking = [k for k, v in branches.items() if len(v) > 1]
    assert forking, f"{case_id}: no decision point takes two different branches across its seeds"


@pytest.mark.parametrize("case_id", sorted(CASES))
def test_the_correct_branch_is_the_guard_walk_and_nothing_else(case_id):
    """Recomputing must reproduce the walk. This is what makes freezing the branch impossible:
    the point set IS ``branch_decisions(graph, walk(...))``, derived on every call."""
    case = CASES[case_id]
    for seed in case.seeds:
        _, results = case.generate(seed)
        expected = branch_decisions(case.graph, walk(case.graph, results), results)
        got = {p["point_id"]: p["correct_branch"] for p in _points(case, seed)}
        assert got == expected, f"{case_id} seed {seed}"


# --------------------------------------------------------------------------- anti-scripting

@pytest.mark.parametrize("case_id", sorted(ROUTE_CASES))
def test_a_frozen_single_path_misses_a_fork_on_every_off_modal_seed(case_id):
    """A solver that always replays one seed's branch decisions must lose a point on EVERY
    other seed. If it does not, that seed is answerable without reading the data."""
    case = ROUTE_CASES[case_id]
    modal = case.seeds[0]
    _, modal_results = case.generate(modal)
    frozen = branch_decisions(case.graph, walk(case.graph, modal_results), modal_results)

    assert score_path(case.graph, modal_results, frozen)["pc"] == 1.0, \
        f"{case_id}: the frozen path does not even satisfy the seed it was frozen from"
    for seed in case.seeds:
        if seed == modal:
            continue
        _, results = case.generate(seed)
        pc = score_path(case.graph, results, frozen)["pc"]
        assert pc < 1.0, (
            f"{case_id} seed {seed}: a scripted single-path solver scores PC {pc} -- this seed "
            f"demands the same route as seed {modal}, so it tests nothing the modal seed does not")


def test_the_method_trap_forks_its_method_even_though_its_route_does_not():
    """The one project whose route is constant BY DESIGN still has to grade something that
    moves. Its graded variable is the method, and a fixed choice must be wrong on some seed."""
    method_cases = {cid: c for cid, c in CASES.items()
                    if getattr(c, "discriminator", "route") == "method"}
    assert method_cases, "no method-discriminated case in the registry"
    for cid, case in method_cases.items():
        chosen = set()
        for seed in case.seeds:
            _, results = case.generate(seed)
            for node in case.method_policy:
                chosen.add((node, tuple(case.methods_at(node, results))))
        nodes = {n for n, _ in chosen}
        for node in nodes:
            verdicts = {m for n, m in chosen if n == node}
            assert len(verdicts) > 1, (
                f"{cid} node {node}: the admissible method is the same on every seed, so a "
                f"contestant that always picks it never has to look at the data")
        # and the split must not be so lopsided that guessing beats reading.
        #
        # A seed the node is NOT ON THE ROUTE FOR counts against every fixed choice, and it has
        # to: `methods_at` answers "which index would be admissible here", but on a seed whose
        # data routes the project away from the node (an out-of-control record, where no
        # capability index is defined at all) NO index is the right thing to report, so
        # crediting the fixed choice there would measure the policy's default rather than the
        # contestant. The denominator stays every seed, so the assertion still bites.
        for node in nodes:
            per_seed = []
            for seed in case.seeds:
                _, results = case.generate(seed)
                on_route = node in walk(case.graph, results)
                per_seed.append(tuple(case.methods_at(node, results)) if on_route else None)
            reached = [p for p in per_seed if p is not None]
            assert reached, f"{cid} node {node}: no seed reaches it"
            most_common = max(set(reached), key=per_seed.count)
            share = per_seed.count(most_common) / len(per_seed)
            assert share <= 0.5, (
                f"{cid} node {node}: always choosing {most_common} is right on "
                f"{share:.0%} of seeds")


# --------------------------------------------------------------------------- evidence rules

@pytest.mark.parametrize("case_id", sorted(CASES))
def test_branch_evidence_never_convicts_a_compliant_run(case_id):
    """A run that executes exactly the methods of the ON-ROUTE nodes must score PQ 1.0.

    This is the regression that the evidence rules exist for, and each exclusion in
    ``branch_evidence`` was added because this test (or its live equivalent) failed: the
    self-loop retry branch, the method the source node also runs, and -- the one that is not
    local -- a method a LATER node on the same route legitimately runs.
    """
    from dmaic_bench import taxonomy as taxonomy_mod
    from dmaic_bench.core.models import (DecisionPoint, Stage, StageMethod, Trace, TraceStep)
    from dmaic_bench.scoring import pq as pq_mod

    case = CASES[case_id]
    tx = taxonomy_mod.load()
    for seed in case.seeds:
        _, results = case.generate(seed)
        nm = _node_methods(case, results)
        on_route = set(walk(case.graph, results))
        executed = sorted({m for k, ms in nm.items() if k in on_route for m in ms})
        trace = Trace(system_id="compliant", task_id=f"{case_id}-{seed}",
                      steps=tuple(TraceStep(step_id=i + 1, method_id=m, outputs={},
                                            status="success")
                                  for i, m in enumerate(executed)),
                      route_decisions=())
        points = tuple(DecisionPoint(
            point_id=p["point_id"], phase=p["phase"], rule=p["rule"], source=p["source"],
            correct_branch=p["correct_branch"],
            acceptable_branches=tuple(p["acceptable_branches"]),
            branch_evidence={k: list(v) for k, v in p["branch_evidence"].items()})
            for p in _points(case, seed))

        class _T:
            decision_points = points
            order_constraints = ()
            stages = (Stage(stage_id="s", phase="measure", label="l", topics=("t",),
                            methods=tuple(StageMethod(method_id=m) for m in executed)),)

        card = pq_mod.score(_T(), trace, tx)
        wrong = [d for d in card["details"] if d.get("verdict") == "incorrect"]
        assert not wrong, (
            f"{case_id} seed {seed}: a run that executed exactly the on-route methods was "
            f"judged to have taken a wrong branch: {wrong}")


@pytest.mark.parametrize("case_id", sorted(CASES))
def test_evidence_is_unique_to_its_branch(case_id):
    """No method may be evidence for two different branches of the same fork, and no method that
    a batch-bearing node elsewhere in the graph also runs may be evidence at all."""
    case = CASES[case_id]
    for seed in case.seeds:
        _, results = case.generate(seed)
        nm = _node_methods(case, results)
        owners = {}
        for node, methods in nm.items():
            for m in methods:
                owners.setdefault(m, set()).add(node)
        for node in case.graph.nodes:
            if not case.graph.is_branch_point(node.key):
                continue
            evidence = HT.branch_evidence(case.graph, node.key, nm)
            assert node.key not in evidence, f"{case_id}: self-loop offered as evidence"
            flat = [m for items in evidence.values() for m in items]
            assert len(flat) == len(set(flat)), f"{case_id} {node.key}: evidence is ambiguous"
            for target, items in evidence.items():
                for m in items:
                    assert owners.get(m) == {target}, (
                        f"{case_id} {node.key}->{target}: {m} is also run by "
                        f"{sorted(owners.get(m, ()) - {target})}")


# --------------------------------------------------------------------------- self-consistency

def test_self_consistency_separates_a_numeric_failure_from_a_judgement_failure():
    """SC and PQ must disagree in the two directions the axis exists to tell apart.

    Built on a real case rather than a toy graph, so the assertion breaks if the guards or the
    field map change shape.
    """
    case = CASES["adb_c25"]
    _, results = case.generate(0)              # stable, normal, capable -> straight to Control
    correct = branch_decisions(case.graph, walk(case.graph, results), results)

    # (a) WRONG NUMBERS, consistent route: the contestant measured Ppk far below target and
    #     routed to root-cause accordingly. PQ must fall (the data says capable); SC must not.
    wrong_numbers = {k: dict(v) if isinstance(v, dict) else v for k, v in results.items()}
    wrong_numbers["cap"] = dict(wrong_numbers["cap"], ppk=0.5)
    consistent = branch_decisions(case.graph, walk(case.graph, wrong_numbers), wrong_numbers)
    assert consistent != correct, "the flipped value did not move the route; test is inert"
    assert score_path(case.graph, results, consistent)["pc"] < 1.0
    assert HT.self_consistency(case.graph, wrong_numbers, consistent)["sc"] == 1.0

    # (b) RIGHT NUMBERS, wrong route: the contestant observed the same values the oracle did and
    #     still went the other way. Both axes must fall.
    off = dict(correct)
    off["A_cap_normal"] = "A_root_cause"
    assert score_path(case.graph, results, off)["pc"] < 1.0
    assert HT.self_consistency(case.graph, results, off)["sc"] < 1.0


def test_a_guard_field_the_trace_cannot_express_is_not_charged_to_the_contestant():
    """``chart.varyingN`` is a property of the batch, not the output of any method. SC must fall
    back to the oracle's value for it and SAY SO, rather than scoring the field map's coverage."""
    case = CASES["adb_c26"]
    _, results = case.generate(2)
    observed, seen, unobservable = HT.observed_results(case.field_map, {}, results)
    assert "chart.varyingN" in unobservable
    assert "chart.varyingN" not in seen
    assert observed["chart"]["varyingN"] == results["chart"]["varyingN"]


def test_observed_results_applies_the_declared_scale():
    """A Gage R&R reports %StudyVariation in PERCENT and the guard is written as a fraction.
    Without the scale the guard reads 19.7 against a threshold of 0.30 and every gauge fails."""
    case = CASES["adb_c25"]
    observed, seen, _ = HT.observed_results(
        {"msa.pctSV": case.field_map["msa.pctSV"]},
        {"msa.gage_rr_crossed": {"percentStudyVariation": 19.72}}, {})
    assert seen == ["msa.pctSV"]
    assert abs(observed["msa"]["pctSV"] - 0.1972) < 1e-9
