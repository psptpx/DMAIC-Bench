"""PoC data-conditioned DMAIC project: injection-molding part dimension.

This is the concrete proof that the v2 design is real, not vaporware. ONE decision graph; the
seed drives the *statistical shape* of the generated run-order data so that different seeds walk
different oracle-correct routes — the property v1 structurally cannot express (v1 freezes the
branch at authoring time and forces the data to match it).

Four shapes (`seed % 4`), each a genuinely different correct DMAIC trajectory:

  shape 0  stable · normal · capable      → assess capability, it's fine, go straight to Control
  shape 1  stable · normal · INcapable    → capability low → root-cause → DOE → confirm → Control
  shape 2  stable · NON-normal            → non-normal capability route → root-cause → … → Control
  shape 3  UNSTABLE (special cause)       → capability is INVALID on an out-of-control process;
                                            the correct move is special-cause investigation, NOT
                                            computing Cpk (Montgomery ISQC 6e §8.2). Data forks the
                                            project away from capability entirely.
  shape 4  GAUGE UNACCEPTABLE             → %GRR above the acceptance limit VOIDS every downstream
                                            comparison (AIAG MSA-4 §II-B: >30% is unacceptable).
                                            The correct move is to correct the measurement system
                                            and re-study it; nothing about the process may be
                                            concluded from readings this coarse. The project stops
                                            at the gauge.

WHY SHAPE 4 NEEDED A NEW NODE. The gauge-rejection branch used to be a SELF-LOOP,
``M_msa -> M_msa``. ``walk`` is cycle-guarded, so a failing gauge terminated the walk AT the fork
and ``branch_decisions`` -- which reads the successor of each branch point on the path -- dropped
the decision point entirely; ``harbor_truth.branch_evidence`` excludes the self-loop for the same
reason ("re-running the gauge study is byte-identical in a trace to doing it right the first
time"). So the fork could not fork and could not be scored, whatever the data did. The
remediation branch is now a real node with no batch of its own: the finding IS that the project
stops here.

Every routing field in `oracle_results` is COMPUTED from the generated data by the real verifiers
(truth/verifiers.py) — generate-then-derive, contamination-proof. The graph guards then read those
computed values, so the correct route is a true function of the data.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2])
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.graph import (DecisionGraph, GraphNode, GuardedEdge,  # noqa: E402
                                        walk)
from dmaic_bench.truth import verifiers  # noqa: E402
from dmaic_bench.v2.cases import _fixtures  # noqa: E402

_LSL, _USL = 12.0, 28.0

# --------------------------------------------------------------------------- the decision graph

PROJECT_GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define", label="Scope: the problem and its target"),
        GraphNode("M_msa", "measure", methods=("msa.gage_rr_crossed",),
                  produces=("msa.pctSV",), label="Measurement-system analysis (crossed Gage R&R)"),
        GraphNode("M_stability", "measure", methods=("control_chart.imr",),
                  produces=("imr.outOfControl",), label="Run stability (individuals chart)"),
        GraphNode("A_route", "analyze", methods=("basic.normality",),
                  produces=("normality.pValue",), label="Capability route (distribution check)"),
        GraphNode("A_cap_normal", "analyze", methods=("capability.normal",),
                  produces=("cap.ppk",), label="Normal process capability"),
        GraphNode("A_cap_nonnormal", "analyze", methods=("capability.nonnormal",),
                  produces=("cap.ppk",), label="Non-normal process capability"),
        GraphNode("M_msa_fix", "measure",
                  label="Correct the gauge and re-run the study (readings cannot support any downstream conclusion)"),
        GraphNode("A_special_cause", "analyze", methods=("control_chart.imr",),
                  label="Special-cause investigation (capability does not apply)"),
        GraphNode("A_root_cause", "analyze", methods=("anova.oneway", "regression.ols"),
                  label="Root-cause analysis"),
        GraphNode("I_doe", "improve", methods=("doe.factorial_analysis",), label="Improve (factorial design)"),
        GraphNode("I_confirm", "improve", methods=("capability.normal",), label="Improvement confirmation"),
        GraphNode("C_control", "control", methods=("control_chart.imr",), label="Control plan"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_msa"),
        # MSA gate: capability/analysis is meaningless if the gauge can't discriminate.
        GuardedEdge("M_msa", "M_stability", "msa.pctSV <= 0.30",
                    guard_fields=("msa.pctSV",)),
        # gauge fails → correct the measurement system; the process questions are unanswerable.
        GuardedEdge("M_msa", "M_msa_fix", is_default=True),
        # Stability gate: an out-of-control process cannot be assessed for capability.
        GuardedEdge("M_stability", "A_route", "imr.outOfControl == 0",
                    guard_fields=("imr.outOfControl",)),
        GuardedEdge("M_stability", "A_special_cause", is_default=True),
        # Normality routes the capability method.
        GuardedEdge("A_route", "A_cap_normal", "normality.pValue >= 0.05",
                    guard_fields=("normality.pValue",)),
        GuardedEdge("A_route", "A_cap_nonnormal", is_default=True),
        # Capability gate: capable → monitor; incapable → improve.
        GuardedEdge("A_cap_normal", "C_control", "cap.ppk >= 1.33", guard_fields=("cap.ppk",)),
        GuardedEdge("A_cap_normal", "A_root_cause", is_default=True),
        GuardedEdge("A_cap_nonnormal", "A_root_cause"),
        GuardedEdge("A_special_cause", "C_control"),
        GuardedEdge("A_root_cause", "I_doe"),
        GuardedEdge("I_doe", "I_confirm"),
        GuardedEdge("I_confirm", "C_control"),
    ),
)

# The methodology gates the environment must enforce. `requires` = the predecessor stage that
# must be accepted first; `unlock_when` (optional) = a guard over the agent's ACCEPTED results
# that must hold for the stage to unlock — this is what makes gating *conclusion-dependent*
# (declare "unstable" and the capability route stays locked; only special-cause unlocks).
GATE_POLICY = (
    {"stage": "M_stability", "requires": "M_msa", "unlock_when": "msa.pctSV <= 0.30",
     "rule": "the gauge must be judged acceptable before stability or capability"},
    {"stage": "M_msa_fix", "requires": "M_msa", "unlock_when": "msa.pctSV > 0.30",
     "rule": "remediation only once the gauge has been judged unusable"},
    {"stage": "A_route", "requires": "M_stability", "unlock_when": "imr.outOfControl == 0",
     "rule": "capability is not valid until the process is shown to be in control (Montgomery ISQC 6e 8.2)"},
    # The capability COMPUTATION nodes are gated too, not just the router — an out-of-control
    # process cannot be assessed for capability by any route.
    {"stage": "A_cap_normal", "requires": "M_stability", "unlock_when": "imr.outOfControl == 0",
     "rule": "the process is not in control, so a capability index would be meaningless"},
    {"stage": "A_cap_nonnormal", "requires": "M_stability", "unlock_when": "imr.outOfControl == 0",
     "rule": "the process is not in control, so a capability index would be meaningless"},
    {"stage": "A_special_cause", "requires": "M_stability", "unlock_when": "imr.outOfControl > 0",
     "rule": "special-cause work only once the run is shown to be unstable"},
    {"stage": "I_doe", "requires": "A_root_cause", "rule": "no improvement or design work until a root cause is confirmed"},
)

# Which staged data block each graph node consumes (what the steward hands out on arrival).
NODE_DATA = {
    "D_scope": "define", "M_msa": "msa",
    "M_stability": "process_run", "A_route": "process_run",
    "A_cap_normal": "process_run", "A_cap_nonnormal": "process_run",
    "A_special_cause": "process_run",
}


# --------------------------------------------------------------------------- data generation

def _imr_out_of_control(data) -> int:
    n = len(data)
    center = sum(data) / n
    mrbar = sum(abs(data[i] - data[i - 1]) for i in range(1, n)) / (n - 1)
    ucl, lcl = center + 2.66 * mrbar, center - 2.66 * mrbar
    return sum(1 for x in data if x > ucl or x < lcl)


def _series_stats(data, msa_stats):
    """Compute the routing fields the graph reads, via the real verifiers (generate-then-derive).

    ``msa_stats`` comes from :func:`_fixtures.gage_rr_study`, i.e. it too is COMPUTED from the
    raw study this project hands out -- it used to be the literal 0.15 typed here, which both
    made the gauge branch unfalsifiable and put the gate's answer in the agent's batch.
    """
    payload = {"data": list(data), "lsl": _LSL, "usl": _USL}
    normality = verifiers.normality(payload)          # {"pValue": adPValue}
    cap = verifiers.capability_normal(payload)         # {"pp","ppk"}
    return {
        "msa": dict(msa_stats),
        "imr": {"outOfControl": _imr_out_of_control(data)},
        "normality": {"pValue": round(normality["pValue"], 4)},
        "cap": {"pp": round(cap["pp"], 4), "ppk": round(cap["ppk"], 4)},
    }


def _draw_normal(rng, mu, sigma, n, cut=2.4):
    return [mu + sigma * g for g in
            (max(-cut, min(cut, rng.gauss(0, 1))) for _ in range(n))]


def _draw_skewed(rng, n):
    # Lognormal-ish, shifted into spec — strongly non-normal, but kept inside limits so it stays
    # in-control on I-MR (the fork we want is normality, not stability).
    raw = [rng.expovariate(1.0) for _ in range(n)]
    return [15.0 + min(v, 3.5) * 2.2 for v in raw]     # floor≈15, bounded, right-skewed


SHAPES = {0: "stable·normal·capable", 1: "stable·normal·incapable",
          2: "stable·non-normal", 3: "unstable·special-cause",
          4: "gauge-unacceptable"}

#: Seeds whose shape is NOT ``seed % 4``. Extending the map rather than widening the modulus is
#: what keeps seeds 0-3 byte-identical: ``4 % 4 == 0`` would have silently re-pointed seed 4 at
#: the capable shape and any later modulus change would move every existing seed at once.
_EXTRA_SHAPES = (4,)


def _shape_for(seed: int) -> int:
    return seed if seed in _EXTRA_SHAPES else seed % 4


def generate(seed: int):
    """Return (blocks, oracle_results). Seed's shape drives the data so the oracle route differs."""
    shape = _shape_for(seed)
    rng = random.Random(seed * 1_000_003 + 20260708)
    n = 30
    if shape == 4:
        # A gauge that cannot discriminate: repeatability and reproducibility are large against
        # the part-to-part spread, so %StudyVariation lands above the 30% acceptance limit under
        # BOTH admissible conventions. Nothing is asserted -- the verdict is computed below.
        msa_block, msa_stats = _fixtures.gage_rr_study(
            random.Random(seed * 7_919 + 20260708), center=20.0, tolerance=16.0,
            repeat_sd=1.30, operator_sd=0.70,
            window=_fixtures.GRR_FAIL_WINDOW, min_ndc=0,
            pooled_window=_fixtures.GRR_FAIL_POOLED_WINDOW)
    else:
        msa_block, msa_stats = _fixtures.gage_rr_study(
            random.Random(seed * 7_919 + 20260708), center=20.0, tolerance=16.0)

    for _ in range(200):                               # redraw until the intended shape verifies
        if shape == 0:                                 # tight, centered, normal → capable
            data = _draw_normal(rng, 20.0, 1.6, n)
        elif shape == 1:                               # wide/off-center normal → incapable
            data = _draw_normal(rng, 22.3, 3.2, n)
        elif shape == 2:                               # skewed → non-normal
            data = _draw_skewed(rng, n)
        elif shape == 3:                               # normal + one injected special cause
            data = _draw_normal(rng, 20.0, 1.6, n)
            data[n // 2] = 20.0 + 6.0 * 1.6            # a clear out-of-control spike
        else:                                          # gauge unacceptable: the run is ordinary
            # The PROCESS record is deliberately unremarkable. What makes this seed's route
            # correct is the gauge, and a run that also happened to be unstable would let a
            # contestant reach the right stopping point for the wrong reason.
            data = _draw_normal(rng, 20.0, 1.6, n)

        res = _series_stats(data, msa_stats)
        ppk, pval, ooc = res["cap"]["ppk"], res["normality"]["pValue"], res["imr"]["outOfControl"]
        ok = {
            0: ooc == 0 and pval >= 0.05 and ppk >= 1.33,
            1: ooc == 0 and pval >= 0.05 and ppk < 1.33,
            2: ooc == 0 and pval < 0.05,
            3: ooc > 0,
            # the gauge is the only thing wrong: an ordinary, in-control, normal process record
            4: (res["msa"]["pctSV"] > 0.30 and res["msa"]["pctSVPooled"] > 0.30
                and ooc == 0 and pval >= 0.05),
        }[shape]
        if ok:
            blocks = {
                # NOTE: no index name and no target figure. This dict is blocks.json, which is
                # read inside the AGENT container, so naming the index here would hand over the
                # method and the threshold the fork turns on.
                "define": {"goal": "bring the critical dimension inside its accepted range and "
                                   "hold it there", "lsl": _LSL, "usl": _USL},
                "msa": dict(msa_block),
                "process_run": {"data": [round(x, 4) for x in data], "lsl": _LSL, "usl": _USL},
            }
            res["_shape"] = SHAPES[shape]
            return blocks, res

    raise RuntimeError(f"generator could not realize shape {shape} for seed {seed}")


def oracle_route(seed: int) -> list:
    _, res = generate(seed)
    return walk(PROJECT_GRAPH, res)


if __name__ == "__main__":
    for s in (0, 1, 2, 3, 4):
        blocks, res = generate(s)
        print(f"seed {s} [{res['_shape']:24s}] grr={res['msa']['pctSV']:.3f} "
              f"ppk={res['cap']['ppk']:.2f} "
              f"p={res['normality']['pValue']:.3f} ooc={res['imr']['outOfControl']}  "
              f"route: {' → '.join(walk(PROJECT_GRAPH, res))}")
