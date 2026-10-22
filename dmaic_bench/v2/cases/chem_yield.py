"""chem_yield — a data-conditioned CONTINUOUS process-optimization DMAIC project (v2).

Domain: a chemical/process line optimizing batch YIELD (%). ONE decision graph; `seed % 4` drives
the statistical shape so four seeds walk four distinct oracle-correct routes. The ANALYZE→IMPROVE
fork is DOE-driven: a screening factorial's factor effect is tested and only a SIGNIFICANT effect
justifies proceeding to full DOE + RSM optimization; a non-significant screen sends the project
back to re-examine the measurement system / root cause instead of chasing noise.

Four shapes:

  shape 0  normal · CAPABLE                → yield already meets the Ppk target → monitor (Control);
                                             no need to run a costly DOE at all.
  shape 1  normal · incapable · SIGNIFICANT screening factor
                                           → capability low → screen factors (factorial), the factor
                                             effect is real (model p < 0.05) → full DOE → RSM
                                             optimization → confirm → Control.
  shape 2  normal · incapable · NON-significant screening factor
                                           → capability low, but the screened factor does NOT explain
                                             the variation (model p >= 0.05) → do NOT chase a DOE on
                                             noise; return to re-examine measurement / root cause.
  shape 3  NON-normal yield                → the Ppk/normal-capability route is invalid; route to a
                                             non-normal capability assessment before any improve
                                             decision (Montgomery ISQC 6e §8.3).
  shape 4  ASSAY UNACCEPTABLE              → %GRR above the 30% acceptance limit. Every downstream
                                             comparison is void (AIAG MSA-4 §II-B); correct the
                                             assay and re-study it before concluding anything
                                             about the line. The project stops at the gauge.
  shape 5  UNSTABLE (special cause)        → an out-of-control charge sequence: capability is not
                                             defined on it (Montgomery ISQC 6e §8.2) and neither
                                             is a screening conclusion drawn against it. The
                                             correct move is special-cause investigation.

WHY SHAPES 4 AND 5 NEEDED NEW NODES. Both of this project's prerequisite gates rejected into a
SELF-LOOP (``M_msa -> M_msa``, ``M_stability -> M_stability``). ``walk`` is cycle-guarded, so a
rejection terminated the walk ON the fork and ``branch_decisions`` -- which reads each branch
point's successor along the path -- never recorded the decision. Two of the six forks in this
corpus that no seed exercised were these. Each now rejects into a real node.

Every routing field in `oracle_results` is COMPUTED from the generated data by the real verifiers
(`basic.normality`, `capability.normal`, `regression.ols` on the screening design) —
generate-then-derive, contamination-proof.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[3])
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from dmaic_bench.core.graph import (DecisionGraph, GraphNode,  # noqa: E402
                                        GuardedEdge, walk)
from dmaic_bench.truth import verifiers  # noqa: E402
from dmaic_bench.v2.cases import _fixtures  # noqa: E402
from dmaic_bench.v2.cases import _fixtures as _f  # noqa: E402
from dmaic_bench.v2.models import V2Case  # noqa: E402

_LSL, _USL = 80.0, 100.0        # yield spec (percent)
_PPK_TARGET = 1.33

# --------------------------------------------------------------------------- the decision graph

PROJECT_GRAPH = DecisionGraph(
    entry="D_scope",
    nodes=(
        GraphNode("D_scope", "define", label="Scope: the yield problem and its target"),
        GraphNode("M_msa", "measure", methods=("msa.gage_rr_crossed",),
                  produces=("msa.pctSV",), label="Measurement-system analysis (crossed Gage R&R)"),
        GraphNode("M_stability", "measure", methods=("control_chart.imr",),
                  produces=("imr.outOfControl",), label="Run stability (individuals chart)"),
        GraphNode("M_msa_fix", "measure",
                  label="Correct the assay method and re-run the study (readings cannot support any downstream conclusion)"),
        GraphNode("A_special_cause", "analyze", methods=("control_chart.imr",),
                  label="Special-cause investigation (capability does not apply)"),
        GraphNode("A_route", "analyze", methods=("basic.normality",),
                  produces=("normality.pValue",), label="Capability route (distribution check)"),
        GraphNode("A_cap_normal", "analyze", methods=("capability.normal",),
                  produces=("cap.ppk",), label="Normal process capability"),
        GraphNode("A_cap_nonnormal", "analyze", methods=("capability.nonnormal",),
                  produces=("cap.ppk",), label="Non-normal process capability"),
        GraphNode("A_screen", "analyze", methods=("regression.ols",),
                  produces=("screen.modelPValue",), label="Factor screening (screening design)"),
        GraphNode("A_remeasure", "analyze", methods=(),
                  label="Re-examine the measurement system and root cause (screening found no significant factor)"),
        GraphNode("I_doe", "improve", methods=("doe.factorial_analysis",),
                  label="Full-factorial design"),
        GraphNode("I_rsm", "improve", methods=("doe.rsm_optimizer",),
                  label="Response-surface optimisation"),
        GraphNode("I_confirm", "improve", methods=("capability.normal",),
                  label="Improvement confirmation (yield re-assessed)"),
        GraphNode("C_control", "control", methods=("control_chart.imr",), label="Control plan"),
    ),
    edges=(
        GuardedEdge("D_scope", "M_msa"),
        # MSA gate: optimization is meaningless if the gauge can't discriminate.
        GuardedEdge("M_msa", "M_stability", "msa.pctSV <= 0.30",
                    guard_fields=("msa.pctSV",)),
        GuardedEdge("M_msa", "M_msa_fix", is_default=True),
        # Stability gate: an out-of-control process cannot be assessed for capability.
        GuardedEdge("M_stability", "A_route", "imr.outOfControl == 0",
                    guard_fields=("imr.outOfControl",)),
        GuardedEdge("M_stability", "A_special_cause", is_default=True),
        # Normality routes the capability method.
        GuardedEdge("A_route", "A_cap_normal", "normality.pValue >= 0.05",
                    guard_fields=("normality.pValue",)),
        GuardedEdge("A_route", "A_cap_nonnormal", is_default=True),
        # Capability gate: capable → monitor; incapable → screen factors.
        GuardedEdge("A_cap_normal", "C_control", "cap.ppk >= 1.33", guard_fields=("cap.ppk",)),
        GuardedEdge("A_cap_normal", "A_screen", is_default=True),
        GuardedEdge("A_cap_nonnormal", "A_screen"),
        # DOE-driven fork: significant screening factor → full DOE→RSM; else re-examine.
        GuardedEdge("A_screen", "I_doe", "screen.modelPValue < 0.05",
                    guard_fields=("screen.modelPValue",)),
        GuardedEdge("A_screen", "A_remeasure", is_default=True),
        GuardedEdge("I_doe", "I_rsm"),
        GuardedEdge("I_rsm", "I_confirm"),
        GuardedEdge("I_confirm", "C_control"),
        GuardedEdge("A_remeasure", "C_control"),
        GuardedEdge("A_special_cause", "C_control"),
    ),
)

GATE_POLICY = (
    {"stage": "M_stability", "requires": "M_msa", "unlock_when": "msa.pctSV <= 0.30",
     "rule": "the measurement system must be judged acceptable before stability or capability"},
    {"stage": "M_msa_fix", "requires": "M_msa", "unlock_when": "msa.pctSV > 0.30",
     "rule": "assay remediation only once the measurement system has been judged unusable"},
    {"stage": "A_route", "requires": "M_stability", "unlock_when": "imr.outOfControl == 0",
     "rule": "capability is not valid until the process is shown to be in control (Montgomery ISQC 6e 8.2)"},
    {"stage": "A_special_cause", "requires": "M_stability", "unlock_when": "imr.outOfControl > 0",
     "rule": "special-cause work only once the run is shown to be unstable"},
    {"stage": "I_doe", "requires": "A_screen", "unlock_when": "screen.modelPValue < 0.05",
     "rule": "no full-factorial design until screening has shown a significant factor (do not optimise noise)"},
    {"stage": "A_remeasure", "requires": "A_screen", "unlock_when": "screen.modelPValue >= 0.05",
     "rule": "with no significant factor screened, re-examine the measurement system and root cause rather than starting a design"},
    {"stage": "I_rsm", "requires": "I_doe", "rule": "response-surface optimisation only after the factorial has confirmed the factors"},
)

NODE_DATA = {
    "D_scope": "define", "M_msa": "msa",
    "M_stability": "process_run", "A_route": "process_run",
    "A_cap_normal": "process_run", "A_cap_nonnormal": "process_run",
    "A_special_cause": "process_run",
    "A_screen": "screening_doe", "A_remeasure": "screening_doe",
    # NOTE the absence of I_confirm / I_doe / I_rsm / C_control. They are real obligations on the
    # route, but this project ships no POST-improvement batch, so "confirm the yield recovered"
    # has nothing to compute against -- it used to be mapped onto `process_run`, i.e. the
    # baseline it is supposed to be compared with, which makes the confirmation vacuous and (in
    # a Harbor build) makes the baseline capability method look like it was run twice.
}


# --------------------------------------------------------------------------- inline statistics

def _imr_out_of_control(data) -> int:
    """Individuals I-MR: count points beyond 3-sigma limits (moving-range estimate of sigma).

    UCL/LCL = xbar ± 2.66 * MRbar (2.66 = 3 / d2 for n=2 moving ranges). Same convention as
    poc_project._imr_out_of_control (Montgomery ISQC 6e §6.4).
    """
    n = len(data)
    center = sum(data) / n
    mrbar = sum(abs(data[i] - data[i - 1]) for i in range(1, n)) / (n - 1)
    ucl, lcl = center + 2.66 * mrbar, center - 2.66 * mrbar
    return sum(1 for x in data if x > ucl or x < lcl)


def _series_stats(data, screen_x, screen_y, msa_stats):
    """Compute the routing fields the graph reads, via the real verifiers (generate-then-derive).

    ``msa_stats`` is derived from the raw Gage R&R study this project hands out (see
    ``_fixtures.gage_rr_study``); it used to be the literal 0.18 asserted here.
    """
    payload = {"data": list(data), "lsl": _LSL, "usl": _USL}
    normality = verifiers.normality(payload)                      # {"pValue"}
    cap = verifiers.capability_normal(payload)                    # {"pp","ppk"}
    screen = verifiers.ols({"x": list(screen_x), "y": list(screen_y)})   # {"modelPValue",...}
    return {
        "msa": dict(msa_stats),
        "imr": {"outOfControl": _imr_out_of_control(data)},
        "normality": {"pValue": round(normality["pValue"], 4)},
        "cap": {"pp": round(cap["pp"], 4), "ppk": round(cap["ppk"], 4)},
        "screen": {"modelPValue": round(screen["modelPValue"], 5),
                   "rSquaredPct": round(screen["rSquaredPct"], 3)},
    }


def _draw_normal(rng, mu, sigma, n, cut=2.4):
    return [mu + sigma * g for g in
            (max(-cut, min(cut, rng.gauss(0, 1))) for _ in range(n))]


def _draw_skewed(rng, n):
    # Right-skewed yield floored inside spec so it stays in-control on I-MR (fork is normality).
    raw = [rng.expovariate(1.0) for _ in range(n)]
    return [83.0 + min(v, 3.5) * 2.0 for v in raw]


def _draw_screen(rng, effect):
    """A 2-level screening design (coded -1/+1) with a controllable factor effect.

    y = 90 + effect * x + noise. A large `effect` relative to noise makes the OLS model p-value
    tiny (significant factor); effect≈0 leaves only noise (non-significant).
    """
    xs = [-1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1]      # replicated 2-level, 12 runs
    ys = [90.0 + effect * x + rng.gauss(0, 1.4) for x in xs]
    return xs, ys


SHAPES = {0: "normal·capable",
          1: "normal·incapable·significant-factor",
          2: "normal·incapable·nonsignificant-factor",
          3: "non-normal",
          4: "gauge-unacceptable",
          5: "unstable·special-cause"}

#: Seeds whose shape is NOT ``seed % 4`` -- see poc_project._EXTRA_SHAPES.
_EXTRA_SHAPES = (4, 5)


def _shape_for(seed: int) -> int:
    return seed if seed in _EXTRA_SHAPES else seed % 4


def generate(seed: int):
    """Return (blocks, oracle_results). Seed's shape drives the data so the oracle route differs."""
    shape = _shape_for(seed)
    rng = random.Random(seed * 1_000_003 + 20260709)
    n = 30
    if shape == 4:
        # An assay that cannot discriminate: repeatability/reproducibility swamp the batch-to-
        # batch spread, so %StudyVariation lands above 30% under BOTH admissible conventions.
        msa_block, msa_stats = _fixtures.gage_rr_study(
            random.Random(seed * 7_919 + 20260709), center=90.0, tolerance=20.0,
            repeat_sd=1.30, operator_sd=0.70,
            window=_fixtures.GRR_FAIL_WINDOW, min_ndc=0,
            pooled_window=_fixtures.GRR_FAIL_POOLED_WINDOW)
    else:
        msa_block, msa_stats = _fixtures.gage_rr_study(
            random.Random(seed * 7_919 + 20260709), center=90.0, tolerance=20.0)

    for _ in range(400):
        if shape == 0:                                   # tight, centered → capable
            data = _draw_normal(rng, 90.0, 1.9, n)
            screen_x, screen_y = _draw_screen(rng, 4.0)  # (unused route, but real data)
        elif shape == 1:                                 # wide/off-center → incapable, real factor
            data = _draw_normal(rng, 87.0, 3.4, n)
            screen_x, screen_y = _draw_screen(rng, 4.0)  # strong effect → significant
        elif shape == 2:                                 # incapable, but screen finds nothing
            data = _draw_normal(rng, 87.0, 3.4, n)
            screen_x, screen_y = _draw_screen(rng, 0.0)  # no effect → non-significant
        elif shape == 3:                                 # skewed → non-normal
            data = _draw_skewed(rng, n)
            screen_x, screen_y = _draw_screen(rng, 4.0)
        elif shape == 4:                                 # assay unusable; the run is ordinary
            data = _draw_normal(rng, 90.0, 1.9, n)
            screen_x, screen_y = _draw_screen(rng, 4.0)
        else:                                            # a charge sequence with a special cause
            data = _draw_normal(rng, 90.0, 1.9, n)
            data[n // 2] = 90.0 - 6.0 * 1.9              # a clear out-of-control excursion
            screen_x, screen_y = _draw_screen(rng, 4.0)

        res = _series_stats(data, screen_x, screen_y, msa_stats)
        ppk = res["cap"]["ppk"]
        pval = res["normality"]["pValue"]
        ooc = res["imr"]["outOfControl"]
        mp = res["screen"]["modelPValue"]
        ok = {
            0: ooc == 0 and pval >= 0.05 and ppk >= _PPK_TARGET,
            1: ooc == 0 and pval >= 0.05 and ppk < _PPK_TARGET and mp < 0.05,
            2: ooc == 0 and pval >= 0.05 and ppk < _PPK_TARGET and mp >= 0.05,
            3: ooc == 0 and pval < 0.05,
            # the assay is the only thing wrong: an ordinary, in-control charge record
            4: (res["msa"]["pctSV"] > 0.30 and res["msa"]["pctSVPooled"] > 0.30
                and ooc == 0 and pval >= 0.05),
            # the run is the only thing wrong: the assay is acceptable and the excursion is real
            5: res["msa"]["pctSV"] <= 0.30 and ooc > 0,
        }[shape]
        if ok:
            blocks = {
                "define": {"goal": "bring batch yield inside its accepted range and hold it "
                                   "there", "lsl": _LSL, "usl": _USL},
                "msa": dict(msa_block),
                "process_run": {"data": [round(x, 4) for x in data], "lsl": _LSL, "usl": _USL},
                "screening_doe": {"x": list(screen_x), "y": [round(y, 4) for y in screen_y]},
            }
            res["_shape"] = SHAPES[shape]
            return blocks, res

    raise RuntimeError(f"generator could not realize shape {shape} for seed {seed}")


def oracle_route(seed: int) -> list:
    _, res = generate(seed)
    return walk(PROJECT_GRAPH, res)


CASE = V2Case(
    case_id="adb_c27",
    title="Lifting batch yield on a process line, and knowing when not to experiment",
    industry="process_industry",
    y_type="continuous",
    graph=PROJECT_GRAPH,
    gate_policy=GATE_POLICY,
    generate=generate,
    # Seeds 4 and 5 exercise the two prerequisite forks -- gauge rejection and stability
    # rejection -- that no seed reached while both rejected into self-loops.
    seeds=(0, 1, 2, 3, 4, 5),
    shapes={s: SHAPES[_shape_for(s)] for s in (0, 1, 2, 3, 4, 5)},
    node_data=NODE_DATA,
    fault_targets=(("M_msa", "msa.gage_rr_crossed",
                    "the Gage R&R raw data for this batch was checked and is genuinely not on file"),),
    budget={"max_turns": 24},
    context=(
        "We are the process engineering group at a fine-chemicals plant. Yield on one "
        "intermediate has been low and swings from batch to batch; the internally accepted "
        "range is 80 to 100 percent. Production has recorded every batch's yield in charge "
        "order, and the archive holds the laboratory's study in which the same samples were "
        "assayed repeatedly by several analysts. Separately, an earlier run of charges was "
        "made deliberately at a high and a low setting, with the resulting yields recorded. "
        "Continuing to run charges is expensive, so we need to know whether the setting is "
        "worth pursuing at all before we commit to more of them."),
    goal=(
        "Work through the batches the data steward can release and say where this project "
        "stands: whether the assay readings can be relied on, how the line has behaved over "
        "the run, where yield sits against its accepted range today, and whether the evidence "
        "justifies spending more charges on the setting or sends us back to look elsewhere. "
        "Every number in your report must come from a computation you ran on this task."),
    blocks_meta={
        "define": {"label": "Project charter and yield requirement", "phase": "define",
                   "topics": ("charter", "yield requirement", "improvement target")},
        "msa": {"label": "Repeat assays of the same samples", "phase": "measure",
                "topics": ("repeat assays", "analyst study")},
        "process_run": {"label": "Per-batch yield record", "phase": "measure",
                        "topics": ("batch yield", "charge order")},
        "screening_doe": {"label": "Charges run at a high and a low setting", "phase": "analyze",
                          "topics": ("setting trial", "high and low")},
    },
    field_map={
        "msa.pctSV": _f.SRC_GRR_PCT, "msa.ndc": _f.SRC_GRR_NDC,
        "imr.outOfControl": _f.SRC_IMR_OOC, "normality.pValue": _f.SRC_NORMALITY,
        "cap.ppk": _f.SRC_PPK, "cap.pp": _f.SRC_PP,
        "screen.modelPValue": ({"method_id": "regression.ols", "output": "modelPValue",
                                "scale": 1.0},),
        "screen.rSquaredPct": ({"method_id": "regression.ols", "output": "rSquaredPct",
                                "scale": 1.0},),
    },
    truth_fields=(
        _f.TRUTH_GRR_PCT,
        {"field": "imr.outOfControl", "method_id": "control_chart.imr",
         "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "normality.pValue", "method_id": "basic.normality",
         "output": "pValue", "scale": 1.0, "tol": 0.01},
        {"field": "cap.ppk", "method_id": "capability.normal",
         "output": "ppk", "scale": 1.0, "tol": 0.01},
        {"field": "cap.pp", "method_id": "capability.normal",
         "output": "pp", "scale": 1.0, "tol": 0.01},
        {"field": "screen.modelPValue", "method_id": "regression.ols",
         "output": "modelPValue", "scale": 1.0, "tol": 0.002},
        {"field": "screen.rSquaredPct", "method_id": "regression.ols",
         "output": "rSquaredPct", "scale": 1.0, "tol": 0.5},
    ),
)


if __name__ == "__main__":
    for s in CASE.seeds:
        _, res = generate(s)
        print(f"seed {s} [{res['_shape']:38s}] ppk={res['cap']['ppk']:.2f} "
              f"p={res['normality']['pValue']:.3f} ooc={res['imr']['outOfControl']} "
              f"screenP={res['screen']['modelPValue']:.4f}  "
              f"route: {' → '.join(walk(PROJECT_GRAPH, res))}")
