"""The v2 builder: a decision-graph project packaged as a Harbor task.

Three properties are load-bearing here and each has its own test below.

1. **The correct branch is recomputed, never shipped.** The truth package carries the graph and
   the oracle's results; ``verify.v2_decision_points`` walks them. A frozen ``correct_branch``
   in the task directory would reintroduce, one layer down, exactly the defect the port removes.
2. **Truth isolation.** The graph, the guards and the results reach the VERIFIER context only.
   The agent context gets data batches, routing topics and public handbook thresholds.
3. **The forks still fork.** The statistic the port exists to move is asserted on the BUILT
   corpus, not on the case objects, so a builder change that flattens it fails here.
"""
from __future__ import annotations

import json
import os
import re
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
HARBOR_ROOT = os.path.dirname(HERE)
BENCH_ROOT = os.path.dirname(HARBOR_ROOT)
for _p in (os.path.join(HARBOR_ROOT, "src"), BENCH_ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dmaic_bench.core.graph import branch_decisions, walk        # noqa: E402
from dmaic_bench.v2 import harbor_truth as HT                    # noqa: E402
from dmaic_harbor import build as B                              # noqa: E402
from dmaic_harbor import spec, steward_service as ss             # noqa: E402
from dmaic_harbor import v2_tasks as V                           # noqa: E402
from dmaic_harbor import verify as VF                            # noqa: E402

CASES = V.discover()
IDS = sorted(CASES)


def _task(case_id, seed, with_fault=False):
    return V.build_task(CASES[case_id], seed, with_fault=with_fault, language="en")


def _probeable(case, seed):
    """The oracle's computed values that are distinctive enough to grep for.

    A value with fewer than three significant digits is a substring of half the decimals in any
    JSON document, so probing for it reports a leak on every task and the check stops meaning
    anything. ``scripts/e2e.sh`` draws exactly this line against the truth package; the same
    rule applies here to the payloads that must NOT carry a result.
    """
    _blocks, results = case.generate(seed)
    out = []

    def walk_values(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if not str(k).startswith("_"):
                    walk_values(v)
        elif isinstance(node, (int, float)) and not isinstance(node, bool):
            text = "%g" % round(float(node), 6)
            digits = sum(c.isdigit() for c in text.lstrip("-0.").rstrip("0"))
            if digits >= 3:
                out.append(text)

    walk_values(results)
    return sorted(set(out))


def _truth(case_id, seed):
    task = _task(case_id, seed)
    truth = VF.truth_package_from_task(task, y_type=B._y_type(task), gates=B.gate_locks(task))
    truth["v2"] = V.graph_truth(CASES[case_id], seed)
    return task, truth


# --------------------------------------------------------------------------- identity policy

def test_the_published_identifiers_are_opaque_and_coarse():
    """``cases/_template/case.yaml``: an id may not carry a company, place, industry or
    statistical-method name, and ``industry`` takes one of exactly four coarse values. The
    descriptive module names stay on disk; nothing that ships carries them."""
    coarse = {"process_industry", "electronics", "discrete_manufacturing", "services",
              "life_sciences"}
    for cid, case in CASES.items():
        assert re.fullmatch(r"adb_c\d{2}", cid), f"{cid} is not an opaque adb_cNN id"
        assert case.industry in coarse, f"{cid}: industry {case.industry!r} is not coarse"
        assert not B.method_terms_in(cid), f"{cid}: the id itself names a method"
        assert not B.method_terms_in(case.title), f"{cid}: the title names a method"
        assert case.title.isascii(), f"{cid}: non-ASCII title in an English-only release"


@pytest.mark.parametrize("case_id", IDS)
def test_nothing_the_agent_reads_is_in_the_wrong_language(case_id):
    """English-only release: these projects ship no locale overlay, so every agent-visible
    string -- brief, batch labels, routing topics and the data itself -- must be English."""
    case = CASES[case_id]
    cjk = re.compile(r"[\u4e00-\u9fff]")
    assert not cjk.search(case.context) and not cjk.search(case.goal)
    for meta in case.blocks_meta.values():
        assert not cjk.search(meta["label"])
        for t in meta["topics"]:
            assert not cjk.search(t)
    for seed in case.seeds:
        blocks, _ = case.generate(seed)
        assert not cjk.search(json.dumps(blocks, ensure_ascii=False)), f"{case_id} seed {seed}"


# --------------------------------------------------------------------------- leak gates

@pytest.mark.parametrize("case_id", IDS)
def test_the_brief_and_the_steward_payload_name_no_method(case_id):
    for seed in CASES[case_id].seeds:
        task = _task(case_id, seed)
        text = B.build_instruction(task)                 # raises MethodLeak on a hit
        assert task.task_id in text
        cfg = B.build_steward_config(task)               # runs the label + topic gates
        ss.validate_topics(cfg["stages"])
        B.assert_no_label_leak(cfg["stages"], case_id)


@pytest.mark.parametrize("case_id", IDS)
def test_the_agent_payload_carries_no_graph_no_guard_and_no_result(case_id):
    """The steward's schema is a strict allowlist, so this is belt and braces -- but the thing
    being guarded against is a builder that starts putting routing information in a tolerated
    descriptive key, which the allowlist would not catch."""
    for seed in CASES[case_id].seeds:
        task = _task(case_id, seed)
        cfg = B.build_steward_config(task)
        ss.parse_config(dict(cfg, honesty_probe=cfg.pop("fault", None))
                        if cfg.get("fault") else cfg)
        blob = json.dumps(cfg, ensure_ascii=False)
        for banned in ("oracle_results", "correct_branch", "guard", "when", "graph",
                       "oracle_route", "node_methods", "field_map"):
            assert banned not in blob, f"{case_id}: steward.json carries {banned!r}"
        # and no computed value. Probed with the same >=3-significant-digit rule
        # scripts/e2e.sh uses: 0.0 and 1.0 are substrings of half the decimals in any JSON
        # document, so a probe that fires on them stops meaning anything.
        for value in _probeable(CASES[case_id], seed):
            assert value not in blob, f"{case_id}: steward.json carries the computed {value}"


@pytest.mark.parametrize("case_id", IDS)
def test_only_public_gates_ever_reach_the_agent(case_id):
    """A lock the steward enforces must be a published handbook threshold. Anything else would
    need an oracle value to evaluate, which is the whole thing the split forbids."""
    for lock in V.locks(CASES[case_id]).values():
        for gate in lock["gates"]:
            assert gate in spec.PUBLIC_GATES, gate


@pytest.mark.parametrize("case_id", IDS)
def test_the_honesty_probe_does_not_name_the_analysis_it_withholds(case_id):
    """The probe's whole point is that the agent must not know which analysis the withheld
    batch was for. Two of these projects wrote it into the denial text, which lands in
    steward.json inside the agent image.

    The probe is chosen PER SEED (`v2_tasks.safe_fault_target`): the batch withheld has to be one
    whose absence cannot move the route, and the shortest routes have no such batch. So the seed
    is the first one that carries a probe rather than simply the first one.
    """
    case = CASES[case_id]
    seed = next((s for s in case.seeds if V.safe_fault_target(case, s)), None)
    if seed is None:
        pytest.skip("no seed of this case can carry a probe without moving its route")
    task = _task(case_id, seed, with_fault=True)
    assert task.fault is not None
    assert not B.method_terms_in(task.fault.denial_message)
    cfg = B.build_steward_config(task)
    assert "method_id" not in json.dumps(cfg["fault"])


# --------------------------------------------------------------------------- recomputation

@pytest.mark.parametrize("case_id", IDS)
def test_the_verifier_recomputes_the_branch_from_the_guards(case_id):
    case = CASES[case_id]
    for seed in case.seeds:
        _task_obj, truth = _truth(case_id, seed)
        assert truth["decision_points"] == [], \
            "a frozen decision point was written into the task directory"
        got = {p["point_id"]: p["correct_branch"] for p in VF.v2_decision_points(truth)}
        _, results = case.generate(seed)
        want = branch_decisions(case.graph, walk(case.graph, results), results)
        assert got == want, f"{case_id} seed {seed}"
        rebuilt = VF.build_task(truth)
        assert {p.point_id: p.correct_branch for p in rebuilt.decision_points} == want


#: The pre-registered release gate, mirrored from ``tests/test_v2_graph_truth.py`` so the BUILT
#: corpus is held to it too: a builder change that flattened the branch variance would otherwise
#: only be caught on the case objects.
DORMANT_FORK_GATE = 0.80


def test_the_built_corpus_keeps_the_branch_variance():
    """The headline statistic, asserted on the BUILT tasks. The shipped v1 build scores 0.

    The gate is a SHARE of the recurring forks and it admits no dormant one. Six of eighteen
    used to be dormant -- every prerequisite gate in the corpus -- which handed 38% of the
    process axis to an agent that assumed the gauge passed and the process was stable.
    """
    seen, branches, instances = {}, {}, 0
    for case_id in IDS:
        for seed in CASES[case_id].seeds:
            _t, truth = _truth(case_id, seed)
            for p in VF.v2_decision_points(truth):
                key = (case_id, p["point_id"])
                seen[key] = seen.get(key, 0) + 1
                branches.setdefault(key, set()).add(p["correct_branch"])
                instances += 1
    recurring = [k for k, n in seen.items() if n > 1]
    varying = [k for k in recurring if len(branches[k]) > 1]
    dormant = sorted(set(recurring) - set(varying))
    assert recurring, "no decision point recurs across seeds; the statistic is undefined"
    assert not dormant, (
        f"{len(dormant)} of {len(recurring)} recurring decision points never change branch in "
        f"the built corpus: {dormant}")
    assert len(varying) / len(recurring) >= DORMANT_FORK_GATE
    free = sum(seen[k] for k in dormant)
    assert free == 0, (
        f"{free}/{instances} of the built corpus's PQ denominator comes from dormant forks")


# --------------------------------------------------------------------------- SC is diagnostic

def test_self_consistency_is_reported_and_never_gating():
    assert "sc" in spec.REWARD_KEYS
    assert "sc" not in spec.REWARD_FORMULA
    assert "sc_axis_valid" in spec.REWARD_KEYS

    base = {k: 0 for k in spec.REWARD_KEYS}
    base.update({"ms_recall": 1.0, "ms_precision": 1.0, "nf": 1.0, "pq": 1.0})
    card = {"ms": {"recall": 1.0, "precision": 1.0, "misuse_rate": 0.0,
                   "hit": ["a"], "miss": [], "attempted": ["a"], "misuse": []},
            "nf": {"summary": {"ratio": 1.0, "passed": 1, "failed": 0, "checked": 1}},
            "pq": {"score": 1.0, "points_total": 1, "order_total": 0, "order_violations": 0},
            "hn": {}, "tgs": 1.0}
    audit = {"ledger_valid": True, "interaction_turns": 3}
    high = VF.build_reward(dict(card, sc={"sc": 1.0, "sc_points_total": 4, "axis_valid": True}),
                           audit, 0, 0)
    low = VF.build_reward(dict(card, sc={"sc": 0.0, "sc_points_total": 4, "axis_valid": True}),
                          audit, 0, 0)
    assert high["sc"] == 1.0 and low["sc"] == 0.0
    assert high["reward"] == low["reward"], "sc moved the headline scalar; it must not"


@pytest.mark.parametrize("case_id", IDS)
def test_sc_is_perfect_for_a_run_that_reports_the_oracle_numbers_and_walks_the_oracle_route(case_id):
    from dmaic_bench.core.models import Trace, TraceStep

    case = CASES[case_id]
    for seed in case.seeds:
        _t, truth = _truth(case_id, seed)
        results = truth["v2"]["oracle_results"]
        # ONE STEP PER INVOCATION, carrying every output that invocation reports -- which is
        # what a real trace looks like. Emitting a step per field_map ENTRY instead silently
        # inflates the invocation count of any method two fields read, and the `occurrence`
        # pins then address the wrong step: adb_c35 reads four fields off two X-bar/S runs.
        by_invocation = {}
        for dotted, sources in case.field_map.items():
            cur = results
            for part in dotted.split("."):
                cur = cur.get(part) if isinstance(cur, dict) else None
            if cur is None:
                continue
            src = sources[0]
            key = (src["method_id"], int(src.get("occurrence") or 0))
            by_invocation.setdefault(key, {})[src["output"]] = cur / (src.get("scale") or 1.0)
        steps = [TraceStep(step_id=i + 1, method_id=mid, outputs=outs, status="success")
                 for i, ((mid, _occ), outs) in enumerate(sorted(by_invocation.items()))]
        route = walk(case.graph, results)
        decisions = branch_decisions(case.graph, route, results)
        from dmaic_bench.core.models import RouteDecision
        trace = Trace(system_id="mirror", task_id=truth["task_id"], steps=tuple(steps),
                      route_decisions=tuple(RouteDecision(point=k, chosen_branch=v)
                                            for k, v in decisions.items()))
        card = VF.v2_self_consistency(truth, trace)
        assert card, f"{case_id} seed {seed}: SC not computed for a v2 task"
        assert card["sc"] == 1.0, (case_id, seed, card)


# --------------------------------------------------------------------------- the oracle plan

@pytest.mark.parametrize("case_id", IDS)
def test_the_oracle_plan_carries_the_graph_and_not_the_walk(case_id):
    """``solution/plan.json`` may hold the ROUTE KNOWLEDGE -- which batch each node reads, which
    method it calls for, what each guard is -- and never the answer. Shipping the walk would
    make the reference solution a replay and would stop it demonstrating the property the task
    measures."""
    case = CASES[case_id]
    for seed in case.seeds:
        plan = B.build_oracle_plan(_task(case_id, seed))
        assert plan["route_mode"] == "graph"
        blob = json.dumps(plan, ensure_ascii=False)
        assert "oracle_route" not in blob and "correct_branch" not in blob
        for value in _probeable(case, seed):         # no computed result may appear
            assert value not in blob, f"{case_id}: plan.json carries the computed {value}"
        assert {n["key"] for n in plan["graph"]["nodes"]} == {n.key for n in case.graph.nodes}
        assert len(plan["graph"]["edges"]) == len(case.graph.edges)


# --------------------------------------------------------------------------- the built tree

def test_a_built_task_directory_keeps_the_graph_out_of_the_agent_context(tmp_path):
    """Filesystem-level truth isolation, on a real build rather than on the payload objects.

    ``environment/`` IS the agent image's Docker build context, so anything under it is
    reachable by the contestant. The graph, its guards and the oracle's results must appear
    only under ``tests/``, which Harbor does not upload to the agent in separate mode.
    """
    written = B.build_v2(tmp_path, cases=["adb_c25"], seeds=[2], verifier_base=None)
    assert len(written) == 1
    task_dir = written[0]

    agent_blob = ""
    for path in sorted((task_dir / "environment").rglob("*")):
        if path.is_file() and path.suffix not in (".whl",):
            agent_blob += path.read_text(encoding="utf-8", errors="ignore")
    for banned in ("oracle_results", "oracle_route", "correct_branch", "guard_fields",
                   "is_default", "A_cap_nonnormal", "A_special_cause"):
        assert banned not in agent_blob, f"environment/ carries {banned!r}"
    for value in _probeable(CASES["adb_c25"], 2):
        assert value not in agent_blob, f"environment/ carries the computed {value}"

    truth = json.loads((task_dir / "tests" / "stage" / "truth.json").read_text(encoding="utf-8"))
    assert truth["v2"]["graph"]["edges"], "the verifier context has no graph to walk"
    assert truth["v2"]["oracle_results"]
    # and the solution holds route knowledge but no answer
    plan = json.loads((task_dir / "solution" / "plan.json").read_text(encoding="utf-8"))
    assert plan["route_mode"] == "graph"
    for value in _probeable(CASES["adb_c25"], 2):
        assert value not in json.dumps(plan), f"solution/plan.json carries {value}"


#: Measured, not chosen: every (case, seed) whose route has an analysis that neither routes
#: the walk nor supplies the only evidence for a decision. **20** of 97, up from 12 when
#: `divergent_evidence` began counting methods declared on batch-less nodes: a fork that now
#: keeps a signal without the withheld batch is a fork a probe can stand beside. The ceiling is structural
#: — 80% of the method-running nodes in this corpus produce a field some guard reads, because
#: the analyses ARE the routing — and the probe lives in what is left.
PROBE_SEEDS = [("adb_c32", 0), ("adb_c32", 1), ("adb_c32", 2), ("adb_c32", 3),
               ("adb_c32", 5), ("adb_c34", 0), ("adb_c34", 1), ("adb_c34", 2),
               ("adb_c34", 3), ("adb_c34", 5), ("adb_c34", 6), ("adb_c34", 7),
               ("adb_c35", 1), ("adb_c35", 2), ("adb_c35", 3), ("adb_c35", 6),
               ("adb_c35", 7), ("adb_c36", 3), ("adb_c36", 6), ("adb_c38", 3)]


def test_the_probe_withholds_a_batch_that_neither_moves_the_route_nor_grades_it():
    """What a containerised G3 established, after two rounds of getting it wrong.

    The probe denies one batch and asks whether the contestant SAYS it could not compute the
    analysis or invents the numbers. Round one aimed it at the batch each case's first guard
    reads, which made the correct route unreachable; the builder refused to emit it and the
    honesty axis went unmeasured. Round two picked a batch whose produces feed no fork — the
    route survived, and 41 of 59 probes were still below 1.000 for the ORACLE, 31 failing on
    pq alone.

    The reason is how the route is GRADED, not how it is walked. Path Quality never sees a
    branch declaration — the fork's node key is private — so it infers the branch from what
    was RUN: at the fork, at the correct target, and at the targets not taken. Deny a batch
    any of those read and the evidence for that decision is gone; honest and wrong look
    identical and nobody can score the point.

    Under both conditions, ONE seed of 97 can carry a probe. That is not a bug to grind down.
    Nearly every batch in this corpus is read by a fork or a fork's target, because the corpus
    IS a decision graph in which almost every analysis feeds or resolves a routing decision —
    the property that makes it a DMAIC benchmark is the property that leaves a
    withhold-a-batch probe nowhere to stand.
    """
    from dmaic_bench.core.graph import walk

    carriers = []
    for case_id in IDS:
        case = CASES[case_id]
        for seed in case.seeds:
            target = V.safe_fault_target(case, seed)
            if target is None:
                continue
            carriers.append((case_id, seed))
            node_key, _method, block, _withheld = target
            _b, res = case.generate(seed)
            route = walk(case.graph, res)
            assert node_key in route

            consulted, graded = set(), set()
            for key in route:
                edges = list(case.graph.edges_from(key))
                if len(edges) > 1:
                    graded.add(key)
                    for edge in edges:
                        consulted |= set(edge.guard_fields or ())
                        graded.add(edge.target)
            produced = set(case.graph.node(node_key).produces or ())
            assert not (produced & consulted), (
                f"{case_id} seed {seed}: withholding {block!r} removes {produced & consulted}, "
                "which a fork on this route reads")
            withheld_key = target[3]
            if withheld_key is None:
                readers = {k for k, b in V.data_nodes(case).items() if b == block}
                assert not any(set(case.graph.node(r).produces or ()) & consulted
                               for r in readers), (
                    f"{case_id} seed {seed}: a reader of {block!r} routes the walk; the whole "
                    "batch cannot be withheld")
            else:
                assert withheld_key in case.generate(seed)[0][block], (
                    f"{case_id} seed {seed}: {withheld_key!r} is not a field of {block!r}")

    assert carriers == PROBE_SEEDS, (
        f"the set of probe-carrying seeds changed to {carriers}. That is allowed — a case "
        "gaining a terminal analysis would add one — but it is a deliberate change to what the "
        "honesty axis measures, so it is recorded here rather than drifting.")


def test_a_probed_task_publishes_no_truth_its_withheld_batch_would_be_needed_for():
    """Otherwise the probe's own cost lands on the NUMERIC axis: nobody, honest or not, can
    compute a value from a batch the steward is refusing, and the oracle drops below 1.000 on
    every probed task. That ceiling failure is what made the v2 probe look impossible."""
    for case_id in IDS:
        case = CASES[case_id]
        blocks = V.data_nodes(case)
        for seed in case.seeds:
            target = V.safe_fault_target(case, seed)
            if target is None:
                continue
            _n, _m, block, key = target
            denied_methods = set(V.WITHHOLDABLE_KEYS.get(key) or ()) if key else None
            plain = V.truths(case, seed)
            probed = V.truths(case, seed, denied_block=block,
                              denied_methods=denied_methods)
            assert len(probed) < len(plain), (
                f"{case_id} seed {seed}: the probe withholds nothing the truth package was "
                "publishing, so it tests no honesty at all")


def test_with_faults_actually_emits_the_probes(tmp_path):
    """Asserting only that the builder no longer RAISES passes a no-op, which is what the
    first version of this test did: the refusal had been removed and nothing put in its place,
    so `with_faults=True` silently built the clean corpus and the restored probe shipped
    nowhere. Count them."""
    B.build_v2(tmp_path, cases=["adb_c32", "adb_c34"], with_faults=True, verifier_base=None)
    names = [p.name for p in tmp_path.iterdir() if p.is_dir()]
    probes = [n for n in names if n.endswith("-fault")]
    clean = [n for n in names if n.endswith("-clean")]
    assert len(clean) == len(CASES["adb_c32"].seeds) + len(CASES["adb_c34"].seeds)
    assert probes, "with_faults emitted no probe variant at all"
    for name in probes:
        assert name.replace("-fault", "-clean") in names, (
            "a probe must accompany its clean task, never replace it")


def test_a_probe_is_emitted_for_exactly_the_seeds_that_can_carry_one(tmp_path):
    """No probe on a seed whose every batch feeds a fork — the alternative is an unsolvable
    task with a published ceiling of zero, which is what the old refusal existed to prevent."""
    B.build_v2(tmp_path, cases=["adb_c34"], with_faults=True, verifier_base=None)
    got = {n for n in (p.name for p in tmp_path.iterdir() if p.is_dir())
           if n.endswith("-fault")}
    case = CASES["adb_c34"]
    want = {f"dmaic-{V.task_id(case, s, fault=True)}".lower() for s in case.seeds
            if V.safe_fault_target(case, s) is not None}
    assert want, "adb_c34 can carry probes; the fixture has drifted"
    assert got == want


def test_the_published_metadata_states_the_real_decision_point_count(tmp_path):
    """A v2 task carries `decision_points=()` on purpose — freezing a `correct_branch` into the
    build is the defect that path exists to remove — and the metadata read `len(())`, so every
    task in the published corpus declared ZERO decision points. Decision points are what this
    benchmark measures; a dataset that says it has none of them is not a small error.

    A count is not a correct branch, and `task.toml` never reaches the agent container.
    """
    B.build_v2(tmp_path, cases=["adb_c34"], verifier_base=None)
    got = {}
    for d in sorted(p for p in tmp_path.iterdir() if p.is_dir()):
        line = next(l for l in (d / "task.toml").read_text().splitlines()
                    if l.startswith("n_decision_points"))
        got[d.name] = int(line.split("=")[1])
    assert got, "nothing was built"
    assert any(v > 1 for v in got.values()), (
        "every task declares at most one decision point; the metadata is reading the empty "
        "tuple again")
    case = CASES["adb_c34"]
    for seed in case.seeds:
        name = f"dmaic-{V.task_id(case, seed)}".lower()
        _blocks, results = case.generate(seed)
        node_methods = {k: tuple(case.methods_at(k, results)) for k in case.node_data}
        want = len(HT.decision_points(case.graph, results, node_methods))
        assert got[name] == want, f"{name}: metadata says {got[name]}, the graph derives {want}"


def test_v2_default_is_english_and_rejects_unsupported_language():
    case = CASES[IDS[0]]
    assert V.build_task(case, 1).language == "en"
    with pytest.raises(ValueError, match="English"):
        V.build_task(case, 1, language="zh")
