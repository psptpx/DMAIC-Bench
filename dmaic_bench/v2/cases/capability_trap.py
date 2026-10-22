"""capability_trap — a D2 method-selection trap (v3).

The data is a moderately right-skewed process characteristic. It has a well-defined mean and SD, so
the NORMAL capability formula returns a plausible-looking Ppk — a careless agent reports it. But an
Anderson-Darling test rejects normality (p<0.05), so the methodologically-correct choice is a
NON-NORMAL capability analysis. `capability.normal` here is MISUSE even though it yields a number;
only an agent that tests normality first selects correctly. This is the trap v2 could not express
(it fed the method). Seeds 0-2 vary skew magnitude; a "clean-normal" control seed (3) is included so
the SAME method (capability.normal) is correct there — proving method-validity is data-conditioned.

A FOURTH SHAPE, AND WHY THE STABILITY FORK HAD TO BECOME ONE. ``M_stability`` was written with
two guarded edges that BOTH pointed at ``A_capability``, so the guard was decorative: the correct
branch was ``A_capability`` on every seed no matter what the chart showed, and the fork was one
of the six in this corpus that no seed could exercise. Capability is not defined on an
out-of-control process (Montgomery ISQC 6e §8.2), so the out-of-control edge now leads where the
methodology says it does — a special-cause investigation — and seed 4 is a record that goes
there. The graded variable on the other four seeds is unchanged.
"""
from __future__ import annotations

import math
import random

from dmaic_bench.core.graph import DecisionGraph, GraphNode, GuardedEdge, walk
from dmaic_bench.truth import verifiers
from dmaic_bench.v2.cases import _fixtures as _f
from dmaic_bench.v2.models import V2Case

_LSL, _USL = 40.0, 100.0

GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define", label="Scope: capability of the critical characteristic"),
        # `basic.normality` is required HERE, at the node before the fork, because testing the
        # distribution is what makes the method choice at A_capability a judgement rather than a
        # coin toss -- and because a normality test is defensible on any continuous batch, so
        # requiring it discloses nothing about which capability index is right.
        GraphNode("M_stability", "measure",
                  methods=("control_chart.imr", "basic.normality"),
                  produces=("imr.outOfControl", "normality.pValue"),
                  label="Run stability (individuals chart)"),
        GraphNode("A_capability", "analyze", produces=("cap.ppk",),
                  label="Process capability (method chosen from the distribution)"),
        GraphNode("A_special_cause", "analyze", methods=("control_chart.imr",),
                  label="Special-cause investigation (process not in control; a capability index would be meaningless)"),
        GraphNode("C_control", "control", label="Control"),
    ),
    edges=(GuardedEdge("D_scope", "M_stability"),
           GuardedEdge("M_stability", "A_capability", "imr.outOfControl == 0",
                       guard_fields=("imr.outOfControl",)),
           GuardedEdge("M_stability", "A_special_cause", is_default=True),
           GuardedEdge("A_capability", "C_control"),
           GuardedEdge("A_special_cause", "C_control")),
)

GATE_POLICY = (
    {"stage": "A_capability", "requires": "M_stability", "unlock_when": "imr.outOfControl == 0",
     "rule": "no capability study on a process that is not in control"},
    {"stage": "A_special_cause", "requires": "M_stability", "unlock_when": "imr.outOfControl > 0",
     "rule": "special-cause work only once the run is shown to be unstable"},
)
NODE_DATA = {"D_scope": "define", "M_stability": "process_run", "A_capability": "process_run",
             "A_special_cause": "process_run"}

#: TWO skewed seeds and TWO clean-normal ones, deliberately balanced. The earlier 3-to-1 split
#: handed a contestant that always reaches for the non-normal index a 75% hit rate on the one
#: variable this case grades; at 2-2 a fixed choice is right half the time, which is what a fair
#: binary verdict looks like. Measured on the scripted solver frozen to one seed's method: with
#: the 3-1 split it scored 1.000 on three of four seeds.
SHAPES = {0: "moderate-skew·trap", 1: "clean-normal·control", 2: "mild-skew·trap",
          3: "wide-normal·control", 4: "unstable·special-cause"}
#: which seeds are the normal controls (the rest are lognormal-skewed traps)
_NORMAL_SHAPES = (1, 3)
#: Seeds whose shape is NOT ``seed % 4`` -- see poc_project._EXTRA_SHAPES.
_EXTRA_SHAPES = (4,)


def _shape_for(seed: int) -> int:
    return seed if seed in _EXTRA_SHAPES else seed % 4


def _imr_ooc(data):
    n = len(data); c = sum(data) / n
    mrbar = sum(abs(data[i] - data[i - 1]) for i in range(1, n)) / (n - 1)
    ucl, lcl = c + 2.66 * mrbar, c - 2.66 * mrbar
    return sum(1 for x in data if x > ucl or x < lcl)


def _percentile_ppk(data):
    """Non-normal Ppk via the ISO/percentile method: (USL-LSL)/(P99.865-P0.135) and the one-sided
    minimum against the median — the correct index for skewed data."""
    xs = sorted(data)
    n = len(xs)

    def q(p):
        i = p * (n - 1)
        lo = int(math.floor(i)); hi = min(lo + 1, n - 1)
        return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)
    p00135, p50, p99865 = q(0.00135), q(0.5), q(0.99865)
    ppu = (_USL - p50) / (p99865 - p50)
    ppl = (p50 - _LSL) / (p50 - p00135)
    return min(ppu, ppl)


def generate(seed: int):
    shape = _shape_for(seed)
    rng = random.Random(seed * 1_000_003 + 20260709)
    n = 60
    for _ in range(300):
        if shape == 4:                                   # a shift part-way through the run
            data = [70.0 + 8.0 * max(-2.4, min(2.4, rng.gauss(0, 1))) for _ in range(n)]
            for i in range(n // 2, n):
                data[i] += 26.0
        elif shape in _NORMAL_SHAPES:                    # normal control
            spread = {1: 8.0, 3: 11.0}[shape]
            data = [70.0 + spread * max(-2.4, min(2.4, rng.gauss(0, 1))) for _ in range(n)]
        else:
            sigma = {0: 0.45, 2: 0.32}[shape]            # lognormal skew magnitude
            data = [48.0 + 14.0 * math.exp(sigma * rng.gauss(0, 1)) for _ in range(n)]
            data = [min(x, 99.0) for x in data]          # keep in spec-ish, stays in control
        pval = verifiers.normality({"data": data})["pValue"]
        ooc = _imr_ooc(data)
        if shape == 4:
            # No capability index is published here, by either convention: on an out-of-control
            # record the number would be arithmetic without meaning, which is the whole point of
            # the branch. `cap` is simply absent from the results.
            if ooc == 0:
                continue
            blocks = {"define": {"goal": "state where the characteristic stands against its "
                                         "accepted range", "lsl": _LSL, "usl": _USL},
                      "process_run": {"data": [round(x, 3) for x in data],
                                      "lsl": _LSL, "usl": _USL}}
            return blocks, {"imr": {"outOfControl": ooc},
                            "normality": {"pValue": round(pval, 4)},
                            "_shape": SHAPES[shape]}
        want_skew = shape not in _NORMAL_SHAPES
        if ooc == 0 and ((want_skew and pval < 0.05) or (not want_skew and pval >= 0.05)):
            if want_skew:
                ppk = round(_percentile_ppk(data), 4)
            else:
                ppk = round(verifiers.capability_normal({"data": data, "lsl": _LSL, "usl": _USL})["ppk"], 4)
            blocks = {"define": {"goal": "state where the characteristic stands against its "
                                         "accepted range", "lsl": _LSL, "usl": _USL},
                      "process_run": {"data": [round(x, 3) for x in data], "lsl": _LSL, "usl": _USL}}
            res = {"imr": {"outOfControl": ooc}, "normality": {"pValue": round(pval, 4)},
                   "cap": {"ppk": ppk}, "_shape": SHAPES[shape]}
            return blocks, res
    raise RuntimeError(f"capability_trap: could not realize shape {shape} for seed {seed}")


CASE = V2Case(
    # The old id and title -- "capability_trap", "method-selection trap" -- named the statistical
    # concept AND announced what the task was testing, in the one string the agent reads back out
    # of instruction.md. Both are now neutral; what forks here is stated only in the truth
    # package and in this module's docstring.
    case_id="adb_c29", title="Reporting where one critical characteristic stands",
    industry="discrete_manufacturing", y_type="continuous",
    graph=GRAPH, gate_policy=GATE_POLICY, generate=generate,
    # Seed 4 is the out-of-control seed: it exercises the ``M_stability`` fork, whose two
    # guarded edges used to lead to the same node and could therefore never differ.
    seeds=(0, 1, 2, 3, 4),
    shapes={s: SHAPES[_shape_for(s)] for s in (0, 1, 2, 3, 4)}, node_data=NODE_DATA,
    fault_targets=(), budget={"max_turns": 16}, discriminator="method",
    # THE GRADED VARIABLE HERE IS THE METHOD, NOT THE PATH. Every seed walks the same route, so
    # `produces`/`methods` on A_capability cannot be a constant without handing over the answer:
    # the admissible index depends on whether the batch is normal. This clause is evaluated
    # against the ORACLE's results at build time, so the required method is data-conditioned in
    # exactly the way the route is in the other four cases.
    method_policy={
        "A_capability": (
            {"when": "normality.pValue >= 0.05", "methods": ("capability.normal",)},
            {"methods": ("capability.nonnormal",)},
        ),
    },
    context=(
        "We are the quality group at a components plant. One critical characteristic has an "
        "internally accepted range of 40 to 100, and the line has left a record of sixty "
        "consecutive pieces in the order they came off. The customer has asked us to state "
        "where this characteristic stands today and to show how we arrived at that figure. "
        "Do not assume the shape of this record; look at the data itself first."),
    goal=(
        "From the record the data steward can release, say whether the line has been steady "
        "over the run and where the characteristic stands against its accepted range today. "
        "Justify in your report why the figure you report is the right one for THIS data. "
        "Every number must come from a computation you ran on this task."),
    blocks_meta={
        "define": {"label": "Project charter and accepted range", "phase": "define",
                   "topics": ("charter", "accepted range", "customer request")},
        "process_run": {"label": "Consecutive piece record", "phase": "measure",
                        "topics": ("piece record", "off the line")},
    },
    field_map={
        "imr.outOfControl": _f.SRC_IMR_OOC,
        "normality.pValue": _f.SRC_NORMALITY,
        "cap.ppk": _f.SRC_PPK,
    },
    truth_fields=(
        {"field": "imr.outOfControl", "method_id": "control_chart.imr",
         "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "normality.pValue", "method_id": "basic.normality",
         "output": "pValue", "scale": 1.0, "tol": 0.01},
        # cap.ppk is NOT published as a truth on the skewed seeds: this case computes the ISO
        # percentile index and the reference solution fits a Weibull, which are different
        # statistics (1.058 vs 0.406 on the same batch). The entry below is emitted only when
        # the method_policy selects capability.normal, i.e. on the clean-normal control seed,
        # where the two conventions coincide.
        {"field": "cap.ppk", "method_id": "capability.normal",
         "output": "ppk", "scale": 1.0, "tol": 0.01},
    ),
)

if __name__ == "__main__":
    for s in CASE.seeds:
        _, r = generate(s)
        ppk = r.get("cap", {}).get("ppk")
        print(f"seed {s} [{r['_shape']:22s}] normality_p={r['normality']['pValue']:.4f} "
              f"ppk={ppk} ooc={r['imr']['outOfControl']} route={' → '.join(walk(GRAPH, r))}")
