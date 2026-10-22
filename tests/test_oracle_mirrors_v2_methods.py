"""The reference solution must reproduce every v2 truth and walk every v2 route.

`solve.sh` is a HAND-PORT. It talks to the steward over HTTP and recomputes everything with
numpy/scipy inside the agent container, so it is a second implementation of every method the
corpus grades — and the ceiling every contestant is read against. When it drifts from the
verifier the ceiling drops, and it drops for a reason that looks exactly like a hard task.

Nothing was checking it against the v2 projects. `test_oracle_round_trip` runs the real script
end to end but only on `adb_c24`, and `tests/test_v2_runtime.py` scores an in-process
`OracleAgent` that walks the decision graph directly — a different program. Two defects
survived to a live containerised run because of that gap:

* `m_rsm` emitted no `lackOfFitPValue` at all, so `adb_c39`'s route read a missing field, fell
  to the default branch, and the reference solution walked a branch its own scorer called
  **incorrect**. Ceiling 0.777.
* `m_equal_variances` defaults to Bartlett where the verifier is Levene/median, and
  `adb_c37`'s batch declared no convention. 0.573 against 0.879 on a 0.08 tolerance.
  Ceiling 0.952.

Both are task defects wearing the costume of hard tasks, which is the failure mode G3 exists
for. This test is G3's method-level half, run without a container.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                                # noqa: E402

from dmaic_bench.core.graph import walk                      # noqa: E402
from dmaic_bench.v2 import harbor_truth as HT                # noqa: E402
from dmaic_bench.v2 import registry                          # noqa: E402
from dmaic_harbor import v2_tasks                            # noqa: E402

SOLVE_SH = _ROOT / "harbor" / "templates" / "solution" / "solve.sh"
CASES = registry.discover()


@pytest.fixture(scope="module")
def oracle():
    """The analysis program solve.sh writes out, imported as a module.

    Same technique as `harbor/tests/test_oracle_mirrors_guard_dsl.py`: execute our own template
    rather than re-implement it, so the thing under test is the thing that ships.
    """
    lines = SOLVE_SH.read_text(encoding="utf-8").split("\n")
    start = next(i for i, l in enumerate(lines)
                 if l.startswith('cat > "$SCRATCH/oracle_analysis.py"'))
    end = next(i for i, l in enumerate(lines) if l.strip() == "PYEOF" and i > start)
    module = types.ModuleType("oracle_analysis")
    exec(compile("\n".join(lines[start + 1:end]),          # noqa: S102 - our own template
                 "solve.sh:oracle_analysis", "exec"), module.__dict__)
    assert "METHODS" in module.__dict__, "solve.sh no longer exposes a METHODS table"
    return module


def _run_route(oracle, case, seed):
    """Run solve.sh's own methods along the oracle route, on the real batches.

    Returns ``(by_method, by_occurrence, route, results)``. Per-INVOCATION outputs are kept as
    well as the merged view, because a case that runs a method twice — two agreement studies,
    two charts, two capability indices — has two answers and the merged view keeps only the
    last. Collapsing them here would make this test report a route defect on the very cases
    whose ``field_map`` pins its sources to an invocation to avoid exactly that.
    """
    blocks, results = case.generate(seed)
    by_method, by_occurrence, counts = {}, {}, {}
    route = walk(case.graph, results)
    for node in route:
        block = blocks.get((case.node_data or {}).get(node))
        if block is None:
            continue
        for method_id in case.methods_at(node, results):
            fn = oracle.METHODS.get(method_id)
            assert fn is not None, (
                f"{case.case_id} seed {seed}: {node} calls {method_id}, which solve.sh does "
                f"not implement — the reference solution cannot run this task's route")
            try:
                out = fn(dict(block))
            except Exception as exc:                        # noqa: BLE001
                pytest.fail(f"{case.case_id} seed {seed}: solve.sh's {method_id} raised on the "
                            f"{node} batch: {type(exc).__name__}: {exc}")
            numeric = {k: v for k, v in out.items() if isinstance(v, (int, float))}
            index = counts.get(method_id, 0)
            counts[method_id] = index + 1
            by_occurrence[(method_id, index)] = numeric
            by_method.setdefault(method_id, {}).update(numeric)
    return by_method, by_occurrence, route, results


@pytest.mark.parametrize("case_id", sorted(CASES))
def test_the_reference_solution_reproduces_every_published_truth(oracle, case_id):
    """Against the PUBLISHED truth package, not the case's raw declaration.

    What ships is `v2_tasks.truths(case, seed)`: filtered to this seed's route, and carrying the
    alternative conventions each truth admits at its own precision. Checking the raw declaration
    instead would fail every truth whose second convention is the one the reference solution
    computes — which is most of the gauge study.
    """
    case = CASES[case_id]
    bad = []
    for seed in case.seeds:
        _by_method, by_occurrence, _route, _res = _run_route(oracle, case, seed)
        for entry in v2_tasks.truths(case, seed):
            # A truth is satisfied by ANY invocation of its method, as nf._claim_step does: a
            # case that runs capability twice publishes a truth for each, and either invocation
            # may be the one this truth names.
            seen = [v[entry.field] for (mid, _i), v in sorted(by_occurrence.items())
                    if mid == entry.method_id and entry.field in v]
            if not seen:
                continue          # not produced on this seed's route; nothing was owed
            windows = [(entry.expected, entry.tol)] + [(v, t) for _c, v, t in
                                                       (entry.accepts or ())]
            if not any(abs(float(got) - float(want)) <= float(tol)
                       for got in seen for want, tol in windows):
                bad.append((seed, entry.method_id, entry.field,
                            [round(float(v), 6) for v in seen],
                            [(round(float(w), 6), t) for w, t in windows]))
    assert not bad, (
        "solve.sh disagrees with every window the published truth admits "
        f"(seed, method, field, got, windows): {bad}")


@pytest.mark.parametrize("case_id", sorted(CASES))
def test_the_reference_solution_walks_the_route_its_own_scorer_expects(oracle, case_id):
    """The failure that matters most: not a number out of tolerance, but a BRANCH.

    A guard reading a field solve.sh does not emit falls through to the default edge, and the
    reference solution then does different work from the one the truth package derives. The
    ceiling drops and every contestant on that task is read against a broken maximum.
    """
    case = CASES[case_id]
    for seed in case.seeds:
        by_method, by_occurrence, route, results = _run_route(oracle, case, seed)
        observed, _seen, _unobs = HT.observed_results(
            dict(case.field_map or {}), by_method, results, by_occurrence)
        # batch_facts are structural readings of a batch, not method outputs; the oracle makes
        # them by looking, exactly as the reference solution's plan tells it to.
        for field in (case.batch_facts or {}):
            cur, parts = results, field.split(".")
            for part in parts:
                cur = cur.get(part) if isinstance(cur, dict) else None
            if cur is not None:
                tgt, keys = observed, parts
                for key in keys[:-1]:
                    tgt = tgt.setdefault(key, {})
                tgt[keys[-1]] = cur
        assert walk(case.graph, observed) == route, (
            f"{case_id} seed {seed}: on its OWN numbers the reference solution walks\n"
            f"  {walk(case.graph, observed)}\nbut the truth package derives\n  {route}")
