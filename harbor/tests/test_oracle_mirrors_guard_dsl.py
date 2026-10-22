"""The reference solution hand-ports the guard parser; this stops the port drifting.

`solution/solve.sh` runs inside the AGENT container, which deliberately does not carry the bench
package, so it cannot import `dmaic_bench.core.graph`. Its guard evaluator is therefore a
hand-copy of a recursive-descent parser -- and a routing decision made by a parser that has
drifted from the one the verifier scores against is the worst kind of benchmark defect: the
reference solution takes a branch the verifier calls wrong, so the CEILING moves and every other
number on the board becomes unreadable.

Same guarantee as `test_oracle_mirrors_perturber`: the copy is allowed, drifting is not. The
cases are drawn from the real corpus's guards plus the shapes that separate the two parsers if
one of them is edited carelessly -- precedence, defaults, missing fields and bare enums.
"""
from __future__ import annotations

import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
HARBOR_ROOT = os.path.dirname(HERE)
BENCH_ROOT = os.path.dirname(HARBOR_ROOT)
for _p in (os.path.join(HARBOR_ROOT, "src"), BENCH_ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dmaic_bench.core import graph as core_graph      # noqa: E402
from dmaic_harbor import v2_tasks as V                # noqa: E402

SOLVE_SH = os.path.join(HARBOR_ROOT, "templates", "solution", "solve.sh")


@pytest.fixture(scope="module")
def oracle():
    """Execute just the ported guard block out of solve.sh, without running the oracle."""
    src = open(SOLVE_SH, encoding="utf-8").read()
    start = src.index("# ------------------------------------------------------------------ guard DSL")
    end = src.index("def observe_batch(")
    ns: dict = {}
    exec(src[start:end], ns)          # noqa: S102 - executing our own template, by design
    assert "guard_holds" in ns
    return ns


RESULTS = {
    "msa": {"pctSV": 0.1972, "ndc": 7},
    "imr": {"outOfControl": 0},
    "normality": {"pValue": 0.0525},
    "cap": {"ppk": 2.0335, "verdict": "good"},
    "chart": {"varyingN": 1},
    "screen": {"modelPValue": 0.06642},
    "machine": {"pValue": 0.0031},
    "scope": {"topCategoryPct": 62.5},
    "sustain": {"varyingN": 0},
    "agree": {"kappaMin": 0.83},
    "xbar": {"outOfControl": 0},
    "chart1": {"outOfControl": 0},
    "chart2": {"outOfControl": 2},
    "confirm": {"pValue": 0.2399, "concordance": 0.8},
    # second-domain pilot (DMAIC_PILOT_DOMAINS=1)
    "qc": {"minReplicates": 4, "sampleFailFraction": 0.0125},
    "design": {"confounded": 0, "batchCount": 2},
    "de": {"nSignificant": 31},
    "strat": {"separated": 0, "pc1PValue": 0.0},
    "assoc": {"nSignificant": 1},
    "replic": {"nReplicated": 0},
    "variances": {"pValue": 0.001},
    "recipes": {"factorPValue": 0.4338},
    "kruskal": {"pValue": 0.0002},
    "cap1": {"cpk": 0.71},
    "cap2": {"cpk": 1.63},
    "agree1": {"kappaMin": 0.42},
    "agree2": {"kappaMin": 0.97},
    "pchart": {"outOfControl": 0, "centerLine": 0.00599},
    "factors": {"modelPValue": 0.9923},
    "effect": {"pValue": 0.2239},
    "after": {"avgP": 0.00336},
    "rsm": {"lackOfFitPValue": 0.0019},
    "opt": {"predictedResponse": 48.36},
}

EXPRESSIONS = [
    # every guard the shipped v2 corpus actually uses
    "msa.pctSV <= 0.30",
    "imr.outOfControl == 0",
    "imr.outOfControl > 0",
    "normality.pValue >= 0.05",
    "cap.ppk >= 1.33",
    "chart.varyingN == 0",
    "screen.modelPValue < 0.05",
    "screen.modelPValue >= 0.05",
    "agree.kappaMin >= 0.60",
    "pchart.outOfControl == 0",
    "cap.avgP <= 0.05",
    "cap.avgP <= 0.0015",
    "msa.pctSV <= 0.30 and msa.ndc >= 5",
    "machine.pValue < 0.05",
    "agree1.kappaMin >= 0.60",
    "agree2.kappaMin >= 0.60",
    "cap.avgP <= 0.02",
    "xbar.outOfControl == 0",
    "xbar.outOfControl == 0 and xbar.rangeOutOfControl == 0",
    "cap.cpk >= 1.33",
    "cap.cp >= 1.33",
    "chart1.outOfControl == 0",
    "chart2.outOfControl == 0",
    "chart1.outOfControl == 0 and chart1.sOutOfControl == 0",
    "chart2.outOfControl == 0 and chart2.sOutOfControl == 0",
    "sustain.pointSize >= 2",
    "cap1.cpk >= 1.33 and cap2.cpk >= 1.33",
    # a guard whose right-hand side is another FIELD, not a literal
    "cap1.cpk < cap2.cpk",
    "confirm.pValue < 0.05",
    "variances.pValue >= 0.05",
    "recipes.factorPValue < 0.05",
    "kruskal.pValue < 0.05",
    # second-domain pilot guards (exercised whether or not the pilot is discovered)
    "qc.minReplicates >= 3",
    "design.confounded == 0 and design.batchCount == 1",
    "design.confounded == 0",
    "de.nSignificant >= 1",
    "confirm.concordance >= 0.75",
    "qc.sampleFailFraction <= 0.10",
    "strat.separated == 0 and strat.pc1PValue >= 0.05",
    "strat.separated == 0",
    "assoc.nSignificant >= 1",
    "replic.nReplicated >= 1",
    "pchart.outOfControl > 0",
    "pchart.centerLine <= 0.0025",
    "factors.modelPValue < 0.05",
    "effect.pValue < 0.05",
    "after.avgP <= 0.0025",
    "scope.topCategoryPct >= 50",
    "sustain.varyingN == 0",
    "rsm.lackOfFitPValue >= 0.05",
    "opt.predictedResponse >= 55",
    # and the shapes that separate two parsers if either is edited carelessly
    "",
    "   ",
    "msa.ndc >= 5 and msa.pctSV < 0.30",
    "msa.ndc >= 5 and msa.pctSV < 0.10",
    "msa.ndc >= 5 or msa.pctSV < 0.10",
    "not imr.outOfControl > 0",
    "not (msa.ndc >= 5 and msa.pctSV < 0.10)",
    "(normality.pValue >= 0.05 or cap.ppk >= 1.33) and imr.outOfControl == 0",
    "cap.verdict in [good, marginal]",
    "cap.verdict in [poor]",
    "cap.verdict == good",
    "cap.verdict != good",
    "cap.verdict == 'good'",
    "missing.field >= 1",              # a comparison over an unobserved field is never satisfied
    "missing.field == 0",
    "not missing.field",
    "true",
    "false",
    "true and not false",
    "1 >= 0",
    "-1.5 < 0",
    "1e-3 < 0.05",
]


@pytest.mark.parametrize("expr", EXPRESSIONS)
def test_the_ported_parser_agrees_with_the_scorers_parser(oracle, expr):
    want = core_graph.evaluate(expr, RESULTS)
    got = oracle["guard_holds"](expr, RESULTS)
    assert got == want, (
        f"solve.sh routes on {expr!r} as {got} while the verifier scores it as {want}. "
        "The reference solution would take a branch its own scorer calls wrong.")


def test_every_guard_in_the_shipped_corpus_is_covered_by_this_test():
    """A guard nobody exercises here is a guard whose port is unverified."""
    used = set()
    for case in V.discover().values():
        for edge in case.graph.edges:
            if edge.when:
                used.add(edge.when.strip())
        for clauses in (case.method_policy or {}).values():
            for clause in clauses:
                if clause.get("when"):
                    used.add(clause["when"].strip())
    missing = sorted(used - {e.strip() for e in EXPRESSIONS})
    assert not missing, f"guards used by the corpus but not exercised here: {missing}"


def test_the_two_parsers_agree_on_every_edge_of_every_shipped_seed(oracle):
    """The end-to-end statement: for every case, seed and edge, the ported parser and the
    scorer's parser make the SAME routing decision on the same numbers."""
    for case_id, case in sorted(V.discover().items()):
        for seed in case.seeds:
            _blocks, results = case.generate(seed)
            for edge in case.graph.edges:
                want = core_graph.evaluate(edge.when or "", results)
                got = oracle["guard_holds"](edge.when or "", results)
                assert got == want, (case_id, seed, edge.source, edge.target, edge.when)


def test_a_missing_field_never_satisfies_a_guard_in_either_parser(oracle):
    """The rule that makes an un-computed value fail closed rather than route by accident."""
    for expr in ("cap.ppk >= 1.33", "cap.ppk < 1.33", "cap.ppk == 0"):
        assert core_graph.evaluate(expr, {}) is False
        assert oracle["guard_holds"](expr, {}) is False
