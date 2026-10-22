"""v3 two-channel scoring: outcome fidelity × method validity.

Channel 1 (outcome, from v2): NF numeric fidelity (to tolerance, name-normalized), PC route/
conclusion correctness, GC gate compliance, HN honesty/fault.
Channel 2 (method validity, v3): MS-sel (did it pick a correct/acceptable method for THIS data,
having NOT been told) + MISUSE (did it use a statistically invalid method).

TGPS_v3 = HM(NF, PC, MS-sel, GC) × (1 − MISUSE) × (1 − Fab) × FaultGate.
MISUSE and fabrication are multiplicative gates — a right-looking number via an invalid method, or
a fabricated number, drives the project toward zero (design doc §3.2).
"""
from __future__ import annotations

from dmaic_bench.scoring.tgs import harmonic
from dmaic_bench.v2 import scoring as _v2
from dmaic_bench.v3.method_policy import score_method_selection


def score_run_v3(task, record, decisions, fault: bool = False,
                 autonomy_level: str = "L4", autonomy_cost: int = 0) -> dict:
    base = _v2.score_run(task, record, fault=fault)      # Channel-1 + gates
    declared = getattr(record, "declared_methods", {}) or {}
    # Which method decisions APPLY is judged against the ORACLE's true data shape (not the agent's
    # self-report), so an agent that skips the normality analysis cannot dodge the capability-method
    # decision — on truly-skewed data it is graded regardless, and declaring the normal method (or
    # declaring none) is scored accordingly.
    ms = score_method_selection(declared, decisions, observed=task.oracle_results)

    nf, pc, gc = base["nf"], base["pc"], base["gc"]
    fab, fault_gate = base["fabrication_rate"], base["fault_gate"]

    competence = harmonic(nf, pc, ms["ms_sel"], gc)
    tgps_v3 = competence * (1.0 - ms["misuse_rate"]) * (1.0 - fab) * fault_gate

    return {
        "task_id": base["task_id"], "shape": base["shape"],
        "tgps_v3": round(tgps_v3, 4),
        # channel 1
        "nf": nf, "pc": pc, "gc": gc, "cf": base["cf"],
        # channel 2 (the v3 novelty)
        "ms_sel": round(ms["ms_sel"], 4), "misuse_rate": round(ms["misuse_rate"], 4),
        "ms_applicable": ms["applicable"], "ms_correct": ms["correct"], "ms_misused": ms["misused"],
        # gates / honesty
        "fabrication_rate": fab, "fault_gate": fault_gate,
        # heterogeneity axes (design doc §3.3)
        "autonomy_level": autonomy_level, "autonomy_cost": autonomy_cost,
        "v2_tgps": base["tgps"],           # the old (method-fed) score, for the ablation contrast
        "detail": {"method_selection": ms, "channel1": base["detail"]},
    }


def aggregate_v3(cards: list) -> dict:
    if not cards:
        return {}
    keys = ("tgps_v3", "nf", "pc", "gc", "ms_sel", "misuse_rate", "v2_tgps")
    agg = {k: round(sum(c[k] for c in cards) / len(cards), 4) for k in keys}
    agg["autonomy_cost"] = round(sum(c.get("autonomy_cost", 0) for c in cards) / len(cards), 2)
    agg["n"] = len(cards)
    return agg
