"""Does the verifier grade what the instruction asks for?

``build.assert_no_method_leak`` guards one direction: the instruction must not name the method,
because choosing it is the measured capability. Nothing guarded the other direction, and that is
where the worst defect this benchmark has shipped lived.

Path Quality compared a contestant's declared branch against ``correct_branch`` -- a decision-graph
node key that is private to the case module and appears in no instruction, no batch and no steward
reply. The verifier was testing for a string the task never gave anyone a way to produce, so
declining correctly and pressing on wrongly were the same trace. Measured across 7 models x 9 such
tasks: reward 0.000 on all 63, beside ``ms_recall`` 1.000 and ``nf`` 1.000. It stayed invisible for
a whole campaign because the oracle is generated from the truth and is the one agent that can name
the key.

Tencent's environment-task delivery requirements call an instruction/verifier mismatch "a severe
defect" and ask for it to be justified per component. This module states the property as five
checks a case must satisfy, each one the generalisation of a defect that actually shipped:

  C1  every graded truth names a method some oracle route actually calls          ERROR
  C2  every field a guard reads is one a contestant's own trace can express       ERROR
  C3  every graded decision point can be scored WRONG by some trace               ERROR
  C4  a node does not declare methods that scoring will never require             WARN
  C5  the brief asks for the artifact the verifier reads                          ERROR
  C6  two fields read one method's one output from nodes that can co-occur        ERROR
  C6W the same, but no shipped seed reaches both nodes -- latent, not live         WARN
  C7  every gate a batch is locked behind can be declared by a method on its route  ERROR

C4 is a warning rather than an error because the mismatch it names is inert in the built task:
required methods are keyed on the BATCH a node reads, so a node without one contributes nothing
to the requirement set, to ``plan.json``, or to branch evidence. What it costs is a reader of the
case module, who sees ``C_control`` declaring a control chart and reasonably concludes the agent
must run one. Some of those declarations are deliberate and documented -- ``sla_attribute`` says
in as many words why its improvement nodes ship no batch -- so the set is pinned rather than
emptied, and a new one has to declare itself.

Findings are returned rather than raised, so a caller can report all of them at once.
"""
from __future__ import annotations

from dmaic_bench.core.graph import branch_decisions, walk
from dmaic_bench.v2 import harbor_truth as HT

#: Decision points that are knowingly unobservable, with the reason. An entry here is a point the
#: benchmark cannot see, declared rather than silently tolerated. It is the same set as
#: ``tests/test_sc_branch_inference.KNOWN_UNOBSERVABLE``, which states the sibling property for
#: Self-Consistency, and a test asserts the two do not drift apart.
EXEMPT_POINTS = {
    ("adb_c25", "A_cap_normal"): "-> C_control | A_root_cause, neither branch carries a batch",
    ("adb_c28", "A_cap_normal"): "same fork, same reason",
    ("adb_c27", "A_screen"): "-> I_doe (no batch) | A_remeasure (no methods)",
    ("adb_c30", "A_cap_normal"): "-> C_control | A_root_cause, neither branch carries a batch",
}


def _node_methods(case, results):
    return {k: tuple(case.methods_at(k, results)) for k in case.node_data}


def _dotted(mapping, field):
    cur = mapping
    for part in str(field).split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    return True


#: check -> severity. Only ERROR findings fail a build.
# NOTE C6. The header above calls it an ERROR and this table has never listed it, so
# `errors()` has always dropped it — C6 has been inert since it was written. Promoting it
# here fires on 7 cases, and a look at the first says the check over-fires: adb_c34 maps
# four fields onto `capability.normal`, but they come back from ONE invocation, which is
# not the last-wins collision C6 exists to catch. Left inert deliberately rather than
# promoted as a side effect of adding C7; it needs its own pass.
SEVERITY = {"C1": "ERROR", "C2": "ERROR", "C3": "ERROR", "C4": "WARN", "C5": "ERROR",
            "C6": "ERROR", "C6W": "WARN", "C7": "ERROR"}


def errors(findings) -> list:
    return [f for f in findings if SEVERITY.get(f[0]) == "ERROR"]


def check_case(case) -> list:
    """``[(check, seed, detail)]`` -- every correspondence finding for one v2 case."""
    out = []
    routed_methods, per_seed = set(), {}
    for seed in case.seeds:
        blocks, res = case.generate(seed)
        nm = _node_methods(case, res)
        route = walk(case.graph, res)
        per_seed[seed] = (blocks, res, nm, route)
        routed_methods |= {m for key in route for m in nm.get(key, ())}

    # C1 -- a truth for a method no route calls grades work the brief never asks for.
    for truth in case.truth_fields:
        mid = truth.get("method_id")
        if mid not in routed_methods:
            out.append(("C1", None,
                        f"truth {truth.get('field')} is graded from {mid}, which no oracle "
                        f"route calls"))

    # C2 -- a guard over a field no trace can express is a field only the oracle can answer.
    observable = set(case.field_map or {}) | set(case.batch_facts or {})
    for edge in case.graph.edges:
        for field in edge.guard_fields or ():
            if field not in observable:
                out.append(("C2", None,
                            f"guard field {field} ({edge.source} -> {edge.target}) is in neither "
                            f"field_map nor batch_facts"))

    for seed, (blocks, res, nm, route) in per_seed.items():
        # C3 -- the pq defect itself. A point is only worth grading if SOME trace can score it
        # wrong; where no branch out of the fork entails work the others do not, every
        # contestant scores the same on it whatever it did, and the point measures nothing.
        # The private ``correct_branch`` key was the whole handle, and it reaches no contestant.
        for point in HT.decision_points(case.graph, res, nm, case.method_policy):
            pid = point.get("point_id")
            if (case.case_id, pid) in EXEMPT_POINTS:
                continue
            targets = [e.target for e in case.graph.edges_from(pid) if e.target != pid]
            if not any(HT.convergent_evidence(case.graph, pid, t, nm) for t in targets):
                out.append(("C3", seed,
                            f"decision point {pid} cannot be scored wrong by any trace: no "
                            f"branch out of it entails work the others do not"))

        # C4 -- a declaration scoring will never act on. Read from the GRAPH, not from ``nm``:
        # ``nm`` is keyed on node_data, so a node missing from node_data has no methods there
        # and the check would exempt exactly the case it exists to name.
        for key in route:
            methods = tuple(case.methods_at(key, res))
            if not methods:
                continue
            block_key = (case.node_data or {}).get(key)
            if not block_key:
                out.append(("C4", seed,
                            f"node {key} declares {sorted(methods)} but reads no batch, so "
                            f"nothing will ever require them"))
            elif block_key not in blocks:
                out.append(("C4", seed,
                            f"node {key} reads batch {block_key!r}, which generate() did not "
                            f"emit"))

    # C6 -- field_map is the ROUTING table, and `merged_outputs` is last-wins per method. An
    # entry for a field no guard reads adds a second producer under the same method_id, and the
    # later invocation's value then answers for the guard field too. Measured while extending
    # adb_c32: the sustaining chart's out-of-control count overwrote the lot record's, and the
    # Self-Consistency re-walk took the in-control branch on a seed whose record is not.
    guard_fields = {f for e in case.graph.edges for f in (e.guard_fields or ())}
    # C6 -- two fields reading the SAME output of the SAME method, from nodes that can both
    # be on one route, with nothing to tell the invocations apart.
    #
    # Rewritten on 2026-09-13, and the first version is why it had never fired: it flagged any
    # method feeding two fields, which is the ordinary case (one Gage R&R run reports pctSV AND
    # ndc; one capability run reports cp, cpk and ppk). Those come back from ONE invocation and
    # read DIFFERENT output keys, so there is nothing to collide. It fired on 10 cases, all of
    # them that shape, which is presumably why it was left out of SEVERITY and went inert.
    #
    # The real hazard is narrower: `merged_outputs` is last-wins over INVOCATIONS, so two
    # fields reading one method's one output can only be told apart by an `occurrence` pin --
    # and only need to be when their nodes can actually co-occur. adb_c35 reads
    # `basic.correlation.correlationCoefficient` at two nodes with no pin, and is safe today
    # only because those two nodes sit on mutually exclusive branches. That is a fact about
    # the seeds, not about the design, so it is reported as a WARN: a seed reaching both would
    # bind the second study's r to the first.
    fields_by_source = {}
    for field, sources in (case.field_map or {}).items():
        for src in sources or ():
            if not isinstance(src, dict):
                continue
            key = (str(src.get("method_id")), str(src.get("output")))
            fields_by_source.setdefault(key, []).append((field, src.get("occurrence")))

    node_of = {}
    for node in case.graph.nodes:
        for field in (node.produces or ()):
            node_of.setdefault(field, set()).add(node.key)

    co_occurring = set()
    for seed in case.seeds:
        try:
            route = set(walk(case.graph, case.generate(seed)[1]))
        except Exception:  # noqa: BLE001
            continue
        co_occurring.add(frozenset(route))

    for (method_id, output), readers in sorted(fields_by_source.items()):
        if len(readers) < 2:
            continue
        pins = [occ for _f, occ in readers]
        if len(set(pins)) == len(pins) and None not in pins:
            continue                        # every invocation is pinned to its own occurrence
        fields = sorted(f for f, _ in readers)
        nodes = [node_of.get(f, set()) for f in fields]
        together = any(all(ns & route for ns in nodes if ns) for route in co_occurring)
        if together:
            out.append(("C6", None,
                        f"{fields} all read {method_id}.{output} and can be on one route "
                        "together, with no occurrence pin; last-wins binds them to the same "
                        "invocation"))
        else:
            out.append(("C6W", None,
                        f"{fields} all read {method_id}.{output} with no occurrence pin. Safe "
                        "only because no shipped seed reaches their nodes together -- a fact "
                        "about the seeds, not the design"))

    # C7 -- a gate the steward holds a batch against must be one the run can actually satisfy.
    #
    # Found by G3, after it had already cost a full control run. The gate derivation added in
    # P0 reads a guard like `settings.modelPValue < 0.05` and emits `screening_significant`,
    # whose declare key is `any_factor_significant`. In adb_c38 the method producing that
    # p-value is `regression.ols`, and only `doe.factorial_analysis` declared the key -- so
    # the batch behind the gate could not be unlocked by ANYONE, the reference solution
    # included, and the oracle scored 0.706 on a task that had been 1.000 in three prior runs.
    #
    # The declare keys are read from the reference solution itself, because it is the thing
    # that has to satisfy the gate. A key nothing declares is a locked batch nobody opens.
    try:
        declarable = _declarable_keys()
    except Exception:  # noqa: BLE001 - a source tree without the template still checks C1-C6
        declarable = None
    if declarable is not None:
        from dmaic_harbor import spec, v2_tasks
        for block, rule in sorted(v2_tasks.locks(case).items()):
            for gate in rule.get("gates") or ():
                key = (spec.PUBLIC_GATES.get(gate) or {}).get("field")
                if not key:
                    continue
                methods = declarable.get(key) or set()
                on_route = {m for seed in case.seeds
                            for ms in _node_methods(case, case.generate(seed)[1]).values()
                            for m in ms}
                if not (methods & on_route):
                    out.append(("C7", None,
                                f"batch {block!r} is locked behind {gate!r}, which reads the "
                                f"declaration {key!r}; no method this case runs declares it "
                                f"(declared by {sorted(methods) or 'nothing'})"))

    # C5 -- the verifier reads report.md; the brief has to ask for it.
    brief = f"{case.context}\n{case.goal}".lower()
    if "report" not in brief:
        out.append(("C5", None, "the brief never asks for a report, and the verifier grades one"))
    return out


def _declarable_keys() -> dict:
    """``{declare_key: {method_id, ...}}``, read out of the reference solution.

    Static, because the alternative is executing every method against fabricated data. Each
    ``def m_xxx`` block is scanned for the ``_declare`` mapping it emits, and the METHODS table
    at the end of the template maps method ids onto those functions.
    """
    import re
    from pathlib import Path as _P

    root = _P(__file__).resolve().parents[2]
    text = (root / "harbor" / "templates" / "solution" / "solve.sh").read_text(encoding="utf-8")
    by_func: dict = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"^def (m_\w+)\(", line)
        if m:
            current = m.group(1)
            continue
        if current and '"_declare"' in line:
            body = line.split('"_declare"', 1)[1]
            by_func.setdefault(current, set()).update(re.findall(r'"(\w+)"\s*:', body))
        elif current and re.search(r'\bout\["_declare"\]\s*=', line):
            by_func.setdefault(current, set()).update(
                re.findall(r'"(\w+)"\s*:', line.split("=", 1)[1]))
    out: dict = {}
    for mid, func in re.findall(r'^\s*"([\w.]+)":\s*(m_\w+),?\s*$', text, re.M):
        for key in by_func.get(func, ()):
            out.setdefault(key, set()).add(mid)
    return out


def check_corpus(cases) -> dict:
    """``{case_id: findings}``, empty values dropped."""
    out = {}
    for cid, case in sorted(cases.items()):
        findings = check_case(case)
        if findings:
            out[cid] = findings
    return out
